# HA-C4 v2 — Stress fails to drop during rest periods after overexertion ("stuck sympathetic"), 3-channel confirmatory triad

## Authorship

**Drafted 2026-06-18** by Claude (Opus 4.7) in reviewer-mode-with-authorization per [CONVENTIONS §1.2](../../../CONVENTIONS.md#12-reviewer-mode-claude-reads--critiques--explains-does-not-edit-unless-asked). Authorising user: Willem. **Fresh-session drafting per [`hypothesis_lock_process.md` §3.2](../../../methodology/hypothesis_lock_process.md#32-drafting-step-step-1-of-the-arc)** following the post-dry-run-halt v2 arc per [§3.9](../../../methodology/hypothesis_lock_process.md#39-run-step-post-lock).

**v2 trigger**: v1 (LOCKED 2026-06-17 r2 commit `da79387`; archived at [`hypothesis-v1-archived.md`](hypothesis-v1-archived.md)) was dry-run-halted (commit `19d33e4`; archived at [`dry-run-report-v1-archived.md`](dry-run-report-v1-archived.md)) at §7.5 gate 2 because Channel 3 validate-arm n = 25 < the §5.4 inconclusive bar of 30 (the §4.7 chain-T+1 exclusion dropped 16 of 41 validate heavy-T days). The locked-pre-reg discipline ([`hypothesis_lock_process.md` §3.9](../../../methodology/hypothesis_lock_process.md#39-run-step-post-lock)) halted the test and required a v2 redraft. A separate fresh-session triage analysis (see [`dry-run-report-v1-archived.md`](dry-run-report-v1-archived.md) "Recommendation for HA-C4-v2" section) identified five disposition options + recommended a **composite path**: Option A (explicit INCONCLUSIVE handling in §5.3) + §7.3 arithmetic rebuild (Option E first half) + Option C as a §4.11.3 descriptive sensitivity arm (NOT promoted to primary).

**This drafting session's input**: the composite-path recommendation from the v1 dry-run-report triage section. The drafter has read v1's `hypothesis.md`, `test.py`, `dry-run-report.md` (the recommendation block + §7.5 gate breakdown + §7.3 arithmetic discrepancy), and the §4 / §5 handoff brief. The drafter has NOT seen any per-episode z-values or per-day channel values from the v1 test (the v1 full run never executed because of the halt); the dry-run surfaced only sample-size cell counts (n_heavy, n_non_heavy per channel × era), which are fair-game pre-test descriptive aggregates.

**Data exposure context** (audit-able): the v2 drafter inherits v1's shared-context drafting boundary (which is permanently archived in `hypothesis-v1-archived.md` §Authorship) — the v1 drafter knew the identity of 10 unmedicated heavy-T-and-crash days from HA-C4b's pool. v2's structural changes do not depend on those identities; the §5.3 INCONCLUSIVE-handling rule, §7.3 arithmetic rebuild, and §4.11.3 sensitivity arm are structural decisions in response to the v1 dry-run halt, not data-driven. The §3.2-clause shared-context concern remains priced-in per v1 r2 user acceptance; this v2 draft does not re-open the boundary discipline question.

**v2 deltas from v1** (three integrated changes, all structural):

1. **§5.3 verdict rule rewritten** with explicit handling of channel × era cells whose outcome is INCONCLUSIVE under the §5.4 ≥30 inconclusive bar. v1's §5.3 implicitly assumed every cell yields a binary SUPPORTED / REFUTED verdict; the dry-run halt exposed that an INCONCLUSIVE cell breaks the binary triad logic. v2 introduces a 3-state per-cell verdict (SUPPORTED / REFUTED / INCONCLUSIVE) and a per-channel aggregation rule that distinguishes CONFIRMED (1.0 contribution; SUPPORTED in both eras), CONFIRMED-PARTIAL (0.5 contribution; SUPPORTED in one era + INCONCLUSIVE in the other), and REFUTED (0 contribution; everything else). Triad verdict bands: 3.0 = SUPPORTED strong; 2.0-2.5 = SUPPORTED; 1.0-1.5 = PARTIAL; < 1.0 = REJECTED. **Honest framing per [CONVENTIONS §4.2](../../../CONVENTIONS.md#42-caveats-yes-a-priori-claims-no)**: this rule was added in v2 in response to the v1 dry-run halt. The rule is structural — applies regardless of which cell turns out INCONCLUSIVE — and is named here as a post-halt closure, not as a pre-emptive design choice.

2. **§7.3 sample-size table rebuilt** with chain-T+1-corrected counts (the dry-run report surfaces these exactly). v1's §7.3 implicitly assumed the 35-day pre-train buffer (Apr–Aug 2022, in the unmedicated phase but BEFORE train start of 2022-09-03) was already excluded from the heavy-T count: it asserted train heavy-T n = 206 = 247 − 41, when the correct value is n = 171 = 247 − 41 − 35. v2 corrects this AND adds the per-channel chain-T+1 decomposition for Channel 3 (train n = 117 after 54 chain-drops; validate n = 25 after 16 chain-drops). The bug-fix does NOT change the v1 halt verdict (the binding §7.5 gate-2 failure was on Ch3 validate, not on train Ch1/Ch2); it is recorded here as an honest spec-bug fix.

3. **§4.11.3 new sensitivity arm**: a descriptive Ch3-validate variant with the §4.7 chain-T+1 exclusion **relaxed** (n = 41 instead of 25). Reported alongside the primary Ch3 validate cell as a descriptive what-if read — not promoted to the primary verdict; the chain-T+1 rule remains the discipline-binding choice for the headline. Per [CONVENTIONS §3.3](../../../CONVENTIONS.md#33-one-column-per-definitional-pair) (column-duplication discipline) the sensitivity-arm cell is explicitly marked as derived from the Ch3 validate primary cell with the chain rule as the only difference; the two read together.

**What stays UNCHANGED from v1** (verbatim inheritance — do NOT re-derive):

- §1 Claim, §2 Why we think this, §3 Data sources.
- §4.1-§4.6 (heavy-T eligibility, channel definitions, day-validity, citalopram-phase treatment, NaN-as-positive encoding, missing-data handling).
- §4.7 chain-T+1 exclusion rule itself (Channel 3 primary), §4.8 statistical machinery (Mann-Whitney + Cliff's delta + block-permutation null at E[L]=7), §4.9 block-permutation procedure + E[L]\* companion + factor-of-2 flag, §4.10 walk-forward gate per channel, §4.11.1 (crash-drop sensitivity) + §4.11.2 (Ch3 spike-companion).
- §5.0 single-cell headline lock, §5.1 per-channel confirmation bar (p < 0.05 + Cliff's delta ≥ +0.20), §5.2 per-channel confirmation across eras, §5.4 inconclusive bar (≥ 30 per arm; v2 §5.3 explicit INCONCLUSIVE handling absorbs the formerly halt-triggering condition for sample-size shortfall), §5.5 Holm step-down secondary report.
- §6 exclusion rules.
- §7.1 per-channel unmedicated-only descriptives (full pool), §7.2 per-channel × heavy-T-vs-non-heavy-T descriptives, §7.4 under-SUPPORTED expected effect sizes, §7.5 sanity gates (with one wording adjustment: gate 2's "<30 per arm" outcome routes to §5.4 INCONCLUSIVE per §5.3, not to a HALT — distribution-sanity gates 1 and 3 still HALT on failure).
- §8 v1 caveats (v2 prepends 5 v2-specific caveats; v1 caveats inherited verbatim below them).
- §10.1 (data stage), §10.2 (test stage), §10.3 (result.md template), §10.4 (run protocol; HALT trigger for distribution-sanity failures preserved as v1 designed).

**Revision 2026-06-18-r2** (post-audit, shared-context with drafting per [`hypothesis_lock_process.md` §3.5](../../../methodology/hypothesis_lock_process.md#35-revise-step-stage-3-of-the-arc-r2--the-bulk-of-methodological-strengthening)). Four wording closures absorbed from the [fresh-session `/research-review` audit report](../../../reviews/HA-C4-v2-2026-06-18.md) (verdict: **PASS with caveats**). The audit found no Layer-1 fires (the v1 L1.4 §7-anchor concern stays closed via §7.1+§7.2 rebuild); one Layer-2 substantive concern (L2.5 drafting-with-knowledge-of-which-cell-failed; **user-binding lock-stage call** per §3.6); zero Layer-3 fires; one Layer-4 minor inherited carry-forward (L4.5 Ch3 mean-vs-spike; §4.11.2 mitigates). The four side observations from the audit's Section 4 are all closed as mechanical r2 wording changes (no architectural change, no falsification-bar change, no new statistical machinery):

- **§5.3 honest-framing paragraph tightened** (closes audit Side obs 1). The v1 gap v2 resolves is not "binary triad logic" (v1 already had a 0.5-single-era category) but specifically **the interaction between v1 §5.4 ("INCONCLUSIVE channels do not count") and v1 §5.3's 2-of-3 rule when a channel has one SUPPORTED era + one INCONCLUSIVE era**. v2's CONFIRMED-PARTIAL category at 0.5 resolves this interaction explicitly. The 0.5 contribution + ≥ 2.0 SUPPORTED bar are inherited verbatim from v1's pre-dry-run lock; v2 extends rather than re-calibrates with hindsight.
- **§4.11.3 non-heavy-T arm construction made explicit** (closes audit Side obs 4). The §4.7 chain rule was always heavy-T-only by construction ("EXCLUDE heavy-T days T where T+1 is heavy"); the non-heavy-T arm has no T+1-is-heavy exclusion to relax. r2 explicitly states: non-heavy-T arm = byte-identical to primary (n=58 in validate), via natural-pool count after §4.3 + §6 + §4.6 — NOT re-paired 1:N per heavy-T day; the comparison stays the standard two-sample Mann-Whitney shape.
- **§5.5 Holm fewer-comparisons disclosure added** (closes audit Side obs 2). When a channel × era cell is INCONCLUSIVE, the per-era Holm step-down operates on 2 channels (cutoffs α/2 and α/1) instead of 3 (α/3, α/2, α/1) — less stringent. The result.md Holm column MUST be annotated explicitly when this occurs (form: *"Holm (2-of-2 comparisons; Ch3 validate INCONCLUSIVE)"*). Reporting-discipline only; the §5.0 hard rule still binds Holm as secondary report.
- **`stress_recovery_pct_within_2h` pre-lock pandas check PASSED** (closes audit Side obs 3). Column verified present in `per_day_master.csv` at index 117, coverage 1526/1755 = 87.0%. The §4.11 secondary companion is implementable; no test.py KeyError risk.

The L2.5 substantive concern (drafting v2 with knowledge of which v1 cell failed) is **acknowledged but not structurally closeable at r2** — the audit's recommendation is that the user re-confirm at §3.6 whether the v1 r2 "priced-in" disposition of the §3.2-clause shared-context concern carries forward to v2's drafting context, OR whether the v2 structural inheritance from v1's pre-dry-run bands is enough to materially weaken the L2.5 fire below the "priced-in" threshold. **This is a lock-time user decision**, not an r2 mechanical fix. r2 documents the disposition options; lock-commit confirms the chosen path.

**Status: LOCKED-PENDING-USER-ACCEPTANCE 2026-06-18 at revision r2** by Claude (Opus 4.7) in reviewer-mode-with-authorization. The fresh-session §3.4 audit completed (verdict PASS with caveats); all four side-observation closures applied in r2 as mechanical wording fixes; the L2.5 user-binding decision is pending at lock time. Per [`hypothesis_lock_process.md` §3.6 compression criteria](../../../methodology/hypothesis_lock_process.md#36-re-audit-step-stage-4-of-the-arc), re-audit compression is **available** because r2 changes are mechanical (wording tightenings + an explicit construction-rule clarification + a reporting-discipline annotation + a pre-lock data-presence verification) with no architectural change, no new statistical machinery, and no falsification-bar change. **User decides** at lock time: (a) §3.6 compression accepted (lock at r2 with the L2.5 priced-in disposition carrying forward) OR (b) fresh-session re-audit on r2 (strictest discipline). Lock signal awaits explicit user acceptance + lock-commit message naming the four §3.8 gate confirmations + the L2.5 disposition.

---

**Pre-registration drafted 2026-06-18 as v2 post-dry-run-halt-v1**, BEFORE any test run on the v2 spec. Any subsequent change after lock creates HA-C4-v3 with v2 archived as v2.

HA-C4 tests Wiggers' **"After overexertion, stress fails to drop during rest periods — stuck sympathetic"** claim (PDF lines 1112-1119, 1140-1143, 1223-1231, 1306-1314, source-verified per the [register entry](../../../wiggers_testable_hypotheses.md#c4--stress-fails-to-drop-during-rest-periods-after-overexertion-stuck-sympathetic) batch 2 2026-06-12). The claim has three temporal scales — same-day decay failure, walls-of-orange sustained-high, and next-day stress-spike reactivity — operationalised as a **3-channel confirmatory triad** per the design MD's expansion (single-metric C4 missed two source-named channels).

## 1. Claim

On heavy-exertion days (`exertion_class_lagged_lcera ∈ {heavy, very_heavy}` on T) within the unmedicated phase (2022-04-04 → 2024-04-08), three independent stress-recovery channels should each show systematic degradation relative to non-heavy-exertion days within the same phase and era:

- **Channel 1 (same-day decay)**: `stress_post_peak_time_to_rest_min` on T is **longer** on heavy-T days than on non-heavy-T days. NaN value = "stress never returned to rest that day" = C4-positive case; coded as the day's awake-window maximum (1080 min ≈ 18 hours; see §4.5).
- **Channel 2 (walls of orange)**: `stress_high_duration_min` on T (count of waking minutes with stress > 75) is **higher** on heavy-T days.
- **Channel 3 (t+1 reactivity)**: `awake_stress_avg` on T+1 is **higher** on heavy-T days than on non-heavy-T days.

The directional prediction in all three channels: heavy-T degrades the recovery. Each channel's confirmation requires both a statistically discriminative effect (block-permutation p < 0.05) AND a non-negligible effect size (|Cliff's delta| > 0.20), in the predicted direction, replicated independently in the train era (2022-09-03 → 2023-12-31) AND the validate era (2024-01-01 → 2024-04-08) within the unmedicated phase.

**Headline triad cell**: unmedicated phase × {Ch1 + Ch2 + Ch3} × heavy-T-vs-non-heavy-T × Mann-Whitney + Cliff's delta × block-permutation null E[L]=7 × INCONCLUSIVE-aware per-channel aggregation × triad verdict rule applied across all three channels.

**Verdict rule** (v2 rewritten with explicit INCONCLUSIVE handling): each channel × era cell yields SUPPORTED / REFUTED / INCONCLUSIVE. Each channel aggregates across eras to CONFIRMED (1.0), CONFIRMED-PARTIAL (0.5), or REFUTED (0). Triad sum bands: 3.0 = SUPPORTED strong; 2.0-2.5 = SUPPORTED; 1.0-1.5 = PARTIAL; < 1.0 = REJECTED. See §5.3.

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

### 4.1 Heavy-T eligibility (locked; verbatim from v1)

A day `T` is a **heavy-T candidate** if `exertion_class_lagged_lcera ∈ {heavy, very_heavy}` on T. A day is a **non-heavy-T candidate** if `exertion_class_lagged_lcera ∈ {none, light, moderate}` on T. Days with missing exertion classification are excluded from the comparison.

**Note vs HA-C4b**: HA-C4b conditioned on `heavy/very_heavy` on T OR T-1 (union, capturing crashes triggered by exertion on either day). HA-C4 conditions on T only (more conservative; the t+1 reactivity channel will use T+1 separately).

### 4.2 Channel definitions (locked; verbatim from v1)

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

### 4.3 Day validity (locked; verbatim from v1)

A day `T` enters the comparison if:
1. `T` is in the LC era (`>= 2022-04-04`) AND in the unmedicated phase (`< 2024-04-09`).
2. `T` is NOT in the April 2024 cluster (`2024-04-09 → 2024-04-16`).
3. The relevant channel value is computable (non-NaN, except for Channel 1's documented NaN-as-positive encoding).
4. For Channel 3 specifically: `T+1` is ALSO in the unmedicated phase AND NOT in the April 2024 cluster AND has computable `awake_stress_avg`.

**Per-channel sample minimums (inconclusive bar per §5.4)**: each channel × era cell must have ≥ 30 heavy-T days AND ≥ 30 non-heavy-T days to produce a verdict. Below this, the channel × era result is INCONCLUSIVE for that era — per v2 §5.3, INCONCLUSIVE is now explicitly handled at the per-channel aggregation layer, NOT a halt trigger for the test as a whole.

### 4.4 Citalopram phase treatment (locked; verbatim from v1)

**Primary scope**: unmedicated phase only (LC era start 2022-04-04 → 2024-04-08). Rationale: avoids the [`citalopram_dose_response §5.6`](../../../methodology/citalopram_dose_response_stress_mean_sleep.md#56-v3-amendment--multi-channel-confirmation-added-2026-06-14) dose-modulation confound on the stress channel (β = +0.57/mg for `all_day_stress_avg`; β = +0.43/mg for `stress_mean_sleep`). At 30 mg plasma the stress baseline shifts by ~12-17 points, which would contaminate the Channel 2 (>75 minutes count) and Channel 3 (`awake_stress_avg` directly) comparisons if pooled across phases.

**Sensitivity arms** (descriptive only, no SUPPORTED-bar promotion): per-phase tests on consolidation, buildup, afbouw with the §5.B dose-adjustment applied per the methodology MD. Reported in result.md alongside the primary unmedicated verdict; not part of the §5 SUPPORTED-bar decision.

### 4.5 NaN-as-positive encoding for Channel 1 (locked; verbatim from v1)

`stress_post_peak_time_to_rest_min` has NaN semantics that **invert the usual rule**: NaN means "stress never dropped below the 25 'rest' threshold within the same calendar day" — the C4-POSITIVE case, not a coverage problem (per [DATA_DICTIONARY §C4](../../../DATA_DICTIONARY.md)).

**Encoding**: NaN values for Channel 1 are coded as **1080 minutes** (= 18 hours, an upper bound on the typical waking window) for the purpose of Mann-Whitney U + Cliff's delta computation. This ensures NaN-as-positive observations contribute to the heavy-T-vs-non-heavy-T comparison rather than being silently dropped.

**Sensitivity check**: report the per-arm (heavy-T vs non-heavy-T) NaN fraction in result.md as a descriptive companion. If heavy-T NaN fraction is substantially higher than non-heavy-T NaN fraction, that itself is direct C4 evidence (the C4-positive case is more common after heavy exertion). The 1080-encoding is one way to surface this within the Mann-Whitney framework; the raw NaN-fraction contrast is the alternative descriptive read.

### 4.6 Day-validity gate: missing-data handling for the other channels (locked; verbatim from v1)

- Channel 2 NaN: drop the day from Channel 2's comparison (no positive-encoding semantics for `stress_high_duration_min`).
- Channel 3 NaN on T+1: drop the corresponding heavy-T (or non-heavy-T) day from Channel 3's comparison.
- Channel 1 NaN: encode as 1080 per §4.5 (positive case).
- Days with `exertion_class_lagged_lcera` NaN: excluded entirely (can't classify heavy vs non-heavy).

### 4.7 Chained-regime adjustment (locked per design MD §C4 pre-reg specifics; verbatim from v1)

**Channel 3 (t+1 reactivity) specifically requires chained-regime handling** because the test compares `awake_stress_avg[T+1]` for heavy-T-on-T vs heavy-T-not-on-T. If `T+1` is itself a heavy day (i.e. the participant overdid it for two consecutive days), the comparison is confounded.

**Rule**: for the Channel 3 comparison, EXCLUDE heavy-T days `T` where `exertion_class_lagged_lcera ∈ {heavy, very_heavy}` on `T+1`. This restricts Channel 3 to "heavy-T followed by non-heavy-T+1" — the cleanest test of "the day AFTER overdoing it" claim.

**Channel 1 and Channel 2 are not affected** by this adjustment (they test on T only).

**Sensitivity arm** (descriptive only): a Channel 3 variant **without** the chained-regime exclusion, reported alongside the primary. If both variants reach the same verdict, the chained-regime adjustment didn't materially affect the result; if they differ, the chained-regime sequences are doing analytical work. **v2 §4.11.3 expands this sensitivity arm to a dedicated reporting block** for the Ch3 validate cell specifically, where the chain-T+1 exclusion drops the arm size from 41 to 25 (the v1-halt cell).

### 4.8 Per-channel statistical method (locked per design MD; verbatim from v1)

For each channel × era cell:

1. **Mann-Whitney U statistic** on the channel values: heavy-T arm vs non-heavy-T arm. One-sided (heavy-T > non-heavy-T per the directional prediction in §1).
2. **Cliff's delta** as the non-parametric effect size: `delta = (n_heavy>non - n_heavy<non) / (n_heavy * n_non)`. Range [-1, +1]; positive = heavy-T > non-heavy-T. The 0.20 threshold is "small-to-medium" effect per the standard interpretation.
3. **Block-permutation null** (per §4.9 below): empirical p-value = fraction of B = 10,000 null permutations whose U statistic equals or exceeds the observed U.
4. **Channel confirmed in era** if: empirical p < 0.05 AND Cliff's delta > +0.20 (in the predicted positive direction). If the cell's sample size violates §5.4 (either arm < 30), the cell is INCONCLUSIVE, not REFUTED.

### 4.9 Null sample — block-permutation of heavy-T labels (locked, inherits from [`permutation_null_block_length.md`](../../../methodology/permutation_null_block_length.md); verbatim from v1)

The independence assumption for raw Mann-Whitney U is violated by the autocorrelation in the channel values (consecutive days share physiological state). The project-canonical inference framework is **stationary bootstrap with E[L] = 7 days** per the methodology MD.

**For HA-C4 specifically**: we **permute the binary `is_heavy_T[d]` label sequence** in blocks (geometric-distributed block length with mean E[L] = 7) while keeping the channel values in their original temporal positions. This preserves the channel autocorrelation and breaks the heavy-T → channel relationship.

**Procedure**:
1. Take the observed sequence `(date, is_heavy_T[d], channel_value[d])` for the era.
2. Generate B = 10,000 null draws: for each draw, resample the `is_heavy_T` label sequence via stationary bootstrap (E[L]=7) while keeping `channel_value` fixed in place.
3. For each null draw, recompute the Mann-Whitney U statistic on the resampled labels.
4. Empirical one-sided p-value = `(1 + #{U_null >= U_observed}) / (B + 1)`.

**Seed**: `RANDOM_SEED = 20260618` (HA-C4 v2 seed; distinct from v1's `20260617` and HA-C4b v3's `20260615` to keep v2 cell statistics independently reproducible from v1's archived null distribution).

**E[L] derivation vs application** (inherits from v1 r2 L3.1 closure): the E[L]=7 anchor in [`permutation_null_block_length.md`](../../../methodology/permutation_null_block_length.md) is derived for *channel-value* autocorrelation (daily physiological signals' ACF typically decay within a week per the methodology MD §4). For HA-C4 the permutation acts on the *heavy-T LABEL sequence*, which has its own autocorrelation driven by sustained-push regimes (the chained-regime framing in the design MD). The label-sequence E[L] may differ from the channel-value E[L]; the **data-driven E[L]\* companion below is the empirical check on this assumption**.

**E[L]\* companion + factor-of-2 flag**: data-driven `E[L]*` estimator per [`permutation_null_block_length.md`](../../../methodology/permutation_null_block_length.md) Operational consequences. Compute E[L]* on **both** (a) each channel's value series AND (b) the heavy-T label sequence; flag if `|E[L]* - 7| / 7 > 0.5` on either. The flag fires only on SUPPORTED verdicts (per the methodology MD); for PARTIAL or REJECTED, the flag is descriptive context only.

### 4.10 Walk-forward gate per channel (locked per design MD; verbatim from v1)

Each channel is independently tested in **train** (2022-09-03 → 2023-12-31, within unmedicated) and **validate** (2024-01-01 → 2024-04-08, within unmedicated). Both eras must reach the channel-confirmation threshold (§4.8 step 4) for the channel to count toward the §5.3 triad verdict at the full 1.0 contribution. A single-era confirmation with the other era INCONCLUSIVE contributes 0.5 (CONFIRMED-PARTIAL) per the v2 §5.3 rule.

**Walk-forward integrity**: the train era is tested first; the validate era confirmation is an out-of-sample replication on a strictly later time window. No within-era data crosses the temporal boundary.

### 4.11 Secondary descriptive outcomes (locked, no verdict weight)

- **`stress_post_peak_drop_avg` companion**: report the parallel Mann-Whitney + Cliff's delta on `stress_post_peak_drop_avg` (Channel 1's secondary aggregate) alongside the primary `stress_post_peak_time_to_rest_min` result. If both Channel 1 metrics agree directionally, the Channel 1 confirmation is internally consistent; if they diverge, flag for review.
- **`stress_recovery_pct_within_2h` companion**: parallel test on this column (the "direct rate-of-recovery metric" per the dictionary). Pair with `stress_post_peak_time_to_rest_min` to distinguish slow-but-complete recovery from fast-then-stall.
- **NaN-fraction descriptive contrast** for Channel 1: report per-arm NaN fractions explicitly (heavy-T vs non-heavy-T). If heavy-T NaN fraction > 10pp higher than non-heavy-T, that is direct C4-positive descriptive evidence independent of the 1080-encoded Mann-Whitney result. (Per §7.2 the v1 r2 descriptive shows these are essentially tied at 18%; this companion is reported anyway as the encoding-fragility check per §4.5.)

#### 4.11.1 Crash-drop sensitivity arm (inherited verbatim from v1 r2; closes audit L4.4 substantive)

The v1 audit fired CONVENTIONS §3.4 (crash-drop sensitivity row) because the drafter knows the identity of 21 unmedicated heavy-T-and-crash days, and the heavy-T arm intentionally pools crash with non-crash heavy-T days. Per the audit's Section-4 item-2 closure path (option a), the spec adds an explicit crash-drop sensitivity arm:

**Rule**: re-run the per-channel × per-era Mann-Whitney + Cliff's delta with `is_crash == True` dropped from BOTH the heavy-T arm AND the non-heavy-T arm. Compare the crash-dropped Cliff's delta vs the primary Cliff's delta per channel. Report Δ Cliff's delta in the result.md sensitivity table.

**Flag**: if |Δ Cliff's delta| > 0.10 on any channel, surface as a §3.4 finding ("the channel's signal is crash-driven, not robust across the broader heavy-T pool"). The primary verdict per §5.3 is unchanged; the crash-drop sensitivity is a descriptive read on the verdict's robustness.

**Rationale**: the C4 mechanism IS expected to be strongest on crash days (per §9 — the "protective-rather-than-predictive" alternative reading depends on this); a strong dependence of the verdict on crash-day inclusion is informative-for-interpretation, not verdict-modifying. The §3.4 hook's purpose is to surface this dependence explicitly.

#### 4.11.2 Channel 3 spike-metric sensitivity companion (inherited verbatim from v1 r2; closes audit L4.5 minor)

The v1 audit fired CONVENTIONS §3.5 (spike-detecting metrics over daily averages for sympathetic-arousal proxies) on Channel 3's choice of `awake_stress_avg` (a mean) when the verbatim Wiggers wording ("stress spikes much faster") suggests a spike-reading. Per Section-4 item-5 closure: add a parallel Mann-Whitney on `stress_high_duration_min` on T+1 (the spike-count companion; chain-T+1 exclusion applies per §4.7) alongside the primary `awake_stress_avg` on T+1.

**Reporting rule**: both readings in the result.md table. If both agree (same verdict direction and approximate effect-size), the average-vs-spike question is closed. If they diverge, the divergence is informative for §9 interpretation.

**Note**: this is a descriptive companion only. The primary Channel 3 metric remains `awake_stress_avg` per the design-MD-locked triad; the spike-companion does NOT promote to a 4th channel.

#### 4.11.3 Channel 3 validate sensitivity arm — chain-T+1 relaxed (added v2 in response to v1 dry-run halt)

The v1 dry-run halted on the §7.5 gate-2 failure for Ch3 validate (n=25 < 30 after the §4.7 chain-T+1 exclusion dropped 16 of 41 heavy-T days). The triage analysis identified Option C — relaxing §4.7 chain-T+1 for validate only — as creating asymmetric chain-discipline (methodologically awkward as a primary), BUT also as reader-useful as a descriptive sensitivity companion. v2 adopts Option C in the latter capacity only.

**Rule** (descriptive sensitivity arm, NOT promoted to primary):

- Compute the Ch3 validate cell with the §4.7 chain-T+1 exclusion **relaxed for the heavy-T arm only**: heavy-T arm n = 41 (NOT 25 — the 16 days where T+1 is also heavy are restored). **Non-heavy-T arm is byte-identical to the primary** (n = 58 in validate; the §4.7 chain rule was always heavy-T-only by construction — it never excluded non-heavy-T days because the rule explicitly says *"EXCLUDE heavy-T days T where exertion_class_lagged_lcera ∈ {heavy, very_heavy} on T+1"*; the non-heavy-T arm has no T+1-is-heavy exclusion to relax). **Construction rule made explicit r2 to address audit Side obs 4**: non-heavy-T arm = natural-pool count after §4.3 + §6 exclusions and T+1 NaN handling per §4.6 (NOT re-paired 1:N per heavy-T day; the comparison stays the standard two-sample Mann-Whitney shape, NOT a paired-test).
- Re-run Mann-Whitney U + Cliff's delta + block-permutation null at E[L]=7 on this relaxed cell.
- Report in `result.md` §10.3 sensitivity block: *"Ch3 validate (chain-T+1 relaxed): n_heavy=41, n_non=58, U=<value>, Cliff's δ=<value>, p_empirical=<value>. Companion to the primary Ch3 validate cell (n_heavy=25, n_non=58, INCONCLUSIVE per §5.4); chain-relaxed values shown for descriptive context only and DO NOT modify the §5.3 verdict."*

**Reading rule**:

- If the chain-relaxed Ch3 validate Cliff's delta agrees in sign and approximate magnitude with the primary Ch1 + Ch2 verdict direction in validate, this is **confirming descriptive context** — the chain rule is doing the binding work; without it the signal is consistent.
- If the chain-relaxed value contradicts Ch1 + Ch2 in validate, this is **conflicting descriptive context** — the chain rule reveals a sub-pattern that the relaxed comparison obscures.
- In NEITHER case does the relaxed value promote to a verdict bar contribution: the primary Ch3 validate cell remains INCONCLUSIVE per §5.4, and the §5.3 channel-3 aggregation applies the CONFIRMED-PARTIAL (0.5) contribution if Ch3 train is SUPPORTED.

**Discipline framing**: per [CONVENTIONS §3.3](../../../CONVENTIONS.md#33-one-column-per-definitional-pair) (column-duplication discipline), the chain-relaxed Ch3 validate is explicitly marked as derived-from the Ch3 validate primary cell with the chain-T+1 rule as the only difference. The two cells are read TOGETHER as one diagnostic, not as two independent verdicts. The relaxed cell does NOT contribute an independent "Ch3 validate confirmed" signal toward the triad sum.

**Honest framing** (per [CONVENTIONS §4.2](../../../CONVENTIONS.md#42-caveats-yes-a-priori-claims-no)): this sensitivity arm was added in v2 in direct response to the v1 dry-run halt on the chain-T+1-excluded n=25 cell. Its design preserves the §4.7 chain rule for the primary verdict (which is the design-MD-inherited choice) while providing the descriptive read on what the cell would look like without the chain rule. The relaxed cell is NOT a halt-avoidance fix; it is a descriptive companion that gives the result.md reader the chain-rule fragility context explicitly.

- **Sister-test cross-reference table**: report HA-C4b's NOT-SUPPORTED verdict + HA11's SUPPORTED-on-train verdict as descriptive context for interpretation. No statistical machinery — just the audit-table.

## 5. Pre-registered falsification criterion

### 5.0 Multi-comparison discipline — triad with pre-specified verdict rule (locked; verbatim from v1)

HA-C4 is a **3-channel confirmatory triad**, NOT a single-cell test. The multi-comparison discipline is provided by the **pre-specified per-channel aggregation + triad verdict rule** (§5.3), which itself is the single-decision-cell at the verdict level.

**Hard rule**: ALL OTHER configurations (other phases, single-channel verdicts, alternative encodings, sensitivity arms including the new §4.11.3 chain-relaxed Ch3 validate) are diagnostic / sensitivity arms ONLY. They are reported in result.md but **none can promote to a SUPPORTED verdict on their own**. The headline verdict is the triad-sum outcome on the unmedicated × triad cell.

### 5.1 Per-channel confirmation bar (applied independently to each of the 3 channels × 2 eras; verbatim from v1)

For each channel × era cell that meets the §5.4 sample-size bar:

**(a) Discrimination**: empirical one-sided p < 0.05 from the block-permutation null at E[L]=7 (per §4.8 step 4 + §4.9).

**(b) Effect size**: Cliff's delta ≥ +0.20 in the predicted direction (heavy-T > non-heavy-T).

**Channel × era SUPPORTED** if BOTH (a) and (b) hold in the predicted positive direction.
**Channel × era REFUTED** if either (a) fails or (b) fails (or the effect is in the wrong direction).
**Channel × era INCONCLUSIVE** if the cell's sample-size bar (§5.4) is not met — independent of (a) / (b), which are not computable on an underpowered cell.

### 5.2 Per-channel confirmation across eras (walk-forward; rewritten in v2)

A channel aggregates its two per-era cells (train + validate) into ONE of three per-channel verdicts:

- **CONFIRMED (1.0 contribution to triad sum)**: SUPPORTED in BOTH train AND validate eras.
- **CONFIRMED-PARTIAL (0.5 contribution)**: SUPPORTED in ONE era AND INCONCLUSIVE in the OTHER era. INCONCLUSIVE blocks full credit but is not refutation — the train + validate pair has only positive evidence with no contradicting era; the missing era simply cannot be evaluated at the locked sample-size bar.
- **REFUTED (0 contribution)**: any other combination — both eras REFUTED, one SUPPORTED + one REFUTED, both INCONCLUSIVE, etc. Mixed evidence or no evidence both fall here.

### 5.3 Triad verdict rule (v2 rewritten with explicit INCONCLUSIVE handling)

The triad sum is the sum of the three per-channel contributions per §5.2 (each channel contributes 0, 0.5, or 1.0). The triad verdict bands:

| triad sum | verdict |
|---|---|
| **3.0** | **SUPPORTED (strong)** — all 3 channels CONFIRMED in both eras |
| **2.5** | **SUPPORTED** — e.g. 2 channels CONFIRMED + 1 channel CONFIRMED-PARTIAL |
| **2.0** | **SUPPORTED** — e.g. 2 channels CONFIRMED + 1 channel REFUTED, OR 1 channel CONFIRMED + 2 channels CONFIRMED-PARTIAL |
| **1.5** | **PARTIAL** — e.g. 1 channel CONFIRMED + 1 channel CONFIRMED-PARTIAL + 1 channel REFUTED, OR 3 channels CONFIRMED-PARTIAL |
| **1.0** | **PARTIAL** — e.g. 1 channel CONFIRMED + 2 channels REFUTED, OR 2 channels CONFIRMED-PARTIAL + 1 channel REFUTED |
| **0.5** | **REJECTED** — e.g. 1 channel CONFIRMED-PARTIAL + 2 channels REFUTED |
| **0.0** | **REJECTED** — all 3 channels REFUTED |

**Verdict rule summary**: triad sum ≥ 2.0 = SUPPORTED; 1.0 ≤ sum < 2.0 = PARTIAL; sum < 1.0 = REJECTED.

**Honest framing per [CONVENTIONS §4.2](../../../CONVENTIONS.md#42-caveats-yes-a-priori-claims-no)** (tightened r2 to address audit Side obs 1): this verdict rule was added in v2 in response to the v1 dry-run halt on Ch3 validate (n=25 < 30 after §4.7 chain-T+1 exclusion). v1 §5.3 already included a 0.5-single-era-confirmation mechanism (v1 "2.0 → SUPPORTED, 1.5 → PARTIAL+, 1.0 → PARTIAL, 0.5 → PARTIAL−, 0 → REJECTED"); v1 §5.4 separately said INCONCLUSIVE channels "do not count toward the triad verdict". **The actual ambiguity v2 resolves** is the interaction between v1 §5.4 and v1 §5.3 when a channel has one SUPPORTED era and one INCONCLUSIVE era — under v1's wording it was unclear whether the channel scored 0.5 (per §5.3's single-era category) or 0 (per §5.4 "do not count"). v2's CONFIRMED-PARTIAL category at 0.5 contribution is the explicit operationalisation that closes this interaction. The rule is **structural** — applies regardless of which channel × era cell turns out INCONCLUSIVE — and treats INCONCLUSIVE as "blocks full credit but is not refutation". The expected v2 outcome under the v1 cell counts (Ch1+Ch2 CONFIRMED both eras + Ch3 train CONFIRMED + Ch3 validate INCONCLUSIVE) would be triad sum = 1.0 + 1.0 + 0.5 = 2.5 → SUPPORTED; the v2 rule absorbs the v1 halt without dropping Ch3 from the triad structurally and without re-calibrating thresholds (the 0.5 contribution + ≥ 2.0 SUPPORTED bar are inherited verbatim from v1's pre-dry-run lock).

### 5.4 Inconclusive bar (locked; verbatim from v1; v2 §5.3 absorbs the formerly halt-triggering condition)

A channel × era cell is **INCONCLUSIVE** if either the heavy-T arm OR the non-heavy-T arm has < 30 days in the era. INCONCLUSIVE cells DO NOT REFUTE; they yield a 0.5 contribution at the per-channel aggregation layer per §5.2 if the OTHER era is SUPPORTED (CONFIRMED-PARTIAL); otherwise they contribute 0 (REFUTED).

**v2 disposition of the v1-halt condition**: v1's §7.5 gate-2 sample-size sanity check fired HALT on Ch3 validate n=25. Per v2 §5.3, this case is now handled at the per-channel aggregation layer (Ch3 train SUPPORTED + Ch3 validate INCONCLUSIVE → Ch3 = CONFIRMED-PARTIAL = 0.5 contribution) rather than halting the test. The §7.5 gate-2 wording (§7.5 bullet 1) is correspondingly clarified to route sub-30-per-arm cells to §5.4 INCONCLUSIVE per §5.3, not to HALT. §7.5 distribution-sanity gates 1 and 3 still HALT on failure per §10.4.

### 5.5 Holm step-down across channels (locked, within-test multiplicity correction; verbatim from v1)

The 3-channel triad p-values per era are corrected for multiplicity via **Holm step-down at α = 0.05**: order the 3 p-values ascending, compare to α/(3 - k + 1) for k = 1, 2, 3. A channel passes Holm if its p-value is below the corresponding cutoff AND all preceding (lower-p) channels also pass.

**Holm result is REPORTED alongside the uncorrected per-channel verdict**; the §5.3 triad rule uses the uncorrected per-channel p-values per the design MD's *"pass-triad-sum"* phrasing. The Holm result is a stricter sensitivity-bar report — if the verdict survives Holm correction, that's stronger; if it doesn't, that's a multiplicity-fragility flag. Holm cannot be computed on a cell that is INCONCLUSIVE (no p-value); that cell is omitted from the Holm step-down ordering.

**Holm with INCONCLUSIVE cells — fewer-comparisons disclosure** (added r2 to address audit Side obs 2). When a channel × era cell is INCONCLUSIVE, the per-era Holm step-down operates on fewer comparisons (2 channels instead of 3) and is therefore **less stringent** than a full 3-channel Holm at the same α: a 2-comparison Holm uses cutoffs α/2 and α/1 (vs. 3-comparison's α/3, α/2, α/1). **The result.md Holm column MUST be annotated explicitly** when this occurs, in the form *"Holm (2-of-2 comparisons; Ch3 validate INCONCLUSIVE)"* — so a reader does not mistake the reduced-stringency Holm for a 3-channel Holm. This is a reporting-discipline requirement; the §5.0 hard rule still binds (Holm is secondary report, not verdict-driving).

## 6. Exclusion rules (locked; verbatim from v1)

- **LC era only**: days before `2022-04-04` are excluded.
- **Unmedicated phase only (primary scope)**: days `>= 2024-04-09` (citalopram start) are excluded from the primary test. Sensitivity arms on later phases are reported separately per §4.4.
- **April 2024 cluster (2024-04-09 → 2024-04-16)**: structurally unanalyzable per [`citalopram_phase_stratification.md`](../../../methodology/citalopram_phase_stratification.md); excluded from all arms.
- **Chain-T+1 (Channel 3 primary only)**: heavy-T days where T+1 is also heavy are excluded from the Channel 3 primary comparison per §4.7. The §4.11.3 sensitivity arm computes Ch3 validate with this exclusion relaxed (descriptive only; not verdict-modifying).
- **Missing exertion classification**: days with `exertion_class_lagged_lcera` NaN are excluded.
- **Channel-specific NaN handling**: per §4.5 + §4.6.

## 7. Expected effect size if hypothesis is true

**§7 anchors inherit verbatim from v1 r2** for §7.1, §7.2, §7.4, §7.5 (computed from `per_day_master.csv` on the `2022-04-04 ≤ date ≤ 2024-04-08` unmedicated filter; source script `c:\tmp\hac4_anchor_query.py` preserved for audit traceability). **§7.3 is rebuilt in v2** with chain-T+1-corrected counts per the v1 dry-run report's surface analysis (the v1 §7.3 missed the 35-day pre-train buffer arithmetic AND did not apply the §4.7 chain-T+1 exclusion that Channel 3 specifically requires).

### 7.1 Per-channel unmedicated-only descriptive distributions — FULL pool, both arms combined (verbatim from v1)

| channel | n (non-NaN) | p25 | p50 | p75 | min | max |
|---|---:|---:|---:|---:|---:|---:|
| Channel 1 — `stress_post_peak_time_to_rest_min` | 603 of 736 (81.9%) | 39 | **81** | 161 | 1 | 842 |
| Channel 1 sec. — `stress_post_peak_drop_avg` | 717 of 736 (97.4%) | 50.1 | **61.0** | 72.3 | 21.5 | 99.8 |
| Channel 2 — `stress_high_duration_min` | 724 of 736 (98.4%) | 41 | **73** | 115 | 0 | 373 |
| Channel 3 — `awake_stress_avg` | 724 of 736 (98.4%) | 41 | **46** | 52 | 21 | 73 |

**Channel 1 NaN fraction (unmedicated-only)**: 18.1% — these are the days where stress never dropped below the 25 "rest" threshold all day (C4-positive cases per [DATA_DICTIONARY §C4](../../../DATA_DICTIONARY.md)). NaN-as-positive encoding per §4.5 captures these in the Mann-Whitney via the 1080-min cap.

### 7.2 Per-channel unmedicated heavy-T vs non-heavy-T descriptives — the comparison arms (verbatim from v1)

| channel | heavy-T n | heavy-T p50 | heavy-T IQR | non-heavy-T n | non-heavy-T p50 | non-heavy-T IQR | descriptive delta (heavy-T − non-heavy-T) |
|---|---:|---:|---|---:|---:|---|---:|
| Channel 1 primary | 201 | 111 | [46, 188] | 343 | 76 | [38, 146] | +35 min |
| Channel 1 sec. (drop_avg) | 243 | 66.1 | [53.7, 79.0] | 405 | 58.6 | [48.1, 69.9] | +7.5 |
| Channel 2 | 247 | 90 | [56, 132] | 407 | 61 | [36, 101] | +29 min |
| Channel 3 | 247 | 49 | [44, 53] | 407 | 45 | [40, 49] | +4 |

**All four channels show the predicted direction (heavy-T > non-heavy-T) at the descriptive level.** Whether the Mann-Whitney + Cliff's delta + block-permutation null clears the §5.1 bar is the test that runs after lock.

**Channel 1 NaN fractions by arm**: heavy-T 18.6% (46/247) vs non-heavy-T 18.1% (76/419) — **essentially tied**. The "C4-positive case" (NaN-as-failure-to-rest) is NOT meaningfully more common on heavy-T days at the unmedicated descriptive level. The 1080-min Mann-Whitney encoding will absorb the NaN observations rank-equivalently across arms; the directional signal comes from the non-NaN distribution shift, not the NaN-fraction contrast. Per §4.11 the descriptive NaN-fraction contrast is reported anyway as a companion.

### 7.3 Per-channel × per-era sample sizes — v2 rebuild with chain-T+1-corrected counts

**v2 §7.3 spec-bug-fix note**: v1's §7.3 asserted train heavy-T n = 206 for Ch1/Ch2 (computed implicitly as 247 unmedicated heavy − 41 validate heavy = 206); this missed the **35-day pre-train buffer** (April–August 2022: Jun=7, Jul=16, Aug=12; total = 35 heavy-T days that are in the unmedicated phase but BEFORE the train-era start of 2022-09-03 per the Stratum-4 boundary). The correct train heavy-T n for Ch1/Ch2 is **n = 171** (= 247 − 41 − 35). v1 §7.3 also did NOT apply the §4.7 chain-T+1 exclusion that Channel 3 specifically requires; v2 §7.3 surfaces the per-channel decomposition explicitly. **This rebuild does NOT change the v1 halt verdict** (the binding §7.5 gate-2 failure was on Ch3 validate, not on train Ch1/Ch2 at 171 vs 206); it is recorded here as an honest spec-bug fix.

| channel | era | heavy-T n (post §4.3 + §4.7) | non-heavy-T n | min arm n | passes §5.4 (≥ 30 both arms)? |
|---|---|---:|---:|---:|:---:|
| Channel 1 | train (2022-09-03 → 2023-12-31) | **171** (= 247 − 41 validate − 35 pre-train buffer) | 314 | 171 | ✓ |
| Channel 1 | validate (2024-01-01 → 2024-04-08) | **41** | 58 | 41 | ✓ |
| Channel 2 | train | **171** (same as Ch1; no chain exclusion) | 311 | 171 | ✓ |
| Channel 2 | validate | **41** | 58 | 41 | ✓ |
| Channel 3 | train | **117** (= 171 − 54 chain-dropped by §4.7) | 311 | 117 | ✓ |
| Channel 3 | validate | **25** (= 41 − 16 chain-dropped by §4.7) | 58 | 25 | ✗ **INCONCLUSIVE per §5.4** |

**Per-channel × per-era cell counts derived from the v1 dry-run computation** (`dry-run-report-v1-archived.md` §7.5 gate 2 table + Failure analysis decomposition); the v1 dry-run code computed these correctly even though the v1 spec text under-stated them.

**Expected v2 outcome on these cell counts** (per v2 §5.3 + §5.4): 5 of 6 channel × era cells pass the sample-size bar and yield SUPPORTED/REFUTED verdicts; 1 cell (Ch3 validate at n=25) is INCONCLUSIVE. If Ch1, Ch2 confirm in both eras AND Ch3 train confirms (with Ch3 validate INCONCLUSIVE), the triad sum = 1.0 + 1.0 + 0.5 = 2.5 → SUPPORTED. If any of Ch1/Ch2 fails in either era, the sum drops accordingly per §5.3. The full-test outcome distribution is structurally unaffected by the §7.3 arithmetic correction; only the descriptive sample-size honesty improves.

### 7.4 Under-SUPPORTED expected effect sizes per channel (verbatim from v1)

Based on the descriptive deltas above + the §5.1 bar (Cliff's delta ≥ +0.20):

- **Channel 1**: heavy-T median 111 vs non-heavy-T 76 → +35 min descriptive delta → Cliff's delta likely in [+0.15, +0.30] range. Borderline on the bar.
- **Channel 2**: heavy-T median 90 vs non-heavy-T 61 → +29 min descriptive delta → Cliff's delta likely in [+0.20, +0.35] range. Likely passes if the distribution shape supports it.
- **Channel 3**: heavy-T median 49 vs non-heavy-T 45 → +4-point descriptive delta on a 0-100 scale → Cliff's delta likely in [+0.10, +0.25] range. **At-risk for the +0.20 bar**; the precise value depends on within-group variance. The descriptive direction is correct but the magnitude is modest.

The block-permutation p-value test is structurally separate from the effect-size bar; both must pass per §5.1. The descriptive deltas suggest Ch2 is most likely to confirm, Ch1 is borderline, Ch3 is at-risk for the effect-size bar. Whether the triad-sum threshold for SUPPORTED is met is the test that runs after lock.

### 7.5 Sanity gate (verbatim from v1, with one v2 wording clarification on gate 2 routing)

- **Sample size** (gate 2; v2 clarified): per-channel × per-era arm has ≥ 30 days post-§4.3 + §4.7 exclusions. If a cell has < 30 per arm, it is INCONCLUSIVE per §5.4 + §5.3 (CONFIRMED-PARTIAL if the OTHER era is SUPPORTED, else REFUTED). **Sub-30 cells DO NOT halt the test** (this is the v2 disposition of the v1 halt condition); only distribution-sanity failures (gates 1, 3 below) halt.
- **Distribution check** (gate 1): per-channel median of the FULL unmedicated-only pool (heavy-T + non-heavy-T combined) falls within **±30% of the §7.1 reference**:
  - Ch1: 81 ± 30% = [56.7, 105.3]
  - Ch1 sec.: 61.0 ± 30% = [42.7, 79.3]
  - Ch2: 73 ± 30% = [51.1, 94.9]
  - Ch3: 46 ± 30% = [32.2, 59.8]
- **Channel 1 NaN-fraction sanity** (gate 3): the unmedicated NaN fraction falls within [12%, 25%] (descriptive baseline ~18%; tolerance widened to absorb sampling variation across re-extracts).
- If gate 1 or gate 3 fails → halt + revise → HA-C4-v3 per [`hypothesis_lock_process.md` §3.9](../../../methodology/hypothesis_lock_process.md#39-run-step-post-lock). Gate 2 sub-30 cells route to §5.4 INCONCLUSIVE per §5.3 (NOT halt).

## 8. Caveats `result.md` must explicitly acknowledge

**v2-specific caveats (added in response to the v1 dry-run halt)** — highest priority surface in result.md:

1. **v1 → v2 transition disclosure**: v1 (LOCKED 2026-06-17 r2) was dry-run-halted on Ch3 validate n=25 < 30 (per §4.7 chain-T+1 exclusion dropping 16 of 41 validate heavy-T days); v1 §5.3 had no explicit INCONCLUSIVE-handling rule so the cell broke the binary triad logic. v2 §5.3 introduces explicit handling: INCONCLUSIVE cells contribute 0.5 (CONFIRMED-PARTIAL) at the per-channel aggregation layer when the OTHER era is SUPPORTED, blocking full credit but not refuting. The Wiggers 3-channel triad structure is preserved; Ch3 is NOT dropped from the triad. The v1 halt was the locked-pre-reg discipline working exactly as designed; v2 is the corrective draft.

2. **§7.3 arithmetic spec-bug fix (honest disclosure)**: v1 §7.3 implicitly assumed the 35-day pre-train buffer (Apr–Aug 2022 unmedicated heavy-T days) was already excluded from the heavy-T count; it asserted train heavy-T n = 206 when the correct value is n = 171. v2 §7.3 corrects this AND adds the per-channel chain-T+1 decomposition. The bug-fix does NOT change the v1 halt verdict (the binding §7.5 gate-2 failure was on Ch3 validate, not on train Ch1/Ch2 at the corrected n=171, which comfortably clears the ≥30 bar). Recorded here as an honest spec-bug fix per [CONVENTIONS §4.2](../../../CONVENTIONS.md#42-caveats-yes-a-priori-claims-no).

3. **§4.11.3 sensitivity arm framing (chain-T+1 relaxation)**: the v2 §4.11.3 chain-relaxed Ch3 validate cell (n=41) is **descriptive sensitivity only**; it does NOT promote to the primary verdict. The §4.7 chain-T+1 rule is preserved for the headline because asymmetric chain-discipline (relaxing for validate only) is methodologically awkward as a primary. The reader sees what the cell would look like without the chain rule, but the primary verdict honors the chain rule. Per [CONVENTIONS §3.3](../../../CONVENTIONS.md#33-one-column-per-definitional-pair) the relaxed cell is marked as derived-from the primary Ch3 validate cell; the two read together as one diagnostic.

4. **Audit-Layer-2.5 v2 disposition (pragmatic-pre-registration acknowledgment)**: v2 was drafted with knowledge that Ch3 validate has the n=25 boundary issue + Ch3 train passes at n=117. The triage analysis (which option to choose from the five identified in the v1 dry-run report) was done in a separate fresh session per [`hypothesis_lock_process.md` §3.2](../../../methodology/hypothesis_lock_process.md#32-drafting-step-step-1-of-the-arc); this drafting session was given only the composite-path recommendation and no per-day data values from the v1 test (the v1 full run never executed because of the halt). The §3.2-clause shared-context concern from v1 r2 (user-accepted as priced-in per audit L2.5 disposition) remains the documented boundary; v2 does not introduce new exposure to per-day per-channel values. A strict reviewer may still object on the principle that drafting v2 with knowledge of the v1 halt (rather than blind to the cell counts) is a pragmatic pre-registration position; this is the v2.3-style discipline-stretch acknowledgment.

5. **Power-calc dispatch** (per [`hypothesis_lock_process.md` §3.8 gate 1](../../../methodology/hypothesis_lock_process.md#38-lock-step-stage-5-of-the-arc)): power calculation is inapplicable per [Daza 2018](../../../literature/methodology/daza_2018_self_tracked_n_of_1_counterfactual.pdf) within-subject design — the n-of-1 corpus does not have separate treatment and control arms in the classical sense. The block-permutation null at E[L]=7 (§4.9) is the within-subject inferential machinery; the §5.1 (a) discrimination + (b) effect-size gates determine per-channel confirmation rather than a power-thresholded p-value. The new §5.3 INCONCLUSIVE handling does NOT introduce a separate power-calc requirement: the ≥30-per-arm sample-size bar (§5.4) inherits from v1, and the INCONCLUSIVE outcome at sub-30 is the operational definition of "underpowered for this cell" rather than a hidden additional power computation.

**v1 caveats (inherited verbatim from v1; valid for v2)**:

- **Drafting under shared-context with HA-C4b test session** (per v1 §Authorship, permanently archived in [`hypothesis-v1-archived.md`](hypothesis-v1-archived.md)). The data-exposure boundary is documented: the v1 drafter knew the identity of 10 heavy-T days that are also crash episodes; the drafter had NOT seen the HA-C4 channel values on individual days. The fresh-session audit ([`reviews/HA-C4-v1-2026-06-17.md`](../../../reviews/HA-C4-v1-2026-06-17.md)) was the integrity check on §4 / §5 operational choices. **The user explicitly accepted at v1 r2 absorption (2026-06-17) that the §3.2-clause shared-context drafting concern is priced in** per audit L2.5 Section 4 item-6 option (a). v2 inherits this disposition; the §4.11.1 crash-drop sensitivity arm (inherited verbatim) further insulates the spec from "drafter knew the crash IDs and silently chose not to test sensitivity" concerns.

- **NaN-as-positive encoding for Channel 1** (§4.5): the 1080-min coding is one operationalisation; the NaN-fraction descriptive contrast (§4.11) is the alternative. Result.md must report both. If the verdict depends on the encoding choice, flag as encoding-fragile.

- **Chained-regime adjustment for Channel 3** (§4.7): heavy-T-followed-by-heavy-T+1 days are excluded from the Channel 3 primary. This reduces the heavy-T sample size in Channel 3 (train 117 of 171; validate 25 of 41). The v1 dry-run confirmed that this exclusion drops Channel 3 validate below the §5.4 inconclusive bar; v2 §5.3 + §4.11.3 explicitly handle this case (CONFIRMED-PARTIAL contribution at the channel-aggregation layer; chain-relaxed descriptive sensitivity arm in the result.md).

- **Citalopram dose-modulation** (§4.4): the primary scope is unmedicated only specifically to avoid the dose-confound on the stress channel. Cross-phase sensitivity arms require §5.B dose-adjustment per [`citalopram_phase_stratification.md`](../../../methodology/citalopram_phase_stratification.md). This pre-reg does not attempt cross-phase aggregation.

- **No motion filter** (unlike HA-C4b): HA-C4 tests `awake_stress_avg`, `stress_high_duration_min`, and `stress_post_peak_time_to_rest_min` without conditioning on motion. The Garmin-stress-is-partly-motion-sensitive caveat applies (per [`hrv_proxy_via_stress.md §2`](../../../methodology/hrv_proxy_via_stress.md#2-how-garmin-stress-is-derived)); some of the channel signal may be motion-artefact rather than true sympathetic load. Result.md must acknowledge this and cross-reference HA-C4b's motion-filter test.

- **Unmedicated = pre-citalopram corpus, not "no medication overall"**: the participant had other lived-experience interventions in the 2022-04 → 2024-04 window (CPAP started 2024-01-10; daily pacing protocols evolved through this period; ergotherapy program 2022-06-17 → 2023-03-10; PWC reintegratie 2023-03-06 → 2023-11-28). The unmedicated headline is "no SSRI" not "no intervention". The §4.1 heavy-T classification absorbs the gross exertion effect; finer-grained context lives at the result.md interpretation layer.

- **Pacing-behaviour confounder (inherited from HA-C4b v3 §8)**: `exertion_class_lagged_lcera` captures physical exertion only. Cognitive, emotional, and orthostatic exertion are not in the classification. A "non-heavy-T" day in this test could include high cognitive / emotional load days that are physiologically demanding. The C4 pattern may appear on those days too; mis-classifying them as non-heavy-T arm would dilute the heavy-T vs non-heavy-T contrast (i.e. bias toward NULL / NOT-SUPPORTED). Result.md must note this as a directional bias toward false-NOT-SUPPORTED.

- **Single-subject n=1**: thresholds in §5.1 (p < 0.05, |delta| > 0.20) are calibrated to the participant's distribution. The Mann-Whitney is non-parametric so the threshold-on-effect-size choice is the binding decision; the alternative (a stricter Cliff's delta threshold like 0.33 for "medium" effect) would shift the gate.

- **HA11 / HA-C4b cross-references**: HA11 SUPPORTED on the inverse (U-dip = sharp drop) signal; HA-C4b NOT-SUPPORTED on the motion-filtered crash-precursor framing. HA-C4 SUPPORTED would complete the picture (the failure-to-recover signal IS detectable at the descriptive level even though the crash-precursor framing didn't pan out). HA-C4 REJECTED would shrink the C4-mechanism reading further. Result.md must surface this triangulation.

- **The block-permutation null preserves the heavy-T autocorrelation structure but breaks the heavy-T → channel relationship**. Under the null, the heavy-T labels are reshuffled in blocks while channel values stay fixed; this tests "is the observed difference larger than what random block-permutation produces?" The empirical p-value is the appropriate within-subject inferential statistic.

## 9. What we do with each outcome

### 9.1 SUPPORTED strong (triad sum = 3.0)

All 3 channels CONFIRMED in BOTH train AND validate eras. The Wiggers C4 pattern is empirically confirmed at the **pattern-existence level** on this corpus at all three temporal scales: same-day decay failure (Ch1), walls of orange (Ch2), and next-day reactivity (Ch3). This is the strongest verdict: every channel's predicted directional shift survives both the discrimination bar and the effect-size bar in both eras independently.

### 9.2 SUPPORTED (triad sum = 2.0 or 2.5)

The Wiggers C4 pattern is empirically confirmed at the pattern-existence level with one channel either REFUTED or CONFIRMED-PARTIAL. The specific channel breakdown is reported as **verdict-invariant descriptive labels** (per v1 audit L4.7 closure, inherited):

- **Triad sum = 2.5**: 2 channels CONFIRMED + 1 channel CONFIRMED-PARTIAL (one era SUPPORTED, other era INCONCLUSIVE). Example: Ch1 + Ch2 CONFIRMED both eras + Ch3 train SUPPORTED + Ch3 validate INCONCLUSIVE — the expected v2 outcome under the v1 cell counts if Ch1/Ch2 confirm.
- **Triad sum = 2.0**: 2 channels CONFIRMED + 1 channel REFUTED; OR 1 channel CONFIRMED + 2 channels CONFIRMED-PARTIAL. Different operational configurations both yield SUPPORTED; the result.md author interprets the specific configuration against observed magnitudes + sister-test context.

**Cross-reference downstream** (verdict-invariant):

- **HA-C4 SUPPORTED + HA-C4b NOT-SUPPORTED** (the actual cross-result expected from HA-C4b v3): the Wiggers pattern exists but isn't a per-episode crash precursor at the motion-filtered operationalisation. This is the **protective-rather-than-predictive** alternative reading from HA-C4b §9, now with corroborating evidence — the pattern Wiggers describes IS real on this corpus, but the participant's real-time use of it as a pacing trigger prevents the crashes the precursor test would have caught.
- **HA-C4 SUPPORTED + HA11 SUPPORTED-on-train (U-dip)**: the autonomic-recovery story is multi-channel-confirmed: both the U-dip (calm-day signal) and the failure-to-recover (heavy-day signal) work as expected on this corpus.
- **Downstream synthesis**: [`garmin_pacing_practice.md`](../../../methodology/garmin_pacing_practice.md) may strengthen the §3.3 rest-stress trigger's standing from "operational heuristic" to "empirically-confirmed pattern".

### 9.3 PARTIAL (triad sum = 1.0 or 1.5)

The C4 pattern shows partial signal but not the SUPPORTED bar. Specific descriptive labels:

- **Triad sum = 1.5**: 1 channel CONFIRMED + 1 channel CONFIRMED-PARTIAL + 1 channel REFUTED; OR 3 channels CONFIRMED-PARTIAL. One scale of the Wiggers C4 claim shows full signal with another partial; the third either contradicts or is missing.
- **Triad sum = 1.0**: 1 channel CONFIRMED + 2 channels REFUTED; OR 2 channels CONFIRMED-PARTIAL + 1 channel REFUTED. One temporal scale stands; the others don't.

PARTIAL outcomes are descriptively informative but don't carry the SUPPORTED-bar weight for downstream protocol claims. The result.md author names which specific channel(s) confirmed and at what era; readers interpret against observed magnitudes.

### 9.4 REJECTED (triad sum < 1.0)

All 3 channels REFUTED (sum = 0), OR 1 channel CONFIRMED-PARTIAL and 2 REFUTED (sum = 0.5). The Wiggers C4 pattern does NOT show systematic post-exertion degradation at the descriptive level on this corpus. This is a meaningful finding: either the pattern doesn't exist on this participant, OR the heavy-T classification doesn't capture the right exertion threshold, OR the protocol-disturbance from active pacing has flattened the signal entirely.

**Cross-reference downstream**: REJECTED + HA-C4b NOT-SUPPORTED + HA11 SUPPORTED-on-train would mean: the Wiggers C4 framework doesn't operationalise cleanly on this corpus at either the descriptive or precursor level, but the U-dip (HA11) sister channel does. The C4 mechanism question would need different operationalisation (e.g. bout-level recovery curves per the synthesis discussion) to be testable.

### 9.5 Sensitivity-arm divergence

- **§4.11 `stress_post_peak_drop_avg` companion diverges from primary Ch1**: the Ch1 result is encoding-fragile; flag for review.
- **§4.11 `stress_recovery_pct_within_2h` companion diverges from primary Ch1**: the slow-but-complete-vs-fast-then-stall distinction is doing analytical work; flag for descriptive write-up.
- **§4.7 chain-T+1-excluded Ch3 diverges from chain-included Ch3** (Ch3 sensitivity arm per §4.7 last paragraph): the chained-regime sequences are doing analytical work; report both.
- **§4.11 NaN-fraction contrast for Ch1 disagrees with 1080-encoded Mann-Whitney**: the encoding choice matters more than the underlying signal; report both with explanatory paragraph.
- **§4.11.1 crash-drop sensitivity surfaces |Δ Cliff's delta| > 0.10 on any channel** (per CONVENTIONS §3.4): the channel's signal is crash-driven, not robust across the broader heavy-T pool. Verdict per §5.3 is unchanged; the dependence is informative-for-interpretation.
- **§4.11.2 Ch3 spike-companion (`stress_high_duration_min` on T+1) diverges from primary Ch3 (`awake_stress_avg` on T+1)**: the average-vs-spike question matters for the next-day-reactivity reading; the divergence is informative for §9 interpretation per the CONVENTIONS §3.5 spike-preference framing.
- **§4.11.3 Ch3 validate chain-relaxed cell (n=41) diverges from primary Ch3 validate (n=25 INCONCLUSIVE) in directional implication** (new v2 sensitivity arm): the chain rule is doing binding analytical work; the chain-relaxed cell shows what the validate-era Ch3 signal looks like without the §4.7 discipline. Per §4.11.3, this divergence is descriptive context only; it does NOT modify the primary verdict per §5.3. If the chain-relaxed Ch3 validate signal agrees with Ch1 + Ch2 validate direction, it is confirming descriptive context; if it conflicts, it is conflicting descriptive context. Report both.

### 9.6 Spec sanity-check fails on dry-run (v2 disposition)

Per v2 §7.5 + §10.4 (inherited from v1 with the gate-2 clarification):

- **Gate 1 (distribution check) fails** (full-pool channel median outside ±30% of §7.1 reference): DO NOT run the full test. Document the failure in the dry-run report; revise the spec creating HA-C4-v3 with this pre-reg archived as v2 per [`hypothesis_lock_process.md` §3.9](../../../methodology/hypothesis_lock_process.md#39-run-step-post-lock).
- **Gate 3 (NaN-fraction sanity) fails** (Ch1 NaN fraction outside [12%, 25%]): same as gate 1 — halt + revise → HA-C4-v3.
- **Gate 2 (sample-size sub-30 per arm in any cell) — v2 NEW behaviour**: this is NOT a halt trigger. The cell routes to §5.4 INCONCLUSIVE per §5.3; per-channel aggregation handles via CONFIRMED-PARTIAL (0.5) if the OTHER era is SUPPORTED, else REFUTED (0). The test proceeds to full run. **This is the explicit v2 closure of the v1 halt condition.**

## 10. Detection script architecture

### 10.1 Stage 1 — data (already done; verbatim from v1)

All channel columns and the heavy-T classification are already in `$GEVOELSCORE_DATA_PATH/unified/per_day_master.csv`. No new extraction needed.

### 10.2 Stage 2 — test (`HA-C4/test.py`, to be written post-lock in a separate session)

Loads `per_day_master.csv`, applies §4 eligibility filtering (LC era + unmedicated phase + April 2024 exclusion + non-NaN channel values + heavy-T classification non-NaN), computes per-channel × per-era Mann-Whitney U + Cliff's delta + block-permutation p-value at E[L]=7, applies §5.3 v2 INCONCLUSIVE-aware triad verdict rule + §5.5 Holm step-down correction across non-INCONCLUSIVE channels. Implements §4.11.1 crash-drop sensitivity arm, §4.11.2 Ch3 spike-companion, and the new §4.11.3 Ch3 validate chain-relaxed sensitivity arm.

**Spec-sanity-gate at dry-run** (v2 routing):
- Gate 1: full-pool channel medians within ±30% of §7.1 reference → halt on failure.
- Gate 2 (v2 NEW): cells with < 30 per arm route to §5.4 INCONCLUSIVE per §5.3 (NOT halt). The dry-run report names the INCONCLUSIVE cell(s) explicitly.
- Gate 3: Ch1 NaN fraction within [12%, 25%] → halt on failure.

**Seed**: `RANDOM_SEED = 20260618` (v2; distinct from v1's `20260617`) for reproducibility.

### 10.3 Stage 3 — `result.md`

Reports the triad verdict block at top (one cell: the triad sum + the v2 §5.3 verdict band — SUPPORTED-strong / SUPPORTED / PARTIAL / REJECTED), followed by per-channel × per-era contingency tables with (a) p-value, (b) Cliff's delta, (c) Holm-corrected p-value, (d) per-cell verdict (SUPPORTED / REFUTED / INCONCLUSIVE). Then secondary descriptive outcomes per §4.11 (drop-avg companion, recovery-pct companion, NaN-fraction contrast, §4.7 chain-T+1 sensitivity, §4.11.1 crash-drop sensitivity, §4.11.2 Ch3 spike-companion, **§4.11.3 Ch3 validate chain-relaxed sensitivity arm — descriptive only, marked as derived-from primary Ch3 validate cell per §4.11.3**). Then sister-test cross-reference table. Caveats per §8 including the v2-specific caveats prominent at top + the data-exposure context disclosure.

### 10.4 Run protocol (verbatim from v1, with v2-version-number update)

1. **Dry-run** (`python test.py --dry-run`): prints sample sizes per channel × era × arm; checks §10.2 sanity gates. **If gate 1 or gate 3 fails → halt + revise spec → HA-C4-v3.** Gate 2 sub-30 cells DO NOT halt; they route to §5.4 INCONCLUSIVE per §5.3 (v2 NEW behaviour).
2. **Full run** (`python test.py`): emits `result.md` + `result-data.json` directly into this folder.
3. **No iteration on the spec after the dry-run passes.** Any post-dry-run revision creates HA-C4-v3 with the v2 result archived.

---

*Pre-registration drafted 2026-06-18 by Claude (Opus 4.7) in reviewer-mode-with-authorization per a fresh-session handoff brief (composite-path recommendation from the v1 dry-run-report triage section). Per [`hypothesis_lock_process.md` §3.2](../../../methodology/hypothesis_lock_process.md#32-drafting-step-step-1-of-the-arc) drafting permitted; the data-exposure boundary is documented in the v1 Authorship block (permanently archived in [`hypothesis-v1-archived.md`](hypothesis-v1-archived.md)); v2's structural changes do not depend on per-day data values. The fresh-session [§3.4 audit](../../../reviews/) is the next stage of the v2 lock arc. Lock requires user acceptance + audit clearance + the four §3.8 gate confirmations.*
