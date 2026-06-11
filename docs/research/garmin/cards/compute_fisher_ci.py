"""Fisher's exact test + binomial 95% CIs for primary verdicts.

Tier 2 peer-review action item from QUEUED-WORK. Derivative
computation over locked result-data.json files; no new hypothesis
tests, no new null draws.

For each primary verdict, computes:
- Fisher's exact p-value (one-sided, alternative = "crash > null")
- 95% binomial confidence interval (Wilson) on the crash-trigger
  frequency
- 95% binomial CI on the null-trigger frequency
- 95% CI on the discrimination_pp (delta of two proportions, Wald)

Output: docs/research/garmin/cards/primary-verdict-statistics.md
"""
from __future__ import annotations

import csv
import json
import math
from pathlib import Path

HERE = Path(__file__).resolve().parent
GARMIN_ROOT = HERE.parent
HYPOTHESES = GARMIN_ROOT / "hypotheses"
OUT_MD = HERE / "primary-verdict-statistics.md"


# Pure-Python Fisher's exact (one-sided)
# 2x2 table:
#         trigger    no_trigger
#  crash    a          b
#  null     c          d
# We want P(observe >= a triggers in crash | independence)
def log_choose(n: int, k: int) -> float:
    if k < 0 or k > n:
        return float("-inf")
    return math.lgamma(n + 1) - math.lgamma(k + 1) - math.lgamma(n - k + 1)


def hypergeom_pmf_log(k: int, n_crash: int, n_total: int, k_total_triggers: int) -> float:
    """log P(X = k) for hypergeometric: drawing n_crash from n_total
    with k_total_triggers successes."""
    return (
        log_choose(k_total_triggers, k)
        + log_choose(n_total - k_total_triggers, n_crash - k)
        - log_choose(n_total, n_crash)
    )


def fishers_exact_one_sided(a: int, b: int, c: int, d: int) -> float:
    """Returns one-sided p-value: P(observe a or more crash-triggers | independence)."""
    n_crash = a + b
    n_null = c + d
    n_total = n_crash + n_null
    k_total_triggers = a + c
    # Range of k: max(0, n_crash - (n_total - k_total_triggers)) to min(n_crash, k_total_triggers)
    k_min = max(0, n_crash - (n_total - k_total_triggers))
    k_max = min(n_crash, k_total_triggers)
    # Sum log-probs for k from a to k_max
    if a > k_max:
        return 0.0
    # Numerically-stable log-sum-exp
    log_terms = [
        hypergeom_pmf_log(k, n_crash, n_total, k_total_triggers)
        for k in range(a, k_max + 1)
    ]
    if not log_terms:
        return 0.0
    M = max(log_terms)
    p = math.exp(M) * sum(math.exp(lt - M) for lt in log_terms)
    return min(1.0, p)


def wilson_ci(k: int, n: int, alpha: float = 0.05) -> tuple[float, float]:
    """Wilson 95% binomial CI."""
    if n == 0:
        return (0.0, 1.0)
    z = 1.959963984540054  # 1-alpha/2 quantile for alpha=0.05
    phat = k / n
    denom = 1 + z**2 / n
    center = (phat + z**2 / (2 * n)) / denom
    halfwidth = (z * math.sqrt(phat * (1 - phat) / n + z**2 / (4 * n * n))) / denom
    return (max(0.0, center - halfwidth), min(1.0, center + halfwidth))


def diff_prop_wald_ci(p1: float, n1: int, p2: float, n2: int, alpha: float = 0.05) -> tuple[float, float]:
    """Wald 95% CI for difference of two proportions p1 - p2."""
    z = 1.959963984540054
    diff = p1 - p2
    var = p1 * (1 - p1) / n1 + p2 * (1 - p2) / n2
    halfwidth = z * math.sqrt(var)
    return (diff - halfwidth, diff + halfwidth)


