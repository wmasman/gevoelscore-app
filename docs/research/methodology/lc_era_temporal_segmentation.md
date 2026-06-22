# LC-era temporal segmentation: data-given strata and methodological sub-boundaries

*Methodology decision drafted 2026-06-13 per [[feedback_methodology_decisions_documented_reasoning]]. Open until user review.*

## Citation status

This MD currently runs on first-principles reasoning only. Candidate statistical / methodological references (SCED replication standards, time-series sensitivity-analysis conventions, observational-cohort stratification practice) have **not** been read or verified in our literature folder. They are listed in [`queued_work.md`](queued_work.md) as a fetch-and-verify task. Until those refs land, the literature row of the four-input reasoning is honestly downgraded to "deferred". The methodological reasoning stands on its own and does not depend on any specific paper.

---

## Aim

Clarify which temporal boundaries within the gevoelscore corpus are **dictated by the data / empirical reality** (and therefore not methodological choices) versus which are **methodological or hypothesis-driven sub-segmentations** (and therefore require justification before they are introduced).

The previous source of phase boundaries (`project_recovery_trajectory` memory) was deleted on 2026-06-13 because the trajectory framing did not survive [[feedback_descriptive_before_inference]]. This MD picks up the question fresh — without anchoring on any previously-considered framing — and asks: **what boundaries do the data themselves give us, and what further sub-segmentation, if any, is warranted on methodological or hypothesis-driven grounds?**

---

## 1. Data-given strata (background, not a methodological choice)

**Sub-segmentation position** (added 2026-06-19 at the `lc_recovery_phase_axis.md` r2 lock): the within-Stratum-4 sub-segmentation that THIS MD §6 declines to default-commit to is provided by [`lc_recovery_phase_axis.md`](lc_recovery_phase_axis.md) §3.3-§3.5 (with §3.4 splitting into sub-phases 4a + 4b per the §7b operationalisation interview cleared 2026-06-19). That MD adopts the M1 lived-experience + M2 documented-confounder warrant framework from §2 of THIS MD and supplies the per-phase warrants directly. Descriptive analyses using the 3-layer axis (data-given outer + recovery-phase middle + citalopram-phase inner) cite both MDs; HA pre-regs opt in per §6 discipline below. Reciprocal lock-time cross-citation added 2026-06-19.

**Hard-boundary status in collapsibility conventions** (added 2026-06-22 at the `phase_axis_collapsibility_conventions.md` lock-commit): the data-given strata defined in this §1 (pre-corona / corona_infection / LC) are the **HARD BOUNDARY** in [`phase_axis_collapsibility_conventions.md`](phase_axis_collapsibility_conventions.md) §3.4 — pooling across these boundaries is a category error (mixing healthy / acute-viral / chronic-illness states; pooled estimate uninterpretable as a coherent quantity). The collapsibility conventions provide **3 within-LC tiers** for pooling phases of the recovery-phase axis ([`lc_recovery_phase_axis.md`](lc_recovery_phase_axis.md)) when justified by hypothesis (Tier A: 4a + 4b within phase 4; Tier B: phase 4 + phase 5 with `citalopram_phase_stratification §5.A/B/C` correction on CONFIRMED-citalopram channels; Tier C: phase 3 + 4 + 5 = full Stratum 4). The trigger is **hypothesis-driven only** — no data-driven collapse pathway, which is the dual of THIS MD §4 anti-data-driven-boundary-tuning discipline. Reciprocal-cite added 2026-06-22 at the `phase_axis_collapsibility_conventions.md` lock-commit.

Four temporal strata are dictated by the data:

| stratum | date range | what data exists | what analyses are possible |
|---|---|---|---|
| **1. Pre-corona** | 2021-08-16 → 2022-03-20 | Garmin only (started with the dump start date) | Garmin-only baseline characterisation: pre-illness reference distributions for RHR, sleep stress, BB, activity load |
| **2. Acute corona infection** | 2022-03-21 → 2022-04-03 | Garmin only | Short window (14 days); usable as a labelled acute-infection contrast for Garmin-only signals, too short for most analyses on its own |
| **3. LC, pre-gevoelscore** | 2022-04-04 → 2022-09-02 | Garmin only | LC characterisation on Garmin-only signals; no subjective score, no crash-label-based event detection |
| **4. LC, with gevoelscore + crash labels** | 2022-09-03 → present | Garmin + gevoelscore + note text + crash_v2 labels + intensity triage + PwC dossier (latter through 2024-02-26) | Full Wiggers-test machinery available |

