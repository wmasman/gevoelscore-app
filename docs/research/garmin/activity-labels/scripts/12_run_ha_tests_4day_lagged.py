"""Run bundled HA01b-recomputed + HA02c re-test on A.1 lagged baseline.

Pre-registered 2026-06-06 in severity_spec.md sec Lagged baseline (v3.2)
and registry.md sec 4b Theme A entry, BEFORE this script ran. The
pre-commitments are:

- Same SUPPORTED bar as the original HA01b/HA02b runs:
  - crit (a) frequency >= 60% of crash episodes
  - crit (b) discrimination >= +15 pp above null
  - crit (c) magnitude (median + lower-q on the metric)
- Both tests evaluated together as a single bundle (symmetric re-test
  discipline, not selective rescue).
- Same null seed (20260605) and same 4-day lead-up window as
  09_run_ha_tests_4day.py for direct comparability.

The only differences from script 09 are the metric columns read:
- exertion_class_lagged instead of exertion_class
- push_burden_7d_lagged instead of push_burden_7d

Output: ha_results_4day_lagged.md + ha_results_4day_lagged.json.

Verdict interpretation:
- HA01b-recomputed stays SUPPORTED (>= +15 pp on lagged) -> the
  validate-era precursor headline holds; the original +17.3 pp
  was robust to the baseline construction.
- HA01b-recomputed weakens below +15 pp -> the headline softens,
  the original finding was partly a rolling-baseline artifact.
- HA02c becomes SUPPORTED on lagged -> push burden was real but
  the rolling baseline was masking it.
- HA02c stays refuted -> push burden is genuinely not a precursor
  for this person, on either reference frame.
"""
from __future__ import annotations

import csv
import json
import random
import statistics
from datetime import date, timedelta
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
FEATURES_CSV = ROOT / "output" / "activity_features_daily.csv"
LABELS_CSV = (
    ROOT.parent / "hypotheses" / "crash_v2-definition" / "labels_crash_v2.csv"
)
OUT_MD = ROOT / "output" / "ha_results_4day_lagged.md"
OUT_JSON = ROOT / "output" / "ha_results_4day_lagged.json"

# Match script 09 exactly for direct comparability
ANALYSIS_START = date(2022, 9, 3)
TRAIN_END = date(2023, 12, 31)
VALIDATE_END = date(2026, 6, 5)
LEADUP_DAYS = 4
NULL_SAMPLE_SIZE = 200
RANDOM_SEED = 20260605

SHOCK_CLASSES = {"heavy", "very_heavy"}
PUSH_T = 3

CRIT_A_FRAC = 0.60
CRIT_B_DISC_PP = 15

# HA01 criterion C
HA01_MEDIAN_MIN = 1
HA01_LQ_MIN = 0

# HA02 criterion C
HA02_MEDIAN_MIN = 3
HA02_LQ_MIN = 2

# Lagged column names (the only substantive difference from script 09)
EXERTION_CLASS_COL = "exertion_class_lagged"
PUSH_BURDEN_COL = "push_burden_7d_lagged"


def load_features() -> dict[date, dict]:
    out = {}
    for r in csv.DictReader(FEATURES_CSV.open(encoding="utf-8")):
        out[date.fromisoformat(r["date"])] = r
    return out


def load_crashes_and_dips() -> tuple[list[date], list[date]]:
    crashes_by_id: dict[str, list[date]] = {}
    dips = []
    for r in csv.DictReader(LABELS_CSV.open(encoding="utf-8")):
        d = date.fromisoformat(r["date"])
        if r["label"] == "crash":
            crashes_by_id.setdefault(r["episode_id"], []).append(d)
        elif r["label"] == "dip":
            dips.append(d)
    crash_starts = sorted(min(ds) for ds in crashes_by_id.values())
    return crash_starts, sorted(dips)


def parse_int(v):
    if v in (None, "", "None"):
        return None
    try:
        return int(float(v))
    except ValueError:
        return None


