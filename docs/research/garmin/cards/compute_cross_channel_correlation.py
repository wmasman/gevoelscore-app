"""Cross-channel correlation matrix for load-bearing primitives.

Tier 2 peer-review action item from QUEUED-WORK. Loads per-day
primitive values from existing CSV sources, restricts to the
analysis window (2022-09-03 to 2026-06-05), inner-joins on date,
and computes Pearson + Spearman correlation matrices.

Empirically anchors the "channels aren't statistically independent"
caveat that appears in synthesis docs — replaces a sentence with
a number.

Primitives included (8 channels):
- H02b daily max spike duration (minutes)
- H02d daily max spike duration bridge variant (minutes)
- HA11 daily U-dip event count
- HA06b nightly resting heart rate (bpm)
- HA07c nightly sleep stress mean
- HA07d nightly sleep stress stdev (the variability metric)
- HA08c sleep stress mean (used as the slope input)
- HA10 morning Body Battery peak (from UDS HIGHEST anchor)

Note: HA08c uses the same nightly stress mean as HA07c but
operates on its slope; so we report HA07c/HA08c on the same raw
primitive (sleep_stress_mean).

Output: docs/research/garmin/cards/cross-channel-correlation.md
"""
from __future__ import annotations

import csv
import json
from datetime import date
from pathlib import Path

HERE = Path(__file__).resolve().parent
GARMIN_ROOT = HERE.parent
HYPOTHESES = GARMIN_ROOT / "hypotheses"
ACTIVITY_OUTPUT = GARMIN_ROOT / "activity-labels" / "output"
SLEEP_STRESS_CSV = GARMIN_ROOT / "scripts" / "sleep_stress_extract" / "sleep_stress_nightly.csv"
OUT_MD = HERE / "cross-channel-correlation.md"

ANALYSIS_START = date(2022, 9, 3)
ANALYSIS_END = date(2026, 6, 5)
TRAIN_END = date(2023, 12, 31)


def parse_float(v):
    if v in (None, "", "None"):
        return None
    try:
        return float(v)
    except ValueError:
        return None


def load_h02b() -> dict[date, float]:
    """daily max contiguous stress >=75 >=5min duration (minutes)."""
    out = {}
    p = HYPOTHESES / "H02b-stress-spikes" / "daily_max_spike.csv"
    for r in csv.DictReader(p.open(encoding="utf-8")):
        if r.get("valid", "0") != "1":
            continue
        d = date.fromisoformat(r["date"])
        v = parse_float(r.get("max_spike_minutes"))
        if v is not None:
            out[d] = v
    return out


def load_h02d_bridge() -> dict[date, float]:
    """daily max spike duration bridge variant."""
    out = {}
    p = HYPOTHESES / "H02d-stress-spikes-uncensored" / "daily_max_spike_v2.csv"
    for r in csv.DictReader(p.open(encoding="utf-8")):
        if r.get("valid", "0") != "1":
            continue
        d = date.fromisoformat(r["date"])
        v = parse_float(r.get("max_spike_minutes_bridge"))
        if v is not None:
            out[d] = v
    return out


def load_ha11_udip() -> dict[date, float]:
    """daily U-dip event count."""
    out = {}
    p = HYPOTHESES / "HA11-stress-udip" / "udip_counts.csv"
    for r in csv.DictReader(p.open(encoding="utf-8")):
        if r.get("valid", "0") != "1":
            continue
        d = date.fromisoformat(r["date"])
        v = parse_float(r.get("u_dip_count"))
        if v is not None:
            out[d] = v
    return out


def load_ha06b_rhr() -> dict[date, float]:
    """nightly resting heart rate (bpm) from daily_uds."""
    out = {}
    p = ACTIVITY_OUTPUT / "daily_uds.csv"
    for r in csv.DictReader(p.open(encoding="utf-8")):
        d = date.fromisoformat(r["date"])
        v = parse_float(r.get("resting_hr"))
        if v is None:
            continue
        if not (30 <= v <= 130):
            continue
        out[d] = v
    return out


