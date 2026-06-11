# Research stocktake — what we have, what it shows, what could become a feature

*Snapshot of the Garmin × gevoelscore × notes research as of 2026-06-06
(crash_v2 phase). Original snapshot 2026-06-05; updated 2026-06-06.
Source-of-truth pointers below each section. The crash_v2 phase has its
own writeup at [RESEARCH-REPORT-ADDENDUM.md](RESEARCH-REPORT-ADDENDUM.md);
this stocktake folds the new findings into the cross-cutting view.*

The goal of this document: one frame in which to see (a) the data we
actually have, (b) what looks insightful **before / during / after** a
crash, and (c) which indicators have earned enough evidence to be
candidates for the app — versus which would be misleading to build.

---

## 1. The data

### Subjective (gevoelscore + notes)

- **1.372 day_entries** with score across **2022-09-03 → 2026-06-05**.
  100% have a score on a 1–6 scale heavily clustered at 4–5.
- **686 day_entries (50%) have a written note.** Note coverage is
  uneven by year: 18% (2022, partial) → 40% (2023) → **71% (2024 peak)** →
  52% (2025) → 44% (2026 partial).
- Crash labels via locked `crash_v1`: score ≤ 3 for ≥2 consecutive days,
  episodes within 3 days merged.
- **`crash_v2` (locked 2026-06-06)** adds a tier-2 `dip` category for
  isolated single days at score ≤ 3 with neighbours ≥ 4. Tier-1 `crash`
  is exactly `crash_v1` — a pre-registered slow-recovery filter was
  empirically removed after the data showed all 29 v1 episodes have a
  multi-day rough tail (tail_median ∈ {4.0, 5.0}). See
  [crash_v2 definition](garmin/hypotheses/crash_v2-definition/definition.md).
- **Activity feature table (locked 2026-06-06, v3.1 percentile-rank)**:
  daily features at `garmin/activity-labels/output/activity_features_daily.csv`
  with `exertion_class` (4-axis composite of personal-baseline-relative
  percentile ranks), `push_burden_7d` (sustained-push count), and a
  passively-detected unified UDS intensity-minutes channel (empirically
  a superset of recorded-activity vigorous minutes). Spec is
  PEM-envelope, not athletic-training, and uses deviations from personal
  baseline throughout (no absolutes). Sensitivity-tested across 13
  parameter alternates; `exertion_class` is ROBUST (Jaccard ≥0.78
  on heavy+very_heavy across all variations); `push_burden_class`
  binning was SENSITIVE and was deprecated (raw count used downstream).

### Crash counts under `crash_v1`

| year | episodes | note |
|------|---------:|------|
| 2022 | 5 | partial year (~4 months of tracking) |
| 2023 | 9 | |
| 2024 | 11 | peak |
| **2025** | **2** | full year |
| 2026 | 2 | partial year (~5 months) |
| **total** | **29** | episodes |

Derived counts: **98 crash days** total (any day inside an episode with
score ≤ 3); **84 lead-up days** (3 days before each episode start);
**59 crash days have notes** (60%); **45 lead-up days have notes** (54%).

Episode span distribution (calendar days from first to last low day):
2-day = 19; 3–4-day = 4; 5–7-day = 3; 8–14-day = 3; 15+ = 0 (merge rule).
Long-crash tail collapsed from 5/14 early-era to 1/15 late-era.

Nadir distribution: early min = score 1 (3 episodes), late min = score 2
(no score-1 episodes in late era).

### Dip counts under `crash_v2`

**79 isolated single-day dips** across the corpus, on top of the 29
crash episodes (which are unchanged from `crash_v1`).

| era | crashes | dips | dip:crash ratio |
|---|---:|---:|---:|
| 2022-09-03 → 2023-12-31 (train) | 14 | 26 | 1.9× |
| 2024-01-01 → 2026-06-05 (validate) | 15 | 53 | 3.5× |

The dip:crash ratio nearly doubles between eras. The participant has
disproportionately more transient single-day rough patches in the
validate era — a finding the original `crash_v1`-only framework could
not surface formally.

**Dip clusters (descriptive overlay)**: 45 of the 79 dips (57%)
chain into 15 multi-day rough-patch clusters under a 7-day proximity
rule. 5 clusters are in the train era (covering 13 dips), 10 in the
validate era (covering 32 dips). The longest cluster spans
2024-03-14 → 2024-04-16 (9 dips, 34 days). The cluster concentration
in the validate era reinforces the "kind of crash changed" narrative:
rough patches in the residual era are protracted and intermittent
rather than sustained-low. Per-day labels are unchanged; clusters
are captured as a `dip_cluster_id` column for downstream analyses.

### Objective (Garmin)

- **~1.700 days** of monitoring data (2021-08-16 → 2026-06-04, 98.8%
  coverage). Pre-LC period (2021-08 → 2022-09) is healthy-baseline
  reference, not used for labelled tests.
- Daily aggregates we use: RHR, average stress, charged/drained body
  battery, sleep efficiency.
- Per-minute samples we extracted: stress (~1.400/day) for spike
  analysis (H02b).
- Per-minute body battery is NOT yet extracted — encoded in undocumented
  FIT message type 233. **2026-06-06 literature sweep confirmed no public
  decode exists** (HarryOnline community spreadsheet lists it with a
  question mark; tcgoetz/Fit, GoldenCheetah, fitdecode all treat it as
  unknown). A two-path H04b protocol is locked at
  [.claude/plans/adaptive-foraging-hamming.md](../../.claude/plans/adaptive-foraging-hamming.md):
  Path C uses `cyberjunky/python-garminconnect` to pull per-minute BB
  via Garmin Connect REST API (ToS-grey but accepted for personal use);
  Path B decodes `unknown_233` from FIT using Path C as supervised labels.
- Sub-daily signals also confirmed-present in FIT but not yet extracted:
  HRV (the channel H04 hinted at, untested), respiration, SpO2.

---

## 2. What each phase shows — before / during / after a crash

The phase split is the user-natural way to ask "what does the data tell us?"

### 2a. Before a crash (the precursor question)

Across all four daily-aggregate signals we tested, only one cleared its
pre-registered bar in any window:

