# Descriptive audit -- Q24 MD-beta Wave 2D: 2024 residual tension investigation (per-quarter + by-intensity + per-episode diagnostic + threshold + absolute-step + neighbouring-year + pre-window load)

*Producer-mode Stage -1 descriptive audit per [CONVENTIONS section 1.1](../../../CONVENTIONS.md#11-producer-mode-claude-writes--edits--runs). Drafted 2026-07-16 by Claude (Opus 4.7) in producer-mode subagent under user delegation. Authorising user: Willem.*

**Status**: **LOCKED r1 2026-07-16** post-review absorption per [`../../../reviews/methodology-Q24-mdbeta-wave2d-2024-residual-tension-2026-07-16.md`](../../../reviews/methodology-Q24-mdbeta-wave2d-2024-residual-tension-2026-07-16.md) (verdict: DEFENSIBLE with revision; 2 audit-level absorb fires + explicit Path R2B recommendation for MD-beta r2 downstream). Reviewer confirmed the section 10.3 "2023 anomaly" is the KNOWN citalopram phase-boundary effect (verified against MD-alpha section 3.1 + MD-alpha Wave 2A audit section 8 numbers) and that section 9 within-2024 finding is UNAFFECTED (all 3 crash events post-2024-04-09 citalopram onset). See section 10.3 (L2.2 absorb -- citalopram phase-boundary anchor) + section 11.2 (L4.3 absorb -- definitional-pair tightening on joint (b) + (e) reading).

**Wave**: 2D. Sibling of parent [Wave 2C Stage -1 audit LOCKED r1 2026-07-16](../Q24-mdbeta-wave2c-reactive-vs-proactive-rest/audit.md). Extension of the parent [Wave 2B Stage -1 audit LOCKED r1 2026-07-16](../Q24-mdbeta-precursor-rest-streak/audit.md) and the parent [Q24 Stage -1 audit LOCKED r1 2026-07-15](../Q24-precursor-heavy-day-structure/audit.md). Points at [MD-beta LOCKED r1 2026-07-16](../../../methodology/heavy_day_crash_risk_prediction.md) for operand + machinery lock.

**Frame**: LC-era stratum (`lc_phase == 'lc'`), n=1524 days (2022-04-04 -> 2026-06-05), matches parent Stage -1 audit stratum. Heavy-day definition, episode unit, and rest-day primary operand inherited verbatim from parent Wave 2B audit. Within-year focus on **year_end == 2024**; secondary comparators on 2023 and 2025.

**Reproducibility**: [`scripts/audit.py`](scripts/audit.py) + outputs in [`output/`](output/); idempotent re-run against `$GEVOELSCORE_DATA_PATH/unified/per_day_master.csv`. `RANDOM_SEED = 20260716` per MD-beta section 3.6; declared but not exercised in this Wave 2D audit (no randomisation needed).

**Discipline scope**: Stage -1 descriptive audit only. NO inferential-verdict framing. All contingency tables reported as descriptive-with-Wilson-CI per MD-beta section 3.6 + [CONVENTIONS section 2.1](../../../CONVENTIONS.md#21-descriptive-before-inference). The five candidate readings of the 2024 exception are treated as **partial-testable at n=1**: findings can be described as CONSISTENT-WITH, AMBIGUOUS-FOR, or FALSIFYING for each candidate reading, but no test in this audit constitutes a verdict on any of them.

**What "resolved" means for this Wave 2D**: not that we know which candidate reading is correct, but that we have enough descriptive characterisation for MD-beta r2 to make a defensible codification decision on the rest-adjacency arc (gevoelscore-conditioning, intensity stratification, cumulative-load pre-window covariate).

**Cross-refs**:

- [Parent Wave 2C Stage -1 audit LOCKED r1 2026-07-16](../Q24-mdbeta-wave2c-reactive-vs-proactive-rest/audit.md) -- source of the 2024 tension (section 5.1 per-year table + section 5.3 candidate-readings framing + section 10.5 reviewer L10.5 extension).
- [Parent Wave 2B Stage -1 audit LOCKED r1 2026-07-16](../Q24-mdbeta-precursor-rest-streak/audit.md) -- section 10 intensity stratification (heavy RR = 2.07 vs very_heavy RR = 0.96 whole-corpus).
- [MD-beta LOCKED r1 2026-07-16](../../../methodology/heavy_day_crash_risk_prediction.md) -- operand + machinery lock; section 3.1 rest-day operand; section 3.7 pre-committed direction.
- [Parent Q24 MD LOCKED r1 2026-07-15](../../../methodology/post_heavy_day_compensatory_rest.md) -- stratum + heavy-day inheritance.
- [CONVENTIONS sections 1.2, 2.1, 3.1, 3.6, 3.10, 4.2, 5](../../../CONVENTIONS.md).
- Memory pointers: `project_rest_day_operand_semantics`, `feedback_narrative_only_events`, `feedback_research_discipline_interpretive`, `feedback_research_discipline_statistical`.

---

## 1. Corpus summary + Wave 2C anchor (where the 2024 tension came from)

Corpus counts inherited from parent Wave 2C audit and parent Wave 2B audit; not re-emitted.

| Measure | Value | Source |
|---|---|---|
| LC-era rows | 1524 days | [parent Stage -1 section 1](../Q24-precursor-heavy-day-structure/audit.md#1-corpus-summary) |
| gap=0 heavy episodes | 314 | [parent Wave 2B section 3](../Q24-mdbeta-precursor-rest-streak/audit.md#3-heavy-episode-construction) |
| Episodes with rest-after K=3 primary True + full crash window | 312 (2 NaN rest-after dropped) | [parent Wave 2C section 5.1](../Q24-mdbeta-wave2c-reactive-vs-proactive-rest/audit.md#51-per-pool-2x2) |
| Wave 2C pooled proactive-strategic RR | 0.354 (5/80 vs 41/232) | ibid |
| Wave 2C 2023 proactive-strategic RR | 0.223 (1/20 vs 15/67) | ibid |
| Wave 2C 2024 proactive-strategic RR | **0.929** (3/15 vs 14/65) | ibid |
| Wave 2C 2025 proactive-strategic RR | 0.000 (0/23 vs 2/43) | ibid |
| Wave 2C 2026 partial proactive-strategic RR | 0.000 (0/15 vs 4/21) | ibid |
| 2024 PS-True arm crash count | 3 events (episode-unit) | ibid; also this Wave 2D section 5 |

**The 2024 tension in plain terms**: 2023 / 2025 / 2026 all sign-flip cleanly on the proactive-strategic subset (RR ~ 0.2 or 0.0); 2024 does not (RR ~ 0.9, PS arm rate 20% vs complement 21.5%). The reviewer of Wave 2C called this a "sign-flip PAUSE, not a smooth transition curve" and endorsed a formal Wave 2D investigation before Stage H pre-registration on the rest-adjacency arc.

---

## 2. Five candidate readings for the 2024 exception

Recap from [parent Wave 2C section 5.3 + section 10.5 reviewer L10.5 extension](../Q24-mdbeta-wave2c-reactive-vs-proactive-rest/audit.md#53-consistency-with-interpretation-a). Each candidate is partial-testable at n=1; the Wave 2D findings describe each as CONSISTENT-WITH, AMBIGUOUS-FOR, or FALSIFYING.

- **(a) Small-n artefact** -- 2024 PS-True arm has 15 episodes with 3 crashes; Wilson CI [7.0, 45.2] does not credibly rule out RR ~ 1 or RR ~ 2. Test: threshold sensitivity on the gevoelscore boundary should stay wide and directionally-unstable if it is just noise. **See §6.**
- **(b) Partial-mitigation only** -- gevoelscore >= 5 does not fully isolate calibrated pacing in 2024; residual endogeneity may operate through a mechanism not captured by gevoelscore-on-rest-day (e.g. cumulative-load in the pre-window, forward-window compensatory failure). Test: per-episode diagnostic on the 3 crash-in-5d events should share features. **See §5 + §9.**
- **(c) Transition-year mid-shift** -- 2024 sits between crisis-dominant (2023) and strategic-dominant (2025+) composition; the shift may have happened mid-2024 rather than at year boundaries. Test: per-quarter proactive-strategic RR within 2024 should show the shift happening within the year. **See §3 + §8 comparator.**
- **(d) Real endogeneity residual specific to 2024** -- some 2024-specific factor (medication titration mid-year, seasonal effect, life-event stress cluster) drives the 3 crash-in-5d events beyond what gevoelscore captures. Test: per-episode diagnostic should surface common features (dates, seasonal cluster, other exposures). **See §5.**
- **(e) Intensity-interaction residual** -- Wave 2B section 10 found heavy-terminal episodes drove the whole-corpus sign-inversion (heavy RR = 2.07 vs very_heavy RR = 0.96). If 2024 PS-True arm is disproportionately heavy-terminal, that could explain the residual. Test: cross-tab 2024 PS episodes by end_class. **See §4.**

**Reading discipline**: candidate readings are not mutually exclusive. Small-n artefact (a) and intensity-interaction (e) can both be true simultaneously; per-episode diagnostic (b) + (d) tests can both surface partial-signal features. The audit does not force a single-winner reading.

---

## 3. Within-2024 per-quarter proactive-strategic RR (test candidate (c))

Source: [`output/pssubset_per_quarter_2024.csv`](output/pssubset_per_quarter_2024.csv).

**Operational definition** (same as Wave 2C section 5): episode is proactive-strategic if `rest_after_3_primary = True` AND at least one of the K=3 rest-days has NO `is_crash = True` in `[rest_day - 3, rest_day - 1]` AND `gevoelscore >= 5` on rest_day. Within-year stratification by quarter of the episode's D_end.

### 3.1 Per-quarter 2024 2x2

| Quarter | n_used | PS-True n / crash | PS-False n / crash | Rate PS-True [Wilson] | Rate PS-False [Wilson] | RR (PS/complement) | viable_n_min5 |
|---|---:|---|---|---|---|---:|:---:|
| 2024 ALL | 80 | 15 / 3 | 65 / 14 | 20.00% [7.0, 45.2] | 21.54% [13.3, 33.0] | **0.929** | yes |
| 2024 Q1 | 23 | 1 / 0 | 22 / 6 | 0.00% [0.0, 79.3] | 27.27% [13.2, 48.2] | 0.000 | **no** (PS n=1) |
| 2024 Q2 | 23 | 3 / 1 | 20 / 4 | 33.33% [6.1, 79.2] | 20.00% [8.1, 41.6] | 1.667 | **no** (PS n=3) |
| 2024 Q3 | 18 | 5 / 2 | 13 / 2 | 40.00% [11.8, 76.9] | 15.38% [4.3, 42.2] | **2.600** | yes |
| 2024 Q4 | 16 | 6 / 0 | 10 / 2 | 0.00% [0.0, 39.0] | 20.00% [5.7, 51.0] | 0.000 | yes |

Row-total check: Q1 + Q2 + Q3 + Q4 = 23 + 23 + 18 + 16 = 80 = 2024 ALL. Sum of PS-True crash: 0+1+2+0 = 3; sum of complement crash: 6+4+2+2 = 14. Matches 2024 ALL row.

### 3.2 Descriptive observations

**Headline: the 3 crashes on the 2024 PS-True arm are concentrated in Q2 (n=1) and Q3 (n=2). Q1 and Q4 both have zero crashes on the PS-True arm.**

- **Q1 2024**: PS-True n = 1 (too small to read; narrative-only per parent Stage -1 audit convention). Complement rate 27.3% is the highest single-quarter complement rate.
- **Q2 2024**: PS-True n = 3, 1 crash (33% rate). PS-False n = 20, 4 crashes (20% rate). RR = 1.67, but PS arm n < 5 -- narrative-only.
- **Q3 2024**: PS-True n = 5, **2 crashes (40% rate)**. PS-False n = 13, 2 crashes (15% rate). RR = **2.60** -- viable n_min5 but Wilson CI on PS arm is [11.8, 76.9], very wide; RR is directionally sign-inverted (PS arm carries HIGHER crash rate than complement) but not credibly distinguishable from RR = 1.
- **Q4 2024**: PS-True n = 6, **0 crashes** (rate 0% [0.0, 39.0]). PS-False n = 10, 2 crashes (20%). RR = 0.00 -- viable n_min5, first quarter within 2024 that shows the clean-flip pattern seen in 2025 / 2026.

### 3.3 Consistency with candidate reading (c) transition mid-shift

**Descriptively consistent with the transition-mid-shift reading at the quarter resolution**: PS-True crash rate 40% in Q3 -> 0% in Q4 is the largest single-quarter shift, and Q4 aligns with the pattern seen in all of 2025 (RR = 0.00). The 2024 -> 2025 sign-flip is descriptively visible as a Q3 -> Q4 flip within 2024.

**But**: sample sizes are tiny (Q4 n = 6 on PS-True arm), Wilson CIs overlap heavily, and the 2 crash events in Q3 dominate the whole-year 2024 signal. Alternate reading: the 2 Q3 events are outliers within an otherwise sign-flipped year; not a mid-year composition shift.

**Assessment**: CONSISTENT-WITH candidate (c) at the descriptive resolution; AMBIGUOUS given cell sizes. Cannot rule out the "Q3 events are outliers within a year that would otherwise have sign-flipped" reading, which is closer to candidates (b) / (d) / (e) than to (c).

**Reader guidance**: per-quarter within a single year at n_min5 = viable only for Q3 (n=5 PS) and Q4 (n=6 PS) is right at the parent Stage -1 audit threshold. Wilson CI [11.8, 76.9] on Q3 PS arm crash rate means the observed 40% could plausibly reflect a true rate anywhere from ~ 12% to ~ 77%. Any reading of "Q3 is the tension quarter" must survive that CI.

---

## 4. Within-2024 by-intensity proactive-strategic RR (test candidate (e))

Source: [`output/pssubset_2024_by_intensity.csv`](output/pssubset_2024_by_intensity.csv).

**Cross-tab**: 2024 PS episodes by `end_class` (heavy vs very_heavy). Compare to [parent Wave 2B section 10](../Q24-mdbeta-precursor-rest-streak/audit.md#10-intensity-stratified-episode-end-class) whole-corpus intensity stratification (heavy RR = 2.07 vs very_heavy RR = 0.96 on rest-after primary K=3, NOT the proactive-strategic subset).

### 4.1 Per-end-class 2024 2x2

| end_class | n_used | PS-True n / crash | PS-False n / crash | Rate PS-True [Wilson] | Rate PS-False [Wilson] | RR (PS/complement) |
|---|---:|---|---|---|---|---:|
| 2024 ALL | 80 | 15 / 3 | 65 / 14 | 20.00% [7.0, 45.2] | 21.54% [13.3, 33.0] | **0.929** |
| 2024 heavy | 39 | 9 / 0 | 30 / 9 | **0.00%** [0.0, 29.9] | 30.00% [16.7, 47.9] | **0.000** |
| 2024 very_heavy | 41 | 6 / 3 | 35 / 5 | **50.00%** [18.8, 81.2] | 14.29% [6.3, 29.4] | **3.500** |

Row-total check: heavy + very_heavy = 39 + 41 = 80. Sum PS-True crash: 0 + 3 = 3; sum PS-False crash: 9 + 5 = 14. Matches 2024 ALL.

### 4.2 Descriptive observations

**Headline: all 3 crashes on the 2024 PS-True arm are on very_heavy-end episodes; zero crashes on heavy-end PS-True episodes.**

- **Heavy-end (n=39)**: PS-True arm 0 crashes on 9 episodes (0% [0.0, 29.9]); complement 9 crashes on 30 (30.0% [16.7, 47.9]). RR = 0.00, sign flip fully clean at the heavy-end stratum.
- **Very_heavy-end (n=41)**: PS-True arm 3 crashes on 6 episodes (**50% [18.8, 81.2]**); complement 5 crashes on 35 (14.3% [6.3, 29.4]). RR = **3.50**, sign INVERTED at the very_heavy-end stratum. All 3 PS-True crashes are here.

### 4.3 Comparison to Wave 2B whole-corpus intensity stratification

[Parent Wave 2B section 10](../Q24-mdbeta-precursor-rest-streak/audit.md#10-intensity-stratified-episode-end-class) reported the whole-corpus K=3 rest-after primary 2x2 stratified by intensity (heavy RR = 2.07; very_heavy RR = 0.96). That analysis was on the FULL rest-after arm (not restricted to proactive-strategic).

**Wave 2D finding is the inverse pattern within 2024 PS-True**: heavy-end PS-True is clean (RR = 0.00), very_heavy-end PS-True is sign-inverted (RR = 3.50). This is DIFFERENT from the Wave 2B whole-corpus signal.

**Reading**: within the 2024 proactive-strategic subset, the intensity-interaction residual candidate reading (e) is CONSISTENT-WITH the descriptive pattern -- the residual sits entirely on very_heavy-end PS episodes. Gevoelscore-on-rest-day + no-crash-in-3d-lookback does NOT protect 2024 very_heavy-end episodes from crash-in-5d at the same rate it protects heavy-end episodes.

### 4.4 Consistency with candidate reading (e) intensity-interaction residual

**CONSISTENT-WITH candidate (e) at high descriptive resolution**: the 2024 residual sign-lack sits entirely on very_heavy-end PS episodes (RR = 3.50 in that stratum vs RR = 0.00 in the heavy-end stratum). The reading is: gevoelscore-conditioning is sufficient to reveal the pre-committed direction when the terminal-episode intensity is heavy-only, but NOT when it is very_heavy.

**Caveat**: n = 6 on the 2024 very_heavy PS-True arm with 3 crashes. Wilson CI [18.8, 81.2] on the 50% crash rate is very wide. The observed 3.5x RR is not credibly distinguishable from RR = 1.5 at the lower end of the CI. However, the DIRECTION of the residual (very_heavy carries the residual within 2024 PS) is consistent with what a stronger sample size would be expected to preserve if the mechanism is real.

**Combined with (a) small-n artefact**: candidates (a) and (e) are not mutually exclusive. The 2024 very_heavy PS-True stratum is BOTH small-n (n=6) AND directionally intensity-loaded (all 3 crashes here). Both readings are partially supported.

---

## 5. Per-episode diagnostic on the 3 crash-in-5d 2024 PS-True events + n=12 non-crash baseline (test candidates (b) + (d))

Sources: [`output/pssubset_2024_crash_events_diagnostic.csv`](output/pssubset_2024_crash_events_diagnostic.csv) (n = 3 events) + [`output/pssubset_2024_noncrash_baseline_diagnostic.csv`](output/pssubset_2024_noncrash_baseline_diagnostic.csv) (n = 12 baseline).

**Discipline note per [memory feedback_narrative_only_events]**: n = 3 is narrative-only per parent Stage -1 audit threshold. The per-episode diagnostic is reported as a descriptive table + narrative observations; NO inferential statistic is computed on the 3-vs-12 comparison.

### 5.1 The 3 crash-in-5d 2024 PS-True events

| episode_id | ep_start | ep_end | streak | end_class | quarter | rest_day | gs_on_rest | first_crash_offset | 7d_prior_exertion | 14d_prior_exertion | 30d_prior_exertion | days_since_prev_crash | prior_30d_crashes | subsequent_7d_exertion |
|---:|---|---|---:|---|---:|---|---:|---:|---:|---:|---:|---:|---:|---:|
| 163 | 2024-04-26 | 2024-04-27 | 2 | very_heavy | Q2 | 2024-04-28 | 5.0 | 3.0 | 47.5 | 74.5 | 178.6 | 56.0 | 0 | 8.5 |
| 179 | 2024-07-11 | 2024-07-11 | 1 | very_heavy | Q3 | 2024-07-12 | 5.0 | 4.0 | 37.0 | 57.5 | **277.2** | 15.0 | **4** | 10.0 |
| 190 | 2024-08-24 | 2024-08-25 | 2 | very_heavy | Q3 | 2024-08-26 | 5.0 | 4.0 | 31.0 | 94.0 | 206.0 | 39.0 | 0 | 2.0 |

### 5.2 Common features across the 3 crash events

- **All 3 events are very_heavy end_class** (echoing §4.4).
- **All 3 events had gevoelscore = 5 exactly on the rest-day** (right at the strategic threshold -- borderline-strategic).
- **All 3 events cluster in Apr-Aug (Q2-Q3 seasonal window)**; none in Q1 or Q4.
- **All 3 events had short streaks (1-2 days)**; not accumulated-heavy-streak driven.
- **All 3 first-crashes occur 3-4 days after episode-end**, at the upper end of the 5-day crash window.
- **Cumulative prior-30d effective_exertion_min sums range 178-277 minutes**, all elevated (see §9 comparison to non-crash baseline mean of 115 min).
- **Subsequent-7d exertion is LOW (2-10 min) across all 3**, so the crash is not attributable to post-rest-day overshoot; the crash trajectory was already loaded before the "rest" happened.

### 5.3 The n = 12 non-crash 2024 PS-True baseline (comparison)

Key contrasts (see §9 for aggregate statistics):

- **7 of 12 non-crash episodes are heavy end_class** (only 5 are very_heavy). Vs 3/3 crash cases very_heavy.
- **Prior-30d exertion sums range 42-264 min, with mean ~115 min** -- roughly HALF of the crash-case mean 214 min.
- **Post-rest subsequent-7d exertion ranges 1.5-88 min, mean ~34 min** -- meaningfully higher than crash-case mean 8 min. Non-crash episodes involve continued light-moderate activity in the recovery window; crash-case episodes had near-zero activity in the +7d window (crash already imminent by day 3-4).
- **Gevoelscore = 5 exactly on the rest-day is universal across all 12 non-crash cases too** -- the "gs = 5 exactly" observation on crash cases is NOT distinguishing.
- **Non-crash cases span all 4 quarters** (Q1: 1, Q2: 2, Q3: 4, Q4: 5); no seasonal clustering pattern.

### 5.4 Consistency with candidates (b) + (d)

**Candidate (b) partial-mitigation only via cumulative-load-in-pre-window**: **CONSISTENT-WITH descriptively**. The 3 crash cases carry a ~2x higher prior-30d cumulative effective-exertion load (mean 214 min vs 115 min for non-crash baseline; see §9). Gevoelscore >= 5 on the rest-day did NOT reflect the higher cumulative load coming into the episode. This is the strongest signal in the per-episode diagnostic: **the residual endogeneity operates through a pre-window load channel that gevoelscore-on-rest-day does not capture**.

**Candidate (d) real endogeneity residual specific to 2024**: **AMBIGUOUS-FOR** at the descriptive resolution. The 3 events cluster in Apr-Aug (a seasonal Q2-Q3 window) but 4 of the 12 non-crash cases are also in Q3, so seasonality alone does not discriminate. No medication-titration or other 2024-specific exogenous marker is available in `per_day_master.csv`. The dates themselves are the only 2024-specific feature that could carry a real-life residual, and the sample of 3 is too small to distinguish "life-event cluster" from "coincidence".

### 5.5 Reader guidance for per-episode diagnostic

Per [CONVENTIONS section 3.6](../../../CONVENTIONS.md#36-name-every-count-n-unit-per-scheme-in-file): the 3 crash-cases are 3 events on 3 episodes on 3 rest-days on 3 dates; the 12 non-crash baseline are 12 events on 12 episodes on 12 rest-days on 12 dates. Aggregate statistics on n = 3 vs n = 12 are descriptive-only.

**The strongest per-episode reading is §5.4 candidate (b) partial-mitigation-via-cumulative-load**: prior-30d effective-exertion load is ~2x higher on crash cases (mean 214 vs 115). This is a load-bearing signal for MD-beta r2 codification (see §12).

---

## 6. Gevoelscore threshold sensitivity within 2024 (test candidate (a) small-n artefact)

Source: [`output/pssubset_threshold_sensitivity_2024.csv`](output/pssubset_threshold_sensitivity_2024.csv).

**Three gevoelscore thresholds** applied to the 2024 proactive-strategic 2x2:

- **primary_gs_ge_5** -- current Wave 2C definition; PS-True requires gevoelscore >= 5 on rest-day.
- **strict_gs_ge_6** -- strict-only; drops the gs = 5 rest-days from the PS-True arm.
- **loose_gs_ge_4** -- borderline-inclusive; adds gs = 4 rest-days to the PS-True arm.

### 6.1 Per-threshold 2024 2x2

| Threshold | PS-True n / crash | PS-False n / crash | Rate PS-True [Wilson] | Rate PS-False [Wilson] | RR (PS/complement) | viable_n_min5 |
|---|---|---|---|---|---:|:---:|
| primary_gs_ge_5 | 15 / 3 | 65 / 14 | 20.00% [7.0, 45.2] | 21.54% [13.3, 33.0] | **0.929** | yes |
| strict_gs_ge_6 | **0 / 0** | 80 / 17 | -- | 21.25% [13.7, 31.4] | -- | **no** (PS n = 0) |
| loose_gs_ge_4 | 35 / 5 | 45 / 12 | 14.29% [6.3, 29.4] | 26.67% [16.0, 41.0] | **0.536** | yes |

### 6.2 Descriptive observations

**Headline: the strict-only (gs >= 6) threshold has ZERO PS-True episodes in 2024. Every 2024 PS-True rest-day carries a gevoelscore of exactly 5 or lower (with gs = 5 the exact boundary population).**

- **strict_gs_ge_6 = 0 PS-True episodes in 2024**. This means during 2024, on every rest-day within a K=3 rest-after window of a heavy-episode-end, the participant's gevoelscore was <= 5. No "solid 6+ felt-state" strategic rest occurred within the K=3 window in 2024. This is itself a load-bearing composition observation about 2024. Cannot be run as a 2x2 (PS arm undefined).
- **primary_gs_ge_5 = 15 PS-True (all at gs = 5 exactly)**. RR = 0.93 (the tension).
- **loose_gs_ge_4 = 35 PS-True (adds 20 gs=4 rest-days), 5 crashes on PS arm (adds 2 crashes)**. RR = **0.54** -- shifts substantially TOWARD the pre-committed direction under the borderline-inclusive threshold.

### 6.3 Consistency with candidate (a) small-n artefact

**AMBIGUOUS-FOR candidate (a)**:

- **Under strict_gs_ge_6**: the 2024 PS arm collapses to 0 episodes. This is NOT a "PS RR stays near 1" pattern (which would rule against small-n artefact); it is a "PS arm ceases to exist" pattern, which is a different kind of failure mode: the strict definition simply has no positive observations in 2024. Cannot inform (a).
- **Under loose_gs_ge_4**: the 2024 PS RR shifts from 0.93 to 0.54, moving toward the pre-committed direction. If the small-n artefact were the whole story, the direction would be roughly random across thresholds; the fact that loosening the threshold moves the RR consistently toward < 1 is more consistent with candidate (b) or (e) (residual mechanism at gs = 5 exact boundary) than with pure small-n artefact.

**Combined reading**: threshold sensitivity does not falsify small-n artefact (Wilson CIs remain wide across all thresholds; loose RR = 0.54 has PS Wilson [6.3, 29.4] still overlapping RR = 1). But the direction of the threshold shift is more consistent with a **real residual at the gs = 5 exact boundary** in 2024 -- consistent with candidate (b) partial-mitigation-only where gs = 5 is not a strong-enough felt-state signal to reflect the pre-window cumulative load.

### 6.4 Load-bearing composition observation about 2024

**No 2024 PS-True rest-day carried a gevoelscore of 6 or higher.** This is a hard composition fact: in 2024, whenever the participant rested within 3 days of a heavy-episode-end and had NO prior 3-day crash, their gevoelscore on the rest-day was capped at 5 (or below). Compare to 2023 / 2025 / 2026 where the strict threshold sensitivity would need to be checked separately to see if this is 2024-specific or a general LC-era pattern at K=3 rest-after.

**Reader guidance for MD-beta r2**: the strict_gs_ge_6 threshold is not viable as a primary operand at Stage H if it has zero positive observations in one of the years being pre-registered. The primary threshold should stay at gs >= 5; the loose threshold at gs >= 4 can be a sensitivity companion; the strict threshold at gs >= 6 must be caveated as sample-limited.

---

## 7. Absolute-step-threshold companion (rolling-baseline moves-with-envelope artefact test per Wave 2C section 5.5)

Source: [`output/pssubset_absolute_step_threshold_2024.csv`](output/pssubset_absolute_step_threshold_2024.csv).

**Operational definition**: rest-day = `total_steps < 3000` (absolute) AND gevoelscore >= 5. Rebuild episodes under this operand, recompute proactive-strategic 2x2 for pooled + 2024 + 2023 (as reference). Compare directly to the rolling-p25 rest-day operand results.

### 7.1 Side-by-side 2x2 under both operands

| Pool | Operand | PS-True n / crash | PS-False n / crash | Rate PS-True [Wilson] | Rate PS-False [Wilson] | RR (PS/complement) |
|---|---|---|---|---|---|---:|
| ALL_ERA_POOLED | abs_steps_lt_3000 | 52 / 1 | 260 / 45 | 1.92% [0.3, 10.1] | 17.31% [13.2, 22.4] | **0.111** |
| ALL_ERA_POOLED | rolling_p25 | 80 / 5 | 232 / 41 | 6.25% [2.7, 13.8] | 17.67% [13.3, 23.1] | 0.354 |
| 2024 | abs_steps_lt_3000 | 7 / 1 | 73 / 16 | 14.29% [2.6, 51.3] | 21.92% [14.0, 32.7] | **0.652** |
| 2024 | rolling_p25 | 15 / 3 | 65 / 14 | 20.00% [7.0, 45.2] | 21.54% [13.3, 33.0] | 0.929 |
| 2023 | abs_steps_lt_3000 | 15 / 0 | 72 / 16 | 0.00% [0.0, 20.4] | 22.22% [14.2, 33.1] | 0.000 |
| 2023 | rolling_p25 | 20 / 1 | 67 / 15 | 5.00% [0.9, 23.6] | 22.39% [14.1, 33.7] | 0.223 |

### 7.2 Descriptive observations

**Headline: the absolute-step operand tightens the PS arm and moves the 2024 RR toward < 1, but does not fully resolve the tension.**

- **Pooled**: RR shifts from 0.354 (rolling-p25) to **0.111** (abs). The pooled sign-flip strengthens under the absolute-step operand.
- **2024**: RR shifts from 0.929 (rolling-p25) to **0.652** (abs). Directionally closer to the pre-committed direction, but PS arm shrinks from n = 15 to n = 7 and still carries 1 crash (rate 14.3% vs complement 21.9%). Wilson CI [2.6, 51.3] is very wide.
- **2023**: RR shifts from 0.223 to 0.000 (0 crashes on the abs PS arm). Sign-flip cleanly preserved.
- **Under the absolute-step operand, 2024 PS still has 1 crash-event on 7 episodes**; the tension has narrowed but not disappeared.

### 7.3 Consistency with Wave 2C section 5.5 rolling-baseline artefact concern

The rolling-baseline moves-with-envelope caveat (Wave 2C §5.5) predicted that absolute-step operand results might diverge from rolling-p25 if the step envelope has moved down over time. Findings:

- **Pooled sign-flip is preserved and slightly strengthened under abs operand** (RR 0.354 -> 0.111). The moving-target artefact does not undermine the pooled Wave 2C finding.
- **2024 tension is narrowed but not resolved under abs operand** (RR 0.93 -> 0.65). Suggests the rolling-p25 operand contributed modestly to the 2024 residual (moving-target artefact accounts for maybe ~1/3 of the difference between 2024's RR = 0.93 and 2023's RR = 0.22), but is not the primary driver.
- **2023 sign-flip is preserved cleanly under abs operand** (RR 0.22 -> 0.00). Also consistent with the moving-target artefact not being the dominant driver.

### 7.4 Consistency with candidate readings

- The abs-step operand does NOT resolve the 2024 tension (RR = 0.65 still carries a crash-event; complement rate similar). So candidate (b) / (d) / (e) mechanisms are not attributable to the rolling-p25 operand alone.
- The abs-step operand shrinks the 2024 PS arm to n = 7 with 1 crash; Wilson CI is wider and does not credibly distinguish from RR = 1. Small-n concerns from candidate (a) are AMPLIFIED under the abs-step operand.

**Combined reading**: the moving-target artefact contributed modestly (2024 RR moved 0.93 -> 0.65), but the residual tension (RR > 0 with a crash on the PS arm) survives under both operands. The rolling-baseline artefact is NOT the dominant driver of the 2024 exception.

---

## 8. Per-quarter proactive-strategic RR in 2023 + 2025 (context comparison)

Source: [`output/pssubset_per_quarter_all_years.csv`](output/pssubset_per_quarter_all_years.csv).

Neighbouring-year within-quarter comparison so §3's 2024 within-year pattern can be read against the pattern in the two clean-flip years.

### 8.1 Per-quarter 2023 2x2

| Quarter | n_used | PS-True n / crash | PS-False n / crash | Rate PS-True [Wilson] | Rate PS-False [Wilson] | RR (PS/complement) | viable_n_min5 |
|---|---:|---|---|---|---|---:|:---:|
| 2023 ALL | 87 | 20 / 1 | 67 / 15 | 5.00% [0.9, 23.6] | 22.39% [14.1, 33.7] | **0.223** | yes |
| 2023 Q1 | 26 | 8 / 0 | 18 / 3 | 0.00% [0.0, 32.4] | 16.67% [5.8, 39.2] | 0.000 | yes |
| 2023 Q2 | 25 | 3 / 0 | 22 / 6 | 0.00% [0.0, 56.2] | 27.27% [13.2, 48.2] | 0.000 | **no** (PS n=3) |
| 2023 Q3 | 20 | 6 / 1 | 14 / 4 | 16.67% [3.0, 56.4] | 28.57% [11.7, 54.6] | 0.583 | yes |
| 2023 Q4 | 16 | 3 / 0 | 13 / 2 | 0.00% [0.0, 56.2] | 15.38% [4.3, 42.2] | 0.000 | **no** (PS n=3) |

### 8.2 Per-quarter 2025 2x2

| Quarter | n_used | PS-True n / crash | PS-False n / crash | Rate PS-True [Wilson] | Rate PS-False [Wilson] | RR (PS/complement) | viable_n_min5 |
|---|---:|---|---|---|---|---:|:---:|
| 2025 ALL | 66 | 23 / 0 | 43 / 2 | 0.00% [0.0, 14.3] | 4.65% [1.3, 15.5] | 0.000 | yes |
| 2025 Q1 | 22 | 5 / 0 | 17 / 0 | 0.00% [0.0, 43.4] | 0.00% [0.0, 18.4] | undef (0/0) | yes |
| 2025 Q2 | 16 | 7 / 0 | 9 / 2 | 0.00% [0.0, 35.4] | 22.22% [6.3, 54.7] | 0.000 | yes |
| 2025 Q3 | 13 | 6 / 0 | 7 / 0 | 0.00% [0.0, 39.0] | 0.00% [0.0, 35.4] | undef (0/0) | yes |
| 2025 Q4 | 15 | 5 / 0 | 10 / 0 | 0.00% [0.0, 43.4] | 0.00% [0.0, 27.8] | undef (0/0) | yes |

### 8.3 Descriptive observations

**Headline for 2023**: PS-True crash rate is 0% in 3 of 4 quarters (Q1, Q2, Q4); only 1 event across the whole year (Q3, on 6 PS episodes, 17%). The 2023 sign-flip is broadly-distributed across quarters; no single quarter carries a disproportionate residual.

**Headline for 2025**: PS-True crash rate is 0% in all 4 quarters. Complement arm crashes are 2 events, both in Q2. The 2025 sign-flip is total (no PS crashes anywhere in the year).

**Headline for 2024** (from §3): PS-True crashes are 3 events, concentrated in Q3 (2 events, 40% rate) and Q2 (1 event, 33% rate). Q1 (0/1) and Q4 (0/6) are clean.

### 8.4 Consistency with candidate (c) transition mid-shift

**Descriptively consistent** with a Q3 -> Q4 2024 transition inside a broader 2023 -> 2025 arc:

- **2023 quarter pattern**: crash rate uniformly low across all quarters (0%, 0%, 17%, 0%).
- **2024 quarter pattern**: front-loaded (Q1 clean but too small; Q2 1/3; Q3 2/5 = 40%; Q4 0/6). The Q4 pattern matches 2025 Q1-Q4 (all 0%).
- **2025 quarter pattern**: uniformly 0% across all quarters.

Reading: 2024 Q3 -> 2024 Q4 -> 2025 (all quarters) is a plausible descriptive transition where the residual concentrates in Q2-Q3 2024 and resolves by Q4 2024.

**Caveat**: 2024 Q3 sample size (PS n = 5, 2 crashes) is right at the parent Stage -1 n_min5 threshold; the 40% rate has Wilson [11.8, 76.9]; not credibly distinguishable from RR = 1 or from the 2023 Q3 rate of 17%. The apparent "mid-year transition" reading is fragile.

**Assessment**: AMBIGUOUS. Descriptively consistent with candidate (c) but sample sizes do not support a firm within-year transition claim. The Q4 2024 clean-flip is real, but attributing it to a mid-year shift vs a within-year Q3 outlier cluster is not distinguishable at n = 5/6.

---

## 9. Cumulative-load-in-pre-window comparison for 2024 PS-True crash vs non-crash episodes

Source: [`output/pssubset_2024_pre_window_load.csv`](output/pssubset_2024_pre_window_load.csv).

**Operational definition**: for each of the 15 2024 PS-True episodes, compute the sum + daily-mean of `effective_exertion_min`, `total_steps`, and `vigorous_min` over the 30-day pre-window `[D_start - 30, D_start - 1]`. Group by crash_in_5d True (n = 3) vs False (n = 12).

### 9.1 Per-group aggregate statistics

| Metric | Group | n | mean | median | std |
|---|---|---:|---:|---:|---:|
| pre_effective_exertion_min (30d sum) | crash | 3 | **214.7** | 206.0 | 45.1 |
| pre_effective_exertion_min (30d sum) | non-crash | 12 | 114.8 | 107.6 | 61.1 |
| pre_effective_exertion_min (30d sum) | ALL | 15 | 134.8 | 126.0 | 70.2 |
| pre_effective_exertion_min (30d daily-mean) | crash | 3 | **7.16** | 6.87 | 1.50 |
| pre_effective_exertion_min (30d daily-mean) | non-crash | 12 | 3.83 | 3.59 | 2.04 |
| pre_effective_exertion_min (30d daily-mean) | ALL | 15 | 4.49 | 4.20 | 2.34 |
| pre_total_steps (30d sum) | crash | 3 | 167412 | 163085 | 23184 |
| pre_total_steps (30d sum) | non-crash | 12 | 155381 | 155181 | 15822 |
| pre_vigorous_min (30d sum) | crash | 3 | **44.0** | 47.0 | 6.1 |
| pre_vigorous_min (30d sum) | non-crash | 12 | 27.2 | 21.0 | 12.8 |
| pre_vigorous_min (30d daily-mean) | crash | 3 | **1.47** | 1.57 | 0.20 |
| pre_vigorous_min (30d daily-mean) | non-crash | 12 | 0.91 | 0.72 | 0.42 |

### 9.2 Descriptive observations

**Headline: the 3 crash-cases carry roughly 2x higher pre-window cumulative effective-exertion load than the 12 non-crash baseline cases.**

- **pre_effective_exertion_min 30d sum**: crash mean 214.7 min vs non-crash mean 114.8 min. Ratio 1.87x. Median ratio (206 vs 108) is 1.91x.
- **pre_vigorous_min 30d sum**: crash mean 44.0 min vs non-crash mean 27.2 min. Ratio 1.62x. Median ratio (47 vs 21) is 2.24x.
- **pre_total_steps 30d sum**: crash mean 167k vs non-crash mean 155k. Ratio 1.08x (much smaller separation on steps than on effective_exertion_min or vigorous_min).

The separation is strongest on the **intensity-weighted metrics** (effective_exertion_min, vigorous_min) and weakest on the **volume-only metric** (total_steps). Consistent with an intensity-load-driven pre-window mechanism rather than a raw-volume-driven one.

### 9.3 Consistency with candidate (b) partial-mitigation only

**CONSISTENT-WITH candidate (b) at strong descriptive resolution**. The pre-window intensity-load carries a ~2x separation between crash and non-crash 2024 PS episodes. Gevoelscore >= 5 on the rest-day did NOT reflect this pre-window intensity accumulation. This suggests the residual endogeneity operates through a pre-window intensity-load channel that gevoelscore-on-rest-day does not capture -- a candidate covariate for MD-beta r2 codification.

**Caveat**: n = 3 vs n = 12; the crash-group mean is influenced by any single event. Wilson-style CIs are not applicable to means (this is a per-episode-level aggregate). Standard deviations for the crash group are narrower than for the non-crash group (crash 30d sum std = 45 vs non-crash std = 61); the crash cases are relatively concentrated near the ~200 min mark.

**Not falsifying**: the finding does not rule out that gevoelscore = 5 exact boundary carries a different meaning in 2024 vs 2023 / 2025 (which would be candidate (d) 2024-specific), but the pre-window load pattern is a more direct mechanistic reading.

### 9.4 Reader guidance for MD-beta r2 covariate codification

If MD-beta r2 adopts a pre-window cumulative-load covariate on the rest-adjacency arc, the descriptive signal supports:

- **effective_exertion_min over a 30-day pre-window** as the primary intensity-load metric.
- **vigorous_min over a 30-day pre-window** as a corroborating intensity metric.
- **total_steps over a 30-day pre-window** as a weak / non-discriminating volume metric (do NOT prioritise).

Cut-point selection is out of scope for this Stage -1 audit; the descriptive separation at ~200 min (crash) vs ~115 min (non-crash) on the 30d effective_exertion sum suggests a threshold in the 150-180 min region could be a reasonable candidate for Stage H pre-registration, but this is speculation that a proper Stage D operationalisation session would need to resolve.

---

## 10. Neighbouring-year composition comparison (2023 vs 2024 vs 2025 PS-arm)

Source: [`output/pssubset_2024_neighbouring_context.csv`](output/pssubset_2024_neighbouring_context.csv).

Per-year PS-arm composition on: mean gevoelscore-on-rest-day, mean pre-window activity, mean streak length of the terminal heavy episode, end_class split.

### 10.1 Per-year PS-arm composition

| Year | n_PS_ep | mean_gs_on_rest | median_gs | mean_pre_effex_day | mean_pre_steps_day | mean_streak | median_streak | n_heavy_end | n_vh_end |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| 2023 | 20 | 5.05 | 5.0 | 26.28 | 5429 | 1.40 | 1.0 | 7 | 13 |
| 2024 | 15 | 5.00 | 5.0 | 4.49 | 5294 | 1.27 | 1.0 | 9 | 6 |
| 2025 | 23 | 5.22 | 5.0 | 5.15 | 4931 | 2.09 | 1.0 | 13 | 10 |

### 10.2 Descriptive observations

**Headline: 2024 PS arm is compositionally similar to 2025 on gs-on-rest-day (mean 5.00 vs 5.22, both median 5.0) but distinctly DIFFERENT from 2023 on pre-window activity (mean effective_exertion_min per day 4.49 vs 2023 = 26.28).**

- **mean_gs_on_rest_day**: 2023 = 5.05, 2024 = 5.00, 2025 = 5.22. Essentially flat around 5.0-5.2. The gs-on-rest-day distribution does NOT distinguish 2024 from the neighbouring years.
- **mean_pre_window_effective_exertion_min per day**: 2023 = **26.28**, 2024 = 4.49, 2025 = 5.15. **2023 stands out as ~5x higher** than 2024 or 2025.
- **mean_pre_window_total_steps per day**: 2023 = 5429, 2024 = 5294, 2025 = 4931. Flat across the 3 years.
- **mean_streak_length**: 2023 = 1.40, 2024 = 1.27, 2025 = 2.09. 2025 has the LONGEST mean streaks among the 3 years -- yet the smoothest sign-flip.
- **end_class heavy vs very_heavy**: 2023 = 7/13 (35% heavy), 2024 = 9/6 (60% heavy), 2025 = 13/10 (57% heavy). 2024 has the HIGHEST proportion of heavy-end episodes in the PS arm, but the crashes concentrate on the smaller very_heavy subset (per §4).

### 10.3 The 2023 vs 2024/2025 pre-window activity step-shift (citalopram phase-boundary explanation added at r1 lock post-review absorption per L2.2 substantive fire)

**2023's mean pre-window effective_exertion_min per day of 26.28** vs 2024's 4.49 vs 2025's 5.15 is a 5-6x step-shift at the 2023/2024 boundary. **This is the KNOWN citalopram phase-boundary effect at 2024-04-09** (citalopram onset), documented in [MD-alpha section 3.1 recovery_phase axis](../../../methodology/post_heavy_day_pacing_learning.md#31-phase-axis) + [MD-alpha Wave 2A audit section 8 pre-window mean-level table](../Q24-mdalpha-precursor-phase-intensity/audit.md#8-per-phase-pre-window-mean-level-table-md-alpha-35-level-vs-change-discipline):

- `pacing_habit_established` phase (2022-11-17 -> 2024-04-08; covers most of 2023): full-pool pre-window `effective_exertion_min` mean = **19.39 min/day**.
- `citalopram_modulated` phase (2024-04-09 -> 2026-06-05; covers 2024 post-Apr through 2026 partial): full-pool pre-window `effective_exertion_min` mean = **5.17 min/day**.

Wave 2D's per-year numbers (2023 = 26.28; 2024 = 4.49; 2025 = 5.15) sit on either side of the phase boundary and are consistent with the known citalopram baseline shift. 2023's PS-subset mean of 26.28 sits ABOVE the full-pool phase mean of 19.39 because PS-subset selection (heavy-episode-end + rest-after K=3 + gs >= 5) further elevates pre-window intensity (heavy-episode-ends occur on higher-intensity pre-window days by construction).

**Not a data artefact.** The 5-6x step-shift is a phase-boundary confound driven by citalopram's documented effect on activity capacity, not a data quality issue.

**Implication for Wave 2D section 9 within-2024 finding**: **UNAFFECTED**. All 3 crash-in-5d events in the 2024 PS-True arm are dated 2024-04-26 / 2024-07-11 / 2024-08-24 (all post-2024-04-09 citalopram onset), so section 9's crash-vs-non-crash pre-window comparison is a within-phase (all `citalopram_modulated`) comparison. The 2x pre-window separation (crash mean 214.7 min vs non-crash 114.8 min) is a within-2024 within-phase signal and is not confounded by the phase boundary.

**Implication for section 12.3 pre-window covariate recommendation**: **REQUIRES PHASE-STANDARDISATION**. Any MD-beta r2 codification of pre-window 30d effective_exertion_min as a covariate must be either **phase-standardised** (subtract per-episode phase mean before applying cut-point) or **phase-stratified** (separate cut-points per phase), NOT applied on absolute values across the citalopram boundary. Applying an absolute cut-point (e.g. "pre-window sum > 150 min/day") without phase-standardisation would create a fully-phase-confounded covariate (everything in 2023 above threshold; everything post-2024-04-09 below).

**Reader guidance**: read the 2024 vs 2025 pre-window contrast as reliable (both `citalopram_modulated`, both ~5 min/day). Do NOT compare 2024 pre-window values to 2023 pre-window values in absolute terms without phase-adjustment.

### 10.4 Consistency with candidate readings

- **Candidate (c) transition mid-shift**: **AMBIGUOUS-FOR** at the year-average composition resolution. 2024 PS arm composition is compositionally intermediate between 2023 (higher pre-window load, larger vh proportion in PS) and 2025 (longer streaks, lower vh proportion) but the transition is not clean on any single metric.
- **Candidate (e) intensity-interaction residual**: **AMBIGUOUS-FOR** at the composition resolution. 2024's PS arm has the SMALLEST very_heavy proportion of the three years (6/15 = 40% vs 2023 65% vs 2025 43%), yet all 3 crashes are on the very_heavy subset. This means the residual is not a compositional "2024 had more very_heavy PS episodes" story; it is more like "2024's few very_heavy PS episodes carried disproportionate crash risk".
- **Candidate (b) + (d)**: **AMBIGUOUS-FOR** at the composition resolution. Mean gs-on-rest is flat across years, so 2024 is not compositionally distinct on the gs distribution.

---

## 11. Findings summary -- which candidate readings does the evidence support / refute / leave ambiguous?

### 11.1 Per-candidate summary

**(a) Small-n artefact**: **AMBIGUOUS**.

- §6 threshold sensitivity: strict >= 6 collapses PS arm to n = 0 (uninformative); loose >= 4 moves RR from 0.93 to 0.54 (direction consistent with a real signal), but Wilson CIs remain wide. Does not falsify pure-noise reading; directionally suggests a real signal component.
- §3 per-quarter within 2024: sample sizes drop below n_min5 in Q1 and Q2. Q3 (2/5) has Wilson [11.8, 76.9]; overlaps RR = 1 heavily.
- **Reading**: small-n concerns are real but likely explain only a portion of the 2024 residual. Wave 2D findings suggest the residual has a real signal component beyond pure noise (see (b) + (e)).

**(b) Partial-mitigation only (pre-window cumulative load)**: **CONSISTENT-WITH at strong descriptive resolution**.

- §5.4 + §9: 3 crash-cases have ~2x higher pre-window 30d effective-exertion load (mean 214.7 vs non-crash 114.8 min). Vigorous_min shows similar 2x separation.
- Gevoelscore >= 5 on rest-day does NOT reflect this pre-window intensity accumulation.
- Load-bearing signal for MD-beta r2 covariate codification (see §12).

**(c) Transition-year mid-shift**: **AMBIGUOUS-FOR at fragile sample sizes**.

- §3: PS-True crash rate 40% in Q3 (2/5) -> 0% in Q4 (0/6). Descriptively consistent with a mid-year shift, but Q3 PS n = 5 with Wilson [11.8, 76.9] does not support a firm claim.
- §8: 2023 quarter pattern is broadly-flat (no residual-quarter); 2025 quarter pattern is uniformly zero. 2024 Q3 concentration of PS crashes is unique to 2024 among the 3 years.
- **Reading**: descriptively consistent but not distinguishable from a Q3-outlier reading at n = 5 PS-True episodes.

**(d) Real endogeneity residual specific to 2024**: **AMBIGUOUS-FOR**.

- §5.4: 3 crash-cases cluster in Apr-Aug (Q2-Q3) but 4 of 12 non-crash cases are also in Q3. Seasonality alone does not distinguish.
- No exogenous marker for 2024-specific factors (medication titration, life-event stress cluster) is available in `per_day_master.csv`.
- **Reading**: not tested at descriptive resolution beyond what is inline in §5.

**(e) Intensity-interaction residual**: **CONSISTENT-WITH at strong descriptive resolution**.

- §4: 2024 very_heavy PS-True stratum has RR = 3.50 (3 crashes on 6 episodes); 2024 heavy PS-True stratum has RR = 0.00 (0 crashes on 9 episodes). All 3 crashes are on very_heavy-end episodes.
- §5.2: all 3 crash cases are very_heavy end_class.
- §10.4: not attributable to compositional shift (2024 PS arm has SMALLER vh proportion than 2023 or 2025); the vh episodes in 2024 PS carry disproportionate crash risk.
- Load-bearing signal for MD-beta r2 joint-stratifier codification (see §12).

### 11.2 Multi-candidate reading (tightened at r1 lock post-review absorption per L4.3 substantive fire)

The evidence is most consistent with a **joint reading of (b) + (e)**: within 2024, the very_heavy-end PS episodes with elevated pre-window intensity load carry the residual crash risk that gevoelscore-on-rest-day does not detect. Candidate (a) small-n and (c) transition are partial background contributors (Wilson CIs remain wide; Q3 concentration is descriptively real but fragile). Candidate (d) 2024-specific real residual is not testable at this audit's data resolution.

**Definitional-pair discipline per [CONVENTIONS section 3.3](../../../CONVENTIONS.md#33-one-column-per-definitional-pair) on the joint (b) + (e) framing**: candidate (b) partial-mitigation-via-pre-window-load is tested at TWO DIFFERENT operational channels within this audit:

- **section 6 threshold-sensitivity channel** tests whether raising the gevoelscore boundary (>= 5 -> >= 6 strict-only) reduces residual crash risk on the PS arm. Finding: strict >= 6 collapses to n=0 in 2024; loose >= 4 moves RR from 0.93 to 0.54; the direction of the shift under loose threshold is consistent with a real gevoelscore-boundary-specific residual (candidate b as gevoelscore-scale insufficient).
- **section 9 pre-window-load-magnitude channel** tests whether crash cases within the PS arm are characterised by higher pre-window cumulative activity. Finding: 2024 crash-cases carry ~2x higher pre-window 30d effective_exertion_min sum (mean 214.7 vs non-crash 114.8) at n=3 vs n=12 narrative-only resolution (candidate b as pre-window-load carries additional signal not captured by gevoelscore).

**These are distinct empirical channels of the same candidate (b) mechanism, not independent evidence for a common conclusion.** Per [CONVENTIONS section 3.3](../../../CONVENTIONS.md#33-one-column-per-definitional-pair) discipline, any downstream Stage H pre-registration or MD-beta r2 codification that adopts pre-window cumulative load as a covariate must pick ONE of {threshold-shift, load-magnitude} as the primary channel and the other as sensitivity companion; they are not independently-evidencing at Stage S1 (internal synthesis).

Candidate (e) intensity-interaction is tested at ONE channel (section 4 within-2024 by-intensity 2x2 + section 5.2 all-3-crashes-on-vh confirmation). The candidate (e) evidence is not itself a definitional-pair internally; it is a single-channel finding.

The joint (b) + (e) reading combines TWO independently-observed mechanism-signals (pre-window load + end_class intensity) that operate at different granularities (episode-level vs intra-episode-composition-level). They are complementary characterisations of the same residual, NOT independent evidence for a single mechanism.

### 11.3 What Wave 2D supports / falsifies / leaves ambiguous for MD-beta r2

**SUPPORTS** (evidence for MD-beta r2 to adopt):

- Joint intensity + gevoelscore stratification: gevoelscore-on-rest-day is insufficient on its own within very_heavy-end PS episodes; end_class should be a joint primary stratifier alongside gevoelscore.
- Pre-window cumulative-load (30d effective_exertion_min or vigorous_min) as a candidate covariate on the rest-adjacency arc.

**FALSIFIES** (evidence against MD-beta r2 adopting):

- The strict_gs_ge_6 threshold as a viable primary operand at Stage H (2024 has zero PS-True episodes under this threshold; sample-limited).
- The rolling-baseline moves-with-envelope artefact as the dominant driver of the 2024 tension (abs-step operand narrows the tension modestly, from RR 0.93 to 0.65, but does not resolve it).

**LEAVES AMBIGUOUS**:

- Whether the 2024 residual is primarily (b) pre-window intensity-load, (e) intensity-interaction, or a joint (b) + (e) mechanism. Both are strongly consistent with the descriptive evidence but sample sizes do not distinguish them cleanly.
- Whether candidate (c) transition mid-shift is a distinct mechanism or a Q3-outlier reading.
- The 2023 pre-window activity anomaly (mean effective_exertion_min per day = 26.28 vs 2024 / 2025 ~5) -- flagged as reviewer concern.

---

## 12. Reader guidance -- what does this mean for MD-beta r2 codification of gevoelscore-conditioning?

**Reader**: the MD-beta r2 downstream session author (whoever picks up the rest-adjacency arc codification after Wave 2D absorption).

### 12.1 Wave 2D refines the Wave 2C section 10.5 (a) definitional-pair recommendation

Wave 2C section 10.5 (a) recommended MD-beta r2 codify `rest_day_p25_strategic` + `rest_day_p25_crisis` as a definitional pair. Wave 2D findings refine this:

- **Primary operand for the strategic member**: keep `rest_day_p25` (rolling baseline; primary from MD-beta section 3.1) AND `gevoelscore >= 5` (primary from Wave 2C section 5). The strict >= 6 threshold is NOT viable as a primary at Stage H (2024 zero-observation problem per §6.2 + §6.4).
- **Absolute-step sensitivity companion (per Wave 2C section 5.5)**: keep as codified in Wave 2C; §7 confirms the sign-flip is preserved under abs-step operand at the pooled level.
- **Loose-threshold sensitivity companion (>= 4)**: consider adding as a definitional-pair sensitivity per [CONVENTIONS section 3.3](../../../CONVENTIONS.md#33-one-column-per-definitional-pair) -- §6.1 shows the direction of the 2024 RR moves toward the pre-committed direction under the loose threshold (0.93 -> 0.54), suggesting a real residual at the gs = 5 exact boundary in 2024.

### 12.2 Wave 2D adds a JOINT-STRATIFIER recommendation for end_class

**Load-bearing new recommendation from Wave 2D §4**: end_class (heavy vs very_heavy) should be a JOINT PRIMARY STRATIFIER alongside gevoelscore-on-rest-day for any Stage H pre-registration on the rest-adjacency arc. Rationale:

- Within 2024 PS-True, end_class = heavy has RR = 0.00 (clean flip); end_class = very_heavy has RR = 3.50 (sign-inverted). The gevoelscore-conditioning alone is not sufficient to reveal the pre-committed direction within very_heavy-end episodes.
- This is consistent with the parent Wave 2B section 10 finding that heavy-terminal and very_heavy-terminal episodes carry different sign-directions; Wave 2D extends this to WITHIN the proactive-strategic subset.

MD-beta r2 codification suggestion: report the rest-adjacency 2x2 stratified simultaneously by (rest-day gevoelscore bucket) x (end_class), not just by gevoelscore bucket alone.

### 12.3 Wave 2D adds a PRE-WINDOW COVARIATE recommendation

**Load-bearing new recommendation from Wave 2D §5 + §9**: pre-window cumulative effective_exertion_min (30d) is a candidate covariate on the rest-adjacency arc. Rationale:

- 2024 PS-True crash cases carry ~2x higher pre-window 30d effective_exertion_min sum (mean 214.7 min) than non-crash cases (mean 114.8 min).
- Gevoelscore-on-rest-day does NOT reflect this pre-window intensity accumulation.
- This is a candidate mechanistic explanation for the residual endogeneity that gevoelscore-conditioning does not fully mitigate.

MD-beta r2 codification suggestion: add pre-window 30d effective_exertion_min as either a **covariate** on the rest-adjacency 2x2 (via a matched-comparator design or stratified within pre-window load quartiles) or as an **additional stratifier** at Stage H. Cut-point selection is out of scope for this audit; the descriptive separation at ~150-180 min on the 30d sum suggests a rough starting point.

### 12.4 What Wave 2D does NOT recommend

- Wave 2D does NOT recommend abandoning the gevoelscore-conditioning primary operand. The pooled RR = 0.354 (Wave 2C) + 2023 RR = 0.223 + 2025 / 2026 RR = 0.000 sign-flips all preserved. The 2024 residual is a caveat, not a falsification of the primary operand.
- Wave 2D does NOT recommend a specific pre-window load cut-point at Stage H. Cut-point selection needs a Stage D operationalisation session or an explicit descriptive-with-CI pre-registration on the cut-point itself.
- Wave 2D does NOT resolve whether the 2024 residual is (b), (e), or (b) + (e); both are strongly-consistent descriptive readings and the sample sizes do not distinguish them.

### 12.5 Decision the MD-beta r2 author must make

Given the evidence, the MD-beta r2 author has three viable codification paths:

- **Path R2A -- minimal codification**: keep gevoelscore-conditioning as-is per Wave 2C section 10.5 (a); flag 2024 residual as caveat-class per [CONVENTIONS section 4.2](../../../CONVENTIONS.md#42-caveats-yes-a-priori-claims-no). Do NOT add end_class or pre-window covariate.
- **Path R2B -- joint-stratifier extension**: add end_class as a joint primary stratifier (per §12.2). Pre-window covariate deferred to Stage H pre-registration as its own definitional-pair. Wave 2D §4 + §5 + §9 support this.
- **Path R2C -- full extension**: joint end_class stratifier AND pre-window 30d effective_exertion_min covariate. Most defensible against Stage H reviewer scepticism but adds definitional-pair count that may exceed [CONVENTIONS section 3.3](../../../CONVENTIONS.md#33-one-column-per-definitional-pair) discipline.

The choice among R2A / R2B / R2C is a methodology-editing decision for the r2 author + user, NOT a Stage -1 descriptive-audit decision. Wave 2D's role is to provide the descriptive evidence; the codification decision is downstream.

---

## 13. Reviewer-concerns for a fresh-session walk

1. **§3 per-quarter Q3 concentration**: 2024 Q3 PS-True has 2 crashes on 5 episodes (Wilson [11.8, 76.9]). This is right at the n_min5 threshold. Fresh-session reviewer should decide whether §3.2 + §3.3 are adequately caveated for the fragile sample size, or whether the "Q3 -> Q4 mid-year shift" reading in §3.3 overreaches given the CI.

2. **§4 by-intensity within 2024**: RR = 3.50 on 2024 very_heavy PS-True (n = 6, 3 crashes) with Wilson [18.8, 81.2]. Directionally strong signal but very wide CI. Fresh-session reviewer should confirm whether §4.4 CONSISTENT-WITH candidate (e) framing is adequate, or whether the strength of the descriptive signal warrants a firmer framing.

3. **§5 per-episode diagnostic n = 3**: the crash-vs-non-crash comparison is n = 3 vs n = 12. Per memory `feedback_narrative_only_events`, this is narrative-only. Fresh-session reviewer should confirm the §5 narrative-only framing is adequate (no inferential statistic computed) and the load-bearing pre-window observation in §5.4 is appropriately qualified.

4. **§5 rest-day date privacy**: the per-episode diagnostic emits episode-start / episode-end / rest-day dates. Per task instruction "OK to emit dates in per-episode diagnostic" (dates already in the corpus and prior audit reports have used them). Fresh-session reviewer should confirm this is aligned with prior audit conventions.

5. **§6 strict_gs_ge_6 zero-observation problem**: no 2024 PS-True episodes have gs >= 6 on the rest-day. This is a hard sample-availability constraint that rules out the strict threshold as a primary operand at Stage H. Fresh-session reviewer should confirm whether §6.4 reader-guidance on this is adequate, and whether Wave 2D should recommend checking the strict-threshold availability in 2023 / 2025 / 2026 as a companion (currently not in scope).

6. **§7 abs-step operand narrows the tension only modestly**: 2024 RR shifts 0.93 -> 0.65 under abs-step. Fresh-session reviewer should decide whether the moving-target artefact is adequately characterised as "modest contributor, not dominant driver" or whether the shift from 0.93 to 0.65 (a ~30% reduction) warrants a stronger claim about the rolling-baseline operand.

7. **§9 pre-window 2x separation at n = 3 vs n = 12**: crash-group mean 214.7 min vs non-crash 114.8 min on 30d effective_exertion. Fresh-session reviewer should decide whether the ~2x separation is descriptively load-bearing enough to justify §12.3's pre-window covariate recommendation, or whether the n = 3 crash-group mean is too fragile to build MD-beta r2 codification on.

8. **§10.3 2023 pre-window activity anomaly**: mean effective_exertion_min per day = 26.28 in 2023 PS arm vs 4.49 in 2024 and 5.15 in 2025. This is a 5-6x anomaly not explained in this audit. Fresh-session reviewer should decide whether this warrants a Wave 2E or a data-diagnostic companion, or whether §10.3's "flagged as reviewer concern" caveat is sufficient.

9. **§11.2 joint (b) + (e) reading**: the audit reads the evidence as most consistent with a joint (b) + (e) mechanism. Fresh-session reviewer should decide whether this is an appropriate multi-candidate framing per §2 discipline (candidate readings are not mutually exclusive), or whether the audit should more explicitly refuse to prioritise a single reading.

10. **§12 MD-beta r2 recommendation surface**: §12.2 + §12.3 make new load-bearing recommendations (joint end_class stratifier + pre-window covariate) that go beyond Wave 2C section 10.5 (a). Fresh-session reviewer should decide whether these recommendations are appropriately narrow (point at codification, do not draft it) or whether they overreach into methodology-editing territory that should be out of scope for a Stage -1 audit.

11. **Discipline scope -- descriptive-only framing**: no verdicts, no p-values, all rates + RRs reported with Wilson CI. Fresh-session reviewer should confirm this discipline is honoured across all sections and no candidate reading is treated as "verdicted".

12. **Reading discipline -- narrative-only per §2 for n = 3 events**: the 3 crash-events in §5 are treated as narrative-only per [memory feedback_narrative_only_events]. Fresh-session reviewer should confirm this treatment is applied consistently in §5 + §9 + §11.

---

## 14. Lock log

- **DRAFT r0 2026-07-16**: initial draft by Claude (Opus 4.7) in producer-mode subagent per [CONVENTIONS section 1.1](../../../CONVENTIONS.md#11-producer-mode-claude-writes--edits--runs). Authorising user: Willem. Wave 2D sibling of parent [Wave 2C Stage -1 audit LOCKED r1 2026-07-16](../Q24-mdbeta-wave2c-reactive-vs-proactive-rest/audit.md). Pending fresh-session methodology-review absorption before LOCK. Next-step in user-endorsed sequence: fresh-session reviewer walks Wave 2D, absorbs fires, then MD-beta r2 is drafted informed by BOTH Wave 2C section 10.5 (a) definitional-pair recommendation AND Wave 2D §12.2 + §12.3 joint-stratifier + pre-window covariate recommendations.
- **r1 LOCKED 2026-07-16**: Fresh-session methodology review absorbed from [`../../../reviews/methodology-Q24-mdbeta-wave2d-2024-residual-tension-2026-07-16.md`](../../../reviews/methodology-Q24-mdbeta-wave2d-2024-residual-tension-2026-07-16.md) (verdict: DEFENSIBLE with revision; 2 audit-level absorb fires + explicit codification-path recommendation for MD-beta r2 downstream). Two surgical patches applied per [CONVENTIONS section 1.2](../../../CONVENTIONS.md#12-reviewer-mode-claude-reads--writes-a-reasoned-report--recommendations) compression discipline (mechanical clarifications only; no architectural change). **Patch 1** (section 10.3, review L2.2 substantive absorb): the "2023 pre-window activity anomaly" (26.28 vs 2024/2025 ~5) reframed from data-artefact-vs-real-behaviour ambiguity to the KNOWN citalopram phase-boundary effect at 2024-04-09 (verified against MD-alpha section 3.1 recovery_phase axis + MD-alpha Wave 2A audit section 8 pre-window mean-level table: `pacing_habit_established` = 19.39 vs `citalopram_modulated` = 5.17 min/day; Wave 2D per-year numbers sit on either side of the phase boundary consistent with the known shift). Section 10.3 also documents that section 9 within-2024 crash-vs-non-crash comparison is UNAFFECTED (all 3 crash events dated 2024-04-26 / 2024-07-11 / 2024-08-24 are all post-citalopram-onset, so section 9 is a within-`citalopram_modulated`-phase comparison). Section 10.3 further adds implication for section 12.3 pre-window covariate recommendation: any MD-beta r2 codification of the covariate MUST be phase-standardised or phase-stratified, NOT applied on absolute values across the citalopram boundary. **Patch 2** (section 11.2, review L4.3 substantive absorb): joint (b) + (e) multi-candidate reading tightened per [CONVENTIONS section 3.3](../../../CONVENTIONS.md#33-one-column-per-definitional-pair) definitional-pair discipline. Section 6 (threshold-sensitivity channel) + section 9 (pre-window-load-magnitude channel) explicitly named as TWO DIFFERENT operational channels testing the SAME candidate (b) mechanism; not independent evidence for a common conclusion. Section 4 (candidate e) is a single-channel finding, not a definitional pair internally. Joint (b) + (e) is complementary characterisation of the same residual at different granularities (episode-level pre-window load vs intra-episode-composition intensity), NOT independent evidence for a single mechanism. **Reviewer's Path R2B codification recommendation for MD-beta r2**: joint end_class stratifier NOW; pre-window covariate DEFERRED to Stage H pre-registration. Reviewer rejected Path R2A (section 4 signal has internal replication via section 5.2 + inherits from Wave 2B section 10; not a lone fragile finding) and Path R2C (codifying pre-window covariate at r2 requires phase-standardisation which this audit does not compute, or phase-stratification which stresses definitional-pair discipline, and risks overfitting two mechanism-hypotheses to n=3 crash events). Path R2B is supported by two audits reading the same intensity pattern, is not sensitive to the citalopram phase-boundary confound, and is already partially codified via parent Wave 2B section 13.10 Path A upgrade. Preserved byte-identically: section 1 corpus summary + Wave 2C anchor, section 2 five candidate readings recap, sections 3-9 all tables + descriptive observations (no numerical revision), section 10.1-10.2 + 10.4 (only 10.3 reframed), section 11.1 per-candidate summary + section 11.3 support/falsify/ambiguous, section 12 R2A/R2B/R2C paths surfaced (r2 author + user pick per user-endorsed sequence), section 13 reviewer-concerns list, section 14 lock log DRAFT entry. **STATUS**: LOCKED r1 2026-07-16 post-review absorption. Next-step in user-endorsed sequence: MD-beta r2 drafted via reviewer-recommended Path R2B informed by Wave 2C section 10.5 (a) + Wave 2D section 12.2 (joint end_class stratifier now) + Wave 2D section 12.3 (pre-window covariate deferred to Stage H per Path R2B).

Producer-mode discipline attestations:

- Parent MDs (MD-alpha, MD-beta), CONVENTIONS, and the three prior audits (Wave 2A, 2B, 2C) NOT edited by this session.
- Named counts per [CONVENTIONS section 3.6](../../../CONVENTIONS.md#36-name-every-count-n-unit-per-scheme-in-file): all cell counts + rates carry scheme (K=3 rest-after primary, proactive-strategic subset, PS = proactive-strategic) + unit (episode / rest-day / event) + source CSV filename in-text.
- Zero-vs-NaN discipline per [CONVENTIONS section 3.10 NaN-boundary rule (parent Q24 MD "zero-vs-NaN" shorthand inherited from `bout_level_recovery_dynamics.md`)](../../../CONVENTIONS.md#310-operationalisation-faithful-to-the-data-not-just-to-the-description): `is_crash.fillna(False).astype(bool)` only; gevoelscore NaN preserved as its own bucket via `_bucket_from_gs`; rest_day_p25 NaN preserved via inherited Wave 2B `_rest_indicator` logic.
- No emoji, no em-dash in outputs or narrative.
- Idempotent script per [CONVENTIONS section 3.6](../../../CONVENTIONS.md#36-name-every-count-n-unit-per-scheme-in-file): re-runnable, no `datetime.now()`, byte-identical CSVs on identical input. `RANDOM_SEED = 20260716` declared per MD-beta section 3.6, not exercised.
- Descriptive-with-CI framing per [CONVENTIONS section 2.1](../../../CONVENTIONS.md#21-descriptive-before-inference): no verdicts, no p-values, Wilson 95% CIs on all rates, RR + RD reported with per-arm cell counts.
- Per-episode diagnostic discipline per [memory feedback_narrative_only_events]: 3-vs-12 comparison in §5 + §9 is narrative-only; no inferential statistic computed.
- Candidate-reading discipline per §2: all 5 candidate readings partial-testable at n = 1; findings framed as CONSISTENT-WITH / AMBIGUOUS-FOR / FALSIFYING; joint-reading multi-candidate framing per §11.2.
- Physical-rest-only semantic constraint (memory `project_rest_day_operand_semantics`) inherited from Wave 2C section 2.1; not re-emitted.
