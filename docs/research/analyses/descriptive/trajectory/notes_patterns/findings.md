# `trajectory/notes_patterns/` -- findings (Q4.7 note-categorisation patterns)

## Authorship

- **Computed**: 2026-06-26 by Claude (Opus 4.7) via [`run.py`](run.py) under the user-LOCKED operationalisation in [`README.md`](README.md) (Strand B section 7c interview 2026-06-26).
- **Data**: `per_day_master.csv` at `$GEVOELSCORE_DATA_PATH/unified/`; as-of-date **2026-06-04**; coverage window **2022-09-03** -> **2026-06-04** (Stratum 4; gevoelscore corpus start). **1371 day-level rows**; **685 has_note=True rows** (write-rate 50.0% over the window).
- **Axes**: 6-phase LC recovery axis from [`methodology/lc_recovery_phase_axis.md`](../../../../methodology/lc_recovery_phase_axis.md) (LOCKED `d47e0d3` 2026-06-19) + 5-phase citalopram axis from [`methodology/citalopram_phase_stratification.md`](../../../../methodology/citalopram_phase_stratification.md) section 3.
- **BINDING discipline**: [`methodology/symptom_mention_asymmetry.md`](../../../../methodology/symptom_mention_asymmetry.md) LOCKED 2026-06-11 -- LOAD-BEARING for every framing in this document. Per the rule (asymmetry MD section 1): **a mention is high-specificity positive evidence; absence of mention is NOT evidence of absence** (5 distinct causes per asymmetry MD section 2; only one is symptom-absent). Per asymmetry MD section 3: v24 CANNOT do prevalence trajectories; v24 CAN do stratify-by-content + conditional-on-note share. `has_note` IS daily_computed -- its trajectory IS clean (Layer A); v24 cat_* columns are presence_conditioned (Layer B; conditional-on-note share only per user-locked choice 4).
- **Layer 1 descriptive per [CONVENTIONS section 2.1 + section 4.3](../../../../CONVENTIONS.md)**: NO causal claims; NO `SUPPORTED` bar; NO `REFUTED` mark. Per CONVENTIONS section 4.2 caveat-class: Layer-B findings reported as `share-of-clauses on cluster X is Y conditional-on-note in phase Z` -- **NEVER** `cluster X is more prevalent in phase Z`. The 5-cause-of-absence rule is invoked at every Layer-B reading.
- **Cross-references**: [`run.py`](run.py) + [`summary.json`](summary.json) (gitignored) + [`plots/`](plots/) (5 PNGs, gitignored). Per-stage numbers below trace to the JSON.

---

## Headline

**Layer A (write-rate; daily_computed; trajectory-clean)**:

- Per-recovery-phase write-rate: `lc_pre_ergo`=0.0% (n=19); `pacing_pre_citalopram_learning`=25.0% (n=56); `pacing_habit_established`=47.9% (n=509); `citalopram_modulated`=54.3% (n=787).
- Per-citalopram-phase write-rate: `unmedicated`=44.2% (n=584); `buildup`=84.7% (n=72); `consolidation`=50.6% (n=638); `afbouw`=55.8% (n=77).
- Per-DOW write-rate: chi2 across 7 days p=0.2036 (dof=6); weekday=50.7% vs weekend=48.2% (chi2 2x2 p=0.4473). **SISTER to Q4.8 Stage 4 on Garmin channels**.
- Per-month write-rate: chi2 across 12 months p=0.0000 (dof=11). **SISTER to Q4.8 Stage 3 on Garmin channels**.
- has_note <-> gevoelscore correlation (on n=1371 shared-coverage rows): Spearman rho=-0.2109 (p=0.0000); chi2 2x3 across score-tertiles p=0.0000. **Descriptive only** per CONVENTIONS section 4.2; does NOT imply low score causes writing.

**Layer B (within-note share; presence_conditioned; conditional-on-note ONLY per user-locked choice 4)**:

- Per-recovery-phase top-3 cluster-share spreads (conditional-on-note):
  - `cat_symptoom_fysiek`: spread=30.9% (pacing_pre_citalopram_learning=68.8%, pacing_habit_established=39.8%, citalopram_modulated=37.9%).
  - `cat_context_neutraal`: spread=13.7% (pacing_pre_citalopram_learning=28.8%, pacing_habit_established=42.6%, citalopram_modulated=42.3%).
  - `cat_belasting_gezin`: spread=7.5% (pacing_pre_citalopram_learning=1.8%, pacing_habit_established=4.8%, citalopram_modulated=9.3%).
