#!/usr/bin/env python3
"""Ikat marketing MCP server — stdio JSON-RPC 2.0, no SDK, no dependencies beyond PIL+ffmpeg.

Exposes the same capabilities as bin/make-assets.py + bin/make-promo-video.py
as MCP tools so a coding agent can generate OG images, social cards, and promo
videos without shelling out manually.

    python3 bin/ikat-mcp.py                          # stdio server
    # or via MCP config:
    # { "mcpServers": { "ikat": { "command": ["python3", "bin/ikat-mcp.py"] } } }

Tools:
  ikat_list_themes      list all themes with colours + blurb
  ikat_theme_info       details for one theme
  ikat_generate_og      OG image (1200×630) for a theme
  ikat_generate_assets  batch: og/square/story/favicon per theme
  ikat_generate_promo   promo video or preview frame per theme
  ikat_render_preview   single PNG preview (any size) for quick visual check

Pattern copied from framedeck/mcp_server.py — newline-delimited JSON-RPC 2.0
over stdio, no SDK vendoring, handles initialize/notifications/ping/tools/*.
See second-brain note: framedeck — Bikin video kebaca agent lewat MCP.
"""

from __future__ import annotations

import json
import os
import subprocess
import sys
import tempfile
import traceback

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SPEC = os.path.join(ROOT, "themes", "themes.json")

PROTOCOL_VERSION = "2024-11-05"
SERVER_INFO = {"name": "ikat-marketing", "version": "0.1.0"}

# ------------------------------------------------------------------ tools spec

TOOLS = [
    {
        "name": "ikat_list_themes",
        "description": "List all Ikat themes with slug, name, mood, blurb, and palette. Use to pick a theme for asset generation.",
        "inputSchema": {"type": "object", "properties": {}, "required": []},
    },
    {
        "name": "ikat_theme_info",
        "description": "Get full spec for one theme (colours, fonts, shape, pattern).",
        "inputSchema": {
            "type": "object",
            "properties": {"slug": {"type": "string", "description": "Theme slug, e.g. 'butter'"}},
            "required": ["slug"],
        },
    },
    {
        "name": "ikat_generate_og",
        "description": "Generate an Open Graph image (1200×630) for a theme. Returns the absolute file path — read it as an image to verify.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "slug": {"type": "string", "description": "Theme slug"},
                "out": {"type": "string", "description": "Output path. Defaults to temp file."},
                "format": {"type": "string", "enum": ["png", "webp", "jpg"], "default": "png"},
            },
            "required": ["slug"],
        },
    },
    {
        "name": "ikat_generate_assets",
        "description": "Generate marketing assets (og/square/story/favicon) for one or all themes. Returns manifest with file paths.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "slug": {"type": "string", "description": "Theme slug, or omit with all=true"},
                "all": {"type": "boolean", "default": False, "description": "Generate for all themes"},
                "kinds": {"type": "array", "items": {"type": "string", "enum": ["og", "square", "story", "favicon"]}, "description": "Asset kinds (default: [\"og\"])"},
                "out_dir": {"type": "string", "description": "Output directory (default: temp)"},
                "format": {"type": "string", "enum": ["png", "webp", "jpg"], "default": "png"},
            },
            "required": [],
        },
    },
    {
        "name": "ikat_generate_promo",
        "description": "Generate a promo video (PIL + ffmpeg) for a theme. 6s by default, vertical 1080×1920. Returns video path. Use preview=true for a single PNG instead (faster, no ffmpeg).",
        "inputSchema": {
            "type": "object",
            "properties": {
                "slug": {"type": "string", "description": "Theme slug"},
                "preset": {"type": "string", "enum": ["vertical", "horizontal", "square"], "default": "vertical"},
                "duration": {"type": "number", "default": 6.0},
                "fps": {"type": "integer", "default": 30},
                "preview": {"type": "boolean", "default": False, "description": "If true, render a single PNG preview instead of video"},
                "out": {"type": "string", "description": "Output path (file)"},
            },
            "required": ["slug"],
        },
    },
    {
        "name": "ikat_render_preview",
        "description": "Render a single preview PNG for a theme at any size. Fast visual check without video encoding.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "slug": {"type": "string"},
                "width": {"type": "integer", "default": 1080},
                "height": {"type": "integer", "default": 1920},
                "out": {"type": "string", "description": "Output path"},
            },
            "required": ["slug"],
        },
    },
]

# ------------------------------------------------------------------ helpers

def _load_themes() -> list[dict]:
    with open(SPEC, encoding="utf-8") as f:
        return json.load(f).get("themes", [])

