"""Run H02b's spike-precursor test against crash_v2 isolated dips.

Mirrors H02b/test.py exactly in metric + null logic; only difference is
the episode list source: dips (label='dip' in labels_crash_v2.csv,
treated as single-day events) instead of crash_v1 episodes.

Question: do isolated single-day dips show the same spike-precursor
pattern as multi-day crashes? If yes -> spike events predict bad days
of any duration. If no -> spike-precursor is specifically a multi-day
PEM phenomenon.

Output: h02b_on_dips_result.md + h02b_on_dips_data.json.
"""
from __future__ import annotations

import csv
import json
import random
import statistics
import sys
from datetime import date, timedelta
from pathlib import Path

# Same locked params as H02b/test.py for direct comparability
ANALYSIS_START = date(2022, 9, 3)
TRAIN_END = date(2023, 12, 31)
VALIDATE_END = date(2026, 6, 5)

LEADUP_DAYS = 3
BASELINE_WINDOW_DAYS = 90

MIN_LEADUP_VALID = 2
MIN_BASELINE_VALID = 30
TRIMMED_PCT = 0.10

NULL_SAMPLE_SIZE = 200
RANDOM_SEED = 20260605  # IDENTICAL to H02b so null samples match

CRIT_A_FRACTION = 0.60
CRIT_A_DELTA_MIN = 10
CRIT_B_DISCRIMINATION_PP = 15
CRIT_C_MEDIAN_MIN = 5
CRIT_C_LOWER_QUARTILE_MIN = 0
MIN_EPISODES_PER_WINDOW = 10

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
LABELS_CSV = ROOT / "labels_crash_v2.csv"
SPIKE_CSV = ROOT.parent / "H02b-stress-spikes" / "daily_max_spike.csv"
OUT_DATA = ROOT / "h02b_on_dips_data.json"
OUT_MD = ROOT / "h02b_on_dips_result.md"


def load_dip_dates() -> list[date]:
    if not LABELS_CSV.exists():
        sys.exit(f"\nERROR: {LABELS_CSV} not found.\n"
                 f"Run apply_crash_v2.py first.\n")
    dates_ = []
    with LABELS_CSV.open(encoding="utf-8") as fh:
        for r in csv.DictReader(fh):
            if r["label"] == "dip":
                dates_.append(date.fromisoformat(r["date"]))
    return sorted(dates_)


def load_crash_episodes() -> list[date]:
    """Get crash start dates for null-sample exclusion."""
    if not LABELS_CSV.exists():
        sys.exit(f"\nERROR: {LABELS_CSV} not found.\n")
    starts = set()
    with LABELS_CSV.open(encoding="utf-8") as fh:
        for r in csv.DictReader(fh):
            if r["label"] == "crash":
                starts.add(date.fromisoformat(r["episode_start"]))
    return sorted(starts)


def load_spike_by_date() -> dict[date, float]:
    if not SPIKE_CSV.exists():
        sys.exit(
            f"\nERROR: {SPIKE_CSV} not found.\n"
            f"Run H02b extract_daily_max_spike.py first.\n"
        )
    out = {}
    with SPIKE_CSV.open(encoding="utf-8") as fh:
        for r in csv.DictReader(fh):
            if r["valid"] != "1":
                continue
            d = date.fromisoformat(r["date"])
            out[d] = float(r["max_spike_minutes"])
    return out


def trimmed_mean(values, trim_pct):
    if not values:
        return None
    vs = sorted(values)
    n = len(vs)
    trim = int(n * trim_pct)
    if n - 2 * trim < 1:
        return statistics.mean(vs)
    return statistics.mean(vs[trim : n - trim])


