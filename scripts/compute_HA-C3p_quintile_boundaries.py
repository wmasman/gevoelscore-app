"""Compute HA-C3p quintile boundaries on the full-Stratum-4 + day-validity-gate pool.

Mirrors HA-C3 v2 r1 §4.2 (full Stratum 4 single pool) + §4.3 day-validity gate
(LC era + non-NaN both columns + April 2024 cluster exclusion + first 21
device-baseline days exclusion). Computes equal-N quintile boundaries via numpy's
np.quantile with linear interpolation (default) at q = [0.0, 0.2, 0.4, 0.6, 0.8, 1.0],
then per-bin n verification with left-inclusive / right-exclusive intervals
(except top bin which is closed-above).

Stratum 4 includes consolidation + afbouw (full LC era), NOT just unmedicated.
This matches HA-C3p §4.2's full-pool primary (per session handoff §3 decision 1).

Also reports per-bin n on the unmedicated-only sub-arm for forecast vs the
~80/bin handoff §6 expectation.

ASCII-only stdout.
"""
from __future__ import annotations
import csv
import hashlib
import math
import os
import sys
from datetime import date
from pathlib import Path

import numpy as np

DATA_ROOT = Path(os.environ.get(
    "GEVOELSCORE_DATA_PATH",
    r"C:\Users\Gebruiker\Documents\gevoelscore-data",
))
MASTER_CSV = DATA_ROOT / "unified" / "per_day_master.csv"

LC_ERA_START = date(2022, 4, 4)
UNMEDICATED_END_INCL = date(2024, 4, 8)
APRIL2024_CLUSTER_START = date(2024, 4, 9)
APRIL2024_CLUSTER_END_INCL = date(2024, 4, 16)
DEVICE_BASELINE_DAYS = 21


def parse_float(s):
    if s == "" or s is None:
        return None
    try:
        v = float(s)
        if math.isnan(v):
            return None
        return v
    except (ValueError, TypeError):
        return None


def load_master():
    rows = []
    with MASTER_CSV.open(encoding="utf-8") as fh:
        for row in csv.DictReader(fh):
            try:
                d = date.fromisoformat(row["date"])
            except (KeyError, ValueError):
                continue
            rows.append((d, row))
    rows.sort(key=lambda r: r[0])
    return rows


def find_device_baseline_cutoff(rows):
    n_uds = 0
    for d, row in rows:
        if (row.get("has_garmin_uds", "") or "").strip().lower() == "true":
            n_uds += 1
            if n_uds == DEVICE_BASELINE_DAYS:
                return d
    return None


def day_passes(d, row, baseline_cutoff, stratum="stratum4"):
    """stratum4: full LC era through today (cap not enforced; cluster excluded)
    unmedicated: LC era through 2024-04-08 inclusive (cluster excluded)
    """
    if d < LC_ERA_START:
        return False
    if stratum == "unmedicated" and d > UNMEDICATED_END_INCL:
        return False
    if APRIL2024_CLUSTER_START <= d <= APRIL2024_CLUSTER_END_INCL:
        return False
    if baseline_cutoff is not None and d <= baseline_cutoff:
        return False
    s = parse_float(row.get("all_day_stress_avg", ""))
    if s is None or s < 0.0 or s > 100.0:
        return False
    g = parse_float(row.get("gevoelscore", ""))
    if g is None:
        return False
    return True


def assign_bin(s, edges):
    n_bins = len(edges) - 1
    for i in range(n_bins):
        lo = edges[i]
        hi = edges[i + 1]
        if i == n_bins - 1:
            if lo <= s <= hi:
                return i
        else:
            if lo <= s < hi:
                return i
    return None


def sha256_path(p):
    h = hashlib.sha256()
    with open(p, "rb") as fh:
        while True:
            blk = fh.read(1 << 16)
            if not blk:
                break
            h.update(blk)
    return h.hexdigest()


