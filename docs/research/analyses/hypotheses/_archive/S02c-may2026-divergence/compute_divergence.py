"""S02c -- May 2026 channel divergence: descriptive characterisation.

Implements the pre-registered spec at hypothesis.md. Computes
per-channel z-scores against a locked 180-day reference window
(2025-09-08 -> 2026-03-07), characterises the 90-day perturbation
window (2026-03-08 -> 2026-06-05) on all five channels, identifies
algorithmic onset dates, and reports within-perturbation channel-pair
correlations.

Outputs:
  - channel_summary.csv
  - channel_pair_correlations.csv
  - divergence_plot.png

Descriptive only; no support/refute verdict. Numbers feed the locked
notes.md answer-questions.
"""
from __future__ import annotations

import csv
import json
import statistics
from datetime import date, timedelta
from pathlib import Path

# Window definitions (locked)
PERT_START = date(2026, 3, 8)
PERT_END = date(2026, 6, 5)
REF_START = date(2025, 9, 8)
REF_END = date(2026, 3, 7)

# Onset rule parameters (locked S3.5)
ONSET_Z_THRESHOLD = 1.0
ONSET_FOLLOWUP_DAYS = 14
ONSET_FOLLOWUP_MIN_SAMEDIR = 7

# Reading rules (locked S3.7)
READ_VISIBLE_MAG = 1.0
READ_UNMOVED_MAG = 0.5

# Co-varying threshold (locked S3.6)
COVAR_R_THRESHOLD = 0.5

# Paths
HERE = Path(__file__).resolve().parent
UDS_DIR = Path(
    r"C:\Users\Gebruiker\Documents\gevoelscore-data\garmin data"
    r"\DI_CONNECT\DI-Connect-Aggregator"
)
SLEEP_DIR = Path(
    r"C:\Users\Gebruiker\Documents\gevoelscore-data\garmin data"
    r"\DI_CONNECT\DI-Connect-Wellness"
)
SPIKE_CSV = HERE.parent / "H02b-stress-spikes" / "daily_max_spike.csv"
DAY_ENTRIES_CSV = HERE / "day_entries.csv"

OUT_SUMMARY = HERE / "channel_summary.csv"
OUT_PAIRS = HERE / "channel_pair_correlations.csv"
OUT_PNG = HERE / "divergence_plot.png"

INVALID_SLEEP_TYPES = {"UNCONFIRMED", "OFF_WRIST", "NOT_CONFIRMED"}

# Direction conventions (locked)
WORSEN_DIRECTION = {
    "score": "lower",
    "avg_stress": "higher",
    "max_spike_minutes": "higher",
    "rhr": "higher",
    "sleep_efficiency": "lower",
}


def load_score():
    out = {}
    with DAY_ENTRIES_CSV.open(encoding="utf-8") as fh:
        for r in csv.DictReader(fh):
            out[date.fromisoformat(r["date"])] = float(r["score"])
    return out


def load_uds():
    rhr, stress = {}, {}
    for p in sorted(UDS_DIR.glob("UDSFile_*.json")):
        with p.open(encoding="utf-8") as fh:
            data = json.load(fh)
        for rec in data:
            cd = rec.get("calendarDate")
            if not cd:
                continue
            d = date.fromisoformat(cd)
            v = rec.get("restingHeartRate")
            if v not in (None, 0):
                if d not in rhr or int(v) > rhr[d]:
                    rhr[d] = float(v)
            ad = rec.get("allDayStress") or {}
            agg = ad.get("aggregatorList") or []
            total = next((a for a in agg if a.get("type") == "TOTAL"), None)
            if total:
                vs = total.get("averageStressLevel")
                if vs not in (None, -1, -2):
                    if d not in stress or int(vs) > stress[d]:
                        stress[d] = float(vs)
    return rhr, stress


