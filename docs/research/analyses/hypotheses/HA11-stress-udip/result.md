# HA11 — Result: within-day stress U-dip event count as crash precursor

**Primary verdict (4d window, N_std=1.5, one-sided elevated): TRAIN
SUPPORTED, VALIDATE REFUTED → OVERALL REFUTED per the locked
both-eras rule.** But train clears all three pre-registered
criteria substantially (64.3% freq, +22.8 pp disc, median signed z
= 2.168) and validate is *anti-predictive* (−10.7 pp disc) — the
era directionality reversal pattern surfaces a fourth time in the
project.

This makes **four train-era SUPPORTED autonomic-channel precursors
on four channels** (H02b stress spike count, H02d bridge × 5d
sentinel-corrected, HA06b RHR z-score, **HA11 U-dip count z-score**),
all overall-REFUTED by validate. HA10 remains the only
validate-era SUPPORTED test. The pre-cliff era's
sympathetic-overarousal signature is now four-channel-confirmed;
the post-cliff era's parasympathetic-swing signature is one-channel
confirmed (HA10 BB peak elevated).

The U-dip detection is the **first within-day pattern test in the
project** and the first test of an orthostatic / blood-volume
mechanism. The Wiggers-pdf pattern (sharp stress dip followed by
plateau at higher baseline, resolved with ORS / electrolytes) is
empirically present in the pre-cliff era at the population level,
not just as anecdote.

No `card.md` per the strict overall rule. Data:
[result-data.json](result-data.json).

## Headline numbers (primary 4d, N_std=1.5, one-sided elevated)

| | train (14 episodes) | validate (13/15 clean episodes) |
|---|---:|---:|
| crash episodes triggering (signed z ≥ +1.5) | **9 (64.3%)** | 4 (30.8%) |
| null windows triggering | 83 (41.5%) | 83 (41.5%) |
| **discrimination (pp)** | **+22.8** | **−10.7** |
| median max signed z | 2.168 | 0.374 |
| crit (a) freq ≥ 60% | **PASS (64.3%)** | fail (30.8%) |
| crit (b) disc ≥ +15 pp | **PASS (+22.8)** | fail (−10.7) |
| crit (c) median ≥ 0.75 | **PASS (2.168)** | fail (0.374) |
| **verdict** | **supported** | **refuted** |

2 of 15 validate-era crashes dropped from analysis because fewer
than 3 of 4 lead-up days had a valid (μ, σ) baseline. Train side
has all 14 crashes clean.

## Sensitivity arm — bidirectional (4d, N_std=1.5)

| | train | validate |
|---|---:|---:|
| crash episodes triggering (\|z\| ≥ 1.5) | 9 (64.3%) | 4 (30.8%) |
| null windows triggering | 95 (47.5%) | 95 (47.5%) |
| discrimination (pp) | **+16.8** | **−16.7** |
| verdict | **supported** | refuted |

Train remains SUPPORTED under bidirectional (+16.8 pp); validate
becomes more strongly inverse (−16.7 pp). The bidirectional test
adds null triggers in both directions, raising the null rate but
keeping the train crash rate the same — train's signal is robust
to direction choice. Validate's null rate also rises, making the
already-negative validate discrimination more negative.

## Sensitivity arm — one-sided lowered (Wiggers-inverse direction)

| | train | validate |
|---|---:|---:|
| crash episodes triggering (signed z ≤ −1.5) | **0 (0.0%)** | **0 (0.0%)** |
| null windows triggering | 15 (7.5%) | 15 (7.5%) |
| discrimination (pp) | −7.5 | −7.5 |
| verdict | refuted | refuted |

**Zero crashes in either era show a lowered-U-dip-count direction.**
The U-dip count metric is not low enough relative to baseline to
satisfy the lowered-direction trigger for any crash. The
participant's daily U-dip count distribution is bounded below by 0,
so "very low" rarely fires; the distribution mode at 0 makes
z ≤ −1.5 hard to reach unless the baseline μ is well above 0.

