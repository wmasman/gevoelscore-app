"""Extract per-day nested-object UDS fields not covered by daily_uds.csv.

Reads UDSFile_*.json from the Garmin GDPR dump and writes one row per
calendar date with Body Battery, all-day stress, respiration, and
SpO2 fields.

These are JSON-level metrics. No FIT parsing. The fields are named in
the UDS JSON; no reverse-engineering involved.

Output: $GEVOELSCORE_DATA_PATH/processed/garmin/uds_extras_daily.csv

Coverage: from 2021-08-16 (earliest UDS file) onward, per the
re-extract-from-earliest-coverage convention (memory:
`feedback_garmin_reextract_from_2021_08_16`).

Field mapping:
- bodyBattery.chargedValue / drainedValue                   -> bb_charged_24h, bb_drained_24h
- bodyBattery.bodyBatteryStatList[HIGHEST/LOWEST/...]       -> bb_highest, bb_lowest, bb_sleep_start_value, bb_sleep_end_value, bb_during_sleep_value
- derived bb_overnight_gain = sleep_end - sleep_start
- allDayStress.aggregatorList[TOTAL/AWAKE/ASLEEP]           -> all_day_stress_avg/max, awake_stress_avg/max, asleep_stress_avg_uds
- respiration.{avgWakingRespirationValue,highest,lowest}    -> respiration_avg_waking, respiration_max_24h, respiration_min_24h
- averageSpo2Value, lowestSpo2Value                         -> spo2_avg_24h, spo2_min_24h
"""
from __future__ import annotations

import csv
import json
import os
from pathlib import Path

# --- Resolve $GEVOELSCORE_DATA_PATH from .env or env ---
HERE = Path(__file__).resolve().parent
# docs/research/pipeline/01_extract -> 01_extract -> pipeline -> research -> docs -> repo
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

UDS_DIR = DATA_ROOT.parent / "gevoelscore-data" / "garmin data" / "DI_CONNECT" / "DI-Connect-Aggregator"
# If DATA_ROOT itself IS the gevoelscore-data folder, the line above adds an
# extra hop. Tolerate both layouts.
if not UDS_DIR.exists():
    UDS_DIR = DATA_ROOT / "garmin data" / "DI_CONNECT" / "DI-Connect-Aggregator"
if not UDS_DIR.exists():
    raise SystemExit(f"UDS dir not found, tried: {UDS_DIR}")

OUT = DATA_ROOT / "processed" / "garmin" / "uds_extras_daily.csv"

FIELDS = [
    "date",
    # Body Battery
    "bb_charged_24h", "bb_drained_24h",
    "bb_highest", "bb_lowest",
    "bb_sleep_start_value", "bb_sleep_end_value",
    "bb_during_sleep_value", "bb_overnight_gain",
    # All-day stress (3 aggregator types)
    "all_day_stress_avg", "all_day_stress_max",
    "awake_stress_avg", "awake_stress_max",
    "asleep_stress_avg_uds",
    # Respiration (24h / waking)
    "respiration_avg_waking", "respiration_max_24h", "respiration_min_24h",
    # SpO2 (24h)
    "spo2_avg_24h", "spo2_min_24h",
]


def _bb_stat(stat_list: list[dict], stat_type: str):
    """Return statsValue for a given bodyBatteryStatType, or None."""
    if not isinstance(stat_list, list):
        return None
    for s in stat_list:
        if isinstance(s, dict) and s.get("bodyBatteryStatType") == stat_type:
            return s.get("statsValue")
    return None


def _stress_agg(agg_list: list[dict], agg_type: str) -> dict:
    """Return the aggregator dict for a given type (TOTAL / AWAKE / ASLEEP), or {}."""
    if not isinstance(agg_list, list):
        return {}
    for a in agg_list:
        if isinstance(a, dict) and a.get("type") == agg_type:
            return a
    return {}


def parse_one(p: Path) -> list[dict]:
    raw = json.loads(p.read_text(encoding="utf-8"))
    rows = []
    for item in raw:
        cd = item.get("calendarDate")
        if not cd:
            continue
        row = {f: None for f in FIELDS}
        row["date"] = cd

        # Body Battery
        bb = item.get("bodyBattery") or {}
        if isinstance(bb, dict):
            row["bb_charged_24h"] = bb.get("chargedValue")
            row["bb_drained_24h"] = bb.get("drainedValue")
            sl = bb.get("bodyBatteryStatList") or []
            row["bb_highest"] = _bb_stat(sl, "HIGHEST")
            row["bb_lowest"] = _bb_stat(sl, "LOWEST")
            ss = _bb_stat(sl, "SLEEPSTART")
            se = _bb_stat(sl, "SLEEPEND")
            row["bb_sleep_start_value"] = ss
            row["bb_sleep_end_value"] = se
            row["bb_during_sleep_value"] = _bb_stat(sl, "DURINGSLEEP")
            if ss is not None and se is not None:
                row["bb_overnight_gain"] = se - ss

        # All-day stress
        ads = item.get("allDayStress") or {}
        if isinstance(ads, dict):
            al = ads.get("aggregatorList") or []
            total = _stress_agg(al, "TOTAL")
            awake = _stress_agg(al, "AWAKE")
            asleep = _stress_agg(al, "ASLEEP")
            row["all_day_stress_avg"] = total.get("averageStressLevel")
            row["all_day_stress_max"] = total.get("maxStressLevel")
            row["awake_stress_avg"] = awake.get("averageStressLevel")
            row["awake_stress_max"] = awake.get("maxStressLevel")
            row["asleep_stress_avg_uds"] = asleep.get("averageStressLevel")

        # Respiration
        rsp = item.get("respiration") or {}
        if isinstance(rsp, dict):
            row["respiration_avg_waking"] = rsp.get("avgWakingRespirationValue")
            row["respiration_max_24h"] = rsp.get("highestRespirationValue")
            row["respiration_min_24h"] = rsp.get("lowestRespirationValue")

        # SpO2
        row["spo2_avg_24h"] = item.get("averageSpo2Value")
        row["spo2_min_24h"] = item.get("lowestSpo2Value")

        rows.append(row)
    return rows


def main():
    files = sorted(UDS_DIR.glob("UDSFile_*.json"))
    if not files:
        raise SystemExit(f"No UDS files found in {UDS_DIR}")
    print(f"Reading {len(files)} UDS files from {UDS_DIR}")
    all_rows: dict[str, dict] = {}
    for p in files:
        for r in parse_one(p):
            # Dedupe by date; later wins (files may overlap dates across
            # quarterly boundaries).
            all_rows[r["date"]] = r
    rows = sorted(all_rows.values(), key=lambda r: r["date"])
    OUT.parent.mkdir(parents=True, exist_ok=True)
    with OUT.open("w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=FIELDS)
        w.writeheader()
        for r in rows:
            # Convert None to "" for CSV cleanliness
            w.writerow({k: ("" if v is None else v) for k, v in r.items()})
    print(f"Wrote {len(rows)} rows to {OUT}")
    # Quick fill-rate summary
    print("\nFill rates:")
    for f in FIELDS[1:]:
        n = sum(1 for r in rows if r[f] is not None)
        print(f"  {f}: {n}/{len(rows)} ({100*n/len(rows):.1f}%)")


if __name__ == "__main__":
    main()