def main():
    snap_sha = sha256_path(MASTER_CSV)
    print("PER_DAY_MASTER SNAPSHOT SHA-256:", snap_sha)
    print("PATH:", MASTER_CSV)

    rows = load_master()
    print("TOTAL ROWS:", len(rows))

    baseline_cutoff = find_device_baseline_cutoff(rows)
    print("DEVICE_BASELINE_CUTOFF (inclusive exclusion):", baseline_cutoff)

    # === STRATUM 4 FULL POOL =========================================
    stress_s4 = []
    for d, row in rows:
        if day_passes(d, row, baseline_cutoff, stratum="stratum4"):
            s = parse_float(row["all_day_stress_avg"])
            stress_s4.append(s)
    stress_s4 = np.asarray(stress_s4, dtype=float)
    print("\n=== STRATUM 4 FULL POOL (HA-C3p primary bin-computation pool) ===")
    print("POOL N:", len(stress_s4))
    print("STRESS MIN/MEDIAN/MAX:", float(stress_s4.min()),
          float(np.median(stress_s4)), float(stress_s4.max()))
    qs = np.quantile(stress_s4, [0.2, 0.4, 0.6, 0.8])
    print("QUINTILE BOUNDARIES (q=0.2, 0.4, 0.6, 0.8):", qs.tolist())

    # Decide rounding: stress is integer 0-100 per DATA_DICTIONARY.
    # Quintile boundaries should be integers for clean cross-test reading.
    qs_int = [int(round(x)) for x in qs.tolist()]
    print("QUINTILE BOUNDARIES ROUNDED TO INT:", qs_int)

    # Verify: build per-bin n with [0, q1, q2, q3, q4, 100] edges using
    # left-inclusive / right-exclusive (top closed).
    edges_int = [0.0] + [float(x) for x in qs_int] + [100.0]
    print("FINAL EDGES:", edges_int)
    bin_counts = [0] * (len(edges_int) - 1)
    for s in stress_s4:
        b = assign_bin(s, edges_int)
        if b is not None:
            bin_counts[b] += 1
    print("PER-BIN N (int-rounded edges, full Stratum 4):", bin_counts)
    print("SUM:", sum(bin_counts), "expected:", len(stress_s4))

    # === UNMEDICATED-ONLY SUB-ARM (descriptive forecast) =============
    stress_un = []
    for d, row in rows:
        if day_passes(d, row, baseline_cutoff, stratum="unmedicated"):
            s = parse_float(row["all_day_stress_avg"])
            stress_un.append(s)
    stress_un = np.asarray(stress_un, dtype=float)
    print("\n=== UNMEDICATED SUB-ARM (HA-C3p §5.A headline) ===")
    print("POOL N:", len(stress_un))
    print("STRESS MIN/MEDIAN/MAX:", float(stress_un.min()),
          float(np.median(stress_un)), float(stress_un.max()))
    # REUSE the full-pool bin edges (cross-arm cleanliness per handoff §8)
    bin_counts_un = [0] * (len(edges_int) - 1)
    for s in stress_un:
        b = assign_bin(s, edges_int)
        if b is not None:
            bin_counts_un[b] += 1
    print("PER-BIN N ON UNMEDICATED (REUSING full-pool edges):", bin_counts_un)
    print("SUM:", sum(bin_counts_un), "expected:", len(stress_un))

    # === DESCRIPTIVE: also report what unmedicated-only quintile edges
    #     would look like (for documentation in §4.2 rationale) ========
    qs_un = np.quantile(stress_un, [0.2, 0.4, 0.6, 0.8])
    print("\n(DESCRIPTIVE ONLY) UNMEDICATED-ONLY QUINTILES would be:",
          [round(x, 2) for x in qs_un.tolist()])
    print("(DESCRIPTIVE ONLY) ROUNDED:",
          [int(round(x)) for x in qs_un.tolist()])

    print("\nDONE")


if __name__ == "__main__":
    main()
