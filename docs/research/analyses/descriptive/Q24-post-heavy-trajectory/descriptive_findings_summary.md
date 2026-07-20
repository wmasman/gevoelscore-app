# Q24 post-heavy-day trajectory — descriptive findings summary

*A plain-language distillation of [`descriptive_audit.md`](descriptive_audit.md) (LOCKED r4, Stage D Wave 1). This file is a reading aid; the audit is the source of truth. Nothing here re-opens a locked verdict. Charts are regenerated from the (gitignored) output CSVs by [`scripts/make_summary_charts.py`](scripts/make_summary_charts.py) into [`charts/`](charts/); the tables below stand alone if the images do not render.*

---

## The question in one line

After a heavy exertion day (an "episode-end"), does the body and felt-state recover on its own, and does that trajectory look different on the days that end in a crash versus the days that don't? Wave 1 compares each post-heavy trajectory against a **matched-ordinary day** (same window, no heavy day, no crash, valid data), split into two pools:

- **compensatory-success** = no crash in the follow-up window (the recovery that worked)
- **compensatory-failure** = a crash happened in the window (the recovery that didn't)

All findings are **descriptive only**. No inferential test compares the two pools; bootstrap 95% CIs are reported as descriptive markers, not p-values.

---

## Headline findings (the four things that matter)

1. **The felt-state trajectory cleanly separates the two pools, and this is the strongest signal in the whole audit.** On days that don't crash, `gevoelscore` dips then recovers toward baseline within a few days. On days that do crash, it stays low (sustained worseness) for the whole window. The failure-pool subjective response is roughly **8× the success-pool magnitude at +3d** and **7× at +5d**.

2. **Behavioural compensation is real and unambiguous.** After a heavy episode-end the participant does **less** (fewer steps, less vigorous/active time) and sleeps **longer** — direction is consistent at every window, and the effect scales with window length.

3. **The autonomic (Garmin) picture is mixed and splits by pool.** On the success pool, overnight/waking HR is elevated the day after (a cost signal), but the Garmin *stress* channels trend *below* matched-ordinary. On the failure pool, stress trends *above* matched-ordinary. The two pools show opposite-signed autonomic stress trajectories.

4. **Most of the success-pool raw signals do not survive detrending.** 44 of 118 cells are trajectory-confound-suspect. On the success pool, envelope drift (LC recovery over 4 years) *inflates* activity/sleep signals; on the failure pool, the same drift *masks* real autonomic-cost signals. Only **5 signals survive both raw and detrended reads** (all on the failure pool), plus 1 rescuable-by-detrend.

---

## Frame and method (brief)

| item | Wave 1 choice |
|---|---|
| Stratum | LC-era only (`date >= 2022-04-04`), N = 1524 days |
| Heavy day | `exertion_class_lagged_lcera ∈ {heavy, very_heavy}` — 532 heavy days (34.9%) |
| Unit | episode-end (gap=0 contiguous run of heavy) — 314 total on LC-era |
| Trigger | combined heavy ∪ very_heavy (intensity-stratified deferred to Wave 2) |
| Overlap | strict-clean only (no other heavy day inside the window) |
| Windows | +3d and +5d primary, +10d extended (wide CIs) |
| Comparator | matched-ordinary day, recomputed per outcome |
| Statistics | per-cell AUC, slope, peak, RTBT etc. + B=10,000 bootstrap 95% CI |
| Detrend companion | per-episode 30d pre-window linear extrapolation, reported side-by-side |

**Reading the AUC sign** (physiologically-meaningful "cost/compensation" direction per outcome):

| outcome family | negative AUC means | positive AUC means |
|---|---|---|
| activity (steps, vigorous, active min) | **compensation** (did less) | did more |
| sleep duration / light / deep / REM | did less | **rebound** (slept more) |
| gevoelscore | **cost** (felt worse) | felt better |
| Garmin stress, waking/overnight HR | recovered / below baseline | **cost** (elevated) |
| bb_lowest (Body Battery floor) | **cost** (depleted) | more reserve |

"Bold AUC" in the tables = bootstrap 95% CI excludes zero (a descriptive marker only).

---

## Sample sizes

Strict-clean episode-ends split by pool and window:

| window | compensatory-success | compensatory-failure | strict-clean total |
|---:|---:|---:|---:|
| **+3d** | **109** | **16** | 125 |
| **+5d** | **43** | **9** | 52 |
| **+10d** | **11** | **1** | 12 |

Discipline flags: failure-pool **+10d (n=1) is NOT DEFENSIBLE**; **+5d (n=9)** is borderline (wide-CI caveat); **+3d (n=16)** is the most reliable failure-pool read.

**Crash-in-window rate** on strict-clean episode-ends: 12.8% (+3d), 17.3% (+5d), 8.3% (+10d) — roughly **2× the corpus baseline** LC-era crash rate of 6.8%. The day after a heavy episode is a higher-risk period.

---

## The corpus at a glance (timeline)

All 532 heavy/very-heavy days and all 103 crashes fall inside the LC era. The timeline puts them on one axis with the exertion-intensity and gevoelscore trends underneath, so the alignment is visible:

![LC-era timeline: heavy days, crashes, intensity, gevoelscore](charts/05_lc_era_timeline.png)

- **Top (event raster):** every very_heavy day, heavy day, and crash day as a tick.
- **Middle:** daily exertion intensity (none → very_heavy) with a 14-day rolling mean.
- **Bottom:** daily `gevoelscore` (1–6) with a 14-day rolling mean; crash days marked in red (they sit low by construction).

> **Read the intensity axis as *relative*, not absolute.** `exertion_class_lagged_lcera` is not an absolute-load ladder. Each day is percentile-ranked against a **lagged** baseline window (days d−90 to d−31, LC-era only), across **four axes** — effective_exertion_min, total_steps, max_hr, vigorous_min — and the class is the **worst of the four** (cutoffs: heavy = 85th percentile, very_heavy = 95th). So "very_heavy" means heavy *relative to the recent preceding baseline*, not a fixed number of minutes or steps. The lag (dropping the most recent 30 days) is deliberate: it stops a slow sustained push from rebasing itself. Because the baseline itself moves, a "very_heavy" day in 2026 is a materially lighter absolute load than one in 2023 — see the baseline-drift chart below.

The clearest pattern is the **recovery envelope**: crashes are dense in 2022–2024 and nearly disappear in 2025–2026, while felt-state drifts upward. Note the *count* of heavy/very_heavy days holds roughly steady across years — but that is a relative classification holding steady, not absolute load; the absolute bar for those classes actually falls after 2023 (next chart). This drift is exactly what the audit's detrend companion is wrestling with.

| year | heavy | very_heavy | crashes | mean gevoelscore |
|---|---:|---:|---:|---:|
| 2022 | 27 | 52 | 20 | 4.13 |
| 2023 | 75 | 52 | 45 | 4.19 |
| 2024 | 65 | 60 | 30 | 4.24 |
| 2025 | 68 | 59 | 4 | 4.70 |
| 2026 (to Jun) | 41 | 33 | 4 | 4.65 |

Because the crash rate collapses while the *relative* activity classification stays roughly constant, the drift being removed by the detrend is partly *the very thing Q24 is trying to measure* (pacing/recovery improving over the LC course). That is the drift-entanglement argument (Finding 4) in one picture: raw signals mix the event response with this multi-year improvement.

### How the exertion class is defined, and why the baseline moves

The four panels below show the **lagged baseline** for each of the four axes that feed the composite class. Each panel plots that axis's baseline median (50th percentile of the lagged window) with a bootstrap 95% CI, plus the two class thresholds — heavy (85th) and very_heavy (95th) — as they drift over the LC era. A day's dot sitting above the dashed lines is roughly what makes that axis "heavy" / "very_heavy"; the composite class is the worst axis.

![lagged baseline drift across four axes](charts/06_lagged_baseline_drift.png)

The baseline is clearly **not stationary**, and it moves differently per axis (very_heavy / 95th-percentile threshold shown):

| axis | 2022 | 2023 | 2024 | 2025 | 2026 | shape |
|---|---:|---:|---:|---:|---:|---|
| effective_exertion_min | 47 | 75 | 32 | 20 | 21 | peaks 2023, then falls |
| total_steps | 10233 | 9760 | 8018 | 7752 | 6886 | steady decline |
| max_hr (bpm) | 138 | 144 | 135 | 135 | 139 | ~flat (physiological ceiling) |
| vigorous_min | 9.3 | 6.4 | 5.0 | 4.7 | 3.5 | steady decline |

Three of the four axes fall substantially after 2023; only `max_hr` holds, because a max-heart-rate ceiling doesn't decondition the way volume/intensity does. The practical consequence: the *absolute* load that earns a "very_heavy" label in 2025–26 is much lower than in 2023 (roughly a third of the effective-exertion minutes, two-thirds of the steps). This is why the recovery-envelope reading has to be stated in relative terms, and it is the concrete, per-axis form of the envelope drift the detrend companion removes.

### Full smartwatch period: the deconditioning cliff

The charts above are LC-era only (matching the audit). Extended back over the whole consolidated smartwatch record (2021-08 → 2026-06), the raw signals show *why* the LC-era classification is what it is. Note two data facts: `gevoelscore` self-tracking only begins 2022-09-03 (blank in the healthy phase), and all crashes are LC-only — so this view uses raw signals in absolute units rather than the `_lcera` class, which is undefined pre-LC.

![full smartwatch period across phases](charts/07_full_period_timeline.png)

**Vigorous minutes are not "mostly absent" in general — they collapse at LC onset.** In the healthy pre-corona phase the participant did substantial vigorous exercise; that falls off a cliff through the 2-week infection and stays near-zero for the whole LC era:

| phase | days with any vigorous min | mean vigorous_min/day | p95 |
|---|---:|---:|---:|
| pre_corona (healthy) | 69% | 31.9 | 109 |
| corona_infection | 43% | 10.7 | 53 |
| Long COVID | 34% | 1.2 | 6 |

The same cliff appears in effective-exertion minutes and steps. This is the backdrop for everything in the audit: the LC-era "heavy"/"very_heavy" days are heavy *relative to a deconditioned baseline*, and the within-LC recovery envelope (Section above) sits on top of a far larger drop from the pre-LC healthy baseline. Vigorous minutes in particular are so sparse in LC (median 0, p95 = 6 min) that Axis D contributes little discriminating information within the LC era — which is what you correctly spotted in the baseline chart.

---

## Finding 1 — Subjective (`gevoelscore`): the clearest signal

![gevoelscore: success recovers, failure sustains](charts/01_gevoelscore_success_vs_failure.png)

| pool | window | n_t | AUC | AUC 95% CI |
|---|---:|---:|---:|---|
| compensatory-success | +3d | 109 | **−0.47** | [−0.83, −0.12] |
| compensatory-success | +5d | 43 | −0.78 | [−1.57, +0.04] |
| compensatory-success | +10d | 11 | +0.16 | [−1.72, +1.98] |
| compensatory-failure | +3d | 16 | **−3.77** | [−4.84, −2.77] |
| compensatory-failure | +5d | 9 | **−5.33** | [−7.17, −3.51] |
| compensatory-failure | +10d | 1 | — | (not defensible) |

The decision-tree screen confirms the shape: **subjective decays at every window on the success pool, and sustains at every window on the failure pool.** This is the load-bearing empirical anchor for the Q24.5 counterfactual sub-part.

**One honest caveat:** part of the ~8× failure-vs-success gap is definitional. Crash days have low `gevoelscore` by construction (crash is derived from gevoelscore), and failure-pool windows *contain* those low values. The pool split is designed to answer the counterfactual, so the finding isn't spurious, but the *magnitude* of the contrast carries some circularity. A matched-subjective-baseline sensitivity arm is flagged for Wave 2.

---

## Finding 2 — Activity and sleep: behavioural compensation

![activity down, sleep up](charts/02_activity_sleep_compensation.png)

**Activity (success pool)** — negative AUC = did less than a matched-ordinary day, at every window, diverging from day 1:

| outcome | +3d AUC | +5d AUC | +10d AUC |
|---|---:|---:|---:|
| total_steps | **−1356** | **−3865** | **−15316** |
| vigorous_min | **−1.72** | **−4.26** | **−14.51** |
| active_min | **−15.3** | **−47.3** | **−229** |

*(`effective_exertion_min`, the composite, is the exception — near-zero/slightly positive at +3d/+5d. It tells a "level vs change" story rather than a clean compensation story; see the robust-core section.)*

**Sleep (success pool)** — positive `sleep_duration_min` AUC = slept longer, cleanest sleep signal in the audit:

| outcome | +3d AUC | +5d AUC | +10d AUC | note |
|---|---:|---:|---:|---|
| sleep_duration_min | **+74** | **+180** | **+279** | the extra sleep |
| sleep_light_min | **+89** (+3d) | | | accounts for most of the +3d duration gain |
| sleep_deep_min | **−24** | +12 | **+308** | genuine sign reversal across windows |
| sleep_efficiency_tib | ~0 | ~0 | ~0 | the extra sleep is longer, not more efficient |

Direction holds on the failure pool too (both pools sleep more, do less), with the failure pool showing ~2× the activity drop — consistent with either a rougher lived experience or the crash itself forcing inactivity.

---

## Finding 3 — Autonomic: mixed, and pool-divergent

![autonomic stress diverges by pool](charts/03_autonomic_pool_divergence.png)

**Success pool** (n_t 109 / 43 / 11):

| channel | +3d AUC | +5d AUC | +10d AUC | reading |
|---|---:|---:|---:|---|
| hr_median_waking | **+3.51** | +2.59 | +5.83 | elevated day-after HR (cost, as expected) |
| sleep_hr_avg_spo2 | **+2.30** | +2.53 | −6.62 | elevated overnight HR at +3d |
| stress_mean_sleep | −0.74 | −4.16 | +14.9 | **inverts** — stress *below* matched-ordinary |
| all_day_stress_avg | −1.06 | **−6.68** | **−33.1** | **inverts** — stress below matched-ordinary |
| bb_lowest | −0.02 | **+13.6** | **+76.0** | **inverts** — more BB reserve, not less |

The elevated-HR signals align with Radin 2024 nightly-HR persistence. The stress/BB **sign inversions** (opposite the pre-committed cost direction) are a finding in their own right, not a null — but most of them do **not** survive detrending (see Finding 4), which pushes the reading toward "envelope drift created them" rather than "post-heavy pacing suppressed autonomic load."

A second arousal channel (`asleep_stress_max_uds`, from a different aggregator) mirrors the same below-baseline pattern at +5d/+10d, which is convergence across two independent arousal measures.

**Failure pool:** the same autonomic channels trend in the *elevated* (cost) direction, and detrending makes those signals **stronger**, not weaker (drift was masking them). The two pools genuinely diverge.

---

## Finding 4 — The big caveat: detrend fragility

![detrend survival](charts/04_detrend_survival.png)

Of 118 (outcome × window × pool) cells, **44 are trajectory-confound-suspect**: the raw and detrended reads disagree on whether the CI excludes zero.

- **36 cells: raw significant → detrended not** ("detrend-erasing"). Concentrated on the **success pool**. Envelope drift (4 years of LC recovery, crash rate 10/y → 2/y) *inflates* the apparent activity/sleep/autonomic signals.
- **8 cells: raw not significant → detrended is** ("detrend-surfacing"). Concentrated on the **failure pool**. The same drift *masks* real autonomic-cost signals (stress/HR up, BB/efficiency/SpO2 down) that only appear after detrending.

**How to read raw vs detrended (the drift-entanglement reframe, §9.1):** the 30d linear detrend removes *all* time-varying drift bundled together — disease natural history, citalopram, deconditioning, aging, seasonality, **and the pacing-improvement the study is trying to measure**. So:

- **raw = upper bound** on the compensatory response (keeps all time-associated variance)
- **detrended = lower bound** (removes it all, including any learning signal)
- **truth is between the two**

The 36 raw-only cells are therefore **not dismissible as "not real"** — they are drift-entangled, and are the motivating input for Q24 sub-part 3 (phase-stratification: does the compensatory response strengthen across LC epochs?).

---

## The robust core (what survives everything)

**5 sign-consistent survivors** — raw AND detrended CI both exclude zero, same sign. These are the defensible Stage-H seed set. **All 5 cluster on the compensatory-failure pool** (the success pool has zero survivors):

| outcome | window | pool | direction | raw AUC | detrended AUC |
|---|---:|---|---|---:|---:|
| total_steps | +3d | failure | negative | **−2539** | **−2741** |
| sleep_awake_min | +3d | failure | positive | **+11.6** | **+10.3** |
| sleep_efficiency_tib | +3d | failure | negative | **−0.018** | **−0.018** |
| gevoelscore | +3d | failure | negative | **−3.77** | **−1.86** |
| gevoelscore | +5d | failure | negative | **−5.33** | **−3.16** |

**+1 rescuable sign-flipper** (Wave 2 close): `spo2_avg_sleep` +3d failure — raw AUC +1.01 flips to detrended −1.36. Diagnostic (§6.4) confirmed a **drift-entanglement** mechanism (failure episodes cluster in 2022–2024, a rising-SpO2 era; slope-diff p=0.0003). Verdict: **RESCUABLE for Stage H with pre-committed direction = detrended (negative)**; the raw positive is an era-selection artefact, not physiology. Era-stratified comparator sensitivity is armed as required at Stage H.

**1 discarded sign-flipper:** `effective_exertion_min` +3d success — raw +3.55 vs detrended −6.49. Diagnostic found a **level-vs-change disagreement** (slopes indistinguishable, p=0.34; pre-episode ambient exertion ~55% higher before heavy days). Both reads are true: the participant still does *more* absolute activity than a matched-ordinary day (raw), yet drops *further from their own recent baseline* (detrended). Verdict: **DISCARD as a Stage-H seed** (neither read is a-priori primary), but preserved as a **calibrated-partial-compensation** observation to surface at synthesis (Stage S1/S2), not an empirical null.

---

## Decision-tree branch verdicts (autonomic recovery shape)

A channel "decays" when `|Δ(w)| / |Δ(k*)| < 0.5` on the raw delta trajectory. `[frag]` = the underlying raw trajectory doesn't survive detrending, so treat as shape-only, not independent evidence.

**Success pool:**

| channel | +3d | +5d | +10d |
|---|---|---|---|
| stress_mean_sleep | BOTH decay | BOTH decay | BOTH decay |
| all_day_stress_avg | BOTH decay | only subjective `[frag]` | only subjective `[frag]` |
| bb_lowest | only subjective | only subjective `[frag]` | only subjective `[frag]` |
| hr_median_waking | only subjective `[frag]` | BOTH decay | BOTH decay |
| sleep_hr_avg_spo2 | only subjective `[frag]` | BOTH decay | BOTH decay |

Subjective decays in every cell. Autonomic decay is channel-heterogeneous: HR channels show the delayed-decay pattern the literature predicts (sustained at +3d, decayed by +5d/+10d); `stress_mean_sleep` decays throughout; `bb_lowest` diverges. Channel split is 2:3 at +3d, 3:2 at +5d/+10d.

**Failure pool:** the **subjective channel does not decay at any window** — sustained worseness, the direct counterfactual to the success pool. (+10d is n=1, not defensible.)

---

## What this cannot say (confounds)

| # | caveat | status |
|---:|---|---|
| 1 | 2026 heavy-rate elevation | **relevant** — a no-2026 sensitivity arm is a Wave 2 candidate |
| 3 | baseline drift | **relevant** — this is exactly what the 44 detrend-fragility cells measure |
| 4 | deconditioning floor | partially relevant to the success-pool autonomic inversions |
| 5 | citalopram era mixing | structural — `stress_mean_sleep` BOTH-decay is a candidate for the sub-part 3 follow-up |
| 6 | small +10d samples (n=12) | **relevant** — all +10d verdicts are descriptive-only |
| 8 | comparator envelope-drift asymmetry | **relevant, ESCALATED** — 44/118 fragility crosses the threshold; era-stratified comparator now armed for Stage H |

Wave 1 deliberately deferred: intensity-stratified arms, inclusive-overlap arm, Stage H pre-registration drafting, and Q24 sub-part 3 phase-stratification.

---

## Pointers

- Full audit: [`descriptive_audit.md`](descriptive_audit.md) (§4 tables, §5 branches, §6 detrend, §6.4 sign-flipper diagnostic, §7 pool contrast, §9 confounds)
- Methodology: [`../../../methodology/post_heavy_day_compensatory_rest.md`](../../../methodology/post_heavy_day_compensatory_rest.md)
- Data (gitignored, regenerable): [`output/trajectory_summary.csv`](output/trajectory_summary.csv), [`output/per_day_trajectories.csv`](output/per_day_trajectories.csv)
- Charts in this summary: [`charts/`](charts/) (regenerated from the output CSVs; gitignored)
