# Stress-with-low-motion minute count — primitive methodology

*Producer-mode methodology MD. Drafted 2026-06-15 (Session E). Locks
the per-day primitive `stress_low_motion_min_count_<S>_<M>` used by
Wiggers C4b ([`wiggers_testable_hypotheses.md §C4b`](../wiggers_testable_hypotheses.md#c4b--stress-with-low-motion-minute-count-c4-with-motion-filter))
and any downstream test on the "elevated stress while at rest"
construct from [`garmin_pacing_practice.md §3.3`](garmin_pacing_practice.md#33-stress-when-at-rest).*

Producer-mode artefact per [CONVENTIONS §1.1](../CONVENTIONS.md#11-producer-mode-claude-writes--edits--runs).
Inherits the four-input reasoning bar from [§2.2](../CONVENTIONS.md#22-methodology-md-before-locking-a-major-choice).

---

## 1. What this MD asks, and what it does not

### 1.1 The question

The construct of interest — *elevated autonomic stress while the
body is clearly at rest* — is operationally defined in the
participant's lived pacing protocol as a **mismatch** between
nervous-system load (Garmin `stress_level`) and physical motion
(low / absent step activity). Wiggers C4 frames the same pattern
as "stuck sympathetic / walls of orange" but does NOT specify a
motion filter; C4b is the participant's refinement adding the
filter to discriminate true sympathetic-arousal-during-rest from
motion-artefact stress (Garmin's stress score is partly motion-
sensitive; minutes with concurrent activity may inflate stress
without indicating sympathetic load).

**The primitive this MD locks** is a per-day integer count:

> Number of minutes on day `d` where `stress(t) >= S` AND
> `motion_proxy(t)` is in the low-motion class, for thresholds
> `(S, M)` in the §4 sensitivity ladder.

This MD locks: the FIT-data extraction path; the operational
definition of `motion_proxy(t)`; the canonical thresholds; the
sensitivity ladder; the NaN policy; the dose-adjustment policy.
It does NOT lock: any hypothesis test using the primitive
(those live in the relevant test MDs); the rolling-baseline z-score
form of the primitive (that's a separate column family if it lands).

### 1.2 What this MD does NOT do

- **Does NOT integrate dose-adjustment into the primitive.** Per
  the user-confirmed Session E decision 2026-06-15, the primitive is
  extracted at **raw stress thresholds**. Cross-phase aggregation by
  downstream tests applies [`citalopram_phase_stratification §5.B`](citalopram_phase_stratification.md#5b-dose-adjusted-predictor-recommended-for-cross-phase-tests)
  on the predictor side; the primitive itself is dose-naive.
  Rationale: keeps the primitive reusable for any test that wants
  raw thresholds (not just C4b) and decouples it from future
  refinements to the per-mg-plasma offset.
- **Does NOT compute per-minute step counts.** Per §3 below, the FIT
  `monitoring_b` files do NOT carry per-minute step counts directly;
  they carry sparse aggregate `cycles` records + per-minute `intensity`
  classifications. The hypothesis-spec phrasing "`steps_per_minute <= 5`"
  in [`wiggers_testable_hypotheses.md §C4b`](../wiggers_testable_hypotheses.md#c4b--stress-with-low-motion-minute-count-c4-with-motion-filter)
  conceptually means "low/absent stepping activity"; this MD
  operationalises that via Garmin's own intensity classification
  (§3.2), which is the closest defensible measure in this data.
- **Does NOT run a hypothesis test.** This is a primitive extraction
  methodology; C4b's actual test lives in
  [`wiggers_testable_hypotheses.md §C4b`](../wiggers_testable_hypotheses.md#c4b--stress-with-low-motion-minute-count-c4-with-motion-filter).

### 1.3 Inherited substantive caveats

- **Citalopram dose-modulation of stress channels** (per
  [`citalopram_dose_response §5.6`](citalopram_dose_response_stress_mean_sleep.md#56-v3-amendment--multi-channel-confirmation-added-2026-06-14)).
  The raw stress value at threshold `S=60` corresponds to a different
  *underlying autonomic state* depending on the phase of the
  Citalopram-traject — at 30mg plasma the raw stress channel sits
  ~12-17 points higher than at 0mg. A primitive at raw threshold
  will count more minutes in the 30mg consolidation phase than in
  the unmedicated phase even if the *true* sympathetic-arousal-while-
  at-rest rate were constant. This is exactly why C4b's caveat now
  requires §5.B dose-adjustment in the consumer test. The primitive
  itself is dose-naive by design (§1.2).
- **n=1 within-subject; no cross-subject generalisation.** Thresholds
  in §4 are calibrated to this participant's stress-channel distribution;
  another FR245 wearer with different autonomic baseline would need
  different thresholds.
- **Single FR245 device throughout.** Per `project_garmin_research_bias_boundary`
  the device is constant; no device-change confound.

### 1.4 Framing — descriptive per CONVENTIONS §4.3

The primitive is a Layer-1 descriptive measurement, not a
hypothesis test. Its values inform downstream tests (C4b, HA11
joint analyses, P5b's predictor); the threshold-cherry-picking
discipline that prevents post-hoc selection is the §4 sensitivity
ladder + the per-test pre-spec.

---

## 2. The construct, in code (target)

```python
# For day d in the LC era:
def stress_low_motion_min_count(d: date, S: int, M: str) -> int:
    """
    Count minutes on day d where:
      - a stress sample exists in [1, 100] (in-range, not censored)
      - stress sample value >= S
      - motion class for the same minute is in {low motion classes for M}
    """
```

Output: **9 stress×motion count columns** + **2 respiration companion
columns** (§4b) + **1 valid flag** = 12 columns in `per_day_master.csv`.
The 9 stress×motion columns take the form
`stress_low_motion_min_count_S<S>_M<motion>` for each
`(S, motion) in {50, 60, 75} x {strict_sedentary, low_or_below, any_below_moderate}`.
The valid flag indicates sufficient stress sample coverage on day `d`
(>= 600 stress samples in [1,100], the HA11 gate).

---

## 3. Operationalising `motion_proxy(t)` — the FIT-data investigation

### 3.1 What `monitoring_b` FIT files actually contain (verified 2026-06-15)

Empirical inspection of a mid-corpus FIT file (`227083925651.fit`,
2023-12-27/28 spanning ~24h) shows:

| message type | count | per-minute? | carries motion? |
|---|---:|---|---|
| `stress_level` | 501 | yes (~1/min) | no |
| `monitoring` with `heart_rate` | 326 | yes (~1/min during day) | indirectly (HR alone) |
| `monitoring` with `intensity` + `activity_type` | 84 | irregular (per-bin) | **yes — direct** |
| `respiration_rate` | 501 | yes | no |
| `monitoring` with `cycles` / `steps` / `distance` | ~1-5 per day | aggregate bins only | yes but aggregate |

Critical finding: **per-minute step counts are NOT in the FIT data**.
The `monitoring` messages with `steps`/`cycles`/`distance` are
**aggregate bin records** summarising periods of activity — a single
record like `{activity_type: walking, steps: 83, duration_min: 9, ...}`
covers a whole walking bin, not one minute. A naive distribution of
`steps` across `duration_min` would assume uniform stepping within
the bin, which is the kind of imputation [CONVENTIONS §3.5](../CONVENTIONS.md#35-spike-detecting-metrics-over-daily-averages)
warns against (smoothing kills the spike signal).

The `intensity` field on per-bin records IS per-minute-attributable:
when a bin starts, the intensity classification applies until the
next bin overrides it. This is Garmin's own classification of "what
is the body doing right now" — sedentary (0), low (1), moderate (2),
highly active (3) — and it is what the participant's lived rest-stress
trigger effectively uses (the participant reads "is the body moving?"
from intensity-level signals on the watch, not from step counts).

### 3.2 The operationalisation — three candidate definitions

Three operationalisations of "low motion" are candidate:

| name | definition | rationale |
|---|---|---|
| `M=strict_sedentary` | `intensity == 0` (Garmin "sedentary" class) OR no monitoring record covers this minute | tightest filter; matches "body is fully at rest" |
| `M=low_or_below` (default) | `intensity <= 1` (sedentary or light activity) OR no monitoring record | matches lived-experience "I am not actively moving" — includes light fidget but excludes purposeful walking |
| `M=any_below_moderate` | `intensity <= 1` OR (no monitoring record) — equivalent to `M=low_or_below` until further analysis suggests otherwise. **Currently merged with `low_or_below`; placeholder for future refinement** | conceptual placeholder; one-paragraph follow-up needed if data suggests intensity=2 should sometimes count as low |

In practice the sensitivity ladder collapses `low_or_below` and
`any_below_moderate` to the same definition; the meaningful pair is
`strict_sedentary` vs `low_or_below`. The third name is retained as
a placeholder for a future-refinement intensity-class boundary
investigation.

### 3.3a Other motion indicators surveyed (Session E expansion 2026-06-15)

A broader probe of `monitoring_b` revealed several additional per-minute
indicators that were NOT in the original §3.2 design. Survey:

| indicator | per-minute? | coverage | role in this primitive |
|---|---|---|---|
| `respiration_rate` | yes (~100% of stress-sampled minutes) | dense | **INCLUDED as 2 orthogonal companion columns** (§4 expansion) — motion-OR-arousal correlate; see §3.3b for the physiology + honest interpretation |
| sleep-window membership | yes per night | per-night | **QUEUED for v2** — sleep IS low motion; requires sleep-window derivation from FIT or join with existing `sleep_start_gmt` column; not in this primitive's v1 to avoid pipeline ordering complication |
| recorded activity sessions (DI-Connect-Fitness) | yes within session | only during recorded sessions | **QUEUED for v2** — explicit "this minute is in a recorded walk/run/cycle" signal that overrides everything else; requires parsing a separate FIT folder |
| `activity_type == 'sedentary'` | sparse (~17%) | bin-transition emit | implicit in §3.2's intensity classification (sedentary correlates with intensity == 0); not a separate column |
| `spo2_data` presence | sparse (~50% on sleep nights) | when stillness-measurement attempted | not used; sparsity too high and overlaps with sleep-window signal already queued |
| HR vs personal baseline | dense (~70%) | when HR sampled | not used; confounded with stress itself (circular for C4b's "stress while at rest" question) |

The respiration-companion columns address an empirical observation
from §3.1's probe: **81% of HR-sampled minutes have NO intensity
record** (the watch doesn't emit intensity classifications often).
Those minutes default to "low motion" in §3.2's design, which is
generous. Respiration adds a dense per-minute signal that lets
downstream tests check whether high-stress-low-motion minutes were
ALSO accompanied by elevated respiration (suggesting hidden motion
or sympathetic arousal) or low respiration (suggesting genuine
restfulness).

### 3.3b What `respiration_rate` actually measures, honestly

The Forerunner 245 derives respiration rate from the **optical
heart-rate sensor** (PPG), NOT from chest motion or airflow. The
algorithm extracts breathing rate from the
**Respiratory Sinus Arrhythmia (RSA)** — the cyclical HR modulation
that syncs with the breath (HR rises slightly on inhale, falls on
exhale). The period of that modulation is the respiration rate.
Garmin's product term for this is "All-day Respiration Rate". One
sample per minute; same physical sensor as `stress_level`; same
data density.

**This is a dual-channel signal, NOT a clean motion-only indicator.**
Both motion AND sympathetic arousal raise respiration. Typical
distributions (general adult physiology):

| context | typical resp/min |
|---|---|
| Deep sleep | 10-14 |
| Quiet awake rest | 12-18 |
| Light walking | 16-22 |
| Anxious / aroused but still | 16-24 (overlaps with light walking) |
| Active walking | 20-28 |
| Vigorous exercise | 30-40+ |

The overlap between "anxious but still" and "light walking" is
exactly what makes respiration imperfect as a *pure* motion proxy
— but it is also what makes it **complementary to the intensity
proxy and to stress**, both of which have their own overlap
problems in different directions. The intensity proxy classifies
"is the body moving" via Garmin's per-bin labeller; respiration
catches what intensity misses on the 81% of minutes without an
intensity record AND it catches sympathetic arousal that occurs
without motion. Both signals fail differently; using them in
combination is what downstream tests gain.

**Honest reading rules for the companion columns**:

- A high-stress-low-motion minute (intensity ≤ 1 OR no record) that
  is ALSO in `n_minutes_resp_in_rest_band_10_18` → highest-confidence
  "stress while at genuine rest" minute.
- A high-stress-low-motion minute that ALSO contributes to
  `n_minutes_resp_above_18` → either hidden motion the intensity
  proxy missed (and the low-motion classification was wrong) OR
  genuine sympathetic arousal with breathing change (which is the
  C4b signal *stronger* than stress alone). Downstream tests can
  treat this as a stricter or laxer reading per the question they
  ask.
- A day with high `n_minutes_resp_above_18` independent of the
  primary stress-motion count is a separate signal indicating
  pervasive sympathetic/activity load.

**Reliability characteristics**:

- At rest: ~2-3 bpm of chest-strap reference (Garmin's published
  validation).
- During motion: PPG signal degrades; respiration estimates become
  noisier or are dropped by the algorithm.
- Calibration: the thresholds in §4b (10, 18) are from general
  adult physiology, NOT calibrated to this participant's baseline.
  A v2 of the primitive could compute a personal rest-band by
  taking the median in the longest verifiably-asleep window per
  the existing sleep columns. Out of scope for v1.

### 3.3 Why NOT step-count thresholds (`<= 5 steps/min`)

The hypothesis-spec phrasing in C4b literally says
"`steps_per_minute <= 5`", which sounded fine in design but is NOT
implementable as written on this corpus's `monitoring_b` data
without inferential imputation:

1. Aggregate `steps` records sum over a `duration_min` window of
   tens of minutes; distributing uniformly across the bin assumes
   constant cadence, which is wrong on real walks (warm-up, stop
   lights, fatigue).
2. Bin records appear sparsely (often 1-5 per day); minutes outside
   any bin have *no record*, but inferring `steps=0` is wrong for a
   day with a 30-minute walk record that doesn't have explicit
   minute-by-minute attribution.
3. Adding interpolation to a primitive that downstream tests assume
   is observational adds an interpretive layer violating
   [CONVENTIONS §4.1](../CONVENTIONS.md#41-no-interpretive-marks-on-raw-or-descriptive-layers).

The `intensity`-classification path uses Garmin's own algorithmic
labelling (which is what the watch face displays during pacing) and
matches the lived-experience trigger. The naming in the C4b spec
should be revised to say "low motion class (intensity-based)"
rather than "steps_per_minute"; a doc-update note is added to
C4b's notes in [`wiggers_testable_hypotheses.md`](../wiggers_testable_hypotheses.md)
when this primitive lands.

---

## 4. The sensitivity ladder

Per the §C4b spec (carried over verbatim except for the motion-filter
operationalisation), the primitive emits **9 columns** = 3 stress
thresholds × 3 motion classes:

| stress threshold `S` | motion class `M` | column name |
|---:|---|---|
| 50 | strict_sedentary | `stress_low_motion_min_count_S50_Mstrict` |
| 50 | low_or_below | `stress_low_motion_min_count_S50_Mlow` |
| 50 | any_below_moderate | `stress_low_motion_min_count_S50_Mbelow_mod` |
| **60** | strict_sedentary | `stress_low_motion_min_count_S60_Mstrict` |
| **60** | **low_or_below** | `stress_low_motion_min_count_S60_Mlow` (**primary**) |
| 60 | any_below_moderate | `stress_low_motion_min_count_S60_Mbelow_mod` |
| 75 | strict_sedentary | `stress_low_motion_min_count_S75_Mstrict` |
| 75 | low_or_below | `stress_low_motion_min_count_S75_Mlow` |
| 75 | any_below_moderate | `stress_low_motion_min_count_S75_Mbelow_mod` |

**Primary column**: `stress_low_motion_min_count_S60_Mlow` (canonical
C4b). Reason: matches the §C4b 2026-06-14 working spec (`stress >= 60`)
combined with the lived-experience reading (`low_or_below` is what
the participant actually pattern-matches against — not strict
sedentary because hand fidgets while sitting still are common).
The other 8 are sensitivity arms.

### 4b. Respiration companion columns (orthogonal, per §3.3a + §3.3b)

Two additional per-day columns enable downstream tests to read
respiration as either a hidden-motion check OR a sympathetic-arousal
signal (see §3.3b for the dual-channel physiology):

| column name | definition |
|---|---|
| `n_minutes_resp_above_18` | per-day count of minutes where `respiration_rate > 18` (elevated; **motion-OR-arousal** correlate; see §3.3b reading rules) |
| `n_minutes_resp_in_rest_band_10_18` | per-day count of minutes where `10 <= respiration_rate <= 18` (normal-rest band; suggests genuine restful breathing) |

These are NOT joined with stress; they are per-day totals across
all valid minutes. Consumer tests can compute the overlap with
`stress_low_motion_min_count_S<>_M<>` as a covariate, use the totals
directly as predictors, or restrict to "high-confidence rest minutes"
(low motion AND respiration in rest band per §3.3b's reading rules).
Respiration values outside `[5, 40]` breaths/min are treated as
off-wrist / sensor-error and excluded from both counts.

Respiration-band thresholds (10, 18) are anchored to general adult-rest
physiology (12-18 / min canonical resting range); the 18 upper bound
is chosen as the "elevated above rest" gate. **These are NOT calibrated
to this participant's personal baseline.** A v2 personal-baseline
refinement is queued (see §3.3b reliability paragraph); v1 uses the
general thresholds so downstream tests can compute on this primitive
without waiting for the calibration pass.

**Threshold rationale**:
- Stress 50: low end; catches mid-range arousal. Likely overcounts.
- Stress 60: canonical; corresponds to Garmin's "elevated" band on
  the watch face (0-25 rest, 26-50 low, 51-75 medium, 76-100 high).
- Stress 75: high end; conservative; catches only the strongly-
  elevated minutes. Likely undercounts.

**Sensitivity discipline**: any test using the primary column must
also report the corresponding two strict and below_moderate variants
at the same stress threshold (so 3 of the 9 columns at minimum); any
test claiming a threshold-invariant finding must report all 9.

---

## 5. NaN policy + day-validity gate

Per the HA11 precedent ([`HA11-stress-udip/extract_udip_counts.py`](../analyses/hypotheses/HA11-stress-udip/extract_udip_counts.py)):

- Day-validity gate: **`>= 600` in-range stress samples** (values
  in `[1, 100]`). Days below this gate get a `_valid_flag = 0` and
  the 9 primitive columns are set to integer 0 (not NaN — the day
  was tracked but coverage was insufficient).
- Days with no `monitoring_b` FIT file at all: all 9 columns NaN +
  `_valid_flag` NaN. (These are device-off days; not a measurement.)
- Sentinel handling: stress values outside `[1, 100]` are NOT
  in-range. Per
  [`H02d-stress-spikes-uncensored/extract_daily_max_spike_v2.py`](../analyses/hypotheses/H02d-stress-spikes-uncensored/extract_daily_max_spike_v2.py)
  sentinels can be classified as `too_active` (HR within ±60s
  suggests active sample) or `off_wrist` (no co-occurring HR).
  This primitive treats both as **not counted** — `too_active`
  sentinels are by definition NOT low-motion (the algorithm is
  censoring because the watch detected activity); `off_wrist`
  sentinels are missing data. Both contribute to the day's
  in-range-sample-count being below the 600 gate if numerous.

---

## 6. Source FIT files + pipeline location

**Source**: `garmin data/DI_CONNECT/DI-Connect-Uploaded-Files/*.fit`
files classified as `monitoring_b` in
`analyses/garmin_exploration/fit_files_classified.csv`. Same source
as HA11.

**Extractor**:
[`pipeline/01_extract/stress_low_motion_extract.py`](../pipeline/01_extract/stress_low_motion_extract.py)
(to be implemented). Pattern reusable verbatim from HA11's
`extract_udip_counts.py` for the FIT-walk loop; the per-minute
join of stress + intensity is the new part.

**Output**: `$GEVOELSCORE_DATA_PATH/processed/garmin/stress_low_motion_minutes.csv`
with schema `date, sample_count, valid, [9 count columns]`.

**Propagator**: `pipeline/03_consolidate/build_unified_dataset.py`
merges the output CSV into `per_day_master.csv` via left-join on
`date`. Same pattern as existing per-day Garmin columns.

---

## 7. Four-input reasoning (per CONVENTIONS §2.2)

### 7.1 Best-practices standards

The state-of-art for *concurrence-thresholding of two physiological
signals* is straightforward: per-minute threshold-crossing followed
by per-day count. WWC 2022 SCED on aggregating per-minute behavioural
data into per-day counts is the methodological reference (for n-of-1
behavioural-physiological observation, daily counts are the standard
unit of analysis). The within-subject thresholding decision is the
ladder, not the level.

The state-of-art *not* used here: imputation-based per-minute step
estimation (§3.3 rationale). The choice is intentional and aligned
with [CONVENTIONS §4.1](../CONVENTIONS.md#41-no-interpretive-marks-on-raw-or-descriptive-layers).

### 7.2 Established literature

No directly-relevant external literature on stress-and-motion
concurrence-thresholding in n-of-1 self-tracking exists. The
closest anchor is the participant's own protocol (per
[`garmin_pacing_practice.md §3.3`](garmin_pacing_practice.md#33-stress-when-at-rest))
— which is a lived-experience prior per
[CONVENTIONS §4.3](../CONVENTIONS.md#43-prior-driven-hypotheses-are-confirmatory-not-exploratory)
— plus the Firstbeat 2014 white paper on the stress algorithm
(documented in [`hrv_proxy_via_stress.md §2`](hrv_proxy_via_stress.md#2-how-garmin-stress-is-derived))
which establishes that Garmin stress is partly motion-sensitive
and that filtering for low motion ISOLATES the autonomic-only
component. SSRI/autonomic literature (Licht 2010, Kemp 2010,
Wichniak 2017 — queued at QUEUED-WORK Tier 3) is mechanistic
context for the dose-adjustment caveat in §1.3, not the primitive
itself.

### 7.3 Tradeoffs

| dimension | choice | tradeoff |
|---|---|---|
| Motion proxy | Garmin `intensity` classification | implementable + matches lived trigger; gives up the fine-grained "exactly 5 steps/min" boundary the spec named |
| Per-day aggregation | integer count of qualifying minutes | matches WWC standard; gives up fractional-minute resolution |
| Sensitivity ladder | 3 × 3 = 9 columns | preserves robustness check; costs +9 columns in master |
| Primary column | `S60_Mlow` | matches working spec + lived trigger; arbitrary among the 9 if no consumer test pre-specs |
| Dose-adjustment | NOT in primitive (consumer's job) | reusable; consumer must apply §5.B per [`citalopram_phase_stratification`](citalopram_phase_stratification.md) |

### 7.4 Research limits + objectives

n=1, single FR245 watch, observational, daily-resolution outcome
(crash labels are per-day). The primitive's intended objective is
to enable C4b's confirmatory test + any joint analysis with HA11's
u_dip metric (which uses the same FIT source). 9-column overhead is
acceptable for a load-bearing primitive that multiple tests will
consume.

---

## 8. Validation plan

Once extracted, the primitive is validated descriptively before any
hypothesis test:

1. **Coverage**: days with `_valid_flag = 1` should be ~the same set
   as HA11's valid days (same FIT source + same 600-sample gate).
   Mismatch suggests a parsing bug.
2. **Distribution shape**: median + IQR + extremes per column. A
   "stress-with-low-motion" minute count of 0 on most days is
   acceptable (most days don't have prolonged stress-at-rest); long
   right tail expected.
3. **Threshold ordering**: at the same motion class, the count must
   monotonically decrease as `S` increases (S=50 ≥ S=60 ≥ S=75).
   Violations are bugs.
4. **Motion-class ordering**: at the same stress threshold, the
   count must monotonically increase as the motion-class broadens
   (strict ≤ low ≤ below_moderate). Equal under §3.2 collapse;
   violations are bugs.
5. **Spot check**: pick 2-3 known days and audit the per-minute
   join. Specifically: (a) a known sleep night → high count
   expected (low motion + variable stress); (b) a known active
   workout day → low count expected (high motion blocks even
   high stress); (c) a known stable workday → small-to-medium
   count.
6. **Correlation with HA11 u_dip count**: weak positive correlation
   expected (both pick up sympathetic-pattern minutes) but not
   strong (HA11's U-dip detects a SHAPE pattern, this primitive
   detects a CONCURRENCE pattern). Correlation > 0.7 would suggest
   redundancy; correlation < 0.2 means the two metrics are picking
   up genuinely different signals.

Validation script writes a one-page report to
`docs/research/analyses/garmin_exploration/stress_low_motion/validation.md`
(or similar location, established at run-time).

---

## 9. Status + revision log

**Status**: Drafted 2026-06-15 (v1) per CONVENTIONS §2.2. Awaiting
user sign-off on the §3 operationalisation choice (intensity-based,
not per-minute-steps). Script implementation gated on that sign-off.

### Revision log

| version | date | change | source |
|---|---|---|---|
| v1 | 2026-06-15 | Initial draft. Surfaces FIT-data investigation that per-minute steps are NOT directly extractable from `monitoring_b`; proposes Garmin `intensity` classification as the operational motion proxy. Locks 9-column sensitivity ladder + NaN policy + dose-adjustment policy (consumer-side). Validation plan in §8. | Session E spin-off from the post-Session-D framework cascade. |

### Audit hooks engaged

- [CONVENTIONS §2.1](../CONVENTIONS.md#21-descriptive-before-inference) — Layer-1 primitive; no inference baked in.
- [CONVENTIONS §2.2](../CONVENTIONS.md#22-methodology-md-before-locking-a-major-choice) — four-input reasoning in §7.
- [CONVENTIONS §3.5](../CONVENTIONS.md#35-spike-detecting-metrics-over-daily-averages) — the primitive IS a spike-counting metric by construction (per-minute threshold-crossing aggregated to per-day count) rather than a daily-average; matches §3.5 audit hook.
- [CONVENTIONS §4.1](../CONVENTIONS.md#41-no-interpretive-marks-on-raw-or-descriptive-layers) — no interpretive marks baked in; "low motion" is operationally Garmin's intensity classification, not the analyst's imputation.
- [CONVENTIONS §4.3](../CONVENTIONS.md#43-prior-driven-hypotheses-are-confirmatory-not-exploratory) — operational definition anchored to lived-experience pacing protocol (§3.3 of pacing-practice MD); confirmatory framing supported.

---

## 10. Cross-references

- [`wiggers_testable_hypotheses.md §C4b`](../wiggers_testable_hypotheses.md#c4b--stress-with-low-motion-minute-count-c4-with-motion-filter) — the hypothesis test consuming this primitive. Note: C4b's spec text "`steps_per_minute <= 5`" should be revised to "low motion class (intensity-based)" when this primitive lands.
- [`garmin_pacing_practice.md §3.3`](garmin_pacing_practice.md#33-stress-when-at-rest) — the lived-experience prior for the construct.
- [`citalopram_phase_stratification.md §5.B`](citalopram_phase_stratification.md#5b-dose-adjusted-predictor-recommended-for-cross-phase-tests) — the dose-adjustment framework consumer tests apply on top of this primitive.
- [`HA11-stress-udip/extract_udip_counts.py`](../analyses/hypotheses/HA11-stress-udip/extract_udip_counts.py) — the FIT-walk pattern reusable verbatim for the extractor.
- [`H02d-stress-spikes-uncensored/extract_daily_max_spike_v2.py`](../analyses/hypotheses/H02d-stress-spikes-uncensored/extract_daily_max_spike_v2.py) — the sentinel classification pattern (too_active vs off_wrist) reusable for the in-range-count gate.
- [`hrv_proxy_via_stress.md §2`](hrv_proxy_via_stress.md#2-how-garmin-stress-is-derived) — Firstbeat 2014 background on the stress algorithm being partly motion-sensitive.
- [CONVENTIONS §3.5](../CONVENTIONS.md#35-spike-detecting-metrics-over-daily-averages) — binding audit hook the primitive satisfies.
