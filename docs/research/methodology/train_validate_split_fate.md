# Fate of the 2023-12-31 train / validate split

*Methodology decision drafted 2026-06-13 per [[feedback_methodology_decisions_documented_reasoning]]. Open until user review.*

## Citation status

This MD currently runs on first-principles reasoning only. Candidate references on single-subject longitudinal validation, n-of-1 trial reporting standards, and held-out validation for time-series inference have **not** been read or verified in our literature folder. They are listed in [`_pending_literature_fetch.md`](_pending_literature_fetch.md) as a fetch-and-verify task. Until those refs land, the literature row of the four-input reasoning is honestly downgraded to "deferred". The methodological reasoning stands on its own and does not depend on any specific paper.

---

## Aim

Decide the **fate of the existing 2023-12-31 date-based train / validate split** within Stratum 4 (LC with gevoelscore + crash labels, see [`lc_era_temporal_segmentation.md`](lc_era_temporal_segmentation.md)).

The 2023-12-31 boundary is currently locked in `crash_v2` ([`docs/research/analyses/hypotheses/crash_v2-definition/definition.md`](../analyses/hypotheses/crash_v2-definition/definition.md)) and is the primary validation surface for HA01b, HA02c, and a handful of other historical pre-regs.

This MD reasons from first principles — acting as if new to the question — about what role (if any) the date split should play going forward.

---

## 1. Data-given vs methodologically-chosen boundaries (recap)

Per [`lc_era_temporal_segmentation.md`](lc_era_temporal_segmentation.md), four temporal strata are dictated by data:

1. Pre-corona (2021-08-16 → 2022-03-20) — Garmin only
2. Acute corona infection (2022-03-21 → 2022-04-03) — Garmin only
3. LC, pre-gevoelscore (2022-04-04 → 2022-09-02) — Garmin only
4. LC, with gevoelscore + crash labels (2022-09-03 → present) — primary stratum for Wiggers pre-regs

**The 2023-12-31 boundary falls inside Stratum 4 and is NOT data-given.** It was chosen historically to split Stratum 4 into a "train" (before) and "validate" (after) portion. The original justification rested on the now-deleted trajectory / stabilisation framing. The boundary itself remains in `crash_v2`, but its motivation has been removed.

This MD asks: **given that the boundary is no longer motivated by an externally-grounded reason, what validation framework do we want going forward?**

---

## 2. Decision (proposed; pending user review)

**Primary validation framework for new Wiggers pre-regs: full Stratum 4 as a single pool**, with permutation null + stationary bootstrap CI per [`permutation_null_block_length.md`](permutation_null_block_length.md). No primary train / validate split.

**Historical pre-regs that locked under the 2023-12-31 split keep their original verdicts** as historical record. We do not retroactively re-lock HA01b, HA02c, or any other pre-2026-06-13 verdict.

**The 2023-12-31 split is preserved as a sensitivity overlay** (M3 per [`lc_era_temporal_segmentation.md`](lc_era_temporal_segmentation.md)) available to any new pre-reg that has a specific reason to report train-era vs validate-era discrimination as descriptive context. The overlay is descriptive only — no per-portion confirmatory verdict, no per-portion α threshold.

**No new date-based split is introduced in `crash_v2` or in the per-day master.** The existing `is_train_era` / `is_validate_era` columns are kept in the master for backward compatibility with locked verdicts but are not used by new pre-regs.

In short: **single-pool primary, historical split preserved as reproducibility artefact, optional descriptive overlay.**

## 3. Alternatives considered

| label | proposal | verdict | reason |
|---|---|---|---|
| **(a) original** | Keep 2023-12-31 split as reproducibility artefact only; new pre-regs use permutation null on full pool | accepted with refinement | The closest match to the chosen path. Refined here to explicitly retain the split as an optional M3 descriptive overlay (not just a reproducibility artefact). |
| **(b) original** | Remove the split entirely; drop `is_train_era` / `is_validate_era` columns | rejected | Breaks HA01b / HA02c reproducibility unnecessarily. The columns are zero-cost to keep; the policy not to use them in new pre-regs is what matters. |
| **(c) original** | Continue 2023-12-31 split as primary | rejected | The boundary date was chosen under the deleted trajectory / stabilisation framing. Continuing to lock new pre-regs to it is a sustained a-priori commitment without warrant — exactly what [[feedback_caveats_vs_apriori]] flags. |
| **(d)** | Re-choose the boundary on a methodological ground (e.g. corpus midpoint 2024-09-02) | rejected | Trades one a-priori boundary for another; introduces a new boundary without specific justification. If a hypothesis or methodological need emerges (M1/M2 per [`lc_era_temporal_segmentation.md`](lc_era_temporal_segmentation.md)), the new boundary is introduced inside that pre-reg with its warrant. |
| **(e)** | Adopt walk-forward cross-validation as primary | rejected | Walk-forward is appropriate for predictive-model evaluation but does not fit confirmatory hypothesis testing. Our framework is the latter. |
| **(f)** | Leave-one-out by crash episode | rejected as primary | Useful for prediction-quality assessment but not a natural fit for the discrimination-statistic framework we use. May be revisited as a sensitivity exercise. |
| **(g)** | Block time-series cross-validation (e.g. `TimeSeriesSplit` with embargo) | rejected | Model-evaluation framework, not confirmatory-inference. Falls under the same critique as (e) walk-forward. |
| **CHOSEN** | Single-pool primary + historical split as reproducibility artefact + optional M3 descriptive overlay | proposed | Cleanest reading of "primary surface determined by data; sub-boundaries warranted only by M1/M2/M3". Honest about within-subject inference at n=29. Does not break historical reproducibility. |

