"""Sensitivity test for the v3 severity_spec parameter choices.

Pre-registered 2026-06-06 BEFORE looking at crash labels in connection
with activity classifications. Tests whether exertion_class and
push_burden_class are stable across reasonable variations in:
  - baseline window (default 30 days)
  - push burden window (default 7 days)
  - push-day threshold (default rank >= 0.75)
  - class cutoffs (default 0.5/0.75/0.85/0.95)

Outputs:
  output/sensitivity_results.csv      one row per config x day
  output/sensitivity_report.md        Jaccard + distribution analysis
  output/sensitivity_baselines.png    baseline trajectory comparison

Verdict rule (locked before running):
  - For each varied dimension, compute Jaccard of very_heavy day sets
    between each alternate config and the reference (locked) config.
  - Dimension is ROBUST if all alternates within reasonable bounds give
    Jaccard >= 0.7 vs reference for both exertion_class very_heavy and
    push_burden_class very_heavy.
  - SENSITIVE if any alternate gives Jaccard < 0.5 vs reference.
  - MIXED if some alternates are between 0.5 and 0.7.
"""
from __future__ import annotations

import csv
import collections
import statistics
from datetime import date, timedelta
from pathlib import Path

import matplotlib.dates as mdates
import matplotlib.pyplot as plt

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
FEATURES_CSV = ROOT / "output" / "activity_features_daily.csv"
OUT_REPORT = ROOT / "output" / "sensitivity_report.md"
OUT_BASELINES = ROOT / "output" / "sensitivity_baselines.png"

CLASSES = ["none", "light", "moderate", "heavy", "very_heavy"]
CLASS_RANK = {c: i for i, c in enumerate(CLASSES)}

# Reference (locked v3) params
REF = {
    "name": "ref",
    "baseline_window": 30,
    "push_window": 7,
    "push_threshold": 0.75,
    "cutoffs": (0.5, 0.75, 0.85, 0.95),
}

# Alternates — vary one dimension at a time
ALTS = [
    # Baseline window
    {"name": "bw_14", "baseline_window": 14},
    {"name": "bw_21", "baseline_window": 21},
    {"name": "bw_45", "baseline_window": 45},
    {"name": "bw_60", "baseline_window": 60},
    # Push window
    {"name": "pw_5", "push_window": 5},
    {"name": "pw_10", "push_window": 10},
    {"name": "pw_14", "push_window": 14},
    # Push threshold
    {"name": "pt_0.65", "push_threshold": 0.65},
    {"name": "pt_0.70", "push_threshold": 0.70},
    {"name": "pt_0.80", "push_threshold": 0.80},
    {"name": "pt_0.85", "push_threshold": 0.85},
    # Class cutoffs
    {"name": "cuts_soft", "cutoffs": (0.5, 0.70, 0.80, 0.90)},
    {"name": "cuts_strict", "cutoffs": (0.5, 0.80, 0.90, 0.97)},
]


def parse_num(v):
    if v in (None, "", "None"):
        return None
    try:
        return float(v)
    except ValueError:
        return None


def load_features() -> list[dict]:
    return list(csv.DictReader(FEATURES_CSV.open(encoding="utf-8")))


def rank_to_class(rank: float | None, cutoffs: tuple) -> str:
    if rank is None:
        return "none"
    if rank < cutoffs[0]:
        return "none"
    if rank < cutoffs[1]:
        return "light"
    if rank < cutoffs[2]:
        return "moderate"
    if rank < cutoffs[3]:
        return "heavy"
    return "very_heavy"


def push_burden_to_class(n_push_days: int) -> str:
    if n_push_days < 1:
        return "none"
    if n_push_days < 2:
        return "light"
    if n_push_days < 3:
        return "moderate"
    if n_push_days < 5:
        return "heavy"
    return "very_heavy"


