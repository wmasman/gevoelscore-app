# Wiggers hypotheses — progress map as of 2026-06-07

*A snapshot of which Wiggers testable hypotheses
([wiggers_testable_hypotheses.md](wiggers_testable_hypotheses.md)) have
been addressed by the Garmin × crash investigation so far, how, what
the outcome was, and what remains queued or untouched.*

*Source register: ~40 testable hypotheses across nine sections (A–I).
This map cross-references each to the relevant H## / HA## / S## test
in [docs/research/garmin/hypotheses/](garmin/hypotheses/).*

---

## How to read this map

Each row carries one of five statuses:

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

Where a Wiggers hypothesis is flagged ⚠️ in the source (high-value /
counter-intuitive / contradicts a prior finding), that flag is
preserved.

---

## Priority shortlist (Wiggers' top six) — current status

Wiggers explicitly named six tests as the ones that would decide
product direction. Their status here is the most important reading
of this whole map:

| Wiggers ID | Question | Status as of 2026-06-07 |
|---|---|---|
| **H1 ⚠️** | Do wearable signals lead the felt crash? | **PARTIAL → daily-resolution lead/lag REFUTED in the empirically-observed direction (S02b, 2026-06-07); Wiggers-direction not directly tested.** Every precursor test uses a 3–5 day lead-up window and several SUPPORT in some era — implicitly demonstrating wearables can lead self-report. The project's **first direct cross-correlation lag test** ([S02b](garmin/hypotheses/S02b-score-lead/notes.md)) tested the empirically-observed score-leads-Garmin direction (from S02's trajectory-level T1 trigger) at daily resolution with block-bootstrap CI. **REFUTED**: primary lagged ρ at +149d = +0.099 vs matched same-day ρ = −0.097, |delta| = +0.002 against the 0.10 criterion-c bar. Trajectory-level lead/lag (S02 T1) does not survive to daily resolution. The Wiggers-direction (wearables-lead-score) remains untested directly, but the magnitude of all observed lagged ρ values (none above \|0.10\|) suggests it would also be small at daily resolution. |
| **H2 ⚠️** | How many crashes are "activity-invisible"? | **PARTIAL.** HA01b-recomputed refuted activity-shock as a precursor on a clean baseline → consistent with most validate-era crashes being activity-invisible. Not yet a formal count of crash episodes by physical-signature presence/absence. |
| **H3 ⚠️** | Acute-illness vs PEM crashes separable in Garmin? | **NOT ADDRESSED.** Requires illness-vs-PEM labels (queued as crash_v3 from notes; gated on notes-quality work). |
| **C3 / D1 / D2** | Non-linearity of stress; level-vs-dynamics for BB | **NOT ADDRESSED for C3 + D2; PARTIAL for D1** (H04 refuted BB net delta as a precursor; not a same-day correlation test). |
| **B4 / H4 ⚠️** | Parasympathetic-swing as an inverted indicator | **TESTED — proxy, SUPPORTED both eras under v2 criteria (atomic restoration 2026-06-07 after v2 diagnostic round).** Trajectory: v1 diagnostic CLOSE both eras on HA07d + HA10 → demoted. v2 criteria revision (five-category shape rule responding to v1's overspecification of canonical-decline robustness) was locked separately and applied symmetrically to HA10/HA07d/HA06b/HA11. **v2 outcomes**: HA07d both eras RESCUE (train via Cat 3 rising/late-peak; validate via Cat 2 stable plateau + Cat 3). HA10 validate RESCUE via Cat 3. HA06b train PERMANENTLY CLOSED via Cat 4 (2 sign-changes in meaningful range — discipline binds in the demotion direction too). HA11 train RESCUE via Cat 1 (canonical decline). **Restored anchors for B4/H4**: HA07d primary + HA10 corroborating secondary for validate-era card (b2); HA11 + HA07d (train arm) for train-era card (b). The parasympathetic-swing finding is restored to load-bearing under v2 with principled shape categories; the discipline-cost of HA06b's permanent demotion is real. |
| **G3 ⚠️** | Barometric pressure × headache | **NOT ADDRESSED.** Requires external weather data join; not yet attempted. |

**Of Wiggers' six product-decisive tests, two are PARTIAL, one is
TESTED-via-proxy-with-LOAD-BEARING-STATUS-PENDING-v2 (downgraded
from SUPPORTED), two are NOT ADDRESSED, and one is NOT ADDRESSED
pending notes-quality work.** The B4+H4 cluster — formerly the
project's primary empirical anchor for validate-era findings — was
demoted in synthesis-level framing on 2026-06-07 after the HA07d
threshold-monotonicity diagnostic v1 returned CLOSE in both eras.
Locked SUPPORTED verdicts remain on record per audit-trail
discipline; load-bearing status depends on v2 diagnostic outcomes
(pre-registered same day; running pending review of revised
criteria). In the interim, the validate-era retrospective card
family has no load-bearing anchor.

---

## Section-by-section progress

### A. Resting HR & night HR

| Wiggers | Status | Project tests | Outcome |
|---|---|---|---|
| A1: RHR elevated on/before crashes | TESTED — direct | [H01](garmin/hypotheses/H01-rhr-drift/result.md) (daily RHR, rolling 90d, ≥3 bpm); [HA06](garmin/hypotheses/HA06-morning-rhr-delta/result.md) (nightly lowest stable HR, absolute thresholds); [HA06b](garmin/hypotheses/HA06b-rhr-zscore/result.md) (nightly lowest stable HR, z-score thresholds) | **H01 refuted both eras. HA06 refuted both eras (validate 0/15). HA06b train SUPPORTED +18.9 pp @ 1.5σ; validate refuted.** Direction matters: only when measured as z-score deviation, not absolute bpm, does the train-era signal emerge. |
| A2: RHR deviates either direction | TESTED — direct | [HA06](garmin/hypotheses/HA06-morning-rhr-delta/result.md) bidirectional arm; [HA06b](garmin/hypotheses/HA06b-rhr-zscore/result.md) bidirectional primary + directionality split | **Confirmed empirically**: train 70% elevated / 30% lowered; validate 25% elevated / 75% lowered. The "either direction" Wiggers prediction is correct; the *dominant* direction reverses across eras. |
| A3: Night RHR elevated from t-2 onwards | TESTED — direct | HA06 / HA06b 4d primary + 5d secondary lead-up windows | Lead-up structure addressed. Train-era SUPPORTED at 4d on z-score. |
| A4: Sustained multi-hour RHR elevation (not brief spike) | BLOCKED — no intraday HR analysis run | — | Would need intraday HR aggregation; not yet attempted. |

### B. HRV

| Wiggers | Status | Project tests | Outcome |
|---|---|---|---|
| B1: Day-over-day HRV drop ≥ 10 predicts crash | TESTED — proxy (queued, not yet run) | [HA07c](garmin/hypotheses/HA07c-sleep-stress-mean-delta/hypothesis.md) — sleep-stress mean delta as HRV-drop proxy | Pending API path C backfill. |
| B2 ⚠️: HRV declines multi-day even with rest | TESTED — proxy (queued, not yet run) | [HA08c](garmin/hypotheses/HA08c-sleep-stress-slope/hypothesis.md) — multi-day sleep-stress slope as HRV-creep proxy | Pending API path C backfill. |
| B3: Rising 7d HRV baseline = improving | NOT ADDRESSED | — | S01 trajectories cover related metrics (stress, RHR, sleep-eff, max-spike) but not an HRV-equivalent. |
| **B4 ⚠️: Sudden HRV spike is a NEGATIVE leading indicator (parasympathetic swing)** | **TESTED — proxy, SUPPORTED both eras** | [HA07d](garmin/hypotheses/HA07d-sleep-stress-variability/hypothesis.md) — sleep-stress variability delta; corroborated by [HA10](garmin/hypotheses/HA10-bb-overnight-recharge/result.md) validate elevated arm + [HA06b](garmin/hypotheses/HA06b-rhr-zscore/result.md) validate directionality | **HA07d SUPPORTED both eras with directionality reversal: train shows variability shifts in either direction, validate shows variability collapse. The "great-looking numbers precede a crash" Wiggers prediction is empirically present.** |
| B5: HRV rises at acute-illness onset | BLOCKED (HRV not on FR245) + NOT ADDRESSED (no illness labels yet) | — | Doubly gated: HRV unavailable AND no illness-vs-PEM labels. |

### C. Stress score

| Wiggers | Status | Project tests | Outcome |
|---|---|---|---|
| C1: Night high-stress elevated on/before crashes | TESTED — proxy (queued, not yet run) | [HA07c](garmin/hypotheses/HA07c-sleep-stress-mean-delta/hypothesis.md) — sleep-stress mean as the "night high-stress" measurement | Pending API path C backfill. Note: HA07c uses the mean of sleep-window stress samples, which is one of the operationalisations Wiggers' C1 implies. |
| C2: High daily stress predicts worse next-day recharge | NOT ADDRESSED | — | Would be a stress(t) → BB-gain(t→t+1) correlation. H04 looked at BB net delta as a precursor (refuted) but not as the consequent of daytime stress. |
| C3 ⚠️: Stress→fatigue relationship is non-linear/convex | NOT ADDRESSED | — | No non-linearity test has been run. [S02 §3.8](garmin/hypotheses/S02-score-trajectory/notes.md) (executed 2026-06-07) added a same-day Spearman ρ for monotonic association (primary ρ = −0.0557 [−0.164, +0.009], ambiguous-underpowered); not a curvature test. C3 still untested. |
| C4: Stress fails to drop during rest (stuck sympathetic) | PARTIAL | [HA11](garmin/hypotheses/HA11-stress-udip/result.md) — within-day stress U-dip event count | HA11 detects the *opposite* — sharp U-shaped dips followed by plateau. Train SUPPORTED +22.8 pp. The "stuck sympathetic" claim (failure to dip) would be the inverse arm and is partly captured by HA11's lowered-arm (0 of 14 train, 0 of 15 validate — distribution-bounded; the bidirectional arm shows the elevated dominates). |

### D. Body battery

| Wiggers | Status | Project tests | Outcome |
|---|---|---|---|
| D1 ⚠️: Absolute BB level is a weak indicator of gevoelscore | PARTIAL | [H04](garmin/hypotheses/H04-body-battery/result.md) (BB net delta, refuted) | H04 tested net delta as precursor, not same-day level correlation with gevoelscore. The level-vs-gevoelscore correlation is not directly measured. S02's §3.8 will compute Spearman ρ between score and avg stress but not BB. |
| D2: BB dynamics beat BB level | NOT ADDRESSED | — | Requires per-minute BB (gated on H04b) plus a same-day or next-day correlation. |
| D3: Higher BB floor in low-crash stretches | NOT ADDRESSED | — | Would be a trajectory comparison; S01 doesn't track BB floor specifically. |
| D4: BB declines steeply around crashes; slope leads felt dip | PARTIAL | [HA10](garmin/hypotheses/HA10-bb-overnight-recharge/result.md) | HA10 tests morning BB *peak* level (HIGHEST anchor), not the *slope* of the decline. Validate SUPPORTED +16.2 pp (threshold-fragile); train refuted. The "slope leads felt dip" sub-claim is unaddressed at coarse resolution; gated on H04b for per-minute. |
| **D5 ⚠️: Paradoxically HIGH morning BB precedes a crash** | **TESTED — direct, validate SUPPORTED (fragile)** | [HA10](garmin/hypotheses/HA10-bb-overnight-recharge/result.md) elevated arm | Validate 69% of triggering crashes are elevated direction. +29.0 pp one-sided elevated discrimination. **This is Wiggers' counter-intuitive D5 prediction empirically present in this participant's validate-era data.** Caveat: threshold-fragile (only fires at N_std=1.5; refuted at 2.0 and 2.5). |

### E. Steps / activity load

| Wiggers | Status | Project tests | Outcome |
|---|---|---|---|
| E1 ⚠️: Personal step threshold where crash probability rises | NOT ADDRESSED (no breakpoint analysis) | [HA01 / HA01b / HA01b-recomputed](garmin/hypotheses/) all refuted | HA01 family used the percentile-rank composite `exertion_class`, not raw steps with a breakpoint search. The Wiggers personal-threshold prediction has not been operationalised as a breakpoint test. |
| E2: Rising step average without rising crashes = improvement | PARTIAL | [S01](garmin/hypotheses/S01-stabilisation-trajectories/notes.md) describes the stabilisation pendulum across multiple metrics; crash-frequency drop documented in [00-crash_v1-counts](garmin/hypotheses/00-crash_v1-counts/counts.md) | The "improvement" framing is empirically present (10/year → 2/year crashes) but not formally cross-checked against rolling step averages. |
| E3: Intensive minutes track exertion better than raw steps | **ADDRESSED 2026-06-07** | activity-labels v3.1 uses both effective_exertion_min and step_burden in the percentile-rank composite; **[HA01b per-axis decomposition diagnostic](garmin/hypotheses/HA01b-per-axis-diagnostic/result.md)** ran the head-to-head | **effective_exertion (UDS intensity-min + recorded activity duration) SUPPORTED both eras at +21.3 / +19.5 pp**. step_burden (raw steps) SUPPORTED validate-only (+16.6 pp; train misses crit-c by 0.008). max_hr_peak refuted both eras (inverted in validate, consistent with chronotropic incompetence). vigorous_min SUPPORTED validate-only. **Wiggers' E3 prediction partially confirmed**: effective_exertion (intensity-minutes-based axis) is the only one that survives the both-eras gate, more reliably discriminating than raw steps. Composite REFUTED was hiding this axis-specific signal (MAX-rank composite triggers ~78% in null windows, diluting per-axis spread). Per-axis primary now pre-registered as [HA01c](garmin/hypotheses/HA01c-effective-exertion-shock/hypothesis.md) for clean re-test + v2 threshold-monotonicity diagnostic. |

### F. Sleep

| Wiggers | Status | Project tests | Outcome |
|---|---|---|---|
| F1: Longer sleep duration typical during PEM | NOT ADDRESSED | — | Sleep duration not tested as a precursor or correlate. |
| F2: Deep-sleep deviation (over OR under) associates with worse score | NOT ADDRESSED | — | H03b (sleep architecture sub-components) is pre-registered as a stub but not yet specified or run. |
| F3: Garmin sleep score predicts next-day capacity | NOT ADDRESSED | — | Not tested. |
| F4: Bedtime inconsistency worsens next-day energy | NOT ADDRESSED | — | Not tested. |

Sleep-channel coverage is thin. The one test that ran ([H03](garmin/hypotheses/H03-sleep-efficiency/result.md), sleep efficiency) was refuted decisively (0% triggered) and S01 confirmed sleep efficiency is essentially flat across the entire window. But Wiggers' sleep hypotheses target *different* sleep dimensions (duration, deep-sleep, sleep-score, bedtime variance) that are all untouched.

### G. Other sensors

| Wiggers | Status | Project tests | Outcome |
|---|---|---|---|
| G1: Elevated respiration rate = stuck sympathetic | NOT ADDRESSED | — | Respiration rate is recorded by the watch but no test has been written. |
| G2: Skin temperature rises around PEM (or drops, n-of-1) | NOT ADDRESSED | — | Temperature not tested. |
| **G3 ⚠️: Barometric pressure × headache** | NOT ADDRESSED | — | Requires external weather-data join. The participant's headache tag is the most-cited symptom in notes-language work; pairing with pressure data is an untouched but cheap opportunity. |
| G4: SpO2 dips on exertion | DEPRIORITISED PER SOURCE | — | Wiggers herself flags SpO2 as unreliable on Garmin. Skipped, correctly. |

### H. Mechanism & lead/lag (the decisive tests)

| Wiggers | Status | Project tests | Outcome |
|---|---|---|---|
| **H1 ⚠️: Wearable signals lead the felt crash** | **PARTIAL + first direct lag test REFUTED in observed direction** | All H## / HA## precursor tests use 3–5 day lead-up windows; [S02b](garmin/hypotheses/S02b-score-lead/notes.md) (2026-06-07) is the first direct cross-correlation lag test | Every SUPPORTED finding (H02b train, H02d train, HA06b train, HA11 train, HA10 validate, HA07d both eras) implicitly demonstrates wearable signals discriminate days BEFORE the felt crash. **S02b tested the direct lag-vs-same-day question** using lag values pre-committed from S02's algorithm (149d for avg stress, 100d for max-spike). **REFUTED on criterion (c)**: primary ρ_lag = +0.099 [+0.035, +0.203] vs matched same-day ρ = −0.097, |delta| = +0.002 (bar 0.10). Sign-flipped near-identical magnitudes at both lag conditions; no daily-resolution lead/lag signal in either direction. Wiggers-direction (wearables-lead-score) remains untested directly but the magnitude data suggests it would also be small. **Methodology lesson banked: rolling-curve turnaround-date mismatches can occur without daily-resolution lead/lag signals.** Implicit lead in lead-up window tests stands; explicit daily cross-correlation refuted. |
| **H2 ⚠️: A fraction of crashes are activity-invisible** | PARTIAL | [HA01b-recomputed](garmin/hypotheses/) refuted; H02b-on-dips heterogeneity finding | HA01b's clean-baseline refutation says activity shock does NOT precede most validate-era crashes — consistent with "validate-era crashes are largely activity-invisible." Not yet a formal per-crash count of "physical signature present vs absent." |
| **H3 ⚠️: Acute-illness vs PEM crashes have different Garmin signatures** | NOT ADDRESSED | — | Requires illness-vs-PEM labels (crash_v3 from notes, queued). Direct mechanism-separation test is downstream of this labelling work. |
| **H4 ⚠️: Parasympathetic-swing signature (HRV↑ + RHR↓ post-overexertion) precedes a dip within 1–2 days** | **TESTED — proxy, SUPPORTED across three channels** | [HA06b](garmin/hypotheses/HA06b-rhr-zscore/result.md) validate 75% lowered; [HA10](garmin/hypotheses/HA10-bb-overnight-recharge/result.md) validate 69% elevated BB (inverse of RHR); [HA07d](garmin/hypotheses/HA07d-sleep-stress-variability/hypothesis.md) variability collapse | **The parasympathetic-swing pattern is empirically present in this participant's validate-era data on three independent operationalisations.** This is the most-developed corner of the Wiggers register in the project. |
| H5: Each metric has a characteristic lag vs exertion | PARTIAL | H02d 3d/4d/5d monotonic profile; HA01b lag-profile report | Empirical lag observations exist (4–5 day lag is now well-documented) but a formal "lag map" per metric has not been compiled. |

### I. Data-quality / methodology checks

| Wiggers | Status | Project tests | Outcome |
|---|---|---|---|
| I1: Re-run primary results excluding first ~3 weeks of each device | NOT ADDRESSED | — | The 2022-09-03 analysis-window start is ~13 months after the watch's first record, so device-warm-up should not contaminate the analysis. But this hasn't been systematically robustness-checked. |
| I2: Mark device-change points; test for level shifts | NOT ADDRESSED | — | Firmware version is referenced (FR245 7.x → 10.4) but no level-shift test has been run. |
| I3: Confirm the rich-metrics overlap window | PARTIAL | Analysis window starts 2022-09-03 (the gevoelscore start) | The overlap question is implicitly handled by the window choice but not explicitly named per-metric. |

---

## Status totals

| Status | Count of Wiggers items |
|---|---:|
| TESTED — direct, with verdict | 5 (A1, A2, A3, D5, C4 partial) |
| TESTED — proxy, with verdict, SUPPORTED both eras under v2 | 1 (B4 / H4 cluster — HA07d both eras RESCUE under v2 Cat 2/3; HA10 validate RESCUE under v2 Cat 3; HA11 train RESCUE under v2 Cat 1; HA06b train permanently CLOSED under v2 Cat 4) |
| TESTED — proxy, queued/pending run | 2 (B1 → HA07c; B2 → HA08c) |
| PARTIAL (some aspect addressed) | 7 (H1, H2, H5, C4, D1, D4, E2, E3, I3) |
| NOT ADDRESSED | ~17 (B3, B5, C2, C3, D2, D3, E1, F1, F2, F3, F4, G1, G2, G3, H3, I1, I2) |
| BLOCKED (hardware) | A4, B-family direct (B1–B5 without proxy substitute) |

**Roughly half the Wiggers register is untouched.** The half that has
been addressed includes most of his autonomic / parasympathetic-swing
material (the most counter-intuitive part) and a substantial chunk of
the resting-HR / night-HR material. The sleep material and the
external-data material (G3 pressure × headache) are large untouched
zones.

---

## What's queued vs what's not even queued

### Queued / pre-registered / in flight

- **HA07c** (sleep-stress mean delta) — addresses B1 + C1.
- **HA08c** (multi-day sleep-stress slope) — addresses B2.
- **H04b** (per-minute BB decode, two parallel paths) — would unlock
  D2 + D4 slope analysis + better H03b sleep architecture.
- **H03b** (sleep architecture sub-components) — would address F2;
  not yet specified in detail; gated on H04b.
- **Crash_v3 mechanism subtyping from notes** — would unlock H3
  (acute-illness vs PEM separation).
- **S02 score trajectory** *(EXECUTED 2026-06-07)* — addressed H1
  (lead/lag) via S02b daily-resolution cross-correlation. S02 found
  trajectory-level T1 inflection-date mismatch (score peaks ~5 months
  before Garmin avg-stress); S02b REFUTED the daily-resolution
  version of that finding (criterion c failed by 0.10). The H1
  question now has a direct lag-test datapoint in the observed
  direction; Wiggers-direction remains untested directly.
  S02c characterised the recent May 2026 perturbation against
  recent baseline (only RHR drift; others essentially unmoved).

### Not queued — Wiggers items the project has NOT planned a test for

- **B3** (rising 7-day HRV baseline = improving stretches).
- **B5** (HRV rise at acute-illness onset).
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
personal-step-threshold, G3 pressure × headache, plus B3 / B5 / F-family
sleep dimensions) deserve registry consideration. Especially G3 — the
participant has a headache tag that appears in 78% of crash-day notes
per the notes-language analysis, and barometric pressure is free
external data. The pairing has not been attempted.

