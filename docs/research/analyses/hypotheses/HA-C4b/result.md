# HA-C4b v3 - Result: stress-with-low-motion minute count as crash precursor (unmedicated pooled headline, §4.3 1b.ii dropped)

**Headline verdict (unmedicated phase × train+validate POOLED × `stress_low_motion_min_count_S60_Mlow` × N_std=1.5 × primary 4d × one-sided elevated): NOT-SUPPORTED**

Single-cell lock per v3 §5.0 (byte-identical with v2); no other cell can promote. Data: `result-data.json` (gitignored). Companion: [dry-run-report.md](dry-run-report.md). v3 lock commit `32ba3b9`.

## v3-specific caveats (surfaced prominently per v3 §8 + handoff brief §4.4)

### 1. §4.3 1b.ii dropped - deliberate override of a real catch

v2 applied §4.3 1b.ii (wake-window quartile-coverage gate) at the full run only, dropping one train episode (`2023-02-04`, `max_signed_z = +3.73` on d-1) from the pooled-unmedicated headline cell, taking n from 10 to 9 → INCONCLUSIVE per §5.3. **v3 drops 1b.ii and restores 2023-02-04.**

An ad-hoc empirical check absorbed into v3 r2 confirmed 2023-02-04 shows the **pathological quartile-concentrated under-sampling pattern** 1b.ii was designed to catch: sleep-window-aware Q3 = 8 samples; mid-day uncovered ~11:45-14:00 local CET; wake-window only 9.1 hours. Aggregate: 22 of 709 unmedicated 1b.i-passing days (3.1%) fail sleep-aware 1b.ii. **The 1b.ii catch on 2023-02-04 IS real.** v3 overrides this catch as a deliberate trade-off.

**The override is justified by the load-bearing asymmetry** between the crash-start day and the lead-up days. The §5.1 (a)+(b)+(c) bar reads z-scores in the 4-day LEAD-UP window, not the crash-start day. 2023-02-04's lead-up days [2023-02-03, 02-02, 02-01, 01-31] all pass sleep-aware 1b.ii comfortably (Q-min = 159, 153, 161, 128, all well above 50). The z-scores driving the headline-cell verdict are unaffected by 2023-02-04's own coverage. The `crash_v2` label is user-set, not Garmin-derived, so coverage doesn't affect label validity. **Cost**: 22 unmedicated days enter the baseline lagged-mean pool and the bootstrap-null distribution with noisier day-level predictor values.

**The discipline cost (audit Layer 2.5 substantive concern)**. The v3 drafting context knew that 2023-02-04 was the train arm's highest-z episode at the time of the v3 spec choice. The choice within the asymmetry-fix space (drop 1b.ii vs apply 1b.ii at dry-run vs tighten 1b.i) was made under exposure to which option restores this specific high-signal episode. The §5.1 falsification bar is byte-identical with v2; the cell-coordinate invariance is preserved - but the operational choice IS data-informed.

**A strict-pre-registration reviewer's defensible objection**: this is post-hoc 'rescue' of a specific high-signal episode dressed up as a spec-design fix. **v3's counter**: the override is independently supported by the primitive's own validity requirement (only the 600-sample gate is primitive-mandated; 1b.i + 1b.ii were both HA-C4b-specific strengthenings) AND the load-bearing-asymmetry argument above; the §5.1 bar is unchanged. **The reader judges.** The honest framing: v3's drop is defensible but not strictly-pre-registered; the verdict it produces sits at the §3.3 same-session refinement level of discipline, not the §3.2 fresh-session level. A future v4 (if needed) under fresh-session redraft would adjudicate whether the v3 verdict survives the strictest discipline.

### 2. v2 → v3 transition disclosure

The v3 spec was drafted in the same Claude session that ran v2's test (and saw v2's per-episode z-scores including the dropped 2023-02-04 episode, E[L]\* = 3.30, and the train 42.9% / validate 0% directional inconsistency). Per `hypothesis_lock_process.md` §3.3, this data-exposure context permits operationalisation refinements (which v3 is) but NOT headline-cell relocks (v3 makes no headline-cell change; v3 §5.0 is byte-identical with v2).