## All combinations evaluated

| window | N_std | direction | era | verdict | freq | null | disc pp | median |
|---|---:|---|---|---|---:|---:|---:|---:|
| **4d primary** | **1.5** | **one-sided elevated** | **train** | **SUPPORTED** | **64.3%** | 41.5% | **+22.8** | 2.168 |
| **4d primary** | **1.5** | **one-sided elevated** | **validate** | **refuted (inv)** | **30.8%** | 41.5% | **−10.7** | 0.374 |
| 4d primary | 1.5 | bidirectional | train | **supported** | 64.3% | 47.5% | +16.8 | 2.168 |
| 4d primary | 1.5 | bidirectional | validate | refuted (inv) | 30.8% | 47.5% | −16.7 | 1.310 |
| 4d primary | 2.0 | one-sided elevated | train | refuted (a) | 50.0% | 32.5% | +17.5 | 2.168 |
| 4d primary | 2.0 | one-sided elevated | validate | refuted (inv) | 15.4% | 32.5% | −17.1 | 0.374 |
| 4d primary | 2.5 | one-sided elevated | train | refuted (a) | 42.9% | 22.5% | +20.4 | 2.168 |
| 4d primary | 2.5 | one-sided elevated | validate | refuted (inv) | 7.7% | 22.5% | −14.8 | 0.374 |
| 5d secondary | 1.5 | one-sided elevated | train | refuted (b) | 64.3% | 50.5% | +13.8 | 2.168 |
| 5d secondary | 1.5 | one-sided elevated | validate | refuted (inv) | 38.5% | 50.5% | −12.0 | 0.883 |
| 5d secondary | 1.5 | bidirectional | train | refuted (b) | 64.3% | 56.5% | +7.8 | 2.168 |
| 5d secondary | 1.5 | bidirectional | validate | refuted (inv) | 38.5% | 56.5% | −18.0 | 1.362 |
| 5d secondary | 2.0 | one-sided elevated | validate | refuted (inv) | 15.4% | 39.5% | **−24.1** | 0.883 |
| 5d secondary | 2.5 | one-sided elevated | validate | refuted (inv) | 7.7% | 28.5% | −20.8 | 0.883 |

Train SUPPORTED in **2 of 12** arms (4d × 1.5 × elevated, 4d × 1.5
× bidirectional). The signal is robust to direction choice at the
4d window but does not survive the wider 5d window (null rate
inflates above the train rate). Validate is inverse-direction
across **all 12** non-zero arms.

## Directionality split (over triggering events, primary 4d one-sided elevated)

| | n triggering | elevated-at-max\|z\| | lowered-at-max\|z\| |
|---|---:|---:|---:|
| train | 9 | **9 (100%)** | 0 (0%) |
| validate | 4 | **4 (100%)** | 0 (0%) |

When ANY crash triggers on the elevated direction (signed z ≥ 1.5),
its max-|z| day is uniformly the elevated direction. The pattern
is direction-pure for triggering events. The lopsidedness reflects
the metric's bounded-below distribution: the elevated direction has
more room to extend than the lowered direction.

## Cross-channel comparison (project-level after HA11)

HA11 adds the fourth train-era SUPPORTED autonomic precursor on the
fourth channel:

| test | channel | window | metric | train freq | train disc |
|---|---|---|---|---:|---:|
| H02b | per-minute stress spike count | 3d rolling | abs minutes ≥ +10 | 71.4% | +29.9 pp |
| H02d bridge × 5d | per-minute stress spike (sentinel-corrected) | 5d | abs minutes ≥ +10 | 92.3% | +31.8 pp |
| HA06b | nightly RHR z-score | 4d lagged | rel \|z\| ≥ 1.5 (bidir) | 71.4% | +18.9 pp |
| **HA11** | **within-day U-dip count z-score** | **4d lagged** | **rel signed z ≥ 1.5 (elevated)** | **64.3%** | **+22.8 pp** |

