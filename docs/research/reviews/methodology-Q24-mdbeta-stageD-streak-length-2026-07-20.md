# Methodology review: Q24 MD-beta Stage D descriptive audit -- streak-length arc

**Target artefact**: [`analyses/descriptive/Q24-mdbeta-stageD-streak-length/descriptive_audit.md`](../analyses/descriptive/Q24-mdbeta-stageD-streak-length/descriptive_audit.md) DRAFT r1 2026-07-19 (producer-mode Stage D descriptive audit per [CONVENTIONS section 1.2](../CONVENTIONS.md#12-reviewer-mode-claude-reads--writes-a-reasoned-report--recommendations); drafted by producer-mode subagent under user delegation).

**Target commit**: uncommitted DRAFT r1 (working tree state 2026-07-19; script `scripts/stage_d_streak_length.py` at 1004 lines + 12 output CSVs + `episode_table.csv` at OUTPUT_DIR).

**Reviewer**: fresh-session Claude (Opus 4.7) under user delegation. Cold context. Read target audit MD end-to-end + companion `scripts/stage_d_streak_length.py` (1004 lines) + all 12 output CSVs + MD-beta LOCKED r2 2026-07-17 (sections 1 to 6.9 + confounds 2 / 3 / 5 / 6 / 7 + section 4.1-4.7 streak-length arc) + reviews README 4-layer spec + sibling Wave 2C rest-adjacency arc review report as structural template + CONVENTIONS sections cited by the audit from disk. No exposure to drafting-session context.

**Review type**: reviewer-mode per [CONVENTIONS section 1.2](../CONVENTIONS.md#12-reviewer-mode-claude-reads--writes-a-reasoned-report--recommendations); 4-layer checklist walk per [`reviews/README.md`](README.md), adapted for a producer-mode Stage D descriptive audit rather than a reviewer-mode hypothesis-result artefact. Verdict per this doc's section 5.

**Discipline**: NO edits to target audit, MD-beta LOCKED r2, CONVENTIONS, memories, or output CSVs. All recommendations go in section 4. No em-dash. No emoji. No stage or commit action taken.

---

## 1. What the data shows

Empirical claims made by the target audit, plain restate (interpretive framing separated in section 2). All numbers cross-verified against `output/*.csv` byte-for-byte.

1. **Baseline reproduction anchor 1 (audit section 1.2)**. MD-beta section 6.2 streak distribution on 314 gap=0 heavy episodes: L=1 n=188 (59.87%), L=2 n=77 (24.52%), L=3 n=27 (8.60%), L=4+ n=22 (7.01%). Sub-bin breakdown within 4+: L=4 n=12, L=5 n=6, L=6/7/8/10 n=1 each. Reproduces MD-beta 6.2 byte-for-byte. Verified against `output/md_beta_6_2_streak_distribution.csv`.

2. **Baseline reproduction anchor 2 (audit section 1.3)**. MD-beta section 6.3 streak x intensity fingerprint: mean vh_frac 0.436 / 0.481 / 0.519 / 0.538 across L in {1, 2, 3, 4+}; mean vh_count 0.436 / 0.961 / 1.556 / 2.636. Median vh_frac 0.000 / 0.500 / 0.667 / 0.550. Reproduces MD-beta 6.3 byte-for-byte to three decimals. Verified against `output/md_beta_6_3_streak_intensity.csv`.

3. **Baseline reproduction anchor 3 (audit section 1.4)**. MD-beta section 6.4 streak x era cross-tab: 2022 n=44 (26/11/2/5), 2023 n=87 (59/20/5/3), 2024 n=81 (50/23/4/4), 2025 n=66 (37/14/9/6), 2026 partial n=36 (16/9/7/4); total 314 (188/77/27/22). Reproduces MD-beta 6.4 exactly. Verified against `output/md_beta_6_4_streak_era.csv`.

4. **Baseline reproduction anchor 4 (audit section 1.1 + 3)**. Crash-in-5d rate on the 314-episode pool: 46/314 = 14.65%. Corpus baseline (LC-era): 103/1524 = 6.8%. Ratio approximately 2x baseline, consistent with MD-beta section 6.7 anchor. Verified against `output/per_bin_crash_rate.csv` era=ALL rows (pool_k_this_era = 46; pool_rate_this_era = 0.1465).

5. **Headline cell (audit section 3.1, `output/per_bin_crash_rate.csv`)**. Per-bin crash rate era-pooled: L=1 28/188 = 14.89% (Wilson 10.51 to 20.68); L=2 10/77 = 12.99% (Wilson 7.21 to 22.28); L=3 5/27 = 18.52% (Wilson 8.18 to 36.70); L=4+ 3/22 = 13.64% (Wilson 4.75 to 33.33). All four bins pass the informal Wilson-viable floor of n = 10 exposed.

6. **Per-bin RR versus L=1 reference (audit section 3.1 companion, `output/per_bin_rr_vs_L1.csv`)**. L=2 RR = 0.872 (bootstrap 95% CI 0.376 to 1.628); L=3 RR = 1.243 (CI 0.303 to 2.611); L=4+ RR = 0.916 (CI 0.000 to 2.229). All three non-reference bootstrap CIs include 1.0.

7. **Cochran-Armitage era-pooled (audit section 3.2, `output/cochran_armitage_trend.csv`)**. n=314; n_crashes=46; row_scores [1,2,3,4]; Z_asymptotic = 0.025; p_asymptotic two-sided = 0.9804; p_permutation two-sided (B=10000, block=1, seed=20260716) = 0.9675. Null Z quantiles: 2.5% = -1.9069, median = 0.0246, 97.5% = 1.9561.

8. **Era-stratified per-bin (audit section 4.1 + 4.2)**. Pre-cital (2022-04-04 to 2024-04-08) n=156, 29 crashes, pool rate 18.59%: L=1 19/100 (19.00%, Wilson 12.51-27.78, pass); L=2 6/39 (15.38%, Wilson 7.25-29.73, pass); L=3 3/8 (37.50%, Wilson 13.68-69.43, FAIL narrative-only); L=4+ 1/9 (11.11%, Wilson 1.99-43.50, FAIL narrative-only). Post-cital (2024-04-09 to 2026-06-05) n=158, 17 crashes, pool rate 10.76%: L=1 9/88 (10.23%); L=2 4/38 (10.53%); L=3 2/19 (10.53%); L=4+ 2/13 (15.38%). All four post-cital cells pass floor.

9. **Cochran-Armitage era-stratified (audit section 4.3)**. Pre-cital Z = -0.060, p_asymptotic = 0.9522, p_permutation = 1.0000. Post-cital Z = 0.4325, p_asymptotic = 0.6654, p_permutation = 0.6934. Signs opposite; both far from conventional thresholds.

10. **Intensity-stratified (audit section 5.2 + 5.3, `output/intensity_stratified.csv`)**. Low vh_frac subset (<= 0.5), n=186 total, 31 crashes: L=1 21/106 = 19.81% (Wilson 13.34-28.40); L=2 7/56 = 12.50% (Wilson 6.19-23.63); L=3 2/13 = 15.38% (Wilson 4.33-42.23); L=4+ 1/11 = 9.09% (Wilson 1.62-37.74). Cochran-Armitage Z = -1.189, p = 0.234 (sign inverted). High vh_frac subset (> 0.5), n=128 total, 15 crashes: L=1 7/82 = 8.54%; L=2 3/21 = 14.29%; L=3 3/14 = 21.43%; L=4+ 2/11 = 18.18%. Cochran-Armitage Z = 1.508, p = 0.131 (sign matches pre-commit). All eight intensity cells pass floor at n >= 10.

11. **E[L]* diagnostic (audit section 6.1 + 6.2, `output/el_star_diagnostic.csv`)**. Day-level streak_length on LC-era stratum: n=1524 days; mean 0.873; max 10; zero-fraction 65.1%; lag-1 rho = 0.6641. Politis-White-style estimator: E[L]* = 7.802. Factor vs locked block length = 1: 7.80x. FLAG triggered (>= 2x locked).

12. **Streak-clustering probe (audit section 6.3, `output/el_star_4plus_pair_details.csv`)**. 22 L=4+ episodes total; 8 pairs within 30d rolling window. Clusters: 2022-07-20 / 07-28 / 08-03 (3 episodes in 14d); 2025-06-07 / 06-12 / 06-21 (3 episodes in 14d); 2025-08-08 to 08-29 (21d apart); 2026-03-12 to 04-10 (29d apart).

13. **E[L]*-block-length sensitivity companion (audit section 6.5, `output/per_bin_boot_at_el_star.csv`)**. Stationary bootstrap with expected block length = 8, B=10000, seed=20260716: L=1 CI 9.04-20.74%; L=2 CI 6.49-20.78%; L=3 CI 3.70-33.33%; L=4+ CI 4.55-22.73%. Comparison to primary block=1 CIs preserves the non-monotonic descriptive pattern; no verdict inversion under block-length change.

14. **Preflight sample-floor probe (audit section 1.5, `output/preflight_sample_floor.csv`)**. 20 cells: 12 era-pooled + era-stratified (10 pass, 2 fail: pre-cital L=3 n=8, pre-cital L=4+ n=9) + 8 intensity-stratified (all pass). Failing cells reported narrative-only per user Option B endorsement.

15. **Discipline attestations (audit section 8)**. Descriptive-before-inference, personal baseline, named-count, NaN-boundary, caveat-class, descriptive-before-theory (no `resilience_latent_state.md` citation; no latent-state / R(t) / reserve / buffer / envelope-capacity constructs), 6-mechanism era caveat verbatim, circularity with parent Q24 MD, rolling-window autocorrelation flag with HA-P7 section 4.6 closure template, Wilson-viable floor, multiple-testing surface disclosure, no em-dash, no emoji all attested.

---

## 2. What fired and why

Layer-grouped fires with citation, magnitude, and absorb-vs-escalate signal per fire.

### Layer 1 -- Universal reporting (SCRIBE 2016; STROBE 2007)

**L1.1 Pre-registration of the operand contract -- PASSES with high confidence.** The audit executes precisely what MD-beta r2 sections 4.1 + 4.2 + 4.3 + 4.4 + 4.5 + 4.6 + 4.7 pre-committed for the streak-length arc: `streak_length(D_end) = |{contiguous heavy days ending at D_end}|` at gap=0 unit-of-analysis; L_bin in {1, 2, 3, 4+}; outcome `crash_in_5d`; per-bin Wilson 95% CI + Cochran-Armitage trend + bootstrap 95% CI B=10000 block=1 seed=20260716 + permutation null on Cochran-Armitage. No silent operand redefinition detected. Section 1.2 verifies the MD-beta 6.2 anchor byte-for-byte (188/77/27/22); section 1.3 verifies 6.3 (mean vh_frac 0.436/0.481/0.519/0.538); section 1.4 verifies 6.4 (cross-tab exactly); section 1.1 verifies 6.7 (46/314 = 14.65%). **Absorb**: none needed.

**L1.2 Named operationalisation with computation path -- PASSES with high confidence.** Every operand is defined in section 2 or in each subsection preamble with column name (`exertion_class_lagged_lcera` filter to `{heavy, very_heavy}`; `is_crash` day-level column; `crash_in_5d` derived indicator), the row-filter (`lc_phase == 'lc'`, `crash_window_full == True`), and source CSV path. Script `stage_d_streak_length.py` is idempotent, well-commented, 1004 lines, and every cell reproducible via `main()`. **Absorb**: none needed.

**L1.3 Statistical method named with parameters -- PASSES.** Section 2 + section 3.2 list Wilson `proportion_confint(method='wilson')` at alpha=0.05; Cochran-Armitage manual per Armitage 1955 with row_scores [1,2,3,4]; two-sided asymptotic p via `scipy.stats.norm`; permutation null on Cochran-Armitage Z with B=10000 block=1 seed=20260716; bootstrap 95% CI B=10000 block=1; stationary bootstrap for E[L]*-block-length sensitivity with expected block = 8 via Politis-Romano geometric-mean-block sampling with wrap-around. Verified against script lines 200 to 850. **Absorb**: none needed.

**L1.4 Confounders enumerated not silently controlled -- PASSES.** Section 4.5 reproduces the 6-mechanism era caveat verbatim (citalopram, learned-pacing, tactical-Garmin-use, natural LC trajectory, envelope drift with the 19.39 vs 5.17 anchor from MD-alpha Wave 2A section 8, aging + seasonality). Section 8 lists all five MD-beta section 5 confounds (2, 3, 5, 6, 7) as caveats, not corrections. No post-hoc adjustment attempted. **Absorb**: none needed.

**L1.5 Limitations separate from headline -- PASSES.** Section 3.3 explicitly enumerates five candidate explanations for the flat pattern (genuine flat, sample-floor sparsity, intensity confounding, era instability, rolling-window autocorrelation) and marks all as descriptive-open per CONVENTIONS section 2.1. Section 4.1 marks failing cells narrative-only per Wilson-computable-but-withheld policy. Section 5.4 explicitly notes wide CIs on tightest cells and marks intensity-stratified reads as exploratory descriptive companions, not primary. **Absorb**: none needed.

**L1.6 Null-Z quantiles reported at section 3.2 do not match CSV values -- SUBSTANTIVE (absorb-tier fix).** Section 3.2 states null Z quantiles "2.5% = -1.919, median = 0.001, 97.5% = 1.986". The CSV `cochran_armitage_trend.csv` row `cochran_armitage_era_ALL` shows null_Z_lo_2p5 = -1.9069, null_Z_median = 0.0246, null_Z_hi_97p5 = 1.9561. The median discrepancy is the load-bearing one: 0.001 vs 0.0246. The interpretive claim ("Z = 0.025 sits essentially at the null-median (0.001)") is qualitatively correct because both values are near zero, but the specific null-median value in the text does not match the CSV. This looks like a transcription residue from an earlier bootstrap run or a rounding artefact (0.001 may be a truncation of a different intermediate) rather than a substantive numerical error. **Absorb-tier recommendation**: correct section 3.2 to state "2.5% = -1.907, median = 0.025, 97.5% = 1.956" per the emitted CSV; drop the "essentially at the null-median (0.001)" comparison and replace with a comparison to the observed Z = 0.025 which is exactly the null-median rounded to three decimals. Not a numerical revision of any downstream finding; a transcription clean-up.

**L1.7 Discipline attestation coverage vs actual practice -- PASSES.** Section 8 asserts "no latent-state / R(t) / reserve / buffer / envelope-capacity constructs anywhere". Spot-check confirms compliance; the audit uses only descriptive-with-CI language and the cumulative-load framing cited from MD-beta section 4.4 is explicitly labelled as descriptive dose-response reading only, without appeal to any latent-capacity mechanism. Section 8 attestation bullet is honoured. **Absorb**: none needed.

### Layer 2 -- Observational n=1 (Daza 2018; Personal Science norms)

**L2.1 Counterfactual framing at subject-level -- PASSES.** Section 3 primary contrast compares per-bin crash rates on L_bin subsets of the same 314-episode heavy-end pool. Section 3.3 uses "does not support" and "descriptive-open" rather than "confirms" or "falsifies". Section 4.4 uses "compatible with a flat dose-response within each era". Section 5.4 uses "descriptively consistent with" and "does NOT resolve into a clean streak-length dose-response either". No between-subject comparison implied. **Absorb**: none needed.

**L2.2 Stationarity acknowledged -- PASSES with high confidence.** Section 4.3 documents opposite Cochran-Armitage signs across the era boundary (pre-cital Z = -0.06 vs post-cital Z = +0.43) plus substantial pool-baseline shift (pre-cital 18.6% vs post-cital 10.8%). Section 4.5 reproduces the 6-mechanism era caveat verbatim. Section 7.3 restates the era instability at findings-summary level. This is exactly the stationarity-surfacing the MD-beta r2 sections 3.5 + 5 confound 3 + 7 revision requires. **Absorb**: none needed.

**L2.3 Calendar-time vs subject-time separation -- PASSES.** The pre-cital / post-cital boundary at 2024-04-09 is calendar-anchored per section 2 and section 4.1 + 4.2 header ranges. Section 4.5 uses "temporal anchor" language rather than any phase-mechanism claim. Episode unit is D_end calendar date; no subject-time confusion. **Absorb**: none needed.

**L2.4 Data provenance traceable -- PASSES.** Section 2 lists script path + input path (`$GEVOELSCORE_DATA_PATH/unified/per_day_master.csv`) + dump version (v3.2) + random seed + statistical machinery per operand + NaN handling + era stratifier + unit of analysis + L_bin ordinal encoding. Script `load_lc_stratum()` at lines 97 to 119 anchors the pipeline including a contiguity check on the LC-era date sequence. Every CSV writes with `.to_csv(...)`. **Absorb**: none needed.

**L2.5 Held-out structure per `project_garmin_research_bias_boundary` -- PASSES.** The audit reads across 2022 to 2026-06-05 including the 2026 pre-dump extraction window. Streak-length is derived from `exertion_class_lagged_lcera`, which is Garmin-derived and was a tactical input pre-dump; consistent with the memory. No fire on the bias-boundary. **Absorb**: none needed.

**L2.6 Prior motivation named -- PASSES.** Sections 3, 4, 5, 6 each preamble cite MD-beta anchor sections (4.1, 4.2, 4.3, 4.4, 4.5, 4.6, 4.7 + 5 confounds 2, 3, 5, 6, 7 + 6.2, 6.3, 6.4, 6.7). Nothing surfaced without explicit MD-beta anchor. **Absorb**: none needed.

### Layer 3 -- Time-series specific (Natesan 2023; WWC 2022; CENT 2015)

**L3.1 Autocorrelation addressed -- PASSES with high confidence, SUBSTANTIVE-LOAD-BEARING PASS.** This is the load-bearing item for the streak-length arc per the review brief. The audit walks all three steps of the HA-P7 section 4.6 closure template pre-committed at MD-beta section 4.7:

- Step (a) cite the structural clustering: audit section 6.3 emits 8 pairs of L=4+ within 30d, concentrated in 3-4 tight windows (July-August 2022, June 2025, August 2025, March-April 2026). Explicitly named as "the specific clustering behaviour the MD-beta section 4.7 anticipatory-drafting note flagged as a review trigger".
- Step (b) recompute per-bin bootstrap at E[L]*-block-length: audit section 6.5 reports the stationary-bootstrap CI at E[L]*=8 with a comparison table to the primary block=1 CIs. E[L]* = 7.80 rounded to nearest integer = 8; stationary bootstrap via Politis-Romano geometric-mean-block with wrap-around (script lines 764 to 785); episode-level D_end-ordered index array.
- Step (c) verify verdict robustness across block-length arms: audit section 6.5 explicit closure statement: "the non-monotonic per-bin pattern surfaced at section 3.1 (L=1 14.9%, L=2 13.0%, L=3 18.5%, L=4+ 13.6%) is preserved under the E[L]*-block-length sensitivity companion; the block-length flag does NOT change the descriptive pattern or the section 3.3 read that the era-pooled per-bin crash rate does not show the MD-beta section 4.4 pre-commit monotonic dose-response direction. Per HA-P7 section 4.6 closure template step (c), verdict robustness across block-length arms is confirmed at the descriptive-with-CI level."

The audit correctly distinguishes the day-level lag-1 autocorrelation of 0.6641 (structural: consecutive days in the same episode share streak_length identity by construction) from the episode-end unit-of-analysis (which already deflects most of the concern per MD-beta section 4.7 rationale). The E[L]* = 7.80 tripping the factor-of-2 flag is documented but framed correctly as "a foreseen review trigger, not a hard override" per MD-beta section 4.7. This is a model of how to handle a pre-committed review trigger. **Absorb**: none needed; positive precedent for the HA-P7 section 4.6 template application to a Stage D descriptive audit.

**L3.2 Lag-carryover -- N/A at Stage D descriptive scope.** Outcome is a binary crash-in-5d occurrence; lag-carryover machinery not applicable. **Absorb**: none needed.

**L3.3 Multiple testing across cells -- PASSES with high confidence.** Section 8 attestation bullet 10 explicitly enumerates 20 per-bin cells + 8 intensity-stratified cells + 4 E[L]*-block-length sensitivity cells + 3 Cochran-Armitage Z + 2 intensity-stratum Cochran-Armitage Z; states that the largest p is 0.9804 and the smallest is 0.131 (intensity-stratified high-vh-frac Z=1.51); attests that no single p crosses to a verdict at Stage D and descriptive-with-CI is the primary evidential surface. This is exactly the multiple-testing surface disclosure the sibling audit review absorbed at recommendation 4; the streak-length audit already includes it upfront. **Absorb**: none needed; positive precedent.

**L3.4 Permutation null block length documented -- PASSES.** Block length = 1 documented in section 2 + section 8 attestation + script line 300 comment. Consistent with MD-beta section 4.5 primary + parent Q24 MD section 7.10 (episode-end unit-of-analysis argument). The audit further documents the block=8 sensitivity companion at section 6.5 with rationale explicit. **Absorb**: none needed.

**L3.5 Trend vs level claim separation -- PASSES with high confidence.** Section 3.1 reports per-bin rates + Wilson CIs (level axis); section 3.2 reports Cochran-Armitage Z + two-sided p + permutation null (trend axis). Section 3.3 correctly separates the two: per-bin rates are "non-monotonic" (level) and the Cochran-Armitage Z "sits essentially at the null-median" (trend). Neither is conflated. Section 7.1 restates trend-vs-level separation explicitly at findings-summary level. Note that at Cochran-Armitage p_asymptotic = 0.9804 the interpretive risk is real (a fresh reader could read "trend test null" as a verdict); the audit avoids this by consistently labelling as "descriptive-only per CONVENTIONS section 2.1". **Absorb**: none needed.

### Layer 4 -- Project-specific audit hooks (CONVENTIONS sections 3-4 + memories)

**L4.1 Personal baseline per CONVENTIONS section 3.1 -- PASSES.** Streak length is a structural count on the LC-era stratum; no threshold-based operand; no personal-baseline concern. Section 8 attestation explicit. Wilson CIs use standard normal-approximation-corrected form. **Absorb**: none needed.

**L4.2 Lagged variant per CONVENTIONS section 3.5 -- PASSES.** Script line 105 uses `exertion_class_lagged_lcera` for the heavy-day definition, consistent with MD-beta section 2.2 inheritance from parent Q24 MD. Verified at script + reproduced counts (188/77/27/22). **Absorb**: none needed.

**L4.3 One column per definitional pair per CONVENTIONS section 3.3 -- PASSES.** Streak-length is a single ordinal operand, not a definitional pair. The intensity-stratified companion at section 5 uses vh_frac cutoff 0.5 (low vs high) as a per-episode intensity fingerprint stratifier; this is not a definitional-pair concern because vh_frac is a derived within-episode summary of the same underlying `exertion_class_lagged_lcera` column used to build the streak. No hidden definitional pair. **Absorb**: none needed.

**L4.4 Crash-drop sensitivity per CONVENTIONS section 3.4 -- N/A.** The outcome IS crash occurrence at binary crash-in-5d; not applicable at Stage D on binary outcome. **Absorb**: none needed.

**L4.5 Spike-detecting metric per CONVENTIONS section 3.5 -- PASSES.** Streak_length is a per-episode structural count, operationalised as episode-length not daily-average. Section 8 attestation bullet 2 explicit. `end_class` at episode-end is a spike metric, not a daily-average. No silent daily-average slippage detected. **Absorb**: none needed.

**L4.6 Counts named with scheme + unit + source per CONVENTIONS section 3.6 -- PASSES with high confidence.** Section 1.1 corpus counts each carry scheme + unit + source (e.g. "Heavy days (heavy + very_heavy) | 532 (34.9%) | parent Stage -1 section 1"; "gap=0 heavy episodes | 314 | script + parent Stage -1 section 4"; "Corpus baseline crash rate (LC-era) | 103 / 1524 = 6.8% | MD-beta section 6.7"). Every table cites its source CSV path in the section preamble. Section 8 named-count discipline attestation explicit. **Absorb**: none needed.

**L4.7 Caveat-class vs a-priori-class framing -- PASSES with high confidence, SUBSTANTIVE-LOAD-BEARING PASS.** Per the review brief, the non-monotonic pattern (14.9 / 13.0 / 18.5 / 13.6) does NOT support the MD-beta section 4.4 pre-commit direction (longer streaks -> HIGHER crash rate). The audit consistently uses "does not support that pre-commit direction at descriptive-with-CI resolution" (section 3.3) and "descriptively non-monotonic" (section 7.1), never "falsifies", "rejects", or "refutes". Section 3.3 explicitly enumerates five candidate explanations for the flat pattern (genuine flat, sample-floor sparsity, intensity confounding, era instability, rolling-window autocorrelation) and marks all as "descriptive-open at Stage D; no verdict is emitted here per CONVENTIONS section 2.1". This is exactly the discipline CONVENTIONS section 4.2 caveat-class framing requires; the audit stays within it consistently across sections 3, 4, 5, 6, 7. **Absorb**: none needed; positive precedent for how to frame a pre-commit-non-supporting pattern at Stage D without leaking into inferential-verdict language.

**L4.8 Prior-driven hypothesis framing (Stage D producer-mode) -- PASSES.** Section 3.3 explicit: "this is a substantive descriptive finding: the era-pooled per-bin crash rate does not show the predicted dose-response". Section 7.1 restates: "the pre-commit direction is not confirmed by this Stage D descriptive audit; whether the flat pattern is genuine or reflects sample-floor sparsity, intensity confounding, era instability, or rolling-window autocorrelation inflating effective sample size is descriptive-open". No "validates" / "confirms" / "falsifies" / "rejects". **Absorb**: none needed.

**L4.9 Descriptive-before-theory per user 2026-07-17 directive -- PASSES with high confidence.** No citation of `resilience_latent_state.md`. No latent-state / R(t) / reserve / buffer / envelope-capacity constructs. The cumulative-load framing at section 3 / section 7 is cited as descriptive dose-response reading only. Section 8 attestation explicit. **Absorb**: none needed.

**L4.10 Physical-rest-only semantic constraint per memory `project_rest_day_operand_semantics` -- N/A for streak-length arc.** No `_physical_` operand invoked; no gevoelscore-conditioning; correctly N/A per review brief. **Absorb**: none needed.

**L4.11 6-mechanism era caveat verbatim per MD-beta section 5 confound 7 -- PASSES with high confidence.** Section 4.5 lists the six mechanisms verbatim in MD-beta's order (citalopram, learned-pacing, tactical-Garmin-use, natural LC trajectory, envelope drift with the 19.39 vs 5.17 min/day envelope-drift anchor from MD-alpha Wave 2A section 8 preserved, aging + seasonality). Closes with "The stratifier does NOT identify medication effect at n=1... No causal claim about medication is made or supported by this stratifier." Faithful reproduction. **Absorb**: none needed.

**L4.12 NaN-handling consistency per CONVENTIONS section 3.10 -- PASSES.** Section 2 documents `is_crash` NaN propagates as False via `.fillna(False)` (script line 107); no other operand-side NaN semantics load-bearing for streak_length because streak_length is a structural count on the heavy-vs-not-heavy indicator, not an operand with NaN semantics. Episodes with truncated crash-window (`crash_window_full == False`) are excluded from every per-bin cell (script line 472). Section 8 attestation explicit. **Absorb**: none needed.

**L4.13 Circularity with parent Q24 MD per MD-beta section 5 confound 6 -- PASSES.** Section 3.3 closing paragraph + section 7.5 explicitly flag the shared 314-episode crash-in-5d outcome sample with the parent Q24 MD Stage D r4 audit and forbid Stage S1 double-invocation: "Any Stage S1 synthesis must pick ONE of {this MD, parent Q24 MD} as headline per Q24 sub-part and cite the other as complementary; the two Stage D findings are NOT independent evidence at the Stage S1 level." Section 7.5 further reconciles the audit's 46/314 = 14.65% all-episodes pool rate with the parent MD's 9/52 = 17.3% strict-clean +5d rate as descriptively coexisting without duplicating the descriptive surface. Section 8 attestation explicit. **Absorb**: none needed; positive precedent.

**L4.14 Sample-floor discipline -- PASSES with high confidence.** Section 1.5 explicitly names the informal Wilson-viable floor as n >= 10 exposed per user Option B endorsement. Section 4.1 reports the two failing cells (L=3 pre-cital n=8; L=4+ pre-cital n=9) with the Wilson bounds written to the CSV for reproducibility trace but the audit body treating them as narrative-only per the sibling audit section 6.5 Wilson-computable-but-withheld policy. Explicit restraint statement: "The Wilson CI (13.7%, 69.4%) is mathematically computable but is deliberately not treated as an evidential surface at this floor per the sibling audit section 6.5 Wilson-computable-but-withheld policy. The script writes the Wilson bounds to the output CSV for reproducibility trace; the audit body treats the cell as narrative-only per user Option B endorsement." Section 8 attestation explicit. **Absorb**: none needed; positive precedent.

**L4.15 E[L]* flag handling -- PASSES with high confidence, SUBSTANTIVE-LOAD-BEARING PASS.** See L3.1 above for the full walk. All three HA-P7 section 4.6 template steps executed: (a) structural clustering cited at section 6.3 with 8 L=4+ pairs enumerated + tight-window clusters named; (b) E[L]*-block-length stationary bootstrap sensitivity companion computed at section 6.5 via Politis-Romano geometric-mean-block sampling with wrap-around, comparison table to primary block=1 CIs included; (c) verdict robustness across block-length arms confirmed with explicit closure statement. Framing note at section 6.5 explicitly cites the 1.61x effective-independent-episode ratio (E[L]* * n_episodes / n_days_lc_stratum = 7.80 * 314 / 1524) as a companion diagnostic, not a correction pre-committed at Stage D, preserving the unit-of-analysis argument. Sample-viability at L=4+ arm (n=22) is smaller than block-length (8), which is an inherent artefact for that specific arm; section 6.5 acknowledges "this is a small-sample artefact where the stationary-bootstrap block length is comparable to the arm-size 22". Model treatment of the load-bearing pre-committed review trigger. **Absorb**: none needed; positive precedent.

**L4.16 Intensity-stratified sign-inversion framing -- PASSES.** Section 5.4 correctly frames the low-vh-frac Z = -1.19 vs high-vh-frac Z = +1.51 pattern as "directionally-opposite pattern by intensity stratum" and "descriptively consistent with intensity being the load-bearing signal, not streak length in the era-pooled contrast at section 3". Explicitly cites MD-beta section 5 confound 2 for the streak-length x intensity confound reading and states "the flat era-pooled Cochran-Armitage Z = 0.025 is at least partially explained by the intensity-stratum sign cancellation". Section 5.4 also notes the L=1 crash rate reversal between intensity strata (low-vh-frac L=1 19.8% vs high-vh-frac L=1 8.5%; at L=4+ the ordering reverses to high-vh-frac 18.2% vs low-vh-frac 9.1%) and reads it as "the intensity signal on crash rate is bin-dependent; this is a substantive descriptive finding on the intensity confound but does NOT resolve into a clean streak-length dose-response either". Section 7.4 restates at findings-summary level. Sample-viability caveat at n=11 (L=4+ both strata) and n=13 (L=3 low-vh-frac) is surfaced explicitly. This is the substantive descriptive finding of the audit alongside the era-pooled flat pattern per the review brief and the audit itself identifies it as such at section 7.2. **Absorb**: none needed.

**L4.17 Null Z quantiles transcription discrepancy at section 3.2 -- SUBSTANTIVE PARTIAL FIRE (absorb-tier).** See L1.6 above. Section 3.2 text states "null Z quantiles (permutation): 2.5% = -1.919, median = 0.001, 97.5% = 1.986"; CSV emits -1.9069 / 0.0246 / 1.9561. The median-value discrepancy (0.001 vs 0.0246) is the load-bearing one; the interpretive claim "Z = 0.025 sits essentially at the null-median (0.001)" is qualitatively correct but the specific null-median value is wrong. **Absorb-tier recommendation** (single-place text patch): correct section 3.2 to match the CSV values -1.907 / 0.025 / 1.956; drop the "essentially at the null-median (0.001)" parenthetical and replace with "Z_observed = 0.025 is exactly at the null-median (rounded to three decimals)". This is a transcription cleanup, not a numerical revision; no downstream finding depends on the null-median value.

---

## 3. What does not fire (selective)

Non-trivial passes worth stating positively:

- **HA-P7 section 4.6 closure template walk on the E[L]* flag**. This is the substantive load-bearing item for the streak-length arc per MD-beta section 4.7 anticipatory-drafting-note discipline. The audit walks all three steps of the template explicitly, computes the sensitivity companion at E[L]*=8 via Politis-Romano stationary bootstrap with wrap-around continuation, emits a comparison table to the primary block=1 CIs, and states verdict robustness across block-length arms in a single closure sentence. Any Stage D reader can trace the flag response end-to-end.

- **Non-monotonic pattern framing discipline**. The section 3.1 per-bin rates (14.9 / 13.0 / 18.5 / 13.6) do NOT support the MD-beta section 4.4 pre-commit direction. The audit resists two failure modes: (a) inferential-verdict language like "falsifies" or "rejects" the pre-commit; (b) burying the non-support in caveat-language that obscures it. Section 3.3 says clearly "does not support that pre-commit direction at descriptive-with-CI resolution" and enumerates five candidate explanations without adjudicating any as primary. Section 7.1 restates at findings-summary level. This is exactly the caveat-class-not-a-priori-class discipline CONVENTIONS section 4.2 requires for a pre-commit-non-supporting pattern.

- **Circularity-with-parent-MD flag placed at three touchpoints**. Section 3.3 closing paragraph cites the shared 314-episode pool with parent Q24 MD Stage D r4 audit and forbids Stage S1 double-invocation. Section 7.5 restates at findings-summary level with the additional reconciliation of the audit's 46/314 = 14.65% pool rate against the parent MD's 9/52 = 17.3% strict-clean +5d rate. Section 8 attestation explicit. Fresh Stage S1 reader has no path to double-invoke the two Stage D findings as independent evidence.

- **Multiple-testing surface disclosure upfront**. Section 8 attestation bullet 10 explicitly enumerates 20 per-bin cells + 8 intensity-stratified cells + 4 E[L]*-block-length sensitivity cells + 3 Cochran-Armitage Z + 2 intensity-stratum Cochran-Armitage Z; states the largest and smallest p; attests no verdict at Stage D. This is exactly the discipline the sibling audit review absorbed at recommendation 4; the streak-length audit ships it in r1.

- **6-mechanism era caveat verbatim reproduction**. Section 4.5 lists all six mechanisms in the MD-beta order with the 19.39 vs 5.17 min/day envelope-drift anchor from MD-alpha Wave 2A section 8 preserved. Closes with the "does NOT identify medication effect at n=1" attestation.

- **Preflight sample-floor probe emitted as its own CSV**. `output/preflight_sample_floor.csv` is a 20-row surface that lets a downstream consumer verify the floor logic per cell without recomputing anything. Two failing cells (L=3 pre-cital n=8; L=4+ pre-cital n=9) are named verbatim in section 1.5 and treated narrative-only at section 4.1.

- **Byte-for-byte MD-beta anchor reproduction across four independent anchors**. Sections 1.2, 1.3, 1.4, plus the derived 46/314 = 14.65% baseline at section 1.1, all reproduce MD-beta sections 6.2, 6.3, 6.4, 6.7 to the last digit. This is the single most important reproducibility check a Stage D descriptive audit can make; the streak-length audit provides four anchors, not one.

- **Descriptive-before-theory compliance**. No citation of `resilience_latent_state.md`, no reserve / buffer / envelope-capacity language, no latent-state constructs. The cumulative-load framing at section 3 is cited from MD-beta section 4.4 as descriptive dose-response reading only.

---

## 4. What would strengthen this finding

Concrete + named. Each recommendation states expected effect.

### 4.1 (Absorb) Correct null Z quantile values at section 3.2

**Recommendation**: at section 3.2, replace the parenthetical "null Z quantiles (permutation): 2.5% = -1.919, median = 0.001, 97.5% = 1.986" with the CSV-emitted values "-1.907, 0.025, 1.956". Replace the trailing sentence "Z = 0.025 sits essentially at the null-median (0.001)" with "Z_observed = 0.025 is exactly at the null-median rounded to three decimals". No downstream finding depends on the null-median value; this is a transcription cleanup.

**Rationale**: The CSV `cochran_armitage_trend.csv` row `cochran_armitage_era_ALL` emits null_Z_lo_2p5 = -1.9069, null_Z_median = 0.0246, null_Z_hi_97p5 = 1.9561. The audit body reports different values. The interpretive claim is qualitatively preserved but the specific numbers do not match the emitted CSV; a fresh reader spot-checking against the CSV would flag the discrepancy.

**Expected effect**: hardens the reproducibility gate at the specific cell where the audit body diverges from the emitted CSV. Preserves the CSV-and-body byte-for-byte match discipline the audit otherwise enforces at four independent MD-beta anchors.

### 4.2 (Absorb, discretionary) Cross-reference the intensity-stratified Cochran-Armitage p-values at section 5.4

**Recommendation**: at section 5.4, add a one-line explicit statement that the low-vh-frac p = 0.234 and high-vh-frac p = 0.131 are both above conventional thresholds and are reported descriptively per CONVENTIONS section 2.1 (mirroring the section 3.2 discipline at the era-pooled cell). Section 8 attestation bullet 10 already covers this globally, but section 5.4 body does not restate at the intensity-stratified cells.

**Rationale**: The intensity-stratified Z values (-1.19 low, +1.51 high) look like they might read inferentially at first glance because they are the highest-magnitude Cochran-Armitage Z in the audit and they are the most substantively-interesting finding per section 7.2. Section 8 covers the discipline globally; a one-line restatement at section 5.4 would prevent a Stage S1 reader from picking up the Z = -1.19 or Z = +1.51 as an inferential verdict without noticing the descriptive-only framing.

**Expected effect**: hardens the descriptive-before-inference gate at the substantive intensity-stratified cell where the temptation to over-read a two-sided p-value is real (Z = 1.51 is the largest |Z| in the audit at 1.5-standard-deviations from null).

### 4.3 (Absorb, discretionary) Sample-viability caveat at the L=4+ arm for the E[L]*-block-length sensitivity companion

**Recommendation**: at section 6.5, extend the existing "small-sample artefact where the stationary-bootstrap block length is comparable to the arm-size 22" note to also flag the L=3 arm (n=27) and to be explicit that at both L=3 and L=4+ the E[L]*=8 stationary-bootstrap CI is a companion diagnostic rather than a strict correction. The current note names only L=4+ but the same artefact applies to L=3 (n=27, arm-to-block ratio 3.4x, marginal for stationary bootstrap).

**Rationale**: The E[L]*=8 stationary-bootstrap sensitivity is a foreseen review trigger response per HA-P7 section 4.6 template, but the sensitivity itself has smaller-sample artefacts on the two tightest bins. The audit acknowledges this on L=4+ but not on L=3. A fresh reader could take the L=3 sensitivity CI (3.70 to 33.33%) at face value without noticing that the block-length is comparable to the arm-size.

**Expected effect**: hardens the sensitivity-companion caveat at the exact cells where the block-length choice is marginal. Not a numerical revision; a caveat-strengthening.

### 4.4 (Absorb, discretionary) Explicit label of the deferred-parent-MD complementarity at section 7.5

**Recommendation**: at section 7.5, add a one-line pointer that the parent Q24 MD Stage D r4 audit at `analyses/descriptive/Q24-post-heavy-trajectory/descriptive_audit.md` LOCKED r4 is the sibling artefact on the shared 314-episode pool; explicitly name the sibling audit file so a Stage S1 reader can navigate to the complementary reading without re-deriving the pointer from MD-beta section 5 confound 6. The current section 7.5 cites the parent MD by name but does not link the specific Stage D r4 file.

**Rationale**: Section 3.3 closing paragraph and section 8 attestation cover the shared-sample flag; section 7.5 restates at findings-summary level. A single link at section 7.5 to the sibling Stage D r4 audit file makes the "pick ONE as headline per Q24 sub-part" instruction actionable without a MD-beta lookup.

**Expected effect**: hardens the circularity flag at the findings-summary level. Not a numerical revision; a navigation-aid tightening.

---

## 5. Verdict

**DEFENSIBLE with revision.**

The Stage D descriptive audit r1 correctly operationalises the MD-beta r2 LOCKED streak-length arc pre-commit contract (sections 4.1 to 4.7 + section 5 confounds 2, 3, 5, 6, 7), reproduces the section 6.2 / 6.3 / 6.4 / 6.7 baseline anchors byte-for-byte across four independent surfaces, executes the per-bin Wilson 95% CI + Cochran-Armitage trend + bootstrap 95% CI + permutation null per section 4.5 statistical machinery, correctly frames the non-monotonic era-pooled pattern (14.9 / 13.0 / 18.5 / 13.6) as "does not support the section 4.4 pre-commit direction at descriptive-with-CI resolution" without leaking into "falsifies" / "rejects" language, walks the HA-P7 section 4.6 closure template on the E[L]* = 7.80 factor-of-2 flag through all three steps (cite structural clustering + recompute at E[L]*=8 stationary bootstrap + verify verdict robustness), surfaces the intensity-stratified sign-inversion (low vh_frac Z = -1.19 vs high vh_frac Z = +1.51) as the substantive descriptive finding consistent with MD-beta section 5 confound 2 (streak-length x intensity), reproduces the 6-mechanism era caveat verbatim at section 4.5 with the MD-alpha Wave 2A envelope-drift anchor preserved, flags the shared-314-episode pool with parent Q24 MD at three touchpoints (sections 3.3, 7.5, 8) with explicit Stage-S1-single-headline instruction, reports the sample-floor failures at pre-cital L=3 and L=4+ narrative-only per sibling audit Wilson-computable-but-withheld policy, and enumerates the 20 + 8 + 4 + 3 + 2 = 37-cell multiple-testing surface upfront at section 8. Four absorb-tier recommendations: (4.1) correct null Z quantile transcription discrepancy at section 3.2 to match `cochran_armitage_trend.csv` values; (4.2) restate descriptive-only framing at section 5.4 intensity-stratified cells; (4.3) extend section 6.5 small-sample-artefact caveat to also cover L=3 arm; (4.4) name the sibling parent-MD Stage D r4 audit file explicitly at section 7.5. No BLOCKING issue found; the audit is safe to lock at r1 with the section 4 absorb-tier patches applied inline per producer-mode compression discipline. No architectural revision required.

---

## Methodology footer

This review walks the 4-layer checklist defined in [`reviews/README.md`](README.md), which inherits from:

- **Layer 1**: SCRIBE 2016 items 3 to 5, 14, 18, 22 to 24 (Tate et al., PMC4873717); STROBE 2007 items 6, 12, 13.
- **Layer 2**: Daza 2018 self-tracked n-of-1 counterfactual; Personal Science norms; project memory `project_garmin_research_bias_boundary` for held-out-structure framing.
- **Layer 3**: Natesan Batley et al. 2023 systematic review; WWC 2022 SCED handbook v5.0; CENT 2015 (Shamseer et al.). Applied at Stage D descriptive scope to bootstrap block-length + multiple-testing surface + trend-vs-level separation + HA-P7 section 4.6 closure template.
- **Layer 4**: [CONVENTIONS.md](../CONVENTIONS.md) sections 2.1 (descriptive-before-inference), 3.1 (personal baseline, N/A for structural count), 3.3 (definitional pair, N/A for single-ordinal operand), 3.4 (crash-drop sensitivity, N/A at binary outcome), 3.5 (spike-detecting metrics), 3.6 (named counts), 3.10 (NaN-boundary rule), 4.2 (caveat-class framing); memories `project_garmin_research_bias_boundary` (held-out-structure), user 2026-07-17 descriptive-before-theory directive.

Cochran-Armitage anchor: Armitage 1955 (standard biostatistical practice for ordinal-exposure x binary-outcome trend). Politis-Romano stationary bootstrap: Politis & Romano 1994 (Journal of the American Statistical Association).

**Reviewer discipline**: fresh-session; cold context; read target audit MD end-to-end + companion `scripts/stage_d_streak_length.py` (1004 lines) + all 12 output CSVs (spot-checked `per_bin_crash_rate.csv`, `cochran_armitage_trend.csv`, `md_beta_6_2_streak_distribution.csv`, `md_beta_6_3_streak_intensity.csv`, `md_beta_6_4_streak_era.csv`, `intensity_stratified.csv`, `el_star_diagnostic.csv`, `el_star_4plus_pair_details.csv`, `preflight_sample_floor.csv`, `per_bin_rr_vs_L1.csv`, `per_bin_boot_at_el_star.csv`; all reproduce audit-cited numbers byte-for-byte except the section 3.2 null-Z-quantiles discrepancy flagged at L1.6 + L4.17) + MD-beta LOCKED r2 sections 1 through 6.9 + section 5 confounds 2, 3, 5, 6, 7 + section 4.1 through 4.7 streak-length arc + sibling Wave 2C rest-adjacency arc review report as structural template + CONVENTIONS sections cited by the audit from disk. NO edits to target audit, MD-beta, CONVENTIONS, memories, or output CSVs. No stage or commit action taken.
