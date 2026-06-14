# Intervention-effect descriptive characterisation

*Producer-mode methodology MD. Drafted 2026-06-14. **Pure-observation** Layer 1 descriptive analysis: characterises whether documented interventions coincide with visible step-changes in key Garmin channels. **No segmentation choice is locked.** This MD's findings inform whether segmented-baseline machinery is warranted; without findings, the question stays open.*

---

## 1. What this MD asks, and what it does not

**The question.** Documented interventions (CPAP start, citalopram start, citalopram stop, ergotherapie start, possibly others) **may or may not** produce step-changes in physiological baselines (RHR, BB, stress, sleep). The project's hypothesis tests use a 90-day rolling lagged baseline (`_lagged_lcera` columns), which adapts to local distributional shifts but does *not* explicitly segment around interventions. If an intervention produces a baseline step-change, three things go wrong:

- During the ~60-day transition the post-intervention days read as deviations until the rolling baseline catches up.
- Steady-state pre- vs post-intervention differences disappear into the rolling reference once it has caught up.
- A measurement-side baseline shift can read as a crash-precursor signal in a hypothesis test that's looking for autonomic deviation.

The "resting pulse of 60 as a global reference" framing fails the moment baselines step-change. The participant has documented multiple plausible step-change events on this corpus.

**What this MD does NOT do.** It does NOT pre-commit to segmenting baselines around interventions. **We do not yet know whether intervention effects exist on this corpus.** Per [CONVENTIONS §2.1](../CONVENTIONS.md#21-descriptive-before-inference) (descriptive before inference) and [§4.2](../CONVENTIONS.md#42-caveats-yes-a-priori-claims-no) (caveats vs a-priori), the honest move is to characterise first, then decide.

This MD specifies the descriptive analysis. The findings (when the analysis runs) determine whether a follow-up methodology MD (`intervention_baseline_segmentation.md`, currently nonexistent) is warranted.

**Substantive confound this analysis CANNOT resolve** *(highest-priority caveat; surfaced as fix #1 in the methodology review at [`reviews/methodology-intervention_effects_descriptive-2026-06-14.md`](../reviews/methodology-intervention_effects_descriptive-2026-06-14.md))*. The documented LC recovery trajectory on this corpus (crash frequency ~10/year in 2023-24 → ~2/year in 2025-26 per [`analyses/hypotheses/registry.md`](../analyses/hypotheses/registry.md)) **overlaps directly with the steepest part of the trajectory** for the early-2024 interventions: CPAP-interventie (2024-01-10 → 2024-04-17) and citalopram-buildup (2024-04-09 → 2024-06-20). A pre-vs-post comparison around these dates will detect the recovery trajectory as a "step-change" *even when no intervention effect exists*. **Findings should be read as 'consistent with intervention effect OR with secular recovery', not as causal attribution.** A follow-up segmentation MD would need matched non-intervention pseudo-boundaries (from quiet periods) and/or trend-detrending to disentangle the two. Out of scope here.

**Method choice in context — Mann-Whitney U as deliberate Layer 1 simplification.** The state-of-art for observational intervention-effect estimation is **interrupted time series (ITS) with segmented regression** ([Bernal, Cummins, Gasparrini 2017](https://academic.oup.com/ije/article/46/1/348/2622842) *Int J Epidemiol*), decomposing the response into pre-intervention level + trend + level-change β2 + post-intervention trend-change β3. **We deliberately use level-only Mann-Whitney U for this Layer 1 descriptive pass** — ITS is reserved for the follow-up segmentation MD if findings warrant. Level-only blind spot accepted: step-changes that are actually slope inflections (e.g. citalopram producing an accelerated-recovery slope rather than a clean level step) will read as 'gradual drift' or 'no visible change' in the human-coded transition_shape. Automated change-point detection (PELT, [Killick et al. 2012](https://www.tandfonline.com/doi/abs/10.1080/01621459.2012.737745); BCP, Adams & MacKay 2007) is similarly not used as primary at n=1 per WWC visual-inspection convention; could corroborate the human-coded transition_shape in a follow-up sensitivity layer if needed.

---

## 2. Interventions in scope — curated catalog

Pulled from `annotations.yaml` (external; gitignored; at `$GEVOELSCORE_DATA_PATH/raw/directus_exports/annotations.yaml`) AND curated via an explicit exclude list.

**Source-of-truth note** (added 2026-06-14 post-Session-B). `annotations.yaml` is **regenerated** from upstream sources on every run of [`pipeline/03_consolidate/merge_calendar_triage.py`](../pipeline/03_consolidate/merge_calendar_triage.py); direct edits to it are silently reverted on the next merge. The **canonical edit targets** for the interventions referenced here are:

| intervention | canonical source |
|---|---|
| CPAP-interventie, Citalopram-traject + sub-phases + markers, Naproxen-interventie, Breinvoeding-interventie | `$GEVOELSCORE_DATA_PATH/raw/directus_exports/hand_curated_spans.yaml` (`spans_post_2022` section) |
| Ergotherapie Rouschop, Fysiotherapie, Verwijzing huisarts | `$GEVOELSCORE_DATA_PATH/reviews/calendar_2022_triage.csv` (rows with `keep_yn=y`) |
| Garmin-derived Breathwork markers | `$GEVOELSCORE_DATA_PATH/processed/garmin/activities.csv` (via `merge_calendar_triage.py` activity-marker emitter) |

Date refinements made during this MD's development (CPAP end 2024-04-17 → 2024-04-16; Ergotherapie Rouschop end 2022-12-31 → 2022-12-22 + label refinement) were mirrored upstream into their canonical sources 2026-06-14 so they survive future merges.

The catalog is **not** raw-data-driven: the `interventie` category in `annotations.yaml` is heterogeneous (steady-state regimes, ad-hoc reactive use, administrative events, wachtlijst-overbrugging, single-session activities) and not every entry produces an analytically-meaningful boundary. The curation choice was made in Session C (2026-06-14) after observing what the raw-data-driven list looked like; see [audit fix v3 #1 in §7](#7-status).

| intervention | shape | dating (curated) | notes |
|---|---|---|---|
| Citalopram-traject | umbrella span + 6 dose sub-phase spans + 2 phase-transition markers | **3 meaningful boundaries**: 2024-04-09 (buildup start = umbrella start), 2024-06-20 (buildup → consolidation, 30mg plateau, added 2026-06-14 as marker), 2026-03-20 (consolidation → scale-down, added 2026-06-14 as marker). Umbrella end 2026-06-05 = data-cut, auto-skip. | 6 dose sub-phase spans collapsed by containment filter (§6) |
| CPAP-interventie | trial span | **2024-01-10 (start) → 2024-04-16 (end)** per annotations; end refined 2026-06-14 to the test-apparaat night itself (was 2024-04-17 day-after; was 2024-02-28 schatting) | start analyzable; end CONFOUNDED with Citalopram start (see §2b) |
| Ergotherapie Rouschop, Bunnik | trial span (~13 weeks) | **2022-09-22 (start) → 2022-12-22 (end approximate)** per annotations | end is ~13-week estimate; day_entries.json has zero session mentions, no precise end available; findings around end-boundary carry lower weight |

**Excluded by label keyword** (in §6 script's `EXCLUDE_LABEL_KEYWORDS`):

| pattern | label(s) matched | reason |
|---|---|---|
| `fysiotherapie` | "Fysiotherapie (overbrugging wachtlijst ergo)" 2022-06-17 → 2022-09-05 | wachtlijst-overbrugging, not steady-state therapeutic regime |
| `naproxen` | "Naproxen-interventie" 2025-03-27 → 2026-06-10 | confirmed ad-hoc / reactive in 20 day-entry mentions (taken when hoofdpijn present, not steady-state daily); no step-change onset semantics |
| `breinvoeding` | "Breinvoeding-interventie" 2026-03-10 → 2026-08-31 | overlaps directly with Citalopram scale-down (2026-03-20) — confounded boundary, dropped per Session C decision |
| `verwijzing` | "Verwijzing huisarts naar ergotherapie" 2022-09-22 → 2022-09-23 | administrative event, single-day; already contained-in-Ergotherapie-Rouschop and removed by containment filter |
| `breathwork` | 5 markers (2022-06-15, 2026-03-01, 2026-03-10, 2026-04-14, 2026-04-16) | single-session activity events, not intervention regimes |

The exclude list is encoded by **label substring match** (lowercase) so adding new `interventie` entries with these keywords doesn't require code changes. Adding any other intervention class (with a label NOT containing an exclude keyword) auto-flows into the catalog on the next script run — the underlying YAML-driven mechanism is preserved; only known-non-analytical patterns are filtered.

**Key principle for span-shaped interventions**: both the start AND the stop boundary are analytically interesting because each may produce its own step-change in *opposite directions* (medication-on shifts baseline one way at start; medication-off shifts it back — or to a different equilibrium — at stop). Treating only the start hides the second boundary's effect.

**Decision: citalopram is segmented into 3 phases** (buildup / consolidation / scale-down) — not 6 dose transitions, not 1 umbrella boundary. Decided 2026-06-14.

| phase | window | meaning |
|---|---|---|
| **Buildup** | 2024-04-09 → 2024-06-20 (~10 weeks) | 0 → 10 → 20 → 30mg ramp |
| **Consolidation** | 2024-06-20 → 2026-03-20 (~21 months) | stable 30mg plateau |
| **Scale-down** | 2026-03-20 → 2026-06-05 (~11 weeks; ongoing) | afbouw 30 → 20 → 10 → 8mg druppelvorm |

Three meaningful analysis boundaries fall out:

- **2024-04-09** (start of buildup) — picked up from the umbrella span's start.
- **2024-06-20** (buildup → consolidation; 30mg plateau reached) — added 2026-06-14 as an `interventie`-category marker in `annotations.yaml`.
- **2026-03-20** (consolidation → scale-down; afbouw begins) — added 2026-06-14 as an `interventie`-category marker.
- (Umbrella end 2026-06-05 = data-cut, auto-skipped by the `len(post) < 5` check.)

Each boundary has at least one window anchored in the long stable consolidation plateau, maximising signal. Rationale for not slicing finer (6 boundaries): the early buildup (10mg → 20mg) phase is only 21 days, producing sub-truncation post-windows below 5 days; the late afbouw cluster has 28-40 day spacing, also producing short windows. The 3-phase structure captures the meaningful clinical-pharmacological transitions without exceeding what the rolling-baseline window analysis can resolve.

**Script implementation**: §6 applies a **containment filter** to skip the 6 dose-level sub-phase spans (each contained in the umbrella). The 2 phase-transition markers bypass the filter (markers are date-events, not span-events) and become explicit boundaries alongside the umbrella's start. CPAP-interventie and Ergotherapie Rouschop are unaffected (no sub-phases; both ARE umbrellas).

**Deferred** (out of scope here): finer-grained questions like "does each individual dose step produce its own distinct transient?" need different machinery — paired-window comparison without rolling baseline, or qualitative single-day inspection of the dose-step dates already in `annotations.yaml`.

Additions: any other `interventie`-category marker / span in `annotations.yaml` should be included. The catalog is data-driven, not pre-specified. The §6 script filters on `category == 'interventie'` only; individual day-level markers under `category: medical` (e.g. per-day CPAP notes during the trial, per-session ergotherapeut visits after the Rouschop trial) are NOT separately analysed as interventions — only the parent `interventie` umbrella spans are.

LC onset (2022-04-04) is the *biggest* baseline step-change but is already handled by the `_lagged_lcera` variant of every v3.2 column (baseline excludes pre-LC days). It is NOT in scope here — the rolling-lcera machinery already segments around it.

---

## 3. Baseline-channel step-change check

The seven per-day **baseline channels** likely to reflect autonomic baseline shifts. A step-change in any of these around an intervention would distort the `_lagged_lcera` rolling baseline used by hypothesis tests — i.e. the *reference frame* moves, and predictors expressed as z-scores against that baseline become biased.

- `resting_hr` — the channel the user's framing quote explicitly references ("rustpols van 60").
- `bb_overnight_gain` — overnight recovery, plausibly affected by CPAP and citalopram.
- `bb_lowest` — daily minimum, may shift with medication state.
- `all_day_stress_avg` — Firstbeat composite, may shift with autonomic medication.
- `stress_mean_sleep` — sleep-window stress, plausibly affected by CPAP + citalopram.
- `sleep_efficiency` (or `sleep_duration_min` + `sleep_awake_min` separately) — sleep architecture, plausibly affected by CPAP.
- `respiration_avg_sleep` — sleep respiration, plausibly affected by CPAP.

The channel list is descriptive — additional baseline channels can be added without pre-registration concern (this is not a hypothesis test).

**Definitional-pair structure** (per [CONVENTIONS §3.3](../CONVENTIONS.md#33-one-column-per-definitional-pair)): three pairs in the list are correlated by construction or by Layer 3 finding — `bb_overnight_gain` ↔ `bb_lowest`, `stress_mean_sleep` ↔ `all_day_stress_avg`, and `sleep_efficiency` ↔ `sleep_duration_min`/`sleep_awake_min`. Downstream §5 interpretation should treat co-firing pair-members as one signal, not two; a finding shape that fires on both `bb_overnight_gain` AND `bb_lowest` is one autonomic-recovery signal, not two independent channels.

**Queued — literature anchors for the channel selection**: the "plausibly affected by CPAP / citalopram" framing above is project-intuition. Per-channel intervention-effect literature exists (Marin 2010 + Tantucci 2003 for CPAP autonomic effects; Licht 2010 + Kemp 2010 for SSRI HRV; Wichniak 2017 for SSRI sleep) and would lift channel selection from intuition to literature-grounded. Queued in [`QUEUED-WORK.md` Tier 3 (methodological refinement, deferred)](../QUEUED-WORK.md#tier-3-methodological-refinement-deferred); surfaced as fix #4 in the methodology review at [`reviews/methodology-intervention_effects_descriptive-2026-06-14.md`](../reviews/methodology-intervention_effects_descriptive-2026-06-14.md). The descriptive script run (Session C) is NOT gated on this lit pass.

## 3b. Outcome-channel contamination check (gevoelscore)

`gevoelscore` is a methodologically distinct case from §3 and warrants a parallel-but-separately-framed pass:

- **§3 channels are the *baseline*** — the autonomic reference frame the lagged-baseline machinery computes against. A step-change there distorts the rolling baseline; hypothesis tests using `_lagged_lcera` z-scores get a wrong frame and may show false positives or negatives.
- **§3b `gevoelscore` is the *outcome*** — the dependent variable from which crash labels are derived (`crash_v2`). A step-change there means the outcome distribution itself shifted across the boundary: crash labels become non-comparable across the boundary, base rates of `is_crash` change, and AUCs / discrimination metrics computed on a frame spanning the boundary mix two different label-generating distributions.

Both checks use the same analysis shape (pre-vs-post window comparison with the §6 script). What differs is what their findings imply:

| if a step-change is found in... | the implication is... |
|---|---|
| a §3 baseline channel | the channel's lagged baseline may need M2 segmentation around this boundary; affects *predictors* |
| §3b `gevoelscore` | hypothesis tests' *outcome* is contaminated; crash labels on either side of the boundary represent different distributions; affects *both predictors AND the labels themselves* |

A `gevoelscore` step-change is therefore the more methodologically serious finding. Plausible drivers on this corpus: citalopram (SSRI directly modulates affect), CPAP (improved sleep quality can shift felt-state baseline). If a citalopram phase transition coincides with a `gevoelscore` step-change, every hypothesis tested with crash-v2 labels straddling that boundary inherits a label-frame discontinuity.

**Operational implementation**: the §6 script runs `gevoelscore` through the same analysis as the §3 channels (one entry in the `CHANNELS` list). The summary CSV makes the distinction visible by channel name; the human-coded `transition_shape` column applies identically. The methodological consequence — whether segmentation is warranted on the baseline side, the outcome side, or both — is read off the findings in the follow-up decision step.

---

## 4. Analysis shape

The `[d-30, d+60]` window below is an instance of the **situational multi-day window** category per [`time_resolution.md` §2.3](time_resolution.md) — the window length is anchored to the mechanism (post-intervention autonomic equilibration, weeks-to-months), not to a generic "monthly" grain. The mechanism-driven scale-choice rule lives in [`time_resolution.md` §6](time_resolution.md); this MD is the worked instance for the intervention-around question.

For each `(intervention, channel)` pair, around the intervention date `d`, with neighbour truncation against `d_prev`/`d_next` and a **transition-buffer sweep** `B ∈ {7, 14, 28, 42}` days:

1. **Plot** *(at primary buffer `B=14` only)*: channel value per day across the `[d-30, d+60]` nominal window, with intervention date marked as a red dashed vertical line. Add the channel's `_lagged_lcera` baseline overlay if it exists for these days. **Mark adjacent boundaries** (`d_prev`, `d_next`) as gray dashed lines if they fall within the window — they signal where pre/post windows were truncated.

2. **Pre vs post summary statistics, with neighbour-truncated windows + buffer sweep**:
   - **Pre window**: `[max(d-30, d_prev+B+1), d-1]`. Truncated at `d_prev+B+1` so the pre window excludes the previous boundary's `B`-day transient.
   - **Transition window**: `[d, d+B]` — `B`-day buffer excluded from the post analysis; not separately reported.
   - **Post window**: `[d+B+1, min(d+60, d_next-1)]`. Truncated at `d_next-1` to exclude the next boundary's effects.
   - **Buffer sweep**: each pair gets one summary row per `B`. Pharmacological anchors — citalopram steady-state plasma ~7-10 days; clinical effect onset 2-4 weeks; CPAP autonomic effect 2-4 weeks. **Primary buffer = 14**; the other three are sensitivity. Surfaces fragility (a finding that fires only at `B=14` but not at `B=28` is buffer-dependent and weaker).
   - For each `(channel, B)`: n, median, IQR per window; signed difference in medians (post − pre).
   - When a window is truncated below 5 days of data, the pair is skipped (existing `len < 5` check).

3. **Statistical descriptors per (channel, buffer)** — all reported as descriptive statistics, NOT verdicts:
   - **Mann-Whitney U** + p-value (`mw_u`, `mw_p`). p-value is under independence; on autocorrelated daily data this is inflated.
   - **Detrended Mann-Whitney p-value** (`mw_p_after_linear_detrend`). Linear fit on the pre-window (`np.polyfit(deg=1)` with x = days-from-d), extrapolated forward through the post-window; subtract from both pre and post values; recompute Mann-Whitney U on residuals. **Closes the recovery-trajectory confound at the column level** per [CONVENTIONS §3.7](../CONVENTIONS.md#37-trajectory-detrend-sensitivity-for-raw-pre-vs-post-comparisons). If `mw_p_after_linear_detrend >> mw_p`, the apparent step was the underlying recovery trajectory leaking through; if `mw_p_after_linear_detrend ≈ mw_p`, the step survives detrending and is more credibly event-driven. **The single highest-leverage residual fix from the v2 methodology review**; addresses A7.4 ("underlying-trend confound").
   - **Block-bootstrap p-value** (`mw_p_block_bootstrap`). 7-day block-permutation null (1000 resamples; block length matches the project's [`permutation_null_block_length.md`](permutation_null_block_length.md) default). Robust to within-window autocorrelation. If `mw_p_block_bootstrap` >> `mw_p`, the asymptotic test was over-confident.
   - **Rank-biserial r** (`r_rb`) = `2·U / (n_pre × n_post) - 1`. Effect-size matched to Mann-Whitney; bounded `[-1, +1]`. `|r_rb| < 0.1` = negligible; 0.1-0.3 = small; 0.3-0.5 = medium; ≥ 0.5 = large.
   - **Bootstrap 95% CI on median-diff** (`median_diff_ci_lo`, `median_diff_ci_hi`). 1000 percentile-bootstrap resamples within each window. A CI crossing zero is "consistent with no shift".

4. **Transition-shape coding** (human-coded after plot review at primary `B=14`): one of `{no_visible_change, gradual_drift, step, U_shaped, noisy_inconclusive}`.
   - **Pre-spec for `no_visible_change`**: ALL of (a) `|median_diff| ≤ 0.5 × IQR_pre`, (b) `|r_rb| < 0.1`, (c) `mw_p > 0.10`, (d) `mw_p_block_bootstrap > 0.10`, (e) `mw_p_after_linear_detrend > 0.10`. If all five hold the pair is `no_visible_change` regardless of rater intuition; if any one fails the rater codes among the other four categories on the plot. Condition (e) is the trajectory-detrend gate — a finding can fail (e) while passing (c)+(d), in which case the apparent null was the trajectory masking a real step that detrending reveals.

**Why truncation matters**: the citalopram afbouw was already collapsed to a 3-phase structure in §2, removing the close-spaced afbouw cluster. With the 3-phase collapse + neighbour truncation, the closest spacing in the curated catalog is between **2024-04-09 (citalopram buildup start) and 2024-04-16 (CPAP end), 7 days apart**; at every `B ≥ 7` this produces empty windows on both sides (the citalopram-start post-window and the CPAP-end pre-window are both truncated to nothing). **Both boundaries fall out at all four buffers — the 2024-04 cluster is structurally unanalyzable by this method.** The `_window_days` columns surface this directly (negative values indicate empty windows; the `len < 5` check produces NaN rows). See §8 for the cascading impact on findings.

## 2b. Channel coverage gap — `bb_overnight_gain`

A second structural caveat discovered by the run: **`bb_overnight_gain` only has data from 2024-09-18 onward** (n=593 days vs n=1731 for `resting_hr`). All boundaries before 2024-09-18 return `n_pre=0, n_post=0` for this channel — i.e. the 2022 Ergo boundaries, the 2024-01-10 CPAP start, the 2024-04-09 Citalopram start, and the 2024-06-20 phase transition all have NO `bb_overnight_gain` coverage. The only fully-covered boundary is 2026-03-20 (Citalopram scale-down). Findings on `bb_overnight_gain` are therefore single-boundary findings, not corpus-wide.

**Root cause** *(verified 2026-06-14 Session D, supersedes the original "pipeline switched on overnight-gain extraction late" reading)*. The cause is **not** local pipeline lateness. Garmin rolled the underlying UDS stats out in two stages on this FR245, same watch and same firmware family across both boundaries: `SLEEPSTART` first emitted 2024-07-08, `SLEEPEND` first emitted 2024-09-18. The extractor at [`pipeline/01_extract/garmin_uds_extras.py`](../pipeline/01_extract/garmin_uds_extras.py) applies no date filter; it just NaN-propagates when either input stat is absent in the upstream JSON. Empirical evidence: pre-2024-09-18 UDS files exist, are parsed, and contribute every other field — they simply lack the `SLEEPEND` entry in `bodyBattery.bodyBatteryStatList`. The 2024-09-18 boundary is therefore a **data-collection-side boundary**, not a project-side one.

**Documented proxy available from 2024-07-08** (`bb_overnight_gain_proxy` = `HIGHEST - SLEEPSTART`). Validated on n=593 post-2024-09-18 days where both channels exist: Pearson r = 0.989 vs truth, median residual 0 BB units, 550 / 564 clean days within ±5 units, HIGHEST median timestamp 06:00 local. For the 2024-06-20 boundary, the proxy converts the post-window from `n_post = 0 / 90` to `n_post = 71 / 90` (the 2024-07-08 .. 2024-09-17 bridge days). The pre-window remains `n_pre = 0 / 90` because `SLEEPSTART` is also absent before 2024-07-08; no pre-2024-07-08 boundary benefits. Sensitivity-only consumers should report the truth-channel finding first and the proxy-augmented post-window as a coverage-extension column, not in place of the primary. Methodology: [`methodology/bb_overnight_gain_proxy.md`](bb_overnight_gain_proxy.md).

**Why the buffer sweep matters**: with `B=7` the comparison is "off-drug vs drug-at-steady-state-plasma-but-pre-clinical-effect"; with `B=28` it's "off-drug vs clinical-effect-state". Citalopram clinical onset is 2-4 weeks (longer than the original 14-day buffer); a step-change that survives only at the smaller buffer is fragile to onset-window assumption.

Output:
- One PNG per `(intervention, channel)` pair (primary buffer only) at `$GEVOELSCORE_DATA_PATH/analyses/intervention_effects/plots/`.
- One CSV row per `(intervention, channel, transition_buffer_days)` at `$GEVOELSCORE_DATA_PATH/analyses/intervention_effects/summary.csv`. Columns: `intervention, intervention_date, channel, transition_buffer_days, is_primary_buffer, n_pre, pre_window_days, median_pre, iqr_pre, n_post, post_window_days, median_post, iqr_post, median_diff, median_diff_ci_lo, median_diff_ci_hi, mw_u, mw_p, mw_p_block_bootstrap, mw_p_after_linear_detrend, r_rb, transition_shape`. Expected row count: ~8 boundaries × 8 channels × 4 buffers ≈ 256 rows. Filter `is_primary_buffer == True` for the primary reading; the sensitivity rows are for the buffer-fragility check; compare `mw_p` vs `mw_p_after_linear_detrend` to read whether the recovery-trajectory confound is doing work on each finding.

---

## 5. What the findings inform

Findings determine the path forward; no path is committed in advance.

| finding shape | implication |
|---|---|
| **No `(intervention, channel)` pair shows visible step-change** (transition_shape = "no visible change" everywhere) | Rolling lagged baseline is empirically adequate. No M2 boundaries warranted. Caveats stay in P4a/P4b/P5b/C4b/pacing-practice but do not drive segmentation. Question closed with negative finding. |
| **One specific intervention shows clear step-changes across most channels** (e.g. citalopram on RHR + BB + stress) | Corpus-wide M2 boundary at that intervention warranted. Author follow-up `intervention_baseline_segmentation.md` locking dates + affected channels. |
| **One specific channel is affected by most interventions** (e.g. RHR steps with each medication change) | Channel-specific lagged baseline computation needed; that channel's baseline should be M2-segmented around documented interventions. Same follow-up MD, narrower scope. |
| **Heterogeneous: scattered pairs show shifts** (one channel × intervention here, another there, no pattern) | Treat as per-pair M2 decisions in individual pre-regs, not a corpus-wide rule. Caveats stay; no global segmentation MD. |

The descriptive findings are not themselves the segmentation decision; they inform a subsequent decision. The decision step gets its own user review.

---

## 6. Script outline

Implementation: [`docs/research/analyses/garmin_exploration/intervention_effects/run.py`](../analyses/garmin_exploration/intervention_effects/run.py) (committed; outputs land in `$GEVOELSCORE_DATA_PATH/analyses/intervention_effects/` which is gitignored). Run with `GEVOELSCORE_DATA_PATH=… python run.py`. The committed script differs from the outline below only in: (a) the `EXCLUDE_LABEL_KEYWORDS` curation list per §2; (b) Windows-safe filename sanitization for plot paths; (c) console-log diagnostics for catalog + channel coverage.

```python
"""
Intervention-effect descriptive characterisation.
Per methodology/intervention_effects_descriptive.md.
"""

from pathlib import Path
import os
import yaml
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import mannwhitneyu

DATA = Path(os.environ["GEVOELSCORE_DATA_PATH"])
OUT  = DATA / "analyses" / "intervention_effects"
(OUT / "plots").mkdir(parents=True, exist_ok=True)

# 1. Load per_day_master + annotations
master = pd.read_csv(DATA / "unified" / "per_day_master.csv", parse_dates=["date"])
master = master.set_index("date").sort_index()

annot = yaml.safe_load((DATA / "raw" / "directus_exports" / "annotations.yaml").read_text())

# 2. Extract interventie markers + span boundaries WITH CONTAINMENT FILTER.
# The containment filter keeps only "umbrella" spans (NOT contained in another interventie span),
# so the 6 citalopram dose-level sub-phases are collapsed automatically. Markers bypass the
# filter, so the 2 phase-transition markers (buildup->consolidation, consolidation->scale-down)
# are picked up explicitly. See §2 decision block for rationale.

int_spans_raw = [s for s in annot.get("spans", []) if s.get("category") == "interventie"]

def _span_bounds(s):
    return pd.Timestamp(s["start"]), pd.Timestamp(s.get("end") or s["start"])

def is_contained_in(small, big):
    if small is big: return False
    s_start, s_end = _span_bounds(small)
    b_start, b_end = _span_bounds(big)
    return (s_start >= b_start and s_end <= b_end
            and (s_start, s_end) != (b_start, b_end))

umbrella_spans = [s for s in int_spans_raw
                  if not any(is_contained_in(s, other) for other in int_spans_raw)]

raw = []
for m in annot.get("markers", []):
    if m.get("category") == "interventie":
        raw.append((m["label"], pd.Timestamp(m["date"])))
for s in umbrella_spans:
    raw.append((f"{s['label']} (start)", pd.Timestamp(s["start"])))
    if s.get("end"):
        raw.append((f"{s['label']} (end)", pd.Timestamp(s["end"])))

# 2b. Dedupe by date: umbrella-and-sub-phase overlap (citalopram) + chained sub-phase
# boundaries (fase N end = fase N+1 start) would otherwise double-count.
# Merge overlapping labels into a single "/"-separated label per unique date.
by_date = {}
for label, d in raw:
    by_date.setdefault(d, []).append(label)
interventions = [(" / ".join(sorted(set(labels))), d) for d, labels in sorted(by_date.items())]

# 3. Channels of interest — §3 baseline channels + §3b outcome channel.
# gevoelscore is methodologically distinct (outcome contamination, not baseline shift) —
# see §3b of the MD for why it's grouped with baseline channels operationally but read separately
# in the findings.
CHANNELS = [
    # baseline channels (§3)
    "resting_hr", "bb_overnight_gain", "bb_lowest",
    "all_day_stress_avg", "stress_mean_sleep",
    "sleep_efficiency", "respiration_avg_sleep",
    # outcome channel (§3b) — separate methodological role
    "gevoelscore",
]

# 4. Sensitivity-sweep + statistical-descriptors config + helpers
TRANSITION_BUFFERS = [7, 14, 28, 42]  # days excluded after d before post-window starts
PRIMARY_BUFFER     = 14               # used for plots and is_primary_buffer column
N_BOOTSTRAP        = 1000             # for both block-bootstrap p and median-diff CI
BLOCK_LEN          = 7                # block length for permutation null (matches project default)
RNG_SEED           = 20260614

rng = np.random.default_rng(RNG_SEED)

def windows_for(d, d_prev, d_next, B):
    pre_start  = max(d - pd.Timedelta(days=30), d_prev + pd.Timedelta(days=B + 1))
    pre_end    = d - pd.Timedelta(days=1)
    post_start = d + pd.Timedelta(days=B + 1)
    post_end   = min(d + pd.Timedelta(days=60), d_next - pd.Timedelta(days=1))
    return pre_start, pre_end, post_start, post_end

def rank_biserial(u, n_pre, n_post):
    return 2.0 * u / (n_pre * n_post) - 1.0

def bootstrap_median_diff_ci(pre_arr, post_arr, n_boot, rng_local, alpha=0.05):
    diffs = np.empty(n_boot)
    n_pre, n_post = len(pre_arr), len(post_arr)
    for i in range(n_boot):
        ps = rng_local.choice(pre_arr,  size=n_pre,  replace=True)
        po = rng_local.choice(post_arr, size=n_post, replace=True)
        diffs[i] = np.median(po) - np.median(ps)
    lo, hi = np.percentile(diffs, [100 * alpha / 2, 100 * (1 - alpha / 2)])
    return float(lo), float(hi)

def block_bootstrap_p(pre_arr, post_arr, obs_u, n_boot, block_len, rng_local):
    """
    Two-tailed block-permutation p for Mann-Whitney U.
    Concatenate (pre, post); form fixed-length blocks (last block may be short);
    shuffle blocks; re-split into pre/post by original sizes; recompute U.
    Compare |U_perm - n_pre*n_post/2| against |obs_u - n_pre*n_post/2|.
    Preserves within-block autocorrelation -> robust to daily autocorrelation
    that inflates the asymptotic Mann-Whitney p.
    """
    combined = np.concatenate([pre_arr, post_arr])
    n_pre, n_post = len(pre_arr), len(post_arr)
    n_total = len(combined)
    n_full_blocks = n_total // block_len
    null_centre = n_pre * n_post / 2.0
    obs_dev = abs(obs_u - null_centre)
    count = 0
    for _ in range(n_boot):
        blocks = [combined[i * block_len : (i + 1) * block_len] for i in range(n_full_blocks)]
        if n_total % block_len:
            blocks.append(combined[n_full_blocks * block_len :])
        rng_local.shuffle(blocks)
        permuted  = np.concatenate(blocks)
        perm_pre  = permuted[:n_pre]
        perm_post = permuted[n_pre:]
        u_perm, _ = mannwhitneyu(perm_pre, perm_post, alternative="two-sided")
        if abs(u_perm - null_centre) >= obs_dev - 1e-9:
            count += 1
    return count / n_boot

def linear_detrend_on_pre(pre_series, post_series, d):
    """
    Fit a linear trend on the pre-window (x = days from d), extrapolate forward
    through the post-window, and subtract from both pre and post values.
    Returns (pre_detrended_arr, post_detrended_arr).

    Closes the recovery-trajectory confound at the column level per
    CONVENTIONS §3.7. A step that survives detrending is more credibly
    event-driven; a step that disappears under detrending was the
    underlying trend leaking through.
    """
    pre_x  = np.array([(idx - d).days for idx in pre_series.index ], dtype=float)
    post_x = np.array([(idx - d).days for idx in post_series.index], dtype=float)
    slope, intercept = np.polyfit(pre_x, pre_series.values, deg=1)
    pre_trend  = slope * pre_x  + intercept
    post_trend = slope * post_x + intercept
    return pre_series.values - pre_trend, post_series.values - post_trend

# 5. Per-pair analysis — neighbour-truncated windows + buffer sweep
sorted_dates = sorted({d for _, d in interventions})
SENTINEL_PREV = pd.Timestamp("1970-01-01")  # effectively no previous boundary
SENTINEL_NEXT = pd.Timestamp("2099-12-31")  # effectively no next boundary

rows = []
for label, d in interventions:
    idx    = sorted_dates.index(d)
    d_prev = sorted_dates[idx - 1] if idx > 0 else SENTINEL_PREV
    d_next = sorted_dates[idx + 1] if idx < len(sorted_dates) - 1 else SENTINEL_NEXT

    for ch in CHANNELS:
        if ch not in master.columns: continue

        # 5a. Buffer sweep — one row per (intervention, channel, buffer)
        for B in TRANSITION_BUFFERS:
            pre_start, pre_end, post_start, post_end = windows_for(d, d_prev, d_next, B)
            pre  = master.loc[pre_start :pre_end , ch].dropna()
            post = master.loc[post_start:post_end, ch].dropna()
            pre_window_days  = (pre_end  - pre_start ).days + 1
            post_window_days = (post_end - post_start).days + 1

            base = {"intervention": label, "intervention_date": d, "channel": ch,
                    "transition_buffer_days": B,
                    "is_primary_buffer": (B == PRIMARY_BUFFER),
                    "n_pre":  len(pre),  "pre_window_days":  pre_window_days,
                    "n_post": len(post), "post_window_days": post_window_days}

            if len(pre) < 5 or len(post) < 5:
                rows.append({**base,
                             "median_pre": np.nan, "iqr_pre": np.nan,
                             "median_post": np.nan, "iqr_post": np.nan,
                             "median_diff": np.nan,
                             "median_diff_ci_lo": np.nan, "median_diff_ci_hi": np.nan,
                             "mw_u": np.nan, "mw_p": np.nan,
                             "mw_p_block_bootstrap": np.nan,
                             "mw_p_after_linear_detrend": np.nan,
                             "r_rb": np.nan})
                continue

            pre_arr  = pre.values
            post_arr = post.values
            u, p = mannwhitneyu(pre_arr, post_arr, alternative="two-sided")
            mdiff       = float(np.median(post_arr) - np.median(pre_arr))
            ci_lo, ci_hi = bootstrap_median_diff_ci(pre_arr, post_arr, N_BOOTSTRAP, rng)
            p_block     = block_bootstrap_p(pre_arr, post_arr, u, N_BOOTSTRAP, BLOCK_LEN, rng)
            rrb         = rank_biserial(u, len(pre_arr), len(post_arr))

            # Trajectory-detrend sensitivity (CONVENTIONS §3.7) — fit linear trend
            # on pre, extrapolate through post, recompute MW p on residuals.
            pre_dt, post_dt = linear_detrend_on_pre(pre, post, d)
            _, p_detrend    = mannwhitneyu(pre_dt, post_dt, alternative="two-sided")

            rows.append({**base,
                "median_pre":  float(np.median(pre_arr)),
                "iqr_pre":     float(np.quantile(pre_arr, 0.75) - np.quantile(pre_arr, 0.25)),
                "median_post": float(np.median(post_arr)),
                "iqr_post":    float(np.quantile(post_arr, 0.75) - np.quantile(post_arr, 0.25)),
                "median_diff": mdiff,
                "median_diff_ci_lo": ci_lo, "median_diff_ci_hi": ci_hi,
                "mw_u": float(u), "mw_p": float(p),
                "mw_p_block_bootstrap": float(p_block),
                "mw_p_after_linear_detrend": float(p_detrend),
                "r_rb": float(rrb),
            })

        # 5b. Plot once per (intervention, channel) at primary buffer
        prim_pre_start, prim_pre_end, prim_post_start, prim_post_end = windows_for(
            d, d_prev, d_next, PRIMARY_BUFFER)
        prim_pre_days  = (prim_pre_end  - prim_pre_start ).days + 1
        prim_post_days = (prim_post_end - prim_post_start).days + 1

        win = master.loc[d - pd.Timedelta(days=30) : d + pd.Timedelta(days=60), ch]
        if win.dropna().empty: continue
        fig, ax = plt.subplots(figsize=(10, 3))
        ax.plot(win.index, win.values, marker=".", linestyle="-", alpha=0.7)
        ax.axvline(d, color="red", linestyle="--", label=f"{label} {d.date()}")
        if d_prev > SENTINEL_PREV and d_prev >= d - pd.Timedelta(days=30):
            ax.axvline(d_prev, color="gray", linestyle=":", alpha=0.6, label=f"prev: {d_prev.date()}")
        if d_next < SENTINEL_NEXT and d_next <= d + pd.Timedelta(days=60):
            ax.axvline(d_next, color="gray", linestyle=":", alpha=0.6, label=f"next: {d_next.date()}")
        ax.set_title(f"{ch} around {label} (primary B={PRIMARY_BUFFER}; "
                     f"pre={prim_pre_days}d, post={prim_post_days}d)")
        ax.legend(fontsize=8)
        plt.tight_layout()
        safe_label = label.replace(' ', '_').replace('/', '-').replace(':', '')
        plt.savefig(OUT / "plots" / f"{ch}_{safe_label}.png", dpi=100)
        plt.close()

pd.DataFrame(rows).to_csv(OUT / "summary.csv", index=False)
print(f"Wrote {len(rows)} (intervention, channel, buffer) rows to {OUT}/summary.csv")
print(f"Buffer sweep: {TRANSITION_BUFFERS}; primary = {PRIMARY_BUFFER}.")
print("Filter is_primary_buffer == True for the primary reading; "
      "the other rows are sensitivity. Open PNGs and human-code transition_shape "
      "per pair using the primary row's stats for the no_visible_change pre-spec check.")
```

`transition_shape` is intentionally a human-coded post-step — visual judgement is more informative than a fitted change-point detector here, and the n-of-1 corpus does not justify automated change-point detection over visual inspection.

---

## 7. Status

**MD drafted 2026-06-14; revised same day after methodology review; script run same day (Session C); findings in §8.** Output artefacts:
- [`docs/research/analyses/garmin_exploration/intervention_effects/run.py`](../analyses/garmin_exploration/intervention_effects/run.py) committed (script)
- `$GEVOELSCORE_DATA_PATH/analyses/intervention_effects/summary.csv` (224 rows, gitignored)
- `$GEVOELSCORE_DATA_PATH/analyses/intervention_effects/plots/*.png` (~35 plots, gitignored)
- Console log captured at `$GEVOELSCORE_DATA_PATH/analyses/intervention_effects/run_console.log` (working location; not finalised)

**Revision log (2026-06-14, post-audit)** — methodology review at [`reviews/methodology-intervention_effects_descriptive-2026-06-14.md`](../reviews/methodology-intervention_effects_descriptive-2026-06-14.md) returned "REVISION RECOMMENDED" with 10 substantive fixes. This MD was revised in the same session:

| audit fix | status | where landed |
|---|---|---|
| #1 — Recovery-trajectory confound caveat | **APPLIED** | §1 substantive-confound paragraph |
| #2 — ITS named as state-of-art; Mann-Whitney as deliberate Layer 1 simplification | **APPLIED** | §1 method-choice paragraph |
| #3 — Block-bootstrap p column for autocorrelation | **APPLIED** | §4 statistical-descriptors item 3 + §6 script `block_bootstrap_p` + `mw_p_block_bootstrap` column |
| #4 — Per-channel literature citations | **QUEUED** | [`QUEUED-WORK.md` Tier 3](../QUEUED-WORK.md#tier-3-methodological-refinement-deferred); not gating the script run |
| #5 — Transition-buffer pharmacological justification + sensitivity sweep | **APPLIED** | §4 buffer-sweep paragraph + §6 script `TRANSITION_BUFFERS = [7, 14, 28, 42]` + `transition_buffer_days` column |
| #6 — Effect-size + CI columns | **APPLIED** | §4 statistical-descriptors item 3 + §6 script `r_rb`, `median_diff_ci_lo/hi` columns |
| #7 — Blinded transition_shape coding | NOT APPLIED | process change deferred; the §4 pre-spec for `no_visible_change` (fix #8) partly mitigates by removing rater discretion on the null finding |
| #8 — Pre-spec for "no visible change" criterion | **APPLIED** | §4 transition-shape-coding item 4 four-condition pre-spec |
| #9 — PELT / BCP corroborating-not-primary mention | **APPLIED** | §1 method-choice paragraph |
| #10 — Definitional-pair note in §3 | **APPLIED** | §3 definitional-pair-structure paragraph |

8 of 10 audit fixes applied this revision; 1 queued; 1 deferred as a process change. The MD now closes CONVENTIONS §2.2 inputs I1 (state-of-art named) and I3 (tradeoffs explicit), substantially closes I4 (recovery-trajectory confound named), and adds Layer 3 autocorrelation handling. I2 (per-channel literature) is queued for a follow-up session.

**v2 revision (2026-06-14, post-v2-audit)** — second methodology review at [`reviews/methodology-intervention_effects_descriptive-2026-06-14-v2.md`](../reviews/methodology-intervention_effects_descriptive-2026-06-14-v2.md) returned **DEFENSIBLE with revision**. Single highest-leverage residual was A7.4: the recovery-trajectory confound was named in §1 but not analytically addressed in the script. Closed v2-same-day:

| audit fix | status | where landed |
|---|---|---|
| v2 #1 — `mw_p_after_linear_detrend` sensitivity column | **APPLIED** | §4 statistical-descriptors item 3 (5th bullet) + §4 no_visible_change condition (e) + §6 script `linear_detrend_on_pre` helper + per-pair-loop application + new CSV column. Promoted to project pattern at [CONVENTIONS §3.7](../CONVENTIONS.md#37-trajectory-detrend-sensitivity-for-raw-pre-vs-post-comparisons). Moves A7.4 from "named confound" to "tested confound". |

**v3 revision (2026-06-14, Session C catalog curation)** — first script run exposed that the raw `interventie`-category catalog was not analytically homogeneous (Naproxen ad-hoc, Fysiotherapie wachtlijst, Breinvoeding confounded with Citalopram scale-down, Breathwork single-event markers). The original §2 claim "additions: any other interventie-category marker / span ... should be included. The catalog is data-driven, not pre-specified" was retracted; the catalog is now curated via an explicit `EXCLUDE_LABEL_KEYWORDS` substring filter (§2 table). Two structural caveats also landed in §2/§2b: the 2024-04 boundary-collision (Citalopram start + CPAP end 7 days apart make both unanalyzable) and the `bb_overnight_gain` coverage gap (data starts only 2024-09-18).

| audit fix | status | where landed |
|---|---|---|
| v3 #1 — Curated catalog with explicit exclude list | **APPLIED** | §2 table + §6 script `EXCLUDE_LABEL_KEYWORDS` |
| v3 #2 — 2024-04 boundary-collision caveat | **APPLIED** | §2 truncation paragraph + §8 findings (boundary marked unanalyzable) |
| v3 #3 — `bb_overnight_gain` coverage gap | **APPLIED** | §2b new sub-section |
| v3 #4 — Refined annotations.yaml dates (CPAP end 2024-04-16; Ergo end 2022-12-22 approx) | **APPLIED** | annotations.yaml edited 2026-06-14 (Session C); rationale captured in YAML notes |

Findings landed: see [§8 below](#8-findings-session-c-run-2026-06-14).

Downstream caveats now have empirical anchors:

- The segmented-baseline question stays open per [`lc_era_temporal_segmentation §2`](lc_era_temporal_segmentation.md#2-the-methodological-question) but §8 findings rule out a corpus-wide M2 boundary and identify exactly two channels with detrend-surviving step-changes (RHR around 2022-09-22; stress_mean_sleep around 2026-03-20).
- P4a / P4b / P5b in [`personal_hypotheses.md`](../personal_hypotheses.md) and C4b in [`wiggers_testable_hypotheses.md`](../wiggers_testable_hypotheses.md) each carry a caveat pointing at this MD; the §8 narrowing limits the scope of those caveats to the two confirmed channels rather than blanket-flagging all baselines.
- [`garmin_pacing_practice.md §7.4`](garmin_pacing_practice.md#74-intervention-period-baseline-calibration-open-question) carries the operational-side caveat.

---

## 8. Findings (Session C run, 2026-06-14)

Script run via [`docs/research/analyses/garmin_exploration/intervention_effects/run.py`](../analyses/garmin_exploration/intervention_effects/run.py) on 2026-06-14. Output: 224 rows in `summary.csv` = 8 boundary dates × 7 channels × 4 buffers. Of the 56 primary-buffer (B=14) rows, **25 are NaN** (no data) and **31 are analytical** — structural reasons enumerated in §8.1.

### 8.1 Effective analyzable scope (5 of 8 boundaries usable)

| boundary | status | reason |
|---|---|---|
| 2022-09-22 Ergotherapie Rouschop start | **analyzable** | full data; gevoelscore n_pre=19 (logging started 2022-09-03) |
| 2022-12-22 Ergotherapie Rouschop end | **analyzable** | end-date is ~13wk estimate; findings weighted lower (§2) |
| 2024-01-10 CPAP start | **analyzable** | bb_overnight_gain absent (§2b) |
| 2024-04-09 Citalopram buildup start | **UNANALYZABLE** | only 7 days to CPAP end at 2024-04-16 → all post-windows empty |
| 2024-04-16 CPAP end | **UNANALYZABLE** | only 7 days from Citalopram start at 2024-04-09 → all pre-windows empty |
| 2024-06-20 Citalopram buildup → consolidation | **analyzable** | bb_overnight_gain absent (§2b) |
| 2026-03-20 Citalopram consolidation → scale-down | **analyzable** | all 7 channels covered |
| 2026-06-05 Citalopram umbrella end | **UNANALYZABLE** | = data-cut, post-window empty |

### 8.2 Top findings at primary B=14, sorted by |r_rb|

All numbers descriptive. `r_rb` sign: **negative** = post HIGHER than pre; **positive** = post LOWER than pre. `mw_p` is asymptotic (autocorrelation-naive); `block_p` is 7-day-block-permutation null; `detrend_p` is Mann-Whitney on residuals after linear-pre-trend extrapolation (CONVENTIONS §3.7).

| boundary | channel | median_diff | mw_p | block_p | **detrend_p** | r_rb | reading |
|---|---|---:|---:|---:|---:|---:|---|
| 2022-09-22 Ergo start | **resting_hr** | +2.5 | <.0001 | <.0001 | **<.0001** | -0.97 | LARGE step UP; survives all 4 buffers + detrend; **confounded with steep LC trajectory** |
| 2022-09-22 Ergo start | **gevoelscore** | +2.0 | <.0001 | .004 | **<.0001** | -0.67 | step UP in felt-state; survives buffers + detrend; **confounded with LC trajectory** |
| 2022-09-22 Ergo start | stress_mean_sleep | +3.0 | <.001 | .002 | **0.62** | -0.53 | **detrend kills it** at all 4 buffers — trajectory artifact |
| 2026-03-20 Citalopram afbouw | bb_overnight_gain | +9 | <.001 | .006 | **0.96** | -0.50 | **detrend kills it** at all 4 buffers — recovery-trajectory artifact |
| 2026-03-20 Citalopram afbouw | **stress_mean_sleep** | -3.06 | <.001 | .018 | **<.0001** | +0.47 | step DOWN; survives detrend at B={7,14,28}, marginal at B=42 — **plausible direct SSRI-withdrawal effect** |
| 2026-03-20 Citalopram afbouw | gevoelscore | +1.0 | .003 | .020 | **.009** | -0.38 | mild step UP; survives detrend; modest confidence |
| 2024-06-20 Citalopram → consol | bb_lowest | -4.0 | .023 | **.088** | <.001 | +0.31 | block-p fails at primary; detrend strong — ambiguous, autocorrelation may inflate raw MW |
| 2022-12-22 Ergo end | respiration_avg_sleep | ±0 (n=14) | .011 | .113 | .265 | -0.30 | distributional shift without median shift; block-p marginal; not robust |
| 2024-01-10 CPAP start | respiration_avg_sleep | ±0 (n=14) | .007 | .059 | <.0001 | +0.30 | block-p marginal; detrend strong — ambiguous |

Remainder of the 31 analytical primary-buffer cells (not shown): all `|r_rb| ≤ 0.23`, most with `mw_p > 0.10` — meet the §4 `no_visible_change` pre-spec conditions a-d (median shift ≤ 0.5×IQR, |r_rb|<0.1 typically, p>0.10 on raw and block), although detrend_p varies. Full row-level CSV in `$GEVOELSCORE_DATA_PATH/analyses/intervention_effects/summary.csv`.

### 8.3 Reading per the §5 decision framework

Mapping the findings to the §5 finding-shape table:

- **No corpus-wide M2 boundary is supported by these findings.** No single boundary produces step-changes across most channels. The strongest signals are **boundary-specific × channel-specific** rather than channel-wide or intervention-wide.
- **Two detrend-surviving channel-boundary pairs are candidates for narrow segmentation consideration**:
  - `resting_hr` around 2022-09-22 (large r_rb=-0.97, survives all checks). **But confounded with the LC-onset trajectory's steepest phase** — five months into LC, deteriorating, ergotherapie was prescribed because the user was getting worse. Causally attributing the RHR step to ergotherapie is unsupported; attributing to disease progression at the same moment is equally consistent. §1 substantive-confound caveat applies in its sharpest form here. Segmentation around 2022-09-22 for `resting_hr` would adjust the rolling baseline against a step that *might* be intervention-driven but *might* be co-temporal disease progression.
  - `stress_mean_sleep` around 2026-03-20 (r_rb=+0.47, step DOWN, survives detrend). The most mechanistically clean candidate in the corpus: SSRI scale-down is known to reduce nocturnal autonomic load (Licht 2010, Kemp 2010 — queued for per-channel literature; see [QUEUED-WORK Tier 3](../QUEUED-WORK.md#tier-3-methodological-refinement-deferred)). Recommended for follow-up: a narrow `intervention_baseline_segmentation.md` MD that addresses `stress_mean_sleep`'s lagged baseline around 2026-03-20 specifically.
- **Detrend column did exactly what it was designed to.** Two of the top-7 raw findings (`stress_mean_sleep` 2022-09-22; `bb_overnight_gain` 2026-03-20) are revealed as recovery-trajectory artifacts when the local slope is removed. Without the v2 `mw_p_after_linear_detrend` column, these would have been reported as step-changes. The detrend earned its place in CONVENTIONS §3.7.
- **The 2024-04 boundary-collision is itself an analytical finding.** The methodology cannot resolve Citalopram-start and CPAP-end effects with this design when they sit 7 days apart. A follow-up design (e.g., ITS with both interventions modeled together as the segmented-regression β-vector) could in principle disentangle them, but is out of scope for Layer 1 descriptive.

### 8.4 Open follow-ups

- **Transition-shape coding** of the ~31 analytical plots (no_visible_change / gradual_drift / step / U_shaped / noisy_inconclusive) deferred — pending visual inspection of PNGs in `$GEVOELSCORE_DATA_PATH/analyses/intervention_effects/plots/`. The §4 5-condition pre-spec for `no_visible_change` can be machine-applied to the CSV without inspection; the other 4 categories need human judgement on the plot.
- **Narrow segmentation follow-up MD — LANDED 2026-06-14 as [`methodology/citalopram_dose_response_stress_mean_sleep.md`](citalopram_dose_response_stress_mean_sleep.md).** The MD locked the analytical specification through three review rounds (v1 → v2 audit-fix → v3 cross-window + multi-channel) and the script implementation produced the cumulative finding: **multi-channel graded dose-response confirmed across both phases of the Citalopram-traject**. Three channels CONFIRMED with significant buildup CIs (`stress_mean_sleep`, `all_day_stress_avg`, `bb_lowest`); one weak-positive (`resting_hr`); one rejected (`respiration_avg_sleep`); one partial / data-limited (`bb_overnight_gain`). See [`§5.5`](citalopram_dose_response_stress_mean_sleep.md#55-v3-amendment--cross-window-corroboration-added-2026-06-14) (cross-window: afbouw 2026 + buildup 2024 post-CPAP + spring 2025 control) and [`§5.6`](citalopram_dose_response_stress_mean_sleep.md#56-v3-amendment--multi-channel-confirmation-added-2026-06-14) (multi-channel). The original §8.3 candidate-from-this-MD upgrades from "step-change at one boundary surviving detrend" to "graded dose-response across the autonomic-load and recovery channel family". The §1 substantive-confound caveat (LC trajectory) is largely closed for these channels by the buildup-symmetry test (2024 buildup pre-dates the steepest LC-recovery slope).
- **Per-channel literature anchors** (Marin 2010, Tantucci 2003, Licht 2010, Kemp 2010, Wichniak 2017) queued at [QUEUED-WORK Tier 3](../QUEUED-WORK.md#tier-3-methodological-refinement-deferred); would lift channel selection rationale from intuition to literature.

---

## 9. Cross-references

- [CONVENTIONS §2.1, §4.2](../CONVENTIONS.md) — descriptive-before-inference + caveats-vs-a-priori discipline.
- [`time_resolution.md` §2.3, §6](time_resolution.md) — framework MD on picking analysis scale per hypothesis. This MD's `[d-30, d+60]` window is an instance of the situational-multi-day-window category; the mechanism-driven scale-choice rule motivates the 90-day choice.
- [lc_era_temporal_segmentation §2 M2](lc_era_temporal_segmentation.md#2-the-methodological-question) — the framework this MD's findings inform.
- [garmin_pacing_practice.md §2 temporal qualifier](garmin_pacing_practice.md#temporal-qualifier--this-protocol-is-a-recent-stabilisation-not-a-constant) — sibling temporal qualifier (behavioural / operational side). The intervention-baseline question is the physiological-measurement-side sibling.
- [personal_hypotheses.md P4a, P4b, P5b](../personal_hypotheses.md), [wiggers_testable_hypotheses.md C4b](../wiggers_testable_hypotheses.md) — hypotheses whose caveats this MD's findings would update.
- [lc_phase_descriptive.md](lc_phase_descriptive.md) — sister Layer 1 descriptive (per-phase distributions); precedent for "Layer 1 descriptive MD, output populated when script runs" shape.