- Per-citalopram-phase top-3 cluster-share spreads (conditional-on-note):
  - `cat_symptoom_fysiek`: spread=20.4% (unmedicated=41.4%, buildup=54.9%, consolidation=35.2%, afbouw=34.5%).
  - `cat_context_neutraal`: spread=13.0% (unmedicated=41.8%, buildup=33.7%, consolidation=43.4%, afbouw=46.7%).
  - `cat_belasting_gezin`: spread=5.2% (unmedicated=4.6%, buildup=7.5%, consolidation=9.8%, afbouw=7.7%).
- Per-event-class top-3 cluster-share spreads (conditional-on-note; **Q4.4 sister**):
  - `cat_symptoom_fysiek`: spread=31.6% (crash=59.4%, dip=65.6%, normal=34.0%).
  - `cat_context_neutraal`: spread=24.1% (crash=26.8%, dip=22.1%, normal=46.1%).
  - `cat_belasting_gezin`: spread=6.7% (crash=1.9%, dip=3.6%, normal=8.6%).
- Per-Q4.3-boundary top conditional-share delta (post minus pre, +/-30d window):
  - `rp4_4a_to_4b` (2022-11-17; n_pre=14 n_post=5): top shift = `cat_symptoom_fysiek` delta=-23.8% (pre=68.8% post=45.0%).
  - `rp5_4b_to_citalopram_modulated` (2024-04-09; n_pre=27 n_post=28): top shift = `cat_symptoom_fysiek` delta=23.2% (pre=26.8% post=50.0%).
  - `cp3_consolidation_to_afbouw` (2026-03-20; n_pre=12 n_post=8): top shift = `cat_symptoom_cognitief` delta=15.6% (pre=0.0% post=15.6%).

**CRITICAL FRAMING per asymmetry MD section 3 + CONVENTIONS section 4.2**: every Layer-B number above is a `share-of-clauses-conditional-on-note`. A higher cluster share in phase Z relative to phase Y does **NOT** support the claim that the corresponding symptom/topic is more prevalent in phase Z. The 5-cause-of-absence rule (asymmetry MD section 2) applies: a lower share could equally reflect (1) symptom absent, (2) symptom present but unworthy of writing, (3) symptom present but crowded out by another topic, (4) symptom present but routine/habituated, or (5) the day's note simply did not exist (which the Layer-A write-rate analysis exposes is itself unequally distributed across phases).

---

## 1. Layer A Stage 2 -- write-rate per-recovery-phase

**Method**: per phase, count `has_note=True` rows / total rows in phase. `has_note` is daily_computed; the trajectory is CLEAN per asymmetry MD section 3 (the daily_computed family that includes `gevoelscore`, Garmin biometric channels, coverage flags).

| phase | n_days | n_notes | P(has_note) |
|---|---:|---:|---:|
| `pre_illness_healthy` | 0 | 0 | n/a |
| `acute_infection` | 0 | 0 | n/a |
| `lc_pre_ergo` | 19 | 0 | 0.0% |
| `pacing_pre_citalopram_learning` | 56 | 14 | 25.0% |
| `pacing_habit_established` | 509 | 244 | 47.9% |
| `citalopram_modulated` | 787 | 427 | 54.3% |

**Reading**: write-rate trajectory across the 6-phase recovery axis is fair to characterise (this is a daily_computed signal). `pre_illness_healthy` + `acute_infection` predate the notes corpus (user started writing 2022-10-18, within `lc_pre_ergo`); these phases show 0% write-rate by construction, NOT because the user was healthier or because nothing was worth writing about.

---

## 2. Layer A Stage 3 -- write-rate per-citalopram-phase

**Method**: per phase, count `has_note=True` rows / total rows in phase. Phase boundaries per [`citalopram_phase_stratification.md`](../../../../methodology/citalopram_phase_stratification.md) section 3.

| phase | n_days | n_notes | P(has_note) |
|---|---:|---:|---:|
| `unmedicated` | 584 | 258 | 44.2% |
| `buildup` | 72 | 61 | 84.7% |
| `consolidation` | 638 | 323 | 50.6% |
| `afbouw` | 77 | 43 | 55.8% |
| `post_afbouw` | 0 | 0 | n/a |

