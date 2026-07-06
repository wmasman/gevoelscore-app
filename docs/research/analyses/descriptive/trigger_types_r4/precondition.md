# Descriptive precondition -- R4 trigger types (physical / emotional / cognitive), and the autonomic fingerprints of load

**Status**: producer-mode descriptive precondition, Layer-1 descriptive per
[CONVENTIONS section 4.1](../../../CONVENTIONS.md). Two roles in one document:

1. **The R4 precondition.** Characterises the self-reported trigger data (what
   exists, how sparse, how it sits around crashes) so the site request **R4**
   ("what share of crashes are physically vs emotionally / cognitively
   triggered") can be scoped honestly, or honestly declined.
2. **A data-description finding in its own right.** A cross-modal check: does
   each self-reported load type leave a distinct *autonomic fingerprint* in the
   Garmin channels? (Physical in cardiac / activity, emotional in
   stress / battery, cognitive in ... ?)

Drafted 2026-07-04 by Claude (Opus 4.8) under producer-mode authorization, for
the participant-researcher (repo owner). All numbers are reproduced by
[`precondition_analysis.py`](precondition_analysis.py) (seed 20260704, only the
bootstrap CIs use it). No inferential verdict is locked here; this is descriptive
groundwork.

> "stress" = Garmin HRV-derived Stress Score (GSS), never mental / emotional
> stress. "physical load / exertion" = bodily activity load, distinct from the
> emotional and cognitive load categories below.

---

## 1. The R4 question and why it needs a precondition

R4 asks for a share: of the crashes, how many were physically triggered vs
emotionally / cognitively triggered. Before any such share can be computed, three
basics must be settled: (a) do we even have trigger data, and how sparse; (b) is
whatever we have *specific* to crashes, or just ambient; (c) can the wearable
corroborate any of it. This document settles all three. The register logged R4 as
`weak` on the assumption of ~35% note-day fill; that assumption is revisited in
section 3.

## 2. The trigger data: three layers

Per [DATA_DICTIONARY.md](../../../DATA_DICTIONARY.md) sections 2 and 9, three
distinct sources carry trigger-type signal, all **presence-conditioned** (a value
appears only when the thing was recorded; absence is not the same as "did not
happen"):

- **Section 2 -- manual load triage (the 1-3 scores).** `phy_load`, `emo_load`,
  `cog_load`, each **1 / 2 / 3 = mild / moderate / severe event intensity**,
  built from calendar events plus day-notes
  (`processed/manual_triage/per_day_intensity.csv`). Gated on
  **`has_intensity_triage`** (`intensity_source != ""`). This is the structured
  trigger signal R4 wants.
- **Section 9 -- note categorisation rollup.** `cat_belasting_{fysiek,
  emotioneel, cognitief, gezin, sociaal}` (clause counts), plus
  `cat_triggers_extern` (corona / griep / infectie). Note-derived, gated on
  `has_note`. A **broader** load taxonomy (adds family and social load) but a
  sparser, count-not-intensity layer.
- **`cat_triggers_extern`** singles out the one *external* trigger class
  (infection), which behaves very differently from the internal loads (section 4).

**The presence-conditioning is load-bearing.** A blank `emo_load` on a reviewed
day means "no emotional-load event noted," not "missing." That distinction is only
usable because the triage turns out to be near-complete (section 3).

## 3. Coverage: we have the data (the register's `weak` was too pessimistic)

On the LC corpus (**1372 gevoelscore days, 2022-09-03 onward**; named per
[CONVENTIONS section 3.6](../../../CONVENTIONS.md)):

| Section-2 load (1-3) | days with an event | of LC corpus |
|---|---|---|
| `cog_load` | 351 | 25.6% |
| `phy_load` | 272 | 19.8% |
| `emo_load` | 165 | 12.0% |

The event-rate looks low, but the decisive number is that
**`has_intensity_triage` = 100%** (all 1372 LC days reviewed): **149** carry the
explicit `_no_info` "reviewed, no signal" marker, **1223** are context-sufficient.
So a blank load on a reviewed day is a genuine "no such event," not a gap. The
Section-9 note layer (`cat_belasting_*`, `cat_triggers_extern`) covers **686 /
1372 = 50.0%**. Intensity, when present, skews moderate-to-severe (`phy` L1:74 /
L2:93 / L3:105; `cog` L1:33 / L2:163 / L3:155; `emo` L1:47 / L2:53 / L3:65).

**Peri-crash (the number that matters for R4).** Over the **29 crash episodes**,
run-up window [nadir-5 .. nadir]: **100% of run-ups are context-reviewed**, and
**83% (24/29) carry at least one structured load event**; the remaining **5/29
were reviewed and had none** (a real "no identifiable structured trigger," not
missing data). So coverage is **not** the blocker. The register can move R4 off
"not enough data."

## 4. The load-bearing finding: presence-based triggers are NOT crash-specific

Coverage is adequate, but a raw "N% of crashes were physically / emotionally /
cognitively triggered" share is **degenerate**, for the same reason the push-crash
binary exposure was
([`../post_crash_exertion_relapse/precondition.md`](../post_crash_exertion_relapse/precondition.md)
section 3.1): the loads are near-ubiquitous, so their presence in a crash run-up
is almost entirely base rate.

| trigger | crash run-up rate | random-window base rate | elevation |
|---|---|---|---|
| physical | 69% | 65% | +4pp |
| emotional | 55% | 48% | +7pp |
| cognitive | 76% | 74% | +2pp |
| **infection (extern)** | **7%** | **2%** | **+5pp (~3.5x)** |

(Random-window = any [t-5..t] window on the LC corpus.) The internal loads are so
common that a 6-day window contains one 48-74% of the time regardless of a crash;
the crash elevation is +2 to +7pp, near-certainly noise at n=29. And the
"cognitive dominates" impression is an artefact of differential base rates (cog is
simply most common everywhere). **So the honest verdict: a presence-based
crash-trigger share is not defensible.** This is itself a finding, and it
**strengthens site request R32(a)** ("no visible trigger-into-crash signal"):
even the self-report load data does not distinguish crash run-ups from ordinary
weeks.

**The one exception is infection** (`cat_triggers_extern`): rare (0.3% of days)
but ~3.5x elevated in crash run-ups (7% vs 2%). Real specificity, but ~2 crashes
-- a tiny-n signal, reportable only as such.

The remaining hope for an *internal*-load answer is **intensity**, not presence:
do *severe* (level-3) loads elevate before crashes even though presence does not?
That is the natural R4 analysis (section 7), out of scope for this precondition.

## 5. The autonomic fingerprints of load (the data-description finding)

Separate question, and interesting on its own: for each self-reported load type,
what do the Garmin channels do on load days, in personal-baseline units (lagged-
lcera ranks 0-1 or z-scores)? This is a **cross-modal validity check** and, for
emotional and cognitive load, a **non-circular** one (those loads are tagged from
notes / calendar, not from the wearable, so agreement is genuine corroboration;
physical-load-vs-activity is partly circular since a logged workout tags both).

### 5.1 The good-day confound (why the isolated read is the honest one)

Physical- and cognitive-load days are **better-felt** days (mean gevoelscore
delta **+0.29** physical, **+0.24** cognitive), because you do physical and
cognitive things when you have capacity. Emotional load carries **no** felt-state
gradient (**+0.02**; isolated of physical, **-0.16**) -- it happens regardless of
state. Because the loads co-occur (only 41 phy-only, 32 emo-only, 83 cog-only vs
271 multi-load days), that good-day effect leaks across the marginal comparisons.
The honest read therefore **isolates** each load (removes co-occurring physical)
and **partials out felt-state** (residualises each channel on gevoelscore). Both
are in the table below; `*` = 95% bootstrap CI excludes 0.

### 5.2 The fingerprints (isolated where noted, felt-state-adjusted)

| load | cardiac / activity | daytime GSS | overnight sleep autonomics |
|---|---|---|---|
| **Physical** (present vs absent) | `max_hr_rank` **+0.06\*** and `eff_exertion` **+0.05\*** (both survive adj) | +0.09 ns | `bb_lowest` **-0.21\***, `resting_hr` **-0.20\*** (survive adj; activity depletion). `sleep_stress` raw -0.34\* was mostly the good-day confound (adj -0.16, ns) |
| **Cognitive** (isolated) | ns | ns | ns |
| **Emotional** (isolated) | **+0.02 ns** (invisible in HR) | **+0.35\*** (survives adj) | `bb_lowest` **-0.43\*** (survives adj); `sleep_stress` +0.16 adj (suggestive, CI spans 0); `resting_hr` ns |

### 5.3 Three headlines

- **Physical load is visible, modestly, in the activity / cardiac channels** and
  in overnight battery depletion, robust to felt-state. The self-reported
  physical-load event and Garmin activity are only *loosely* coupled (deltas ~0.05
  rank points), echoing the "how they walk, not how much" theme.
- **Cognitive load is essentially Garmin-invisible** once isolated: every channel's
  CI spans 0. A severe-only daytime-stress blip did not survive removing the
  physical co-occurrence. "Cognitive maybe" resolves to "mostly no."
- **Emotional load is the striking, non-circular keeper.** It is **flat in heart
  rate** (+0.02, ns) yet **robustly elevated in daytime GSS (+0.35\*) and lowered
  in the body-battery floor (-0.43\*)**, both surviving felt-state adjustment;
  sleep-stress is suggestive (+0.16, CI spans 0). So the watch *does* see emotional
  load -- the load a step-counter would miss -- but in the autonomic
  stress / battery channels, not in HR. This nuances "the watch can't see mental
  PEM": it cannot see it in heart rate, but emotional load surfaces in the
  autonomic channels.

An honesty correction carried from the drafting: an earlier point-estimate read
oversold "emotional -> sleep-stress +0.34." With bootstrap CIs and felt-state
adjustment that same-day channel is only suggestive (+0.16, CI spans 0); the
robust emotional autonomic signals same-day are daytime GSS and the battery floor.
The sleep-stress channel does reach significance on the FOLLOWING night, which is
exactly the timing Wiggers describes; see section 5.4.

### 5.4 The Wiggers timing test ("HRV drops that night or the following night")

Wiggers' handleiding makes a specific, testable concession (the mental-PEM
passage, PDF lines 1448-1457): *"Too much mental activity, such as working on your
laptop or writing, often goes undetected in your Garmin, but excessive mental
activity can still cause PEM. It will also cause your HRV to drop that night or the
following night."* Overnight stress (GSS) is the HRV-derived proxy (higher stress
= lower HRV), so this is directly testable at lag 0 (that night) and lag +1 (the
following night). Isolated + bootstrap CIs; `*` = CI excludes 0.

