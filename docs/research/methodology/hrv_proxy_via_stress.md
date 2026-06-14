# HRV proxy via Garmin stress score

*Methodology note — Wave 4+ pre-registration support. Drafted 2026-06-12.*

## Aim

The Forerunner 245 / Elevate V3 sensor used across the entire dump does
not produce nightly HRV Status (see
[`garmin_indicators_audit.md` § HRV — hardware blocked](garmin_indicators_audit.md)).
The current pre-registration draft
([`../wiggers_testable_hypotheses.md`](../wiggers_testable_hypotheses.md))
therefore marks the **B-block (B1–B5)** and the **HRV-dependent parts of
H1, H2, H3, H4, H5** as hardware-blocked and excludes them from
pre-registration on this corpus.

This note revisits that exclusion. The question is narrow:

> The Garmin "stress" score (0–100) is computed by the same Firstbeat
> algorithm that underlies HRV Status, from the same R-R interval
> stream from the same optical sensor. To what extent does the stress
> score — which IS produced on the Forerunner 245 and IS in
> `per_day_master.csv` — function as a usable proxy for the HRV signal
> the blocked hypotheses reference?

The conclusion below is a partial unblock: **sleep-window stress
columns are a noisy but usable HRV proxy** for the directional claims
Wiggers makes (HRV drops around PEM, HRV spikes signal
parasympathetic swing, HRV drift across multi-day overexertion). The
blocker as currently written in
[`garmin_indicators_audit.md`](garmin_indicators_audit.md) is
technically accurate (HRV Status itself is absent) but operationally
overstated for the Wiggers-pre-reg use case (the underlying HRV
signal is partially recoverable from stress).

This is a methodology proposal grounded in descriptive
characterisation (§ 7.1-7.3 below, run 2026-06-12). The
pre-registration draft has been revised on descriptive grounds
(B-block + H4 → PARTIAL); channel-selection (single vs multi) and
out-of-sample behaviour are pre-reg-level choices, not locked here.

---

## Status update 2026-06-13 — descriptive characterisation complete

The within-subject descriptive characterisation in § 7 has been run
via
[`../analyses/garmin_exploration/hrv_proxy_validation/run_71_72.py`](../analyses/garmin_exploration/hrv_proxy_validation/run_71_72.py).
Three descriptive findings carry the methodology forward (full
numbers below; raw run results in
[`../analyses/garmin_exploration/hrv_proxy_validation/result-table.txt`](../analyses/garmin_exploration/hrv_proxy_validation/result-table.txt)):

1. **Crash signal is real and concentrated in `stress_mean_sleep`.**
   Episode-level (n=29 crashes vs 1,162 normal-day base rate): Cohen's
   d = +0.90, CI95 [+1.51, +8.22]. Day-level supplementary (n=101):
   Cohen's d = +1.03. The CI does not cross zero at either unit.
2. **Day-level exertion signal is absent at the daily-aggregate
   resolution offered by `exertion_class_lagged_lcera`.** Checks 7.1,
   7.1b, 7.1c show flat heavy-vs-rest comparisons (all Cohen's d ≤
   0.08, all CIs cross zero) for `stress_mean_sleep`, `resting_hr_z`,
   and `stress_stdev_sleep`. Crashes are detected; ordinary heavy
   days are not. This is a real constraint on interpretation —
   whatever the proxy detects on crash days is NOT a simple
   "yesterday-was-heavy" exertion residual.
3. **HR-confound separability is moderate.** Pearson
   r(stress_mean_sleep, resting_hr) = +0.342 (LC all, n=1476),
   R² = 0.117 → ~88% of sleep-stress variance is not HR-driven.
   Crash-distortion sensitivity per
   [[feedback_crash_distortion_sensitivity]] barely moves the result
   (r = +0.331 with crash days dropped).

**What these descriptive findings support**:

