# Wiggers hypotheses — progress map as of 2026-06-08

*Successor to [wiggers_progress_2026-06-07.md](wiggers_progress_2026-06-07.md). Two material changes
since that snapshot:*
1. *H03b (per-minute BB overnight recharge) ran 2026-06-07 (late) and returned
   **INCONCLUSIVE × 12** on data availability — the Garmin API only populates
   `sleepBodyBattery` from ~2024-06-03 onwards, so train era has zero coverage
   and validate has only 6 of 15 usable crashes.*
2. *2026-06-08 Tier 2 statistics audit — Fisher's exact + 95% CIs on 11 primary
   verdicts + cross-channel Spearman/Pearson correlation matrix on the seven
   load-bearing primitives. **Two structural collinearities surfaced**:
   H02b ≡ H02d (ρ = +1.000) and HA10 ≡ −HA07c (ρ = −0.922). The
   "seven SUPPORTED on six channels" project framing collapses to roughly
   **3–4 effectively independent signal clusters**. Only the within-day
   stress-spike cluster (H02b/H02d train) survives an honest effective-N
   Bonferroni at α = 0.0125.*

*A snapshot of which Wiggers testable hypotheses
([wiggers_testable_hypotheses.md](wiggers_testable_hypotheses.md)) have
been addressed by the Garmin × crash investigation so far, how, what
the outcome was, and what remains queued or untouched.*

*Source register: ~40 testable hypotheses across nine sections (A–I).
This map cross-references each to the relevant H## / HA## / S## test
in [docs/research/garmin/hypotheses/](garmin/hypotheses/).*

---

## How to read this map

Each row carries one of six statuses:

- **TESTED — direct.** A hypothesis was operationalised and tested as
  the Wiggers hypothesis describes (same physiological construct,
  same measurement intent).
- **TESTED — proxy.** A different measurement was used to address the
  same physiological question (typically because the original signal
  is unavailable on the FR245 hardware).
- **PARTIAL.** Some aspect of the hypothesis was addressed but not the
  full claim.
- **QUEUED.** Pre-registered but not yet run, or queued in
  `QUEUED-WORK.md`.
- **NOT ADDRESSED.** No test has been run; no pre-registration locked.
- **BLOCKED.** Cannot be tested with available data/hardware on the
  current participant device.
- **INCONCLUSIVE-BY-DATA.** Pre-registered, run, but the locked
  inconclusive-cutoff binds because of data-availability gaps.

Where a Wiggers hypothesis is flagged ⚠️ in the source (high-value /
counter-intuitive / contradicts a prior finding), that flag is
preserved.

---

## Priority shortlist (Wiggers' top six) — current status

Wiggers explicitly named six tests as the ones that would decide
product direction. Their status here is the most important reading
of this whole map:

| Wiggers ID | Question | Status as of 2026-06-08 |
|---|---|---|
| **H1 ⚠️** | Do wearable signals lead the felt crash? | **PARTIAL → daily-resolution lead/lag REFUTED in the empirically-observed direction (S02b, 2026-06-07); Wiggers-direction not directly tested.** Every precursor test uses a 3–5 day lead-up window and several SUPPORT in some era — implicitly demonstrating wearables can lead self-report. The project's **first direct cross-correlation lag test** ([S02b](garmin/hypotheses/S02b-score-lead/notes.md)) tested the empirically-observed score-leads-Garmin direction at daily resolution. **REFUTED on criterion (c)**: primary lagged ρ at +149d = +0.099 vs matched same-day ρ = −0.097, |delta| = +0.002 against the 0.10 bar. Trajectory-level lead/lag (S02 T1) does not survive to daily resolution. The Wiggers-canonical direction (wearables-lead-score) remains untested directly, but the magnitude of all observed lagged ρ values (none above \|0.10\|) suggests it would also be small. |
| **H2 ⚠️** | How many crashes are "activity-invisible"? | **PARTIAL.** HA01b-recomputed refuted the composite activity-shock as a precursor on a clean baseline → consistent with most validate-era crashes being activity-invisible. The HA01b per-axis decomposition + HA01c SUPPORTED both eras at the locked τ=0.75 threshold (effective_exertion, intensity-minutes-based) — but with posterior-per-fire ~2.2% vs base rate 1.7% (60% null-fire rate), so the channel is not card-shippable and load-bearing status is withheld (HA01c v2 mixed: validate Cat 1 RESCUE, train AMBIGUOUS). Not yet a formal count of crash episodes by physical-signature presence/absence. |
| **H3 ⚠️** | Acute-illness vs PEM crashes separable in Garmin? | **NOT ADDRESSED.** Requires illness-vs-PEM labels (queued as crash_v3 from notes; gated on notes-quality work). |
| **C3 / D1 / D2** | Non-linearity of stress; level-vs-dynamics for BB | **NOT ADDRESSED for C3 + D2; PARTIAL for D1** (H04 refuted BB net delta as a precursor; not a same-day correlation test). **D2 newly BLOCKED-pending-FIT-decode**: H03b INCONCLUSIVE × 12 confirmed the API can only deliver per-3-min BB from ~2024-06-03 onwards, with train era at zero coverage. Path B (FIT decode of `unknown_233`) remains the only route to per-minute BB for the full corpus. |
| **B4 / H4 ⚠️** | Parasympathetic-swing as an inverted indicator | **TESTED — proxy, SUPPORTED — but the "three independent channels" framing is now retracted.** Trajectory: v1 diagnostic CLOSE both eras on HA07d + HA10 → demoted. v2 criteria revision applied symmetrically. **v2 outcomes**: HA07d both eras RESCUE (Cat 2/3). HA10 validate RESCUE via Cat 3. HA06b train PERMANENTLY CLOSED via Cat 4. HA11 train RESCUE via Cat 1. **Restored anchors**: HA07d primary + HA10 corroborating secondary for validate-era. **But the 2026-06-08 cross-channel correlation audit collapses HA10 and HA07c into a single autonomic-state signal (ρ = −0.922, structural in Garmin's BB algorithm), and HA07d is moderately correlated with HA07c (ρ = +0.501).** What looked like three independent operationalisations of parasympathetic-swing is closer to **one autonomic-state cluster (HA10/HA07c ± HA06b) plus a partially-related variability channel (HA07d)**. The qualitative finding "great-looking numbers precede a crash" is present; the quantitative "three independent channels converge" headline must soften. Effective-N Bonferroni: HA07d validate p=0.070, HA10 validate p=0.148 — neither clears α=0.0125 once collinearity is acknowledged. |
| **G3 ⚠️** | Barometric pressure × headache | **NOT ADDRESSED.** Requires external weather data join; not yet attempted. |

**Of Wiggers' six product-decisive tests, two are PARTIAL, one is
TESTED-via-proxy-with-QUANTITATIVE-FRAMING-SOFTENED (B4/H4), two are
NOT ADDRESSED, and one is NOT ADDRESSED pending notes-quality work.**
The 2026-06-08 audit changed the synthesis-level reading of B4/H4
without changing any locked verdicts: the discrimination findings
remain on record; what changed is the count of independent channels
backing them. With H02b ≡ H02d folded, HA10 ≡ −HA07c folded, and
HA07d-HA07c moderately collinear, the project's effective channel
count is closer to **three signal clusters** (within-day stress;
autonomic state; autonomic variability) rather than the previously
claimed seven.

---

## Section-by-section progress

### A. Resting HR & night HR

| Wiggers | Status | Project tests | Outcome |
|---|---|---|---|
| A1: RHR elevated on/before crashes | TESTED — direct | [H01](garmin/hypotheses/H01-rhr-drift/result.md); [HA06](garmin/hypotheses/HA06-morning-rhr-delta/result.md); [HA06b](garmin/hypotheses/HA06b-rhr-zscore/result.md) | **H01 refuted both eras. HA06 refuted both eras. HA06b train SUPPORTED +18.9 pp @ 1.5σ (Fisher p=0.136, fails α=0.05); validate refuted.** Direction matters: only z-score deviation surfaces a signal. HA06b was permanently demoted in v2 (Cat 4, 2 sign-changes). |
| A2: RHR deviates either direction | TESTED — direct | [HA06](garmin/hypotheses/HA06-morning-rhr-delta/result.md) + [HA06b](garmin/hypotheses/HA06b-rhr-zscore/result.md) bidirectional + directionality split | **Confirmed empirically**: train 70% elevated / 30% lowered; validate 25% elevated / 75% lowered. Wiggers' "either direction" prediction is correct; the *dominant* direction reverses across eras. |
| A3: Night RHR elevated from t-2 onwards | TESTED — direct | HA06 / HA06b 4d primary + 5d secondary lead-up windows | Lead-up structure addressed. Train-era SUPPORTED at 4d on z-score (not statistically significant after honest effective-N correction). |
| A4: Sustained multi-hour RHR elevation (not brief spike) | BLOCKED — no intraday HR analysis run | — | Would need intraday HR aggregation; not yet attempted. |

### B. HRV

| Wiggers | Status | Project tests | Outcome |
|---|---|---|---|
| B1: Day-over-day HRV drop ≥ 10 predicts crash | TESTED — proxy | [HA07c](garmin/hypotheses/HA07c-sleep-stress-mean-delta/result.md) — sleep-stress mean delta as HRV-drop proxy | **HA07c train SUPPORTED +23.2 pp @ 1.5σ (Fisher p=0.058, fails α=0.05); validate refuted.** Now known to be the same underlying primitive as HA10 (Spearman ρ = −0.922) — the sleep-stress mean is the negative of morning BB peak by Garmin's BB algorithm. |
| B2 ⚠️: HRV declines multi-day even with rest | TESTED — proxy | [HA08c](garmin/hypotheses/HA08c-sleep-stress-slope/result.md) — multi-day sleep-stress slope as HRV-creep proxy | **HA08c train SUPPORTED +23.0 pp @ 1.5σ (Fisher p=0.054, fails α=0.05); validate refuted.** Trailing-5-day OLS slope of the same primitive as HA07c — confirms multi-day creep pattern in train era. |
| B3: Rising 7d HRV baseline = improving | NOT ADDRESSED | — | S01 trajectories cover related metrics (stress, RHR, sleep-eff, max-spike) but not an HRV-equivalent. |
| **B4 ⚠️: Sudden HRV spike is a NEGATIVE leading indicator (parasympathetic swing)** | **TESTED — proxy, SUPPORTED** (framing softened) | [HA07d](garmin/hypotheses/HA07d-sleep-stress-variability/result.md) — sleep-stress variability delta; corroborated by [HA10](garmin/hypotheses/HA10-bb-overnight-recharge/result.md) validate elevated arm + [HA06b](garmin/hypotheses/HA06b-rhr-zscore/result.md) validate directionality | **HA07d SUPPORTED both eras** (validate +21.7 pp Fisher p=0.070; train +19.6 pp Fisher p=0.093). HA07d Cat 2/3 RESCUE in v2. The parasympathetic-swing direction is empirically present, but the **2026-06-08 collinearity audit** shows the three "independent channels" share substantial variance: HA10/HA07c are one signal, HA07d is partially tied to it (ρ = +0.501). Honest effective-N reading: ~2 channels, neither clearing α=0.0125. |
| B5: HRV rises at acute-illness onset | BLOCKED (HRV not on FR245) + NOT ADDRESSED (no illness labels) | — | Doubly gated. |

### C. Stress score

| Wiggers | Status | Project tests | Outcome |
|---|---|---|---|
| C1: Night high-stress elevated on/before crashes | TESTED — proxy | [HA07c](garmin/hypotheses/HA07c-sleep-stress-mean-delta/result.md) — sleep-stress mean as the "night high-stress" measurement | HA07c train SUPPORTED +23.2 pp; validate refuted. See B1 for collinearity caveat (HA07c ≡ −HA10). |
| C2: High daily stress predicts worse next-day recharge | NOT ADDRESSED | — | Would be a stress(t) → BB-gain(t→t+1) correlation. H04 looked at BB net delta as a precursor (refuted) but not as the consequent of daytime stress. |
| C3 ⚠️: Stress→fatigue relationship is non-linear/convex | NOT ADDRESSED | — | No non-linearity test has been run. [S02 §3.8](garmin/hypotheses/S02-score-trajectory/notes.md) added a same-day Spearman ρ for monotonic association (primary ρ = −0.0557 [−0.164, +0.009], ambiguous-underpowered); not a curvature test. |
| C4: Stress fails to drop during rest (stuck sympathetic) | PARTIAL | [HA11](garmin/hypotheses/HA11-stress-udip/result.md) — within-day stress U-dip event count | HA11 detects the *opposite* — sharp U-shaped dips followed by plateau. Train SUPPORTED +22.8 pp (Fisher p=0.084, fails α=0.05). HA11 train Cat 1 RESCUE in v2. The "stuck sympathetic" claim (failure to dip) is partly captured by HA11's lowered-arm (distribution-bounded). |

### D. Body battery

| Wiggers | Status | Project tests | Outcome |
|---|---|---|---|
| D1 ⚠️: Absolute BB level is a weak indicator of gevoelscore | PARTIAL | [H04](garmin/hypotheses/H04-body-battery/result.md) (BB net delta, refuted) | H04 tested net delta as precursor, not same-day level correlation with gevoelscore. |
| D2: BB dynamics beat BB level | **BLOCKED-PENDING-PATH-B (NEW since 2026-06-07)** | [H03b](garmin/hypotheses/H03b-bb-overnight-recharge-permin/result.md) returned **INCONCLUSIVE × 12** | The pre-registered per-minute BB overnight recharge test ran 2026-06-07 (late). Found two Garmin Connect API cutover dates: `bodyBatteryChange` populated from ~2023-12-31, `sleepBodyBattery` array from ~2024-06-03. Train era (14 crashes): zero coverage. Validate (15 crashes): only 6 have both per-minute data AND a usable baseline. Locked n_clean ≥ 10 threshold binds → INCONCLUSIVE in all 12 cells. **Path B (FIT decode of `unknown_233`) is the only route to per-minute BB for the full corpus.** HA10 stays as the canonical BB overnight recharge finding (peak-only metric, coarse resolution) for the validate era. |
| D3: Higher BB floor in low-crash stretches | NOT ADDRESSED | — | Would be a trajectory comparison; S01 doesn't track BB floor specifically. |
| D4: BB declines steeply around crashes; slope leads felt dip | PARTIAL | [HA10](garmin/hypotheses/HA10-bb-overnight-recharge/result.md) | HA10 tests morning BB *peak* level (HIGHEST anchor), not the *slope* of the decline. Validate SUPPORTED +16.2 pp (Fisher p=0.148; v2 Cat 3 RESCUE; threshold-fragile). **Now known to be ≡ −HA07c (ρ = −0.922)**. The "slope leads felt dip" sub-claim is unaddressed at coarse resolution; gated on FIT decode for per-minute. |
| **D5 ⚠️: Paradoxically HIGH morning BB precedes a crash** | **TESTED — direct, validate SUPPORTED (fragile)** | [HA10](garmin/hypotheses/HA10-bb-overnight-recharge/result.md) elevated arm | Validate 69% of triggering crashes are elevated direction. +29.0 pp one-sided elevated discrimination. **This is Wiggers' counter-intuitive D5 prediction empirically present in this participant's validate-era data.** Caveat: threshold-fragile (only fires at N_std=1.5; refuted at 2.0 and 2.5) AND the channel is now folded into the HA07c/HA10 cluster. |

### E. Steps / activity load

| Wiggers | Status | Project tests | Outcome |
|---|---|---|---|
| E1 ⚠️: Personal step threshold where crash probability rises | NOT ADDRESSED (no breakpoint analysis) | [HA01 / HA01b / HA01b-recomputed](garmin/hypotheses/) all refuted | HA01 family used the percentile-rank composite `exertion_class`, not raw steps with a breakpoint search. |
| E2: Rising step average without rising crashes = improvement | PARTIAL | [S01](garmin/hypotheses/S01-stabilisation-trajectories/notes.md); [00-crash_v1-counts](garmin/hypotheses/00-crash_v1-counts/counts.md) | The "improvement" framing is empirically present (10/year → 2/year crashes) but not formally cross-checked against rolling step averages. |
| E3: Intensive minutes track exertion better than raw steps | **TESTED — direct (HA01b per-axis + HA01c locked + HA01c v2)** | [HA01b per-axis diagnostic](garmin/hypotheses/HA01b-per-axis-diagnostic/result.md); [HA01c](garmin/hypotheses/HA01c-effective-exertion-shock/result.md); [HA01c v2](garmin/hypotheses/HA01c-threshold-monotonicity-diagnostic-v2/result.md) | **effective_exertion (UDS intensity-min + recorded activity duration) SUPPORTED both eras at +21.3 / +19.5 pp at τ=0.75**. step_burden (raw steps) SUPPORTED validate-only. max_hr_peak refuted both eras (inverted in validate, consistent with chronotropic incompetence). **Wiggers' E3 prediction confirmed at the locked threshold**: effective_exertion is the only axis surviving the both-eras gate. HA01c v2 mixed (validate Cat 1 RESCUE; train AMBIGUOUS — first AMBIGUOUS verdict in v2 series). Per playbook §4.4 → HA01c stays SUPPORTED-with-stability-mixed (honest but NOT load-bearing). Specificity gate also fails (60% of 4d windows trigger in nulls). |

### F. Sleep

| Wiggers | Status | Project tests | Outcome |
|---|---|---|---|
| F1: Longer sleep duration typical during PEM | NOT ADDRESSED | — | Sleep duration not tested as a precursor or correlate. |
| F2: Deep-sleep deviation (over OR under) associates with worse score | NOT ADDRESSED | — | Not specified in detail; gated on path B FIT decode for sharper sleep architecture. |
| F3: Garmin sleep score predicts next-day capacity | NOT ADDRESSED | — | Not tested. |
| F4: Bedtime inconsistency worsens next-day energy | NOT ADDRESSED | — | Not tested. |

Sleep-channel coverage is thin. The one test that ran ([H03](garmin/hypotheses/H03-sleep-efficiency/result.md), sleep efficiency) was refuted decisively. S01 confirmed sleep efficiency is flat across the entire window. Wiggers' sleep hypotheses target *different* sleep dimensions (duration, deep-sleep, sleep-score, bedtime variance) that are all untouched.

### G. Other sensors

| Wiggers | Status | Project tests | Outcome |
|---|---|---|---|
| G1: Elevated respiration rate = stuck sympathetic | NOT ADDRESSED | — | Respiration rate recorded by the watch; no test written. |
| G2: Skin temperature rises around PEM (or drops, n-of-1) | NOT ADDRESSED | — | Temperature not tested. |
| **G3 ⚠️: Barometric pressure × headache** | NOT ADDRESSED | — | Requires external weather-data join. The participant's headache tag appears in 78% of crash-day notes (per notes-language analysis); pressure data is free external data. Untouched but cheap opportunity. |
| G4: SpO2 dips on exertion | DEPRIORITISED PER SOURCE | — | Wiggers herself flags SpO2 as unreliable on Garmin. |

### H. Mechanism & lead/lag (the decisive tests)

| Wiggers | Status | Project tests | Outcome |
|---|---|---|---|
| **H1 ⚠️: Wearable signals lead the felt crash** | **PARTIAL + first direct lag test REFUTED in observed direction** | All H## / HA## precursor tests use 3–5 day lead-up windows; [S02b](garmin/hypotheses/S02b-score-lead/notes.md) is the first direct cross-correlation lag test | Every SUPPORTED finding (H02b train, H02d train, HA06b train, HA11 train, HA10 validate, HA07d both eras) implicitly demonstrates wearable signals discriminate days BEFORE the felt crash. **S02b tested the direct lag-vs-same-day question** using lag values pre-committed from S02. **REFUTED on criterion (c)**: primary ρ_lag = +0.099 vs matched same-day ρ = −0.097, |delta| = +0.002. **Methodology lesson banked**: rolling-curve turnaround-date mismatches can occur without daily-resolution lead/lag signals. |
| **H2 ⚠️: A fraction of crashes are activity-invisible** | PARTIAL | HA01b-recomputed refuted; H02b-on-dips heterogeneity finding; HA01c locked SUPPORTED but not card-shippable | HA01b's clean-baseline refutation says activity shock does NOT precede most validate-era crashes — consistent with "validate-era crashes are largely activity-invisible." HA01c rescues effective_exertion as the surviving axis, but at 60% null-fire rate → not a formal per-crash count. |
| **H3 ⚠️: Acute-illness vs PEM crashes have different Garmin signatures** | NOT ADDRESSED | — | Requires illness-vs-PEM labels (crash_v3 from notes, queued). |
| **H4 ⚠️: Parasympathetic-swing signature precedes a gevoelscore dip within 1–2 days** | **TESTED — proxy, SUPPORTED on direction; framing softened on independence** | [HA06b](garmin/hypotheses/HA06b-rhr-zscore/result.md) validate 75% lowered; [HA10](garmin/hypotheses/HA10-bb-overnight-recharge/result.md) validate 69% elevated BB; [HA07d](garmin/hypotheses/HA07d-sleep-stress-variability/result.md) variability collapse | **The parasympathetic-swing direction is empirically present on three operationalisations.** Per the 2026-06-08 audit, those three operationalisations share substantial variance (HA10 ≡ −HA07c; HA07d-HA07c +0.501; HA10-HA06b −0.393) — so the headline "three independent channels converge" must soften to "one autonomic-state signal viewed three ways + a partially-related variability channel." The direction holds; the convergence-as-corroboration framing was overstated. |
| H5: Each metric has a characteristic lag vs exertion | PARTIAL | H02d 3d/4d/5d monotonic profile; HA01b lag-profile report | Empirical lag observations exist (4–5 day lag is well-documented) but a formal "lag map" per metric has not been compiled. |

### I. Data-quality / methodology checks

| Wiggers | Status | Project tests | Outcome |
|---|---|---|---|
| I1: Re-run primary results excluding first ~3 weeks of each device | NOT ADDRESSED | — | The 2022-09-03 analysis-window start is ~13 months after the watch's first record, so device-warm-up should not contaminate the analysis. |
| I2: Mark device-change points; test for level shifts | NOT ADDRESSED | — | Firmware version is referenced (FR245 7.x → 10.4) but no level-shift test has been run. |
| I3: Confirm the rich-metrics overlap window | **PARTIAL → SHARPENED 2026-06-07 (H03b)** | Analysis window starts 2022-09-03 (the gevoelscore start) | The overlap question was implicitly handled by the window choice but not explicitly named per-metric. **H03b explicitly surfaced the cutover**: `sleepBodyBattery` populated only from ~2024-06-03 via API. Path B (FIT decode) is the only route to per-minute BB for the full corpus. Methodology lesson banked: verify data-availability across analysis window BEFORE locking inconclusive thresholds for any API-dependent pre-registration. |

---

## Status totals (revised 2026-06-08)

| Status | Count of Wiggers items |
|---|---:|
| TESTED — direct, with verdict | 6 (A1, A2, A3, E3 (HA01c locked), D5, C4 partial) |
| TESTED — proxy, with verdict | 6 (B1 → HA07c train SUPPORTED; B2 → HA08c train SUPPORTED; B4 → HA07d both eras; C1 → HA07c; H4 → HA06b/HA10/HA07d) |
| TESTED — proxy, queued/pending run | 0 (HA07c + HA08c executed 2026-06-07) |
| INCONCLUSIVE-BY-DATA (NEW status) | 1 (D2 → H03b INCONCLUSIVE × 12 on `sleepBodyBattery` cutover) |
| PARTIAL (some aspect addressed) | 7 (H1, H2, H5, C4, D1, D4, E2, I3) |
| NOT ADDRESSED | ~16 (B3, B5, C2, C3, D3, E1, F1, F2, F3, F4, G1, G2, G3, H3, I1, I2) |
| BLOCKED (hardware) | A4, B5 (HRV not on FR245), and now D2 BLOCKED-PENDING-FIT-DECODE rather than just queued |

**Roughly half the Wiggers register is still untouched.** The half that
has been addressed includes most of the autonomic / parasympathetic-swing
material and a substantial chunk of the resting-HR / night-HR material.
The sleep material and the external-data material (G3 pressure ×
headache) are large untouched zones.

---

## What's queued vs what's not even queued

### Queued / pre-registered / in flight

- **Path B (FIT decode of `unknown_233`)** — would unlock per-minute BB
  for the full corpus 2021-08-16 → 2026-06-04. Newly elevated to a
  bottleneck after H03b INCONCLUSIVE × 12; without it, D2 / D4 slope
  analysis stays blocked, H03b cannot be re-run with sufficient n on
  both eras, and sharper sleep architecture for F2 stays out of reach.
- **Crash_v3 mechanism subtyping from notes** — would unlock H3
  (acute-illness vs PEM separation).
- **Wiggers H1 Wiggers-direction lag test** — S02b only tested the
  empirically-observed score-leads-Garmin direction. A separate
  pre-registration testing the canonical wearables-lead-score direction
  at daily resolution remains warranted.

### Not queued — Wiggers items the project has NOT planned a test for

- **B3** (rising 7-day HRV baseline = improving stretches).
- **C2** (high daily stress → worse next-day recharge as causal-like
  correlation).
- **C3 ⚠️** (non-linearity / convexity of stress→fatigue).
- **D3** (higher BB floor in low-crash stretches).
- **E1 ⚠️** (personal step-threshold breakpoint analysis).
- **F1** (longer-than-normal sleep duration during PEM).
- **F3** (Garmin sleep score → next-day capacity).
- **F4** (bedtime variance → next-day energy).
- **G1** (respiration rate as stuck-sympathetic marker).
- **G2** (temperature deviation around PEM).
- **G3 ⚠️** (barometric pressure × headache).
- **H5** (formal per-metric lag map).
- **I1, I2** (device-warm-up + level-shift robustness).

Of the unqueued items, the four ⚠️-flagged ones (C3 non-linearity, E1
personal-step-threshold, G3 pressure × headache, plus B3 / F-family
sleep dimensions) deserve registry consideration. **G3 in particular**
— the participant's headache tag appears in 78% of crash-day notes per
the notes-language analysis, and barometric pressure is free external
data. The pairing has not been attempted.

---

## Where this leaves the project relative to Wiggers' framing

Three readings of this map are now all true:

**Optimistic reading (UPDATED 2026-06-08).** The most counter-intuitive
piece of Wiggers' register — the parasympathetic-swing pattern
(B4 + H4 + D5) — has empirical support on multiple operationalisations.
The participant's validate-era crashes look consistent with Wiggers'
lived description: "the body looks recharged but isn't." This is real
convergence between a qualitative clinical observation and biometric
signals.

**Sober reading (UNCHANGED).** Roughly half the Wiggers register is
genuinely untouched. The sleep material is the largest gap (F1–F4 + B3
all unaddressed). External-data material (G3 pressure) is untouched.
Behavioural-channel material (E1 step threshold) is untouched. Several
of the data-quality robustness checks (I1, I2) Wiggers explicitly calls
out have not been run.

**Statistically-honest reading (NEW 2026-06-08).** The 2026-06-08
Tier 2 audit (Fisher's exact + cross-channel correlation) revealed that
the "seven SUPPORTED on six channels" project framing was overstated.
H02b ≡ H02d (ρ = +1.000), HA10 ≡ −HA07c (ρ = −0.922), HA07d-HA07c are
moderately collinear (+0.501). The effective independent channel count
is closer to **3–4 signal clusters**. Of 11 primary verdicts, only
**H02b train and H02d train clear α = 0.05 one-sided Fisher's exact**,
and once the H02b/H02d collinearity is folded, only **one distinct
primitive** survives an honest effective-N Bonferroni at α = 0.0125
(the within-day stress spike cluster, train era only). The bar-pass
findings remain on record; what changed is how many genuinely
independent measurements back them. For the parasympathetic-swing
cluster specifically: the *direction* is preserved across multiple
views, but the *count of independent corroborations* is one fewer than
the "three channels converge" headline suggested.

For the product question that anchors the whole investigation —
"would a watch-based warning system be useful here?" — the autonomic
findings are necessary but not sufficient. H1 was tested directly
(S02b) on 2026-06-07 and REFUTED at daily resolution in the observed
direction; H2 and H3 remain PARTIAL / NOT ADDRESSED. The per-axis
finding on effective_exertion (HA01c) fails the specificity gate
(60% null-fire rate) and so is not card-shippable.

The natural next-phase prioritisation, read off the Wiggers register
specifically (revised 2026-06-08):

1. **Path B FIT decode** — unblocks D2 (BB dynamics), F2 (deep-sleep
   sharper), and re-running H03b with sufficient n in both eras.
   Currently the project's tightest data-availability bottleneck.
2. **H1 Wiggers-direction lag test** — S02b only tested the observed
   direction. The canonical Wiggers direction remains untested.
3. **H2 formal activity-invisible-crash count** (small, cheap, would
   sharpen the synthesis given the HA01c specificity-fail).
4. **G3 barometric pressure × headache** (cheap, untouched, plausibly
   strong; headache is the master variable in notes).
5. **F-family sleep dimensions** (F1 duration, F3 sleep score, F4
   bedtime variance) — Wiggers' sleep material is broader than H03b's
   architecture focus.
6. **H3 acute-vs-PEM separation** (gated on notes-quality work).

---

## Changelog vs 2026-06-07 snapshot

| change | effect |
|---|---|
| **H03b run 2026-06-07 (late) → INCONCLUSIVE × 12** | D2 moves from QUEUED to INCONCLUSIVE-BY-DATA + BLOCKED-PENDING-FIT-DECODE. I3 sharpened with the explicit `sleepBodyBattery` ~2024-06-03 cutover. |
| **2026-06-08 Fisher's exact + 95% CIs on 11 primary verdicts** | Only H02b train (p=0.029) and H02d bridge × 5d train (p=0.011) clear α=0.05 one-sided. HA07d/HA10/HA06b/HA01c all fail conventional significance. |
| **2026-06-08 cross-channel Spearman/Pearson correlation matrix** | H02b ≡ H02d (ρ=+1.000) and HA10 ≡ −HA07c (ρ=−0.922) are structural collinearities, not independent channels. Effective channel count drops from ~7 to ~3–4. |
| **B4 / H4 framing** | "three independent channels converge" softens to "one autonomic-state signal viewed three ways + partially-related variability." Direction unchanged; bar-pass verdicts unchanged on record. |
| **E3 status** | HA01c locked SUPPORTED both eras at τ=0.75 (+21.3 / +19.5 pp); HA01c v2 mixed (validate Cat 1 RESCUE; train AMBIGUOUS — first in v2 series). SUPPORTED-with-stability-mixed, not load-bearing, not card-shippable on specificity. |

---

*Map compiled 2026-06-08 by the independent reviewer agent. Reads
against the Wiggers source register
([wiggers_testable_hypotheses.md](wiggers_testable_hypotheses.md)) and
the current state of [docs/research/garmin/](garmin/). Snapshot in
time; will need refreshing as crash_v3 unlocks H3, as path B unlocks
D2/D4/F2, and as G3 / F-family items eventually get pre-registered.*
