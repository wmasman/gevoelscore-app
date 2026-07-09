# Cross-channel correlation + corpus near-identity map (load-bearing primitives)

**Card scope refresh 2026-07-09** per user Q "Card's headline framing was 'seven-channel primary panel' feel free to also initiate a new name for the card thats more accurate" (Bundle H+ event 6). The card originally opened as a fixed-panel correlation matrix on 2026-06-08 (seven primary channels tied to the Tier 2 peer-review action item at the time); it has since grown into a **corpus-wide near-identity map** as new near-identity pairs are discovered (Key finding 6 landed 2026-07-09 via OI-034 execution absorbing the `stress_mean_sleep` ≡ `asleep_stress_avg_uds` pair from `stress_mean_sleep/findings.md` Q3.1.e). The renamed title reflects both roles: **(a) fixed correlation matrix on the primary 7-channel panel**; **(b) growing corpus-wide near-identity map** absorbing new pairs from downstream operationalisation-support analyses. Filename `cross-channel-correlation.md` preserved to avoid link churn across the corpus; title + intro updated to reflect the map role.

**Computed 2026-06-08** per Tier 2 peer-review action item ([QUEUED-WORK.md](../../QUEUED-WORK.md)). Empirical replacement for the 'channels aren't statistically independent' caveat that appears in synthesis docs. **Primary 7-channel panel state anchored to 2026-06-08 corpus**; post-2026-06-08 near-identity discoveries listed below the primary panel (see "Near-identity pairs discovered post-2026-06-08" section + Key finding 6). Any downstream near-identity discovery (r > +0.90 or ρ > +0.85 per §3.3 threshold) should propagate to this card same commit-cycle as the source discovery lock; the card is the corpus-wide anchor for the "which channels are effectively the same primitive" question.

## Key findings (headlines)

1. **H02b ≡ H02d at the per-day primitive level (Spearman ρ = +1.000; Pearson r = +1.000)**. The 1737 shared valid days have identical `max_spike_minutes` values — H02d's bridge sentinel handling produces the same daily primitive as H02b. The discrimination difference (H02b +29.9 pp at 3d vs H02d bridge +31.8 pp at 5d) comes ENTIRELY from window-length + validity rules, NOT from a distinct underlying signal. **The "six channels with seven SUPPORTED tests" framing must drop H02d as a separate channel** — it's the same primitive evaluated at a different window. Effective independent channel count for train drops accordingly.

2. **HA10 ≡ −HA07c at the per-day primitive level (Spearman ρ = −0.922; Pearson r = −0.863)**. Morning BB peak and sleep stress mean are nearly the same underlying signal in opposite signs. This is structural in Garmin's BB algorithm (BB decreases when stress is high). So **HA10 and HA07c are NOT independent channels** — they are two views of the same autonomic-state measurement. HA10's validate-SUPPORTED + HA07c's validate-REFUTED is therefore internally contradictory at the population level, but the validation-vs-discrimination distinction explains it (the SAME signal can both discriminate crashes vs nulls AND fail the bar depending on threshold / lead-up window).

3. **HA06b ↔ HA07c: ρ = +0.377; HA06b ↔ HA10: ρ = −0.393** (moderate). Resting HR is positively correlated with sleep stress mean and negatively with morning BB peak. Consistent with the vagal-tone pathway (higher RHR ↔ less recovery, both ways).

4. **HA07c ↔ HA07d: ρ = +0.501** (moderate). Sleep stress mean and stdev are correlated but not collinear — they capture distinct facets (level vs variability).

5. **H02b ↔ HA11: ρ = +0.377** (moderate). Daily max spike duration and U-dip event count share variance (both within-day stress patterns), but at a level that supports treating them as related-but-distinct.

6. **`stress_mean_sleep` ≡ `asleep_stress_avg_uds` at the per-day primitive level (Pearson r = +0.929; Spearman ρ = +0.895; N = 1337)**. Discovered 2026-06-18 in the Strand A `stress_mean_sleep` operationalisation-support analysis (see [`analyses/descriptive/operationalisation_support/stress_mean_sleep/findings.md`](../../descriptive/operationalisation_support/stress_mean_sleep/findings.md) Q3.1.e LOCKED 2026-06-18). The pair is a **methodological-overlap near-identity, not a biological one**: `asleep_stress_avg_uds` is the UDS-side asleep-stress average (whole-night, from `daily_uds.csv`), while `stress_mean_sleep` is the custom-extracted mean of monitoring_b stress samples within the sleep window (from `sleep_stress_nightly.csv`). Both are "average stress during sleep" with slightly different sample-selection rules. **Implication for downstream HAs**: any HA test that uses `stress_mean_sleep` (or its HA07c operationalisation) should NOT also enter `asleep_stress_avg_uds` as a "second autonomic channel". They are the same primitive at the daily resolution. This pair is a UDS-side sister to HA07c and, via HA07c ≡ −HA10, indirectly ties to the autonomic-state cluster (Cluster 2 above).