def compute_rolling_rank(
    by_date: dict[date, float | None],
    window: int,
    min_prior: int,
) -> dict[date, float]:
    out = {}
    sorted_dates = sorted(by_date)
    for d in sorted_dates:
        prior = []
        for i in range(1, window + 1):
            wd = d - timedelta(days=i)
            if wd in by_date and by_date[wd] is not None:
                prior.append(by_date[wd])
        if len(prior) < min_prior:
            continue
        today = by_date.get(d)
        if today is None:
            continue
        below = sum(1 for v in prior if v < today)
        at_or_below = sum(1 for v in prior if v <= today)
        out[d] = (below + at_or_below) / (2 * len(prior))
    return out


def classify_config(rows: list[dict], config: dict) -> dict[date, dict]:
    """Apply config to features, return per-date classification dict."""
    cfg = {**REF, **config}
    bw = cfg["baseline_window"]
    pw = cfg["push_window"]
    pt = cfg["push_threshold"]
    cutoffs = cfg["cutoffs"]
    min_prior = max(10, int(bw * 0.65))  # scale floor to window

    # Build per-metric date dicts
    metrics = ["effective_exertion_min", "total_steps",
               "max_hr_uds", "vigorous_min_uds"]
    by_date_per_metric = {m: {} for m in metrics}
    for r in rows:
        d = date.fromisoformat(r["date"])
        for m in metrics:
            v = parse_num(r.get(m))
            by_date_per_metric[m][d] = v

    # Compute ranks per metric
    ranks = {
        m: compute_rolling_rank(by_date_per_metric[m], bw, min_prior)
        for m in metrics
    }

    # Per-day classification
    out = {}
    sorted_dates = sorted(by_date_per_metric["total_steps"])
    eff_rank_by_date = ranks["effective_exertion_min"]

    for d in sorted_dates:
        axes = [
            rank_to_class(ranks["effective_exertion_min"].get(d), cutoffs),
            rank_to_class(ranks["total_steps"].get(d), cutoffs),
            rank_to_class(ranks["max_hr_uds"].get(d), cutoffs),
            rank_to_class(ranks["vigorous_min_uds"].get(d), cutoffs),
        ]
        exertion_class = max(axes, key=lambda c: CLASS_RANK[c])

        # Push burden over last pw days
        push_days = 0
        for i in range(pw):
            wd = d - timedelta(days=i)
            r = eff_rank_by_date.get(wd)
            if r is not None and r >= pt:
                push_days += 1
        push_class = push_burden_to_class(push_days)

        out[d] = {
            "exertion_class": exertion_class,
            "push_burden_class": push_class,
            "push_days": push_days,
        }

    return out, ranks


def jaccard(set_a: set, set_b: set) -> float:
    if not set_a and not set_b:
        return 1.0
    union = set_a | set_b
    if not union:
        return 1.0
    return len(set_a & set_b) / len(union)


