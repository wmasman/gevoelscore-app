# HA-C3 v2 — Non-linear / convex stress→fatigue mapping (Tier 1 Wiggers), 4-bin redraft post-HALT

## Authorship

**Drafted 2026-06-23** by Claude (Opus 4.7, 1M context) in producer-mode under user authorisation per [CONVENTIONS §1.1](../../../CONVENTIONS.md#11-producer-mode-claude-edits-the-docs--codebase-the-default). Authorising user: Willem. **§3.2 fresh-session drafting per [`hypothesis_lock_process.md` §3.2](../../../methodology/hypothesis_lock_process.md#32-drafting-step-step-1-of-the-arc)** per the session handoff brief at `C:/Users/Gebruiker/.claude/plans/session-HA-C3-v2-redraft-handoff-2026-06-23.md`. Worktree-isolated session.

**v2 trigger**: v1 r2 was LOCKED 2026-06-23 (commit `de22b68`) and test-executed 2026-06-23 (commit `a9423af`) → **HALT on dry-run §7.5 Gate 1** because the locked 5-bin spec had **B1 [0,20) n = 0** (the participant's `all_day_stress_avg` distribution never reaches the low-stress register Wiggers' general claim assumes) and **B5 [60,100] n = 1**. The locked r2 §7.3 halt-option-A pre-commitment was scoped to sole-B5 underpower; the B1 zero-population failure mode was not absorbed by either halt-option-A or halt-option-B as documented. Per [`hypothesis_lock_process §10.4 step 3`](../../../methodology/hypothesis_lock_process.md#104-five-stage-arc-iteration-policy) ("any post-dry-run revision creates v2"), this v2 redraft is the required response. v1 r2 archived at [`hypothesis-v1-archived.md`](hypothesis-v1-archived.md); v1 r2 test at [`test-v1-archived.py`](test-v1-archived.py); v1 r2 HALT result at [`result-v1-archived.md`](result-v1-archived.md); v1 r2 dry-run report at [`dry-run-report-v1-archived.md`](dry-run-report-v1-archived.md).

**Data exposure context** (audit-able; the central reason this redraft must run with discipline): the drafter has now seen the v1 partial-pool descriptives — pool n = 581, stress median = 34, gevoelscore median = 4, and the populated-bins-only bin-mean trajectory B2[20,30) → B3[30,40) → B4[40,60) = 3.958 → 4.265 → 3.860 (non-monotone at the descriptive level, peak at B3 = stress 30-40). Per [CONVENTIONS §4.2](../../../CONVENTIONS.md#42-caveats-yes-a-priori-claims-no) caveat-class framing, this v1 partial-pool trajectory is logged as a prior informing v2's interpretation, **NOT promoted to a quasi-result or to a substantive output of v2**. v2 does not pre-commit to any inverted-U or threshold-pattern alternative claim; the substantive question (Wiggers' verbatim C3 convex claim) is unchanged. v2 is a spec revision for testability under the corpus's stress-distribution property, with the v1 trajectory observation entering only as a §8 caveat-class disclosure.

**Locked decisions at draft time** (load-bearing pre-commits; surfaced explicitly per the session handoff brief §2.3 + per [`hypothesis_lock_process §3.2 step 5`](../../../methodology/hypothesis_lock_process.md#32-drafting-step-step-1-of-the-arc)):

1. **v1 lineage and HALT cause** — HA-C3 v1 r2 LOCKED at commit `de22b68` 2026-06-23, test-executed at commit `a9423af` 2026-06-23, HALT on §7.5 Gate 1: B1 [0,20) n = 0 + B5 [60,100] n = 1. v1's §7.3 halt-option-A pre-commit addressed only sole-B5 underpower, not B1's zero-population case → v2 redraft required per [`hypothesis_lock_process §10.4 step 3`](../../../methodology/hypothesis_lock_process.md#104-five-stage-arc-iteration-policy).

2. **v2 bin scheme** — 4 bins `[0, 30), [30, 40), [40, 60), [60, 100]` (B1 collapse to address the corpus-property finding that `all_day_stress_avg < 20` never occurs on this pool; **the Wiggers verbatim 30→40 stair-step anchor is preserved at the new B2-B3 boundary**). Left-inclusive, right-exclusive intervals (except B4 `[60, 100]` closed-above). Boundary discipline: bin edges at the integer stress-unit values matching the Wiggers verbatim 30→40 anchor; not data-driven, not quintile-anchored.

3. **§7.3 halt-option-A pre-committed for B4** — at v2 lock, halt-option-A (widen B3 to absorb B4 if B4 n < 30 at dry-run) is pre-committed as the default. v1 r2's lock-time §7.3 pre-commit was scoped to sole-B5 underpower and missed B1; the v1 → v2 cycle made the lesson visible. v2 closes the rough edge by pre-committing the **only remaining at-risk bin (B4 from the v1 partial-pool re-projection, n ≈ 100 of unmedicated days)** to halt-option-A absorption rather than leaving it to a v2 → v3 round-trip. Halt-option-B (B4 INCONCLUSIVE + run on 3 bins) requires explicit user override before any v3 redraft. **This eliminates the "B-block-structurally-absent-or-underpowered" category in v2** because B1 has been collapsed away and B4 has a pre-committed absorber.

4. **Spline knot placement** — natural cubic spline regression with **3 internal knots at the new bin boundaries (30, 40, 60)** (down from v1's 4 knots at 20/30/40/60 because B1 is collapsed). Knot-at-bin-boundary placement is retained for consistency with the primary bin spec. **Visual gating via the sign of the spline's second derivative at the 3 bin midpoints** {midpoint of [0,30) = 15; midpoint of [30,40) = 35; midpoint of [40,60) = 50; midpoint of [60,100] = 80 — but the leftmost segment's [0,30) midpoint x = 15 sits inside the natural-cubic *boundary segment*, which differs from v1's situation where x = 10 was the leftmost-segment midpoint with a tight boundary-condition forcing}. Pass requires **≥ 2 of 3 midpoints from segments {[30,40), [40,60), [60,100]} showing NEGATIVE spline-second-derivative, with strict sign agreement (both met midpoints must be negative; no positive-sign midpoint contributes to the 2-of-3 count)**. The [0,30) midpoint x = 15 is **dropped from the count** for the same reason v1's r2 dropped its B1 midpoint at x = 10: the natural-cubic boundary condition forces near-zero second derivative throughout the leftmost segment by construction; x = 15 carries no convexity information. Gating becomes ≥ 2 of 3 segment midpoints, not ≥ 2 of 4.

5. **Convexity contrast** — primary convexity statistic is the **mean of two second-differences** `S = (Δ²_2 + Δ²_3) / 2` where `Δ²_i = m_{i+1} − 2·m_i + m_{i-1}` for i ∈ {2, 3} computed on the 4-bin trajectory `(m1, m2, m3, m4)`. Under SUPPORTED (gevoelscore convexly decreasing in stress-bin), `S < 0` systematically. One-sided block-permutation null at E[L] = 7 (§4.7); pass condition empirical p < 0.05 AND `S < 0`. Verification of the contrast form: the discretisation of the second derivative is `m_{i+1} − 2·m_i + m_{i-1}`; for a 4-bin trajectory the available second-differences are at interior bins i = 2 and i = 3 (i = 1 and i = 4 are endpoints with no `m_{i-1}` or `m_{i+1}` respectively). Mean of two is the textbook generalisation of v1's mean-of-three; structurally identical machinery, only the number of summands changes. (See §4.5.1 (b) for the inline orthogonality check on the companion vector.)

6. **Companion contrast (4-bin orthogonal quadratic)** — RETAINED for transparency, **NEW 4-bin orthogonal quadratic vector `c = (+1, -1, -1, +1)`** (the textbook orthogonal quadratic contrast for 4 evenly-spaced points). Verification (inline): sum = 1 + (-1) + (-1) + 1 = 0 ✓; dot product with the linear contrast `(-3, -1, +1, +3)` = 1·(-3) + (-1)·(-1) + (-1)·1 + 1·3 = -3 + 1 - 1 + 3 = 0 ✓ (orthogonal). Direction: under SUPPORTED (concave-down / accelerating-decrement shape, where m2 and m3 lie above the linear chord from m1 to m4), the middle weights (-1, -1) act on the elevated middle bin-means and the endpoint weights (+1, +1) act on the extremes, yielding `c · m < 0` — consistent with the §4.5.1 (b) primary statistic's `S < 0` SUPPORTED direction. Note: the v2 bins are unequally spaced ([0,30) width 30, [30,40) width 10, [40,60) width 20, [60,100] width 40), so the "evenly-spaced" textbook assumption is approximate; the orthogonality verification above uses bin-index (1,2,3,4) not stress-value. The companion is **descriptive-only, NOT part of the §5 verdict bar** — same role as v1's companion. Reported in result.md alongside the primary `S`.

7. **§5 3-condition gated verdict retained from v1** — (a) Jonckheere-Terpstra monotone-decreasing trend across the 4 bins + (b) convexity second-difference contrast `S < 0` per the new 2-second-difference form + (c) spline non-linearity at ≥ 2 of 3 segment midpoints with sign agreement per locked decision 4. Conjunctive 3-of-3 = SUPPORTED; 2-of-3 = PARTIAL; ≤ 1-of-3 OR any wrong-direction firing = REJECTED. Holm step-down on **3** adjacent-bin pairs (B1↔B2, B2↔B3, B3↔B4) for the §4.5.2 secondary pairwise Mann-Whitney (down from v1's 4 pairs because there are 4 bins, 3 adjacent comparisons). Holm cutoffs α/3, α/2, α/1 at α = 0.05.

8. **§4.4 citalopram approach inherited from v1** — **§5.A per-phase stratification as the PRIMARY**, with the **unmedicated phase as the headline pool** (2022-04-04 → 2024-04-08, ~735 days of which ~583 have gevoelscore — pool n = 581 per v1 partial-pool). **§5.B dose-adjusted predictor as a CROSS-PHASE SENSITIVITY ARM** per [`citalopram_phase_stratification §4`](../../../methodology/citalopram_phase_stratification.md#4-per-channel-inheritance-rules) CONFIRMED-channel inheritance (`all_day_stress_avg` β = +0.57/mg buildup-post-CPAP per [`citalopram_dose_response_stress_mean_sleep §5.6.1`](../../../methodology/citalopram_dose_response_stress_mean_sleep.md#561-per-channel-three-pronged-read) — load-bearing for the §4.4 approach choice). §5.C unmedicated-only restriction dispatched: §5.A primary already IS effectively unmedicated-only at the headline level.

### §3.8 gate-verification block (template at draft time per [`hypothesis_lock_process.md` §3.8](../../../methodology/hypothesis_lock_process.md#38-lock-step-stage-5-of-the-arc))

The four [§3.8 lock-blocking gates](../../../methodology/hypothesis_lock_process.md#38-lock-step-stage-5-of-the-arc) will be confirmed at lock-commit time. Pre-flight template:

1. **Power-calc dispatch** — to be confirmed MET via §8 caveat 1 (Daza 2018 within-subject design citation; block-permutation null at E[L] = 7 named as the within-subject inferential machinery; the §5.1 3-condition gated verdict determines SUPPORTED/PARTIAL/REJECTED; INCONCLUSIVE per §5.2 is the operational definition of "underpowered for this cell").
2. **Multi-comparison discipline** — to be confirmed MET via §5.0 single-cell headline lock (one headline cell: unmedicated × 4-bin × `gevoelscore` × 3-condition gated outcome); every other arm is descriptive sensitivity only and cannot promote to SUPPORTED. The conjunctive 3-of-3 SUPPORTED gate provides effective multiplicity control at the SUPPORTED bar; PARTIAL is a descriptive band per the v1 r2 audit's L3.3 framing.
3. **Register-row pointer** — to be confirmed MET at lock-commit time by updating [`wiggers_testable_hypotheses.md` Tier 1 C3 row](../../../wiggers_testable_hypotheses.md#tier-1--source-verified-verbatim--no-family-history-priority-pre-regs) to point at this v2 LOCKED spec (currently points at v1 r2 LOCKED at `de22b68`). **Register-row update happens at v2 LOCK time per `hypothesis_lock_process §3.8 gate 3`, NOT at this draft commit.**
4. **Re-audit clean OR §3.6 compression** — to be confirmed at lock time after the fresh-session `/research-review` audit. v1 → v2 transition is a §10.4 step 3 post-dry-run respec (the bin-collapse + cascading machinery adjustments + §7.3 B4 pre-commit + §8 caveat-class additions); the audit must verify the cascade is complete and that no new audit fires arise from the 4-bin re-derivation (notably condition (b) contrast-vector orthogonality + condition (c) spline-midpoint segment count + §4.6 / §4.7 / §4.8 mechanical updates from 5 bins → 4 bins).

| revision | date | summary |
|---|---|---|
| v1 r1 | 2026-06-22 | drafted at commit `ec99c2f`; fresh-session-isolated drafter; bin-spec/contrast/spline/seed/citalopram-approach all pre-committed before joint-distribution inspection. Archived at [`hypothesis-v1-archived.md`](hypothesis-v1-archived.md). |
| v1 r2 | 2026-06-23 | §3.6-compression absorb of audit fires per `8f3f269` report; LOCKED 2026-06-23 at commit `de22b68`. Test-executed at commit `a9423af` → HALT on §7.5 Gate 1 (B1 n = 0; B5 n = 1). |
| v2 r1 | 2026-06-23 | drafted at THIS COMMIT post-HALT per [`hypothesis_lock_process §10.4 step 3`](../../../methodology/hypothesis_lock_process.md#104-five-stage-arc-iteration-policy). v2 deltas from v1: 5 bins → 4 bins `[0,30), [30,40), [40,60), [60,100]` (B1 collapse to address corpus-property finding; Wiggers 30→40 anchor preserved at new B2-B3 boundary); convexity contrast `S = (Δ²_2 + Δ²_3) / 2`; spline 3 knots at (30, 40, 60); spline-second-derivative sign gating at ≥ 2 of 3 segment midpoints; Holm on 3 adjacent-bin pairs; **§7.3 halt-option-A pre-committed for B4** (widen B3 to absorb B4 if B4 n < 30 at dry-run; closes the v1 halt-mismatch rough edge by eliminating any remaining structurally-absent-or-underpowered category); **§8 caveat-class disclosure of v1 partial-pool non-monotone trajectory** (B2→B3→B4 = 3.958 → 4.265 → 3.860 from v1 result.md) as a prior informing v2 interpretation, NOT promoted to a v2 substantive output. **Status: drafted, not locked.** |

**Status**: drafted, not locked.

---

**Pre-registration drafted 2026-06-23 as v2 r1**, BEFORE any v2 test run and BEFORE any further inspection of the joint `all_day_stress_avg` × `gevoelscore` distribution beyond the v1 partial-pool descriptives surfaced in v1's result.md (the 3-populated-bins trajectory B2-B3-B4 = 3.958 → 4.265 → 3.860). Any change after lock creates HA-C3-v3 with v2 archived as v2.

HA-C3 v2 tests Wiggers' **"the stress→fatigue relationship is non-linear/convex — a 30→40 step costs more than it looks"** claim, source-verified verbatim per the register [C3 verification log](../../../wiggers_testable_hypotheses.md#c3--non-linear--convex-stressfatigue) batch 2 2026-06-12 (PDF lines 1357-1368, Annual Stress Scores section). v2 inherits v1's substantive question unchanged; v2 revises only the operationalisation (bin scheme and cascading machinery) to be testable on this corpus's stress-distribution property.

## 1. Claim

Within the LC frame and within the unmedicated phase (2022-04-04 → 2024-04-08), the **marginal effect of `all_day_stress_avg` on `gevoelscore` increases in magnitude as `all_day_stress_avg` rises**. The stress→fatigue function is **convex** (more precisely: monotone-decreasing with an accelerating decrement — gevoelscore drops by more per stress-unit at higher bins than at lower bins).

**Scope statement (v2-specific, per Locked decision 2 + handoff §3 surface-decision)**: this v2 tests the convex stress→fatigue claim on the `all_day_stress_avg` stress range **AS REPRESENTED IN THE CORPUS** (effectively `[20, 100]` per the v1 partial-pool finding that `all_day_stress_avg < 20` is structurally absent on this pool, with the upper open-top bin `[60, 100]` populated by only n = 1 day at v1 dry-run), **NOT the abstract Wiggers register range** which Wiggers' general claim assumes covers the full 0-100 stress register. The v1 corpus-property finding (B1 [0,20) structurally absent) is acknowledged as the §8 caveat 7 v2-scope clarification; the convex-cost claim CANNOT speak to the low-stress register Wiggers' general claim assumes because the participant's distribution does not populate it.

**Headline cell**: unmedicated phase × full Stratum 4 single pool × `all_day_stress_avg` binned at (0-30, 30-40, 40-60, 60+) × `gevoelscore` bin-mean × {Jonckheere-Terpstra monotone-decreasing test + convexity second-difference contrast `S = (Δ²_2 + Δ²_3)/2` + spline non-linearity test with 3 internal knots at bin boundaries + spline-second-derivative sign at ≥ 2 of 3 segment midpoints} × block-permutation null E[L] = 7 × 3-condition gated verdict per §5.

**Direction of effect under SUPPORTED**: (a) monotone-decreasing bin-means (high-stress bins have LOWER gevoelscore); (b) accelerating decrement (the bin-mean step from B2 [30,40) to B3 [40,60) is LARGER in magnitude than the step from B1 [0,30) to B2 [30,40); quantified as `S = (Δ²_2 + Δ²_3)/2 < 0`); (c) spline non-linearity term significant with shape visually consistent with convexity (≥ 2 of 3 segment midpoints showing negative spline second derivative).

**Verdict rule** (3-condition gated): see §5.

## 2. Why we think this

Inherited from [v1 §2](hypothesis-v1-archived.md#2-why-we-think-this) wholesale — the substantive question is unchanged. The three priors anchoring the test (Wiggers verbatim source PDF lines 1357-1368; lived-experience pacing-protocol prior; CONFIRMED dose-response on `all_day_stress_avg` at +0.57/mg per [`citalopram_dose_response_stress_mean_sleep §5.6`](../../../methodology/citalopram_dose_response_stress_mean_sleep.md#56-v3-amendment--multi-channel-confirmation-added-2026-06-14)) are unchanged from v1. Sister-test context (HA-C4 v2 REJECTED at daily-aggregate; HA11 SUPPORTED on train) is unchanged from v1.

**v2-specific note on Wiggers' "stair-step" framing**: the Wiggers verbatim "a day with a score of 40 is much more tiring than a day with a score of 30 — a step appears very small on the graph, but it isn't" is anchored at the 30 → 40 boundary, **preserved verbatim at v2's new B2-B3 boundary** (`[30, 40)` → `[40, 60)`). The B1 collapse from v1's `[0, 20)` + `[20, 30)` into v2's single `[0, 30)` does NOT touch the Wiggers verbatim anchor; the collapse responds to the corpus-property finding (`all_day_stress_avg < 20` structurally absent), not to a re-interpretation of the source claim.

## 3. Data sources

Inherited from [v1 §3](hypothesis-v1-archived.md#3-data-sources) verbatim. Predictor column `all_day_stress_avg`; outcome column `gevoelscore`; phase derivation `citalopram_phase(d)` per [`citalopram_phase_stratification §3`](../../../methodology/citalopram_phase_stratification.md#3-the-four-phase-citalopram-traject-stratification); PK-smoothed dose `dose_plasma_mg(d)` for §5.B sensitivity; `is_crash` from crash_v2 labels. All columns are already in `$GEVOELSCORE_DATA_PATH/unified/per_day_master.csv` per the [C3 column-mapping row](../../../wiggers_testable_hypotheses.md#c-stress-score) (status: ✅). **No new extraction required.**

## 4. Measurement protocol

### 4.1 Bin specification (v2; locked)

The predictor `all_day_stress_avg` is binned into **4** categories with **left-inclusive, right-exclusive intervals (except B4 [60,100] which is closed-above)**:

| bin id | label | range | rationale |
|---|---|---|---|
| B1 | low-mid | `[0, 30)` | collapsed-from-v1 low-stress range (v1's B1 + B2). Addresses the v1 corpus-property finding that `all_day_stress_avg < 20` is structurally absent on this pool. |
| B2 | mid | `[30, 40)` | the lower side of the verbatim Wiggers 30→40 anchor (preserved from v1's B3). |
| B3 | mid-high | `[40, 60)` | the upper side of the verbatim Wiggers 30→40 anchor extended to 60 (preserved from v1's B4); asymmetric width-of-20 absorbs the sparser upper-tail register. |
| B4 | high | `[60, 100]` | rare upper tail where the convex-cost prediction is sharpest (preserved from v1's B5). |

**Boundary discipline**: bin edges are at integer stress-unit values matching the Wiggers verbatim 30→40 step; not data-driven, not quintile-anchored. The verbatim alignment is the load-bearing justification (per [`hypothesis_lock_process §5`](../../../methodology/hypothesis_lock_process.md#5-sanity-check-questions-before-lock) trigger-phrase-binding rule: the natural-language anchor "30 → 40 step" is bound to the operational B2 → B3 step here).

**Pre-flight check** (§7.5 sanity gate 1 below): the descriptive distribution of `all_day_stress_avg` on the unmedicated pool is reported at dry-run; **HALT if any of B1, B2, B3 has < 30 observations**. **If B4 [60,100] has < 30 observations**, §7.3 halt-option-A pre-commit fires automatically: B3 is widened to absorb B4 (new B3 becomes `[40, 100]`) and the test runs on the 3-bin reduction `{[0,30), [30,40), [40,100]}` with the contrast reduced to a single second-difference `S = Δ²_2 = m_3 - 2·m_2 + m_1` (one second-difference because 3 bins have one interior point). This automatic absorption closes the v1 halt-mismatch rough edge: no human-in-the-loop decision is required for B4-only failure.

**Per-bin n re-projection from v1 partial-pool descriptives** (audit-able; the v1 dry-run-report rows for the populated bins translate directly into v2 bins because v1 B1 had n = 0 and the v1 → v2 bin boundaries on B2-B5 are preserved):

| v2 bin | v2 range | source v1 bins | projected n |
|---|---|---|---:|
| B1 | `[0, 30)` | v1 B1 [0,20) + v1 B2 [20,30) | 0 + 95 = **95** |
| B2 | `[30, 40)` | v1 B3 [30,40) | **385** |
| B3 | `[40, 60)` | v1 B4 [40,60) | **100** |
| B4 | `[60, 100]` | v1 B5 [60,100] | **1** |

**Per-projection §7.5 gate evaluation at v2 lock-time (forecast)**: B1 = 95 ≥ 30 PASS; B2 = 385 ≥ 30 PASS; B3 = 100 ≥ 30 PASS; **B4 = 1 < 30 → §7.3 halt-option-A pre-commit will fire automatically at dry-run**. The expected post-absorption configuration: B1 [0,30) n ≈ 95; B2 [30,40) n ≈ 385; B3' [40,100] n ≈ 101 (= 100 + 1). The 3-bin reduction is tested with a single-second-difference `S = m_3 - 2·m_2 + m_1`; the spline reduces to 2 internal knots at (30, 40); the visual-gating count reduces to ≥ 1 of 2 segment midpoints {35; 70} showing negative spline-second-derivative.

### 4.2 Stratum + pool (locked)

Inherited from [v1 §4.2](hypothesis-v1-archived.md#42-stratum--pool-locked) verbatim. **Primary pool**: full Stratum 4 single pool per [`train_validate_split_fate.md`](../../../methodology/train_validate_split_fate.md) — `date >= 2022-04-04` (LC era start) AND `date <= 2024-04-08` (unmedicated phase end). Train/validate split is NOT used as a primary verdict surface; see §4.8 below for the M3 descriptive overlay.

### 4.3 Day-validity gate (locked)

Inherited from [v1 §4.3](hypothesis-v1-archived.md#43-day-validity-gate-locked) verbatim (gates 1-5: LC era; unmedicated for primary, all phases for §5.B sensitivity; April 2024 cluster exclusion; non-NaN `all_day_stress_avg`; non-NaN `gevoelscore`). Expected post-gate pool size: **n = 581** per v1 dry-run.

### 4.4 Citalopram phase treatment (locked — §5.A primary; load-bearing; inherited from v1)

Inherited from [v1 §4.4](hypothesis-v1-archived.md#44-citalopram-phase-treatment-locked--5a-primary-per-the-locked-decisions-block-load-bearing) verbatim. **Primary approach**: §5.A per-phase stratification with the unmedicated phase as the headline pool. **Secondary descriptive sensitivity**: §5.A within-consolidation replication (with v1's §7.3 halt-option-A 4-bin reduction discipline applied recursively at the **3-bin reduction level** if any within-consolidation bin has n < 30 — i.e. if 3 of 4 consolidation bins have ≥ 30 but B4 has < 30, report the consolidation replication on the 3-bin reduction with B3 widened to absorb B4; if fewer than 3 bins have ≥ 30, suppress the consolidation secondary entirely); §5.B dose-adjusted-predictor cross-phase test per `all_day_stress_avg_adj(d) = all_day_stress_avg(d) − 0.57 · dose_plasma_mg(d)` per [`citalopram_phase_stratification §5.B`](../../../methodology/citalopram_phase_stratification.md#5b-dose-adjusted-predictor-recommended-for-cross-phase-tests). Per-phase sample minimums: ≥ 30 per bin to produce a descriptive bin-mean; below this, INCONCLUSIVE per §5.4 for that phase's read (does NOT halt the primary).

### 4.5 Statistical machinery (locked; v2-revised from v1 for 4-bin form)

#### 4.5.1 Primary tests — three conditions (all on the unmedicated pool)

For the unmedicated × 4-bin × `gevoelscore` bin-mean trajectory `(m1, m2, m3, m4)`:

**Condition (a) — Monotone decreasing**: **Jonckheere-Terpstra one-sided test** for monotone-decreasing trend across bins. H0: no trend across bins; H1: bins ordered B1 → B4 show monotone-decreasing `gevoelscore` distributions. Test statistic: standard Jonckheere-Terpstra `J*` standardised by the null SD; one-sided p-value via block-permutation at E[L] = 7 per §4.7 below. **Pass condition**: empirical one-sided p < 0.05 in the decreasing direction.

**Condition (b) — Convexity second-difference contrast** (v2-revised; the only structural change from v1): compute the **two** second-differences of bin-means `Δ²_i = m_{i+1} − 2·m_i + m_{i-1}` for i ∈ {2, 3}. The convexity statistic is the **mean** `S = (Δ²_2 + Δ²_3) / 2`. Under SUPPORTED (gevoelscore convexly decreasing in stress-bin), `S < 0` systematically. **One-sided block-permutation test at E[L] = 7**: H0: `E[S] = 0`; H1: `E[S] < 0`. Empirical p-value computed from the null distribution of `S` under block-permutation of the `(date, all_day_stress_avg)` label sequence (keeping `gevoelscore` fixed in place); B = 10,000 resamples. **Pass condition**: empirical one-sided p < 0.05 AND `S < 0` (correct direction).

**Companion contrast vector for transparency** (v2-revised — NEW 4-bin form per Locked decision 6): report `c · m` where `c = (+1, -1, -1, +1)` (the textbook orthogonal quadratic contrast for 4 evenly-spaced points). Verification: sum = 1 + (-1) + (-1) + 1 = 0 ✓; dot product with the linear contrast `(-3, -1, +1, +3)` = 1·(-3) + (-1)·(-1) + (-1)·1 + 1·3 = -3 + 1 - 1 + 3 = 0 ✓ (orthogonal). Direction: under SUPPORTED (concave-down / accelerating-decrement shape, where m2 and m3 lie above the linear chord from m1 to m4), the middle weights (-1, -1) act on the elevated middle bin-means and the endpoint weights (+1, +1) act on the extremes, yielding `c · m < 0` — consistent with the §4.5.1 (b) primary statistic's `S < 0` SUPPORTED direction. Not part of the §5 verdict bar; reported in result.md.

**Condition (c) — Spline non-linearity test** (v2-revised; 3 internal knots; ≥ 2 of 3 midpoints with sign agreement per Locked decision 4): natural cubic spline regression of `gevoelscore = f(all_day_stress_avg)` with **3 internal knots placed at the v2 bin boundaries (30, 40, 60)**. Compare the full-spline model against the linear-only model via the F-statistic on the difference in residual sum of squares (degrees of freedom = number of non-linear basis terms = 2 for a natural cubic spline with 3 internal knots). **F-statistic significance is computed via block-permutation at E[L] = 7 per §4.7** (same machinery as condition (a) Jonckheere-Terpstra and condition (b) second-difference contrast — the v1 r2 §3.6-compression closure of audit L3.4 substantive is preserved in v2): compute the F-statistic on the observed bin-label sequence, then on each of B = 10,000 null draws under the same §4.7 stationary-bootstrap label-resampling target, and report the empirical one-sided p-value. The parametric F-distribution p-value is reported alongside as descriptive only (anti-conservative on the autocorrelated `gevoelscore` residuals per [`permutation_null_block_length.md`](../../../methodology/permutation_null_block_length.md) discipline). **Pass condition**: empirical block-permutation p < 0.05 AND **spline-second-derivative sign at ≥ 2 of 3 segment midpoints from {[30,40), [40,60), [60,100]} must be NEGATIVE, with strict sign agreement (both contributing midpoints must agree on the negative sign; a positive-sign midpoint does NOT count toward the 2-of-3 threshold)**. The leftmost segment's [0,30) midpoint x = 15 is **dropped from the count** because the natural-cubic boundary condition at x = 30 forces near-zero second derivative throughout the leftmost segment by construction; sign at x = 15 carries no convexity information (analogous to v1 r2's drop of B1's midpoint at x = 10). Gating becomes ≥ 2 of 3 segment midpoints from {x = 35; x = 50; x = 80}, not ≥ 2 of 4 raw midpoints. Reported as a numerical check, not subjective visual approval.

#### 4.5.2 Secondary descriptive outcomes (no verdict weight)

- **Bin-mean table** + 95% CI per bin (stationary bootstrap at E[L] = 7 per [`permutation_null_block_length.md`](../../../methodology/permutation_null_block_length.md)) + per-bin n. The descriptive table is the read a human can interpret without inferential machinery; the §5 verdict is the formal closure.
- **Pairwise Mann-Whitney across adjacent bins** (B1↔B2, B2↔B3, B3↔B4) with Holm step-down correction. **3 adjacent comparisons → Holm cutoffs α/3, α/2, α/1 at α = 0.05** (v2-revised; was 4 cutoffs in v1).
- **Companion contrast** `c · m` value with `c = (+1, -1, -1, +1)` (v2-revised; new 4-bin orthogonal quadratic per Locked decision 6 + §4.5.1 (b) inline orthogonality check).
- **Linear correlation Spearman ρ** between `all_day_stress_avg` (continuous) and `gevoelscore` (continuous). **Reported as a sanity-check companion ONLY**: per the register, the C3 hypothesis *itself rejects linearity*; a positive-Spearman-but-failing-convexity result would mean "the relationship is roughly monotone-but-linear-or-concave" — i.e. against C3. The linear Spearman is the *opposing model* in disguise; reported for falsification-discipline.

### 4.6 Crash-drop sensitivity arm (locked; per [CONVENTIONS §3.4](../../../CONVENTIONS.md#34-crash-drop-sensitivity-for-correlations-and-regressions); inherited from v1)

Re-run the three primary tests (Jonckheere-Terpstra, two-second-difference contrast, spline non-linearity) with `is_crash == True` dropped from the unmedicated pool. Report the second-difference statistic `S` both on the full pool and on the crash-dropped pool. **Flag if `|Δ S|` crosses the convex/concave sign boundary**. Per the §3.4 hook's purpose, the dependence is **informative-for-interpretation but does NOT modify the primary verdict** per §5: the C3 mechanism is expected to be strongest near crash days.

### 4.7 Block-permutation null at E[L] = 7 (locked, inherits from [`permutation_null_block_length.md`](../../../methodology/permutation_null_block_length.md); inherited from v1 r2)

Inherited from [v1 §4.7](hypothesis-v1-archived.md#47-block-permutation-null-at-el--7-locked-inherits-from-permutation_null_block_lengthmd) verbatim, with the following 4-bin-form changes only:

1. The null draws now operate on the **4-bin label sequence** (down from 5-bin in v1).
2. Per null draw, recompute (a) Jonckheere-Terpstra `J*` on 4 bins and (b) mean second-difference `S = (Δ²_2 + Δ²_3) / 2` (mean of 2 second-differences; was mean of 3 in v1) and (c) spline F-statistic with 3 internal knots (was 4 in v1).
3. B = 10,000 null draws; seed `RANDOM_SEED = 20260623` (v2 seed; distinct from v1's `20260622`, HA-C4 v2's `20260618`, HA-C4 v1's `20260617`).
4. E[L]* companion factor-of-2 flag retained from v1 r2: report two `E[L]*` values — (i) on the linear-residual series and (ii) on the bin-label categorical sequence; each fires the factor-of-2 flag if `|E[L]* − 7| / 7 > 0.5`. Per the methodology MD, the flags fire only on SUPPORTED verdicts; for PARTIAL or REJECTED, descriptive context only.

### 4.8 Sensitivity arms reported alongside the primary (no verdict weight; v2-revised for 4-bin form)

- **§4.4 §5.B dose-adjusted cross-phase**: per §4.4 above; report bin-means + convexity test on the cross-phase pool with the dose-adjusted predictor `all_day_stress_avg_adj(d)`, applying the v2 4-bin scheme. If §7.3 halt-option-A fires on the cross-phase pool's B4, apply the same 3-bin reduction (B3 widened to absorb B4).
- **§4.4 within-consolidation replication**: per §4.4 above; report bin-means + convexity test within consolidation under the v2 4-bin scheme; recursive §7.3 halt-option-A 3-bin reduction discipline applied if any consolidation bin n < 30.
- **§4.6 crash-drop arm**: per §4.6 above.
- **Train+validate M3 overlay**: bin-means + second-difference statistic computed separately for train (2022-09-03 → 2023-12-31) and validate (2024-01-01 → 2024-04-08) sub-windows of the unmedicated pool. Reported as descriptive side-by-side; no per-portion verdict per [`train_validate_split_fate.md §5`](../../../methodology/train_validate_split_fate.md).
- **§4.8 same-day vs t+1 lagged variant**: compute the same primary three conditions but with `gevoelscore[T+1]` as outcome (the same `all_day_stress_avg[T]` as predictor) under the v2 4-bin scheme. Reported as descriptive cross-test alignment with PEM-pacing hypotheses; not promoted to primary.

### 4.9 Operationalisation choices (per pre-reg constraint #9; one sentence per dimension; v2-revised for 4-bin form)

- **Window selection**: per-day single-cell (the claim is about the *same-day* mapping); justified by C3's claim shape that has no temporal-window dimension.
- **Signal reduction**: predictor `all_day_stress_avg` is binned into **4** categories per §4.1 (down from 5 in v1; the "step appears very small on the graph, but it isn't" is *about* the step boundary, preserved at the new B2-B3 boundary); outcome `gevoelscore` stays continuous (the gevoelscore granularity 1-10 is already coarse).
- **Threshold choice**: bin boundaries are at the Wiggers-verbatim integer steps (0, 30, 40, 60), NOT data-driven quintiles or equal-width 20-unit bins; justified by the source-verified anchor.
- **Test family**: Jonckheere-Terpstra monotonicity (rank-based, distribution-free) + second-difference contrast (the discrete analogue of the second derivative; v2 form mean of 2) + natural cubic spline (continuous-domain confirmation companion; v2 with 3 internal knots and ≥ 2-of-3 segment-midpoint sign gating). Robust + distribution-free + shape-aware.
- **Verdict shape**: 3-condition gated SUPPORTED with PARTIAL fallback (2-of-3); REJECTED otherwise. Not a binary p-bar.
- **Temporal structure**: per-day same-day mapping; no temporal collapse beyond per-day default per [`time_resolution.md §6`](../../../methodology/time_resolution.md#6-the-discipline-rule).
- **Multi-channel**: single-channel test.
- **Functional form**: explicit convexity test via the second-difference contrast and the spline non-linearity test; the test *does NOT assume linearity* — it tests *against* linearity as the null.
- **Effect-size grounding**: bin-mean deltas between adjacent bins (in gevoelscore units 1-10) as the effect-size unit; the absolute deltas tell the human-interpretable size of the convex cost. Reference scale: the gevoelscore SD on the unmedicated pool (reported at dry-run for context).

## 5. Pre-registered falsification criterion (locked)

### 5.0 Multi-comparison discipline — single-cell headline lock

HA-C3 v2 has **ONE headline verdict cell**: the unmedicated × 4-bin × `gevoelscore` × 3-condition gated outcome per §5.1 below. Every other arm — secondary phases (§4.4), dose-adjusted cross-phase (§4.8), crash-drop sensitivity (§4.6), t+1 lagged (§4.8), train/validate M3 overlay (§4.8) — is **descriptive sensitivity ONLY** and CANNOT promote to SUPPORTED on its own. Per [`hypothesis_lock_process §4.2`](../../../methodology/hypothesis_lock_process.md#42-layer-3-substantive--multi-comparison-discipline) Option (a) single-cell headline lock.

### 5.1 Verdict bar — 3-condition gated (locked)

A condition is **MET** when its test statistic passes the §4.5.1 pass condition (one-sided empirical p < 0.05 AND correct direction; for condition (c) additionally the spline-second-derivative sign check at ≥ 2 of 3 segment midpoints from {[30,40) → x = 35; [40,60) → x = 50; [60,100] → x = 80} with strict sign agreement per §4.5.1 (c) — B1's midpoint at x = 15 is dropped because the natural-cubic boundary condition at x = 30 forces near-zero second derivative throughout the leftmost segment by construction).

A condition is **NOT MET** when either: (i) the test p-value fails the bar, OR (ii) the test statistic is in the wrong direction (e.g. monotone-increasing rather than decreasing for condition (a); convex-up `S > 0` for condition (b); positive spline second derivative at majority of midpoints for condition (c)).

| outcome | condition status | verdict |
|---|---|---|
| (a) MET AND (b) MET AND (c) MET | all 3 met | **SUPPORTED** |
| Exactly 2 of {(a), (b), (c)} MET | 2-of-3 | **PARTIAL** |
| 0 or 1 of {(a), (b), (c)} MET | ≤ 1-of-3 | **REJECTED** |
| Any of the 3 conditions is in the WRONG DIRECTION (regardless of p-value) | wrong-direction firing | **REJECTED** |

**Wrong-direction-overrides-2-of-3 clause**: if condition (a) shows monotone-INCREASING (gevoelscore RISES with stress bin) the claim is structurally falsified regardless of whether (b) and (c) reach significance; reports REJECTED. Same logic for (b) `S > 0` (concave rather than convex) and (c) positive spline second derivative at majority of midpoints.

### 5.2 Inconclusive bar

A condition that cannot be evaluated because of structural sample-size shortfall (e.g. a bin has < 30 observations after §4.3) routes to **INCONCLUSIVE** for that condition. The 3-condition verdict is computed treating INCONCLUSIVE conditions as NOT MET for the SUPPORTED/PARTIAL/REJECTED count. **The dry-run sanity gate at §7.5 catches this case before the full run**: if B1, B2, or B3 has < 30 observations, the test HALTS and a v3 redraft with revised bins is required (B4 < 30 absorbs into B3 via §7.3 halt-option-A pre-commit automatically — no halt, no redraft).

## 6. Exclusion rules (locked)

Inherited from [v1 §6](hypothesis-v1-archived.md#6-exclusion-rules-locked) verbatim. LC era only (`>= 2022-04-04`); unmedicated phase only for primary (`<= 2024-04-08`); April 2024 cluster excluded from all arms; first 21 days of `has_garmin_uds=True` coverage as a §6 sensitivity arm; pre-gevoelscore days (`< 2022-09-03`) excluded via the §4.3 NaN-drop; sentinel-filtered `all_day_stress_avg` dates excluded via §4.3 gate 4; days with NaN on either column excluded via §4.3 gates 4-5.

## 7. Expected effect size if hypothesis is true

### 7.1 Bin-mean trajectory under SUPPORTED (v2-revised)

Under SUPPORTED, the bin-mean `gevoelscore` trajectory across bins B1 → B4 should be:

- **Monotone decreasing**: `m1 > m2 > m3 > m4` (with monotonicity that need not be strict at each step but the Jonckheere-Terpstra trend must be significant per §5.1 (a)).
- **Convex (accelerating decrement)**: the step from B2 to B3 (across the Wiggers verbatim 30 → 40 boundary) is the load-bearing one; under SUPPORTED, `(m2 − m3)` is larger in magnitude than `(m1 − m2)`. The (B3 → B4) step (mid-high → high) is expected to be the largest of all if SUPPORTED.

**Sanity-check expected ranges** (not pre-specified bin values, just envelope expectations the dry-run reads against; v2-revised for the new B1 collapse):

- `m1` (low-mid stress, 0-30): in the 4-6 range on the 1-10 gevoelscore scale (the v1 partial-pool descriptive showed B2 [20,30) mean = 3.958; v2's B1 [0,30) inherits this because v1's B1 [0,20) was n = 0, so v2's B1 = v1's B2; envelope is set to span 4-6 to accommodate the unobserved [0,20) sub-bin if any low-stress days had appeared, with the realised B1 expected near 3.96).
- `m4` (high stress, 60+): in the 2-4 range (extrapolating from v1's single-day B5 reading of gevoelscore = 1, with the envelope widened because n = 1 is a single-day anchor).
- Absolute spread `m1 − m4`: in the 2-5 gevoelscore-unit range (the convex-cost claim implies the spread exists, the convexity test answers *how* it accumulates).
- Mean second-difference `S` (per §4.5.1 (b)): expected in the range `[-0.5, -0.05]` if SUPPORTED (negative, but small in magnitude because gevoelscore varies on a 1-10 integer scale).

### 7.2 Sanity-check expected sample sizes (v2-revised; based on v1 partial-pool descriptives)

The post-§4.3-gate unmedicated pool has been observed at n = 581 per v1 dry-run. Expected per-bin n on the v2 4-bin scheme (from the v1 partial-pool re-projection above):

- **B1 [0,30)**: ≈ 95 (= v1 B1 0 + v1 B2 95). PASS the §7.5 gate 1 bar of ≥ 30.
- **B2 [30,40)**: ≈ 385 (= v1 B3 385). PASS comfortably.
- **B3 [40,60)**: ≈ 100 (= v1 B4 100). PASS.
- **B4 [60,100]**: ≈ 1 (= v1 B5 1). **FAIL §7.5 gate 1 bar of ≥ 30** → §7.3 halt-option-A pre-commit fires automatically.

### 7.3 Sample-size sanity gates — v2 halt-option-A PRE-COMMITTED for B4

The per-bin n must be ≥ 30 on the unmedicated pool for B1, B2, B3 to produce a fully-resolved 3-condition test. **For B4 specifically, §7.3 halt-option-A is PRE-COMMITTED at v2 lock**:

- **Halt option A (PRE-COMMITTED DEFAULT at v2 lock for B4)**: if B4 [60,100] has n < 30 at dry-run, B3 [40,60) is widened to absorb B4 (new B3 becomes `[40, 100]`); the test runs on the 3-bin reduction `{B1 [0,30), B2 [30,40), B3' [40,100]}` with the contrast reduced to a single second-difference `S = m_3 − 2·m_2 + m_1` (3 bins have one interior bin); the spline reduces to 2 internal knots at (30, 40); the visual-gating count reduces to ≥ 1 of 2 segment midpoints from {[30,40) → x = 35; [40,100] → x = 70} showing negative spline-second-derivative. The cost is the loss of the high-stress-tail-most-extreme reading where the convex cost is sharpest — explicit trade-off documented and accepted at v2 lock time. **No human-in-the-loop decision required at dry-run; no v2 → v3 round-trip on B4-underpower.**

- **Halt option B (B4 INCONCLUSIVE; primary runs on the 4-bin scheme with B4 as INCONCLUSIVE per §5.2)**: requires explicit user override before any v3 redraft. **NOT preferred**: drops the load-bearing high-tail reading AND complicates the §5.1 verdict computation by introducing a partial-bin INCONCLUSIVE state into the 3-condition gate.

**For B1, B2, or B3 underpower** (which is NOT forecast per the v1 partial-pool re-projection — B1 = 95, B2 = 385, B3 = 100 — but is named here for completeness): if any of B1, B2, B3 has n < 30 at dry-run, **HALT + v3 redraft required** (this is the v1 → v2 lesson applied: any structural-absence-or-underpower OTHER than the pre-committed B4 absorber requires a fresh spec revision, not a halt-option absorption).

**v2 closes the v1 halt-mismatch rough edge**: v1's lock-time §7.3 pre-commit was scoped to sole-B5 underpower and missed B1's zero-population case; the v1 → v2 cycle made the lesson visible. v2 pre-commits halt-option-A on the only remaining at-risk bin (B4) AND has structurally eliminated the low-stress underpower path by collapsing B1. The "B-block-structurally-absent-or-underpowered category" is eliminated in v2 by construction.

### 7.4 Expected verdict-distribution shape (v2-revised)

If the Wiggers C3 verbatim is **true** on this corpus (within the v2 scope statement of `[20, 100]` AS-REPRESENTED, NOT the abstract `[0, 100]`), expect: **SUPPORTED** (all three conditions met) — most likely after the §7.3 halt-option-A absorption gives a 3-bin test on `{[0,30), [30,40), [40,100]}` with the load-bearing single second-difference. If the relationship is **monotone but linear**, expect: PARTIAL (condition (a) MET, (b) and (c) NOT MET). If the relationship is **monotone but concave** (decelerating decrement — opposite of C3), expect: REJECTED via the wrong-direction clause on (b). If there is **no monotone relationship at all** (e.g. flat, U-shaped, or the inverted-U / threshold pattern the v1 partial-pool trajectory was descriptively informally consistent with at the §7.4 caveat-class level), expect: REJECTED via condition (a) failure.

**§7.4 prior-observation note** (per Locked decision in handoff §3, surfaced as caveat-class per [CONVENTIONS §4.2](../../../CONVENTIONS.md#42-caveats-yes-a-priori-claims-no)): v1's HALT-time partial-pool descriptive trajectory across the 3 populated bins (v1 B2-B3-B4 = 3.958 → 4.265 → 3.860, peak at v1 B3 = stress 30-40) was descriptively non-monotone. This v1 partial-pool observation is a **caveat-class prior informing v2's verdict-interpretation, NOT a v2 substantive output**; v2's primary §5.1 verdict will formally evaluate whether this pattern is statistically robust, and the verdict bar treats the non-monotone-rejection branch via condition (a) failure rather than via a v2-specific inverted-U / threshold-pattern alternative claim. **v2 does NOT pre-commit to an inverted-U / threshold-pattern alternative claim**; promoting the v1 trajectory observation to a substantive v2 output would require a different pre-reg (a §3.2 fresh-session redraft to HA-C3-v3 with the alternative-shape claim as the primary), which is out of v2's scope.

### 7.5 Sanity gate (HALT triggers at dry-run; v2-revised)

- **Gate 1 — sample size**: each of B1, B2, B3 on the unmedicated pool has ≥ 30 observations. **B4 underpower is absorbed automatically via §7.3 halt-option-A pre-commit (no halt, no redraft)**. **HALT if any of B1, B2, B3 has < 30 observations**; v3 redraft required (B1, B2, B3 < 30 is not forecast per the v1 partial-pool re-projection but is the v1-lesson safety net).
- **Gate 2 — distribution sanity**: `all_day_stress_avg` median on the unmedicated pool falls in a plausible range. **HALT if the median is outside [20, 60]** (v1 dry-run observed 34, well inside).
- **Gate 3 — gevoelscore overall distribution sanity**: `gevoelscore` median on the unmedicated pool falls in [3, 6] (v1 dry-run observed 4, inside).
- **Gate 4 — power-density**: across the 4 bins (or 3 bins post-§7.3-absorption), at least 2 bins have ≥ 30 observations AND the total n ≥ 100 on the unmedicated pool. **HALT if total n < 100** (v1 dry-run observed n = 581, well above).

If Gate 1, 2, 3, or 4 fails at dry-run → HALT → revise spec → HA-C3-v3 per [`hypothesis_lock_process §10.4 step 3`](../../../methodology/hypothesis_lock_process.md#104-five-stage-arc-iteration-policy). **The dry-run report names the failing gate(s) explicitly and reports whether §7.3 halt-option-A absorption is sufficient (B4-only) or whether v3 redraft is required (B1/B2/B3 failure).**

## 8. Caveats `result.md` must explicitly acknowledge

1. **Power-calc dispatch** (per [`hypothesis_lock_process §3.8 gate 1`](../../../methodology/hypothesis_lock_process.md#38-lock-step-stage-5-of-the-arc)): power calculation is **inapplicable per Daza 2018 within-subject design** ([Daza 2018](../../../literature/methodology/daza_2018_self_tracked_n_of_1_counterfactual.pdf) *Methods Inf Med*). The block-permutation null at E[L] = 7 (§4.7) is the within-subject inferential machinery; the §5.1 3-condition gated verdict determines SUPPORTED/PARTIAL/REJECTED rather than asymptotic-power thresholds. INCONCLUSIVE per §5.2 is the operational definition of "underpowered for this cell".

2. **n=1 single-subject caveats** per [CONVENTIONS §3.1](../../../CONVENTIONS.md#31-personal-baseline-not-population-norm): thresholds in §5.1 (p < 0.05, second-difference sign, spline second-derivative sign at ≥ 2 of 3 segment midpoints) are calibrated against the participant's distribution. The block-permutation null is the within-subject inferential anchor; the 3-condition verdict band is the within-subject decision rule. No cross-subject generalisation is claimed.

3. **Citalopram-phase confound + chosen mitigation** per [`citalopram_phase_stratification §6`](../../../methodology/citalopram_phase_stratification.md#6-pre-registration-template-for-new-hypothesis-mds): the predictor `all_day_stress_avg` is dose-modulated at +0.57/mg per mg of plasma citalopram (v3 2026-06-14 confirmed). v2 inherits v1's §4.4 treatment §5.A primary + §5.B sensitivity arm per [`citalopram_phase_stratification §5`](../../../methodology/citalopram_phase_stratification.md#5-the-three-downstream-test-treatment-patterns); within-phase results (primary unmedicated + secondary consolidation if n ≥ 30 per bin) are the primary read; cross-phase aggregation without treatment is not.

4. **Crash-day inclusion structural fragility** (per [CONVENTIONS §3.4](../../../CONVENTIONS.md#34-crash-drop-sensitivity-for-correlations-and-regressions)): the convex-cost shape is expected to be **strongest on crash days**; the §4.6 crash-drop sensitivity arm reports `S` on both the full pool and the crash-dropped pool. A sign-boundary flag firing is informative for interpretation; does NOT modify the §5 verdict.

5. **Within-subject shape, NOT between-subject prediction**: the convex stress→fatigue claim is about the **within-subject mapping** on this participant's corpus. No claim is made about how the shape generalises across people.

6. **No causal-direction inference**: the test answers "does the gevoelscore-vs-stress-bin mapping have a convex shape?" — it does NOT answer "does stress *cause* fatigue?" or "does fatigue *cause* stress?". Per [CONVENTIONS §4.1-§4.3](../../../CONVENTIONS.md#4-statistical-discipline) the test is a *descriptive characterisation of the mapping shape*, not a causal mechanism claim.

7. **v2 scope is corpus-stress-range AS-REPRESENTED, NOT Wiggers' abstract register range** (NEW in v2 per the v1 HALT lineage). v1 r2 was test-executed 2026-06-23 and HALTed at §7.5 Gate 1 because B1 [0,20) had n = 0 on the unmedicated pool (the participant's `all_day_stress_avg` distribution never reaches the low-stress register Wiggers' general claim assumes covers the full 0-100 stress register). v2 responds to this corpus-property finding by collapsing v1's B1 [0,20) into v1's B2 [20,30) to form v2's new B1 [0,30). The v2 verdict scope is therefore **`[0, 100]` stress range AS REPRESENTED IN THE CORPUS** (effectively `[20, 100]` per the corpus-property finding), **NOT the abstract Wiggers register range** which Wiggers' general claim assumes covers the full 0-100. A SUPPORTED v2 verdict would mean: the convex shape is empirically confirmed on this participant's `all_day_stress_avg` distribution AS REPRESENTED, with the explicit caveat that the low-stress register (`< 20`) is structurally absent and therefore not tested. A REJECTED v2 verdict would mean: the convex shape is NOT empirically confirmed on the corpus-represented range, with the same caveat about the unobserved low-stress register; the Wiggers verbatim is not universally falsified at the qualitative level (it remains operationalisation-specific per caveat 8 below).

8. **Wiggers' phrasing is qualitative**: the verbatim source "a day with a score of 40 is much more tiring than a day with a score of 30" + "stair step" is qualitative. v2's binning (0-30, 30-40, 40-60, 60+) is one operationalisation of the stair-step framing; the verbatim does not specify these exact bins. A REJECTED verdict on these specific bins does not falsify the qualitative Wiggers framing universally; it falsifies it on **this specific v2 operationalisation** per [CONVENTIONS §4.2](../../../CONVENTIONS.md#42-caveats-yes-a-priori-claims-no).

9. **v1 partial-pool non-monotone trajectory as caveat-class prior informing v2 interpretation** (NEW in v2 per handoff §3 surface-decision + [CONVENTIONS §4.2](../../../CONVENTIONS.md#42-caveats-yes-a-priori-claims-no)). v1's HALT-time partial-pool descriptive trajectory across the 3 populated bins (v1 B2-B3-B4 = 3.958 → 4.265 → 3.860, peak at v1 B3 = stress 30-40) was descriptively **non-monotone** — informally consistent with EITHER §7.4's "no monotone relationship → REJECTED via condition (a) failure" OR an inverted-U / threshold-pattern alternative reading. **This v1 partial-pool observation is a caveat-class prior informing v2's verdict-interpretation, NOT a quasi-result of v2 and NOT a substantive output of v2.** v2's primary §5.1 verdict will formally evaluate whether this pattern is statistically robust; the verdict bar treats the non-monotone-rejection branch via condition (a) failure rather than via a v2-specific inverted-U / threshold-pattern alternative claim. **v2 does NOT promote the v1 trajectory observation to a SUPPORTED-of-inverted-U claim** — that would require a different pre-reg (a §3.2 fresh-session redraft to HA-C3-v3 with the alternative-shape claim as the primary), which is out of v2's scope.

10. **Independent-obligations block** (per [`citalopram_phase_stratification §6`](../../../methodology/citalopram_phase_stratification.md#6-pre-registration-template-for-new-hypothesis-mds) "Independent obligations" — adopting §5.A does NOT relieve the test of):
    - **Autocorrelation handling**: handled via §4.7 block-permutation at E[L] = 7 + data-driven E[L]\* companion.
    - **Crash-drop sensitivity** per [CONVENTIONS §3.4](../../../CONVENTIONS.md#34-crash-drop-sensitivity-for-correlations-and-regressions): handled via §4.6.
    - **Spike-detecting metrics where applicable** per [CONVENTIONS §3.5](../../../CONVENTIONS.md#35-spike-detecting-metrics-over-daily-averages): the C3 claim is structurally about the daily-aggregate stress channel (Wiggers' "annual stress overview score line"); the per-day-mean operationalisation IS the source-faithful read. **No spike-companion required.** Spike-companion testing belongs to HA-C4 / HA-C4b / HA11 which are within-day shape tests.
    - **Trajectory-detrend sensitivity** per [CONVENTIONS §3.7](../../../CONVENTIONS.md#37-trajectory-detrend-sensitivity-for-raw-pre-vs-post-comparisons): not applicable — this is not a pre-vs-post comparison.

11. **Drafting context disclosure** (NEW in v2): this v2 r1 was drafted in a fresh worktree-isolated session 2026-06-23 per the handoff brief. The drafter HAS seen the v1 partial-pool descriptives (pool n = 581, stress median 34, gevoelscore median 4, populated-bins trajectory 3.958 → 4.265 → 3.860 from v1 result.md / dry-run-report.md), and the §4.1 v2 bin spec was chosen with knowledge of this distribution. The data-exposure level is honestly disclosed in the Authorship block's "Data exposure context" — the v2 bin scheme is NOT a fresh-from-blind redraft, it is the minimum-viable v1-HALT response with the v1 partial-pool trajectory treated as a caveat-class prior per caveat 9. Per [`hypothesis_lock_process §3.2`](../../../methodology/hypothesis_lock_process.md#32-drafting-step-step-1-of-the-arc) drafting permitted; the §3.4 audit step is a separate fresh-session pass that should verify the v1 → v2 cascade is complete and that the data-exposure-conditional drafting did not import any v2-specific substantive claim.

12. **Sister-test cross-references** (informational; inherited from v1): HA-C4 v2 REJECTED at daily-aggregate; HA11 SUPPORTED on train; HA-C3 v2's primary cell (cross-day-aggregate shape) is structurally distinct from both. No prior import.

## 9. What we do with each outcome

### 9.1 SUPPORTED (3 of 3 conditions MET)

The Wiggers C3 verbatim claim is **empirically confirmed on this corpus** at the corpus-stress-range-AS-REPRESENTED scope per §8 caveat 7: same-day `all_day_stress_avg` maps onto `gevoelscore` with a monotone-decreasing AND convex shape across the v2 4-bin scheme (or the 3-bin reduction post-§7.3-absorption). **Downstream implications**:

- **High-stress days carry disproportionate cost**: a 30→40 stress step costs more gevoelscore than a 20-(now-collapsed-into-low-mid) → 30 step, in line with the Wiggers verbatim at the new B1-B2 boundary. Analytical consequence: stress-budgeting models for pacing-behaviour analyses should treat the high-stress register as carrying convex (not linear) cost; budget-allocation heuristics that linearly weight stress-units are mis-specified for this participant within the corpus-represented range.
- **Cross-test reading**: the convex shape would join the H02b stress-spike count + HA06b RHR z-score + HA11 U-dip count SUPPORTED-on-train cluster as the cross-day-aggregate complement of the within-day-shape sister channels.
- **Scope-limited confirmation per §8 caveat 7**: the confirmation extends only to the corpus-represented stress range; the low-stress register (`< 20`) is structurally absent on this pool and therefore not tested.
- **No causal direction claim** per §8 caveat 6.

### 9.2 PARTIAL (2 of 3 conditions MET)

Inherited from [v1 §9.2](hypothesis-v1-archived.md#92-partial-2-of-3-conditions-met) with the 4-bin form substituted. Three operationally distinguishable PARTIAL configurations: (a) + (b) MET / (c) NOT MET (bin-aggregate convex but continuous-domain non-linearity not detected); (a) + (c) MET / (b) NOT MET (non-linear but not cleanly convex via the bin-second-difference test); (b) + (c) MET / (a) NOT MET (structurally suspect — convexity test interpreting noise as convex shape; report descriptively but flag the configuration as inferentially-unstable; downstream interpretation likely needs a v3 redraft).

PARTIAL is descriptively informative but does NOT carry the SUPPORTED-bar weight for downstream pacing-behaviour analytic claims.

### 9.3 REJECTED (≤ 1 of 3 conditions MET; or any wrong-direction firing)

The C3 verbatim claim is NOT empirically confirmed on this corpus at the chosen v2 operationalisation within the §8 caveat 7 scope. Three distinguishable REJECTED configurations:

- **Wrong-direction (a) firing** (gevoelscore RISES with stress bin): substantively surprising; investigate data-direction issue.
- **Wrong-direction (b) firing** (`S > 0` concave / decelerating decrement): substantively meaningful "law of diminishing returns" reading; informative against the Wiggers C3 verbatim and toward a different cost-shape model.
- **0 or 1 conditions MET, no wrong-direction firing**: the mapping is roughly linear-or-flat OR **non-monotone in the v1-partial-pool-trajectory direction**. Downstream interpretation under the non-monotone branch: §8 caveat 9 v1-trajectory prior is statistically robust at v2's primary §5.1 verdict bar; the Wiggers C3 verbatim does not operationalise cleanly at the v2 daily-aggregate resolution on this corpus; an inverted-U / threshold-pattern alternative shape claim is *informally suggested* but would require a separate §3.2 fresh-session redraft to HA-C3-v3 to test as a primary.

REJECTED is informative against the Wiggers C3 verbatim at the v2 operationalisation. Cross-reference downstream: HA-C3 v2 REJECTED + HA-C4 v2 REJECTED would mean the Wiggers C-family at daily-aggregate is exhaustively-tested-and-not-supported on this corpus.

### 9.4 Sensitivity-arm divergences (descriptive interpretation, no verdict modification)

Inherited from [v1 §9.4](hypothesis-v1-archived.md#94-sensitivity-arm-divergences-descriptive-interpretation-no-verdict-modification) verbatim. §5.B dose-adjusted cross-phase / within-consolidation replication / §4.6 crash-drop sign-boundary flag / §4.8 t+1 lagged variant / §4.8 train+validate M3 overlay divergences are descriptive only; none promote to SUPPORTED.

### 9.5 Dry-run halt (per §7.5; v2-revised)

- **Gate 1 (B1, B2, or B3 n < 30) fails**: HALT + v3 redraft required (B4 < 30 is absorbed automatically via §7.3 halt-option-A pre-commit, no halt).
- **Gate 2 (distribution sanity on `all_day_stress_avg`) fails**: HALT + investigate pipeline / sentinel-filter regression.
- **Gate 3 (distribution sanity on `gevoelscore`) fails**: HALT + investigate gevoelscore export pipeline.
- **Gate 4 (total n < 100) fails**: HALT + redraft with widened phase scope.

## 10. Detection script architecture

### 10.1 Stage 1 — data (already done)

Both columns are in `$GEVOELSCORE_DATA_PATH/unified/per_day_master.csv`. No new extraction needed.

### 10.2 Stage 2 — test (`HA-C3/test.py`, to be written post-lock in a separate session; v2-revised)

The script:

1. Loads `per_day_master.csv`.
2. Applies §4.3 day-validity gate (LC era + unmedicated phase + April 2024 cluster exclusion + non-NaN both columns).
3. Bins `all_day_stress_avg` per §4.1 (**4 left-inclusive bins** at edges `[0, 30, 40, 60, 100]`).
4. Runs §7.5 sanity gates 1-4 at dry-run.
   - **If only B4 fails**: §7.3 halt-option-A pre-commit fires automatically; widen B3 to absorb B4 and proceed with the 3-bin reduction `{[0,30), [30,40), [40,100]}`. NO halt, NO v3 redraft.
   - **If B1, B2, or B3 fails (or any other gate)**: HALT + emit dry-run report naming the failing gate(s) + require v3 redraft.
5. Computes the three primary conditions per §4.5.1:
   - (a) Jonckheere-Terpstra one-sided trend test on 4 bins (or 3 if halt-option-A fired).
   - (b) Second-difference contrast `S = (Δ²_2 + Δ²_3) / 2` on 4 bins (or `S = m_3 − 2·m_2 + m_1` on 3 bins post-absorption) + one-sided block-permutation null at E[L] = 7 (B = 10,000).
   - (c) Natural-cubic-spline regression with **3** knots at (30, 40, 60) on 4 bins (or 2 knots at (30, 40) on 3 bins post-absorption); F-test on non-linearity via §4.7 block-permutation; spline-second-derivative sign at the segment midpoints {35, 50, 80} (or {35, 70} post-absorption) with the ≥ 2-of-3 (or ≥ 1-of-2) strict-sign-agreement gating per §4.5.1 (c).
6. Computes the §4.5.2 secondary descriptive outcomes (bin-mean + CI, pairwise Mann-Whitney + Holm on **3** adjacent pairs (or 2 post-absorption), companion contrast `c = (+1, -1, -1, +1)` (or 3-bin form post-absorption), Spearman ρ).
7. Computes the §4.6 crash-drop sensitivity (re-run primary on `is_crash == True`-dropped pool; sign-boundary flag).
8. Computes the §4.8 sensitivity arms (§5.B dose-adjusted cross-phase, within-consolidation replication if n ≥ 30 per bin per the recursive halt-option-A 3-bin reduction, train+validate M3 overlay, t+1 lagged variant — all on the v2 4-bin scheme with the same halt-option-A discipline applied recursively).
9. Computes the §4.7 data-driven E[L]\* + factor-of-2 flag (two derivations: linear-residual + bin-label categorical).
10. Applies the §5.1 3-condition verdict bar → SUPPORTED / PARTIAL / REJECTED.
11. Emits `result.md` + `result-data.json` per §10.3 template.

**Seed**: `RANDOM_SEED = 20260623` (HA-C3 v2; distinct from v1's `20260622`).

### 10.3 Stage 3 — `result.md` template

Reports the §5.1 verdict at top (one cell: the 3-condition outcome + SUPPORTED/PARTIAL/REJECTED band), followed by:

- The per-bin descriptive table (n, bin-mean, 95% CI, mean second-difference per the v2 form, spline non-linearity F-stat + p) — note whether the 4-bin or 3-bin (post-§7.3-absorption) scheme was used.
- Per-condition (a)/(b)/(c) outcomes (statistic value, empirical p, pass/fail).
- The §4.5.2 secondary descriptive outcomes (pairwise Mann-Whitney + Holm on 3 or 2 pairs; companion contrast `c · m`; linear Spearman ρ as opposing-model sanity check).
- The §4.6 crash-drop sensitivity table (full vs crash-dropped second-difference; sign-boundary flag status).
- The §4.4 secondary phase reads (consolidation replication on v2 4-bin scheme; §5.B dose-adjusted cross-phase) — descriptive only, no verdict.
- The §4.8 sensitivity arms (train+validate M3 overlay per-era; t+1 lagged variant; first-21-days-dropped per §6 device-baseline-warmup).
- The §4.7 data-driven E[L]\* + factor-of-2 flag status.
- Caveats per §8 (all 12; new in v2: caveats 7, 9, 11).
- The §7.5 dry-run gate results table (which gates fired or passed; whether §7.3 halt-option-A absorption fired on B4).

### 10.4 Run protocol

1. **Dry-run** (`python test.py --dry-run`): prints per-bin sample sizes + descriptive distribution + the §7.5 sanity gate evaluations. **If only B4 fails Gate 1 → automatic §7.3 halt-option-A absorption + proceed**. **If B1/B2/B3 fails any gate → HALT + v3 redraft.**
2. **Full run** (`python test.py`): emits `result.md` + `result-data.json` directly into this folder.
3. **No iteration on the spec after the dry-run passes.** Any post-dry-run revision creates HA-C3-v3 with the v2 spec archived.

### 10.5 Reproducibility

- `RANDOM_SEED = 20260623` locked at v2 draft time.
- B = 10,000 block-permutation resamples for all permutation p-values.
- Stationary bootstrap (geometric-distributed block lengths with mean E[L] = 7) for CI per [`permutation_null_block_length.md`](../../../methodology/permutation_null_block_length.md).
- Holm step-down at α = 0.05 for the pairwise Mann-Whitney secondary on 3 (or 2 post-absorption) adjacent-bin pairs.
- All inputs sourced from `per_day_master.csv`; no derived in-script columns beyond bin label assignment and the `_adj` dose-adjusted column for §5.B sensitivity.

---

*Pre-registration drafted 2026-06-23 v2 r1 by Claude (Opus 4.7, 1M context) in producer-mode under user authorisation per [CONVENTIONS §1.1](../../../CONVENTIONS.md#11-producer-mode-claude-edits-the-docs--codebase-the-default) per the session handoff brief `session-HA-C3-v2-redraft-handoff-2026-06-23.md`. v1 r2 archived at `hypothesis-v1-archived.md` (LOCKED 2026-06-23 `de22b68`; test-executed 2026-06-23 `a9423af`; HALT on dry-run §7.5 Gate 1). **Status: drafted, not locked.** Test execution is a separate post-lock session per the canonical arc.*
