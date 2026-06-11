"""HA07c/HA08c/HA07d Stage 1 - Per-night sleep-window stress aggregates.

Re-parses all monitoring_b FIT files for per-minute stress samples
(same as H02b/HA11 extraction); for each calendar day, intersects
with the sleep window from the local sleepData.json files; emits
per-night sleep_stress_mean + sleep_stress_stdev + sample_count.

Output schema:
  date, sleep_start_gmt, sleep_end_gmt, n_samples,
  stress_mean, stress_stdev, valid
where valid = 1 if n_samples >= MIN_SAMPLES_PER_NIGHT (120).

Sleep windows: from DI-Connect-Wellness/*_sleepData.json (local
GDPR dump, full corpus 2021-08 -> 2026-05).

This is the expensive stage (~7 min). Cached to sleep_stress_nightly.csv
so test.py runs in seconds.

USAGE:
  python extract_sleep_stress.py
"""
from __future__ import annotations

import collections
import csv
import io
import json
import statistics
import sys
import zipfile
from datetime import date, datetime, timedelta, timezone
from pathlib import Path

import fitdecode

GARMIN_DUMP = Path(
    r"C:\Users\Gebruiker\Documents\gevoelscore-data\garmin data\DI_CONNECT\DI-Connect-Uploaded-Files"
)
WELLNESS_DIR = Path(
    r"C:\Users\Gebruiker\Documents\gevoelscore-data\garmin data\DI_CONNECT\DI-Connect-Wellness"
)
CLASSIFIED_CSV = (
    Path(__file__).resolve().parents[2] / "output" / "fit_files_classified.csv"
)
OUT_CSV = Path(__file__).resolve().parent / "sleep_stress_nightly.csv"

STRESS_MIN_VALID = 1
STRESS_MAX_VALID = 100
MIN_SAMPLES_PER_NIGHT = 120  # ~6h at per-3min cadence


def load_sleep_windows() -> dict[date, tuple[datetime, datetime]]:
    """Returns mapping calendar_date -> (sleep_start_utc, sleep_end_utc)."""
    out: dict[date, tuple[datetime, datetime]] = {}
    for p in sorted(WELLNESS_DIR.glob("*_sleepData.json")):
        try:
            with p.open(encoding="utf-8") as fh:
                data = json.load(fh)
        except Exception as e:
            print(f"  warn: failed to load {p.name}: {e}", file=sys.stderr)
            continue
        if not isinstance(data, list):
            continue
        for rec in data:
            cd = rec.get("calendarDate")
            ss = rec.get("sleepStartTimestampGMT")
            se = rec.get("sleepEndTimestampGMT")
            if not (cd and ss and se):
                continue
            try:
                d = date.fromisoformat(cd)
                # Garmin format: "2022-09-02T23:00:00.0" (with .0 for fractional seconds)
                # Treat as UTC (the GMT suffix)
                s_dt = datetime.fromisoformat(ss.replace(".0", "")).replace(tzinfo=timezone.utc)
                e_dt = datetime.fromisoformat(se.replace(".0", "")).replace(tzinfo=timezone.utc)
            except Exception:
                continue
            if d in out:
                # Multiple records for same date (rare) - keep the longer window
                existing = out[d]
                if (e_dt - s_dt) > (existing[1] - existing[0]):
                    out[d] = (s_dt, e_dt)
            else:
                out[d] = (s_dt, e_dt)
    return out