def compute_window(ref: date, spike_by_date: dict[date, float]) -> dict:
    """Same lead-up + baseline shape as H02b/test.py compute_window."""
    leadup = [ref - timedelta(days=i) for i in range(1, LEADUP_DAYS + 1)]
    baseline_start = ref - timedelta(days=BASELINE_WINDOW_DAYS + LEADUP_DAYS)
    baseline_end = ref - timedelta(days=LEADUP_DAYS + 1)
    baseline_days = []
    d = baseline_start
    while d <= baseline_end:
        baseline_days.append(d)
        d += timedelta(days=1)
    leadup_vals = [spike_by_date[d] for d in leadup if d in spike_by_date]
    baseline_vals = [spike_by_date[d] for d in baseline_days if d in spike_by_date]
    leadup_valid = len(leadup_vals) >= MIN_LEADUP_VALID
    baseline_valid = len(baseline_vals) >= MIN_BASELINE_VALID
    if leadup_valid and baseline_valid:
        leadup_max = max(leadup_vals)
        baseline_tm = trimmed_mean(baseline_vals, TRIMMED_PCT)
        delta = leadup_max - baseline_tm
        return {
            "leadup_max": leadup_max,
            "baseline_tm": baseline_tm,
            "delta": delta,
            "leadup_n": len(leadup_vals),
            "baseline_n": len(baseline_vals),
            "valid": True,
        }
    return {
        "leadup_n": len(leadup_vals),
        "baseline_n": len(baseline_vals),
        "valid": False,
    }


def build_null_sample(
    crash_starts: list[date],
    dip_dates: list[date],
    spike_by_date: dict[date, float],
) -> list[float]:
    """Random 3-day windows disjoint from both crash lead-ups and dip lead-ups."""
    rng = random.Random(RANDOM_SEED)
    occupied: set[date] = set()
    for ref in crash_starts + dip_dates:
        for i in range(1, LEADUP_DAYS + 1):
            occupied.add(ref - timedelta(days=i))
    all_dates = sorted(spike_by_date)
    # Need reference dates >= ANALYSIS_START + 93 days to fit baseline window
    min_ref = ANALYSIS_START + timedelta(days=BASELINE_WINDOW_DAYS + LEADUP_DAYS)
    candidates = [d for d in all_dates if d >= min_ref]
    null_deltas = []
    attempts = 0
    while len(null_deltas) < NULL_SAMPLE_SIZE and attempts < 10000:
        attempts += 1
        ref = rng.choice(candidates)
        leadup = {ref - timedelta(days=i) for i in range(1, LEADUP_DAYS + 1)}
        if leadup & occupied:
            continue
        prof = compute_window(ref, spike_by_date)
        if not prof["valid"]:
            continue
        null_deltas.append(prof["delta"])
    return null_deltas


def evaluate(deltas: list[float], null_deltas: list[float], label: str) -> dict:
    if len(deltas) < MIN_EPISODES_PER_WINDOW:
        return {
            "window": label,
            "verdict": "inconclusive",
            "reason": f"only {len(deltas)} usable dips (< {MIN_EPISODES_PER_WINDOW})",
            "n": len(deltas),
            "null_n": len(null_deltas),
        }
    frac_crash = sum(1 for d in deltas if d >= CRIT_A_DELTA_MIN) / len(deltas)
    frac_null = sum(1 for d in null_deltas if d >= CRIT_A_DELTA_MIN) / len(null_deltas)
    discrim_pp = (frac_crash - frac_null) * 100
    sorted_d = sorted(deltas)
    median_d = statistics.median(sorted_d)
    lower_q = sorted_d[int(len(sorted_d) * 0.25)]
    crit_a = frac_crash >= CRIT_A_FRACTION
    crit_b = discrim_pp >= CRIT_B_DISCRIMINATION_PP
    crit_c = median_d >= CRIT_C_MEDIAN_MIN and lower_q >= CRIT_C_LOWER_QUARTILE_MIN
    return {
        "window": label,
        "n": len(deltas),
        "null_n": len(null_deltas),
        "frac_dip_above_threshold": frac_crash,
        "frac_null_above_threshold": frac_null,
        "discrimination_pp": discrim_pp,
        "median_delta": median_d,
        "lower_q_delta": lower_q,
        "crit_a_pass": crit_a,
        "crit_b_pass": crit_b,
        "crit_c_pass": crit_c,
        "verdict": (
            "supported" if (crit_a and crit_b and crit_c)
            else "refuted"
        ),
    }


