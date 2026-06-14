"""Build per_day_master.csv — the unified per-day dataset.

Phase B of the dataset-unification plan: reads source files at their
CURRENT in-repo locations (pre-Phase C reorganisation) and produces
the master at a temporary path for user spot-check.

After Phase C, paths shift to $GEVOELSCORE_DATA_PATH/processed/* and
the output goes to $GEVOELSCORE_DATA_PATH/unified/per_day_master.csv.

Spec: docs/research/DATA_DICTIONARY.md
Methodology: docs/research/methodology/{nightly_attribution,symptom_mention_asymmetry}.md
"""
from __future__ import annotations

import csv
import json
import math
import os
import statistics
from collections import Counter, defaultdict
from datetime import date, datetime, timedelta
from pathlib import Path
from zoneinfo import ZoneInfo

import yaml

# Europe/Amsterdam used to derive `sleep_start_afternoon_flag` from
# `sleep_start_gmt`. DST-correct via stdlib zoneinfo.
TZ_LOCAL = ZoneInfo("Europe/Amsterdam")


def load_env_file(env_path: Path) -> None:
    """Tiny .env loader — sets os.environ from KEY=VALUE lines.
    Avoids the python-dotenv dependency for a one-key file."""
    if not env_path.exists():
        return
    for line in env_path.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, _, value = line.partition("=")
        key = key.strip()
        value = value.strip().strip('"').strip("'")
        if key and key not in os.environ:
            os.environ[key] = value


# Load .env if present (resolves GEVOELSCORE_DATA_PATH)
HERE = Path(__file__).resolve().parent
# docs/research/pipeline/03_consolidate -> 03_consolidate -> pipeline -> research -> docs -> repo
REPO_ROOT = HERE.parent.parent.parent.parent
load_env_file(REPO_ROOT / ".env")

DATA_PATH = Path(os.environ.get("GEVOELSCORE_DATA_PATH", ""))
if not DATA_PATH or not DATA_PATH.exists():
    raise SystemExit(
        "GEVOELSCORE_DATA_PATH is not set or does not exist. "
        "Copy .env.example to .env and edit the path. "
        f"Tried: {DATA_PATH!r}"
    )

# === Source paths (Phase C: all data lives in $GEVOELSCORE_DATA_PATH) ===
DAY_ENTRIES_JSON = DATA_PATH / "raw/directus_exports/day_entries.json"
DAILY_UDS = DATA_PATH / "processed/garmin/daily_uds.csv"
ACTIVITY_FEATURES = DATA_PATH / "processed/garmin/activity_features_daily.csv"
SLEEP_STRESS = DATA_PATH / "processed/garmin/sleep_stress_nightly.csv"
DAILY_MAX_SPIKE = DATA_PATH / "processed/garmin/daily_max_spike.csv"
UDS_EXTRAS = DATA_PATH / "processed/garmin/uds_extras_daily.csv"
SLEEP_EXTRAS = DATA_PATH / "processed/garmin/sleep_extras_daily.csv"
INTRADAY_HR_STRESS = DATA_PATH / "processed/garmin/intraday_hr_stress_daily.csv"
LABELS_CRASH = DATA_PATH / "processed/crash_labels/labels_crash_v2.csv"
V24_CLAUSES = DATA_PATH / "processed/notes/notes-categorized-v24-clauses.csv"
PER_DAY_INTENSITY = DATA_PATH / "processed/manual_triage/per_day_intensity.csv"
SUB_THRESHOLD_DIPS = DATA_PATH / "processed/crash_labels/sub_threshold_dips.csv"
TRIAGE_EVENTS = DATA_PATH / "processed/manual_triage/triage_events.csv"
ANNOTATIONS = DATA_PATH / "raw/directus_exports/annotations.yaml"
REINTEGRATION_HOURS = DATA_PATH / "processed/pwc/reintegration_hours_2022-2024.csv"

# === Output: in the external personal-data folder, NEVER in the repo ===
OUTPUT = DATA_PATH / "unified" / "per_day_master.csv"

# === Era + window boundaries (per DATA_DICTIONARY.md identity section) ===
# `era` (train / validate) uses the pre-registered crash_v2 era split that
# was locked before the validate-era data came in — so it generalises
# honestly.
SCORE_START = date(2022, 9, 3)
TRAIN_END = date(2023, 12, 31)
# wachttijd-loondoorbetaling 104w window: 2022-04-25 → 2024-04-17.
# Used only to compute `has_pwc_dossier_window`; not a methodological period.
WACHTTIJD_START = date(2022, 3, 28)
WACHTTIJD_END = date(2024, 4, 17)
# Calendar-coverage window: from the date the user began maintaining the
# external calendar that feeds annotations.yaml. Before this date,
# n_events_on_day=0 is unobserved (calendar not yet maintained); from this
# date onwards, n_events_on_day=0 is observed-no-event. Used to compute
# `has_calendar_coverage` (added 2026-06-12 per Layer 2 gating-flag audit).
CALENDAR_COVERAGE_START = date(2022, 6, 17)
# LC research-era boundaries (added 2026-06-12 per user lock).
# CORONA_START = first day of the documented corona-ziek-week
# (2022-03-21 to 2022-03-27, per the Training-periode span note in
# annotations.yaml). LC_ERA_START = Monday after the Fietsweekend Ardennen
# (2022-04-01 to 2022-04-03), the user's locked factual boundary for the
# post-corona / LC-symptom-onset window. See the 2022-04-04 marker in
# annotations.yaml. Used to compute the `lc_phase` derived column and
# referenced by the *_lagged_lcera variant in 11_compute_lagged_baseline.py.
CORONA_START = date(2022, 3, 21)
LC_ERA_START = date(2022, 4, 4)
# NOTE: an earlier draft included a derived bool with arbitrary boundaries
# based on qualitative trajectory framing. Removed 2026-06-11 per user
# feedback: the boundaries were not pre-registered, not data-driven, and
# any classification of that kind belongs in descriptive-analysis output
# rather than the schema. See DATA_DICTIONARY.md update log.

# Per-period umbrella booleans emitted alongside the descriptive `in_umbrella` OR.
# Added 2026-06-12 after Layer 3 spot-investigation showed that the three
# umbrella periods are semantically distinct (medication, work, relational)
# and barely overlap in time, so `in_umbrella` as a single binary is
# confounded by year. The per-period booleans below are the analytical
# surface for any correlation / stratification on umbrella membership.
# Substrings match the canonical name prefix in hand_curated_spans.yaml.
UMBRELLA_FLAGS = {
    "in_citalopram_traject": "Citalopram-traject",
    "in_pwc_reintegratie_2023": "PwC reintegratie 2023",
    "in_relational_spanning_2024": "Relational-spanning 2024",
    "in_naproxen_interventie": "Naproxen-interventie",
}

