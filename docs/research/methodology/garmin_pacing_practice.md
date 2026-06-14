# Garmin pacing practice — operational protocol

*Producer-mode methodology MD. Drafted 2026-06-14 from a structured
interview with the participant; supersedes ad-hoc references in the
[lived-experience braindump](../lived_experience_garmin_pacing_2026-06-14.md).
Status: working document, locked sections marked.*

---

## 1. What this MD is, and what it is not

**This MD documents how the participant uses Garmin (Forerunner 245)
in daily life to pace through Long COVID.** It is written from the
*wearer-as-operator* perspective: which signals are read live, at what
checkpoints, and what action each warning triggers.

It serves as a **prior-source document** for the Personal-register
([personal_hypotheses.md](../personal_hypotheses.md)). Hypotheses about
Garmin-derived signals may cite this MD as evidence that the
participant operates on these patterns *before* any analysis on the
corpus runs, satisfying [CONVENTIONS §4.3](../CONVENTIONS.md#43-prior-driven-hypotheses-are-confirmatory-not-exploratory)
(prior-driven hypotheses are confirmatory).

It is NOT:

- a treatment recommendation,
- a test of whether the protocol works (descriptive characterisation
  of pacing efficacy lives under [QUEUED-WORK.md C.4 + C.5](../QUEUED-WORK.md)),
- a mechanistic claim about what each Garmin channel measures (per
  [CONVENTIONS §4.1](../CONVENTIONS.md#41-no-interpretive-marks-on-raw-or-descriptive-layers),
  describes operator response, not imputed device meaning),
- a general PEM-pacing guide (n=1 protocol; thresholds are this
  participant's, learnt by trial-and-error).

---

## 2. Origins

Trial-and-error / observational. Specifically:

- **Concept of pacing**: came from ergotherapie (standard Dutch
  ergo-PEM track) early in the LC course. Ergo gave the *framework*
  (pacing exists; envelope is finite; cognitive + emotional load
  count).
- **Specific Garmin thresholds and read-patterns**: learnt from years
  of wearing the watch through many crashes. The 25/20/15 BB floor,
  the rest-stress trigger, the late-afternoon decision check, and
  the felt-state-vs-BB mismatch diagnostic all emerged from
  observation rather than from any external source.
- **Wiggers handleiding (2025-07)**: found and read **only very
  recently** (2026), well after the protocol was already operational.
  Wiggers' value is **naming patterns the participant already saw**
  — vocabulary ("stuck sympathetic", "walls of orange", "false
  energy", "parasympathetic swing") that retrospectively fit
  existing observations. The protocol was not built from Wiggers;
  Wiggers gave language to a protocol the participant had already
  arrived at independently. Where Wiggers' specific numbers differ
  from the participant's (e.g. Wiggers' 70-80% BB floor target vs
  the participant's 25/20/15 working floor), §3.2 + §7 below
  document the divergence.

### Temporal qualifier — this protocol is a recent stabilisation, not a constant

This protocol was not in place from the start of LC. It **emerged
and evolved over time**, with elements added, refined, and dropped
across years of wearing the watch through many crashes. The coherent
form described in §3-§6 is **most consistent in the most recent
months (as of 2026-06-14)**; earlier periods of the LC corpus reflect
partial, less-stable, or different operational rules.

Implication for hypotheses citing this MD: the protocol as documented
is a **recent stabilisation**, not a constant across the dataset.
Personal-register hypotheses tested across the full LC corpus should
acknowledge this — what the participant *operates on* now is not
identical to what they operated on in 2022-23 (when pacing as a
practice was being learnt), or in the work-attempt / work-stop
periods (where context disrupted any stable protocol). The protocol
is increasing-fidelity evidence in the most recent months and
partial-fidelity evidence earlier.

This is honest caveat-class framing per [CONVENTIONS §4.2](../CONVENTIONS.md#42-caveats-yes-a-priori-claims-no);
it does NOT license sub-segmenting Stratum 4 around a "stable-protocol
phase" boundary as a methodological default (that would violate
[lc_era_temporal_segmentation §2](lc_era_temporal_segmentation.md#2-the-methodological-question)).
A specific Personal-register hypothesis may introduce a recent-period
sub-boundary under M1 if its predicted direction is specifically
about protocol-stabilised behaviour, but the default analytic surface
remains full Stratum 4.

This origin matters for the prior-source framing: Personal hypotheses
citing this MD are citing *trial-and-error operationalisations*, not
literature-derived ones. The prior is lived-experience-as-practice,
not lived-experience-as-belief.

---

## 3. Channels in the live protocol

The participant actively reads five signals during the day. Each has
its own threshold structure and action ladder.

### 3.1 Morning Body Battery (read at wake)

Multi-signal, not just a level read. Four sub-signals come from the
morning BB:

| sub-signal | what it tells | response |
|---|---|---|
| **Overnight gain** (`bb_overnight_gain`) | Did I recover? Did something strange happen? | If gain is absent or very small, change pacing approach for the day. |
| **Absolute level** | Where today starts in the envelope. | Mid-range (~50) is not by itself a problem; watch the drain. |
| **Carryover alertness** | If recent days drained BB below 15/20 (especially below 10/5), alertness is elevated even on a recovered morning. | Pace more aggressively today regardless of this morning's number. |
| **Felt-state divergence** | High BB + felt-bad is a recognised crash pattern; in that case the morning BB is not a useful signal. | Trust the felt state. Treat as crash mode. |

### 3.2 Daytime Body Battery — level + drain rate

Two signals from the same channel, both monitored:

**Drain rate during the day** (separate from absolute level):
- Flat / shallow drain → unalerted, plan holds.
- Steep drain → pace more aggressively (shift / shrink load).

**Level floor** (locked tier):
- **25 soft target** — aim to end the day above this.
- **20 warning** — react if approaching from above.
- **15 hard floor** — never let BB touch this; protective action mandatory.

Note divergence from Wiggers' "70-80% as pacing target" (PDF 1380-1397):
the participant's working floor is much lower and operates as a
*don't-cross* threshold, not as a *try-to-stay-above-it* target.
Wiggers' framing presumes more daytime envelope than the participant
has available; the working floor is calibrated to lived envelope.

### 3.3 Stress when at rest

The trigger is **stress elevation whilst the participant is clearly at
rest (no motion, sitting / lying down)**, NOT stress-sustained-high
alone. Sustained-high during activity is not by itself protocol-relevant;
the *mismatch* between low motion and high stress is.

Maps to Wiggers' "stuck sympathetic" / "walls of orange" framing
([Wiggers C4](../wiggers_testable_hypotheses.md#c4--stress-fails-to-drop-during-rest-periods-after-overexertion-stuck-sympathetic),
PDF 1140-1143, 1223-1231). Wiggers' framing is *post-exertion-specific*;
the participant's is *prevailing* — same signal, broader trigger window.

**Evening amplifies the signal into a different action** (see §5.3).

### 3.4 Cognitive / emotional load — "hard-and-loose" awareness budget

Not a fixed daily cap. The participant maintains a general awareness
that cognitive and emotional exertion contribute to the day's envelope
on the same axis as physical load, with three operational features:

- **Reactive downward adjustment**: if a morning interaction (e.g. a
  demanding conversation with partner / kids) was heavier than
  expected, later-day appointments may be cancelled.
- **Informal 16:00 horizon**: in general, nothing is planned after
  16:00 — felt state is too variable late-day to commit. Anything
  that is planned after 16:00 is understood by all parties to be
  cancellable last minute.
- **No fixed numerical cap** (e.g. not "one demanding meeting per
  day"). The budget is felt + observed, not counted.

Maps to Wiggers' "Activity Scale" endorsement (PDF 174-186) and to the
[per_day_intensity triage](methodology.md) `cog_load` + `emo_load`
columns — the data-side encoding of the same axis.

### 3.5 Felt state as an independent channel

Felt state (subjective how-I-feel) is read alongside Garmin, not
downstream of it. The participant's standing rule is **trust the
divergence**:

- **BB 50 + feel fine** → not a problem in itself; watch the drain
  rate during the day.
- **High BB + feel bad** → known crash pattern; BB is not a useful
  signal in this mode. Trust the bad feel.
- **Low BB + feel fine** → still elevates alertness (carryover, §3.1);
  pace as if the day's envelope were tighter.

This makes felt state the protocol's **independent ground-truth
channel**. Garmin signals are read against it; on disagreement, the
felt state often wins.

---

## 4. Channels NOT in the live protocol (research-side only)

### 4.1 Within-day RHR

The participant does **not** monitor within-day RHR live. The
[Wiggers A4 quote](../wiggers_testable_hypotheses.md#a4--sustained-multi-hour-rhr-elevation-marks-real-overexertion)
("5-10 bpm above = unhappy; 100 vs 60 for hours = thoroughly overdone",
PDF 165-177) matches the felt experience of overdoing-it *retrospectively*
— i.e. when the participant reads Wiggers' description of post-exertion
RHR elevation, it resonates with felt memory. But the participant does
not read RHR on the watch during the day.

This matters for hypothesis pre-registration: the Wiggers A4 columns
(`hr_sustained_elevated_flag`, `hr_longest_elevated_run_min_waking`,
`hr_area_above_daytime_baseline_waking`) are **research-side primitives**,
not operator signals. Personal-register hypotheses that operationalise
on A4-shaped columns are testing whether the lived-experience post-hoc
recognition has measurable substrate, not whether a live behavioural
loop exists.

### 4.2 HRV

Not available on FR245 (verified 2026-06-07; see [QUEUED-WORK §H04b](../QUEUED-WORK.md)).
Even when available via path C, HRV would be retrospective (nightly
overnight average), not actionable mid-day. Not in the live protocol.

---

## 5. Day rhythm — three checkpoints

Three structural moments where the protocol commits to a read. Reactive
glances happen on top, triggered by felt cues.

### 5.1 Morning glance

Sets the envelope for the day. Reads the four morning-BB sub-signals
(§3.1) and the felt state (§3.5). Output: a working assumption about
today's available load.

### 5.2 Late-afternoon decision check (~14:00-16:00)

**Compares observed drain rate against the morning envelope.** If drain
has been steeper than the morning envelope suggested, **evening plans
shrink**. This is the protocol's commit-or-shrink moment.

The check happens earlier than the BB number itself becomes alarming
(it's about trajectory, not level) — and crucially, it happens *before*
the 16:00 informal horizon (§3.4), so adjustments can be made while
plans are still flexible.

### 5.3 Evening rule

Evening rest-stress (§3.3) crosses from "wait it out" into **early-bed
call**. This is the only place in the protocol where the same signal
triggers a different action by time-of-day:

- Mid-day rest-stress → wait it out, dim light, hydrate, quiet.
- Evening rest-stress → bedtime moves up; today's tail is cut short.

---

## 6. Action ladder

Compact summary of which signal triggers which action.

| signal | action |
|---|---|
| Mild BB drain during day | Shift to lower-load alternative; no active rest needed. |
| Steep BB drain + low level | Active rest until BB stabilises or recovers. |
| BB approaches 20 warning | Cancel non-essential remainder of day. |
| BB at or near 15 hard floor | Protective action mandatory (active rest + early bed). |
| Stress at rest, mid-day | Wait it out: dim light, hydrate, quiet, minimal stimulation. |
| Stress at rest, evening | Move bedtime earlier; cut day's tail. |
| Morning cog/emo load heavier than expected | Cancel later-day appointments where possible. |
| Cog/emo headroom dropping mid-day | Pull the 16:00 horizon earlier; no new commitments. |
| High BB + felt-bad | Trust the felt state. Treat as crash mode; BB read is not informative. |
| Low BB + felt-fine | Trust felt state but elevate alertness (carryover); pace tighter than the felt state alone suggests. |

---

## 7. Known failure modes of the protocol's signals

### 7.1 High BB + felt-bad mismatch

Recognised crash pattern. BB is not a useful signal in this mode;
the felt state is. Wiggers names a related shape ("false energy" /
parasympathetic swing, PDF 1433-1444); the participant operates on
the divergence regardless of whether the specific Wiggers swing
mechanism applies.

### 7.2 Watch-off intervals

Any night the watch is off invalidates the morning-gain read (§3.1).
The protocol falls back to felt-state alone on those mornings.

### 7.3 Wiggers' BB floor target (70-80%) does not apply

The participant's protocol uses 25/20/15 as the working tier, not
Wiggers' 70-80%. This is a calibration difference; either Wiggers'
patient population has more envelope, or her framing as a *target*
vs the participant's as a *don't-cross* differs in kind. Personal
hypotheses citing this MD should use the participant's tier, not
Wiggers'.

### 7.4 Intervention-period baseline calibration — resolved 2026-06-14 across the autonomic-load family

The protocol's thresholds (25/20/15 BB floor, "stress at rest"
trigger level, etc.) were calibrated under the participant's
*current* physiological state. Documented interventions on this
corpus — CPAP start, citalopram start, citalopram phase transitions,
ergotherapie start — were the source of concern that the
physiological baseline shifted across these dates, invalidating the
protocol's lived calibration across boundaries.

**Resolved 2026-06-14 across the autonomic-load family.** Two
sequential analyses landed the finding:

1. **Session C** (parent MD descriptive sweep, [`intervention_effects_descriptive.md` §8](intervention_effects_descriptive.md#8-findings-session-c-run-2026-06-14))
   identified `stress_mean_sleep` × 2026-03-20 (Citalopram afbouw)
   as the mechanistically clean SSRI candidate, with `resting_hr` ×
   2022-09-22 (Ergotherapie) as a confounded second candidate.
2. **Dose-response narrow MD v3** ([`citalopram_dose_response_stress_mean_sleep.md`](citalopram_dose_response_stress_mean_sleep.md))
   confirmed via three-pronged tests (afbouw 2026 primary + buildup
   2024 post-CPAP symmetric + spring 2025 calendar control) that the
   dose-response is real, with per-channel verdicts:

| channel | verdict | magnitude (buildup post-CPAP β/mg) |
|---|---|---:|
| `stress_mean_sleep` | CONFIRMED | +0.43 (p = 0.001) |
| `all_day_stress_avg` | CONFIRMED | +0.57 (p = 0.000) |
| `bb_lowest` | CONFIRMED | −1.13 (p = 0.000) |
| `resting_hr` | weakly consistent | +0.03 (p = 0.34) |
| `bb_overnight_gain` | partial — no 2024 buildup data | — |
| `respiration_avg_sleep` | REJECTED | −0.01 (p = 0.86) |

See [`§5.6.1`](citalopram_dose_response_stress_mean_sleep.md#561-per-channel-three-pronged-read)
for the full table; [`§5.6.3`](citalopram_dose_response_stress_mean_sleep.md#563-combined-v3-verdict-super-553)
for the combined verdict.

**Operational implications for the protocol** (substantive revision
of the pre-v3 Session-C reading):

- **BB nadir threshold (25/20/15) IS dose-modulated** — superseding
  the pre-v3 "BB thresholds survive intact" reading. `bb_lowest` is
  CONFIRMED dose-responsive at ~1.13 BB-points per mg in the buildup
  phase; the same SD-normalised magnitude as the stress channels.
  Practically: at 30mg plasma steady-state the BB-nadir distribution
  sits ~25-30 BB-points lower than at 0mg plasma. The protocol's
  25/20/15 floor was lived-calibrated during the 30mg-plateau
  consolidation phase (2024-06 → 2026-03); during the afbouw (and
  potentially again post-afbouw at lower steady-state) the floor
  thresholds may need re-calibration upward. Felt-state recalibration
  by the participant continues to absorb this automatically.
- **Rest-stress trigger IS dose-modulated** — strengthened from the
  pre-v3 "may have shifted" reading. Both `stress_mean_sleep` and
  `all_day_stress_avg` are CONFIRMED dose-responsive; the latter is
  actually the strongest signal (~+0.57 stress-points per mg plasma
  in the buildup phase). The stress-with-low-motion concurrence that
  triggered an early-bed decision in 2025 (30mg plateau) maps to a
  meaningfully different absolute stress value at lower plasma
  levels.
- **Respiration rate (`respiration_avg_sleep`) is NOT dose-modulated**
  — useful negative finding. SSRI does not alter sleep respiration
  rate at this dose range on this participant. Personal-register
  hypotheses can use respiration-rate channels without inheriting
  the dose-calibration concern.
- **Resting HR is weakly dose-modulated** — direction matches the
  HRV-reduction prior (higher dose → mildly higher RHR) but the
  buildup CI brushes zero. The protocol does not use absolute RHR
  as a trigger anyway, so this is a research-side caveat rather
  than an operational one.
- **The pre-2024 interventions (Ergotherapie 2022) sit before the
  buildup window** and are not directly testable by the v3 design;
  the LC-trajectory confound at 2022-09-22 (parent MD §8.3) remains
  the most likely explanation for the `resting_hr` step there. The
  protocol's lived calibration is not retroactively invalidated for
  those eras, but a separate ITS-style design would be needed to
  formally test.

**For Personal-register hypotheses (P4a, P4b, P5b, P6, P7) and
Wiggers C4b**: each carries a per-channel-quantified caveat now.
The pre-v3 reading "only P5b and C4b inherit sharply" has been
**substantively revised**: P4a (BB-floor crossing) now inherits the
caveat as load-bearingly as P5b (stress-trigger) does, because
`bb_lowest` joined the confirmed-channel set. P5b and C4b inherit
both the `stress_mean_sleep` AND `all_day_stress_avg` confirmations
(jointly, since both channels enter their predictors). P6
(post-crash recovery shape) inherits on three channels rather than
one.

This is the *physiological-state* sibling of the §2
*behavioural-practice* temporal qualifier; the two qualifiers
interact at the 2026-03-20 boundary specifically (the behavioural
protocol stabilised over recent months *while* the physiological
baseline for the autonomic-load family was shifting from SSRI
withdrawal). The quantified per-channel magnitudes from
[`citalopram_dose_response §5.6.1`](citalopram_dose_response_stress_mean_sleep.md#561-per-channel-three-pronged-read)
turn this from "qualifier known" to "qualifier corrected" — downstream
analyses can apply a per-mg-plasma dose-adjustment offset to the
affected channels instead of treating the calibration as an
unresolvable confound.

---

## 8. Where this maps to existing research artefacts

Forward pointers to existing research-side work that touches the same
signals. Not interpretation — just pointers.

| protocol element (this MD) | research-side artefact |
|---|---|
| §3.1 Morning BB sub-signals | `bb_overnight_gain` column ([DATA_DICTIONARY.md](../DATA_DICTIONARY.md)); [HA10](../analyses/hypotheses/HA10-bb-overnight-recharge/) (validate-era SUPPORTED); [H03b](../analyses/hypotheses/H03b-bb-overnight-recharge-permin/) gated on H04b path C |
| §3.2 Daytime BB drain rate + tiered floor | per-minute BB columns blocked on [H04b path C](../QUEUED-WORK.md#h04b-path-c-authorisation--highest-leverage-next-step); [CONVENTIONS §3.5](../CONVENTIONS.md#35-spike-detecting-metrics-over-daily-averages) (BB-rise count as meaningful) |
| §3.3 Stress at rest | [HA11 within-day stress U-dip](../analyses/hypotheses/HA11-stress-udip/) (train-SUPPORTED); [Wiggers C4](../wiggers_testable_hypotheses.md#c4--stress-fails-to-drop-during-rest-periods-after-overexertion-stuck-sympathetic) (overlapping but narrower trigger window) |
| §3.4 Cog/emo budget | `per_day_intensity.csv` `cog_load` + `emo_load` ([methodology.md](methodology.md)); Wiggers Activity Scale endorsement (PDF 174-186) |
| §3.5 Felt-state divergence | `gevoelscore` ↔ Garmin channel-divergence work; [P1](../personal_hypotheses.md#p1-sleep-window-stress-is-elevated-on-crash-episodes) sleep-stress + crash framing |
| §4.1 Within-day RHR (research-side only) | [Wiggers A4](../wiggers_testable_hypotheses.md#a4--sustained-multi-hour-rhr-elevation-marks-real-overexertion); `hr_sustained_elevated_flag`, `hr_longest_elevated_run_min_waking`, `hr_area_above_daytime_baseline_waking` columns |
| §5.2 Late-afternoon decision check (~14:00-16:00) | No existing artefact; candidate for a time-of-day-stratified descriptive primitive |
| §5.3 Evening rule | No existing artefact; candidate for a time-of-day-amplified rest-stress primitive (would underwrite a future Personal P5) |

---

## 9. How Personal-register hypotheses should cite this MD

Use the project's `[[name]]` linking convention:

> *Prior sources: (1) Lived experience — [[lived_experience_garmin_pacing_2026-06-14.md §<section>]]; (2) Operational protocol — [[methodology/garmin_pacing_practice.md §<section>]]; (3) [literature, where applicable]; (4) Mechanism, where applicable.*

The operational-protocol citation establishes that the participant
*acts on* the signal pattern in daily life, predating any analysis on
the corpus. This is a stronger prior than belief alone — it is
behaviour, recorded in this MD before the test ran.

---

## 10. Open questions deferred

- **Late-afternoon check threshold** (§5.2): what exactly counts as
  "drain steeper than morning envelope"? Currently judgement-based;
  could be operationalised as a research-side primitive (drain rate
  vs morning baseline).
- **Evening time-of-day boundary** (§5.3): when does "evening" begin
  for the bedtime-call rule — strict clock time, light-level cue,
  or felt-state cue? Currently felt.
- **Wiggers BB-floor calibration** (§7.3): is the 70-80% vs 25/20/15
  divergence about population, framing-as-target-vs-floor, or
  measurement era? Worth a footnote in any future Wiggers-aligned
  pre-reg that uses Wiggers' number.

These are not gaps blocking use of the MD as a prior source; they are
items to surface to a future researcher considering operationalising
the protocol into a test.

---

## 11. Cross-references

- [lived_experience_garmin_pacing_2026-06-14.md](../lived_experience_garmin_pacing_2026-06-14.md) — primary-source braindump this MD draws from
- [personal_hypotheses.md](../personal_hypotheses.md) — where hypotheses citing this MD live
- [wiggers_testable_hypotheses.md](../wiggers_testable_hypotheses.md) — Wiggers' claims as testable hypotheses; cross-referenced for vocabulary
- [CONVENTIONS.md](../CONVENTIONS.md) §4.1 (no interpretive marks), §4.3 (prior-driven confirmatory)
- [methodology.md](methodology.md) — research methodology umbrella, including per_day_intensity triage
- [garmin_indicators_audit.md](garmin_indicators_audit.md) — per-Garmin-column provenance
- [QUEUED-WORK.md](../QUEUED-WORK.md) — H04b path C (unblocks per-minute BB for §3.2), C.4 + C.5 (efficacy descriptive work)