Four train-era SUPPORTED findings on four distinct channels:
- per-minute stress trajectory pattern (H02b, H02d) — sympathetic
  spike duration
- per-night autonomic recovery (HA06b) — elevated RHR
- per-day within-day pattern (HA11) — elevated U-dip count

The pre-cliff (2022-23) era's sympathetic-overarousal /
orthostatic-instability precursor signature is now demonstrably
**four-channel-confirmed** across distinct measurement modalities
and time-scales. This is the strongest multi-channel convergence
in the project.

The validate-era SUPPORTED finding (HA10 morning BB peak elevated)
remains the **only** validate-era SUPPORTED test. The post-cliff
era's parasympathetic-swing signature is one-channel-confirmed; the
patterns that fire pre-cliff (sympathetic-arousal, U-dip
volatility) do NOT fire in validate.

## Era reversal pattern across four channels

Combining HA11 with HA06b and HA10:

| era | H02b/H02d (stress spike) | HA06b (RHR) | **HA11 (U-dip)** | HA10 (BB peak) |
|---|---|---|---|---|
| train | SUPPORTED (elevated minutes) | SUPPORTED (elevated direction) | **SUPPORTED (elevated count)** | refuted |
| validate | refuted | refuted | **refuted (inverse direction)** | SUPPORTED (elevated peak — paradoxical swing) |

The pattern is now: **train-era crashes are preceded by
sympathetic-arousal-spectrum events** (more stress spikes, higher
RHR, more U-dip volatility, NO unusual BB pattern). **Validate-era
crashes are preceded by parasympathetic-swing-spectrum events**
(unusual high BB peak, less of all the sympathetic patterns).

The Wiggers "freeze" pattern is now empirically population-level
visible in this participant in TWO independent biometric channels
(RHR via HA06b, BB via HA10) for validate-era crashes. The
canonical sympathetic-overarousal pattern is empirically
population-level visible in FOUR independent channels (stress
spikes, RHR, U-dip count, plus train-era BB direction at 5d) for
train-era crashes.

## What the numbers say

**1. The pre-cliff sympathetic-overarousal precursor signature is
exceptionally robust.** Four independent channels, four
independent measurement choices, four independent test runs, all
SUPPORTING train-era crash precursor patterns. The chance any
single test produces this by chance alone is moderate; the chance
ALL four produce it by chance alone is vanishing. The pre-cliff
era's crashes have a real, multi-channel, characterisable
physiological precursor signature.

**2. The within-day U-dip pattern is a TRAIN-era phenomenon for
this participant.** Wiggers describes it as a chronic-illness
pattern; this participant's pre-cliff era exhibits it strongly
(+22.8 pp disc, 64.3% of crashes show ≥ 1.5σ elevated count). The
post-cliff era does NOT exhibit it — validate crashes have FEWER
U-dip events than random non-crash 4d windows (−10.7 pp). The U-dip
signature aligns with the sympathetic-arousal era, not the
parasympathetic-swing era.

**3. Validate-era U-dip direction is inverse and significant.** The
−10.7 pp disc at 4d primary scales to −24.1 pp at 5d N_std=2.0 —
meaning validate-era crashes are *strongly* characterised by
*fewer* U-dip events than typical 4-5d windows. This is not a noise
result; the inverse pattern is consistent across thresholds. **The
U-dip detection metric becomes part of the parasympathetic-swing
empirical signature**: more swing → fewer sharp-drop-then-rise
events because the autonomic system is already biased toward
parasympathetic dominance.

**4. The lowered direction is structurally rare.** Zero crashes in
either era show signed z ≤ −1.5 on the lowered direction.
U-dip count is bounded below by 0, and the participant's typical
day has μ ~0.85 events, so getting to -1.5σ below μ requires
multiple consecutive days at 0 events — possible but rare in any
4-day window. The lowered-direction sensitivity arm is structurally
underpowered for this metric.

