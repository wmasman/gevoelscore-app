# S02c — May 2026 channel divergence: notes

**Status: descriptive characterisation completed. The May 2026
"perturbation" identified by S02 T2 is much smaller against the
recent 180-day daily reference window than against S01's 5-year
trajectory-level σ. Only RHR shows any algorithmic onset; no
"visibly worsening" reading by the locked 1.0σ rule. The score is
also "essentially unmoved" against the recent reference,
re-framing the "all-time high" interpretation from S02.**

Spec at [hypothesis.md](hypothesis.md). Script at
[compute_divergence.py](compute_divergence.py). CSVs at
[channel_summary.csv](channel_summary.csv) and
[channel_pair_correlations.csv](channel_pair_correlations.csv).
Plot at [divergence_plot.png](divergence_plot.png). Execution log at
[execution-log.txt](execution-log.txt). Run 2026-06-07.

## Headline

**Composite Garmin-worsen z minus score-z over the perturbation
window = +0.324 σ (mean of 83 perturbation days).**

The "channel divergence" claim from S02 T2 stands directionally —
the Garmin composite is positive (slight worsening tilt) while
score is also positive (slight improvement tilt). But the
**magnitude is small**: a 0.32σ separation across the 90-day
window. Under the locked §3.7 reading rules, neither side reaches
"visibly worsening" / "visibly improving."

This is a substantively different read than S02 T2 suggested. S02 T2
fired because it compared the last anchor against S01's full
5-year trajectory σ (~2.5 stress points, ~2.3 spike minutes); the
recent 180-day daily σ is much larger (~6.2 stress points,
~14.8 spike minutes) because daily values vary more than
90-day-smoothed anchor values. **The perturbation visible in S01's
trajectory view is partly a smoothing-vs-baseline artifact** —
real direction, but smaller in σ-units against recent
day-to-day variability.

## Per-channel summary

| channel | μ_ref | σ_ref | μ_pert | **z_mean_pert** | max\|z\|_pert | onset date | reading |
|---|---:|---:|---:|---:|---:|---:|---|
| score | 4.65 | 0.78 | 4.70 | **+0.07** | 3.40 (2026-05-12) | none | **essentially unmoved** |
| avg_stress | 32.4 | 6.21 | 33.9 | **+0.24** | 3.32 (2026-05-02) | none | essentially unmoved |
| max_spike_minutes | 10.6 | 14.77 | 13.0 | **+0.16** | 2.13 (2026-04-28) | none | essentially unmoved |
| RHR | 58.5 | 2.70 | 60.7 | **+0.82** | 1.68 (2026-05-26) | **2026-05-14** | directional toward worsening, not clearly visible |
| sleep_efficiency | 0.989 | 0.017 | 0.989 | **−0.0006** | 3.92 (2026-04-21) | none | essentially unmoved |

**RHR is the only channel** with an algorithmic onset under the
locked §3.5 rule and the only channel reading "directional toward
worsening" (z_mean_pert = +0.82, close to the +1.0 visibility bar
but below it). The onset rule placed RHR's drift starting
2026-05-14.

## Answers to the five §4 questions

### Q1 — Is the score genuinely flat or rising in the perturbation period?

**Essentially flat against the recent reference.** Score
z_mean_pert = +0.07 — well inside the "unmoved" reading band
(|z| < 0.5). The S02 T2 framing of "score IMPROVING while Garmin
perturbs" needs re-reading: at the recent-baseline reference, the
score is barely moving. It is at slightly above its recent normal,
but not exceptionally so.

The max single-day z was +3.40 on 2026-05-12 — a single high day,
not a pattern. The 30-day-rolling-mean uptick observed in S02's
zoom strip (4.23 → 4.60) is real at trajectory level but the
recent 90-day window's MEAN value (4.70) is only 0.07 σ above the
recent 180-day mean (4.65). The score's recent stretch is **not
extraordinarily different from the preceding six months** — it
looks similar.

This is a meaningful re-read of S02. The "score at all-time high
in the tracked window" framing was correct in 5-year context but
overstated against recent context. The two reference frames
disagree on what counts as "exceptional."

