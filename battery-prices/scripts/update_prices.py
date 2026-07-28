#!/usr/bin/env python3
"""Maintain data/batteries.json.

The workflow this supports, in order:

  1. --check       validate specs before you trust anything
  2. --export-csv  dump rows to a spreadsheet for manual price entry
  3. --import-csv  read the prices back in and stamp checked_at
  4. --from-paapi  swap to the Amazon API once you have the sales to qualify

Steps 2-3 are how the site runs for its first few months. Step 4 needs
qualifying sales that you cannot have before launching, so it stays a stub
until the site has made them.

Stdlib only. No install step.
"""

from __future__ import annotations

import argparse
import csv
import json
import sys
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DATA = ROOT / "data" / "batteries.json"

STALE_HOURS = 24  # Amazon caps displayed price age at 24h.
CSV_FIELDS = ["id", "brand", "platform_name", "model", "name", "amp_hours",
              "pack_count", "rated_wh", "price", "url", "asin"]


# ---------- io ----------

def load() -> dict:
    with DATA.open(encoding="utf-8") as fh:
        return json.load(fh)


def save(doc: dict) -> None:
    doc["meta"]["generated_at"] = datetime.now(timezone.utc).isoformat(timespec="seconds")
    with DATA.open("w", encoding="utf-8") as fh:
        json.dump(doc, fh, indent=2, ensure_ascii=False)
        fh.write("\n")


def now() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


def age_hours(iso: str | None) -> float:
    if not iso:
        return float("inf")
    try:
        return (datetime.now(timezone.utc) - datetime.fromisoformat(iso)).total_seconds() / 3600
    except ValueError:
        return float("inf")


# ---------- check ----------

def cmd_check(doc: dict) -> int:
    """Validate the dataset. Exit non-zero on anything that would mislead a visitor."""
    platforms = doc["platforms"]
    errors: list[str] = []
    warnings: list[str] = []
    seen: set[str] = set()

    # Sample rows have no urls and no timestamps by definition. Nagging about
    # every one of them buries the spec errors that actually matter.
    sample = doc["meta"].get("price_source") == "sample"

    for b in doc["batteries"]:
        bid = b.get("id", "<no id>")

        if bid in seen:
            errors.append(f"{bid}: duplicate id")
        seen.add(bid)

        plat = platforms.get(b.get("platform"))
        if plat is None:
            errors.append(f"{bid}: unknown platform {b.get('platform')!r}")
            continue

        if not b.get("amp_hours") or b["amp_hours"] <= 0:
            errors.append(f"{bid}: amp_hours must be > 0")
            continue
        if not b.get("pack_count") or b["pack_count"] < 1:
            errors.append(f"{bid}: pack_count must be >= 1")
            continue

        # The whole premise of the site is that this number is right.
        computed = plat["nominal_volts"] * b["amp_hours"]
        rated = b.get("rated_wh")
        if rated is not None and abs(rated - computed) > max(1.0, computed * 0.02):
            errors.append(
                f"{bid}: rated {rated}Wh vs {plat['nominal_volts']}V x {b['amp_hours']}Ah "
                f"= {computed:.1f}Wh — one of them is wrong"
            )

        price = b.get("price")
        if price is None:
            warnings.append(f"{bid}: no price (row will render but not rank)")
        elif price <= 0:
            errors.append(f"{bid}: price must be > 0")
        elif not sample:
            if not b.get("url"):
                warnings.append(f"{bid}: priced but has no affiliate url — unclickable")
            hrs = age_hours(b.get("checked_at"))
            if hrs > STALE_HOURS:
                label = "never checked" if hrs == float("inf") else f"{hrs:.0f}h old"
                warnings.append(f"{bid}: price {label} (limit {STALE_HOURS}h)")

    for w in warnings:
        print(f"warn  {w}")
    for e in errors:
        print(f"ERROR {e}", file=sys.stderr)

    n = len(doc["batteries"])
    print(f"\n{n} batteries · {len(errors)} errors · {len(warnings)} warnings")

    if doc["meta"].get("price_source") == "sample":
        print("\nprice_source is still 'sample' — the page shows a placeholder banner "
              "until you set it to 'manual' or 'paapi'.")

    return 1 if errors else 0


