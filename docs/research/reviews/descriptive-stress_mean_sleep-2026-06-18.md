# Review: `stress_mean_sleep` operationalisation-support descriptive analysis

**Target**: [docs/research/analyses/descriptive/operationalisation_support/stress_mean_sleep/](../analyses/descriptive/operationalisation_support/stress_mean_sleep/) (folder: README.md + run.py + findings.md + summary.json + 5 plots)
**Target commit**: working-tree only — entire folder uncommitted (untracked) as of 2026-06-18, sitting on HEAD `0fcb2c5`. No prior committed revision of this artefact exists.
**Reviewer mode**: Claude (independent peer reviewer per [CONVENTIONS §1.2](../CONVENTIONS.md)). Note on role-split: the target is technically a producer-mode artefact under §1.1 ("descriptive analysis scripts on `per_day_master.csv` and their result docs"); the user explicitly authorised `/research-review` per §1.3 ambiguous-case clause because the artefact is load-bearing for HA07c / HA07d / HA08c re-interpretation and carries non-trivial substantive claims (E[L]* deviation flag, new near-identity pair, phase-stratified medians vs locked dose-response). Reviewed under the same 4-layer checklist applied to reviewer-mode artefacts.
**Review date**: 2026-06-18

---

## 1. What the data shows

On Stratum 4 (n=1339 sleep-valid days, 2022-09-03 → 2026-06-05), `stress_mean_sleep` is a heavily right-skewed daily channel (median=19.21, MAD=2.87, skew=+2.72, excess kurtosis=+15.5) with persistent serial dependence (lag-7 ρ=+0.14; data-driven Politis-White E[L]\*=12.6, flagged as factor-of-2 deviation from the project default E[L]=7). Across the four citalopram phases the medians sit in a narrow band (unmedicated 19.51 / buildup 17.04 / consolidation 19.07 / afbouw 20.20); the consolidation−unmedicated step is −0.44 (≈ 0.15 MAD). Crash-vs-normal separation is large and consistent with the canonical HRV-proxy-validation finding (episode-level n=29 vs 1238, Cohen's d=+0.91, bootstrap CI95 on mean diff [+1.58, +8.40]). One new near-identity pair surfaces vs `asleep_stress_avg_uds` (Pearson r=+0.929, just over the §3.3 threshold).

The author's interpretive framing — most clearly Q3.1.d — separates the empirical pattern (flat medians across phases) from the locked +0.43/mg dose-response slope by reading the slope as a within-buildup-window effect rather than a between-phase steady-state level shift. That framing is the load-bearing interpretive claim and is explicitly caveat-class.

## 2. What fired and why

### Layer 1 — Universal reporting (inherits from SCRIBE 2016, STROBE 2007)

No blocking fires. Two minor items:

- **[L1.2 — CONVENTIONS §1.2 / DATA_DICTIONARY discipline]** — *minor*. Column references in Q3.1.e (six channels) and Q3.1.i (`resting_hr`, `dose_plasma_mg(d)`, `stress_mean_sleep_lagged_mean_14d`) do not link to [DATA_DICTIONARY.md](../DATA_DICTIONARY.md) rows. The pipeline chain for the primary channel IS named end-to-end (`per_day_master.csv ← build_unified_dataset.py ← sleep_stress_nightly.csv ← extract_sleep_stress.py`), so source-file provenance per §3.6 is clean — but the column-row semantics that DATA_DICTIONARY carries (especially the near-identical-pair annotations for the §3.3 audit hook) are not directly cited. STROBE Item 7 ("clearly define all variables") would prefer the per-column link. Fix is one-line each: link the column name on first mention in each Q.

- **[L1.5 — STROBE Item 12 / SCRIBE Item 22]** — *minor*. Limitations are present but woven into Q3.1.d (three readings of the medians-vs-slope discrepancy) and Q3.1.g (daily-mean dilution-vulnerability for spike mechanisms). There is no separated "Limitations" section. For a producer-mode descriptive doc this is acceptable, but a one-paragraph consolidation at the bottom of `findings.md` would lift Layer-1 conformance without changing any substantive claim.

### Layer 2 — Observational n=1 (inherits from Daza 2018, Personal Science)

No fires. Stationarity is acknowledged via Q3.1.h drift check; counterfactual framing is subject-internal (crash episode vs the subject's own non-crash baseline); calendar-time anchoring is correct for a phase-stratified citalopram question; provenance is traceable; the held-out-structure framing concern from memory `project_garmin_research_bias_boundary` does not apply (no train/validate split invoked).

### Layer 3 — Time-series specific (inherits from Natesan Batley 2023, WWC 2022, CENT 2015)

One substantive item:

- **[L3.4 — [permutation_null_block_length.md](../methodology/permutation_null_block_length.md) §3 + Operational consequence 2 step 5]** — *substantive (not blocking)*. The data-driven E[L]\*=12.6 fires the methodology MD's factor-of-2 deviation flag (deviation_ratio=0.80 > 0.5 threshold). The MD's binding rule reads "If E[L]* differs from 7 by more than a factor of 2, flag for review before locking the verdict." The flag IS surfaced in Q3.1.b and the downstream-HA implication is named — but the analysis's own day-level CI in Q3.1.f.day_level is computed at E[L]=7 (`stationary_bootstrap_E_L7`), producing CI95 [+2.80, +9.56] on the mean diff. That CI is narrower than what E[L]≈13 would yield, and it is published in a table without a flag-firing footnote next to it. Mitigating factors: (a) the descriptive layer explicitly has no falsification bar per §2.1, so no verdict is being locked; (b) the table's narrative note ("autocorrelation-inflated supplementary read") is correct as far as it goes; (c) the headline finding rests on the episode-level d=+0.91 with its event-level bootstrap, which doesn't depend on the day-level block-length choice. Why this still matters: the methodology MD's flag-firing rule is explicitly an audit gate; running the day-level CI at the flagged-deviant default and not at the surfaced E[L]*≈13 sits half-in-half-out of the MD's own discipline. A second CI row at E[L]=13 alongside the existing E[L]=7 would close the loop. Natesan Batley 2023 finds 83.8% of n-of-1 medical studies ignore autocorrelation outright; this analysis is far above that bar — the concern is one specific inconsistency, not a category failure.

The other Layer 3 items pass and are flagged in §3 below.

### Layer 4 — Project-specific audit hooks (inherits from CONVENTIONS §3, §4)

No fires. The analysis is unusually clean on this layer — see §3 for the specifics, particularly L4.5 (spike-metric discipline) and L4.7 (caveat-class framing).

### Side observations

- **Side** — *numerical*. `findings.md` Q3.1.b text reads "rho_lag7=+0.14, still above the Politis-White 2σ threshold of ~0.07". The threshold formula used in `run.py:769` is `2.0 * np.sqrt(np.log(len(arr)) / len(arr))` which at n=1339 evaluates to ≈ 0.147, not ≈ 0.07. The white-noise rule-of-thumb 2/√n at n=1339 is ≈ 0.055. Neither value matches the cited "~0.07". The qualitative claim ("lag-7 ACF is non-trivial") still holds because lag-7 ACF = +0.142, comparable to the run.py threshold — but readers comparing the text to the plot will see a discrepancy. The fig5_acf.png caption uses the run.py threshold, so the plot and the prose disagree on the numerical reference.
- **Side** — *cross-reference numerical*. Q3.1.i §2 reports r=+0.342 on the LC era (inherited from hrv_proxy_validation Check 7.2, R²=0.117 → 88% unexplained variance) and r=+0.359 on the current Stratum 4 — both are correct and internally consistent, but the prose juxtaposes the two without explicitly flagging the frame switch between sentences. A one-clause clarification (`r=+0.342 LC-era / r=+0.359 S4`) would help.
- **Side** — *headline framing*. The README and findings.md headline both report "CI95 [+1.58, +8.40] stress-unit mean diff" inline with "Cohen's d=+0.91". A fast reader could conflate the CI as bracketing d rather than the mean diff. The findings.md body Q3.1.f table disambiguates correctly ("Bootstrap 95% CI on mean diff"); the headlines could match by adding "on mean diff".

## 3. What does not fire (selective)

- **L3.1 (autocorrelation) — strong pass**. Q3.1.b computes Politis-White E[L]\* via the project's `inference.py::compute_data_driven_block_length`, reports ACF at lags 1/2/3/7/14, surfaces the cutoff lag M=6, and explicitly fires the factor-of-2 deviation flag against the locked [`permutation_null_block_length.md`](../methodology/permutation_null_block_length.md) default. The episode-level bootstrap in Q3.1.f uses event-level resampling (5000 iters, seed=20260618) which doesn't need a block parameter, and the day-level uses the stationary bootstrap (not fixed-block, per the methodology MD's §Decision wording). For a descriptive layer this exceeds standard reporting practice.

- **L3.5 (trend vs level separation) — strong pass**. Q3.1.d's explicit "the +0.43/mg dose-response slope is a within-buildup-window effect, NOT a between-phase steady-state level shift" is the cleanest possible enactment of the caveat-vs-a-priori distinction CONVENTIONS §4.2 prescribes. The three readings of the discrepancy (LC-trajectory absorbs the slope's implied step / §5.B framework is correct for within-window not between-phase / the 30mg extrapolation is slope-not-level) each name a specific mechanism and let the downstream HA designer pick. This is exactly the level of interpretive separation Layer 3 wants on a multi-phase frame.

- **L4.3 (one column per definitional pair) — strong pass with active discovery**. The §3.3 near-identity threshold |ρ|≥0.92 is applied; Q3.1.e discovers a **new** near-identity pair (`asleep_stress_avg_uds` Pearson r=+0.929) not previously in the cross-channel-correlation card's 7-channel panel. The §3.3 audit hook is firing in the project's favour — surfacing a pair to be propagated, not flagging a violation in the present analysis. The mechanistic explanation ("methodological overlap, not a biological finding") is correct.

- **L4.4 (crash-drop sensitivity) — strong pass**. Q3.1.f reports Spearman(stress_mean_sleep, gevoelscore) full=−0.194, crash-dropped=−0.147, |Δ|=0.047 — well below the §3.4 0.10 threshold. The sensitivity is computed via `_utils/frame.py::crash_drop_sensitivity`, which is the canonical implementation. Comparison to the §3.4 example (exertion × resting_hr Spearman swings ~0 to ~0.4 on crash drop) is explicit.

- **L4.5 (spike-detecting metric) — strong pass**. Q3.1.g directly addresses CONVENTIONS §3.5 and admits, without hedging, that `stress_mean_sleep` is structurally a daily mean and therefore dilution-vulnerable for any acute-load mechanism; it names `max_spike_minutes` as the in-master spike companion (Pearson r=+0.058 with the daily mean — i.e. genuinely independent), names the latent FIT primitive that would be the correct surface, and flags that a sleep-window spike primitive is a queued extraction task. Rare for a daily-mean channel to face this honestly.

- **L4.6 (named counts) — clean**. Every n in `findings.md` carries scheme + unit + source file: n=1339 sleep-valid days (`stress_mean_sleep` non-NaN in S4); 29 crash-episodes (`labels_crash_v2.csv` unique `episode_id` starting with `crash-`); 101 crash-days (`label=='crash'`); 1238 non-crash days; 33 NaN nights via the MIN_SAMPLES_PER_NIGHT=120 gate.

- **L4.7 (caveat-class framing) — strong pass throughout**. The findings.md verdict-equivalent statements are all caveat-class: "delegate to lc_phase_descriptive.md AND extend" (not "supersedes"), "the locked +0.43/mg dose-response slope is a within-buildup-window effect, NOT a between-phase steady-state level shift", "the day-level d=+1.05 is the expected within-episode-autocorrelation inflation; the episode-level is the headline", "the outliers are not artefacts ... they look like real night-stress events". None of these claim what was not measured.

## 4. What would strengthen this finding

1. **Add a second day-level CI at E[L]=13 in Q3.1.f.day_level** alongside the existing E[L]=7 row, with a one-line note "factor-of-2 deviation flag fired at Q3.1.b". Inherits from [permutation_null_block_length.md](../methodology/permutation_null_block_length.md) §3 (the audit gate is explicit in the MD; the present analysis surfaces the flag but doesn't apply it to its own CI). Expected effect: the day-level CI on the mean diff likely widens by ~30-40% (back-of-envelope from the autocorrelation ratio), still excluding zero, but readers see both anchors and can judge robustness. Closes the half-in-half-out posture on L3.4.

2. **Fix the "Politis-White 2σ threshold of ~0.07" prose in Q3.1.b** to either cite the formula used in run.py (`2·√(log n / n)` ≈ 0.147 at n=1339, which matches the plot) or the white-noise rule-of-thumb 2/√n ≈ 0.055. Inherits from STROBE Item 13 (numeric reporting accuracy). Expected effect: prose and plot agree; no change to the qualitative conclusion (lag-7 ACF=+0.14 still non-trivial under either threshold).

3. **Link each column on first mention to its DATA_DICTIONARY row** — Q3.1.e (6 channels), Q3.1.g (`max_spike_minutes`, `stress_high_duration_min`, `stress_low_motion_min_count_S60_Mlow`), Q3.1.i (`resting_hr`, `dose_plasma_mg(d)`). Inherits from STROBE Item 7 + CONVENTIONS §3.3 (the near-identical-pair annotations live in DATA_DICTIONARY). Expected effect: column semantics are one click away; the new `asleep_stress_avg_uds` near-identity finding has a natural home to be propagated to.

4. **Reconcile Q3.1.i covariate #3 with the canonical `_lagged_lcera` family in CONVENTIONS §3.2**. The proposed `stress_mean_sleep_lagged_mean_14d(d) = mean(channel[d-14:d-1])` is a sensible covariate for the autocorrelation-vs-mechanism disambiguation, but CONVENTIONS §3.2 already mandates a `_lagged_lcera` 60→30d-window construction for PEM-pacing hypotheses on the LC frame. Either (a) name the 14d construction as the descriptive-substrate companion to the `_lagged_lcera` variant the future HA actually pre-regs, or (b) justify why 14d (just past M=6 cutoff) is the descriptive's choice and `_lagged_lcera` is the HA's. Inherits from CONVENTIONS §3.2. Expected effect: a future HA pre-reg reading Q3.1.i won't be left choosing between two trailing-mean windows.

5. **Consolidate a one-paragraph "Limitations" section at the foot of findings.md** that names the four limitations currently woven into Q3.1.d / Q3.1.g / Q3.1.f.day_level / Q3.1.h: (i) the cross-phase analysis is on raw channel, not dose-adjusted; (ii) the channel is a daily mean and dilution-vulnerable for acute-load mechanisms; (iii) the day-level Cohen's d is autocorrelation-inflated relative to the episode-level headline; (iv) the outlier rule MAD-z|>5 is descriptive-stage and downstream HA tests should NOT trim. Inherits from SCRIBE Item 22 / STROBE Item 19. Expected effect: a reviewer or HA-pre-reg author reads the limitations cold without having to assemble them from Q3.x bodies.

## 5. Verdict

**PASS with caveats** — Layer 3 surfaces one substantive consistency concern (the Q3.1.f day-level CI runs at the deviation-flagged default E[L]=7 without a companion row at the surfaced E[L]\*≈13), and Layer 1 / side observations name several minor numerical and cross-reference fixes; all other layers including the §3 audit-hook battery pass cleanly, with L3.5 (trend-vs-level separation on Q3.1.d) and L4.5 (spike-metric §3.5 discipline on Q3.1.g) particularly strong.

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
