# HA-C3p — Convex stress→fatigue shape on personal-baseline-anchored bins (Wiggers C3 sister pre-reg)

## Authorship

**Drafted 2026-06-23** by Claude (Opus 4.7, 1M context) in producer-mode under user authorisation per [CONVENTIONS §1.1](../../../CONVENTIONS.md#11-producer-mode-claude-edits-the-docs--codebase-the-default). Authorising user: Willem. **§3.2 fresh-session drafting per [`hypothesis_lock_process.md` §3.2](../../../methodology/hypothesis_lock_process.md#32-drafting-step-step-1-of-the-arc)** per the session handoff brief at `C:/Users/Gebruiker/.claude/plans/session-HA-C3p-pre-reg-drafting-handoff-2026-06-23.md`. Worktree-isolated session.

**Drafting trigger**: sister pre-reg to [HA-C3 v2 r1](../HA-C3/hypothesis.md) drafted 2026-06-23 at commit `724c814`. HA-C3 v2 is the **Wiggers-verbatim-anchored test arm** (bins `[0,30), [30,40), [40,60), [60,100]` preserve Wiggers' specific 30→40 numerical step at the B2-B3 boundary). HA-C3p is the **project-canonical personal-baseline-anchored sister test** per [CONVENTIONS §3.1](../../../CONVENTIONS.md#31-personal-baseline-not-absolute-thresholds) ("Personal baseline, not absolute thresholds"): same substrate (`all_day_stress_avg` × `gevoelscore`), same Wiggers-inspired convex-shape question, BUT bins anchored to the participant's own distribution (equal-N quintiles on the full Stratum 4 pool) rather than Wiggers' specific numerical edges. The user's framing: HA-C3 v2 stays honest against the original Wiggers document; **HA-C3p goes further to see if we can find the mechanism Wiggers is describing besides the numbers she uses**.

**Data exposure context** (audit-able): the drafter has seen (a) the v1 partial-pool descriptives (pool n = 581 unmedicated, stress median = 34, gevoelscore median = 4, B2-B3-B4 trajectory 3.958 → 4.265 → 3.860) per [`result-v1-archived.md`](../HA-C3/result-v1-archived.md); (b) the full-Stratum-4 pool sample size (n = 1351 days post-§4.3 gate per the bin-computation snapshot below); (c) the §4.1 quintile boundary values themselves (28, 31, 34, 37 per `np.quantile` at q = [0.2, 0.4, 0.6, 0.8]). The drafter has NOT inspected the per-bin gevoelscore means on the quintile-binned full-Stratum-4 distribution; the joint bin-mean trajectory is deferred to dry-run per [`hypothesis_lock_process.md` §3.9](../../../methodology/hypothesis_lock_process.md#39-run-step-post-lock). The v1 partial-pool trajectory enters as a **caveat-class prior** per [CONVENTIONS §4.2](../../../CONVENTIONS.md#42-caveats-yes-a-priori-claims-no) informing HA-C3p's interpretation; HA-C3p does NOT pre-commit to an inverted-U / threshold-pattern alternative claim.

**Locked decisions at draft time** (load-bearing pre-commits per [`hypothesis_lock_process §3.2 step 5`](../../../methodology/hypothesis_lock_process.md#32-drafting-step-step-1-of-the-arc) + session handoff §3 six surfaced decisions):

1. **Bin computation pool** — **full Stratum 4** (LC era + non-NaN both columns + April 2024 cluster excluded + first 21 device-baseline days excluded; n = 1351 days per the §4.1 snapshot). NOT the unmedicated-only sub-arm. Rationale: (i) larger n per bin (~270/bin vs ~80-100/bin on the unmedicated sub-pool); (ii) **cross-arm cleanliness** — sub-arms (§5.A unmedicated headline, §5.B dose-adjusted cross-phase) REUSE the same full-pool boundaries rather than re-computing per sub-arm, which keeps the bin-edge meaning stable across arms; (iii) cross-test comparability with HA-C3 v2 which also uses full-pool framing.

2. **z-score sensitivity arm baseline window** — **28-day lagged** baseline `(all_day_stress_avg[d] − μ_28d_lagged[d]) / σ_28d_lagged[d]` per HA01b-recomputed precedent + [CONVENTIONS §3.1](../../../CONVENTIONS.md#31-personal-baseline-not-absolute-thresholds) prototype. Rationale: smaller window → more sensitive to recent state; consistent with HA01b-recomputed; the 90d-30d-lagged window per [CONVENTIONS §3.2](../../../CONVENTIONS.md#32-lagged-baseline-for-sustained-push-hypotheses) is a sustained-push variant scoped for exertion-class metrics, not for the C3 shape claim. Documented as §4.8(b) sensitivity arm; the **raw quintile bins are primary** because the bin-edge stability across §5.A / §5.B arms requires a stationary edge spec (a rolling-baseline z-score has edges that drift in raw stress-units over time).

3. **Bin labels** — **Q1-Q5** (quintile-explicit), not B1-B5. Rationale: Q1-Q5 makes the personal-baseline-anchored quintile semantics explicit, and visually distinguishes HA-C3p's bin scheme from HA-C3 v2's B1-B4 (Wiggers-verbatim) bins in cross-test discussion / agreement-matrix readings (§9). Distinct labelling also prevents accidental cross-reference of the same numeric index meaning different stress ranges between the two pre-regs.

4. **Bin boundary computation timing** — **at draft time** (pre-commit specific boundary values; documented inline at §4.1). Rationale: defers no decision to test-execution time; eliminates boundary-drift risk if the per_day_master snapshot moves between draft and execution (per [feedback_check_index_before_add] + [feedback_audit_before_push] discipline). Snapshot SHA documented at §4.1 for reproducibility audit.

5. **Cross-test interpretation framing** — **HA-C3p result.md §6 open-questions** carries the 4-cell agreement matrix with HA-C3 v2 (not a separate cross-test reviews/ doc). Rationale: HA-C3p is the project-canonical personal-baseline arm per [CONVENTIONS §3.1](../../../CONVENTIONS.md#31-personal-baseline-not-absolute-thresholds); the cross-test reading naturally lives in HA-C3p's open-questions because HA-C3p is the canonical primary. HA-C3 v2's result.md §6 will cross-link back, but the cross-test interpretation home is HA-C3p's. Each pre-reg stands on its own §5 verdict; the cross-test reading is a §6 framing.

6. **HA-C3p Wiggers register-row treatment** — **note under existing C3 register row at HA-C3p LOCK time per [`hypothesis_lock_process §3.8 gate 3`](../../../methodology/hypothesis_lock_process.md#38-lock-step-stage-5-of-the-arc)**, NOT as a separate register row. Rationale: one register entry per Wiggers source-row; sister pre-regs are sub-references not register rows. This avoids the multiplicity inflation of treating HA-C3 v2 + HA-C3p as two separate Wiggers C3 register entries (they test the same Wiggers source row at different operationalisation levels). Register-row update happens at lock time per [`hypothesis_lock_process §3.8 gate 3`](../../../methodology/hypothesis_lock_process.md#38-lock-step-stage-5-of-the-arc), NOT at this draft commit.

### §3.8 gate-verification block (template at draft time per [`hypothesis_lock_process.md` §3.8](../../../methodology/hypothesis_lock_process.md#38-lock-step-stage-5-of-the-arc))

The four [§3.8 lock-blocking gates](../../../methodology/hypothesis_lock_process.md#38-lock-step-stage-5-of-the-arc) will be confirmed at lock-commit time. Pre-flight template:

1. **Power-calc dispatch** — to be confirmed MET via §8 caveat 1 (Daza 2018 within-subject design citation; block-permutation null at E[L] = 7 is the within-subject inferential machinery; the §5.1 3-condition gated verdict determines SUPPORTED/PARTIAL/REJECTED; INCONCLUSIVE per §5.2 is the operational definition of "underpowered for this cell"). Equal-N quintile-bin design makes total-pool underpower the only meaningful INCONCLUSIVE branch.
2. **Multi-comparison discipline** — to be confirmed MET via §5.0 single-cell headline lock (one headline cell: §5.A unmedicated × 5-bin × `gevoelscore` × 3-condition gated outcome on the full-pool-derived quintile bins); every other arm — §5.B dose-adjusted cross-phase (§4.4), z-scored sensitivity (§4.8), crash-drop (§4.6), t+1 lagged (§4.8), train+validate M3 overlay (§4.8) — is descriptive sensitivity ONLY and cannot promote to SUPPORTED. Conjunctive 3-of-3 gate provides effective multiplicity control at the SUPPORTED bar.
3. **Register-row pointer** — to be confirmed MET at lock-commit time per Locked decision 6: HA-C3p will be added under the existing [`wiggers_testable_hypotheses.md` Tier 1 C3 row](../../../wiggers_testable_hypotheses.md#tier-1--source-verified-verbatim--no-family-history-priority-pre-regs) as the personal-baseline-anchored sister test pointer (HA-C3 v2 remains the primary register-row anchor as the Wiggers-verbatim test). **Register-row update happens at HA-C3p LOCK time, NOT at this draft commit.**
4. **Re-audit clean OR §3.6 compression** — to be confirmed at lock time after the fresh-session `/research-review` audit. HA-C3p is a sister pre-reg with substantively distinct operationalisation from HA-C3 v2; the audit must verify (a) the personal-baseline framing per [CONVENTIONS §3.1](../../../CONVENTIONS.md#31-personal-baseline-not-absolute-thresholds) is correctly bound; (b) the quintile-bin machinery (5 bins, mean of 3 second-differences, 4-knot spline, ≥3-of-5 midpoint visual gating) cascades correctly from v1's 5-bin form without inheritance from v2's 4-bin reductions; (c) the cross-arm bin-edge cleanliness discipline (sub-arms REUSE full-pool edges, never re-compute) is honored everywhere.

| revision | date | summary |
|---|---|---|
| r1 | 2026-06-23 | drafted at THIS COMMIT per session handoff `session-HA-C3p-pre-reg-drafting-handoff-2026-06-23.md`. Sister pre-reg to HA-C3 v2 r1 `724c814` (Wiggers-verbatim arm). HA-C3p tests the underlying convex stress→fatigue shape claim Wiggers describes on personal-baseline-anchored bins per [CONVENTIONS §3.1](../../../CONVENTIONS.md#31-personal-baseline-not-absolute-thresholds). Equal-N quintile bins on full Stratum 4 distribution (n=1351; ~270 days per bin). §5.A unmedicated headline + §5.B dose-adjusted cross-phase sensitivity inherited from v2 per [`citalopram_phase_stratification §4`](../../../methodology/citalopram_phase_stratification.md#4-per-channel-inheritance-rules) CONFIRMED-channel inheritance. **Status: drafted, not locked.** |

**Status**: drafted, not locked.

---

**Pre-registration drafted 2026-06-23 as r1**, BEFORE any HA-C3p test run, BEFORE any inspection of the per-bin gevoelscore means on the quintile-binned full-Stratum-4 distribution. The drafter has the v1 partial-pool descriptives (per [`result-v1-archived.md`](../HA-C3/result-v1-archived.md): pool n = 581 unmedicated, stress median 34, gevoelscore median 4, B2-B3-B4 trajectory 3.958 → 4.265 → 3.860) as caveat-class context per [CONVENTIONS §4.2](../../../CONVENTIONS.md#42-caveats-yes-a-priori-claims-no), but the §4.1 quintile bin scheme is a substantively-distinct operationalisation from v1's Wiggers-verbatim bins, and the per-bin gevoelscore means on the new bin scheme have NOT been inspected. Any change after lock creates HA-C3p-v2 with r1 archived.

HA-C3p tests the **underlying convex stress→fatigue shape claim** Wiggers describes (PDF lines 1357-1368, "Annual Stress Scores": "a day with a score of 40 is much more tiring than a day with a score of 30 — a step appears very small on the graph, but it isn't; this graph shows a kind of stair step") on personal-baseline-anchored bins, rather than the Wiggers-verbatim numerical 30→40 anchor which HA-C3 v2 tests. The two pre-regs are sister operationalisations of the same Wiggers C3 substantive question.

## 1. Claim

Within the LC frame, on the full Stratum 4 single pool (LC era through today, citalopram-channel-inheritance handled per §4.4), the **marginal effect of `all_day_stress_avg` on `gevoelscore` increases in magnitude as `all_day_stress_avg` rises across the participant's own stress distribution**. The stress→fatigue function is **convex on personal-baseline-anchored quintile bins** — gevoelscore drops by more per quintile at higher quintiles than at lower quintiles.

**Headline cell** (§5.A unmedicated primary per §4.4): unmedicated phase × full Stratum 4 single pool × `all_day_stress_avg` binned at the §4.1 personal-baseline-anchored quintile boundaries (Q1 `[0, 28)`, Q2 `[28, 31)`, Q3 `[31, 34)`, Q4 `[34, 37)`, Q5 `[37, 100]`) × `gevoelscore` bin-mean × {Jonckheere-Terpstra monotone-decreasing test + convexity second-difference contrast `S = (Δ²_2 + Δ²_3 + Δ²_4) / 3` + spline non-linearity test with 4 internal knots at the quintile bin boundaries + spline-second-derivative sign at ≥ 3 of 5 quintile bin midpoints} × block-permutation null E[L] = 7 × 3-condition gated verdict per §5.

**Sister-pre-reg pointer** (load-bearing per session handoff §1 framing): HA-C3p is the **personal-baseline-anchored sister** to [HA-C3 v2 r1](../HA-C3/hypothesis.md) (the **Wiggers-verbatim-anchored** primary test of the same Wiggers C3 substantive question). The two pre-regs are sister operationalisations:

| HA-C3 v2 verdict | HA-C3p verdict | reading |
|---|---|---|
| SUPPORTED | SUPPORTED | strong Wiggers C3; both numerical anchor AND underlying shape fire |
| SUPPORTED | REJECTED | suspicious bin-edge artefact in v2's Wiggers-verbatim (under-fit by personal-range test), or vice versa |
| REJECTED | SUPPORTED | convex shape exists on participant's range, but NOT at Wiggers' specific anchors — Wiggers' numbers are wrong-for-this-participant, underlying shape is real |
| REJECTED | REJECTED | informative null on both operationalisations |

Each pre-reg's §5 verdict stands on its own; the 4-cell agreement-matrix interpretation lives in HA-C3p's result.md §6 open-questions per Locked decision 5.

**Direction of effect under SUPPORTED** (HA-C3p): (a) monotone-decreasing bin-means across Q1 → Q5 (higher-stress quintiles have LOWER gevoelscore); (b) accelerating decrement (the step from Q4 to Q5 is LARGER in magnitude than the step from Q1 to Q2; quantified as `S = (Δ²_2 + Δ²_3 + Δ²_4) / 3 < 0`); (c) spline non-linearity term significant with shape visually consistent with convexity (≥ 3 of 5 quintile midpoints showing negative spline second derivative).

**Verdict rule** (3-condition gated): see §5.

## 2. Why we think this

Three priors anchor HA-C3p:

**(a) Wiggers source — verbatim** (qualitative claim, mechanism-not-numbers reading): the Wiggers PDF lines 1357-1368 ("Annual Stress Scores") describe a **stair-step convex stress→fatigue mechanism** — *"a day with a score of 40 is much more tiring than a day with a score of 30. Such a step appears very small on the graph, but it isn't. This graph shows a kind of stair step. This person has overexerted themselves."* Per the [C3 register verification log](../../../wiggers_testable_hypotheses.md#c3--non-linear--convex-stressfatigue) (batch 2 2026-06-12). HA-C3 v2 tests the verbatim 30→40 numerical anchor; **HA-C3p tests the underlying mechanism Wiggers describes** — the convex-cost shape — on the participant's own stress register, on the prior that the mechanism is testable on any well-defined stress register even if Wiggers' specific numerical anchors don't fit this participant's distribution. The qualitative Wiggers claim is mechanism-bound, not number-bound.

**(b) [CONVENTIONS §3.1](../../../CONVENTIONS.md#31-personal-baseline-not-absolute-thresholds) personal-baseline discipline**: "For any PEM-pacing metric, work with deviations from the participant's own rolling baseline rather than absolute cutoffs. A max HR of 130 is a spike for one PEM patient and a calm afternoon for another." The personal-baseline framing is the project-canonical operationalisation discipline; HA-C3p is the project-canonical sister to HA-C3 v2's Wiggers-verbatim absolute-threshold framing. Equal-N quintile bins on the participant's own stress distribution are the cleanest expression of personal-baseline-anchored binning (z-scored-against-personal-rolling-baseline bins are the alternative; documented as §4.8(b) sensitivity arm per Locked decision 2).

**(c) HA-C3 v1 partial-pool non-monotone observation as caveat-class prior** per [CONVENTIONS §4.2](../../../CONVENTIONS.md#42-caveats-yes-a-priori-claims-no): v1's HALT-time partial-pool descriptive trajectory (per [`result-v1-archived.md`](../HA-C3/result-v1-archived.md)) across the 3 populated bins was gevoelscore mean **3.958 → 4.265 → 3.860** across v1's B2 [20,30) → B3 [30,40) → B4 [40,60), peak at v1 B3 = stress 30-40, **non-monotone** at the descriptive level. This v1 partial-pool observation is a **caveat-class prior informing HA-C3p's verdict-interpretation, NOT a quasi-result and NOT promoted to a substantive HA-C3p output**. HA-C3p's primary §5.1 verdict will formally evaluate whether this non-monotone pattern is statistically robust on the personal-range bins (which have higher resolution than v1's coarser scheme — 5 bins vs 5 bins with much finer mid-range divisions because the quintiles cluster at the dense median region of the participant's distribution). If the v1 non-monotone observation reflects a real inverted-U / threshold-pattern alternative shape, HA-C3p's quintile-bin scheme is more sensitive than HA-C3 v2's coarser 4-bin Wiggers-verbatim scheme to detecting it; but **HA-C3p does NOT pre-commit to an inverted-U / threshold-pattern alternative claim** — that would require a separate §3.2 fresh-session pre-reg, which is out of HA-C3p's scope.

**The CONFIRMED dose-response on `all_day_stress_avg` establishes channel signal-bearing causality** (inherited from HA-C3 v2 §2(c) — load-bearing for the §4.4 citalopram approach): the v3 multi-channel dose-response analysis ([`citalopram_dose_response_stress_mean_sleep.md §5.6`](../../../methodology/citalopram_dose_response_stress_mean_sleep.md#56-v3-amendment--multi-channel-confirmation-added-2026-06-14)) confirmed `all_day_stress_avg` as dose-modulated at +0.57/mg buildup-post-CPAP β (p = 0.0003, CI [+0.24, +0.89]). This establishes that `all_day_stress_avg` is a causally-modifiable channel and binds HA-C3p's §4.4 to the §5.A unmedicated headline + §5.B dose-adjusted cross-phase sensitivity arm pattern per [`citalopram_phase_stratification §4`](../../../methodology/citalopram_phase_stratification.md#4-per-channel-inheritance-rules) CONFIRMED-channel inheritance.

**Sister-test context** (informational; no cross-test prior on convexity is claimed):

- **HA-C3 v2 r1** (Wiggers-verbatim sister): drafted `724c814` 2026-06-23; the test of Wiggers' specific 30→40 numerical anchor on `[0,30), [30,40), [40,60), [60,100]` 4-bin scheme. **Cross-test interpretation per §1's 4-cell agreement matrix**.
- **HA-C4 v2 REJECTED at daily-aggregate** (commit `52bddb5`): inherited from v1 §2; substantively distinct claim (recovery-dynamics triad, not same-day shape).
- **HA11 SUPPORTED on train** (within-day stress U-dip count): inherited from v1 §2; structurally distinct (within-day vs cross-day-aggregate).

## 3. Data sources

Inherited from [HA-C3 v2 §3](../HA-C3/hypothesis.md#3-data-sources) verbatim — same substrate (`all_day_stress_avg` × `gevoelscore` × `is_crash` × `citalopram_phase` × `era`), different binning. Source: `$GEVOELSCORE_DATA_PATH/unified/per_day_master.csv`. PK-smoothed dose `dose_plasma_mg(d)` for §5.B sensitivity per [`citalopram_dose_response §2.3`](../../../methodology/citalopram_dose_response_stress_mean_sleep.md#23-pk-smoothed-plasma-proxy-primary-exposure). `is_crash` from crash_v2 labels. **No new extraction required.**

## 4. Measurement protocol

### 4.1 Bin specification (primary; locked at draft time per Locked decision 4)

The predictor `all_day_stress_avg` is binned into **5 equal-N quintile bins** computed on the **full Stratum 4 single pool** (per §4.2 + Locked decision 1) with **left-inclusive, right-exclusive intervals (except Q5 which is closed-above)**:

| bin id | label | range | rationale |
|---|---|---|---|
| Q1 | low-quintile | `[0, 28)` | bottom quintile of the full-Stratum-4 distribution; the participant's "calm-day" register on their own scale |
| Q2 | mid-low-quintile | `[28, 31)` | second quintile; tightly packed around the lower-median region |
| Q3 | mid-quintile | `[31, 34)` | central quintile; straddles the participant's stress median (32 on full pool; 34 on unmedicated sub-arm) |
| Q4 | mid-high-quintile | `[34, 37)` | fourth quintile; tightly packed around the upper-median region |
| Q5 | high-quintile | `[37, 100]` | top quintile; the long upper tail where the convex-cost prediction is sharpest |

**Bin midpoints** (used for spline second-derivative check per §4.5.1(c)):
- Q1 midpoint x = 14 (= (0 + 28) / 2); **dropped from the count** because the natural-cubic boundary condition at x = 28 forces near-zero second derivative throughout the leftmost segment by construction (mirrors v1 r2's drop of B1's midpoint at x = 10 + HA-C3 v2 r1's drop of B1's midpoint at x = 15)
- Q2 midpoint x = 29.5
- Q3 midpoint x = 32.5
- Q4 midpoint x = 35.5
- Q5 midpoint x = 68.5 (= (37 + 100) / 2)

The visual-gating count operates over **5 quintile midpoints {Q1: x=14; Q2: x=29.5; Q3: x=32.5; Q4: x=35.5; Q5: x=68.5}**, with Q1 dropped per the natural-cubic boundary-condition rationale. **Pass requires ≥ 3 of the 4 contributing midpoints {Q2, Q3, Q4, Q5} showing NEGATIVE spline-second-derivative, with strict sign agreement (a positive-sign midpoint does NOT count toward the threshold)**. Gating threshold matches v1 r2's discipline (≥ 3 of 4 contributing midpoints; v1 had 4 contributing midpoints from {B2, B3, B4, B5}).

**Bin boundary computation snapshot** (audit-able; per Locked decision 4):
- **`per_day_master.csv` SHA-256**: `d0ff9253f7199a40165b6d229a4a68534b4a36b7de87bfbe8a18c23bb9ab189d` (computed 2026-06-23 at draft time)
- **Path**: `$GEVOELSCORE_DATA_PATH/unified/per_day_master.csv`
- **Computation**: `np.quantile(stress_full_stratum4_pool, [0.2, 0.4, 0.6, 0.8])` with linear interpolation (numpy default) on the post-§4.3-gate full Stratum 4 pool (n = 1351 days)
- **Raw quintile boundaries** (pre-rounding): `[28.0, 31.0, 34.0, 37.0]` (integer-valued because `all_day_stress_avg` is int 0-100 per [DATA_DICTIONARY.md §7B](../../../DATA_DICTIONARY.md))
- **Bin script for audit reproducibility**: `scripts/compute_HA-C3p_quintile_boundaries.py` (worktree-side; the canonical detection script `test.py` will re-validate the boundaries at dry-run against the same snapshot SHA)

**Per-bin n at draft time on the full Stratum 4 pool** (computed at draft time per §4.1 bin script):

| bin | range | full-pool n |
|---|---|---:|
| Q1 | `[0, 28)` | **248** |
| Q2 | `[28, 31)` | **253** |
| Q3 | `[31, 34)` | **294** |
| Q4 | `[34, 37)` | **251** |
| Q5 | `[37, 100]` | **305** |
| **total** | — | **1351** |

Quintiles are slightly unequal because `all_day_stress_avg` is integer-valued and the underlying distribution has discrete mass at integer stress values (so quintile boundaries rounded to integers split the distribution into bins that approximate but don't exactly hit n/5 = 270.2). All quintile bin counts are **comfortably above the §7.5 sanity-gate ≥ 30 bar** for the full-pool primary computation.

**Per-bin n at draft time on the §5.A unmedicated sub-arm** (computed REUSING the full-pool boundaries per Locked decision 1 — sub-arms do NOT re-compute boundaries):

| bin | range | unmedicated n |
|---|---|---:|
| Q1 | `[0, 28)` | **45** |
| Q2 | `[28, 31)` | **80** |
| Q3 | `[31, 34)` | **129** |
| Q4 | `[34, 37)` | **138** |
| Q5 | `[37, 100]` | **189** |
| **total** | — | **581** |

**Observation surfaced at draft time** (load-bearing for §7.2 + §8 caveats): the unmedicated sub-arm bin counts are **right-shifted relative to the full-pool quintiles** (Q1 = 45 vs full-pool Q1 = 248 — i.e. only ~18% of unmedicated days fall in the full-pool's bottom quintile, vs 20% by construction on the full pool). The shift is consistent with the +0.57/mg dose-modulation on `all_day_stress_avg` per [`citalopram_dose_response §5.6.1`](../../../methodology/citalopram_dose_response_stress_mean_sleep.md#561-per-channel-three-pronged-read): medication (consolidation + afbouw phases of Stratum 4) compresses the stress range; the unmedicated phase populates the higher quintiles disproportionately. **All five unmedicated bins still PASS the §7.5 ≥ 30 sanity-gate bar (minimum = 45 for Q1)**; HA-C3p's §5.A primary headline is testable on the unmedicated sub-arm using the full-pool boundaries. This right-shift is logged as §7.2 + §8 caveat (the unmedicated headline reads on the upper 4 quintiles of the participant's own distribution more heavily than on the full distribution; the bottom quintile Q1 has n = 45 which is the borderline cell).

**Boundary discipline**: bin edges are at the quintile values of the full-Stratum-4 distribution; **NOT** at Wiggers-verbatim integer stress-units (HA-C3 v2 carries that operationalisation). The personal-baseline alignment is the load-bearing justification per [CONVENTIONS §3.1](../../../CONVENTIONS.md#31-personal-baseline-not-absolute-thresholds) ("Personal baseline, not absolute thresholds"). **Cross-arm cleanliness**: sub-arms (§5.A unmedicated, §5.B dose-adjusted cross-phase, §4.6 crash-dropped, §4.8 train/validate, §4.8 t+1 lagged) REUSE these exact edges; they do NOT re-compute quintiles per sub-arm.

**Pre-flight check** (§7.5 sanity gate 1 below): the descriptive distribution of `all_day_stress_avg` on the unmedicated pool is reported at dry-run; HALT if any of Q1-Q5 has < 30 observations on the §5.A unmedicated sub-arm. The draft-time forecast above shows all five unmedicated bins ≥ 30 (minimum 45 for Q1); no halt expected.

### 4.2 Stratum + pool (locked; per Locked decision 1)

**Primary pool**: full Stratum 4 single pool per [`train_validate_split_fate.md`](../../../methodology/train_validate_split_fate.md) — `date >= 2022-04-04` (LC era start) through today's data cutoff. NOT restricted to unmedicated. The **bin-computation pool** uses the full Stratum 4 pool to derive the quintile boundaries (per Locked decision 1; n = 1351 days at the draft-time snapshot). The **headline verdict cell** restricts to the §5.A unmedicated sub-arm (per §4.4 + Locked decision per HA-C3 v2 inheritance; n = 581 unmedicated days reusing the full-pool quintile boundaries). The cross-arm cleanliness pattern — bin boundaries from full pool, verdict cell from sub-pool — keeps the bin-edge meaning stable across the §5.A / §5.B arms.

Train/validate split is NOT used as a primary verdict surface; see §4.8 below for the M3 descriptive overlay.

### 4.3 Day-validity gate (locked; inherited from HA-C3 v2 §4.3)

Inherited from [HA-C3 v2 §4.3](../HA-C3/hypothesis.md#43-day-validity-gate-locked) verbatim:

1. `T` is in the LC era (`date >= 2022-04-04`).
2. For the §5.A unmedicated primary headline: `T` is in the unmedicated phase (`date <= 2024-04-08`). For the §5.B cross-phase sensitivity arm: all Stratum 4 phases.
3. `T` is NOT in the April 2024 cluster (`2024-04-09 → 2024-04-16`) per [`citalopram_phase_stratification`](../../../methodology/citalopram_phase_stratification.md) (structural exclusion).
4. `T` has a non-NaN `all_day_stress_avg` value (excludes the sentinel-filtered dates per DATA_DICTIONARY §7B).
5. `T` has a non-NaN `gevoelscore` value (excludes pre-2022-09-03 days where gevoelscore was not yet logged).
6. `T` is NOT in the first 21 days of `has_garmin_uds == True` (device-baseline warmup; inherited from v1 §6 + HA-C3 v2 §6 → §4.3 binding consistent).

**Expected post-gate pool size**: **full Stratum 4 n = 1351** at draft-time snapshot (per §4.1); **§5.A unmedicated sub-arm n = 581** (matches v1 dry-run per [`result-v1-archived.md`](../HA-C3/result-v1-archived.md)).

### 4.4 Citalopram phase treatment (locked; inherited from HA-C3 v2 §4.4 — load-bearing per `citalopram_phase_stratification §4`)

Inherited from [HA-C3 v2 §4.4](../HA-C3/hypothesis.md#44-citalopram-phase-treatment-locked--5a-primary-load-bearing-inherited-from-v1) wholesale. **Primary approach**: **§5.A per-phase stratification** with the **unmedicated phase as the headline pool** (HA-C3p §5.A primary headline cell). **Secondary cross-phase sensitivity**: §5.B dose-adjusted predictor `all_day_stress_avg_adj(d) = all_day_stress_avg(d) − 0.57 × dose_plasma_mg(d)` per [`citalopram_phase_stratification §5.B`](../../../methodology/citalopram_phase_stratification.md#5b-dose-adjusted-predictor-recommended-for-cross-phase-tests) using the locked +0.57/mg buildup-post-CPAP β per [`citalopram_dose_response_stress_mean_sleep §5.6.1`](../../../methodology/citalopram_dose_response_stress_mean_sleep.md#561-per-channel-three-pronged-read). §5.C unmedicated-only restriction dispatched: §5.A primary IS effectively unmedicated-only at the headline level.

**Per-phase sample minimums**: ≥ 30 per bin to produce a descriptive bin-mean; below this, INCONCLUSIVE per §5.4 for that phase's read (does NOT halt the primary). At draft time, all 5 §5.A unmedicated bins have ≥ 45 (per §4.1); the §5.B cross-phase pool is the full Stratum 4 n = 1351 with bin counts ≥ 248 each (per §4.1 above; both pass comfortably).

**§5.B dose-adjustment bin-edge note** (load-bearing): the §5.B sensitivity arm runs on `all_day_stress_avg_adj` (the dose-adjusted predictor). For cross-arm cleanliness per Locked decision 1, the §5.B arm REUSES the same §4.1 quintile boundaries `[0, 28, 31, 34, 37, 100]` applied to `all_day_stress_avg_adj` rather than re-computing dose-adjusted-quintile boundaries. The trade-off: §5.B bin-counts will shift relative to the full-pool quintile counts because `all_day_stress_avg_adj` has a slightly different distribution than the raw `all_day_stress_avg`; this is reported descriptively at dry-run and at result.md time. A re-derivation-of-quintiles-from-dose-adjusted-distribution variant is NOT part of the locked pre-reg (would introduce a second bin-edge spec that complicates the §5 verdict).

### 4.5 Statistical machinery (locked; 5-bin form per the personal-range quintile spec)

#### 4.5.1 Primary tests — three conditions (all on the §5.A unmedicated pool)

For the unmedicated × 5-bin × `gevoelscore` bin-mean trajectory `(m1, m2, m3, m4, m5)` indexed Q1 → Q5:

**Condition (a) — Monotone decreasing**: **Jonckheere-Terpstra one-sided test** for monotone-decreasing trend across the 5 quintile bins. H0: no trend across bins; H1: bins ordered Q1 → Q5 show monotone-decreasing `gevoelscore` distributions. Test statistic: standard Jonckheere-Terpstra `J*` standardised by the null SD; one-sided p-value via block-permutation at E[L] = 7 per §4.7 below. **Pass condition**: empirical one-sided p < 0.05 in the decreasing direction.

**Condition (b) — Convexity second-difference contrast**: compute the **three** second-differences of bin-means `Δ²_i = m_{i+1} − 2·m_i + m_{i-1}` for i ∈ {2, 3, 4}. The convexity statistic is the **mean** `S = (Δ²_2 + Δ²_3 + Δ²_4) / 3`. Under SUPPORTED (gevoelscore convexly decreasing in stress-bin), `S < 0` systematically. **One-sided block-permutation test at E[L] = 7**: H0: `E[S] = 0`; H1: `E[S] < 0`. Empirical p-value computed from the null distribution of `S` under block-permutation of the `(date, all_day_stress_avg)` label sequence (keeping `gevoelscore` fixed in place); B = 10,000 resamples. **Pass condition**: empirical one-sided p < 0.05 AND `S < 0` (correct direction).

This is the v1 r2 form of the convexity contrast (mean of 3 second-differences for a 5-bin trajectory), inherited because HA-C3p has 5 bins. HA-C3 v2 has 4 bins → mean of 2 second-differences; HA-C3p's 5-bin form recovers the v1 r2 machinery.

#### 4.5.1 Companion contrast (descriptive overlay; per §4.5.1(b) Helmert-style precedent)

Report `c · m` where `c = (+2, -1, -2, -1, +2)` — the **textbook orthogonal quadratic contrast for 5 evenly-spaced points** (inherited verbatim from v1 r2 + HA-C3 v2 §4.5.1(b) companion). Verification (inline; matches v1 r2 lock-time verification per [`hypothesis-v1-archived.md`](../HA-C3/hypothesis-v1-archived.md) §4.5.1(b)): sum = 2 + (-1) + (-2) + (-1) + 2 = 0 ✓; dot product with the linear contrast `(-2, -1, 0, +1, +2)` = 2·(-2) + (-1)·(-1) + (-2)·0 + (-1)·1 + 2·2 = -4 + 1 + 0 - 1 + 4 = 0 ✓ (orthogonal). Direction: under SUPPORTED (concave-down / accelerating-decrement shape, where m2, m3, m4 lie above the linear chord from m1 to m5), the middle weights (-1, -2, -1) act on the elevated middle bin-means and the endpoint weights (+2, +2) act on the extremes, yielding `c · m < 0` — consistent with the §4.5.1(b) primary statistic's `S < 0` SUPPORTED direction.

**Note on quintile-bin spacing**: HA-C3p's bins are unequally spaced in stress-value (Q1 width 28, Q2-Q4 widths 3 each, Q5 width 63), so the "evenly-spaced" textbook assumption is approximate; the orthogonality verification above uses bin-index (1,2,3,4,5) not stress-value. The companion is **descriptive-only, NOT part of the §5 verdict bar**. Reported in result.md alongside the primary `S`.

**Condition (c) — Spline non-linearity test**: natural cubic spline regression of `gevoelscore = f(all_day_stress_avg)` with **4 internal knots placed at the §4.1 quintile bin boundaries (28, 31, 34, 37)**. Compare the full-spline model against the linear-only model via the F-statistic on the difference in residual sum of squares (degrees of freedom = number of non-linear basis terms = 3 for a natural cubic spline with 4 internal knots). **F-statistic significance is computed via block-permutation at E[L] = 7 per §4.7** (same machinery as condition (a) Jonckheere-Terpstra and condition (b) second-difference contrast — inherited verbatim from v1 r2 §4.5.1(c) post-§3.6 compression closure of audit L3.4 substantive): compute the F-statistic on the observed bin-label sequence, then on each of B = 10,000 null draws under the same §4.7 stationary-bootstrap label-resampling target, and report the empirical one-sided p-value. The parametric F-distribution p-value is reported alongside as descriptive only (anti-conservative on the autocorrelated `gevoelscore` residuals per [`permutation_null_block_length.md`](../../../methodology/permutation_null_block_length.md) discipline).

**Pass condition**: empirical block-permutation p < 0.05 AND **spline-second-derivative sign at ≥ 3 of 4 contributing midpoints from {Q2: x=29.5; Q3: x=32.5; Q4: x=35.5; Q5: x=68.5} must be NEGATIVE, with strict sign agreement (a positive-sign midpoint does NOT count toward the threshold)**. Q1's midpoint at x = 14 is **dropped from the count** because the natural-cubic boundary condition at x = 28 forces near-zero second derivative throughout the leftmost segment by construction (mirrors v1 r2's drop of B1's midpoint at x = 10 + HA-C3 v2 r1's drop of B1's midpoint at x = 15). Gating becomes ≥ 3 of 4 contributing midpoints, not ≥ 3 of 5 raw midpoints.

#### 4.5.2 Secondary descriptive outcomes (no verdict weight)

- **Bin-mean table** + 95% CI per quintile (stationary bootstrap at E[L] = 7 per [`permutation_null_block_length.md`](../../../methodology/permutation_null_block_length.md)) + per-bin n.
- **Pairwise Mann-Whitney across 4 adjacent quintile pairs** (Q1↔Q2, Q2↔Q3, Q3↔Q4, Q4↔Q5) with **Holm step-down correction**. 4 adjacent comparisons → Holm cutoffs α/4, α/3, α/2, α/1 at α = 0.05 (matches v1 r2 form for 5 bins).
- **Companion contrast** `c · m` value with `c = (+2, -1, -2, -1, +2)` per §4.5.1.
- **Linear correlation Spearman ρ** between `all_day_stress_avg` (continuous) and `gevoelscore` (continuous). Reported as a sanity-check companion ONLY (the C3 hypothesis itself rejects linearity; a positive-Spearman-but-failing-convexity result would mean "the relationship is roughly monotone-but-linear-or-concave" — against C3).

### 4.6 Crash-drop sensitivity arm (locked; per [CONVENTIONS §3.4](../../../CONVENTIONS.md#34-crash-drop-sensitivity-row-on-every-layer-4-correlation); inherited from HA-C3 v2 §4.6)

Re-run the three primary tests (Jonckheere-Terpstra, three-second-difference contrast, spline non-linearity) with `is_crash == True` dropped from the §5.A unmedicated pool. Report the second-difference statistic `S` both on the full pool and on the crash-dropped pool. **Flag if `|Δ S|` crosses the convex/concave sign boundary**. Per the §3.4 hook's purpose, the dependence is **informative-for-interpretation but does NOT modify the primary verdict** per §5: the C3 mechanism is expected to be strongest near crash days.

### 4.7 Block-permutation null at E[L] = 7 (locked; inherits from [`permutation_null_block_length.md`](../../../methodology/permutation_null_block_length.md); inherited from HA-C3 v2 §4.7 r2 amendment)

Same machinery as HA-C3 v2 §4.7 with the following form changes for HA-C3p's 5-bin scheme (recovering v1 r2 form):

1. Null draws operate on the **5-bin label sequence** (matches v1 r2; HA-C3 v2's 4-bin sequence is a different form).
2. Per null draw, recompute (a) Jonckheere-Terpstra `J*` on 5 bins; (b) mean second-difference `S = (Δ²_2 + Δ²_3 + Δ²_4) / 3` (mean of 3 second-differences for a 5-bin trajectory; recovers v1 r2 form); (c) spline F-statistic with 4 internal knots.
3. B = 10,000 null draws; seed `RANDOM_SEED = 20260624` (HA-C3p seed; distinct from HA-C3 v2's `20260623`, v1's `20260622`, HA-C4 v2's `20260618`, HA-C4 v1's `20260617`).
4. **E[L]\* companion factor-of-2 flag** retained from HA-C3 v1 r2 amendment + HA-C3 v2 §4.7 inheritance: report **two `E[L]*` values** — (i) on the **linear-residual series** (residuals from the linear `gevoelscore ~ all_day_stress_avg` fit); (ii) on the **bin-label categorical sequence** (the quintile-bin labels as the actual permutation target). Each fires the factor-of-2 flag if `|E[L]* − 7| / 7 > 0.5`. Per the methodology MD, the flags fire only on SUPPORTED verdicts; for PARTIAL or REJECTED, descriptive context only.

### 4.8 Sensitivity arms reported alongside the primary (no verdict weight)

- **§4.4 §5.B dose-adjusted cross-phase**: per §4.4 above; report bin-means + convexity test on the full Stratum 4 cross-phase pool with the dose-adjusted predictor `all_day_stress_avg_adj`, **REUSING the §4.1 quintile boundaries** (cross-arm cleanliness per Locked decision 1). Per-bin n on the cross-phase pool is reported at dry-run.
- **§4.8 z-scored-against-personal-rolling-baseline sensitivity** (per Locked decision 2; [CONVENTIONS §3.1](../../../CONVENTIONS.md#31-personal-baseline-not-absolute-thresholds) most-canonical alternative): compute `stress_z_28d_lagged(d) = (all_day_stress_avg(d) − μ_28d_lagged(d)) / σ_28d_lagged(d)` where `μ_28d_lagged` and `σ_28d_lagged` are the median + MAD (robust per [CONVENTIONS §3.1](../../../CONVENTIONS.md#31-personal-baseline-not-absolute-thresholds) prototype) on the **lagged** 28-day window `[d-28, d-1]` (excludes day d itself per the lagged-baseline discipline; pre-LC days excluded from the baseline). Re-bin into **quintiles of the `stress_z_28d_lagged` distribution** on the full Stratum 4 pool (computed at dry-run time on the same snapshot as the §4.1 raw quintiles; pre-committed to be quintile-anchored on the z-score distribution). Re-run the 3-condition test on the z-bin trajectory. **Reported as descriptive sensitivity ONLY**: a SUPPORTED-on-raw + SUPPORTED-on-z reading is "the convex shape is structural-within-subject regardless of whether bins are anchored to absolute or rolling-baseline-relative stress"; a SUPPORTED-on-raw + REJECTED-on-z reading is "the convex shape is anchored to the participant's all-time stress distribution, not their recent rolling baseline" — substantively interesting but does NOT modify the primary verdict.

  Rationale for raw-primary-not-z-primary: bin-edge stability across §5.A / §5.B / sub-arms requires a stationary edge spec (z-scored edges drift in raw stress-units across time as the rolling baseline moves); the raw quintiles are the cleanest expression of the personal-baseline-anchored bin scheme that holds stable across sub-arms.

- **§4.6 crash-drop arm**: per §4.6 above.
- **Train+validate M3 overlay**: bin-means + second-difference statistic computed separately for train (2022-09-03 → 2023-12-31) and validate (2024-01-01 → 2024-04-08) sub-windows of the unmedicated pool. Reported as descriptive side-by-side; no per-portion verdict per [`train_validate_split_fate.md §5`](../../../methodology/train_validate_split_fate.md).
- **§4.8 same-day vs t+1 lagged variant**: compute the same primary three conditions but with `gevoelscore[T+1]` as outcome (the same `all_day_stress_avg[T]` as predictor) under the §4.1 quintile bin scheme. Reported as descriptive cross-test alignment with PEM-pacing hypotheses; not promoted to primary.

### 4.9 Operationalisation choices (per pre-reg constraint #9; one sentence per dimension)

- **Window selection**: per-day single-cell (the claim is about the *same-day* mapping); justified by C3's claim shape that has no temporal-window dimension.
- **Signal reduction**: predictor `all_day_stress_avg` is binned into **5 equal-N quintile bins** per §4.1 (matches v1 r2 5-bin form; departs from HA-C3 v2 r1's 4-bin Wiggers-verbatim form); outcome `gevoelscore` stays continuous.
- **Threshold choice**: bin boundaries are at the **equal-N quintile values of the full-Stratum-4 distribution** per [CONVENTIONS §3.1](../../../CONVENTIONS.md#31-personal-baseline-not-absolute-thresholds), NOT at Wiggers-verbatim integer steps (HA-C3 v2 carries that operationalisation); the personal-baseline alignment is the load-bearing justification per the Wiggers-mechanism-not-numbers reading per §2(a).
- **Test family**: Jonckheere-Terpstra monotonicity (rank-based, distribution-free) + second-difference contrast (the discrete analogue of the second derivative; 5-bin form mean of 3) + natural cubic spline (continuous-domain confirmation companion; 4 internal knots and ≥ 3-of-4-contributing-midpoint sign gating). Robust + distribution-free + shape-aware.
- **Verdict shape**: 3-condition gated SUPPORTED with PARTIAL fallback (2-of-3); REJECTED otherwise. Not a binary p-bar.
- **Temporal structure**: per-day same-day mapping; no temporal collapse beyond per-day default per [`time_resolution.md §6`](../../../methodology/time_resolution.md#6-the-discipline-rule).
- **Multi-channel**: single-channel test.
- **Functional form**: explicit convexity test via the second-difference contrast and the spline non-linearity test; the test *does NOT assume linearity* — it tests *against* linearity as the null.
- **Effect-size grounding**: bin-mean deltas between adjacent quintile bins (in gevoelscore units 1-10) as the effect-size unit; the absolute deltas tell the human-interpretable size of the convex cost. Reference scale: the gevoelscore SD on the unmedicated pool (reported at dry-run for context).

## 5. Pre-registered falsification criterion (locked)

### 5.0 Multi-comparison discipline — single-cell headline lock

HA-C3p has **ONE headline verdict cell**: the §5.A unmedicated × 5-quintile-bin × `gevoelscore` × 3-condition gated outcome per §5.1 below. Every other arm — §5.B dose-adjusted cross-phase (§4.4 + §4.8), z-scored sensitivity (§4.8), crash-drop (§4.6), t+1 lagged (§4.8), train+validate M3 overlay (§4.8) — is **descriptive sensitivity ONLY** and CANNOT promote to SUPPORTED on its own. Per [`hypothesis_lock_process §4.2`](../../../methodology/hypothesis_lock_process.md#42-layer-3-substantive--multi-comparison-discipline) Option (a) single-cell headline lock.

### 5.1 Verdict bar — 3-condition gated (locked)

A condition is **MET** when its test statistic passes the §4.5.1 pass condition (one-sided empirical p < 0.05 AND correct direction; for condition (c) additionally the spline-second-derivative sign check at ≥ 3 of 4 contributing midpoints from {Q2: x=29.5; Q3: x=32.5; Q4: x=35.5; Q5: x=68.5} with strict sign agreement per §4.5.1(c) — Q1's midpoint at x = 14 is dropped because the natural-cubic boundary condition at x = 28 forces near-zero second derivative throughout the leftmost segment by construction).

A condition is **NOT MET** when either: (i) the test p-value fails the bar, OR (ii) the test statistic is in the wrong direction (e.g. monotone-increasing rather than decreasing for condition (a); convex-up `S > 0` for condition (b); positive spline second derivative at majority of midpoints for condition (c)).

| outcome | condition status | verdict |
|---|---|---|
| (a) MET AND (b) MET AND (c) MET | all 3 met | **SUPPORTED** |
| Exactly 2 of {(a), (b), (c)} MET | 2-of-3 | **PARTIAL** |
| 0 or 1 of {(a), (b), (c)} MET | ≤ 1-of-3 | **REJECTED** |
| Any of the 3 conditions is in the WRONG DIRECTION (regardless of p-value) | wrong-direction firing | **REJECTED** |

**Wrong-direction-overrides-2-of-3 clause**: if condition (a) shows monotone-INCREASING (gevoelscore RISES with stress quintile) the claim is structurally falsified regardless of whether (b) and (c) reach significance; reports REJECTED. Same logic for (b) `S > 0` (concave rather than convex) and (c) positive spline second derivative at majority of midpoints.

**Cross-test interpretation**: HA-C3p's §5 verdict stands on its own as a personal-range test of the Wiggers C3 convex-shape mechanism. The §1 4-cell agreement matrix with HA-C3 v2's verdict is interpreted ALONGSIDE HA-C3p's verdict per the result.md §6 open-questions framing (Locked decision 5). **HA-C3p does NOT claim HA-C3 v2's verdict pre-emptively**; the cross-test reading is a §6 framing for the open-questions discussion, not a §5 verdict claim.

### 5.2 Inconclusive bar

A condition that cannot be evaluated because of structural sample-size shortfall (e.g. a bin has < 30 observations after §4.3 on the §5.A unmedicated sub-arm) routes to **INCONCLUSIVE** for that condition. The 3-condition verdict is computed treating INCONCLUSIVE conditions as NOT MET for the SUPPORTED/PARTIAL/REJECTED count. **The dry-run sanity gate at §7.5 catches this case before the full run**: per the §4.1 draft-time forecast, all five unmedicated quintile bins have n ≥ 45 (well above the ≥ 30 bar), so an INCONCLUSIVE branch is not forecast.

## 6. Exclusion rules (locked)

Inherited from [HA-C3 v2 §6](../HA-C3/hypothesis.md#6-exclusion-rules-locked) verbatim. LC era only (`>= 2022-04-04`); unmedicated phase only for §5.A primary (`<= 2024-04-08`); April 2024 cluster excluded from all arms; first 21 days of `has_garmin_uds = True` coverage as a §6 sensitivity arm; pre-gevoelscore days (`< 2022-09-03`) excluded via the §4.3 NaN-drop; sentinel-filtered `all_day_stress_avg` dates excluded via §4.3 gate 4; days with NaN on either column excluded via §4.3 gates 4-5.

## 7. Expected effect size if hypothesis is true

### 7.1 Bin-mean trajectory under SUPPORTED

Under SUPPORTED, the bin-mean `gevoelscore` trajectory across quintile bins Q1 → Q5 should be:

- **Monotone decreasing**: `m1 > m2 > m3 > m4 > m5` (with monotonicity that need not be strict at each step but the Jonckheere-Terpstra trend must be significant per §5.1(a)).
- **Convex (accelerating decrement)**: the step from Q4 to Q5 (across the largest stress range — Q5 has width 63 vs Q4 width 3) is expected to carry the largest gevoelscore decrement; under SUPPORTED, the mean of three second-differences `S = (Δ²_2 + Δ²_3 + Δ²_4) / 3 < 0`.

**Sanity-check expected ranges** (not pre-specified bin values, just envelope expectations the dry-run reads against):

- `m1` (Q1 [0,28), unmedicated n = 45): expected in the **4-6 range** on the 1-10 gevoelscore scale (Q1 contains the participant's lower-stress days; under the v1 partial-pool descriptive read, the v1 B2 [20,30) had mean 3.958 — Q1 [0,28) overlaps but is slightly broader; envelope is set conservatively).
- `m5` (Q5 [37,100], unmedicated n = 189): expected in the **3-5 range** under SUPPORTED (lower than m1 by 1-3 gevoelscore units if convex).
- Absolute spread `m1 − m5`: in the **1-4 gevoelscore-unit range** (the convex-cost claim implies the spread exists; the convexity test answers *how* it accumulates across the 5 quintiles).
- Mean second-difference `S` (per §4.5.1(b)): expected in the range **`[-0.5, -0.05]`** if SUPPORTED (negative but small in magnitude because gevoelscore varies on a 1-10 integer scale and the per-bin stress range is narrow for Q2-Q4).

### 7.2 Sanity-check expected sample sizes (based on draft-time §4.1 snapshot)

The post-§4.3-gate full-Stratum-4 pool has n = 1351 at the draft-time snapshot (per §4.1). Expected per-bin n on the §5.A unmedicated sub-arm REUSING full-pool quintile boundaries (per §4.1 draft-time forecast):

- **Q1 [0,28) unmedicated**: ≈ 45. PASS the §7.5 gate 1 bar of ≥ 30 (borderline cell — n=45 is the smallest of the 5 bins).
- **Q2 [28,31) unmedicated**: ≈ 80. PASS.
- **Q3 [31,34) unmedicated**: ≈ 129. PASS.
- **Q4 [34,37) unmedicated**: ≈ 138. PASS.
- **Q5 [37,100] unmedicated**: ≈ 189. PASS.

**Right-shift caveat** (load-bearing per §4.1 observation surfaced at draft time): the unmedicated sub-arm is **right-shifted** relative to the full-Stratum-4 distribution (only ~18% of unmedicated days fall in the full-pool Q1 vs 20% by construction on the full pool). This is consistent with the +0.57/mg dose-modulation per [`citalopram_dose_response §5.6.1`](../../../methodology/citalopram_dose_response_stress_mean_sleep.md#561-per-channel-three-pronged-read): medication (consolidation + afbouw phases of Stratum 4) compresses the stress range; the unmedicated phase populates the higher quintiles disproportionately. **All five bins still PASS the ≥ 30 sanity-gate bar**; the unmedicated headline test is testable on the §4.1 quintile boundaries. No halt-option-A pre-commit is required (equal-N quintile-bin design eliminates the structurally-absent-or-underpowered category that drove v1 → v2 HA-C3 halt; HA-C3p has NO at-risk bin on the unmedicated sub-arm at draft-time forecast).

### 7.3 No halt-option-A pre-commit required

HA-C3p's equal-N quintile-bin design on the full-Stratum-4 distribution (n = 1351; ~250-300 per bin) makes structural underpower unlikely on the bin-computation pool, and the §5.A unmedicated sub-arm has per-bin n ≥ 45 (per §4.1 draft-time forecast). **No halt-option-A pre-commit is required** (unlike HA-C3 v2 r1 which pre-committed halt-option-A for B4 due to the v1 dry-run B5=1 underpower). Any post-dry-run revision of HA-C3p creates HA-C3p-v2 per [`hypothesis_lock_process §10.4 step 3`](../../../methodology/hypothesis_lock_process.md#104-five-stage-arc-iteration-policy).

### 7.4 Expected verdict-distribution shape

If the Wiggers C3 underlying convex-shape mechanism is **true on the participant's stress range**, expect: **SUPPORTED** (all three conditions met). If the relationship is **monotone but linear**, expect: PARTIAL (condition (a) MET, (b) and (c) NOT MET). If the relationship is **monotone but concave** (decelerating decrement — opposite of C3), expect: REJECTED via the wrong-direction clause on (b). If there is **no monotone relationship at all** (e.g. flat, U-shaped, or the inverted-U / threshold pattern the v1 partial-pool trajectory was descriptively informally consistent with at the §7.4 / §8 caveat-class level), expect: REJECTED via condition (a) failure.

**§7.4 prior-observation note** (per [CONVENTIONS §4.2](../../../CONVENTIONS.md#42-caveats-yes-a-priori-claims-no) caveat-class framing): v1's HALT-time partial-pool descriptive trajectory across the 3 populated v1 bins (v1 B2-B3-B4 = 3.958 → 4.265 → 3.860, peak at v1 B3 = stress 30-40) was descriptively **non-monotone**. **This v1 partial-pool observation is a caveat-class prior informing HA-C3p's verdict-interpretation, NOT a quasi-result and NOT a substantive output of HA-C3p**. HA-C3p's primary §5.1 verdict will formally evaluate whether this pattern is statistically robust on the personal-range quintile bins (which have higher resolution in the dense median region than v1's coarser scheme); the verdict bar treats the non-monotone-rejection branch via condition (a) failure rather than via an HA-C3p-specific inverted-U / threshold-pattern alternative claim. **HA-C3p does NOT pre-commit to an inverted-U / threshold-pattern alternative claim**; promoting the v1 trajectory observation to a substantive HA-C3p output would require a separate §3.2 fresh-session pre-reg, which is out of HA-C3p's scope.

### 7.5 Sanity gate (HALT triggers at dry-run)

- **Gate 1 — sample size**: each of Q1, Q2, Q3, Q4, Q5 on the §5.A unmedicated sub-arm has ≥ 30 observations (draft-time forecast: Q1=45, Q2=80, Q3=129, Q4=138, Q5=189; all PASS).
- **Gate 2 — distribution sanity**: `all_day_stress_avg` median on the unmedicated pool falls in a plausible range. **HALT if the median is outside [20, 60]** (draft-time observation: median = 34, well inside).
- **Gate 3 — gevoelscore overall distribution sanity**: `gevoelscore` median on the unmedicated pool falls in [3, 6] (v1 dry-run observed 4, inside).
- **Gate 4 — power-density**: across the 5 bins on the §5.A unmedicated sub-arm, all 5 bins have ≥ 30 observations AND the total n ≥ 100 (draft-time observation: total n = 581, well above).
- **Gate 5 — bin-edge snapshot consistency**: re-compute the §4.1 quintile boundaries on the test-time `per_day_master.csv` snapshot; **HALT if any boundary shifts by > 1 stress-unit from the locked draft-time edges (28, 31, 34, 37)**. Per Locked decision 4, the bin boundaries are pre-committed at draft time; a > 1 stress-unit shift would indicate the underlying full-Stratum-4 distribution has drifted between draft time and test time, requiring an HA-C3p-v2 redraft with the new snapshot.

If Gate 1, 2, 3, 4, or 5 fails at dry-run → HALT → revise spec → HA-C3p-v2 per [`hypothesis_lock_process §10.4 step 3`](../../../methodology/hypothesis_lock_process.md#104-five-stage-arc-iteration-policy).

## 8. Caveats `result.md` must explicitly acknowledge

1. **Power-calc dispatch** (per [`hypothesis_lock_process §3.8 gate 1`](../../../methodology/hypothesis_lock_process.md#38-lock-step-stage-5-of-the-arc)): power calculation is **inapplicable per Daza 2018 within-subject design** ([Daza 2018](../../../literature/methodology/daza_2018_self_tracked_n_of_1_counterfactual.pdf) *Methods Inf Med*). The block-permutation null at E[L] = 7 (§4.7) is the within-subject inferential machinery; the §5.1 3-condition gated verdict determines SUPPORTED/PARTIAL/REJECTED rather than asymptotic-power thresholds. INCONCLUSIVE per §5.2 is the operational definition of "underpowered for this cell". Equal-N quintile-bin design (per §4.1) eliminates structural-underpower from the bin-design dimension; the §5.A unmedicated sub-arm has all bins ≥ 45 (per §4.1 draft-time forecast).

2. **Sister-pre-reg framing** (NEW in HA-C3p; load-bearing per session handoff §1): HA-C3p tests the **underlying convex-shape claim Wiggers describes** on **personal-baseline-anchored bins** per [CONVENTIONS §3.1](../../../CONVENTIONS.md#31-personal-baseline-not-absolute-thresholds); HA-C3 v2 tests **Wiggers' verbatim 30→40 numerical anchor** on `[0,30), [30,40), [40,60), [60,100]` bins. The two pre-regs are **sister operationalisations of the Wiggers C3 substantive question**. Each pre-reg's §5 verdict stands on its own; the **4-cell agreement matrix interpretation** lives in HA-C3p's result.md §6 open-questions per Locked decision 5 (HA-C3 v2's result.md §6 will cross-link back to HA-C3p's framing). The sister-pre-reg framing does NOT modify either pre-reg's §5 verdict; it is the cross-test reading layered on top of each independent verdict.

3. **[CONVENTIONS §3.1](../../../CONVENTIONS.md#31-personal-baseline-not-absolute-thresholds) personal-baseline framing**: HA-C3p's quintile bins are **pool-anchored** (equal-N quintiles on the full Stratum 4 distribution; pool n = 1351 at draft time per §4.1 snapshot). This is the project-canonical personal-baseline operationalisation for cross-day-aggregate bins where the bin-edge stability across sub-arms requires a stationary edge spec. The **z-scored-against-personal-rolling-baseline** alternative is the §4.8(b) sensitivity arm (28-day lagged rolling median + MAD per [CONVENTIONS §3.1](../../../CONVENTIONS.md#31-personal-baseline-not-absolute-thresholds) prototype + HA01b-recomputed precedent); the raw quintiles are primary because the rolling-baseline z-score has edges that drift in raw stress-units over time, complicating cross-arm bin-edge cleanliness. A SUPPORTED-on-raw + REJECTED-on-z reading is "the convex shape is anchored to the participant's all-time stress distribution, not their recent rolling baseline" — substantively interesting but does NOT modify the primary verdict.

4. **Citalopram-channel inheritance** per [`citalopram_phase_stratification §4`](../../../methodology/citalopram_phase_stratification.md#4-per-channel-inheritance-rules): `all_day_stress_avg` is **CONFIRMED dose-modulated** at +0.57/mg per [`citalopram_dose_response §5.6.1`](../../../methodology/citalopram_dose_response_stress_mean_sleep.md#561-per-channel-three-pronged-read). HA-C3p's §4.4 inherits HA-C3 v2's §5.A unmedicated headline + §5.B dose-adjusted cross-phase sensitivity arm pattern (the §4 binding rule for CONFIRMED channels). The **unmedicated sub-arm is right-shifted** relative to the full-pool quintile boundaries (only ~18% of unmedicated days fall in Q1 vs 20% by construction on the full pool; per §4.1 draft-time observation); this is consistent with the dose-modulation evidence — medication compresses the stress range; the unmedicated phase populates higher quintiles disproportionately. **All five unmedicated bins still PASS the ≥ 30 sanity-gate bar**; the §5.A primary is testable on the §4.1 quintile boundaries.

5. **HA-C3 v1 partial-pool non-monotone observation as caveat-class prior** per [CONVENTIONS §4.2](../../../CONVENTIONS.md#42-caveats-yes-a-priori-claims-no): v1's HALT-time partial-pool descriptive trajectory across the 3 populated v1 bins (B2-B3-B4 = 3.958 → 4.265 → 3.860, peak at v1 B3 = stress 30-40) was descriptively **non-monotone**. **This is a caveat-class prior informing HA-C3p's interpretation, NOT a quasi-result and NOT promoted to a substantive HA-C3p output.** HA-C3p formally evaluates whether this pattern is statistically robust on the personal-range quintile bins; the verdict bar treats the non-monotone-rejection branch via condition (a) failure rather than via an HA-C3p-specific inverted-U / threshold-pattern alternative claim. **HA-C3p does NOT pre-commit to an inverted-U / threshold-pattern alternative claim** — that would require a separate §3.2 fresh-session pre-reg, which is out of HA-C3p's scope.

6. **n=1 single-subject** per [CONVENTIONS §3.1](../../../CONVENTIONS.md#31-personal-baseline-not-absolute-thresholds): thresholds in §5.1 (p < 0.05, second-difference sign, spline second-derivative sign at ≥ 3 of 4 contributing midpoints) are calibrated against the participant's distribution. The block-permutation null is the within-subject inferential anchor; the 3-condition verdict band is the within-subject decision rule. No cross-subject generalisation is claimed.

7. **Operational vs mechanistic** per [CONVENTIONS §4.1-§4.3](../../../CONVENTIONS.md#4-stay-close-to-the-data--defer-interpretation): the convex shape is the operationalised pattern; the "stress-cost asymmetry" mechanism Wiggers describes is the **substantive interpretation but not the operational measure**. A SUPPORTED verdict means the operationalised convex-shape pattern fires on the personal-range bins; it does NOT prove the substantive Wiggers stress-cost-asymmetry mechanism causally. Per [CONVENTIONS §4.1-§4.3](../../../CONVENTIONS.md#4-stay-close-to-the-data--defer-interpretation) the test is a *descriptive characterisation of the mapping shape*, not a causal mechanism claim.

8. **Crash-day inclusion structural fragility** (per [CONVENTIONS §3.4](../../../CONVENTIONS.md#34-crash-drop-sensitivity-row-on-every-layer-4-correlation)): the convex-cost shape is expected to be **strongest on crash days**; the §4.6 crash-drop sensitivity arm reports `S` on both the full pool and the crash-dropped pool. A sign-boundary flag firing is informative for interpretation; does NOT modify the §5 verdict.

9. **No causal-direction inference**: the test answers "does the gevoelscore-vs-stress-quintile mapping have a convex shape?" — it does NOT answer "does stress *cause* fatigue?" or "does fatigue *cause* stress?". Per [CONVENTIONS §4.1-§4.3](../../../CONVENTIONS.md#4-stay-close-to-the-data--defer-interpretation) the test is a *descriptive characterisation of the mapping shape*, not a causal mechanism claim.

10. **Bin-edge snapshot pinning** (NEW in HA-C3p per Locked decision 4): the §4.1 quintile boundaries are **pre-committed at draft time** to the snapshot `per_day_master.csv` SHA-256 `d0ff9253f7199a40165b6d229a4a68534b4a36b7de87bfbe8a18c23bb9ab189d` (computed 2026-06-23). The §7.5 Gate 5 sanity check verifies the boundaries have not shifted by > 1 stress-unit on the test-time snapshot; any shift > 1 stress-unit HALTs and requires HA-C3p-v2 with the new snapshot. This avoids the silent-boundary-drift failure mode that would otherwise make HA-C3p's cross-test agreement-matrix reading with HA-C3 v2 ambiguous.

11. **Independent-obligations block** (per [`citalopram_phase_stratification §6`](../../../methodology/citalopram_phase_stratification.md#6-pre-registration-template-for-new-hypothesis-mds) "Independent obligations" — adopting §5.A does NOT relieve the test of):
    - **Autocorrelation handling**: handled via §4.7 block-permutation at E[L] = 7 + two data-driven E[L]\* companion checks (linear-residual + bin-label categorical).
    - **Crash-drop sensitivity** per [CONVENTIONS §3.4](../../../CONVENTIONS.md#34-crash-drop-sensitivity-row-on-every-layer-4-correlation): handled via §4.6.
    - **Spike-detecting metrics where applicable** per [CONVENTIONS §3.5](../../../CONVENTIONS.md#35-spike-detecting-metrics-over-daily-averages): the C3 claim is structurally about the daily-aggregate stress channel (Wiggers' "annual stress overview score line"); the per-day-mean operationalisation IS the source-faithful read. **No spike-companion required.**
    - **Trajectory-detrend sensitivity** per [CONVENTIONS §3.7](../../../CONVENTIONS.md#37-trajectory-detrend-sensitivity-for-raw-pre-vs-post-comparisons): not applicable — this is not a pre-vs-post comparison.

12. **Drafting context disclosure**: this HA-C3p r1 was drafted in a fresh worktree-isolated session 2026-06-23 per the handoff brief. The drafter HAS seen (a) the v1 partial-pool descriptives per [`result-v1-archived.md`](../HA-C3/result-v1-archived.md); (b) the §4.1 quintile boundary values themselves at draft time (28, 31, 34, 37 per `np.quantile`); (c) the per-bin n on both the full Stratum 4 pool (248/253/294/251/305) and the §5.A unmedicated sub-arm (45/80/129/138/189). The drafter has NOT inspected the **per-bin gevoelscore means on the quintile-binned distribution** — the joint bin-mean trajectory is deferred to dry-run per [`hypothesis_lock_process.md` §3.9](../../../methodology/hypothesis_lock_process.md#39-run-step-post-lock). The data-exposure level is honestly disclosed in the Authorship block's "Data exposure context" — the §4.1 bin scheme is NOT a fresh-from-blind redraft (the drafter has the bin boundaries and per-bin n in working memory); but the §5 verdict criteria are mechanism-bound (Jonckheere + convexity + spline + sign agreement; same machinery as v1 r2 + HA-C3 v2) and the per-bin gevoelscore means are NOT in working memory. Per [`hypothesis_lock_process §3.2`](../../../methodology/hypothesis_lock_process.md#32-drafting-step-step-1-of-the-arc) drafting permitted; the §3.4 audit step is a separate fresh-session pass that should verify the data-exposure-conditional drafting did not import any HA-C3p-specific substantive claim.

13. **Wiggers' phrasing is qualitative** (load-bearing for the §1 sister-pre-reg framing): the verbatim source "a day with a score of 40 is much more tiring than a day with a score of 30" + "stair step" is qualitative. HA-C3 v2's `[0,30), [30,40), [40,60), [60,100]` bins are ONE operationalisation (Wiggers-verbatim numerical anchor); **HA-C3p's quintile bins on the personal-baseline distribution are a DIFFERENT operationalisation** (the underlying mechanism on the participant's own register). A REJECTED verdict on HA-C3p's specific bins does not falsify the qualitative Wiggers framing universally; it falsifies it on **this specific HA-C3p operationalisation** per [CONVENTIONS §4.2](../../../CONVENTIONS.md#42-caveats-yes-a-priori-claims-no).

14. **Sister-test cross-references** (informational; inherited from HA-C3 v2 §8 caveat 12): HA-C4 v2 REJECTED at daily-aggregate; HA11 SUPPORTED on train; HA-C3 v2 r1 in parallel sister-pre-reg execution. HA-C3p's primary cell (cross-day-aggregate shape on personal-baseline quintile bins) is structurally distinct from HA-C4 v2's within-day-shape claim and HA11's within-day U-dip count. **HA-C3 v2 is the parallel Wiggers-verbatim sister**; cross-test reading per §1 4-cell agreement matrix → result.md §6.

## 9. What we do with each outcome

### 9.1 SUPPORTED (3 of 3 conditions MET)

The underlying convex stress→fatigue shape claim is **empirically confirmed on this participant's stress distribution at the personal-baseline-anchored quintile bins**: same-day `all_day_stress_avg` maps onto `gevoelscore` with a monotone-decreasing AND convex shape across the §4.1 quintile bin scheme. **Downstream implications**:

- **High-stress days carry disproportionate cost on the participant's own register**: the convex shape exists on the personal-baseline-anchored bins, independent of whether Wiggers' specific numerical anchors fire. Analytical consequence: stress-budgeting models for pacing-behaviour analyses should treat the high-quintile register as carrying convex (not linear) cost on the participant's own scale.
- **Cross-test reading per §1 4-cell agreement matrix** (carried in result.md §6 open-questions per Locked decision 5):
  - **HA-C3 v2 SUPPORTED + HA-C3p SUPPORTED** → strong Wiggers C3; both the numerical anchor AND the underlying shape fire on this corpus. Cross-channel cluster: HA-C3 family (cross-day-aggregate shape) joins the cross-day complement of within-day sister channels (H02b stress-spike count, HA06b RHR z-score, HA11 U-dip count SUPPORTED-on-train).
  - **HA-C3 v2 REJECTED + HA-C3p SUPPORTED** → **substantively novel finding**: the convex shape exists on the participant's own register, but NOT at Wiggers' specific 30→40 anchor. Reading: Wiggers' specific numerical anchors don't fit this participant's distribution, but the underlying stair-step mechanism Wiggers describes is real on this participant's stress range. This is the centerpiece "we found the mechanism Wiggers describes besides the numbers she uses" finding per the user's framing in the session handoff §1.
- **No causal direction claim** per §8 caveat 9.

### 9.2 PARTIAL (2 of 3 conditions MET)

Three operationally distinguishable PARTIAL configurations: (a) + (b) MET / (c) NOT MET (bin-aggregate convex but continuous-domain non-linearity not detected); (a) + (c) MET / (b) NOT MET (non-linear but not cleanly convex via the bin-second-difference test); (b) + (c) MET / (a) NOT MET (structurally suspect — convexity test interpreting noise as convex shape; report descriptively but flag the configuration as inferentially-unstable). PARTIAL is descriptively informative but does NOT carry the SUPPORTED-bar weight for downstream pacing-behaviour analytic claims.

### 9.3 REJECTED (≤ 1 of 3 conditions MET; or any wrong-direction firing)

The underlying convex-shape claim is NOT empirically confirmed on the participant's distribution at the §4.1 quintile-bin operationalisation. Three distinguishable REJECTED configurations:

- **Wrong-direction (a) firing** (gevoelscore RISES with stress quintile): substantively surprising; investigate data-direction issue.
- **Wrong-direction (b) firing** (`S > 0` concave / decelerating decrement): substantively meaningful "law of diminishing returns" reading; informative against the Wiggers C3 underlying-mechanism claim and toward a different cost-shape model.
- **0 or 1 conditions MET, no wrong-direction firing**: the mapping is roughly linear-or-flat OR **non-monotone in the v1-partial-pool-trajectory direction** (per §8 caveat 5). Downstream interpretation under the non-monotone branch: the v1-trajectory prior is statistically robust at HA-C3p's primary §5.1 verdict bar; the underlying-mechanism C3 claim does not operationalise cleanly at HA-C3p's personal-baseline-anchored quintile-bin scheme; an inverted-U / threshold-pattern alternative shape claim is *informally suggested* but would require a separate §3.2 fresh-session redraft to HA-C3p-v2 to test as a primary.

**Cross-test reading per §1 4-cell agreement matrix** (carried in result.md §6):
- **HA-C3 v2 SUPPORTED + HA-C3p REJECTED** → suspicious bin-edge artefact in v2's Wiggers-verbatim 4-bin scheme (the under-fit by personal-range test). Reading: v2's verdict may be carried by an artefact of where v2's bin edges fall on the participant's distribution; the underlying shape on the personal-baseline-anchored bins does NOT fire.
- **HA-C3 v2 REJECTED + HA-C3p REJECTED** → **informative null on both operationalisations**: the Wiggers C-family at daily-aggregate is exhaustively-tested-and-not-supported on this corpus across both the Wiggers-verbatim and personal-baseline-anchored framings.

### 9.4 Sensitivity-arm divergences (descriptive interpretation, no verdict modification)

§5.B dose-adjusted cross-phase / §4.8 z-scored-against-personal-rolling-baseline / §4.6 crash-drop sign-boundary flag / §4.8 t+1 lagged variant / §4.8 train+validate M3 overlay divergences are descriptive only; none promote to SUPPORTED.

### 9.5 Dry-run halt (per §7.5)

- **Gate 1 (any of Q1-Q5 unmedicated n < 30) fails**: HALT + HA-C3p-v2 redraft required (NOT forecast at draft-time; minimum bin n=45).
- **Gate 2 (distribution sanity on `all_day_stress_avg`) fails**: HALT + investigate pipeline / sentinel-filter regression.
- **Gate 3 (distribution sanity on `gevoelscore`) fails**: HALT + investigate gevoelscore export pipeline.
- **Gate 4 (total n < 100) fails**: HALT + redraft with widened phase scope.
- **Gate 5 (bin-edge snapshot shift > 1 stress-unit) fails**: HALT + HA-C3p-v2 redraft with new snapshot.

## 10. Detection script architecture

### 10.1 Stage 1 — data (already done)

Both columns are in `$GEVOELSCORE_DATA_PATH/unified/per_day_master.csv`. No new extraction needed. Snapshot SHA-256 at draft time: `d0ff9253f7199a40165b6d229a4a68534b4a36b7de87bfbe8a18c23bb9ab189d`.

### 10.2 Stage 2 — test (`HA-C3p/test.py`, to be written post-lock in a separate session)

The script:

1. Loads `per_day_master.csv` + computes snapshot SHA-256; HALTs if shifted from the §4.1 locked snapshot SHA AND any boundary shifts by > 1 stress-unit (§7.5 Gate 5).
2. Applies §4.3 day-validity gate (LC era + April 2024 cluster exclusion + non-NaN both columns + first 21 device-baseline days exclusion; §5.A primary additionally requires `date <= 2024-04-08` unmedicated).
3. **Computes the full Stratum 4 pool quintile boundaries** for cross-validation against the §4.1 locked edges `[0, 28, 31, 34, 37, 100]` (Gate 5 verification).
4. Bins `all_day_stress_avg` per §4.1 (**5 left-inclusive bins** at edges `[0, 28, 31, 34, 37, 100]`).
5. Runs §7.5 sanity gates 1-5 at dry-run. HALT if any fails.
6. Computes the three primary conditions per §4.5.1 on the §5.A unmedicated sub-arm:
   - (a) Jonckheere-Terpstra one-sided trend test on 5 bins.
   - (b) Second-difference contrast `S = (Δ²_2 + Δ²_3 + Δ²_4) / 3` on 5 bins + one-sided block-permutation null at E[L] = 7 (B = 10,000).
   - (c) Natural-cubic-spline regression with **4 knots at (28, 31, 34, 37)**; F-test on non-linearity via §4.7 block-permutation; spline-second-derivative sign at the segment midpoints {29.5, 32.5, 35.5, 68.5} (Q1's x=14 dropped per §4.5.1(c)) with the ≥ 3-of-4 strict-sign-agreement gating.
7. Computes the §4.5.2 secondary descriptive outcomes (bin-mean + CI, pairwise Mann-Whitney + Holm on **4** adjacent quintile pairs, companion contrast `c = (+2, -1, -2, -1, +2)`, Spearman ρ).
8. Computes the §4.6 crash-drop sensitivity (re-run primary on `is_crash == True`-dropped pool; sign-boundary flag).
9. Computes the §4.8 sensitivity arms (§5.B dose-adjusted cross-phase REUSING §4.1 boundaries, z-scored-against-28d-lagged-baseline quintiles, train+validate M3 overlay, t+1 lagged variant — all on the §4.1 quintile bin scheme).
10. Computes the §4.7 data-driven E[L]\* + factor-of-2 flag (two derivations: linear-residual + bin-label categorical).
11. Applies the §5.1 3-condition verdict bar → SUPPORTED / PARTIAL / REJECTED.
12. Emits `result.md` + `result-data.json` per §10.3 template (cross-reference HA-C3 v2 in §6 open-questions).

**Seed**: `RANDOM_SEED = 20260624` (HA-C3p seed; distinct from HA-C3 v2's `20260623`, v1's `20260622`, HA-C4 v2's `20260618`, HA-C4 v1's `20260617`).

### 10.3 Stage 3 — `result.md` template

Reports the §5.1 verdict at top (one cell: the 3-condition outcome + SUPPORTED/PARTIAL/REJECTED band), followed by:

- The per-bin descriptive table (n, bin-mean, 95% CI, mean second-difference per the 5-bin form, spline non-linearity F-stat + p).
- Per-condition (a)/(b)/(c) outcomes (statistic value, empirical p, pass/fail).
- The §4.5.2 secondary descriptive outcomes (pairwise Mann-Whitney + Holm on 4 pairs; companion contrast `c · m`; linear Spearman ρ as opposing-model sanity check).
- The §4.6 crash-drop sensitivity table (full vs crash-dropped second-difference; sign-boundary flag status).
- The §4.4 secondary phase reads (consolidation replication; §5.B dose-adjusted cross-phase) — descriptive only, no verdict.
- The §4.8 sensitivity arms (z-scored-against-28d-lagged sensitivity per Locked decision 2; train+validate M3 overlay per-era; t+1 lagged variant; first-21-days-dropped per §6 device-baseline-warmup).
- The §4.7 data-driven E[L]\* + factor-of-2 flag status.
- Caveats per §8 (all 14).
- The §7.5 dry-run gate results table (which gates fired or passed).
- **§6 open-questions: 4-cell agreement-matrix cross-test reading with HA-C3 v2** (per Locked decision 5).

### 10.4 Run protocol

1. **Dry-run** (`python test.py --dry-run`): prints per-bin sample sizes + descriptive distribution + the §7.5 sanity gate evaluations including Gate 5 bin-edge snapshot consistency. **If any gate fails → HALT + HA-C3p-v2 redraft.**
2. **Full run** (`python test.py`): emits `result.md` + `result-data.json` directly into this folder.
3. **No iteration on the spec after the dry-run passes.** Any post-dry-run revision creates HA-C3p-v2 with the r1 spec archived.

### 10.5 Reproducibility

- `RANDOM_SEED = 20260624` locked at HA-C3p r1 draft time.
- B = 10,000 block-permutation resamples for all permutation p-values.
- Stationary bootstrap (geometric-distributed block lengths with mean E[L] = 7) for CI per [`permutation_null_block_length.md`](../../../methodology/permutation_null_block_length.md).
- Holm step-down at α = 0.05 for the pairwise Mann-Whitney secondary on 4 adjacent quintile pairs.
- **`per_day_master.csv` snapshot SHA-256 at draft time**: `d0ff9253f7199a40165b6d229a4a68534b4a36b7de87bfbe8a18c23bb9ab189d` (locked at §4.1 + §7.5 Gate 5).
- All inputs sourced from `per_day_master.csv`; no derived in-script columns beyond bin label assignment, the `_adj` dose-adjusted column for §5.B sensitivity, and the `stress_z_28d_lagged` column for §4.8(b) z-scored sensitivity.
- **Bin boundary derivation script**: `scripts/compute_HA-C3p_quintile_boundaries.py` (worktree-side; the canonical `test.py` will re-validate the boundaries at dry-run).

---

*Pre-registration drafted 2026-06-23 r1 by Claude (Opus 4.7, 1M context) in producer-mode under user authorisation per [CONVENTIONS §1.1](../../../CONVENTIONS.md#11-producer-mode-claude-edits-the-docs--codebase-the-default) per the session handoff brief `session-HA-C3p-pre-reg-drafting-handoff-2026-06-23.md`. Sister pre-reg to [HA-C3 v2 r1](../HA-C3/hypothesis.md) (Wiggers-verbatim arm; commit `724c814`). **Status: drafted, not locked.** Audit + lock are separate fresh sessions per the canonical arc.*
