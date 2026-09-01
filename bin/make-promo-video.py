#!/usr/bin/env python3
"""Generate promo videos per Ikat theme — ffmpeg fallback with PIL frame rendering.

    ./bin/make-promo-video.py --list
    ./bin/make-promo-video.py --theme butter -o dist/promo-butter.mp4
    ./bin/make-promo-video.py --all --format vertical -o dist/
    ./bin/make-promo-video.py --theme forest-lace --preview -o /tmp/preview.png
    ./bin/make-promo-video.py --theme butter --no-encode --frames-dir /tmp/frames

Why PIL + ffmpeg instead of Remotion: the VPS ffmpeg build has no drawtext, and
there is no Node/Remotion project in this repo yet. This script is zero-dependency
beyond Pillow + ffmpeg (both already on the box). The second-brain Remotion notes
at Resources/Learning-DevOps/Remotion - Programmatic Video with React.md describe
the upgrade path — when a React preview exists, swap the PIL renderer for a
Remotion composition and keep the same CLI surface (see docs/MARKETING.md).

Video structure (default 6s @ 30fps, 1080x1920 vertical):
  0.0-1.0s  Title card — theme name fades + scales in
  1.0-3.0s  Palette + blurb — colour swatches slide in
  3.0-5.0s  Mock invitation card — uses theme bg/surface/ink/accent
  5.0-6.0s  CTA — "Ikat — undangan yang kebuka"

All text is rendered with system fonts (DejaVu Sans). Theme display fonts from
Google Fonts are not bundled — the video uses colour + shape to carry identity,
which is enough for a 6-second promo and keeps the tool offline-capable.
"""

from __future__ import annotations

import argparse
import json
import math
import os
import shutil
import subprocess
import sys
import tempfile

try:
    from PIL import Image, ImageDraw, ImageFont
except ImportError:
    sys.exit("Pillow is required: pip install Pillow  (or uv pip install Pillow)")

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SPEC = os.path.join(ROOT, "themes", "themes.json")

# ------------------------------------------------------------------ presets

PRESETS = {
    "vertical":   (1080, 1920),   # reels / story / TikTok
    "horizontal": (1920, 1080),   # YouTube / OG video
    "square":     (1080, 1080),   # feed post
}

FPS_DEFAULT = 30
DURATION_DEFAULT = 6.0  # seconds

# Scene boundaries as fractions of total duration (must sum to 1.0)
SCENES = [
    ("title",   0.17),   # ~1s
    ("palette", 0.33),   # ~2s
    ("card",    0.33),   # ~2s
    ("cta",     0.17),   # ~1s
]

# ------------------------------------------------------------------ helpers

def hex_to_rgb(h: str) -> tuple[int, int, int]:
    h = h.strip().lstrip("#")
    if len(h) == 3:
        h = "".join(c * 2 for c in h)
    # ignore alpha in rgba() strings — caller should pass hex only
    if len(h) > 6:
        h = h[:6]
    return int(h[0:2], 16), int(h[2:4], 16), int(h[4:6], 16)

def rgba_to_rgb(s: str, fallback: str = "#ffffff") -> tuple[int, int, int]:
    """Parse 'rgba(r,g,b,a)' or hex; returns RGB tuple."""
    s = s.strip()
    if s.startswith("rgba") or s.startswith("rgb"):
        import re
        nums = re.findall(r"[\d.]+", s)
        if len(nums) >= 3:
            return int(float(nums[0])), int(float(nums[1])), int(float(nums[2]))
    if s.startswith("#"):
        return hex_to_rgb(s)
    return hex_to_rgb(fallback)

def lerp(a: float, b: float, t: float) -> float:
    return a + (b - a) * t

def ease_out_cubic(t: float) -> float:
    t = max(0.0, min(1.0, t))
    return 1 - pow(1 - t, 3)

def ease_in_out(t: float) -> float:
    t = max(0.0, min(1.0, t))
    return 0.5 * (1 - math.cos(t * math.pi))

def clamp01(t: float) -> float:
    return max(0.0, min(1.0, t))

# ------------------------------------------------------------------ fonts

def load_font(size: int, bold: bool = False) -> ImageFont.FreeTypeFont:
    """Try DejaVu Sans (always on this VPS), fall back to default."""
    candidates = []
    if bold:
        candidates = [
            "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
            "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
        ]
    else:
        candidates = [
            "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
            "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
        ]
    for p in candidates:
        if os.path.exists(p):
            try:
                return ImageFont.truetype(p, size)
            except Exception:
                continue
    return ImageFont.load_default()

