"""Extract per-night sleep-extra fields from sleepData.json.

Companion to `extract_sleep_stress.py` (which extracts the stress
samples within the sleep window from FIT files). This script reads
the named JSON fields in `*_sleepData.json` that are already
flattened by Garmin Connect: sleep stages, sleep-window respiration,
sleep-window SpO2.

These are JSON-level metrics. No FIT parsing.

Output: $GEVOELSCORE_DATA_PATH/processed/garmin/sleep_extras_daily.csv

Coverage: from 2021-06-25 (earliest sleepData file) onward, per the
re-extract-from-earliest-coverage convention (memory:
`feedback_garmin_reextract_from_2021_08_16`). Garmin's `calendarDate`
is the wake-up date — the wake-up-date attribution convention used
by the rest of the master.

Field mapping:
- deepSleepSeconds / 60                                  -> sleep_deep_min
- lightSleepSeconds / 60                                 -> sleep_light_min
- remSleepSeconds / 60                                   -> sleep_rem_min
- awakeSleepSeconds / 60                                 -> sleep_awake_min
- unmeasurableSeconds / 60                               -> sleep_unmeasurable_min
- averageRespiration / highestRespiration / lowestRespiration  -> respiration_avg_sleep, _max_sleep, _min_sleep
- spo2SleepSummary.averageSPO2                           -> spo2_avg_sleep
- spo2SleepSummary.lowestSPO2                            -> spo2_min_sleep
- spo2SleepSummary.averageHR                             -> sleep_hr_avg_spo2
- sleepWindowConfirmationType                            -> sleep_window_confirmation_type

Note on REM: an earlier version of this extractor asserted that the
Forerunner 245 does not produce REM-stage classification. That assertion
was incorrect on this corpus. `remSleepSeconds` is present at 97.2%
coverage across LC-era nights (1685/1734, mean 115.6 min, range 5-287),
so `sleep_rem_min` IS emitted. The ~2.8% gap corresponds to nights where
Garmin fell back to the deep/light/awake-only classifier.

`sleep_window_confirmation_type` is the Garmin sleep-window validity
flag (ENHANCED_CONFIRMED, ENHANCED_CONFIRMED_FINAL, UNCONFIRMED,
AUTO_CONFIRMED_FINAL, OFF_WRIST, AUTO_CONFIRMED) — a validity gate for
downstream analyses that need to exclude non-confirmed windows.

`sleep_hr_avg_spo2` is the overnight-average HR reported inside the
spo2SleepSummary block (95% coverage). Overnight HR proxy for cardiac
autonomic contrasts; complements resting_hr (which is a daily value).
"""
from __future__ import annotations

import csv
import json
import os
from pathlib import Path

HERE = Path(__file__).resolve().parent
REPO_ROOT = HERE.parent.parent.parent.parent


def _load_env_file(env_path: Path) -> None:
    if not env_path.exists():
        return
    for line in env_path.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        k, _, v = line.partition("=")
        k = k.strip()
        v = v.strip().strip('"').strip("'")
        if k and k not in os.environ:
            os.environ[k] = v


_load_env_file(REPO_ROOT / ".env")
DATA_ROOT = Path(os.environ.get("GEVOELSCORE_DATA_PATH", ""))
if not DATA_ROOT or not DATA_ROOT.exists():
    raise SystemExit("GEVOELSCORE_DATA_PATH not set or does not exist.")

WELLNESS_DIR = DATA_ROOT / "garmin data" / "DI_CONNECT" / "DI-Connect-Wellness"
if not WELLNESS_DIR.exists():
    raise SystemExit(f"Wellness dir not found: {WELLNESS_DIR}")

OUT = DATA_ROOT / "processed" / "garmin" / "sleep_extras_daily.csv"

FIELDS = [
    "date",
    "sleep_deep_min", "sleep_light_min", "sleep_rem_min",
    "sleep_awake_min", "sleep_unmeasurable_min",
    "respiration_avg_sleep", "respiration_max_sleep", "respiration_min_sleep",
    "spo2_avg_sleep", "spo2_min_sleep",
    "sleep_hr_avg_spo2",
    "sleep_window_confirmation_type",
]


def _sec_to_min(v):
    if v is None:
        return None
    try:
        return round(float(v) / 60, 1)
    except (ValueError, TypeError):
        return None


def parse_one(p: Path) -> list[dict]:
    try:
        data = json.loads(p.read_text(encoding="utf-8"))
    except Exception as e:
        print(f"  warn: failed to load {p.name}: {e}")
        return []
    if not isinstance(data, list):
        return []
    rows = []
    for item in data:
        cd = item.get("calendarDate")
        if not cd:
            continue
        row = {f: None for f in FIELDS}
        row["date"] = cd

        # Sleep stages (sec -> min)
        row["sleep_deep_min"] = _sec_to_min(item.get("deepSleepSeconds"))
        row["sleep_light_min"] = _sec_to_min(item.get("lightSleepSeconds"))
        row["sleep_rem_min"] = _sec_to_min(item.get("remSleepSeconds"))
        row["sleep_awake_min"] = _sec_to_min(item.get("awakeSleepSeconds"))
        row["sleep_unmeasurable_min"] = _sec_to_min(item.get("unmeasurableSeconds"))

        # Sleep-window respiration
        row["respiration_avg_sleep"] = item.get("averageRespiration")
        row["respiration_max_sleep"] = item.get("highestRespiration")
        row["respiration_min_sleep"] = item.get("lowestRespiration")

        # Sleep-window SpO2 (+ overnight HR from same block)
        sp = item.get("spo2SleepSummary") or {}
        if isinstance(sp, dict):
            row["spo2_avg_sleep"] = sp.get("averageSPO2")
            row["spo2_min_sleep"] = sp.get("lowestSPO2")
            row["sleep_hr_avg_spo2"] = sp.get("averageHR")

        # Sleep-window validity gate (Garmin's own confirmation label)
        row["sleep_window_confirmation_type"] = item.get("sleepWindowConfirmationType")

        rows.append(row)
    return rows


def main():
    files = sorted(WELLNESS_DIR.glob("*_sleepData.json"))
    if not files:
        raise SystemExit(f"No sleepData files found in {WELLNESS_DIR}")
    print(f"Reading {len(files)} sleepData files from {WELLNESS_DIR}")
    all_rows: dict[str, dict] = {}
    for p in files:
        for r in parse_one(p):
            # Dedupe by date; later wins (files overlap at quarter boundaries).
            all_rows[r["date"]] = r
    rows = sorted(all_rows.values(), key=lambda r: r["date"])
    OUT.parent.mkdir(parents=True, exist_ok=True)
    with OUT.open("w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=FIELDS)
        w.writeheader()
        for r in rows:
            w.writerow({k: ("" if v is None else v) for k, v in r.items()})
    print(f"Wrote {len(rows)} rows to {OUT}")
    print("\nFill rates:")
    for f in FIELDS[1:]:
        n = sum(1 for r in rows if r[f] is not None)
        print(f"  {f}: {n}/{len(rows)} ({100*n/len(rows):.1f}%)")


if __name__ == "__main__":
    main()