def main() -> int:
    if not CLASSIFIED_CSV.exists():
        print(f"ERROR: {CLASSIFIED_CSV} not found", file=sys.stderr)
        return 1

    print("Loading sleep windows from local sleepData.json...", file=sys.stderr)
    sleep_windows = load_sleep_windows()
    print(f"  {len(sleep_windows)} dates with sleep windows", file=sys.stderr)

    with CLASSIFIED_CSV.open(encoding="utf-8") as fh:
        rows = list(csv.DictReader(fh))
    mfiles = [r for r in rows if r["type"] == "monitoring_b"]
    print(f"monitoring_b files to parse: {len(mfiles)}", file=sys.stderr)

    open_zips: dict[str, zipfile.ZipFile] = {}
    for z in {r["zip"] for r in mfiles}:
        open_zips[z] = zipfile.ZipFile(GARMIN_DUMP / z)

    # cal_date -> [(timestamp_utc, value), ...]
    # Key by the calendar date the timestamp falls into based on its sleep window
    # (i.e. the calendar date where sleep_window[d-1] -> sleep_window[d] contains it)
    # We assign each sample to whatever sleep window contains it (if any).
    by_date: dict[date, list[int]] = collections.defaultdict(list)

    for i, r in enumerate(mfiles):
        if i % 500 == 0:
            print(f"  parsed {i}/{len(mfiles)} files", file=sys.stderr)
        try:
            buf = open_zips[r["zip"]].read(r["filename"])
            with fitdecode.FitReader(io.BytesIO(buf)) as fit:
                for frame in fit:
                    if not isinstance(frame, fitdecode.FitDataMessage):
                        continue
                    if frame.name != "stress_level":
                        continue
                    ts_field = next(
                        (f for f in frame.fields if f.name == "stress_level_time"),
                        None,
                    )
                    val_field = next(
                        (f for f in frame.fields if f.name == "stress_level_value"),
                        None,
                    )
                    if ts_field is None or val_field is None:
                        continue
                    ts = ts_field.value
                    val = val_field.value
                    if ts is None or val is None or not isinstance(ts, datetime):
                        continue
                    try:
                        v = int(val)
                    except (TypeError, ValueError):
                        continue
                    if v < STRESS_MIN_VALID or v > STRESS_MAX_VALID:
                        continue
                    # Make ts timezone-aware UTC (fitdecode returns naive UTC)
                    if ts.tzinfo is None:
                        ts = ts.replace(tzinfo=timezone.utc)
                    # Bucket by the date whose sleep window contains this ts.
                    # Garmin's calendar_date convention: a sleep at 2025-08-02 22:00
                    # GMT belongs to calendar_date 2025-08-03. We use the local
                    # sleepData.json mappings directly: walk the date range of
                    # plausible calendar dates (today and tomorrow) and check.
                    ts_date = ts.date()
                    for candidate in (ts_date, ts_date + timedelta(days=1)):
                        win = sleep_windows.get(candidate)
                        if win and win[0] <= ts < win[1]:
                            by_date[candidate].append(v)
                            break
        except Exception as e:
            print(f"  warn: failed {r['filename']}: {e}", file=sys.stderr)
            continue

    print(f"parsed sleep-window samples for {len(by_date)} dates", file=sys.stderr)

    # Emit per-night CSV
    out_rows: list[dict] = []
    for d in sorted(sleep_windows.keys()):
        samples = by_date.get(d, [])
        n = len(samples)
        valid = 1 if n >= MIN_SAMPLES_PER_NIGHT else 0
        if valid:
            mean = statistics.mean(samples)
            sd = statistics.stdev(samples) if n > 1 else 0.0
        else:
            mean = sd = None
        win = sleep_windows[d]
        out_rows.append({
            "date": d.isoformat(),
            "sleep_start_gmt": win[0].isoformat(),
            "sleep_end_gmt": win[1].isoformat(),
            "n_samples": n,
            "stress_mean": round(mean, 4) if mean is not None else "",
            "stress_stdev": round(sd, 4) if sd is not None else "",
            "valid": valid,
        })

    with OUT_CSV.open("w", encoding="utf-8", newline="") as fh:
        w = csv.DictWriter(
            fh,
            fieldnames=["date", "sleep_start_gmt", "sleep_end_gmt", "n_samples",
                        "stress_mean", "stress_stdev", "valid"],
        )
        w.writeheader()
        for r in out_rows:
            w.writerow(r)

    n_valid = sum(1 for r in out_rows if r["valid"])
    mean_n = statistics.mean(r["n_samples"] for r in out_rows if r["valid"]) if n_valid else 0
    print(f"Wrote {OUT_CSV} ({len(out_rows)} nights, {n_valid} valid, "
          f"mean samples/valid-night: {mean_n:.0f})", file=sys.stderr)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