# ---------- csv round trip ----------

def cmd_export(doc: dict, path: Path) -> int:
    platforms = doc["platforms"]
    with path.open("w", newline="", encoding="utf-8") as fh:
        w = csv.DictWriter(fh, fieldnames=CSV_FIELDS)
        w.writeheader()
        for b in doc["batteries"]:
            p = platforms[b["platform"]]
            w.writerow({
                "id": b["id"],
                "brand": p["brand"],
                "platform_name": p["name"],
                "model": b["model"],
                "name": b["name"],
                "amp_hours": b["amp_hours"],
                "pack_count": b["pack_count"],
                "rated_wh": b.get("rated_wh", ""),
                "price": b.get("price", ""),
                "url": b.get("url", ""),
                "asin": b.get("asin", ""),
            })
    print(f"wrote {len(doc['batteries'])} rows to {path}")
    print("Fill in price + url, then: update_prices.py --import-csv " + str(path))
    return 0


def cmd_import(doc: dict, path: Path) -> int:
    by_id = {b["id"]: b for b in doc["batteries"]}
    stamp = now()
    updated = skipped = unknown = 0

    with path.open(newline="", encoding="utf-8") as fh:
        for r in csv.DictReader(fh):
            bid = (r.get("id") or "").strip()
            if bid not in by_id:
                if bid:
                    print(f"warn  unknown id {bid!r}, skipped")
                    unknown += 1
                continue

            b = by_id[bid]
            raw = (r.get("price") or "").strip()
            if not raw:
                skipped += 1
                continue

            try:
                price = round(float(raw.lstrip("$").replace(",", "")), 2)
            except ValueError:
                print(f"warn  {bid}: unparseable price {raw!r}, skipped")
                skipped += 1
                continue

            if price <= 0:
                print(f"warn  {bid}: non-positive price {price}, skipped")
                skipped += 1
                continue

            b["price"] = price
            b["checked_at"] = stamp
            if (r.get("url") or "").strip():
                b["url"] = r["url"].strip()
            if (r.get("asin") or "").strip():
                b["asin"] = r["asin"].strip()
            updated += 1

    if updated:
        # Anything hand-entered is 'manual', which clears the sample-data banner.
        if doc["meta"].get("price_source") == "sample":
            doc["meta"]["price_source"] = "manual"
            doc["meta"].pop("warning", None)
            print("price_source: sample -> manual")
        save(doc)

    print(f"updated {updated} · skipped {skipped} · unknown {unknown}")
    return 0


# ---------- amazon ----------

def cmd_paapi(doc: dict) -> int:
    print(
        "PA-API is not wired up yet, and cannot be until the site has sales.\n"
        "\n"
        "  Access requires ~3 qualifying sales within 180 days of joining\n"
        "  Associates, and keeping it requires ongoing sales in a rolling\n"
        "  30-day window. No sales, no key — and no key means no data, which\n"
        "  means no sales. Do not build the site on it.\n"
        "\n"
        "Launch on --export-csv/--import-csv, get the first sales, then\n"
        "implement here:\n"
        "\n"
        "  1. GetItems with the asin field already in the dataset\n"
        "  2. Map Offers.Listings[0].Price.Amount -> price\n"
        "  3. Set checked_at = now, run --check, then build.py\n"
        "  4. Schedule daily (GitHub Actions cron is free and enough)\n",
        file=sys.stderr,
    )
    return 2


# ---------- cli ----------

def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    g = ap.add_mutually_exclusive_group(required=True)
    g.add_argument("--check", action="store_true", help="validate specs, prices and staleness")
    g.add_argument("--export-csv", metavar="PATH", help="dump rows for manual price entry")
    g.add_argument("--import-csv", metavar="PATH", help="read prices back in")
    g.add_argument("--from-paapi", action="store_true", help="(stub) fetch from Amazon")
    args = ap.parse_args()

    doc = load()

    if args.check:
        return cmd_check(doc)
    if args.export_csv:
        return cmd_export(doc, Path(args.export_csv))
    if args.import_csv:
        return cmd_import(doc, Path(args.import_csv))
    return cmd_paapi(doc)


if __name__ == "__main__":
    raise SystemExit(main())
