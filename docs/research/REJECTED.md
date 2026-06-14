# Rejected hypotheses — project audit trail

A running register of hypotheses that have been **rejected, blocked, or
superseded** during this research project. Maintained to preserve the
audit trail of what was tried that did not survive — at project scale,
the garden-of-forking-paths is invisible without this register.

**Sister registers** (active hypotheses):

- [wiggers_testable_hypotheses.md](wiggers_testable_hypotheses.md) —
  active Wiggers-derived hypotheses (the Tier 1/2/3 shortlist)
- [personal_hypotheses.md](personal_hypotheses.md) — active
  personally-derived hypotheses
- [analyses/hypotheses/registry.md](analyses/hypotheses/registry.md) —
  HA pre-registration + result registry (this is the canonical source
  the bulk of the entries below were extracted from)

## Categories

- **NULL** — pre-registered test ran; result was null on the project's
  3-criterion bar (frequency / discrimination / magnitude) or on the
  both-eras rule. Evidence column links to the `result.md`.
- **DESCRIPTIVE-FAIL** — descriptive screening found no signal worth
  pre-registering on this corpus.
- **BLOCKED** — data, hardware, or external dependency does not support
  testing on this corpus. May be re-openable on future data.
- **SUPERSEDED** — reformulated into a different hypothesis. Evidence
  column links to the successor.
- **WITHDRAWN** — deliberately removed from consideration (e.g. low
  marginal leverage given other tests already cover the construct, or
  spec-induced trivial result).

## Register

Chronological by closure date. Train/validate split is the historical
2023-12-31 split; "overall" verdicts apply the locked both-eras rule.

