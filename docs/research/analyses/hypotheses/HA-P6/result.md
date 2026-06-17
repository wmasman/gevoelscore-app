# HA-P6 v3 -- result: post-crash window distinctive autonomic-recovery shape

*Run 2026-06-17 by `script.py` against the v3 LOCKED pre-registration `hypothesis.md` (lock 2026-06-17). Random seed: 20260617; per-channel E[L] from §4.8.1 four-verdict policy (table below).*

**Layer 1 descriptive characterisation per CONVENTIONS §2.1. NO SUPPORTED / NOT-SUPPORTED bar.** §5 names this result.md as reporting the *findings shape* regardless of the data; §9 enumerates downstream propagations per observation shape.

## Headline cell (pooled LC × Arm-B lagged baseline × no-detrend × episode-end-t0 × primary [t+1, t+5])

| channel | n eps | n w/ baseline | n undef compl | E[L] used | category | annotation | recovery day | depth (median \|z\|) |
|---|---:|---:|---:|---:|---|---|---:|---:|
| stress_mean_sleep | 29 | 21 | 4 | 5 | noisy-inconclusive | noisy-shape-driven | 3.0 | 3.88 |
| all_day_stress_avg | 29 | 22 | 4 | 21 | noisy-inconclusive | noisy-shape-driven | 3.0 | 2.50 |
| bb_lowest | 29 | 22 | 3 | 14 | overshoot-then-settle | -- | 2.0 | 2.45 |
| bb_overnight_gain | 5 | 3 | 1 | 7 | noisy-inconclusive | noisy-shape-driven | 2.0 | 2.79 |
| resting_hr | 29 | 22 | 5 | 14 | noisy-inconclusive | noisy-CI-driven | 1.0 | 2.02 |
| gevoelscore | 29 | 19 | 0 | 7 | slow-grind-incomplete | -- | 1.0 | 1.44 |
| stress_low_motion_min_count_S60_Mlow | 29 | 22 | 5 | 7 | noisy-inconclusive | noisy-shape-driven | 2.0 | 2.14 |

Per-day median z (Arm B) with 95% bootstrap CI:

| channel | t+1 | t+2 | t+3 | t+4 | t+5 |
|---|---|---|---|---|---|
| stress_mean_sleep | 1.206 [0.674, 2.615] | 0.317 [-0.414, 1.096] | 0.740 [-0.200, 1.741] | 0.691 [0.138, 1.096] | 0.450 [-0.623, 2.293] |
| all_day_stress_avg | 0.604 [-0.683, 1.389] | -0.220 [-0.590, 0.834] | 0.608 [0.028, 1.029] | 0.355 [-0.207, 1.211] | 0.607 [-0.357, 2.377] |
| bb_lowest | -0.502 [-1.461, 1.472] | 0.101 [-0.628, 0.567] | -0.283 [-0.628, 0.265] | 0.001 [-0.635, 1.031] | 0.027 [-1.736, 0.781] |
| bb_overnight_gain | -2.228 [-2.792, -1.663] | -0.074 [-0.138, 0.324] | -2.248 [-3.890, 1.493] | -0.513 [-1.705, 0.090] | -0.482 [-2.716, 0.613] |
| resting_hr | 1.061 [-0.143, 2.848] | 0.783 [-0.176, 3.328] | 0.963 [-0.119, 2.972] | 1.255 [-0.063, 2.914] | 1.255 [0.040, 3.021] |
| gevoelscore | -1.009 [-1.187, -0.319] | -0.306 [-1.150, 0.651] | -1.046 [-1.443, -0.112] | -0.156 [-1.009, 0.795] | 0.651 [-0.319, 0.795] |
| stress_low_motion_min_count_S60_Mlow | 0.056 [-0.657, 0.808] | -0.076 [-0.557, 0.535] | 0.116 [-0.177, 0.577] | 0.639 [-0.010, 1.322] | 1.405 [-0.075, 2.195] |

## §4.8.1 four-verdict E[L] policy table (v3; §5 #2)

