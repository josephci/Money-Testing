#!/usr/bin/env python3
"""Maintain data/batteries.json.

The workflow this supports, in order:

  1. --check       validate specs before you trust anything
  2. --export-csv  dump rows to a spreadsheet for manual price entry
  3. --import-csv  read the prices back in, stamp checked_at, append history
  4. --history     what the recorded price history looks like so far
  5. --from-paapi  swap to the Amazon API once you have the sales to qualify

Steps 2-3 are how the site runs for its first few months. Step 5 needs
qualifying sales that you cannot have before launching, so it stays a stub
until the site has made them.

Every import appends to data/history.jsonl. That file is the one asset here
that cannot be copied by someone starting later — a year in, it answers
"when is this pack usually cheapest" and nobody else can catch up.

Stdlib only. No install step.
"""

from __future__ import annotations

import argparse
import csv
import json
import sys
from collections import defaultdict
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DATA = ROOT / "data" / "batteries.json"
HISTORY = ROOT / "data" / "history.jsonl"

STALE_HOURS = 24  # Amazon caps displayed price age at 24h.
CSV_FIELDS = ["id", "brand", "platform_name", "model", "name", "amp_hours",
              "pack_count", "rated_wh", "verified", "spec_url", "price", "url", "asin"]


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


def append_history(rows: list[dict], stamp: str) -> int:
    """Append one line per priced battery. Append-only — never rewrite this file."""
    if not rows:
        return 0
    with HISTORY.open("a", encoding="utf-8") as fh:
        for r in rows:
            fh.write(json.dumps({"t": stamp, **r}, ensure_ascii=False,
                                separators=(",", ":")) + "\n")
    return len(rows)


def read_history() -> list[dict]:
    if not HISTORY.exists():
        return []
    out = []
    for line in HISTORY.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line:
            continue
        try:
            out.append(json.loads(line))
        except json.JSONDecodeError:
            print(f"warn  skipping malformed history line: {line[:60]}", file=sys.stderr)
    return out


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

    # Spec verification is the one step that needs a human with a browser:
    # --check only proves the numbers agree with each other, not that they
    # match the manufacturer's sheet.
    done = sum(1 for b in doc["batteries"] if b.get("verified"))
    bar = "#" * round(done / n * 24) + "." * (24 - round(done / n * 24))
    print(f"specs verified · [{bar}] {done}/{n}")
    if done < n:
        print(f"  {n - done} rows still unverified. Set verified=yes in the CSV as you "
              f"confirm each against the manufacturer spec sheet.")

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
                "verified": "yes" if b.get("verified") else "",
                "spec_url": b.get("spec_url", ""),
                "price": b.get("price", ""),
                "url": b.get("url", ""),
                "asin": b.get("asin", ""),
            })
    print(f"wrote {len(doc['batteries'])} rows to {path}")
    print("Fill in price + url (and verified=yes once you have checked the spec sheet),")
    print("then: update_prices.py --import-csv " + str(path))
    return 0


def cmd_import(doc: dict, path: Path) -> int:
    by_id = {b["id"]: b for b in doc["batteries"]}
    stamp = now()
    updated = skipped = unknown = 0
    snapshot: list[dict] = []

    with path.open(newline="", encoding="utf-8") as fh:
        for r in csv.DictReader(fh):
            bid = (r.get("id") or "").strip()
            if bid not in by_id:
                if bid:
                    print(f"warn  unknown id {bid!r}, skipped")
                    unknown += 1
                continue

            b = by_id[bid]

            # Verification is independent of price — record it either way.
            if (r.get("verified") or "").strip().lower() in ("yes", "y", "true", "1"):
                b["verified"] = True
            if (r.get("spec_url") or "").strip():
                b["spec_url"] = r["spec_url"].strip()

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
            snapshot.append({"id": bid, "price": price})

    if updated:
        # Anything hand-entered is 'manual', which clears the sample-data banner.
        if doc["meta"].get("price_source") == "sample":
            doc["meta"]["price_source"] = "manual"
            doc["meta"].pop("warning", None)
            print("price_source: sample -> manual")
        save(doc)
        n = append_history(snapshot, stamp)
        print(f"history  +{n} rows -> {HISTORY.name}")

    print(f"updated {updated} · skipped {skipped} · unknown {unknown}")
    return 0


# ---------- history ----------

def cmd_history(doc: dict) -> int:
    rows = read_history()
    if not rows:
        print("No history yet. It starts accumulating on your first --import-csv.\n"
              "This is the one asset a competitor starting later cannot copy — "
              "run the import on a schedule even during months when nothing changes.")
        return 0

    names = {b["id"]: f"{doc['platforms'][b['platform']]['brand']} {b['model']}"
             for b in doc["batteries"]}

    by_id: dict[str, list[dict]] = defaultdict(list)
    for r in rows:
        by_id[r["id"]].append(r)

    days = {r["t"][:10] for r in rows}
    print(f"{len(rows)} observations · {len(by_id)} batteries · "
          f"{len(days)} distinct days ({min(days)} .. {max(days)})\n")

    movers = []
    for bid, obs in by_id.items():
        if len(obs) < 2:
            continue
        obs.sort(key=lambda r: r["t"])
        first, last = obs[0]["price"], obs[-1]["price"]
        lo = min(o["price"] for o in obs)
        movers.append((abs(last - first), bid, first, last, lo))

    if not movers:
        print("Only one observation per battery so far — come back after a few imports.")
        return 0

    movers.sort(reverse=True)
    print(f"{'battery':<28} {'first':>9} {'latest':>9} {'change':>9} {'lowest seen':>12}")
    for _, bid, first, last, lo in movers[:15]:
        pct = (last - first) / first * 100
        flag = "  <= at its lowest" if abs(last - lo) < 0.005 else ""
        print(f"{names.get(bid, bid):<28} {first:>9.2f} {last:>9.2f} "
              f"{pct:>8.1f}% {lo:>12.2f}{flag}")
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
    g.add_argument("--history", action="store_true", help="summarise recorded price history")
    g.add_argument("--from-paapi", action="store_true", help="(stub) fetch from Amazon")
    args = ap.parse_args()

    doc = load()

    if args.check:
        return cmd_check(doc)
    if args.export_csv:
        return cmd_export(doc, Path(args.export_csv))
    if args.import_csv:
        return cmd_import(doc, Path(args.import_csv))
    if args.history:
        return cmd_history(doc)
    return cmd_paapi(doc)


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except BrokenPipeError:
        # Piping into head/less closes stdout early; that is not a failure.
        sys.stderr.close()
        raise SystemExit(0)