---

## 3. Layer A Stage 4 -- write-rate per-DOW (Q4.8 sister on `has_note`)

**Method**: per day-of-week, count `has_note=True` rows / total rows on that DOW. Chi-square 2x7 contingency test across the 7 day-groups (more natural than KW for a binary outcome). Weekday-vs-weekend chi-square 2x2. **Sister analysis** to [`trajectory/seasonality_dow/`](../seasonality_dow/findings.md) Stage 4 on the 6 Garmin channels.

| DOW | n_days | n_notes | P(has_note) |
|---|---:|---:|---:|
| Mon | 196 | 93 | 47.4% |
| Tue | 196 | 103 | 52.6% |
| Wed | 196 | 114 | 58.2% |
| Thu | 196 | 97 | 49.5% |
| Fri | 195 | 89 | 45.6% |
| Sat | 196 | 92 | 46.9% |
| Sun | 196 | 97 | 49.5% |

**Across 7 days**: chi2 statistic = 8.50 (dof=6), p = 0.2036 (no-flag at p<0.05).

**Weekday vs weekend**: P(weekday)=50.7% (n=979) vs P(weekend)=48.2% (n=392); chi2 2x2 p=0.4473 (no-flag at p<0.05).

**Reading per CONVENTIONS section 4.2 caveat-class**: a SUSPECT flag indicates a non-uniform write-rate across DOWs at p < 0.05. This is a DESCRIPTIVE substrate; mechanism (e.g. weekend habit shift, work-week structuring) is out of scope.

---

## 4. Layer A Stage 5 -- write-rate per-month (Q4.8 sister)

**Method**: per calendar-month, count `has_note=True` rows / total rows in that month. Chi-square 2x12 contingency. **Sister analysis** to [`trajectory/seasonality_dow/`](../seasonality_dow/findings.md) Stage 3.

| month | n_days | n_notes | P(has_note) |
|---|---:|---:|---:|
| Jan | 124 | 53 | 42.7% |
| Feb | 113 | 64 | 56.6% |
| Mar | 124 | 67 | 54.0% |
| Apr | 120 | 84 | 70.0% |
| May | 124 | 84 | 67.7% |
| Jun | 94 | 76 | 80.9% |
| Jul | 93 | 62 | 66.7% |
| Aug | 93 | 35 | 37.6% |
| Sep | 118 | 34 | 28.8% |
| Oct | 124 | 36 | 29.0% |
| Nov | 120 | 40 | 33.3% |
| Dec | 124 | 50 | 40.3% |

**Across 12 months**: chi2 statistic = 153.00 (dof=11), p = 0.0000 (**SUSPECT** at p<0.05).

---

## 5. Layer A Stage 6 -- has_note <-> gevoelscore correlation

**Method**: on rows where both `has_score=True` and `has_note` is defined (it is defined for all rows in Stratum 4; the gate is on `has_score`). Score-bin contingency (low=1-2, mid=3, high=4-5) + Spearman rho. **In the same family as Q4.6 MCAR diagnostic**: missingness in v24 is structured, not random; this stage characterises one specific dimension of the structure (score-conditional write-rate).

**Shared-coverage rows (has_score=True)**: 1371.

| score bin | n_days | n_notes | P(has_note) |
|---|---:|---:|---:|
| low_1_2 | 39 | 22 | 56.4% |
| mid_3 | 152 | 111 | 73.0% |
| high_4_5 | 1103 | 519 | 47.1% |

**Spearman rho(gevoelscore, has_note)** = -0.2109; p = 0.0000 (**SUSPECT** at p<0.05).
**Chi-square 2x3 (note x score-tertile)**: chi2 = 36.63 (dof=2), p = 0.0000 (**SUSPECT** at p<0.05).

**Reading per CONVENTIONS section 4.2**: a SUSPECT correlation is a DESCRIPTIVE observation that write-propensity covaries with self-reported felt-state. It does NOT imply (a) low score causes writing, (b) writing causes low score, or (c) the underlying symptom prevalence at low-score-days differs from high-score-days. Per Q4.6 the MAR/MNAR character of v24 missingness is structured; this stage characterises one dimension of the structure.

---

## 6. Layer B Stage 7 -- within-note share per-recovery-phase

