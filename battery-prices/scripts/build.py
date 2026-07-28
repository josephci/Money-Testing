#!/usr/bin/env python3
"""Bundle the site into a single self-contained dist/index.html.

CSS, JS and the dataset all get inlined, so the output is one file with no
requests of its own. Drop it on Cloudflare Pages, GitHub Pages, S3, anywhere.
"""

from __future__ import annotations

import json
import re
import shutil
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DIST = ROOT / "dist"


def inline(html: str, css: str, js: str, data: dict) -> str:
    html = html.replace(
        '<link rel="stylesheet" href="assets/style.css">',
        f"<style>\n{css}\n</style>",
    )

    # </script> inside the JSON would close the tag early.
    payload = json.dumps(data, ensure_ascii=False, separators=(",", ":")).replace("</", "<\\/")

    html = html.replace(
        '<script src="assets/app.js"></script>',
        f"<script>\nwindow.__DATA__ = {payload};\n</script>\n<script>\n{js}\n</script>",
    )
    return html


def main() -> int:
    html = (ROOT / "index.html").read_text(encoding="utf-8")
    css = (ROOT / "assets" / "style.css").read_text(encoding="utf-8")
    js = (ROOT / "assets" / "app.js").read_text(encoding="utf-8")
    data = json.loads((ROOT / "data" / "batteries.json").read_text(encoding="utf-8"))

    out = inline(html, css, js, data)

    if DIST.exists():
        shutil.rmtree(DIST)
    DIST.mkdir()
    (DIST / "index.html").write_text(out, encoding="utf-8")

    for leftover in re.findall(r'(?:src|href)="assets/[^"]+"', out):
        print(f"warn  {leftover} was not inlined")

    kb = len(out.encode()) / 1024
    print(f"dist/index.html · {kb:.1f} KB · {len(data['batteries'])} batteries")

    if data["meta"].get("price_source") == "sample":
        print("\nNOTE: still sample data — do not deploy this build.")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