| load | overnight channel | that night (lag+0) | following night (lag+1) |
|---|---|---|---|
| **cognitive** (her own laptop/writing example) | sleep-stress | -0.10 ns | -0.09 ns |
| cognitive **severe L3** ("excessive mental activity") | sleep-stress | -0.24 ns | -0.15 ns |
| **emotional** | sleep-stress | +0.27 ns | **+0.53\*** |
| emotional | battery floor | **-0.42\*** | **-0.42\*** |

Two clean reads:

- **For cognitive load, Wiggers' claim fails in this body.** Her own example
  (laptop, writing) produces **no overnight HRV drop on either night, even at
  severe intensity** -- the point estimates are if anything in the wrong direction
  (slightly lower stress). So the watch misses not just the *activity* of cognitive
  overexertion but its *autonomic aftermath* too. The watch is blinder to cognitive
  load than the guide expects.
- **For emotional load, Wiggers' claim holds, with her exact timing.** The overnight
  HRV drop (sleep-stress up) is suggestive that night (+0.27) and **significant the
  following night (+0.53\*)**, and the body-battery floor is robustly down both
  nights. Wiggers' "that night *or the following night*" hedge captures a real lag:
  the emotional-load autonomic aftermath peaks on the second night.

So the guide's mechanism (non-physical load -> overnight HRV drop) is **confirmed
for emotional load with the exact timing Wiggers states, and refuted for cognitive
load** -- a refinement of a taxonomy the guide lumps together as "mental activity."