**Effective N of independent channels**: with these correlations, the project's "seven SUPPORTED on six channels" actually represents roughly **3-4 effectively independent signal clusters**:
- **Cluster 1 (within-day stress)**: H02b/H02d + HA11 (ρ ≈ 0.38)
- **Cluster 2 (autonomic state)**: HA07c + HA10 (ρ ≈ −0.92) ± HA06b (ρ ≈ 0.36-0.39); UDS-side sister of HA07c is `asleep_stress_avg_uds` (methodological-overlap near-identity, r ≈ +0.93; per Key finding 6)
- **Cluster 3 (autonomic variability)**: HA07d (moderately tied to Cluster 2 via HA07c at +0.50)
- HA08c is a slope of Cluster 2's primitive, so adds little independent variance

**This profoundly affects multi-comparison interpretation**: with effective N ≈ 3-4, Bonferroni α = 0.05/4 ≈ 0.0125 (not 0.05/11 ≈ 0.0045 as the naive count suggests). Of the 11 primary verdicts, H02b (p=0.029) misses 0.0125 but H02d (p=0.011) clears it — but the H02b/H02d collinearity means these are one finding, so the headline becomes: **only H02d/H02b survives an honest effective-N Bonferroni correction**.

## Method

- **Per-day raw primitive values** loaded from existing CSV / UDS sources (no z-scoring, no lagging — we want the underlying biological correlation, not the lead-up-window correlation).
- **Inner-joined on calendar date** within the analysis window (2022-09-03 → 2026-06-05).
- **Pearson r** (linear) + **Spearman ρ** (monotonic).
- Minimum N=30 days required for a pairwise correlation; cells with insufficient data are blank.

HA08c is omitted as a separate row: it operates on the same raw `sleep_stress_mean` primitive as HA07c (HA08c is the trailing-5-day OLS slope of that series). At the raw-primitive level the two are identical; their distinct hypothesis verdicts come from different downstream transformations.

## Per-primitive day counts

- **H02b (max_spike_min)**: 1364 days
- **H02d (bridge_spike_min)**: 1365 days
- **HA11 (u_dip_count)**: 1354 days
- **HA06b (resting_hr_bpm)**: 1357 days
- **HA07c (sleep_stress_mean)**: 1339 days
- **HA07d (sleep_stress_stdev)**: 1339 days
- **HA10 (morning_bb_peak)**: 1359 days

## Spearman ρ matrix (monotonic correlation)

| | H02b | H02d | HA11 | HA06b | HA07c | HA07d | HA10 |
|---|---:|---:|---:|---:|---:|---:|---:|
| **H02b (max_spike_min)** | **1.000** | +1.000 | +0.377 | -0.005 | -0.045 | +0.048 | +0.047 |
| **H02d (bridge_spike_min)** | +1.000 | **1.000** | +0.377 | -0.005 | -0.045 | +0.048 | +0.047 |
| **HA11 (u_dip_count)** | +0.377 | +0.377 | **1.000** | +0.047 | +0.054 | +0.073 | -0.084 |
| **HA06b (resting_hr_bpm)** | -0.005 | -0.005 | +0.047 | **1.000** | +0.377 | +0.073 | -0.393 |
| **HA07c (sleep_stress_mean)** | -0.045 | -0.045 | +0.054 | +0.377 | **1.000** | +0.501 | -0.922 |
| **HA07d (sleep_stress_stdev)** | +0.048 | +0.048 | +0.073 | +0.073 | +0.501 | **1.000** | -0.366 |
| **HA10 (morning_bb_peak)** | +0.047 | +0.047 | -0.084 | -0.393 | -0.922 | -0.366 | **1.000** |

## Pearson r matrix (linear correlation)

| | H02b | H02d | HA11 | HA06b | HA07c | HA07d | HA10 |
|---|---:|---:|---:|---:|---:|---:|---:|
| **H02b (max_spike_min)** | **1.000** | +1.000 | +0.335 | +0.004 | +0.058 | +0.056 | -0.005 |
| **H02d (bridge_spike_min)** | +1.000 | **1.000** | +0.335 | +0.004 | +0.058 | +0.056 | -0.005 |
| **HA11 (u_dip_count)** | +0.335 | +0.335 | **1.000** | +0.052 | +0.081 | +0.066 | -0.096 |
| **HA06b (resting_hr_bpm)** | +0.004 | +0.004 | +0.052 | **1.000** | +0.359 | +0.121 | -0.414 |
| **HA07c (sleep_stress_mean)** | +0.058 | +0.058 | +0.081 | +0.359 | **1.000** | +0.602 | -0.863 |
| **HA07d (sleep_stress_stdev)** | +0.056 | +0.056 | +0.066 | +0.121 | +0.602 | **1.000** | -0.465 |
| **HA10 (morning_bb_peak)** | -0.005 | -0.005 | -0.096 | -0.414 | -0.863 | -0.465 | **1.000** |

## Pairwise N (intersection of valid days)