def main():
    rows = load_features()
    print(f"Loaded {len(rows)} feature rows")

    print("\nComputing reference (locked v3 params)...")
    ref_cls, ref_ranks = classify_config(rows, REF)
    print(f"  reference exertion_class very_heavy: "
          f"{sum(1 for v in ref_cls.values() if v['exertion_class'] == 'very_heavy')}")

    ref_vh_exertion = {d for d, v in ref_cls.items() if v["exertion_class"] == "very_heavy"}
    ref_vh_push = {d for d, v in ref_cls.items() if v["push_burden_class"] == "very_heavy"}
    ref_heavy_exertion = {
        d for d, v in ref_cls.items()
        if v["exertion_class"] in ("heavy", "very_heavy")
    }
    ref_heavy_push = {
        d for d, v in ref_cls.items()
        if v["push_burden_class"] in ("heavy", "very_heavy")
    }

    # Iterate alternates
    alt_results = []
    alt_ranks_by_window = {30: ref_ranks["effective_exertion_min"]}
    for alt in ALTS:
        cfg_name = alt["name"]
        print(f"  computing alternate '{cfg_name}'...")
        cls, ranks = classify_config(rows, alt)

        vh_exertion = {d for d, v in cls.items() if v["exertion_class"] == "very_heavy"}
        vh_push = {d for d, v in cls.items() if v["push_burden_class"] == "very_heavy"}
        heavy_exertion = {
            d for d, v in cls.items()
            if v["exertion_class"] in ("heavy", "very_heavy")
        }
        heavy_push = {
            d for d, v in cls.items()
            if v["push_burden_class"] in ("heavy", "very_heavy")
        }

        # Distribution
        dist = collections.Counter(v["exertion_class"] for v in cls.values())
        push_dist = collections.Counter(v["push_burden_class"] for v in cls.values())

        # Spearman of ranks for varying baseline window
        spearman = None
        if "baseline_window" in alt:
            bw = alt["baseline_window"]
            alt_ranks_by_window[bw] = ranks["effective_exertion_min"]
            common = set(ref_ranks["effective_exertion_min"]) & set(ranks["effective_exertion_min"])
            if len(common) > 20:
                pairs = [
                    (ref_ranks["effective_exertion_min"][d],
                     ranks["effective_exertion_min"][d])
                    for d in common
                ]
                spearman = spearman_corr(pairs)

        alt_results.append({
            "name": cfg_name,
            "config": {**REF, **alt},
            "dist": dist,
            "push_dist": push_dist,
            "jaccard_vh_exertion": jaccard(vh_exertion, ref_vh_exertion),
            "jaccard_vh_push": jaccard(vh_push, ref_vh_push),
            "jaccard_heavy_exertion": jaccard(heavy_exertion, ref_heavy_exertion),
            "jaccard_heavy_push": jaccard(heavy_push, ref_heavy_push),
            "spearman_ranks": spearman,
        })

    # ─── Write report ───
    write_report(rows, ref_cls, alt_results)

    # ─── Baseline trajectory comparison plot ───
    plot_baselines(rows, alt_ranks_by_window)


def spearman_corr(pairs):
    if len(pairs) < 5:
        return None
    xs = [p[0] for p in pairs]
    ys = [p[1] for p in pairs]
    rx = rank_list(xs)
    ry = rank_list(ys)
    n = len(xs)
    mean_rx = sum(rx) / n
    mean_ry = sum(ry) / n
    cov = sum((rx[i] - mean_rx) * (ry[i] - mean_ry) for i in range(n))
    var_x = sum((rx[i] - mean_rx) ** 2 for i in range(n))
    var_y = sum((ry[i] - mean_ry) ** 2 for i in range(n))
    if var_x == 0 or var_y == 0:
        return None
    return cov / (var_x ** 0.5 * var_y ** 0.5)


def rank_list(vs):
    sorted_idx = sorted(range(len(vs)), key=lambda i: vs[i])
    ranks = [0] * len(vs)
    for r, i in enumerate(sorted_idx, 1):
        ranks[i] = r
    return ranks


