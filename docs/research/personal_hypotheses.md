# Personal hypotheses — non-Wiggers-derived

*n-of-1 hypotheses motivated by lived experience and literature, formulated independent of the Wiggers handleiding's specific claims. Tested against the personal Garmin + gevoelscore corpus.*

## Distinction from the Wiggers register

[`wiggers_testable_hypotheses.md`](wiggers_testable_hypotheses.md) collects hypotheses derived from the Wiggers smartwatch-pacing handleiding (07-2025, ME/cvs Vereniging). It tests Wiggers' specific claims with her specific operationalisations.

This file collects hypotheses that arose from other sources:

- The user's **lived experience** of multi-year daily Garmin + gevoelscore tracking
- General **published literature** on sleep autonomic markers, PEM physiology, and chronic illness
- **Mechanistic reasoning** about device + algorithm behaviour

These hypotheses are NOT proxy-tests of Wiggers' claims. They stand or fall on their own merits.

## Framing discipline

Each hypothesis in this register names:

- **Prior sources** (lived experience entries, published literature, mechanistic argument) that motivated the hypothesis BEFORE any look at the corpus
- **Predicted direction** from the prior sources (pre-specified)
- **Operationalisation** (predictor / outcome / test method) on `per_day_master.csv` columns
- **Descriptive observation** (means, CIs, Cohen's d) that confirms / disconfirms the predicted direction
- **Caveats** on magnitude (in-sample numbers will be slightly inflated)
- **Onward work** that would tighten the inference but does not gate credibility
- **Not in scope** to set explicit boundaries

The discipline this register follows:

- **Confirmatory, not exploratory** — each hypothesis has independent prior motivation, so the in-corpus observation is corroboration not origination (per [[feedback-data-peeking-needs-prior-check]]).
- **Descriptive characterisation, not classifier discrimination** — no AUCs, no logistic regression, no joint-model verdicts. Means, CIs, effect sizes only.
- **Forward-collected data is the natural ongoing validation** — no held-out splits required for credibility; onward replication accrues over time.
- **Validated eras only** — pre-covid / infection / long-covid per [[project-lc-era-boundaries]]. No LC-internal stratification.
- **Label discipline** — every count states scheme + unit + source per [[feedback-name-count-definition]].

---

## P1. Sleep-window stress is elevated on crash episodes

**Hypothesis:** Within the long-covid era (date `>=` 2022-04-04), the user's mean `stress_mean_sleep` is higher on nights that belong to crash episodes (crash_v2 day-level label `==` "crash" in `labels_crash_v2.csv`) than on normal-day base rate nights (label `==` "normal").

### Prior sources

1. **Lived experience.** The user has noticed across years of daily wear that Garmin stress stays high during and after PEM episodes — both in terms of overall stress level and in terms of overnight failure to recover. This observation pre-dates any analysis of the master dataset. It is recorded in the project's framing memory ([[project-crash-triggers-user-experience]]) and was a motivation for building the unified dataset in the first place.

2. **Literature.** Rosenbach et al. 2025 (*Stress and Health*, Wiley, [PMC12647429](https://pmc.ncbi.nlm.nih.gov/articles/PMC12647429/)) established Garmin Stress Score correlates with HRV (RMSSD r `≈` −0.6 group-level) and with heart rate (r `≈` +0.74 within-subject). The Firstbeat 2014 white paper (*Stress and Recovery Analysis Method Based on 24-hour HRV*) documents the stress algorithm as multivariate HRV-derived. Broader sleep-medicine literature on autonomic dysfunction in ME/CFS and Long COVID consistently reports elevated sympathetic tone and reduced parasympathetic activity during sleep in PEM-class conditions.

3. **Mechanism.** During sleep, motion artefacts are absent, HR is at baseline, and respiration is regular. The Firstbeat multivariate composite (RMSSD + HFP + LFP + HR + respiration) collapses toward its autonomic-state component. If PEM episodes involve elevated autonomic arousal as the literature describes, sleep-window stress should reflect this.

All three priors point the same direction.

### Predicted direction

**Positive**: `stress_mean_sleep` mean on crash-episode nights > `stress_mean_sleep` mean on normal-day base rate nights. Pre-specified from the prior sources above.

### Operationalisation

| field | value |
|---|---|
| Predictor (label) | `is_crash` from `labels_crash_v2.csv` (boolean day-level); cross-reference to `crash_episode_id` for episode-level aggregation |
| Outcome | `stress_mean_sleep` (FIT-derived sleep-window mean stress, Garmin 0–100 scale) |
| Sample | LC era only (`date >= 2022-04-04`); `sleep_valid_flag == True` |
| Unit (primary) | **Episode** (crash_v2 unique `crash-NNN` `episode_id`, n=29 in LC era) |
| Unit (secondary) | **Day** (n=101 crash-days in LC era; autocorrelation-inflated, supplementary view only) |
| Base rate | Normal-day pool (`label == "normal"` in `labels_crash_v2.csv`, n=1,162 LC-era days) |
| Test method | Mean comparison; bootstrap 95% CI on means + on diff; Cohen's d as effect size |
| Sources | `per_day_master.csv` for `stress_mean_sleep`; `labels_crash_v2.csv` for crash labels |

### Descriptive observation

From [`analyses/garmin_exploration/hrv_proxy_validation/run_71_72.py`](analyses/garmin_exploration/hrv_proxy_validation/run_71_72.py) Check 7.3 (descriptive characterisation):

| unit | crash mean | normal mean | mean diff | CI95 on diff | Cohen's d |
|---|---|---|---|---|---|
| Episode (primary) | 24.18 | 19.52 | +4.66 | [+1.51, +8.22] | +0.90 |
| Day (supplementary) | 25.67 | 19.52 | +6.15 | [+3.78, +8.77] | +1.03 |

CI does not cross zero at either unit. Direction matches the pre-specified prediction. Effect size is large by conventional benchmarks (d > 0.8).

### Interpretation

The prior is supported. Sleep-window stress is elevated on crash episodes in this corpus, in the direction predicted from lived experience + literature + mechanism. The magnitude is substantial.

### Caveats

1. **In-sample magnitude.** The effect-size estimate is in-sample on the corpus that motivated the hypothesis. Magnitude will likely shrink slightly under onward replication. The directional finding is what's load-bearing; the exact d-value is suggestive.

2. **Crash labels are self-reported.** `is_crash` derives from `gevoelscore` self-report via the crash_v2 definition (gevoelscore `≤` 3 for `≥` 2 consecutive days). The hypothesis is about agreement between self-reported PEM episodes and a wearable-derived autonomic-state signal, not about an objective "true" PEM ground truth.

3. **Single-night aggregate.** `stress_mean_sleep` is one number per night. Within-night dynamics, lag profiles, and timing relative to the crash event are not addressed here.

4. **Sleep-fragmentation contamination.** Nights with high `sleep_awake_min` (median 3, q90 = 13 min in LC era) may have movement artefacts inflating sleep-window stress. Sensitivity analysis excluding high-fragmentation nights would tighten the inference.

5. **No causal claim.** This hypothesis is descriptive of co-occurrence. Whether elevated sleep stress *causes*, *follows*, or merely *co-occurs with* crash days is not addressed.

### Onward work (not gating credibility)

- **Forward replication**: as new days accrue, re-compute the comparison. The hypothesis predicts the directional finding will hold; magnitude shrinkage is the natural calibration.
- **Sleep-fragmentation sensitivity**: re-run with `sleep_awake_min` exclusion at q90 threshold (`> 13` min).
- **Sliding-window descriptive view**: characterise how the crash-vs-normal stress gap moves across time within the LC era. NOT a phase-stratified split — just a continuous descriptive view.
- **Dip-granularity check**: same comparison on `is_dip == True` days (79 single-day dip episodes in crash_v2). Tests whether the signature is graded with severity.

### Not in scope

- Whether `stress_mean_sleep` is a "valid HRV proxy" — that question requires inferential discrimination testing against held-out data and is not addressed here.
- Whether `stress_mean_sleep` **leads** the felt crash — that's a lag question, not the same-day question this hypothesis addresses.
- Whether `stress_mean_sleep` adds incremental information beyond other channels for crash prediction — that's a model-comparison question requiring pre-registered classifier design.
- Wiggers' B1-B5 / H4 claims — those test specific lead-lag and composite signatures she described; the hypothesis here is freestanding.

---

## P2. Wearable exertion-axis signals are elevated in the 4-day window before crash episodes

**Hypothesis**: Within Stratum 4 (LC with gevoelscore + crash labels, 2022-09-03 → as-of-date), wearable-derived exertion-axis signals (effective exertion, steps, max-HR, vigorous minutes) are elevated more frequently in the 4-day window `t-4 … t-1` before a crash day than in matched non-crash 4-day windows.

### Prior sources

1. **Lived experience.** The user has noticed across years of daily tracking that "push days" tend to precede felt crashes by several days — the activity that turns into a crash is rarely the same-day event but typically a buildup over the preceding window. This pattern observation pre-dates the locked HA01b verdict and was a motivation for building the exertion-axis machinery.

2. **Literature.** Aitken et al. 2026 (visible biomarkers symptom prediction in LC, in `docs/research/literature/`) supports wearable signals as leading indicators of subjective state in chronic illness. Broader training-load literature on athletic populations (Banister, Foster's session-RPE, acute-chronic workload ratio) frames acute load above a chronic baseline as a precursor to overreaching / non-functional fatigue. These do not predict the specific PEM crash pattern in LC, but they support exertion-as-leading-indicator framing.

3. **Mechanism.** Physical exertion at `t-N` produces an autonomic + metabolic stress trace whose downstream effects bridge to subjective awareness through a multi-day PEM window. The 4-day lag is consistent with the PEM mechanism described in Long-COVID literature, which is itself the prior for crash_v2's definition of crash as a sustained post-exertion state.

### Predicted direction

**Positive**: frequency of `exertion_rank_composite_lagged_lcera >= 0.75` in the 4-day pre-crash window exceeds the frequency in matched non-crash 4-day windows. Pre-specified from the prior sources above. Magnitude not pre-specified.

### Operationalisation

| field | value |
|---|---|
| Predictor | any-shock-in-4-day-window flag (`max(exertion_rank_composite_lagged_lcera[t-4 .. t-1]) >= 0.75`) |
| Outcome | `is_crash` at t0 from `labels_crash_v2.csv` |
| Sample | Stratum 4 only (per [`methodology/lc_era_temporal_segmentation.md`](methodology/lc_era_temporal_segmentation.md)) |
| Unit (primary) | **Crash episode** (n=29 in Stratum 4) |
| Base rate | Matched non-crash 4-day windows (n=200 per HA01b protocol) |
| Test method | Frequency comparison; Wilson 95% CI per cell; Wald 95% CI on discrimination (point-estimate difference) |
| Sources | `per_day_master.csv` for `exertion_rank_composite_lagged_lcera` + per-axis ranks; `labels_crash_v2.csv` for crash labels |

### Descriptive observation

From [REJECTED.md](REJECTED.md) row `HA01b-recomputed` (2026-06-06) and row `HA01c` (2026-06-07):

**HA01b-recomputed (composite, all-axis) at 4-day window, on the v3.2 lagged baseline (CONVENTIONS §3.2 default for PEM-pacing):**

| era | discrimination | locked verdict |
|---|---|---|
| Train (n=14 crashes) | +5.8 pp | REFUTED |
| Validate (n=15 crashes) | +4.0 pp | REFUTED |

Direction: positive (consistent with the prior). Magnitude: weak; both below the +15 pp pre-reg bar. **The pre-registered HA01b verdict on the correct lagged baseline is REFUTED both eras** — the original "validate +17.3 pp SUPPORTED" reading was on the v3.1 rolling baseline (an artifact-baseline framing per REJECTED.md).

**HA01c (effective-exertion shock, single-axis, τ = 0.75) on the lagged baseline:**

| era | discrimination | locked verdict |
|---|---|---|
| Train (n=11 crashes) | +21.3 pp | SUPPORTED |
| Validate (n=15 crashes) | +19.5 pp | SUPPORTED |

But: HA01c's load-bearing status is **withheld** because the v2 threshold-monotonicity diagnostic returned AMBIGUOUS (bumpy-but-never-negative across the τ ladder). Per REJECTED.md row HA01c, HA01c stays SUPPORTED at the pre-reg bar but cannot be cited as a load-bearing project finding.

### Interpretation

The prior is **weakly supported descriptively** by HA01b-recomputed (direction positive, magnitude well below the pre-reg bar both eras) and **more strongly but diagnostically ambiguously supported** by HA01c (SUPPORTED both eras at the bar but the threshold-monotonicity diagnostic prevents load-bearing claim). The composite multi-axis framing on the lagged baseline does not survive the pre-reg bar; the single-axis effective-exertion framing at τ = 0.75 does (with the diagnostic caveat). The hypothesis stands on the independent prior (lived experience + Aitken 2026 + mechanism); the in-corpus descriptive corroboration is real but weaker than the original artifact-baseline reading suggested.

### Caveats

1. **Train / validate divergence on the correct frame is small.** HA01b-recomputed gives train +5.8 pp / validate +4.0 pp — a ~1.8 pp difference, well below the +15 pp pre-reg bar. The original P2 cited the artifact-baseline numbers (+8.6 / +17.3 pp on the v3.1 rolling baseline) which over-stated both magnitudes AND the divergence. Under the corrected reading there is essentially no divergence to interpret. The "number not narrative" framing from [`methodology/train_validate_split_fate.md`](methodology/train_validate_split_fate.md) §5 still applies in principle, but there is no material divergence to apply it to.

2. **Legacy-split framework**. HA01b-recomputed was still computed under the historical 2023-12-31 train/validate split. Per [`methodology/train_validate_split_fate.md`](methodology/train_validate_split_fate.md), new pre-regs use single-pool primary on Stratum 4. Single-pool re-computation of the underlying composite signal is queued (Q10 in [`methodology/queued_work.md`](methodology/queued_work.md)); under that re-computation the verdict may shift again.

3. **Crash labels are self-reported.** `is_crash` derives from `gevoelscore` self-report via the crash_v2 definition. The hypothesis is about agreement between self-reported crash days and a wearable-derived activity signal, not about an objective "true" PEM ground truth.

4. **Exertion is a daytime activity signal, not an autonomic recovery signal.** P2 is about activity load preceding subjective crash; the autonomic-channel lag question (does BB / stress / RHR ALSO lead at a similar window?) is queued separately as Q15.

5. **Axes are not independent.** `A_effective` is partly composite of steps + vigorous; per-axis ρ across A/B/D is high by construction. The original per-axis decomposition in the artifact-baseline reading appeared to show four independent axes contributing; on the lagged baseline the per-axis decomposition has not been re-run (the lagged-baseline HA01b-recomputed result is composite-only). Per-axis lagged-baseline numbers are needed before any axis-level claim.

6. **5-day post-hoc peak was on the artifact baseline only**. The lag_profile_report.md +23.0 pp validate at 5-day window was on the v3.1 rolling baseline. The 5-day window has not been re-run on the v3.2 lagged baseline; the post-hoc peak finding does not transfer.

### Onward work (not gating credibility)

- **Single-pool re-computation under the new framework** (Q10 in [`methodology/queued_work.md`](methodology/queued_work.md)). Critical for P2 — replaces both the HA01b-recomputed train/validate framing AND the HA01c diagnostic-ambiguous verdict with a single full-Stratum-4 reading on the lagged baseline.
- **HA01c diagnostic resolution**: HA01c was SUPPORTED both eras with diagnostic AMBIGUOUS, load-bearing withheld. If the diagnostic clears under re-analysis (or under single-pool re-computation per Q10), HA01c becomes a load-bearing positive for the broader exertion → crash family — meaningfully strengthening P2's effective-exertion arm.
- **Per-axis re-run on the lagged baseline**: the artifact-baseline per-axis decomposition (A_effective +17.4, B_steps +15.3, C_max_hr +12.9, D_vigorous +17.4) does not transfer to the lagged baseline; re-run on the corrected frame is needed before any axis-level claim. Descriptive characterisation; could batch with Q10.
- **Forward replication**: as new crashes accrue, re-compute the discrimination on the lagged baseline. The hypothesis predicts the positive direction holds; magnitude shrinkage is the natural calibration.
- **Autonomic-channel lag profiling** (Q15 in [`methodology/queued_work.md`](methodology/queued_work.md)). Tests whether autonomic primitives (BB, stress, RHR) ALSO lead at a similar 4-day window, which would broaden P2 from "activity load leads" to "wearable signals broadly lead".
- **Block sensitivity overlay** (M3 per [`methodology/lc_era_temporal_segmentation.md`](methodology/lc_era_temporal_segmentation.md)). Calendar-time-block discrimination point estimates per ~12-month block within Stratum 4. Descriptive only; no per-block confirmatory claim.

### Correction (2026-06-14)

The original P2 entry (written 2026-06-13) cited HA01b's validate-era +17.3 pp SUPPORTED finding + per-axis decomposition from [`lag_profile_report.md`](analyses/garmin_exploration/activity-labels/output/lag_profile_report.md) as strong descriptive corroboration. **That citation was wrong**: those numbers are from the v3.1 rolling-baseline framing. Per CONVENTIONS §3.2, the v3.2 lagged baseline (`*_lagged_lcera` variants) is the correct frame for PEM-pacing tests. Under the correct lagged-baseline frame, HA01b-recomputed is REFUTED both eras at +5.8 / +4.0 pp (per [REJECTED.md](REJECTED.md) row `HA01b-recomputed`, 2026-06-06).

The hypothesis itself stands: independent prior motivation (lived experience + Aitken 2026 + mechanism) does not depend on the descriptive support number. What changed is the strength of the in-corpus descriptive corroboration:

- **Before**: "strong, validate +17.3 pp SUPPORTED, per-axis decomposition all positive"
- **After**: "weak on HA01b-recomputed (+5.8 / +4.0 pp REFUTED at the pre-reg bar); stronger but diagnostically ambiguous on HA01c (+21.3 / +19.5 pp SUPPORTED but load-bearing withheld)"

Per [[feedback_data_peeking_needs_prior_check]]: the prior is independent of any in-corpus observation, so the hypothesis remains confirmatory-framed even with weaker descriptive corroboration. Per [[feedback_caveats_vs_apriori]]: this correction note is the caveat (honest about what was previously claimed and what is now known on the correct frame); the wrong claim is cut. Per the project-scope REJECTED.md audit-trail principle: the correction is part of the visible record, not silently absorbed.

### Not in scope

- **HRV-specific lead-lag** — that is Wiggers H1 (Tier 3 in [`wiggers_testable_hypotheses.md`](wiggers_testable_hypotheses.md)), blocked on FR245 sensor capability.
- **Predictive classifier framing** — whether the 4-day window flag can be used to forecast crashes in a held-out prediction sense is a model-comparison question; that belongs in a pre-reg, not here.
- **Causal claim that exertion → crash** — the lead-lag is correlational. Whether exertion *triggers* PEM or whether both share a common upstream driver is not addressed.
- **Train-vs-validate divergence interpretation** — per Caveats §1, the design cannot adjudicate among plausible drivers of the divergence; P2 does not claim one.
- **Wiggers' B-block claims** — those test specific HRV-derived signatures; the hypothesis here is freestanding and uses activity signals, not autonomic signals.

---

## P3. Within-day RHR recovery — ROUTED to Wiggers register

Considered 2026-06-14 as a Personal-register hypothesis derived from the [lived-experience braindump §"Resting heart rate after overdoing it"](lived_experience_garmin_pacing_2026-06-14.md#resting-heart-rate-after-overdoing-it). **Routed instead to** [Wiggers A4](wiggers_testable_hypotheses.md#a4--sustained-multi-hour-rhr-elevation-marks-real-overexertion).

**Reason for routing.** The participant does not actively monitor within-day RHR on the Forerunner 245 (per [garmin_pacing_practice §4.1](methodology/garmin_pacing_practice.md#41-within-day-rhr)). The lived-experience component is *retrospective felt-recognition* of the pattern Wiggers describes, not an active-monitoring prior. That's a Wiggers-test shape (literature prior + on-corpus test), not a Personal-register shape (lived-experience-protocol prior).

**Refinement suggestion to A4**: extend the locked +20 bpm threshold (Flack-via-Wiggers) to **tiered above-baseline severity bands** {+5, +10, +15, +20 bpm} × duration {30, 60, 120, 240 min}, matching the participant's quoted Wiggers ladder (PDF 165-177: "5-10 bpm above = unhappy; 100 vs 60 bpm for hours = thoroughly overdone"). A4 currently has a "sensitivity ladder recommended" note; this would operationalise it. Reviewer-mode change — surfaced for user decision, not silently edited.

---

## P4a. End-of-day BB minimum below personal floor predicts next-day crash

**Hypothesis:** Within the LC era (`date >= 2022-04-04`), days on which BB minimum during waking hours crossed below the participant's personal warning floors (specifically `<` 20 or `<` 15 at any point before sleep) are followed by elevated crash risk on `t+1` to `t+3`.

### Prior sources

1. **Lived experience + operational protocol.** The participant maintains a three-tier BB floor (25 soft / 20 warning / 15 hard) with active protective action when the floor is crossed (per [lived-experience braindump §"How I used the Garmin for pacing"](lived_experience_garmin_pacing_2026-06-14.md#how-i-used-the-garmin-for-pacing) + [garmin_pacing_practice §3.2](methodology/garmin_pacing_practice.md#32-daytime-body-battery--level--drain-rate)). The protocol *acts on* this signal, predating any analysis on the corpus.

2. **Mechanism.** Body Battery is Garmin's integrated autonomic-state proxy; depletion below personal floors indicates insufficient daytime parasympathetic recovery, which the Long COVID PEM literature ties to next-day symptom exacerbation.

3. **Literature partial.** Wiggers identifies 70-80% as a population-level pacing target (PDF 1380-1397); the participant's 25/20/15 represents lived-envelope-calibrated working floors (divergence documented in [garmin_pacing_practice §7.3](methodology/garmin_pacing_practice.md#73-wiggers-bb-floor-target-70-80-does-not-apply)). Wiggers supports the floor mechanism, not the specific numbers.

### Predicted direction

**Positive**: probability of `is_crash == True` at `t+1` is higher on days where `min(bb_per_minute[waking])` `<` 20 (warning) than on days where it stays above 20. Effect stronger at `<` 15 (hard floor) than at `<` 20. Magnitude not pre-specified.

### Operationalisation

| field | value |
|---|---|
| Predictor | `min(bb_per_minute[waking])` `<` {20, 15} on day T; two-arm pre-reg |
| Outcome | `is_crash` at t+1 (primary); t+1 to t+3 (secondary) |
| Sample | LC era (`date >= 2022-04-04`) |
| Unit (primary) | Day-level next-day crash conditional |
| Base rate | Days where BB minimum stayed above 20 / above 15 |
| Test method | Frequency comparison; Wilson 95% CI; Cohen's d |
| Sources | per-minute BB blocked on [H04b path C](QUEUED-WORK.md#h04b-path-c-authorisation--highest-leverage-next-step); `bb_lowest` daily-min fallback conflates waking + overnight, not usable |

### Status

**Registered 2026-06-14. Descriptive observation deferred** until per-minute BB lands via H04b path C. The daily `bb_lowest` column exists but does not separate waking-hour minimums from overnight troughs, so a fallback analysis would conflate the predictor. This entry preserves the a-priori commitment for the audit trail.

### Caveats (anticipated)

1. **Per-minute BB unavailable** until H04b path C.
2. **Floor calibration recently stabilised** — per [garmin_pacing_practice §2 temporal qualifier](methodology/garmin_pacing_practice.md#temporal-qualifier--this-protocol-is-a-recent-stabilisation-not-a-constant), the 25/20/15 tier is most consistent in the most recent months. Earlier LC-era days reflect partial/less-stable floor-management; the predictor is *cleaner* in recent periods.
3. **Protocol disturbs the test.** If the participant successfully acts on a floor-cross (active rest + early bed), the downstream crash may be prevented. The test then conflates floor-crossed-but-acted-on vs floor-crossed-but-pushed-through. Sensitivity stratification by protocol-stable period needed.
4. **Self-reported crash labels** via crash_v2.
5. **Intervention-baseline dose-response — quantified by [`citalopram_dose_response §5.6`](methodology/citalopram_dose_response_stress_mean_sleep.md#56-v3-amendment--multi-channel-confirmation-added-2026-06-14) (v3 2026-06-14).** *Substantive revision of the earlier "narrowed" reading.* The corpus-wide descriptive sweep (Session C parent MD §8) initially flagged only `stress_mean_sleep` × 2026-03-20; the v3 multi-channel follow-up **upgraded `bb_lowest` to a CONFIRMED dose-modulated channel** (buildup post-CPAP β = −1.13 BB-points per mg plasma, HAC 95% CI [−1.78, −0.49], p = 0.0003; afbouw direction-consistent). **For P4a specifically — this is now a substantive caveat, not a narrow one**: `bb_lowest` is dose-modulated at ~1.13 BB-points per mg, so the BB-nadir distribution shifts substantially across the Citalopram dose history (lowest at 30mg-plateau 2024-06 → 2026-03; rising as the afbouw progresses; will continue rising if the participant stops). The 25/20/15 floor was lived-calibrated during the 30mg plateau (per [garmin_pacing_practice §7.4](methodology/garmin_pacing_practice.md#74-intervention-period-baseline-calibration--resolved-2026-06-14-across-the-autonomic-load-family)) and corresponds to a different *floor-crossing rate* at lower plasma levels. **Required sensitivity arm**: stratify P4a tests by Citalopram-traject phase (pre-2024-04 unmedicated, 2024-04 → 2024-06 buildup, 2024-06 → 2026-03 consolidation 30mg-plateau, 2026-03 → present afbouw) OR apply a per-mg-plasma offset to the BB-nadir predictor before computing floor-crossing. Within-phase P4a tests remain interpretable; cross-phase aggregation is not.

### Onward work (not gating credibility)

- H04b path C primitive when it lands.
- M1 sub-boundary on protocol-stabilised period (per [lc_era_temporal_segmentation §6](methodology/lc_era_temporal_segmentation.md#6-criteria-for-adding-a-sub-boundary-in-a-specific-pre-reg)) to test whether the predictor sharpens in stable-pacing periods.
- Interaction with concurrent cog/emo load (`per_day_intensity` columns).

### Not in scope

- Whether Wiggers' / Workwell BB-floor mechanism is causally correct.
- Per-minute BB as a real-time forecasting tool (model-comparison question).
- The 25 soft-target arm (no protective action triggered at 25 alone).

---

## P4b. Late-afternoon BB drain steeper than morning envelope predicts next-day crash

**Hypothesis:** Within the LC era, days on which the BB drain trajectory observed by ~14:00-16:00 is steeper than the morning envelope suggested are followed by elevated crash risk on `t+1` to `t+3`. Distinct from P4a in metric: P4a is a floor-crossing event (end-state); P4b is a trajectory deviation (mid-day early warning).

### Prior sources

1. **Lived experience + operational protocol.** The participant performs a structural late-afternoon decision check (~14:00-16:00) comparing observed drain rate to the morning envelope; steeper-than-expected drain triggers shrinkage of evening plans (per [lived-experience braindump §"How I used the Garmin for pacing"](lived_experience_garmin_pacing_2026-06-14.md#how-i-used-the-garmin-for-pacing) + [garmin_pacing_practice §5.2](methodology/garmin_pacing_practice.md#52-late-afternoon-decision-check-1400-1600)). The check is part of the protocol's commit-or-shrink moment.

2. **Mechanism.** Drain rate is a velocity metric; level is a position metric. Velocity changes precede position changes — i.e. a trajectory deviation surfaces sooner than a floor-cross. If autonomic strain is building, the drain-rate signal should appear before the floor-cross signal.

3. **Literature partial.** No specific Wiggers analogue; the rate-vs-level distinction is the participant's operational refinement. Broader pacing literature on "training load" velocity (Banister, acute-chronic workload ratio) treats acute load above chronic baseline as a leading indicator — directional parallel.

### Predicted direction

**Positive**: probability of `is_crash == True` at `t+1` is higher on days where the 09:00-16:00 BB drain rate exceeds the participant's rolling-median drain rate by ≥ N_std standard deviations. Threshold N_std = 1.5 primary (matching the project's HA06b autonomic-channel default), 2.0 secondary.

### Operationalisation

| field | value |
|---|---|
| Predictor | `drain_rate_0900_1600` z-scored against personal `[d-90, d-30]` lagged baseline; flag if z ≥ 1.5 (primary) |
| Outcome | `is_crash` at t+1 (primary); t+1 to t+3 (secondary) |
| Sample | LC era (`date >= 2022-04-04`) |
| Unit (primary) | Day-level next-day crash conditional |
| Base rate | Days where z `<` 1.5 |
| Test method | Frequency comparison; Wilson 95% CI; Cohen's d |
| Sources | per-minute BB blocked on H04b path C; no fallback possible (daily aggregates lose trajectory) |

### Status

**Registered 2026-06-14. Descriptive observation deferred** until per-minute BB lands via H04b path C. No daily-aggregate fallback exists — the predictor is fundamentally a trajectory metric. Audit trail preserved.

### Caveats (anticipated)

1. **Per-minute BB unavailable** until H04b path C.
2. **Drain-rate definition ambiguity**. "09:00-16:00 drain rate" is one operational choice among several (e.g. drain-per-hour averaged, peak-to-trough slope, OLS slope). Specific operationalisation locked at pre-reg time.
3. **Drain rate is partly behavioural.** A steep drain may reflect deliberately heavy exertion that day (which would itself predict t+1 crash) rather than a separate autonomic-strain signal. P4b alone cannot disambiguate; sensitivity covariate on `exertion_class_lagged_lcera` would help.
4. **Floor calibration recently stabilised** (same as P4a caveat 2).
5. **Protocol disturbs the test** (same as P4a caveat 3): if the late-afternoon check successfully shrinks evening plans, the downstream crash may be prevented.
6. **Intervention-baseline dose-response — partial verdict on `bb_overnight_gain` per [`citalopram_dose_response §5.6`](methodology/citalopram_dose_response_stress_mean_sleep.md#56-v3-amendment--multi-channel-confirmation-added-2026-06-14) (v3 2026-06-14).** See P4a caveat 5 for the family-wide framing. **For P4b specifically**: the predictor is a rolling-baseline z-score on `bb_overnight_gain` and similar BB-trajectory metrics. The v3 multi-channel test could not run the buildup-symmetric test on `bb_overnight_gain` (0 observations in the 2024-05-01 → 2024-06-19 window per parent §2b channel-coverage gap); the afbouw-2026 spec returned a counter-prior-sign β with wide CI (sign mismatch, low confidence). **`bb_overnight_gain` therefore inherits a partial / data-limited verdict** — not confirmed dose-modulated but also not cleanly null. Spring 2025 control DID show a notable +0.16 BB-points/day calendar-time trend on this channel (CI excludes zero), suggesting bb_overnight_gain has its own non-dose-driven seasonal/recovery dynamics independent of citalopram. **For P4b**: the BB-trajectory predictor probably *is not* dose-confounded (no symmetric buildup signal to confirm a dose-response), but it IS calendar-time-dynamic in ways the rolling baseline may not absorb cleanly. Sensitivity arm: track P4b results across Citalopram-traject phases and report any phase-stratified divergence, but treat divergence as candidate calendar-time-dynamic rather than dose-driven.

### Onward work (not gating credibility)

- H04b path C per-minute BB primitive.
- P4a + P4b joint analysis: do they fire on overlapping days, or do they capture distinct signal modes?
- Activity-class stratification (covariate on `exertion_class_lagged_lcera`).
- M1 sub-boundary on protocol-stabilised period.

### Not in scope

- Mechanistic claim that drain-rate measures something different from level.
- Real-time mid-day forecasting (model-comparison).
- Determining the "optimal" drain-rate window (e.g. 09:00-12:00 vs 09:00-16:00) — pre-reg specifies one window.

---

## P5a. Post-exertion rest-stress with motion filter — ROUTED to Wiggers register

Originally drafted 2026-06-14 as a Personal-register hypothesis (Wiggers C4 + motion-filter hybrid). **Routed** to [Wiggers C4b](wiggers_testable_hypotheses.md#c4b--stress-with-low-motion-minute-count-c4-with-motion-filter) on 2026-06-14 per user-direction for unambiguous placement: Wiggers C4 is the dominant prior; the motion filter is the participant's operational refinement on the same shape, not a distinct theoretical claim.

The participant's lived-experience operational protocol (per [garmin_pacing_practice.md §3.3](methodology/garmin_pacing_practice.md#33-stress-when-at-rest)) still operates on rest-stress as the trigger; that operational fact is cited in the C4b prior-sources, not lost. **P5b remains in this register** because its *prevailing* (not exertion-conditioned) framing with evening amplification genuinely extends beyond Wiggers' C4.

---

## P5b. Prevailing rest-stress (any time of day) with evening amplification predicts next-day crash

**Hypothesis:** Within the LC era, periods of elevated stress with concurrent low motion (the rest-stress pattern) — regardless of preceding exertion — are more frequent on the `t-1 → t` window before crashes than on matched non-crash days. Effect is **amplified in the evening window** (e.g. 18:00-22:00). Distinct from P5a in trigger: P5a is post-exertion-conditioned (Wiggers C4 strict); P5b is prevailing (extends beyond Wiggers).

### Prior sources

1. **Lived experience + operational protocol.** The participant's rest-stress trigger does not require recent heavy exertion; stress-with-low-motion at any time is the signal (per [garmin_pacing_practice §3.3](methodology/garmin_pacing_practice.md#33-stress-when-at-rest)). The evening amplification is a structural protocol feature — same signal triggers a different action (bedtime call) (per [§5.3](methodology/garmin_pacing_practice.md#53-evening-rule)).

2. **Mechanism.** Sympathetic arousal during rest periods unrelated to immediate exertion suggests autonomic dysregulation as a *state*, not just a load response. Time-of-day shape (worse in evening) plausibly reflects circadian autonomic tone interacting with cumulative day-load.

3. **Literature partial.** Wiggers C4 covers post-exertion-only; P5b extends to the prevailing form. No specific literature anchor for the broader form; the extension is the participant's lived contribution.

### Predicted direction

**Positive**: per-day count of "stress ≥ 60 with steps_per_minute ≤ 5" minutes is higher on the day before a crash than on matched non-crash days. **Stronger effect** when restricted to the evening window (18:00-22:00) vs the morning window (06:00-12:00). The time-of-day asymmetry is the differentiating prediction vs P5a + HA11.

### Operationalisation

| field | value |
|---|---|
| Predictor | Per-day count of stress-with-low-motion minutes, stratified by time-of-day bins {morning 06:00-12:00, afternoon 12:00-18:00, evening 18:00-22:00} |
| Outcome | `is_crash` at t+1 (primary); also dip secondary |
| Sample | LC era (`date >= 2022-04-04`), full (NOT exertion-conditioned, unlike P5a) |
| Unit (primary) | Day |
| Base rate | Days NOT followed by crash |
| Test method | Frequency comparison per bin; Wilson 95% CI; Cohen's d; primary test on the **evening-vs-morning differential** |
| Sources | monitoring_b FIT files; needs stress-with-motion-by-bin primitive |

### Status

**Registered 2026-06-14. Descriptive observation deferred** until the stress-with-motion-by-time-of-day primitive lands. Shares the extraction pipeline with P5a; adds the time-of-day binning. Audit trail preserved.

### Caveats (anticipated)

1. **Sample-size by bin.** Splitting per-day stress-rest minutes into three time-bins reduces the per-bin count. Evening bin (4h) is shorter than morning + afternoon (6h each); base-rate adjustment needed.
2. **Time-of-day confounds.** Evening activity patterns differ from morning (sedentary watching TV, family time). The "low motion" condition is more easily satisfied in evening regardless of autonomic state. The discriminative claim is per-day-count, not per-minute base rate; the confound is partly base-controlled.
3. **Goes beyond Wiggers.** The prevailing form is the participant's extension; Wiggers does not specifically claim this. P5b is honest-extension territory, not literature-replication.
4. **Protocol disturbs the test**, especially for evening: if rest-stress in evening triggers early bed (per pacing-practice §5.3), the downstream crash may be prevented.
5. **Differential prediction is fragile.** The evening-vs-morning differential is a second-order claim; absolute-effect interpretation should not depend on it being significant.
6. **Intervention-baseline dose-response — quantified by [`citalopram_dose_response §5.6`](methodology/citalopram_dose_response_stress_mean_sleep.md#56-v3-amendment--multi-channel-confirmation-added-2026-06-14) (v3 2026-06-14).** See P4a caveat 5 for the family-wide framing. **For P5b specifically — substantively strengthened**: the predictor combines stress (`stress_mean_sleep` AND/OR `all_day_stress_avg`) with motion. The v3 multi-channel test CONFIRMED BOTH stress channels as dose-modulated: `stress_mean_sleep` buildup post-CPAP β = +0.43/mg (p = 0.001), `all_day_stress_avg` buildup post-CPAP β = +0.57/mg (p = 0.0003) — the latter is actually the strongest signal in the whole multi-channel sweep. **P5b inherits this caveat jointly on both stress channels**: at 30mg plasma steady-state the stress-with-low-motion concurrence threshold sits ~12-17 stress-points higher than at 0mg steady-state for both channels. **Required (no longer optional) sensitivity arm**: stratify P5b tests by Citalopram-traject phase (pre-2024-04 unmedicated, 2024-04 → 2024-06 buildup, 2024-06 → 2026-03 consolidation 30mg-plateau, 2026-03 → present afbouw), OR apply a per-mg-plasma offset to the absolute stress values before computing the "stress ≥ 60" threshold-crossing count. Within-phase P5b tests remain interpretable; cross-phase aggregation requires the dose-adjustment. The evening-amplification differential prediction is robust to this caveat because both bins share the offset, but the absolute-level interpretation is not.

### Onward work (not gating credibility)

- Stress-with-motion-by-time-of-day primitive extraction.
- M1 sub-boundary on protocol-stabilised period — P5b is *especially* sensitive to this because the evening rule's stability is itself a recent development.
- Joint with P5a: does P5b add discriminative information beyond P5a's post-exertion-conditioned form?
- Joint with HA11: does motion filter + time stratification sharpen HA11's U-dip count?

### Not in scope

- Mechanistic claim about circadian autonomic tone.
- Real-time intervention.
- Determining "optimal" evening window boundaries — pre-reg locks one (18:00-22:00).

---

## P6. Post-crash window — distinctive autonomic-recovery shape

> **→ Superseded by [HA-P6 pre-reg](analyses/hypotheses/HA-P6/hypothesis.md) v2 locked 2026-06-17 under option-A compression** (v1 archived at [`hypothesis-v1-archived.md`](analyses/hypotheses/HA-P6/hypothesis-v1-archived.md), LOCKED 2026-06-15-r3; v1 dry-run HALTED on 2026-06-17 at the §7 E[L]\* sanity gate per [`dry-run-report-v1-archived.md`](analyses/hypotheses/HA-P6/dry-run-report-v1-archived.md); v1 implementation archived at [`script-v1-archived.py`](analyses/hypotheses/HA-P6/script-v1-archived.py); v2 closes three named spec-precision issues per §4.8.1 + §7 + §4.8.4: interpretation of the E[L]\* input pool (pooled-LC daily time series under v2; matches HA-P7), three-verdict §7 sanity policy with per-channel E[L] override for FAIL channels, and per-episode `completeness_per_episode` threading from §4.8.1 to §4.8.4 with ε = 0.5×σ_ch denominator-undefined rule). The pre-reg substantively narrows the channel set to 7 (stress_mean_sleep, all_day_stress_avg, bb_lowest, bb_overnight_gain, resting_hr, gevoelscore, stress_low_motion_min_count_S60_Mlow) and locks Option C dual matched-baseline (matched-deep-trough Arm A + lagged personal baseline Arm B); reframed as Layer 1 descriptive characterisation per [CONVENTIONS §2.1](CONVENTIONS.md#21-descriptive-before-inference) with no SUPPORTED bar (§5 is "findings shape", not a falsification criterion; §9 enumerates downstream propagations per observation shape, not verdict branching). Register text below is the historical genesis; for canonical operationalisation, the algorithmic shape classifier, the per-channel E[L] policy, and the §9 propagation triggers see the pre-reg. Per [`methodology/hypothesis_lock_process.md`](methodology/hypothesis_lock_process.md) §3.8 v1.1 register-row pointer discipline + §3.9 step 4 v(N-1)-archived discipline.

**Hypothesis (primary, descriptive):** Within the LC era, days `t+1` through `t+5` after a crash episode-end show channel-specific recovery trajectories (on RHR, BB overnight gain, stress, sleep efficiency) that differ in shape from matched non-crash days.

**Hypothesis (secondary, predictive):** Recovery shape characteristics (recovery rate, recovery completeness) co-vary with same-episode crash duration and with next-crash interval.

### Prior sources

1. **Lived experience.** [Lived-experience braindump](lived_experience_garmin_pacing_2026-06-14.md): "and just after a crash?" is explicitly raised as an underexplored timescale; the multi-scale dynamics framing ("strings of crashes, response to a previous longer period of ineffective pacing") motivates examining what happens *after* a crash, not just before.

2. **Mechanism.** PEM-recovery is a multi-day autonomic re-equilibration process; recovery completeness plausibly mediates next-crash risk. If a crash is followed by partial-only recovery, the post-crash window itself becomes an elevated-risk window.

3. **Literature.** [Wiggers H5 — lag order](wiggers_testable_hypotheses.md#h5--each-metric-has-a-characteristic-lag-vs-exertion-lags-differ-by-metric) (PDF 925-928): HRV *"drops after several days of overexertion ... even if the person rested well immediately after."* Implies a multi-day post-event autonomic tail. Aitken et al. 2026 supports wearable signals as lagging indicators of subjective state.

### Predicted direction

**Primary (descriptive)**: per-channel post-crash trajectory differs from matched non-crash trajectory on at least one of {depth, duration, completeness}.

**Secondary (predictive)**: slower / less-complete recovery on `t+1` to `t+5` co-varies with longer same-episode crash duration; slower recovery predicts shorter next-crash interval.

### Operationalisation

| field | value |
|---|---|
| Predictor (primary) | Per-day channel value on `t+1` through `t+5`, where `t0` = crash_v2 episode-end |
| Outcome (primary) | Trajectory shape comparison vs matched non-crash days |
| Predictor (secondary) | Recovery rate (slope on `t+1..+5`), recovery completeness (% return to lagged baseline by `t+5`) |
| Outcome (secondary) | Same-episode crash duration (days, from crash_v2); next-crash interval (days to next `crash-NNN` episode start) |
| Sample | LC era (`date >= 2022-04-04`) |
| Unit (primary) | Crash episode (n=29 in LC era per crash_v2) |
| Test method | Peri-event alignment + median trajectory per channel; bootstrap CI; sensitivity to t0 definition (episode-start vs episode-end) |
| Scale | Situational multi-day window, 5d (`t+1..t+5`). Mechanistically anchored to multi-day autonomic re-equilibration tail per [`methodology/time_resolution.md` §2.3, §6](methodology/time_resolution.md). Neighbouring-scale check: per-day reads of any single `t+k` would lose the trajectory shape (finer-scale aggregation risk); the lagged baseline used for "% return to lagged baseline by `t+5`" is the reference-frame construction per [`time_resolution.md` §2.4](methodology/time_resolution.md). |
| Sources | `per_day_master.csv` + `labels_crash_v2.csv` — both exist; **no upstream blocker** |

### Status

**Registered 2026-06-14. Observation pending bandwidth.** No upstream primitive blockers; observable on existing data. Cheapest of the P-hypotheses to actually observe alongside P7.

### Caveats (anticipated)

1. **Regression to the mean.** Crash days have low gevoelscore by definition; subsequent days regress toward the participant's mean by construction. The "recovery shape" partly reflects RTM, not autonomic-specific recovery. Needs a baseline-shape comparison from matched non-crash deep-trough days as a control.

2. **n=29 LC-era episodes.** Per-channel per-day post-crash distributions are sparse; CIs will be wide. Descriptive characterisation is informative; predictive sub-claims need careful framing.

3. **Crash_v2 episode boundaries.** `t0` = episode-end depends on the crash_v2 episode-end definition (gevoelscore above threshold for `N` consecutive days). Sensitivity to definition; report primary + alternative t0 anchoring.

4. **Self-reported crash labels** via crash_v2.

5. **Intervention-baseline dose-response — quantified by [`citalopram_dose_response §5.6`](methodology/citalopram_dose_response_stress_mean_sleep.md#56-v3-amendment--multi-channel-confirmation-added-2026-06-14) (v3 2026-06-14).** See P4a caveat 5 for the family-wide framing. **For P6 specifically — substantively broadened from the pre-v3 reading**: P6's post-crash recovery shape is per-channel. The v3 multi-channel test confirmed **three channels** as dose-modulated: `stress_mean_sleep`, `all_day_stress_avg`, and `bb_lowest` (the latter is in P6's RHR/BB/stress/sleep panel). Pre-v3 the caveat applied only to `stress_mean_sleep` near the 2026-03-20 boundary; **post-v3 the caveat applies to all three channels across the entire Citalopram-traject (2024-04 → ongoing)**, with the strongest effect during the afbouw transition. **For P6**: a crash whose `t0` falls within the buildup, plateau, or afbouw of citalopram inherits a recovery-shape calibration concern on each of the three confirmed channels. `respiration_avg_sleep` is REJECTED dose-modulated (the v3 finding is informative-by-rejection) and can be used in P6 panels without inheriting the caveat; `resting_hr` is weakly dose-modulated and inherits a soft caveat. **Required sensitivity arm**: stratify P6 panels by Citalopram-traject phase (pre-2024-04, buildup, consolidation, afbouw); within each phase the rolling-baseline z-scores are interpretable; cross-phase recovery-shape pooling requires per-channel per-mg-plasma adjustment OR phase-by-phase reporting. CONVENTIONS §3.7 trajectory-detrend pattern continues to apply per default.

### Onward work (not gating credibility)

- Joint with P7: if the post-crash window is itself elevated-risk (P7's recent-crash-density positive), what is the recovery-shape signature of high-recurrence-risk crashes vs low-recurrence-risk crashes?
- Stratification by crash subtype once crash_v3 (mechanism subtyping) lands.
- Channel-specific recovery-lag estimates (per Wiggers H5 — does each channel have its own characteristic recovery tail?).

### Not in scope

- Pre-crash window (`t-N` to `t-1`) — covered by P2 / HA01b family / HA11 / P4 / P5.
- Mechanistic claim about recovery physiology.
- Real-time intervention.

---

## P7. Recent-crash-density predicts elevated crash risk

> **→ Superseded by [HA-P7 pre-reg](analyses/hypotheses/HA-P7/hypothesis.md) r3 locked 2026-06-15 at commit `7f1ecc8`.** The pre-reg revised the eligibility rule from "d not in episode" to "d-1 not in episode" (the register version excluded the outcome `is_crash at d` by construction; see [HA-P7 §4.2](analyses/hypotheses/HA-P7/hypothesis.md)). Register text below is the historical genesis; for canonical operationalisation, falsification bar, and the 4-layer-clean audit lineage see the pre-reg. Per [`methodology/hypothesis_lock_process.md`](methodology/hypothesis_lock_process.md) §3.8 v1.1 register-row pointer discipline.

**Hypothesis:** Within the LC era, on a day `d` not currently in a crash episode, the count of crash-days in the preceding 14 days predicts elevated probability of crash at `d` (or in the days immediately following `d`).

### Prior sources

1. **Lived experience.** [Lived-experience braindump](lived_experience_garmin_pacing_2026-06-14.md): *"some intuitive ideas are that crash risk is increased in a period with multiple crashes. Things we have to test empirically."* Explicit prior; user-stated as needing empirical test.

2. **Mechanism.** PEM-recovery is multi-day; if recovery from a recent crash is incomplete, the participant enters subsequent days with reduced envelope and elevated vulnerability. "Recovery debt" framing.

3. **Literature partial.** Wiggers does not specifically claim recent-crash-density elevates next-crash risk. Broader chronic-illness pacing literature on cumulative load / recovery debt supports the directional intuition without operationalising it.

### Predicted direction

**Positive**: P(`is_crash` at `d`) is monotonically increasing in count of crash-days in `[d-14, d-1]`. Window length is operationally locked at **14 days primary** (mechanistically anchored to typical PEM-recovery tail), with 7d and 30d as sensitivity arms. Windows beyond 30d are out of scope (would conflate recovery-debt mechanism with phase-of-life signals).

### Operationalisation

| field | value |
|---|---|
| Predictor (primary) | `count(is_crash) over [d-14, d-1]` |
| Predictor (sensitivity) | Same metric with windows {7d, 30d} |
| Outcome | `is_crash` at `d` (primary); `any(is_crash) over [d, d+3]` (secondary) |
| Sample | LC era (`date >= 2022-04-04`) days where `d` itself is NOT in a crash episode (exclude within-episode autocorrelation). *[Revised in [HA-P7 §4.2](analyses/hypotheses/HA-P7/hypothesis.md) to "d-1 not in episode" — see top-of-section supersession pointer.]* |
| Unit (primary) | Day |
| Test method | Logistic regression with crash_count_14d as continuous predictor; report odds ratio + Wilson CI on cell frequencies for crash_count_14d ∈ {0, 1, 2, 3+} bins |
| Scale | Situational multi-day window, 14d primary + 7d/30d sensitivity arms. Mechanistically anchored to PEM-recovery tail (recovery-debt mechanism) per [`methodology/time_resolution.md` §2.3, §6](methodology/time_resolution.md). Neighbouring-scale check: `is_crash` itself has a 2-day aggregation window baked in (§5 of `time_resolution.md`); the 14d count over `is_crash` is a multi-day window applied to a label that already aggregates 2-day stretches — the test does not own the 2-day baked-in aggregation as a mechanism. |
| Sources | `labels_crash_v2.csv` only — **no upstream blocker** |

### Status

**Registered 2026-06-14. Observation pending bandwidth.** No upstream primitive blockers; observable on labels alone. **Cheapest of all P-hypotheses to actually observe.**

### Caveats (anticipated)

1. **Causal confound is the central concern.** A period with multiple recent crashes also reflects underlying causes (heavy life events, infection, intervention transitions) that may *both* cause the recent crashes AND independently elevate current-day risk. P7's positive result is consistent with "recovery-debt mechanism" AND with "shared underlying cause"; the design cannot adjudicate. Sensitivity covariate on documented life-events / interventions would partly mitigate but does not resolve.

2. **Selection bias on conditioning.** Excluding within-episode days from the sample concentrates the analysis on inter-crash gap days — these have systematically different distributional properties than pure baseline days. The comparison is "gap days with recent crashes" vs "gap days without recent crashes", not "any day" vs "any day with recent crashes".

3. **Self-reported crash labels** via crash_v2.

4. **Intervention-baseline dose-response — `gevoelscore` axis unchanged from Session C, per [`citalopram_dose_response §5.6`](methodology/citalopram_dose_response_stress_mean_sleep.md#56-v3-amendment--multi-channel-confirmation-added-2026-06-14) (v3 2026-06-14).** See P4a caveat 5 for the family-wide framing. **For P7 specifically**: the predictor is crash-label-density and the outcome is a crash-label flag, both derived from `gevoelscore`. Intervention-baseline dose-response operates on the Garmin baseline-channel frame, not directly on `gevoelscore`. The v3 multi-channel test did not extend to `gevoelscore` (which is the outcome-channel side per parent §3b and is out of scope for the dose-response MD). Session C's finding for `gevoelscore` (small detrend-surviving step UP around 2026-03-20) stands unchanged; the v3 work does not refine or contradict it. **Operational implication for P7 (unchanged)**: report the 14d-window crash density separately for "all LC era" vs "afbouw era (2026-03-20 onward)" as a sensitivity arm. **New consideration from v3**: if a future P7 variant uses any of the three CONFIRMED Garmin baseline channels as a *secondary* density predictor (e.g. "crash plus high-stress days"), inherit the P4a-shape per-phase stratification caveat for that channel.

5. **14d window choice is operational.** Mechanistically anchored but not derived from data. Sensitivity arms (7d, 30d) report magnitude; the directional claim is window-invariant if all three arms agree.

### Onward work (not gating credibility)

- Sensitivity ladder on window {7d, 14d, 30d}.
- Interaction with documented intervention periods (sub-stratification — descriptive overlay, *not* sub-boundary).
- Joint with P6: does recovery-shape (P6) interact with recent-crash-density (P7)? — i.e. does the recovery-debt mechanism manifest both as slower recovery (P6) and as elevated next-crash risk (P7)?
- Once crash_v3 mechanism-subtyping lands, stratify by subtype.

### Not in scope

- Causal claim that recent crashes elevate next-crash risk via a specific mechanism.
- Window > 30 days (would conflate recovery-debt with phase-of-life).
- Predictive classifier framing.

---

*Add new hypotheses with a `P<n>` header following the same shape: **Prior sources**, **Predicted direction**, **Operationalisation**, **Descriptive observation**, **Interpretation**, **Caveats**, **Onward work**, **Not in scope**. Hypotheses without independent prior motivation (lived experience / literature / mechanism) belong in an exploratory register, not here.*