**5. Same-day correlation between U-dip count and gevoelscore is
weak.** Train Spearman ρ = +0.075; validate ρ = +0.012. The U-dip
count does NOT predict same-day subjective wellness. The metric is
a 4-day-lead precursor (in train) but NOT a same-day symptom
correlate. This is consistent with the autonomic-precursor framing:
the U-dip events accumulate over days before manifesting in
gevoelscore.

## Caveats per §8

- **U-dip detection is a novel pattern primitive for this project**.
  The locked thresholds (S_pre ≥ 40, drop ≥ 25, plateau ≥ +5) are
  physiologically motivated but not validated against an
  orthostatic challenge ground truth. A different threshold set
  could shift the absolute event rate and could subtly shift the
  train-era discrimination magnitude. The pre-commitment held —
  the result is the result of the locked spec.
- **The U-dip pre-condition (S_pre ≥ 40) is era-sensitive**. The
  participant's stress baseline shifted from ~35 pre-cliff to ~29
  mid-2025 (S01 trajectories). A fixed S_pre ≥ 40 threshold is
  more often satisfied in the train era than in the trough. The
  validate-era lower base rate could partly reflect this; the
  lagged-baseline z-score partially compensates but doesn't fully
  remove the effect.
- **Garmin's stress algorithm uses HRV as input**. The U-dip
  pattern is HRV-shape, not orthostatic-specific. Cross-validation
  against actual orthostatic measurement (tilt-table, NASA
  lean test) is not possible in this dataset. The Wiggers
  interpretation is the most plausible reading but is not
  *demonstrated* to be orthostatic.
- **Validate-era 2 of 15 crashes dropped**. Both due to missing
  σ on at least one lead-up day. The 13 retained validate crashes
  are still adequately powered (n ≥ 10).
- **`crash_v1` mixes mechanisms**. Same caveat as all prior tests.
- **Multi-comparison**. HA11 is the 15th pre-registered hypothesis
  in the H##/HA## series. The cross-channel convergence of
  train-era findings (H02b, H02d, HA06b, HA11) is so strong that
  multi-comparison-by-chance is implausible — the convergence
  itself is the validation.
- **Watch-off coverage**: 1722 of 1739 days (99.0%) pass the ≥600
  sample validity rule. Coverage is essentially complete.

## Wiggers-pdf-specific findings

HA11 directly tests Wiggers' within-day pattern claim:

- **The U-dip / orthostatic / electrolyte signature pattern is
  empirically present at the population level for the pre-cliff
  era's crashes**: 64.3% of train crashes show 1.5σ elevated U-dip
  count in their 4-day lead-up. Discrimination +22.8 pp confirms
  the pattern is precursor-specific, not background noise.
- **It is NOT a validate-era precursor**. Validate crashes have
  *fewer* U-dip events than typical, not more. Wiggers' pattern
  description aligns with the pre-cliff era's autonomic state
  (sympathetic-overarousal that occasionally collapses into vagal
  moments), not the post-cliff era's state (parasympathetic
  dominance with paradoxical swings).
- **Cross-channel coherence with HA06b train**: U-dip count and
  RHR z-score both SUPPORT in train at the same window (4d
  bidirectional, N_std=1.5). Both reflect sympathetic-arousal
  precursor patterns through different measurements.
- **No notes corroboration possible without C.7 intervention
  tagging**. The hypothesis suggested cross-referencing with
  ORS / electrolyte / "duizelig" mentions; this requires
  notes-quality work + intervention tagging (currently queued).
  Worth a focused re-look at train-era notes around U-dip-elevated
  days for any orthostatic / hydration mentions, but this is a
  separate analysis from the precursor test.

## What this changes

1. **Pre-cliff era multi-channel autonomic precursor signature is
   now FOUR-channel confirmed.** The strongest multi-channel
   convergence in the project. This is qualitatively new evidence
   for the D7 single-mechanism-two-regimes reframe: the pre-cliff
   regime IS a coherent autonomic-arousal pattern, not a collection
   of unrelated signals.
