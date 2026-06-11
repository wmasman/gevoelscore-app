"""S02b -- Score-lead lagged correlation.

Implements the pre-registered spec at hypothesis.md. Computes Spearman
rho between score(t) and metric(t + lag) for pre-committed lag values
(149d for avg stress, 100d for max spike), plus same-day rho on the
same pair-window for comparison. Block-bootstrap CI (90-day blocks,
10 000 iter).

Outputs:
  - lagged_correlation_results.csv
  - lagged_correlation_plot.png

Verdict against the locked SUPPORTED bar (S3.5 in hypothesis.md)
printed to stdout for copy into notes.md.
"""
from __future__ import annotations

import csv
import json
import random
import statistics
from datetime import date, timedelta
from pathlib import Path

# Locked parameters (mirror S02 S3.8)
BOOTSTRAP_ITER = 10_000
BLOCK_LEN_DAYS = 90
BOOTSTRAP_SEED = 42

# Pre-committed lags from S02 algorithm
LAG_AVG_STRESS = 149
LAG_MAX_SPIKE = 100

# Window
GEVOELSCORE_START = date(2022, 9, 3)

# Paths
HERE = Path(__file__).resolve().parent
UDS_DIR = Path(
    r"C:\Users\Gebruiker\Documents\gevoelscore-data\garmin data"
    r"\DI_CONNECT\DI-Connect-Aggregator"
)
SPIKE_CSV = HERE.parent / "H02b-stress-spikes" / "daily_max_spike.csv"
DAY_ENTRIES_CSV = HERE / "day_entries.csv"
OUT_CSV = HERE / "lagged_correlation_results.csv"
OUT_PNG = HERE / "lagged_correlation_plot.png"


def load_score():
    out = {}
    with DAY_ENTRIES_CSV.open(encoding="utf-8") as fh:
        for r in csv.DictReader(fh):
            out[date.fromisoformat(r["date"])] = int(r["score"])
    return out


def load_avg_stress():
    stress = {}
    for p in sorted(UDS_DIR.glob("UDSFile_*.json")):
        with p.open(encoding="utf-8") as fh:
            data = json.load(fh)
        for rec in data:
            cd = rec.get("calendarDate")
            if not cd:
                continue
            d = date.fromisoformat(cd)
            ad = rec.get("allDayStress") or {}
            agg = ad.get("aggregatorList") or []
            total = next((a for a in agg if a.get("type") == "TOTAL"), None)
            if total:
                v = total.get("averageStressLevel")
                if v not in (None, -1, -2):
                    if d not in stress or int(v) > stress[d]:
                        stress[d] = int(v)
    return stress


def load_max_spike():
    out = {}
    with SPIKE_CSV.open(encoding="utf-8") as fh:
        for r in csv.DictReader(fh):
            if r["valid"] != "1":
                continue
            out[date.fromisoformat(r["date"])] = float(r["max_spike_minutes"])
    return out


def rankdata(xs):
    n = len(xs)
    idx = sorted(range(n), key=lambda i: xs[i])
    ranks = [0.0] * n
    i = 0
    while i < n:
        j = i
        while j + 1 < n and xs[idx[j + 1]] == xs[idx[i]]:
            j += 1
        avg = (i + j) / 2 + 1
        for k in range(i, j + 1):
            ranks[idx[k]] = avg
        i = j + 1
    return ranks


def spearman(xs, ys):
    rx = rankdata(xs)
    ry = rankdata(ys)
    n = len(xs)
    mx = sum(rx) / n
    my = sum(ry) / n
    num = sum((rx[i] - mx) * (ry[i] - my) for i in range(n))
    dx = sum((rx[i] - mx) ** 2 for i in range(n)) ** 0.5
    dy = sum((ry[i] - my) ** 2 for i in range(n)) ** 0.5
    if dx == 0 or dy == 0:
        return 0.0
    return num / (dx * dy)


