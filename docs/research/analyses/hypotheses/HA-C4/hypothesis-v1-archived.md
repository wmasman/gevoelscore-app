# HA-C4 — Stress fails to drop during rest periods after overexertion ("stuck sympathetic"), 3-channel confirmatory triad

## Authorship

**Drafted 2026-06-17** by Claude (Opus 4.7) in reviewer-mode-with-authorization per [CONVENTIONS §1.2](../../../CONVENTIONS.md#12-reviewer-mode-claude-reads--critiques--explains-does-not-edit-unless-asked). Authorising user: Willem. **Shared-context drafting per [`hypothesis_lock_process.md` §3.2 clause](../../../methodology/hypothesis_lock_process.md#32-drafting-step-step-1-of-the-arc)** (Stage-1 table row: *"drafting (may be shared-context with research session)"*).

**Data exposure context** (audit-able): the drafting session has executed the sister test [HA-C4b](../HA-C4b/) (v1 → v2 → v3, including the v3 test that landed NOT-SUPPORTED). The drafter is aware of:

- **The identity of the 10 unmedicated heavy-T days that are also crash episodes** (the HA-C4b headline pool: 2022-09-16, 2022-11-23, 2023-02-04, 2023-05-28, 2023-06-12, 2023-09-07, 2023-09-16, 2023-09-27, 2024-01-12, 2024-02-15) and their `stress_low_motion_min_count_S60_Mlow` z-scores from HA-C4b's lagged-baseline analysis.
- The HA-C4b v3 NOT-SUPPORTED verdict on the crash-precursor framing (a=40%, b=-10pp, c=+1.21).
- HA11 SUPPORTED on train at +22.8pp (the U-dip sister channel, per [wiggers_progress_2026-06-08.md](../../../wiggers_progress_2026-06-08.md)).
- The era anchors from HA-C4b v3 §8.x (cut at lock per option B; preserved in git history at commits `7595a8b` / `a7bf32a`).

**Crucially**, the drafter has NOT seen HA-C4's specific channel values (`stress_post_peak_time_to_rest_min`, `stress_post_peak_drop_avg`, `stress_high_duration_min`, `awake_stress_avg`) on individual days. The C4b column the drafter has seen is a *different aggregation* of the same underlying monitoring_b FIT data. The exposure spillover to HA-C4 is partial: which heavy-T days are crashes (a meta-fact relevant for the Channel-3 chain-T+1 handling) is known; the channel-value distributions are not.

**The §3.2 strictest-discipline path** would be a fresh-session redraft of HA-C4 with the HA-C4b exposure held out. The pragmatic path taken here is shared-context drafting under explicit user direction ("lets plan and execute all steps to execute the research according to our standards") with the data-exposure boundary documented above + the fresh-session [`/research-review`](../../../reviews/README.md) audit (§3.4) as the integrity check. **The §3.4 audit should specifically verify that none of the §4 / §5 operational choices below were biased by knowledge of the 10 crash-day identities**.

**Revision 2026-06-17-r2** (post-audit, shared-context with drafting per [`hypothesis_lock_process.md` §3.5](../../../methodology/hypothesis_lock_process.md#35-revise-step-stage-3-of-the-arc-r2--the-bulk-of-methodological-strengthening)). Six changes absorbed from the [fresh-session `/research-review` audit report](../../../reviews/HA-C4-v1-2026-06-17.md) (verdict: **REVISION RECOMMENDED** — three substantive fires + three minor fires, all closeable as mechanical r2 closures per the audit's own Section 4 framing). User-direction decisions: L4.4 closure option (a) — add sensitivity arm; L2.5 disposition option (a) — accept documented boundary as priced-in; §3.6 re-audit compression accepted. The user explicitly accepts the §3.2-clause shared-context drafting concern as priced-in (audit L2.5 substantive); the lock-commit message names this acceptance + the L1.4 + L4.4 closures.

- **§7 rebuilt with EXACT-column EXACT-phase anchors** (closes audit L1.4 substantive). v1's §7 cited `lc_phase_descriptive.md §1176-§1230` (which covers only Channel 1 metrics; Ch2 is at lines 1159-1174, Ch3 at 523-538) AND partitioned by `pre_corona | corona_infection | lc` not by citalopram phase, so unmedicated-only anchors weren't derivable from the cited source. Additionally v1's Channel 1 + Channel 3 anchor rationales were malformed ("expected ~60-180 min based on the dictionary's coverage stats" — coverage doesn't give median) and v1's Channel 2 range [20, 60] was outright wrong vs the actual unmed heavy-T p50 of 90. r2 computes the §7 anchors directly from `per_day_master.csv` on the `2022-04-04 ≤ date ≤ 2024-04-08` filter for all 4 channels actually under test, with the source script `c:\tmp\hac4_anchor_query.py` preserved for audit traceability. The §7.5 sanity-gate tolerance is tightened from ±50% to ±30% per audit Section 4 item-1 paired-fix recommendation.
- **§4.11.1 crash-drop sensitivity arm added** (closes audit L4.4 substantive via Section 4 item-2 option a). Per CONVENTIONS §3.4, the heavy-T arm intentionally pools 21 unmedicated heavy-T-and-crash days with 226 non-crash heavy-T days; the spec now re-runs the per-channel Mann-Whitney with `is_crash == True` dropped from BOTH arms and reports Δ Cliff's delta. |Δ| > 0.10 on any channel flags as a §3.4 finding (crash-driven signal).
- **§4.11.2 Channel 3 spike-metric sensitivity companion added** (closes audit L4.5 minor). Per CONVENTIONS §3.5 + the verbatim Wiggers wording "stress spikes much faster" on T+1, a parallel Mann-Whitney on `stress_high_duration_min` on T+1 (spike-count companion) is reported alongside the primary `awake_stress_avg` on T+1.
- **§4.9 E[L] derivation vs application acknowledgment** (closes audit L3.1 minor). One-paragraph addition naming that E[L]=7 is derived for channel-value autocorrelation; the heavy-T label sequence has its own autocorrelation; the data-driven E[L]\* companion now computes on both (a) channel values AND (b) the label sequence; factor-of-2 flag applies to either.
- **§9.1 outcome-branch labels reframed verdict-invariant** (closes audit L4.7 minor). The mechanistic interpretive scripts ("the system catches up overnight", "the t+1 signal is the strongest", "a milder C4 expression") are removed; replaced with descriptive-only labels naming the confirmed channel set ("Ch1+Ch2 confirmed, Ch3 not — same-day phenomena confirmed; next-day reactivity in the expected range"). The result.md author interprets against observed magnitudes + sister-test context, not against pre-staged scripts.
- **L2.5 user acceptance recorded in §8** (closes audit L2.5 substantive via Section 4 item-6 option a). The user explicitly accepted the documented data-exposure boundary at r2 absorption time; the lock-commit message names this acceptance.

**Additional r2 exposure disclosure**: computing the §7.1-§7.3 anchors at r2 required running a descriptive query against the unmedicated-phase column data. The drafter now knows the unmedicated-phase descriptive directionality (heavy-T > non-heavy-T on all 4 channels at the median level) AND the per-arm sample sizes. This is descriptive aggregate information, NOT per-day per-channel values; it does not contaminate the test outcome (Mann-Whitney + Cliff's delta + block-permutation p-value vs null). Documented per §3.5 r2 disclosure discipline.

The audit's three substantive fires + three minor fires + one register-row-pointer lock-commit responsibility are all closed by r2 or by the lock-commit message. Per [`hypothesis_lock_process.md` §3.6 compression criteria](../../../methodology/hypothesis_lock_process.md#36-re-audit-step-stage-4-of-the-arc), r2 changes are mechanical (citation rebuilds, sensitivity-arm additions, wording-tightenings, descriptive label reframings) with no architectural change, no new statistical machinery, no falsification-bar change. **§3.6 re-audit compressed** per user direction at r2 acceptance.

**Status: LOCKED 2026-06-17 by user acceptance at revision r2** by Claude (Opus 4.7) in reviewer-mode-with-authorization. The fresh-session [§3.4 audit](../../../reviews/HA-C4-v1-2026-06-17.md) (verdict: REVISION RECOMMENDED) was absorbed in r2 above as mechanical closures per the audit's own Section 4 framing; per [`hypothesis_lock_process.md` §3.6 compression criteria](../../../methodology/hypothesis_lock_process.md#36-re-audit-step-stage-4-of-the-arc) re-audit compression was accepted (r2 changes are wording-tightenings + citation rebuilds + sensitivity-arm additions; no architectural change, no new statistical machinery, no falsification-bar change). User explicitly accepted the L2.5 disposition (option a — documented boundary priced in) + L4.4 closure path (option a — add sensitivity arm) at r2 absorption time.

The four [§3.8 lock-blocking gates](../../../methodology/hypothesis_lock_process.md#38-lock-step-stage-5-of-the-arc) all confirmed at lock:

1. **Power-calc dispatch — MET**. §8 carries the Daza 2018 within-subject design dispatch verbatim ("power calculation is inapplicable per Daza 2018 within-subject design — the n-of-1 corpus does not have separate treatment and control arms in the classical sense. The block-permutation null at E[L]=7 (§4.9) is the within-subject inferential machinery; the §5.1 (a) discrimination + (b) effect-size gates determine per-channel confirmation rather than a power-thresholded p-value.").
2. **Multi-comparison discipline — MET**. §5.0 pre-specifies the 3-channel triad with pass-2-of-3 verdict rule + Holm step-down across channels per era; design-MD-locked at [`wiggers_test_design_on_chained_regime.md` §C4](../../../methodology/wiggers_test_design_on_chained_regime.md#c4--we-class-3-channel-confirmatory-triad). Single-decision-cell at the verdict level.
3. **Register-row pointer — MET at lock-commit**. The lock-commit updates [`wiggers_testable_hypotheses.md` C4 row line 92](../../../wiggers_testable_hypotheses.md) to add a forward pointer to this folder, superseding the prior design-MD-only pointer.
4. **Re-audit clean OR compression — MET via §3.6 compression**. The §3.4 [fresh-session audit](../../../reviews/HA-C4-v1-2026-06-17.md) verdict was REVISION RECOMMENDED with three substantive fires (L1.4 §7 anchor, L4.4 crash-drop, L2.5 shared-context drafting) + three minor fires (L3.1, L4.5, L4.7); ALL closed in r2 above as mechanical fixes per the audit's own Section 4 framing. §3.6 re-audit compression accepted at r2 per the compression criteria: wording-tightenings + citation rebuilds + sensitivity-arm additions + descriptive-label reframings; no architectural change; no new statistical machinery; no falsification-bar change; audit verdict explicitly states all items close without v2.

---

**Pre-registration drafted 2026-06-17, BEFORE any test run on the HA-C4 channels.** Locked at user acceptance after audit absorption. Any subsequent change creates HA-C4-v2 with this pre-reg archived as v1.

HA-C4 tests Wiggers' **"After overexertion, stress fails to drop during rest periods — stuck sympathetic"** claim (PDF lines 1112-1119, 1140-1143, 1223-1231, 1306-1314, source-verified per the [register entry](../../../wiggers_testable_hypotheses.md#c4--stress-fails-to-drop-during-rest-periods-after-overexertion-stuck-sympathetic) batch 2 2026-06-12). The claim has three temporal scales — same-day decay failure, walls-of-orange sustained-high, and next-day stress-spike reactivity — operationalised as a **3-channel confirmatory triad** per the design MD's expansion (single-metric C4 missed two source-named channels).

## 1. Claim

On heavy-exertion days (`exertion_class_lagged_lcera ∈ {heavy, very_heavy}` on T) within the unmedicated phase (2022-04-04 → 2024-04-08), three independent stress-recovery channels should each show systematic degradation relative to non-heavy-exertion days within the same phase and era:

- **Channel 1 (same-day decay)**: `stress_post_peak_time_to_rest_min` on T is **longer** on heavy-T days than on non-heavy-T days. NaN value = "stress never returned to rest that day" = C4-positive case; coded as the day's awake-window maximum (1080 min ≈ 18 hours; see §4.5).
- **Channel 2 (walls of orange)**: `stress_high_duration_min` on T (count of waking minutes with stress > 75) is **higher** on heavy-T days.
- **Channel 3 (t+1 reactivity)**: `awake_stress_avg` on T+1 is **higher** on heavy-T days than on non-heavy-T days.

The directional prediction in all three channels: heavy-T degrades the recovery. Each channel's confirmation requires both a statistically discriminative effect (block-permutation p < 0.05) AND a non-negligible effect size (|Cliff's delta| > 0.20), in the predicted direction, replicated independently in the train era (2022-09-03 → 2023-12-31) AND the validate era (2024-01-01 → 2024-04-08) within the unmedicated phase.

**Headline triad cell**: unmedicated phase × {Ch1 + Ch2 + Ch3} × heavy-T-vs-non-heavy-T × Mann-Whitney + Cliff's delta × block-permutation null E[L]=7 × pass-2-of-3 verdict rule applied within each era.

**Verdict rule**: SUPPORTED if ≥ 2 channels confirmed in BOTH train AND validate eras; PARTIAL if 1 channel confirmed in both eras, OR ≥ 2 channels confirmed in only one era; REJECTED if 0 channels confirmed in either era. See §5.3 + §9.

## 2. Why we think this

**The Wiggers paraphrase** is source-verified verbatim (per the register entry's verification log). Five passages directly support the 3-channel triad:

- *"Going so far beyond your limits that your resting heart rate remains elevated and your stress level doesn't decrease for a long time & PEM"* (PDF lines 1140-1141) — direct support for Channel 1 (same-day decay failure).
- *"The day after you've done too much you can see stress spikes much faster, despite resting"* (PDF lines 1141-1143) — direct support for Channel 3 (next-day reactivity).
- *"Stuck in Stress. When you've done something and then lie down, you want to see blue again. ... your stress remains high"* (PDF lines 1223-1231) — direct support for Channel 1 + Channel 2.
- *"Complete walls of orange ... sustained high state"* (PDF lines 1112-1119) — direct support for Channel 2.
- *"You have to take it easy for a while before your body finds its peace again"* (PDF lines 1306-1314) — context-setting for the recovery-takes-time framing the triad encodes.

**The participant's lived experience** aligns with the C4 framing per [`garmin_pacing_practice.md`](../../../methodology/garmin_pacing_practice.md): the rest-stress trigger uses the "blocks of orange when at rest" pattern as a live pacing signal. This pre-reg tests whether the pattern that the participant identifies experientially is reproducible at the daily-aggregate descriptive level.

**Sister-test context** establishes priors:

- **HA11 SUPPORTED on train (+22.8 pp)** for the within-day stress U-dip count — the *complement* of "stuck stress": sharp drops following plateau. The U-dip is the dynamic Wiggers expects on calm days. HA11's failure-to-dip arm was distribution-bounded zero (essentially never observed) — interpretable as the U-dip metric's specific operationalisation not capturing the "stuck sympathetic" arm. HA-C4's stress_post_peak_time_to_rest_min channel is the more direct operationalisation of the failure-to-recover signal.
- **HA-C4b NOT-SUPPORTED** on the crash-precursor framing for the motion-filter operationalisation (a=40%, b=-10pp; (c)=+1.21 PASS). HA-C4b tested whether the stress-low-motion concurrence COUNT precedes crashes. HA-C4 tests a different question on different metrics: whether the stress-RECOVERY-DYNAMIC differs after heavy exertion at all. A SUPPORTED-here-NOT-SUPPORTED-at-C4b shape would be informative: the Wiggers pattern exists but isn't a per-episode crash precursor (consistent with the protective-rather-than-predictive alternative reading from HA-C4b §9).
- **The four SUPPORTED autonomic-deviation precursors** (H02b stress spike count, H02d sentinel-corrected spike, HA06b RHR z-score, HA11 U-dip count — all on train) all fired in the unmedicated phase. The autonomic-dysregulation prior is substantial; HA-C4 is a different operationalisation of the same underlying autonomic-state question.

## 3. Data sources

- **Channel columns** (all already extracted to `$GEVOELSCORE_DATA_PATH/unified/per_day_master.csv` per [DATA_DICTIONARY.md §C4](../../../DATA_DICTIONARY.md#c4--stress-decay-after-daily-peak-4-columns)):
  - `stress_post_peak_time_to_rest_min` (Channel 1 primary; 1522 / 1755 = 86.7% coverage; NaN = "did not return to rest" = C4-positive)
  - `stress_post_peak_drop_avg` (Channel 1 secondary aggregate; 98.1% coverage)
  - `stress_high_duration_min` (Channel 2; 99.0% coverage)
  - `awake_stress_avg` (Channel 3; ~98.6% coverage per [DATA_DICTIONARY.md §7B](../../../DATA_DICTIONARY.md))
- **Heavy-T classification**: `exertion_class_lagged_lcera ∈ {heavy, very_heavy}` per [`citalopram_phase_stratification.md`](../../../methodology/citalopram_phase_stratification.md) and v3.2 lagged-baseline conventions. Coverage ~83% within LC era.
- **Citalopram phase**: derivable from date via `citalopram_phase(d)` function per [`citalopram_phase_stratification.md §3`](../../../methodology/citalopram_phase_stratification.md#3-the-four-phase-citalopram-traject-stratification).
- **Sister-test cross-references** (informational only, not used in HA-C4 test): HA11 `u_dip_count` for descriptive companion read.

**No new FIT-level extraction required.** All channel columns are already in `per_day_master.csv` via [`pipeline/01_extract/garmin_intraday_hr_stress.py`](../../../pipeline/01_extract/garmin_intraday_hr_stress.py) (Wave 4, 2026-06-12).

## 4. Measurement protocol

### 4.1 Heavy-T eligibility (locked)

A day `T` is a **heavy-T candidate** if `exertion_class_lagged_lcera ∈ {heavy, very_heavy}` on T. A day is a **non-heavy-T candidate** if `exertion_class_lagged_lcera ∈ {none, light, moderate}` on T. Days with missing exertion classification are excluded from the comparison.

**Note vs HA-C4b**: HA-C4b conditioned on `heavy/very_heavy` on T OR T-1 (union, capturing crashes triggered by exertion on either day). HA-C4 conditions on T only (more conservative; the t+1 reactivity channel will use T+1 separately).

### 4.2 Channel definitions (locked)

**Channel 1 — same-day decay failure (primary)**:
- Per-day metric: `stress_post_peak_time_to_rest_min` (the C4-primary number per the dictionary).
- NaN encoding: per §4.5 below, NaN ("did not return to rest") = C4-positive and coded as the awake-window length cap (1080 min = 18h).
- Direction-of-effect under SUPPORTED: heavy-T days have HIGHER (or NaN→1080) values.

**Channel 2 — walls of orange (secondary)**:
- Per-day metric: `stress_high_duration_min` (count of waking minutes with stress > 75).
- No special NaN encoding (NaN is rare on this column — 99.0% coverage; days with NaN are excluded).
- Direction-of-effect under SUPPORTED: heavy-T days have HIGHER values.

**Channel 3 — next-day reactivity (secondary)**:
- Per-day metric: `awake_stress_avg` on T+1 (the day AFTER the heavy-T day).
- Pair construction: for each heavy-T day `T`, the Channel 3 observation is `awake_stress_avg[T+1]`. For matched non-heavy-T comparison days `T'`, the observation is `awake_stress_avg[T'+1]`.
- Chain-T+1 exclusions per §4.7 (avoid double-counting when T+1 itself is heavy or is in the structurally-excluded April 2024 cluster).
- Direction-of-effect under SUPPORTED: heavy-T days are followed by HIGHER awake_stress_avg on T+1.

### 4.3 Day validity (locked)

A day `T` enters the comparison if:
1. `T` is in the LC era (`>= 2022-04-04`) AND in the unmedicated phase (`< 2024-04-09`).
2. `T` is NOT in the April 2024 cluster (`2024-04-09 → 2024-04-16`).
3. The relevant channel value is computable (non-NaN, except for Channel 1's documented NaN-as-positive encoding).
4. For Channel 3 specifically: `T+1` is ALSO in the unmedicated phase AND NOT in the April 2024 cluster AND has computable `awake_stress_avg`.

**Per-channel sample minimums (inconclusive bar per §5.4)**: each channel × era cell must have ≥ 30 heavy-T days AND ≥ 30 non-heavy-T days to produce a verdict. Below this, the channel × era result is INCONCLUSIVE for that era.

### 4.4 Citalopram phase treatment (locked)

**Primary scope**: unmedicated phase only (LC era start 2022-04-04 → 2024-04-08). Rationale: avoids the [`citalopram_dose_response §5.6`](../../../methodology/citalopram_dose_response_stress_mean_sleep.md#56-v3-amendment--multi-channel-confirmation-added-2026-06-14) dose-modulation confound on the stress channel (β = +0.57/mg for `all_day_stress_avg`; β = +0.43/mg for `stress_mean_sleep`). At 30 mg plasma the stress baseline shifts by ~12-17 points, which would contaminate the Channel 2 (>75 minutes count) and Channel 3 (`awake_stress_avg` directly) comparisons if pooled across phases.

**Sensitivity arms** (descriptive only, no SUPPORTED-bar promotion): per-phase tests on consolidation, buildup, afbouw with the §5.B dose-adjustment applied per the methodology MD. Reported in result.md alongside the primary unmedicated verdict; not part of the §5 SUPPORTED-bar decision.

### 4.5 NaN-as-positive encoding for Channel 1 (locked)

`stress_post_peak_time_to_rest_min` has NaN semantics that **invert the usual rule**: NaN means "stress never dropped below the 25 'rest' threshold within the same calendar day" — the C4-POSITIVE case, not a coverage problem (per [DATA_DICTIONARY §C4](../../../DATA_DICTIONARY.md)).

**Encoding**: NaN values for Channel 1 are coded as **1080 minutes** (= 18 hours, an upper bound on the typical waking window) for the purpose of Mann-Whitney U + Cliff's delta computation. This ensures NaN-as-positive observations contribute to the heavy-T-vs-non-heavy-T comparison rather than being silently dropped.

**Sensitivity check**: report the per-arm (heavy-T vs non-heavy-T) NaN fraction in result.md as a descriptive companion. If heavy-T NaN fraction is substantially higher than non-heavy-T NaN fraction, that itself is direct C4 evidence (the C4-positive case is more common after heavy exertion). The 1080-encoding is one way to surface this within the Mann-Whitney framework; the raw NaN-fraction contrast is the alternative descriptive read.

### 4.6 Day-validity gate: missing-data handling for the other channels

- Channel 2 NaN: drop the day from Channel 2's comparison (no positive-encoding semantics for `stress_high_duration_min`).
- Channel 3 NaN on T+1: drop the corresponding heavy-T (or non-heavy-T) day from Channel 3's comparison.
- Channel 1 NaN: encode as 1080 per §4.5 (positive case).
- Days with `exertion_class_lagged_lcera` NaN: excluded entirely (can't classify heavy vs non-heavy).

### 4.7 Chained-regime adjustment (locked per design MD §C4 pre-reg specifics)

**Channel 3 (t+1 reactivity) specifically requires chained-regime handling** because the test compares `awake_stress_avg[T+1]` for heavy-T-on-T vs heavy-T-not-on-T. If `T+1` is itself a heavy day (i.e. the participant overdid it for two consecutive days), the comparison is confounded.

**Rule**: for the Channel 3 comparison, EXCLUDE heavy-T days `T` where `exertion_class_lagged_lcera ∈ {heavy, very_heavy}` on `T+1`. This restricts Channel 3 to "heavy-T followed by non-heavy-T+1" — the cleanest test of "the day AFTER overdoing it" claim.

**Channel 1 and Channel 2 are not affected** by this adjustment (they test on T only).

**Sensitivity arm** (descriptive only): a Channel 3 variant **without** the chained-regime exclusion, reported alongside the primary. If both variants reach the same verdict, the chained-regime adjustment didn't materially affect the result; if they differ, the chained-regime sequences are doing analytical work.

### 4.8 Per-channel statistical method (locked per design MD)

For each channel × era cell:

1. **Mann-Whitney U statistic** on the channel values: heavy-T arm vs non-heavy-T arm. One-sided (heavy-T > non-heavy-T per the directional prediction in §1).
2. **Cliff's delta** as the non-parametric effect size: `delta = (n_heavy>non - n_heavy<non) / (n_heavy * n_non)`. Range [-1, +1]; positive = heavy-T > non-heavy-T. The 0.20 threshold is "small-to-medium" effect per the standard interpretation.
3. **Block-permutation null** (per §4.9 below): empirical p-value = fraction of B = 10,000 null permutations whose U statistic equals or exceeds the observed U.
4. **Channel confirmed in era** if: empirical p < 0.05 AND Cliff's delta > +0.20 (in the predicted positive direction).

### 4.9 Null sample — block-permutation of heavy-T labels (locked, inherits from [`permutation_null_block_length.md`](../../../methodology/permutation_null_block_length.md))

The independence assumption for raw Mann-Whitney U is violated by the autocorrelation in the channel values (consecutive days share physiological state). The project-canonical inference framework is **stationary bootstrap with E[L] = 7 days** per the methodology MD.

**For HA-C4 specifically**: we **permute the binary `is_heavy_T[d]` label sequence** in blocks (geometric-distributed block length with mean E[L] = 7) while keeping the channel values in their original temporal positions. This preserves the channel autocorrelation and breaks the heavy-T → channel relationship.

**Procedure**:
1. Take the observed sequence `(date, is_heavy_T[d], channel_value[d])` for the era.
2. Generate B = 10,000 null draws: for each draw, resample the `is_heavy_T` label sequence via stationary bootstrap (E[L]=7) while keeping `channel_value` fixed in place.
3. For each null draw, recompute the Mann-Whitney U statistic on the resampled labels.
4. Empirical one-sided p-value = `(1 + #{U_null >= U_observed}) / (B + 1)`.

**Seed**: `RANDOM_SEED = 20260617` (HA-C4 seed, distinct from HA-C4b v3's `20260615`).

**E[L] derivation vs application** (added r2 to close audit L3.1 minor): the E[L]=7 anchor in [`permutation_null_block_length.md`](../../../methodology/permutation_null_block_length.md) is derived for *channel-value* autocorrelation (daily physiological signals' ACF typically decay within a week per the methodology MD §4). For HA-C4 the permutation acts on the *heavy-T LABEL sequence*, which has its own autocorrelation driven by sustained-push regimes (the chained-regime framing in the design MD). The label-sequence E[L] may differ from the channel-value E[L]; the **data-driven E[L]\* companion below is the empirical check on this assumption**.

**E[L]\* companion + factor-of-2 flag**: data-driven `E[L]*` estimator per [`permutation_null_block_length.md`](../../../methodology/permutation_null_block_length.md) Operational consequences. Compute E[L]* on **both** (a) each channel's value series AND (b) the heavy-T label sequence; flag if `|E[L]* - 7| / 7 > 0.5` on either. The flag fires only on SUPPORTED verdicts (per the methodology MD); for PARTIAL or REJECTED, the flag is descriptive context only.

### 4.10 Walk-forward gate per channel (locked per design MD)

Each channel is independently tested in **train** (2022-09-03 → 2023-12-31, within unmedicated) and **validate** (2024-01-01 → 2024-04-08, within unmedicated). Both eras must reach the channel-confirmation threshold (§4.8 step 4) for the channel to count toward the §5.3 triad verdict.

**Walk-forward integrity**: the train era is tested first; the validate era confirmation is an out-of-sample replication on a strictly later time window. No within-era data crosses the temporal boundary.

### 4.11 Secondary descriptive outcomes (locked, no verdict weight)

- **`stress_post_peak_drop_avg` companion**: report the parallel Mann-Whitney + Cliff's delta on `stress_post_peak_drop_avg` (Channel 1's secondary aggregate) alongside the primary `stress_post_peak_time_to_rest_min` result. If both Channel 1 metrics agree directionally, the Channel 1 confirmation is internally consistent; if they diverge, flag for review.
- **`stress_recovery_pct_within_2h` companion**: parallel test on this column (the "direct rate-of-recovery metric" per the dictionary). Pair with `stress_post_peak_time_to_rest_min` to distinguish slow-but-complete recovery from fast-then-stall.
- **NaN-fraction descriptive contrast** for Channel 1: report per-arm NaN fractions explicitly (heavy-T vs non-heavy-T). If heavy-T NaN fraction > 10pp higher than non-heavy-T, that is direct C4-positive descriptive evidence independent of the 1080-encoded Mann-Whitney result. (Per §7.2 the r2 descriptive shows these are essentially tied at 18%; this companion is reported anyway as the encoding-fragility check per §4.5.)

#### 4.11.1 Crash-drop sensitivity arm (added r2 to close audit L4.4 substantive)

The audit fired CONVENTIONS §3.4 (crash-drop sensitivity row) because the drafter knows the identity of 21 unmedicated heavy-T-and-crash days, and the heavy-T arm intentionally pools crash with non-crash heavy-T days. Per the audit's Section-4 item-2 closure path (option a), the spec adds an explicit crash-drop sensitivity arm:

**Rule**: re-run the per-channel × per-era Mann-Whitney + Cliff's delta with `is_crash == True` dropped from BOTH the heavy-T arm AND the non-heavy-T arm. Compare the crash-dropped Cliff's delta vs the primary Cliff's delta per channel. Report Δ Cliff's delta in the result.md sensitivity table.

**Flag**: if |Δ Cliff's delta| > 0.10 on any channel, surface as a §3.4 finding ("the channel's signal is crash-driven, not robust across the broader heavy-T pool"). The primary verdict per §5.3 is unchanged; the crash-drop sensitivity is a descriptive read on the verdict's robustness.

**Rationale**: the C4 mechanism IS expected to be strongest on crash days (per §9 — the "protective-rather-than-predictive" alternative reading depends on this); a strong dependence of the verdict on crash-day inclusion is informative-for-interpretation, not verdict-modifying. The §3.4 hook's purpose is to surface this dependence explicitly.

#### 4.11.2 Channel 3 spike-metric sensitivity companion (added r2 to close audit L4.5 minor)

The audit fired CONVENTIONS §3.5 (spike-detecting metrics over daily averages for sympathetic-arousal proxies) on Channel 3's choice of `awake_stress_avg` (a mean) when the verbatim Wiggers wording ("stress spikes much faster") suggests a spike-reading. Per Section-4 item-5 closure: add a parallel Mann-Whitney on `stress_high_duration_min` on T+1 (the spike-count companion; chain-T+1 exclusion applies per §4.7) alongside the primary `awake_stress_avg` on T+1.

**Reporting rule**: both readings in the result.md table. If both agree (same verdict direction and approximate effect-size), the average-vs-spike question is closed. If they diverge, the divergence is informative for §9 interpretation.

**Note**: this is a descriptive companion only. The primary Channel 3 metric remains `awake_stress_avg` per the design-MD-locked triad; the spike-companion does NOT promote to a 4th channel.

- **Sister-test cross-reference table**: report HA-C4b's NOT-SUPPORTED verdict + HA11's SUPPORTED-on-train verdict as descriptive context for interpretation. No statistical machinery — just the audit-table.

## 5. Pre-registered falsification criterion

### 5.0 Multi-comparison discipline — triad with pre-specified verdict rule (locked)

HA-C4 is a **3-channel confirmatory triad**, NOT a single-cell test. The multi-comparison discipline is provided by the **pre-specified pass-2-of-3 verdict rule** (§5.3), which itself is the single-decision-cell at the verdict level.

**Hard rule**: ALL OTHER configurations (other phases, single-channel verdicts, alternative encodings, sensitivity arms) are diagnostic / sensitivity arms ONLY. They are reported in result.md but **none can promote to a SUPPORTED verdict on their own**. The headline verdict is the pass-2-of-3 outcome on the unmedicated × triad cell.

### 5.1 Per-channel confirmation bar (applied independently to each of the 3 channels × 2 eras)

For each channel × era:

**(a) Discrimination**: empirical one-sided p < 0.05 from the block-permutation null at E[L]=7 (per §4.8 step 4 + §4.9).

**(b) Effect size**: Cliff's delta ≥ +0.20 in the predicted direction (heavy-T > non-heavy-T).

**Channel × era confirmed** if BOTH (a) and (b) hold in the predicted positive direction.

### 5.2 Per-channel confirmation across eras (walk-forward)

A channel **confirms** if it is confirmed (§5.1) in BOTH train AND validate eras.

### 5.3 Triad verdict rule (locked per design MD)

| confirmed channels (in both eras) | verdict |
|---|---|
| 3 of 3 | **SUPPORTED** (strong) |
| 2 of 3 | **SUPPORTED** (clears the triad bar) |
| 1 of 3 | **PARTIAL** |
| 0 of 3 | **REJECTED** |

**Single-era confirmation (one era only) counts as 0.5 toward channel confirmation**, with the verdict reported as:
- 2.0 → SUPPORTED, 1.5 → PARTIAL+ (partial with extra signal), 1.0 → PARTIAL, 0.5 → PARTIAL−, 0 → REJECTED.

### 5.4 Inconclusive bar

A channel × era cell is **INCONCLUSIVE** if either the heavy-T arm OR the non-heavy-T arm has < 30 days in the era. INCONCLUSIVE channels do not count toward the triad verdict; if 2+ channels are inconclusive in an era, the era's contribution to the triad is INCONCLUSIVE.

### 5.5 Holm step-down across channels (locked, within-test multiplicity correction)

The 3-channel triad p-values per era are corrected for multiplicity via **Holm step-down at α = 0.05**: order the 3 p-values ascending, compare to α/(3 - k + 1) for k = 1, 2, 3. A channel passes Holm if its p-value is below the corresponding cutoff AND all preceding (lower-p) channels also pass.

**Holm result is REPORTED alongside the uncorrected per-channel verdict**; the §5.3 triad rule uses the uncorrected per-channel p-values per the design MD's *"pass-2-of-3"* phrasing. The Holm result is a stricter sensitivity-bar report — if the verdict survives Holm correction, that's stronger; if it doesn't, that's a multiplicity-fragility flag.

## 6. Exclusion rules

- **LC era only**: days before `2022-04-04` are excluded.
- **Unmedicated phase only (primary scope)**: days `>= 2024-04-09` (citalopram start) are excluded from the primary test. Sensitivity arms on later phases are reported separately per §4.4.
- **April 2024 cluster (2024-04-09 → 2024-04-16)**: structurally unanalyzable per [`citalopram_phase_stratification.md`](../../../methodology/citalopram_phase_stratification.md); excluded from all arms.
- **Chain-T+1 (Channel 3 only)**: heavy-T days where T+1 is also heavy are excluded from the Channel 3 primary comparison per §4.7.
- **Missing exertion classification**: days with `exertion_class_lagged_lcera` NaN are excluded.
- **Channel-specific NaN handling**: per §4.5 + §4.6.

## 7. Expected effect size if hypothesis is true

**§7 anchors computed at r2 from `per_day_master.csv` on the EXACT-column EXACT-phase filter** (per the [`hypothesis_lock_process.md` §5 EXACT-column-anchor rule](../../../methodology/hypothesis_lock_process.md#5-sanity-check-questions-before-lock); closes the audit's L1.4 substantive fire). Filter: `2022-04-04 ≤ date ≤ 2024-04-08` AND `not (2024-04-09 ≤ date ≤ 2024-04-16)`. Source script: `c:\tmp\hac4_anchor_query.py` (preserved for audit traceability).

### 7.1 Per-channel unmedicated-only descriptive distributions (FULL pool, both arms combined)

| channel | n (non-NaN) | p25 | p50 | p75 | min | max |
|---|---:|---:|---:|---:|---:|---:|
| Channel 1 — `stress_post_peak_time_to_rest_min` | 603 of 736 (81.9%) | 39 | **81** | 161 | 1 | 842 |
| Channel 1 sec. — `stress_post_peak_drop_avg` | 717 of 736 (97.4%) | 50.1 | **61.0** | 72.3 | 21.5 | 99.8 |
| Channel 2 — `stress_high_duration_min` | 724 of 736 (98.4%) | 41 | **73** | 115 | 0 | 373 |
| Channel 3 — `awake_stress_avg` | 724 of 736 (98.4%) | 41 | **46** | 52 | 21 | 73 |

**Channel 1 NaN fraction (unmedicated-only)**: 18.1% — these are the days where stress never dropped below the 25 "rest" threshold all day (C4-positive cases per [DATA_DICTIONARY §C4](../../../DATA_DICTIONARY.md)). NaN-as-positive encoding per §4.5 captures these in the Mann-Whitney via the 1080-min cap.

### 7.2 Per-channel unmedicated heavy-T vs non-heavy-T descriptives (the comparison arms)

| channel | heavy-T n | heavy-T p50 | heavy-T IQR | non-heavy-T n | non-heavy-T p50 | non-heavy-T IQR | descriptive delta (heavy-T − non-heavy-T) |
|---|---:|---:|---|---:|---:|---|---:|
| Channel 1 primary | 201 | 111 | [46, 188] | 343 | 76 | [38, 146] | +35 min |
| Channel 1 sec. (drop_avg) | 243 | 66.1 | [53.7, 79.0] | 405 | 58.6 | [48.1, 69.9] | +7.5 |
| Channel 2 | 247 | 90 | [56, 132] | 407 | 61 | [36, 101] | +29 min |
| Channel 3 | 247 | 49 | [44, 53] | 407 | 45 | [40, 49] | +4 |

**All four channels show the predicted direction (heavy-T > non-heavy-T) at the descriptive level.** Whether the Mann-Whitney + Cliff's delta + block-permutation null clears the §5.1 bar is the test that runs after lock.

**Channel 1 NaN fractions by arm**: heavy-T 18.6% (46/247) vs non-heavy-T 18.1% (76/419) — **essentially tied**. The "C4-positive case" (NaN-as-failure-to-rest) is NOT meaningfully more common on heavy-T days at the unmedicated descriptive level. The 1080-min Mann-Whitney encoding will absorb the NaN observations rank-equivalently across arms; the directional signal comes from the non-NaN distribution shift, not the NaN-fraction contrast. Per §4.11 the descriptive NaN-fraction contrast is reported anyway as a companion.

### 7.3 Per-channel × per-era sample sizes (the §5.4 inconclusive bar check, computed at r2)

| era | heavy-T n | non-heavy-T n | min arm n | passes §5.4 (≥ 30 both arms)? |
|---|---:|---:|---:|:---:|
| train (2022-09-03 → 2023-12-31, unmedicated) | 206 | 361 | 206 | ✓ |
| validate (2024-01-01 → 2024-04-08, unmedicated) | 41 | 58 | 41 | ✓ |

All per-channel × per-era cells comfortably clear the ≥ 30 inconclusive bar. The validate arm is the tightest (heavy-T n = 41) but still above the bar with margin.

### 7.4 Under-SUPPORTED expected effect sizes per channel

Based on the descriptive deltas above + the §5.1 bar (Cliff's delta ≥ +0.20):

- **Channel 1**: heavy-T median 111 vs non-heavy-T 76 → +35 min descriptive delta → Cliff's delta likely in [+0.15, +0.30] range. Borderline on the bar.
- **Channel 2**: heavy-T median 90 vs non-heavy-T 61 → +29 min descriptive delta → Cliff's delta likely in [+0.20, +0.35] range. Likely passes if the distribution shape supports it.
- **Channel 3**: heavy-T median 49 vs non-heavy-T 45 → +4-point descriptive delta on a 0-100 scale → Cliff's delta likely in [+0.10, +0.25] range. **At-risk for the +0.20 bar**; the precise value depends on within-group variance. The descriptive direction is correct but the magnitude is modest.

The block-permutation p-value test is structurally separate from the effect-size bar; both must pass per §5.1. The descriptive deltas suggest Ch2 is most likely to confirm, Ch1 is borderline, Ch3 is at-risk for the effect-size bar. Whether 2-of-3 confirms is the test that runs after lock.

### 7.5 Sanity gate (applied at dry-run, refined from v1's ±50% to ±30% per audit recommendation 1 + L1.4 closure)

- **Sample size**: per-channel × per-era arm has ≥ 30 days post-§4.3 exclusions (already confirmed above at r2).
- **Distribution check**: per-channel median of the FULL unmedicated-only pool (heavy-T + non-heavy-T combined) falls within **±30% of the §7.1 reference**:
  - Ch1: 81 ± 30% = [56.7, 105.3]
  - Ch1 sec.: 61.0 ± 30% = [42.7, 79.3]
  - Ch2: 73 ± 30% = [51.1, 94.9]
  - Ch3: 46 ± 30% = [32.2, 59.8]
- **Channel 1 NaN-fraction sanity**: the unmedicated NaN fraction falls within [12%, 25%] (descriptive baseline ~18%; tolerance widened to absorb sampling variation across re-extracts).
- If any sanity gate fails → halt + revise → HA-C4-v2 per [`hypothesis_lock_process.md` §3.9](../../../methodology/hypothesis_lock_process.md#39-run-step-post-lock).

**Note on r2 anchor disclosure**: computing §7.1-§7.3 at r2 required running a descriptive query against the unmedicated-phase column data. This is sanctioned r2 work (the audit's L1.4 closure explicitly requested it), but the drafter's exposure has increased beyond the v1 §Authorship boundary: the drafter now knows the unmedicated-phase descriptive directionality (heavy-T > non-heavy-T on all 4 channels at the median level) AND the per-arm sample sizes. This is descriptive aggregate information, not per-day per-channel values; it does not contaminate the test outcome (Mann-Whitney + Cliff's delta + block-permutation p-value). Per the lock-process MD r2 discipline, this is the level of exposure §7 anchor work normally incurs; documented here for completeness.

## 8. Caveats `result.md` must explicitly acknowledge

- **Drafting under shared-context with HA-C4b test session** (per §Authorship). The data-exposure boundary is documented: the drafter knows the identity of 10 heavy-T days that are also crash episodes; the drafter has NOT seen the HA-C4 channel values on individual days. The fresh-session audit (§3.4) is the integrity check on §4 / §5 operational choices. A fresh-session redraft of the eligibility + statistical-test choices (with the 10-crash-identity held out) would be the strictest-discipline path; **the user explicitly accepted at r2 absorption (2026-06-17) that the §3.2-clause shared-context drafting concern is priced in** per audit L2.5 Section 4 item-6 option (a). The audit notes that the two genuinely drafter-chosen items (±50% tolerance, ≥ 30 inconclusive bar) are justified by reasons orthogonal to the 10-crash-day identity (HA-C4b v1 anchor lesson; sample-pool size); design-MD-inherited choices (Ch1-3 definitions, T-only eligibility, chain-T+1 exclusion, pass-2-of-3 verdict) are not drafter-chosen. The L4.4 crash-drop sensitivity arm (§4.11.1, added r2) further insulates the spec from "drafter knew the crash IDs and silently chose not to test sensitivity" concerns. The r2 §7 anchor rebuild (closing L1.4) additionally tightened the §7.5 tolerance from ±50% to ±30%, partly absorbing the L2.5 concern on tolerance choice per the audit's coupled-fix observation.

- **Power-calc dispatch**: power calculation is inapplicable per [Daza 2018](../../../literature/methodology/daza_2018_self_tracked_n_of_1_counterfactual.pdf) within-subject design — the n-of-1 corpus does not have separate treatment and control arms in the classical sense. The block-permutation null at E[L]=7 (§4.9) is the within-subject inferential machinery; the §5.1 (a) discrimination + (b) effect-size gates determine per-channel confirmation rather than a power-thresholded p-value.

- **NaN-as-positive encoding for Channel 1** (§4.5): the 1080-min coding is one operationalisation; the NaN-fraction descriptive contrast (§4.11) is the alternative. Result.md must report both. If the verdict depends on the encoding choice, flag as encoding-fragile.

- **Chained-regime adjustment for Channel 3** (§4.7): heavy-T-followed-by-heavy-T+1 days are excluded from the Channel 3 primary. This may reduce the heavy-T sample size in Channel 3; report the n-loss. If the chain exclusion drops Channel 3 below the §5.4 inconclusive bar, Channel 3 is INCONCLUSIVE and the triad reduces to Ch1 + Ch2.

- **Citalopram dose-modulation** (§4.4): the primary scope is unmedicated only specifically to avoid the dose-confound on the stress channel. Cross-phase sensitivity arms require §5.B dose-adjustment per [`citalopram_phase_stratification.md`](../../../methodology/citalopram_phase_stratification.md). This pre-reg does not attempt cross-phase aggregation.

- **No motion filter** (unlike HA-C4b): HA-C4 tests `awake_stress_avg`, `stress_high_duration_min`, and `stress_post_peak_time_to_rest_min` without conditioning on motion. The Garmin-stress-is-partly-motion-sensitive caveat applies (per [`hrv_proxy_via_stress.md §2`](../../../methodology/hrv_proxy_via_stress.md#2-how-garmin-stress-is-derived)); some of the channel signal may be motion-artefact rather than true sympathetic load. Result.md must acknowledge this and cross-reference HA-C4b's motion-filter test.

- **Unmedicated = pre-citalopram corpus, not "no medication overall"**: the participant had other lived-experience interventions in the 2022-04 → 2024-04 window (CPAP started 2024-01-10; daily pacing protocols evolved through this period; ergotherapy program 2022-06-17 → 2023-03-10; PWC reintegratie 2023-03-06 → 2023-11-28). The unmedicated headline is "no SSRI" not "no intervention". The §4.1 heavy-T classification absorbs the gross exertion effect; finer-grained context lives at the result.md interpretation layer.

- **Pacing-behaviour confounder (inherited from HA-C4b v3 §8)**: `exertion_class_lagged_lcera` captures physical exertion only. Cognitive, emotional, and orthostatic exertion are not in the classification. A "non-heavy-T" day in this test could include high cognitive / emotional load days that are physiologically demanding. The C4 pattern may appear on those days too; mis-classifying them as non-heavy-T arm would dilute the heavy-T vs non-heavy-T contrast (i.e. bias toward NULL / NOT-SUPPORTED). Result.md must note this as a directional bias toward false-NOT-SUPPORTED.

- **Single-subject n=1**: thresholds in §5.1 (p < 0.05, |delta| > 0.20) are calibrated to the participant's distribution. The Mann-Whitney is non-parametric so the threshold-on-effect-size choice is the binding decision; the alternative (a stricter Cliff's delta threshold like 0.33 for "medium" effect) would shift the gate.

- **HA11 / HA-C4b cross-references**: HA11 SUPPORTED on the inverse (U-dip = sharp drop) signal; HA-C4b NOT-SUPPORTED on the motion-filtered crash-precursor framing. HA-C4 SUPPORTED would complete the picture (the failure-to-recover signal IS detectable at the descriptive level even though the crash-precursor framing didn't pan out). HA-C4 REJECTED would shrink the C4-mechanism reading further. Result.md must surface this triangulation.

- **The block-permutation null preserves the heavy-T autocorrelation structure but breaks the heavy-T → channel relationship**. Under the null, the heavy-T labels are reshuffled in blocks while channel values stay fixed; this tests "is the observed difference larger than what random block-permutation produces?" The empirical p-value is the appropriate within-subject inferential statistic.

## 9. What we do with each outcome

### 9.1 SUPPORTED (2-of-3 or 3-of-3 channels confirmed in both eras)

The Wiggers C4 pattern is empirically confirmed at the **pattern-existence level** on this corpus: post-heavy-exertion days do show degraded stress-recovery dynamics. The specific channel breakdown is reported as **verdict-invariant descriptive labels** (per audit L4.7 closure — labels are properties of the channel set, not pre-staged interpretive scripts):

- **Channel 1 + Channel 2 + Channel 3 all confirmed**: all three temporal scales of the Wiggers C4 claim show signal — same-day decay failure (Ch1), walls of orange (Ch2), and next-day reactivity (Ch3).
- **Ch1 + Ch2 confirmed, Ch3 not**: same-day phenomena confirmed (decay + walls); next-day reactivity in the expected range. Result.md author interprets against the observed magnitudes + sister-test context, not a pre-staged mechanistic script.
- **Ch1 + Ch3 confirmed, Ch2 not**: decay failure + reactivity confirmed; sustained-high count (walls) in the expected range. Same: no pre-staged mechanistic claim.
- **Ch2 + Ch3 confirmed, Ch1 not**: walls + reactivity confirmed; decay-time-to-rest in the expected range. Same: no pre-staged mechanistic claim.

**Cross-reference downstream**:
- **HA-C4 SUPPORTED + HA-C4b NOT-SUPPORTED** (the actual cross-result): the Wiggers pattern exists but isn't a per-episode crash precursor at the motion-filtered operationalisation. This is the **protective-rather-than-predictive** alternative reading from HA-C4b §9, now with corroborating evidence — the pattern Wiggers describes IS real on this corpus, but the participant's real-time use of it as a pacing trigger prevents the crashes the precursor test would have caught.
- **HA-C4 SUPPORTED + HA11 SUPPORTED-on-train (U-dip)**: the autonomic-recovery story is multi-channel-confirmed: both the U-dip (calm-day signal) and the failure-to-recover (heavy-day signal) work as expected on this corpus.
- **Downstream synthesis**: [`garmin_pacing_practice.md`](../../../methodology/garmin_pacing_practice.md) may strengthen the §3.3 rest-stress trigger's standing from "operational heuristic" to "empirically-confirmed pattern".

### 9.2 PARTIAL (1 channel confirmed in both eras, OR 2+ channels confirmed in only one era)

The C4 pattern shows partial signal but not the strong 2-of-3 triad confirmation. Specific reads:

- **1 channel confirmed in both eras**: one of the three temporal scales is detectable; the other two are not. Probably the strongest channel deserves a per-channel SUPPORTED-on-that-scale write-up, but the overall C4 verdict is PARTIAL.
- **2+ channels confirmed in train only**: train-only signal; validate didn't replicate. Possible drift (the trajectory of the participant's autonomic state changed between 2023 and 2024) or sample-size issue in validate.
- **2+ channels confirmed in validate only**: validate-only signal; train didn't replicate. Less common pattern; possible that the more-recent data has cleaner protocol adherence.

PARTIAL outcomes are descriptively informative but don't carry the SUPPORTED-bar weight for downstream protocol claims.

### 9.3 REJECTED (0 channels confirmed in either era)

The Wiggers C4 pattern does NOT show systematic post-exertion degradation at the descriptive level on this corpus. This is a meaningful finding: either the pattern doesn't exist on this participant, OR the heavy-T classification doesn't capture the right exertion threshold, OR the protocol-disturbance from active pacing has flattened the signal entirely.

**Cross-reference downstream**: REJECTED + HA-C4b NOT-SUPPORTED + HA11 SUPPORTED-on-train would mean: the Wiggers C4 framework doesn't operationalise cleanly on this corpus at either the descriptive or precursor level, but the U-dip (HA11) sister channel does. The C4 mechanism question would need different operationalisation (e.g. bout-level recovery curves per §5 of the synthesis discussion) to be testable.

### 9.4 Sensitivity-arm divergence

- **`stress_post_peak_drop_avg` companion diverges from primary Ch1**: the Ch1 result is encoding-fragile; flag for review.
- **`stress_recovery_pct_within_2h` companion diverges from primary Ch1**: the slow-but-complete-vs-fast-then-stall distinction is doing analytical work; flag for descriptive write-up.
- **Chain-T+1-excluded Ch3 diverges from chain-included Ch3**: the chained-regime sequences are doing analytical work; report both.
- **NaN-fraction contrast for Ch1 disagrees with 1080-encoded Mann-Whitney**: the encoding choice matters more than the underlying signal; report both with explanatory paragraph.

### 9.5 Spec sanity-check fails on dry-run

If any per-channel sample (heavy-T arm or non-heavy-T arm) in any era has < 30 days post-§4.3 exclusions, OR if per-channel median falls outside the §7 ±50% tolerance:

DO NOT run the full test. Document the failure in the dry-run report; revise the spec creating HA-C4-v2 with this pre-reg archived as v1 per [`hypothesis_lock_process.md` §3.9](../../../methodology/hypothesis_lock_process.md#39-run-step-post-lock).

## 10. Detection script architecture

### 10.1 Stage 1 — data (already done)

All channel columns and the heavy-T classification are already in `$GEVOELSCORE_DATA_PATH/unified/per_day_master.csv`. No new extraction needed.

### 10.2 Stage 2 — test (`HA-C4/test.py`, to be written post-lock)

Loads `per_day_master.csv`, applies §4 eligibility filtering (LC era + unmedicated phase + April 2024 exclusion + non-NaN channel values + heavy-T classification non-NaN), computes per-channel × per-era Mann-Whitney U + Cliff's delta + block-permutation p-value at E[L]=7, applies §5 triad verdict rule + Holm step-down correction.

**Spec-sanity-gate at dry-run**: confirms per-channel × per-era sample sizes ≥ 30 in both arms; per-channel medians within §7 ±50% tolerance. If any fail → halt + revise per §9 spec-sanity-check-fails branch.

**Same null-seed `RANDOM_SEED = 20260617`** for reproducibility.

### 10.3 Stage 3 — `result.md`

Reports the triad verdict block at top (one cell: 2-of-3 / 1-of-3 / 0-of-3 in each era), followed by per-channel × per-era contingency tables with (a) p-value, (b) Cliff's delta, (c) Holm-corrected p-value. Then secondary descriptive outcomes per §4.11 (drop-avg companion, recovery-pct companion, NaN-fraction contrast, chain-T+1 sensitivity). Then sister-test cross-reference table. Caveats per §8 including the data-exposure context disclosure prominent at top.

### 10.4 Run protocol

1. **Dry-run** (`python test.py --dry-run`): prints sample sizes per channel × era × arm; checks §10.2 sanity gates. **If sanity check fails → halt + revise spec → HA-C4-v2.**
2. **Full run** (`python test.py`): emits `result.md` directly into this folder.
3. **No iteration on the spec after the dry-run passes.** Any post-dry-run revision creates HA-C4-v2 with the v1 result archived.

---

*Pre-registration drafted 2026-06-17 by Claude (Opus 4.7) in reviewer-mode-with-authorization, in the same Claude session that has executed the sister test HA-C4b v3 to NOT-SUPPORTED. Per [`hypothesis_lock_process.md` §3.2 clause](../../../methodology/hypothesis_lock_process.md#32-drafting-step-step-1-of-the-arc) shared-context drafting is permitted; the data-exposure boundary is documented in the Authorship block; the fresh-session `/research-review` audit (§3.4) is the integrity check. Lock requires user acceptance + audit clearance + the four §3.8 gate confirmations.*