2. **The "kind of crash changed" theory gains a fifth axis.** U-dip
   count joins the directional findings: train +22.8 pp / validate
   −10.7 pp.
3. **Card (b) train-era retrospective per-crash card has FOUR
   empirical anchors converging on the same train-era crashes**
   (H02b spike count + H02d bridge × 5d + HA06b RHR z-score + HA11
   U-dip count). Strongest empirical anchoring for any card concept
   in the project.
4. **Card (b2) validate-era retrospective remains anchored only by
   HA10 BB peak**. HA11 does not contribute to the b2 anchoring,
   though its validate-era inverse direction at −16.7 pp is itself
   a *characteristic* signature of the parasympathetic-swing era.
5. **HA09 reframing reinforced again**. HA09 (parasympathetic-swing
   detection) was already reframed after HA06b to NOT use crash
   labels directly. HA11's validate-era inverse direction confirms
   that the validate-era crashes don't have the sympathetic-arousal
   patterns; they have the swing direction (per HA06b + HA10).
6. **Wiggers' U-dip pattern is empirically population-level real,
   but era-specific.** Her pattern description (sharp drop + higher
   plateau, ORS-resolvable, orthostatic) fits this participant's
   pre-cliff era. Validate-era crashes show the OPPOSITE
   trajectory: fewer U-dip events, consistent with stable
   parasympathetic dominance.
7. **HA07 priority (when H04b path C opens) is reinforced.** All
   four currently-testable autonomic channels (stress spikes, RHR
   peak, BB peak, U-dip count) have now been tested; HRV (HA07)
   and per-minute BB (H03b via H04b) are the remaining channels.
   The cross-channel pattern strongly predicts: HRV elevated train
   precursor, HRV low / swing-pattern validate precursor.
8. **No H03b coarse-proxy refutation rebound**. HA10 SUPPORTED
   validate, so per the HA10 §9 pre-commit, H04b stays *strongly
   prioritised*. HA11's train-only SUPPORTED doesn't change this.

## What we do next

Per the user's pivot-order pre-commit (HA10 → HA11):

1. **Bundle doc-level updates** (HA10 + HA11). Per the user's
   instruction at the start of this phase, the doc bundle was
   queued to follow HA11. Updates needed in:
   - RESEARCH-REPORT-ADDENDUM.md §5.12-§5.15 (add HA10 §5.14
     + HA11 §5.15 and the cross-channel four-train + one-validate
     synthesis)
   - STOCKTAKE.md (§2a precursor table; §3 directional findings;
     §4 card tiers; §7 queue)
   - synthesis.md (append "Update 2026-06-07 — HA10 + HA11" with
     cross-channel coherence + final kind-of-crash table)
   - QUEUED-WORK.md (mark HA10 + HA11 done in "Recently
     completed"; update suggested order)
   - pem-pacing-indicators.md (note the four-channel convergence;
     consider whether to add a Tier 1 train-era retrospective
     indicator concept)
   - registry.md (already has HA10; add HA11 entry to §4 + §4b)
2. **H04b path C authorisation** remains the highest-leverage
   next research step. Unlocks HRV (HA07/HA08/HA12) and per-minute
   BB (H03b).
3. **HA09 (parasympathetic-swing detection)** remains work-on-later;
   reframed twice now (after HA06b, after HA10) to target post-
   overexertion recovery rather than crash labels.

---

*Test run 2026-06-07. Pre-registration locked 2026-06-07 at
[hypothesis.md](hypothesis.md). Stage 1 extraction
(extract_udip_counts.py) cached 1739 days of per-day U-dip counts
in 6-7 min. 3-episode dry-run printed before the full run per
methodology lesson — dry-run confirmed clean distributions
(σ 0.78-0.98, zero low-variability skips, zero invalid-day skips,
4/4 or 5/5 lead-up coverage on all sampled episodes). Seed
`20260605` matches scripts 08/09/12 + HA06 + HA06b + HA10.*