# === v24 vocab ===
V24_CATEGORIES = [
    "belasting_cognitief", "belasting_emotioneel", "belasting_fysiek",
    "belasting_gezin", "belasting_sociaal",
    "symptoom_cognitief", "symptoom_emotioneel", "symptoom_fysiek",
    "medicatie", "recovery_actie", "triggers_extern", "context_neutraal",
]
V24_SUB_FYSIEK = [
    "hoofdpijn", "spier", "keel_respiratoir", "koorts",
    "gastro", "huid", "neuro", "systemisch_vermoeid", "slaap", "overig",
]
# CSV column-name overrides for sub-tags whose source key would produce
# an unwieldy column name. The lookup key (left) is the source subtype
# value in notes-categorized-v24-clauses.csv; the emitted column suffix
# (right) is the dictionary-canonical short name.
V24_SUB_CSV_NAME = {"keel_respiratoir": "keel_resp"}
STATE_SEVERITY = {"absent": 0, "mild": 1, "present": 2, "severe": 3}
STATE_SEVERITY_INV = {v: k for k, v in STATE_SEVERITY.items()}


def parse_iso(s):
    if not s or s in ("None", "NaN", "nan"):
        return None
    try:
        return date.fromisoformat(str(s))
    except (ValueError, TypeError):
        return None


def parse_float_safe(s):
    if s in (None, "", "None", "NaN", "nan"):
        return None
    try:
        return float(s)
    except (ValueError, TypeError):
        return None


def drop_neg_sentinel(raw):
    """Garmin negative-value sentinel filter.

    The UDS extras export emits negative integers (-1, -2, -4, -5) on
    some days as a "no data" sentinel — sometimes whole-day (Pattern A:
    watch off / first day of coverage) and sometimes channel-specific
    (Pattern B: no asleep_stress computed even though FIT-derived sleep
    window may be valid). Negative values are physically impossible for
    stress (0-100 scale) and body battery (0-100 scale), so they cannot
    be real measurements. Replace with blank.

    Class 2 ambiguous zeros (e.g. *_stress_max = 0 only on whole-day
    void days) are left alone — they only co-occur with Class 1 sentinels
    that this function catches, so the affected days end up correctly
    flagged via the negative-stress-avg drop anyway. Class 3 legitimate
    zeros (sleep_unmeasurable_min, sleep_awake_min, sleep_deep_min) are
    real states and stay.

    Applied 2026-06-12 per Layer 1 Wiggers-enrichment sentinel audit.
    See DATA_DICTIONARY.md sec 7B sentinel-policy note.
    """
    if not raw or raw in ("None", "NaN", "nan"):
        return ""
    try:
        if float(raw) < 0:
            return ""
    except (ValueError, TypeError):
        pass
    return raw


def load_csv_by_date(path: Path, date_col: str = "date") -> dict:
    if not path.exists():
        print(f"  WARNING: {path} does not exist")
        return {}
    out = {}
    for r in csv.DictReader(path.open(encoding="utf-8")):
        d = parse_iso(r.get(date_col))
        if d:
            out[d] = r
    return out


def load_day_entries() -> dict:
    out = {}
    with DAY_ENTRIES_JSON.open(encoding="utf-8") as f:
        for entry in json.load(f):
            d = parse_iso(entry.get("date"))
            if d:
                out[d] = {
                    "gevoelscore": entry.get("score"),
                    "note_text": entry.get("note") or "",
                }
    return out


def aggregate_v24_per_day() -> dict:
    """Aggregate clause-level v24 to per-day rollup."""
    per_day = defaultdict(lambda: {
        "n_clauses": 0,
        "cat_counts": defaultdict(int),
        "sub_counts": defaultdict(int),
        "state_max": defaultdict(int),
        "state_absent_seen": set(),
        "polarities": [],
        "neutral_forward_looking": False,
    })
    for r in csv.DictReader(V24_CLAUSES.open(encoding="utf-8")):
        d = parse_iso(r.get("date"))
        if not d:
            continue
        rec = per_day[d]
        rec["n_clauses"] += 1
        for c in (r.get("categories") or "").split("|"):
            c = c.strip()
            if c:
                rec["cat_counts"][c] += 1
        for s in (r.get("symptoom_fysiek_subtype") or "").split(";"):
            s = s.strip()
            if s:
                rec["sub_counts"][s] += 1
        for token in (r.get("symptom_states") or "").split(";"):
            token = token.strip()
            if "=" in token:
                sym, state = token.split("=", 1)
                if sym.startswith("symptoom_"):
                    family = sym.replace("symptoom_", "")
                    if state == "absent":
                        rec["state_absent_seen"].add(family)
                    else:
                        sev = STATE_SEVERITY.get(state, 0)
                        if sev > rec["state_max"][family]:
                            rec["state_max"][family] = sev
        pol = (r.get("polarity") or "").strip()
        if pol:
            rec["polarities"].append(pol)
        if (r.get("neutral_forward_looking") or "").strip().lower() == "y":
            rec["neutral_forward_looking"] = True
    return per_day


def aggregate_events() -> tuple[dict, dict]:
    """From annotations.yaml: events per day + umbrella memberships.

    Umbrella detection: a span is an umbrella iff the word 'umbrella'
    appears anywhere in its label (the explicit user-curated marker per
    methodology §4). Matches both '(umbrella)' and '(umbrella, ... ongoing)'
    forms. Earlier draft used a 14-day duration fallback; removed
    2026-06-11 as arbitrary — the user labels umbrellas explicitly when
    they intend them.
    """
    import re
    umbrella_pat = re.compile(r"\bumbrella\b", re.IGNORECASE)
    events_by_day = defaultdict(list)
    umbrella_by_day = defaultdict(list)
    if not ANNOTATIONS.exists():
        return events_by_day, umbrella_by_day
    raw = yaml.safe_load(ANNOTATIONS.read_text(encoding="utf-8")) or {}
    for span in (raw.get("spans") or []):
        ds = parse_iso(span.get("start"))
        de = parse_iso(span.get("end")) or ds
        if not ds:
            continue
        cat = span.get("category", "")
        label = span.get("label", "")
        is_umbrella = bool(umbrella_pat.search(label))
        d = ds
        while d <= de:
            events_by_day[d].append({"label": label, "category": cat})
            if is_umbrella:
                umbrella_by_day[d].append(label)
            d += timedelta(days=1)
    for m in (raw.get("markers") or []):
        d = parse_iso(m.get("date"))
        if d:
            events_by_day[d].append({"label": m.get("label", ""), "category": "marker"})
    return events_by_day, umbrella_by_day


