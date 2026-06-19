"""Single-day per-minute FIT re-parse, adapted from
docs/research/pipeline/01_extract/stress_low_motion_extract.py.

Given a target date, find the monitoring_b FIT files that overlap, walk them
once, and return per-minute records covering that day. Used by Family A.
"""
from __future__ import annotations

import bisect
import collections
import io
import sys
import zipfile
from datetime import date, datetime, timedelta
from pathlib import Path

import fitdecode
import pandas as pd

from _master_loader import DATA_ROOT, FIT_DIR, FIT_INDEX_CSV

# fit_utils lives at <repo>/docs/research/analyses/garmin_exploration/scripts/
_REPO = Path(r"C:\Users\Gebruiker\Documents\gevoelscore-app")
sys.path.insert(0, str(_REPO / "docs" / "research" / "analyses"
                       / "garmin_exploration" / "scripts"))
from fit_utils import Monitoring16Resolver  # noqa: E402


STRESS_MIN_VALID = 1
STRESS_MAX_VALID = 100
RESP_MIN_VALID = 5
RESP_MAX_VALID = 40


def _candidate_files(target: date, buffer_days: int = 10) -> list[dict]:
    """Filter the FIT classified index to monitoring_b files whose time_created
    is within buffer_days of the target date. Returns the candidate rows."""
    idx = pd.read_csv(FIT_INDEX_CSV)
    monb = idx[idx["type"] == "monitoring_b"].copy()
    monb["time_created"] = pd.to_datetime(monb["time_created"], errors="coerce", utc=True)
    target_ts = pd.Timestamp(target, tz="UTC")
    delta = (monb["time_created"] - target_ts).abs()
    keep = monb[delta <= pd.Timedelta(days=buffer_days)]
    # also keep rows with missing time_created — safer if buffer misses edge cases
    keep = pd.concat([keep, monb[monb["time_created"].isna()]]).drop_duplicates(
        subset=["zip", "filename"]
    )
    return keep.to_dict("records")


def parse_day(target: date, buffer_days: int = 10) -> dict[str, list]:
    """Re-parse the monitoring_b FITs covering target date, return per-minute
    series for stress / intensity / respiration / hr. Each list is sorted by
    timestamp; intensity is sparse, others are dense (~1/min).

    Returns dict with keys: stress, intensity, respiration, hr — each a list
    of (datetime, value) tuples for the target day.
    """
    candidates = _candidate_files(target, buffer_days=buffer_days)
    if not candidates:
        return {"stress": [], "intensity": [], "respiration": [], "hr": []}

    zips_to_open = {r["zip"] for r in candidates}
    open_zips: dict[str, zipfile.ZipFile] = {
        z: zipfile.ZipFile(FIT_DIR / z) for z in zips_to_open
    }

    stress: list[tuple[datetime, int]] = []
    intensity: list[tuple[datetime, int]] = []
    resp: list[tuple[datetime, float]] = []
    hr: list[tuple[datetime, int]] = []

    for r in candidates:
        try:
            buf = open_zips[r["zip"]].read(r["filename"])
        except Exception as e:
            print(f"  warn: failed to read {r['filename']}: {e}", file=sys.stderr)
            continue
        resolver = Monitoring16Resolver()
        try:
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
                        if ts is None or val is None: continue
                        if ts.date() != target: continue
                        try: v = int(val)
                        except (TypeError, ValueError): continue
                        if not (STRESS_MIN_VALID <= v <= STRESS_MAX_VALID): continue
                        stress.append((ts, v))
                    elif frame.name == "monitoring":
                        ts = resolver.resolve_frame(frame)
                        if ts is None or ts.date() != target: continue
                        i_val = next((f.value for f in frame.fields
                                      if f.name == "intensity"), None)
                        hr_val = next((f.value for f in frame.fields
                                       if f.name == "heart_rate"), None)
                        if i_val is not None:
                            try: iv = int(i_val); intensity.append((ts, iv))
                            except (TypeError, ValueError): pass
                        if hr_val is not None:
                            try:
                                hv = int(hr_val)
                                if 30 <= hv <= 220:
                                    hr.append((ts, hv))
                            except (TypeError, ValueError): pass
                    elif frame.name == "respiration_rate":
                        ts = next((f.value for f in frame.fields
                                   if f.name == "timestamp"
                                   and isinstance(f.value, datetime)), None)
                        v = next((f.value for f in frame.fields
                                  if f.name == "respiration_rate"), None)
                        if ts is None or v is None: continue
                        if ts.date() != target: continue
                        try: vf = float(v)
                        except (TypeError, ValueError): continue
                        if not (RESP_MIN_VALID <= vf <= RESP_MAX_VALID): continue
                        resp.append((ts, vf))
        except Exception as e:
            print(f"  warn: parse error {r['filename']}: {e}", file=sys.stderr)
            continue

    # sort everything by timestamp
    stress.sort(key=lambda x: x[0])
    intensity.sort(key=lambda x: x[0])
    resp.sort(key=lambda x: x[0])
    hr.sort(key=lambda x: x[0])

    # dedupe stress to per-minute (keep latest)
    by_min: dict[datetime, int] = {}
    for ts, v in stress:
        key = ts.replace(second=0, microsecond=0)
        by_min[key] = v
    stress = sorted(by_min.items())

    return {"stress": stress, "intensity": intensity, "respiration": resp, "hr": hr}


def primary_positive_minutes(stress: list, intensity: list) -> list[datetime]:
    """Return list of minute timestamps where the primary condition (S60_Mlow)
    fires: stress >= 60 AND (intensity <= 1 OR no record at or before)."""
    if not stress:
        return []
    intensity = sorted(intensity, key=lambda x: x[0])
    int_times = [t for (t, _) in intensity]
    int_vals  = [v for (_, v) in intensity]
    out = []
    for (tm, sv) in stress:
        if sv < 60:
            continue
        i = bisect.bisect_right(int_times, tm)
        iv = int_vals[i - 1] if i > 0 else None
        if iv is None or iv <= 1:
            out.append(tm)
    return out