### Q2 — Are the 3 elevated Garmin metrics moving together?

**Only one channel pair co-varies above |r| = 0.5: avg_stress
and max_spike_minutes (r = +0.61, n = 83).** Both are stress-derived
measures from the same physiological substrate (sympathetic
activation, per the project's pacing-document framing), so their
co-variation is unsurprising.

The other within-Garmin pairs are weak:
- avg_stress × RHR: r = −0.01 (essentially zero)
- avg_stress × sleep efficiency: r = −0.19
- max_spike × RHR: r = −0.12
- max_spike × sleep efficiency: r = −0.13
- RHR × sleep efficiency: r = −0.11

**RHR is independent of stress and max-spike within this window.**
The RHR drift identified in Q3 (onset 2026-05-14, +0.82σ mean) is
not synchronised with stress or max-spike — it's a separate
channel-specific drift.

Cross-channel including score:
- score × avg_stress: r = +0.26 (positive — unusual; high score
  correlating with high stress within the window)
- score × max_spike: r = +0.20 (same direction, weaker)
- score × RHR: r = +0.05 (essentially zero)
- score × sleep efficiency: r = +0.04 (essentially zero)

The positive r between score and stress within the perturbation
window is **opposite to the expected direction** (better day → less
stress). Within a 83-day window with 1 effective block this is
not verdict-bearing per §3.6, but it suggests that on
high-score days during this period, the user was also experiencing
elevated stress — a possible "productive activity → high score AND
high stress" pattern that the full-corpus S02 §3.8 same-day ρ
(−0.06) does not show. **Descriptive observation only; not a
finding.**

### Q3 — Is there a specific onset date, or is the perturbation gradual?

**Only RHR has an algorithmic onset (2026-05-14).** No other channel
meets the §3.5 onset rule (|z| ≥ 1.0 with ≥ 7 of next 14 days same
direction at |z| ≥ 1.0). The avg_stress and max_spike channels
do have individual high-|z| days (3.32 on 2026-05-02 for stress,
2.13 on 2026-04-28 for spike), but no sustained run cleared the
rule.

**Interpretation**: there is no coordinated multi-channel event
onset. The RHR drift is the only sustained directional pattern,
and it's solo. The other Garmin channels' positive z_mean_pert
values (stress +0.24, spike +0.16) are slight mean shifts
distributed across the window, not driven by a discrete event.

The RHR onset on 2026-05-14 was 22 days before the corpus edge
(2026-06-05). That's a short window — RHR has been drifting
upward for roughly 3 weeks. Whether this is the start of a longer
drift or a transient state cannot be told from this data window.
(Forecasting is out of scope per §2.)

### Q4 — Does sleep efficiency join the perturbation?

**No, by both the trajectory-level and daily-resolution measures.**
z_mean_pert = −0.0006 (essentially zero); reading: essentially
unmoved. Single highest-|z| day was 2026-04-21 (|z| = 3.92,
a one-off bad night), but the window mean equals the reference
mean to 4 decimal places.

This corroborates S02 T2's finding that sleep efficiency was the
exception among Garmin channels. The sleep channel remains the
most stable in this user's data — both H03 originally (precursor
test refuted, fragmentation flat) and now S02c (no perturbation
joining). The original H03 finding ("sleep efficiency for this user
is flat as a board") generalises beyond the crash-precursor
question to the broader trajectory-level question.

### Q5 — Score-Garmin divergence magnitude in σ units

**+0.324 σ mean gap** between composite Garmin-worsen z and
score-z across the 83 days where all four channels (stress,
spike, RHR, score) have data.

- Composite Garmin-worsen z (mean of stress, spike, RHR z-scores):
  +0.407
- Score z: +0.083
- Gap (composite − score): +0.324 σ
- Max single-day gap: +3.07 σ (driven by RHR + stress high-day
  coincidence with neutral score)

**Reading**: there IS a directional separation between the
channels — Garmin pulled slightly more toward "worsening" while
score pulled slightly more toward "improving" — but the magnitude
is small at recent-baseline reference. Under any naive reading,
this is more "the channels barely moved relative to recent normal"
than "the channels dramatically diverged."

The 3.07σ max single-day gap is informative as an extremum but
not as the typical state — most days the gap is small.

## Channel-pair correlation table

(within the perturbation window, n=81-89 per pair; no CI — see
§3.6 caveat)

| channel_a | channel_b | r | n | co-varying? |
|---|---|---:|---:|---|
| score | avg_stress | **+0.26** | 83 | |
| score | RHR | +0.05 | 83 | |
| score | sleep_efficiency | +0.04 | 81 | |
| score | max_spike | **+0.20** | 89 | |
| avg_stress | RHR | −0.01 | 83 | |
| avg_stress | sleep_efficiency | −0.19 | 81 | |
| **avg_stress** | **max_spike** | **+0.61** | 83 | **YES** |
| RHR | sleep_efficiency | −0.11 | 81 | |
| RHR | max_spike | −0.12 | 83 | |
| sleep_efficiency | max_spike | −0.13 | 81 | |

Only one pair co-varies at |r| ≥ 0.5: avg_stress and max_spike, both
sympathetic-arousal measures. Note the **two positive cross-channel
r values involving score** (with avg_stress at +0.26 and max_spike
at +0.20) — both unexpected in direction, both small in magnitude,
both descriptive-only. The "score and stress both up on the same
days" pattern is consistent with a "productive / engaged → high
sympathetic activation AND high subjective day-rating" interpretation
that S02 §3.8's full-corpus same-day ρ (−0.06) does not surface.
Worth flagging for future hypothesis generation about which kinds of
days within a stabilisation stretch produce which kinds of
sympathetic-load patterns; not pursued here.

## What this means for the project

### S02 T2 trigger needs nuancing

S02 T2 "fired forward" because the May 2026 perturbation cleared
the 1σ-vs-trough rule against S01's 5-year anchor σ for 3 of 4
Garmin channels. **S02c re-measures the same period against the
recent 180-day daily σ and finds that only RHR has any clear
directional signal**, and even RHR (z_mean +0.82) is below the
"visibly worsening" 1σ bar.

This is not "S02 was wrong." The 5-year trajectory σ and the
recent 180-day daily σ are two legitimately different reference
frames asking two legitimately different questions:
- S02's question: is the current state exceptional compared to the
  user's whole tracked history?
- S02c's question: is the current state exceptional compared to
  the user's recent baseline?

The two answers disagree because day-to-day variability is much
larger than 90-day-rolling variability. **S02's T2 finding stands
as a trajectory-level observation; S02c's finding stands as a
daily-resolution observation; both are correct in their own frame.**
What S02c forecloses is the strongest reading of T2 — that the
Garmin perturbation is unambiguous and the score's stability is
striking.

### Updates needed in dependent documents

- **[S02 notes.md](../S02-score-trajectory/notes.md)** T2 section
  should be cross-referenced to S02c so readers see both the
  trajectory-level and daily-resolution framings.
- **[STOCKTAKE.md](../../STOCKTAKE.md)** entries that cite S02's
  T2 finding should mention the S02c nuance.
- **The "score at all-time high" framing from S02** should be
  qualified: trajectory-level yes; daily-resolution against recent
  baseline, essentially unmoved.

### Combined with S02b's refutation

[S02b](../S02b-score-lead/notes.md) refuted the daily-resolution
T1 (score-leads-Garmin) interpretation. S02c shows the
daily-resolution T2 (channel divergence) magnitude is small.

**Combined reading**: at the day-to-day timescale, the
score and Garmin channels are essentially moving on parallel,
mostly-independent recent baselines. Both T1 and T2 are
trajectory-level findings about how the 90-day-rolling curves
behave; neither survives strongly at daily resolution. The
**"the score channel measures something different from the
Garmin channels at daily resolution"** reading from S02 §3.8 is the
most consistent across all three pieces (S02, S02b, S02c). The
two channels live on different daily-noise floors; their
trajectory-level shapes co-vary in the broad sense
(both move with stabilisation) but the daily dynamics are
substantially independent.

## Methodology notes

- **Reference window σ is much larger than S01 anchor σ.** Example:
  avg stress S01-anchor σ = 2.51 (the 238 trajectory values);
  avg stress S02c-reference σ = 6.21 (180 daily values). The
  factor-of-2.5 difference is the smoothing effect: a 90-day rolling
  mean has much less variance than the underlying daily series.
  Both σ values are correct for their respective questions; the
  reading just needs to be against the right σ.
- **Onset rule at z=1.0 + 14d/7d sensitivity is locked, not
  swept.** A more sensitive rule (z=0.7 + 10d/5d) might surface
  onset dates for avg_stress and max_spike; a less sensitive one
  (z=1.5 + 21d/11d) might miss RHR. The §3.5 rule was chosen
  pre-data for reasonability; sensitivity testing would be a
  separate pre-registration.
- **Channel-pair r values within 83-89 days are point estimates
  only.** At 1 effective block under the project's 90-day-block
  discipline, no CI is meaningful. The "co-varying" flag at
  |r| ≥ 0.5 is a descriptive threshold; the only flagged pair
  (stress × max_spike at +0.61) is unsurprising given they're
  both stress-derived.
- **Sleep efficiency reference window n is 178, perturbation
  window n is 81** — slightly below the 180 / 90 day-count
  because of off-wrist confirmation-type exclusions per the S01
  sleep loader. Effect on z-scoring is negligible (σ computed on
  178 days is close to σ computed on 180 days).
- **The +3.92 σ sleep efficiency outlier on 2026-04-21** is a single
  bad night. The perturbation-window MEAN equals the reference mean,
  so this is not a sustained shift. Worth noting because of the
  extremity (largest single-day |z| across all channels) but
  reading would be "one bad sleep night, isolated" not
  "sleep efficiency is also perturbing."

## Caveats

- **Reference window is locked at 180 days immediately preceding
  the perturbation.** A different reference window choice would
  produce different σ values and therefore different z-readings.
  The 180-day choice is the locked compromise per §3.1; not
  sensitivity-tested.
- **Perturbation window length matches S01's 90-day rolling
  window.** Reading is consistent with "this is what fed S01's
  last anchor." Different window length would not match S01's
  framing.
- **"Recent" is a moving target.** The participant's stabilisation
  trajectory means recent baselines have themselves drifted across
  years. The reference window (Sep 2025 – Mar 2026) is the most
  stable, most-recovered, lowest-burden stretch in the tracked
  window per S02's distribution panel. So the perturbation is being
  measured against the user's best baseline state — a strict
  reference that makes "exceptional" harder to clear than
  against a 5-year average.
- **Forecasting out of scope.** The RHR drift starting 2026-05-14
  has been ongoing for 22 days at the corpus edge. This data does
  not tell us whether it continues, plateaus, or reverses.
- **Causation out of scope.** None of the channel-pair
  correlations or directional drifts establishes mechanism. The
  participant's life context is not in the analysis.

## What this enables

- A **methodologically honest** revision of S02 T2's framing.
  S02 T2 was correctly fired against its own bar; S02c against
  its own bar produces a different reading; both can be cited.
- A **first daily-resolution characterisation of the
  May-June 2026 period** with all 5 channels at once, for later
  comparison if the perturbation continues into Q3 2026.
- A **specific RHR onset date** (2026-05-14) that can be the
  starting point for any future per-day analysis of recent
  dynamics — e.g. "did RHR continue to rise after 2026-06-05?"
  Re-runnable as more data arrives.

## What this does NOT do

- Does not predict whether the RHR drift continues or resolves.
- Does not establish causation.
- Does not test other reference window choices (e.g. 90 days,
  360 days).
- Does not test sensitivity of the onset rule parameters.
- Does not address why the score and stress channels co-vary
  positively within this specific window (opposite of full-corpus
  same-day direction).
- Does not generalise to other users.

---

*S02c executed 2026-06-07. Spec at [hypothesis.md](hypothesis.md);
reference frame and reading rules locked before execution; reading
reported faithfully without drift. Sibling [S02b](../S02b-score-lead/)
addresses S02's T1 trigger separately and is also refuted.*
