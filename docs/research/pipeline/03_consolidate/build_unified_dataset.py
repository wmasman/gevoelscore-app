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
import os
from collections import Counter, defaultdict
from datetime import date, timedelta
from pathlib import Path

import yaml


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
# NOTE: an earlier draft included a `stabilisation_period` bool with
# arbitrary boundaries (2024-01-01 → 2025-06-30). Removed 2026-06-11 per
# user feedback: that boundary is not pre-registered, not data-driven, and
# belongs in descriptive-analysis output rather than the schema. See
# DATA_DICTIONARY.md update log.

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
            dossier_by_day,
        )
        rows.append(row)

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
              umbrella_by_day, dossier_by_day):
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

    # HR — pass Garmin's algorithmic RHR through directly.
    # An inherited 30-130 bpm sanity filter was removed 2026-06-11 after
    # the Garmin audit (see methodology/garmin_indicators_audit.md) showed
    # the observed range over 1731 days is 47-65 bpm with 0 outliers — the
    # filter was a no-op.
    row["resting_hr"] = u.get("resting_hr") or ""
    row["min_hr"] = u.get("min_hr") or ""
    row["max_hr"] = u.get("max_hr") or ""
    row["max_avg_hr_uds"] = u.get("max_avg_hr") or ""  # max-of-averages from UDS

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

    # --- Sleep-stress (wake-up-date attributed; see methodology/nightly_attribution.md) ---
    s = sleep.get(d, {})
    row["sleep_start_gmt"] = s.get("sleep_start_gmt") or ""
    row["sleep_end_gmt"] = s.get("sleep_end_gmt") or ""
    row["stress_mean_sleep"] = s.get("stress_mean") or ""
    row["stress_stdev_sleep"] = s.get("stress_stdev") or ""
    sleep_valid = s.get("valid") == "1" if s else False
    row["sleep_valid_flag"] = sleep_valid
    row["has_garmin_sleep"] = sleep_valid

    # --- Stress spikes ---
    sp = spike.get(d, {})
    row["max_spike_minutes"] = sp.get("max_spike_minutes") or ""

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

    # --- PwC dossier events (subset) ---
    dossier_evs = dossier_by_day.get(d, [])
    row["dossier_event_today"] = bool(dossier_evs)
    row["dossier_event_labels"] = ";".join(e["label"] for e in dossier_evs)
    row["dossier_event_categories"] = ";".join(e["category"] for e in dossier_evs)
    row["has_pwc_dossier_window"] = WACHTTIJD_START <= d <= WACHTTIJD_END

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
