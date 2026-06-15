"""Session E - Stage 1: parse all monitoring_b FIT files, build per-day
per-minute joins of stress + intensity, emit stress_low_motion_minutes.csv.

Per methodology/stress_low_motion_primitive.md.

Output schema:
  date, sample_count, valid,
  stress_low_motion_min_count_S50_Mstrict,
  stress_low_motion_min_count_S50_Mlow,
  stress_low_motion_min_count_S50_Mbelow_mod,
  stress_low_motion_min_count_S60_Mstrict,
  stress_low_motion_min_count_S60_Mlow,    (primary)
  stress_low_motion_min_count_S60_Mbelow_mod,
  stress_low_motion_min_count_S75_Mstrict,
  stress_low_motion_min_count_S75_Mlow,
  stress_low_motion_min_count_S75_Mbelow_mod

A day is "valid" when in-range stress sample_count >= 600
(matches HA11's coverage gate).

Definitions per methodology MD section 3.2:
  - M=strict_sedentary : intensity == 0 OR no monitoring record covers this minute
  - M=low_or_below     : intensity <= 1 OR no monitoring record covers this minute
  - M=any_below_moderate : currently equivalent to low_or_below (placeholder for
    future refinement; emitted as a separate column slot)

Per-minute join logic:
  - Stress samples are 1/min from `stress_level` messages with `stress_level_time`.
  - Intensity classifications come from `monitoring` messages with an `intensity`
    field; these are sparse and emitted at activity transitions. The intensity
    at a given minute is the most-recent intensity classification at or before
    that minute; if no record precedes the minute on the same day, the minute is
    treated as 'no record' (counts as low motion in all 3 classes).

This is the expensive stage. Cached to stress_low_motion_minutes.csv so
downstream consumers run in seconds.
"""
from __future__ import annotations

import bisect
import collections
import csv
import io
import sys
import zipfile
from datetime import date, datetime
from pathlib import Path

import fitdecode

# Path setup -- relative to this script's location.
# Script lives at <repo>/docs/research/pipeline/01_extract/; fit_utils lives at
# <repo>/docs/research/analyses/garmin_exploration/scripts/. From this script:
# parents: 01_extract -> pipeline -> research.
HERE = Path(__file__).resolve().parent
RESEARCH_ROOT = HERE.parent.parent  # <repo>/docs/research/
sys.path.insert(0, str(RESEARCH_ROOT / "analyses"
                       / "garmin_exploration" / "scripts"))
from fit_utils import Monitoring16Resolver  # noqa: E402

import os
DATA_ROOT = Path(os.environ.get("GEVOELSCORE_DATA_PATH",
                                r"C:\Users\Gebruiker\Documents\gevoelscore-data"))
if not DATA_ROOT.exists():
    print(f"ERROR: data path not found: {DATA_ROOT}", file=sys.stderr)
    sys.exit(1)

GARMIN_DUMP = DATA_ROOT / "garmin data" / "DI_CONNECT" / "DI-Connect-Uploaded-Files"
CLASSIFIED_CSV = DATA_ROOT / "analyses" / "garmin_exploration" / "fit_files_classified.csv"
OUT_DIR = DATA_ROOT / "processed" / "garmin"
OUT_CSV = OUT_DIR / "stress_low_motion_minutes.csv"

# Stress validity (matches HA11 and the methodology MD section 5)
STRESS_MIN_VALID = 1
STRESS_MAX_VALID = 100
MIN_SAMPLES_FOR_VALID_DAY = 600

# Sensitivity ladder per methodology MD section 4
STRESS_THRESHOLDS = [50, 60, 75]
MOTION_CLASSES = ["strict", "low", "below_mod"]

# Output column schema (9 stress-motion + 2 respiration companion)
COUNT_COLS = [
    f"stress_low_motion_min_count_S{s}_M{m}"
    for s in STRESS_THRESHOLDS
    for m in MOTION_CLASSES
]
RESP_COLS = ["n_minutes_resp_above_18", "n_minutes_resp_in_rest_band_10_18"]
ALL_COLS = ["date", "sample_count", "valid"] + COUNT_COLS + RESP_COLS