**Method**: filter to `has_note=True` rows. For each (cluster, phase) cell, compute `mean(cluster_count / n_clauses)` across days in the phase (each note weighted equally). The number is the **conditional-on-note mean cluster-share**; per asymmetry MD section 3 it does NOT estimate prevalence. The state_symptoom categorical columns + day_dominant_polarity get separate categorical distributions; neutral_forward_looking_flag gets a boolean rate.

**Conditional-on-note mean cluster-share x recovery_phase** (values as percent of clauses):

| cluster | pre_illness_healthy | acute_infection | lc_pre_ergo | pacing_pre_citalopram_learning | pacing_habit_established | citalopram_modulated |
|---|---:|---:|---:|---:|---:|---:|
| `cat_belasting_cognitief` | n/a | n/a | n/a | 3.6% | 2.6% | 1.2% |
| `cat_belasting_emotioneel` | n/a | n/a | n/a | 0.7% | 1.0% | 0.9% |
| `cat_belasting_fysiek` | n/a | n/a | n/a | 0.0% | 4.9% | 3.1% |
| `cat_belasting_gezin` | n/a | n/a | n/a | 1.8% | 4.8% | 9.3% |
| `cat_belasting_sociaal` | n/a | n/a | n/a | 0.0% | 0.8% | 2.4% |
| `cat_symptoom_cognitief` | n/a | n/a | n/a | 0.0% | 1.7% | 3.1% |
| `cat_symptoom_emotioneel` | n/a | n/a | n/a | 0.0% | 0.1% | 0.0% |
| `cat_symptoom_fysiek` | n/a | n/a | n/a | 68.8% | 39.8% | 37.9% |
| `cat_medicatie` | n/a | n/a | n/a | 0.0% | 0.1% | 2.4% |
| `cat_recovery_actie` | n/a | n/a | n/a | 7.1% | 6.1% | 6.1% |
| `cat_triggers_extern` | n/a | n/a | n/a | 0.0% | 0.6% | 0.1% |
| `cat_context_neutraal` | n/a | n/a | n/a | 28.8% | 42.6% | 42.3% |

**n_notes per phase**: `pre_illness_healthy` n_notes=0; `acute_infection` n_notes=0; `lc_pre_ergo` n_notes=0; `pacing_pre_citalopram_learning` n_notes=14; `pacing_habit_established` n_notes=244; `citalopram_modulated` n_notes=427.

**Conditional-on-note boolean flag `neutral_forward_looking_flag` x recovery_phase**:

| phase | n_notes | n_with_value | n_true | rate (conditional) |
|---|---:|---:|---:|---:|
| `pre_illness_healthy` | 0 | 0 | 0 | n/a |
| `acute_infection` | 0 | 0 | 0 | n/a |
| `lc_pre_ergo` | 0 | 0 | 0 | n/a |
| `pacing_pre_citalopram_learning` | 14 | 14 | 0 | 0.0% |
| `pacing_habit_established` | 244 | 244 | 0 | 0.0% |
| `citalopram_modulated` | 427 | 427 | 3 | 0.7% |

**Conditional-on-note categorical `day_dominant_polarity` x recovery_phase**:

| phase | n_with_value | positive | neutral | negative | mixed |
|---|---:|---:|---:|---:|---:|
| `pre_illness_healthy` | 0 | n/a | n/a | n/a | n/a |
| `acute_infection` | 0 | n/a | n/a | n/a | n/a |
| `lc_pre_ergo` | 0 | n/a | n/a | n/a | n/a |
| `pacing_pre_citalopram_learning` | 14 | 14.3% | 85.7% | 0.0% | 0.0% |
| `pacing_habit_established` | 244 | 10.7% | 88.1% | 1.2% | 0.0% |
| `citalopram_modulated` | 427 | 10.1% | 88.3% | 1.6% | 0.0% |

**Reading per asymmetry MD section 3**: each cell is a `share-of-clauses-conditional-on-note`. The 5-cause-of-absence rule applies: a cluster's share dropping from phase X to phase Y could reflect any of (1) symptom absent, (2) routine, (3) crowded out by other topics, (4) habituated, or (5) the note didn't exist (the write-rate Layer A documents this systematically). NOT a prevalence claim.

---

## 7. Layer B Stage 8 -- within-note share per-citalopram-phase

**Method**: same as Stage 7, on the 5-phase citalopram axis.

