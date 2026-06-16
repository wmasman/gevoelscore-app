# HA-C4b v2 — Stress-with-low-motion minute count as crash precursor (Wiggers C4 + motion filter), headline relocked to unmedicated pooled

## Authorship

**Drafted 2026-06-15** by Claude (Opus 4.7) in reviewer-mode-with-authorization per [CONVENTIONS §1.2](../../../CONVENTIONS.md#12-reviewer-mode-claude-reads--critiques--explains-does-not-edit-unless-asked). Authorising user: Willem. **Fresh-session drafting** per [`hypothesis_lock_process.md` §3.2](../../../methodology/hypothesis_lock_process.md#32-drafting-step-step-1-of-the-arc) — no shared context with v1's dry-run session (which had executed `test.py --dry-run` and seen per-episode z-scores on actual crash lead-up windows; per [`hypothesis_lock_process.md` §3.3](../../../methodology/hypothesis_lock_process.md#33-optional-post-draft-revision-r1-data-exploration-absorption) that level of data exposure permits only operationalisation refinements, not the headline-cell relock that is v2's whole point). Fresh-session handoff was the contamination-prevention mechanism.

**v2 trigger**: v1's dry-run halt on 2026-06-15 fired three §7 sanity gates:
- `consolidation x train` n = 0 (by phase-boundary construction; consolidation phase starts 2024-06-20, train ends 2023-12-31 — zero overlap; the locked headline cell was unsatisfiable for the train arm by arithmetic).
- `consolidation x validate` n = 5 (below the §5.3 inconclusive bar of n ≥ 10 after §4.2 exertion-conditioning + §4.3 1b.i validity + §6 buildup-buffer).
- `unmedicated` median primary = 78 minutes (outside v1's §7 anchor range of [15, 60] — calibration miss; v1's anchor was bound to a definitional cousin's distribution rather than to the exact column being measured).

v1 archived at [`hypothesis-v1-archived.md`](hypothesis-v1-archived.md) (locked at commit `80607e4`, halted at dry-run 2026-06-15). v1's [dry-run report](dry-run-report.md) records the halt analysis (eligible-n + median-predictor tables only; per-episode z-scores held out from this v2 drafting session per the fresh-session handoff). v1's locked spec stands as the audit-able predecessor; this v2 references it as the inherited baseline rather than re-stating its sections.

**v2 deltas from v1 r3** (localised; v2 inherits everything else wholesale):

- **§1 Claim** relocked to the unmedicated phase (was: consolidation). The Wiggers-C4 "stuck sympathetic / walls of orange" pattern should be MOST visible in the unmedicated phase — citalopram's stress-channel suppression (per [`citalopram_dose_response §5.6`](../../../methodology/citalopram_dose_response_stress_mean_sleep.md#56-v3-amendment--multi-channel-confirmation-added-2026-06-14)) is absent there. Different prior than v1's consolidation framing, but mechanistically defensible.
- **§3 labels CSV path** corrected per the [README v2-must-inherit fix](README.md): v1 cited `crash_v2-definition/labels_crash_v2.csv` for the labels source; the in-repo path holds the **scheme definition MD only**, not the labels CSV. The labels CSV lives at `$GEVOELSCORE_DATA_PATH/processed/crash_labels/labels_crash_v2.csv` per the project privacy boundary. v2's §3 (and §4.5 baseline cross-reference) cites the external CSV path with the in-repo `crash_v2-definition/definition.md` cited separately for the scheme.
- **§4.4 headline-verdict sentence** updated to point at the unmedicated phase (was: consolidation). The phase table itself + the buildup-buffer + the afbouw-merge prose are unchanged.
- **§5.0 single-cell headline lock** re-pointed to: `unmedicated phase × pooled train + validate × S60_Mlow × N_std = 1.5 × primary 4d × one-sided elevated`. The both-eras-independent rule is **abandoned for this hypothesis** — pooling train (n = 8) + validate (n = 2) within the unmedicated phase reaches n = 10, just clearing the §5.3 inconclusive bar. The both-eras rule was a v1 inheritance from the consolidation framing; for v2's unmedicated headline it would force the entire test inconclusive (validate-unmedicated has n = 2 alone). Documented in §5.3.
- **§5.1 (b-interp) worked example** updated to use unmedicated-phase illustrative numbers (was: consolidation). The (a)+(b)+(c) bar shape + RD/OR reporting machinery is unchanged.
- **§5.3 inconclusive bar** updated: pooled-headline n = 10 is the gate. Validate-unmedicated alone (n = 2) is **pre-declared INCONCLUSIVE** — reported in the result.md as a descriptive directional-consistency companion to the pooled headline, with no SUPPORTED-bar weight or NOT-SUPPORTED weight independently. Train-unmedicated alone (n = 8) is **pre-declared INCONCLUSIVE** under the same rule — below the n ≥ 10 bar individually; reported as a descriptive companion only. The pooled cell is the only SUPPORTED-bar-driving arm.
- **§7 sanity ranges** re-anchored against the exact column's per-phase descriptive card (raw column, no §4.3 eligibility restriction): [`$GEVOELSCORE_DATA_PATH/analyses/stress_low_motion_descriptive/per_phase_card.md`](file://$GEVOELSCORE_DATA_PATH/analyses/stress_low_motion_descriptive/per_phase_card.md), reproducible from [`docs/research/analyses/garmin_exploration/stress_low_motion_viz/per_phase_descriptive.py`](../../garmin_exploration/stress_low_motion_viz/per_phase_descriptive.py). Pre-cit / unmedicated phase: n = 725 day-rows, median 76, IQR [48, 114], min 0, max 364, mean 86.6, std 53.6. Replaces v1's `[15, 60]` anchor which was a definitional-cousin miss.
- **§8 power-calc dispatch** added per [`hypothesis_lock_process.md` §3.8 gate 1](../../../methodology/hypothesis_lock_process.md#38-lock-step-stage-5-of-the-arc): "power calc inapplicable per [Daza 2018](../../../literature/methodology/daza_2018_self_tracked_n_of_1_counterfactual.pdf) within-subject design". v1 lacked this dispatch (the lock-process MD landed after v1 r3); v2 closes the §3.8 gate explicitly.
- **§8 v1→v2 transition caveat** added: the relock from consolidation to unmedicated is a substantive prior-shift; multi-comparison + researcher-degrees-of-freedom concerns from the relock are surfaced as a caveat the result.md must explicitly acknowledge.
- **§9 outcome branching** rewritten for the unmedicated-pooled headline cell. Other phases (consolidation n = 5 validate, buildup n = 2 validate, afbouw n = 2 validate; train arms empty by phase-boundary construction) are all pre-declared INCONCLUSIVE / descriptive companions — none promote to SUPPORTED.
- **§4.11.5 episode-level leave-one-out fragility check** added as a v2-specific secondary descriptive outcome. At pooled n = 10 a single episode is worth 10 percentage points on the (a) gate, so verdict stability is a real concern. The LOO check drops one episode at a time, recomputes the headline numbers on n = 9, reports the range across all 10 LOO drops, and flags any single episode whose removal would flip the (a) verdict. Descriptive only (no SUPPORTED-bar weight) — fits the [lock-process §3.7](../../../methodology/hypothesis_lock_process.md#37-optional-r3-interpretability-augmentation) "reporting layer not approach change" heuristic and doesn't trigger a new audit gate.

**v2 inherits the following sections from v1 r3 verbatim** (cited but not restated below; read v1-archived for the locked content):
- §2 Why we think this — Wiggers C4 framing + lived-experience motion-filter + Session E construct validity. The "consolidation plateau" rationale shifts in v2 (see §1 / §4.4); the underlying claim is unchanged.
- §4.1 Predictor primitive (`stress_low_motion_min_count_S60_Mlow`).
- §4.2 Exertion-conditioning rule.
- §4.3 Day validity (1b.i ≥ 900 total in-range stress samples + 1b.ii wake-window quartile coverage).
- §4.5 Lagged personal baseline (`[d − 90, d − 30]` LC-era + same-phase restricted; trimmed mean; σ ≤ 5 flag).
- §4.6 Per-day z-score.
- §4.7 Per-episode lead-up profile (4d primary / 5d secondary).
- §4.8 Threshold N_std tiers (1.5 / 2.0 / 2.5).
- §4.9 Null sample (stationary bootstrap with E[L] = 7, B = 10,000 headline + B = 1,000 sensitivity; seed `20260615`; per-phase eligible pool; `E[L]*` companion + factor-of-2 flag).
- §4.10 Sensitivity ladder (6 unique columns + 3 identical-by-construction duplicates).
- §4.11 Secondary descriptive outcomes (same-day Spearman with crash-drop sensitivity row; primary disambiguation vs `stress_high_duration_min` ρ = 0.79; secondary vs HA11 `u_dip_count` ρ = 0.556; respiration-companion sensitivity).
- §6 Exclusion rules (buildup `< 2024-04-30` strict buffer; 2024-04-09 to 2024-04-16 unanalyzable cluster; null-sample contamination guard).

**Revision 2026-06-15-r2** (post-audit, shared-context with drafting per [`hypothesis_lock_process.md` §3.5](../../../methodology/hypothesis_lock_process.md#35-revise-step-stage-3-of-the-arc-r2--the-bulk-of-methodological-strengthening)). Three changes absorbed from the [fresh-session `/research-review` audit report](../../../reviews/HA-C4b-v2-2026-06-15.md) (verdict: **PASS with caveats** — one Layer-1 minor fire + three Section-4 polish recommendations, no approach changes). The audit also confirmed itself as the canonical §3.6 re-audit step (its target was r2-equivalent v2 drafting, second-pass discipline implicit). All three closures are wording / sentence-additions, no new conjuncts or machinery — they fit the [§3.7 reporting-layer-not-approach-change heuristic](../../../methodology/hypothesis_lock_process.md#37-optional-r3-interpretability-augmentation) and do NOT trigger a new audit gate:

- **§2 self-readability polish** (closes L1.5 Layer-1 minor fire). Added a "Why each inherited v1 r3 motivation still favours unmedicated as the v2 headline phase" sub-block immediately after the §2 wrapper sentence — three bullets tracing (i) Wiggers C4's uninhibited-sympathetic-regulation assumption against the §5.6-confirmed citalopram suppression cascade, (ii) the four sibling SUPPORTED autonomic-deviation precursors (H02b / H02d / HA06b / HA11) all firing in train (which is entirely inside the unmedicated phase), (iii) the Session E construct-validity ρ values being phase-agnostic. Closes the audit's concern that §2 in isolation could read as v1-consolidation-framing.
- **§7 σ-range lower-bound anchor** (closes audit side observation 1). Replaced the hand-wavy "the lagged baseline typically narrows this somewhat" with explicit anchor wording: the [25, 55] range brackets v1's dry-run-observed σ_median = 33.4 with a margin-below to 25 and the raw 53.6 just above. The 25 lower bound is now an explicit margin-below of the observed median, not an estimate.
- **§4.11.5 boundary-fragility note** (closes audit side observation 3). Added a structural-observation block describing the k = 6 / k = 7+ / k ≤ 5 LOO behaviour at the n = 10 (a)-gate boundary: an empty load-bearing list is not "no fragility detected" but a boundary-distance signal. v2 reports this in result.md so the empty-list case is interpreted correctly.

The audit's side observation 2 (partial closure of v1 audit's external-viz citations) is acknowledged but not addressed in this r2 — the audit's own §4.4 recommendation #4 explicitly labels this "not load-bearing for v2", and consolidating the external viz-notes into a single in-repo summary is a separate documentation task. Queued in §3.5 propagation-discipline style:

### Pending v3 fixes (queued per §3.5 propagation discipline)

- **External viz-notes citations in §4.3 + §4.11**. v2 §3 + §7 closed the §7 anchor to in-repo; §4.3 (Family A 2024-11-26 case) and §4.11 (Family D2a ρ = 0.79, Family D2b) still cite `$GEVOELSCORE_DATA_PATH/analyses/stress_low_motion_viz/viz-notes.md` outside the audit-able tree. v3 (or a parallel documentation commit) should consolidate into `analyses/garmin_exploration/stress_low_motion_viz/key-findings.md` so the next fresh-session reviewer can verify the cited values without leaving the repo. Source: HA-C4b v2 audit 2026-06-15 §4.4 recommendation #4.

**Status: LOCKED 2026-06-16 by user acceptance.** The pre-registration is locked at the state of revision r2 (this file's HEAD). The [v2 audit](../../../reviews/HA-C4b-v2-2026-06-15.md) served as the canonical fresh-session §3.6 re-audit step — verdict PASS with caveats, all three caveats (audit Section 4 items 1-3) closed in r2 as wording-only sentence additions per the [`hypothesis_lock_process.md` §3.6 compression criteria](../../../methodology/hypothesis_lock_process.md#36-re-audit-step-stage-4-of-the-arc) (mechanical sentence additions / wording tightenings, no architectural change, no new statistical machinery; further re-audit after r2 NOT required). The four [§3.8 lock-blocking gates](../../../methodology/hypothesis_lock_process.md#38-lock-step-stage-5-of-the-arc) all pass:

1. **Power-calc dispatch present in §8** — Daza 2018 within-subject design citation; block-permutation null at E[L]=7 named as the within-subject inferential machinery.
2. **Single-cell headline lock** — §5.0 retargets to `unmedicated × train+validate pooled × S60_Mlow × N_std=1.5 × primary 4d × one-sided elevated`; hard rule preserved verbatim from v1 r3.
3. **Register-row pointer added** — [`wiggers_testable_hypotheses.md` C4b row line 285](../../../wiggers_testable_hypotheses.md) status cell now carries a forward pointer to this v2 + v1-archived pre-reg; register row is generic at the headline-cell level so this is non-supersession of operational anchor + caveats, just navigation.
4. **Re-audit completed clean** — the [v2 audit](../../../reviews/HA-C4b-v2-2026-06-15.md) is the canonical §3.6 re-audit (verdict PASS with caveats; all three caveats closed in r2).

Further modifications create HA-C4b-v3 with v2 archived per the locked-pre-reg discipline. The next session writes `test.py` + runs + emits `result.md` per §10 — **the test-writing session must be a fresh session** because the v1 dry-run produced per-episode z-scores on the same predictor column that contaminate any same-context v2 test implementation (the same fresh-session discipline that produced the v2 draft applies to the v2 test).

---

**Pre-registration drafted 2026-06-15, BEFORE any v2 test run on the relocked headline cell.** v1's test.py output (eligible-n and median-predictor tables read from the dry-run-report; per-episode z-scores held out) informs the §7 anchor + §5.3 n-threshold decisions but does NOT inform §5.1 falsification-bar parameters. Locked at user acceptance. Any subsequent change creates HA-C4b-v3.

HA-C4b tests Wiggers' "stuck sympathetic / walls of orange" pattern ([Wiggers C4, PDF lines 1140-1143, 1223-1231](../../../wiggers_testable_hypotheses.md#c4--stress-fails-to-drop-during-rest-periods-after-overexertion-stuck-sympathetic)) refined with the participant's lived **motion filter** ([garmin_pacing_practice §3.3](../../../methodology/garmin_pacing_practice.md#33-stress-when-at-rest)): elevated Garmin stress *while concurrent body motion is low* — discriminates true sympathetic-arousal-while-at-rest from motion-artefact stress readings.

**v2 reframe relative to v1**: v1's headline locked the consolidation phase (largest n, dose-stable plateau). v1's dry-run halt revealed (a) the consolidation × train cell was empty by construction and (b) the consolidation × validate cell n = 5 was below the inconclusive bar. v2 relocks the headline on the **unmedicated phase** — pooled across train + validate — where the "stuck sympathetic" pattern is mechanistically expected to be MOST visible (citalopram's stress-channel suppression is absent). The pooled n = 10 is the minimum that clears the project inconclusive bar; validate-unmedicated alone (n = 2) is pre-declared INCONCLUSIVE.

## 1. Claim

In the **4 days** before a `crash_v2` episode (primary) and the **5 days** before a `crash_v2` episode (secondary), conditioned on `exertion_class_lagged_lcera ∈ {heavy, very_heavy}` on T OR T-1, at least one day's `stress_low_motion_min_count_S60_Mlow` deviates from its lagged personal baseline by `(count − μ) / σ ≥ N_std` (N_std locked in §4.8; one-sided ELEVATED direction). The crash-episode frequency of this deviation is discriminative against block-permutation-null windows on the **unmedicated phase, train + validate windows pooled**.

A bidirectional sensitivity arm reports the `|z| ≥ N_std` result. The primary direction is one-sided elevated (more stress-low-motion minutes = more sympathetic-while-at-rest events = pre-crash precursor) per Wiggers C4's "walls of orange" framing.

**v2 headline cell**: unmedicated phase × train + validate pooled × `S60_Mlow` × `N_std = 1.5` × primary 4d lead-up × one-sided elevated. Pooling train + validate within the unmedicated phase is the v2 inconclusive-bar handler (n = 8 train + n = 2 validate → pooled n = 10 ≥ the §5.3 bar); abandons the both-eras-independent rule for this hypothesis. See §5.0.

Secondary descriptive outcomes (inherited from v1 r3 wholesale; cited at §4.11):
- Same-day Spearman correlation between `stress_low_motion_min_count_S60_Mlow` and `gevoelscore` per phase + pooled LC era, with crash-drop sensitivity row.
- Construct-disambiguation against `stress_high_duration_min` (PRIMARY sibling, ρ = 0.79) and against HA11's `u_dip_count` (SECONDARY sibling, ρ = 0.556) on the same lead-up windows.
- Respiration-companion sensitivity: report whether episodes firing on the primary ALSO have elevated `n_minutes_resp_above_18` in the lead-up.

## 2. Why we think this

Inherited from v1 r3 §2 wholesale. The v2 reframe is the **phase of expected visibility**: v1 framed consolidation as "where citalopram makes the pattern testable on a dose-stable plateau"; v2 reframes the unmedicated phase as "where the stuck-sympathetic pattern is MOST visible because citalopram's stress-channel suppression is absent" — same Wiggers C4 mechanism, different operational window. The underlying Wiggers documentation, motion-filter lived-experience anchor, Session E construct validity, and sibling SUPPORTED-precursor context are all unchanged.

**Why each inherited v1 r3 motivation still favours unmedicated as the v2 headline phase** (added r2 2026-06-15 to close the audit's L1.5 self-readability concern):

- **Wiggers C4's "stuck sympathetic / walls of orange" mechanism assumes uninhibited sympathetic regulation.** The [citalopram dose-response §5.6 multi-channel confirmation](../../../methodology/citalopram_dose_response_stress_mean_sleep.md#56-v3-amendment--multi-channel-confirmation-added-2026-06-14) established that 30 mg plasma suppresses the raw stress channel by ~12-17 points and the `bb_lowest` floor by ~30-50 BB points — that is exactly the autonomic suppression cascade Wiggers C4 assumes is absent. The unmedicated phase is therefore the cleanest mechanistic test ground; consolidation is the test ground where the suppression cascade is most active and the C4 pattern is most muted (the v1 framing's "dose-stable plateau" advantage was a confound, not a cleaning).
- **The four sibling SUPPORTED autonomic-deviation precursors that motivated this test all fired in pre-cliff windows.** H02b stress spike count (train), H02d sentinel-corrected spike (train), HA06b RHR z-score (train), and HA11 U-dip count (train) all landed SUPPORTED on the train era — which falls entirely inside the unmedicated phase (train ends 2023-12-31; citalopram starts 2024-04-09). The precursor evidence base motivating HA-C4b is unmedicated-leaning by corpus structure, not consolidation-leaning; v1's consolidation framing departed from where the sibling support actually lives.
- **The Session E construct-validity work** ([`stress_low_motion_primitive §8 validation plan`](../../../methodology/stress_low_motion_primitive.md#8-validation-plan)) computed its cross-channel ρ on the LC-pooled corpus, which is ~48% unmedicated-day rows by [v2 §7's per-phase n table](#7-expected-effect-size-if-hypothesis-is-true-v2-re-anchored) (725 of 1508). The 0.79 vs `stress_high_duration_min` and 0.556 vs `u_dip_count` correlations are not phase-specific; they apply equally to the unmedicated headline as to v1's consolidation headline.

Read [v1 §2](hypothesis-v1-archived.md#2-why-we-think-this) for the full provenance of the inherited motivation body.

## 3. Data sources

- **Crash labels (scheme)**: `crash_v2` scheme defined in [`crash_v2-definition/definition.md`](../crash_v2-definition/definition.md). HA-C4b uses crash_v2 (not crash_v1 like HA11).
- **Crash labels (data CSV)**: external at `$GEVOELSCORE_DATA_PATH/processed/crash_labels/labels_crash_v2.csv` per the project privacy boundary. **v2 path-fix relative to v1**: v1 §3 cited the in-repo `crash_v2-definition/labels_crash_v2.csv` for the labels source; that path holds the scheme definition MD only, not the labels data. The labels CSV is external; v2 corrects this.
- **Predictor primitive**: 9 stress × motion count columns + 2 respiration companions in `per_day_master.csv`, extracted by [`pipeline/01_extract/stress_low_motion_extract.py`](../../../pipeline/01_extract/stress_low_motion_extract.py) per [`methodology/stress_low_motion_primitive.md`](../../../methodology/stress_low_motion_primitive.md). 1739 days covered (1722 valid via the ≥ 600-stress-sample gate); HA-C4b further restricts to ≥ 900 + quartile-coverage per §4.3 1b.
- **Exertion class**: `exertion_class_lagged_lcera` column in `per_day_master.csv` (per [CONVENTIONS §3.2](../../../CONVENTIONS.md#32-lagged-baseline-for-sustained-push-hypotheses)). Values: `{none, light, moderate, heavy, very_heavy}`.
- **Citalopram phase + plasma dose**: `dose_plasma_mg` column in `per_day_master.csv` (PK-smoothed per [`citalopram_phase_stratification §3`](../../../methodology/citalopram_phase_stratification.md#3-the-four-phase-citalopram-traject-stratification)); phase derivable from the date via that MD's `citalopram_phase(d)` function.
- **HA11 sibling for construct disambiguation**: `u_dip_count` column from [HA11's udip_counts.csv](../HA11-stress-udip/udip_counts.csv) (joined on `date`).
- **Per-phase descriptive card (§7 anchor source)**: `$GEVOELSCORE_DATA_PATH/analyses/stress_low_motion_descriptive/per_phase_card.md`, reproducible from [`docs/research/analyses/garmin_exploration/stress_low_motion_viz/per_phase_descriptive.py`](../../garmin_exploration/stress_low_motion_viz/per_phase_descriptive.py). Calibrates the §7 ranges against the exact column being tested per [`hypothesis_lock_process.md` §5 last row](../../../methodology/hypothesis_lock_process.md#5-sanity-check-questions-before-lock).
- **Analysis window + train/validate split**: same as HA11 / HA06b / HA10 (train 2022-09-03 → 2023-12-31; validate 2024-01-01 → 2026-06-05). v1's dry-run confirmed phase-stratified eligible-n: unmedicated train = 8, unmedicated validate = 2, consolidation validate = 5, buildup validate = 2, afbouw validate = 2; all consolidation/buildup/afbouw train cells = 0 by phase-boundary construction. v2 inherits these counts as the operating assumption.

## 4. Measurement protocol

### 4.1 Predictor primitive — `stress_low_motion_min_count_S60_Mlow` (locked, inherited from v1 r3)

Inherited from [v1 §4.1](hypothesis-v1-archived.md#41-predictor-primitive--stress_low_motion_min_count_s60_mlow-locked) verbatim. The primitive's full operationalisation is locked in [`methodology/stress_low_motion_primitive.md`](../../../methodology/stress_low_motion_primitive.md) §3-§5 and implemented in [`pipeline/01_extract/stress_low_motion_extract.py`](../../../pipeline/01_extract/stress_low_motion_extract.py). No re-derivation in this pre-reg.

### 4.2 Exertion-conditioning rule (locked, inherited from v1 r3)

Inherited from [v1 §4.2](hypothesis-v1-archived.md#42-exertion-conditioning-rule-locked) verbatim. A day is C4b-eligible if `exertion_class_lagged_lcera ∈ {heavy, very_heavy}` on `d` OR `d − 1` (union).

### 4.3 Day validity (locked, inherited from v1 r3-post-viz)

Inherited from [v1 §4.3](hypothesis-v1-archived.md#43-day-validity-revised-post-viz-2026-06-15) verbatim. Three gates: (1) primitive stress-sample gate ≥ 600 samples; (1b.i) total in-range samples ≥ 900; (1b.ii) wake-window quartile coverage ≥ 50 samples per quartile (sleep-boundary-aware or fixed-time fallback); (2) §4.2 exertion-conditioning satisfied; (3) day has a `crash_v2` label.

### 4.4 Citalopram phase-stratified treatment (per §5.B framework, locked) — v2 headline-verdict-sentence update

Inherited from [v1 §4.4](hypothesis-v1-archived.md#44-citalopram-phase-stratified-treatment-per-5b-framework-locked) **except** for the headline-verdict-sentence at the end. The phase table, the per-phase n estimates, the buildup-CPAP-buffer (strictly < 2024-04-30), and the afbouw-merge are unchanged.

| phase | window | n estimate (heavy-exertion subset) | v1 dry-run eligible-n (train / validate) |
|---|---|---|---|
| unmedicated | LC start 2022-04-04 → 2024-04-08 | ~50-100 | 8 / 2 |
| buildup | 2024-04-09 → 2024-06-19 (post-buffer: 2024-04-30 → 2024-06-19) | ~10-20 | 0 / 2 |
| consolidation (30mg plateau) | 2024-06-20 → 2026-03-19 | ~80-150 | 0 / 5 |
| afbouw (post-afbouw merged, see prose) | 2026-03-20 → 2026-06-05 | ~10-20 | 0 / 2 |

**v2 headline-verdict sentence (replaces v1 r3's last paragraph)**: The **headline verdict** is the **unmedicated-phase verdict** — pooled across train + validate windows (n = 10) — at the §5.0 locked cell. The validate-unmedicated subset (n = 2) and the train-unmedicated subset (n = 8) are pre-declared INCONCLUSIVE individually and reported only as descriptive directional-consistency companions to the pooled verdict (see §5.3). The consolidation, buildup, and afbouw phases are all pre-declared INCONCLUSIVE at v2 (validate n = 5, 2, 2 respectively; train n = 0 for each by phase-boundary construction); reported as descriptive companions only — none promote to SUPPORTED.

**Rationale for pooling train + validate within unmedicated (vs the both-eras-independent rule)**: v1 inherited the HA11-family both-eras rule, which gave independent verdicts in train and validate as cross-era replication. For v2's unmedicated headline that rule would force n = 8 (train alone) and n = 2 (validate alone) — both below the §5.3 bar — making the entire headline inconclusive. Pooling within the unmedicated phase is the trade-off: the HA-family cross-era replication structure is abandoned for this hypothesis in exchange for one above-bar pooled verdict. The cost is named in §8 (no cross-era independent replication; the pooled verdict cannot be cross-validated against itself). The validate-unmedicated subset directional-consistency descriptive read in §9 partially compensates by flagging if validate-arm episodes go the same direction as train-arm episodes.

### 4.5 Lagged personal baseline (per CONVENTIONS §3.2, locked, inherited from v1 r3)

Inherited from [v1 §4.5](hypothesis-v1-archived.md#45-lagged-personal-baseline-per-conventions-32) verbatim. Baseline window `[d − 90, d − 30]`, LC-era + same-phase restricted, trimmed mean (10/90), ≥ 40 of 60 prior days, σ ≤ 5 low-variability flag.

**v2 note on the labels CSV path** (referenced from §3): the baseline construction reads the same external `labels_crash_v2.csv` as §3 for `crash_v2` membership; the in-repo path correction applies here as well.

### 4.6 Per-day z-scored count (locked, inherited from v1 r3)

Inherited from [v1 §4.6](hypothesis-v1-archived.md#46-per-day-z-scored-count) verbatim. `delta(d) = count(d) − μ(d)`, `z(d) = delta(d) / σ(d)`.

### 4.7 Per-episode lead-up profile (locked, inherited from v1 r3)

Inherited from [v1 §4.7](hypothesis-v1-archived.md#47-per-episode-lead-up-profile) verbatim. 4-day primary lead-up `[C-4, C-3, C-2, C-1]`; 5-day secondary `[C-5, C-4, C-3, C-2, C-1]`; min valid 3 of 4 primary / 4 of 5 secondary; episode trigger flag `max_signed_z ≥ N_std` (one-sided) and `max |z| ≥ N_std` (bidirectional sensitivity).

### 4.8 Threshold N_std (locked, inherited from v1 r3)

Inherited from [v1 §4.8](hypothesis-v1-archived.md#48-threshold-n_std) verbatim. Primary 1.5 / secondary 2.0 / sensitivity 2.5. **Primary tier (N_std = 1.5) determines the v2 headline verdict** (consistent with v1).

### 4.9 Null sample — stationary bootstrap with E[L] = 7 (locked, inherited from v1 r3)

Inherited from [v1 §4.9](hypothesis-v1-archived.md#49-null-sample--stationary-bootstrap-with-el--7-revised-post-audit-2026-06-15) verbatim, with one operational note for v2's pooled cell: the stationary-bootstrap operates within the **unmedicated phase eligible pool, pooled across train + validate eras** (no cross-phase resampling; the pool spans the LC-era unmedicated window 2022-04-04 → 2024-04-08). The block-permutation null preserves within-block autocorrelation on the pooled time series. B = 10,000 for the pooled headline; seed `20260615` (unchanged from v1). `E[L]*` companion + factor-of-2 flag rule applies per the methodology MD.

### 4.10 Sensitivity ladder report (locked, inherited from v1 r3)

Inherited from [v1 §4.10](hypothesis-v1-archived.md#410-sensitivity-ladder-report-revised-post-audit-2026-06-15) verbatim. 6 unique columns + 3 identical-by-construction duplicates; only the headline cell drives the SUPPORTED verdict; within-row and across-motion-classes monotonicity checks apply.

### 4.11 Secondary descriptive outcomes (locked, inherited from v1 r3)

Inherited from [v1 §4.11](hypothesis-v1-archived.md#411-secondary-descriptive-outcomes) verbatim. Same-day Spearman (with crash-drop sensitivity row per CONVENTIONS §3.4); primary construct-disambiguation against `stress_high_duration_min` (ρ = 0.79); secondary against HA11 `u_dip_count` (ρ = 0.556); respiration-companion sensitivity on `n_minutes_resp_above_18`.

**v2 phase-scope adjustment**: the per-phase × per-era splits in §4.11.1 (same-day Spearman) are reported as v1 specified; the unmedicated-pooled cell additionally surfaces a Spearman on the pooled unmedicated heavy-exertion-conditioned subset for cross-reference with the headline.

**§4.11.5 Episode-level leave-one-out (LOO) fragility check (v2-specific, added 2026-06-15)**.

At the pooled-unmedicated n = 10 headline, a single episode is worth 10 percentage points on the (a) frequency gate, so the verdict is structurally one-episode-from-flipping at the 60% threshold. Jackknife / leave-one-out sensitivity (Quenouille 1949; Tukey 1958) is the canonical robustness check for this fragility.

**Procedure**:

1. For each of the 10 unmedicated-pooled crash episodes E_i (i = 1..10), drop it and recompute on the remaining 9:
   - (a) frequency: `count(max_signed_z ≥ 1.5) / 9`
   - (b) discrimination: `p_crash_LOO − p_null` against the same block-permutation null at E[L] = 7 from §4.9 (the null is fixed across LOO drops; the LOO operation drops a crash episode from the numerator, not from the null pool)
   - (c) magnitude: median `max_signed_z` across the 9 remaining episodes
2. Report the **range** of (a), (b), (c) across the 10 LOO drops alongside the headline numbers on the full n = 10. Also report the **mean and std** of each across LOO drops as a stability summary.
3. **Load-bearing-episode flag**: for each LOO drop, mark whether the headline (a) verdict at the §5.1 60% gate flips (i.e. headline (a) ≥ 60% but LOO (a) < 60%, or vice versa). Any episode whose removal flips the verdict is flagged as **load-bearing** and surfaces in the result.md §9 SUPPORTED / NOT-SUPPORTED branch as a case-study candidate (which day, which signed_z values, what notes were logged that week).
4. **Honest framing**: each LOO drop leaves n = 9, which is **below the §5.3 inconclusive bar of n ≥ 10**. The LOO results are NOT re-evaluations of the verdict at n = 9 — they are descriptions of headline-frequency stability. The §5.1 verdict locks at the full pooled n = 10; LOO informs how confidently we can read it.

**Boundary-fragility structural note** (added r2 2026-06-15 to close the audit's LOO-boundary side observation). The LOO load-bearing-episode flag is *structurally* most informative at exactly the §5.1 (a) 60% gate boundary — at pooled n = 10 the gate fires when ≥ 6 of 10 episodes trigger; LOO drops then split into:

- **k = 6 firing (just clears)**: every LOO-dropped firing episode flips the verdict (5/9 = 0.556 < 0.60), every LOO-dropped non-firing episode keeps it (6/9 = 0.667 ≥ 0.60). The load-bearing list is *populated* and is the informative-case read.
- **k = 7+ (clears comfortably)**: no LOO drop flips the verdict (worst case 6/9 = 0.667 still passes). Load-bearing list is empty; LOO range tight.
- **k ≤ 5 (fails)**: no LOO drop flips into passing (best case 5/9 = 0.556 still fails). Load-bearing list is empty (in the verdict-flipping sense); LOO range tight.

So an empty load-bearing list is not "no fragility detected" — it is a *boundary-distance signal* meaning k is not exactly at the 60% boundary. v2 reports the empty-list case as such ("verdict comfortably clears / fails the (a) gate; no single episode is load-bearing in the verdict-flipping sense") rather than silently. The fragility check earns its keep at the boundary.

**Reporting**:

- LOO range table: per-LOO-drop (a) / (b) / (c) numbers + which episode was dropped (date, era).
- Stability summary: mean ± std across LOO drops; min and max (a) rate.
- Load-bearing-episode list: episodes whose removal would flip the (a) verdict at the 60% gate (if any). The boundary-fragility note above is restated in the result.md so the reader interprets an empty list correctly.
- Era stratification within LOO: the 10 LOO drops decompose into 8 train-drops + 2 validate-drops. Whether the load-bearing episodes cluster in one era is a v2-specific descriptive observation given the pooled-cell trade-off (§4.4 rationale).

**Scope clarification**: LOO sensitivity is fine-grained episode-level. It is distinct from (and complementary to) the era-level descriptive companions in §5.3 (train-only n = 8 vs validate-only n = 2 directional consistency). LOO answers "is any single episode load-bearing?"; the era-level companions answer "do the eras agree in direction?". Both are descriptive; neither promotes to SUPPORTED.

**Not in scope at v2**: K-fold reshuffling of train ↔ validate buckets. Train/validate is a *temporal* split (2022-2023 train vs 2024-2026 validate), not a random one; reshuffling would break the era-replication intent inherited from the HA11 family. The v2 abandoned-both-eras-rule (§4.4 rationale) already absorbs this; reshuffling would compound the methodological cost.

## 5. Pre-registered falsification criterion

### 5.0 Multi-comparison discipline — single-cell headline lock (v2 relock)

**v2 relocks** the single-cell headline from v1's `consolidation × both-eras × S60_Mlow × N_std = 1.5 × primary 4d × one-sided` to:

> **Unmedicated phase × train + validate pooled × `S60_Mlow` column × `N_std = 1.5` × primary 4-day lead-up × one-sided elevated direction.**

**Hard rule (inherited from v1 r3, retargeted)**: ALL OTHER cells in the family (3 stress thresholds × 3 motion classes × 3 N_std tiers × 4 phases × {primary 4d, secondary 5d} × {one-sided, bidirectional} × {pooled, train-only, validate-only, both-independent}) are **diagnostic / sensitivity arms ONLY**. They are reported in the result.md, but **none can promote to a SUPPORTED verdict on their own**. The headline verdict is the single pooled-unmedicated cell, full stop.

The other phase cells (consolidation × validate n = 5; buildup × validate n = 2; afbouw × validate n = 2) are pre-declared INCONCLUSIVE in §5.3 and reported as descriptive companions; they are not eligible to promote even if their cell-level numbers cross the §5.1 bar. This is the v2 trade-off for shifting the headline to the only above-bar pooled cell available on the corpus.

### 5.1 Three-criterion bar (applied to the single locked v2 headline cell)

Identical three-criterion bar shape to v1 r3 (and the H02b / HA01b / HA06b / H02d / HA10 / HA11 family), applied **to the single v2-locked cell** (unmedicated pooled × S60_Mlow × N_std = 1.5 × primary 4d × one-sided):

**(a) Frequency**: at least **60%** of unmedicated-pooled crash episodes have `max signed_z ≥ 1.5` (one-sided) in their lead-up window.

**(b) Discrimination**: the unmedicated-pooled crash-episode frequency from (a) is at least **15 percentage points higher** than the unmedicated-pooled **stationary-bootstrap-null frequency** (per §4.9 — block-permutation null at `E[L] = 7`, operating on the unmedicated-phase pooled eligible pool).

**(b-interp) Effect-size reporting**. Criterion (b) is a risk-difference gate at 15pp; the same underlying `p_crash` vs `p_null` discrimination is reported in two community-standard formulations alongside the gate:

- **Risk difference (RD)**: `RD = p_crash − p_null`. Already gated at ≥ 0.15 by criterion (b). Report point estimate + bootstrap 95% CI from the same B = 10,000 stationary-bootstrap resamples specified in §4.9.
- **Odds ratio (OR)**: `OR = (p_crash / (1 − p_crash)) / (p_null / (1 − p_null))`. Report point estimate + bootstrap 95% CI. **Reporting threshold (not a separate falsification conjunct)**: at the §5 (b) gate of `RD = 0.15` with a typical `p_null ∈ [0.10, 0.20]`, the equivalent OR ranges 2.15 to 3.00. An OR < 1.5 with 95% CI containing 1 alongside an apparently-passing RD would be suspect — flag for review.

**Interpretation, v2 worked example (unmedicated pooled)**. Suppose the pooled headline gives `p_null = 0.15` and `p_crash = 0.40` (illustrative; not a prediction). The unmedicated baseline is wider than v1's consolidation worked example (per the §7 anchor card, unmedicated median 76 vs consolidation median 38 minutes); the null rate `p_null` may run higher than v1's worked example because the lagged baseline σ is larger and ordinary day-to-day variability picks up more `z ≥ 1.5` excursions in null windows.

- RD = 0.40 − 0.15 = **0.25** (25 percentage points; passes the 15pp gate)
- OR = (0.40 / 0.60) / (0.15 / 0.85) = 0.667 / 0.176 = **3.79** (crash-episode odds ~4× higher than null odds)
- Reading: "When a heavy-exertion-conditioned crash episode occurs in the unmedicated phase, its 4-day lead-up contains a `stress_low_motion_min_count_S60_Mlow` z ≥ 1.5 deviation about 40% of the time, vs ~15% in matched non-crash null windows on the same pooled phase. The odds of seeing the deviation in a crash lead-up are roughly four times the odds in a null window."

The OR and RD are reported alongside the §5.1 (a)(b)(c) verdicts on the v2 locked headline cell. They are **interpretability augmentation, not additional falsification conjuncts** — the (a)+(b)+(c) bar determines SUPPORTED / NOT-SUPPORTED.

**(c) Magnitude**: the median `max signed_z` across unmedicated-pooled crash episodes is at least **0.75** (N_std / 2 = 1.5 / 2).

Any one of (a), (b), (c) failing at the v2 locked headline cell → **headline refuted**. (No both-eras independence requirement at v2 — pooled is the headline.)

### 5.2 Diagnostic / sensitivity arms (no independent SUPPORTED bar)

- **N_std = 2.0 and N_std = 2.5 tiers** at the unmedicated-pooled × S60_Mlow × primary 4d × one-sided cell: **fragility checks** as in v1.
- **Other 8 stress × motion cells** at N_std = 1.5 within the unmedicated-pooled cell: sensitivity-ladder diagnostics for threshold-monotonicity (§4.10) + motion-filter-doing-analytical-work disambiguation.
- **Other 3 phases** (consolidation, buildup, afbouw) at any tier: pre-declared INCONCLUSIVE per §5.3, reported as descriptive companion verdicts only.
- **Train-only and validate-only subsets within unmedicated** (n = 8 and n = 2): pre-declared INCONCLUSIVE per §5.3, reported as descriptive directional-consistency companions to the pooled headline.
- **Episode-level LOO fragility check** (per §4.11.5): descriptive only; no SUPPORTED promotion; informs how confidently the pooled headline verdict can be read.
- **Secondary 5d lead-up** + **bidirectional sensitivity arm**: transparency arms, no SUPPORTED promotion.

### 5.3 Inconclusive bar (v2 update)

The §5.3 inconclusive bar is **n ≥ 10 crash episodes** in the headline cell after exclusions. Cell-level handling per v2:

- **Unmedicated pooled (train + validate)**: n = 10 (8 train + 2 validate); **just clears the bar**; this is the SUPPORTED-driving headline cell.
- **Unmedicated train alone (n = 8)**: pre-declared INCONCLUSIVE; reported as descriptive directional-consistency companion to the pooled headline. (Below the n ≥ 10 bar individually.)
- **Unmedicated validate alone (n = 2)**: pre-declared INCONCLUSIVE; reported as descriptive directional-consistency companion only — no SUPPORTED-bar weight or NOT-SUPPORTED weight. (Below any reasonable cell-level bar.)
- **Consolidation × validate (n = 5)**: pre-declared INCONCLUSIVE.
- **Buildup × validate (n = 2)**: pre-declared INCONCLUSIVE.
- **Afbouw × validate (n = 2)**: pre-declared INCONCLUSIVE.
- **All train arms outside unmedicated (consolidation / buildup / afbouw)**: pre-declared NULL (n = 0 by phase-boundary construction) — these cells are not in scope at all; the §10.1 dry-run will confirm.

**v2 trade-off explicit**: the unmedicated pool is the only above-bar cell available on this corpus given the v1-archived dry-run counts. Pooling train + validate within unmedicated is the price; the cross-era independent replication structure that v1 inherited from the HA11 family is abandoned for this hypothesis. The compensating mechanism in §9 is the directional-consistency descriptive read between the train-unmedicated and validate-unmedicated subsets — concordant direction in the descriptive companions partly substitutes for independent verdicts. NOT a full substitute; the result.md caveat list makes this explicit (§8).

## 6. Exclusion rules (locked, inherited from v1 r3)

Inherited from [v1 §6](hypothesis-v1-archived.md#6-exclusion-rules) verbatim. Day-level (< 600 stress samples; § 4.2 exertion-conditioning failed; baseline σ ≤ 5; < 40 of 60 prior same-phase valid days); phase-level (buildup `< 2024-04-30`); structural (2024-04-09 to 2024-04-16 unanalyzable cluster); null-sample contamination guard (crash lead-up windows excluded from null pool).

## 7. Expected effect size if hypothesis is true (v2 re-anchored)

**v2 re-anchors the §7 sanity ranges against the exact column's per-phase descriptive card** (raw column, no §4.3 eligibility restriction): see `$GEVOELSCORE_DATA_PATH/analyses/stress_low_motion_descriptive/per_phase_card.md`, reproducible from [`per_phase_descriptive.py`](../../garmin_exploration/stress_low_motion_viz/per_phase_descriptive.py). Replaces v1's `[15, 60]` anchor which was a definitional-cousin miss (the cousin's distribution, not the S60_Mlow column's distribution).

**Per-phase raw-column distribution** (RAW; before §4.3 eligibility filter; n = day-rows in `per_day_master.csv` LC era):

| phase | n | median | IQR (Q25-Q75) | min-max | mean | std |
|---|---:|---:|---:|---:|---:|---:|
| unmedicated (pre_cit) | 725 | 76 | 48-114 | 0-364 | 86.6 | 53.6 |
| buildup | 72 | 35 | 22-57 | 1-167 | 44.1 | 32.9 |
| consolidation | 634 | 38 | 21-66 | 0-297 | 51.1 | 43.6 |
| afbouw | 77 | 63 | 39-96 | 2-186 | 69.1 | 40.2 |
| LC pooled | 1508 | 57 | 31-96 | 0-364 | 68.8 | 51.2 |

Cross-check: v1's dry-run-report.md per-phase median predictor on §4.3-eligible-only days was unmedicated 78 / buildup 36 / consolidation 39 / afbouw 64 — within 1-2 minutes of the raw-column medians above, confirming §4.3 eligibility doesn't materially bias the per-phase distribution centre.

**v2 expected ranges** (against the raw card, the EXACT column):

- **Headline phase median primary expected in [48, 114]** (unmedicated IQR). v1's [15, 60] anchor was wrong for this phase; the v2 range is the unmedicated phase's actual IQR.
- **Headline-phase lagged-baseline σ expected in [25, 55]** (range anchored r2 2026-06-15 to close the audit's σ-lower-bound side observation). The raw unmedicated phase std is 53.6 (upper bound: the [25, 55] range brackets this just above). The lagged baseline operates on a 60-day window — narrower than the full 725-day phase variation — so the lagged σ will fall below the raw phase std: v1's dry-run-report.md observed σ_median = 33.4 on §4.3-eligible unmedicated days, and the [25, 55] range brackets that with a margin below (down to 25) and the raw 53.6 above. The 25 lower bound is therefore an explicit margin-below of the 33.4 observed median, not a hand-wavy estimate.
- **`max signed_z` distribution under SUPPORTED hypothesis**: 60-80% of unmedicated crash episodes have `max signed_z ≥ 1.5` in the 4-day lead-up (the (a) gate at 60%). Median `max signed_z` in [1.5, 2.5] (the (c) gate at 0.75).
- **Null-window trigger rate under random labels (block-permutation null at E[L] = 7)**: 7-25% (one-sided Gaussian tail expectation ~6.7% per day; max over 4 days inflates; the unmedicated baseline σ being larger than consolidation's mildly broadens the null rate too).

**Sanity gate (revised from v1)**: if the unmedicated phase median primary is OUTSIDE [48, 114], OR the lagged-baseline σ_median is OUTSIDE [25, 55], OR consolidation/buildup/afbouw raw medians shift > 20% from the table above → the per-phase distribution may have changed since extraction (e.g. re-extracted CSV with different definition). Halt the test, investigate, then re-evaluate. The dry-run is the gate per §10.4.

**v2 lesson absorbed from v1**: the §7 anchor must cite the EXACT column's descriptive card (per [`hypothesis_lock_process.md` §5 last row](../../../methodology/hypothesis_lock_process.md#5-sanity-check-questions-before-lock)). v1's anchor was bound to a definitional cousin's distribution and was wrong by a factor of ~2 on the medians. v2 closes this by citing the raw-card with the exact column.

## 8. Caveats `result.md` must explicitly acknowledge

Inherited from [v1 §8](hypothesis-v1-archived.md#8-caveats-resultmd-must-explicitly-acknowledge) wholesale + the following v2-specific additions:

- **v1 → v2 relock disclosure**. The headline cell was relocked from `consolidation × both-eras` (v1) to `unmedicated × train+validate pooled` (v2) **after v1's dry-run halt**. The relock honoured the locked-pre-reg discipline (v1 archived, v2 drafted in a fresh session with per-episode z-scores held out), but introduces researcher-degrees-of-freedom concern: the corpus's available cells were known at v2 drafting time (eligible-n table from v1's dry-run-report), and the pooled-unmedicated cell was selected partly because it was the only above-bar cell available. The result.md must acknowledge this as a v2-specific multi-comparison concern; the §5.0 single-cell lock + the descriptive companion treatment of all other arms is the within-test discipline. The block-permutation null at E[L] = 7 (§4.9) is the inferential defence; the lock-process v1.2 §5 row added 2026-06-15 (structural-completeness + EXACT-column anchor) is the upstream defence that v2 closes for future pre-regs.
- **No cross-era independent replication for v2's headline cell**. v1 inherited the HA11-family both-eras-independent rule (separate verdicts in train + validate). v2 pools train + validate within unmedicated to clear the n ≥ 10 bar. The pooled cell carries one verdict; cross-era replication is not a structural property of v2's headline. The compensating mechanism is the descriptive directional-consistency companion (§9) on the train-only (n = 8) and validate-only (n = 2) subsets within unmedicated. The result.md must explicitly note that v2's pooled-unmedicated SUPPORTED verdict, if it lands, is **not** a both-eras finding in the project's HA-family sense; it is a single-phase pooled-corpus finding.
- **Power-calc dispatch**: power calculation is inapplicable per [Daza 2018](../../../literature/methodology/daza_2018_self_tracked_n_of_1_counterfactual.pdf) within-subject design — the n-of-1 corpus does not have separate "treatment" and "control" arms in the sense classical power calculations require. The block-permutation null at E[L] = 7 (§4.9) is the within-subject inferential machinery; the §5.1 (a)(b)(c) gates determine SUPPORTED / NOT-SUPPORTED rather than a power-thresholded p-value. Closes [`hypothesis_lock_process.md` §3.8 gate 1](../../../methodology/hypothesis_lock_process.md#38-lock-step-stage-5-of-the-arc).
- **Unmedicated phase = pre-citalopram corpus, not "no medication overall"**. The participant was unmedicated for SSRI but had other lived-experience interventions in the 2022-04 → 2024-04 window (CPAP started 2024-01-10; daily pacing protocols evolved through this period; PEM-pacing practice was being established). The unmedicated headline is "no SSRI" not "no intervention". The result.md must note the surrounding context — particularly the CPAP-start mid-phase (2024-01-10 to 2024-04-08, the last ~3 months of unmedicated) — even though §4.2 exertion-conditioning and §4.5 phase-stratified baseline absorb most of that.

## 9. What we do with each outcome

The outcome space at v2 is `{pooled-unmedicated SUPPORTED, pooled-unmedicated NOT-SUPPORTED, pooled-unmedicated INCONCLUSIVE}`. The headline is the **single pooled-unmedicated cell** at the primary N_std tier. Branching:

- **Pooled-unmedicated SUPPORTED** (n = 10 pooled; (a)+(b)+(c) all pass at the v2-locked cell). The Wiggers C4 "stuck sympathetic" pattern is empirically validated in the unmedicated phase (where it's mechanistically expected to be most visible). Then: descriptive companions:
  - **Train-unmedicated subset (n = 8) directional consistency**: report `(a)` rate + median `max signed_z` on the train-only subset; if consistent direction with the pooled (i.e. (a) rate > the null rate from §4.9 + median signed_z > 0), descriptive directional-confirmation. If train-only rate fires below the null, surface as an internal inconsistency (the pooled SUPPORTED may have been driven by the n = 2 validate subset).
  - **Validate-unmedicated subset (n = 2) directional consistency**: report (a) flag + signed_z per episode; if both episodes fire on the primary, descriptive directional-confirmation. If neither fires, surface as an internal inconsistency.
  - **Episode-level LOO fragility report** (per §4.11.5): LOO range table + load-bearing-episode list. If any episode is flagged load-bearing (removal would flip the (a) verdict), case-study the day in the result.md — date, signed_z values across the lead-up, notes / tags around it, what was happening. The strongest SUPPORTED reading is "stable across LOO drops, no single episode load-bearing"; a weaker but still SUPPORTED reading is "verdict holds at n = 10 but is sensitive to specific episodes which are reported and motivated".
  - **`card.md` for a rest-stress-aware retrospective card concept** (carried from v1 r3 §9).
  - **Construct-disambiguation verdicts per v1 r3 §9**: against `stress_high_duration_min` (primary) and HA11 `u_dip_count` (secondary).
  - **Cross-phase descriptive companions**: consolidation × validate (n = 5), buildup × validate (n = 2), afbouw × validate (n = 2) — all pre-declared INCONCLUSIVE; report (a) rate and median signed_z as descriptive companions. Concordance (other phases also descriptively elevated) is supportive context, not promoting evidence; divergence (other phases descriptively NOT elevated) is documented for the [phase_stratification §8.4 buildup-vs-afbouw asymmetry question](../../../methodology/citalopram_phase_stratification.md#84-the-buildup-and-afbouw-magnitude-asymmetry-as-a-research-question).
- **Pooled-unmedicated NOT-SUPPORTED** (one or more of (a)(b)(c) fails on the pooled n = 10 cell). The motion-filtered stress-elevated-minute count does NOT carry crash-precursor signal at the unmedicated-phase population level. **Recommended primary alternative reading**: the lived-experience pacing trigger may be PROTECTIVE rather than PREDICTIVE (the participant has been operationally using the rest-stress trigger per [garmin_pacing_practice §3.3](../../../methodology/garmin_pacing_practice.md#33-stress-when-at-rest)) — the participant acts on the trigger and prevents the crash; document this as a follow-up question for [garmin_pacing_practice](../../../methodology/garmin_pacing_practice.md). Construct-disambiguation verdicts per v1 r3 §9 apply. **LOO companion read**: report §4.11.5 LOO range alongside the NOT-SUPPORTED verdict — if some LOO drops would pass the 60% gate, this is "headline doesn't hold but is close" rather than "headline fails clearly"; if all LOO drops fall below 60%, the NOT-SUPPORTED reading is robust.
- **Pooled-unmedicated INCONCLUSIVE** (n drops below 10 after final exclusions at the dry-run gate — e.g. additional §4.5 baseline-insufficiency exclusions consume train episodes). Halt the test; revise via v3 if a recoverable operationalisation change exists, otherwise descriptive companions become the only output. No SUPPORTED claim.
- **Construct-disambiguation differs from primary headline** (vs `stress_high_duration_min` ρ = 0.79 or vs HA11 `u_dip_count` ρ = 0.556): inherited from v1 r3 §9 wholesale.
- **Respiration-companion sensitivity differs from primary headline**: inherited from v1 r3 §9 wholesale.
- **Sensitivity ladder shows non-monotonicity** (S=50 < S=60 frequency, or strict > low frequency): inherited from v1 r3 §9 — bug or extreme baseline shift; halt + investigate.
- **Spec sanity-check fails on v2 dry-run** (unmedicated pooled n falls below 10; or per-phase median falls outside the v2-revised §7 ranges; or median σ outside [25, 55] for unmedicated): DO NOT run the full test. Document the failure in the v2 dry-run report; revise the spec (creating HA-C4b-v3 with audit trail per [`hypothesis_lock_process.md` §2 5-stage arc](../../../methodology/hypothesis_lock_process.md#2-the-arc-canonical--option-a-compression)).
- **Train-only vs validate-only directional inconsistency within unmedicated** (train (a) rate ≥ null rate AND validate both episodes do NOT fire, OR vice versa): document as an internal inconsistency in the result.md. The pooled headline still stands as the locked verdict (it's the single-cell lock), but the descriptive companion read is "the pooled SUPPORTED was driven asymmetrically by one era". Flag for follow-up; do NOT retroactively re-split the headline.

## 10. Detection script architecture

Inherited from [v1 §10](hypothesis-v1-archived.md#10-detection-script-architecture) wholesale, with the following v2 operational notes:

### 10.1 Stage 1 — primitive (already done)

Unchanged from v1.

### 10.2 Stage 2 — test (`HA-C4b/test.py`, to be written post-lock)

Loads `per_day_master.csv`, joins HA11's `udip_counts.csv`, applies §4.2-§4.5 filtering + lagged baseline + per-day z + per-episode `max signed_z` + §5 falsification per phase × per N_std tier × per sensitivity-ladder column. **v2 operational delta**: the headline cell evaluation operates on `unmedicated phase, train + validate eras pooled` rather than v1's `consolidation phase, train and validate independently`. The block-permutation null at E[L] = 7 runs on the pooled unmedicated-phase eligible pool. Train-only and validate-only subsets within unmedicated are evaluated as descriptive companions, NOT independent verdict cells. Same lagged-baseline machinery as HA06b / HA10 / HA11; same null-seed `20260615`; same `--dry-run` mode that prints first-3-episodes per phase × era to confirm v2 spec sanity before the full evaluation runs.

**v2 spec-sanity-gate at dry-run**: confirms (1) pooled-unmedicated n ≥ 10 after final §4.5 exclusions; (2) per-phase median primary inside v2 §7 ranges; (3) per-phase median σ inside [25, 55] for unmedicated. If any fail → halt + revise per §9 spec-sanity-check-fails branch + [`hypothesis_lock_process.md` §3.9](../../../methodology/hypothesis_lock_process.md#39-run-step-post-lock).

### 10.3 Stage 3 — `result.md`

Reports the v2 pooled-unmedicated headline verdict block at top (one cell), followed by descriptive companion tables for train-only / validate-only subsets within unmedicated + all other phases × validate-only cells (all pre-declared INCONCLUSIVE per §5.3) + the §4.11.5 episode-level LOO fragility table + load-bearing-episode list. Construct-disambiguation against `stress_high_duration_min` + HA11. Respiration-companion sensitivity. Caveats per §8 including the v1 → v2 transition disclosure.

### 10.4 Run protocol (v2)

1. **Dry-run** (`python test.py --dry-run`): prints sample sizes per phase × era; checks v2 §7 sanity ranges + §10.2 v2 spec-sanity-gate. **If sanity check fails → halt + revise spec → HA-C4b-v3** (the v1 → v2 → v3 pattern; the locked-pre-reg discipline holds at each generation).
2. **Full run** (`python test.py`): emits v2 `result.md` directly into this folder.
3. **No iteration on the spec after the dry-run passes.** Any post-dry-run revision creates HA-C4b-v3 with the v2 result archived.

---

*Pre-registration v2 drafted 2026-06-15 by Claude (Opus 4.7) in reviewer-mode-with-authorization, fresh session per [`hypothesis_lock_process.md` §3.2](../../../methodology/hypothesis_lock_process.md#32-drafting-step-step-1-of-the-arc). Lock requires user acceptance per [CONVENTIONS §1.2](../../../CONVENTIONS.md#12-reviewer-mode-claude-reads--critiques--explains-does-not-edit-unless-asked) + the four [§3.8 lock-blocking gates](../../../methodology/hypothesis_lock_process.md#38-lock-step-stage-5-of-the-arc). Fresh-session `/research-review` audit (per §3.4) runs between drafting and lock.*
