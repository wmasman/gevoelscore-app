# S02c — May 2026 channel divergence: pre-registered spec

**Pre-registration written 2026-06-07, before
`compute_divergence.py` runs against any data. Locked. Any
subsequent change AFTER data inspection creates `S02c-revised/`;
this spec is not edited in place.**

**Status**: pending. **Descriptive characterisation** of S02's
T2 finding (May 2026 channel divergence). No support/refute verdict;
locked answer-questions per S02's discipline. Sibling to
[S02b-score-lead](../S02b-score-lead/) addressing T1.

---

## 1. Purpose

[S02 §7.2 T2](../S02-score-trajectory/notes.md) found that the
May 2026 perturbation is **visible in 3 of 4 S01 Garmin metrics
(avg stress, max-spike duration, RHR) but NOT in either score view
(90d trajectory OR 6-month zoom strip)**. The score is currently
at its all-time-high in the tracked window while the Garmin
pendulum is perturbing.

S02c **describes this divergence at daily resolution** across the
perturbation period (April-June 2026), characterises whether the
3 elevated Garmin channels move in coordinated or independent ways,
and identifies whether there is a specific onset date or a gradual
drift.

This is descriptive only — no support/refute bar. The spec locks
methodology + answer-questions before data inspection.

## 2. Scope

In scope:
- Per-day raw values for 5 channels across the perturbation window:
  score, avg stress, max-spike duration, RHR, sleep efficiency.
- Pre-perturbation reference window (locked at 180 days = 2025-09-08
  → 2026-03-07, six months pre-perturbation).
- Per-channel z-score against reference-window mean/std.
- Per-day, per-channel "perturbation magnitude" trace.
- Channel-pair correlations within the perturbation window only.
- Identification of an onset date per channel (algorithmic rule).

Out of scope:
- No prediction or forecasting of how the perturbation will evolve.
- No causation attribution.
- No cross-window inference (e.g. "this perturbation is similar to
  past perturbations"); the scope is the specific April-June 2026
  window.
- No mechanism attribution. We describe the pattern, not its driver.
- No new pre-registered hypothesis on lead/lag within the
  perturbation. If lead/lag within the perturbation looks
  interesting, that's a new follow-up.

## 3. Methodology — locked

### 3.1 Window definitions

- **Perturbation window** = 2026-03-08 → 2026-06-05 (90 days
  ending at corpus edge). Length matches S01's 90-day rolling
  window so the "last anchor" of S01 represents exactly this
  period.
- **Reference window** = 2025-09-08 → 2026-03-07 (180 days
  immediately preceding the perturbation window). 180 days = 2×
  perturbation window length so per-channel std is computed on a
  population sufficient to characterise the channel's recent
  normal-state variability.

### 3.2 Data sources

- **Score**: `day_entries.csv` (1–6 integer).
- **Avg stress**: UDS `allDayStress.aggregatorList[TOTAL].
  averageStressLevel` (raw daily).
- **Max-spike minutes**: `H02b-stress-spikes/daily_max_spike.csv`
  (`max_spike_minutes` where `valid=1`).
- **RHR**: UDS `restingHeartRate` (raw daily).
- **Sleep efficiency**: per S01's loader (TST / TIB; excludes
  `UNCONFIRMED`/`OFF_WRIST`/`NOT_CONFIRMED` confirmation types and
  TIB < 4 hours).

All five channels are loaded at raw daily resolution; no smoothing.

### 3.3 Z-score against reference window

For each channel:
- `μ_ref = mean of channel values in [2025-09-08, 2026-03-07]`
- `σ_ref = stdev of channel values in [2025-09-08, 2026-03-07]`
- `z(d) = (value(d) − μ_ref) / σ_ref` for each day d in the
  perturbation window (and also in the reference window for the
  per-channel plot)
- **Sign convention**: z is left in its raw direction (positive z =
  higher than reference). For worsen-direction metrics (stress,
  max-spike, RHR), positive z = worsening. For improve-direction
  metrics (sleep efficiency, score), positive z = improving. The
  sign convention is **NOT flipped** in the plot; the plot legend
  states the direction explicitly per channel.

### 3.4 Per-channel summaries

