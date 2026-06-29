# Companion stock-take session — ideas & conclusions

*Recorded 2026-06-28. A reviewer-mode synthesis + ideas note produced
in a "take stock" companion session between the participant and Claude.
It **summarises conclusions already established** in the project's
result/synthesis docs and **proposes new analysis directions** — it does
**not** report any new test run in this session. Established findings are
cited to their source docs; proposed work is flagged as proposed.*

*Sister to [personal_hypotheses.md](personal_hypotheses.md) (the
hypotheses themselves) and the formal
[STOCKTAKE.md](STOCKTAKE.md) (the programme-status ledger). This is a
lighter session-level capture, not a replacement for either.*

## Authorship

- **Drafted by**: Claude (reviewer-mode, drafting under explicit user
  request to "save the ideas and conclusions of this conversation").
- **Authorising user**: repository owner.
- **Date**: 2026-06-28.
- **Status**: not a locked artefact. Ideas here are candidate directions;
  any that become analyses follow the normal CONVENTIONS §2.2 → §6 gate.

## Privacy note

Two lived examples discussed in session are abstracted here per the
[README §6](README.md#6-privacy-boundary) privacy boundary (no person
names, no identifying specifics): "office-commute day" = a day with a
long (~45 min each-way) drive plus sustained in-person social/cognitive
load; "high-emotional-load session" = a recurring 1:1 session with high
emotional load. No raw note text or names are reproduced.

---

## 1. Why this note exists

A foundation-complete checkpoint: the descriptive programme is closed,
~25 hypotheses are tested, the methodology scaffold is locked, and five
new literature reviews just landed in
[literature/reviews/](literature/reviews/). This note captures what we
*concluded* reading across all of it, and the *ideas* worth pursuing
next, so the thread isn't lost.

---

## 2. Conclusions drawn this session

### 2.1 The personal corpus independently reproduces the field's central gap

The five-review
[SYNTHESIS](literature/reviews/SYNTHESIS_wearables_autonomic_PEM_research_programme.md)
argues the whole field is stalled on one missing keystone: **no
validated, time-stamped, free-living PEM label**, so detection,
prediction, and wearable-guided pacing all run aground. Two of its
through-lines — *"descriptive is strong, predictive is empty"* and *"the
loop is never closed because the label is missing"* — are exactly what
this n=1 corpus shows from the inside:

- daily-aggregate precursors are closed (H01–H04 refuted both eras),
- the real signal is shape-not-linear and lives **below** daily
  resolution (bout-level / event-matched), and
- a forward alarm would fire at ~4% PPV at the current ~2-crash/year
  base rate.

**Conclusion:** the project is not "just personal" — it is a working
existence-proof of the field's keystone problem, reached independently
with consumer hardware.

### 2.2 The recovery story is real and multi-dimensional — but watch the trajectory confound

Independent axes converge on measurable, multi-dimensional improvement:
crash frequency (~10/yr → ~2/yr), stress baseline (~halved), peak
stress-spike duration (~13 → ~6 min), worst-tail days (score ≤3 down
~65%), upper mode (score 6 up ~6×), long-tail crash episodes (5 → 1).
No single axis clears the strict pre-registration bar alone; the
**convergence of 7–11 non-contradicting axes** is the stronger evidence.

Caveats (reviewer-mode, kept honest):
- the axes are **not independent**, and several are entangled with the
  recovery trajectory they describe (CONVENTIONS §3.7 detrend discipline
  already caught two "event" steps that were trajectory leaking through);
- citalopram / pacing-skill / time are mutually confounded — the 2024-04
  intervention cluster is structurally unanalysable (§3.8);
- almost everything "supported" is **train-era only**; the single
  both-eras-supported test is HA07d.

### 2.3 The phenotype shifted — "the kind of crash changed"

Early crashes (2022–23) carried strong sympathetic-load precursors and
long tails; residual crashes (2024+) are fewer, shallower, shorter, more
physical-symptom-flavoured, more embedded in functional/mixed days. The
mechanism is **inverted-U / threshold, not monotone-convex** (Wiggers'
convex-cost claim was refuted; HA-C3 found concave). This phenotype
shift is the corpus's most original contribution — the literature
doesn't describe it because nobody else has a continuous multi-year
recovery arc at this resolution.

### 2.4 Garmin signal: a good thermometer, a poor barometer

Garmin carries real **state / descriptive** signal and essentially no
usable **predictive** signal at daily resolution:

- **Strong state signal**: citalopram dose-response (3 CONFIRMED-modulated
  channels; the citalopram-start boundary rp5 is the strongest empirical
  boundary in the corpus); crash-state autonomic elevation (28/29 crashes
  in the matched-episode window); the macro recovery arc.