| cluster | unmedicated | buildup | consolidation | afbouw | post_afbouw |
|---|---:|---:|---:|---:|---:|
| `cat_belasting_cognitief` | 2.6% | 0.1% | 1.2% | 2.9% | n/a |
| `cat_belasting_emotioneel` | 0.9% | 0.9% | 0.7% | 1.8% | n/a |
| `cat_belasting_fysiek` | 4.6% | 1.2% | 3.9% | 0.3% | n/a |
| `cat_belasting_gezin` | 4.6% | 7.5% | 9.8% | 7.7% | n/a |
| `cat_belasting_sociaal` | 0.8% | 1.2% | 2.5% | 3.3% | n/a |
| `cat_symptoom_cognitief` | 1.6% | 2.2% | 3.0% | 4.6% | n/a |
| `cat_symptoom_emotioneel` | 0.1% | 0.0% | 0.1% | 0.0% | n/a |
| `cat_symptoom_fysiek` | 41.4% | 54.9% | 35.2% | 34.5% | n/a |
| `cat_medicatie` | 0.1% | 0.0% | 2.9% | 2.1% | n/a |
| `cat_recovery_actie` | 6.1% | 6.8% | 5.7% | 8.3% | n/a |
| `cat_triggers_extern` | 0.6% | 0.0% | 0.1% | 0.2% | n/a |
| `cat_context_neutraal` | 41.8% | 33.7% | 43.4% | 46.7% | n/a |

**n_notes per phase**: `unmedicated` n_notes=258; `buildup` n_notes=61; `consolidation` n_notes=323; `afbouw` n_notes=43; `post_afbouw` n_notes=0.

---

## 8. Layer B Stage 9 -- within-note share per-event-class (Q4.4 sister)

**Method**: filter to `has_note=True`; stratify by `is_crash` + `is_dip` + `normal` (mutually exclusive per [`crash_v2-definition`](../../../hypotheses/crash_v2-definition/) section 2.2). **Q4.4 sister**: cohort_topology defines the event classes; this stage answers the asymmetry MD's worked example -- 'of crash-day notes, what fraction of clauses are on cluster X conditional-on-note?'

**`is_crash` per-day vs Q4.4 episode count**: Q4.4 reports 29 crash *episodes* (mean duration 3.55 days, max 14 days); per-day `is_crash=True` rows therefore total ~103 (29 episodes x mean duration). The Stage 9 counts use the per-day flag (each day in a multi-day crash counted independently). This is the natural unit for per-day-note stratification but the day-count is NOT directly comparable to the episode-count.

| cluster | crash | dip | normal |
|---|---:|---:|---:|
| `cat_belasting_cognitief` | 0.7% | 1.0% | 1.9% |
| `cat_belasting_emotioneel` | 1.5% | 0.6% | 0.9% |
| `cat_belasting_fysiek` | 1.2% | 4.4% | 3.9% |
| `cat_belasting_gezin` | 1.9% | 3.6% | 8.6% |
| `cat_belasting_sociaal` | 0.8% | 0.2% | 2.1% |
| `cat_symptoom_cognitief` | 4.9% | 3.8% | 2.1% |
| `cat_symptoom_emotioneel` | 0.0% | 0.0% | 0.1% |
| `cat_symptoom_fysiek` | 59.4% | 65.6% | 34.0% |
| `cat_medicatie` | 0.3% | 0.6% | 1.8% |
| `cat_recovery_actie` | 5.1% | 5.1% | 6.4% |
| `cat_triggers_extern` | 2.7% | 0.0% | 0.0% |
| `cat_context_neutraal` | 26.8% | 22.1% | 46.1% |

**n_notes per class**: `crash` n_notes=62; `dip` n_notes=64; `normal` n_notes=559.

**Conditional-on-note categorical `day_dominant_polarity` x event_class**:

| class | n_with_value | positive | neutral | negative | mixed |
|---|---:|---:|---:|---:|---:|
| `crash` | 62 | 8.1% | 91.9% | 0.0% | 0.0% |
| `dip` | 64 | 1.6% | 96.9% | 1.6% | 0.0% |
| `normal` | 559 | 11.6% | 86.8% | 1.6% | 0.0% |