For each channel, compute and report in the CSV:
- `n_ref` (days of valid value in reference window)
- `n_pert` (days of valid value in perturbation window)
- `mean_ref`, `std_ref`
- `mean_pert`
- `z_mean_pert` = (mean_pert − mean_ref) / std_ref (the perturbation
  window's mean shift in σ units; aligned with S02's "visible
  perturbation" definition but using a different reference window)
- `max_abs_z_pert` (largest |z| observed in the perturbation window)
- `max_abs_z_day` (the date where that |z| occurred)

### 3.5 Onset date — algorithmic rule

For each channel, an "onset date" is identified algorithmically
within the perturbation window:
- `onset_date(channel)` = the first day `d` in
  [2026-03-08, 2026-06-05] where `|z(d)| ≥ 1.0` AND the next 14
  consecutive days each have at least 7 of the 14 with `|z| ≥ 1.0`
  in the same direction (positive or negative as the onset day).

The "next 14 days with 7 in same direction" rule prevents an
isolated spike day from being mis-identified as onset. Length
14 ≈ a fortnight, short enough to be reactive and long enough to
exclude one-shot noise.

If no channel meets this rule, report "no clear algorithmic onset."

### 3.6 Channel-pair correlation within the perturbation window

Pearson r between each pair of channels' z-scored series across the
90 perturbation-window days. **No bootstrap CI** at this stage —
the window is small (~90 days, 1 effective block at 90-day block
length, so block-bootstrap is degenerate). Report point estimates
only, marked as "descriptive, not verdict-bearing."

Channel pairs that have ≥ 0.5 |r| within the window are flagged as
"co-varying within the perturbation."

### 3.7 Reading-direction interpretation rules

Locked before data so the read in notes.md is consistent:

- **z_mean_pert ≥ +1.0** for worsen-direction metric → perturbation
  is visibly worsening this channel.
- **z_mean_pert ≤ −1.0** for improve-direction metric → perturbation
  is visibly worsening this channel.
- **z_mean_pert magnitude < 0.5** → channel is essentially unmoved.
- **Between 0.5 and 1.0 in either direction** → directional but
  not clearly visible.

These rules apply to mean shifts; |z|_max_day is reported as a
secondary signal showing whether any single day reached extremity.

## 4. Locked questions notes.md must answer

1. **Is the score genuinely flat or rising in the perturbation
   period?** Report score `z_mean_pert` and `max_abs_z_pert` against
   the reading-direction rules. The S02 T2 finding said "score is
   IMPROVING" — verify this at daily resolution.
2. **Are the 3 elevated Garmin metrics (stress, max-spike, RHR)
   moving together?** Report channel-pair correlations among them
   within the perturbation window; flag pairs ≥ 0.5 |r| as
   co-varying.
3. **Is there a specific onset date, or is the perturbation
   gradual?** Apply §3.5 onset rule per channel. Report dates or
   "no clear algorithmic onset." If multiple channels have onset
   dates within ≤ 14 days of each other, treat as a coordinated
   event onset.
4. **Does sleep efficiency join the perturbation?** S02 said no
   (it was the 4th Garmin metric and was not visible). Verify at
   daily resolution against the new reference window.
5. **What is the score-Garmin divergence magnitude in σ units?**
   Compute (avg_z_garmin − avg_z_score) where avg_z_garmin is the
   mean across stress + max-spike + RHR (worsen-direction
   composite, sign-flipped if necessary to align directions).
   This is the headline characterisation number.

## 5. Outputs

### 5.1 `channel_summary.csv`

One row per channel × window-position:
- `channel`
- `window` (`reference` | `perturbation`)
- `n_days`
- `mean`
- `std` (reference-window std only; copied to perturbation row for
  ease of reading)
- `z_mean_pert` (only on perturbation row)
- `max_abs_z_pert` (only on perturbation row)
- `max_abs_z_day` (only on perturbation row)
- `onset_date` (only on perturbation row; blank if no onset)
- `reading` (locked interpretation per §3.7; blank on reference row)

### 5.2 `channel_pair_correlations.csv`

One row per channel pair (10 rows for 5 channels):
- `channel_a`, `channel_b`
- `pearson_r` (z-scored series, perturbation window only)
- `n_pairs` (days with both channels present)
- `co_varying` (`YES` if |r| ≥ 0.5, else blank)

### 5.3 `divergence_plot.png`

Two panels stacked vertically, sharing x-axis:
- **Panel A** — 5 daily z-score lines (score, stress, max-spike,
  RHR, sleep eff) across the reference window + perturbation window
  (270 days total). Vertical line marks the
  reference/perturbation boundary (2026-03-08). Direction-convention
  legend states "positive z = higher than reference; for stress /
  max-spike / RHR that is worsening; for score / sleep efficiency
  that is improving." Onset dates per channel marked with channel-
  coloured arrowheads on the x-axis.
- **Panel B** — composite divergence trace: `worsen_garmin_z(d)` =
  (z_stress(d) + z_max_spike(d) + z_rhr(d)) / 3 (positive =
  worsening) and `score_z(d)` (positive = improving), with a shaded
  band between them showing the cross-channel gap. Single visual
  for the "Garmin perturbing while score improving" claim from S02
  T2.

### 5.4 `notes.md`

Sections:
- Status statement (descriptive, no verdict).
- Headline: the divergence magnitude number from §4 Q5.
- Answers to the five §4 questions in order, each with locked
  reading per §3.7.
- Per-channel summary table (transcribed from
  channel_summary.csv).
- Channel-pair correlations (transcribed from
  channel_pair_correlations.csv).
- Methodology notes (including the 90-day-window-1-block caveat
  on §3.6 correlations).
- Caveats.
- "What this means for the project" — implications for STOCKTAKE
  and synthesis given S02 T2 + S02b refuted T1.

## 6. Caveats locked into notes.md

- **Small perturbation-window sample.** 90 days at daily resolution
  is ~90 observations but effectively 1 block at the project's
  90-day block-length discipline. Channel-pair r values are point
  estimates only; CI not computed. A larger window would dilute
  the perturbation signal with pre-perturbation days.
- **Reference window choice is locked at 180 days immediately
  pre-perturbation.** A longer reference window would absorb older
  baseline; a shorter would lose statistical resolution on the
  reference std. 180 days = 2× perturbation window is the locked
  compromise. NOT sensitivity-tested.
- **z-score normalisation is per-channel.** Channels with naturally
  high day-to-day variance (e.g. sleep efficiency, n_ref ~ 180 with
  σ in the third decimal) have small z magnitudes more often than
  low-variance channels. Interpretation in σ units handles this
  correctly but reading "1 σ on sleep efficiency vs 1 σ on stress"
  as "equal magnitude" requires the σ-unit framing.
- **Confirmation-type-based sleep filtering is per S01 loader.**
  Off-wrist nights are excluded. The reference window may have
  fewer-than-180 valid sleep nights depending on wear
  compliance.
- **Onset rule (§3.5) is sensitive to its parameters** (the 1.0 σ
  threshold + 14-day-7-of-14 rule). Locked here without sensitivity
  testing. If notes.md reports "the onset rule produced surprising
  output," that goes into the audit log, not a silent fix.
- **The score channel has no "elevated" or "worsened" direction
  pre-perturbation** — it was already at its trajectory peak. So
  the question "is the score perturbed" is actually "is the score
  visibly *deviating in any direction* from a recent already-high
  baseline." Direction matters for interpretation; the reading
  rules in §3.7 handle this.

## 7. Audit-trail discipline

- This spec is committed BEFORE `compute_divergence.py` runs against
  any data.
- All reading-direction rules (§3.7) and onset rules (§3.5) are
  locked before execution.
- If a methodology issue surfaces during execution, it is logged
  in notes.md as a finding, not silently fixed.
- Any methodology change AFTER data inspection creates
  `S02c-revised/`.

### 7.1 Prior-knowledge disclosure

What was known before locking S02c:
- **From S02 T2**: stress, max-spike, RHR were "visible" perturbing
  per S02's 1σ-vs-trough rule; sleep efficiency was not; score was
  NOT visible perturbing (either way). S02's σ was computed against
  S01's full anchor distribution; S02c's σ is computed against the
  specific 180-day pre-perturbation window. **The two reference
  frames differ deliberately**: S02 used "is current state
  exceptional vs the whole 5-year span"; S02c asks "is current state
  exceptional vs the recent baseline."
- **From [S02b](../S02b-score-lead/notes.md)**: the daily-resolution
  T1 lead/lag pattern is refuted. So if S02c finds Garmin and score
  diverging at daily resolution, that divergence is NOT a
  manifestation of a daily-resolution lag — they're simply moving
  on independent or differently-driven trajectories.
- **User's recent stabilisation framing** (memory item): the score
  is at its highest-burden-period stretch in the tracked window;
  the perturbation in Garmin is real but the user's subjective
  experience does not (currently) carry it.

What was NOT inspected before locking:
- Any per-channel z value in the perturbation window.
- Any channel-pair correlation.
- Any onset date.
- The score's z value across the perturbation window.

## 8. Registry update — locked

Once notes.md is committed:

> - **S02c May 2026 channel divergence**
>   ([S02c-may2026-divergence/notes.md](S02c-may2026-divergence/notes.md),
>   run 2026-06-07) — daily-resolution z-score characterisation of
>   the April-June 2026 perturbation. Reference window 2025-09-08 →
>   2026-03-07 (180 days). Reports per-channel z-mean-pert, onset
>   dates, channel-pair r within the perturbation window. Descriptive
>   characterisation of S02 T2; sibling to S02b. **[Headline
>   divergence number + onset-coordination finding to fill in
>   post-run.]**

## 9. What this does NOT do

- Does not predict whether the perturbation will worsen or resolve.
- Does not establish causation.
- Does not declare a new era boundary.
- Does not re-run S02b's lagged correlation on the perturbation
  window (the n is far too small).
- Does not test mechanism hypotheses (e.g. "an external stressor
  drove this"); the participant's life context is not in scope of
  the analysis.
- Does not generalise to other users.

---

*Spec written 2026-06-07. Execution pending same-day.*