| date | ID | source | category | reason | evidence |
|---|---|---|---|---|---|
| 2026-06-05 | H01 | HA-test | NULL | RHR drift before crashes — refuted both eras; validate window shows RHR *lower* in lead-up than baseline (inverted). | [H01-rhr-drift/result.md](analyses/hypotheses/H01-rhr-drift/result.md) |
| 2026-06-05 | H02 | HA-test | SUPERSEDED | Daily-aggregate stress elevation — refuted overall; reformulated as H02b (per-minute spike count) after user clarified the spike-vs-average framing. | [H02-stress-elevation/result.md](analyses/hypotheses/H02-stress-elevation/result.md) → H02b |
| 2026-06-05 | H03 | HA-test | NULL | Sleep efficiency drop before crashes — refuted decisively both eras (0% of episodes crossed −5 pp threshold). Sleep efficiency is flat for this user; sharper metrics queued as H03b. | [H03-sleep-efficiency/result.md](analyses/hypotheses/H03-sleep-efficiency/result.md) |
| 2026-06-05 | H04 | HA-test | NULL | Body battery net-drain elevated before crashes — refuted both eras; only marginal validate-side hint (+13.3 pp, just below +15 bar). | [H04-body-battery/result.md](analyses/hypotheses/H04-body-battery/result.md) |
| 2026-06-05 | H05 | HA-test | WITHDRAWN | Recovery-time descriptive (baseline−1 target) — spec-induced trivial (all 25 episodes recover "0 days" by construction). Queued as H05b with sustained-target reformulation. | [H05-recovery-time/result.md](analyses/hypotheses/H05-recovery-time/result.md) |
| 2026-06-05 | K01 | HA-test | NULL | Crash depth shifted across eras — refuted on permutation bar (p=0.28) but direction unambiguous (delta_median +1.0, 0/15 late-era crashes reached score 1 vs 3/14 early). Median brittle on integer scale at small samples. | [K01-crash-depth/result.md](analyses/hypotheses/K01-crash-depth/result.md) |
| 2026-06-05 | K02 | HA-test | NULL | Crash duration shortened across eras — refuted on bar (delta_median −0.5 days) but long-crash tail (≥5 days) collapsed from 36% to 7%. Same median brittleness as K01. | [K02-crash-duration/result.md](analyses/hypotheses/K02-crash-duration/result.md) |
| 2026-06-06 | H02b-on-dips | HA-test | NULL | H02b's spike-count metric re-run against 79 v2 dips — refuted by strict bar (+9.1 train, +5.2 validate); ~3× weaker than crashes. | [crash_v2-definition/h02b_on_dips_result.md](analyses/hypotheses/crash_v2-definition/h02b_on_dips_result.md) |
| 2026-06-06 | HA01 | HA-test | SUPERSEDED | 3-day exertion shock window — refuted; replaced by HA01b at 4-day after experiential PEM-lag framing. | [activity-labels/output/ha_results.md](analyses/garmin_exploration/activity-labels/output/ha_results.md) → HA01b |
| 2026-06-06 | HA02 | HA-test | SUPERSEDED | 3-day push burden — refuted; replaced by HA02b at 4-day window. | [activity-labels/output/ha_results.md](analyses/garmin_exploration/activity-labels/output/ha_results.md) → HA02b |
| 2026-06-06 | HA05 | HA-test | SUPERSEDED | 3-day exertion-shock variant — refuted; replaced by HA05b at 4-day. | [activity-labels/output/ha_results.md](analyses/garmin_exploration/activity-labels/output/ha_results.md) → HA05b |
| 2026-06-06 | HA02b | HA-test | NULL | 4-day push burden — refuted at the 4-day window; push burden is genuinely not a precursor for this user. | [activity-labels/output/ha_results_4day.md](analyses/garmin_exploration/activity-labels/output/ha_results_4day.md) |
| 2026-06-06 | HA05b | HA-test | NULL | 4-day exertion-shock variant — refuted alongside HA02b at 4-day. | [activity-labels/output/ha_results_4day.md](analyses/garmin_exploration/activity-labels/output/ha_results_4day.md) |
| 2026-06-06 | HA02c | HA-test | NULL | Push burden on Theme A lagged baseline — refuted both eras (train −18.7, validate +0.7). Lagged baseline improves measurement standing but does not resurrect push_burden as a predictor. | [activity-labels/output/ha_results_4day_lagged.md](analyses/garmin_exploration/activity-labels/output/ha_results_4day_lagged.md) |
| 2026-06-06 | HA01b-recomputed | HA-test | NULL | HA01b composite on lagged baseline — refuted both eras (train +5.8, validate +4.0). The original rolling-baseline validate +17.3 pp "first SUPPORTED" headline softened by −13.3 pp; that headline was substantially a baseline-construction artifact. | [activity-labels/output/ha_results_4day_lagged.md](analyses/garmin_exploration/activity-labels/output/ha_results_4day_lagged.md) |
| 2026-06-06 | H02b | HA-test | NULL | Per-minute stress spike count (4-day) — train SUPPORTED but validate near-miss; overall refuted by both-eras rule. Still the cleanest train-era signal in the project. | [H02b-stress-spikes/](analyses/hypotheses/H02b-stress-spikes/) |
| 2026-06-06 | H02d | HA-test | SUPERSEDED | Sentinel-corrected spike count — validate refuted across all 4 arms; train SUPPORTED at bridge × 5d (+31.8 pp). Subsequent cross-channel correlation showed H02b ≡ H02d at ρ=+1.000 — H02d folded into H02b as a single channel, not a distinct primitive. | [H02d-stress-spikes-uncensored/result.md](analyses/hypotheses/H02d-stress-spikes-uncensored/result.md) → H02b |
| 2026-06-07 | HA06 | HA-test | SUPERSEDED | Morning RHR delta with absolute bpm thresholds — refuted both eras (validate 0/15 crashes trigger at 5 bpm). Thresholds mis-calibrated to participant variability. Replaced by HA06b with z-score thresholds. | [HA06-morning-rhr-delta/result.md](analyses/hypotheses/HA06-morning-rhr-delta/result.md) → HA06b |
| 2026-06-07 | HA07 | Wiggers | BLOCKED | HRV day-over-day drop — Forerunner 245 (Elevate V3) does not record HRV Status; `/hrv-service/hrv/{date}` returns empty across the full corpus. Substituted by HA07c (sleep stress as proxy); re-openable on Forerunner 255/265/955/965 or Fenix 7 hardware. | [HA07c-sleep-stress-mean-delta/](analyses/hypotheses/HA07c-sleep-stress-mean-delta/) |
| 2026-06-07 | HA08 | Wiggers | BLOCKED | HRV slope variant — same FR245 hardware blocker as HA07. Substituted by HA08c. | [HA08c-sleep-stress-slope/](analyses/hypotheses/HA08c-sleep-stress-slope/) |
| 2026-06-07 | HA06b | HA-test | NULL | Morning RHR delta with z-score thresholds — train SUPPORTED at N_std=1.5 (+18.9 pp); validate refuted (+0.8 pp non-discriminative). Validate directionality split (25% elevated / 75% lowered) shows Wiggers' parasympathetic-swing pattern present but non-discriminative. | [HA06b-rhr-zscore/result.md](analyses/hypotheses/HA06b-rhr-zscore/result.md) |
| 2026-06-07 | HA07c | HA-test | NULL | Sleep stress mean delta (HRV proxy) — train SUPPORTED (+23.2 pp); validate refuted (−6.0 pp). HRV-proxy validated for train; HRV hypothesis itself remains untestable. | [HA07c-sleep-stress-mean-delta/result.md](analyses/hypotheses/HA07c-sleep-stress-mean-delta/result.md) |
| 2026-06-07 | HA08c | HA-test | NULL | Sleep stress slope (5d OLS) — train SUPPORTED (+23.0 pp); validate refuted (+1.5 pp) and anti-predictive at higher thresholds. Validate-era crashes arrive against unusually-flat baseline. | [HA08c-sleep-stress-slope/result.md](analyses/hypotheses/HA08c-sleep-stress-slope/result.md) |
| 2026-06-07 | HA10 | HA-test | NULL | Morning BB peak z-score (bidirectional) — train refuted (−20.5 pp); validate SUPPORTED (+16.2 pp, first validate-era SUPPORTED test in project) — overall refuted by both-eras rule. Striking era-directionality reversal (train 100% lowered / validate 69% elevated). | [HA10-bb-overnight-recharge/result.md](analyses/hypotheses/HA10-bb-overnight-recharge/result.md) |
| 2026-06-07 | HA11 | HA-test | NULL | Within-day stress U-dip event count — train SUPPORTED (+22.8 pp); validate refuted (inverse-direction, −10.7 pp at 4d, scales to −24.1 at 5d N_std=2.0). Validate-era crashes have fewer U-dip events than null windows. | [HA11-stress-udip/result.md](analyses/hypotheses/HA11-stress-udip/result.md) |
| 2026-06-07 | HA10 v1 diag | HA-test | SUPERSEDED | v1 threshold-monotonicity diagnostic returned CLOSE (peak past rescue window). v1 criteria methodological defect acknowledged; superseded by v2 with five-category shape rule. | [HA10-threshold-monotonicity-diagnostic/result.md](analyses/hypotheses/HA10-threshold-monotonicity-diagnostic/result.md) → HA10 v2 (RESCUE) |
| 2026-06-07 | HA07d v1 diag | HA-test | SUPERSEDED | v1 diagnostic CLOSE both eras; criteria penalised stable-plateau and rising-with-threshold shapes equally robust as canonical decline. Superseded by v2. | [HA07d-threshold-monotonicity-diagnostic/result.md](analyses/hypotheses/HA07d-threshold-monotonicity-diagnostic/result.md) → HA07d v2 (RESCUE both eras) |
| 2026-06-07 | HA06b v2 diag | HA-test | SUPERSEDED | v2 diagnostic CLOSE via Cat 4 (sign-changes in [1.0, 3.0]; Spearman near zero). Train SUPPORTED verdict stays on record but **permanently demoted to non-load-bearing**. | [HA06b-threshold-monotonicity-diagnostic-v2/result.md](analyses/hypotheses/HA06b-threshold-monotonicity-diagnostic-v2/result.md) |
| 2026-06-07 | HA01c | HA-test | SUPERSEDED | Effective-exertion shock — SUPPORTED both eras at locked τ=0.75 (train +21.3, validate +19.5) BUT v2 threshold-monotonicity diagnostic returned AMBIGUOUS in train (bumpy-but-never-negative). Load-bearing status withheld. | [HA01c-effective-exertion-shock/result.md](analyses/hypotheses/HA01c-effective-exertion-shock/result.md) + [HA01c v2 diag](analyses/hypotheses/HA01c-threshold-monotonicity-diagnostic-v2/result.md) |
| 2026-06-07 | H03b | HA-test | BLOCKED | Per-minute BB overnight recharge — INCONCLUSIVE × 12 cells by data availability (`sleepBodyBattery` per-3-min array populated only from ~2024-06-03; train era zero coverage). Re-runnable only after `unknown_233` decode unlocks per-minute BB for old corpus. | [H03b-bb-overnight-recharge-permin/result.md](analyses/hypotheses/H03b-bb-overnight-recharge-permin/result.md) |
| 2026-06-07 | S01 | descriptive | SUPERSEDED | Stabilisation trajectories (90-day rolling means of 4 metrics) — archived 2026-06-13; qualitative framing not a validated analytical era. | [_archive/S01-stabilisation-trajectories/notes.md](analyses/hypotheses/_archive/S01-stabilisation-trajectories/notes.md) |
| 2026-06-07 | S02 | descriptive | SUPERSEDED | Score trajectory + same-day rank correlation — archived 2026-06-13; §3.8 primary ρ=−0.0557 ambiguous-underpowered at 16 effective blocks; tail-collapse + new upper mode findings reported as descriptive notes. | [_archive/S02-score-trajectory/notes.md](analyses/hypotheses/_archive/S02-score-trajectory/notes.md) |
| 2026-06-07 | S02b | HA-test | NULL | Score-lead lagged correlation (primary ρ at +149d, secondary at +100d) — REFUTED on criterion (c) lag-improves-over-same-day (|delta|=+0.002 vs bar 0.10); also fails magnitude and sign. Rolling-curve T1 finding does NOT survive at daily resolution. | [S02b-score-lead/notes.md](analyses/hypotheses/S02b-score-lead/notes.md) |
| 2026-06-07 | S02c | descriptive | SUPERSEDED | May 2026 channel divergence z-score characterisation — archived 2026-06-13; descriptive only; perturbation modest (composite gap +0.324σ) and concentrated in RHR. | [_archive/S02c-may2026-divergence/notes.md](analyses/hypotheses/_archive/S02c-may2026-divergence/notes.md) |
| 2026-06-13 | H02b-trajectory | descriptive | SUPERSEDED | Rolling 12-month discrimination curve replacing H02b binary verdict — archived 2026-06-13; superseded by the cross-channel correlation matrix finding that H02b ≡ H02d (ρ=+1.000) and the project-shape revision around effective signal clusters. | [_archive/H02b-trajectory-sub-files/trajectory-notes.md](analyses/hypotheses/_archive/H02b-trajectory-sub-files/trajectory-notes.md) |
| 2026-06-06 | crash_v2-from-notes | informal | SUPERSEDED | NLP-derived crash labels — superseded 2026-06-06; current `crash_v2` is the score-based two-tier (crash + dip) definition. NLP angle lives in notes-label-quality work + Goal B tagging-suggestion engine. | [crash_v2-definition/](analyses/hypotheses/crash_v2-definition/) |
| 2026-06-14 | F3 | Wiggers | WITHDRAWN | Garmin sleep score predicts next-day capacity — not in `sleepData.json`, FIT-side unverified, low marginal leverage given F1 + F2 + F4 already cover sleep. | [wiggers_testable_hypotheses.md](wiggers_testable_hypotheses.md) §F |
| 2026-06-14 | G2 | Wiggers | BLOCKED | Skin-temperature deviation around PEM onset — sensor not present on FR245; re-openable on a device with skin-temp (Forerunner 265+, fēnix 7, Venu 3). | [wiggers_testable_hypotheses.md](wiggers_testable_hypotheses.md) §G |