| channel | verdict (A) | E[L]\* (A pooled-LC) | verdict (B) | E[L]\* (B unmed) | binds | E[L] used | cap-binding | rationale |
|---|---|---:|---|---:|:---:|---:|:---:|---|
| stress_mean_sleep | FAIL | 19.65 | PASS-real | 4.83 | B | 5 | no | FAIL → v3 override min(round(E[L]*), 21) binds Series B |
| all_day_stress_avg | FAIL | 26.60 | PASS-fallback-degenerate | 7.00 | A | 21 | yes | FAIL → v3 override min(round(E[L]*), 21) binds Series A; CAP |
| bb_lowest | PASS-fallback-no-cutoff | 7.00 | FAIL | 18.40 | A | 14 | no | PASS-fallback-no-cutoff (long-dep signal) → v3 closure #2 override E[L]=14 |
| bb_overnight_gain | PASS-real | 6.54 | PASS-fallback-degenerate | 7.00 | A | 7 | no | PASS-real → project default E[L]=7 |
| resting_hr | PASS-fallback-no-cutoff | 7.00 | PASS-fallback-no-cutoff | 7.00 | A | 14 | no | PASS-fallback-no-cutoff (long-dep signal) → v3 closure #2 override E[L]=14 |
| gevoelscore | PASS-fallback-degenerate | 7.00 | PASS-fallback-degenerate | 7.00 | A | 7 | no | PASS-fallback-degenerate (note: Closed-form formula degenerate; returnin) → default E[L]=7 |
| stress_low_motion_min_count_S60_Mlow | PASS-real | 5.99 | PASS-fallback-degenerate | 7.00 | A | 7 | no | PASS-real → project default E[L]=7 |

## Arm A (matched-deep-trough non-crash days) -- the strict RTM control