def _find_theme(slug: str) -> dict | None:
    for t in _load_themes():
        if t["slug"] == slug:
            return t
    return None

def _run_cli(args: list[str], timeout: int = 120) -> subprocess.CompletedProcess:
    return subprocess.run(args, capture_output=True, text=True, timeout=timeout)

# ------------------------------------------------------------------ plumbing

def _send(msg: dict) -> None:
    sys.stdout.write(json.dumps(msg, ensure_ascii=False) + "\n")
    sys.stdout.flush()

def _result(rid, result) -> None:
    _send({"jsonrpc": "2.0", "id": rid, "result": result})

def _error(rid, code: int, message: str) -> None:
    _send({"jsonrpc": "2.0", "id": rid, "error": {"code": code, "message": message}})

def _text(s: str, is_error: bool = False) -> dict:
    return {"content": [{"type": "text", "text": s}], "isError": is_error}

# ------------------------------------------------------------------ tool handlers

def _h_list_themes(args: dict) -> dict:
    themes = _load_themes()
    # Compact listing for token efficiency
    rows = [{"slug": t["slug"], "name": t["name"], "mood": t.get("mood"), "blurb": t.get("blurb"), "colors": t.get("colors")} for t in themes]
    return _text(json.dumps({"count": len(rows), "themes": rows}, indent=2, ensure_ascii=False))

def _h_theme_info(args: dict) -> dict:
    slug = args.get("slug")
    if not slug:
        return _text("slug is required", True)
    t = _find_theme(slug)
    if not t:
        return _text(f"unknown theme: {slug}", True)
    return _text(json.dumps(t, indent=2, ensure_ascii=False))

def _h_generate_og(args: dict) -> dict:
    slug = args.get("slug")
    if not slug:
        return _text("slug is required", True)
    if not _find_theme(slug):
        return _text(f"unknown theme: {slug}", True)
    fmt = args.get("format", "png")
    out = args.get("out") or os.path.join(tempfile.mkdtemp(prefix="ikat-og-"), f"og-{slug}.{fmt}")
    os.makedirs(os.path.dirname(os.path.abspath(out)), exist_ok=True)
    cli = [sys.executable, os.path.join(ROOT, "bin", "make-assets.py"), "--theme", slug, "--og", "-o", out, "--format", fmt]
    r = _run_cli(cli)
    if r.returncode != 0:
        return _text(f"make-assets failed:\n{r.stderr or r.stdout}", True)
    abs_path = os.path.abspath(out)
    kb = os.path.getsize(abs_path) / 1024 if os.path.exists(abs_path) else 0
    return _text(json.dumps({"path": abs_path, "size_kb": round(kb, 1), "slug": slug, "kind": "og", "hint": "Read this path as an image to verify."}, indent=2))

def _h_generate_assets(args: dict) -> dict:
    slug = args.get("slug")
    all_flag = args.get("all", False)
    kinds = args.get("kinds") or ["og"]
    fmt = args.get("format", "png")
    out_dir = os.path.abspath(args.get("out_dir") or tempfile.mkdtemp(prefix="ikat-assets-"))
    os.makedirs(out_dir, exist_ok=True)

    if not all_flag and not slug:
        return _text("provide slug or set all=true", True)

    cli = [sys.executable, os.path.join(ROOT, "bin", "make-assets.py")]
    if all_flag:
        cli.append("--all")
    else:
        cli += ["--theme", slug]
    for k in kinds:
        cli.append(f"--{k}")
    cli += ["-o", out_dir, "--format", fmt]

    r = _run_cli(cli, timeout=180)
    if r.returncode != 0:
        return _text(f"make-assets failed:\n{r.stderr or r.stdout}", True)

    files = sorted(os.path.join(out_dir, f) for f in os.listdir(out_dir) if os.path.isfile(os.path.join(out_dir, f)))
    manifest = {"out_dir": out_dir, "count": len(files), "files": files, "hint": "Read file paths as images to verify."}
    # Also include stdout summary
    if r.stdout.strip():
        manifest["log"] = r.stdout.strip()
    return _text(json.dumps(manifest, indent=2, ensure_ascii=False))

