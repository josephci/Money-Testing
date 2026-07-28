#!/usr/bin/env python3
"""Bundle the site into dist/.

Emits:
  dist/index.html            every platform
  dist/<platform>/index.html one page per battery platform
  dist/assets/og.png         social card
  dist/sitemap.xml
  dist/robots.txt

CSS, JS and the dataset are inlined into every page, so each one is a single
file with no requests of its own.

The per-platform pages exist for search traffic. "milwaukee m18 battery
comparison" is a real query with real volume; a single-page site cannot rank
for nine of those at once, and each page carries its own title, description
and opening copy derived from that platform's data.

  python3 scripts/build.py --base-url https://yourdomain.com
"""

from __future__ import annotations

import argparse
import html
import json
import re
import shutil
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DIST = ROOT / "dist"


# ---------- helpers ----------

def esc(s: str) -> str:
    return html.escape(str(s), quote=True)


def platform_stats(data: dict, key: str) -> dict:
    plat = data["platforms"][key]
    rows = [b for b in data["batteries"] if b["platform"] == key]

    best = None
    for b in rows:
        price = b.get("price")
        if not price or price <= 0:
            continue
        per_pack = b["rated_wh"] if b.get("rated_wh") is not None else plat["nominal_volts"] * b["amp_hours"]
        per_wh = price / (per_pack * b["pack_count"])
        if best is None or per_wh < best[0]:
            best = (per_wh, b)

    return {"plat": plat, "count": len(rows), "best": best}


def intro_html(key: str, st: dict) -> str:
    """Opening copy for a platform page, built from that platform's own numbers."""
    p, n, best = st["plat"], st["count"], st["best"]
    name = f"{p['brand']} {p['name']}"

    parts = [
        f"<h2>{esc(name)} batteries by cost per watt-hour</h2>",
        f"<p>All {n} {esc(name)} batteries we track, ranked by what a watt-hour "
        f"actually costs. Multi-packs are divided by their total energy, so a "
        f"two-pack competes on the same terms as a single.</p>",
    ]

    if p["marketing_volts"] != p["nominal_volts"]:
        parts.append(
            f"<p><strong>{esc(name)} packs are sold as {p['marketing_volts']}V but run at "
            f"{p['nominal_volts']}V nominal.</strong> {esc(p.get('note', ''))} "
            f"Every figure below uses the nominal {p['nominal_volts']}V, which is why these "
            f"numbers compare cleanly against any other brand.</p>"
        )
    else:
        parts.append(
            f"<p>{esc(name)} is marketed at its nominal {p['nominal_volts']}V, so the sticker "
            f"and the real figure already agree — unlike platforms that advertise peak voltage.</p>"
        )

    if best:
        per_wh, b = best
        parts.append(
            f"<p>Best value right now: <strong>{esc(b['name'])}</strong> "
            f"({esc(b['model'])}) at <strong>${per_wh:.3f}/Wh</strong>.</p>"
        )

    return '<section class="intro">' + "".join(parts) + "</section>"


def battery_metrics(data: dict, b: dict) -> dict:
    plat = data["platforms"][b["platform"]]
    per_pack = b["rated_wh"] if b.get("rated_wh") is not None else plat["nominal_volts"] * b["amp_hours"]
    total_wh = per_pack * b["pack_count"]
    price = b.get("price")
    return {
        "plat": plat,
        "per_pack_wh": per_pack,
        "total_wh": total_wh,
        "per_wh": (price / total_wh) if price else None,
        "per_ah": (price / (b["amp_hours"] * b["pack_count"])) if price else None,
    }


