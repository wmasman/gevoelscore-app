"""H02d Stage 1 — parse all monitoring_b FIT files and emit per-day
max-spike-duration for BOTH arms:
  - max_spike_minutes_imputed: too_active sentinels count as >=75
    (primary)
  - max_spike_minutes_bridge:  too_active sentinels treated as invisible
    (sensitivity)

Off-wrist sentinels are always treated as invisible (skipped from the
walk) for both arms.

Classification rule per stress sample with value outside [1, 100]:
  - if an HR sample exists within +/-60s -> too_active
  - else -> off_wrist
HR cadence is ~60s; the +-60s window covered 100% of sentinels in the
8-file calibration ([../H02b-stress-spikes/calibrate_sentinel_hr_result.md](../H02b-stress-spikes/calibrate_sentinel_hr_result.md)).

Output schema:
  date, sample_count, valid_count, too_active_count, off_wrist_count,
  max_spike_minutes_imputed, max_spike_minutes_bridge, valid

A day is "valid" when (valid_count + too_active_count) >= 60. This is
the H02b coverage gate, adjusted to count too_active as real samples
(since they ARE physiological data, just censored by the algorithm).
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

sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent / "scripts"))
from fit_utils import Monitoring16Resolver  # noqa: E402

GARMIN_DUMP = Path(
    r"C:\Users\Gebruiker\Documents\gevoelscore-data\garmin data\DI_CONNECT\DI-Connect-Uploaded-Files"
)
CLASSIFIED_CSV = Path(__file__).resolve().parent.parent.parent / "output" / "fit_files_classified.csv"
OUT_CSV = Path(__file__).resolve().parent / "daily_max_spike_v2.csv"

SPIKE_THRESHOLD = 75
MIN_SPIKE_MINUTES = 5
MAX_GAP_MINUTES = 3
HR_WINDOW_SECONDS = 60
MIN_SAMPLES_FOR_VALID_DAY = 60


def parse_file(buf: bytes) -> tuple[list[tuple[datetime, int]], list[datetime]]:
    """Return (stress_samples, hr_timestamps) for one FIT file."""
    stress: list[tuple[datetime, int]] = []
    hr_ts: list[datetime] = []
    resolver = Monitoring16Resolver()

    with fitdecode.FitReader(io.BytesIO(buf)) as fit:
        for frame in fit:
            if not isinstance(frame, fitdecode.FitDataMessage):
                continue
            if frame.name == "stress_level":
                ts = None
                val = None
                for f in frame.fields:
                    if f.name == "stress_level_time" and isinstance(f.value, datetime):
                        ts = f.value
                    elif f.name == "stress_level_value" and isinstance(f.value, int):
                        val = f.value
                if ts is not None and val is not None:
                    stress.append((ts, val))
            elif frame.name == "monitoring_info":
                for f in frame.fields:
                    if f.name == "timestamp" and isinstance(f.value, datetime):
                        resolver.set_reference(f.value)
                        break
            elif frame.name == "monitoring":
                ts = resolver.resolve_frame(frame)
                hr = next(
                    (f.value for f in frame.fields
                     if f.name == "heart_rate" and isinstance(f.value, int)),
                    None,
                )
                if ts is not None and hr is not None:
                    hr_ts.append(ts)
    return stress, hr_ts


def classify_samples(
    stress: list[tuple[datetime, int]],
    hr_sorted: list[datetime],
) -> list[tuple[datetime, str, int]]:
    """Classify each stress sample by HR-presence rule.

    Returns list of (timestamp, label, value) where label is
    'valid' | 'too_active' | 'off_wrist'. For 'too_active' samples
    the value is set to the SPIKE_THRESHOLD (75) so imputed-arm
    spike logic can treat them uniformly.
    """
    classified: list[tuple[datetime, str, int]] = []
    for ts, v in stress:
        if 1 <= v <= 100:
            classified.append((ts, "valid", v))
            continue
        # Sentinel: classify by HR presence within +/- HR_WINDOW_SECONDS
        if hr_sorted and _has_hr_nearby(ts, hr_sorted, HR_WINDOW_SECONDS):
            classified.append((ts, "too_active", SPIKE_THRESHOLD))
        else:
            classified.append((ts, "off_wrist", v))
    return classified


def _has_hr_nearby(target: datetime, sorted_ts: list[datetime], window_s: int) -> bool:
    """True iff sorted_ts contains an element within +/- window_s of target."""
    if not sorted_ts:
        return False
    i = bisect.bisect_left(sorted_ts, target)
    if i < len(sorted_ts):
        if abs((sorted_ts[i] - target).total_seconds()) <= window_s:
            return True
    if i > 0:
        if abs((target - sorted_ts[i - 1]).total_seconds()) <= window_s:
            return True
    return False


def find_max_spike(
    classified: list[tuple[datetime, str, int]],
    *,
    include_too_active: bool,
) -> float:
    """Walk the day's classified samples; return longest spike duration
    in minutes.

    A "member" is a sample that contributes to a spike. Membership rule:
      - 'valid' sample with value >= SPIKE_THRESHOLD is always a member.
      - 'too_active' is a member iff include_too_active=True.
      - Anything else (valid<75, off_wrist, or too_active when
        include_too_active=False) is NOT a member.

    Non-members are SKIPPED entirely - they do not extend or break a
    spike. The 3-minute gap rule applies between consecutive members
    (skipped samples do not count toward the gap).

    Wait: that's not quite right for the bridge arm. The hypothesis spec
    §4.3 says too_active under the bridge rule "counts toward continuity
    but not toward duration." Since 'continuity' here means "doesn't
    break the spike," and 'doesn't add to duration' means "doesn't
    extend the spike's endpoints," skipping the too_active sample
    achieves both: it doesn't break the spike (because we don't
    consider it a non-member that would terminate the run), and it
    doesn't extend duration (because endpoints come from valid members
    only). So skipping is correct for both arms - the include_too_active
    flag just controls whether too_active samples themselves act as
    member endpoints.
    """
    if not classified:
        return 0.0
    sorted_samples = sorted(classified, key=lambda x: x[0])
    best = 0.0
    cur_start: datetime | None = None
    cur_last: datetime | None = None
    for ts, label, v in sorted_samples:
        is_member = (
            (label == "valid" and v >= SPIKE_THRESHOLD)
            or (label == "too_active" and include_too_active)
        )
        is_breaker = (label == "valid" and v < SPIKE_THRESHOLD)
        # too_active under bridge arm AND off_wrist: skipped entirely.
        if is_member:
            if cur_start is None:
                cur_start = ts
                cur_last = ts
            else:
                gap_min = (ts - cur_last).total_seconds() / 60.0
                if gap_min > MAX_GAP_MINUTES:
                    dur = (cur_last - cur_start).total_seconds() / 60.0
                    if dur >= MIN_SPIKE_MINUTES and dur > best:
                        best = dur
                    cur_start = ts
                    cur_last = ts
                else:
                    cur_last = ts
        elif is_breaker:
            if cur_start is not None:
                # Apply gap rule: if breaker is close to last member,
                # only finalize if breaker is past the gap window.
                # Actually, any breaker terminates the current spike
                # regardless of gap - it is a measured low-stress sample.
                dur = (cur_last - cur_start).total_seconds() / 60.0
                if dur >= MIN_SPIKE_MINUTES and dur > best:
                    best = dur
                cur_start = None
                cur_last = None
        else:
            # skipped (too_active in bridge arm, off_wrist always)
            continue
    if cur_start is not None:
        dur = (cur_last - cur_start).total_seconds() / 60.0
        if dur >= MIN_SPIKE_MINUTES and dur > best:
            best = dur
    return best


def main() -> int:
    with CLASSIFIED_CSV.open(encoding="utf-8") as fh:
        rows = list(csv.DictReader(fh))
    mfiles = [r for r in rows if r["type"] == "monitoring_b"]
    print(f"monitoring_b files to parse: {len(mfiles)}", file=sys.stderr)

    open_zips = {z: zipfile.ZipFile(GARMIN_DUMP / z) for z in {r["zip"] for r in mfiles}}

    # date -> aggregated stress + hr lists across files for that date
    stress_by_date: dict[date, list[tuple[datetime, int]]] = collections.defaultdict(list)
    hr_by_date: dict[date, list[datetime]] = collections.defaultdict(list)

    for i, r in enumerate(mfiles):
        if i % 500 == 0:
            print(f"  {i}/{len(mfiles)}", file=sys.stderr)
        try:
            buf = open_zips[r["zip"]].read(r["filename"])
            stress, hr_ts = parse_file(buf)
            for ts, v in stress:
                stress_by_date[ts.date()].append((ts, v))
            for ts in hr_ts:
                hr_by_date[ts.date()].append(ts)
        except Exception as e:
            print(f"  ERROR on {r['filename']}: {e}", file=sys.stderr)

    for z in open_zips.values():
        z.close()

    print("\nDeduping, classifying, and computing per-day spikes...", file=sys.stderr)
    out_rows = []
    for d in sorted(stress_by_date):
        # dedup stress on timestamp (keep max value)
        seen: dict[datetime, int] = {}
        for ts, v in stress_by_date[d]:
            if ts not in seen or v > seen[ts]:
                seen[ts] = v
        deduped_stress = list(seen.items())
        # dedup HR timestamps
        hr_sorted = sorted(set(hr_by_date.get(d, [])))

        classified = classify_samples(deduped_stress, hr_sorted)
        valid_n = sum(1 for _, label, _ in classified if label == "valid")
        too_active_n = sum(1 for _, label, _ in classified if label == "too_active")
        off_wrist_n = sum(1 for _, label, _ in classified if label == "off_wrist")

        max_imputed = find_max_spike(classified, include_too_active=True)
        max_bridge = find_max_spike(classified, include_too_active=False)

        # coverage gate: count valid + too_active (the actually-measured samples)
        on_wrist_n = valid_n + too_active_n
        valid_day = on_wrist_n >= MIN_SAMPLES_FOR_VALID_DAY

        out_rows.append({
            "date": d.isoformat(),
            "sample_count": len(classified),
            "valid_count": valid_n,
            "too_active_count": too_active_n,
            "off_wrist_count": off_wrist_n,
            "max_spike_minutes_imputed": round(max_imputed, 1),
            "max_spike_minutes_bridge": round(max_bridge, 1),
            "valid": 1 if valid_day else 0,
        })

    with OUT_CSV.open("w", newline="", encoding="utf-8") as fh:
        w = csv.DictWriter(fh, fieldnames=[
            "date", "sample_count", "valid_count", "too_active_count",
            "off_wrist_count", "max_spike_minutes_imputed",
            "max_spike_minutes_bridge", "valid",
        ])
        w.writeheader()
        w.writerows(out_rows)
    print(f"wrote {len(out_rows)} days -> {OUT_CSV}", file=sys.stderr)
    n_valid = sum(1 for r in out_rows if r["valid"])
    n_imputed_change = sum(
        1 for r in out_rows
        if r["valid"] and r["max_spike_minutes_imputed"] != r["max_spike_minutes_bridge"]
    )
    print(f"  valid days (on-wrist samples >= {MIN_SAMPLES_FOR_VALID_DAY}): {n_valid}", file=sys.stderr)
    print(f"  days where imputed != bridge (sentinel imputation changed max-spike): {n_imputed_change}", file=sys.stderr)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