## 6. What R4 can and cannot deliver

- **Cannot**: a defensible presence-based "X% physical vs Y% emotional vs Z%
  cognitive" crash-trigger share (section 4: degenerate, base-rate-dominated).
- **Can, honestly**:
  1. an **intensity-graded, base-rate-referenced** descriptive (do *severe* loads
     elevate in crash run-ups vs matched baseline; wide error at n=29);
  2. the **infection-trigger fraction** (small but the one specific signal);
  3. the **autonomic-fingerprint cross-validation** (section 5) as a standalone
     data-description / beyond-the-guide candidate;
  4. the **stated finding** that presence-based internal-load triggers are
     crash-non-specific (feeds R32(a)).

The honest R4 output is a note plus these bounded reads, not a pie chart --
consistent with the register's "we can raise this, not resolve it," now backed by
measurement.

## 7. Further measurement passes (recommended, with reasoning)

1. **Intensity-graded crash-specificity (highest value).** Presence is degenerate;
   test whether *level-3* loads elevate in crash run-ups against a matched
   ordinary-window baseline. This is the R4 analysis proper; it belongs in a
   follow-up, not this precondition.
2. **Graded dose-CIs on the concordance (medium).** Confirm L1 < L2 < L3 for the
   robust fingerprint channels (emotional battery-floor, physical cardiac). Small
   per-level n (emo L3 = 65) will give wide bands; report them.