# Respiration validity range + thresholds (methodology MD section 4b)
RESP_MIN_VALID = 5
RESP_MAX_VALID = 40
RESP_REST_LOW = 10
RESP_REST_HIGH = 18  # also the "above_18" gate


def _classify_minute(intensity_at_minute: int | None) -> dict[str, bool]:
    """Return a dict of motion-class -> qualifies-as-low-motion."""
    if intensity_at_minute is None:
        # No monitoring record covers this minute: counts as low in all classes
        return {"strict": True, "low": True, "below_mod": True}
    return {
        "strict": intensity_at_minute == 0,
        "low": intensity_at_minute <= 1,
        "below_mod": intensity_at_minute <= 1,  # placeholder; identical to low
    }


def _process_day(
    stress_samples: list[tuple[datetime, int]],
    intensity_samples: list[tuple[datetime, int]],
    respiration_samples: list[tuple[datetime, float]],
) -> dict[str, int]:
    """Compute the 9 per-day stress-motion counts + 2 respiration
    companion counts + sample_count + valid flag.

    `stress_samples` is a list of (timestamp, stress_level_value) tuples.
    `intensity_samples` is a list of (timestamp, intensity) tuples, sorted.
    `respiration_samples` is a list of (timestamp, respiration_rate) tuples.
    """
    # Filter in-range stress samples
    in_range = [(t, v) for (t, v) in stress_samples
                if STRESS_MIN_VALID <= v <= STRESS_MAX_VALID]
    # Dedupe to per-minute (keep latest reading in each minute slot)
    by_min: dict[datetime, int] = {}
    for (t, v) in in_range:
        tm = t.replace(second=0, microsecond=0)
        by_min[tm] = v
    sample_count = len(by_min)
    valid = 1 if sample_count >= MIN_SAMPLES_FOR_VALID_DAY else 0

    counts = {col: 0 for col in COUNT_COLS}
    resp_counts = {col: 0 for col in RESP_COLS}
    if not valid:
        return {"sample_count": sample_count, "valid": valid,
                **counts, **resp_counts}

    # Respiration per-day counts (independent of stress; per methodology MD section 4b)
    resp_by_min: dict[datetime, float] = {}
    for (t, v) in respiration_samples:
        try:
            vf = float(v)
        except (TypeError, ValueError):
            continue
        if not (RESP_MIN_VALID <= vf <= RESP_MAX_VALID):
            continue
        tm = t.replace(second=0, microsecond=0)
        resp_by_min[tm] = vf
    for vf in resp_by_min.values():
        if vf > RESP_REST_HIGH:
            resp_counts["n_minutes_resp_above_18"] += 1
        if RESP_REST_LOW <= vf <= RESP_REST_HIGH:
            resp_counts["n_minutes_resp_in_rest_band_10_18"] += 1

    # Build a sorted intensity timeline for bisect lookup
    intensity_samples_sorted = sorted(intensity_samples, key=lambda x: x[0])
    intensity_times = [t for (t, _) in intensity_samples_sorted]
    intensity_values = [v for (_, v) in intensity_samples_sorted]

    for (tm, stress_value) in by_min.items():
        # Find most-recent intensity at or before this minute
        # bisect_right gives insertion point for tm in intensity_times;
        # the most-recent at-or-before is at index (i-1)
        i = bisect.bisect_right(intensity_times, tm)
        intensity_at_minute = intensity_values[i - 1] if i > 0 else None
        motion_qualifies = _classify_minute(intensity_at_minute)
        for s in STRESS_THRESHOLDS:
            if stress_value >= s:
                for m in MOTION_CLASSES:
                    if motion_qualifies[m]:
                        counts[f"stress_low_motion_min_count_S{s}_M{m}"] += 1

    return {"sample_count": sample_count, "valid": valid,
            **counts, **resp_counts}