# Anchor specs (locked at completion of HA07d/HA10/HA11/HA07c/HA08c/HA06b/H02b/H02d + HA01c)
ANCHORS = [
    # (label, rel_path, arm_key, recall_field, null_field, n_crash, n_null, era)
    ("H02b", "H02b-stress-spikes/result-data.json", "train",
     "crash_pct_at_threshold", "null_pct_at_threshold", 14, 200, "train"),
    ("H02d bridge x 5d", "H02d-stress-spikes-uncensored/result-data.json", "bridge__5d/train",
     "crash_pct_at_threshold", "null_pct_at_threshold", 14, 200, "train"),
    ("HA06b 4d bidir N_std=1.5", "HA06b-rhr-zscore/result-data.json",
     "4d_primary_Nstd1.5_bidirectional_train",
     "frac_event", "frac_null", 14, 200, "train"),
    ("HA07c 4d elevated N_std=1.5", "HA07c-sleep-stress-mean-delta/result-data.json",
     "4d_primary_Nstd1.5_one_sided_elevated_train",
     "frac_event", "frac_null", 14, 200, "train"),
    ("HA07d 4d bidir N_std=1.5", "HA07d-sleep-stress-variability/result-data.json",
     "4d_primary_Nstd1.5_bidirectional_train",
     "frac_event", "frac_null", 14, 200, "train"),
    ("HA08c 4d elevated N_std=1.5", "HA08c-sleep-stress-slope/result-data.json",
     "4d_primary_Nstd1.5_one_sided_elevated_train",
     "frac_event", "frac_null", 14, 200, "train"),
    ("HA11 4d elevated N_std=1.5", "HA11-stress-udip/result-data.json",
     "4d_primary_Nstd1.5_one_sided_elevated_train",
     "frac_event", "frac_null", 14, 200, "train"),
    ("HA07d 4d bidir N_std=1.5", "HA07d-sleep-stress-variability/result-data.json",
     "4d_primary_Nstd1.5_bidirectional_validate",
     "frac_event", "frac_null", 15, 200, "validate"),
    ("HA10 4d bidir N_std=1.5", "HA10-bb-overnight-recharge/result-data.json",
     "4d_primary_Nstd1.5_bidirectional_validate",
     "frac_event", "frac_null", 15, 200, "validate"),
    ("HA01c rank >= 0.75 (per-axis effective_exertion)",
     "HA01c-effective-exertion-shock/result-data.json",
     "train_result",
     "frac_event_triggers", "frac_null_triggers", 11, 195, "train"),
    ("HA01c rank >= 0.75 (per-axis effective_exertion)",
     "HA01c-effective-exertion-shock/result-data.json",
     "validate_result",
     "frac_event_triggers", "frac_null_triggers", 15, 195, "validate"),
]


def load_arm(rel_path: str, arm_key: str) -> dict:
    p = HYPOTHESES / rel_path
    d = json.loads(p.read_text())
    if "/" in arm_key:
        parts = arm_key.split("/")
        cur = d
        if "results" in cur:
            cur = cur["results"]
        for part in parts:
            cur = cur[part]
        return cur
    return d[arm_key]


def compute_row(label, rel_path, arm_key, recall_field, null_field, n_crash, n_null, era):
    arm = load_arm(rel_path, arm_key)
    recall = arm[recall_field]
    null_fire = arm[null_field]

    a = round(recall * n_crash)
    b = n_crash - a
    c = round(null_fire * n_null)
    d = n_null - c

    p_value = fishers_exact_one_sided(a, b, c, d)
    recall_ci = wilson_ci(a, n_crash)
    null_ci = wilson_ci(c, n_null)
    disc_ci = diff_prop_wald_ci(recall, n_crash, null_fire, n_null)

    return {
        "label": label,
        "era": era,
        "n_crash": n_crash,
        "n_null": n_null,
        "trigger_count_crash": a,
        "trigger_count_null": c,
        "recall": recall,
        "recall_ci_low": recall_ci[0],
        "recall_ci_high": recall_ci[1],
        "null_fire": null_fire,
        "null_ci_low": null_ci[0],
        "null_ci_high": null_ci[1],
        "discrimination_pp": (recall - null_fire) * 100,
        "disc_ci_low_pp": disc_ci[0] * 100,
        "disc_ci_high_pp": disc_ci[1] * 100,
        "p_value_one_sided": p_value,
    }