**Cross-corroboration but NOT promotion** (per handoff section 3.4): if a per-event-class finding 'lines up with' a HA-* finding (e.g. crash-day notes show a higher share of `cat_symptoom_cognitief` than normal-day notes, and HA01b is about cognitive load), surface as descriptive cross-reference. The corroboration does NOT extend HA01b's verdict here; HA01b operationalises at a different layer.

---

## 9. Layer B Stage 10 -- within-note share per Q4.3-boundary +/-30d

**Method**: for each of the 6 strong Q4.3 boundaries (per [`era_boundaries/findings.md`](../era_boundaries/findings.md) section 1), restrict to the +/-30d window around the boundary date; filter to `has_note=True`; compute pre vs post side cluster-share table. Delta = post share minus pre share. **Q4.3 substrate**: 6 boundaries (rp1, rp2, rp3, rp4, rp5, cp3) each get an independent pre/post comparison.

### 9.rp1 `rp1_pre_illness_to_acute` (2022-03-21; n_notes_pre=0; n_notes_post=0)

Skipped: one side has 0 notes in the +/-30d window (typical for early-LC boundaries before the user started writing notes 2022-10-18).

### 9.rp2 `rp2_acute_to_lc_pre_ergo` (2022-04-04; n_notes_pre=0; n_notes_post=0)

Skipped: one side has 0 notes in the +/-30d window (typical for early-LC boundaries before the user started writing notes 2022-10-18).

### 9.rp3 `rp3_lc_pre_ergo_to_4a` (2022-09-22; n_notes_pre=0; n_notes_post=5)

Skipped: one side has 0 notes in the +/-30d window (typical for early-LC boundaries before the user started writing notes 2022-10-18).

### 9.rp4 `rp4_4a_to_4b` (2022-11-17; n_notes_pre=14; n_notes_post=5)

| cluster | pre share | post share | delta (post - pre) |
|---|---:|---:|---:|
| `cat_symptoom_fysiek` | 68.8% | 45.0% | -23.8% |
| `cat_belasting_fysiek` | 0.0% | 20.0% | 20.0% |
| `cat_recovery_actie` | 7.1% | 0.0% | -7.1% |
| `cat_context_neutraal` | 28.8% | 35.0% | 6.2% |
| `cat_belasting_cognitief` | 3.6% | 0.0% | -3.6% |
| `cat_belasting_gezin` | 1.8% | 0.0% | -1.8% |
| `cat_belasting_emotioneel` | 0.7% | 0.0% | -0.7% |
| `cat_belasting_sociaal` | 0.0% | 0.0% | 0.0% |
| `cat_symptoom_cognitief` | 0.0% | 0.0% | 0.0% |
| `cat_symptoom_emotioneel` | 0.0% | 0.0% | 0.0% |
| `cat_medicatie` | 0.0% | 0.0% | 0.0% |
| `cat_triggers_extern` | 0.0% | 0.0% | 0.0% |

**Reading per asymmetry MD section 3**: delta in share at boundary does NOT mean delta in prevalence. Could reflect (a) a real shift in what the user wrote about across the boundary (note-content shift), OR (b) the 5-cause-of-absence rule. The boundary substrate is Q4.3 (descriptive) and the conditional-share shift is descriptive.

### 9.rp5 `rp5_4b_to_citalopram_modulated` (2024-04-09; n_notes_pre=27; n_notes_post=28)

| cluster | pre share | post share | delta (post - pre) |
|---|---:|---:|---:|
| `cat_symptoom_fysiek` | 26.8% | 50.0% | 23.2% |
| `cat_context_neutraal` | 49.7% | 40.7% | -9.1% |
| `cat_belasting_gezin` | 11.9% | 5.9% | -5.9% |
| `cat_recovery_actie` | 3.3% | 6.9% | 3.6% |
| `cat_belasting_cognitief` | 2.9% | 0.2% | -2.7% |
| `cat_belasting_fysiek` | 2.5% | 0.0% | -2.5% |
| `cat_belasting_emotioneel` | 2.5% | 0.0% | -2.5% |
| `cat_medicatie` | 0.7% | 0.0% | -0.7% |
| `cat_symptoom_cognitief` | 0.2% | 0.0% | -0.2% |
| `cat_belasting_sociaal` | 1.3% | 1.4% | 0.1% |
| `cat_symptoom_emotioneel` | 0.0% | 0.0% | 0.0% |
| `cat_triggers_extern` | 0.0% | 0.0% | 0.0% |

