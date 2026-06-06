"""Run HA01 + HA02 + HA05 pre-registered tests.

Per hypotheses.md, mirrors H02b's bar shape:
  (a) Frequency >= 60% of crashes have precursor
  (b) Discrimination >= +15 pp vs null
  (c) Magnitude criteria specific to each test

All three required, both train and validate windows.

Output: ha_results.md + ha_results.json.
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
OUT_MD = ROOT / "output" / "ha_results.md"
OUT_JSON = ROOT / "output" / "ha_results.json"

ANALYSIS_START = date(2022, 9, 3)
TRAIN_END = date(2023, 12, 31)
VALIDATE_END = date(2026, 6, 5)
LEADUP_DAYS = 3
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


def load_features() -> dict[date, dict]:
    out = {}
    for r in csv.DictReader(FEATURES_CSV.open(encoding="utf-8")):
        out[date.fromisoformat(r["date"])] = r
    return out


def load_crashes_and_dips() -> tuple[list[date], list[date]]:
    """Crash episode start dates and dip dates."""
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
    """Compute n_shock_days and max_push_7d for the lead-up to ref."""
    leadup_days = [ref - timedelta(days=i) for i in range(1, LEADUP_DAYS + 1)]
    leadup_rows = [features.get(d) for d in leadup_days]
    valid_rows = [r for r in leadup_rows if r and r.get("exertion_class")]
    if len(valid_rows) < 2:
        return None

    n_shock = sum(
        1 for r in valid_rows if r["exertion_class"] in SHOCK_CLASSES
    )
    push_values = []
    for r in valid_rows:
        pb = parse_int(r.get("push_burden_7d"))
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
    """Random 3-day windows disjoint from crash + dip lead-ups."""
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
            "test": f"HA01 ({label})",
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
        "test": f"HA01 ({label})",
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
            "test": f"HA02 ({label})",
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
        "test": f"HA02 ({label})",
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


def main():
    features = load_features()
    crash_starts, dip_dates = load_crashes_and_dips()
    print(f"Loaded {len(features)} feature days | "
          f"{len(crash_starts)} crashes | {len(dip_dates)} dips")

    # Window split
    train_crashes = [d for d in crash_starts if d <= TRAIN_END]
    validate_crashes = [d for d in crash_starts if d > TRAIN_END]
    train_dips = [d for d in dip_dates if d <= TRAIN_END]
    validate_dips = [d for d in dip_dates if d > TRAIN_END]
    print(f"  train: {len(train_crashes)} crashes, {len(train_dips)} dips")
    print(f"  validate: {len(validate_crashes)} crashes, {len(validate_dips)} dips")

    # Build null
    null_records = build_null_sample(features, crash_starts, dip_dates)
    print(f"  null sample: {len(null_records)}")

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
    train_dip_m = collect_metrics(train_dips)
    validate_dip_m = collect_metrics(validate_dips)

    print(f"  clean events: train crash {len(train_crash_m)}, "
          f"validate crash {len(validate_crash_m)}, "
          f"train dip {len(train_dip_m)}, validate dip {len(validate_dip_m)}")

    # Run tests
    results = {
        "HA01_train_crash": evaluate_HA01(train_crash_m, null_records, "train crash"),
        "HA01_validate_crash": evaluate_HA01(validate_crash_m, null_records, "validate crash"),
        "HA02_train_crash": evaluate_HA02(train_crash_m, null_records, "train crash"),
        "HA02_validate_crash": evaluate_HA02(validate_crash_m, null_records, "validate crash"),
        "HA01_train_dip": evaluate_HA01(train_dip_m, null_records, "train dip"),
        "HA01_validate_dip": evaluate_HA01(validate_dip_m, null_records, "validate dip"),
        "HA02_train_dip": evaluate_HA02(train_dip_m, null_records, "train dip"),
        "HA02_validate_dip": evaluate_HA02(validate_dip_m, null_records, "validate dip"),
    }

    # HA05: discrimination ratio
    ha05 = {
        "HA01_train_crash_disc": results["HA01_train_crash"].get("discrimination_pp"),
        "HA01_train_dip_disc": results["HA01_train_dip"].get("discrimination_pp"),
        "HA02_train_crash_disc": results["HA02_train_crash"].get("discrimination_pp"),
        "HA02_train_dip_disc": results["HA02_train_dip"].get("discrimination_pp"),
    }
    if ha05["HA01_train_dip_disc"] and ha05["HA01_train_dip_disc"] != 0:
        ha05["HA01_disc_ratio"] = ha05["HA01_train_crash_disc"] / ha05["HA01_train_dip_disc"]
    else:
        ha05["HA01_disc_ratio"] = None
    if ha05["HA02_train_dip_disc"] and ha05["HA02_train_dip_disc"] != 0:
        ha05["HA02_disc_ratio"] = ha05["HA02_train_crash_disc"] / ha05["HA02_train_dip_disc"]
    else:
        ha05["HA02_disc_ratio"] = None

    # HA05 verdict
    ha01_ratio_ok = ha05["HA01_disc_ratio"] is not None and ha05["HA01_disc_ratio"] >= 2
    ha02_ratio_ok = ha05["HA02_disc_ratio"] is not None and ha05["HA02_disc_ratio"] >= 2
    ha05["verdict"] = "supported" if (ha01_ratio_ok and ha02_ratio_ok) else "refuted"
    results["HA05"] = ha05

    # Save raw JSON
    OUT_JSON.write_text(json.dumps(results, indent=2, default=str), encoding="utf-8")

    # Render report
    lines = []
    lines.append("# HA01 + HA02 + HA05 — Activity-vs-PEM test results\n")
    lines.append("Pre-registered 2026-06-06; criteria locked before run. "
                 "All three criteria required, both windows, for 'supported'.\n")

    for key in ["HA01_train_crash", "HA01_validate_crash",
                "HA02_train_crash", "HA02_validate_crash"]:
        r = results[key]
        lines.append(f"## {r['test']}\n")
        if r["verdict"] == "inconclusive":
            lines.append(f"INCONCLUSIVE (n_clean={r['n_clean']} < 10).\n")
            continue
        lines.append(f"- n events clean: **{r['n_clean']}** | null sample: {r['n_null']}")
        if "frac_event_with_shock" in r:
            lines.append(f"- frac event with shock: **{r['frac_event_with_shock']*100:.1f}%** "
                         f"| frac null: {r['frac_null_with_shock']*100:.1f}%")
            lines.append(f"- median n_shock_days: **{r['median_n_shock_days']}** "
                         f"| lower-q: {r['lower_q_n_shock_days']}")
        else:
            lines.append(f"- frac event >=push_T: **{r['frac_event_above_T']*100:.1f}%** "
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

    # HA05 section
    lines.append("## HA05 — Crash-vs-dip discrimination ratio\n")
    lines.append(f"- HA01 train: crash disc = {ha05['HA01_train_crash_disc']:+.1f} pp, "
                 f"dip disc = {ha05['HA01_train_dip_disc']:+.1f} pp, "
                 f"ratio = {ha05['HA01_disc_ratio']:.2f}x" if ha05['HA01_disc_ratio'] is not None
                 else f"- HA01 train: dip discrimination is 0 — ratio undefined")
    lines.append(f"- HA02 train: crash disc = {ha05['HA02_train_crash_disc']:+.1f} pp, "
                 f"dip disc = {ha05['HA02_train_dip_disc']:+.1f} pp, "
                 f"ratio = {ha05['HA02_disc_ratio']:.2f}x" if ha05['HA02_disc_ratio'] is not None
                 else f"- HA02 train: dip discrimination is 0 — ratio undefined")
    lines.append(f"\n**verdict: {ha05['verdict'].upper()}** "
                 "(supported if both ratios ≥2)\n")

    # Dip tests for reference
    lines.append("## Reference: HA01 + HA02 on dips (informs HA05)\n")
    for key in ["HA01_train_dip", "HA01_validate_dip",
                "HA02_train_dip", "HA02_validate_dip"]:
        r = results[key]
        if r["verdict"] == "inconclusive":
            lines.append(f"- {r['test']}: INCONCLUSIVE\n")
            continue
        v = "frac_event_with_shock" if "frac_event_with_shock" in r else "frac_event_above_T"
        lines.append(f"- {r['test']}: frac={r[v]*100:.1f}%, "
                     f"disc={r['discrimination_pp']:+.1f} pp, "
                     f"verdict={r['verdict']}")
    lines.append("")

    lines.append("---\n")
    lines.append(f"*Run 2026-06-06. Seed `{RANDOM_SEED}` matches H02b.*")
    OUT_MD.write_text("\n".join(lines), encoding="utf-8")

    print(f"\nWrote {OUT_MD}")
    print(f"Wrote {OUT_JSON}")

    # Headline summary on stdout
    print("\n=== Verdicts ===")
    for key in ["HA01_train_crash", "HA01_validate_crash",
                "HA02_train_crash", "HA02_validate_crash"]:
        r = results[key]
        if "discrimination_pp" in r:
            print(f"  {r['test']:32}: {r['verdict']:>11}  "
                  f"(disc {r['discrimination_pp']:+.1f} pp)")
        else:
            print(f"  {r['test']:32}: {r['verdict']:>11}")
    print(f"  HA05 (crash >= 2x dip on disc): {results['HA05']['verdict']}")


if __name__ == "__main__":
    main()