**§3.3 discipline-stretch acknowledgment** (per v3 Authorship block): §3.3's written envelope is *'r1 between initial draft and first audit'*. v3's situation - *r1-of-successor between a v2 test execution and a v3 pre-reg draft* - **extends §3.3's literal envelope**. The discipline-preserving requirements that the §3.3 invocation honours (no headline-cell change; fresh-session v3 test execution mandated via this very session's handoff brief; honest §8 disclosure of the data-exposure level and the operational-choice-within-asymmetry-fix-space concern) honour §3.3's *intent* even though the literal scope is stretched. This stays an audit-able marker for a future `hypothesis_lock_process.md` revision that formalises §3.3b 'post-result operationalisation refinement'.

### 3. Pacing-behaviour confounder (qualitative; verdict-invariant per v3 §9)

The §4.2 exertion-conditioning column `exertion_class_lagged_lcera` captures **physical exertion only** (Garmin-derived from heart-rate / motion / training-load aggregates). It does NOT capture: **cognitive exertion** (concentration, reading, fast conversation, screen time); **emotional exertion** (grief, relational stress, conflict, high-stakes meetings, exposure to triggering content); **orthostatic exertion** (being upright; orthostatic load draws on the same envelope).

Per [`pacing-and-crash-mitigation.md` §1](../../../literature/pacing-and-crash-mitigation.md): *"All exertion counts, not just physical. ... The brain uses ~20% of the body's energy; cognitive overexertion can crash someone as hard as a walk."* The energy envelope is shared.

**Two structural consequences for HA-C4b**:

1. Some unmedicated-phase crashes may have been **emotionally / cognitively triggered without a matching heavy physical exertion in the lead-up window**, in which case §4.2 exertion-conditioning **excludes them from the eligible-crash pool entirely**. The HA-C4b test cannot speak to these crashes by construction.
2. Some eligible-pool crashes (those that DO pass §4.2 exertion-conditioning) may have an emotional component that is the *actual proximate trigger*, with the physical exertion being incidental rather than causal.

**The corpus has partial quantitative proxies** for emotional / cognitive load (`cat_belasting_emotioneel`, `cat_belasting_cognitief`, `state_symptoom_emotioneel`, `state_symptoom_cognitief`, `in_pwc_reintegratie_2023`; see DATA_DICTIONARY §9, §11) with sparsity caveats: presence-conditioned (value-0-low-specificity-about-absence); ~35% unmedicated-phase fill on note-days only; max observed value 2. **They are NOT used in v3 §4.2 conditioning** (would be a §3.7 approach change requiring new audit gate; queued as a methodology MD documenting construct validity + sparsity + how to read the proxy). They are available to result.md interpretation as descriptive context if needed, but are NOT spec-locked here.

**The §9 verdict-branch READS in the next section restate this confounder per v3 r2.** The pacing-era / event-proximity annotation table was CUT per user direction 2026-06-17 (v3 §8.x removed; option B in the discipline-cost-vs-spec-weight trade); any era-classification or event-proximity flagging the result reader wants to attach lives at the post-test interpretation layer, not as a spec-locked artefact.

## Headline numbers (unmedicated × pooled × `stress_low_motion_min_count_S60_Mlow` × N_std=1.5 × primary 4d × one-sided elevated)

| metric | value |
|---|---:|
| episodes pre-§4.5 | 10 |
| episodes post-§4.5 (n_clean) | 10 |
| (a) frac event (observed) | 40.0% |
| null median freq (B=10000) | 50.0% |
| (b) discrimination pp | -10.0pp |
| p-value (one-sided, block-permutation E[L]=7) | 0.6250 |
| (c) median magnitude (max_signed_z) | +1.21 |
| RD (point) | -0.100 |
| RD 95% CI | [-0.600, +0.400] |
| OR (point) | 0.67 |
| OR 95% CI | [0.00, 666666.00] |
| crit (a) freq ≥ 60% | FAIL |
| crit (b) disc ≥ +15pp | FAIL |
| crit (c) med ≥ 0.75 | PASS |
| overall verdict | **NOT-SUPPORTED** |