def compute_window_metrics(ref: date, features: dict[date, dict]) -> dict | None:
    leadup_days = [ref - timedelta(days=i) for i in range(1, LEADUP_DAYS + 1)]
    leadup_rows = [features.get(d) for d in leadup_days]
    valid_rows = [r for r in leadup_rows if r and r.get(EXERTION_CLASS_COL)]
    if len(valid_rows) < 2:
        return None

    n_shock = sum(
        1 for r in valid_rows if r[EXERTION_CLASS_COL] in SHOCK_CLASSES
    )
    push_values = []
    for r in valid_rows:
        pb = parse_int(r.get(PUSH_BURDEN_COL))
        if pb is not None:
            push_values.append(pb)
    max_push = max(push_values) if push_values else 0

    return {
        "n_shock_days": n_shock,
        "has_shock": n_shock >= 1,
        "max_push_7d": max_push,
        "has_push": max_push >= PUSH_T,
        "n_valid_days": len(valid_rows),
    }


def build_null_sample(
    features: dict[date, dict],
    crash_starts: list[date],
    dip_dates: list[date],
) -> list[dict]:
    rng = random.Random(RANDOM_SEED)
    occupied: set[date] = set()
    for ref in crash_starts + dip_dates:
        for i in range(1, LEADUP_DAYS + 1):
            occupied.add(ref - timedelta(days=i))

    all_dates = sorted(
        d for d in features if ANALYSIS_START + timedelta(days=10) <= d <= VALIDATE_END
    )
    out = []
    attempts = 0
    while len(out) < NULL_SAMPLE_SIZE and attempts < 10000:
        attempts += 1
        ref = rng.choice(all_dates)
        leadup = {ref - timedelta(days=i) for i in range(1, LEADUP_DAYS + 1)}
        if leadup & occupied:
            continue
        m = compute_window_metrics(ref, features)
        if m is None:
            continue
        out.append({"ref": ref, **m})
    return out


def evaluate_HA01(events: list[dict], null: list[dict], label: str) -> dict:
    if len(events) < 10:
        return {
            "test": f"HA01b-recomputed ({label})",
            "verdict": "inconclusive",
            "n_clean": len(events),
        }
    frac_event = sum(1 for e in events if e["has_shock"]) / len(events)
    frac_null = sum(1 for e in null if e["has_shock"]) / len(null)
    disc_pp = (frac_event - frac_null) * 100
    shock_counts = sorted(e["n_shock_days"] for e in events)
    median_count = statistics.median(shock_counts)
    lq_count = shock_counts[int(len(shock_counts) * 0.25)]

    a = frac_event >= CRIT_A_FRAC
    b = disc_pp >= CRIT_B_DISC_PP
    c = median_count >= HA01_MEDIAN_MIN and lq_count >= HA01_LQ_MIN

    return {
        "test": f"HA01b-recomputed ({label})",
        "n_clean": len(events),
        "n_null": len(null),
        "frac_event_with_shock": frac_event,
        "frac_null_with_shock": frac_null,
        "discrimination_pp": disc_pp,
        "median_n_shock_days": median_count,
        "lower_q_n_shock_days": lq_count,
        "crit_a_pass": a,
        "crit_b_pass": b,
        "crit_c_pass": c,
        "verdict": "supported" if (a and b and c) else "refuted",
    }


def evaluate_HA02(events: list[dict], null: list[dict], label: str) -> dict:
    if len(events) < 10:
        return {
            "test": f"HA02c ({label})",
            "verdict": "inconclusive",
            "n_clean": len(events),
        }
    frac_event = sum(1 for e in events if e["has_push"]) / len(events)
    frac_null = sum(1 for e in null if e["has_push"]) / len(null)
    disc_pp = (frac_event - frac_null) * 100
    push_vals = sorted(e["max_push_7d"] for e in events)
    median_push = statistics.median(push_vals)
    lq_push = push_vals[int(len(push_vals) * 0.25)]

    a = frac_event >= CRIT_A_FRAC
    b = disc_pp >= CRIT_B_DISC_PP
    c = median_push >= HA02_MEDIAN_MIN and lq_push >= HA02_LQ_MIN

    return {
        "test": f"HA02c ({label})",
        "n_clean": len(events),
        "n_null": len(null),
        "frac_event_above_T": frac_event,
        "frac_null_above_T": frac_null,
        "discrimination_pp": disc_pp,
        "median_max_push_7d": median_push,
        "lower_q_max_push_7d": lq_push,
        "crit_a_pass": a,
        "crit_b_pass": b,
        "crit_c_pass": c,
        "verdict": "supported" if (a and b and c) else "refuted",
    }