| signal (3 or 7-day lead-up) | early-era (2022–23) | late-era (2024+) | source |
|---|---|---|---|
| Daily resting HR drift (Workwell rule) | flat | flat, slight inversion | [H01](garmin/hypotheses/H01-rhr-drift/result.md) |
| Daily avg stress | clear positive direction, refuted at strict bar | flat | [H02](garmin/hypotheses/H02-stress-elevation/result.md) |
| Daily sleep efficiency | flat | flat | [H03](garmin/hypotheses/H03-sleep-efficiency/result.md) |
| Daily body-battery net delta | slight inversion | weak positive (almost cleared bar, +13 pp) | [H04](garmin/hypotheses/H04-body-battery/result.md) |
| **Per-minute stress spike duration (max contiguous ≥75 ≥5min), 3-day window** | **SUPPORTED** (71% of episodes, +29.9 pp discrim) | refuted; near-miss | [H02b](garmin/hypotheses/H02b-stress-spikes/result.md) |
| **Per-minute stress spike duration, sentinel-corrected + 4-5 day window (H02d, 2026-06-06)** | **bridge × 5d SUPPORTED at +31.8 pp — strongest train-era single-channel signal of the whole project**; imputed arms refuted (sentinel imputation too generous; ~159 too_active samples/day) | refuted in all 4 arms (imputed × {4d, 5d}, bridge × {4d, 5d}). 5 stress-channel tests now consistent on validate refutation | [H02d](garmin/hypotheses/H02d-stress-spikes-uncensored/result.md) |
| Spike duration before *dips* (2026-06-06) | refuted (+9.1 pp, ~3× weaker than crashes), but criterion C passes | refuted (+5.2 pp), criterion C passes; converges with crash signal | [H02b on dips](garmin/hypotheses/crash_v2-definition/h02b_on_dips_result.md) |
| Activity shock 3-day lead-up (HA01, 2026-06-06) | refuted (+0.7 pp) | refuted (+11.5 pp, close to bar) | [HA01](garmin/activity-labels/output/ha_results.md) |
| **Activity shock 4-day lead-up, rolling baseline (HA01b, 2026-06-06)** | refuted (+8.6 pp, underpowered) | **originally reported SUPPORTED (+17.3 pp) — see next row for re-test** | [HA01b](garmin/activity-labels/output/ha_results_4day.md) |
| **Activity shock 4-day lead-up, lagged baseline (HA01b-recomputed + HA02c, 2026-06-06)** | refuted (+5.8 pp) | **REFUTED (+4.0 pp; -13.3 pp delta vs rolling)** — the original +17.3 pp was substantially a rolling-baseline construction artifact | [bundled re-test](garmin/activity-labels/output/ha_results_4day_lagged.md) |
| **HA01b per-axis decomposition diagnostic (2026-06-07; first diagnostic under consolidated playbook §9)** | composite control reproduces HA01b REFUTED (+3.4 pp); **per-axis: effective_exertion SUPPORTED +21.3 pp** (step_burden close-miss crit-c; vigorous_min misses crit-b at +10.7; max_hr_peak REFUTED) | composite control reproduces HA01b REFUTED (+1.5 pp); **per-axis: effective_exertion SUPPORTED +19.5 pp + step_burden SUPPORTED +16.6 pp + vigorous_min SUPPORTED +24.6 pp** (max_hr_peak REFUTED, inverted -7.7 pp) — only effective_exertion clears both-eras rule; specificity caveat: posterior-per-fire ~2.2% vs 1.7% base rate; **HA01c + v2 pre-registered as pre-committed follow-up** | [per-axis diagnostic](garmin/hypotheses/HA01b-per-axis-diagnostic/result.md) |
| **HA01c effective-exertion shock (per-axis re-formulation, 2026-06-07)** | **SUPPORTED** at locked 0.75 threshold (81.8% freq, +21.3 pp disc, median rank 0.883; n_clean=11) | **SUPPORTED** at locked 0.75 threshold (80.0% freq, +19.5 pp disc, median rank 0.909; n_clean=15) | [HA01c result.md](garmin/hypotheses/HA01c-effective-exertion-shock/result.md) |
| **HA01c v2 threshold-monotonicity diagnostic (2026-06-07; 5th v2 diagnostic; FIRST AMBIGUOUS IN V2 SERIES)** | **AMBIGUOUS** (bumpy-but-never-negative: 15.4→6.4→16.2→21.3→10.3→7.9→2.0→7.3; peak τ=0.75 +21.3 pp; 0 sign-changes — fails all 5 categories) | **RESCUE via Cat 1** (textbook canonical decline: 15.4→24.6→21.0→19.5→13.3→13.3→12.3→6.7; peak τ=0.60 +24.6 pp; ρ=-0.850 — cleanest Cat 1 in v2 round) | [HA01c v2 result.md](garmin/hypotheses/HA01c-threshold-monotonicity-diagnostic-v2/result.md) |
| **H03b per-minute BB overnight recharge (2026-06-07; INCONCLUSIVE × 12 by data availability)** | **INCONCLUSIVE** (0 of 14 crashes have any per-minute BB data; `sleepBodyBattery` empty pre-2024-06) | **INCONCLUSIVE** (only 6 of 15 have data + usable baseline; below locked n=10 threshold; HA10 stays canonical for BB channel) | [H03b result.md](garmin/hypotheses/H03b-bb-overnight-recharge-permin/result.md) |
| Activity shock lag profile (post-hoc, 2026-06-06) | empirical peak at 5d (+15.3 pp; not pre-registered, exploratory only; also subject to the same baseline-construction concern) | empirical peak at 5d (+23.0 pp; exploratory only; same caveat) | [lag profile](garmin/activity-labels/output/lag_profile_report.md) |
| Push burden 3 or 4 day lead-up (HA02 / HA02b / HA02c) | refuted on both baselines | refuted on both baselines | [HA02](garmin/activity-labels/output/ha_results.md) + [HA02c](garmin/activity-labels/output/ha_results_4day_lagged.md) |
| **Morning nightly RHR delta, absolute bidirectional thresholds, lagged baseline (HA06, 2026-06-07)** | refuted (+13.9 pp, 21.4% freq — close but fails crit a; magnitude 3.5 bpm vs 5 bpm bar) | **refuted decisively (0 of 15 crashes trigger at 5 bpm; median max-\|delta\| 1.6 bpm — Wiggers/Workwell-calibrated thresholds exceed this participant's variability range)** | [HA06](garmin/hypotheses/HA06-morning-rhr-delta/result.md) |
| **Morning nightly RHR delta, z-score relative thresholds (HA06b, 2026-06-07)** | **SUPPORTED at N_std=1.5 (71.4% freq, +18.9 pp disc, median \|z\|=2.31); also SUPPORTED at N_std=2.0 (+21.3 pp) — third train-era SUPPORTED autonomic-deviation precursor under clean methodology** | refuted (53.3% freq, +0.8 pp disc — non-discriminative); directionality reversal: train 70% elevated / 30% lowered → validate 25% elevated / **75% lowered** (Wiggers' parasympathetic-swing pattern empirically present at 75% but does not discriminate from null); validate one-sided elevated-only **−16.2 pp** (classical direction anti-predictive) | [HA06b](garmin/hypotheses/HA06b-rhr-zscore/result.md) |
| **Morning BB peak, z-score relative thresholds (HA10, 2026-06-07)** | refuted at 4d primary bidirectional (50.0% freq, **−20.5 pp disc**, 100% lowered direction); 5d one-sided lowered SUPPORTED at +18.3 pp (64.3% freq — Wiggers' canonical "didn't recharge" direction) | **SUPPORTED at 4d primary bidirectional (86.7% freq, +16.2 pp disc, median \|z\|=2.121, 69% elevated direction — paradoxical "looked like a great night but" swing direction); 5d one-sided elevated SUPPORTED at +27.5 pp — FIRST VALIDATE-ERA SUPPORTED IN THE PROJECT under canonical bar.** Era directionality reversal: each era SUPPORTED in opposite direction at the 5d secondary window. Cross-channel coherence with HA06b: BB ∝ vagal tone (inverse to RHR), so opposite-direction-per-era pattern is internally consistent — strongest internal-physiological-consistency evidence in the project. | [HA10](garmin/hypotheses/HA10-bb-overnight-recharge/result.md) |
| **Within-day stress U-dip event count, z-score (HA11, 2026-06-07)** | **SUPPORTED at 4d N_std=1.5 one-sided elevated (64.3% freq, +22.8 pp disc, median signed z=2.168); also SUPPORTED at 4d bidirectional (+16.8 pp) — fourth train-era SUPPORTED autonomic-channel precursor on fourth channel under clean methodology** | refuted inverse-direction (30.8% freq at 4d elevated, **−10.7 pp disc**; scales to **−24.1 pp at 5d N_std=2.0** — strongly anti-predictive); validate-era crashes have FEWER U-dip events than typical 4-5d windows; first within-day pattern test in the project; Wiggers' orthostatic / electrolyte pattern aligns with pre-cliff era, absent / inverse in post-cliff era | [HA11](garmin/hypotheses/HA11-stress-udip/result.md) |
| **Sleep stress mean delta, z-score one-sided elevated (HA07c, 2026-06-07; HRV-proxy substitute for blocked HA07)** | **SUPPORTED at 4d N_std=1.5 (69.2% freq, +23.2 pp disc, median signed z=1.677) — 5th train-era SUPPORTED on 5th channel**; multi-arm robustness (5d secondary +18.4 pp, 4d N_std=2.0 lowered +26.0 pp); directionality split 33% elevated / 67% lowered-at-max-\|z\| (high autonomic VOLATILITY) | refuted (40.0% freq, −6.0 pp disc) | [HA07c](garmin/hypotheses/HA07c-sleep-stress-mean-delta/result.md) |
| **Sleep stress slope (5-day trailing), z-score one-sided elevated (HA08c, 2026-06-07)** | **SUPPORTED at 4d N_std=1.5 (61.5% freq, +23.0 pp disc); 5d secondary +23.2 pp also SUPPORTED — 6th train-era finding; sustained creep mode (Wiggers' "HRV daalt over meerdere dagen na overbelasten")** | refuted (40.0% freq, +1.5 pp disc); strong anti-predictive at N_std=2.0 bidirectional (**−36.2 pp**, validate crashes arrive against unusually-FLAT baseline) | [HA08c](garmin/hypotheses/HA08c-sleep-stress-slope/result.md) |
| **Sleep stress VARIABILITY delta (stdev), z-score BIDIRECTIONAL (HA07d, 2026-06-07; PROJECT FIRST OVERALL-SUPPORTED)** | **SUPPORTED at 4d N_std=1.5 bidirectional (84.6% freq, +19.6 pp disc, median \|z\|=2.541); one-sided elevated +27.4 pp AND one-sided lowered +16.5 pp BOTH SUPPORTED — train crashes preceded by autonomic VOLATILITY in either direction** | **SUPPORTED at 4d N_std=1.5 bidirectional (86.7% freq, +21.7 pp disc, median \|z\|=2.752); validate one-sided LOWERED +28.5 pp at N_std=2.0 — autonomic STILLNESS / freeze signature (variability DROPS before validate-era crashes; autonomic state becomes unusually stable while symptoms continue) — STRONGEST VALIDATE-ERA DISCRIMINATION ON ANY ARM IN THE PROJECT** | [HA07d](garmin/hypotheses/HA07d-sleep-stress-variability/result.md) |
| Lead-up notes language | (less informative than during) | less symptom-warning language, more cognitive-load mention | [notes v2](notes/02-categorize-clauses/categories-analysis-v2.md) |

**Headline takeaway** (revised 2026-06-07 after the threshold-monotonicity v2 round completed — atomic update):

**v2 verdicts (all four diagnostics run with locked v2 five-category shape criteria):**
- **HA10 validate bidirectional → RESCUE** via Cat 3 (rising/late-peak; +14 pp held at N_std=2.0, +11 pp at 2.5, 1 sign-change in [1.0, 3.0], peak at 1.75 with +19.5 pp). HA10 restored to **load-bearing corroborating secondary anchor** for validate-era.
- **HA07d train bidirectional → RESCUE** via Cat 3 (peak 1.75 with +21.4 pp; positive across rise; 0 sign-changes in meaningful range). The reviewer's pre-locked walkthrough prediction confirmed: the discipline binds against the researcher's earlier intuition that "4 direction-reversals = bumpy = CLOSE" — direction reversals are descriptive, sign-changes (zero-crossings) are dispositive, and HA07d train has zero in [1.0, 3.0].
- **HA07d validate bidirectional → RESCUE** via Cat 2 (stable plateau, 8 contiguous tiers > +15 pp from N_std=1.0 to 2.75) AND Cat 3. Strongest restoration in the v2 round.
- **HA11 train one-sided elevated → RESCUE** via Cat 1 (canonical decline; textbook robust shape; peak at 1.25 with +45.4 pp; Spearman −0.683; sign-changes 0).
- **HA06b train bidirectional → CLOSE** via Cat 4 (2 sign-changes in meaningful range; curve crosses zero at N_std=1.0 with disc −4.1 then at N_std=3.0 with disc −2.1). HA06b train **permanently demoted** to non-load-bearing — the discipline binds in the demotion direction too. HA06b's locked +18.9 pp SUPPORTED verdict stays on record.

**Restoration map**:
- **HA07d** is restored as the project's first **overall-SUPPORTED** test (both eras at primary under v2). The era-as-moderator narrative on a single channel is restored.
- **HA10 validate** restored as corroborating secondary anchor for the freeze-pattern.
- **HA11 train** restored as load-bearing (clean Cat 1 canonical decline).
- **HA06b train** permanently demoted (was in interim "pending v2"; v2 confirms demotion). One of four pre-cliff anchors removed.

**Card status after the v2 round**:
- **Card (b2) validate-era retrospective**: anchors restored. **HA07d sleep stress variability lowered direction (primary anchor)** + **HA10 morning BB peak elevated direction (corroborating secondary)**. Both consistent with Wiggers' freeze pattern. Ship is unblocked pending specificity-tables completion (separate Tier 2 item; posterior probability per fire is the gate).
- **Card (b) train-era retrospective**: load-bearing anchors confirmed under v2: H02b stress spike (not yet v2-diagnosed, primitive uses absolute minutes not z-score — v2 framework doesn't apply directly), H02d bridge × 5d (same), HA11 U-dip count (RESCUE Cat 1), HA07d sleep stress variability (RESCUE Cat 3 train). HA07c sleep stress mean delta and HA08c sleep stress slope not yet v2-diagnosed. HA06b RHR z-score **permanently demoted** out of the load-bearing list.

**Project net state after the v2 round**:
- Locked SUPPORTED verdicts on record: unchanged.
- Load-bearing in synthesis: **HA07d (both eras), HA10 (validate corroborating), HA11 (train), H02b/H02d (train, not yet v2-diagnosed)**. HA06b removed.
- Overall-SUPPORTED under canonical bar with v2 shape robustness: **HA07d** (the project's only such finding, now confirmed under v2).
- The methodology playbook gains "threshold-monotonicity v2 diagnostic" as a required step for any test with primary SUPPORTED at the loosest threshold tier.

**Discipline-cost paid in full**: the v1 demotions stood until v2 ran. HA06b genuinely lost load-bearing status (one of four findings). The restorations are principled — Cat 3 (rising/late-peak) captures a robust shape the v1 criteria missed; Cat 1/2 cleanly apply to the canonical/plateau shapes. The v2 framework is now the project's locked methodology for threshold-tier sweep diagnostics.

**HA01b per-axis diagnostic finding (2026-06-07, first diagnostic under consolidated playbook)**: HA01b composite REFUTED was hiding a per-axis signal. Decomposed into 4 axes, **effective_exertion is SUPPORTED both eras** (train +21.3 pp, validate +19.5 pp, ~80% freq). Two more axes SUPPORTED in validate only (step_burden +16.6 pp, vigorous_min +24.6 pp); max_hr_peak REFUTED both eras (consistent with chronotropic incompetence). Composite control reproduces HA01b REFUTED at +3.4 / +1.5 pp — confirms the per-axis decomposition is honestly extracting signal the MAX-rank composite obscured. **Both-eras rule reduces load-bearing to 1 axis (effective_exertion)**. Cross-axis Spearman 0.31-0.69 (effective N ≈ 2.5). **Critical specificity caveat**: at the locked 0.75 threshold, ~60% of any 4-day window triggers in the null distribution — posterior-per-fire ~2.2% vs 1.7% base rate. HA01b composite REFUTED stays on record; the per-axis diagnostic produces a **diagnostic finding**, NOT a re-test verdict, per playbook §5.2. Generalisable methodology lesson: MAX-rank composites can dilute per-axis signal in the null distribution; landed in playbook §3.8 addendum. Full result + caveats: [HA01b per-axis diagnostic result.md](garmin/hypotheses/HA01b-per-axis-diagnostic/result.md).

**HA01c + HA01c v2 outcomes (2026-06-07, same-day execution after per-axis diagnostic)**: HA01c locked-threshold verdict is **SUPPORTED both eras** at τ=0.75 (numbers identical to per-axis diagnostic: train +21.3 / validate +19.5 pp; disciplinary re-run, not informational; HA01b composite REFUTED stays on record per playbook §2.2). HA01c v2 threshold-monotonicity diagnostic returned a **MIXED verdict — first AMBIGUOUS in the v2 series**: train AMBIGUOUS (bumpy-but-never-negative shape 15.4→6.4→16.2→21.3→10.3→7.9→2.0→7.3; peak τ=0.75 +21.3 pp; 0 sign-changes so doesn't fit Cat 4; peak not in [0.50, 0.70] or ≥ 0.80 so doesn't fit Cat 1 or Cat 3); validate RESCUE via Cat 1 (textbook canonical decline 15.4→24.6→21.0→19.5→13.3→13.3→12.3→6.7; peak τ=0.60 +24.6 pp; ρ=-0.850 — cleanest Cat 1 in v2 round). **Per playbook §4.4 both-eras rule, HA01c stays SUPPORTED-with-stability-mixed — honest at τ=0.75 but NOT load-bearing**. The locked v2 framework correctly surfaces the train edge case rather than forcing a fit. **No HA01c card.md drafted** per playbook §2.7 (card-craft rule: only if SUPPORTED + specificity tables pass) AND §6.2 (2.2% posterior per fire already blocked card draft regardless of v2 outcome). **Project net state**: effective_exertion joins the noted-but-not-load-bearing list; HA07d remains the only project-level overall-SUPPORTED + v2-validated finding (both eras RESCUE). Discipline binds in both directions: HA06b was permanently demoted by v2 CLOSE; HA01c is admitted but bounded by v2 AMBIGUOUS. Full results: [HA01c result.md](garmin/hypotheses/HA01c-effective-exertion-shock/result.md) + [HA01c v2 result.md](garmin/hypotheses/HA01c-threshold-monotonicity-diagnostic-v2/result.md).

**H03b per-minute BB overnight recharge outcome (2026-06-07, executed after HA01c chain)**: **INCONCLUSIVE × 12** (all evaluation cells; 3 N_std × 2 windows × 2 eras). Data-availability investigation 2026-06-07 surfaced two Garmin API cutover dates: `bodyBatteryChange` daily scalar populated from ~2023-12-31, `sleepBodyBattery` per-3-min array populated from ~2024-06-03. Of 29 crash_v1 episodes, only 6 of 15 validate crashes have BOTH per-minute data AND a usable lagged baseline (the baseline window [d-90, d-30] needs ≥40 valid days, stabilising only ~Sept 2024). Train has zero coverage. **Locked n_clean ≥ 10 threshold from hypothesis.md §5 binds**. User pre-committed (2026-06-07) to running H03b as-locked and accepting the verdict rather than lowering the threshold mid-run (which would have required H03c per playbook §2.2). **Endpoint clarification audit trail**: hypothesis.md §3 had specified the `/wellness-service/wellness/bodyBattery/events/{date}` endpoint; investigation showed this returns event records (sleep/activities/naps), not per-minute samples. The per-3-min BB during sleep window is available via `get_sleep_data().sleepBodyBattery` — already captured in path C sleep backfill (no separate BB backfill needed). Per playbook §2.5, this is an implementation-source clarification, not a spec change. **HA10 stays canonical for BB overnight recharge channel** (validate SUPPORTED at +16.2 pp, v2 RESCUE Cat 3). H03b sharpening test is **re-runnable only after path B FIT decode of `unknown_233` unlocks per-minute BB for the old corpus**. Methodology lesson banked: when a pre-registered hypothesis depends on a third-party API endpoint, verify data availability across the analysis window BEFORE locking the inconclusive threshold. Full result: [H03b result.md](garmin/hypotheses/H03b-bb-overnight-recharge-permin/result.md).

**Tier 2 specificity tables for load-bearing anchors (2026-06-07, urgent Tier 2 peer-review item)**: locked per [specificity-tables-spec.md](garmin/methodology/specificity-tables-spec.md). Derivative Bayes computation over locked result-data.json files (no new hypothesis tests, no new null draws). Base rates: train 14/485 = 2.89%; validate 15/887 = 1.69%. **DECISIVE FINDING: all 9 load-bearing anchors land in Tier C** (lift < 2× or precision < 5% — retrospective annotation only, NOT viable as forward-warning cards). Best train: H02b 3d at **4.87% precision, 1.69× lift** (lift = recall/null_fire = 0.714/0.415). Best validate: HA07d 4d N_std=1.5 bidirectional at **2.24% precision, 1.33× lift** (0.867/0.65). Zero anchors reach Tier B (5-30% precision + 2-5× lift) or Tier A (≥30% + ≥5×). **Critical structural insight**: lift ≈ recall/null_fire is independent of base rate; the 2× lift threshold cannot be cleared at any base rate because no anchor's recall/null_fire ratio exceeds 2×. The hypothesis-test 3-criterion bar confirms metrics differ between crash and null windows, but does NOT confirm forward-predictive viability. **Card framing implications**: Card (b) train-era retrospective and Card (b2) validate-era retrospective both restricted to **retrospective-annotation-only surfaces** per playbook §6.6 no-go list. No crash-risk percentages, traffic lights, push notifications, or automated targets — even for HA07d which is the project's only overall-SUPPORTED + v2-validated finding. The acceptable surface is timeline annotation during after-the-fact review, paired with the gevoelscore record. Full tables: [card-b-train-specificity.md](garmin/cards/card-b-train-specificity.md) + [card-b2-validate-specificity.md](garmin/cards/card-b2-validate-specificity.md).

**Tier 2 statistical audits (2026-06-08, Fisher's exact + cross-channel correlation)**: two cheap derivative computations over locked result-data.json + per-day primitive CSVs. **Fisher's exact + 95% CIs on 11 primary verdicts** ([primary-verdict-statistics.md](garmin/cards/primary-verdict-statistics.md)): only **H02b train (p=0.029) and H02d bridge × 5d train (p=0.011) reach α=0.05** one-sided. Zero reach Bonferroni α=0.005. HA07d train (+19.6 pp, p=0.0934), HA07d validate (+21.7 pp, p=0.0703), HA10 validate (+16.2 pp, p=0.1475), HA01c train+validate (+21.3/+19.5 pp, p=0.136/0.109) — all fail α=0.05. **The project's 60%/15pp/magnitude bar is more permissive than conventional α=0.05 statistical significance** with n=14-15 crashes; this is a conscious choice for n-of-1 exploratory work but should be documented honestly. **Cross-channel correlation matrix** ([cross-channel-correlation.md](garmin/cards/cross-channel-correlation.md)): two paradigm-shifting findings — (1) **H02b ≡ H02d at the per-day primitive level (ρ = +1.000, identical for all 1737 shared valid days)** — the "six channels with seven SUPPORTED tests" framing must drop H02d as a separate channel; it's the same primitive evaluated at a different window. (2) **HA10 ≡ −HA07c (ρ = −0.922)** — morning BB peak and sleep stress mean are nearly the same underlying signal in opposite signs (structural in Garmin's BB algorithm). HA10 and HA07c are NOT independent channels. (3) Mean |ρ| per channel: HA10 (0.366) and HA07c (0.343) most central; H02b (0.254), HA11 (0.169), HA06b (0.150), HA07d (relatively independent at 0.193). **Effective N of independent signal clusters: ~3-4 (not 7)** — Cluster 1 within-day stress (H02b/H02d + HA11), Cluster 2 autonomic state (HA07c + HA10 ± HA06b), Cluster 3 autonomic variability (HA07d, partially tied to Cluster 2). **Honest effective-N Bonferroni**: α = 0.05/4 ≈ 0.0125; only H02d (p=0.011) clears it. But H02b/H02d collinearity means **only ONE distinct primitive survives honest effective-N statistical-significance correction**. The discrimination findings are real; the "many converging channels" framing was overstated. This profoundly tightens the load-bearing list and is now under-pinned by numbers, not by sentence-caveats.

The autonomic-deviation precursor is **era-moderated** (per the peer-reviewed framing fix): pre-cliff crashes preceded by autonomic VOLATILITY (variability shifts in either direction); post-cliff crashes preceded by autonomic STILLNESS (variability collapse / paradoxical "looks like great recovery"). HA07d demonstrates this directly on a single channel — the era reversal is now a *within-test* finding, not a cross-channel inference.

The pre-cliff era's precursor signature is demonstrated across **six distinct channels with seven SUPPORTED tests** (the sleep-stress channel was tested through three primitives — mean delta, slope, variability — and all three SUPPORTED in train): H02b stress spike 3d, H02d bridge × 5d, HA06b RHR z-score 4d, HA11 U-dip count 4d, HA07c sleep stress mean delta 4d, HA08c sleep stress slope 4d, HA07d sleep stress variability delta 4d. Note that channels are **not statistically independent** — Body Battery is a fused composite of HR / HRV / stress / sleep, and sleep stress is per-minute stress restricted to the sleep window. The "six channels" framing reflects six distinct measurement axes, not six independent samples of nature. Card (b) train-era retrospective card has seven converging empirical anchors with this caveat acknowledged.

The post-cliff era's precursor signature has **one load-bearing anchor** after the HA10 threshold-monotonicity diagnostic CLOSE verdict (2026-06-07): **HA07d sleep stress variability lowered, robust across thresholds N_std=1.5 and 2.0, +21.7 to +28.5 pp discrimination**. HA10 morning BB peak elevated direction was previously framed as a corroborating-but-fragile second anchor; the diagnostic ([HA10-threshold-monotonicity-diagnostic/result.md](garmin/hypotheses/HA10-threshold-monotonicity-diagnostic/result.md)) confirmed via a fine N_std grid that HA10's primary bidirectional arm peaks at N_std=1.75 (one σ-tier past the pre-committed rescue window [1.0, 1.5]) and triggers the locked CLOSE clause. HA10's pre-registered SUPPORTED verdict stays on record under pre-registration discipline; but the validate-era narrative no longer leans on HA10 as a load-bearing finding. Nuance: HA10's one-sided ELEVATED arm (Wiggers' paradoxical-swing direction) IS threshold-robust (+23 pp plateau N_std=1.5 → 2.5), so the *direction* HA10 identified is supported; only HA10's specific bidirectional-primary choice failed the monotonicity diagnostic. Both are consistent with the parasympathetic-swing / freeze pattern. Card (b2) validate-era retrospective is Tier 1 with two anchors, but **card framing must explicitly use specificity / posterior-probability language**: HA07d validate fires on 86.7% of crashes AND 65% of random non-crash days — discrimination magnitude is NOT the same as conditional probability of a crash given the card fires. See §4 below for the calibrated card framing.

Sub-headlines below for completeness: For pre-cliff (2022-23) era crashes, the autonomic-deviation precursor is now demonstrated across **four independent channels** — H02b per-minute stress spike count at 3d (+29.9 pp), H02d sentinel-corrected stress spike at 5d bridge arm (+31.8 pp — strongest train signal of the project), HA06b nightly RHR z-score at 4d (+18.9 pp, 71.4% freq), and **HA11 within-day U-dip count z-score at 4d (+22.8 pp, 64.3% freq)**. Four SUPPORTED train findings on four different channels (per-minute stress, per-minute stress corrected, per-night RHR z-score, within-day U-dip count) on four different time-scales / pattern types, all converging on the same train-era crashes — **strongest multi-channel convergence in the project**. For post-cliff (2024+) era crashes, **HA10 (morning BB peak z-score, 4d primary bidirectional) is SUPPORTED at +16.2 pp / 86.7% freq / median |z|=2.121 — the FIRST validate-era SUPPORTED test in the entire investigation under the canonical 3-criterion bar**. 13 prior pre-registered tests had refuted validate-era. HA10's directionality split is striking: train 100% lowered direction (canonical Wiggers "didn't recharge"), validate 69% elevated direction (paradoxical "looked like a great night but" swing pattern). At the 5d secondary window, **each era is SUPPORTED in its respective opposite direction** (train +18.3 pp lowered, validate +27.5 pp elevated) — cleanest era-directionality reversal in the project. Cross-channel coherence with HA06b is strong: BB is inversely-related to RHR via the vagal-tone pathway, so the opposite-direction-per-era pattern is internally consistent. HA11 contributes a fifth era-directional finding: train SUPPORTED elevated direction (+22.8 pp); validate refuted *inverse* direction (−10.7 pp at 4d, −24.1 pp at 5d N_std=2.0) — the inverse signal is itself a characteristic signature of the parasympathetic-swing era. **The era directionality reversal is now formalised across four channels** (stress, RHR, U-dip, BB): pre-cliff era = sympathetic-arousal-spectrum events fire; post-cliff era = parasympathetic-swing-spectrum events fire. **Wiggers' "freeze" pattern is empirically population-level visible in two independent channels** (HA06b lowered RHR + HA10 elevated BB) for validate-era crashes — not just lived-experience anecdote, but a quantitative signature with discriminative frequency rates. The b retrospective card (train-era) now has FOUR converging empirical anchors (H02b + H02d + HA06b + HA11) — strongest empirical anchoring for any card concept. The b2 retrospective card (validate-era) regains an empirical anchor on HA10 elevated BB peak (promote back to Tier 1 candidate, pending H04b per-minute trajectory enrichment). The 4-5 day empirical lag is now confirmed across four channels. Methodology lesson banked: **pre-register relative thresholds (z-score or percentile rank) as the default for autonomic-channel tests**; HA07 (HRV, gated on H04b path C authorisation), HA08, and HA10 all follow this lesson. Direction shifts firmly to (i) H04b path C authorisation as the highest-leverage next step (unlocks HRV channel HA07/HA08/HA12 AND per-minute BB H03b proper, sharpens HA10's validate-era signal), (ii) C.3 personal-lag teaching (4-5 day lag now four-channel confirmed), and (iii) HA11's invitation to re-look at train-era notes around U-dip-elevated days for orthostatic / hydration / ORS mentions.

### 2b. During a crash (the symptom and topology signature)

This is where the data is strongest. Crash days have a clear and
reproducible signature, and the signature has shifted across the
stabilisation transition.

**The reliable signature** (from notes v2 categorisation, all 59
crash days with notes):

| signature | crash rate | vs. non-crash | source |
|---|---:|---:|---|
| Physical symptom mentioned (hoofdpijn, koorts, etc.) | 92% | 68% | notes v2 |
| Cognitive symptom mentioned (brainfog, mistig) | 19% | 6% | notes v2 |
| External-illness trigger (corona, griep, keelpijn) | 5% | <1% | notes v2 (8.7x ratio) |
| Emotional load mentioned (load not symptom) | 7% | 4% | notes v2 (2.9x ratio) |

**The era-shift in crash signature** (early vs late, on crash days):

| dimension | early | late | shift |
|---|---:|---:|---|
| symptoom_fysiek state = severe | 4% | 22% | **+18 pp** |
| symptoom_fysiek state = present (default) | 81% | 69% | −13 pp |
| `belasting_gezin` mentioned | 0% | 22% | **+22 pp** |
| `symptoom_cognitief` (brainfog etc.) | 11% | 25% | **+14 pp** |
| `triggers_extern` | 7% | 3% | −4 pp |
| day is "mixed-day topology" (positive content + crash) | 11% | 50% | **+39 pp** |

**Headline takeaway**: residual crashes are categorically different
in their during-crash signature, not just less frequent. They're
more often severe in physical-symptom intensity, more often paired
with caregiving context (kids, partner), more cognitive-symptom-heavy,
fewer infection-triggered, and crucially **more often embedded in
days that also contain functional/positive content** — the crashes
are less totalizing.

### 2c. After a crash (recovery / aftermath)

Less mature than during-crash. Two threads:

- **H05 (recovery time)** was spec-broken (recovery target structurally
  trivial). [H05b](garmin/hypotheses/H05-recovery-time/result.md)
  queued with a sustained-recovery target.
- **Long-arc stabilisation visible across the whole window**
  ([S01 trajectories](garmin/hypotheses/S01-stabilisation-trajectories/notes.md)):
  - Max stress-spike duration: 10.5 min (pre-LC) → **13.2 min** (mid-2023
    peak) → **5.8 min** (Apr 2025 trough) → 11.4 min (May 2026 uptick)
  - Avg stress baseline: 32.6 → 36 → 29 → 33.7 (recent uptick)
  - RHR: mostly stable, but **notable recent rise to 60.8 bpm in May
    2026** (highest in the whole window)
  - Sleep efficiency: flat at ~99% throughout (the body's sleep
    continued to work through everything)

The stabilisation-arc card is now empirically anchored across multiple
biometric dimensions, plus the per-episode K## findings (depth, duration).

---

## 3. The directional findings supporting the "kind of crash changed" theory

A single tabulated view of how the picture coheres across H##, K##,
notes, `crash_v2`, and the autonomic-channel sibling family:

| axis | source | direction (early → late) |
|---|---|---|
| stress precursor (daily avg) | H02 | yes → no |
| stress precursor (spike count, 3d) | H02b | train SUPPORTED +29.9 pp → validate refuted |
| **stress precursor (spike count, 4-5d, sentinel-corrected)** *(new 2026-06-06)* | **H02d** | **train SUPPORTED bridge × 5d +31.8 pp (project-strongest) → validate refuted in all 4 arms** |
| **RHR z-score deviation, 4d lagged baseline** *(new 2026-06-07)* | **HA06b** | **train SUPPORTED +18.9 pp at N_std=1.5 (71.4% freq) → validate refuted +0.8 pp; directionality reversal: train 70% elevated → validate 75% lowered (parasympathetic swing physiologically present but non-discriminative)** |
| **Morning BB peak z-score, 4d lagged baseline** *(new 2026-06-07)* | **HA10** | **train refuted (−20.5 pp, 100% lowered direction) → validate SUPPORTED +16.2 pp at N_std=1.5 (86.7% freq, 69% elevated — PARADOXICAL SWING DIRECTION); FIRST validate-era SUPPORTED in the project; 5d each-era opposite-direction SUPPORTED** |
| **Within-day U-dip count z-score, 4d lagged baseline** *(new 2026-06-07)* | **HA11** | **train SUPPORTED +22.8 pp at N_std=1.5 (64.3% freq, elevated direction) → validate refuted inverse-direction (−10.7 pp at 4d, −24.1 pp at 5d N_std=2.0); FOURTH train-era SUPPORTED on the FOURTH channel — strongest multi-channel convergence in the project** |
| **Sleep stress mean delta z-score, 4d lagged** *(new 2026-06-07 — HRV proxy)* | **HA07c** | **train SUPPORTED +23.2 pp (69.2%, elevated direction); validate refuted (-6.0 pp); 5th train-era SUPPORTED; HRV proxy validated for train; train directionality split shows VOLATILITY (33% elev / 67% lowered at max-\|z\|)** |
| **Sleep stress slope z-score, 4d lagged** *(new 2026-06-07)* | **HA08c** | **train SUPPORTED +23.0 pp (61.5%, elevated direction); validate refuted (+1.5 pp, anti-predictive at higher thresholds); 6th train-era SUPPORTED — Wiggers' "HRV daalt over meerdere dagen na overbelasten" creep mode confirmed** |
| **Sleep stress VARIABILITY delta z-score, 4d lagged BIDIRECTIONAL** *(new 2026-06-07; PROJECT FIRST OVERALL-SUPPORTED)* | **HA07d** | **TRAIN +19.6 pp SUPPORTED + VALIDATE +21.7 pp SUPPORTED → OVERALL SUPPORTED at primary; validate ONE-SIDED LOWERED +28.5 pp at N_std=2.0 — strongest validate-era discrimination in project; validate signature is AUTONOMIC STILLNESS (variability collapse / freeze pattern)** |
| crash depth (score nadir) | K01 | late shallower (no score-1) |
| crash duration (span) | K02 | late shorter (long-tail 5→1) |
| crash language: symptom severity | notes v2 | late severe-symptom +18 pp |
| crash language: day topology | notes v2 | late mixed +39 pp |
| lead-up language | notes v2 | late less warning, more cognitive |
| **dip:crash ratio** *(new 2026-06-06)* | **crash_v2** | **1.9× → 3.5×** (more transient single-day events) |

Plus one cross-class **convergence** finding:

| axis | source | direction (early → late) |
|---|---|---|
| **crash vs dip precursor magnitude** *(new 2026-06-06)* | **H02b on dips** | **+29.9 pp / +9.1 pp (3× ratio, train) → −8.2 pp / +5.2 pp (converged, validate)** |

And one within-class structure finding:

| axis | source | direction (early → late) |
|---|---|---|
| **dip cluster concentration** *(new 2026-06-06)* | **crash_v2 cluster overlay** | **5 clusters / 13 dips train → 10 clusters / 32 dips validate** (multi-day rough patches concentrate in residual era) |

**Fifteen directional findings on independent axes, plus a
cross-class convergence, no contradictions.** The cumulative weight
is now overwhelming.

**Seven train-era SUPPORTED tests on record across SIX distinct
channels** (sleep-stress channel through three primitives — mean
delta, slope, variability — all SUPPORTED in train): H02b stress
spike count 3d, H02d bridge × 5d stress spike, HA06b RHR z-score
4d, HA11 within-day U-dip count 4d, HA07c sleep stress mean delta
4d, HA08c sleep stress slope 4d, HA07d sleep stress variability
delta 4d.

**Post-v2 status** (atomic update 2026-06-07 after all four v2
diagnostics completed):
- **HA10 validate**: RESCUED via Cat 3 (rising/late-peak).
  Restored as corroborating secondary anchor.
- **HA07d both eras**: RESCUED — train via Cat 3, validate via
  Cat 2 + Cat 3. Restored as primary load-bearing anchor;
  overall-SUPPORTED status restored.
- **HA11 train**: RESCUED via Cat 1 (canonical decline; textbook
  robust shape). Restored to load-bearing.
- **HA06b train**: CLOSED via Cat 4 (2 sign-changes in [1.0, 3.0]).
  Permanently demoted to non-load-bearing. Locked +18.9 pp
  SUPPORTED verdict stays on record. One of four anchors removed
  from the train-era load-bearing list.

Net effect on the train cluster: H02b + H02d + HA11 + HA07d
confirmed load-bearing under v2 (where v2 was applicable); HA06b
removed; HA07c + HA08c not yet v2-diagnosed. Six-channel narrative
becomes "five channels with three sleep-stress primitives" with
HA06b channel removed.

**Honest caveat on channel independence** (per peer-review §3
critique): channels are NOT statistically independent. Body Battery
is `g(HR, HRV, stress, sleep)`; sleep stress is per-minute stress
restricted to the sleep window; HA07c/HA08c/HA07d are three
primitives of the same underlying sleep-stress channel. The "six
distinct channels" framing reflects six distinct measurement axes,
not six independent samples of nature. A more honest reading: the
project has identified an underlying autonomic-state construct that
manifests across multiple operationalisations, most of which
SUPPORT in train. The pre-cliff sympathetic-overarousal precursor
signature is well-replicated; "convergence" overstates the
independence of the convergence axes.

The train-era retrospective card (b) has seven converging empirical
anchors with this caveat acknowledged in card copy.

**TWO validate-era SUPPORTED autonomic-channel precursors**:
HA10 morning BB peak z-score 4d (elevated direction, paradoxical
"swing" — +16.2 pp); **HA07d sleep stress variability delta 4d
bidirectional (one-sided lowered SUPPORTED at +21.7 pp at
N_std=1.5, +28.5 pp at N_std=2.0 — autonomic stillness /
freeze)**. Both consistent with Wiggers' "freeze" pattern. The
b2 retrospective card now has TWO empirical anchors — promote to
Tier 1 with anchors.

**ONE OVERALL-SUPPORTED test on record** (HA07d) under the strict
locked rule — the first in 19 pre-registered hypotheses. However,
**HA07d's bidirectional primary closes per the threshold-
monotonicity diagnostic v1 (CLOSE both eras 2026-06-07)** —
synthesis-level framing demotes HA07d from load-bearing per the
diagnostic's locked rescue/close rule, even though HA07d's
locked SUPPORTED verdict stays on record per audit-trail
discipline. The era reversal at the per-direction-arm level
(train SUPPORTS both directions of variability shift; validate
SUPPORTS only the lowered direction) is still observable in
HA07d's result.md data, but the synthesis-level claim that HA07d
load-bears the era-as-moderator finding is paused pending v2
diagnostic outcomes.

**Era directionality reversal formalised across multiple
channels.** Train era: sympathetic-arousal-spectrum + autonomic-
volatility events fire (elevated stress spikes, elevated RHR,
elevated U-dip count, elevated sleep stress delta, elevated sleep
stress slope, VOLATILE sleep stress variability). Validate era:
parasympathetic-swing-spectrum + autonomic-stillness events fire
(elevated BB peak, LOW sleep stress variability — the
"freeze" / paradoxical "looked like great recovery" signature).
**Wiggers' "freeze" pattern is empirically population-level
visible** in two independent biometric channels (HA10 + HA07d)
for validate-era crashes at substantial discrimination magnitudes.

---

## 4. Candidate indicators for the app — ranked by evidence

The candidates fall into three confidence tiers. Each is a card concept,
not a fully designed feature.

### Tier 1 — Strong evidence, ready to prototype

These have multi-axis empirical support. Build first.

**a. The stabilisation-arc card (retrospective).** A long-arc view of
the user's journey: crash frequency by year, stress baseline shift,
spike-duration compression, sleep stability, **plus the score-side
distribution shift now empirically anchored by [S02](garmin/hypotheses/S02-score-trajectory/notes.md)
(executed 2026-06-07)**. Backed by seven directional findings (§3),
the S01 biometric trajectories, and S02's score-distribution evolution
(tail-collapse on the worst end: score≤3 share 20% → 7%; emergence
of a new upper mode: score=6 share 2% → 12%; trajectory shape
characterised algorithmically with peak 2023-01-27, trough
2025-01-10, all-time-high at corpus edge 4.72). Frames the
recovery story honestly: not "you're recovered" and not "you're
still ill" — "you're stabilising, here's the arc."

*Caveat re reading the S02 vs S01 trajectories together:* the score
LEADS the Garmin pendulum at trajectory-level turnaround dates
(S02 T1 fired: score peaks 149d before avg-stress; troughs 100d
before max-spike), BUT [S02b](garmin/hypotheses/S02b-score-lead/notes.md)
refuted the daily-resolution version of this lead. The
score-leads-Garmin story for the card is a TRAJECTORY-LEVEL pattern
only; it should NOT be presented as "your score predicts your
biometrics" in the card copy. The honest framing is "your typical-day
band reshaped before your biometric pendulum did, in the smoothed
view." [S02c](garmin/hypotheses/S02c-may2026-divergence/notes.md)
further nuances the recent perturbation framing: against the recent
180d daily baseline, only RHR shows directional drift; the rest are
essentially unmoved.

**b. The per-crash retrospective card for pre-2024 crashes.** Now
with SEVEN converging empirical anchors (H02b spike 3d / H02d
bridge × 5d / HA06b RHR / HA11 U-dip / HA07c sleep stress mean /
HA08c sleep stress slope / HA07d sleep stress variability) — though
**three of those seven are sleep-stress primitives on the same
underlying channel** (per peer-review §3 channel-independence
critique). Honest framing: six distinct measurement axes, well-
replicated via multiple operationalisations on the train side.

Card framing example: "Around 5 March your stress was at ~30 most
of the day, but a 22-minute spike to 88 in the afternoon — what was
happening?" Train-era crashes show this autonomic-deviation pattern
across multiple measurements; the card surface picks the most
visually-intuitive single anchor (likely the H02b stress spike) and
mentions the broader signature in a tooltip.

**Same card specificity caveat as b2 applies here.** Train H02b
discrimination is the strongest in the project (+29.9 pp) but the
card still fires on ~42% of non-crash days under train-era base
rates. Calibrated framing required before card.md is written.
Works for historical (2022–23) crashes; less reliable on 2024+
residual crashes — for those, see card (b2).

**b2. The per-crash retrospective card for validate-era crashes
(history: Tier 1 on HA01b 2026-06-06 → downgraded to Tier 2 after
Theme A → promoted Tier 1 candidate after HA10 → promoted Tier 1
ANCHORED ON HA07d after HA07d OVERALL-SUPPORTED → HA10 anchor
dropped after HA10 threshold-monotonicity diagnostic CLOSE →
**HA07d anchor DROPPED 2026-06-07 after HA07d threshold-
monotonicity diagnostic CLOSE both eras per locked v1 rule** →
CANNOT SHIP ANCHORED in v1 framework).**

**Current status (post-v2 atomic update 2026-06-07): card b2 has
TWO LOAD-BEARING EMPIRICAL ANCHORS RESTORED under v2 criteria.**

1. **HA07d sleep stress variability delta (PRIMARY anchor)**:
   v2 RESCUE both eras (train Cat 3, validate Cat 2 + Cat 3).
   Locked SUPPORTED verdict +21.7 pp validate (86.7% freq) at 4d
   primary bidirectional; restored to load-bearing under v2 with
   the revised-criteria reasoning cited. **Lowered direction**
   ("autonomic state became unusually stable / frozen").
2. **HA10 morning BB peak z-score (CORROBORATING secondary
   anchor)**: v2 RESCUE via Cat 3 (rising/late-peak). Locked
   SUPPORTED verdict +16.2 pp validate (86.7% freq); restored as
   corroborating-secondary (HA07d carries primary load-bearing).
   **Elevated direction** ("looked like great recharge").

Both anchors are consistent with Wiggers' "freeze" /
parasympathetic-swing pattern. The discipline-cost paid in the
v1 demotion was real (held until v2 ran), but the v2 strict
reading restored both findings via Cat 3 and Cat 2 + Cat 3
respectively. The restoration is principled — Cat 3 captures a
robust shape (rising/late-peak with disc sustained at strict
tiers) that the v1 criteria failed to recognise.

**Card specificity caveat — STILL REQUIRED before card.md is
written** (per peer-review §5.3): the v2 RESCUE confirms shape
robustness of HA07d's discrimination. It does NOT translate to
"card is right when it fires." Bayesian arithmetic per the
earlier b2 section: P(crash within 4 days | HA07d primary fires)
≈ 2.3% under base rate. The card text MUST use specificity /
posterior-probability language.

Ship pathway: BOTH (i) v2 RESCUE (achieved 2026-06-07) AND
(ii) specificity tables (queued Tier 2 action item) before
card.md is written.

**HA10 morning BB peak — DROPPED as a load-bearing card anchor**
per the [HA10 threshold-monotonicity diagnostic](garmin/hypotheses/HA10-threshold-monotonicity-diagnostic/result.md)
locked-rule CLOSE verdict. The diagnostic ran a fine N_std grid
[0.5 → 4.0] and found HA10's primary bidirectional arm peaks at
N_std=1.75 (one σ-tier past where the locked rescue criterion
required), triggering the CLOSE clause per pre-registered shape
criteria. **HA10's locked SUPPORTED verdict stays on record**
(pre-registration discipline: locked verdicts don't unlock); but
synthesis-level framing demotes HA10 to non-load-bearing. Honest
nuance: the diagnostic also shows HA10's one-sided ELEVATED arm
(Wiggers' paradoxical-swing direction) is threshold-robust
(+23 pp plateau from N_std=1.5 through 2.5), so the directional
finding is supported; only HA10's specific bidirectional-primary
choice was the fragile call. Card text may still mention BB peak
as descriptively consistent with the freeze pattern but must not
treat it as an independent precursor anchor.

**Card specificity caveat — REQUIRED before card.md is written**
(per peer-review §5.3 critique on retrospective-card
under-instrumentation):

Discrimination magnitudes do NOT translate directly to "card
correctness when it fires." Bayesian arithmetic for HA07d
validate primitive: 86.7% fire rate on crashes; 65.0% fire rate
on random non-crash 4d windows; validate-era base rate ~1.7%
(15 crashes / ~890 days). **Posterior**: P(crash within 4 days |
card fires) ≈ (0.867 × 0.017) / (0.867 × 0.017 + 0.65 × 0.983) ≈
**2.3%**.

The card fires on ~65% of validate-era days but tells the truth
~2 in 100 times when it fires. This is NOT a predictive card; it
is a **retrospective explanation** card — fired AFTER a crash to
describe what the data looked like in the lead-up. The card text
must NOT promise prediction.

Acceptable framing: *"After this crash, looking back at the 4
days before: the data shows your overnight autonomic state was
unusually stable AND your body battery peaked unusually high.
This is the 'freeze' signature — the body appearing stable while
symptoms continue."*

UNacceptable framing: *"Watch for this pattern; it precedes
crashes"* (this would be calibrated to discrimination magnitude,
not posterior probability — it would generate false alarms ~98% of
days the user looks at it).

Formal specificity tables (precision / recall / posterior per
arm) added to QUEUED-WORK Tier 2 before any card.md is written.

Ship is unblocked AS A RETROSPECTIVE SURFACE only.

**c. The crash-day signature card.** "On this crash day you mentioned
[physical symptom], [cognitive symptom], [emotional load].
Caregiving was in the background." Built from notes v2
categorisation. Doesn't predict — describes.

**d. The mixed-day topology card.** "Your crashes increasingly happen
on days where good things also happen — your body is finding edges."
Backed by the +39 pp finding in late-era crashes. Powerful framing
for the user's own recovery narrative.

**e. The recent-perturbation awareness card.** "Your RHR is up about
5 bpm in the last few months." Three of four trajectory metrics
moved up together in May 2026. Worth surfacing as awareness, not
alarm.

### Tier 2 — Promising, needs more work or supports a v2

**f. The spike-detection retrospective card for new crashes** (not
prediction). Same shape as (b) but framed: "we see a notable spike
that day but the pattern is less consistent than it used to be."
Fires on ~33% of validate-era crashes with a real spike; rest get a
honest "we don't see an unusual spike pattern before this crash."

**g. Caregiving-context tagging on late-era crashes.** 22% of
late-era crash days mention family/caregiving load. Could surface
as a context tag: "this crash was on a day with caregiving demands."
Needs the eventual app tagging feature to land (research first per
the discipline).

**h. Sleep-as-protector reframe.** Direct positive copy: "your sleep
efficiency has stayed stable at ~99% through this whole journey." The
"good sleep is not a protector" reframe — sleep didn't prevent
crashes but also wasn't disrupted by them. Useful framing, low-risk.

### Tier 3 — Candidates pending further research

Wait for follow-up work before building.

**i. Body-battery intra-day rise/drop occurrences.** User insight
("BB-rise occurrences are themselves meaningful"; afternoon-nap
recovery; sharp drops as stress events). Needs per-minute BB data —
either decode `unknown_233` (FIT-level research) or hit Garmin
Connect REST API. Queued as H04b.

**j. The shielder-vs-reliever experiment.** The eventual pacing-doc
ambition: "did intervention X reduce crash depth or recovery time?"
Needs an `interventie` category in the notes dictionary AND the
recovered H05b sustained-recovery metric. Substantial work, big
payoff if it lands.

**k. Recovery-time card (per crash).** Pending H05b spec fix.

---

## 5. What we know NOT to build

Each of these would look reasonable on first inspection but would
mislead the user.

- **A daily Garmin tile dashboard.** RHR / stress / sleep / body-battery
  as four daily numbers next to today's score. Accurate but useless:
  the daily aggregates don't predict residual crashes. We'd be
  selling a false sense of warning signal.
- **A "you might crash tomorrow" predictor card.** None of H01–H04
  clears the prediction bar on validate-era data. H02b train passed
  but late-era validation failed. Building this would produce a
  steady stream of false alarms with poor true-positive rate.
- **A sleep-as-warning card.** Sleep efficiency was flat across crashes,
  lead-ups, and non-crash days. Telling the user "your sleep is X
  tonight, might be a sign" has no empirical support for them
  personally.
- **A "your stress score is high" alert.** Daily avg stress was
  train-only positive. By the time of the residual crashes, the
  signal is gone. Surfaces noise.

---

## 6. Methodology lessons we've banked

Captured in synthesis.md; restated here so the next round inherits
them.

1. **Pre-register on both median and mean** when the metric clusters
   on integers / minimums (K01 / K02 lesson).
2. **Small dry-run before locking a spec** — three episodes' computed
   values eyeballed catches definitional artifacts that pre-registration
   alone doesn't (H03 confirmation-type whitelist bug, H05 recovery
   target trivially met).
3. **Substring matching needs negation handling** at every layer
   where it matters — symptoms AND polarity. v2 fixed symptoms; the
   v3 follow-up handles polarity.
4. **Output-key naming matters** when a script produces rich
   metadata — use distinct prefixes to avoid clashes (the
   `_present` clash that initially showed 75% instead of 92%).
5. **Look at actual clauses behind every striking statistic** before
   building anything on top.

---

## 7. What's queued

After the 2026-06-07 HA06 + HA06b + HA10 + HA11 + HA07c + HA08c + HA07d phase (including the FIRST PROJECT OVERALL-SUPPORTED test) the queue is:

1. **H03b — per-minute BB overnight recharge** for **sharpening HA10's validate-era SUPPORTED finding**. API backfill running in background (2026-06-07; ~1372 days, 5s rate limit, ~2h ETA). Pre-registration locked at [H03b/hypothesis.md](garmin/hypotheses/H03b-bb-overnight-recharge-permin/hypothesis.md) before any per-minute data inspection. The path C BB endpoint returns per-3-min Body Battery during sleep window for recent dates (the older dates have empty arrays, so H03b validate-era coverage is the primary use case — which is exactly the era HA10 supported in). When complete, runs same pattern as HA10/HA11 with the integral (peak − sleep_onset) as the primary metric.

2. **HA07 / HA08 / HA12 BLOCKED-PENDING-HARDWARE**. The Forerunner 245 does not record HRV. Substitute tests HA07c / HA08c / HA07d landed using sleep stress as HRV proxy. HRV-direct hypotheses cannot run unless the user later upgrades to a Forerunner 255+/Fenix 7+ AND collects ~3+ years of post-upgrade data.

3. **Card prototyping is now unblocked.** Two card concepts are Tier 1 with anchors:
   - **Card (a) stabilisation-arc** — multi-axis recovery-trajectory card. Highest-evidence card in the project; supporting findings are S01 trajectories + **S02 score distribution shift + algorithmic peak/trough dates (2026-06-07)** + K01/K02 era shifts + dip:crash ratio + HA06b/HA07d era directionality reversal. *Note: S02b refuted the daily-resolution score-leads-Garmin reading; trajectory-level lead pattern can be cited but not as a predictive claim.*
   - **Card (b) train-era retrospective per-crash** — SEVEN converging empirical anchors (H02b + H02d + HA06b + HA11 + HA07c + HA08c + HA07d). Empirical case is overwhelming.
   - **Card (b2) validate-era retrospective per-crash** — TWO converging empirical anchors (HA10 + HA07d), both consistent with Wiggers' "freeze" pattern. Ship-ready empirically.

4. **C.3 personal-lag teaching** — derivative one-pager. The 4-day lead-up is now empirically confirmed across SEVEN train-era + TWO validate-era SUPPORTED tests at the same window. Strongest support possible for the teaching content.

5. **C.5 volatility + dip-frequency progress metric** — derivative one-pager (rolling 30-day std + monthly dip count). Operationalises the scale-compression finding.

6. **C.2 cognitive/emotional load mining** — interaction test with the notes/tag layer. The journal-layer angle stays important even with multi-channel autonomic signatures, since the journal carries signal Garmin can't see.

7. **Notes label-quality work** (participant-requested). Also: a focused re-look at train-era notes around U-dip-elevated days for orthostatic / hydration / ORS mentions (per HA11 result.md).

8. **C.4 recovery-completeness over time** — depends on H05b sustained-recovery primitive.

9. **HA09 parasympathetic-swing detection** (work-on-later). HA06b + HA10 + HA11 together confirm the pattern is empirically present in validate at the population level on multiple channels. A swing detection test as a precursor for crash labels is essentially answered by HA10 + HA06b + HA11 inverse. The remaining HA09 question is whether swing events predict *post-overexertion recovery quality* — needs H05b primitive.

10. **HA12 pre-infection HRV rise** (work-on-later; gated on H04b path C for HRV + notes-quality work for cleaner infection labels).

11. **Dip subtyping (dip_v2)** — same lagged-baseline re-evaluation caveat as before.

12. **Card (b2) prototyping** — promoted back to Tier 1 candidate after HA10 SUPPORTED. Needs H04b per-minute trajectory enrichment to sharpen before shipping.

13. **H02e HR-modulated sentinel imputation**, **Dictionary v3**, **H05b sustained-recovery target**. Cheap, deferred.

**Card (a) the stabilisation-arc card** remains the highest-evidence card concept — its supporting findings (S01 trajectories, **S02 score distribution shift + trajectory dates**, K01/K02 era shifts, dip:crash ratio, notes v2 era shifts, HA06b + HA10 + HA11 multi-channel directionality reversal) all use independent data and metrics. **2026-06-07 update**: S02 added the score-side trajectory + distribution shift; S02b refuted the daily-resolution score-leads-Garmin reading (trajectory-level lead stands but not as a predictive claim); S02c characterised the recent perturbation as small at recent-baseline σ (only RHR shows directional drift).

**Card (b) train-era per-crash retrospective** now has **FOUR converging empirical anchors** on the same train-era crashes (H02b spike count 3d + H02d bridge × 5d + HA06b RHR z-score 4d + HA11 U-dip count 4d). Strongest empirical anchoring for any card concept in the project.

**Card (b2) validate-era per-crash retrospective** has its empirical anchor restored by HA10 morning BB peak elevated 4d. Frame in the paradoxical direction (BB *high* before validate-era crashes, not low).

The hardest part — the analytical work that tells us *whether* an
indicator is worth building on — is largely done. What's left is
mostly product / craft decisions about how to surface the findings,
with a few targeted research follow-ups (H04b, H03b, dip subtyping)
supporting specific card concepts.

---

*Stocktake written 2026-06-05 after H## + K## + S## + notes-v2 work
plus the late-positive-dominant verification. Living document — to
be updated as Tier-2 work matures or Tier-3 research lands.*
