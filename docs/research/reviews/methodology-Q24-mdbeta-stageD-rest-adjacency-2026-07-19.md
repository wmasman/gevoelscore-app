# Methodology review: Q24 MD-beta Stage D descriptive audit -- rest-adjacency arc

**Target artefact**: [`analyses/descriptive/Q24-mdbeta-stageD-rest-adjacency/descriptive_audit.md`](../analyses/descriptive/Q24-mdbeta-stageD-rest-adjacency/descriptive_audit.md) DRAFT r1 2026-07-19 (producer-mode Stage D descriptive audit per [CONVENTIONS section 1.2](../CONVENTIONS.md#12-reviewer-mode-claude-reads--writes-a-reasoned-report--recommendations); drafted by producer-mode subagent under user delegation).

**Target commit**: uncommitted DRAFT r1 (working tree state 2026-07-19; script `scripts/stage_d_rest_adjacency.py` + 11 output CSVs + `episode_table.csv` at OUTPUT_DIR timestamped 2026-07-19 12:12).

**Reviewer**: fresh-session Claude (Opus 4.7) under user delegation. Cold context. Read target audit MD end-to-end + companion `scripts/stage_d_rest_adjacency.py` (972 lines) + all 11 output CSVs + `episode_table.csv` head + MD-beta LOCKED r2 2026-07-17 end-to-end + reviews README 4-layer spec + Wave 2C review report as structural template + CONVENTIONS sections cited by the audit from disk. No exposure to drafting-session context; doc-only knowledge.

**Review type**: reviewer-mode per [CONVENTIONS section 1.2](../CONVENTIONS.md#12-reviewer-mode-claude-reads--writes-a-reasoned-report--recommendations); 4-layer checklist walk per [`reviews/README.md`](README.md), adapted for a producer-mode Stage D descriptive audit rather than a reviewer-mode hypothesis-result artefact. Verdict per this doc's section 5.

**Discipline**: NO edits to target audit, MD-beta LOCKED r2, CONVENTIONS, memories, or output CSVs. All recommendations go in section 4. No em-dash. No emoji. No stage or commit action taken.

---

## 1. What the data shows

Empirical claims made by the target audit, plain restate (interpretive framing separated in section 2). All numbers cross-verified against `output/*.csv` byte-for-byte.

1. **Baseline reproduction anchor (audit section 1.2)**. MD-beta section 6.6 baseline 2x2 on omnibus `rest_day_p25` at K=3 rest-after, era ALL, end_class ALL, NaN=False convention: 100 / 12 / 168 / 34, RR = 1.571, bootstrap 95% CI (0.885, 3.297), Wilson per-arm CIs 12.30 to 22.60 (rest-adjacent) vs 6.24 to 17.80 (rest-absent). Byte-for-byte reproduction of MD-beta 6.6 (100 / 12 / 168 / 34, RR = 1.57). Verified against `output/omnibus_by_end_class_K3_after.csv` row `omnibus_ALL_K3_after_era_ALL`.

2. **Wave 2C reproduction spot-check (audit section 1.3)**. Two variants on ALL-end_class K=3 rest-after era-pooled. MD-beta 3.1.1 pure-strategic (`rest_day_p25 == True AND gs >= 5`): 84 / 226 with 8 / 38 crashes, RR = 0.566. Wave 2C proactive-strategic (adds `no is_crash in [d-3, d-1]` filter): 80 / 230 with 5 / 41 crashes, RR = 0.351. Wave 2C reference in its own CSV is 80 / 232 with 5 / 41, RR = 0.354; the audit reproduces to within 2 episodes in the false arm (undef-drop convention differs by 2). Documented explicitly in the audit text.

3. **Headline cell (audit section 3.1, `output/headline_strategic_heavy_K3_after.csv`)**. Strategic x heavy end_class x K=3 rest-after x crash-in-5d, era-pooled: 40 exposed with 2 crashes (5.00%, Wilson 1.38 to 16.50) vs 122 unexposed with 28 crashes (22.95%, Wilson 16.38 to 31.17); RR = 0.218, bootstrap 95% CI (0.000, 0.610) with 10 000 / 10 000 valid rounds; RD = -0.180, bootstrap 95% CI (-0.276, -0.074); Fisher's exact p = 0.0097 (descriptive-only). Wilson-viable floor passes.

4. **Era-stratified immediate companions (audit section 4)**. Pre-cital era: 10 exposed / 72 unexposed with 1 / 21 crashes, RR = 0.343, bootstrap CI (0.000, 1.267). Post-cital era: 30 / 50 with 1 / 7 crashes, RR = 0.238, bootstrap CI (0.000, 1.179). Per-era point estimates sit close to pooled (0.218); per-era bootstrap CIs both include 1.0 while the pooled does not. Verified against `output/headline_strategic_heavy_K3_after.csv` rows for pre_cital + post_cital.

5. **Very_heavy end_class sensitivity (audit section 5, `output/sens_strategic_very_heavy_K3_after.csv`)**. Sign-inversion relative to strategic pre-commit direction. Era-pooled: 44 / 104 with 6 / 10 crashes, RR = 1.418, bootstrap CI (0.417, 3.772). Pre-cital: 19 / 54, 2 / 5 crashes, RR = 1.137. Post-cital: 25 / 50, 4 / 5, RR = 1.600. All three bootstrap CIs on RR include 1.0.

6. **Crisis stratum (audit section 6, `output/crisis_by_end_class_K3_after.csv`)**. Heavy end_class era-pooled: 28 / 132 with 15 / 15 crashes, RR = 4.714, bootstrap CI (2.600, 9.000), Fisher p = 3.26e-06. Heavy pre-cital: 18 / 64, 12 / 10, RR = 4.267, bootstrap CI (2.234, 9.620). Heavy post-cital: 10 / 68, 3 / 5, RR = 4.080, bootstrap CI (0.000, 18.19). Very_heavy pre-cital: exposed n = 8, fails Wilson-viable floor; reported narrative-only at 2 / 8 vs 5 / 65 with raw RR 3.25 and no bootstrap CI.

7. **Borderline stratum (audit section 7)**. Heavy: 54 / 108, 9 / 21, RR = 0.857, bootstrap CI (0.346, 1.674). Very_heavy: 45 / 103, 4 / 12, RR = 0.763, bootstrap CI (0.144, 2.035). Both include 1.0. Descriptive-only per no direction pre-commit.

8. **Omnibus stratum (audit section 8, `output/omnibus_by_end_class_K3_after.csv`)**. Heavy era-pooled: 108 / 57, 24 / 6, RR = 2.111, bootstrap CI (1.017, 6.711). Heavy pre-cital: 57 / 25, 18 / 4, RR = 1.974. Heavy post-cital: 51 / 32, 6 / 2, RR = 1.882. Very_heavy near-null (RR = 0.975 pooled). ALL end_class ALL era = the baseline anchor above.

9. **Absolute-step operand (audit section 9, `output/abs3k_strategic_heavy_K3_after.csv`)**. Era-pooled heavy: 26 / 137, 0 / 30 crashes, rate 0.00% (Wilson 0.00 to 12.87) vs 21.90% (Wilson 15.79 to 29.54). Zero exposed crashes force Haldane; RR (Haldane) = 0.084; RD = -0.219, bootstrap CI (-0.290, -0.151); Fisher p = 0.0047.

10. **K-ladder (audit section 10)**. K=1: 0 / 21 vs 30 / 142, Haldane RR = 0.107, RD = -0.211. K=2: 0 / 28 vs 30 / 135, Haldane RR = 0.077, RD = -0.222. K=3: as headline, RR = 0.218, RD = -0.180. Direction preserved across K; no sign inversion in the ladder.

11. **Rest-BEFORE-heavy companion (audit section 11)**. Era-pooled: 40 / 124, 6 / 24 crashes, RR = 0.775, bootstrap CI (0.242, 1.584). Pre-cital: 12 / 69, 2 / 20, RR = 0.575, bootstrap CI (0.000, 1.597). Post-cital: 28 / 55, 4 / 4, RR = 1.964, bootstrap CI (0.346, 8.848). Cross-era sign-inversion between pre- and post-cital.

12. **Preflight sample-floor probe (audit section 1.4, `output/preflight_sample_floor.csv`)**. 36 cells; 34 pass Wilson-viable floor of 10 exposed / arm; 2 fail. Failing: strategic_abs3k x heavy x pre-cital (4 exposed), crisis_p25 x very_heavy x pre-cital (8 exposed). Both surfaced verbatim with NEEDS-MORE-DATA framing.

13. **Discipline attestations (audit section 13)**. Descriptive-before-inference, definitional-pair, named-count, NaN-boundary, caveat-class, descriptive-before-theory, physical-rest-only, 6-mechanism era caveat, reciprocal-attestation, generalisation-scope, era-pooled headline rationale, autocorrelation block length = 1, Wilson-viable floor, Haldane, no-em-dash + no-emoji all attested.

---

## 2. What fired and why

Layer-grouped fires with citation, magnitude, and absorb-vs-escalate signal per fire.

### Layer 1 -- Universal reporting (SCRIBE 2016; STROBE 2007)

**L1.1 Pre-registration of the operand contract -- PASSES with high confidence.** The audit executes precisely what MD-beta r2 sections 3.1 + 3.1.1 + 3.5.1 + 6.9 pre-committed: `rest_day_p25_physical_strategic` primary at heavy end_class K=3 rest-after era-pooled with immediate era-stratified companions; joint end_class x gevoelscore-bucket stratifier; strategic and crisis reported as the definitional pair with borderline as third bucket and omnibus preserved. Section 1.2 verifies the MD-beta 6.6 anchor byte-for-byte; the CSV row confirms 100 / 12 / 168 / 34, RR = 1.5710 to four decimals. Section 3 headline denominators (162 = 165 heavy pool minus 3 undef-and-False drops) reconcile against the preflight cell (165 with 40 True + 125 False). No silent operand redefinition detected. **Absorb**: none needed.

**L1.2 Named operationalisation with computation path -- PASSES with high confidence.** Every operand is defined in section 3.1 or 6.1 or 7 or 8 or 9 preambles with the column name (`rest_day_p25_physical_strategic`), the row-filter (heavy end_class + LC-era + `crash_window_full == True` + operand undef-drop where applicable), the rolling-window parameter (30d, min_periods=15, p25), and the source CSV path. Script `scripts/stage_d_rest_adjacency.py` is idempotent, 972 lines, well-commented, and every cell reproducible with a single re-run. **Absorb**: none needed.

**L1.3 Statistical method named with parameters -- PASSES.** Section 2 lists Wilson `proportion_confint(method='wilson')` at alpha=0.05; Fisher's exact via `scipy.stats.fisher_exact` two-sided; bootstrap B = 10 000, block length = 1, RANDOM_SEED = 20260716, percentile 2.5 / 97.5; Haldane-Anscombe (+0.5) applied only when a raw cell = 0 and labelled in the `haldane_applied` column. Verified against script lines 360 to 467. **Absorb**: none needed.

**L1.4 Confounders enumerated not silently controlled -- PASSES.** Section 4.4 reproduces the 6-mechanism era caveat verbatim (citalopram, learned-pacing, tactical-Garmin-use, natural LC trajectory, envelope drift with the 19.39 vs 5.17 anchor from MD-alpha Wave 2A section 8, aging + seasonality). Section 13 lists all six MD-beta section 3.9 confounds and all eight MD-beta section 5 confounds as caveats, not corrections. No post-hoc adjustment attempted. **Absorb**: none needed.

**L1.5 Limitations separate from headline -- PASSES.** Section 3.2 descriptive observation labels the bootstrap CI lower bound of 0.000 as "a small-sample feature of a rate-2/40 arm, not a data-quality artefact". Section 12.3 logs sample-floor failures. Section 12.4 explicitly states per-era bootstrap CIs both include 1.0 while pooled does not, without hiding the per-era finding. Section 5.4 acknowledges the very_heavy sign-inversion. **Absorb**: none needed.

**L1.6 Discipline attestation coverage vs actual practice -- ABSORB.** Section 13 asserts "no latent-state / R(t) / reserve / buffer / envelope-capacity constructs anywhere". Spot-check confirms compliance; the audit uses only descriptive-with-CI language throughout. The "no em-dash" attestation is honoured everywhere including the section 4.4 six-mechanism enumeration (numbered list rather than em-dash-separated). **Absorb**: none needed; positive precedent.

### Layer 2 -- Observational n=1 (Daza 2018; Personal Science norms)

**L2.1 Counterfactual framing at subject-level -- PASSES.** Section 3 primary contrast compares strategic-rest-adjacent to strategic-rest-absent within the same 162-episode heavy-end pool at a similar sample-population level, not to a between-subject reference. Wave 2C proactive-strategic operand at section 1.3 explicitly does NOT reweight to an external population. Section 3.2 descriptive observation uses "descriptively consistent with the MD-beta section 3.7 pre-commit direction" rather than "supports" or "confirms". **Absorb**: none needed.

**L2.2 Stationarity acknowledged -- PASSES with high confidence.** Section 4.3 explicitly acknowledges that per-era bootstrap CIs include 1.0 while pooled does not, and reads that as CI-tighter primary plus falsifiability companions rather than as a signal-strength claim on either era. Section 4.4 reproduces the 6-mechanism era caveat verbatim; the audit does NOT claim any medication effect. Section 12.4 restates the era instability at findings-summary level. This is exactly the stationarity-surfacing the MD-beta r2 sections 3.5 + 5 confound 7 upgrade demands. **Absorb**: none needed.

**L2.3 Calendar-time vs subject-time separation -- PASSES.** The pre-cital / post-cital boundary at 2024-04-09 is calendar-anchored and aligned with the MD-alpha `recovery_phase` boundary. Section 4.4 uses "temporal anchor" language rather than any phase-mechanism claim. Episode unit is D_end calendar date; no subject-time confusion. **Absorb**: none needed.

**L2.4 Data provenance traceable -- PASSES.** Section 2 lists script path + input path + dump version (v3.2) + random seed + statistical machinery + NaN handling per operand + era stratifier + unit of analysis + filter chain. Script `load_lc_stratum()` at lines 85 to 158 anchors the pipeline. Every CSV writes with the same `_write_rows()` helper (line 564). **Absorb**: none needed.

**L2.5 Held-out structure per `project_garmin_research_bias_boundary` -- PASSES.** The audit reads across 2022 to 2026-06-05 including the 2026 pre-dump extraction window. Gevoelscore is the user's subjective log, not Garmin-derived, so the analytical-bias boundary does not fire on gs-bucket. `total_steps` and `exertion_class_lagged_lcera` are Garmin-derived but were tactical inputs pre-dump; consistent with the memory. No fire. **Absorb**: none needed.

**L2.6 Prior motivation named -- PASSES.** Sections 1 headline, 5, 6, 7, 8, 9 each preamble cite MD-beta anchor sections (3.1.1, 3.5.1, 3.7, 6.6, 6.9). Nothing surfaced without explicit MD-beta or Wave 2C / 2D anchor. **Absorb**: none needed.

### Layer 3 -- Time-series specific (Natesan 2023; WWC 2022; CENT 2015)

**L3.1 Autocorrelation addressed -- PASSES with high confidence.** Section 2 attests bootstrap block length = 1 per MD-beta section 3.6, matching the episode-end unit-of-analysis argument at parent Q24 MD section 7.10. Section 13 attestation restates the same. Script `bootstrap_rr_rd_ci()` line 417 uses episode-level resampling with `rng.integers(0, n, size=n)` at n = n_episodes, which is block-1 sampling. No time-block structure imposed. Consistent with MD-beta pre-commit. **Absorb**: none needed.

**L3.2 Lag-carryover -- N/A at Stage D descriptive scope.** Outcome is a binary crash-in-5d occurrence, not a continuous trajectory. Lag-carryover machinery not applicable to the operand family. **Absorb**: none needed.

**L3.3 Multiple testing across cells -- SUBSTANTIVE PARTIAL FIRE (absorb-tier).** The audit reports 30+ cells across headline (1 pooled + 2 era-stratified companions), very_heavy sensitivity (3), crisis (5 floor-passing + 1 NEEDS-MORE-DATA), borderline (2), omnibus (9), abs-step (1), K-ladder (3), rest-BEFORE (3). Section 11 Fisher p-values at 0.0097 (headline) + 0.0047 (abs-step) + 3.26e-06 (crisis heavy pooled) + 6.02e-05 (crisis heavy pre-cital) are reported as descriptive-only per CONVENTIONS section 2.1 with explicit "NOT as verdicts" framing at section 13 first bullet. This is the correct discipline label. However, the audit does not explicitly cite the 30+ cell count as a multiple-testing surface, and a fresh Stage S1 reader could inadvertently treat the crisis Fisher p = 3.26e-06 as inferentially load-bearing without noticing that this is one of a dozen comparisons whose direction is pre-committed. **Absorb**: patch section 13 discipline attestations or section 12.3 sample-floor-failures block to explicitly name the 30+ cell count as a multiple-testing surface handled via descriptive-with-CI framing, and to reiterate that no single p-value crosses to a verdict at Stage D. Positive framing: this is a discipline-tightening at the audit level, not a numerical revision; the audit's descriptive-with-CI framing is already correct in substance.

**L3.4 Permutation null block length documented -- PASSES.** Block length = 1 documented in section 2 + section 13 attestation + script line 425 comment. Consistent with MD-beta section 3.6 + parent Q24 MD section 7.10. **Absorb**: none needed.

**L3.5 Trend vs level claim separation -- PASSES.** Section 10.4 correctly separates the K-ladder "tightness of adjacency window does not sign-invert" observation from any trend-claim about K itself. Section 12.5 restates at findings-summary level. **Absorb**: none needed.

### Layer 4 -- Project-specific audit hooks (CONVENTIONS sections 3-4 + memories)

**L4.1 Personal baseline per CONVENTIONS section 3.1 -- PASSES.** `rest_day_p25` = rolling 30d p25 per script line 113 (window=30, min_periods=15). Consistent with MD-beta section 3.1. **Absorb**: none needed.

**L4.2 Lagged variant per CONVENTIONS section 3.5 -- PASSES.** The audit uses `exertion_class_lagged_lcera` for the heavy-episode definition, consistent with MD-beta section 2.2 inheritance from parent Q24 MD. Verified at script line 100. **Absorb**: none needed.

**L4.3 One column per definitional pair per CONVENTIONS section 3.3 -- PASSES with high confidence.** Section 6 head paragraph is a **model** reciprocal-attestation upfront: "strategic + crisis are ONE definitional-pair split of the omnibus `rest_day_p25` operand, NOT two independent tests. Any Stage S1 synthesis that reports the strategic-primary section 3 RR and the crisis-sensitivity section 6 RR as independent evidence violates the definitional-pair discipline codified at MD-beta section 3.7 + Wave 2C section 6.5." Section 12.7 reminder at findings-summary level restates the same. The reads at section 3 (strategic RR = 0.218) and section 6.1 (crisis heavy RR = 4.714) are structurally consistent with the reciprocal-pair reading. No violation of the pair discipline detected anywhere in the audit. **Absorb**: none needed; this is exactly the discipline the MD-beta r2 recommendation 4 codified.

**L4.4 Crash-drop sensitivity per CONVENTIONS section 3.4 -- N/A.** The outcome IS crash occurrence; the crash-drop sensitivity hook applies to Layer 4+ correlations where crash days confound the read. Not applicable at Stage D on binary crash-in-5d outcome. **Absorb**: none needed.

**L4.5 Spike-detecting metric per CONVENTIONS section 3.5 -- PASSES.** `end_class` at episode-end day is a spike metric (per-day intensity classification), not a daily-average. Consistent by construction. **Absorb**: none needed.

**L4.6 Counts named with scheme + unit + source per CONVENTIONS section 3.6 -- PASSES with high confidence.** Section 1.1 corpus counts each carry scheme + unit + source (e.g. "Crash days | 103 (crash_v2, day-level)", "gap=0 heavy episodes | 314 | script + parent Wave 2B section 3"). Every 2x2 table cites its source CSV path in the section preamble. Section 12.3 sample-floor failures carry per-cell counts + source. Section 13 named-count discipline attestation explicit. **Absorb**: none needed.

**L4.7 Caveat-class vs a-priori-class framing -- PASSES with high confidence.** Every finding is framed as "descriptively consistent with", "sign-inverted relative to", or "descriptive-only". No a-priori language leaks in. Section 3.2 explicitly qualifies as descriptive observation not verdict. Section 5.4 sign-inversion is framed as "expected non-generalisation" per MD-beta 6.9 generalisation-scope attestation, not as surprise or falsification. Section 12.2 lists all sign-inversions with the per-pre-commit expectation label. **Absorb**: none needed.

**L4.8 Prior-driven hypothesis framing (Stage D producer-mode) -- PASSES.** Section 3.2: "descriptively consistent with the MD-beta section 3.7 pre-commit direction (strategic-rest-adjacent -> LOWER crash rate) at the era-pooled read on heavy end_class". No "validates" or "confirms". Section 12.1 restates the discipline: "this is a descriptive observation and NOT a validation; the Stage D descriptive audit reports the pattern; any inferential-verdict framing is a downstream Stage H pre-registration + Stage H test concern." **Absorb**: none needed; positive precedent for section 12.1 discipline framing.

**L4.9 Descriptive-before-theory per user 2026-07-17 directive -- PASSES.** No citation of `resilience_latent_state.md`. No latent-state / R(t) / reserve / buffer / envelope-capacity constructs. Section 5.4 "mechanism (b) pre-window-load partial-mitigation" and "mechanism (e) intensity-interaction residual" are the two mechanism-labels used, and both are grounded in MD-beta section 5 confound 8 codified vocabulary; neither invokes an unobserved latent variable. Section 13 discipline attestation explicit. **Absorb**: none needed.

**L4.10 Physical-rest-only semantic constraint per memory `project_rest_day_operand_semantics` -- PASSES.** Section 13 attestation explicit: "`_physical_` operands measure low-step days modulated by gevoelscore-on-that-day; they do NOT measure cognitive rest, emotional rest, or planning quality." No conflation detected in the audit body. The strategic stratifier is (gevoelscore >= 5) not (planning-well) or (rested-well); the discipline is respected. **Absorb**: none needed.

**L4.11 6-mechanism era caveat verbatim per MD-beta section 5 confound 7 -- PASSES.** Section 4.4 lists the six mechanisms verbatim in the order MD-beta uses them, with the 19.39 vs 5.17 min/day envelope-drift anchor from MD-alpha Wave 2A section 8 preserved. Section 4.4 closes with "The stratifier does NOT identify medication effect at n=1... No causal claim about medication is made or supported by this stratifier." Faithful reproduction. **Absorb**: none needed.

**L4.12 NaN-handling consistency per CONVENTIONS section 3.10 -- SUBSTANTIVE PARTIAL FIRE (absorb-tier, clarification recommended).** The audit uses TWO different NaN-handling conventions: omnibus `rest_day_p25` uses NaN=False (to reproduce MD-beta 6.6 byte-for-byte); strategic + crisis + borderline + abs3k use undef-drop-where-observed-False (arm-True observed rest-day resolves ambiguity, so True cases retained). Section 2 documents both explicitly. This is an internally consistent split with a load-bearing rationale (the byte-for-byte MD-beta 6.6 anchor forces NaN=False on the omnibus; the definitional-pair extension operands would drop too many episodes under NaN=False given the 152 / 1524 = 10% gevoelscore-NaN concentration in pre-tracker 2022). **However**, the rationale for the different convention is documented in section 2 in a single line and never re-surfaced in the interpretive sections. A fresh Stage S1 reader might miss the difference and read the strategic-primary 3-episode-undef-drop as introducing an operand-scope confound relative to the omnibus baseline. **Absorb-tier recommendation**: add one sentence to section 3.1 headline preamble explicitly cross-referencing the section 2 NaN policy split, and one sentence to section 8 omnibus preamble stating that omnibus intentionally uses a different NaN policy to preserve the byte-for-byte MD-beta 6.6 anchor. This is a discipline-tightening, not a numerical revision.

**L4.13 Wave 2C operand-scope disclosure -- SUBSTANTIVE PARTIAL FIRE (absorb-tier).** Section 1.3 discloses the tension between the MD-beta 3.1.1 pure-strategic operand (`rest_day_p25 == True AND gs >= 5`, RR = 0.566 on ALL end_class) and the Wave 2C proactive-strategic operand (adds `no is_crash in [d-3, d-1]` filter, RR = 0.351). The audit calls it out honestly: "See section 12 for a note on the operand-scope tension." However, section 12 does NOT return to this tension explicitly; the operand-scope difference is only surfaced in section 1.3 and left as a pointer. The tension is architecturally important: MD-beta 6.9 headline cell is `rest_day_p25_physical_strategic x heavy end_class`, but the RR = 0.354 empirical anchor cited at MD-beta section 3.7 for that direction pre-commit is from the Wave 2C proactive-strategic operand, which is NOT the MD-beta 3.1.1 primary. On the audit's own reproduction, pure-strategic on ALL end_class gives RR = 0.566 (RD -0.073, bootstrap CI including 1.0) versus proactive-strategic RR = 0.351 (RD -0.116, bootstrap CI excluding 1.0). The proactive filter adds a 3-day-crash-lookback that the MD-beta 3.1.1 operand does not have. **Absorb-tier recommendation**: patch section 12 to add a subsection or paragraph explicitly discussing the operand-scope tension. State clearly that the MD-beta 3.7 empirical anchor citation of RR = 0.354 is from a slightly different operand than the MD-beta 3.1.1 primary; both directions match the pre-commit but the empirical-anchor magnitude cited at MD-beta 3.7 is not directly attributable to the r2 primary operand. This is a Stage-S1-and-downstream discipline flag that would prevent the two operand magnitudes from being conflated silently. Not a numerical revision; a framing tightening.

**L4.14 Very_heavy sign-inversion framing -- PASSES.** Section 5 preamble explicitly labels this sensitivity as "the cell where gevoelscore-conditioning alone is insufficient per Wave 2D section 4 empirical anchor" and "NOT an alternative headline". Section 5.4 frames the sign-inversion as consistent with Wave 2D within-2024 finding and MD-beta 6.9 generalisation-scope attestation, calling it out as "expected non-generalisation" rather than surprise. Section 12.2 restates. This is exactly the correct discipline; the audit does NOT try to falsify the strategic pre-commit on this cell. **Absorb**: none needed.

**L4.15 Absolute-step operand result reconciliation -- SUBSTANTIVE PARTIAL FIRE (absorb-tier).** MD-beta section 3.1 sensitivity companion paragraph cites Wave 2D section 7 anchor at "pooled RR shifts 0.354 -> 0.111 in the sign-flip direction". Audit section 9.1 reports pooled RR = 0.084 (Haldane-corrected) on heavy-end-class-only at K=3 rest-after era-pooled. These are two different operand-scope readings: Wave 2D 0.111 is on ALL end_class + proactive filter; audit 0.084 is on heavy end_class only + no proactive filter + Haldane-corrected. Direction preserved on both; magnitudes differ. The audit does NOT reconcile these two numbers explicitly. Section 9.2 says "the observed direction (rest-adjacent lower) survives the operand swap" but does not name the 0.111 vs 0.084 delta or explain that the operand-scope difference (heavy-only + no proactive filter + Haldane) accounts for the magnitude difference. **Absorb-tier recommendation**: add a one-liner to section 9.2 noting the operand-scope difference vs the Wave 2D 0.111 anchor. Not a numerical revision; a cross-reference tightening.

**L4.16 Sample-floor discipline -- PASSES with high confidence.** Section 1.4 explicitly names the informal Wilson-viable floor as ~10 exposed per arm. Section 6.5 crisis vh pre-cital reports narrative-only with raw counts + raw RR + explicit "no bootstrap CI computed at this sample floor" statement; no CI reported despite Wilson still being computable. This is disciplined restraint above what the script strictly enforces (the script still computes Wilson CIs on per-arm rates even under floor-fail, but the audit body correctly does not surface those). Verified against `output/preflight_sample_floor.csv` + `output/crisis_by_end_class_K3_after.csv` row `crisis_very_heavy_K3_after_era_pre_cital` where `wilson_viable_floor_pass = False` and bootstrap columns are NaN. **Absorb**: none needed; positive precedent.

**L4.17 Post-cital crisis heavy floor-pass borderline -- ABSORB.** Post-cital crisis heavy has 10 exposed / 68 unexposed with 3 / 5 crashes; RR = 4.080; bootstrap 95% CI (0.000, 18.19); 9944 valid rounds out of 10 000. The exposed n = 10 is exactly at the floor; bootstrap CI lower bound 0.000 reflects that some rounds hit 0 exposed. Audit section 6.7 notes: "The post-cital era CI includes 0.0 in the bootstrap (from resamples where the arm-True side has 0 exposed episodes) but the point estimate remains 4.08." This is honest surfacing of a floor-pass borderline. **Absorb**: none needed.

---

## 3. What does not fire (selective)

Non-trivial passes worth stating positively:

- **Reciprocal-pair discipline upfront placement**. Section 6 head is a model of reciprocal-attestation-upfront discipline. The audit stakes the definitional-pair frame BEFORE reporting either sub-operand result, then closes at section 12.7 with the mirror reminder. Any Stage S1 reader who reads section 3 (RR = 0.218) and section 6 (RR = 4.714) as independent evidence would be doing so against explicit textual instruction to the contrary in two places.

- **Very_heavy sign-inversion framing restraint**. Every audit that has a sign-inversion on a sensitivity cell risks framing it as "the sign flips!" (implicit falsification-adjacent language). Section 5.4 correctly frames it as expected non-generalisation per MD-beta 6.9 generalisation-scope attestation. The temptation to over-read a sensitivity cell is real; the audit resists it. Section 12.2 restates the same restraint.

- **Baseline byte-for-byte anchor reproduction**. Section 1.2 reproduces MD-beta 6.6's 100 / 12 / 168 / 34 with RR = 1.571 to the last digit, confirming the operand pipeline is faithful to the r2 pre-commit. This is the single most important reproducibility check a Stage D descriptive audit can make, and the audit surfaces it as its own section 1.2 not buried in a footnote.

- **6-mechanism era caveat verbatim reproduction**. Section 4.4 lists all six mechanisms in the MD-beta order, closes with the "does NOT identify medication effect at n=1" attestation, and cross-references the MD-alpha Wave 2A section 8 envelope-drift anchor with the 19.39 vs 5.17 min/day numbers preserved. Fresh reader has no path to attribute era differences to citalopram specifically.

- **Descriptive-before-theory compliance**. No citation of `resilience_latent_state.md`, no reserve / buffer / envelope-capacity language, no latent-state variables. The two mechanism-labels the audit uses (pre-window-load partial-mitigation and intensity-interaction residual) are MD-beta section 5 confound 8 vocabulary, not theory-loaded constructs.

- **Direction language discipline at headline**. Section 3.2 says "descriptively consistent with the MD-beta section 3.7 pre-commit direction" not "validates" or "confirms". Section 12.1 restates. The word choice is load-bearing for the CONVENTIONS section 2.1 descriptive-before-inference gate; the audit stays within it consistently.

- **Preflight sample-floor probe emitted as its own CSV**. `output/preflight_sample_floor.csv` is a 36-row surface that lets a downstream consumer verify the floor logic per cell without recomputing anything. Two failing cells are named verbatim in section 1.4 with counts.

---

## 4. What would strengthen this finding

Concrete + named. Each recommendation states expected effect.

### 4.1 (Absorb) Explicit NaN-policy split disclosure at section 3 and section 8 preambles

**Recommendation**: at section 3.1 headline preamble, add one sentence cross-referencing the section 2 NaN policy split ("Under the operand-specific undef-drop convention from section 2, 3 episodes are dropped from the 165-episode heavy pool"). At section 8 omnibus preamble, add one sentence stating that omnibus intentionally uses NaN=False to preserve the byte-for-byte MD-beta 6.6 anchor.

**Rationale**: Two different NaN conventions are load-bearing for the audit. Section 2 documents both, but the reader who jumps into section 3 or section 8 without reading section 2 first misses the convention. This is a discipline-tightening, not a numerical revision.

**Expected effect**: prevents Stage S1 or downstream Stage H readers from inadvertently reading the strategic 162-episode-used vs omnibus 165-episode-used delta as an operand-selection artefact.

### 4.2 (Absorb) Section 12 subsection on operand-scope tension vs MD-beta 3.7 empirical anchor

**Recommendation**: add a new subsection 12.8 or extend 12.6 to explicitly discuss the operand-scope tension surfaced in section 1.3. State clearly that MD-beta section 3.7 cites RR = 0.354 as the empirical anchor for the strategic pre-commit direction, but that empirical anchor is on the Wave 2C proactive-strategic operand (adds `no is_crash in [d-3, d-1]` filter), NOT the MD-beta section 3.1.1 pure-strategic primary. The audit's own reproduction reports pure-strategic RR = 0.566 vs proactive-strategic RR = 0.351 on the same ALL-end-class pool. Both match the pre-commit direction; the magnitude difference is operand-scope.

**Rationale**: The MD-beta 3.7 anchor citation and the r2 primary operand are two different operands with two different magnitudes. Section 1.3 flags this; section 12 does not close the loop. A Stage S1 reader who reads MD-beta 3.7 and the audit sections 3 + 12 in that order could conclude that the audit's RR = 0.218 on heavy-end validates the RR = 0.354 anchor, when the operand delta and the intensity-restriction delta are structurally distinct. This is a framing tightening, not a numerical revision.

**Expected effect**: prevents Stage S1 or downstream synthesis from conflating the two empirical anchors and reading the audit as validating the RR = 0.354 pooled magnitude directly.

### 4.3 (Absorb) Section 9 absolute-step reconciliation vs Wave 2D 0.111 anchor

**Recommendation**: add a one-liner to section 9.2 noting that MD-beta section 3.1 sensitivity companion paragraph cites Wave 2D section 7 anchor at "pooled RR 0.354 to 0.111"; the audit's own RR = 0.084 differs from 0.111 by operand-scope (heavy-end-class only vs ALL end_class + proactive filter + Haldane correction). Explicitly disclose that the two RRs are both in the sign-flip direction on operand-analogous but not operand-identical reads.

**Rationale**: Same class of issue as recommendation 4.2 but on a different operand pair. The MD-beta cross-reference is honest about the magnitude difference but the audit does not close the loop on it. A single sentence removes the ambiguity.

**Expected effect**: prevents Stage S1 or downstream reads from taking the audit's 0.084 as a byte-match against MD-beta's cited 0.111.

### 4.4 (Absorb) Multiple-testing surface disclosure at section 13 or section 12.3

**Recommendation**: patch section 13 discipline attestations (or extend section 12.3 sample-floor-failures block) to explicitly name the 30+ cell count as a multiple-testing surface. State that Fisher p-values (0.0097 headline, 0.0047 abs-step, 3.26e-06 crisis heavy pooled, 6.02e-05 crisis heavy pre-cital) are reported descriptively per CONVENTIONS section 2.1 and are NOT interpreted at Stage D. Reiterate that the audit does not commit to any inferential threshold at any cell.

**Rationale**: The audit's discipline substance is correct (all p-values are correctly labelled descriptive-only), but the 30+ cell surface is not counted explicitly anywhere. A fresh reader could inadvertently treat the crisis p = 3.26e-06 as inferentially load-bearing. Explicit multiple-testing framing removes that risk.

**Expected effect**: hardens the descriptive-before-inference gate against a Stage S1 reader's temptation to elevate any single Fisher p to a verdict.

### 4.5 (Absorb, discretionary) Section 6.5 crisis vh pre-cital narrative-only computation attestation

**Recommendation**: at section 6.5, briefly state that Wilson per-arm rates ARE computable at n=8 exposed (25.0% Wilson CI, 5-arm 7.7% Wilson CI) but the audit deliberately does NOT report them beyond raw rates given the sample-floor policy. Explicit restraint documentation.

**Rationale**: The script computes Wilson CIs even under floor-fail; the audit body correctly does not report them. A fresh reader might wonder whether the CIs were computed. A one-line attestation ("Wilson CIs computable but withheld per Wilson-viable floor policy") closes the loop.

**Expected effect**: hardens the Wilson-viable floor discipline attestation at the exact cell where it fires.

### 4.6 (Absorb, discretionary) Post-cital rest-BEFORE-3 sign-inversion cross-reference

**Recommendation**: at section 11.3, add a cross-reference to section 12.4 pre-cital vs post-cital era instability paragraph. The post-cital rest-before RR = 1.964 (sign-inverted) is consistent with the endogeneity asymmetry per MD-beta section 3.9 confound 1 item 2 (rest-before more endogenous than rest-after). Section 11.4 states the endogeneity-asymmetry framing but does not link it to the era instability at section 12.4.

**Rationale**: The post-cital rest-before sign-inversion has TWO possible descriptive framings, both consistent with the audit's pre-commit: (i) endogeneity asymmetry per MD-beta 3.9 confound 1 item 2, (ii) era instability per section 12.4. Cross-referencing both would prevent a Stage S1 reader from picking one and running with it.

**Expected effect**: prevents a downstream synthesis from over-attributing the post-cital sign-inversion to a single mechanism.

---

## 5. Verdict

**DEFENSIBLE with revision.**

The Stage D descriptive audit r1 correctly operationalises the MD-beta r2 LOCKED pre-commit contract, reproduces the section 6.6 baseline anchor byte-for-byte (100 / 12 / 168 / 34, RR = 1.571), executes the section 6.9 headline cell (strategic x heavy x K=3 rest-after era-pooled, RR = 0.218 with bootstrap 95% CI 0.000 to 0.610) with the immediate era-stratified companions per section 6.9 falsifiability discipline (pre-cital RR = 0.343, post-cital RR = 0.238; both bootstrap CIs include 1.0), documents the very_heavy sign-inversion (RR = 1.418) as expected non-generalisation per MD-beta 6.9 generalisation-scope attestation rather than as surprise, reports the crisis reciprocal-pair contrast (RR = 4.714) with model reciprocal-attestation-upfront discipline at section 6 head and section 12.7 reminder, and applies the 6-mechanism era caveat verbatim at section 4.4 with the MD-alpha Wave 2A envelope-drift anchor preserved. Sample-floor discipline is exemplary at section 6.5 (crisis vh pre-cital n=8 narrative-only, no CI reported). Descriptive-before-theory compliance passes: no `resilience_latent_state.md` citation, no latent-state constructs, no theory-loaded mechanism-framing. Physical-rest-only semantic constraint respected throughout. Six absorb-tier recommendations improve NaN-policy cross-referencing, operand-scope tension disclosure at section 12, Wave 2D 0.111 vs audit 0.084 reconciliation, multiple-testing surface disclosure, section 6.5 Wilson-viable-floor restraint attestation, and section 11 endogeneity-asymmetry vs era-instability cross-reference. No BLOCKING issue found; the audit is safe to lock at r1 with the section 4 absorb-tier patches applied inline per producer-mode compression discipline. No architectural revision required.

---

## Methodology footer

This review walks the 4-layer checklist defined in [`reviews/README.md`](README.md), which inherits from:

- **Layer 1**: SCRIBE 2016 items 3 to 5, 14, 18, 22 to 24 (Tate et al., PMC4873717); STROBE 2007 items 6, 12, 13.
- **Layer 2**: Daza 2018 self-tracked n-of-1 counterfactual; Personal Science norms; project memory `project_garmin_research_bias_boundary` for held-out-structure framing.
- **Layer 3**: Natesan Batley et al. 2023 systematic review; WWC 2022 SCED handbook v5.0; CENT 2015 (Shamseer et al.). Applied at Stage D descriptive scope to bootstrap block-length + multiple-testing surface + trend-vs-level separation.
- **Layer 4**: [CONVENTIONS.md](../CONVENTIONS.md) sections 2.1 (descriptive-before-inference), 3.1 (personal baseline), 3.3 (definitional pair), 3.4 (crash-drop sensitivity, N/A at binary crash outcome), 3.5 (spike-detecting metrics), 3.6 (named counts), 3.10 (NaN-boundary rule), 4.2 (caveat-class framing); memories `project_rest_day_operand_semantics` (physical-rest-only semantic constraint), `project_garmin_research_bias_boundary` (held-out-structure), user 2026-07-17 descriptive-before-theory directive.

Confounding-by-indication epidemiological anchor: Salas M et al. 2001; Kyriacou DN & Lewis RJ 2016 JAMA (both cited by MD-beta section 3.9 confound 1, re-cited by target audit section 6.7).

**Reviewer discipline**: fresh-session; cold context; read target audit MD end-to-end + companion `scripts/stage_d_rest_adjacency.py` (972 lines) + all 11 output CSVs (spot-checked `headline_strategic_heavy_K3_after.csv`, `omnibus_by_end_class_K3_after.csv`, `crisis_by_end_class_K3_after.csv`, `borderline_by_end_class_K3_after.csv`, `sens_strategic_very_heavy_K3_after.csv`, `abs3k_strategic_heavy_K3_after.csv`, `kladder_strategic_heavy_after.csv`, `restbefore_strategic_heavy_K3.csv`, `wave2c_reproduction_spotcheck.csv`, `preflight_sample_floor.csv`; all reproduce audit-cited numbers byte-for-byte) + MD-beta LOCKED r2 end-to-end + Wave 2C review report as structural template + CONVENTIONS sections cited by the audit from disk. NO edits to target audit, MD-beta, CONVENTIONS, memories, or output CSVs. No stage or commit action taken.