def load_ha07c_ha07d() -> tuple[dict[date, float], dict[date, float]]:
    """nightly sleep stress mean + stdev."""
    means, stdevs = {}, {}
    p = SLEEP_STRESS_CSV
    for r in csv.DictReader(p.open(encoding="utf-8")):
        if r.get("valid", "0") != "1":
            continue
        d = date.fromisoformat(r["date"])
        m = parse_float(r.get("stress_mean"))
        s = parse_float(r.get("stress_stdev"))
        if m is not None:
            means[d] = m
        if s is not None:
            stdevs[d] = s
    return means, stdevs


def load_ha10_bb_peak() -> dict[date, float]:
    """Morning BB peak from UDS HIGHEST anchor."""
    out = {}
    UDS_DIR = Path(r"C:\Users\Gebruiker\Documents\gevoelscore-data\garmin data\DI_CONNECT\DI-Connect-Aggregator")
    if not UDS_DIR.exists():
        print(f"WARNING: UDS dir not found at {UDS_DIR}; HA10 column will be empty")
        return out
    for p in sorted(UDS_DIR.glob("UDSFile_*.json")):
        try:
            data = json.loads(p.read_text())
        except Exception:
            continue
        # data is a list of dicts; each has calendarDate + bodyBattery
        for rec in data if isinstance(data, list) else [data]:
            cdate = rec.get("calendarDate")
            if not cdate:
                continue
            try:
                d = date.fromisoformat(cdate)
            except Exception:
                continue
            bb = rec.get("bodyBattery")
            if not isinstance(bb, dict):
                continue
            stat_list = bb.get("bodyBatteryStatList", [])
            highest = next(
                (s for s in stat_list if s.get("bodyBatteryStatType") == "HIGHEST"), None
            )
            if highest is None:
                continue
            v = parse_float(highest.get("statsValue"))
            if v is not None and 0 <= v <= 100:
                out[d] = v
    return out


def restrict_to_window(d: dict[date, float]) -> dict[date, float]:
    return {k: v for k, v in d.items() if ANALYSIS_START <= k <= ANALYSIS_END}


def pearson(x, y):
    n = len(x)
    if n < 3:
        return None
    mx = sum(x) / n
    my = sum(y) / n
    num = sum((xi - mx) * (yi - my) for xi, yi in zip(x, y))
    denx = (sum((xi - mx) ** 2 for xi in x)) ** 0.5
    deny = (sum((yi - my) ** 2 for yi in y)) ** 0.5
    if denx == 0 or deny == 0:
        return None
    return num / (denx * deny)


def rank(values):
    indexed = sorted(enumerate(values), key=lambda kv: kv[1])
    ranks = [0.0] * len(values)
    i = 0
    while i < len(indexed):
        j = i
        while j + 1 < len(indexed) and indexed[j + 1][1] == indexed[i][1]:
            j += 1
        avg = (i + j) / 2.0 + 1.0
        for k in range(i, j + 1):
            ranks[indexed[k][0]] = avg
        i = j + 1
    return ranks


def spearman(x, y):
    rx = rank(x)
    ry = rank(y)
    return pearson(rx, ry)


def compute_pair(d1, d2):
    """Compute Pearson + Spearman + N on the intersection of dates."""
    common = sorted(set(d1.keys()) & set(d2.keys()))
    if len(common) < 30:
        return None, None, len(common)
    xs = [d1[k] for k in common]
    ys = [d2[k] for k in common]
    return pearson(xs, ys), spearman(xs, ys), len(common)