def main() -> int:
    if not CLASSIFIED_CSV.exists():
        print(f"ERROR: {CLASSIFIED_CSV} not found", file=sys.stderr)
        return 1
    with CLASSIFIED_CSV.open(encoding="utf-8") as fh:
        rows = list(csv.DictReader(fh))
    mfiles = [r for r in rows if r["type"] == "monitoring_b"]
    print(f"monitoring_b files to parse: {len(mfiles)}", file=sys.stderr)

    open_zips: dict[str, zipfile.ZipFile] = {}
    for z in {r["zip"] for r in mfiles}:
        open_zips[z] = zipfile.ZipFile(GARMIN_DUMP / z)

    # date -> stress, intensity, respiration samples
    stress_by_date: dict[date, list[tuple[datetime, int]]] = collections.defaultdict(list)
    intensity_by_date: dict[date, list[tuple[datetime, int]]] = collections.defaultdict(list)
    resp_by_date: dict[date, list[tuple[datetime, float]]] = collections.defaultdict(list)

    for i, r in enumerate(mfiles):
        if i % 500 == 0:
            print(f"  parsed {i}/{len(mfiles)} files", file=sys.stderr)
        try:
            buf = open_zips[r["zip"]].read(r["filename"])
            resolver = Monitoring16Resolver()
            with fitdecode.FitReader(io.BytesIO(buf)) as fit:
                for frame in fit:
                    if not isinstance(frame, fitdecode.FitDataMessage):
                        continue
                    if frame.name == "monitoring_info":
                        for f in frame.fields:
                            if f.name == "timestamp" and isinstance(f.value, datetime):
                                resolver.set_reference(f.value)
                    elif frame.name == "stress_level":
                        ts = next((f.value for f in frame.fields
                                   if f.name == "stress_level_time"
                                   and isinstance(f.value, datetime)), None)
                        val = next((f.value for f in frame.fields
                                    if f.name == "stress_level_value"), None)
                        if ts is None or val is None:
                            continue
                        try:
                            v = int(val)
                        except (TypeError, ValueError):
                            continue
                        stress_by_date[ts.date()].append((ts, v))
                    elif frame.name == "monitoring":
                        # Resolve timestamp (uses full timestamp if present;
                        # falls back to timestamp_16 against rolling reference)
                        ts = resolver.resolve_frame(frame)
                        intensity_val = next((f.value for f in frame.fields
                                              if f.name == "intensity"), None)
                        if ts is None or intensity_val is None:
                            continue
                        try:
                            iv = int(intensity_val)
                        except (TypeError, ValueError):
                            continue
                        intensity_by_date[ts.date()].append((ts, iv))
                    elif frame.name == "respiration_rate":
                        ts = next((f.value for f in frame.fields
                                   if f.name == "timestamp"
                                   and isinstance(f.value, datetime)), None)
                        v = next((f.value for f in frame.fields
                                  if f.name == "respiration_rate"), None)
                        if ts is None or v is None:
                            continue
                        try:
                            vf = float(v)
                        except (TypeError, ValueError):
                            continue
                        resp_by_date[ts.date()].append((ts, vf))
        except Exception as e:
            print(f"  warn: failed {r['filename']}: {e}", file=sys.stderr)
            continue

    print(f"parsed {len(stress_by_date)} dates with stress samples", file=sys.stderr)
    print(f"parsed {len(intensity_by_date)} dates with intensity samples", file=sys.stderr)
    print(f"parsed {len(resp_by_date)} dates with respiration samples", file=sys.stderr)

    # Compute per-day counts
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    out_rows: list[dict] = []
    all_dates = sorted(stress_by_date.keys())
    for d in all_dates:
        result = _process_day(
            stress_by_date[d],
            intensity_by_date.get(d, []),
            resp_by_date.get(d, []),
        )
        out_rows.append({"date": d.isoformat(), **result})

    with OUT_CSV.open("w", encoding="utf-8", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=ALL_COLS)
        w.writeheader()
        for r in out_rows:
            w.writerow(r)

    n_valid = sum(1 for r in out_rows if r["valid"])
    primary_col = "stress_low_motion_min_count_S60_Mlow"
    primary_total = sum(r[primary_col] for r in out_rows if r["valid"])
    primary_nonzero = sum(1 for r in out_rows if r["valid"] and r[primary_col] > 0)
    print(f"Wrote {OUT_CSV} ({len(out_rows)} days, {n_valid} valid)", file=sys.stderr)
    print(f"  primary col {primary_col}: total {primary_total} qualifying minutes "
          f"across {primary_nonzero} non-zero days", file=sys.stderr)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
