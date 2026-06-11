"""H04b Path C - Sleep data backfill.

Pulls get_sleep_data() for every date in the analysis window via
the Garmin Connect REST API. ONE endpoint provides everything we
need for H03b + HA07c + HA08c + HA07d:

  - bodyBatteryChange (overnight recharge integral) -> H03b primary
  - sleepStress array (per-window stress during sleep) -> HA07c/HA08c/HA07d
  - sleepBodyBattery array (per-window BB during sleep) -> H03b trajectory
  - sleepStartTimestampGMT/EndTimestampGMT (sleep window) -> validity gate
  - restingHeartRate (cross-check with UDS) -> sanity
  - sleepHeartRate array (per-window HR during sleep) -> not used now
    but cached for future tests

Resumable: skips dates already cached. Conservative rate limit
(5s between requests). Sequential pull; ~1700 dates -> ~2.5h.

USAGE:
  python backfill_sleep.py
    pulls 2022-09-03 -> 2026-06-05 inclusive

  python backfill_sleep.py 2023-01-01 2023-12-31
    pulls a date range

Cache location:
  C:\\Users\\Gebruiker\\Documents\\gevoelscore-data\\garmin
  data\\api_pull\\sleep\\YYYY-MM\\YYYY-MM-DD.json

Each per-day JSON contains the raw API response (extracted fields
only, to keep file sizes manageable).
"""
from __future__ import annotations

import argparse
import json
import os
import sys
import time
from datetime import date, timedelta
from pathlib import Path

try:
    from garminconnect import Garmin
except ImportError:
    print("ERROR: garminconnect not installed.", file=sys.stderr)
    sys.exit(1)

TOKEN_DIR = Path.home() / ".garminconnect_tokens"
CACHE_ROOT = Path(
    r"C:\Users\Gebruiker\Documents\gevoelscore-data\garmin data\api_pull\sleep"
)
DEFAULT_START = date(2022, 9, 3)
DEFAULT_END = date(2026, 6, 5)

# Rate limit
SLEEP_BETWEEN_REQUESTS_S = 5.0
RETRY_BACKOFF_S = 30.0
MAX_RETRIES_PER_DAY = 3

# Field allowlist - only cache what we'll use
FIELDS_TO_CACHE = [
    "bodyBatteryChange",
    "restingHeartRate",
    "sleepBodyBattery",
    "sleepStress",
    "sleepHeartRate",
    "wellnessEpochRespirationDataDTOList",
]
DAILY_DTO_FIELDS = [
    "calendarDate",
    "sleepStartTimestampGMT",
    "sleepEndTimestampGMT",
    "sleepStartTimestampLocal",
    "sleepEndTimestampLocal",
    "sleepTimeSeconds",
    "deepSleepSeconds",
    "lightSleepSeconds",
    "remSleepSeconds",
    "awakeSleepSeconds",
    "sleepWindowConfirmationType",
    "sleepWindowConfirmed",
    "napTimeSeconds",
]


def extract_record(raw: dict) -> dict:
    """Pull only the fields we'll use, to keep cache files compact."""
    out: dict = {}
    for k in FIELDS_TO_CACHE:
        if k in raw:
            out[k] = raw[k]
    dto = raw.get("dailySleepDTO")
    if isinstance(dto, dict):
        out["dailySleepDTO"] = {k: dto.get(k) for k in DAILY_DTO_FIELDS if k in dto}
    return out


def cache_path_for(d: date) -> Path:
    return CACHE_ROOT / d.strftime("%Y-%m") / f"{d.isoformat()}.json"


def pull_day(client: Garmin, d: date) -> tuple[str, dict | None]:
    """Returns (status, payload). Status in {ok, empty, error}."""
    try:
        raw = client.get_sleep_data(d.isoformat())
    except Exception as e:
        return ("error", {"error": str(e)})
    if not raw:
        return ("empty", None)
    rec = extract_record(raw)
    if not rec:
        return ("empty", None)
    return ("ok", rec)


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("start", nargs="?", default=DEFAULT_START.isoformat())
    ap.add_argument("end", nargs="?", default=DEFAULT_END.isoformat())
    args = ap.parse_args()
    start = date.fromisoformat(args.start)
    end = date.fromisoformat(args.end)
    if start > end:
        print("ERROR: start > end", file=sys.stderr)
        return 1

    CACHE_ROOT.mkdir(parents=True, exist_ok=True)
    if not TOKEN_DIR.exists():
        print(f"ERROR: no tokens at {TOKEN_DIR}. Run setup_auth.py first.",
              file=sys.stderr)
        return 1

    print(f"Backfill window: {start} -> {end} ({(end - start).days + 1} days)")
    print(f"Cache: {CACHE_ROOT}")
    print(f"Rate limit: {SLEEP_BETWEEN_REQUESTS_S}s between requests")
    print(f"Expected wall time: ~{(end - start).days * SLEEP_BETWEEN_REQUESTS_S / 60:.0f} min")
    print()

    client = Garmin()
    try:
        client.login(tokenstore=str(TOKEN_DIR))
    except Exception as e:
        print(f"LOGIN FAILED: {e}", file=sys.stderr)
        return 1

    n_ok = 0
    n_skip = 0
    n_empty = 0
    n_error = 0
    d = start
    total = (end - start).days + 1
    seen = 0
    t0 = time.time()
    while d <= end:
        seen += 1
        out_path = cache_path_for(d)
        if out_path.exists():
            n_skip += 1
            d += timedelta(days=1)
            continue

        # Pull with retry
        status = "error"
        payload = None
        for attempt in range(MAX_RETRIES_PER_DAY):
            status, payload = pull_day(client, d)
            if status != "error":
                break
            # Backoff on error (often 429 or transient)
            err_msg = str(payload.get("error", ""))[:80] if payload else ""
            print(f"  {d.isoformat()} attempt {attempt+1}: error -- {err_msg}",
                  file=sys.stderr)
            time.sleep(RETRY_BACKOFF_S * (attempt + 1))

        if status == "ok":
            out_path.parent.mkdir(parents=True, exist_ok=True)
            out_path.write_text(json.dumps(payload, default=str), encoding="utf-8")
            n_ok += 1
        elif status == "empty":
            # Cache as empty so we don't retry
            out_path.parent.mkdir(parents=True, exist_ok=True)
            out_path.write_text("{}", encoding="utf-8")
            n_empty += 1
        else:
            n_error += 1

        # Progress every 50 days
        if seen % 50 == 0 or seen == total:
            elapsed = time.time() - t0
            rate = seen / elapsed if elapsed > 0 else 0
            eta_s = (total - seen) / rate if rate > 0 else 0
            print(f"  [{seen}/{total}] {d.isoformat()} "
                  f"ok={n_ok} skip={n_skip} empty={n_empty} err={n_error} "
                  f"eta={eta_s/60:.0f}min", flush=True)

        time.sleep(SLEEP_BETWEEN_REQUESTS_S)
        d += timedelta(days=1)

    print(f"\nDone. ok={n_ok} skip={n_skip} empty={n_empty} err={n_error}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