- Pre-registering B-block and HRV-dependent H-block hypotheses on
  `stress_mean_sleep` as candidate HRV-proxy channel.
- Anchoring power planning on the empirical Cohen's d = +0.90
  (replacing the literature-derived 0.6× placeholder in § 4 below).
- Treating channel selection (single vs multi) as a per-hypothesis
  pre-reg choice rather than a globally-locked methodology constant.

**What these descriptive findings do NOT support**:

- Any claim that "the proxy is validated" — that requires
  pre-registered held-out analysis.
- Any claim that single-channel framing is preferred — channel
  selection is a pre-reg choice.
- Any literal HRV-unit interpretation of stress numbers.

§ 5 reclassification (B1-B5 + H4 BLOCKED → PARTIAL) is grounded in
finding (1). § 4 effect-size anchor is updated from the literature
placeholder to the empirical descriptive characterisation. § 9
decision options are simplified: (a) status quo (descriptive
findings filed, no pre-reg revision) vs (c) commit to the partial
unblock on descriptive grounds. Option (b) (run the descriptive
validation) is complete.

---

## 1. The blocker, restated precisely

What is missing on the Forerunner 245 / Elevate V3:

| Artefact | Present on FR245? | Notes |
|---|---|---|
| HRV Status (nightly summary) | No | Elevate V4 feature only |
| Overnight Averages 4-week chart | No | Garmin Connect feature; FR245 not eligible |
| Nightly RMSSD time series | No | Not exposed in any FIT message |
| Continuous R-R intervals in nightly files | No | Sleep type-49 messages contain undocumented `unknown_273/274/276` only |
| Per-activity R-R intervals via `Log HRV` | Yes, but chest-strap-only | OHR not clean enough; sparse, only during workouts |
| **24-hour stress score (0–100, 3-min resolution)** | **Yes** | Continuous through the day except during gaps (movement, no data) |
| **`stress_mean_sleep` (sleep-window aggregate)** | **Yes** | In `per_day_master.csv`; FIT-derived from sleep type-49 |
| **`all_day_stress_avg`** | **Yes** | In `per_day_master.csv` |

The proposal is to test whether the two bold rows can substitute for
the missing rows above for the directional Wiggers claims.

---

## 2. How Garmin stress is derived

Garmin acquired Firstbeat Technologies in 2020. The "stress" score —
both the continuous 24-hour version on the wrist and the manual 3-min
test — is computed by the same Firstbeat algorithm chain:

> R-R intervals (from optical sensor) → artefact correction → HRV
> features (RMSSD, HFP, LFP) + heart rate + respiration → state
> classification → stress score 0–100.

(*Firstbeat white paper "Stress and Recovery Analysis Method Based on
24-hour HRV", 2014; algorithm summarised in Garmin support
documentation and the Firstbeat Analytics technology overview.*)

Key technical facts:

1. **Multivariate composite.** Stress is *not* a one-to-one inverse of
   any single HRV metric. The algorithm weights RMSSD, HF power
   (0.15–0.40 Hz), LF power (0.04–0.15 Hz), heart rate, and
   respiration rate. During elevated-stress states the algorithm
   weights HR + respiration more; during recovery states the algorithm
   weights HRV more.

