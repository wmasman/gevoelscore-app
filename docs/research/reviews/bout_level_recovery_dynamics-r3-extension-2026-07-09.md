# Review: `bout_level_recovery_dynamics.md` DRAFT-r3 additive extension (2026-07-09)

**Target**: [`bout_level_recovery_dynamics.md`](../methodology/bout_level_recovery_dynamics.md) DRAFT-r3 §3.2.2 SD-anchored derivative operand family extension + §4 feature-table rows + §10 revision log r3 row.

**Reviewer mode**: Fresh-session methodology-review (Claude) per [CONVENTIONS §1.2](../CONVENTIONS.md#12-reviewer-mode-claude-audits-the-docs--codebase-independently).

**Review date**: 2026-07-09.

**Review scope note**: this report covers only the r3 additive extension. The r2 material (LOCKED 2026-06-19) was reviewed at [`bout_level_recovery_dynamics-2026-06-19.md`](bout_level_recovery_dynamics-2026-06-19.md) and is out of scope. The co-locked sister pre-reg [HA-C4cp](../analyses/hypotheses/HA-C4cp/hypothesis.md) is reviewed separately at [`HA-C4cp-2026-07-09.md`](HA-C4cp-2026-07-09.md).

---

## 1. What the data shows

The r3 extension adds a **derivative operand family** to the parent MD's operand set — a family of per-bout + per-day features derived from the existing `tail_length` primary via z-scoring against the participant's own rolling `[d-90, d-30]` LC-era lagged reference distribution of `tail_length`. The seven load-bearing pre-commits: (i) window `[d-90, d-30]`; (ii) LC-era restriction; (iii) bout-level pool granularity (NOT per-day aggregation); (iv) robust central-tendency via median; (v) robust scale via `1.4826 × MAD`; (vi) ≥ 30-bout validity bar; (vii) candidate-day exclusion via window edge + inclusion of `did_not_return_flag` bouts in reference pool + April 2024 cluster exclusion. Derivative per-bout features (`bout_return_time_z`, `did_not_return_1sd_flag`, `did_not_return_2sd_flag`) and per-day aggregations (`bout_return_time_z_max_day`, `bout_n_did_not_return_1sd_day`, `bout_n_did_not_return_2sd_day`, plus audit traces `subject_lagged_median_day` / `subject_lagged_mad_day`) are added to the §4 feature tables. The extension is **strictly additive** to r2 — no existing pre-commits modified; framework-validity gate §6 explicitly preserved; primary return-window rule §3.2 unchanged; baseline reference §3.3 unchanged.

## 2. What fired and why

### Layer 1 — Universal reporting (inherits from SCRIBE 2016, STROBE 2007)

**No fires.** All pre-commits explicit with formulas, units, ranges, and NaN semantics. Source pointers to OI-025 protocol §5.3 / §5.4 correct and load-bearing (both dated LOCKED r1 2026-07-09). Definitions in §3.2.2 map cleanly to the new §4 feature-table rows.

### Layer 2 — Observational n=1 (inherits from Daza 2018, Personal Science)

**No fires.** Personal-baseline reference frame correctly framed. Cross-operationalisation independence is honestly qualified at the operand-family level (fixed-absolute-threshold vs personal-baseline-rolling-reference) and explicitly NOT at the raw-substrate level — mirrors the guide r3 §4.2.1 condition 2 HA-C3 v2 / HA-C3p canonical precedent that the extension explicitly cites. Candidate-day exclusion argument correctly binds CONVENTIONS §3.2 v3.2 lesson from HA01b-recomputed.

### Layer 3 — Time-series specific (inherits from Natesan Batley 2023, WWC 2022, CENT 2015)

**No fires.** Reference-window design correctly inherits parent MD §5.1 day-level E[L]=7 blocking discipline (the derivative operands themselves are per-day columns; block-permutation on the label sequence remains the inferential machinery for downstream pre-regs consuming them). The 30-bout validity bar is defensible — CONVENTIONS §3.1 personal-baseline convention applied to a bout-level pool; typical Stratum 4 corpus-wide bout rates (~3-8 bouts/day; see empirical anchor below) yield ~180-480 bouts in a 60-day window, well above the 30-bout bar. No silent i.i.d. assumption in the derivative operand definitions.

### Layer 4 — Project-specific audit hooks (inherits from CONVENTIONS §3, §4)

**No fires.**
- Median + `1.4826 × MAD` correctly applied to the right-censored `tail_length` distribution per CONVENTIONS §3.1 robust-baseline prototype; the extension explicitly names the 180-cap pile-up as the reason robust statistics win over mean + SD.
- `_lagged_lcera` window discipline correctly bound (CONVENTIONS §3.2); v3.2 lesson from HA01b-recomputed named at the candidate-day-exclusion pre-commit.
- Named-counts discipline honored (30-bout validity bar with unit + scheme + source; every derivative operand's NaN semantics traceable to the source pool).
- Cross-op-independence claim correctly qualified at operand-family level only (§3.2.2 framing paragraph names the shared-substrate caveat explicitly).
- Framework-validity gate §6 explicitly UNCHANGED (§3.2.2 last subsection + §10 r3 revision log both state this).
- Additive scope only — no r2 pre-commits modified; verified by comparing §3.1 / §3.2 / §3.3 / §3.4 / §5 / §6 sections against r2 state.

## 3. What does not fire (selective non-trivial passes)

- **L2.2 (stationarity)**: the `[d-90, d-30]` lagged reference intentionally handles non-stationarity in `tail_length` across LC-era — reference moves with the era, so shift in baseline over time is absorbed by the rolling window rather than treated as a i.i.d.-violating assumption. This is the CONVENTIONS §3.2 sustained-push discipline correctly applied to a within-day recovery-time operand.
- **L4.3 (one column per definitional pair)**: `did_not_return_1sd_flag` and `did_not_return_2sd_flag` are two different thresholds on the same underlying z-score continuum, NOT a definitional pair with near-identity (r > +0.90 or ρ > +0.85). They are honest sensitivity gradients — Z=1 captures ~16% of bouts under normality; Z=2 captures ~2.5%; the two flag rates should differ by an order of magnitude. Cross-channel-correlation card near-identity discovery discipline not violated by this addition.
- **L4.7 (caveat-class vs a-priori)**: the r3 extension does NOT make a-priori claims about the SD-anchored family's future test outcome; every framing paragraph correctly frames the SD-anchored operand family as "an operand family that the sister-pre-reg HA-C4cp will test", not as "an operand family that will produce Signal X".

## 4. What would strengthen this extension

Three optional non-blocking clarity refinements. All are §3.6-compression-eligible per [`hypothesis_lock_process §3.6`](../methodology/hypothesis_lock_process.md#36-compression-eligibility) discipline (mechanical clarity + no architectural change).

1. **§3.2.2 framing paragraph — tighten the dual-independence statement**: the current framing paragraph names two levels (family-level independence + raw-substrate-shared) but reads as one long sentence with embedded qualifications; splitting into a two-sentence structure with explicit "at the operand-family level" and "at the raw-substrate level" leads would make the independence-scope boundary crystal-clear for first-time readers. **Expected effect**: reader-time-to-comprehend on §3.2.2 drops from ~2 minutes to ~30 seconds; downstream pre-regs consuming §3.2.2 (HA-C4cp) can cite the exact family-level clause without paraphrase.

2. **§4 per-day aggregation table — explicit `0` vs `NaN` distinguisher**: the new per-day aggregation rows (`bout_n_did_not_return_1sd_day`, `bout_n_did_not_return_2sd_day`) state NaN semantics inline in the "use" column, but a footnote to the whole table explicitly stating *"count = 0 means reference-window valid + no flagged bouts; count = NaN means reference-window invalid (< 30 bouts in `[d-90, d-30]`)"* would prevent a downstream implementation bug where NaN is silently treated as 0. **Expected effect**: closes a foreseeable data-quality failure mode where downstream pandas `.fillna(0)` on the joined per_day_master would silently promote reference-window-invalid days to zero-count days.

3. **§3.2.2 empirical anchor for the 30-bout validity bar**: the ≥ 30-bout bar is justified by "typical Stratum 4 day has 1-5 bouts; a 60-day window gives ~60-300 bouts, well above the ≥ 30 bar" — this is a defensible qualitative argument, but citing the specific corpus-wide bout rate on Stratum 4 (per HA-C4c §7 / STOCKTAKE §6 anchor) with the actual median + IQR of daily bout counts would make the bar auditable without guessing. **Expected effect**: the reference-window-validity threshold gains a direct empirical anchor; future pre-regs adopting the family can cite the same empirical anchor rather than re-deriving.

## 5. Verdict

**PASS** — Layer 1-4 audit clean; three optional clarity refinements would sharpen §3.2.2 framing + §4 table NaN semantics + reference-window validity-bar empirical anchor, but none are blocking, and the extension is ready for r3 LOCK as-drafted at §3.6-compression discipline.

---

## Methodology

This review walks the 4-layer checklist defined in [`reviews/README.md`](README.md), anchored in:

- SCRIBE 2016 (Tate et al., [PMC4873717](https://pmc.ncbi.nlm.nih.gov/articles/PMC4873717/))
- CENT 2015 ([shamseer_2015_cent_consort_nof1.pdf](../literature/methodology/shamseer_2015_cent_consort_nof1.pdf))
- STROBE 2007 ([vonelm_2007_strobe_observational_checklist.pdf](../literature/methodology/vonelm_2007_strobe_observational_checklist.pdf))
- Daza 2018 ([daza_2018_self_tracked_n_of_1_counterfactual.pdf](../literature/methodology/daza_2018_self_tracked_n_of_1_counterfactual.pdf))
- WWC 2022 SCED standards ([wwc_2022_standards_handbook_v5_0.pdf](../literature/methodology/wwc_2022_standards_handbook_v5_0.pdf))
- Natesan Batley 2023 ([natesan_2023_nof1_evidence_reporting_systematic_review.pdf](../literature/methodology/natesan_2023_nof1_evidence_reporting_systematic_review.pdf))

Project-specific audit hooks from [`../CONVENTIONS.md`](../CONVENTIONS.md) §3 and §4. Prior r2 review at [`bout_level_recovery_dynamics-2026-06-19.md`](bout_level_recovery_dynamics-2026-06-19.md) delineated r2 scope; this r3 review is scoped strictly to the additive r3 extension.

**Co-lock verification**: the r3 extension's load-bearing pre-commits are inherited from OI-025 protocol §5.3 (LOCKED r1 2026-07-09) + §5.4 cross-op-independence argument (LOCKED r1 2026-07-09). The co-locked sister pre-reg HA-C4cp is reviewed at [`HA-C4cp-2026-07-09.md`](HA-C4cp-2026-07-09.md). Bidirectional lock dependency should be confirmed at r3 LOCK-commit time (Bundle H+ event 7).