def write_md(train_eval, validate_eval, dip_records, n_dips_train, n_dips_validate,
             null_n):
    lines = []
    lines.append("# H02b on dips — spike-precursor test against crash_v2 tier-2\n")
    lines.append("Re-run of H02b's metric (lead-up max stress spike vs 90-day "
                 "trimmed baseline) using **single-day isolated dips** instead "
                 "of multi-day crash episodes as reference events. Same null "
                 "sample seed, same criteria, same windows.\n")
    lines.append("## Question\n")
    lines.append("Do isolated single-day dips show the same +10-minute "
                 "spike-precursor pattern as crashes? If yes, the spike "
                 "precursor is a generic 'bad day' marker. If no, it is "
                 "specifically a multi-day-crash phenomenon.\n")
    lines.append("## Reference for comparison (from H02b/result.md)\n")
    lines.append("| | train (14 crashes) | validate (15 crashes) |\n"
                 "|---|---:|---:|\n"
                 "| % crash lead-ups with delta >= +10 min | 71.4% | 33.3% |\n"
                 "| discrimination vs null (pp) | +29.9 | -8.2 |\n"
                 "| median delta_spike_minutes | +16.2 | +6.7 |\n"
                 "| verdict | SUPPORTED | refuted |\n")
    lines.append("## Dip results\n")
    lines.append("| | train | validate |\n"
                 "|---|---:|---:|\n"
                 f"| dips in window | {n_dips_train} | {n_dips_validate} |\n"
                 f"| clean dips (valid lead-up + baseline) | {train_eval.get('n','?')} | {validate_eval.get('n','?')} |\n"
                 f"| null sample size | {null_n} | {null_n} |\n"
                 f"| % dip lead-ups with delta >= +10 min | {fmt_pct(train_eval)} | {fmt_pct(validate_eval)} |\n"
                 f"| % null windows with delta >= +10 min | {fmt_null_pct(train_eval)} | {fmt_null_pct(validate_eval)} |\n"
                 f"| **discrimination (dip - null, pp)** | {fmt_discrim(train_eval)} | {fmt_discrim(validate_eval)} |\n"
                 f"| median delta_spike_minutes | {fmt_median(train_eval)} | {fmt_median(validate_eval)} |\n"
                 f"| lower-quartile delta_spike_minutes | {fmt_lq(train_eval)} | {fmt_lq(validate_eval)} |\n"
                 f"| criterion a (>=60% at +10 min) | {fmt_pass(train_eval, 'crit_a_pass')} | {fmt_pass(validate_eval, 'crit_a_pass')} |\n"
                 f"| criterion b (discrim >= +15 pp) | {fmt_pass(train_eval, 'crit_b_pass')} | {fmt_pass(validate_eval, 'crit_b_pass')} |\n"
                 f"| criterion c (median >= +5, lower-q >= 0) | {fmt_pass(train_eval, 'crit_c_pass')} | {fmt_pass(validate_eval, 'crit_c_pass')} |\n"
                 f"| **verdict** | **{train_eval.get('verdict','?').upper()}** | **{validate_eval.get('verdict','?').upper()}** |\n")
    lines.append("## How to read this\n")
    lines.append("**Both supported -> ** spike precursor predicts both crashes and dips. "
                 "It's a generic 'bad day' marker, not crash-specific.\n")
    lines.append("**Both refuted -> ** dips have a different physiological signature than "
                 "crashes. They may be mood-only events with no autonomic precursor.\n")
    lines.append("**Train supported, validate refuted -> ** same trajectory pattern as "
                 "crashes themselves: signal was real in 2022-23, faded with stabilisation. "
                 "Supports the 'kind of bad day changed' broader story.\n")
    lines.append("**Train refuted, validate supported -> ** unlikely; flag for investigation.\n")
    lines.append("## Per-dip deltas — train window\n")
    lines.append("(top 20 by |delta|)\n")
    lines.append("| date | leadup_max | baseline_tm | delta |\n"
                 "|---|---:|---:|---:|")
    train_recs = [r for r in dip_records if r["valid"] and r["in_train"]]
    train_recs.sort(key=lambda r: abs(r["delta"]), reverse=True)
    for r in train_recs[:20]:
        lines.append(f"| {r['date']} | {r['leadup_max']:.1f} | "
                     f"{r['baseline_tm']:.1f} | {r['delta']:+.1f} |")
    lines.append("")
    lines.append("## Per-dip deltas — validate window\n")
    lines.append("(top 20 by |delta|)\n")
    lines.append("| date | leadup_max | baseline_tm | delta |\n"
                 "|---|---:|---:|---:|")
    val_recs = [r for r in dip_records if r["valid"] and not r["in_train"]]
    val_recs.sort(key=lambda r: abs(r["delta"]), reverse=True)
    for r in val_recs[:20]:
        lines.append(f"| {r['date']} | {r['leadup_max']:.1f} | "
                     f"{r['baseline_tm']:.1f} | {r['delta']:+.1f} |")
    lines.append("")
    lines.append("---\n")
    lines.append(f"*Run 2026-06-06. Seed `{RANDOM_SEED}` matches H02b's null sample.*")
    OUT_MD.write_text("\n".join(lines), encoding="utf-8")