2. **Gaps during movement.** The algorithm does not produce a stress
   score when motion artefacts contaminate the signal. The 24-hour
   stress trace shows visible gaps during running, cycling, and
   sometimes during eating or stair-climbing. Wiggers' handleiding
   notes this on p.4 ("Gaps in your stress graph without a gray box
   below them often indicate that your data couldn't be measured")
   and Rosenbach et al. 2025 confirm it ("GSS is not calculated
   continuously, e.g. during movement").

3. **Same algorithm, same sensor, different output channel.** The
   reason HRV Status is unavailable on FR245 is not that the sensor
   doesn't compute HRV — it is that Garmin chose not to expose the
   *nightly summary feature* on Elevate V3 devices, because the
   sensor isn't accurate enough at full nightly resolution to meet
   their quality bar for that specific feature. The continuous
   24-hour stress score, which uses the same underlying HRV signal
   averaged over windows, IS exposed.

4. **The sleep window collapses the composite.** During sleep there
   is (by assumption) no voluntary movement, HR is at near-baseline,
   and respiration is regular. Of the five inputs (RMSSD, HFP, LFP,
   HR, respiration), three (HR, respiration, motion) are effectively
   constant. The stress score during sleep is therefore close to a
   pure function of the remaining HRV inputs. This is the basis of
   the proxy proposal: **`stress_mean_sleep` is the cleanest
   HRV-derived signal we can extract on this sensor**.

---

## 3. Empirical validation of stress vs HRV (peer-reviewed)

The cleanest validation in the literature is Rosenbach et al. 2025,
preregistered and peer-reviewed in *Stress and Health* (Wiley). Design:
60 participants (after a 29-participant pilot), Garmin Vivosmart 4
wrist + Polar H10 chest-strap ECG as gold standard, controlled
stress/rest protocol with concurrent Garmin Stress Score (GSS) and
ECG-derived HRV (RMSSD, SDNN, HF power, LF/HF, SD2/SD1).

### Group-level correlations (across all subjects)

| GSS vs ECG-derived metric | r | p | direction |
|---|---|---|---|
| Mean HR | +0.84 to +0.85 | < 0.0001 | very strong positive |
| SD2/SD1 | +0.61 to +0.64 | < 0.0001 | strong positive (sympathovagal) |
| RMSSD | **−0.59 to −0.63** | < 0.0001 | **strong inverse** |
| HF power | −0.40 to −0.43 | 0.0014 / 0.0006 | moderate inverse |
| LF/HF | +0.32 to +0.38 | 0.013 / 0.003 | moderate positive |

### Within-subject correlations (individual-level, averaged)

| GSS vs ECG-derived metric | r | SD across subjects | p |
|---|---|---|---|
| Mean HR | +0.74 | 0.35 | < 0.0001 |
| RMSSD | **−0.41** | 0.42 | < 0.0001 |
| SD2/SD1 | +0.32 | 0.45 | < 0.0001 |
| HF power | −0.20 | 0.42 | 0.001 |
| LF/HF | +0.18 | 0.41 | 0.001 |

### Authors' verdict

> "GSS … are indicative of mental stress" but "its interpretation as
> a direct measure of 'stress' should be approached with caution."
> Heart rate proved more predictive of subjective stress than GSS
> itself.

The authors conclude GSS is suitable for detecting physiological
arousal during acute stressors in controlled settings, and
unsuitable as a standalone stress measure without contextual
information. They do not advocate it as an HRV substitute.

### Reading the numbers for our use case

Two implications.

**(a) GSS captures HRV variance, but it is closer to a "sympathetic
arousal index" than an HRV inverse.** Within-subject, GSS correlates
more strongly with HR (r=+0.74) than with RMSSD (r=−0.41). Tests that
purport to isolate the HRV component of stress need to co-control for
HR.

**(b) The huge cross-subject SD on within-subject correlations
(0.42 on RMSSD) is the literature's main complaint, but for an n-of-1
corpus it doesn't apply.** That SD says some individuals have
r=−0.83 and some r=0.00. For a single-user dataset the relevant
question is "what is this person's RMSSD↔stress coupling?" and the
descriptive validation in § 7 answers it directly.

---

## 4. Why sleep-window stress is the cleanest available proxy

Combining § 2's multivariate-composite point with the Rosenbach
within-subject HR confound (r=+0.74), the recommended proxy is:

| Column in `per_day_master.csv` | Why |
|---|---|
| `stress_mean_sleep` (primary) | Sleep-window mean stress. Motion ≈ 0, HR at baseline, respiration regular → composite collapses toward HRV-derived component. Closest single-channel approximation to "nightly HRV" that exists on FR245. |
| `asleep_stress_avg_uds` (cross-check) | FIT-derived independent computation; agreement with `stress_mean_sleep` validates pipeline. |
| `all_day_stress_avg` (NOT recommended as HRV proxy) | Contaminated by daytime HR + movement gaps. Use for C-block tests directly, but not as an HRV substitute. |

The intuition: during a 7-hour sleep period, the stress score's
underlying input vector is approximately `[RMSSD, HFP, LFP, baseline
HR, baseline respiration]` where the last two terms are near-constant
night-to-night for a given individual. Variation in
`stress_mean_sleep` from one night to the next is therefore close to
a monotone function of variation in the HRV inputs.

This does not make `stress_mean_sleep` *equal to* RMSSD. It makes it
a windowed composite that is HRV-dominated when computed at rest.

### Effect-size anchor — descriptive (updated 2026-06-13)

The original draft used a literature-derived "0.6× degradation
placeholder". § 7's descriptive characterisation now gives direct
empirical numbers (raw results in
[`../analyses/garmin_exploration/hrv_proxy_validation/result-table.txt`](../analyses/garmin_exploration/hrv_proxy_validation/result-table.txt)):

- **Episode-level crash signal** (n=29 crash episodes vs n=1,162
  normal-day base rate): mean diff = +4.66 stress points,
  CI95 [+1.51, +8.22], **Cohen's d = +0.90**. Same-day reference for
  power planning.
- **Day-level crash signal** (n=101 crash days vs n=1162 normal):
  mean diff = +6.15, CI95 [+3.78, +8.77], **Cohen's d = +1.03**
  (autocorrelation-inflated effective n; the episode-level d = +0.90
  is the cleaner anchor).

These are the actual descriptive effect sizes on this corpus, not a
multiplier of a hypothetical RMSSD test. Pre-registered effect-size
thresholds for B-block hypotheses anchor on these single-channel
numbers directly. The "0.6× degradation" placeholder is retired.

The descriptive characterisation is in-sample; smaller effect sizes
are expected for lead-lag claims and on out-of-sample data.
Walk-forward / hold-out discipline applies to every B-block / H-block
pre-reg.

---

## 5. What this unlocks for the H-matrix

Cross-referenced against the pre-reg draft in
[`../wiggers_testable_hypotheses.md`](../wiggers_testable_hypotheses.md):

| H | Current status | Proposed status with sleep-stress proxy |
|---|---|---|
| B1 — single-day HRV drop predicts crash | BLOCKED | **PARTIAL** — test `stress_mean_sleep(t) − rolling_28d_median` spike → `is_crash(t)` or `is_crash(t+1)`. The "≥10 HRV-point drop" threshold in Wiggers' text doesn't translate; calibrate the proxy threshold from descriptive validation. |
| B2 — multi-day HRV decline even with rest | BLOCKED | **PARTIAL** — rolling 7d `stress_mean_sleep` monotone-rising trend across peri-event window. Directionally Wiggers-faithful. |
| B3 — rising 7d HRV baseline ⇒ improving | BLOCKED | **PARTIAL** — falling rolling 28d `stress_mean_sleep` baseline in low-crash stretches. Direction only; absolute-number anchor lost. |
| B4 — sudden HRV spike as negative indicator (parasympathetic swing) | BLOCKED | **PARTIAL** — `stress_mean_sleep` negative outlier (= HRV positive outlier proxy) → `is_crash(t+1, t+2)`. Composite swing signature with RHR + BB in § H4. |
| B5 — HRV rises at acute-illness onset | BLOCKED | **PARTIAL** — same proxy; conditional on illness labels. |
| H1 — wearable LEADS gevoelscore crash | PARTIAL (non-HRV only) | **PARTIAL EXTENDED** — add CCF on first-differenced `stress_mean_sleep` vs `gevoelscore`. This is the Wiggers-faithful test (her actual claim was HRV-leading); the non-HRV CCF stays as `H1ext`. |
| H4 — parasympathetic-swing composite | BLOCKED | **PARTIAL (revised 2026-06-13)** — composite signature on combined source + descriptive grounds. **Primary (BB-anchored, source-grounded)**: `bb_sleep_end_value` high + `bb_drained_24h` high after `exertion_class_lagged_lcera ∈ heavy`. Wiggers' parasympathetic swing chapter (PDF lines 1431-1457) directly cites the BB-drop pattern, so the BB-anchored framing is source-grounded independent of any RHR claim. **Secondary (proxy)**: `stress_mean_sleep` negative outlier (= HRV positive outlier proxy) on the swing night. **Exploratory**: `resting_hr` ↓ on the swing night. Channel selection (single-channel proxy vs multi-channel composite) is a per-hypothesis pre-reg choice. |
| H5 — per-metric characteristic lags | PARTIAL (HRV missing) | **PARTIAL EXTENDED** — include `stress_mean_sleep` as one of the lag-profile channels (Wiggers-relevant) alongside `resting_hr`, `bb_overnight_gain`. |
| H2 — activity-invisible crashes | PARTIAL | unchanged — the "+ night-HRV drop confirms" subclause Wiggers references becomes "+ `stress_mean_sleep` spike confirms", with proxy degradation noted. |
| H3 — illness vs PEM separable | PARTIAL | unchanged — classifier gains one more feature (`stress_mean_sleep`) at the proxy degradation rate. |

Net effect on the pre-reg draft summary table:

| Category | Current testable | Current blocked | After proposed reclassification |
|---|---|---|---|
| B | 0 | 5 | 0 fully testable, **5 partial** |
| H | 0 fully | 1 (H4) + 4 partial | 0 fully, **5 partial** (H4 reclassified from blocked) |

No H moves from blocked / partial to "fully testable." Five Bs and one
H move from "blocked" to "partial." Documented proxy degradation
(≈0.6× effect size, HR co-control required) applies to all of them.

---

## 6. What stays blocked even with this proposal

1. **Specific UI anchors in Wiggers' text.** The "≥10 HRV-point drop"
   threshold she cites is calibrated to Garmin's HRV Status UI
   units. Stress units don't translate. Tests must be calibrated to
   the proxy's own scale.

2. **The 3-minute manual HRV stress test.** A different feature
   entirely. Never recorded as daily summaries; not in the master.

3. **HRV Status 4-week Overnight Averages chart.** UI feature on
   Elevate V4 devices. We can reconstruct an analogue from rolling
   4-week `stress_mean_sleep`, but it is not the same artefact.

4. **Per-night HRV time series within a single night.** The
   sleep-window stress collapses 7 hours into one average; tests of
   within-night HRV dynamics (e.g. early-sleep vs late-sleep HRV
   recovery shape) remain blocked.

5. **The "raw" Wiggers H1 claim about HRV Status directly.** What we
   test is the *substantive* claim ("a stress-derived HRV proxy
   leads the gevoelscore crash"), not the *literal* claim ("HRV
   Status leads the gevoelscore crash"). Pre-reg framing should be
   honest about this distinction.

---

## 7. Descriptive characterisation — COMPLETED 2026-06-12

The 0.6× degradation estimate, the HR co-control assumption, and the
"sleep-window collapses the composite" claim were checked on the
corpus via
[`../analyses/garmin_exploration/hrv_proxy_validation/run_71_72.py`](../analyses/garmin_exploration/hrv_proxy_validation/run_71_72.py).
Full numbers in
[`result-table.txt`](../analyses/garmin_exploration/hrv_proxy_validation/result-table.txt)
and [`result-data.json`](../analyses/garmin_exploration/hrv_proxy_validation/result-data.json).
These are **descriptive characterisations** — means, CIs, effect
sizes, correlations. They are NOT discrimination-test verdicts and
do NOT replace pre-registered held-out analysis.

### Check 7.1 — Does sleep-stress carry the expected exertion signal?

Compare `stress_mean_sleep(t)` between `exertion_class_lagged_lcera ∈
{heavy, very_heavy}` and `{light, none}` days. If the HRV inverse
holds, heavy-exertion days should have higher `stress_mean_sleep`.

**Result (descriptive)**: NULL at daily-aggregate resolution. Heavy
n=526, rest n=686. Mean diff (heavy − rest) = −0.48 stress points,
CI95 [−1.16, +0.20], Cohen's d = −0.076. CI crosses zero. Same null
characterisation for `resting_hr_z` (Check 7.1b, d=+0.046) and
`stress_stdev_sleep` (Check 7.1c, d=+0.039).

This is a real constraint on interpretation: whatever the proxy
detects on crash days (see Check 7.3), it is NOT a simple
"yesterday-was-heavy" exertion residual. Crashes are physiologically
distinct from heavy-but-non-crash days in a way the lagged
exertion classification does not capture at daily resolution.

### Check 7.2 — Does sleep-stress separate from waking-HR confound?

Regress `stress_mean_sleep ~ resting_hr` and report Pearson r + R².

**Result (descriptive)**: Pearson r(stress_mean_sleep, resting_hr) =
**+0.342** (LC all, n=1476). **R² = 0.117 → ~88% of sleep-stress
variance is not explained by RHR.** Crash-distortion sensitivity
(per [[feedback_crash_distortion_sensitivity]]) barely moves the
result: r=+0.331 with crash days dropped. The two channels carry
substantially distinct information at the variance-correlation
level, supporting channel selection (single vs multi) as a legitimate
per-hypothesis pre-reg choice.

### Check 7.3 — Does sleep-stress correlate with crash days?

Per-event mean of `stress_mean_sleep` on `is_crash` days vs base-rate
days. Effect size + 95% CI.

**Result (descriptive)**: POSITIVE, large effect.

- **Episode-level primary** (crash_v2 unique crash-NNN ids, n=29
  episodes vs n=1162 normal-day base rate): mean diff = +4.66 stress
  points, CI95 [+1.51, +8.22], **Cohen's d = +0.90**.
- **Day-level supplementary** (n=101 crash days vs n=1162 normal
  days): mean diff = +6.15, CI95 [+3.78, +8.77], **Cohen's d = +1.03**
  (autocorrelation-inflated effective n).

CI does not cross zero at either unit. `stress_mean_sleep` is
descriptively elevated on crash episodes at a magnitude that supports
pre-registering directional Wiggers-class tests on the proxy. This
is the empirical effect-size anchor for power planning (§ 4 above).

### Check 7.4 — Within-subject stability across the validated eras

Per [[project_lc_era_boundaries]], the only validated analytical eras
on this dataset are pre-covid (up to 2022-03-20), corona infection
(2022-03-21 to 2022-04-03), and long-covid (from 2022-04-04). All
crash data lives in the long-covid period; the LC era is not
sub-split by any internal date boundary.

Practical implications for this check:

- Pre-covid baseline (~217 days) is available for sanity-checking
  whether `stress_mean_sleep` and `resting_hr` behave as expected in
  a healthy state, but it carries no crash labels and no
  `gevoelscore` data (gevoelscore starts 2022-09-03 per
  [[project_timeline_anchors]]).
- The corona-infection window (14 days) is too small to power a
  within-era comparison and is excluded from analytical use; flag
  separately if any data point falls inside it.
- The long-covid era (~1,524 days) is treated as one regime for
  Checks 7.1-7.3. No internal stratification.

If the proxy carries the expected exertion / HR-separability / crash
signal in the long-covid era, that is sufficient for the
methodology. Cross-era comparison (pre-covid vs long-covid) is
optional and supplementary — it tells you whether the proxy works
the same way in a healthy vs disordered autonomic state, which is
scientifically interesting but not gating the pre-reg revision.

These four checks are small descriptive pieces, low risk,
fast to run. They should land before any of the partial-status B or H
pre-reg files are written.

---

## 8. Caveats and limits of this proposal

1. **Sensor difference.** Rosenbach 2025 used the Vivosmart 4, which
   carries an Elevate V4 sensor (per Garmin's compatibility tables).
   Your FR245 is Elevate V3. The Firstbeat algorithm is identical;
   the sensor input quality is not. Proxy strength on FR245
   specifically is not externally validated. § 7's checks are the
   only available calibration.

2. **Algorithmic opacity.** Firstbeat's exact weighting of RMSSD vs
   HF vs LF vs HR vs respiration in the 24-h stress score is
   proprietary. The mapping is monotone (lower HRV → higher stress
   in expectation) but not analytically invertible. Any "GSS to
   RMSSD reconstruction" beyond directional/rank tests is
   ill-founded.

3. **Sleep-window assumption may not hold uniformly.** Nights with
   sleep fragmentation, prolonged latency, or POTS-related
   awakenings contaminate the sleep-window with movement and elevated
   HR. The `sleep_awake_min` column flags this. Tests using
   `stress_mean_sleep` should at minimum exclude or down-weight
   nights with high `sleep_awake_min`.

4. **HR is a strong confounder.** Every B or H test using
   `stress_mean_sleep` as an HRV proxy should also report the same
   test with `resting_hr` as a covariate. If the effect disappears
   under HR control, the apparent HRV signal is really an HR signal.

5. **This proposal does not unlock H4 fully.** Parasympathetic swing
   is canonically a *spike* in HRV (sudden large positive deviation).
   Our proxy can detect a *trough* in sleep-stress (its mirror). But
   the joint signature Wiggers names — "high HRV + very low HR" (p.28
   diagnostic chart) — requires both channels. We have the RHR
   channel directly, so the joint test is feasible; we just don't
   have HRV in the literal units Wiggers references.

6. **n-of-1 calibration cannot be cross-validated.** All effect-size
   estimates from § 7 will be in-sample. Walk-forward / hold-out
   validation across LC phases is the only available
   out-of-sample check, and it is partially confounded with the
   phase-trajectory shifts themselves.

---

## 9. Decision asked of the user — updated 2026-06-13

The descriptive characterisation (originally option (b)) is complete;
results in § 7.1-7.3 above. Two options remain under a
descriptive-grounded framing:

(a) **Status quo.** File the descriptive findings as a research
    artefact, keep `garmin_indicators_audit.md` § HRV as
    "hardware-blocked" for forward use, and do not revise the pre-reg
    draft. Defensible but leaves the descriptive Cohen's d = +0.90
    crash signal unused.

(c) **Commit to the partial unblock on descriptive grounds.** Revise
    `garmin_indicators_audit.md` § HRV to "hardware blocked for HRV
    Status directly; partial proxy unblock via `stress_mean_sleep` on
    descriptive grounds, see
    [`hrv_proxy_via_stress.md`](hrv_proxy_via_stress.md)." Revise the
    pre-reg draft to mark the 5 B-block hypotheses and H4 as PARTIAL.
    Each B-block / H-block pre-reg file must include:
    1. Acknowledgement that the test is on the stress proxy, not on
       HRV proper.
    2. Effect-size anchor on the descriptive Cohen's d = +0.90
       (episode-level same-day reference).
    3. Walk-forward / hold-out validation discipline (the descriptive
       characterisation is in-sample).
    4. Channel selection (single vs multi) is a per-hypothesis pre-reg
       choice; descriptive r = +0.342 between `stress_mean_sleep` and
       `resting_hr` shows the channels are distinct enough that the
       framing is a legitimate hypothesis-by-hypothesis decision.
       Do NOT lock framing globally.
    5. Wiggers UI anchors do not translate to stress units; calibrate
       the proxy threshold from descriptive characterisation.
    6. No literal-HRV claim in pre-reg conclusions; only the
       proxy-tested claim is defended.

The original middle option (b) is removed — it has been executed.

**Recommendation** (mine, for the user's call): (c) is defensible on
descriptive grounds. The biggest risk is treating descriptive
effect-size as a discrimination verdict; the pre-reg-file constraints
above are prophylactic against that. If single-channel framing turns
out to be wrong, individual pre-regs are free to test multi-channel
composites — the descriptive characterisation does not foreclose
that choice.

If the user is uncomfortable with proxy-based reclassification, (a)
is the conservative fallback. The descriptive findings are valuable
research artefacts in either case.

---

## References

### Peer-reviewed validation

- Rosenbach et al. 2025. *Assessing Stress Level Scores Against
  Wearables-Driven Physiological Measurements.* Stress and Health,
  Wiley. [PMC12647429](https://pmc.ncbi.nlm.nih.gov/articles/PMC12647429/),
  [bioRxiv preprint](https://www.biorxiv.org/content/10.1101/2025.01.06.630177v1).
  Group-level r and within-subject r tables reproduced above.

### Algorithm methodology

- Firstbeat Technologies. 2014. *Stress and Recovery Analysis Method
  Based on 24-hour Heart Rate Variability.* White paper.
  [Landing page](https://www.firstbeat.com/en/stress-and-recovery-analysis-method-based-on-24-hour-heart-rate-variability/),
  [PDF (assets)](https://assets.firstbeat.com/firstbeat/uploads/2015/11/Stress-and-recovery_white-paper_20145.pdf).

- Garmin / Firstbeat Analytics technology overview.
  [Garmin Wiki — Firstbeat Analytics](https://wiki.garminrumors.com/Firstbeat_Analytics).

### Garmin device + sensor reference

- Garmin Support. *HRV Status on Compatible Garmin Watches.*
  [Support FAQ](https://support.garmin.com/en-US/?faq=HnFAR4oFRF4kHeqYme3bU6).
  Confirms Forerunner 245 (Elevate V3) is not compatible with HRV
  Status.

- Garmin Forums. *Can Garmin FR245 record daily HRV and a total
  daily strain?* [Forum thread](https://forums.garmin.com/sports-fitness/running-multisport/f/forerunner-245-series/265424/can-garmin-fr245-record-daily-hrv-and-a-total-daily-strain).
  Confirms FR245 records R-R intervals only during activities (chest
  strap required for clean data), not nightly.

### Internal cross-references

- [`garmin_indicators_audit.md`](garmin_indicators_audit.md) § HRV —
  hardware blocked. The blocker as it currently stands.
- [`../wiggers_testable_hypotheses.md`](../wiggers_testable_hypotheses.md)
  — pre-registration draft B-block and H-block, currently marked
  blocked.
- [`../DATA_DICTIONARY.md`](../DATA_DICTIONARY.md) — column-level
  documentation for `stress_mean_sleep`, `asleep_stress_avg_uds`,
  `all_day_stress_avg`.
- [`../wiggers_response_article_2026-06-08.md`](../wiggers_response_article_2026-06-08.md)
  — prior agent's response article (treats HRV claims as blocked).

### Wiggers source text

- Wiggers, Laure. 07-2025. *English Smartwatch Pacing for people with
  ME, long covid and other energy impairing conditions.* ME/cvs
  Vereniging. The HRV-leading claims are pp.25–26 (chapter "HRV
  status", subsections "Decreasing HRV", "Overnight Averages") and
  p.28 (diagnostic chart "1–5 HR × HRV combinations"). The
  parasympathetic swing chapter is p.42. The mental-PEM HRV-detection
  claim is p.42.