def _h_generate_promo(args: dict) -> dict:
    slug = args.get("slug")
    if not slug:
        return _text("slug is required", True)
    if not _find_theme(slug):
        return _text(f"unknown theme: {slug}", True)
    preset = args.get("preset", "vertical")
    duration = float(args.get("duration", 6.0))
    fps = int(args.get("fps", 30))
    preview = bool(args.get("preview", False))
    out = args.get("out")

    if preview:
        if not out:
            out = os.path.join(tempfile.mkdtemp(prefix="ikat-promo-"), f"preview-{slug}.png")
        os.makedirs(os.path.dirname(os.path.abspath(out)), exist_ok=True)
        cli = [sys.executable, os.path.join(ROOT, "bin", "make-promo-video.py"), "--theme", slug, "--preview", "-o", out]
        # preset controls size via format — map to width/height if needed
        # For preview, use preset dimensions
        r = _run_cli(cli)
        if r.returncode != 0:
            return _text(f"make-promo-video failed:\n{r.stderr or r.stdout}", True)
        abs_path = os.path.abspath(out)
        kb = os.path.getsize(abs_path) / 1024 if os.path.exists(abs_path) else 0
        return _text(json.dumps({"path": abs_path, "size_kb": round(kb, 1), "slug": slug, "kind": "preview", "hint": "Read this path as an image."}, indent=2))

    # Video
    if not out:
        out = os.path.join(tempfile.mkdtemp(prefix="ikat-promo-"), f"promo-{slug}-{preset}.mp4")
    os.makedirs(os.path.dirname(os.path.abspath(out)), exist_ok=True)
    cli = [sys.executable, os.path.join(ROOT, "bin", "make-promo-video.py"), "--theme", slug, "--format", preset, "--duration", str(duration), "--fps", str(fps), "-o", out]
    r = _run_cli(cli, timeout=300)
    if r.returncode != 0:
        return _text(f"make-promo-video failed:\n{r.stderr or r.stdout}", True)
    abs_path = os.path.abspath(out)
    kb = os.path.getsize(abs_path) / 1024 if os.path.exists(abs_path) else 0
    return _text(json.dumps({"path": abs_path, "size_kb": round(kb, 1), "slug": slug, "preset": preset, "duration": duration, "fps": fps, "hint": "Video file — probe with ffprobe or open in a player."}, indent=2))

def _h_render_preview(args: dict) -> dict:
    slug = args.get("slug")
    if not slug:
        return _text("slug is required", True)
    if not _find_theme(slug):
        return _text(f"unknown theme: {slug}", True)
    W = int(args.get("width", 1080))
    H = int(args.get("height", 1920))
    out = args.get("out") or os.path.join(tempfile.mkdtemp(prefix="ikat-preview-"), f"preview-{slug}-{W}x{H}.png")
    os.makedirs(os.path.dirname(os.path.abspath(out)), exist_ok=True)
    # Reuse make-promo-video preview but at custom size via --width/--height
    cli = [sys.executable, os.path.join(ROOT, "bin", "make-promo-video.py"), "--theme", slug, "--preview", "-o", out, "--width", str(W), "--height", str(H)]
    r = _run_cli(cli)
    if r.returncode != 0:
        return _text(f"preview failed:\n{r.stderr or r.stdout}", True)
    abs_path = os.path.abspath(out)
    return _text(json.dumps({"path": abs_path, "size": [W, H], "slug": slug}, indent=2))

HANDLERS = {
    "ikat_list_themes": _h_list_themes,
    "ikat_theme_info": _h_theme_info,
    "ikat_generate_og": _h_generate_og,
    "ikat_generate_assets": _h_generate_assets,
    "ikat_generate_promo": _h_generate_promo,
    "ikat_render_preview": _h_render_preview,
}

# ------------------------------------------------------------------ serve loop

def serve(stdin=None, stdout=None) -> None:
    stdin = stdin or sys.stdin
    for line in stdin:
        line = line.strip()
        if not line:
            continue
        try:
            msg = json.loads(line)
        except json.JSONDecodeError:
            continue
        method = msg.get("method")
        rid = msg.get("id")
        if rid is None:
            continue  # notification — never reply
        try:
            if method == "initialize":
                client = (msg.get("params") or {}).get("protocolVersion")
                _result(rid, {"protocolVersion": client or PROTOCOL_VERSION, "capabilities": {"tools": {}}, "serverInfo": SERVER_INFO})
            elif method == "ping":
                _result(rid, {})
            elif method == "tools/list":
                _result(rid, {"tools": TOOLS})
            elif method == "tools/call":
                params = msg.get("params") or {}
                name = params.get("name")
                h = HANDLERS.get(name)
                if not h:
                    _error(rid, -32602, f"unknown tool: {name}")
                else:
                    _result(rid, h(params.get("arguments") or {}))
            else:
                _error(rid, -32601, f"method not found: {method}")
        except Exception as e:  # noqa: BLE001 — server must not die
            traceback.print_exc(file=sys.stderr)
            _error(rid, -32603, f"internal error: {e}")

if __name__ == "__main__":
    serve()