## How to add a row

- **Add at the time of rejection**, not in batches at the end of a
  session. The register's value is in real-time honesty, not
  retroactive completeness. (The bulk of the rows above were a
  one-time backfill on 2026-06-14 from registry.md; going forward the
  rule is one row per rejection.)
- **Reason column is one sentence.** If more context is needed, link
  to it in the evidence column rather than expanding the row.
- **NULL rows** cite the HA `result.md`; the result stays in place
  as the canonical evidence. This register just makes the rejection
  visible at project scope.
- **SUPERSEDED rows** link to the successor hypothesis (e.g. *"H4 v1
  RHR-anchored → H4 v2 BB-anchored composite, see hypothesis.md
  rev 2026-06-13"*).
- **BLOCKED rows** stay in the register even if hardware changes
  later — instead, add a new row when the hypothesis is re-opened on
  the new data, citing the BLOCKED row as antecedent.

## What this register does NOT replace

- HA `result.md` files remain the canonical record of what each
  pre-registered test produced.
- The Wiggers register's "Out of priority" section + the verification
  log remain the canonical record of which Wiggers hypotheses are
  active and how they were operationalised.
- Methodology MDs in [methodology/](methodology/) remain the
  canonical record of major methodological decisions.

This register is a thin index *on top of* those — one row per
rejection, project-scope, scannable, kept honest by real-time
maintenance.

## What's not in the table (deliberately)

- **Deferred hypotheses** that haven't been tested yet (H02e, HA09,
  HA12, H04b, dictionary-v3 polarity-marker negation, etc.) — these
  are queued in [methodology/queued_work.md](methodology/queued_work.md)
  and [QUEUED-WORK.md](QUEUED-WORK.md), not rejected.
- **Hypotheses with mixed verdicts where the supported arm is
  load-bearing** (e.g. HA07d both-eras SUPPORTED → still active, even
  with statistical-significance caveats).
- **The Wiggers "Out of priority" pool** (A2, A3, B2-B5, C1, C2,
  D1-D5, E1-E3, F1, F2, F4, G1, G4, H2-counting, H3-classifier) —
  these are deprioritised but still available; they belong in the
  active Wiggers register until explicitly rejected.
- **Methodology revisions** (crash_v1 percentile → absolute threshold,
  activity-labels v1 → v3.1, etc.) — these are spec changes
  documented in their own methodology MDs, not hypothesis rejections.