def main():
    print("Loading per-day primitives from CSV/UDS sources...")
    h02b = restrict_to_window(load_h02b())
    h02d = restrict_to_window(load_h02d_bridge())
    ha11 = restrict_to_window(load_ha11_udip())
    ha06b = restrict_to_window(load_ha06b_rhr())
    ha07c_mean, ha07d_stdev = load_ha07c_ha07d()
    ha07c_mean = restrict_to_window(ha07c_mean)
    ha07d_stdev = restrict_to_window(ha07d_stdev)
    ha10 = restrict_to_window(load_ha10_bb_peak())

    print(f"  H02b daily max spike (min):    {len(h02b)} days")
    print(f"  H02d bridge max spike (min):   {len(h02d)} days")
    print(f"  HA11 U-dip count:              {len(ha11)} days")
    print(f"  HA06b nightly RHR (bpm):       {len(ha06b)} days")
    print(f"  HA07c nightly stress mean:     {len(ha07c_mean)} days")
    print(f"  HA07d nightly stress stdev:    {len(ha07d_stdev)} days")
    print(f"  HA10 morning BB peak:          {len(ha10)} days")

    primitives = [
        ("H02b (max_spike_min)", h02b),
        ("H02d (bridge_spike_min)", h02d),
        ("HA11 (u_dip_count)", ha11),
        ("HA06b (resting_hr_bpm)", ha06b),
        ("HA07c (sleep_stress_mean)", ha07c_mean),
        ("HA07d (sleep_stress_stdev)", ha07d_stdev),
        ("HA10 (morning_bb_peak)", ha10),
    ]
    # HA08c uses the same sleep_stress_mean as HA07c (it's the slope of that series);
    # at the raw-primitive level it's identical, so we omit a separate row.

    labels = [p[0] for p in primitives]
    dicts = [p[1] for p in primitives]
    n = len(primitives)

    pearson_matrix = [[None] * n for _ in range(n)]
    spearman_matrix = [[None] * n for _ in range(n)]
    n_matrix = [[0] * n for _ in range(n)]

    for i in range(n):
        for j in range(n):
            if i == j:
                pearson_matrix[i][j] = 1.0
                spearman_matrix[i][j] = 1.0
                n_matrix[i][j] = len(dicts[i])
                continue
            p, s, n_pair = compute_pair(dicts[i], dicts[j])
            pearson_matrix[i][j] = p
            spearman_matrix[i][j] = s
            n_matrix[i][j] = n_pair

    # Render
    md = []
    md.append("# Cross-channel correlation matrix — load-bearing primitives\n")
    md.append("**Computed 2026-06-08** per Tier 2 peer-review action item "
              "([QUEUED-WORK.md](../../QUEUED-WORK.md)). Empirical replacement for "
              "the 'channels aren't statistically independent' caveat that appears "
              "in synthesis docs.\n")
    md.append("## Method\n")
    md.append("- **Per-day raw primitive values** loaded from existing CSV / UDS sources "
              "(no z-scoring, no lagging — we want the underlying biological correlation, "
              "not the lead-up-window correlation).")
    md.append("- **Inner-joined on calendar date** within the analysis window "
              "(2022-09-03 → 2026-06-05).")
    md.append("- **Pearson r** (linear) + **Spearman ρ** (monotonic).")
    md.append("- Minimum N=30 days required for a pairwise correlation; cells with insufficient "
              "data are blank.\n")
    md.append("HA08c is omitted as a separate row: it operates on the same raw `sleep_stress_mean` "
              "primitive as HA07c (HA08c is the trailing-5-day OLS slope of that series). At the "
              "raw-primitive level the two are identical; their distinct hypothesis verdicts come "
              "from different downstream transformations.\n")
    md.append("## Per-primitive day counts\n")
    for label, d in primitives:
        md.append(f"- **{label}**: {len(d)} days")
    md.append("")

    md.append("## Spearman ρ matrix (monotonic correlation)\n")
    md.append("| | " + " | ".join(l.split(" ")[0] for l in labels) + " |")
    md.append("|---|" + "|".join("---:" for _ in labels) + "|")
    for i, lab in enumerate(labels):
        row = "| **" + lab + "** | "
        cells = []
        for j in range(n):
            v = spearman_matrix[i][j]
            if v is None:
                cells.append(f"— (n={n_matrix[i][j]})")
            elif i == j:
                cells.append("**1.000**")
            else:
                cells.append(f"{v:+.3f}")
        row += " | ".join(cells)
        row += " |"
        md.append(row)
    md.append("")

    md.append("## Pearson r matrix (linear correlation)\n")
    md.append("| | " + " | ".join(l.split(" ")[0] for l in labels) + " |")
    md.append("|---|" + "|".join("---:" for _ in labels) + "|")
    for i, lab in enumerate(labels):
        row = "| **" + lab + "** | "
        cells = []
        for j in range(n):
            v = pearson_matrix[i][j]
            if v is None:
                cells.append(f"— (n={n_matrix[i][j]})")
            elif i == j:
                cells.append("**1.000**")
            else:
                cells.append(f"{v:+.3f}")
        row += " | ".join(cells)
        row += " |"
        md.append(row)
    md.append("")

    md.append("## Pairwise N (intersection of valid days)\n")
    md.append("| | " + " | ".join(l.split(" ")[0] for l in labels) + " |")
    md.append("|---|" + "|".join("---:" for _ in labels) + "|")
    for i, lab in enumerate(labels):
        row = "| **" + lab + "** | "
        cells = [str(n_matrix[i][j]) for j in range(n)]
        row += " | ".join(cells)
        row += " |"
        md.append(row)
    md.append("")

    # Compute mean |ρ| per channel (excluding self)
    md.append("## Mean |Spearman ρ| per channel (excluding self)\n")
    md.append("Channels with HIGH mean |ρ| are 'central' — they share variance with many "
              "others. Channels with LOW mean |ρ| are MORE INDEPENDENT.\n")
    md.append("| channel | mean \\|ρ\\| | interpretation |")
    md.append("|---|---:|---|")
    for i, lab in enumerate(labels):
        offdiag = [abs(spearman_matrix[i][j]) for j in range(n) if i != j and spearman_matrix[i][j] is not None]
        mean_abs = sum(offdiag) / len(offdiag) if offdiag else None
        if mean_abs is None:
            interp = "insufficient data"
            mean_str = "—"
        else:
            mean_str = f"{mean_abs:.3f}"
            if mean_abs > 0.3:
                interp = "central — shares variance with many channels"
            elif mean_abs > 0.15:
                interp = "moderately correlated with others"
            else:
                interp = "relatively independent"
        md.append(f"| **{lab}** | {mean_str} | {interp} |")
    md.append("")

    md.append("## What this means for synthesis claims\n")
    md.append("**The 'seven train-era SUPPORTED on six channels' framing**: the actual independence "
              "of these channels is now quantified rather than asserted. Channels with mean |ρ| > 0.3 "
              "are NOT independent samples of nature; they share underlying biology. Conservative "
              "interpretation: the number of effective independent measurements is roughly "
              "1 / (1 + average pairwise |ρ|) × N_channels.\n")
    md.append("**Cross-era anchors (HA07d both eras)**: HA07d (sleep stress stdev) and HA10 (morning "
              "BB peak) are conceptually distinct channels (autonomic variability vs autonomic "
              "recharge). The correlation row tells whether they are biologically independent.\n")
    md.append("**Multi-comparison adjustment**: Bonferroni on 11 primary verdicts at α=0.05 → α=0.0045. "
              "But with effective N of channels < 7 due to correlation, the multi-comparison concern "
              "is bounded. The Fisher's exact + 95% CI doc "
              "([primary-verdict-statistics.md](primary-verdict-statistics.md)) provides the per-verdict "
              "test that this correlation matrix puts in context.\n")
    md.append("**Caveat about HA10**: HA10's morning BB peak is structurally a fused composite of HR, "
              "HRV, and stress per Garmin's BB algorithm. So HA10 ↔ HA06b (RHR), HA10 ↔ HA07c (sleep "
              "stress mean), and HA10 ↔ HA07d (sleep stress stdev) correlations are EXPECTED to be "
              "non-zero by construction, not just biologically.")

    OUT_MD.write_text("\n".join(md), encoding="utf-8")
    print(f"\nWrote {OUT_MD}")

    print("\n=== Spearman rho matrix ===")
    print(f"{'':28} " + " ".join(f"{l.split(' ')[0]:>9}" for l in labels))
    for i, lab in enumerate(labels):
        cells = []
        for j in range(n):
            v = spearman_matrix[i][j]
            cells.append(f"{v:+.3f}" if v is not None else "  —  ")
        print(f"  {lab:28} " + " ".join(f"{c:>9}" for c in cells))


if __name__ == "__main__":
    main()
