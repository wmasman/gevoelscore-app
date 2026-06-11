# Primary verdict statistics — Fisher's exact + 95% CIs

**Computed 2026-06-08** per Tier 2 peer-review action item ([QUEUED-WORK.md](../../QUEUED-WORK.md)). Derivative computation over locked result-data.json files. No new hypothesis tests, no new null draws.

## Method

For each primary verdict, computes:
- **Fisher's exact p-value** (one-sided; alternative = crash trigger > null trigger). Pure-Python hypergeometric tail sum; matches scipy.stats.fisher_exact alternative='greater'.
- **Wilson 95% binomial CI** on the crash-trigger frequency (recall).
- **Wilson 95% binomial CI** on the null-trigger frequency.
- **Wald 95% CI** on the discrimination (difference of two proportions, pp).

Significance threshold reported is α = 0.05 one-sided. Effective N per primary verdict is small (14 train / 15 validate crashes vs 200 nulls); the CIs are wide. **Multi-comparison context**: this audit covers 11 primary verdicts; under the Bonferroni-conservative α = 0.05/11 ≈ 0.0045, only verdicts with p < 0.005 survive. Even more honest: the era-as-moderator framing per playbook §6.3 means train and validate arms are NOT independent re-tests, they are complementary slices.

## Table

| anchor | era | n | triggers (crash) | recall (95% CI) | null_fire (95% CI) | disc pp (95% CI) | Fisher p (one-sided) | sig at α=0.05? | sig at α=0.005 (Bonf)? |
|---|---|---:|---|---|---|---|---|:-:|:-:|
| H02b | train | 14 | 10/14 | 71.4% (45.4%–88.3%) | 41.5% (34.9%–48.4%) | +29.9 (+5.3 to +54.6) | 0.0285 | ✓ | — |
| H02d bridge x 5d | train | 14 | 13/14 | 92.3% (68.5%–98.7%) | 60.5% (53.6%–67.0%) | +31.8 (+16.3 to +47.3) | 0.0112 | ✓ | — |
| HA06b 4d bidir N_std=1.5 | train | 14 | 10/14 | 71.4% (45.4%–88.3%) | 52.5% (45.6%–59.3%) | +18.9 (-5.7 to +43.6) | 0.1362 | — | — |
| HA07c 4d elevated N_std=1.5 | train | 14 | 10/14 | 69.2% (45.4%–88.3%) | 46.0% (39.2%–52.9%) | +23.2 (-1.9 to +48.4) | 0.0581 | — | — |
| HA07d 4d bidir N_std=1.5 | train | 14 | 12/14 | 84.6% (60.1%–96.0%) | 65.0% (58.2%–71.3%) | +19.6 (-0.4 to +39.6) | 0.0934 | — | — |
| HA08c 4d elevated N_std=1.5 | train | 14 | 9/14 | 61.5% (38.8%–83.7%) | 38.5% (32.0%–45.4%) | +23.0 (-3.3 to +49.4) | 0.0539 | — | — |
| HA11 4d elevated N_std=1.5 | train | 14 | 9/14 | 64.3% (38.8%–83.7%) | 41.5% (34.9%–48.4%) | +22.8 (-3.2 to +48.8) | 0.0836 | — | — |
| HA07d 4d bidir N_std=1.5 | validate | 15 | 13/15 | 86.7% (62.1%–96.3%) | 65.0% (58.2%–71.3%) | +21.7 (+3.2 to +40.1) | 0.0703 | — | — |
| HA10 4d bidir N_std=1.5 | validate | 15 | 13/15 | 86.7% (62.1%–96.3%) | 70.5% (63.8%–76.4%) | +16.2 (-2.2 to +34.5) | 0.1475 | — | — |
| HA01c rank >= 0.75 (per-axis effective_exertion) | train | 11 | 9/11 | 81.8% (52.3%–94.9%) | 60.5% (53.5%–67.1%) | +21.3 (-2.5 to +45.1) | 0.1355 | — | — |
| HA01c rank >= 0.75 (per-axis effective_exertion) | validate | 15 | 12/15 | 80.0% (54.8%–93.0%) | 60.5% (53.5%–67.1%) | +19.5 (-1.9 to +40.9) | 0.1085 | — | — |

## Notes

**Interpretation of CIs**: with N=14-15 crashes per era, recall CIs span 30+ percentage points. A point estimate of 86.7% (HA07d validate) has CI roughly [60%, 96%]. The verdict-bar pass (≥ 60%) is robust to lower-CI variation only if the lower bound stays > 60%; this varies by anchor.

**Fisher's exact vs χ²**: chose Fisher because some cells have small counts (e.g. crash trigger counts of 6-13). χ² approximation degrades for cell counts < 5; Fisher's exact is appropriate.

**One-sided choice**: the alternative hypothesis is *crash trigger rate > null trigger rate* per the pre-registered direction in each hypothesis.md. A two-sided test would double the p-value and flip a small number of close-to-α verdicts.

**Why these statistics were not in the original result.md files**: the project's pre-registration discipline emphasised the 3-criterion bar (frequency / discrimination / magnitude) rather than formal hypothesis-testing p-values. The peer-review §2 critique surfaced this gap. This audit retrofits the statistics; future hypothesis.md files should include a Fisher's exact + CI line in result.md by default.