## 4. Four-input reasoning

### 4.1 Best-practices standards

- **Within-subject longitudinal inference** (n-of-1, single-case experimental design): the dominant validation framework is NOT held-out date splits. It is replication-across-time within the same subject combined with permutation-based inference within the available data. Held-out date splits are more typical of cross-subject prediction work (where the held-out group is genuinely a new population).
- **Time-series train / test splits** are appropriate when the test period is genuinely future-relative-to-model-development and the model parameters are fixed at train-time. Our 2023-12-31 split satisfies the first condition (validate period is later than train) but not the second (Wiggers pre-regs were developed iteratively with knowledge of post-2023-12-31 data; the user has been looking at the data continuously since).
- **Pre-registration discipline** under within-subject inference: the right anchor is the pre-registration of the hypothesis + analytical plan + decision rule **before the test runs**, not the artificial creation of a held-out group. Permutation null + bootstrap CI on the full pool is the standard within-subject validation pattern.
- **Reproducibility of historical findings** is preserved by keeping the original analytical pipeline and the original verdict files intact, NOT by forcing all new work to adopt the same framework. Historical findings can co-exist with a different new framework without contradiction.

### 4.2 Literature where it materially supports the choice

**Deferred** (see Citation status above). Candidate references queued in [`_pending_literature_fetch.md`](_pending_literature_fetch.md): CONSORT extension for n-of-1 trials (Shamseer et al. 2015), n-of-1 within-subject inference framing (Lillie et al. 2011), single-case experimental design standards (Kratochwill et al. 2013, also cited in [`lc_era_temporal_segmentation.md`](lc_era_temporal_segmentation.md)).

### 4.3 Our own tradeoff analysis