def aggregate_dossier_events() -> dict:
    """From triage_events.csv with source=pwc_dossier_2022-2024."""
    out = defaultdict(list)
    if not TRIAGE_EVENTS.exists():
        return out
    for r in csv.DictReader(TRIAGE_EVENTS.open(encoding="utf-8")):
        if r.get("source") != "pwc_dossier_2022-2024":
            continue
        ds = parse_iso(r.get("date_start"))
        de = parse_iso(r.get("date_end")) or ds
        if not ds:
            continue
        d = ds
        while d <= de:
            out[d].append({
                "label": r.get("label", ""),
                "category": r.get("category", ""),
            })
            d += timedelta(days=1)
    return out


def main():
    print("Loading sources...")
    day_entries = load_day_entries()
    print(f"  day_entries: {len(day_entries)}")
    uds = load_csv_by_date(DAILY_UDS)
    print(f"  daily_uds: {len(uds)}")
    af = load_csv_by_date(ACTIVITY_FEATURES)
    print(f"  activity_features: {len(af)}")
    sleep = load_csv_by_date(SLEEP_STRESS)
    print(f"  sleep_stress: {len(sleep)}")
    spike = load_csv_by_date(DAILY_MAX_SPIKE)
    print(f"  daily_max_spike: {len(spike)}")
    uds_extras = load_csv_by_date(UDS_EXTRAS)
    print(f"  uds_extras: {len(uds_extras)}")
    sleep_extras = load_csv_by_date(SLEEP_EXTRAS)
    print(f"  sleep_extras: {len(sleep_extras)}")
    intraday_hr_stress = load_csv_by_date(INTRADAY_HR_STRESS)
    print(f"  intraday_hr_stress: {len(intraday_hr_stress)}")
    crash = load_csv_by_date(LABELS_CRASH)
    print(f"  crash labels: {len(crash)}")
    intensity = load_csv_by_date(PER_DAY_INTENSITY)
    print(f"  per_day_intensity: {len(intensity)}")
    sub_dips = load_csv_by_date(SUB_THRESHOLD_DIPS)
    print(f"  sub_threshold_dips: {len(sub_dips)}")
    pwc_hours = load_csv_by_date(REINTEGRATION_HOURS)
    print(f"  reintegration_hours: {len(pwc_hours)}")

    print("  aggregating v24 clauses to per-day...")
    v24_per_day = aggregate_v24_per_day()
    print(f"    v24_per_day: {len(v24_per_day)}")

    print("  parsing annotations.yaml...")
    events_by_day, umbrella_by_day = aggregate_events()
    print(f"    events: {len(events_by_day)} days have events; {len(umbrella_by_day)} in umbrella")

    print("  parsing dossier events...")
    dossier_by_day = aggregate_dossier_events()
    print(f"    dossier events on {len(dossier_by_day)} days")

    # === Date range: union of all source coverages, capped at last gevoelscore date ===
    # Forward-dated rows in any source (e.g. ongoing-span artefacts) are
    # excluded from the master. The cap is the last gevoelscore-tracked
    # date — the dataset describes the period the user has been tracking,
    # which is the analytic window. This is also more reproducible than
    # `today` (build output is stable regardless of run time).
    all_dates = set()
    for src in (day_entries, uds, crash, intensity, sleep, events_by_day):
        all_dates.update(src.keys())
    last_score_date = max(day_entries.keys()) if day_entries else max(all_dates)
    all_dates = {d for d in all_dates if d <= last_score_date}
    min_date = min(all_dates)
    max_date = max(all_dates)
    print(f"\nDate range: {min_date} -> {max_date} (capped at last gevoelscore date={last_score_date})")

    # Generate full calendar index
    all_days = []
    d = min_date
    while d <= max_date:
        all_days.append(d)
        d += timedelta(days=1)
    print(f"Total days in master: {len(all_days)}")

    # === Build each row ===
    print("Building rows...")
    rows = []
    for d in all_days:
        row = build_row(
            d, day_entries, uds, af, sleep, spike, crash, intensity,
            sub_dips, pwc_hours, v24_per_day, events_by_day, umbrella_by_day,
            dossier_by_day, uds_extras, sleep_extras, intraday_hr_stress,
        )
        rows.append(row)

    # === Post-pass: rolling 7-day bedtime std (Wave 1, Wiggers F4) ===
    # Compute trailing 7-day std of bedtime_hour_local (DST-correct local
    # fractional hour). Handles after-midnight wrap: bedtimes < 12 are
    # treated as +24 so a sequence like 22:00, 23:30, 00:30 has small
    # variance (22.0, 23.5, 24.5) instead of being inflated by the 24h
    # discontinuity. Afternoon-flagged nights (<17:00 local) are excluded
    # from the window — they are aberrant per the Layer 2 audit and would
    # distort variance.
    bedtime_window: list[float] = []
    for row in rows:
        bh = row.get("bedtime_hour_local")
        afternoon = row.get("sleep_start_afternoon_flag")
        if bh not in ("", None) and afternoon is not True:
            try:
                v = float(bh)
                bedtime_window.append(v + 24.0 if v < 12 else v)
            except (ValueError, TypeError):
                pass
        # Keep only last 7 values
        if len(bedtime_window) > 7:
            bedtime_window = bedtime_window[-7:]
        row["bedtime_std_7d"] = (
            round(statistics.stdev(bedtime_window), 3)
            if len(bedtime_window) >= 2
            else ""
        )

    # === Post-pass: stress_mean_sleep_lagged_lcera_z (z-score variant) ===
    # Per citalopram_dose_response §4.3-C + citalopram_phase_stratification framework:
    # the v3.2 lagged-baseline pattern from CONVENTIONS §3.2 applied to a raw-continuous
    # channel produces a z-score against the rolling [d-90, d-30] LC-era window using
    # median + 1.4826*MAD (normal-equivalent SD). This is the SAME formulation
    # `dose_response.py` computes on-the-fly for its Sensitivity Column C; promoting
    # to the master so downstream tests can read it directly.
    #
    # Naming: distinct from the existing percentile-rank `_lagged_lcera` family (which
    # applies to rank-source columns like effective_exertion_rank). The `_z` suffix
    # makes the z-score semantics explicit.
    #
    # Window: [d-90, d-30] LC-era only (days >= LC_ERA_START = 2022-04-04).
    # NaN policy: emit "" when fewer than 5 valid LC-era days in the window, when
    # the candidate day's value is missing, or when MAD == 0 (degenerate baseline).
    #
    # Stage 1 of the pipeline patch: stress_mean_sleep first, validate against
    # dose_response.py in-script before extending to the rest of §3 baseline channels.
    LAGGED_LCERA_LOOKBACK = 90
    LAGGED_LCERA_GAP = 30
    LAGGED_LCERA_MIN_WINDOW = 5
    MAD_TO_SD = 1.4826

    def _row_date(row):
        return parse_iso(row["date"])

    def _compute_lagged_lcera_z(rows, src_key, out_key):
        # Build {date: value} for LC-era days where value is parseable
        lc_era_values = {}
        for r in rows:
            d_obj = _row_date(r)
            if d_obj is None or d_obj < LC_ERA_START:
                continue
            v = parse_float_safe(r.get(src_key))
            if v is None:
                continue
            lc_era_values[d_obj] = v
        # Sort dates once
        sorted_lc_dates = sorted(lc_era_values.keys())
        # For each row, compute z
        for r in rows:
            d_obj = _row_date(r)
            if d_obj is None:
                r[out_key] = ""
                continue
            today_val = parse_float_safe(r.get(src_key))
            if today_val is None:
                r[out_key] = ""
                continue
            win_start = d_obj - timedelta(days=LAGGED_LCERA_LOOKBACK)
            win_end = d_obj - timedelta(days=LAGGED_LCERA_GAP)
            window_vals = [
                lc_era_values[wd]
                for wd in sorted_lc_dates
                if win_start <= wd <= win_end
            ]
            if len(window_vals) < LAGGED_LCERA_MIN_WINDOW:
                r[out_key] = ""
                continue
            window_vals.sort()
            n = len(window_vals)
            med = (
                window_vals[n // 2]
                if n % 2 == 1
                else (window_vals[n // 2 - 1] + window_vals[n // 2]) / 2.0
            )
            abs_devs = sorted(abs(v - med) for v in window_vals)
            mad = (
                abs_devs[n // 2]
                if n % 2 == 1
                else (abs_devs[n // 2 - 1] + abs_devs[n // 2]) / 2.0
            )
            scaled_mad = MAD_TO_SD * mad
            if scaled_mad <= 0:
                r[out_key] = ""
                continue
            z = (today_val - med) / scaled_mad
            r[out_key] = round(z, 4)

    # Stage 1 (2026-06-14): stress_mean_sleep validated against dose_response.py
    # in-script computation (abs diff max ~5e-5; PASS).
    # Stage 2 (2026-06-14): extended to the rest of the parent MD §3 baseline
    # channel family. Per citalopram_phase_stratification §4 inheritance table:
    #   - stress_mean_sleep, all_day_stress_avg, bb_lowest -- CONFIRMED dose-modulated
    #   - resting_hr -- weakly consistent
    #   - bb_overnight_gain -- partial (no 2024 buildup data)
    #   - respiration_avg_sleep -- REJECTED dose-modulated
    # All six channels get the z-score variant since the operationalisation is
    # uniform (the z-score is the variable; the v3 verdict is the test).
    for _src, _out in [
        ("stress_mean_sleep",      "stress_mean_sleep_lagged_lcera_z"),
        ("all_day_stress_avg",     "all_day_stress_avg_lagged_lcera_z"),
        ("resting_hr",             "resting_hr_lagged_lcera_z"),
        ("respiration_avg_sleep",  "respiration_avg_sleep_lagged_lcera_z"),
        ("bb_lowest",              "bb_lowest_lagged_lcera_z"),
        ("bb_overnight_gain",      "bb_overnight_gain_lagged_lcera_z"),
    ]:
        _compute_lagged_lcera_z(rows, _src, _out)

    # === Post-pass: dose_plasma_mg (PK-smoothed citalopram plasma proxy) ===
    # Per citalopram_phase_stratification §8.3 forward pointer: the PK-smoothed
    # citalopram plasma dose is a first-class data axis on this corpus, not just
    # an analytical convenience for one MD. Promoted to a master column so any
    # downstream test that needs dose-adjustment per §5.B can read it directly.
    #
    # Formula: one-compartment first-order PK model with t_half = 35h (citalopram
    # SPC, EMA). Initial dose = 0mg pre-2024-04-09 (unmedicated). Subsequent
    # dose-step contributions accumulate via linear superposition of step inputs.
    #
    # See citalopram_dose_response §2.3 for the canonical formula derivation;
    # this implementation mirrors dose_response.py's plasma_dose_mg() function.
    CITALOPRAM_T_HALF_HOURS = 35.0
    CITALOPRAM_T_HALF_DAYS = CITALOPRAM_T_HALF_HOURS / 24.0
    CITALOPRAM_DECAY_K = math.log(2.0) / CITALOPRAM_T_HALF_DAYS
    # Step dates verified against annotations.yaml 2026-06-14:
    #   2024-04-09 phase 1 start (0 -> 10mg), 2024-05-05 phase 2 (10 -> 20mg),
    #   2024-06-20 buildup -> consolidation marker (20 -> 30mg),
    #   2026-03-20 consolidation -> afbouw (30 -> 20mg),
    #   2026-04-17 afbouw step (20 -> 10mg),
    #   2026-05-27 afbouw step (10 -> 8mg druppelvorm).
    CITALOPRAM_DOSE_STEPS = [
        (date(2024,  4,  9), +10.0),
        (date(2024,  5,  5), +10.0),
        (date(2024,  6, 20), +10.0),
        (date(2026,  3, 20), -10.0),
        (date(2026,  4, 17), -10.0),
        (date(2026,  5, 27),  -2.0),
    ]
    CITALOPRAM_INITIAL_DOSE_MG = 0.0

    for r in rows:
        d_obj = _row_date(r)
        if d_obj is None:
            r["dose_plasma_mg"] = ""
            continue
        val = CITALOPRAM_INITIAL_DOSE_MG
        for step_date, delta in CITALOPRAM_DOSE_STEPS:
            if d_obj >= step_date:
                days_since = (d_obj - step_date).days
                val += delta * (1.0 - math.exp(-CITALOPRAM_DECAY_K * days_since))
        r["dose_plasma_mg"] = round(val, 4)

    # === Write ===
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    fields = list(rows[0].keys())
    with OUTPUT.open("w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=fields)
        w.writeheader()
        for row in rows:
            w.writerow(row)

    print(f"\nWrote {OUTPUT}")
    print(f"  rows: {len(rows)}")
    print(f"  columns: {len(fields)}")

    # === Validation summary ===
    print("\n=== Validation ===")
    n_score = sum(1 for r in rows if r["has_score"])
    n_note = sum(1 for r in rows if r["has_note"])
    n_uds = sum(1 for r in rows if r["has_garmin_uds"])
    n_sleep = sum(1 for r in rows if r["has_garmin_sleep"])
    n_intensity = sum(1 for r in rows if r["has_intensity_triage"])
    n_pwc = sum(1 for r in rows if r["has_pwc_log"])
    n_dossier = sum(1 for r in rows if r["dossier_event_today"])
    n_events = sum(1 for r in rows if r["n_events_on_day"])
    print(f"  has_score: {n_score} / {len(rows)}")
    print(f"  has_note: {n_note}")
    print(f"  has_garmin_uds: {n_uds}")
    print(f"  has_garmin_sleep: {n_sleep}")
    print(f"  has_intensity_triage: {n_intensity}")
    print(f"  has_pwc_log: {n_pwc}")
    print(f"  dossier_event_today: {n_dossier}")
    print(f"  days with >=1 event: {n_events}")


def build_row(d, day_entries, uds, af, sleep, spike, crash, intensity,
              sub_dips, pwc_hours, v24_per_day, events_by_day,
              umbrella_by_day, dossier_by_day, uds_extras=None,
              sleep_extras=None, intraday_hr_stress=None):
    intraday_hr_stress = intraday_hr_stress or {}
    uds_extras = uds_extras or {}
    sleep_extras = sleep_extras or {}
    row = {"date": d.isoformat()}

    # --- Identity ---
    row["day_of_week"] = d.strftime("%a")
    if d < SCORE_START:
        row["era"] = "pre_score"
    elif d <= TRAIN_END:
        row["era"] = "train"
    else:
        row["era"] = "validate"

    # --- Subjective state ---
    de = day_entries.get(d, {})
    score = de.get("gevoelscore")
    row["gevoelscore"] = score if score is not None else ""
    note_text = de.get("note_text") or ""
    row["has_note"] = bool(note_text.strip())
    row["note_text"] = note_text
    row["has_score"] = score is not None

    # --- Manual load triage (presence-conditioned on intensity_source) ---
    pdi = intensity.get(d, {})
    intensity_source = (pdi.get("source") or "").strip()
    row["has_intensity_triage"] = bool(intensity_source)
    row["intensity_source"] = intensity_source
    if intensity_source:
        row["cog_load"] = pdi.get("cog") or ""
        row["phy_load"] = pdi.get("phy") or ""
        row["emo_load"] = pdi.get("emo") or ""
        row["intensity_notes"] = pdi.get("notes") or ""
    else:
        row["cog_load"] = ""
        row["phy_load"] = ""
        row["emo_load"] = ""
        row["intensity_notes"] = ""

    # --- Crash labels ---
    cl = crash.get(d, {})
    label = (cl.get("label") or "").strip()
    row["is_crash"] = label == "crash"
    row["is_dip"] = label == "dip"
    row["crash_episode_id"] = cl.get("episode_id") or ""
    sd = sub_dips.get(d, {})
    row["is_sub_threshold_dip"] = bool(sd)
    row["dip_type"] = sd.get("dip_type") or ""

    # --- Garmin daily activity ---
    u = uds.get(d, {})
    row["has_garmin_uds"] = bool(u)
    row["total_steps"] = u.get("total_steps") or ""
    row["moderate_min"] = u.get("moderate_min") or ""
    row["vigorous_min"] = u.get("vigorous_min") or ""
    row["total_calories"] = u.get("active_kcal") or ""
    # Wave 2: finer intensity buckets + step goal (propagated from daily_uds.csv)
    row["highly_active_sec"] = u.get("highly_active_sec") or ""
    row["active_sec"] = u.get("active_sec") or ""
    row["is_vigorous_day"] = u.get("is_vigorous_day") or ""
    row["daily_step_goal"] = u.get("daily_step_goal") or ""
    # Derived: did total_steps clear daily_step_goal? Useful as E1 calibration
    # anchor (Wiggers personal-step-threshold). Boolean; "" when either input
    # is missing.
    _ts = u.get("total_steps")
    _sg = u.get("daily_step_goal")
    if _ts and _sg:
        try:
            row["steps_above_goal_flag"] = float(_ts) >= float(_sg)
        except (ValueError, TypeError):
            row["steps_above_goal_flag"] = ""
    else:
        row["steps_above_goal_flag"] = ""

    # HR — pass Garmin's algorithmic RHR through directly.
    # An inherited 30-130 bpm sanity filter was removed 2026-06-11 after
    # the Garmin audit (see methodology/garmin_indicators_audit.md) showed
    # the observed range over 1731 days is 47-65 bpm with 0 outliers — the
    # filter was a no-op.
    row["resting_hr"] = u.get("resting_hr") or ""
    row["min_hr"] = u.get("min_hr") or ""
    row["max_hr"] = u.get("max_hr") or ""
    row["max_avg_hr_uds"] = u.get("max_avg_hr") or ""  # max-of-averages from UDS

    # --- Wave 3: Body Battery + all-day stress + respiration + SpO2 (from UDS extras) ---
    # Propagated from uds_extras_daily.csv (extracted by
    # pipeline/01_extract/garmin_uds_extras.py). All JSON-source, no FIT
    # parsing. Supports Wiggers D1-D5 (Body Battery), C1-C3 (stress), G1
    # (respiration), G4 (SpO2 — Wiggers deprioritises but included).
    ue = uds_extras.get(d, {})
    row["bb_charged_24h"] = ue.get("bb_charged_24h") or ""
    row["bb_drained_24h"] = ue.get("bb_drained_24h") or ""
    row["bb_highest"] = ue.get("bb_highest") or ""
    row["bb_lowest"] = ue.get("bb_lowest") or ""
    row["bb_sleep_start_value"] = ue.get("bb_sleep_start_value") or ""
    row["bb_sleep_end_value"] = ue.get("bb_sleep_end_value") or ""
    # bb_during_sleep_value: Garmin emits -4/-5 as sentinel for no UDS sleep BB
    # (2 dates). See drop_neg_sentinel + DATA_DICTIONARY.md sec 7B.
    row["bb_during_sleep_value"] = drop_neg_sentinel(ue.get("bb_during_sleep_value"))
    row["bb_overnight_gain"] = ue.get("bb_overnight_gain") or ""
    # Proxy + fused + audit channel for bb_overnight_gain. See methodology/bb_overnight_gain_proxy.md.
    row["bb_overnight_gain_proxy"] = ue.get("bb_overnight_gain_proxy") or ""
    row["bb_overnight_gain_best"] = ue.get("bb_overnight_gain_best") or ""
    row["bb_overnight_gain_source"] = ue.get("bb_overnight_gain_source") or ""
    # all_day / awake stress avg: -1/-2 sentinel on whole-day-void days. Max
    # values stay raw — they go to 0 not negative on those days.
    row["all_day_stress_avg"] = drop_neg_sentinel(ue.get("all_day_stress_avg"))
    row["all_day_stress_max"] = ue.get("all_day_stress_max") or ""
    row["awake_stress_avg"] = drop_neg_sentinel(ue.get("awake_stress_avg"))
    row["awake_stress_max"] = ue.get("awake_stress_max") or ""
    # asleep_stress_avg_uds: -2 sentinel on days where Garmin's UDS asleep_stress
    # didn't compute. Often (8/10) co-occurs with sleep_valid_flag=False, but
    # 2 dates have valid FIT sleep + UDS sentinel — analysts should prefer
    # stress_mean_sleep (FIT-derived) when available; see sec 7B note.
    row["asleep_stress_avg_uds"] = drop_neg_sentinel(ue.get("asleep_stress_avg_uds"))
    row["respiration_avg_waking"] = ue.get("respiration_avg_waking") or ""
    row["respiration_max_24h"] = ue.get("respiration_max_24h") or ""
    row["respiration_min_24h"] = ue.get("respiration_min_24h") or ""
    row["spo2_avg_24h"] = ue.get("spo2_avg_24h") or ""
    row["spo2_min_24h"] = ue.get("spo2_min_24h") or ""

    # --- Activity features ---
    # v3.1 columns (exertion_class, step_z_30d) retained for HA01b/HA02c
    # reproducibility; carry the rolling-baseline contamination issue
    # described in garmin_indicators_audit.md. v3.2 lagged columns
    # (baseline = [d-90, d-30]) are the default for new analyses; see
    # the column-choice matrix in wiggers_testable_hypotheses.md.
    a = af.get(d, {})
    # v3.1 (legacy, backward compat)
    row["exertion_class"] = a.get("exertion_class") or ""
    row["effective_exertion_min"] = a.get("effective_exertion_min") or ""
    row["step_z_30d"] = a.get("step_z_30d") or ""
    # v3.2 lagged-baseline (default for new analyses)
    eff_lag = a.get("effective_exertion_rank_lagged") or ""
    step_lag = a.get("step_rank_lagged") or ""
    max_hr_lag = a.get("max_hr_rank_lagged") or ""
    vig_lag = a.get("vigorous_min_rank_lagged") or ""
    row["exertion_class_lagged"] = a.get("exertion_class_lagged") or ""
    row["eff_exertion_rank_lagged"] = eff_lag
    row["step_rank_lagged"] = step_lag
    row["max_hr_rank_lagged"] = max_hr_lag
    row["vigorous_min_rank_lagged"] = vig_lag
    # Composite rank: max over the 4 axis ranks (mirrors the categorical
    # composite logic in 04_classify_exertion.py but on the underlying
    # rank scale so continuous correlation / lag-profile analyses don't
    # have to re-derive from the categorical class).
    rank_vals = [float(x) for x in (eff_lag, step_lag, max_hr_lag, vig_lag) if x not in ("", None)]
    row["exertion_rank_composite_lagged"] = max(rank_vals) if rank_vals else ""
    row["push_burden_7d_lagged"] = a.get("push_burden_7d_lagged") or ""
    row["effective_exertion_slope_28d"] = a.get("effective_exertion_slope_28d") or ""
    # Wave 2: per-axis classes (v3.1 and v3.2) + above-baseline streak.
    # Propagated from activity_features_daily.csv to support Wiggers E3
    # (per-axis comparison) and supplement E2 (streak as a direct
    # creeping-floor count complementing effective_exertion_slope_28d).
    row["class_axis_A_eff"] = a.get("class_axis_A_eff") or ""
    row["class_axis_B_step"] = a.get("class_axis_B_step") or ""
    row["class_axis_C_maxhr"] = a.get("class_axis_C_maxhr") or ""
    row["class_axis_D_vig"] = a.get("class_axis_D_vig") or ""
    row["class_axis_A_eff_lagged"] = a.get("class_axis_A_eff_lagged") or ""
    row["class_axis_B_step_lagged"] = a.get("class_axis_B_step_lagged") or ""
    row["class_axis_C_maxhr_lagged"] = a.get("class_axis_C_maxhr_lagged") or ""
    row["class_axis_D_vig_lagged"] = a.get("class_axis_D_vig_lagged") or ""
    row["above_baseline_streak"] = a.get("above_baseline_streak") or ""

    # v3.2 LC-era-only lagged variants (baseline restricted to dates >= 2022-04-04 = LCERA_START).
    # See LC_ERA_START constant and DATA_DICTIONARY.md sec 6 "v3.2 LC-era-only" for the methodological
    # rationale. Use *_lagged_lcera for PEM-pacing / Wiggers analyses where the user's pre-LC
    # healthy-capacity days would mis-rank LC-era load.
    eff_lag_lc = a.get("effective_exertion_rank_lagged_lcera") or ""
    step_lag_lc = a.get("step_rank_lagged_lcera") or ""
    max_hr_lag_lc = a.get("max_hr_rank_lagged_lcera") or ""
    vig_lag_lc = a.get("vigorous_min_rank_lagged_lcera") or ""
    row["exertion_class_lagged_lcera"] = a.get("exertion_class_lagged_lcera") or ""
    row["eff_exertion_rank_lagged_lcera"] = eff_lag_lc
    row["step_rank_lagged_lcera"] = step_lag_lc
    row["max_hr_rank_lagged_lcera"] = max_hr_lag_lc
    row["vigorous_min_rank_lagged_lcera"] = vig_lag_lc
    rank_vals_lc = [float(x) for x in (eff_lag_lc, step_lag_lc, max_hr_lag_lc, vig_lag_lc) if x not in ("", None)]
    row["exertion_rank_composite_lagged_lcera"] = max(rank_vals_lc) if rank_vals_lc else ""
    row["push_burden_7d_lagged_lcera"] = a.get("push_burden_7d_lagged_lcera") or ""
    row["class_axis_A_eff_lagged_lcera"] = a.get("class_axis_A_eff_lagged_lcera") or ""
    row["class_axis_B_step_lagged_lcera"] = a.get("class_axis_B_step_lagged_lcera") or ""
    row["class_axis_C_maxhr_lagged_lcera"] = a.get("class_axis_C_maxhr_lagged_lcera") or ""
    row["class_axis_D_vig_lagged_lcera"] = a.get("class_axis_D_vig_lagged_lcera") or ""

    # --- Sleep-stress (wake-up-date attributed; see methodology/nightly_attribution.md) ---
    s = sleep.get(d, {})
    row["sleep_start_gmt"] = s.get("sleep_start_gmt") or ""
    row["sleep_end_gmt"] = s.get("sleep_end_gmt") or ""
    row["stress_mean_sleep"] = s.get("stress_mean") or ""
    row["stress_stdev_sleep"] = s.get("stress_stdev") or ""
    sleep_valid = s.get("valid") == "1" if s else False
    row["sleep_valid_flag"] = sleep_valid
    row["has_garmin_sleep"] = sleep_valid

    # Derived: sleep_start_afternoon_flag + bedtime_hour_local + sleep_duration_min.
    # All three rely on parsing sleep_start_gmt once; co-located so the parse is shared.
    # sleep_start_afternoon_flag: True iff sleep_valid_flag AND sleep_start
    # (converted to Europe/Amsterdam, DST-correct via zoneinfo) has hour < 17.
    # Definition A from Layer 2 audit 2026-06-12; see
    # methodology/nightly_attribution.md "Afternoon sleep_start_gmt values".
    # bedtime_hour_local: fractional local hour (DST-correct), 0.0-23.99.
    # Wave 1 addition for Wiggers F4 (bedtime inconsistency).
    # sleep_duration_min: end - start in minutes. Wave 1 for Wiggers F1.
    ssg = s.get("sleep_start_gmt") or ""
    seg = s.get("sleep_end_gmt") or ""
    if sleep_valid and ssg:
        try:
            ssg_utc = datetime.fromisoformat(ssg.replace("Z", "+00:00"))
            ssg_local = ssg_utc.astimezone(TZ_LOCAL)
            row["sleep_start_afternoon_flag"] = ssg_local.hour < 17
            row["bedtime_hour_local"] = round(ssg_local.hour + ssg_local.minute / 60, 3)
        except (ValueError, TypeError):
            row["sleep_start_afternoon_flag"] = ""
            row["bedtime_hour_local"] = ""
    else:
        row["sleep_start_afternoon_flag"] = ""
        row["bedtime_hour_local"] = ""
    if sleep_valid and ssg and seg:
        try:
            ssg_utc = datetime.fromisoformat(ssg.replace("Z", "+00:00"))
            seg_utc = datetime.fromisoformat(seg.replace("Z", "+00:00"))
            row["sleep_duration_min"] = round((seg_utc - ssg_utc).total_seconds() / 60, 1)
        except (ValueError, TypeError):
            row["sleep_duration_min"] = ""
    else:
        row["sleep_duration_min"] = ""

    # --- Wave 3: Sleep stages + sleep-window respiration + sleep-window SpO2 (from sleep extras) ---
    # Propagated from sleep_extras_daily.csv (extracted by
    # pipeline/01_extract/garmin_sleep_extras.py). JSON-source, no FIT
    # parsing. Supports Wiggers F2 (deep-sleep deviation), G1 (respiration —
    # sleep-window variant complements 24h/waking), G4 (SpO2 — sleep-window
    # variant complements 24h).
    se_extras = sleep_extras.get(d, {})
    row["sleep_deep_min"] = se_extras.get("sleep_deep_min") or ""
    row["sleep_light_min"] = se_extras.get("sleep_light_min") or ""
    row["sleep_awake_min"] = se_extras.get("sleep_awake_min") or ""
    row["sleep_unmeasurable_min"] = se_extras.get("sleep_unmeasurable_min") or ""
    row["respiration_avg_sleep"] = se_extras.get("respiration_avg_sleep") or ""
    row["respiration_max_sleep"] = se_extras.get("respiration_max_sleep") or ""
    row["respiration_min_sleep"] = se_extras.get("respiration_min_sleep") or ""
    row["spo2_avg_sleep"] = se_extras.get("spo2_avg_sleep") or ""
    row["spo2_min_sleep"] = se_extras.get("spo2_min_sleep") or ""

    # --- Stress spikes ---
    sp = spike.get(d, {})
    row["max_spike_minutes"] = sp.get("max_spike_minutes") or ""

    # --- Wave 4: intraday HR + stress (operationalises Wiggers A4 + C4) ---
    # Propagated from intraday_hr_stress_daily.csv (extracted by
    # pipeline/01_extract/garmin_intraday_hr_stress.py from monitoring_b
    # FIT files; per-minute HR + stress samples summarised per day).
    # A4 columns directly test "sustained multi-hour HR elevation marks
    # real overexertion"; C4 columns directly test "after overexertion,
    # stress fails to drop during rest". Both use the WAKING window
    # (sleep-window samples are excluded — sleep dynamics are covered
    # by the existing stress_mean_sleep block).
    ihs = intraday_hr_stress.get(d, {})
    # A4 (v3 2026-06-12): personal daytime baseline (lagged [d-90, d-30])
    # + offset 20. See garmin_intraday_hr_stress.py docstring for the
    # v1 -> v2 -> v3 evolution and reviewer rationale.
    row["hr_median_waking"] = ihs.get("hr_median_waking") or ""
    row["hr_daytime_baseline_lagged"] = ihs.get("hr_daytime_baseline_lagged") or ""
    row["hr_min_above_daytime_baseline_plus_20_waking"] = ihs.get("hr_min_above_daytime_baseline_plus_20_waking") or ""
    row["hr_longest_elevated_run_min_waking"] = ihs.get("hr_longest_elevated_run_min_waking") or ""
    row["hr_sustained_elevated_flag"] = ihs.get("hr_sustained_elevated_flag") or ""
    row["hr_area_above_daytime_baseline_waking"] = ihs.get("hr_area_above_daytime_baseline_waking") or ""
    # A4 LC-era-only variants (window source restricted to dates >= LC_ERA_START
    # = 2022-04-04). Prefer these for PEM-pacing analyses; see memory
    # feedback_use_lagged_exertion_for_pem. Coverage effectively starts
    # 2022-05-18 (when 14 LC-era days have entered the window).
    row["hr_daytime_baseline_lagged_lcera"] = ihs.get("hr_daytime_baseline_lagged_lcera") or ""
    row["hr_min_above_daytime_baseline_plus_20_waking_lcera"] = ihs.get("hr_min_above_daytime_baseline_plus_20_waking_lcera") or ""
    row["hr_longest_elevated_run_min_waking_lcera"] = ihs.get("hr_longest_elevated_run_min_waking_lcera") or ""
    row["hr_sustained_elevated_flag_lcera"] = ihs.get("hr_sustained_elevated_flag_lcera") or ""
    row["hr_area_above_daytime_baseline_waking_lcera"] = ihs.get("hr_area_above_daytime_baseline_waking_lcera") or ""
    # C4 (unchanged from v1)
    row["stress_post_peak_drop_avg"] = ihs.get("stress_post_peak_drop_avg") or ""
    row["stress_post_peak_time_to_rest_min"] = ihs.get("stress_post_peak_time_to_rest_min") or ""
    row["stress_high_duration_min"] = ihs.get("stress_high_duration_min") or ""
    row["stress_recovery_pct_within_2h"] = ihs.get("stress_recovery_pct_within_2h") or ""

    # --- v24 rollup (presence-conditioned on has_note) ---
    if row["has_note"] and d in v24_per_day:
        v = v24_per_day[d]
        row["n_clauses"] = v["n_clauses"]
        for cat in V24_CATEGORIES:
            row[f"cat_{cat}"] = v["cat_counts"].get(cat, 0)
        for sub in V24_SUB_FYSIEK:
            col = V24_SUB_CSV_NAME.get(sub, sub)
            row[f"cat_sub_{col}"] = v["sub_counts"].get(sub, 0)
        for family in ("cognitief", "emotioneel", "fysiek"):
            sev = v["state_max"].get(family, 0)
            if sev > 0:
                row[f"state_symptoom_{family}"] = STATE_SEVERITY_INV[sev]
            elif family in v["state_absent_seen"]:
                row[f"state_symptoom_{family}"] = "absent"
            else:
                row[f"state_symptoom_{family}"] = ""
        pol_count = Counter(v["polarities"])
        row["day_dominant_polarity"] = pol_count.most_common(1)[0][0] if pol_count else ""
        row["n_pos_clauses"] = pol_count.get("positive", 0)
        row["n_neg_clauses"] = pol_count.get("negative", 0)
        row["n_mixed_clauses"] = pol_count.get("mixed", 0)
        row["n_neutral_clauses"] = pol_count.get("neutral", 0)
        row["neutral_forward_looking_flag"] = v["neutral_forward_looking"]
    else:
        # NaN (blank) for all v24 columns when no note / no v24 entry
        row["n_clauses"] = ""
        for cat in V24_CATEGORIES:
            row[f"cat_{cat}"] = ""
        for sub in V24_SUB_FYSIEK:
            col = V24_SUB_CSV_NAME.get(sub, sub)
            row[f"cat_sub_{col}"] = ""
        for family in ("cognitief", "emotioneel", "fysiek"):
            row[f"state_symptoom_{family}"] = ""
        row["day_dominant_polarity"] = ""
        row["n_pos_clauses"] = ""
        row["n_neg_clauses"] = ""
        row["n_mixed_clauses"] = ""
        row["n_neutral_clauses"] = ""
        row["neutral_forward_looking_flag"] = ""

    # --- Timeline events on day ---
    events = events_by_day.get(d, [])
    row["n_events_on_day"] = len(events)
    row["event_labels"] = ";".join(e["label"] for e in events)
    row["event_categories"] = ";".join(e["category"] for e in events)
    umbrellas = umbrella_by_day.get(d, [])
    row["in_umbrella"] = bool(umbrellas)
    row["umbrella_labels"] = ";".join(umbrellas)
    # Per-period umbrella booleans (the analytical surface — in_umbrella is
    # too heterogeneous to correlate against because the three periods are
    # semantically distinct and barely overlap in time).
    for col, needle in UMBRELLA_FLAGS.items():
        row[col] = any(needle in u for u in umbrellas)

    # --- PwC dossier events (subset) ---
    dossier_evs = dossier_by_day.get(d, [])
    row["dossier_event_today"] = bool(dossier_evs)
    row["dossier_event_labels"] = ";".join(e["label"] for e in dossier_evs)
    row["dossier_event_categories"] = ";".join(e["category"] for e in dossier_evs)
    row["has_pwc_dossier_window"] = WACHTTIJD_START <= d <= WACHTTIJD_END
    row["has_calendar_coverage"] = d >= CALENDAR_COVERAGE_START
    # lc_phase: three-tier categorical for LC research timeline.
    # pre_corona     date < 2022-03-21 (the user's healthy / training period)
    # corona_infection  2022-03-21 to 2022-04-03 (corona-ziek-week + post-acute
    #                recovery window; includes Fietsweekend Ardennen 2022-04-01
    #                to 2022-04-03 which the user identifies as the trigger /
    #                end-of-acute-corona event)
    # lc             date >= 2022-04-04 (LC-symptom-onset window per the
    #                LC-era marker in annotations.yaml)
    if d < CORONA_START:
        row["lc_phase"] = "pre_corona"
    elif d < LC_ERA_START:
        row["lc_phase"] = "corona_infection"
    else:
        row["lc_phase"] = "lc"

    # --- PwC work record ---
    p = pwc_hours.get(d, {})
    row["has_pwc_log"] = bool(p)
    if p:
        row["pwc_primary_hours"] = p.get("primary_hours") or ""
        row["pwc_secondary_hours"] = p.get("secondary_hours") or ""
        row["pwc_total_hours"] = p.get("total_hours") or ""
        row["pwc_illness_flag"] = p.get("illness_flag") == "1"
        row["pwc_doctor_visit_flag"] = p.get("doctor_visit_flag") == "1"
        row["pwc_amsterdam_flag"] = p.get("amsterdam_flag") == "1"
        row["pwc_vacation_flag"] = p.get("vacation_flag") == "1"
        row["pwc_toelichting"] = p.get("toelichting") or ""
    else:
        row["pwc_primary_hours"] = ""
        row["pwc_secondary_hours"] = ""
        row["pwc_total_hours"] = ""
        row["pwc_illness_flag"] = ""
        row["pwc_doctor_visit_flag"] = ""
        row["pwc_amsterdam_flag"] = ""
        row["pwc_vacation_flag"] = ""
        row["pwc_toelichting"] = ""

    return row


if __name__ == "__main__":
    main()