def model_intro(data: dict, b: dict) -> str:
    """Opening copy for one battery. Spells out the arithmetic the site exists to do."""
    m = battery_metrics(data, b)
    p = m["plat"]
    name = f"{p['brand']} {b['name']}"
    packs = f" &times; {b['pack_count']} packs" if b["pack_count"] > 1 else ""

    parts = [
        f"<h2>{esc(name)} ({esc(b['model'])}) — the real numbers</h2>",
        f"<p class=\"math\">{p['nominal_volts']}V nominal &times; {b['amp_hours']}Ah{packs} "
        f"= <strong>{m['total_wh']:g}Wh</strong></p>",
    ]

    if p["marketing_volts"] != p["nominal_volts"]:
        parts.append(
            f"<p>This pack is sold as <strong>{p['marketing_volts']}V {b['amp_hours']}Ah</strong>. "
            f"That {p['marketing_volts']}V is the peak reading straight off the charger; it settles "
            f"at {p['nominal_volts']}V for the rest of the discharge, which is the figure the "
            f"energy calculation uses. {esc(p.get('note', ''))}</p>"
        )

    if m["per_wh"] is not None:
        parts.append(
            f"<p>At <strong>${b['price']:.2f}</strong> that works out to "
            f"<strong>${m['per_wh']:.3f} per watt-hour</strong> "
            f"(${m['per_ah']:.2f} per amp-hour).</p>"
        )

        # Where it sits against its own platform — the comparison a buyer locked
        # into this battery system actually needs.
        siblings = [x for x in data["batteries"]
                    if x["platform"] == b["platform"] and x["id"] != b["id"] and x.get("price")]
        better = sorted(
            ((battery_metrics(data, x)["per_wh"], x) for x in siblings),
            key=lambda t: t[0],
        )
        better = [(v, x) for v, x in better if v < m["per_wh"]]

        if not better:
            parts.append(
                f"<p><strong>This is the best value in the {esc(p['brand'])} {esc(p['name'])} "
                f"range</strong> of the {len(siblings) + 1} packs tracked here.</p>"
            )
        else:
            v, x = better[0]
            pct = (m["per_wh"] - v) / m["per_wh"] * 100
            parts.append(
                f"<p>{len(better)} other {esc(p['brand'])} {esc(p['name'])} pack"
                f"{'s' if len(better) > 1 else ''} give more energy per dollar. The best of them, "
                f"<strong>{esc(x['name'])}</strong> ({esc(x['model'])}), is "
                f"<strong>{pct:.0f}% cheaper per watt-hour</strong> at ${v:.3f}/Wh.</p>"
            )

    return '<section class="intro">' + "".join(parts) + "</section>"


def model_jsonld(data: dict, b: dict, url: str) -> str:
    m = battery_metrics(data, b)
    p = m["plat"]
    doc = {
        "@context": "https://schema.org",
        "@type": "Product",
        "name": f"{p['brand']} {b['name']} ({b['model']})",
        "sku": b["model"],
        "brand": {"@type": "Brand", "name": p["brand"]},
        "url": url,
        "additionalProperty": [
            {"@type": "PropertyValue", "name": "Capacity", "value": f"{b['amp_hours']}Ah"},
            {"@type": "PropertyValue", "name": "Nominal voltage", "value": f"{p['nominal_volts']}V"},
            {"@type": "PropertyValue", "name": "Energy", "value": f"{m['total_wh']:g}Wh"},
        ],
    }
    if b.get("asin"):
        doc["gtin"] = b["asin"]
    return ('<script type="application/ld+json">'
            + json.dumps(doc, ensure_ascii=False, separators=(",", ":")).replace("</", "<\\/")
            + "</script>")


def render(html_src: str, css: str, js: str, data: dict, *, base_url: str,
           path: str, title: str, desc: str, platform: str | None,
           page_base: str, intro: str, jsonld: str = "") -> str:
    """Inline everything and stamp this page's metadata."""
    out = html_src.replace(
        '<link rel="stylesheet" href="assets/style.css">',
        f"<style>\n{css}\n</style>" + (f"\n{jsonld}" if jsonld else ""),
    )

    out = out.replace(
        "<title>Battery Prices — cordless tool batteries ranked by $/Wh</title>",
        f"<title>{esc(title)}</title>",
    )
    out = re.sub(r'<meta name="description" content="[^"]*">',
                 f'<meta name="description" content="{esc(desc)}">', out, count=1)
    out = re.sub(r'<meta property="og:title" content="[^"]*">',
                 f'<meta property="og:title" content="{esc(title)}">', out, count=1)
    out = re.sub(r'<meta property="og:description" content="[^"]*">',
                 f'<meta property="og:description" content="{esc(desc)}">', out, count=1)

    url = base_url.rstrip("/") + path
    out = out.replace('<link rel="canonical" href="https://example.com/">',
                      f'<link rel="canonical" href="{esc(url)}">')
    out = out.replace('<meta property="og:url" content="https://example.com/">',
                      f'<meta property="og:url" content="{esc(url)}">')
    out = out.replace('content="https://example.com/assets/og.png"',
                      f'content="{esc(base_url.rstrip("/"))}/assets/og.png"')

    out = out.replace('<div id="intro"></div>', f'<div id="intro">{intro}</div>')

    payload = json.dumps(data, ensure_ascii=False, separators=(",", ":")).replace("</", "<\\/")
    boot = [f"window.__DATA__ = {payload};",
            f"window.__PAGE_BASE__ = {json.dumps(page_base)};"]
    if platform:
        boot.append(f"window.__PLATFORM__ = {json.dumps(platform)};")

    return out.replace(
        '<script src="assets/app.js"></script>',
        "<script>\n" + "\n".join(boot) + f"\n</script>\n<script>\n{js}\n</script>",
    )


# ---------- build ----------