def text_size(draw: ImageDraw.ImageDraw, text: str, font: ImageFont.FreeTypeFont) -> tuple[int, int]:
    bbox = draw.textbbox((0, 0), text, font=font)
    return bbox[2] - bbox[0], bbox[3] - bbox[1]

def wrap_text(text: str, font: ImageFont.FreeTypeFont, max_width: int, draw: ImageDraw.ImageDraw) -> list[str]:
    words = text.split()
    lines: list[str] = []
    cur = ""
    for w in words:
        test = f"{cur} {w}".strip()
        tw, _ = text_size(draw, test, font)
        if tw <= max_width:
            cur = test
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines

# ------------------------------------------------------------------ drawing primitives

def draw_rounded_rect(draw: ImageDraw.ImageDraw, xy: tuple[int,int,int,int], radius: int, fill, outline=None, width: int = 1):
    try:
        draw.rounded_rectangle(xy, radius=radius, fill=fill, outline=outline, width=width)
    except Exception:
        draw.rectangle(xy, fill=fill, outline=outline, width=width)

def draw_palette_swatches(draw: ImageDraw.ImageDraw, colors: dict, x: int, y: int, sw: int, sh: int, gap: int, alpha: float = 1.0):
    """Draw 4 colour swatches (bg, surface, accent, highlight)."""
    keys = ["bg", "surface", "accent", "highlight"]
    for i, k in enumerate(keys):
        hexv = colors.get(k, "#cccccc")
        # handle rgba strings for line colours — skip those
        if isinstance(hexv, str) and hexv.startswith("rgba"):
            hexv = "#cccccc"
        try:
            rgb = hex_to_rgb(hexv) if isinstance(hexv, str) and hexv.startswith("#") else (204, 204, 204)
        except Exception:
            rgb = (204, 204, 204)
        # apply alpha by blending with white
        if alpha < 1.0:
            rgb = tuple(int(lerp(255, c, alpha)) for c in rgb)
        xi = x + i * (sw + gap)
        draw_rounded_rect(draw, (xi, y, xi + sw, y + sh), radius=10, fill=rgb, outline=(0, 0, 0, 30) if alpha >= 1 else None)

# ------------------------------------------------------------------ scene renderers