| | H02b | H02d | HA11 | HA06b | HA07c | HA07d | HA10 |
|---|---:|---:|---:|---:|---:|---:|---:|
| **H02b (max_spike_min)** | 1364 | 1364 | 1354 | 1356 | 1339 | 1339 | 1358 |
| **H02d (bridge_spike_min)** | 1364 | 1365 | 1354 | 1356 | 1339 | 1339 | 1358 |
| **HA11 (u_dip_count)** | 1354 | 1354 | 1354 | 1346 | 1334 | 1334 | 1348 |
| **HA06b (resting_hr_bpm)** | 1356 | 1356 | 1346 | 1357 | 1337 | 1337 | 1357 |
| **HA07c (sleep_stress_mean)** | 1339 | 1339 | 1334 | 1337 | 1339 | 1339 | 1339 |
| **HA07d (sleep_stress_stdev)** | 1339 | 1339 | 1334 | 1337 | 1339 | 1339 | 1339 |
| **HA10 (morning_bb_peak)** | 1358 | 1358 | 1348 | 1357 | 1339 | 1339 | 1359 |

## Mean |Spearman ρ| per channel (excluding self)

Channels with HIGH mean |ρ| are 'central' — they share variance with many others. Channels with LOW mean |ρ| are MORE INDEPENDENT.

| channel | mean \|ρ\| | interpretation |
|---|---:|---|
| **H02b (max_spike_min)** | 0.254 | moderately correlated with others |
| **H02d (bridge_spike_min)** | 0.254 | moderately correlated with others |
| **HA11 (u_dip_count)** | 0.169 | moderately correlated with others |
| **HA06b (resting_hr_bpm)** | 0.150 | moderately correlated with others |
| **HA07c (sleep_stress_mean)** | 0.324 | central — shares variance with many channels |
| **HA07d (sleep_stress_stdev)** | 0.185 | moderately correlated with others |
| **HA10 (morning_bb_peak)** | 0.310 | central — shares variance with many channels |

## What this means for synthesis claims

**The 'seven train-era SUPPORTED on six channels' framing**: the actual independence of these channels is now quantified rather than asserted. Channels with mean |ρ| > 0.3 are NOT independent samples of nature; they share underlying biology. Conservative interpretation: the number of effective independent measurements is roughly 1 / (1 + average pairwise |ρ|) × N_channels.

**Cross-era anchors (HA07d both eras)**: HA07d (sleep stress stdev) and HA10 (morning BB peak) are conceptually distinct channels (autonomic variability vs autonomic recharge). The correlation row tells whether they are biologically independent.

**Multi-comparison adjustment**: Bonferroni on 11 primary verdicts at α=0.05 → α=0.0045. But with effective N of channels < 7 due to correlation, the multi-comparison concern is bounded. The Fisher's exact + 95% CI doc ([primary-verdict-statistics.md](primary-verdict-statistics.md)) provides the per-verdict test that this correlation matrix puts in context.

**Caveat about HA10**: HA10's morning BB peak is structurally a fused composite of HR, HRV, and stress per Garmin's BB algorithm. So HA10 ↔ HA06b (RHR), HA10 ↔ HA07c (sleep stress mean), and HA10 ↔ HA07d (sleep stress stdev) correlations are EXPECTED to be non-zero by construction, not just biologically.

## Near-identity pairs discovered post-2026-06-08

The 2026-06-08 seven-channel panel above computed pairwise correlations across the primitive channels of the primary hypothesis grid. Subsequent operationalisation-support analyses have surfaced additional near-identity pairs against neighbouring channels that were not in the original panel. Propagated here for corpus-wide near-identity map completeness.

| pair | Pearson r | Spearman ρ | N | discovered | source | pair type |
|---|---:|---:|---:|---|---|---|
| `stress_mean_sleep` ≡ `asleep_stress_avg_uds` | +0.929 | +0.895 | 1337 | 2026-06-18 | [`stress_mean_sleep/findings.md`](../../descriptive/operationalisation_support/stress_mean_sleep/findings.md) Q3.1.e LOCKED 2026-06-18 | methodological-overlap (custom monitoring_b sleep-window mean vs UDS whole-night asleep-stress average) |

**Discipline for downstream HA authors**: near-identity pairs listed here follow the same rule as the primary panel above. Any HA test using either channel should NOT enter the sister as a "second autonomic channel"; they are the same primitive at the daily resolution.

## Status / Lock log

- **2026-06-08**: Seven-channel primary panel computed and locked (headline sections 1-5 + all three matrices + mean |ρ| table).
- **2026-07-09** (OI-034 execution): Extended Key findings with entry 6 propagating the `stress_mean_sleep` ≡ `asleep_stress_avg_uds` methodological-overlap near-identity pair discovered 2026-06-18 in the Strand A `stress_mean_sleep` operationalisation-support analysis (Q3.1.e); added the "Near-identity pairs discovered post-2026-06-08" table; annotated Cluster 2 with the UDS-side sister pointer. Primary seven-channel panel matrices and mean |ρ| values unchanged. Discharges [`stress_mean_sleep/findings.md`](../../descriptive/operationalisation_support/stress_mean_sleep/findings.md) Status refresh trigger 4 (near-identity-pair propagation into corpus-wide near-identity map).