---

## Where this leaves the project relative to Wiggers' framing

Two readings of this map are both true:

**Optimistic reading (UPDATED 2026-06-07 after diagnostic-v1
CLOSE).** The single most counter-intuitive piece of
Wiggers' register — the parasympathetic-swing pattern (B4 + H4 + D5)
— was, until 2026-06-07, the part the project had *most thoroughly*
validated through three independent operationalisations (HA07d
sleep-stress variability,
HA10 morning BB peak, HA06b RHR z-score directionality). The
participant's validate-era crashes look exactly like Wiggers' lived
description: "the body looks recharged but isn't." This is real
empirical convergence between a qualitative clinical observation and
a hard biometric signal.

**Sober reading.** Roughly half the Wiggers register is genuinely
untouched. The sleep material is the largest gap (F1–F4 + B3 all
unaddressed). External-data material (G3 pressure) is untouched.
Behavioural-channel material (E1 step threshold) is untouched. Several
of the data-quality robustness checks (I1, I2) Wiggers explicitly
calls out have not been run. The project's depth is concentrated on
the autonomic-channel hypotheses; its breadth across Wiggers' full
register is partial.

For the product question that anchors the whole investigation —
"would a watch-based warning system be useful here?" — the autonomic
findings are necessary but not sufficient. The H1 lead/lag analysis,
the H2 activity-invisible-crash count, and the H3 acute-vs-PEM
separation are the three Wiggers items most directly downstream of the
product question. **H1 was tested directly (S02b) on 2026-06-07 and
REFUTED at daily resolution in the observed direction**; H2 and H3
remain PARTIAL / NOT ADDRESSED.