- **Empty / misleading for prediction**: daily-aggregate precursors dead
  (H01–H04); the strong train-era precursors did not transfer; ~4% PPV
  as a forward alarm; felt-state↔Garmin ≈ independent at daily resolution.
- **Resolution point**: the signal is real but lives below the day, in
  spikes/bouts/event windows — which is precisely why the event-anchored
  cut (§3.2 below) is well-motivated.
- **Hardware honesty**: the FR245 gives a black-box HRV-derived "stress"
  proxy, not validated HRV Status — the channel the literature most wants
  is the one least captured. `resting_hr` is signal-rich but
  trajectory-poisoned (carries the multi-year arc; treat with suspicion).

### 2.5 HA07d is the durable result — with its claim sized correctly

[HA07d](analyses/hypotheses/HA07d-sleep-stress-variability/result.md) —
night-over-night change in the **standard deviation** of in-sleep-window
stress (an "HRV-of-HRV-proxy"), z-scored against a lagged baseline — is
the project's **first and only both-eras-SUPPORTED** crash-precursor test
(train 84.6% / +19.6 pp; validate 86.7% / +21.7 pp, on `crash_v1`).

The deep finding is **one construct, two regimes, opposite sign**:
overnight autonomic *flexibility* is disrupted before crashes in both
eras, but the disruption flips — *volatile* before early crashes,
*frozen-flat* ("autonomic stillness") before late ones. The validate-era
"freeze" is cross-channel coherent (HA10 elevated overnight body-battery
+ HA07d collapsed variability): **the body's dashboard reads like
recovery in the days before a late-era crash, and the crash comes
anyway.** This matches the Wiggers lived-experience "freeze" framing.

Why durable: the channel has the shortest autocorrelation memory (~7-day
reset), so it survived both detrend and single-pool recompute where
trajectory-heavy channels wobble.

Claim sized honestly (push hardest where the claim is strongest):
- tiny n (~13–15 episodes/era);
- 65% null base rate — real discrimination, but the trigger is common,
  so it is a **descriptive precursor, not a deployable alarm** (fully
  consistent with the ~4% PPV conclusion);
- proxy / second-order / sleep-architecture confound;
- on `crash_v1` — **not yet re-run on crash_v2 or bout-level** (the
  single most obvious missing validation);
- "transfers across eras" is true at the **construct** level, not the
  **rule** level (direction flips → no single deployable threshold).

*Correction banked this session:* HA07d (the crash-precursor test) and
the `stress_stdev_sleep × gevoelscore` detrend-robustness check (Q4.5.b)
are **two distinct supports for the same channel**, not one finding.

---

## 3. Ideas proposed this session (candidate directions — none run yet)

### 3.1 Zoom on the unregulated / learning-to-pace window

Characterise the body **before pacing + the first weeks learning to
pace** — `lc_pre_ergo` + early `pacing_4a` (~late Sept → 2026-11-17,
~8 weeks). Conceptual value: the **physiology is still in full PAIS
development while behaviour is only just starting to change**, so it
comes close to isolating "what the unregulated body does on its own."

Honest constraints:
- coverage asymmetry — Garmin full from 2021-08-16; gevoelscore only from
  2022-09-03; notes only from 2022-10-18; the acute April–Aug 2022 months
  are Garmin-only;
- short n (lc_pre_ergo ~19 logged days, 4a ~56) → descriptive only;
- "unregulated" (behaviourally, 2022) and "peak autonomic signal"
  (Garmin amplitude peaks ~mid-2023) do **not** coincide — dysregulation
  appears to keep *building* through the first year; pacing was learned
  mid-storm, not as a calming switch (pacing_4b actually had the highest
  event rate).

**Work-reintegration as the defining context.** A graded return-to-work
is structurally a graded-*increase* protocol — the opposite of pacing.
So this window is a personal natural experiment in the field's central
**GET-vs-pacing** tension (R4 / PACE / NICE), with the participant caught
in the middle, untreated and still dysregulating. The PwC
`reintegration_hours` log is a clean daily-computed exertion channel
(unlike the presence-conditioned soft channels) and has not yet been
integrated into this window's descriptive picture — a genuine addition.

Suggested sharpest cut: **does the body show the learning?** Track
push/exertion spikiness declining across the 8 weeks while crashes and
the stress-spike precursor still fire in the background — behaviour
moving while physiology lags.

### 3.2 Documented high-load event pool (event-anchored load study)

Pool documented high-load events, typed and severity-ranked by the
participant's **own self-scored physical / mental / emotional load**
(the `per_day_intensity` triad), then read the body's response in the
delayed-PEM window (8–72 h) around each, against matched control days
(reuse HA-P6 Arm-A/Arm-B machinery; Q4.9 window design).

Why it fits this corpus:
- it operates at the **resolution where Garmin carries signal** (event
  windows + spike metrics), not the daily aggregate where it cancels;