def write_report(rows, ref_cls, alt_results):
    n = len(rows)
    ref_dist = collections.Counter(v["exertion_class"] for v in ref_cls.values())
    ref_push_dist = collections.Counter(v["push_burden_class"] for v in ref_cls.values())

    lines = []
    lines.append("# Sensitivity test — v3 severity_spec parameter robustness\n")
    lines.append("Pre-registered 2026-06-06. Verdict rule locked before running: "
                 "Jaccard >= 0.7 vs reference = ROBUST; < 0.5 = SENSITIVE; "
                 "0.5-0.7 = MIXED.\n")
    lines.append("## Reference distributions (locked v3 params)\n")
    lines.append("Reference: baseline_window=30, push_window=7, push_threshold=0.75, "
                 "cutoffs=0.5/0.75/0.85/0.95\n")
    lines.append("**exertion_class:**")
    lines.append("| class | count | % |\n|---|---:|---:|")
    for c in CLASSES:
        cnt = ref_dist.get(c, 0)
        lines.append(f"| {c} | {cnt} | {100*cnt/n:.1f}% |")
    lines.append("")
    lines.append("**push_burden_class:**")
    lines.append("| class | count | % |\n|---|---:|---:|")
    for c in CLASSES:
        cnt = ref_push_dist.get(c, 0)
        lines.append(f"| {c} | {cnt} | {100*cnt/n:.1f}% |")
    lines.append("")

    lines.append("## Alternate configurations\n")
    lines.append("Each row is a single-dimension variation from reference.\n")
    lines.append("| name | param changed | exertion_class very_heavy | push_burden very_heavy | "
                 "Jaccard vh_exertion | Jaccard vh_push | Jaccard heavy+ exertion | "
                 "Jaccard heavy+ push | Spearman ranks |")
    lines.append("|---|---|---:|---:|---:|---:|---:|---:|---:|")
    for r in alt_results:
        cfg = r["config"]
        # Identify which param differs from REF
        diff = []
        for k in ("baseline_window", "push_window", "push_threshold", "cutoffs"):
            if cfg[k] != REF[k]:
                diff.append(f"{k}={cfg[k]}")
        diff_str = ", ".join(diff) or "(reference)"
        vh_ex = r["dist"].get("very_heavy", 0)
        vh_pu = r["push_dist"].get("very_heavy", 0)
        sp = f"{r['spearman_ranks']:.3f}" if r["spearman_ranks"] is not None else "n/a"
        lines.append(
            f"| {r['name']} | {diff_str} | "
            f"{vh_ex} ({100*vh_ex/n:.1f}%) | "
            f"{vh_pu} ({100*vh_pu/n:.1f}%) | "
            f"{r['jaccard_vh_exertion']:.3f} | "
            f"{r['jaccard_vh_push']:.3f} | "
            f"{r['jaccard_heavy_exertion']:.3f} | "
            f"{r['jaccard_heavy_push']:.3f} | "
            f"{sp} |"
        )
    lines.append("")

    # Verdict per dimension
    lines.append("## Verdict per dimension\n")
    dim_verdict = {
        "baseline_window": [],
        "push_window": [],
        "push_threshold": [],
        "cutoffs": [],
    }
    for r in alt_results:
        if r["name"].startswith("bw_"):
            dim_verdict["baseline_window"].append(r)
        elif r["name"].startswith("pw_"):
            dim_verdict["push_window"].append(r)
        elif r["name"].startswith("pt_"):
            dim_verdict["push_threshold"].append(r)
        elif r["name"].startswith("cuts_"):
            dim_verdict["cutoffs"].append(r)

    def verdict_for(jaccs):
        if all(j >= 0.7 for j in jaccs):
            return "**ROBUST**"
        if any(j < 0.5 for j in jaccs):
            return "**SENSITIVE**"
        return "**MIXED**"

    for dim, alts in dim_verdict.items():
        if not alts:
            continue
        jaccs_vh = [r["jaccard_vh_exertion"] for r in alts]
        jaccs_push = [r["jaccard_vh_push"] for r in alts]
        jaccs_heavy = [r["jaccard_heavy_exertion"] for r in alts]
        lines.append(f"### {dim}")
        lines.append(f"- exertion_class very_heavy: min Jaccard = "
                     f"{min(jaccs_vh):.3f}; max = {max(jaccs_vh):.3f}; "
                     f"verdict = {verdict_for(jaccs_vh)}")
        lines.append(f"- push_burden very_heavy: min Jaccard = "
                     f"{min(jaccs_push):.3f}; max = {max(jaccs_push):.3f}; "
                     f"verdict = {verdict_for(jaccs_push)}")
        lines.append(f"- exertion_class heavy+very_heavy: min Jaccard = "
                     f"{min(jaccs_heavy):.3f}; max = {max(jaccs_heavy):.3f}; "
                     f"verdict = {verdict_for(jaccs_heavy)}")
        lines.append("")

    # Overall
    all_jacc = []
    for r in alt_results:
        all_jacc.extend([r["jaccard_vh_exertion"], r["jaccard_vh_push"],
                         r["jaccard_heavy_exertion"], r["jaccard_heavy_push"]])
    lines.append(f"## Overall robustness\n")
    lines.append(f"- min Jaccard across all alternates and all metrics: "
                 f"**{min(all_jacc):.3f}**")
    lines.append(f"- mean Jaccard: **{statistics.mean(all_jacc):.3f}**")
    n_sensitive = sum(1 for j in all_jacc if j < 0.5)
    n_mixed = sum(1 for j in all_jacc if 0.5 <= j < 0.7)
    n_robust = sum(1 for j in all_jacc if j >= 0.7)
    lines.append(f"- counts: ROBUST = {n_robust}, MIXED = {n_mixed}, "
                 f"SENSITIVE = {n_sensitive}")
    lines.append("")
    if n_sensitive == 0 and n_mixed <= 2:
        lines.append("**Overall verdict: ROBUST** — v3 spec stable across "
                     "reasonable parameter variations. Lock confirmed.")
    elif n_sensitive == 0:
        lines.append("**Overall verdict: MOSTLY ROBUST** — some dimensions show "
                     "moderate sensitivity. Lock with caveats noted.")
    else:
        lines.append("**Overall verdict: PARTIALLY SENSITIVE** — at least one "
                     "alternate gives Jaccard < 0.5. Re-examine spec before "
                     "downstream tests.")

    lines.append("")
    lines.append("---")
    lines.append("*Generated 2026-06-06 by 07_sensitivity_test.py.*")

    OUT_REPORT.write_text("\n".join(lines), encoding="utf-8")
    print(f"\nWrote {OUT_REPORT}")