def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--base-url", default="https://example.com",
                    help="canonical origin, e.g. https://toolbatteryprices.com")
    args = ap.parse_args()
    base = args.base_url.rstrip("/")

    html_src = (ROOT / "index.html").read_text(encoding="utf-8")
    css = (ROOT / "assets" / "style.css").read_text(encoding="utf-8")
    js = (ROOT / "assets" / "app.js").read_text(encoding="utf-8")
    data = json.loads((ROOT / "data" / "batteries.json").read_text(encoding="utf-8"))

    if DIST.exists():
        shutil.rmtree(DIST)
    DIST.mkdir()

    pages: list[str] = []

    # Home
    (DIST / "index.html").write_text(
        render(
            html_src, css, js, data,
            base_url=base, path="/",
            title="Battery Prices — cordless tool batteries ranked by $/Wh",
            desc=("Every cordless power tool battery ranked by real cost per watt-hour. "
                  "DeWalt, Milwaukee, Makita, Ryobi and Bosch normalised to nominal "
                  "voltage so the comparison is honest."),
            platform=None, page_base="", intro="",
        ),
        encoding="utf-8",
    )
    pages.append("/")

    # One page per platform
    for key in sorted(data["platforms"]):
        st = platform_stats(data, key)
        if st["count"] == 0:
            continue
        p = st["plat"]
        name = f"{p['brand']} {p['name']}"

        desc = (f"All {st['count']} {name} batteries ranked by cost per watt-hour. ")
        if p["marketing_volts"] != p["nominal_volts"]:
            desc += (f"Sold as {p['marketing_volts']}V, actually {p['nominal_volts']}V nominal — "
                     f"we use the real figure.")
        else:
            desc += "Multi-packs divided by total energy, so the comparison is honest."

        d = DIST / key
        d.mkdir()
        (d / "index.html").write_text(
            render(
                html_src, css, js, data,
                base_url=base, path=f"/{key}/",
                title=f"{name} battery comparison — cheapest $/Wh",
                desc=desc, platform=key, page_base="../",
                intro=intro_html(key, st),
            ),
            encoding="utf-8",
        )
        pages.append(f"/{key}/")

        # One page per model. These target queries nobody else has a page for
        # — "DCB205 watt hours", "is the HD12.0 worth it" — which is the only
        # kind of search a brand new domain with no backlinks can win.
        for b in data["batteries"]:
            if b["platform"] != key:
                continue
            slug = b["model"].lower().replace(" ", "-").replace("/", "-")
            m = battery_metrics(data, b)
            mpath = f"/{key}/{slug}/"
            mtitle = (f"{p['brand']} {b['model']} — {b['amp_hours']}Ah, "
                      f"{m['total_wh']:g}Wh, cost per watt-hour")
            mdesc = (f"{p['brand']} {b['name']} ({b['model']}): {p['nominal_volts']}V nominal, "
                     f"{m['total_wh']:g}Wh")
            mdesc += (f", ${m['per_wh']:.3f} per watt-hour. See how it compares to every other "
                      f"{p['brand']} {p['name']} pack." if m["per_wh"] else
                      f". Compared against every other {p['brand']} {p['name']} pack.")

            md = d / slug
            md.mkdir()
            (md / "index.html").write_text(
                render(
                    html_src, css, js, data,
                    base_url=base, path=mpath, title=mtitle, desc=mdesc,
                    platform=key, page_base="../../",
                    intro=model_intro(data, b),
                    jsonld=model_jsonld(data, b, base + mpath),
                ),
                encoding="utf-8",
            )
            pages.append(mpath)

    # Assets referenced by absolute URL (the social card).
    og = ROOT / "assets" / "og.png"
    if og.exists():
        (DIST / "assets").mkdir(exist_ok=True)
        shutil.copy2(og, DIST / "assets" / "og.png")
    else:
        print("warn  assets/og.png missing — og:image will 404")

    today = date.today().isoformat()
    (DIST / "sitemap.xml").write_text(
        '<?xml version="1.0" encoding="UTF-8"?>\n'
        '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
        + "".join(f"  <url><loc>{base}{p}</loc><lastmod>{today}</lastmod></url>\n" for p in pages)
        + "</urlset>\n",
        encoding="utf-8",
    )
    (DIST / "robots.txt").write_text(
        f"User-agent: *\nAllow: /\n\nSitemap: {base}/sitemap.xml\n", encoding="utf-8"
    )

    total = sum(f.stat().st_size for f in DIST.rglob("*") if f.is_file()) / 1024
    print(f"{len(pages)} pages · {total:.0f} KB total · base {base}")

    if base == "https://example.com":
        print("warn  --base-url not set; canonical and sitemap point at example.com")
    if data["meta"].get("price_source") == "sample":
        print("\nNOTE: still sample data — do not deploy this build.")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