**Stratum 1 caveat — seasonality**: pre-corona Garmin coverage is Aug 2021 → Mar 2022, which is ~7 months covering winter + shoulder seasons in a single cycle. Any contrast between Stratum 1 baseline distributions and Strata 3/4 distributions confounds illness state with season by construction — one pre-illness cycle cannot disentangle the two. Garmin-only descriptive contrasts that use Stratum 1 must stratify by season-within-stratum or explicitly acknowledge the confound. See §8 follow-up.

Boundaries between strata are set by **empirical events**, not by methodology:

- **2022-03-21**: corona infection start (clinical / lived-experience event)
- **2022-04-04**: LC start (clinical / lived-experience event — Monday after Fietsweekend Ardennen)
- **2022-09-03**: gevoelscore corpus start (the date the daily score started being logged)
- **2026-06-04**: Garmin dump end (data extraction boundary; updates with each new dump)

Two implications for any analysis:

1. **The primary stratum for any Wiggers pre-reg test is Stratum 4**, because Wiggers' claims involve `gevoelscore` (or its crash-label derivative) AND a Garmin-measured signal AND note-based features. All three coexist only in Stratum 4.
2. **Strata 1 and 3 can support Garmin-only descriptive contrasts** (e.g. RHR baseline shift, sleep-stress baseline shift, BB shape comparison) but they cannot support crash-discrimination or note-correlation tests by construction.

These strata surface in the per-day master as the `lc_phase` column (`pre_corona` / `corona_infection` / `lc`) plus the `has_score` coverage flag. No new column is required.

---

## 2. The methodological question

Given that Stratum 4 is the primary stratum, does sub-segmentation of Stratum 4 add value? Three possible reasons sub-segmentation might be warranted:

| reason | example | warranted? |
|---|---|---|
| **(M1) A specific hypothesis predicts a change-point** | "the effect strengthens after [external event X on date Y]" | Yes, if and only if the hypothesis is independently motivated and pre-registered. |
| **(M2) A methodological need** (e.g. address a known confounder, isolate a specific data-quality regime) | "FR245 device replacement on date Z changes BB calibration; analyse pre- and post-Z separately" | Yes, if the confounder is documented and material. |
| **(M3) Across-time sensitivity replication** | "split into N calendar blocks and check that the effect replicates" | Only if treated as a descriptive sensitivity overlay, not as a confirmatory replication count. |

**Sub-segmentations that are NOT warranted by default:**

- "Trajectory" / "stabilisation" / "recovery" sub-phases: rejected (recreates the deleted `project_recovery_trajectory` framing through a different door).
- "Pre- vs post- LC anniversary" or other calendar-driven splits without an empirical event: rejected (a-priori without justification).
- Data-driven change-point detection (PELT, binary segmentation) applied to `gevoelscore_rolling_*` columns: rejected unless a specific hypothesis warrants it.

---

## 3. Decision (proposed; pending user review)

**Primary analysis for any Wiggers pre-reg: full Stratum 4 (LC with gevoelscore + crash labels), no sub-segmentation.**

**Sub-segmentations are introduced only when one of M1 / M2 / M3 applies, and the warrant is stated in the pre-reg file BEFORE the test runs.**

- **No default calendar-time-block sensitivity overlay**, because no specific concern currently motivates one. If a future Wiggers pre-reg has reason to suspect non-stationarity across time (e.g. a metric shows visible drift in its rolling baseline), that pre-reg may add a calendar-block overlay under M3 — but the overlay is descriptive, not confirmatory, and no per-block α correction is applied because no per-block claim is made.
- **No default device-change overlay** (M2), because no device-change boundary is currently flagged as confounding. If a future re-extraction surfaces a calibration shift, that becomes a documented M2 boundary at that point, not in advance.
- **No default external-event split** (M1), because no current Wiggers hypothesis predicts a specific change-point in Stratum 4. If a Personal-register hypothesis predicts a change-point, the split is justified inside that pre-reg.

In short: **Stratum 4 is the analytic surface; sub-segmentation is added on demand, not by default.**

## 4. Alternatives considered