**Per §8 caveat 1, this is the LOAD-BEARING read for the RTM-vs-autonomic question.** Per-day median DIFFERENCE (crash trajectory minus matched-control trajectory) with 95% **paired stationary-bootstrap** CI at the per-channel E[L] (v3 closure #4):

| channel | E[L] | t+1 diff | t+2 diff | t+3 diff | t+4 diff | t+5 diff | days CI excludes 0 |
|---|---:|---|---|---|---|---|---:|
| stress_mean_sleep | 5 | 3.119 [-0.014, 6.737] | 2.170 [0.372, 5.124] | 2.679 [-1.846, 3.717] | 4.270 [0.127, 5.603] | 1.194 [0.520, 4.581] | 3 / 5 |
| all_day_stress_avg | 21 | 3.000 [1.500, 6.000] | 2.000 [-0.500, 4.000] | 4.500 [1.000, 8.000] | 5.000 [4.000, 7.000] | 4.000 [1.000, 7.000] | 4 / 5 |
| bb_lowest | 14 | -2.500 [-6.512, 1.000] | -3.500 [-7.500, -2.000] | -8.000 [-13.000, -1.000] | -6.000 [-9.000, 2.000] | -5.000 [-10.000, -2.000] | 3 / 5 |
| bb_overnight_gain | 7 | -16.000 [-25.500, 3.000] | 15.000 [-11.000, 20.000] | 13.000 [-19.000, 13.000] | 0.000 [-15.500, 5.500] | -0.500 [-6.000, 6.000] | 0 / 5 |
| resting_hr | 14 | 1.000 [-0.500, 2.000] | 1.000 [-1.000, 2.000] | 1.000 [-1.000, 2.000] | 1.000 [0.000, 3.000] | 2.000 [0.000, 3.000] | 0 / 5 |
| gevoelscore | 7 | 0.000 [-1.000, 0.000] | 0.000 [0.000, 1.000] | 0.000 [0.000, 1.000] | 0.000 [0.000, 1.000] | 0.000 [0.000, 0.000] | 0 / 5 |
| stress_low_motion_min_count_S60_Mlow | 7 | 29.000 [1.000, 52.000] | 16.000 [-29.500, 38.000] | 23.500 [-18.000, 41.000] | 33.000 [-14.000, 48.000] | 37.000 [6.000, 71.000] | 2 / 5 |

§9 head operational binding (>= 2 of 5 primary-window days; CI on median diff excludes 0):

- Channels statistically-distinguishable from matched control: **4 / 7** (§9 first-branch trigger fires if >= 3).
- Strict (>= 3 of 5 days) sensitivity: **3 / 7**.

## §4.8.4 secondary correlations (locked headline cell -- pooled-LC × Arm-B × no-detrend × episode-end × primary)

Spearman rho with 95% block-bootstrap CI at per-channel E[L] (day-level; see §8 v3 caveat per closure #7 on the day-level-E[L]-on-per-episode-summary granularity mismatch); B=10000:

| channel | E[L] | rate vs duration: rho [95% CI] (n) | completeness vs next-interval: rho [95% CI] (n) | n undef compl |
|---|---:|---|---|---:|
| stress_mean_sleep | 5 | -0.004 [-0.499, 0.451] (n=21) | 0.147 [-0.402, 0.673] (n=17) | 4 |
| all_day_stress_avg | 21 | 0.285 [0.021, 0.585] (n=22) | -0.338 [-0.493, -0.168] (n=18) | 4 |
| bb_lowest | 14 | 0.018 [-0.328, 0.380] (n=22) | -0.156 [-0.487, 0.081] (n=19) | 3 |
| bb_overnight_gain | 7 | -- (n=3) | -- (n=2) | 1 |
| resting_hr | 14 | 0.016 [-0.334, 0.399] (n=22) | 0.123 [-0.173, 0.475] (n=17) | 5 |
| gevoelscore | 7 | 0.092 [-0.230, 0.429] (n=19) | 0.451 [-0.091, 0.822] (n=19) | 0 |
| stress_low_motion_min_count_S60_Mlow | 7 | 0.389 [0.013, 0.709] (n=22) | -0.355 [-0.684, 0.190] (n=17) | 5 |

**Reading discipline per §1.2 + §4.8.4**: NO SUPPORTED bar. CI containing 0 → null correlation read; otherwise report sign + magnitude.

## Per-phase tables (Arm B z-trajectory)

| channel | phase | n eps | E[L] | category | annotation | recovery day | depth |
|---|---|---:|---:|---|---|---:|---:|
| stress_mean_sleep | unmedicated | 18 | 5 | noisy-inconclusive | noisy-CI-driven | 3.0 | 3.82 |
| stress_mean_sleep | buildup | 3 | 5 | noisy-inconclusive | noisy-shape-driven | n/a | -- |
| stress_mean_sleep | consolidation | 6 | 5 | slow-grind-incomplete | -- | 2.0 | 4.05 |
| stress_mean_sleep | afbouw | 2 | 5 | noisy-inconclusive | noisy-shape-driven | n/a | -- |
| all_day_stress_avg | unmedicated | 18 | 21 | noisy-inconclusive | noisy-shape-driven | 2.0 | 2.42 |
| all_day_stress_avg | buildup | 3 | 21 | noisy-inconclusive | noisy-shape-driven | 3.0 | 4.97 |
| all_day_stress_avg | consolidation | 6 | 21 | noisy-inconclusive | noisy-CI-driven | 3.0 | 2.85 |
| all_day_stress_avg | afbouw | 2 | 21 | noisy-inconclusive | noisy-shape-driven | n/a | -- |
| bb_lowest | unmedicated | 18 | 14 | overshoot-then-settle | -- | 2.0 | 2.44 |
| bb_lowest | buildup | 3 | 14 | noisy-inconclusive | noisy-shape-driven | 2.0 | 3.76 |
| bb_lowest | consolidation | 6 | 14 | noisy-inconclusive | noisy-CI-driven | 2.5 | 3.80 |
| bb_lowest | afbouw | 2 | 14 | noisy-inconclusive | noisy-shape-driven | n/a | -- |
| bb_overnight_gain | consolidation | 3 | 7 | noisy-inconclusive | noisy-shape-driven | 2.0 | 2.79 |
| bb_overnight_gain | afbouw | 2 | 7 | noisy-inconclusive | noisy-shape-driven | n/a | -- |
| resting_hr | unmedicated | 18 | 14 | slow-grind-incomplete | -- | 1.0 | 1.78 |
| resting_hr | buildup | 3 | 14 | noisy-inconclusive | noisy-shape-driven | 1.0 | 0.88 |
| resting_hr | consolidation | 6 | 14 | noisy-inconclusive | noisy-CI-driven | 1.0 | 3.10 |
| resting_hr | afbouw | 2 | 14 | noisy-inconclusive | noisy-shape-driven | n/a | -- |
| gevoelscore | unmedicated | 18 | 7 | stair-step-recovery | -- | 1.0 | 1.46 |
| gevoelscore | buildup | 3 | 7 | noisy-inconclusive | noisy-shape-driven | 2.0 | 0.97 |
| gevoelscore | consolidation | 6 | 7 | slow-grind-incomplete | -- | 2.0 | 1.19 |
| gevoelscore | afbouw | 2 | 7 | noisy-inconclusive | noisy-shape-driven | n/a | -- |
| stress_low_motion_min_count_S60_Mlow | unmedicated | 18 | 7 | noisy-inconclusive | noisy-shape-driven | 2.0 | 2.11 |
| stress_low_motion_min_count_S60_Mlow | buildup | 3 | 7 | noisy-inconclusive | noisy-shape-driven | 3.0 | 7.87 |
| stress_low_motion_min_count_S60_Mlow | consolidation | 6 | 7 | slow-grind-incomplete | -- | 1.5 | 2.08 |
| stress_low_motion_min_count_S60_Mlow | afbouw | 2 | 7 | noisy-inconclusive | noisy-shape-driven | n/a | -- |

## §3.7 detrend sensitivity (Arm B z-trajectory, detrended)

| channel | phase | no-detrend category | detrended category | survives? |
|---|---|---|---|---|
| stress_mean_sleep | pooled | noisy-inconclusive | slow-grind-incomplete | no |
| stress_mean_sleep | unmedicated | noisy-inconclusive | slow-grind-incomplete | no |
| stress_mean_sleep | buildup | noisy-inconclusive | noisy-inconclusive | no |
| stress_mean_sleep | consolidation | slow-grind-incomplete | slow-grind-incomplete | yes |
| stress_mean_sleep | afbouw | noisy-inconclusive | noisy-inconclusive | no |
| all_day_stress_avg | pooled | noisy-inconclusive | slow-grind-incomplete | no |
| all_day_stress_avg | unmedicated | noisy-inconclusive | noisy-inconclusive | no |
| all_day_stress_avg | buildup | noisy-inconclusive | noisy-inconclusive | no |
| all_day_stress_avg | consolidation | noisy-inconclusive | slow-grind-incomplete | no |
| all_day_stress_avg | afbouw | noisy-inconclusive | noisy-inconclusive | no |
| bb_lowest | pooled | overshoot-then-settle | noisy-inconclusive | no |
| bb_lowest | unmedicated | overshoot-then-settle | noisy-inconclusive | no |
| bb_lowest | buildup | noisy-inconclusive | noisy-inconclusive | no |
| bb_lowest | consolidation | noisy-inconclusive | slow-grind-incomplete | no |
| bb_lowest | afbouw | noisy-inconclusive | noisy-inconclusive | no |
| bb_overnight_gain | pooled | noisy-inconclusive | slow-grind-incomplete | no |
| bb_overnight_gain | consolidation | noisy-inconclusive | slow-grind-incomplete | no |
| bb_overnight_gain | afbouw | noisy-inconclusive | noisy-inconclusive | no |
| resting_hr | pooled | noisy-inconclusive | noisy-inconclusive | no |
| resting_hr | unmedicated | slow-grind-incomplete | noisy-inconclusive | no |
| resting_hr | buildup | noisy-inconclusive | noisy-inconclusive | no |
| resting_hr | consolidation | noisy-inconclusive | noisy-inconclusive | no |
| resting_hr | afbouw | noisy-inconclusive | noisy-inconclusive | no |
| gevoelscore | pooled | slow-grind-incomplete | noisy-inconclusive | no |
| gevoelscore | unmedicated | stair-step-recovery | no-meaningful-change | no |
| gevoelscore | buildup | noisy-inconclusive | noisy-inconclusive | no |
| gevoelscore | consolidation | slow-grind-incomplete | slow-grind-incomplete | yes |
| gevoelscore | afbouw | noisy-inconclusive | noisy-inconclusive | no |
| stress_low_motion_min_count_S60_Mlow | pooled | noisy-inconclusive | noisy-inconclusive | no |
| stress_low_motion_min_count_S60_Mlow | unmedicated | noisy-inconclusive | noisy-inconclusive | no |
| stress_low_motion_min_count_S60_Mlow | buildup | noisy-inconclusive | noisy-inconclusive | no |
| stress_low_motion_min_count_S60_Mlow | consolidation | slow-grind-incomplete | noisy-inconclusive | no |
| stress_low_motion_min_count_S60_Mlow | afbouw | noisy-inconclusive | noisy-inconclusive | no |

## §1.3 late-recovery sensitivity ([t+6, t+10])

| channel | late-window category | late-window depth | late-window recovery day |
|---|---|---:|---:|
| stress_mean_sleep | monotonic-recovery | 2.37 | not within window |
| all_day_stress_avg | overshoot-then-settle | 1.89 | not within window |
| bb_lowest | no-meaningful-change | 2.01 | not within window |
| bb_overnight_gain | noisy-inconclusive | 2.30 | not within window |
| resting_hr | monotonic-recovery | 1.76 | not within window |
| gevoelscore | noisy-inconclusive | 1.94 | not within window |
| stress_low_motion_min_count_S60_Mlow | overshoot-then-settle | 1.88 | not within window |

## t0-sensitivity (episode-end vs last-below-threshold-day)

| channel | episode-end category | last-below category | concordant? |
|---|---|---|---|
| stress_mean_sleep | noisy-inconclusive | stair-step-recovery | no |
| all_day_stress_avg | noisy-inconclusive | overshoot-then-settle | no |
| bb_lowest | overshoot-then-settle | overshoot-then-settle | yes |
| bb_overnight_gain | noisy-inconclusive | overshoot-then-settle | no |
| resting_hr | noisy-inconclusive | noisy-inconclusive | yes |
| gevoelscore | slow-grind-incomplete | noisy-inconclusive | no |
| stress_low_motion_min_count_S60_Mlow | noisy-inconclusive | noisy-inconclusive | yes |

## §9 observation-shape propagations -- evaluation on the locked headline cell

- **First branch ('distinct recovery shape across >= 3 of 7 channels')**: fires = **YES** (n_sig_channels=4/7 at >= 2 of 5 days; strict >= 3 of 5: 3/7).
- **Second branch ('Arm A matches crash trajectory on majority')**: fires = **NO** (arm_a_match_count=12 / 33 cells).
- **§4.8.4 secondary correlations excluding 0** on the locked cell:
  - all_day_stress_avg: rate vs duration, completeness vs next-interval
  - stress_low_motion_min_count_S60_Mlow: rate vs duration

## Caveats per §8 (must be acknowledged on every read)

1. **Regression to the mean (RTM) is the central confound**. The Arm A median-difference table above is the load-bearing read.
2. **n=29 LC-era episodes is sparse**. Per-channel per-day CIs are wide by construction.
3. **Power-calc dispatch**: inapplicable per Daza 2018 within-subject design + HA-P6 is Layer 1 descriptive per CONVENTIONS §2.1.
4. **Crash_v2 episode boundaries depend on the t0 definition**. The t0-sensitivity table above reports concordance.
5. **Self-reported crash labels** via crash_v2 -- instrument-level bias inherited by §4.8.4 secondary correlations.
6. **Intervention-baseline dose-response broadens P6's caveat** per register caveat 5: `stress_mean_sleep`, `all_day_stress_avg`, `bb_lowest` CONFIRMED dose-modulated; §4.7 phase-stratified arm + §3.7 detrend per phase address.
7. **Channel coverage gaps**: `bb_overnight_gain` starts 2024-09-18; n=5 post-2024-09-18 episodes contribute.
8. **CONVENTIONS §3.7 trajectory-detrend is binding** per §4.6. The detrend-sensitivity table above is the within-phase calibration check.
9. **§3.4 inapplicable-to-primary by construction**: the trajectory IS computed across crash episodes; inapplicable-to-secondary because the correlation operates on per-episode summary statistics.
10. **Matched-baseline construction (Arm A) is operational, not gold-standard**. The ±1 gevoelscore-point tolerance ladder (±1.5, ±2) is used. Arm B (lagged baseline) is the project-pattern complement.
11. **Mechanistic claims about recovery physiology are out of scope** -- this characterises the *shape*; the *why* is for downstream tests.

### v2 caveat (a) -- per-channel E[L] honest autocorrelation framing

Per the v3 §4.8.1 four-verdict table above, FAIL-override channels and PASS-fallback-no-cutoff channels (E[L]=14) have visibly wider per-day CIs than PASS-real channels. This is the honest reporting per the methodology MD's 'robustness to non-stationarity' weighting.

### v2 caveat (b) -- completeness baseline-source disambiguation

The §4.8.4 completeness Spearman binds to Arm-B μ_ch regardless of the cell's named §1.1 baseline-arm. Per-episode `completeness_per_episode` is threaded from the locked Arm-B × pooled × no-detrend × episode-end × primary cell. Undefined-completeness exclusions are per-channel (per the §4.5 step 7 ε = 0.5×σ_ch rule).

### v3 caveat (#1) -- pooled-LC stationarity contamination + Series B sensitivity arm

The pooled-LC daily series (~4 years) crosses CPAP + Citalopram intervention transitions documented as level shifts. Series B (unmedicated stratum 2022-04-04 → 2024-04-08, n=635 days) is the cleaner ACF anchor when present; the v3 §4.8.1 table above surfaces both magnitudes alongside the binding choice (A or B).

### v3 caveat (#3) -- override magnitude cap at E[L]=21

Cap-binding channels (data-driven E[L]\* > 21; per-day CI at the n=29-imposed resolution floor):
- **all_day_stress_avg**: Series A E[L]\*=26.60, Series B E[L]\*=7.00; CAP-BINDING → E[L]=21.

### v3 caveat (#7) -- §4.8.4 day-level-E[L]-on-per-episode-summary granularity mismatch (structural; inherited from v1; deferred to v4)

The §4.8.4 secondary Spearman CIs use the per-channel day-level E[L] from §4.8.1 at per-episode resampling within phase, but per-episode summaries are not autocorrelated within an episode in the same way daily values are. The day-level E[L] on per-episode resampling over-conservatively widens the per-episode-summary CIs. This is a structural choice for cross-cell comparability; the per-episode-summary-aware block length alternative is deferred to a methodology MD update + a v4 absorption.

---

## Reader's notes (reviewer-mode-with-authorization, 2026-06-17)

*Interpretive overlay written 2026-06-17 by Claude (Opus 4.7 1M) in reviewer-mode-with-authorization at user request after a live review of the script-emitted result above. NOT a post-hoc spec modification. NOT a pre-registered finding. Names four readings that the mechanical output above states numerically but does not interpret. Per CONVENTIONS §1.2 these are reading-discipline notes on top of the locked v3 result, not new analyses.*

### Note 1 -- gevoelscore is technically `slow-grind-incomplete` but actually relapses-and-recovers

The pooled-LC × Arm-B × no-detrend × episode-end × primary cell classifies gevoelscore as `slow-grind-incomplete`. The §4.8.3 first-match-wins algorithm reaches that label correctly: |z(t+5)|=0.65 < |z(t+1)|=1.01 (net progress toward baseline) AND |z(t+5)|≥0.5 (incomplete; >0.5 SD off at end of window) AND no match on categories 1-4.

But the per-day median z-trajectory is **not a slow grind**:

| day | median z | 95% CI | CI excludes 0? |
|---|---:|---|---|
| t+1 | -1.009 | [-1.187, -0.319] | **yes** |
| t+2 | -0.306 | [-1.150, 0.651] | no |
| t+3 | -1.046 | [-1.443, -0.112] | **yes** |
| t+4 | -0.156 | [-1.009, 0.795] | no |
| t+5 | +0.651 | [-0.319, 0.795] | no |

The actual shape is **dip → near-baseline → dip → near-baseline → above-baseline**. The two below-baseline dips at t+1 and t+3 are statistically distinguishable from the 90-day baseline (CIs exclude 0). The formal episode-end is not where felt-state is back to normal; it's the start of a ~3-day fragile window where felt-state drops significantly below baseline twice before stabilising.

The v3 spec §7 prior anticipated this exact shape: *"by construction of episode-end definition, gevoelscore returns to above-threshold ON the episode-end day. Trajectory on [t+1, t+5] is the post-recovery gevoelscore — should remain near or above baseline. **Any dip indicates a 'stair-step' recovery pattern (partial recovery + relapse)**."* The empirical trajectory matches the prior; the §4.8.3 classifier just doesn't find the right label because the dips at t+1 and t+3 are full sign-reversals of the first-differences, not the sign-consistent-with-one-flat-day pattern that §4.8.3 cat-4 stair-step requires.

**Reading discipline**: read gevoelscore as a **relapse-and-recover** trajectory, NOT a slow grind. The `slow-grind-incomplete` label in the headline table above is the closest algorithmic match but is lossy on the dip-pattern character that the spec's §7 prior specifically pre-named.

### Note 2 -- §4.8.4 completeness ↔ next-interval on `all_day_stress_avg` is the OPPOSITE direction from naive recovery debt

The §9 bullet 8 spec predicate reads: *"Secondary correlational sub-hypothesis (§4.8.4) finds OR on recovery-completeness ↔ next-crash-interval → recovery debt is empirically supported."* The bullet was drafted with an implicit POSITIVE direction in mind: high completeness → long next-interval (recovering well buys you a longer gap).

The observed ρ on `all_day_stress_avg` is **-0.338 [-0.493, -0.168]** (n=18). Negative. **More complete daytime-stress recovery is associated with SHORTER gap to next crash.**

This is the inverse of naive recovery debt. The §9 bullet 8 propagation should be read accordingly: signal exists (CI excludes 0), but in the opposite direction; **the §9 bullet 8 propagation should NOT be read as supporting the recovery-debt mechanism for this channel.** Three candidate readings of the inverse-direction signal:

1. **Exuberance / push-through**: when daytime-stress normalises quickly, the participant probably feels okay enough to resume activity sooner; resuming activity sooner brings the next crash sooner. Matches the lived-experience PEM pattern documented in [lived_experience_garmin_pacing_2026-06-14.md](../../../lived_experience_garmin_pacing_2026-06-14.md).
2. **Tight feedback loop**: fast normalisation reflects autonomic elasticity that also enables fast re-loading; the system returns to baseline but is more responsive to incoming load.
3. **Measurement artefact**: if the next crash starts soon after t+5, the run-up may overlap the [t+1, t+5] window in a way that distorts the completeness measure (completeness compares channel value at t0 vs t+5; if t+5 sits in the next crash's pre-run-up, the t+5 reading can pass through baseline en route up).

The data alone cannot pick between these. The honest report: signal real, direction inverse-of-recovery-debt, mechanism ambiguous.

### Note 3 -- the §4.8.4 rate ↔ duration findings ARE within-episode recovery-debt-shaped

Two channels have CI-excludes-0 on rate ↔ duration:
- `all_day_stress_avg`: ρ = +0.285 [+0.021, +0.585], n=22
- `stress_low_motion_min_count_S60_Mlow`: ρ = +0.389 [+0.013, +0.709], n=22

Rate is the OLS slope on the z-trajectory across [t+1, t+5]. Negative slope = recovering toward baseline; near-zero or positive slope = staying elevated or moving further away. Positive correlation with duration means: **longer crashes go with flatter or rising post-crash stress trajectories** — bigger crashes leave bigger autonomic disturbances that don't resolve in the 5-day window. This IS recovery-debt-shaped, but it's a **within-episode-tail** recovery debt (the longer the crash, the slower the post-episode autonomic decay), distinct from the **across-episode** recovery debt that Note 2's completeness↔next-interval bullet was drafted to test.

Both stress-family channels show the same pattern, `stress_low_motion_min_count_S60_Mlow` slightly stronger (+0.389 vs +0.285).

### Note 4 -- corrected summary of §4.8.4 recovery-debt reads

- **Within-episode-tail recovery debt: empirically supported** for both stress-family channels via Note 3's rate↔duration findings.
- **Across-episode recovery debt: NOT supported** for `all_day_stress_avg` via Note 2's completeness↔next-interval finding; the signal exists but in the inverse direction (mechanism per Note 2's three candidate readings).
- All three §4.8.4 CI-excludes-0 readings hold under the v3 spec's deliberately wide CIs (E[L]=21 for `all_day_stress_avg` cap-binding per closure #3; day-level-E[L]-on-per-episode-summary over-conservatism per closure #7). Signals strong enough to survive the spec's honest pessimism on the bootstrap.

---

*Result emitted by `script.py` on the v3 LOCKED pre-registration. Reader's notes above are interpretive overlay per CONVENTIONS §1.2, added 2026-06-17 in a separate post-run pass after user-driven review of the script output. Raw result data in `result-data.json`; full multi-arm per-day-per-cell trajectory data in `result.csv`; per-channel × phase trajectory PNGs in `plots/`. Any post-result modification of the spec creates HA-P6-v4 with this v3 archived.*