**Reading per asymmetry MD section 3**: delta in share at boundary does NOT mean delta in prevalence. Could reflect (a) a real shift in what the user wrote about across the boundary (note-content shift), OR (b) the 5-cause-of-absence rule. The boundary substrate is Q4.3 (descriptive) and the conditional-share shift is descriptive.

### 9.cp3 `cp3_consolidation_to_afbouw` (2026-03-20; n_notes_pre=12; n_notes_post=8)

| cluster | pre share | post share | delta (post - pre) |
|---|---:|---:|---:|
| `cat_symptoom_cognitief` | 0.0% | 15.6% | 15.6% |
| `cat_belasting_sociaal` | 0.0% | 12.5% | 12.5% |
| `cat_belasting_gezin` | 4.2% | 12.5% | 8.3% |
| `cat_context_neutraal` | 33.3% | 39.6% | 6.2% |
| `cat_symptoom_fysiek` | 50.0% | 44.8% | -5.2% |
| `cat_recovery_actie` | 8.3% | 12.5% | 4.2% |
| `cat_medicatie` | 4.2% | 0.0% | -4.2% |
| `cat_belasting_cognitief` | 0.0% | 0.0% | 0.0% |
| `cat_belasting_emotioneel` | 0.0% | 0.0% | 0.0% |
| `cat_belasting_fysiek` | 0.0% | 0.0% | 0.0% |
| `cat_symptoom_emotioneel` | 0.0% | 0.0% | 0.0% |
| `cat_triggers_extern` | 0.0% | 0.0% | 0.0% |

**Reading per asymmetry MD section 3**: delta in share at boundary does NOT mean delta in prevalence. Could reflect (a) a real shift in what the user wrote about across the boundary (note-content shift), OR (b) the 5-cause-of-absence rule. The boundary substrate is Q4.3 (descriptive) and the conditional-share shift is descriptive.

---

## 10. Caveats (CRITICAL -- per asymmetry MD + CONVENTIONS section 4.2 caveat-class)

1. **Asymmetry discipline (LOAD-BEARING)**: every Layer-B number is `share-of-clauses-conditional-on-note`. A higher share in phase Z is NEVER a claim that the corresponding symptom/topic is more prevalent in phase Z. Five distinct causes of absence-of-mention per asymmetry MD section 2: only one is 'symptom absent'.
2. **Layer A vs Layer B asymmetry**: Layer A (write-rate per-phase/per-DOW/per-month/per-score) is trajectory-clean because `has_note` is daily_computed (asymmetry MD section 3 + DATA_DICTIONARY section 14). Layer B (within-note cluster shares) is asymmetry-conditional and EXCLUDES absolute mention-rate trajectories per user-locked choice 4.
3. **Q4.6 MCAR-rejection family**: per Q4.6 coverage_overview, all 89 tested-eligible channels reject MCAR (missingness depends on other channels). Stage 6 (has_note <-> gevoelscore correlation) is in the same family -- it characterises one specific dimension of that structured missingness.
4. **Cross-corroboration but NOT verdict promotion**: even if a Stage 7-10 finding lines up with a HA-* result (e.g. higher `cat_symptoom_cognitief` share on crash days lines up with cognitive-load HAs), this is a DESCRIPTIVE cross-reference at a different operationalisation -- it does NOT extend the HA's verdict.
5. **Wrong-shape claims that this analysis MUST avoid** (per asymmetry MD section 3 Right-vs-Wrong table): 'brainfog prevalence in 2024 was X%'; 'in 2025 the user had less muscle pain'; 'on the day before a crash, cat_symptoom_cognitief=0 therefore no brainfog'. All forbidden.
6. **5-cause-of-absence applies to state_symptoom categoricals too**: `state_symptoom_cognitief=absent` is itself presence-conditioned positive ('geen brainfog was mentioned') and is distinct from no-mention. The categorical distribution on `has_note=True` rows where `state_symptoom_cognitief` is non-NaN is reported; NaN cells indicate the note did not contain a state-mention for that family.
7. **Write-rate per-phase Layer A includes phases the user predates writing**: `pre_illness_healthy` + `acute_infection` show 0% write-rate by construction (user started writing notes 2022-10-18, within `lc_pre_ergo`). NOT a substantive interpretation of those phases.
8. **Per-Q4.3-boundary windows around early boundaries**: rp1 + rp2 + rp3 + rp4 fall before or near the start of the notes corpus; n_notes_pre is often 0, in which case the boundary is skipped per the n_pre > 0 + n_post > 0 gate.
9. **Statistical tests are descriptive markers, not falsification bars**: Layer A chi-square + Spearman flags are at the 0.05 conventional threshold (CONVENTIONS section 4.2 caveat-class), not multiple-comparison-corrected, not falsification-bar locked.