def block_bootstrap_ci(xs, ys, block_len, n_iter, seed, ci=0.95):
    n = len(xs)
    rng = random.Random(seed)
    n_blocks = -(-n // block_len)
    n_starts = n - block_len + 1
    est = []
    for _ in range(n_iter):
        bx, by = [], []
        for _ in range(n_blocks):
            s = rng.randrange(n_starts)
            bx.extend(xs[s:s + block_len])
            by.extend(ys[s:s + block_len])
        bx = bx[:n]
        by = by[:n]
        est.append(spearman(bx, by))
    est.sort()
    return (est[int((1 - ci) / 2 * n_iter)],
            est[int((1 + ci) / 2 * n_iter) - 1])


def build_lagged_pairs(score, metric, lag_days, window_start, window_end):
    """For lag L: pair score(d) with metric(d + L)."""
    xs, ys = [], []
    dates = []
    n_excluded = 0
    for d in sorted(score):
        if d < window_start or d > window_end:
            continue
        d_shifted = d + timedelta(days=lag_days)
        if d_shifted not in metric:
            n_excluded += 1
            continue
        xs.append(score[d])
        ys.append(metric[d_shifted])
        dates.append(d)
    return xs, ys, dates, n_excluded


def main():
    print("=" * 64)
    print("S02b -- Score-lead lagged correlation: execution")
    print("=" * 64)

    print("\n[1] Loading data...")
    score = load_score()
    print(f"  score:     {len(score)} days "
          f"({min(score)} -> {max(score)})")
    avg_stress = load_avg_stress()
    print(f"  avg stress: {len(avg_stress)} days "
          f"({min(avg_stress)} -> {max(avg_stress)})")
    max_spike = load_max_spike()
    print(f"  max spike:  {len(max_spike)} days "
          f"({min(max_spike)} -> {max(max_spike)})")

    score_min = min(score)
    score_max = max(score)
    metric_max = max(max(avg_stress), max(max_spike))

    # Bound score dates so d + lag <= metric_max
    window_start = max(GEVOELSCORE_START, score_min)

    print("\n[2] Building lagged + same-day pair series...")
    series = {}
    # avg stress: same-day and +149d
    for lag_days in (0, LAG_AVG_STRESS):
        window_end = min(score_max, metric_max - timedelta(days=lag_days))
        xs, ys, dates, n_excl = build_lagged_pairs(
            score, avg_stress, lag_days, window_start, window_end
        )
        series[("avg_stress", lag_days)] = (xs, ys, dates, n_excl)
        print(f"  avg_stress lag={lag_days:>4d}d: "
              f"n_pairs={len(xs)}, excluded={n_excl}")

    # max spike: same-day and +100d
    for lag_days in (0, LAG_MAX_SPIKE):
        window_end = min(score_max, metric_max - timedelta(days=lag_days))
        xs, ys, dates, n_excl = build_lagged_pairs(
            score, max_spike, lag_days, window_start, window_end
        )
        series[("max_spike_minutes", lag_days)] = (xs, ys, dates, n_excl)
        print(f"  max_spike  lag={lag_days:>4d}d: "
              f"n_pairs={len(xs)}, excluded={n_excl}")

    # IMPORTANT: For criterion (c) we need same-day rho computed on
    # the SAME pair-window as the lagged test (subset of data common
    # to both lag arms). Re-compute same-day rho restricted to dates
    # where the lagged pair also has data.
    print("\n[3] Re-computing same-day rho on matched pair-windows...")
    matched_same_day = {}
    for ch, lag in (("avg_stress", LAG_AVG_STRESS),
                    ("max_spike_minutes", LAG_MAX_SPIKE)):
        _, _, lagged_dates, _ = series[(ch, lag)]
        sd_xs, sd_ys = [], []
        metric_map = avg_stress if ch == "avg_stress" else max_spike
        for d in lagged_dates:
            if d in metric_map:
                sd_xs.append(score[d])
                sd_ys.append(metric_map[d])
        matched_same_day[ch] = (sd_xs, sd_ys, len(sd_xs))
        print(f"  {ch} same-day on matched window: n={len(sd_xs)}")

    print("\n[4] Computing rho + block-bootstrap CI...")
    results = []
    for (ch, lag), (xs, ys, _, n_excl) in series.items():
        role = "primary" if ch == "avg_stress" else "secondary"
        rho = spearman(xs, ys)
        seed_off = 0 if ch == "avg_stress" else 1
        seed_off += 10 if lag != 0 else 0
        lo, hi = block_bootstrap_ci(
            xs, ys, BLOCK_LEN_DAYS, BOOTSTRAP_ITER,
            BOOTSTRAP_SEED + seed_off
        )
        n_eff = -(-len(xs) // BLOCK_LEN_DAYS)
        results.append({
            "channel": ch, "role": role, "lag_days": lag,
            "n_pairs": len(xs), "n_excluded": n_excl,
            "n_effective_blocks": n_eff,
            "rho": rho, "ci_lo": lo, "ci_hi": hi,
            "xs": xs, "ys": ys,
        })
        print(f"  {ch:>20s} lag={lag:>4d}d ({role:>9s}): "
              f"n={len(xs):4d}, rho={rho:+.4f}, "
              f"95%CI [{lo:+.4f},{hi:+.4f}], blocks={n_eff}")

    # Also store matched same-day rho for the criterion (c) comparison
    matched_rho = {}
    for ch in ("avg_stress", "max_spike_minutes"):
        sd_xs, sd_ys, n_match = matched_same_day[ch]
        rho_match = spearman(sd_xs, sd_ys)
        # NO bootstrap CI on the matched-same-day; it's used as a
        # comparison reference, not a verdict-bearing number.
        matched_rho[ch] = (rho_match, n_match)
        print(f"  {ch:>20s} same-day on matched window: "
              f"rho_matched={rho_match:+.4f} (n={n_match})")

    # Apply pre-committed bar to primary lagged row
    print("\n[5] Pre-committed bar evaluation (PRIMARY: avg_stress +149d)")
    primary_lagged = next(r for r in results
                          if r["channel"] == "avg_stress"
                          and r["lag_days"] == LAG_AVG_STRESS)
    primary_sd_matched_rho, _ = matched_rho["avg_stress"]

    rho_lag = primary_lagged["rho"]
    lo_lag = primary_lagged["ci_lo"]
    hi_lag = primary_lagged["ci_hi"]

    # Criterion (a): |rho_lagged| >= 0.20
    crit_a = abs(rho_lag) >= 0.20
    print(f"  (a) magnitude |rho|={abs(rho_lag):.4f} >= 0.20? "
          f"{'PASS' if crit_a else 'FAIL'}")

    # Criterion (b): CI excludes 0
    crit_b = (lo_lag > 0 and hi_lag > 0) or (lo_lag < 0 and hi_lag < 0)
    print(f"  (b) CI excludes 0? [{lo_lag:+.4f}, {hi_lag:+.4f}] "
          f"{'PASS' if crit_b else 'FAIL'}")

    # Criterion (c): |rho_lagged| > |rho_same-day matched| + 0.10
    delta = abs(rho_lag) - abs(primary_sd_matched_rho)
    crit_c = delta >= 0.10
    print(f"  (c) lag-better |rho_lag|={abs(rho_lag):.4f} vs "
          f"|rho_sd_matched|={abs(primary_sd_matched_rho):.4f}, "
          f"delta={delta:+.4f} >= 0.10? "
          f"{'PASS' if crit_c else 'FAIL'}")

    # Criterion (d): expected sign (rho_lagged < 0 for stress)
    crit_d = rho_lag < 0
    print(f"  (d) expected sign rho_lag={rho_lag:+.4f} < 0? "
          f"{'PASS' if crit_d else 'FAIL'}")

    # Verdict
    if crit_a and crit_b and crit_c and crit_d:
        verdict = "SUPPORTED"
    else:
        # Check explicit REFUTED conditions
        if abs(rho_lag) < 0.10 and lo_lag >= -0.15 and hi_lag <= 0.15:
            verdict = "REFUTED (no detectable lagged co-variation)"
        elif delta <= 0.05:
            verdict = "REFUTED (lag does not improve over same-day)"
        elif rho_lag > 0 and crit_b and abs(rho_lag) >= 0.20:
            verdict = "REFUTED (inverse-direction significant; queue S02c-revised reframe)"
        else:
            verdict = "INCONCLUSIVE"

    print(f"\n  PRIMARY VERDICT: {verdict}")

    # Secondary (max_spike +100d) — reported, no verdict
    secondary_lagged = next(r for r in results
                            if r["channel"] == "max_spike_minutes"
                            and r["lag_days"] == LAG_MAX_SPIKE)
    sec_sd_matched_rho, _ = matched_rho["max_spike_minutes"]
    print(f"\n  Secondary (max_spike +100d, no verdict):")
    print(f"    rho={secondary_lagged['rho']:+.4f} 95%CI "
          f"[{secondary_lagged['ci_lo']:+.4f}, "
          f"{secondary_lagged['ci_hi']:+.4f}]")
    print(f"    same-day matched: rho={sec_sd_matched_rho:+.4f}")
    print(f"    delta = |rho_lag| - |rho_sd_matched| = "
          f"{abs(secondary_lagged['rho']) - abs(sec_sd_matched_rho):+.4f}")

    # Write CSV
    with OUT_CSV.open("w", newline="", encoding="utf-8") as fh:
        w = csv.writer(fh)
        w.writerow([
            "channel", "role", "lag_days", "n_pairs", "n_excluded",
            "n_effective_blocks", "spearman_rho", "ci95_lo", "ci95_hi",
            "criterion_a_mag", "criterion_b_ci_excl_zero",
            "criterion_c_lag_better", "criterion_d_expected_sign",
            "verdict",
        ])
        for r in results:
            row_crit_a = row_crit_b = row_crit_c = row_crit_d = ""
            row_verdict = ""
            if r["channel"] == "avg_stress" and r["lag_days"] == LAG_AVG_STRESS:
                row_crit_a = "PASS" if crit_a else "FAIL"
                row_crit_b = "PASS" if crit_b else "FAIL"
                row_crit_c = "PASS" if crit_c else "FAIL"
                row_crit_d = "PASS" if crit_d else "FAIL"
                row_verdict = verdict
            w.writerow([
                r["channel"], r["role"], r["lag_days"], r["n_pairs"],
                r["n_excluded"], r["n_effective_blocks"],
                f"{r['rho']:.4f}", f"{r['ci_lo']:.4f}", f"{r['ci_hi']:.4f}",
                row_crit_a, row_crit_b, row_crit_c, row_crit_d,
                row_verdict,
            ])
    print(f"\n  wrote {OUT_CSV.name}")

    # Plot
    print("\n[6] Rendering plots...")
    try:
        import matplotlib
        matplotlib.use("Agg")
        import matplotlib.pyplot as plt
    except ImportError:
        print("  matplotlib not installed, skipping plots")
        return 0

    fig, axes = plt.subplots(1, 2, figsize=(12, 5))

    rng_j = random.Random(42)

    def render_panel(ax, ch, lag, role):
        r = next(x for x in results
                 if x["channel"] == ch and x["lag_days"] == lag)
        xs, ys = r["xs"], r["ys"]
        sd_rho, sd_n = matched_rho[ch]
        # Jitter discrete x
        xs_j = [x + rng_j.uniform(-0.18, 0.18) for x in xs]
        ax.scatter(xs_j, ys, s=10, alpha=0.30, color="#2c3e50")
        # Simple linear regression on (xs, ys) for visual aid
        n = len(xs)
        mx = sum(xs) / n
        my = sum(ys) / n
        cov = sum((xs[i] - mx) * (ys[i] - my) for i in range(n))
        var = sum((xs[i] - mx) ** 2 for i in range(n))
        slope = cov / var if var else 0
        intercept = my - slope * mx
        x_line = [1, 6]
        y_line = [intercept + slope * x for x in x_line]
        ax.plot(x_line, y_line, color="#c0392b",
                linewidth=1.5, linestyle="--", alpha=0.7,
                label=f"OLS visual aid")
        ax.set_xlim(0.5, 6.5)
        ax.set_xticks([1, 2, 3, 4, 5, 6])
        ax.set_xlabel("gevoelscore (1-6)")
        metric_label = "avg stress" if ch == "avg_stress" else "max spike (min)"
        ax.set_ylabel(f"{metric_label} at t + {lag}d")
        bar_label = ""
        if ch == "avg_stress":
            bar_label = f"  ({verdict})"
        ax.set_title(
            f"score(t) vs {metric_label}(t+{lag}d) [{role}]{bar_label}\n"
            f"rho_lag = {r['rho']:+.3f}  CI [{r['ci_lo']:+.3f}, {r['ci_hi']:+.3f}]\n"
            f"rho_same-day_matched = {sd_rho:+.3f}  (n={r['n_pairs']}, blocks={r['n_effective_blocks']})",
            fontsize=9,
        )
        ax.legend(fontsize=7, loc="upper right")
        ax.grid(alpha=0.25)

    render_panel(axes[0], "avg_stress", LAG_AVG_STRESS, "primary")
    render_panel(axes[1], "max_spike_minutes", LAG_MAX_SPIKE, "secondary")

    fig.suptitle("S02b -- score-lead lagged correlation "
                 "(score(t) vs metric(t + lag))", fontsize=12)
    fig.tight_layout(rect=[0, 0, 1, 0.94])
    fig.savefig(OUT_PNG, dpi=110)
    print(f"  wrote {OUT_PNG.name}")

    # Final summary block for notes.md
    print("\n" + "=" * 64)
    print("SUMMARY FOR notes.md")
    print("=" * 64)
    print(f"  Primary (avg stress +149d): "
          f"rho={rho_lag:+.4f}, CI [{lo_lag:+.4f}, {hi_lag:+.4f}], "
          f"n={primary_lagged['n_pairs']}, blocks={primary_lagged['n_effective_blocks']}")
    print(f"    same-day matched rho: {primary_sd_matched_rho:+.4f}")
    print(f"    criteria: a={'PASS' if crit_a else 'FAIL'}, "
          f"b={'PASS' if crit_b else 'FAIL'}, "
          f"c={'PASS' if crit_c else 'FAIL'}, "
          f"d={'PASS' if crit_d else 'FAIL'}")
    print(f"    VERDICT: {verdict}")
    print(f"  Secondary (max spike +100d): "
          f"rho={secondary_lagged['rho']:+.4f}, "
          f"CI [{secondary_lagged['ci_lo']:+.4f}, {secondary_lagged['ci_hi']:+.4f}], "
          f"n={secondary_lagged['n_pairs']}")
    print(f"    same-day matched rho: {sec_sd_matched_rho:+.4f}")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