def render_frame(img: Image.Image, theme: dict, frame_idx: int, total_frames: int, fps: int, W: int, H: int) -> None:
    """Render one frame in-place onto img (RGB)."""
    draw = ImageDraw.Draw(img)
    colors = theme.get("colors", {})
    bg_hex = colors.get("bg", "#f3e0a8")
    bg2_hex = colors.get("bg2", bg_hex)
    surface_hex = colors.get("surface", "#ffffff")
    ink_hex = colors.get("ink", "#333333")
    accent_hex = colors.get("accent", "#c2a05c")
    highlight_hex = colors.get("highlight", "#c2405f")

    try:
        bg_rgb = hex_to_rgb(bg_hex)
        bg2_rgb = hex_to_rgb(bg2_hex)
        surface_rgb = hex_to_rgb(surface_hex)
        ink_rgb = hex_to_rgb(ink_hex)
        accent_rgb = hex_to_rgb(accent_hex)
        highlight_rgb = hex_to_rgb(highlight_hex)
    except Exception:
        bg_rgb, bg2_rgb, surface_rgb, ink_rgb, accent_rgb, highlight_rgb = (243, 224, 168), (230, 207, 144), (255, 250, 240), (61, 50, 24), (168, 121, 42), (217, 111, 74)

    t = frame_idx / max(1, total_frames - 1)  # 0..1
    # figure out which scene we're in
    cum = 0.0
    scene_name = "title"
    scene_t = 0.0  # 0..1 within scene
    for name, frac in SCENES:
        if t < cum + frac or name == SCENES[-1][0]:
            scene_name = name
            scene_t = clamp01((t - cum) / frac) if frac > 0 else 1.0
            break
        cum += frac

    # Background: vertical gradient bg -> bg2
    for y in range(H):
        f = y / max(1, H - 1)
        r = int(lerp(bg_rgb[0], bg2_rgb[0], f))
        g = int(lerp(bg_rgb[1], bg2_rgb[1], f))
        b = int(lerp(bg_rgb[2], bg2_rgb[2], f))
        draw.line([(0, y), (W, y)], fill=(r, g, b))

    # Subtle vignette — darken edges slightly
    # (cheap: semi-transparent overlay via blending is not available in RGB,
    #  so we just skip it; gradient is enough)

    name = theme.get("name", theme.get("slug", "Ikat"))
    blurb = theme.get("blurb", "")
    slug = theme.get("slug", "")

    # Common fonts sized relative to W
    is_vertical = H > W
    title_size = int(W * 0.085) if is_vertical else int(W * 0.055)
    body_size = int(W * 0.032) if is_vertical else int(W * 0.022)
    small_size = int(W * 0.024) if is_vertical else int(W * 0.016)
    font_title = load_font(title_size, bold=True)
    font_body = load_font(body_size, bold=False)
    font_small = load_font(small_size, bold=False)
    font_cta = load_font(int(W * 0.038) if is_vertical else int(W * 0.028), bold=True)

    pad = int(W * 0.06)

    if scene_name == "title":
        p = ease_out_cubic(scene_t)
        # Title scales from 0.92 -> 1.0 and fades in
        scale = lerp(0.92, 1.0, p)
        # We simulate scale by adjusting font size
        eff_title_size = max(8, int(title_size * scale))
        font_eff = load_font(eff_title_size, bold=True)
        # Opacity simulated by blending ink toward bg
        alpha = p
        ink_eff = tuple(int(lerp(bg_rgb[i], ink_rgb[i], alpha)) for i in range(3))

        # Centre vertically
        # Measure title
        tw, th = text_size(draw, name, font_eff)
        # Subtitle "Ikat — Tema"
        sub = f"Ikat  ·  {slug}"
        sw, sh = text_size(draw, sub, font_small)

        cx, cy = W // 2, H // 2
        # Title
        draw.text((cx - tw // 2, cy - th // 2 - 10), name, fill=ink_eff, font=font_eff)
        # Subtitle below, faded
        sub_alpha = clamp01((p - 0.4) / 0.6)
        sub_col = tuple(int(lerp(bg_rgb[i], ink_rgb[i], sub_alpha * 0.55)) for i in range(3))
        draw.text((cx - sw // 2, cy + th // 2 + 8), sub, fill=sub_col, font=font_small)

        # Accent line under title, grows with p
        line_w = int(lerp(0, W * 0.18, p))
        lx = cx - line_w // 2
        ly = cy + th // 2 + 36
        if line_w > 2:
            draw_rounded_rect(draw, (lx, ly, lx + line_w, ly + 3), radius=2, fill=accent_rgb)

    elif scene_name == "palette":
        p = ease_out_cubic(scene_t)
        # Blurb at top
        # Fade in blurb
        blurb_alpha = clamp01(p * 1.4)
        ink_eff = tuple(int(lerp(bg_rgb[i], ink_rgb[i], blurb_alpha)) for i in range(3))
        # Theme name small at top
        label = name.upper()
        # letter-spacing simulation: just draw normally
        f_label = load_font(small_size, bold=True)
        lw, lh = text_size(draw, label, f_label)
        draw.text(((W - lw) // 2, pad), label, fill=tuple(int(lerp(bg_rgb[i], ink_rgb[i], 0.5)) for i in range(3)), font=f_label)

        # Blurb wrapped, centred
        max_w = W - pad * 2
        lines = wrap_text(blurb, font_body, max_w, draw)
        y0 = pad + lh + 18
        for line in lines:
            tw, th = text_size(draw, line, font_body)
            draw.text(((W - tw) // 2, y0), line, fill=ink_eff, font=font_body)
            y0 += th + 6

        # Swatches — slide up from bottom
        sw_w, sw_h = int(W * 0.18), int(W * 0.18)
        gap = int(W * 0.03)
        total_sw_w = 4 * sw_w + 3 * gap
        sx = (W - total_sw_w) // 2
        # animate y: from below to position
        sy_target = y0 + 28
        sy = int(lerp(H + 40, sy_target, p))
        # also fade
        draw_palette_swatches(draw, colors, sx, sy, sw_w, sw_h, gap, alpha=p)

        # Labels under swatches
        labels = ["BG", "SURFACE", "ACCENT", "POP"]
        f_tiny = load_font(max(10, small_size - 2), bold=False)
        for i, lab in enumerate(labels):
            xi = sx + i * (sw_w + gap)
            tw, _ = text_size(draw, lab, f_tiny)
            # fade labels slightly after swatches
            la = clamp01((p - 0.5) / 0.5)
            col = tuple(int(lerp(bg_rgb[j], ink_rgb[j], la * 0.6)) for j in range(3))
            draw.text((xi + (sw_w - tw) // 2, sy + sw_h + 10), lab, fill=col, font=f_tiny)

    elif scene_name == "card":
        p = ease_out_cubic(scene_t)
        # Mock invitation card centred
        card_w = int(W * 0.72) if is_vertical else int(W * 0.42)
        card_h = int(card_w * 1.45)
        cx, cy = W // 2, H // 2
        # Card slides up slightly
        card_y = int(lerp(cy + 30, cy - card_h // 2, p))
        card_x = cx - card_w // 2

        # Shadow — simple offset rect
        shadow_off = 8
        draw_rounded_rect(draw, (card_x + shadow_off, card_y + shadow_off, card_x + card_w + shadow_off, card_y + card_h + shadow_off), radius=16, fill=(0, 0, 0, 40))

        # Card surface
        # Simulate shadow by drawing a slightly darker rect behind (RGB, so just offset)
        # Card itself
        draw_rounded_rect(draw, (card_x, card_y, card_x + card_w, card_y + card_h), radius=16, fill=surface_rgb, outline=accent_rgb, width=2)

        # Card content — all relative to card
        inner_pad = int(card_w * 0.08)
        # Eyebrow
        eyebrow = "The Wedding Of"
        f_eye = load_font(max(9, int(card_w * 0.038)), bold=False)
        ew, eh = text_size(draw, eyebrow, f_eye)
        # fade in content after card appears
        content_alpha = clamp01((p - 0.25) / 0.75)
        eye_col = tuple(int(lerp(surface_rgb[i], ink_rgb[i], content_alpha * 0.55)) for i in range(3))
        draw.text((card_x + (card_w - ew) // 2, card_y + inner_pad), eyebrow, fill=eye_col, font=f_eye)

        # Names — two lines
        f_names = load_font(int(card_w * 0.11), bold=True)
        # Use ink colour, slightly muted until fully in
        name_col = tuple(int(lerp(surface_rgb[i], ink_rgb[i], content_alpha)) for i in range(3))
        n1, n2 = "Dinda", "Rafi"
        # Ampersand
        f_amp = load_font(int(card_w * 0.09), bold=False)
        for idx, nm in enumerate([n1, "&", n2]):
            f = f_amp if nm == "&" else f_names
            tw, th = text_size(draw, nm, f)
            y = card_y + inner_pad + eh + 14 + idx * (th + 4)
            # centre
            draw.text((card_x + (card_w - tw) // 2, y), nm, fill=name_col, font=f)

        # Date line
        date_str = "24 September 2026"
        f_date = load_font(max(9, int(card_w * 0.042)), bold=False)
        dw, dh = text_size(draw, date_str, f_date)
        date_col = tuple(int(lerp(surface_rgb[i], accent_rgb[i], content_alpha)) for i in range(3))
        draw.text((card_x + (card_w - dw) // 2, card_y + card_h - inner_pad - dh - 28), date_str, fill=date_col, font=f_date)

        # Accent line above date
        lw = int(card_w * 0.22)
        lx = card_x + (card_w - lw) // 2
        ly = card_y + card_h - inner_pad - dh - 38
        if content_alpha > 0.3:
            draw_rounded_rect(draw, (lx, ly, lx + lw, ly + 2), radius=1, fill=accent_rgb)

        # Theme tag at bottom of screen, outside card
        tag = f"Tema {name}  ·  ikat"
        f_tag = load_font(small_size, bold=False)
        tw, th = text_size(draw, tag, f_tag)
        tag_col = tuple(int(lerp(bg_rgb[i], ink_rgb[i], 0.55)) for i in range(3))
        draw.text(((W - tw) // 2, H - pad - th), tag, fill=tag_col, font=f_tag)

    elif scene_name == "cta":
        p = ease_out_cubic(scene_t)
        # Darken bg slightly for CTA punch — lerp bg toward ink
        # Instead, draw a semi-transparent overlay by blending
        overlay_a = p * 0.12
        # Blend bg toward ink
        bg_cta = tuple(int(lerp(bg_rgb[i], ink_rgb[i], overlay_a)) for i in range(3))
        # Redraw bg with overlay (simple: fill with blended colour at top half)
        # Just draw a rect overlay
        # (We already drew bg; now overlay a translucent-feel rect by re-blending)
        # For RGB, simulate by drawing lines with blended colour at low alpha — skip, keep bg as is

        # CTA text centred
        line1 = "Undangan yang kebuka."
        line2 = "Bukan yang bikin tamu nunggu."
        f_cta = font_cta
        f_sub = font_body

        # Scale + fade
        scale = lerp(0.96, 1.0, p)
        eff_size = max(8, int((W * 0.038 if is_vertical else W * 0.028) * scale))
        f_cta_eff = load_font(eff_size, bold=True)
        alpha = p
        ink_eff = tuple(int(lerp(bg_rgb[i], ink_rgb[i], alpha)) for i in range(3))
        sub_col = tuple(int(lerp(bg_rgb[i], ink_rgb[i], alpha * 0.62)) for i in range(3))

        w1, h1 = text_size(draw, line1, f_cta_eff)
        w2, h2 = text_size(draw, line2, f_sub)
        cx, cy = W // 2, H // 2
        draw.text((cx - w1 // 2, cy - h1 // 2 - 6), line1, fill=ink_eff, font=f_cta_eff)
        draw.text((cx - w2 // 2, cy + h1 // 2 + 8), line2, fill=sub_col, font=f_sub)

        # Button mock — rounded rect with accent
        btn_label = "Lihat 11 Tema  →"
        f_btn = load_font(small_size, bold=True)
        bw, bh = text_size(draw, btn_label, f_btn)
        btn_w, btn_h = bw + 36, bh + 20
        bx, by = cx - btn_w // 2, cy + h1 // 2 + h2 + 32
        # Button slides up slightly
        by = int(lerp(by + 16, by, p))
        # Button bg = accent, text = accentInk (approx: surface or bg depending on theme)
        # Use surface as button text for contrast
        btn_bg = accent_rgb
        # Simple luminance check for text colour
        lum = (0.299 * btn_bg[0] + 0.587 * btn_bg[1] + 0.114 * btn_bg[2]) / 255
        btn_text_col = ink_rgb if lum > 0.6 else surface_rgb
        draw_rounded_rect(draw, (bx, by, bx + btn_w, by + btn_h), radius=btn_h // 2, fill=btn_bg)
        draw.text((bx + (btn_w - bw) // 2, by + (btn_h - bh) // 2), btn_label, fill=btn_text_col, font=f_btn)

        # URL at bottom
        url = "ikat.id  ·  @ikat.undangan"
        f_url = load_font(max(9, small_size - 1), bold=False)
        uw, uh = text_size(draw, url, f_url)
        url_col = tuple(int(lerp(bg_rgb[i], ink_rgb[i], 0.45)) for i in range(3))
        draw.text(((W - uw) // 2, H - pad - uh), url, fill=url_col, font=f_url)


# ------------------------------------------------------------------ encoding

def encode_video(frames_dir: str, out_path: str, fps: int) -> None:
    """Encode PNG sequence to mp4 via ffmpeg."""
    # Ensure output dir exists
    os.makedirs(os.path.dirname(os.path.abspath(out_path)) or ".", exist_ok=True)
    # Use libx264, yuv420p, crf 18, faststart
    cmd = [
        "ffmpeg", "-v", "error", "-y",
        "-framerate", str(fps),
        "-i", os.path.join(frames_dir, "frame_%04d.png"),
        "-c:v", "libx264",
        "-pix_fmt", "yuv420p",
        "-crf", "18",
        "-preset", "medium",
        "-movflags", "+faststart",
        out_path,
    ]
    r = subprocess.run(cmd, capture_output=True, text=True)
    if r.returncode != 0:
        sys.exit(f"ffmpeg encode failed:\n{r.stderr}")

def have_ffmpeg() -> bool:
    return shutil.which("ffmpeg") is not None

# ------------------------------------------------------------------ main

def load_themes() -> list[dict]:
    data = json.load(open(SPEC, encoding="utf-8"))
    return data.get("themes", [])

def generate_frames(theme: dict, out_frames_dir: str, W: int, H: int, fps: int, duration: float) -> int:
    os.makedirs(out_frames_dir, exist_ok=True)
    total = int(round(fps * duration))
    for i in range(total):
        img = Image.new("RGB", (W, H), (255, 255, 255))
        render_frame(img, theme, i, total, fps, W, H)
        img.save(os.path.join(out_frames_dir, f"frame_{i:04d}.png"))
    return total

def main() -> int:
    p = argparse.ArgumentParser(description="Generate promo videos per Ikat theme (PIL + ffmpeg).")
    p.add_argument("--theme", help="theme slug (e.g. butter)")
    p.add_argument("--all", action="store_true", help="render all themes")
    p.add_argument("--list", action="store_true", help="list available themes and exit")
    p.add_argument("--format", choices=list(PRESETS.keys()), default="vertical", help="video preset (default: vertical)")
    p.add_argument("--fps", type=int, default=FPS_DEFAULT, help=f"frames per second (default {FPS_DEFAULT})")
    p.add_argument("--duration", type=float, default=DURATION_DEFAULT, help=f"duration in seconds (default {DURATION_DEFAULT})")
    p.add_argument("-o", "--out", help="output file (single theme) or directory (with --all). Default: dist/promo-<slug>-<format>.mp4")
    p.add_argument("--preview", action="store_true", help="render a single preview PNG instead of video (uses middle frame)")
    p.add_argument("--no-encode", action="store_true", help="only generate PNG frames, skip ffmpeg encode")
    p.add_argument("--frames-dir", help="custom frames directory (default: temp)")
    p.add_argument("--width", type=int, help="override width (height derived from preset aspect)")
    p.add_argument("--height", type=int, help="override height")
    args = p.parse_args()

    themes = load_themes()
    by_slug = {t["slug"]: t for t in themes}

    if args.list:
        for t in themes:
            print(f"{t['slug']:20s} {t['name']:20s} {t.get('mood',''):8s} {t.get('blurb','')[:60]}")
        return 0

    # Resolve target themes
    if args.all:
        targets = themes
    elif args.theme:
        if args.theme not in by_slug:
            print(f"Unknown theme: {args.theme}\nAvailable: {', '.join(by_slug)}", file=sys.stderr)
            return 1
        targets = [by_slug[args.theme]]
    else:
        # default: list and hint
        print("Specify --theme <slug> or --all. Use --list to see themes.", file=sys.stderr)
        return 1

    # Resolve dimensions
    W, H = PRESETS[args.format]
    if args.width:
        W = args.width
    if args.height:
        H = args.height

    if args.preview:
        if len(targets) != 1:
            print("--preview only works with a single --theme", file=sys.stderr)
            return 1
        theme = targets[0]
        total = int(round(args.fps * args.duration))
        mid = total // 2
        out = args.out or f"preview-{theme['slug']}.png"
        os.makedirs(os.path.dirname(os.path.abspath(out)) or ".", exist_ok=True)
        img = Image.new("RGB", (W, H), (255, 255, 255))
        render_frame(img, theme, mid, total, args.fps, W, H)
        img.save(out)
        print(f"{out}  ({W}x{H}, frame {mid}/{total}, theme {theme['slug']})")
        return 0

    if not have_ffmpeg() and not args.no_encode:
        print("ffmpeg not found on PATH — cannot encode. Use --no-encode to generate frames only.", file=sys.stderr)
        return 1

    for theme in targets:
        slug = theme["slug"]
        # Output path
        if args.all:
            out_dir = args.out or os.path.join(ROOT, "dist")
            os.makedirs(out_dir, exist_ok=True)
            out_path = os.path.join(out_dir, f"promo-{slug}-{args.format}.mp4")
        else:
            out_path = args.out or os.path.join(ROOT, "dist", f"promo-{slug}-{args.format}.mp4")

        # Frames dir
        if args.frames_dir and len(targets) == 1:
            frames_dir = args.frames_dir
        else:
            frames_dir = tempfile.mkdtemp(prefix=f"ikat-promo-{slug}-")

        try:
            print(f"[{slug}] {W}x{H} {args.fps}fps {args.duration}s -> {out_path}", file=sys.stderr)
            total = generate_frames(theme, frames_dir, W, H, args.fps, args.duration)
            print(f"  {total} frames in {frames_dir}", file=sys.stderr)
            if args.no_encode:
                print(f"  frames kept at {frames_dir} (--no-encode)")
                # don't delete
                continue
            encode_video(frames_dir, out_path, args.fps)
            kb = os.path.getsize(out_path) / 1024
            print(f"  {out_path}  ({kb:.0f} KB)")
        finally:
            if not args.no_encode and not args.frames_dir:
                shutil.rmtree(frames_dir, ignore_errors=True)
            elif args.no_encode and not args.frames_dir:
                # keep but inform
                pass

    return 0

if __name__ == "__main__":
    raise SystemExit(main())