def fmt_pct(e):
    if "frac_dip_above_threshold" not in e:
        return "n/a"
    return f"{e['frac_dip_above_threshold']*100:.1f}%"


def fmt_null_pct(e):
    if "frac_null_above_threshold" not in e:
        return "n/a"
    return f"{e['frac_null_above_threshold']*100:.1f}%"


def fmt_discrim(e):
    if "discrimination_pp" not in e:
        return "n/a"
    return f"{e['discrimination_pp']:+.1f} pp"


def fmt_median(e):
    if "median_delta" not in e:
        return "n/a"
    return f"{e['median_delta']:+.1f}"


def fmt_lq(e):
    if "lower_q_delta" not in e:
        return "n/a"
    return f"{e['lower_q_delta']:+.1f}"


def fmt_pass(e, key):
    if key not in e:
        return "n/a"
    return "**PASS**" if e[key] else "fail"


def main():
    dip_dates = load_dip_dates()
    print(f"Loaded {len(dip_dates)} isolated dips")

    crash_starts = load_crash_episodes()
    print(f"Loaded {len(crash_starts)} crash episode starts (for null exclusion)")

    spike_by_date = load_spike_by_date()
    print(f"Loaded {len(spike_by_date)} valid stress days")

    # Per-dip windows
    dip_records = []
    for d in dip_dates:
        prof = compute_window(d, spike_by_date)
        rec = {
            "date": d.isoformat(),
            "in_train": d <= TRAIN_END,
            **prof,
        }
        dip_records.append(rec)

    train_recs = [r for r in dip_records if r["in_train"] and r["valid"]]
    validate_recs = [r for r in dip_records if not r["in_train"] and r["valid"]]
    print(f"  train clean dips: {len(train_recs)}")
    print(f"  validate clean dips: {len(validate_recs)}")

    null_deltas = build_null_sample(crash_starts, dip_dates, spike_by_date)
    print(f"  null sample (3-day windows, disjoint from crashes + dips): {len(null_deltas)}")

    train_deltas = [r["delta"] for r in train_recs]
    validate_deltas = [r["delta"] for r in validate_recs]
    train_eval = evaluate(train_deltas, null_deltas, "train")
    validate_eval = evaluate(validate_deltas, null_deltas, "validate")

    print(f"  train:    {train_eval.get('verdict')}  "
          f"(n={train_eval.get('n')}, discrim={train_eval.get('discrimination_pp', 'n/a')})")
    print(f"  validate: {validate_eval.get('verdict')}  "
          f"(n={validate_eval.get('n')}, discrim={validate_eval.get('discrimination_pp', 'n/a')})")

    OUT_DATA.write_text(json.dumps({
        "train": train_eval,
        "validate": validate_eval,
        "n_dips_total": len(dip_dates),
        "n_dips_train": sum(1 for r in dip_records if r["in_train"]),
        "n_dips_validate": sum(1 for r in dip_records if not r["in_train"]),
        "null_n": len(null_deltas),
        "params": {
            "leadup_days": LEADUP_DAYS,
            "baseline_window_days": BASELINE_WINDOW_DAYS,
            "delta_threshold_min": CRIT_A_DELTA_MIN,
            "null_sample_size": NULL_SAMPLE_SIZE,
            "random_seed": RANDOM_SEED,
        },
        "dips": dip_records,
    }, indent=2), encoding="utf-8")

    write_md(train_eval, validate_eval, dip_records,
             sum(1 for r in dip_records if r["in_train"]),
             sum(1 for r in dip_records if not r["in_train"]),
             len(null_deltas))
    print(f"Wrote {OUT_MD}")
    print(f"Wrote {OUT_DATA}")


if __name__ == "__main__":
    main()