### Per-episode lead-up (pooled unmedicated, n = 10)

| episode date | era | max_signed_z | max&#124;z&#124; | triggered (one-sided ≥1.5) |
|---|---|---:|---:|---|
| 2022-09-16 | train | +0.72 | 1.70 | no |
| 2022-11-23 | train | +1.46 | 1.46 | no |
| 2023-02-04 | train | +3.73 | 3.73 | YES |
| 2023-05-28 | train | +2.02 | 2.02 | YES |
| 2023-06-12 | train | +4.08 | 4.08 | YES |
| 2023-09-07 | train | +2.60 | 2.60 | YES |
| 2023-09-16 | train | +0.82 | 2.41 | no |
| 2023-09-27 | train | +0.96 | 1.31 | no |
| 2024-01-12 | validate | -1.03 | 1.57 | no |
| 2024-02-15 | validate | +0.26 | 1.42 | no |

## §9 verdict-branch interpretation reads

**v3 NOT-SUPPORTED reading** (per v3 §9). One or more of (a) (b)(c) fails on the v3 pooled cell. The locked-pre-reg reading: the motion-filter-refined Wiggers C4 stress signal does NOT carry crash-precursor weight on the unmedicated PHYSICALLY-EXERTION-CONDITIONED subset.

**Recommended primary alternative reading** (from v2 §9, restated): the lived rest-stress trigger may be PROTECTIVE rather than PREDICTIVE - the participant acts on the trigger and prevents the crash. **v3 second alternative reading** (the pacing-behaviour confounder per §8): the unmedicated-phase crashes the §4.2 gate admits may be disproportionately *emotionally / cognitively triggered with incidental physical exertion in the lead-up*, in which case the lack of stress-low-motion signal is exactly what an emotional-trigger story predicts (the body wasn't in the 'stuck sympathetic / walls of orange' state pre-crash; the emotional event simply ran the budget down). Both alternative readings stay open; neither is testable within v3.

**Pacing-behaviour confounder restated** (per v3 §8, verdict-invariant). §4.2 exertion-conditioning is built from Garmin-derived physical exertion only; cognitive, emotional, and orthostatic exertion are not captured. The v3 verdict speaks only to the **physically-exertion-conditioned subset of crashes** and does not generalise to emotionally / cognitively triggered crashes (some excluded by §4.2 entirely, some included with emotional triggers and incidental physical exertion). The corpus has partial proxies (`cat_belasting_emotioneel`, `cat_belasting_cognitief`, `state_symptoom_emotioneel`, `state_symptoom_cognitief`) with the sparsity caveats from DATA_DICTIONARY §9 (presence-conditioned; ~35% unmed-phase fill on note-days; value-0-low-specificity-about-absence; max=2). They are descriptive-only in v3, NOT in §4.2 conditioning.

## Train-only / validate-only descriptive companions (pre-declared INCONCLUSIVE per v3 §5.3; reported for directional consistency only)

| subset | n_clean | (a) rate | median max_signed_z |
|---|---:|---:|---:|
| train-only unmedicated | 8 | 50.0% | +1.74 |
| validate-only unmedicated | 2 | 0.0% | -0.38 |

### Validate-only unmedicated per-episode (n = 2)

| episode date | max_signed_z | max&#124;z&#124; | triggered (one-sided ≥1.5) |
|---|---:|---:|---|
| 2024-01-12 | -1.03 | 1.57 | no |
| 2024-02-15 | +0.26 | 1.42 | no |

## Episode-level leave-one-out (LOO) fragility check (§4.11.5)

Pooled n = 10; k_total triggered = 4 (40.0%). Headline (a) gate: FAIL (≥60%).

LOO (a) range: [33.3%, 44.4%]. Mean ± std: 40.0% ± 5.7%. LOO median magnitude (c) mean ± std: +1.21 ± 0.26.

Load-bearing episodes (removal flips the §5.1 (a) verdict at the 60% gate): **0**.

**Boundary-fragility note** (per v3 §4.11.5, inherited from v2):

> Per v3 §4.11.5 (inherited from v2) boundary-fragility note: at pooled n=10 the §5.1 (a) gate fires when k>=6. LOO flips only happen at k=6 exactly (every firing-drop flips to 5/9=0.556<0.60). At k>=7 no LOO flip (worst 6/9=0.667 passes); at k<=5 no LOO flip (best 5/9=0.556 fails). Observed k=4 -> BELOW BOUNDARY (k<=5); empty load-bearing list at k!=6 is a boundary-distance signal, NOT 'no fragility detected'.

### LOO range table (per drop)

| dropped episode | era | trigger in headline | a_loo | disc_loo_pp | c_loo | flips (a) verdict |
|---|---|---|---:|---:|---:|---|
| 2022-09-16 | train | no | 44.4% | -5.6pp | +1.46 | no |
| 2022-11-23 | train | no | 44.4% | -5.6pp | +0.96 | no |
| 2023-02-04 | train | YES | 33.3% | -16.7pp | +0.96 | no |
| 2023-05-28 | train | YES | 33.3% | -16.7pp | +0.96 | no |
| 2023-06-12 | train | YES | 33.3% | -16.7pp | +0.96 | no |
| 2023-09-07 | train | YES | 33.3% | -16.7pp | +0.96 | no |
| 2023-09-16 | train | no | 44.4% | -5.6pp | +1.46 | no |
| 2023-09-27 | train | no | 44.4% | -5.6pp | +1.46 | no |
| 2024-01-12 | validate | no | 44.4% | -5.6pp | +1.46 | no |
| 2024-02-15 | validate | no | 44.4% | -5.6pp | +1.46 | no |

## Companion-phase descriptive cells (pre-declared INCONCLUSIVE per v3 §5.3)

Phases other than unmedicated have train arms empty by phase-boundary construction (train ends 2023-12-31; consolidation/buildup/afbouw start ≥ 2024-04-09). Only validate arms are reported; none promotes to SUPPORTED.

| phase × era | n_pre_§4.5 | n_clean | (a) rate | median max_signed_z |
|---|---:|---:|---:|---:|
| consolidation × validate | 5 | 2 | 50.0% | +1.51 |
| buildup × validate | 2 | 0 | - | - |
| afbouw × validate | 2 | 0 | - | - |

## Sensitivity ladder (unmedicated × pooled × 6 unique cols × 3 N_std tiers × primary 4d × one-sided)

Per v3 §4.10 + stress_low_motion_primitive §3.2: 6 unique columns + 3 identical-by-construction duplicates (`Mbelow_mod` ≡ `Mlow` at same S threshold; duplicates emitted to result-data.json but not tabulated here). Threshold-monotonicity check: at the same motion class, S=50 ≥ S=60 ≥ S=75 in firing rate (per primitive §8.3). Verdicts diagnostic only; none promotes to SUPPORTED per §5.0.

| col | N_std=1.5 | N_std=2.0 | N_std=2.5 |
|---|---|---|---|
| S50_Mstrict | refu a=50% d=+10pp | refu a=30% d=+0pp | refu a=30% d=+10pp |
| S50_Mlow | refu a=40% d=-3pp | refu a=30% d=+8pp | refu a=20% d=+10pp |
| S60_Mstrict | refu a=40% d=-4pp | refu a=30% d=+0pp | refu a=30% d=+10pp |
| S60_Mlow | refu a=40% d=-10pp | refu a=40% d=+10pp | refu a=30% d=+10pp |
| S75_Mstrict | refu a=60% d=+0pp | refu a=50% d=+10pp | refu a=50% d=+20pp |
| S75_Mlow | refu a=60% d=+3pp | refu a=50% d=+10pp | refu a=50% d=+20pp |

## Headline cell sensitivity arms (transparency only, no SUPPORTED promotion)

| arm | n_clean | verdict | (a) | disc_pp | med_z |
|---|---:|---|---:|---:|---:|
| 4d_primary_bidirectional | 10 | refuted | 70.0% | -10.0pp | +1.86 |
| 5d_secondary_one_sided_elevated | 10 | refuted | 40.0% | -20.0pp | +1.21 |
| 5d_secondary_bidirectional | 10 | refuted | 80.0% | -10.0pp | +1.86 |

## E[L]* data-driven block length (unmedicated pool)

- E[L]* = 3.34; default E[L] = 7; factor-of-2 flag: YES.

Per v3 §4.9 (inherited from v2 + methodology MD): the factor-of-2 re-evaluation rule fires only when the verdict at default E[L] is SUPPORTED. This verdict is NOT-SUPPORTED, so the flag is **descriptive context only** — no re-evaluation is required.

## §4.11 secondary descriptive outcomes

### Same-day Spearman (PRIMARY_COL vs gevoelscore) with §3.4 crash-drop sensitivity

| phase | era | n_full | rho_full | n_no_crash | rho_no_crash | abs(delta rho) |
|---|---|---:|---:|---:|---:|---:|
| unmedicated | train | 476 | -0.041 | 414 | +0.063 | 0.103 **FLAG** |
| unmedicated | validate | 96 | +0.066 | 83 | +0.001 | 0.065 |
| buildup | train | 0 | - | 0 | - | - |
| buildup | validate | 64 | +0.118 | 58 | +0.115 | 0.003 |
| consolidation | train | 0 | - | 0 | - | - |
| consolidation | validate | 620 | +0.025 | 605 | +0.034 | 0.009 |
| afbouw | train | 0 | - | 0 | - | - |
| afbouw | validate | 73 | +0.206 | 69 | +0.191 | 0.015 |

### Spearman on pooled-unmedicated heavy-exertion-conditioned subset (headline cell's universe)

- n = 351, rho = +0.043

### Construct-disambiguation 2x2 (HA-C4b primary vs sibling)

**vs `stress_high_duration_min`** (rho = 0.79):

| phase | era | both_fire | primary_only (HA-C4b only) | sibling_only | neither | n_eval |
|---|---|---:|---:|---:|---:|---:|
| unmedicated | train | 4 | 0 | 1 | 3 | 8 |
| unmedicated | validate | 0 | 0 | 0 | 2 | 2 |
| buildup | validate | 0 | 0 | 0 | 0 | 0 |
| consolidation | validate | 0 | 1 | 0 | 1 | 2 |
| afbouw | validate | 0 | 0 | 0 | 0 | 0 |

**vs `u_dip_count`** (rho = 0.556):

| phase | era | both_fire | primary_only (HA-C4b only) | sibling_only | neither | n_eval |
|---|---|---:|---:|---:|---:|---:|
| unmedicated | train | 0 | 0 | 0 | 0 | 0 |
| unmedicated | validate | 0 | 0 | 0 | 0 | 0 |
| buildup | validate | 0 | 0 | 0 | 0 | 0 |
| consolidation | validate | 0 | 0 | 0 | 0 | 0 |
| afbouw | validate | 0 | 0 | 0 | 0 | 0 |

### Respiration-companion sensitivity (§4.11.4)

Among crash episodes where HA-C4b primary fires (one-sided ≥1.5), did `n_minutes_resp_above_18` also show z > 0 in the lead-up?

| phase | era | primary_fired_resp_elev | primary_fired_resp_normal |
|---|---|---:|---:|
| unmedicated | train | 3 | 0 |
| unmedicated | validate | 0 | 0 |
| buildup | validate | 0 | 0 |
| consolidation | validate | 1 | 0 |
| afbouw | validate | 0 | 0 |

## Inherited v2 caveats (v3 §8 wholesale-inherited block)

- **v1 -> v2 relock disclosure**. The headline cell was relocked from `consolidation × both-eras` (v1) to `unmedicated × train+validate pooled` (v2); researcher-degrees-of-freedom concern from the v1->v2 relock is acknowledged. v3 inherits this caveat; the v3-specific concern is the §4.3 1b.ii drop discipline cost surfaced above.
- **No cross-era independent replication for the pooled headline cell**. v3 (inheriting v2) pools train + validate within unmedicated to clear the n ≥ 10 bar; the HA11-family both-eras-independent rule is abandoned for this hypothesis. The compensating mechanism is the descriptive directional-consistency companion on the train-only and validate-only subsets reported above. Not a full substitute for independent verdicts.
- **Power-calc dispatch**. Inapplicable per Daza 2018 within-subject design - the n-of-1 corpus does not have separate treatment and control arms in the sense classical power calculations require. The block-permutation null at E[L]=7 (§4.9) is the within-subject inferential machinery; the §5.1 (a)+(b)+(c) gates determine SUPPORTED / NOT-SUPPORTED rather than a power-thresholded p-value.
- **Unmedicated = pre-citalopram corpus, not 'no medication overall'**. The participant was unmedicated for SSRI in 2022-04 -> 2024-04 but had other lived-experience interventions in that window (CPAP started 2024-01-10 - the last ~3 months of unmedicated; daily pacing protocols evolved; PEM-pacing practice was being established). §4.2 exertion-conditioning and §4.5 phase-stratified baseline absorb most of this, but it is residual context.
- **Garmin stress is partly motion-sensitive**; the motion filter and respiration-companion sensitivity above are the within-test checks.
- **Garmin `intensity` classification has an 81% gap**; minutes without an explicit intensity record default to 'low motion' (generous; per stress_low_motion_primitive §3.3a).
- **Citalopram dose-modulates the underlying stress channel** (per citalopram_dose_response_stress_mean_sleep.md §5.6: 30 mg plasma suppresses raw stress by ~12-17 points). Per-phase treatment is the dose-confound control; raw count magnitudes not directly comparable across phases. The unmedicated phase headline is the cleanest test ground precisely because the suppression cascade is absent.
- **The `below_moderate` motion class is identical-by-construction to `low_or_below`** in this corpus; the 9-column ladder effectively reduces to 6 unique columns.
- **Exertion-conditioning shrinks n** sharply; per-phase verdicts outside unmedicated × pooled may be inconclusive on low-n phases (reflected in the consolidation / buildup / afbouw companion table above).
- **Construct rho vs `stress_high_duration_min` = 0.79** - close sibling; the construct-disambiguation 2x2 above is the empirical test of whether the motion filter does analytical work.
- **The participant is operationally using the rest-stress trigger** (per garmin_pacing_practice.md §3.3); the protocol disturbs the test. NOT-SUPPORTED reads may indicate a PROTECTIVE-rather-than-PREDICTIVE trigger; SUPPORTED reads survive despite the disturbance.
- **`crash_v2` mixes mechanisms**; multi-mechanism crash population dilutes any one-mechanism precursor signal.
- **Multi-comparison defence**: the §5.0 single-cell discipline + the stationary-bootstrap null at E[L]=7 are the inferential machinery; descriptive companions never promote per §5.2.
- **The bootstrap RD/OR CIs are computed against the stationary-bootstrap null distribution** (varying p_null with fixed observed p_crash); this captures null-side variability only. A fuller joint-bootstrap CI would require resampling crash episodes as well; deferred (inherited from v1 §8).
- **§4.11.5 LOO boundary-fragility**: an empty load-bearing list is NOT 'no fragility detected' - it is a boundary-distance signal indicating k is not exactly at the 60% gate boundary. Restated in the LOO section above.