def load_sleep_efficiency():
    out = {}
    for p in sorted(SLEEP_DIR.glob("*_sleepData.json")):
        with p.open(encoding="utf-8") as fh:
            data = json.load(fh)
        for rec in data:
            cd = rec.get("calendarDate")
            if not cd:
                continue
            if rec.get("sleepWindowConfirmationType") in INVALID_SLEEP_TYPES:
                continue
            deep = int(rec.get("deepSleepSeconds") or 0)
            light = int(rec.get("lightSleepSeconds") or 0)
            rem = int(rec.get("remSleepSeconds") or 0)
            awake = int(rec.get("awakeSleepSeconds") or 0)
            unmeas = int(rec.get("unmeasurableSeconds") or 0)
            tst = deep + light + rem
            tib = tst + awake + unmeas
            if tib < 4 * 3600:
                continue
            d = date.fromisoformat(cd)
            eff = tst / tib
            if d not in out or tib > out[d][1]:
                out[d] = (eff, tib)
    return {d: e for d, (e, _) in out.items()}


def load_max_spike():
    out = {}
    with SPIKE_CSV.open(encoding="utf-8") as fh:
        for r in csv.DictReader(fh):
            if r["valid"] != "1":
                continue
            out[date.fromisoformat(r["date"])] = float(r["max_spike_minutes"])
    return out


def filter_window(channel_data, ws, we):
    return {d: v for d, v in channel_data.items() if ws <= d <= we}


def stats_window(channel_data, ws, we):
    vals = list(filter_window(channel_data, ws, we).values())
    if len(vals) < 2:
        return None, None, len(vals)
    return statistics.mean(vals), statistics.stdev(vals), len(vals)


def z_series(channel_data, ws, we, mu, sigma):
    """Returns dict {date: z}."""
    if sigma == 0:
        return {}
    out = {}
    for d, v in channel_data.items():
        if ws <= d <= we:
            out[d] = (v - mu) / sigma
    return out


def locked_reading(z_mean_pert, worsen_dir):
    """Apply S3.7 reading rules to a per-channel z_mean_pert."""
    abs_z = abs(z_mean_pert)
    if worsen_dir == "higher":
        worsening = z_mean_pert
    else:  # worsen_dir == "lower"
        worsening = -z_mean_pert
    if worsening >= READ_VISIBLE_MAG:
        return "visibly worsening"
    if worsening <= -READ_VISIBLE_MAG:
        return "visibly improving"
    if abs_z < READ_UNMOVED_MAG:
        return "essentially unmoved"
    if worsening > 0:
        return "directional toward worsening, not clearly visible"
    return "directional toward improving, not clearly visible"


def find_onset_date(z_dict, ws, we):
    """S3.5 algorithmic onset rule."""
    day_list = sorted(d for d in z_dict if ws <= d <= we)
    for i, d in enumerate(day_list):
        z_d = z_dict[d]
        if abs(z_d) < ONSET_Z_THRESHOLD:
            continue
        direction = 1 if z_d > 0 else -1
        # Look at next 14 days; need at least 7 in same direction with |z| >= 1.0
        follow = day_list[i + 1 : i + 1 + ONSET_FOLLOWUP_DAYS]
        if len(follow) < ONSET_FOLLOWUP_DAYS:
            # Edge case at corpus end; skip
            continue
        same_dir_count = sum(
            1 for fd in follow
            if abs(z_dict[fd]) >= ONSET_Z_THRESHOLD
            and (1 if z_dict[fd] > 0 else -1) == direction
        )
        if same_dir_count >= ONSET_FOLLOWUP_MIN_SAMEDIR:
            return d, direction
    return None, None


def pearson(xs, ys):
    n = len(xs)
    if n < 2:
        return 0.0
    mx = sum(xs) / n
    my = sum(ys) / n
    num = sum((xs[i] - mx) * (ys[i] - my) for i in range(n))
    dx = sum((xs[i] - mx) ** 2 for i in range(n)) ** 0.5
    dy = sum((ys[i] - my) ** 2 for i in range(n)) ** 0.5
    if dx == 0 or dy == 0:
        return 0.0
    return num / (dx * dy)


