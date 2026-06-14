# Review v2: wiggers_testable_hypotheses.md (wiggers-testable-hypotheses)

**Target**: [../wiggers_testable_hypotheses.md](../wiggers_testable_hypotheses.md)
**Target commit**: `5577492` (2026-06-12 — last committed state)
**Working-tree state**: `M docs/research/wiggers_testable_hypotheses.md` — uncommitted session edits 2026-06-13 (priority shortlist rewrite + two constraint-#3 syncs to MD 3). Review walks the on-disk state including these edits; HEAD short hash `7c81555`.
**Reviewer mode**: Claude (independent peer reviewer per [CONVENTIONS §1.2](../CONVENTIONS.md))
**Review date**: 2026-06-13
**Relationship to prior review**: independent re-walk against the same checklist as the earlier
[wiggers_testable_hypotheses-2026-06-13.md](wiggers_testable_hypotheses-2026-06-13.md) (v1). Where the two reports concur on substantive items, the concurrence is itself informative (two independent walks land on the same fire). Where they diverge (v1 catches things v2 misses, v2 catches things v1 misses, or the readings differ in magnitude) it is called out explicitly in § 6 below.

---

## 1. What the data shows

The target is a **register / pre-registration draft**, not a results doc. It catalogues 39 Wiggers-derived hypotheses (A1–A4, B1–B5, C1–C4, D1–D5, E1–E3, F1–F4, G1–G4, H1–H5, I1–I3), each with a predicted direction and a `per_day_master.csv`-resolved test method. The summary table (§ "what survives, what doesn't") claims:

- **23 testable** (✅) on the current 161-column master,
- **11 partial** (⚠️) via the `stress_mean_sleep` HRV-proxy (5 B-block + 5 H-block) plus G3 (external KNMI data),
- **2 blocked** (❌) — F3 (Garmin sleep score skipped per user) and G2 (skin-temperature sensor absent on FR245).

Interpretive moves carried by the doc beyond the catalogue:

- A **priority shortlist** (rewritten 2026-06-13) using a verification × descriptive-evidence intersection rule: Tier 1 = B1, C3, A1, C4; Tier 2 = A4, H5; Tier 3 = G3, H1, H4; Out = the rest.
- A cross-ref to [`personal_hypotheses.md`](../personal_hypotheses.md) as a parallel register with a different validation discipline (descriptive, prior-driven, no held-out required).
- **Two pre-reg-file constraint blocks** (lines 246 and 344) both updated this session to point at the MD 3 single-pool validation framework with the "number not narrative" wording.
- A **Source verification log** with verbatim Wiggers passages for 6 of the 23 testable hypotheses (A1, A4, C3, C4, H1, H5).

The interpretive framing the doc itself names: "this is a register; per-hypothesis parameters live in the eventual pre-reg files in `analyses/hypotheses/`". Empirical claims (effect sizes, p-values) live in the methodology MDs and the HA-numbered result files this register cross-refs, not in the register itself.

---

## 2. What fired and why

### Layer 1 — Universal reporting (inherits from SCRIBE 2016, STROBE 2007)

**L1.6 — [CONVENTIONS §3] analysis frame named per hypothesis — *minor***
- The Validation-framework note at the head of the priority shortlist (line 144) and the constraint #3 in both blocks (lines 250, 351–357) name **Stratum 4 (LC with gevoelscore + crash labels)** as the primary frame. The default is therefore stated globally.
- But per-hypothesis Pre-reg-draft entries (§ "Pre-registration draft — variable mapping") do not consistently name the frame inline. A1 names "long-covid era only (lc_phase == 'lc')" (line 218), but C1–C4, D1–D5, E1–E3, F1–F4 do not.
- *Why it matters*: SCRIBE 2016 item 14 and STROBE 2007 item 12 require the analysis frame stated alongside the test method, not separately at the top of the doc. A reader who finds C3 by ID-search may not see the frame before they extract the row into a pre-reg.

### Layer 2 — Observational n=1 (inherits from Daza 2018, Personal Science)

**L2.1 — [Daza 2018, CONVENTIONS §5] counterfactual framing not explicit — *substantive***
- The register operationally implements within-subject counterfactual reasoning ("Deviation = value minus your own rolling personal baseline", line 13) but never states the framing in Daza's terms.
- *Why it matters*: Daza 2018 ([daza_2018_self_tracked_n_of_1_counterfactual.pdf](../literature/methodology/daza_2018_self_tracked_n_of_1_counterfactual.pdf)) is the only published framework directly aimed at observational self-tracked n=1 time-series, and the counterfactual ("on day d at exposure X, comparison is to subject-baseline at exposure ~X, not to a population") needs to be stated so that downstream readers can evaluate whether the comparison is well-defined. Implicit framing works when the analyst is also the subject; it travels less well when the doc itself becomes a public-facing reference (which this register is — the response cycle with the advisor cites it back).
- *Concurs with v1 §2 Layer 2.*

**L2.5 — [CONVENTIONS §5; memory `project_garmin_research_bias_boundary`] held-out structure framing inherited transitively — *substantive at the inheritance level, minor at the register level***
- Both constraint-#3 blocks (lines 250 and 351–357) were updated this session to the MD 3 single-pool primary + "number not narrative" wording. The text does not regress to "user has been continuously analysing the data".
- But: the register does not surface the **tactical-vs-analytical Garmin-use distinction** that motivates *why* "a number, not a narrative" is the right framing. The distinction lives in the new memory `project_garmin_research_bias_boundary` and in the parent MD 3 §4.4 (which was tightened in this session). A reader of the register alone gets the rule without the reasoning.
- The deeper issue v1 surfaces (the parent MD's lines 92–93 — *"user has been looking at post-2023-12-31 data continuously since it accrued"*) was actually corrected in this session per the user's correction; the corrected MD 3 §4.4 now uses the tactical-vs-analytical distinction explicitly. The register inherits the corrected framing through the cross-ref.
- *Magnitude*: substantive that the register doesn't surface the reasoning inline; minor that the corrected framing exists transitively. *Partial divergence from v1*: v1 reads the parent MD as still using the superseded framing; the corrected framing landed in this session and is now in place.

**L2.6 — [CONVENTIONS §4.3] prior-driven framing partially anchored — *substantive***
- Confirmatory framing rests on the Wiggers handleiding being the prior. The Source verification log anchors 6 of 23 testable hypotheses (A1, A4, C3, C4, H1, H5) to verbatim Wiggers passages with PDF line numbers.
- **17 of 23 testable hypotheses are not yet source-verified**: A2, A3, B1–B5, C1, C2, D1–D5, E1–E3, F1, F2, F4, G1, G3, G4, H2, H3, H4. The handover lists verification-log expansion as queued / optional, and the register's preamble line 8 frames the handleiding as "lotgenoten observations and n-of-1 generalisations" rather than confirmed facts.
- *Magnitude*: substantive at the meta level (the register's "Wiggers-derived" framing is partial); not blocking — each individual entry stands on the testable-against-`per_day_master` operationalisation.
- *Why it matters*: Natesan Batley 2023 finds prior-claim drift (paraphrase that doesn't match source) is one of the dominant Layer 1 reporting failure modes. The Source verification log is the right structural answer; until the 17 are checked, the register cannot claim the full confirmatory framing.
- *v1 did not catch this directly.*

**L2.3 — [Daza 2018] calendar-time vs subject-time separation — *minor***
- Every lag in the register is calendar-time (`t-1`, `t-3`, etc.). Subject-time anchors (days since LC onset, days since device-baseline learned) exist as data-given strata in MD 1 but are not propagated into per-hypothesis lag definitions.
- Stratum-4-as-default is partly a subject-time anchor (the start date is the gevoelscore corpus start); per-hypothesis lags within Stratum 4 use calendar-time without acknowledgement that subject-time might give different lag profiles for the device-baseline-suspect first 21 days (which I1 handles separately at the sensitivity layer).
- *Why it matters*: Daza 2018 frames n=1 self-tracked data as requiring both conditioning axes; the register addresses calendar-time explicitly and subject-time implicitly via I1.

### Layer 3 — Time-series specific (inherits from Natesan Batley 2023, WWC 2022, CENT 2015)

**L3.3 — [CONVENTIONS §2.2, multiplicity layer ambiguity] — *minor***
- The Validation-framework note (line 144) cites "Holm step-down on N_eff ≈ 4 per [chained-regime doc] § Cross-cutting statistical hygiene" as the multiplicity correction for "all tiers". N_eff ≈ 4 was derived in [cross-channel-correlation.md](../analyses/garmin_exploration/cards/cross-channel-correlation.md) for the **channel** family (7 primitives → ~4 effective independent channels), not the **hypothesis** family (23 testable hypotheses).
- The chained-regime doc § Cross-cutting §3 distinguishes channel-level multiplicity (where N_eff ≈ 4 applies) from hypothesis-level multiplicity (where the broader Bonferroni / Holm framework applies). The register's inline phrasing conflates the two.
- *Magnitude*: minor — the cross-ref is correct; the inline phrasing is loose. One disambiguating sentence would fix it.
- *Why it matters*: Natesan Batley 2023 finds 65.8% of n=1 medical studies fail distributional assumptions, often via mis-applied multiplicity corrections at the wrong family level.
- *v1 did not flag this.*

### Layer 4 — Project-specific audit hooks (inherits from CONVENTIONS §3, §4)

**L4.2 — [CONVENTIONS §3.2] `_lagged_lcera` default mis-applied in top-level Column choice table — *substantive (blocking-adjacent)***
- The Column choice table at lines 17–38 lists `_lagged` (non-lcera) variants for PEM hypotheses: `exertion_rank_composite_lagged`, `exertion_class_lagged`, `step_rank_lagged`, `eff_exertion_rank_lagged`, `max_hr_rank_lagged`, `vigorous_min_rank_lagged`, `push_burden_7d_lagged`.
- This contradicts the doc's own pre-reg-draft default stated at lines 210–212: *"exertion proxy defaults to `exertion_class_lagged_lcera` (PEM) or `exertion_rank_composite_lagged_lcera` (continuous)"*. The per-hypothesis Pre-reg-draft entries (lines 218–308) then correctly use `_lagged_lcera` everywhere (A1, A4, B4, C4, D5, H1, H2, H4, H5).
- *Quote* (line 22): *"Threshold 'did too much' for overexertion stratification (B4, D5, H2, H4) | `exertion_class_lagged` in `{heavy, very_heavy}`"* — should read `exertion_class_lagged_lcera`.
- *Magnitude*: substantive. CONVENTIONS §3.2 names this as an explicit pre-flight audit hook because the failure mode is silent — the analysis runs cleanly, the baseline-creep distortion is invisible at the output level, and the result reads as if it tested PEM-pacing on the LC frame when it actually tested it on a baseline diluted by pre-LC and corona days.
- *Concurs with v1 §2 Layer 4.*

**L4.4 — [CONVENTIONS §3.4] crash-drop sensitivity row not cross-cutting in the constraint blocks — *substantive***
- The register's "Statistical hygiene" preamble (lines 44–50) names multiple-comparisons, autocorrelation, RTM, acute-illness vs PEM, device-baseline lag — but **not §3.4 (crash-drop sensitivity row)**.
- The two pre-reg-file constraint blocks (lines 246–253 and 344–367) list 6 explicit B-block constraints but don't include crash-drop sensitivity.
- The only inline mention of crash-distortion sensitivity is in the G3 (Tier 3) row at line 166, citing `[[feedback_crash_distortion_sensitivity]]`.
- But CONVENTIONS §3.4 says crash-drop sensitivity is required for **every** Layer 4+ correlation / CCF / regression that touches PEM-pacing variables — that includes A1 (Jonckheere-Terpstra dose-response on `resting_hr` × `exertion_rank_composite_lagged_lcera` quartiles), C3 (stress → fatigue spline), H5 (CCF lag-profile), B1 (single-day proxy spike → crash at t+1).
- *Quote* (CONVENTIONS §3.4): *"On crash days the exertion-HR co-movement is suppressed or reversed (typically low exertion at the time of the crash with elevated RHR), which dampens the underlying 'more push → higher resting_hr' signal on the full frame. |Δ| > 0.10 = surface as a finding."*
- *Magnitude*: substantive. A1's Jonckheere-Terpstra is exactly the test §3.4 was added to safeguard.
- *Concurs with v1 §2 Layer 4.*

**L4.3 — [CONVENTIONS §3.3] near-identical pair handling at the column-choice-table level — *possible substantive; needs DATA_DICTIONARY verification***
- v1 reports the A4 row at line 37 lists both members of a ρ = 1.000 pair. CONVENTIONS §3.3 names the A4 pair specifically as *"`hr_area_above_daytime_baseline_waking_lcera` over `hr_min_above_daytime_baseline_plus_20_waking_lcera`"*.
- Reading the line 37 carefully: the columns listed are `hr_sustained_elevated_flag`, `hr_longest_elevated_run_min_waking`, `hr_area_above_daytime_baseline_waking`, plus transparency cols `hr_median_waking` + `hr_daytime_baseline_lagged`.
- The named §3.3 pair is `hr_area_*` + `hr_min_*`. The line 37 has `hr_area_*` but NOT `hr_min_*`; instead it has `hr_longest_elevated_run_min_waking`, which is a *different column* (longest contiguous run in minutes vs total minutes above threshold).
- *Without consulting DATA_DICTIONARY to confirm whether `hr_longest_elevated_run_min_waking` is itself near-identical to either `hr_area_*` or `hr_min_*` on this corpus, I cannot confidently fire L4.3 on the same grounds v1 did.*
- *Magnitude*: possible substantive; needs DATA_DICTIONARY check to confirm or rule out. If `hr_longest_elevated_run_min_waking` is a distinct construct (duration of one contiguous run vs total minutes vs magnitude × duration), the L4.3 fire dissolves.
- *Diverges from v1*: v1 fires L4.3 confidently; v2 cannot confirm without a DATA_DICTIONARY column-name check. Suggest the user verify against DATA_DICTIONARY before acting on the L4.3 finding.

**L4.1 — [CONVENTIONS §3.1] C3 uses absolute bin edges on `all_day_stress_avg` — *minor framing concern***
- C3 (line 261, verification log lines 410–420) is tested via binned mean comparison at 0–20, 20–30, 30–40, 40–60, 60+. These are absolute cutoffs on the Garmin stress score, not deviations from a personal rolling baseline.
- Defensible because Garmin stress is itself a Firstbeat-algorithm-normalised 0–100 value, and the 30/40 step is Wiggers' own UI anchor (PDF lines 1357–1368, verbatim). CONVENTIONS §4.3 supports inheriting source-anchored framing when the prior is independent.
- The verification log (line 420) says "the bin edges are OUR choice, not Wiggers'" — partial honesty but doesn't address §3.1.
- *Magnitude*: minor framing — operationalisation is defensible; the framing-against-§3.1 isn't called out.
- *v1 did not flag this.*

**L4.6 — [CONVENTIONS §3.6] some counts named with scheme/source, some bare — *minor***
- Strong: line 199 (1755 rows × 161 cols, source named); line 333 (23 hypotheses on the 161-column master).
- Weak: the Summary table uses bare totals (23 testable / 11 partial / 2 blocked) without naming the underlying scheme. "29 crash episodes" implicit in methodology cross-refs is not always qualified as `crash_v2`.
- *Magnitude*: minor — internally consistent (one scheme throughout); §3.6 asks for scheme + unit + source per count so it survives extraction.
- *Concurs with v1 §2 L4.6 (date/commit anchor for the column counts).*

### Cross-block consistency

**5 vs 6 pre-reg-file constraints — register vs chained-regime doc — *minor***
- The register has **6** pre-reg-file constraints in both constraint blocks. The chained-regime doc § "Five pre-reg-file constraints inherited" lists **5** with identical items 1–5; the register's item 6 ("No literal HRV claim") is a sub-aspect the chained-regime version implicitly folds into item 1.
- *Magnitude*: minor — items 1–5 align; item 6 is a sub-clarification.
- *Why it matters*: both docs are authoritative for downstream pre-regs. A pre-reg author who reads the chained-regime version may write a pre-reg silent on item 6.

### Side observation (not a Layer fire)

**Cohen's d = +0.90 with CI95 [+1.51, +8.22] — CI does not bracket the point estimate — *factual / labelling concern***
- Line 229 reads *"episode-level Cohen's d = +0.90 (CI95 [+1.51, +8.22])"*. The CI95 of a Cohen's d cannot bracket +1.51 to +8.22 when the point estimate is +0.90 — that's mathematically impossible.
- Likely the CI is for the underlying mean stress-unit difference (Garmin stress 0–100), not for the standardised effect size, OR the d value is wrong, OR the labels are swapped.
- The same number appears at lines 233 and 348 (constraint #2 "descriptive effect-size anchor"), and propagates into power-planning citations.
- *Why it matters*: B-block pre-reg power planning anchors on this number. If the label is wrong, the power calculation will be wrong.
- *Concurs with v1 §2 side observation.* Worth verifying against [`../methodology/hrv_proxy_via_stress.md`](../methodology/hrv_proxy_via_stress.md) §7 and the raw run output at [`../analyses/garmin_exploration/hrv_proxy_validation/result-table.txt`](../analyses/garmin_exploration/hrv_proxy_validation/result-table.txt) before the number propagates further.

---

## 3. What does not fire (selective)

**L3.1 — autocorrelation addressed via documented machinery.** Hygiene preamble line 47 names block bootstrap; constraint #3 in both blocks cites [`methodology/permutation_null_block_length.md`](../methodology/permutation_null_block_length.md), which specifies stationary bootstrap E[L] = 7 days with data-driven companion + pre-registered override rule. The 83.8% n=1-medical-study failure mode flagged by Natesan Batley 2023 is explicitly avoided.

**L4.7 — caveat-class kept, a-priori-class cut.** Line 13 keeps the seasonality + device-changes caveat. No a-priori-class trajectory or stabilisation framing reintroduced after the 2026-06-13 cleanup. The Validation-framework note (line 144) is the chosen-path output of MD 3, not an a-priori commitment.

**L4.5 — spike-detecting metrics for acute-load hypotheses.** A4 uses `hr_sustained_elevated_flag` + `hr_longest_elevated_run_min_waking`; C1/C4 use `stress_post_peak_time_to_rest_min` + `stress_high_duration_min`; B1 uses spike threshold on `stress_mean_sleep` (not nightly mean). CONVENTIONS §3.5 holds.

**L4.8 — prior-driven framed as confirmatory; exploratory caveat preserved for the un-source-verified entries.** The doc explicitly separates Wiggers-sourced hypotheses (need source verification + descriptive evidence before pre-reg) from personally-derived priors (parallel register `personal_hypotheses.md`). This is the right architectural split per CONVENTIONS §4.3.

**Source verification log structure.** Each verified hypothesis (A1, A4, C3, C4, H1, H5) is grounded in verbatim PDF-line quotes with explicit DROPPED / KEPT / EXPANDED annotations and explicit drift call-outs. H1 in particular carefully softens the doc's claim relative to Wiggers' explicit predictive claim ("Wiggers-faithful proxy channel" vs "Wiggers-extension channels"). This makes the verified-subset of the doc auditable independent of any project-internal context.

---

## 4. What would strengthen this finding

1. **Update the top-level Column choice table to default to `_lagged_lcera` for LC-frame tests** (addresses L4.2). Replace `exertion_rank_composite_lagged` → `exertion_rank_composite_lagged_lcera` and `exertion_class_lagged` → `exertion_class_lagged_lcera` in the rows for A1, H1, H3, H5, B4, D5, H2, H4. Keep the non-lcera variant available as a fallback for cross-era trajectory work (per CONVENTIONS §3.2 second paragraph) but make it the non-default. Expected effect: pre-reg authors who consult the top-level table will pick the LC-era-only baseline by default, eliminating the silent baseline-dilution failure mode.

2. **Add §3.4 (crash-drop sensitivity row) to the Statistical hygiene preamble AND as item 7 in both pre-reg-file constraint blocks** (addresses L4.4). One bullet between the autocorrelation and RTM items in the preamble + a 7th item in the constraint blocks: *"Crash-drop sensitivity row: per CONVENTIONS §3.4, every Layer 4+ correlation / CCF / regression reports the result with `is_crash==True` rows dropped; |Δ ρ| > 0.10 surfaced as a finding."* Expected effect: A1's Jonckheere-Terpstra dose-response and H5's CCF get the sensitivity row by construction, not by per-pre-reg memory.

3. **Verify the d = +0.90 / CI95 [+1.51, +8.22] reading** before B-block pre-regs ship (side observation). The CI doesn't bracket the point estimate. If the CI is for the underlying mean stress-unit difference, label it as such (e.g. "Cohen's d = +0.90; mean stress-unit difference 4.87, CI95 [+1.51, +8.22]"). Cross-check against the raw run output at [`../analyses/garmin_exploration/hrv_proxy_validation/result-table.txt`](../analyses/garmin_exploration/hrv_proxy_validation/result-table.txt). Expected effect: B-block power planning anchors on a correctly-labelled effect size.

4. **Expand the Source verification log to cover the remaining 17 testable hypotheses** (addresses L2.6). Order by tier: Tier 2 (A4 — already done; H5 — already done) first, then Tier 3 (G3, H1, H4 — H1 already done; H4 needs work), then Out-of-priority. Each entry follows the existing template: Wiggers passages with PDF line refs, KEPT / DROPPED / EXPANDED findings, drift call-outs. Expected effect: lifts the confirmatory framing from "partial (6/23)" to "full (23/23)" and forecloses paraphrase-drift fires on un-verified entries.

5. **Surface the tactical-vs-analytical Garmin-use distinction in the held-out-structure paragraph** (addresses L2.5). Add to the constraint #3 wording: *"... pre-2026 validate eras are held out from analytical eyes in the strict research sense (no cross-day aggregated analysis until the 2026 GDPR dump) although they were lived through and tactically Garmin-paced; see [`../methodology/train_validate_split_fate.md`](../methodology/train_validate_split_fate.md) §4.4 and memory `project_garmin_research_bias_boundary`."* Expected effect: a reader new to the project understands *why* "a number, not a narrative" is the right framing without having to cross-ref the methodology MD.

6. **Make the Daza 2018 counterfactual framing explicit** (addresses L2.1). One sentence under "How to read this" stating: *"All tests below are within-subject counterfactual comparisons against the participant's own rolling baseline, not against a population. The framework is Daza 2018 ([daza_2018_self_tracked_n_of_1_counterfactual.pdf](../literature/methodology/daza_2018_self_tracked_n_of_1_counterfactual.pdf))."* Expected effect: doc becomes defensible to an outside reader (e.g. Wiggers in a response cycle) without referencing project-internal context.

7. **Verify L4.3 (near-identical pair handling) against DATA_DICTIONARY**. The A4 row at line 37 lists `hr_longest_elevated_run_min_waking` (longest contiguous run in minutes), `hr_area_above_daytime_baseline_waking` (bpm·min). CONVENTIONS §3.3 names the §3.3-relevant pair for A4 as `hr_area_*` + `hr_min_*`. Confirm whether `hr_longest_elevated_run_min_waking` is itself near-identical (ρ ≥ 0.97) to either of the others on the LC frame. If yes, drop one per §3.3. If no, the L4.3 fire dissolves. Expected effect: either the table is cleaned up, or the false-alarm is documented as ruled out.

8. **Disambiguate the Holm-on-N_eff cite in the Validation-framework note** (addresses L3.3). One sentence: *"Multiplicity correction at the **channel** family level is Holm step-down on N_eff ≈ 4 per [chained-regime doc] § Cross-cutting §3; hypothesis-family multiplicity follows the broader Bonferroni / Holm framework specified there."* Expected effect: prevents pre-reg authors from applying the channel-level threshold (α / 4) to a hypothesis-level family.

9. **Inline analysis frame per-hypothesis in Pre-reg-draft entries** (addresses L1.6). A one-line frame stamp per row (e.g. "Frame: Stratum 4, lc_phase == 'lc'"). Expected effect: when an entry is copied into its eventual `analyses/hypotheses/HA*-*/hypothesis.md`, the frame travels with it.

10. **Acknowledge C3's absolute-bin choice against CONVENTIONS §3.1 in the verification log** (addresses L4.1). One sentence in the C3 entry: *"Bin edges 0–20 / 20–30 / 30–40 / 40–60 / 60+ are absolute on Garmin's normalised stress score; this deviates from CONVENTIONS §3.1 personal-baseline default, justified by inheriting Wiggers' own 30/40 UI anchor (PDF lines 1357–1368, verbatim) and by the Garmin stress score being itself a Firstbeat-algorithm-normalised 0–100 value."* Expected effect: defensible exception flagged, not silently absorbed.

11. **Normalise the 6-vs-5 constraint count between register and chained-regime doc**. Either add "No literal HRV claim" as item 6 to the chained-regime doc's constraint list, or fold the register's item 6 into item 1 (Explicit proxy framing). Expected effect: downstream pre-regs cannot satisfy one set without satisfying the other.

---

## 5. Verdict

**REVISION RECOMMENDED** — multiple substantive Layer 4 fires (L4.2 top-level `_lagged` vs `_lagged_lcera` mismatch; L4.4 crash-drop sensitivity not cross-cutting) compound with substantive Layer 2 fires (L2.1 Daza counterfactual not explicit; L2.6 17 of 23 hypotheses unverified against source) to make the register's framing layer thinner than its operationalisation layer; the operationalisations themselves are sound, but the framing should land before Tier 1 pre-regs (B1, C3, A1, C4) ship to `analyses/hypotheses/`.

The highest-priority single concern is **L4.2** — the top-level Column choice table directs PEM-frame work to non-lcera variants while the per-hypothesis specs lower in the same doc correctly use `_lagged_lcera`. A pre-reg author who works from the table risks silent baseline dilution.

---

## 6. Comparison with v1

Per-finding table comparing this review (v2) with [wiggers_testable_hypotheses-2026-06-13.md](wiggers_testable_hypotheses-2026-06-13.md) (v1):

| finding | v1 verdict | v2 verdict | notes |
|---|---|---|---|
| L1.3 (test method coarse for low-tier hypotheses) | minor | not fired | v2 reads the precision-by-tier as principled deferral to the pre-reg layer; v1 calls it inconsistency |
| L1.6 (analysis frame per-hypothesis) | not flagged | minor | v2-only finding |
| L2.1 (Daza counterfactual) | substantive | substantive | concurrent |
| L2.2 (stationarity) | minor | not flagged separately (covered under L3.1) | v1 surfaces; v2 absorbs into L3.1 |
| L2.3 (calendar vs subject time) | not flagged | minor | v2-only finding |
| L2.5 (held-out structure framing inheritance) | substantive (v1 reads parent MD as still wrong) | substantive at inheritance level; minor at register level (v2 reads parent MD as corrected this session) | partial divergence — v2 has seen the corrected MD 3 §4.4 from this session that v1 had not |
| L2.6 (17 of 23 unverified) | not flagged | substantive | v2-only finding |
| L3.1 (autocorrelation) | passes | passes | concurrent |
| L3.3 (multiplicity framing — channel vs hypothesis family) | not flagged | minor | v2-only finding |
| L4.2 (`_lagged` vs `_lagged_lcera` column-choice-table) | substantive | substantive | concurrent — independent walks land on the same fire |
| L4.3 (A4 ρ=1.000 pair) | substantive | possible — needs DATA_DICTIONARY check | partial divergence — v1 fires confidently; v2 cannot confirm without a column-name match check (the line 37 list has `hr_longest_elevated_run_min_waking`, not `hr_min_above_daytime_baseline_plus_20_waking` named in §3.3) |
| L4.4 (crash-drop sensitivity cross-cutting) | substantive | substantive | concurrent |
| L4.5 (spike-detecting; C1 mean vs duration framing) | minor | passes overall, with the C1 nuance worth flagging in the C1 pre-reg | partial — v1 calls the C1 framing a minor fire; v2 reads it as defensible at register level but worth noting at pre-reg-formalisation |
| L4.6 (counts framing + date/commit anchor) | minor | minor | concurrent |
| L4.7 (caveat- vs a-priori) | passes | passes | concurrent |
| L4.8 (prior-driven framing) | passes | passes | concurrent |
| 5 vs 6 constraint count register vs chained-regime | not flagged | minor cross-block | v2-only finding |
| Side: Cohen's d = +0.90 / CI95 [+1.51, +8.22] inconsistency | flagged | flagged | concurrent — same factual concern |
| Verdict | REVISION RECOMMENDED | REVISION RECOMMENDED | concurrent |

Net: two independent walks converge on REVISION RECOMMENDED with the same top concerns (L4.2 column-choice table; L4.4 crash-drop sensitivity not cross-cutting; L2.1 Daza counterfactual; the Cohen's d CI inconsistency). v1 adds the L4.3 fire that v2 cannot confirm without a DATA_DICTIONARY column-name check (recommended as item 7 in v2 § 4). v2 adds L1.6, L2.3, L2.6, L3.3, the cross-block constraint-count item, and reads the L2.5 inheritance as substantive-at-the-inheritance-level but minor-at-the-register-level because the parent MD 3 §4.4 was corrected in this session (which v1 had not seen).

The convergence on REVISION RECOMMENDED from two independent walks is itself evidence the verdict is right.

---

## Methodology

This review walks the 4-layer checklist defined in
[reviews/README.md](README.md), anchored in:

- SCRIBE 2016 (Tate et al., [PMC4873717](https://pmc.ncbi.nlm.nih.gov/articles/PMC4873717/))
- CENT 2015 ([shamseer_2015_cent_consort_nof1.pdf](../literature/methodology/shamseer_2015_cent_consort_nof1.pdf))
- STROBE 2007 ([vonelm_2007_strobe_observational_checklist.pdf](../literature/methodology/vonelm_2007_strobe_observational_checklist.pdf))
- Daza 2018 ([daza_2018_self_tracked_n_of_1_counterfactual.pdf](../literature/methodology/daza_2018_self_tracked_n_of_1_counterfactual.pdf))
- WWC 2022 SCED standards ([wwc_2022_standards_handbook_v5_0.pdf](../literature/methodology/wwc_2022_standards_handbook_v5_0.pdf))
- Natesan Batley 2023 ([natesan_2023_nof1_evidence_reporting_systematic_review.pdf](../literature/methodology/natesan_2023_nof1_evidence_reporting_systematic_review.pdf))

Project-specific audit hooks from
[../CONVENTIONS.md](../CONVENTIONS.md) §3 and §4.