| label | proposal | verdict | reason |
|---|---|---|---|
| **Default to N calendar blocks** (e.g. 4 ~1-year blocks) | every Wiggers pre-reg includes a 4-block sensitivity table | rejected | Per-block n ≈ 7 crashes; CIs ≥ 50 pp wide. Per-block estimates are not informative absent a specific concern. Defaulting to the table risks invisible multiplicity inflation (4 estimates × N hypotheses). The right tool is on-demand under M3, not default. |
| **Default to pre-/post- some external event** | e.g. life-event split, treatment-start split, calendar-year split | rejected | A-priori without justification. Becomes legitimate per M1 if a hypothesis predicts it. |
| **Sub-segment Stratum 4 by `lc_phase`** | re-use existing column | rejected | All Stratum-4 days fall in `lc_phase == 'lc'` by construction. The column is already used for Stratum-level identification, not within-Stratum-4 splits. |
| **Data-driven change-point on `gevoelscore_rolling_*`** | PELT / binary segmentation, then analyse pre- and post- | rejected | Recreates the deleted trajectory framing through a different mechanism. Re-open only with an externally-grounded reason to expect change-points. |
| **CHOSEN: No default sub-segmentation, on-demand via M1/M2/M3 with pre-reg-level warrant** | Stratum 4 as primary surface; sub-segmentation introduced per-pre-reg with documented warrant | proposed | Cleanest reading of "boundaries dictated by data" vs "boundaries needing methodological warrant". Eliminates default multiplicity. Keeps the door open for legitimate per-hypothesis sub-boundaries. |

## 5. Four-input reasoning

### 5.1 Best-practices standards

- **Stratification by data coverage** is standard in observational longitudinal designs. Analyses are run on the stratum where the required variables coexist; cross-stratum comparisons are reported as descriptive contrasts, not as confirmatory tests.
- **Sub-stratification within a primary stratum requires justification** — this is the orthodoxy of observational-cohort and case-series methodology. The default is no sub-stratification; sub-stratification is introduced when a confounder, an externally-defined event, or a hypothesis warrants it.
- **Sensitivity analysis** (across alternative configurations, including time blocks) is a separate question from primary stratification. Sensitivity analysis varies one assumption at a time and reports a distribution; it does not introduce a confirmatory secondary verdict.

### 5.2 Literature where it materially supports the choice

**Deferred** (see Citation status above). Candidate references queued in [`queued_work.md`](queued_work.md): SCED replication standards, observational-cohort stratification orthodoxy, sensitivity-analysis discipline.

### 5.3 Tradeoffs

| dimension | default sub-segmentation | no default + on-demand (CHOSEN) |
|---|---|---|
| Cross-time replication signal | reported by default | reported when warranted |
| Multiplicity inflation risk | invisible (multiple per-block estimates × N hypotheses) | low (only when M1/M2/M3 triggers, and only as descriptive overlay) |
| Researcher degrees of freedom | low (boundaries fixed once) | low (boundaries fixed per pre-reg with documented warrant) |
| Audit trail | full but always-on | full and per-pre-reg |
| Aligned with [[feedback_caveats_vs_apriori]] | mixed (default-on is a soft a-priori commitment) | aligned (a-priori commitments only when warranted) |
| Aligned with [[feedback_descriptive_before_inference]] | mixed (defaults add interpretive layers before descriptive grounding) | aligned (descriptive grounding precedes any sub-segmentation choice) |

### 5.4 Our research limitations + objectives

- **n = 29 crash episodes in Stratum 4, 14 train / 15 validate (under the 2023-12-31 split — see [`train_validate_split_fate.md`](train_validate_split_fate.md)).** Any sub-segmentation reduces per-cell n proportionally.
- **Single-subject** — sub-segmentation across time is the closest available replication test, but it is weaker than across-person replication and should be framed accordingly.
- **Observational design with time-varying confounders** (season, life events, treatment, lifestyle adaptation). These confound any sub-segmentation result and must be acknowledged in any pre-reg that introduces a sub-boundary.
- **Objective**: faithful descriptive characterisation of Wiggers claims under the descriptive-before-inference principle. Defaults that add interpretive layers before descriptive grounding are inconsistent with the principle.

## 6. Criteria for adding a sub-boundary in a specific pre-reg

A Wiggers or Personal pre-reg may add a sub-boundary within Stratum 4 only if it satisfies all four of the following at pre-reg time:

