# Methodology review -- Q24 MD-beta Wave 2E phase-standardised pre-window covariate operand (audit.md DRAFT r0 2026-07-16)

*Reviewer-mode fresh-session cold-context walk per [CONVENTIONS section 1.2](../CONVENTIONS.md#12-reviewer-mode-claude-audits-does-not-edit). Reviewer: Claude (Opus 4.7) in fresh-session subagent under user delegation 2026-07-16. Target: [`../analyses/descriptive/Q24-mdbeta-wave2e-phase-standardised-prewindow/audit.md`](../analyses/descriptive/Q24-mdbeta-wave2e-phase-standardised-prewindow/audit.md) (DRAFT r0). Companion script + outputs read from disk; no edits to target or any methodology MD or CONVENTIONS.*

**Checklist**: [4-layer review checklist](README.md#the-4-layer-review-checklist) (SCRIBE / STROBE / Daza / Natesan / WWC / CENT anchors) plus project-specific audit hooks from [CONVENTIONS section 3](../CONVENTIONS.md) + Wave 2E-specific concerns from user delegation brief.

---

## 1. What the data shows

**Empirical claims (audit's own words + verification against companion CSVs):**

1. Per-phase pre_window_load (30d sum of `effective_exertion_min` at `D_end` anchor) means across all n=314 gap=0 heavy-episode-ends on the LC-era stratum: `lc_pre_ergo` 285.1, `pacing_pre_citalopram_learning` 833.5, `pacing_habit_established` 581.8, `citalopram_modulated` 155.1 min over 30d (audit section 3.1). Confirmed against `output/phase_pre_window_load_baselines.csv`. Normalised to daily-mean units these match MD-alpha Wave 2A audit section 8 to 2 decimal places (9.50 / 27.78 / 19.39 / 5.17 min/day). Full agreement.

2. On 2024 PS-True (n=15, 3 crashes), the phase-standardised residual (`phase_std_pre_window_load = pre_window_load - phase_mean(P)`) separates crashes from non-crashes: crash mean +61.1 vs non-crash mean -75.5 min above phase baseline. All 3 crash-cases carry positive residuals (+24, +108, +51 min); 10 of 12 non-crash cases carry negative residuals (audit section 4.4 + section 7.2).

3. Headline 2x2 at phase_std > 0 cut: 3-of-5 above-phase-mean crash (60% [23.1, 88.2]); 0-of-10 below-phase-mean crash (0% [0.0, 27.8]). RD = +60 pp. RR undefined (zero unexposed crashes) (audit section 10.1). Confirmed against `output/phase_std_pre_window_operand_sensitivity.csv`.

4. By-end-class stratification within 2024 PS-True: heavy end_class (n=9) carries 0 crashes on either arm; very_heavy end_class (n=6) splits 3-above-all-crash + 3-below-all-non-crash = 1:1 within-stratum classifier at n=6 (audit section 9.1 + 9.2).

5. Phase-stratified per-phase p75 operand (`high_pre_window_p75`) at cut > phase p75 flags 3 of 15 PS-True episodes; 2 of 3 flagged crash. RR = 8.00; RD = +58.3 pp (audit section 5.3 + 8.1).

6. Cross-year all-years table (`output/phase_std_pre_window_ps_true_all_years.csv`, n=80 LC-era PS-True): all 3 above-phase-mean crashes are from 2024. 2022 (n=7, 1 crash) and 2023 (n=20, 1 crash) each carry a single crash on the below-phase-mean arm. 2025 (n=23) and 2026 (n=15) are crash-free (audit section 11.4).

7. 2023 asymmetric split: 18 above-phase-mean vs 2 below-phase-mean on n=20 PS-True; single crash on the 2-arm; direction opposite 2024 (audit section 11.1).

8. Cut-point sensitivity: RR undefined at cut A (>0), 8.00x at cut B (>0.5 sd), 3.25x at cut C (>1.0 sd). Direction robust across all three cuts; magnitude varies (audit section 12.2).

**Interpretive framing separated from empirical claims:**

- Audit calls the ~2x separation "SURVIVES phase-standardisation" (section 7.3 headline).
- Audit calls very_heavy 2024 PS-True 3+3 split a "1:1 within-stratum classification" (section 9.2 + 9.3).
- Audit calls the operand "behaves sensibly" in 2023 + 2025 (section 11 headline + 11.3).
- Audit assigns "READY for r2 codification" with 4 construct-validity constraints (section 15.2).
- Audit primary/sensitivity: phase-standardised = primary, phase-stratified = sensitivity, "either is defensible" fallback (section 13.3 + 13.4).

---

## 2. What fired and why

### Layer 1 -- Universal reporting (SCRIBE 2016 items 3-5, 14, 18, 22-24; STROBE 2007 items 6, 12, 13)

**L1.1 -- Operationalisation explicit + reproducible: FIRES-PASS (informational, no concern).**
Every operand is defined mathematically in section 2.4 with cross-refs to source CSVs. Companion `scripts/audit.py` implements exactly what the MD claims: `pre_window_load_at_end()` computes `sum(effective_exertion_min[d] for d in [D_end - 30, D_end - 1])` with `PRE_WINDOW_MIN_VALID = 15` gate; `attach_phase_operands()` builds `phase_std_pre_window_load = pre_window_load - phase_mean(P)` and `high_pre_window_p75 = pre_window_load > phase_p75(P)`; `emit_2x2()` computes Wilson CIs on both arms. **Absorb**: no revision needed; this passes cleanly.

**L1.2 -- Named counts (CONVENTIONS section 3.6): FIRES-PASS.**
Every cell count carries scheme + unit + source. Example section 4.1: "n=80 heavy-episode-ends with full crash-window in 2024. Of these, 15 are PS-True per Wave 2C section 5." Section 10.1: "2024 PS-True (n=15) stratified by phase_std_pre_window_load > 0 ... exposed n=5 (3 crashes) ... unexposed n=10 (0 crashes)." Source CSV named in section header. **Absorb**: no revision needed.

**L1.3 -- Framing not overclaiming -- headline reads "SURVIVES phase-standardisation" in section 7.3 + 4.4 headline: FIRES-CONCERN (moderate).**
Section 4.4 says: "Headline: the ~2x separation from Wave 2D section 9 SURVIVES phase-standardisation." Section 7.3 says: "YES. The direction of the separation ... is preserved." At n=3 crash-cases, "survives" is an interpretation of a 3-of-3 sign-consistency pattern, not a statistical survival test. The audit does declare narrative-only at section 7.4 + 10.3, so the framing is caveated locally, but the section 4.4 and 7.3 headline capitals "SURVIVES" and "YES" read stronger than a narrative-only 3-of-3 observation warrants for a Stage -1 descriptive audit. **Absorb-with-revision**: replace "SURVIVES" with softer verbiage in the section 4.4 + 7.3 headlines (e.g. "directional pattern is preserved"), OR add an inline narrative-only reminder immediately after each SURVIVES / YES.

**L1.4 -- Discipline scope (Stage -1 descriptive only, no verdicts): FIRES-PASS with one exception (see Wave-2E-specific below).**
Sections 4-12 report rates + Wilson CI + RR + RD; no p-values; no verdicts. Section 15.2's "READY for r2 codification" headline is the one exception -- flagged separately under Wave-2E-specific L4.6.

### Layer 2 -- Observational n=1 (Daza 2018; Personal Science norms)

**L2.1 -- Counterfactual framing: FIRES-PASS.**
The two operands are the counterfactual candidates for MD-beta r2 codification, and the audit computes both without pre-committing to either. Section 6 cross-comparison + section 13 primary vs sensitivity assignment do the counterfactual arithmetic explicitly. **Absorb**: no revision.

**L2.2 -- Stationarity assumption + phase-boundary respected: FIRES-PASS (load-bearing).**
This is the audit's central methodological claim: the citalopram phase-boundary at 2024-04-09 creates a 3.75x step-shift in pre-window absolute values (verified against Wave 2D section 10.3). Both operands are natively phase-adjusted (phase_std subtracts phase mean; phase_p75 uses per-phase quartile). Section 3.4 makes the semantic explicit: "A residual of +100 min/30d means 100 more minutes over the last 30 days than the average heavy-episode-end in this phase -- interpretation is identical across all 4 phases." **Absorb**: no revision; this is the audit's strongest methodological move.

**L2.3 -- Calendar-time vs subject-time separation: N/A for a covariate-definition audit.**

**L2.4 -- Data provenance traceability: FIRES-PASS.**
Every CSV cited by filename; audit script re-runnable against `$GEVOELSCORE_DATA_PATH/unified/per_day_master.csv`; RANDOM_SEED declared per MD-beta section 3.6. **Absorb**: no revision.

### Layer 3 -- Time-series specific (Natesan 2023; WWC 2022; CENT 2015)

**L3.1 -- Autocorrelation reporting: N/A.**
Wave 2E is a covariate-definition audit at Stage -1; no lagged-outcome inference is being drawn. Autocorrelation concerns apply at Stage H inferential machinery, not here.

**L3.2 -- Multiple testing across lags/channels: N/A.**
Only one anchor is tested (D_end); one lag window (30d); one intensity channel (`effective_exertion_min`). No multiplicity concern at this scope.

**L3.3 -- Named analysis frame: FIRES-PASS.**
LC-era stratum, gap=0 heavy episodes, K=3 rest-after primary, PS-True definition inherited from Wave 2C section 5. Frame is named in the framing paragraph.

### Layer 4 -- Project-specific audit hooks (CONVENTIONS section 3)

**L4.1 -- Personal baseline (CONVENTIONS section 3.1): FIRES-PASS.**
The entire operand construction is a personal-baseline transformation: subtract per-phase mean (or use per-phase p75). Section 3.4 makes this explicit. **Absorb**: no revision.

**L4.2 -- Definitional-pair discipline (CONVENTIONS section 3.3): FIRES-PASS.**
Two candidate operands computed side-by-side (section 2.4); primary vs sensitivity assignment in section 13. Meets the "one column per definitional pair" convention. **Absorb**: no revision.

**L4.3 -- Zero-vs-NaN (CONVENTIONS section 3.10): FIRES-PASS.**
Script uses `PRE_WINDOW_MIN_VALID = 15` gate; below-threshold pre-windows return NaN, not zero. Audit section 3 confirms all 314 episode-ends carry >=15 valid points (no data-availability drops). Producer-mode attestation in section 17 confirms `fillna(0)` is used only inside the validity-gated helper. **Absorb**: no revision.

**L4.4 -- Caveat vs a-priori (CONVENTIONS section 4.2): FIRES-CONCERN (moderate).**
The primary cut-point `phase_std > 0` is defensibly a-priori: mathematical zero is the operand's own zero (natural boundary between above / below phase baseline). Section 12.5 + 14.2 explicitly justify this as descriptively defined, not outcome-optimised. **However**, cut B and cut C are `0.5 * sd` and `1.0 * sd`, which are also "statistical convention" cut-points. The three-cut menu is presented as sensitivity analysis, but the specific choice of `>0`, `>0.5 sd`, `>1 sd` (rather than, say, phase p50 vs p75 vs p90; or a data-driven cut like phase median) has a whiff of post-hoc-friendly selection because `>0` happens to land 100% sensitivity on the 3 crash-cases at n=3 crash resolution. **Absorb**: the a-priori justification for `>0` is defensible; recommend adding an explicit note that cut B / cut C were pre-specified as statistical-convention sigma multiples not chosen from the observed distribution. See section 4.b below for the escalation on the primary-cut-100%-sensitivity concern.

**L4.5 -- Narrative-only discipline at n<5 (memory `feedback_narrative_only_events`): FIRES-PASS.**
Section 4.4 (crash-vs-non-crash split at n=3), section 8.3 (RR = 8.00 narrative-only), section 9.5 (all cells narrative-only), section 10.3 (RD +60 pp narrative-only), section 11.1 (single crash narrative-only) all carry narrative-only annotations. Consistent. **Absorb**: no revision.

**L4.6 -- Producer-mode Stage -1 scope boundary (CONVENTIONS section 1.1): FIRES-CONCERN (mild).**
Section 15.2 declares "READY for r2 codification" with 4 construct-validity constraints. Sections 13 + 14 recommend primary + sensitivity operand assignments and a specific cut-point. This is close to but not quite methodology-editing. The audit correctly frames these as "Wave 2E's recommendation for MD-beta r2" (section 13.3) and "cut-point recommendation for r2 codification" (section 14), phrased as inputs to a downstream r2 codification session, not as codification itself. The "READY" verb in section 15.2 headline is one step further along the readiness-declaration spectrum than a Stage -1 audit typically goes. **Absorb-with-revision**: soften section 15.2 headline from "READY for r2 codification" to "surface findings supporting r2 codification, subject to downstream review" or similar; the four construct-validity constraints are appropriate to surface but the readiness verdict itself should be the downstream session's call.

### Wave 2E-specific concerns (from user delegation brief)

**W2E.1 -- Section 10 headline framing at n=5 exposed / n=3 crashes: FIRES-CONCERN (substantive).**
The 3-of-5 crash on exposed + 0-of-10 crash on unexposed 2x2 has exposed arm n=5, which is right at the parent Stage -1 audit n_min5 threshold. RD = +60 pp with a Wilson CI on the arm rate (60%) of [23.1, 88.2] -- lower bound 23% is descriptively striking but does not exclude a moderate true rate. Section 10.3 flags "viable_n_min5: exposed arm has n=5 (right at the threshold)". Framing is defensible as descriptive-with-RD but the "clean separation" language in section 10.4 ("The zero-crash outcome on the below-phase-mean arm is the operand's headline strength") reads stronger than n=10 unexposed + 3 crash-events warrants. **Absorb-with-revision**: retain descriptive-only + narrative-only framing; strengthen the section 10.4 assessment to make clear the "zero-crash" observation is a 10-of-10 zero-outcome fact whose interpretability is bounded by the below-arm's Wilson upper of 27.8% (already reported but not integrated into the "headline strength" statement).

**W2E.2 -- Section 9 perfect within-stratum classification at n=6: FIRES-CONCERN (substantive, load-bearing for section 4 below).**
Very_heavy 2024 PS-True (n=6, 3 crashes) splits 3-above-all-crash + 3-below-all-non-crash. The audit calls this "1:1 within-stratum classification" (section 9.2 + 9.3). Section 9.5 adds: "Not a verdict: at n=3 crash-cases + n=3 non-crash within very_heavy 2024 PS-True, the 1:1 within-stratum classifier observation cannot be inferentially confirmed. It is a hard classification-consistency fact at the audit's data resolution." This caveat is appropriate. **However**: perfect classification on n=6 with 3 events is trivially achievable by chance under many null models (probability ~1/20 under exchangeability of the 3 crash labels across 6 slots is 1/(6 choose 3) = 1/20 = 5%). The audit does not compute this null and does not need to at Stage -1, but "perfect classifier" language in section 9.2 + 9.6 is stronger than the n=6 + 3-event resolution supports. **Absorb-with-revision**: retain the finding as a hard classification-consistency observation; soften "perfect classifier" phrasing to "cleanly co-classified" or "sign-consistent within-stratum" and add a footnote acknowledging the trivial-chance rate under a random-permutation null (5%). Do NOT delete the finding -- it is real at data resolution -- just make the framing appropriately narrow.

**W2E.3 -- Cross-year concentration: all 3 above-mean-arm crashes are from 2024: FIRES-CONCERN (substantive, load-bearing for r2 codification readiness).**
Section 11.4 all-years table shows 2024 is the only year with above-mean-arm crashes; 2022 + 2023 crashes are on the below-mean arm; 2025 + 2026 are crash-free. Section 11.5 says: "The operand is behaving as expected: it identifies episodes with above-phase-baseline pre-window load, and within 2024 this classifier separates the crash cases perfectly, while in the clean-flip years the classifier does not spuriously label crashes on the exposed arm." This framing partially addresses the concern but the more honest read is: **the operand's crash-classification signal is entirely a 2024-within-year signal; the operand is descriptively silent on crash discrimination in 2023 (single crash on wrong arm; n=2 arm not viable) and 2025-2026 (0 crashes)**. Section 15.3 open-concern-3 acknowledges this ("The operand is validated only on 2024 ... r2 should NOT extrapolate the effect size beyond 2024 without additional descriptive machinery"), but this framing does not appear in the section 11 headlines or in section 15.2 readiness declaration. **Escalate**: this concern is the load-bearing input to section 4.a below. The section 15.2 readiness declaration should carry a much more prominent caveat that the operand is 2024-specific in this corpus. See section 4.a recommendation.

**W2E.4 -- Section 11 2023 asymmetric arm split (18 vs 2): FIRES-CONCERN (moderate).**
2023 PS-True splits 18 above-phase-mean vs 2 below-phase-mean. The single crash is on the 2-arm. Section 11.1 flags n=2 not viable_n_min5 and single-event narrative-only. Section 11.5 headline: "phase-standardised operand does not fire spuriously in the clean-flip years." This framing overreads the 2023 evidence: the operand cannot fire spuriously on 2023 because 18-of-20 are above-phase-mean by construction -- the operand has almost no room to discriminate on 2023 PS-True. A more honest read: the 2023 evidence is descriptively silent on operand discrimination because the arm split is 18/2 with the single crash sitting on the 2-arm; the operand's classifier is essentially untestable at 2023 PS-True resolution. **Absorb-with-revision**: retain the observation; soften section 11.5 "operand does not fire spuriously" to "operand cannot be tested for spurious firing at 2023 PS-True resolution given the 18/2 arm asymmetry"; make explicit that this is silence, not clean-flip validation.

**W2E.5 -- Section 10 RR undefined framing (RD-only vs Haldane-Anscombe correction): FIRES-PASS with note.**
RR is undefined because unexposed arm has 0 crashes. Section 10.1 reports "RR (True/False) = undefined (division by zero on unexposed arm)". Descriptively this is the honest read at n=5 exposed + n=10 unexposed + 0 unexposed crashes. Haldane-Anscombe correction (add 0.5 to zero cells) would produce a finite RR of ~7 (0.6 / (0.5/10.5)) but this is an inference-level convention, not a descriptive one. Per CONVENTIONS section 2.1 (descriptive-before-inference), RD-only is more honest at this sample size. **Absorb**: no revision; the audit's descriptive-only RD framing is appropriately conservative for a Stage -1 audit. See section 4.b for the load-bearing recommendation on descriptive-narrative vs Haldane-Anscombe framing.

**W2E.6 -- Section 12 cut-point sensitivity data-driven concern: FIRES-PASS with note (see L4.4 above).**
Cut A (>0), cut B (>0.5 sd), cut C (>1 sd) are defensible as a-priori choices: `>0` is the operand's mathematical zero; `>0.5 sd` and `>1 sd` are standard-sigma-multiple statistical conventions. The audit does not, however, explicitly attest that these cuts were pre-specified before looking at the crash distribution. Given that `>0` happens to land 100% sensitivity on the 3 2024 crash-cases, an explicit "pre-specified as statistical convention, not chosen from observed crash distribution" attestation would strengthen the audit's discipline claim. **Absorb-with-revision**: add explicit pre-specification attestation to section 12.5.

**W2E.7 -- Section 13 primary vs sensitivity assignment: FIRES-PASS.**
Section 13 lays out the construct-validity trade-off symmetrically, recommends phase-standardised as primary + phase-stratified as sensitivity with detailed rationale, then explicitly notes the reverse assignment is also defensible (section 13.4). This is appropriate producer-mode framing: surface the trade-off, recommend a default, leave room for the downstream codification session to adjust. **Absorb**: no revision.

**W2E.8 -- Section 14 cut-point `phase_std > 0` justification: FIRES-PASS with note.**
The "mathematical zero, not outcome-optimised" justification is defensible in principle: the phase mean is a natural baseline, and `>0` is its natural boundary. **However**: the specific alignment of `>0` with 100% sensitivity on the 3 2024 crash-cases is a happy coincidence that the audit does not explicitly flag as such. A stronger discipline framing: acknowledge that the mathematical-zero cut-point happens to yield 100% sensitivity, and note that any post-hoc examination of the crash distribution to verify the cut-point's clean-separation property would violate the a-priori-claim discipline. The audit's current framing is defensible but the coincidence should be explicit rather than tacit. **Absorb-with-revision**: add a note to section 14.2 acknowledging that the 100%-sensitivity property is an empirical observation on 2024 PS-True and should not be used as justification for the cut-point choice.

**W2E.9 -- Section 15 READY-for-r2 framing: FIRES-CONCERN (see L4.6 above).**
Duplicate of L4.6. **Absorb-with-revision**: soften "READY for r2 codification" verdict in section 15.2 headline.

**W2E.10 -- Cross-year construct-validity: operand silent outside 2024: FIRES-CONCERN (substantive, see W2E.3 above).**
Section 11 spot-check headline claims the operand "behaves sensibly in the neighbouring years -- no elevated crash risk on the exposed arm in either 2023 or 2025". This is technically true (no false-firing) but reads as validation of construct-validity. A more honest framing: the operand cannot fire meaningfully outside 2024 because 2023 lacks arm balance and 2025-2026 lack crash outcomes. The operand's construct-validity claim -- "identifies episodes with above-phase-baseline pre-window load" -- is defensible on the mechanical side but the "operand discriminates crashes" claim is 2024-specific. Section 15.3 open-concern-3 acknowledges this; section 11 and section 15.2 headlines do not. **Absorb-with-revision**: strengthen section 11.5 and section 15.2 caveating.

**W2E.11 -- MD-alpha Wave 2A audit section 8 verification: FIRES-PASS.**
Cross-verified: audit section 3.2 claim (9.50 / 27.78 / 19.39 / 5.17 min/day) matches MD-alpha Wave 2A audit section 8 empirical table (`docs/research/analyses/descriptive/Q24-mdalpha-precursor-phase-intensity/audit.md` lines 310-313) exactly. Cross-audit arithmetic consistency confirmed. **Absorb**: no revision.

---

## 3. What does not fire (selective)

- **L2.2 phase-boundary respect** -- the audit's central methodological move (both operands natively phase-adjusted; no absolute cut across the 2024-04-09 boundary) directly addresses Wave 2D section 10.3's phase-confound constraint. This is the strongest part of the audit; passes cleanly with non-trivial evidence.

- **L4.3 zero-vs-NaN discipline** -- companion script uses `PRE_WINDOW_MIN_VALID = 15` gate + `fillna(0)` only inside the validity-gated helper. Producer-mode attestation section 17 confirms. Passes cleanly.

- **L4.2 definitional-pair discipline** -- two operand candidates computed side-by-side, primary + sensitivity assignment made with explicit trade-off rationale (section 13). Passes cleanly.

- **W2E.11 cross-audit arithmetic verification** -- 4 phase daily-means match MD-alpha Wave 2A audit section 8 to 2 decimals. Non-trivial cross-audit consistency check passes cleanly.

- **Descriptive-with-Wilson-CI discipline** -- every 2x2 in sections 4-12 carries Wilson CIs on both arms, RR with per-arm cell counts, RD, and viable_n_min5 flag. No p-values, no verdicts (with the caveats above on "SURVIVES" and "READY" verbiage). Passes cleanly.

- **Producer-mode discipline attestations (section 17)** -- named counts + NaN discipline + definitional-pair + descriptive-with-CI + small-n narrative-only + physical-rest-only semantic + phase-boundary respect + idempotent script + non-outcome-optimised cut-point all attested explicitly. Passes cleanly (the "not outcome-optimised" attestation is technically defensible; see W2E.8 note on the tacit 100%-sensitivity coincidence).

---

## 4. What would strengthen this finding

### 4.a Load-bearing: r2-ready or needs-more-validation? -- **NEEDS-MORE-VALIDATION, with staged path**

The audit's "READY for r2 codification" verdict (section 15.2) should be **downgraded to "operand-definition-ready, cross-year-signal-not-yet-validated"**. The specific concerns:

1. **All 3 above-mean-arm crashes concentrate in 2024** (W2E.3). The audit acknowledges this in section 15.3 open-concern-3 but section 15.2 does not carry the caveat prominently. The operand's "identifies crashes on the exposed arm" property is a within-2024 property in this corpus. Codifying it into MD-beta r2 as a primary covariate for the rest-adjacency arc without additional cross-year evidence would treat a 2024-specific pattern as a general mechanism.

2. **The operand is mechanically construct-valid but discriminatively 2024-specific**. The operand does what it says (identifies above-phase-baseline pre-window load); the operand's discrimination of crashes is a 2024 within-year finding. These are two separate claims and the audit does not always separate them (e.g. section 11.5 "operand behaves sensibly" conflates mechanical no-false-firing with discriminative validation).

3. **The very_heavy n=6 perfect classification** (W2E.2) is a hard fact at data resolution but ~5% likely under chance. Codifying it as the primary joint stratifier (end_class + phase_std > 0) at MD-beta r2 without further descriptive evidence would over-anchor on a fragile pattern.

**Recommended staged path**:

- **Option A (minimal)**: allow MD-beta r2 to codify the phase-standardised operand as a candidate covariate on the rest-adjacency arc, but codify it as **prospectively-testable** rather than validated. Explicit r2 language: "the phase-standardised residual is the covariate operand; its discriminative power on 2024 PS-True is a within-year observation and requires additional crash-event accumulation at Stage H prospective monitoring for cross-year validation". Reader should not treat r2's codification as a validated mechanism claim.

- **Option B (fuller)**: Wave 2F broader-cross-year descriptive validation before r2 codification. Wave 2F would extend the operand test to (i) other absolute-load-shift years if any exist in the corpus, (ii) the pooled LC-era with year-fixed-effect adjustment, and (iii) explicit within-2024 sensitivity tests (leave-one-out on the 3 crashes; alternative operand definitions like within-year phase-standardisation to separate cross-year from within-phase variance). If Wave 2F shows the signal is 2024-specific, r2 codifies with a strong "prospectively-testable within-year" caveat; if Wave 2F shows a broader pattern, r2 codifies with more confidence.

**Reviewer recommendation**: Option A is the minimum-defensibility path; Option B is the honest research-discipline path. The user's earlier pivot from Path R2B (defer to Stage H) to Path R2C (codify at r2 with phase-standardisation) resolves the phase-confound but does not resolve the cross-year-concentration concern. Wave 2E surfaces the concern (section 15.3) but does not resolve it, and the "READY" verdict in section 15.2 papers over it.

### 4.b Load-bearing: descriptive-narrative vs Haldane-Anscombe framing -- **DESCRIPTIVE-NARRATIVE IS ADEQUATE, WITH ADDITIONS**

The section 10 RR-undefined + section 9 perfect-classification framings are defensible as descriptive-only-narrative for a Stage -1 audit. Applying Haldane-Anscombe correction to compute a finite RR would be an inference-level convention violation on a Stage -1 descriptive audit; the audit's choice to report RD only is correct per CONVENTIONS section 2.1.

**However**, the descriptive-narrative framing needs three specific additions:

1. **Overfitting-suspected caveat on section 9 perfect classification** (W2E.2). Add a footnote to section 9.2 or 9.5: "Perfect within-stratum classification at n=6 with 3 events is achievable by chance under exchangeability of crash labels with probability ~1/20 (5%)." This does not require the audit to compute a null; it requires the audit to acknowledge that "perfect classifier" language is stronger than the sample size supports and could reflect trivial chance in addition to signal.

2. **Explicit RR-undefined note in section 10.3**: "Zero unexposed crashes make RR undefined; Haldane-Anscombe correction (add 0.5 to zero cells) would yield a finite RR but is an inference-level convention not applied here per Stage -1 descriptive-only scope. The load-bearing signal is the 10-of-10 zero-outcome observation, bounded by Wilson upper 27.8% on the arm rate." This makes the discipline choice explicit rather than tacit.

3. **Cross-year silence acknowledgement in section 11.5** (W2E.3 + W2E.4 + W2E.10 combined): "The operand's discriminative property is tested only on 2024 PS-True; 2023 evidence is uninformative due to 18/2 arm asymmetry and n=2 not viable; 2025-2026 evidence is silent due to zero crashes." Section 11.5's current "behaves sensibly" headline should be replaced.

### 4.c Non-load-bearing revisions

- Soften "SURVIVES phase-standardisation" (section 4.4 + 7.3) to "directional pattern preserved" or similar. (Layer 1.3)
- Soften "READY for r2 codification" (section 15.2) to "operand-definition-ready, cross-year-discrimination-not-yet-validated" or similar. (Layer 4.6, W2E.9)
- Add pre-specification attestation for cut B + cut C in section 12.5: "cut-points >0.5 sd and >1.0 sd are statistical-convention sigma multiples, pre-specified as sensitivity companions, not chosen from the observed crash distribution." (Layer 4.4, W2E.6)
- Add note to section 14.2: "the mathematical-zero cut-point happens to yield 100% sensitivity on the 3 2024 crash-cases; this is an empirical observation, not the justification for the cut-point choice." (W2E.8)
- Add footnote to section 11.1 + 11.3 clarifying 2023 arm asymmetry means the operand is untestable at 2023 PS-True resolution, not that it "does not fire spuriously". (W2E.4)

### 4.d Positive re-anchoring

The audit's central methodological move -- phase-standardised operand construction to respect the citalopram phase-boundary from Wave 2D section 10.3 -- is well-executed. The construct-validity trade-off in section 13 is presented symmetrically. The cross-audit arithmetic verification in section 3 is a non-trivial consistency check that passes cleanly. The concerns above are on framing + readiness declaration, not on the core operand-definition work. With the section 4.a downgrade of the readiness verdict + the section 4.b descriptive-narrative additions, the operand-definition work itself is defensible as a Stage -1 producer-mode Wave 2E audit.

---

## 5. Verdict + one-sentence reasoning

**Verdict: DEFENSIBLE with revision.**

Reasoning: the phase-standardised operand construction correctly respects the Wave 2D section 10.3 citalopram phase-boundary constraint and passes L2 stationarity + L4 personal-baseline + L4 definitional-pair discipline; the framing revisions concern (a) softening "SURVIVES" / "READY" / "perfect classifier" headlines to match the underlying narrative-only + n<10 + within-2024 evidence resolution, and (b) explicit acknowledgement in section 15.2 + section 11.5 that the operand's discriminative property is a 2024-within-year finding whose cross-year generalisability is not validated by Wave 2E.

---

## Methodology footer

**Reviewer**: Claude (Opus 4.7) in fresh-session reviewer-mode subagent per [CONVENTIONS section 1.2](../CONVENTIONS.md#12-reviewer-mode-claude-audits-does-not-edit).
**Date**: 2026-07-16.
**Cold-context attestation**: this session had NO prior knowledge of the Wave 2E audit; all evidence read from disk (target audit.md, companion audit.py, all 11 output CSVs spot-checked, parent Wave 2D audit section 10.3 verified, MD-alpha Wave 2A audit section 8 cross-verified against Wave 2E section 3, CONVENTIONS sections 1-5 read for checklist inheritance, reviews/README.md 4-layer checklist read for verdict spec).
**No edits made**: target audit.md, audit.py, output CSVs, parent Wave 2D audit, MD-alpha Wave 2A audit, MD-alpha + MD-beta + parent Q24 methodology MDs, and CONVENTIONS.md NOT modified by this session.
**Verdict tier used**: three-tier per [reviews/README.md](README.md#verdict-format) (PASS / PASS with caveats / REVISION RECOMMENDED) mapped to the methodology-review tier the user brief specified (DEFENSIBLE / DEFENSIBLE with revision / REVISION RECOMMENDED / BLOCKING). "DEFENSIBLE with revision" chosen as the closest equivalent to "PASS with caveats" given the load-bearing revisions in section 4.a + 4.b.
**Filename**: `methodology-Q24-mdbeta-wave2e-phase-standardised-prewindow-2026-07-16.md`.
**Load-bearing recommendations**: section 4.a (r2-readiness downgrade to NEEDS-MORE-VALIDATION with Option A minimum-defensibility + Option B fuller-Wave-2F path); section 4.b (descriptive-narrative is adequate with 3 specific additions: overfitting-suspected caveat on section 9, explicit RR-undefined framing note in section 10.3, cross-year silence acknowledgement in section 11.5).
**No emoji, no em-dash** in this report per user standing instruction (memory `feedback_no_emdash_in_ui` extends to research artefacts).
