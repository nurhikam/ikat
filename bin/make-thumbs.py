#!/usr/bin/env python3
"""Screenshot cover undangan beneran per tema via Playwright.

    ./bin/make-thumbs.py --all
    ./bin/make-thumbs.py --theme butter
    ./bin/make-thumbs.py --theme spiderman --out /tmp/shot.png

Buka preview.html?theme=<slug> di headless Chromium, tunggu engine render,
screenshot viewport 440x750 (cover doang), simpan webp ke site/thumbs/.
Jauh lebih akurat dari PIL mockup — decoration, font, shape semua kepake.
"""
from __future__ import annotations
import argparse, asyncio, json, os, sys, http.server, threading, socket

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SPEC = os.path.join(ROOT, "themes", "themes.json")

def find_free_port() -> int:
    s = socket.socket()
    s.bind(("127.0.0.1", 0))
    port = s.getsockname()[1]
    s.close()
    return port

def start_server(port: int):
    handler = http.server.SimpleHTTPRequestHandler
    # Serve from ROOT so /engine, /themes, /data, /site all resolve
    os.chdir(ROOT)
    httpd = http.server.ThreadingHTTPServer(("127.0.0.1", port), handler)
    t = threading.Thread(target=httpd.serve_forever, daemon=True)
    t.start()
    return httpd

async def screenshot_one(slug: str, port: int, out_path: str, W: int = 440, H: int = 750):
    from playwright.async_api import async_playwright
    url = f"http://127.0.0.1:{port}/preview.html?theme={slug}"
    async with async_playwright() as p:
        browser = await p.chromium.launch()
        # Viewport exactly thumb size — cover is first screen
        page = await browser.new_page(viewport={"width": W, "height": H}, device_scale_factor=2)
        await page.goto(url, wait_until="networkidle", timeout=15000)
        # Wait for engine render — #app should have content
        try:
            await page.wait_for_selector("#app .u-cover", timeout=8000)
        except Exception:
            # fallback: wait a bit
            await page.wait_for_timeout(1500)
        # Small delay for fonts/decoration
        await page.wait_for_timeout(600)
        # Screenshot full viewport (cover)
        # Clip to viewport — cover is first screen
        await page.screenshot(path=out_path, full_page=False, type="webp", quality=82)
        await browser.close()
    kb = os.path.getsize(out_path) / 1024
    print(f"  {slug:20s} {kb:.0f} KB -> {out_path}")

async def run_all(slugs: list[str], port: int, out_dir: str, W: int, H: int):
    from playwright.async_api import async_playwright
    url_tpl = f"http://127.0.0.1:{port}/preview.html?theme={{}}"
    async with async_playwright() as p:
        browser = await p.chromium.launch()
        for slug in slugs:
            url = url_tpl.format(slug)
            page = await browser.new_page(viewport={"width": W, "height": H}, device_scale_factor=2)
            try:
                await page.goto(url, wait_until="networkidle", timeout=15000)
                try:
                    await page.wait_for_selector("#app .u-cover", timeout=8000)
                except Exception:
                    await page.wait_for_timeout(1500)
                await page.wait_for_timeout(500)
                out_path = os.path.join(out_dir, f"{slug}.webp")
                await page.screenshot(path=out_path, full_page=False, type="webp", quality=82)
                kb = os.path.getsize(out_path) / 1024
                print(f"  {slug:20s} {kb:.0f} KB")
            except Exception as e:
                print(f"  {slug:20s} FAIL: {e}", file=sys.stderr)
            finally:
                await page.close()
        await browser.close()

def main() -> int:
    ap = argparse.ArgumentParser(description="Screenshot cover undangan per tema (Playwright)")
    ap.add_argument("--theme", help="single slug")
    ap.add_argument("--all", action="store_true", help="all themes")
    ap.add_argument("--list", action="store_true")
    ap.add_argument("-o", "--out", help="output file (single) or dir (with --all)")
    ap.add_argument("--width", type=int, default=440)
    ap.add_argument("--height", type=int, default=750)
    args = ap.parse_args()

    data = json.load(open(SPEC, encoding="utf-8"))
    themes = data["themes"]
    by_slug = {t["slug"]: t for t in themes}

    if args.list:
        for t in themes:
            print(f"{t['slug']:20s} {t['name']}")
        return 0

    if args.all:
        slugs = [t["slug"] for t in themes]
        out_dir = args.out or os.path.join(ROOT, "site", "thumbs")
    elif args.theme:
        if args.theme not in by_slug:
            print(f"Unknown theme: {args.theme}", file=sys.stderr)
            return 1
        slugs = [args.theme]
        out_dir = None
    else:
        ap.print_help()
        return 1

    port = find_free_port()
    httpd = start_server(port)
    print(f"Server on :{port}  ({len(slugs)} tema, {args.width}x{args.height})")

    try:
        if args.theme and args.out and os.path.splitext(args.out)[1]:
            # single file
            asyncio.run(screenshot_one(slugs[0], port, args.out, args.width, args.height))
        else:
            out_dir = out_dir or os.path.join(ROOT, "site", "thumbs")
            os.makedirs(out_dir, exist_ok=True)
            asyncio.run(run_all(slugs, port, out_dir, args.width, args.height))
            print(f"\n{len(slugs)} thumbs -> {out_dir}")
    finally:
        httpd.shutdown()

    return 0

if __name__ == "__main__":
    raise SystemExit(main())