# Original numbers from ha_results_4day.md (script 09) for direct comparison
ORIGINAL_HA01B = {
    "train_crash": {"frac": 84.6, "disc": 8.6, "median_shock": 1, "lq_shock": 0, "verdict": "refuted"},
    "validate_crash": {"frac": 93.3, "disc": 17.3, "median_shock": 2, "lq_shock": 1, "verdict": "supported"},
}
ORIGINAL_HA02B = {
    "train_crash": {"frac": 23.1, "disc": -2.0, "median_push": 2, "lq_push": 1, "verdict": "refuted"},
    "validate_crash": {"frac": 6.7, "disc": -7.4, "median_push": 1, "lq_push": 1, "verdict": "refuted"},
}


def main():
    features = load_features()
    crash_starts, dip_dates = load_crashes_and_dips()
    print(f"Loaded {len(features)} feature days | "
          f"{len(crash_starts)} crashes | {len(dip_dates)} dips")

    train_crashes = [d for d in crash_starts if d <= TRAIN_END]
    validate_crashes = [d for d in crash_starts if d > TRAIN_END]
    print(f"  train: {len(train_crashes)} crashes")
    print(f"  validate: {len(validate_crashes)} crashes")

    null_records = build_null_sample(features, crash_starts, dip_dates)
    print(f"  null sample: {len(null_records)} (target {NULL_SAMPLE_SIZE})")

    def collect_metrics(refs):
        out = []
        for d in refs:
            m = compute_window_metrics(d, features)
            if m is None:
                continue
            out.append({"ref": d, **m})
        return out

    train_crash_m = collect_metrics(train_crashes)
    validate_crash_m = collect_metrics(validate_crashes)
    print(f"  clean events: train crash {len(train_crash_m)}, "
          f"validate crash {len(validate_crash_m)}")

    if len(train_crash_m) < len(train_crashes):
        dropped = len(train_crashes) - len(train_crash_m)
        print(f"  WARNING: {dropped} train crashes dropped (lagged-rank boundary)")
    if len(validate_crash_m) < len(validate_crashes):
        dropped = len(validate_crashes) - len(validate_crash_m)
        print(f"  WARNING: {dropped} validate crashes dropped (lagged-rank boundary)")

    results = {
        "HA01b_train_crash": evaluate_HA01(train_crash_m, null_records, "train crash"),
        "HA01b_validate_crash": evaluate_HA01(validate_crash_m, null_records, "validate crash"),
        "HA02c_train_crash": evaluate_HA02(train_crash_m, null_records, "train crash"),
        "HA02c_validate_crash": evaluate_HA02(validate_crash_m, null_records, "validate crash"),
    }

    OUT_JSON.write_text(json.dumps(results, indent=2, default=str), encoding="utf-8")

    # Render report
    lines = []
    lines.append("# HA01b-recomputed + HA02c bundled re-test (A.1 lagged baseline)\n")
    lines.append("Pre-registered 2026-06-06 in [severity_spec.md "
                 "§Lagged baseline (v3.2)](../spec/severity_spec.md) and "
                 "[registry.md §4b Theme A](../../hypotheses/registry.md) "
                 "BEFORE this script ran. Same SUPPORTED bar as the "
                 "original HA01b/HA02b runs (freq ≥60%, disc ≥+15 pp, "
                 "magnitude). Same null seed (`20260605`) and same 4-day "
                 "lead-up window as [09_run_ha_tests_4day.py](../scripts/09_run_ha_tests_4day.py) "
                 "for direct comparability.\n")
    lines.append("Bundled (both tests run together on the same A.1 "
                 "reference) to maintain symmetric re-test discipline: "
                 "re-testing only the refutation while keeping the win "
                 "as-is would be selective rescue.\n")

    # HA01b-recomputed
    lines.append("---\n")
    lines.append("## HA01b-recomputed (validate the win on lagged baseline)\n")
    for key, label in [("HA01b_train_crash", "train crash"),
                       ("HA01b_validate_crash", "validate crash")]:
        r = results[key]
        orig_key = key.replace("HA01b_", "").replace("_crash", "_crash")
        orig = ORIGINAL_HA01B.get(orig_key.replace("_crash", "_crash"))
        # Map keys
        orig_label = {
            "HA01b_train_crash": "train_crash",
            "HA01b_validate_crash": "validate_crash",
        }[key]
        orig = ORIGINAL_HA01B[orig_label]

        lines.append(f"### {r['test']}\n")
        if r["verdict"] == "inconclusive":
            lines.append(f"INCONCLUSIVE (n_clean={r['n_clean']} < 10).\n")
            continue
        lines.append(f"- n events clean: **{r['n_clean']}** | null sample: {r['n_null']}")
        lines.append(f"- frac event with shock (heavy+): "
                     f"**{r['frac_event_with_shock']*100:.1f}%** "
                     f"| frac null: {r['frac_null_with_shock']*100:.1f}%")
        lines.append(f"- median n_shock_days: **{r['median_n_shock_days']}** "
                     f"| lower-q: {r['lower_q_n_shock_days']}")
        lines.append(f"- discrimination: **{r['discrimination_pp']:+.1f} pp**")
        lines.append(f"- crit (a) freq ≥{int(CRIT_A_FRAC*100)}%: "
                     f"{'**PASS**' if r['crit_a_pass'] else 'fail'}")
        lines.append(f"- crit (b) disc ≥+{CRIT_B_DISC_PP} pp: "
                     f"{'**PASS**' if r['crit_b_pass'] else 'fail'}")
        lines.append(f"- crit (c) magnitude: "
                     f"{'**PASS**' if r['crit_c_pass'] else 'fail'}")
        lines.append(f"- **verdict: {r['verdict'].upper()}**\n")
        # Direct side-by-side comparison with the original rolling-baseline run
        lines.append("Side-by-side with the original HA01b (rolling baseline, "
                     "[ha_results_4day.md](../output/ha_results_4day.md)):\n")
        lines.append(f"| metric | rolling (original) | lagged (recomputed) | delta |")
        lines.append(f"|---|---:|---:|---:|")
        delta_frac = r['frac_event_with_shock']*100 - orig['frac']
        delta_disc = r['discrimination_pp'] - orig['disc']
        lines.append(f"| frac event with shock | {orig['frac']:.1f}% | "
                     f"{r['frac_event_with_shock']*100:.1f}% | {delta_frac:+.1f} pp |")
        lines.append(f"| discrimination       | {orig['disc']:+.1f} pp | "
                     f"{r['discrimination_pp']:+.1f} pp | {delta_disc:+.1f} pp |")
        lines.append(f"| verdict              | {orig['verdict']} | "
                     f"{r['verdict']} | {'same' if r['verdict']==orig['verdict'] else 'CHANGED'} |\n")

    # HA02c
    lines.append("---\n")
    lines.append("## HA02c (test if push burden was masked by the rolling baseline)\n")
    for key in ["HA02c_train_crash", "HA02c_validate_crash"]:
        r = results[key]
        orig_label = {
            "HA02c_train_crash": "train_crash",
            "HA02c_validate_crash": "validate_crash",
        }[key]
        orig = ORIGINAL_HA02B[orig_label]

        lines.append(f"### {r['test']}\n")
        if r["verdict"] == "inconclusive":
            lines.append(f"INCONCLUSIVE (n_clean={r['n_clean']} < 10).\n")
            continue
        lines.append(f"- n events clean: **{r['n_clean']}** | null sample: {r['n_null']}")
        lines.append(f"- frac event with max_push ≥{PUSH_T}: "
                     f"**{r['frac_event_above_T']*100:.1f}%** "
                     f"| frac null: {r['frac_null_above_T']*100:.1f}%")
        lines.append(f"- median max_push_7d: **{r['median_max_push_7d']}** "
                     f"| lower-q: {r['lower_q_max_push_7d']}")
        lines.append(f"- discrimination: **{r['discrimination_pp']:+.1f} pp**")
        lines.append(f"- crit (a) freq ≥{int(CRIT_A_FRAC*100)}%: "
                     f"{'**PASS**' if r['crit_a_pass'] else 'fail'}")
        lines.append(f"- crit (b) disc ≥+{CRIT_B_DISC_PP} pp: "
                     f"{'**PASS**' if r['crit_b_pass'] else 'fail'}")
        lines.append(f"- crit (c) magnitude: "
                     f"{'**PASS**' if r['crit_c_pass'] else 'fail'}")
        lines.append(f"- **verdict: {r['verdict'].upper()}**\n")
        # Side-by-side
        lines.append("Side-by-side with the original HA02b (rolling baseline, "
                     "[ha_results_4day.md](../output/ha_results_4day.md)):\n")
        lines.append(f"| metric | rolling (original) | lagged (recomputed) | delta |")
        lines.append(f"|---|---:|---:|---:|")
        delta_frac = r['frac_event_above_T']*100 - orig['frac']
        delta_disc = r['discrimination_pp'] - orig['disc']
        lines.append(f"| frac event ≥push_T   | {orig['frac']:.1f}% | "
                     f"{r['frac_event_above_T']*100:.1f}% | {delta_frac:+.1f} pp |")
        lines.append(f"| discrimination       | {orig['disc']:+.1f} pp | "
                     f"{r['discrimination_pp']:+.1f} pp | {delta_disc:+.1f} pp |")
        lines.append(f"| verdict              | {orig['verdict']} | "
                     f"{r['verdict']} | {'same' if r['verdict']==orig['verdict'] else 'CHANGED'} |\n")

    # Bundled headline verdict
    lines.append("---\n")
    lines.append("## Bundled re-test headline\n")
    h1b_train = results["HA01b_train_crash"]["verdict"]
    h1b_val = results["HA01b_validate_crash"]["verdict"]
    h2c_train = results["HA02c_train_crash"]["verdict"]
    h2c_val = results["HA02c_validate_crash"]["verdict"]

    h1b_val_disc = results["HA01b_validate_crash"].get("discrimination_pp", 0)
    h2c_val_disc = results["HA02c_validate_crash"].get("discrimination_pp", 0)

    lines.append(f"- **HA01b-recomputed validate**: {h1b_val.upper()} "
                 f"({h1b_val_disc:+.1f} pp on lagged baseline; "
                 f"original rolling was +17.3 pp)")
    lines.append(f"- **HA01b-recomputed train**: {h1b_train.upper()}")
    lines.append(f"- **HA02c validate**: {h2c_val.upper()} "
                 f"({h2c_val_disc:+.1f} pp on lagged baseline; "
                 f"original rolling was -7.4 pp)")
    lines.append(f"- **HA02c train**: {h2c_train.upper()}")
    lines.append("")
    if h1b_val == "supported":
        lines.append(f"**HA01b validate-era finding holds on lagged baseline** "
                     f"({h1b_val_disc:+.1f} pp ≥ +15 pp). The +17.3 pp "
                     f"original was robust to the baseline construction.")
    else:
        delta = h1b_val_disc - 17.3
        lines.append(f"**HA01b validate-era finding softens on lagged baseline** "
                     f"({h1b_val_disc:+.1f} pp < +15 pp; "
                     f"delta vs original +17.3 pp = {delta:+.1f} pp). "
                     f"The addendum's 'first SUPPORTED validate-era precursor' "
                     f"headline needs to soften accordingly. Honest accountancy.")
    lines.append("")
    if h2c_val == "supported":
        lines.append(f"**HA02c becomes SUPPORTED on lagged baseline**: "
                     f"push burden WAS a real validate-era precursor; "
                     f"the rolling baseline was masking it. This is the "
                     f"specific bug Theme A predicted.")
    else:
        lines.append(f"**HA02c stays refuted on lagged baseline**: "
                     f"push burden is not a precursor for this person "
                     f"on either reference frame. The Theme A fix improves "
                     f"the metric's measurement-theoretic standing but "
                     f"does not resurrect it as a predictor.")
    lines.append("")
    lines.append("---\n")
    lines.append(f"*Run 2026-06-06. Seed `{RANDOM_SEED}` matches scripts 08/09.*")
    OUT_MD.write_text("\n".join(lines), encoding="utf-8")

    print(f"\nWrote {OUT_MD}")
    print(f"Wrote {OUT_JSON}")

    # Headline summary on stdout
    print("\n=== Bundled verdicts ===")
    for key in ["HA01b_train_crash", "HA01b_validate_crash",
                "HA02c_train_crash", "HA02c_validate_crash"]:
        r = results[key]
        if "discrimination_pp" in r:
            print(f"  {r['test']:42}: {r['verdict']:>10}  "
                  f"(disc {r['discrimination_pp']:+.1f} pp)")
        else:
            print(f"  {r['test']:42}: {r['verdict']:>10}")

    print("\n=== Side-by-side validate-era discrimination ===")
    print(f"  HA01b: rolling +17.3 pp -> lagged "
          f"{results['HA01b_validate_crash'].get('discrimination_pp', 0):+.1f} pp")
    print(f"  HA02b/c: rolling  -7.4 pp -> lagged "
          f"{results['HA02c_validate_crash'].get('discrimination_pp', 0):+.1f} pp")


if __name__ == "__main__":
    main()