| dimension | continue split as primary (c) | drop split entirely (b) | single-pool primary + historical artefact + optional overlay (CHOSEN) |
|---|---|---|---|
| Honesty about n at primary level | poor (n=14 train / n=15 validate; CIs ≥ 30 pp wide) | best (n=29 in single pool) | best (n=29 in single pool) |
| HA01b / HA02c reproducibility | preserved | broken | preserved (verdicts + pipeline intact) |
| New pre-reg motivation discipline | weak (locks new pre-regs to unjustified boundary) | strong (no a-priori boundary commitment) | strong (no a-priori boundary commitment) |
| Backward compat with `is_*_era` columns | required | broken | preserved (columns kept; new pre-regs don't use them) |
| Risk of confusion between historical and new framework | low | high (verdict files reference dropped columns) | moderate (must be flagged in new pre-reg template) |
| Aligned with [[feedback_caveats_vs_apriori]] | mis-aligned (sustained a-priori commitment) | aligned but lossy (drops reproducibility) | aligned (a-priori commitment removed without dropping artefacts) |
| Researcher degrees of freedom | low | low | low (split is descriptive overlay only when invoked; cannot become a re-tuned primary) |

The weighting we apply: honesty-about-n at primary level + new-pre-reg discipline dominate. HA01b / HA02c reproducibility is a constraint we can satisfy without making the historical boundary the new primary. The chosen path satisfies both.

### 4.4 Our research limitations + objectives

- **n = 29 crash episodes in Stratum 4, 14 train / 15 validate under the historical split.** At n=14-15 per portion, recall CIs span ≥ 30 percentage points ([primary-verdict-statistics.md](../analyses/garmin_exploration/cards/primary-verdict-statistics.md)). At n=29 in a single pool, CIs are narrower (still wide by cross-subject standards, but the most defensible we can compute).
- **Single-subject** — there is no second pool of subjects to validate against. Cross-time held-out validation is the closest available analogue, but it is weaker than cross-subject held-out validation. Acknowledging this honestly is preferable to over-claiming the held-out structure.
- **The 2023-12-31 boundary was not blindly chosen** — it was chosen under the deleted trajectory / stabilisation framing. Continuing to use it as primary embeds an analytical artefact from a framing that no longer holds.
- **Observational design with mixed user awareness — tactical vs analytical**. Pre-research, the user used Garmin daily as a **tactical** pacing tool: real-time body battery drain rate AND failure-to-reload signals, heart rate elevation, and exertion readouts informed same-day behaviour, alongside the body signals felt without the watch (the primary pacing anchor) and pacing principles learned in ergotherapy (see project timeline). The user did NOT consciously analyse **aggregated** Garmin patterns across days / weeks / months during this period. The shift to an aggregated analytical view began with the Garmin GDPR dump that landed in 2026; this is when research-level analytical bias is introduced, not earlier. The 2023-12-31 validate era was therefore held out from analytical eyes in the strict research sense (no cross-day aggregated analysis happened during it), although it was lived through and tactically Garmin-paced. The held-out structure is weaker than cross-subject validation but **stronger than "user has been continuously analysing the data" would imply** — historical pre-regs that used the validate era passed a meaningful (if imperfect) held-out test. This refinement informs but does not change the chosen path: at n=14/15 per portion CIs are still ≥30 pp wide, the 2023-12-31 boundary itself was still chosen under a now-deleted framing, and single-pool primary remains the cleaner framework for new pre-regs.
- **Any train-vs-validate divergence** that appears in historical pre-reg verdicts on the legacy split is reportable as a descriptive M3 sensitivity overlay under the new framework. Specific historical divergences are NOT used as worked examples for new pre-regs because (a) the 2023-12-31 cutoff itself is contested (chosen under the now-deleted trajectory framing), and (b) several historical "divergences" rest on baseline-construction artefacts that do not survive the v3.2 lagged-baseline re-computation per CONVENTIONS §3.2 (see [REJECTED.md](../REJECTED.md) row `HA01b-recomputed` for the canonical case). Citing such divergences as worked examples would re-validate a structure the new framework explicitly retreats from.
- **Objective**: faithful descriptive characterisation of Wiggers claims under the descriptive-before-inference principle. The chosen path puts the primary verdict on the full available evidence, the historical artefact in the audit trail, and the descriptive overlay in the sensitivity-analysis layer where it belongs.

## 5. Operational consequences

1. **Per-day master columns**: `is_train_era` and `is_validate_era` are KEPT in `per_day_master.csv` for backward compatibility with historical verdict files and re-runs. They are NOT removed. Data dictionary entry annotated: "Historical artefact from the 2023-12-31 split, preserved for HA01b/HA02c reproducibility. New pre-regs should not use these columns as primary stratification; see [`train_validate_split_fate.md`](train_validate_split_fate.md)."

2. **`crash_v2` definition file**: the existing references to train / validate era in [`docs/research/analyses/hypotheses/crash_v2-definition/definition.md`](../analyses/hypotheses/crash_v2-definition/definition.md) are KEPT. No re-unlocking of `crash_v2`. The era references remain as the historical scaffolding that produced the locked label set.

3. **[`wiggers_test_design_on_chained_regime.md`](wiggers_test_design_on_chained_regime.md) constraint #3**: replace the placeholder "walk-forward discipline" framing with the chosen-path language:
   - Primary validation: full Stratum 4 as a single pool, permutation null + stationary bootstrap CI per [`permutation_null_block_length.md`](permutation_null_block_length.md), stratum framing per [`lc_era_temporal_segmentation.md`](lc_era_temporal_segmentation.md).
   - Historical split preserved as reproducibility artefact; not used by new pre-regs.
   - Optional M3 sensitivity overlay: a new pre-reg may report train-era vs validate-era discrimination as descriptive context, but cannot use either portion as a confirmatory verdict, and cannot apply per-portion α thresholds.

4. **[`wiggers_testable_hypotheses.md`](../wiggers_testable_hypotheses.md) pre-reg-file constraint #3** (the original "walk-forward discipline" line at lines ~138-147): replace with a one-line reference to this MD plus the chosen-path summary. Tier 1 / Tier 2 / Tier 3 shortlist edits are tracked separately.

5. **New pre-reg template** (the shape of any new Wiggers or Personal pre-reg file): the stratification section reads:
   > Primary stratum: LC with gevoelscore + crash labels (Stratum 4, see [`lc_era_temporal_segmentation.md`](lc_era_temporal_segmentation.md)). Primary validation: full-pool permutation null + stationary bootstrap CI per [`permutation_null_block_length.md`](permutation_null_block_length.md). Train / validate split: not used as primary; optional M3 sensitivity overlay per [`train_validate_split_fate.md`](train_validate_split_fate.md).

6. **Historical verdict files** (HA01b/result.md, HA02c/result.md, HA08/result.md, HA11/result.md, H05/result.md): UNCHANGED. Verdicts remain as locked. Any re-running of these under the new framework is a queued descriptive exercise (Q-entry in [`queued_work.md`](queued_work.md)), not a re-lock.

7. **Re-running historical pre-regs under the new framework**: queued as a single descriptive cross-check exercise (Q-entry in [`queued_work.md`](queued_work.md)). The binding recipe:
   - **Output format**: one side-by-side table with one row per locked pre-reg (HA01b, HA02c, HA08, HA11, H05), columns: `locked verdict`, `verdict under MD 2 + MD 3 framework`, `divergence (yes/no)`, `brief note on the source of divergence` (e.g. block scheme, single-pool vs split, multiplicity threshold, finite-sample variability).
   - **No automated re-locking** of any historical verdict. The locked verdict files (`result.md`) remain unchanged regardless of cross-check outcome.
   - **On divergence**: the cross-check report flags the divergence + names plausible drivers descriptively. It does NOT pick which framework is "correct".
   - **User-owned decision** on whether divergence warrants a follow-up action (new pre-reg, methodology revision, footnote on historical verdict). The cross-check report does not pre-commit a path.

8. **Train-vs-validate divergence framing — number, not narrative**. Any train-vs-validate divergence reported under the M3 sensitivity overlay (whether re-computed under MD 2 + MD 3 framework or surfaced from historical pre-reg verdicts on the legacy split) is reported as a descriptive number, not interpreted as evidence for any specific generative story. Effect-strengthening-over-time (the deleted trajectory story), stabilisation, label-precision drift, behavioural adaptation, measurement drift, season / life-event imbalance, and sampling variation at small per-era n are all plausible drivers that a single-subject observational design cannot adjudicate. Selecting any one of these post-hoc is confirmation bias dressed as inference. The overlay answers **"is the primary single-pool verdict robust to era partition?"** — it does NOT answer **"does the effect change over time?"**. The latter question the design cannot answer. Worked examples in pre-regs SHOULD NOT anchor on specific historical divergences (the HA01b case is the canonical reason — its original +17.3 pp validate-era divergence was a v3.1 rolling-baseline artefact that does not survive the v3.2 lagged-baseline re-computation per [REJECTED.md](../REJECTED.md) row `HA01b-recomputed`; using it as a worked example would re-validate both a contested cutoff and a wrong number). The principle is general, not example-anchored. Pre-reg template language to be embedded in [`wiggers_test_design_on_chained_regime.md`](wiggers_test_design_on_chained_regime.md): _"Under the M3 overlay, train-vs-validate divergence is a number, not a narrative."_

## 6. Open follow-ups

- **What if a Personal-register hypothesis has a specific reason to use the date split?** Personal-register entries are descriptive and may use the split if a specific within-subject change-point is hypothesised (e.g. treatment-start date). The Personal-register hypothesis carries its own warrant inside its pre-reg file; this MD does not bind P-entries.
- **Future Wiggers pre-regs at the bottom-of-the-tier list** (Tier 3 entries G3, H1, H4) are descriptive-pass-first per the shortlist update; this MD's framework applies to them when they progress to pre-reg.
- **Calendar-time block sensitivity overlay** (M3 per [`lc_era_temporal_segmentation.md`](lc_era_temporal_segmentation.md)) is a separate question from the train / validate split. A pre-reg may have neither, one, or both, with each warranted independently.

## 7. Cross-references

- Decision discipline: [[feedback_methodology_decisions_documented_reasoning]], [[feedback_caveats_vs_apriori]], [[feedback_descriptive_before_inference]]
- Companion methodology MDs: [`lc_era_temporal_segmentation.md`](lc_era_temporal_segmentation.md), [`permutation_null_block_length.md`](permutation_null_block_length.md)
- Evidence informing this decision: [primary-verdict-statistics.md](../analyses/garmin_exploration/cards/primary-verdict-statistics.md) (n per era and CI width); [REJECTED.md](../REJECTED.md) row `HA01b-recomputed` (the lagged-baseline correction that prompted dropping HA01b as a worked example per §5 bullet 8); [lag_profile_report.md](../analyses/garmin_exploration/activity-labels/output/lag_profile_report.md) was the source of the original artifact-baseline HA01b validate reading and is retained for reproducibility, not as evidence for new work.
- Affected docs: [`wiggers_testable_hypotheses.md`](../wiggers_testable_hypotheses.md), [`wiggers_test_design_on_chained_regime.md`](wiggers_test_design_on_chained_regime.md), per-day master DATA_DICTIONARY (annotation on `is_*_era` columns), [`queued_work.md`](queued_work.md) (re-run historical pre-regs under new framework)
- Citation fetch task: [`_pending_literature_fetch.md`](_pending_literature_fetch.md)