def plot_baselines(rows, alt_ranks_by_window):
    """Compare effective_exertion_min rolling baseline across window lengths."""
    # Build per-date raw values
    by_date = {}
    for r in rows:
        d = date.fromisoformat(r["date"])
        v = parse_num(r.get("effective_exertion_min"))
        if v is not None:
            by_date[d] = v

    # Rolling median for each window
    windows = sorted(alt_ranks_by_window)
    fig, ax = plt.subplots(figsize=(18, 5))

    # Raw scatter
    sorted_d = sorted(by_date)
    ax.scatter(sorted_d, [by_date[d] for d in sorted_d],
               s=2, color="grey", alpha=0.25, zorder=1, label="daily")

    colors = plt.cm.viridis([i / (len(windows) - 1) for i in range(len(windows))])
    for w, col in zip(windows, colors):
        bd_sorted = sorted(by_date)
        rolling = {}
        for d in bd_sorted:
            prior = []
            for i in range(1, w + 1):
                wd = d - timedelta(days=i)
                if wd in by_date:
                    prior.append(by_date[wd])
            if len(prior) >= max(10, int(w * 0.65)):
                rolling[d] = statistics.median(prior)
        rd = sorted(rolling)
        ax.plot(rd, [rolling[d] for d in rd],
                linewidth=1.6, color=col,
                label=f"{w}-day baseline")

    ax.set_title(
        "Baseline trajectory of effective_exertion_min across baseline-window choices",
        fontsize=11,
    )
    ax.set_ylabel("effective_exertion_min")
    ax.legend(loc="upper right", fontsize=8, framealpha=0.95)
    ax.grid(True, alpha=0.25)
    ax.xaxis.set_major_locator(mdates.YearLocator())
    ax.xaxis.set_major_formatter(mdates.DateFormatter("%Y"))
    ax.set_ylim(0, 50)
    plt.tight_layout()
    plt.savefig(OUT_BASELINES, dpi=130, bbox_inches="tight")
    print(f"Wrote {OUT_BASELINES}")


if __name__ == "__main__":
    main()