def main():
    print("=" * 64)
    print("S02c -- May 2026 channel divergence: execution")
    print("=" * 64)

    print("\n[1] Loading data...")
    channels = {
        "score": load_score(),
    }
    rhr, avg_stress = load_uds()
    channels["avg_stress"] = avg_stress
    channels["rhr"] = rhr
    channels["sleep_efficiency"] = load_sleep_efficiency()
    channels["max_spike_minutes"] = load_max_spike()

    for ch, data in channels.items():
        print(f"  {ch:>20s}: {len(data)} days "
              f"({min(data)} -> {max(data)})")

    print(f"\n  reference window: [{REF_START}, {REF_END}] (180d)")
    print(f"  perturbation window: [{PERT_START}, {PERT_END}] (90d)")

    print("\n[2] Per-channel z-scores against reference window...")
    summary_rows = []
    z_pert = {}  # channel -> dict[date, z]
    z_ref = {}   # channel -> dict[date, z]
    for ch, data in channels.items():
        mu_ref, sd_ref, n_ref = stats_window(data, REF_START, REF_END)
        if mu_ref is None:
            print(f"  {ch}: insufficient reference data")
            continue
        pert_vals = list(filter_window(data, PERT_START, PERT_END).values())
        n_pert = len(pert_vals)
        mean_pert = statistics.mean(pert_vals) if pert_vals else None
        z_mean_pert = ((mean_pert - mu_ref) / sd_ref
                       if sd_ref and mean_pert is not None else None)
        z_pert[ch] = z_series(data, PERT_START, PERT_END, mu_ref, sd_ref)
        z_ref[ch] = z_series(data, REF_START, REF_END, mu_ref, sd_ref)
        max_abs_z = 0.0
        max_abs_z_d = None
        for d, z in z_pert[ch].items():
            if abs(z) > max_abs_z:
                max_abs_z = abs(z)
                max_abs_z_d = d
        onset_d, onset_dir = find_onset_date(z_pert[ch], PERT_START, PERT_END)
        reading = locked_reading(z_mean_pert, WORSEN_DIRECTION[ch])
        print(f"  {ch:>20s}: mu_ref={mu_ref:.4f}, sd_ref={sd_ref:.4f}, "
              f"mean_pert={mean_pert:.4f}, z_mean_pert={z_mean_pert:+.4f}, "
              f"max|z|={max_abs_z:.4f} on {max_abs_z_d}, "
              f"onset={onset_d}")
        print(f"    reading: {reading}")
        summary_rows.append({
            "channel": ch,
            "window_ref_n": n_ref,
            "window_pert_n": n_pert,
            "mean_ref": mu_ref,
            "std_ref": sd_ref,
            "mean_pert": mean_pert,
            "z_mean_pert": z_mean_pert,
            "max_abs_z_pert": max_abs_z,
            "max_abs_z_day": max_abs_z_d,
            "onset_date": onset_d,
            "reading": reading,
        })

    print("\n[3] Channel-pair correlations within perturbation window...")
    pair_rows = []
    chs = list(channels.keys())
    for i in range(len(chs)):
        for j in range(i + 1, len(chs)):
            a, b = chs[i], chs[j]
            # Pair dates that have z in both
            dates_a = z_pert.get(a, {})
            dates_b = z_pert.get(b, {})
            common = sorted(set(dates_a) & set(dates_b))
            if len(common) < 2:
                pair_rows.append({
                    "channel_a": a, "channel_b": b,
                    "n_pairs": len(common), "pearson_r": None,
                    "co_varying": "",
                })
                continue
            xs = [dates_a[d] for d in common]
            ys = [dates_b[d] for d in common]
            r = pearson(xs, ys)
            cov = "YES" if abs(r) >= COVAR_R_THRESHOLD else ""
            pair_rows.append({
                "channel_a": a, "channel_b": b,
                "n_pairs": len(common), "pearson_r": r,
                "co_varying": cov,
            })
            print(f"  {a:>20s} vs {b:>20s}: r={r:+.4f} (n={len(common)}) "
                  f"{cov}")

    # Q5 headline: garmin-worsen composite vs score
    worsen_chs = ["avg_stress", "max_spike_minutes", "rhr"]
    worsen_dates = sorted(
        set.intersection(*(set(z_pert[c]) for c in worsen_chs if c in z_pert))
    )
    worsen_z = []
    for d in worsen_dates:
        worsen_z.append(sum(z_pert[c][d] for c in worsen_chs) / len(worsen_chs))
    if "score" in z_pert:
        score_dates = sorted(set(z_pert["score"]) & set(worsen_dates))
        score_z_aligned = [z_pert["score"][d] for d in score_dates]
        worsen_z_aligned = [
            sum(z_pert[c][d] for c in worsen_chs) / len(worsen_chs)
            for d in score_dates
        ]
        # Convention: positive composite_z = Garmin worsening; positive
        # score_z = score improving; gap = composite_z - score_z =
        # how much Garmin says worsening while score says improving
        gap = [(worsen_z_aligned[i] - score_z_aligned[i])
               for i in range(len(score_dates))]
        gap_mean = statistics.mean(gap)
        print(f"\n[Q5] Score-Garmin divergence headline:")
        print(f"  composite Garmin-worsen z (mean across {len(score_dates)} "
              f"perturbation days): {statistics.mean(worsen_z_aligned):+.4f}")
        print(f"  score z (mean across same days): "
              f"{statistics.mean(score_z_aligned):+.4f}")
        print(f"  gap mean (Garmin-worsen - score-improving): "
              f"{gap_mean:+.4f} sigma")
        print(f"  max single-day gap: {max(gap):+.4f}")

    # Write CSVs
    with OUT_SUMMARY.open("w", newline="", encoding="utf-8") as fh:
        w = csv.writer(fh)
        w.writerow([
            "channel", "window_ref_n", "window_pert_n",
            "mean_ref", "std_ref", "mean_pert", "z_mean_pert",
            "max_abs_z_pert", "max_abs_z_day", "onset_date",
            "reading",
        ])
        for r in summary_rows:
            w.writerow([
                r["channel"],
                r["window_ref_n"], r["window_pert_n"],
                f"{r['mean_ref']:.4f}",
                f"{r['std_ref']:.4f}",
                f"{r['mean_pert']:.4f}",
                f"{r['z_mean_pert']:+.4f}",
                f"{r['max_abs_z_pert']:.4f}",
                r["max_abs_z_day"].isoformat() if r["max_abs_z_day"] else "",
                r["onset_date"].isoformat() if r["onset_date"] else "",
                r["reading"],
            ])
    print(f"\nwrote {OUT_SUMMARY.name}")

    with OUT_PAIRS.open("w", newline="", encoding="utf-8") as fh:
        w = csv.writer(fh)
        w.writerow(["channel_a", "channel_b", "n_pairs",
                    "pearson_r", "co_varying"])
        for r in pair_rows:
            w.writerow([
                r["channel_a"], r["channel_b"], r["n_pairs"],
                f"{r['pearson_r']:+.4f}" if r["pearson_r"] is not None else "",
                r["co_varying"],
            ])
    print(f"wrote {OUT_PAIRS.name}")

    # Plot
    print("\n[4] Rendering plot...")
    try:
        import matplotlib
        matplotlib.use("Agg")
        import matplotlib.pyplot as plt
        import matplotlib.dates as mdates
    except ImportError:
        print("  matplotlib not installed, skipping plot")
        return 0

    fig, (axA, axB) = plt.subplots(2, 1, figsize=(13, 9), sharex=True)

    ch_colors = {
        "score": "#2c3e50",
        "avg_stress": "#d68910",
        "max_spike_minutes": "#8e44ad",
        "rhr": "#c0392b",
        "sleep_efficiency": "#16a085",
    }
    ch_labels = {
        "score": "score (positive z = improving)",
        "avg_stress": "avg stress (positive z = worsening)",
        "max_spike_minutes": "max spike (positive z = worsening)",
        "rhr": "RHR (positive z = worsening)",
        "sleep_efficiency": "sleep eff (positive z = improving)",
    }

    for ch in channels:
        if ch not in z_ref or ch not in z_pert:
            continue
        combined = {**z_ref[ch], **z_pert[ch]}
        dates = sorted(combined)
        zs = [combined[d] for d in dates]
        axA.plot(dates, zs, color=ch_colors[ch], linewidth=1.0, alpha=0.8,
                 label=ch_labels[ch])
        # Mark onset date
        onset_d = next((r["onset_date"] for r in summary_rows
                       if r["channel"] == ch), None)
        if onset_d:
            axA.scatter([onset_d], [combined.get(onset_d, 0)],
                        color=ch_colors[ch], marker="v", s=80,
                        edgecolor="black", linewidth=0.5, zorder=5)
    axA.axvline(PERT_START, color="black", linestyle="-",
                linewidth=1.0, alpha=0.6)
    axA.text(PERT_START, axA.get_ylim()[1] * 0.95,
             " perturbation\n window start",
             fontsize=8, va="top")
    axA.axhline(0, color="gray", linewidth=0.5, alpha=0.5)
    axA.axhline(1.0, color="gray", linewidth=0.5,
                linestyle=":", alpha=0.4)
    axA.axhline(-1.0, color="gray", linewidth=0.5,
                linestyle=":", alpha=0.4)
    axA.set_ylabel("z-score vs reference window")
    axA.set_title("Panel A -- per-channel daily z-scores "
                  "(reference + perturbation windows, onset markers)",
                  fontsize=10)
    axA.legend(loc="lower left", fontsize=8, ncol=2)
    axA.grid(alpha=0.25)

    # Panel B: composite divergence
    if score_dates:
        # Render over the full visible range; pre-perturbation portion
        # uses z_ref data
        all_dates = sorted(set(z_ref.get("score", {})) | set(z_pert.get("score", {})))
        score_full = {**z_ref.get("score", {}), **z_pert.get("score", {})}
        # Build composite worsen-z across all dates where all 3
        # worsen channels exist
        composite = {}
        for d in all_dates:
            vals = []
            for c in worsen_chs:
                full = {**z_ref.get(c, {}), **z_pert.get(c, {})}
                if d in full:
                    vals.append(full[d])
            if len(vals) == len(worsen_chs):
                composite[d] = sum(vals) / len(vals)
        common = sorted(set(score_full) & set(composite))
        score_full_aligned = [score_full[d] for d in common]
        composite_aligned = [composite[d] for d in common]
        axB.plot(common, composite_aligned, color="#c0392b",
                 linewidth=1.2,
                 label="Garmin-worsen composite z (mean of stress/spike/RHR)")
        axB.plot(common, score_full_aligned, color="#2c3e50",
                 linewidth=1.2,
                 label="score z (positive = improving)")
        axB.fill_between(common, score_full_aligned, composite_aligned,
                         where=[c > s for c, s in zip(composite_aligned,
                                                       score_full_aligned)],
                         color="#e74c3c", alpha=0.15,
                         label="gap (composite > score)")
        axB.axvline(PERT_START, color="black", linestyle="-",
                    linewidth=1.0, alpha=0.6)
        axB.axhline(0, color="gray", linewidth=0.5, alpha=0.5)
        axB.set_ylabel("z-score vs reference window")
        axB.set_xlabel("date")
        axB.set_title(f"Panel B -- composite divergence "
                      f"(gap mean within perturbation = "
                      f"{gap_mean:+.3f} sigma)", fontsize=10)
        axB.legend(loc="lower left", fontsize=8)
        axB.grid(alpha=0.25)

    axB.xaxis.set_major_locator(mdates.MonthLocator())
    axB.xaxis.set_major_formatter(mdates.DateFormatter("%b %Y"))
    plt.setp(axB.xaxis.get_majorticklabels(), rotation=30, ha="right")

    fig.suptitle("S02c -- May 2026 channel divergence "
                 "(180d reference + 90d perturbation)", fontsize=12)
    fig.tight_layout(rect=[0, 0, 1, 0.96])
    fig.savefig(OUT_PNG, dpi=110)
    print(f"wrote {OUT_PNG.name}")

    # Summary for notes.md
    print("\n" + "=" * 64)
    print("SUMMARY FOR notes.md")
    print("=" * 64)
    for r in summary_rows:
        print(f"  {r['channel']:>20s}: z_mean_pert={r['z_mean_pert']:+.4f}, "
              f"reading={r['reading']}, "
              f"onset={r['onset_date']}")
    print(f"\n  Q5 headline gap (Garmin-worsen - score-improving, "
          f"sigma units): {gap_mean:+.4f}")
    cov_pairs = [r for r in pair_rows if r["co_varying"] == "YES"]
    print(f"\n  co-varying channel pairs (|r| >= {COVAR_R_THRESHOLD}): "
          f"{len(cov_pairs)}")
    for r in cov_pairs:
        print(f"    {r['channel_a']} <-> {r['channel_b']}: "
              f"r={r['pearson_r']:+.4f}")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