- the load triad is **presence-conditioned** (§4.4) — a liability for
  trajectory work, but an event-anchored design *conditions on presence
  by construction*, so the limitation is neutralised here;
- it lets us separate **pure** events (high on one axis, low on others)
  from **composites** (e.g. office-commute day = physical + mental +
  social at once), giving the cleanest available read on whether
  **emotional load drives a distinct autonomic signature / lag** — the
  open question HA-C4b left standing;
- a multi-year self-scored *emotional*-load channel is rare data; the
  field studies PEM provocation mostly as physical exertion.

**The longitudinal gem:** recurring event types (office-commute days,
recurring high-emotional-load sessions) are a roughly fixed stimulus
probed repeatedly across the recovery arc. *Same stimulus, shrinking
response* would be one of the cleanest readouts of regulation forming —
holding the stimulus constant sidesteps much of the trajectory confound.

Honest constraints: small n per bucket; documentation/salience bias;
self-score scale-drift across years (affects event *selection*, less so
the objective Garmin *response*); matched controls essential; same-day
load↔felt-state entanglement (read the *following* window, not the event
day).

**Open forks left unresolved this session:**
1. **Scope** — unregulated-4a portrait, or whole-corpus longitudinal
   (same-load-type response over recovery)? The second is more original.
2. **Anchor channel** — settled: the self-scored three-axis load triad.

### 3.3 HA07d follow-ups

- **Re-run on crash_v2 / bout-level** — cheapest, highest-value
  confirmation; hardens or qualifies the durable claim.
- **Variability, not level, in the event pool** — HA07d says the
  informative overnight primitive is *variability*; watch the night
  *after* a high-load event for volatility vs the "freeze," by load axis.
- **"Freeze detector" (HA09)** — can elevated overnight BB **and**
  collapsed sleep-stress variability be jointly detected as one "freeze
  night" and used to forecast next-day dysregulation? HA10 + HA07d make
  it defensible.

### 3.4 Night-stress as a fatigue-severity predictor (Visible-style)

Prompted by the Visible app's claim that **morning HRV predicts fatigue
severity**. Our nearest construct: overnight Garmin "stress" (HRV-derived
during sleep, so directionally the inverse of HRV) vs next-day
`gevoelscore`. Differences to keep in mind: ours is a whole-night
aggregate, not a morning spot reading; "severity" = gevoelscore; n=1.

What we already see (no clean test of this exact framing yet):
- **Night-stress *level* (mean): not a predictor** — HA07c (sleep-stress
  mean delta) refuted both eras; same-day stress↔gevoelscore ≈ 0 (S02
  −0.06). The level — the closest analogue to a single HRV number — does
  not track fatigue here.
- **Night-stress *variability*: real but wrong-shaped** — HA07d (overnight
  stress stdev) is a both-eras crash precursor, and
  `stress_stdev_sleep × gevoelscore` is weak but detrend-robust (ρ ≈
  −0.12). But that predicts crashes (binary), not continuous severity,
  and even there is descriptive-not-deployable.
- So the informative primitive is **variability, not level** — a
  *divergence* from Visible's level-based HRV score, not a confirmation.

The gap: the **wearables-lead-score** direction (last night → next-day
felt-state) is on the pending list and never tested as a continuous
predictor. The one daily-resolution lead/lag test we ran (S02b,
score-leads-Garmin) was refuted — a prior against a strong link, not a
result. Field caution: the one direct PEM-prediction-from-HR/HRV attempt
failed (Boruch 2021); HRV is under-validated in disease populations (R1).

Proposed test (cheap, well-motivated): regress `gevoelscore[d]` on
`night_stress_mean[d]`, `night_stress_stdev[d]`, and their night-over-
night deltas, with lagged baseline + §3.7 detrend sensitivity + §3.4
crash-drop row, and a **same-day vs next-day contrast** to separate
concurrent from predictive. Directly answers the Visible-style claim on
this corpus and doubles as the pending wearables-lead-score test.

---

## 4. Cross-references

- [literature/reviews/SYNTHESIS_wearables_autonomic_PEM_research_programme.md](literature/reviews/SYNTHESIS_wearables_autonomic_PEM_research_programme.md)
- [analyses/hypotheses/HA07d-sleep-stress-variability/](analyses/hypotheses/HA07d-sleep-stress-variability/)
- [STOCKTAKE.md](STOCKTAKE.md), [personal_hypotheses.md](personal_hypotheses.md), [REJECTED.md](REJECTED.md)
- [CONVENTIONS.md](CONVENTIONS.md) §3.4–§3.9 (audit hooks), §4.3 (prior-driven), §4.4 (presence-conditioned)
- [lived_experience_garmin_pacing_2026-06-14.md](lived_experience_garmin_pacing_2026-06-14.md)