The natural next-phase prioritisation, read off the Wiggers register
specifically (revised after S02b execution):

1. **H1 Wiggers-direction lag test** — S02b only tested the
   empirically-observed score-leads-Garmin direction. A separate
   pre-registration testing the Wiggers-canonical
   wearables-lead-score direction at daily resolution remains
   warranted, though magnitude data from S02b suggests it would
   likely be small.
2. **H2 formal activity-invisible-crash count** (small, cheap, would
   sharpen the synthesis).
3. **G3 barometric pressure × headache** (cheap, untouched, plausibly
   strong).
4. **F-family sleep dimensions** (F1 duration, F3 sleep score, F4
   bedtime variance) — Wiggers' sleep material is broader than H03b's
   architecture focus.
5. **H3 acute-vs-PEM separation** (gated on notes-quality work; will
   become the largest mechanism-separation move when it lands).

---

*Map compiled 2026-06-07 by the independent reviewer agent. Reads
against the Wiggers source register
([wiggers_testable_hypotheses.md](wiggers_testable_hypotheses.md)) and
the current state of [docs/research/garmin/](garmin/). Snapshot in
time; will need refreshing as HA07c / HA08c / S02 land and as crash_v3
unlocks the H3-family separation tests.*

*Update 2026-06-07 (later still): Wiggers' E3 prediction
(intensive-minutes track exertion better than raw steps) addressed
via the HA01b per-axis decomposition diagnostic — effective_exertion
(intensity-minutes-based) is the only axis surviving the both-eras
gate. HA01c + v2 pre-registered as pre-committed follow-ups. See
[garmin/hypotheses/HA01b-per-axis-diagnostic/result.md](garmin/hypotheses/HA01b-per-axis-diagnostic/result.md).
Other Wiggers items unchanged.*

*Update 2026-06-07 (later still ×2): HA01c + v2 chain completed
same-day. HA01c locked-threshold verdict SUPPORTED both eras
(+21.3 / +19.5 pp at τ=0.75). HA01c v2 mixed verdict — first
AMBIGUOUS in v2 series — train AMBIGUOUS (bumpy-but-never-negative,
shape doesn't fit Cat 1-5), validate Cat 1 RESCUE (textbook
canonical decline). Per playbook §4.4 both-eras rule, HA01c stays
SUPPORTED-with-stability-mixed (honest but NOT load-bearing). **E3
status update**: Wiggers' prediction partially confirmed at the
locked threshold (effective_exertion is the most discriminating
single axis both eras) but the train-arm threshold-stability under
the locked v2 framework is undecided. No card.md drafted (specificity
+ v2 mixed both block). See
[HA01c v2 result.md](garmin/hypotheses/HA01c-threshold-monotonicity-diagnostic-v2/result.md).*