---

## 11. Cross-references

### LOAD-BEARING (binding for this analysis's discipline)

- [`methodology/symptom_mention_asymmetry.md`](../../../../methodology/symptom_mention_asymmetry.md) LOCKED 2026-06-11 -- **the binding methodological MD for Q4.7**. Section 1 (the rule) + section 2 (5 causes of absence) + section 3 (what v24 IS and IS NOT) cited at every framing decision.
- [`DATA_DICTIONARY.md`](../../../../DATA_DICTIONARY.md) section 9 (presence-conditioned preamble) + section 10 (state_symptoom + sub-tags) -- column-level types + the `has_note=True` gating-flag convention.
- [`CONVENTIONS.md`](../../../../CONVENTIONS.md) section 2.1 (descriptive-before-inference) + section 4.2 (caveat-class language) + section 4.3 (no interpretive marks).

### Descriptive corroboration (NOT verdict extension)

- [`trajectory/coverage_overview/findings.md`](../coverage_overview/findings.md) section 6.2 -- Q4.6 MCAR diagnostic family (89 of 89 numeric channels reject MCAR at alpha=0.05); Stage 6 is in the same family.
- [`trajectory/seasonality_dow/findings.md`](../seasonality_dow/findings.md) Stage 3 + Stage 4 -- Q4.8 per-month + per-DOW patterns on Garmin channels; Stage 4 + Stage 5 here are SISTERS on `has_note`.
- [`trajectory/cohort_topology/findings.md`](../cohort_topology/findings.md) section 1 + section 5 -- Q4.4 event-class definitions (29 crashes + 79 dips + crash-vs-dip distinction at autonomic-load layer); Stage 9 uses these.
- [`trajectory/era_boundaries/findings.md`](../era_boundaries/findings.md) section 1 + section 2 -- Q4.3 6 strong boundaries; Stage 10 uses these as substrate for +/-30d windows.

### Queued-primitive substrate (NOT promotion)

- **HA-C4b v3 section 8 queued primitive** on emotional/cognitive triggers + state_symptoom_* proxies: Stage 7 + Stage 8 + Stage 9 + Stage 10 provide DESCRIPTIVE substrate for that queued primitive. **NO promotion to that primitive's MD** per CONVENTIONS section 4.2.

### Methodology MDs cited

- [`methodology/lc_recovery_phase_axis.md`](../../../../methodology/lc_recovery_phase_axis.md) section 2 -- 6-phase recovery axis (LOCKED `d47e0d3` 2026-06-19).
- [`methodology/citalopram_phase_stratification.md`](../../../../methodology/citalopram_phase_stratification.md) section 3 -- 5-phase citalopram axis.

### Upstream pipeline

- `pipeline/03_consolidate/build_unified_dataset.py` -- `per_day_master.csv` builder (includes `has_note` + `cat_*` + `state_symptoom_*` + `day_dominant_polarity` + `neutral_forward_looking_flag`).
- `analyses/_utils/frame.py` -- `load_master()` loader (single source of truth for the as-of-date convention).

---

## 12. Status

**Q4.7 findings landed 2026-06-26** from a single execution of [`run.py`](run.py) under the user-LOCKED operationalisation (Strand B section 7c interview 2026-06-26). **Tier 3 deferred-topic 2 of 2 LANDED**; Q4.8 sister landed at `e4db6cc` + STOCKTAKE at `09b9177`. **Strand B 8 of 8 CLOSED**. Foundation now in place for `/research-interpret` skill pivot per user's earlier sequencing: 'before we start using the research interpret skill, i want to make sure we finished all basic and foundational descriptive research'.

Next refresh per [`descriptive/README.md`](../../README.md) section 7d: when new note-corpus data accrues +90 days OR when an HA-* result raises a write-rate-sensitive or conditional-share-sensitive question (e.g. the user-noted hypothesis that crash-day notes show distinctive within-note content).