3. **gezin / sociaal loads + infection peri-crash (completeness).** Fold the
   Section-9 family / social load and the infection signal into the inventory; they
   are note-count, not 1-3 intensity, so lower-resolution.
4. **Next-day / lead-lag sleep alignment (lowest load-bearing value).**
   `stress_mean_sleep[d]` is the sleep *starting* on day d
   (`methodology/nightly_attribution.md`), i.e. already **the night after** the
   load day -- which is why the emotional signal appears there at all. A next-day
   (d+1) pass therefore only tests **persistence into a second night**, secondary.
   The more useful variant is a **lead-lag directionality** check (load[d] ->
   sleep[d] vs sleep[d-1] -> load[d]), because the concordance's main weakness is
   reverse causation (did a stressful day disturb sleep, or did bad sleep produce a
   fragile day logged as emotional load?). An n=1 correlational lead-lag cannot
   fully resolve direction, so this is a caveat to state rather than a pass that
   settles anything.

## 8. Caveats

- **Presence-conditioned, n=1, same-day concordance.** Section 5 is association,
  not causation; the loads are self-reported and partly note-derived.
- **The good-day confound is real** for physical / cognitive load (gevoelscore
  +0.29 / +0.24); the isolated + felt-state-adjusted reads are the defensible ones,
  and even those are day-level bootstrap CIs (**autocorrelation not modelled, so
  the bands are approximate / optimistic**).
- **Small isolated cells** (emo-only 32; emo-isolated concordance n=71; per-level
  n as low as 33-65). Treat every fingerprint as suggestive-not-established.
- **Physical-load-vs-activity is partly circular** (a logged workout tags both);
  emotional / cognitive concordance is non-circular.
- **Reverse causation** (section 7.4) is unresolved for the sleep channels.
- **No interpretive / causal marks** (CONVENTIONS section 4.1): the claim is "load type X
  co-occurred with channel Y in this subject," never "X caused Y."

## 9. Cross-references

- Site register R4 (trigger type), R32 (no visible trigger-into-crash signal), R33
  (compensatory rest / load response): the site's `docs/research-requests.md`
  (external repo `wiggers_research_story`, sibling of this one under the same
  parent directory).
- Sibling degenerate-exposure precondition:
  [`../post_crash_exertion_relapse/precondition.md`](../post_crash_exertion_relapse/precondition.md)
  section 3.1.
- Data semantics: [DATA_DICTIONARY.md](../../../DATA_DICTIONARY.md) section 2
  (manual load triage, `has_intensity_triage`), section 9 (note rollup,
  `cat_belasting_*`, `cat_triggers_extern`); the presence-conditioned rate-
  comparability caveat (section 2 preamble).
- Autonomic channels: `methodology/intervention_effects_descriptive.md` (sleep
  channels as validated autonomic indicators), `methodology/nightly_attribution.md`
  (sleep-night attribution, relevant to section 7.4).
- Analysis: [`precondition_analysis.py`](precondition_analysis.py) (reproduces every
  number here).
- CONVENTIONS section 3.2 (lagged-lcera baseline), section 3.6 (named counts), section 4.1 (no
  interpretive marks).

## Authorship

| Field | Value |
|---|---|
| Drafted by | Claude (Opus 4.8) under producer-mode authorization, for the participant-researcher (repo owner) |
| Date | 2026-07-04 |
| Discipline | Descriptive-only (no locked inferential verdict); no interpretive marks (section 4.1); stress = Garmin GSS; presence-conditioned semantics honoured. |