1. **Warrant**: the sub-boundary is justified by M1 (specific hypothesis predicts change-point) OR M2 (documented confounder or data-quality regime) OR M3 (descriptive sensitivity overlay, not confirmatory).
2. **Documented in the pre-reg file**: date(s), reason, and analytical role (primary stratification vs sensitivity overlay) stated before any test runs.
3. **No re-tuning after seeing results**: the boundary is fixed at pre-reg time; not adjusted in response to per-segment results.
4. **No per-segment confirmatory claim under M3**: M3-driven sensitivity overlays report point estimates + CIs but do not use "supported" / "refuted" / "confirmed" per segment.

If any of these four fail, the sub-boundary is not introduced; the analysis runs on full Stratum 4.

## 7. Operational consequences

1. [`wiggers_test_design_on_chained_regime.md`](wiggers_test_design_on_chained_regime.md) gains a back-pointer to this MD in its statistical-hygiene section, replacing any default-segmentation language.
2. [`wiggers_testable_hypotheses.md`](../wiggers_testable_hypotheses.md) pre-reg-file constraint #3 (walk-forward discipline) references this MD for the primary-stratum framing. Walk-forward discipline applies to the choice of train/validate split ([`train_validate_split_fate.md`](train_validate_split_fate.md)), not to sub-segmentation of Stratum 4.
3. Per-pre-reg files include a stratification section. The default text: "Primary stratum: LC with gevoelscore + crash labels (2022-09-03 → present), per [`lc_era_temporal_segmentation.md`](lc_era_temporal_segmentation.md). No within-stratum sub-segmentation." Pre-regs that introduce a sub-boundary override this with their M1/M2/M3 warrant.
4. Already-locked verdicts (HA01b, HA02c, HA08, HA11, H05) keep their original stratification. Re-running them under this clarified policy is a queued descriptive exercise, not a re-lock.
5. No `stabilisation_period`, `recovery_arc`, or similar columns are introduced into the per-day master.

6. **As-of-date convention**: every Wiggers and Personal pre-reg states its data-cut date in its pre-reg file. New gevoelscore entries (and new Garmin extractions) accruing after a pre-reg locks do NOT trigger re-runs of locked verdicts unless explicitly queued. The right-edge of Stratum 4 advances over time; pre-reg files reference a specific as-of-date, not a moving target. This eliminates the temptation to silently re-fit as the corpus grows.

## 8. Open follow-ups

- **Garmin-only contrasts on Strata 1 and 3** (pre-corona baseline vs LC-pre-gevoelscore) are descriptive characterisations that do not require this MD's machinery. They sit naturally in [`lc_phase_descriptive.md`](lc_phase_descriptive.md) and the queued descriptive work. **Seasonality caveat applies**: per §1, Stratum 1 covers a single winter + shoulder cycle, so any Stratum 1 vs Stratum 3/4 contrast must stratify by season-within-stratum or acknowledge the illness-state × season confound. The cleanest path is a season-decomposition queue entry that splits each Stratum into season subsets before computing distributional contrasts (Q-entry in [`queued_work.md`](queued_work.md)).
- **Calendar-block sensitivity** under M3 is allowed but not required. If a future Wiggers pre-reg has a specific concern about non-stationarity for a specific metric, that pre-reg may add a 4-block sensitivity overlay scoped to that metric. The block construction (boundaries, count) is fixed at pre-reg time and documented as M3 with no per-block confirmatory claim.
- **Stratum 4 boundary moves over time**: the right-edge of Stratum 4 advances with each new gevoelscore entry. Pre-regs should reference "Stratum 4 as of date X" (the data-cut date) rather than a fixed right-edge.

## 9. Cross-references

- Decision discipline: [[feedback_methodology_decisions_documented_reasoning]], [[feedback_caveats_vs_apriori]], [[feedback_descriptive_before_inference]]
- Stratum 4 boundary anchors: [[project_lc_era_boundaries]], [[project_timeline_anchors]]
- Companion methodology MDs: [`permutation_null_block_length.md`](permutation_null_block_length.md), [`train_validate_split_fate.md`](train_validate_split_fate.md)
- Evidence informing this decision: [primary-verdict-statistics.md](../analyses/garmin_exploration/cards/primary-verdict-statistics.md) (per-era n and CI width)
- Affected docs: [`wiggers_testable_hypotheses.md`](../wiggers_testable_hypotheses.md) (pre-reg-file constraint cross-reference), [`wiggers_test_design_on_chained_regime.md`](wiggers_test_design_on_chained_regime.md) (statistical hygiene section), [`lc_phase_descriptive.md`](lc_phase_descriptive.md) (Strata 1-3 contrasts)