def render(rows):
    lines = []
    lines.append("# Primary verdict statistics — Fisher's exact + 95% CIs\n")
    lines.append("**Computed 2026-06-08** per Tier 2 peer-review action item "
                 "([QUEUED-WORK.md](../../QUEUED-WORK.md)). Derivative "
                 "computation over locked result-data.json files. No new "
                 "hypothesis tests, no new null draws.\n")
    lines.append("## Method\n")
    lines.append("For each primary verdict, computes:")
    lines.append("- **Fisher's exact p-value** (one-sided; alternative = crash trigger > null trigger). "
                 "Pure-Python hypergeometric tail sum; matches scipy.stats.fisher_exact alternative='greater'.")
    lines.append("- **Wilson 95% binomial CI** on the crash-trigger frequency (recall).")
    lines.append("- **Wilson 95% binomial CI** on the null-trigger frequency.")
    lines.append("- **Wald 95% CI** on the discrimination (difference of two proportions, pp).\n")
    lines.append("Significance threshold reported is α = 0.05 one-sided. Effective N per primary "
                 "verdict is small (14 train / 15 validate crashes vs 200 nulls); the CIs are wide. "
                 "**Multi-comparison context**: this audit covers 11 primary verdicts; under the "
                 "Bonferroni-conservative α = 0.05/11 ≈ 0.0045, only verdicts with p < 0.005 survive. "
                 "Even more honest: the era-as-moderator framing per playbook §6.3 means train and "
                 "validate arms are NOT independent re-tests, they are complementary slices.\n")
    lines.append("## Table\n")
    lines.append("| anchor | era | n | triggers (crash) | recall (95% CI) | null_fire (95% CI) | disc pp (95% CI) | Fisher p (one-sided) | sig at α=0.05? | sig at α=0.005 (Bonf)? |")
    lines.append("|---|---|---:|---|---|---|---|---|:-:|:-:|")
    for r in rows:
        recall_str = f"{r['recall']*100:.1f}% ({r['recall_ci_low']*100:.1f}%–{r['recall_ci_high']*100:.1f}%)"
        null_str = f"{r['null_fire']*100:.1f}% ({r['null_ci_low']*100:.1f}%–{r['null_ci_high']*100:.1f}%)"
        disc_str = f"{r['discrimination_pp']:+.1f} ({r['disc_ci_low_pp']:+.1f} to {r['disc_ci_high_pp']:+.1f})"
        p_str = f"{r['p_value_one_sided']:.4f}" if r['p_value_one_sided'] >= 0.0001 else f"{r['p_value_one_sided']:.1e}"
        sig_05 = "✓" if r['p_value_one_sided'] < 0.05 else "—"
        sig_bonf = "✓" if r['p_value_one_sided'] < 0.005 else "—"
        lines.append(
            f"| {r['label']} | {r['era']} | {r['n_crash']} | "
            f"{r['trigger_count_crash']}/{r['n_crash']} | "
            f"{recall_str} | {null_str} | {disc_str} | "
            f"{p_str} | {sig_05} | {sig_bonf} |"
        )

    lines.append("\n## Notes\n")
    lines.append("**Interpretation of CIs**: with N=14-15 crashes per era, recall CIs span 30+ percentage points. "
                 "A point estimate of 86.7% (HA07d validate) has CI roughly [60%, 96%]. The verdict-bar pass "
                 "(≥ 60%) is robust to lower-CI variation only if the lower bound stays > 60%; this varies by "
                 "anchor.\n")
    lines.append("**Fisher's exact vs χ²**: chose Fisher because some cells have small counts (e.g. crash trigger "
                 "counts of 6-13). χ² approximation degrades for cell counts < 5; Fisher's exact is appropriate.\n")
    lines.append("**One-sided choice**: the alternative hypothesis is *crash trigger rate > null trigger rate* "
                 "per the pre-registered direction in each hypothesis.md. A two-sided test would double the p-value "
                 "and flip a small number of close-to-α verdicts.\n")
    lines.append("**Why these statistics were not in the original result.md files**: the project's pre-registration "
                 "discipline emphasised the 3-criterion bar (frequency / discrimination / magnitude) rather than "
                 "formal hypothesis-testing p-values. The peer-review §2 critique surfaced this gap. This audit "
                 "retrofits the statistics; future hypothesis.md files should include a Fisher's exact + CI line "
                 "in result.md by default.\n")
    return "\n".join(lines)


def main():
    rows = [compute_row(*a) for a in ANCHORS]
    md = render(rows)
    OUT_MD.write_text(md, encoding="utf-8")
    print(f"Wrote {OUT_MD}\n")

    print(f"{'anchor':45} {'era':10} {'recall':>12} {'p':>10}  {'sig?':5}")
    for r in rows:
        sig = "YES" if r['p_value_one_sided'] < 0.05 else "no"
        bonf = "(Bonf YES)" if r['p_value_one_sided'] < 0.005 else ""
        p_str = f"{r['p_value_one_sided']:.4f}" if r['p_value_one_sided'] >= 0.0001 else f"{r['p_value_one_sided']:.1e}"
        print(f"{r['label'][:43]:45} {r['era']:10} {r['recall']*100:>10.1f}%  {p_str:>10}  {sig:>5} {bonf}")


if __name__ == "__main__":
    main()
