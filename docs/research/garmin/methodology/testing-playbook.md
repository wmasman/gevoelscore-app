# Testing playbook — Garmin × crash investigation methodology

**Locked 2026-06-07 (Option A consolidation)** after the v1→v2
threshold-monotonicity diagnostic round and the independent peer
review, then **expanded 2026-06-07** to incorporate established
project conventions that had been followed but not previously
documented as testing methodology.

This is the project's methodology baseline; subsequent
pre-registered hypotheses and diagnostics must comply with §9
checklist or explicitly justify deviation in their hypothesis.md
/ diagnostic.md.

The playbook consolidates lessons banked across the
H##/HA##/K##/S## series, the Theme A baseline-contamination
episode, the HA06→HA06b → HA10/HA07c/HA08c/HA07d substitute-test
sequence, the v1→v2 threshold-monotonicity diagnostic round, the
independent peer review, AND the project conventions established
in [registry §1](../hypotheses/registry.md), the design brief, and
the data-source structure.

If a lesson here is later revised, the revision is locked as a
separate methodology document following the v2→v3 escape-hatch
discipline (see §5.4).

## 1. Scope

**In scope**: pre-registration discipline; operationalisation rules
(sentinel handling, window length, baseline construction, threshold
choice, direction choice); locked data + computation conventions
(analysis window, crash definitions, train/validate split, null
sampling, validity rules); diagnostic protocols (threshold-
monotonicity, parameter sensitivity, per-axis decomposition);
synthesis-level framing rules (channel non-independence, card
specificity, era as moderator, symmetric application, atomic
synthesis updates); statistical reporting rules (Fisher's exact,
multi-comparison disclosure, pooled-corpus arm).

**Out of scope**: specific test specs (those live in each
hypothesis.md); methodology for tests on non-Garmin data (notes,
gevoelscore, calendar) unless directly referenced; specific
physiological hypotheses; UI/UX design rules (see
[docs/design/brief.md](../../design/brief.md) and
[docs/architecture/frontend-conventions.md](../../architecture/frontend-conventions.md));
code conventions (see [CLAUDE.md](../../../../CLAUDE.md) and
[.claude/conventions.md](../../../../.claude/conventions.md)).

## 2. Pre-registration discipline

### 2.1 Lock hypothesis.md before data inspection

Every pre-registered test gets its own folder under
`hypotheses/H##-name/` containing `hypothesis.md` written **before
any data is inspected for that test**. The hypothesis.md locks:
- Claim
- Why we think this
- Data sources
- Measurement protocol
- Validity rules
- Threshold(s) — values AND units AND direction
- Lead-up window — primary AND secondary
- Null sample construction (seed `20260605` for consistency)
- Falsification criterion bar (typically 3-criterion: ≥ 60% freq /
  ≥ +15 pp disc / median magnitude ≥ threshold/2)
- Exclusion rules
- Expected effect size if hypothesis is true
- Caveats the result.md must explicitly acknowledge
- Decision rules for each outcome (per §2.6 verdict categories)

### 2.2 Spec changes create a new hypothesis ID

- HA01 → HA01b (different window length)
- HA01b → HA01b-recomputed (different baseline construction)
- HA06 → HA06b (different threshold type)
- HA10 → HA10b would be (different direction or different primary)

**Locked verdicts do NOT unlock.** The new hypothesis is a separate
pre-registration on the same data; both verdicts stay on record.

### 2.3 3-episode dry-run before locking spec

Print first 3 crash episodes' raw values per the locked spec BEFORE
running the full test. Confirms:
- Data shape matches expectations
- No definitional artifacts (e.g. H03 confirmation-type whitelist
  bug; H05 recovery target trivially met)
- Threshold values not pathological (e.g. HA10 median max-|delta|
  at 1.6 bpm meant 5 bpm thresholds were unreachable)

If the dry-run surfaces a pathology, the spec needs review BEFORE
running the full test. **The dry-run is the gate.**

### 2.4 Pre-register on multiple summary statistics

For metrics that cluster on integers or have few distinct values
(e.g. K01 nadir on 1-6 scale), pre-register on BOTH median AND
mean. The brittleness of median on small samples can hide real
shifts.

### 2.5 Audit-trail preservation for mid-investigation flaws

When a methodological flaw is caught mid-investigation:
1. Pre-register the re-test with corrections (new hypothesis ID).
2. Lock the new spec BEFORE running.
3. Run the bundled re-test **symmetrically** — re-test BOTH the
   refutation AND any win on the same correction (no selective
   rescue).
4. Pre-commit the bar at the original level.
5. Honest reporting in the same session.

The Theme A episode (HA01b → HA01b-recomputed + HA02c bundled) is
the exemplar.

### 2.6 Locked verdict categories

Every result.md uses the same labels (per [registry §1](../hypotheses/registry.md#1-scope-and-ground-rules)
"honest verdict categories"):

- **SUPPORTED** — pattern present in train AND validate, effect
  size at or above the pre-registered threshold.
- **REFUTED** — pattern absent or below threshold in at least one
  of train / validate.
- **INCONCLUSIVE** — too few crash episodes to power the test, or
  signal noisy enough that we can't tell.
- **PARTIAL / needs reshape** — interesting in one direction but
  the pre-registered measurement was wrong; document and decide
  whether to re-pre-register a v2.

Two additional labels used for diagnostics (per §5.1 v2 framework):
- **RESCUE** — diagnostic confirms shape-robust signal under
  revised criteria.
- **CLOSE** — diagnostic confirms shape-fragile or
  inappropriately-scaled signal.
- **AMBIGUOUS** — diagnostic neither rescues nor closes; defaults
  to CLOSE for synthesis-framing purposes.

### 2.7 The card.md craft rule

Each hypothesis folder may optionally contain `card.md` separate
from `result.md`:

- **card.md is written ONLY if result.md is SUPPORTED.**
- **2-3 candidate card-text variants** using real numbers from the
  analysis and (where notes are present) real quoted phrases from
  the user's `day_entries.note`.
- Must respect the [design brief](../../design/brief.md) tone:
  reflective Dutch, restrained, no em-dashes (per
  [`feedback_no_emdash_in_ui`](../../../../../.claude/projects/c--Users-Gebruiker-Documents-gevoelscore-app/memory/feedback_no_emdash_in_ui.md)).
- Pacing-doc principle: **present conclusions, not prescriptions**.
- Brainfog rule: **the card is readable in seconds**.
- The research determines whether a card *should* exist; the craft
  step determines what it *says*.
- Composing cards across multiple supported hypotheses (e.g. "RHR
  was +5 *and* stress was sustained" when H01 + H02 both fire) is
  a later step.

**Specificity gate** (per §6.2): card.md may not ship until
posterior-probability tables have been computed and the card text
calibrated to posterior probability, NOT discrimination magnitude.

## 3. Operationalisation rules

### 3.1 Sentinel handling

For per-minute Garmin signals (stress especially), sentinel values
(−1, −2) must be classified BEFORE the test, not dropped silently.
The H02d sentinel-corrected re-run is the exemplar. Required:
- Classify off-wrist vs too-active via HR-coverage within ±60s
- Pre-commit imputation rules (e.g. impute too-active as ≥75)
- Pre-register a bridge-only sensitivity arm alongside the
  imputation-primary

### 3.2 Window length

Lead-up windows pre-committed:
- **4-day primary** (matches HA01b's empirically-confirmed lag;
  matches HA06b/HA07d/HA10/HA11 lockings)
- **5-day secondary** (catches lag profile peak)
- Lag profile diagnostic reported alongside, NOT as a primary
  verdict

### 3.3 Baseline construction (Theme A)

For any rank/z-score metric where a sustained creep could rebase
its own reference, use the **lagged baseline `[d-90, d-30]`**:
- 60-day window ending 30 days before the candidate day
- Excludes the recent candidate region from the reference frame
- Minimum 40 valid prior days required
- Trimmed mean / stdev with 10/90 percentile trim
- If sigma below a floor (channel-specific, e.g. 0.5 bpm for RHR,
  2.0 BB points for body battery), flag as low-variability and
  skip

The rolling 30-day baseline is suitable ONLY for metrics that
don't rebase (e.g. `exertion_class` for daily-glance display;
NOT for predictive metrics).

### 3.4 Threshold choice — relative not absolute

For autonomic-channel tests (RHR, HRV, BB, stress derivatives,
sleep stress) and for any test where participant signal-to-noise
may differ materially from published external populations:
- Pre-register **z-score** `(signal − μ) / σ` relative to lagged
  baseline, OR
- Pre-register **percentile rank** against lagged baseline
- Thresholds in standardised units (`N_std = 1.5 / 2.0 / 2.5`,
  or rank ≥ 0.85 / 0.95 / 0.975)
- **Absolute bpm / ms / minutes thresholds drawn from external
  populations are REJECTED as primary**; may be reported as
  sensitivity arm only

The HA06 → HA06b lesson is binding: HA06's absolute 5/10/15 bpm
thresholds were unreachable for this participant (median max-|delta|
1.6 bpm); HA06b's z-score thresholds caught the signal. The
project-level principle is locked in
[`feedback_relative_not_absolute`](../../../../../.claude/projects/c--Users-Gebruiker-Documents-gevoelscore-app/memory/feedback_relative_not_absolute.md).

### 3.5 Direction choice

For each test, pre-register the primary direction based on the
physiological hypothesis:
- **One-sided elevated**: when hypothesis specifies a direction
  (e.g. Wiggers' BB peak elevated; *vermoeidheidskliniek*'s HRV
  drop; HA11's U-dip count elevated)
- **One-sided lowered**: same, opposite direction
- **Bidirectional**: ONLY when direction is a priori genuinely
  ambiguous (e.g. HA07d's variability shift could go either way
  per autonomic-dysregulation theory)

The HA10 lesson is informative: HA10's bidirectional primary was
conservative-but-arguably-wrong; a one-sided elevated primary
would have been the right call given Wiggers specifically predicted
elevated. HA07d's bidirectional primary was correct because
direction was genuinely ambiguous.

### 3.6 Direction reporting (sensitivity arms)

Regardless of the locked primary direction, the result.md must
report ALL THREE arms (bidirectional, one-sided elevated, one-sided
lowered) for inspection. The locked verdict uses ONLY the primary.
Sensitivity arms are descriptive context, NOT a basis for revising
the verdict.

### 3.7 First-order AND second-order primitives

For each channel, consider both:
- **First-order primitive** (mean / level): HA07c sleep stress mean
- **Second-order primitive** (variability / spread / slope):
  HA07d sleep stress variability; HA08c sleep stress slope

The HA07c → HA07d lesson is binding: HA07c (sleep stress mean
delta) refuted validate at +4.3 pp; HA07d (sleep stress
variability delta) SUPPORTED validate at +21.7 pp. **Second-order
primitives can carry signal first-order primitives miss.**

### 3.8 Composite construction — MAX-rank composites can dilute per-axis signal

**The lesson (2026-06-07)**: composite metrics built as
MAX-of-ranks across N input axes can trigger so often in the null
distribution that the crash-vs-null spread collapses, even when one
or more individual axes carry strong per-axis signal.

**Worked example — HA01b**: the composite `exertion_class_lagged ∈
{heavy, very_heavy}` is defined as MAX-of-ranks across 4 axes
(`effective_exertion_min`, `total_steps`, `max_hr_uds`,
`vigorous_min_uds`) crossing rank 0.75. Under HA01b's locked spec,
this composite triggered ~78% in null windows and ~80% in crash
windows. Discrimination on the lagged baseline = +3.4 / +1.5 pp,
locked REFUTED both eras.

The
[HA01b per-axis decomposition diagnostic (2026-06-07)](../hypotheses/HA01b-per-axis-diagnostic/result.md)
decomposed the composite into its 4 input axes. Result: when the
trigger requires a SPECIFIC axis to be elevated (not just MAX),
the null trigger rate drops to ~60% (per axis) and discrimination
jumps to ~+20 pp. effective_exertion_rank_lagged ≥ 0.75 SUPPORTED
both eras (+21.3 / +19.5 pp).

**Mechanism**: with N=4 axes correlated 0.31-0.69, the MAX-rank
union is broader than any single axis (any one of 4 axes being
elevated suffices to trigger). For "elevated" events that happen
on ~25-30% of normal days per axis, the MAX-union triggers on
~75-80% of normal windows, leaving almost no spread to discriminate.

**Rules for composite construction going forward**:

1. **MAX-of-ranks composites must be pre-registered with per-axis
   primaries IN ADDITION to the composite primary** (not as
   substitutes). The composite-vs-per-axis comparison is informative
   for honest verdict framing.

2. **OR use AND-of-axes composites** (require ALL N axes to
   trigger). Tighter specificity at the cost of sensitivity —
   different failure mode, but symmetric trade-off (null rate drops
   to ~5-10% per the same correlations; sensitivity drops too).

3. **The composite's REFUTED verdict is a real verdict**, not a
   stand-in for "no axis carries signal." A per-axis decomposition
   diagnostic remains pre-committed when a MAX-rank composite
   refutes and the per-axis signal question is open.

4. **For new hypotheses on composite metrics**: lock the per-axis
   decomposition pre-registration in the same hypothesis.md, with
   the same locked bar. If the composite REFUTES, run the per-axis
   diagnostic per §5.2 protocol; the composite verdict stays on
   record regardless.

**Cross-references**:
- [HA01b per-axis diagnostic result.md §3](../hypotheses/HA01b-per-axis-diagnostic/result.md)
  — full worked example with discrimination tables.
- §5.2 (per-axis decomposition diagnostic protocol) — the diagnostic
  shape that resolves this question.
- §4.7 (folder structure) — `hypotheses/H##-per-axis-diagnostic/`
  is the canonical location for per-axis decomposition tests.

### 3.9 Same-primitive-different-window tests are NOT independent corroborations

**The lesson (2026-06-08)**: when two pre-registered hypotheses
evaluate the SAME per-day primitive at DIFFERENT lead-up windows
(or with different sentinel handling that produces identical daily
values), they are **one signal with multiple arms**, not two
independent corroborating tests. The cross-channel correlation
matrix surfaces this when ρ ≈ 1.0.

**Worked example — H02b vs H02d (2026-06-08)**: H02b (3d window,
standard sentinel) and H02d bridge × 5d (5d window, sentinel-corrected
"bridge" handling) both extract `max_spike_minutes` per day. The
[cross-channel correlation matrix](../cards/cross-channel-correlation.md)
found **Spearman ρ = +1.000 across all 1737 shared valid days** —
the bridge sentinel handling produces identical daily values to
the standard handling. The discrimination difference (H02b +29.9 pp
vs H02d bridge +31.8 pp) comes entirely from window-length and
validity differences, NOT from a distinct underlying signal.

The prior synthesis framing — "six channels with seven SUPPORTED
tests" — implicitly treated H02b and H02d as independent
corroborating channels. They are not. The corrected framing
("five distinct primitives with six SUPPORTED tests") drops H02d
from the channel count.

**Rules for window-variant hypotheses going forward**:

1. **Before pre-registering a window-variant of an existing primitive**,
   run a per-day correlation check between the two primitive
   extractions. If ρ > 0.95, the new test is an arm of the existing
   hypothesis, not a new hypothesis.

2. **If the variant truly produces a different primitive**
   (different sentinel handling that DOES change daily values, or
   a different aggregation that DOES diverge): pre-register as a
   new hypothesis ID, and report the per-day ρ in result.md as
   evidence the primitive is genuinely distinct.

3. **For sensitivity arms within an existing hypothesis**
   (different N_std, different one-sided vs bidirectional, different
   window): these are correctly framed as arms, not new tests.
   Multi-comparison disclosure per §7.2 applies.

4. **The H02d bridge handling lesson does NOT invalidate H02d's
   verdict on record**. H02d SUPPORTED train at +31.8 pp under
   bridge × 5d is honest at its own bar. The synthesis-level
   "another channel" framing was wrong; H02d's actual contribution
   was "the 5d window catches more crashes than 3d on the same
   primitive."

**Cross-references**:
- [cross-channel-correlation.md key findings §1](../cards/cross-channel-correlation.md)
  — the H02b ≡ H02d empirical finding.
- §6.1 (channel non-independence) — the framing rule that this
  lesson refines empirically.

## 4. Locked data + computation conventions

### 4.1 Analysis window

The label-based analysis window is **2022-09-03 → 2026-06-05**:
- Start: gevoelscore tracking began 2022-09-03 (per
  [`project_timeline_anchors`](../../../../../.claude/projects/c--Users-Gebruiker-Documents-gevoelscore-app/memory/project_timeline_anchors.md))
- End: the gevoelscore corpus as of the registry lock
- ~1,372 day_entries with score on 1-6 scale (~98% coverage)

**Pre-LC Garmin (2021-08-16 → 2022-09-02)** is NOT part of
label-based tests. May be referenced for baseline-calibration
cards ("how far has the system moved") in a later batch, but
never as a source of crash labels.

### 4.2 Crash definitions

**`crash_v1`** (Option B locked 2026-06-05): a run of ≥ 2
consecutive `day_entries.date` rows with **score ≤ 3** (out of
1-6), with episodes within 3 days merged into one (dated to the
first day of the first run). Yields 29 episodes.

**`crash_v2`** (locked 2026-06-06): a two-tier classification:
- **Tier 1 `crash`** — exactly `crash_v1` (pre-registered
  slow-recovery filter empirically removed; every v1 episode has
  tail_median ∈ {4.0, 5.0}, positively validating crash_v1's
  acute condition as a PEM-shape detector).
- **Tier 2 `dip`** — single isolated bad day (score ≤ 3, neighbours
  ≥ 4, excluding crash recovery shadow). Yields 79 events.
- **Dip cluster overlay** — transitive chains of ≥ 2 dips within
  7 days of each other (15 clusters covering 45 of 79 dips).
  Descriptive only — per-day labels unchanged.

**Default convention**: hypotheses use `crash_v1` (29 episodes)
unless explicitly opting into `crash_v2` (so far: H02b-on-dips,
specificity-retag, HA05). Labels live at
[`crash_v2-definition/labels_crash_v2.csv`](../hypotheses/crash_v2-definition/labels_crash_v2.csv).

### 4.3 Train/validate split

Default for any predictive hypothesis (per [registry §1](../hypotheses/registry.md#1-scope-and-ground-rules)):
- **Train**: 2022-09-03 → 2023-12-31 (~16 months, 14 crash_v1
  episodes)
- **Validate**: 2024-01-01 → 2026-06-05 (~29 months, 15 crash_v1
  episodes)

Revised 2026-06-05 after the preflight surfaced a recovery cliff:
crash episodes drop from ~10/year in 2023-24 to ~2/year in
2025-26. A simple time-proportional 70/30 split would have left
the validate window with only 3 episodes; the revised split is
**roughly 50/50 by episode count**, not by time.

The cliff *inside* the validate window is itself the harder test:
if a Garmin precursor pattern is genuinely PEM-related, it should
still appear in the residual 2025+ episodes even though the
underlying state has shifted. If the pattern was an artifact of
overall worse-state physiology, it will fail validation.

### 4.4 Both-eras rule (and the era-moderator caveat)

A predictive hypothesis is SUPPORTED only if the pattern holds in
**both** train and validate windows independently. Train-only or
validate-only verdicts are reported but constitute an overall
REFUTATION under the strict locked rule.

**The both-eras rule is more stringent than scientific practice
normally demands**; it is conservative for the project's
feature-design use-case (a feature that runs in late 2026 must
work both in pre-cliff and post-cliff states). Per §6.3, the
narrative layer treats era as a **moderator-of-interest** —
era-specific findings are findings, not failures.

**Descriptive hypotheses** (e.g. characterising recovery time,
not predicting a future event) DO NOT require a held-out split;
note that per-hypothesis in hypothesis.md.

### 4.5 Null sample construction

For predictive precursor tests:
- **Random seed**: `20260605` (locked; used across all H##/HA##
  tests for reproducibility)
- **Sample size**: 200 random non-overlapping reference windows
- **Non-overlap rule**: reference windows must not overlap any
  crash episode's lead-up window
- **Per-window validity**: same per-day validity rules as the
  primary test (e.g. ≥ 3 of 4 lead-up days valid for 4d window)

Block-bootstrap null sample queued as Tier 3 methodological
refinement (peer review §4 concern about autocorrelation
structure).

### 4.6 Validity floors (locked per data source)

**Per-minute stress samples** (from monitoring_b FIT files):
- A day is valid if it has ≥ **600 in-range stress samples** (per
  H02b convention; ~10 hours of coverage).
- Sentinel handling per §3.1.

**Per-3-minute sleep stress arrays** (from API path C / FIT
re-parse intersected with sleep window):
- A night is valid if it has ≥ **120 in-range samples within the
  sleep window** (~6 hours coverage at per-3-minute cadence).

**Nightly RHR** (from UDS `restingHeartRate`):
- Validity range [30, 130] bpm.
- Lagged baseline σ floor 0.5 bpm (below this, day flagged
  low-variability and skipped).

**Morning BB peak** (from UDS `bodyBattery.bodyBatteryStatList`
HIGHEST anchor):
- Time-window filter: HIGHEST timestamp must be in
  **[03:00, 10:00] local** (overnight rebound, not daytime nap).
- Lagged baseline σ floor 2.0 BB points.

**Trimmed mean / stdev**: 10/90 percentile trim across all
lagged-baseline computations.

### 4.7 Folder structure conventions

Each pre-registered hypothesis lives at
`docs/research/garmin/hypotheses/H##-name/`:

```
H##-name/
├── hypothesis.md          # pre-registration (locked before data)
├── test.py                # implements the locked spec
├── result.md              # honest verdict + caveats
├── result-data.json       # numeric outputs for downstream re-use
└── card.md                # OPTIONAL; only if SUPPORTED per §2.7
```

Diagnostics use the same folder structure with `diagnostic.md`
replacing `hypothesis.md`.

### 4.8 Hardware constraints (FR245-specific)

The participant's hardware is a Forerunner 245 (2019 sensor).
Constraints that affect testing:

- **HRV is NOT recorded** — the FR245's optical HR sensor doesn't
  support HRV Status (added in FR255/265/955/965 + Fenix 7
  generation, 2022-2023). The `/hrv-service/hrv/{date}` endpoint
  returns an empty dict for every date. **Tests requiring HRV are
  BLOCKED-PENDING-HARDWARE** (HA07/HA08/HA12); use the sleep-stress
  proxy (HA07c/HA08c/HA07d) instead.
- **`unknown_233` in monitoring_b FIT** is per-minute Body Battery
  but undecoded by the community. Path C API
  (`cyberjunky/python-garminconnect`) provides per-3-minute BB for
  recent dates only (~2025+); older dates return empty arrays.
- **Sleep stress arrays** from path C API populated only for recent
  dates; FIT re-parse + local `sleepData.json` sleep windows are
  the cross-corpus solution.

Any new hypothesis blocked by hardware should be marked
BLOCKED-PENDING-HARDWARE in its hypothesis.md and re-queued behind
the relevant unblock (typically H04b path C authorisation for HRV
+ per-minute BB).

## 5. Diagnostic protocols

### 5.1 Threshold-monotonicity v2 diagnostic

If a test's locked verdict is SUPPORTED at the loosest threshold
tier (`N_std = 1.5` or equivalent) where the metric primitive is
z-score against a personal baseline:
- The test's load-bearing status in synthesis is **provisional**
  until a v2 threshold-monotonicity diagnostic runs.
- v2 diagnostic uses the locked v2 criteria
  ([threshold-sweep-rescue-criteria-v2.md](threshold-sweep-rescue-criteria-v2.md))
  on a fine N_std grid [0.5 → 4.0, 13 tiers], applied to the
  meaningful range [1.0, 3.0].
- v2 verdict (RESCUE / CLOSE / AMBIGUOUS) determines synthesis-
  level load-bearing status.
- Locked test verdict stays on record regardless of v2 outcome.

### 5.2 Per-axis decomposition for composite-primary tests

If a test's primary metric is a composite of multiple axes (e.g.
HA01b's max-rank-across-4-axes), a per-axis diagnostic may be
locked to ask whether any single axis carries signal the composite
hid:
- Pre-register per-axis diagnostic.md BEFORE inspecting per-axis
  data
- Apply same threshold / direction / bar to each axis
- Report ALL axes (no cherry-picking)
- Multi-comparison disclosed honestly (§7.2)
- Cross-axis correlation matrix reported in result.md
- **If a single axis is SUPPORTED at the locked bar**: this is a
  diagnostic finding, NOT a load-bearing verdict. To become
  load-bearing, the axis must be re-pre-registered as a new
  hypothesis (e.g. HA01c) AND pass v2 threshold-monotonicity per
  §5.1

### 5.3 Parameter-sensitivity diagnostic

For any test with parameter degrees of freedom not externally
anchored (e.g. HA11's U-dip detector with `S_pre ≥ 40`,
`drop ≥ 25`, `plateau ≥ +5`, refractory 60 min), a parameter-
sensitivity diagnostic should be pre-registered:
- Vary each parameter ±20%
- Measure discrimination stability
- If discrimination collapses under reasonable parameter shifts,
  the finding is "load-bearing pending parameter sensitivity
  confirmation"

### 5.4 v3 escape hatch (strict bound)

Per [threshold-sweep-rescue-criteria-v2.md §5](threshold-sweep-rescue-criteria-v2.md#5-application-rules),
a v3 methodology document may only be locked if all three
conditions are met:
1. **External authority** (peer-reviewed paper or methodology
   source)
2. **Pre-locked inadequacy statement** citing the external source
3. **Symmetric re-application** to all v2-evaluated tests

Same principle applies to any methodology revision in this
playbook.

## 6. Synthesis-level framing rules

### 6.1 Channel non-independence

The project's Garmin channels share underlying inputs:
- BB is `g(HR, HRV, stress, sleep)`
- Sleep stress is per-minute stress restricted to the sleep window
- HA07c, HA08c, HA07d are three primitives of the same sleep-
  stress channel
- RHR and stress both have HRV in their derivation

Synthesis-level framing must use language that respects this:
- "Six distinct channels with multiple primitives" NOT "six
  independent channels"
- "Multiple operationalisations of an underlying autonomic-state
  construct" NOT "multi-channel convergence as independent samples"

**Quantification requirement (added 2026-06-08)**: any synthesis
claim about "multiple channels converging" or "N channels
supporting" must be backed by a cross-channel correlation matrix
on the raw per-day primitive values, NOT asserted by sentence.
The
[cross-channel-correlation.md](../cards/cross-channel-correlation.md)
output is the canonical anchor for this claim in the current
project; new SUPPORTED channels added to synthesis must extend
that matrix BEFORE the synthesis claim is updated.

**Findings from the 2026-06-08 matrix that bind future framing**:

- **H02b ≡ H02d at per-day primitive level (ρ = +1.000)** — drop
  H02d from the channel count (see §3.9).
- **HA10 ≡ −HA07c (ρ = −0.922)** — morning BB peak and sleep
  stress mean are structurally the same signal via Garmin's BB
  algorithm. Treat as ONE autonomic-state cluster with two
  opposite-signed views, NOT two corroborating channels.
- **Effective N of independent signal clusters: 3-4 (not 7)**:
  - Cluster 1 (within-day stress): H02b/H02d + HA11 (ρ ≈ 0.38)
  - Cluster 2 (autonomic state): HA07c + HA10 ± HA06b (ρ ≈ −0.92 / ±0.39)
  - Cluster 3 (autonomic variability): HA07d (partially tied to
    Cluster 2 via HA07c at ρ ≈ 0.50)

**Honest effective-N Bonferroni**: α = 0.05 / N_clusters, NOT
α = 0.05 / N_verdicts. With 3-4 clusters, α_effective ≈ 0.013;
of the project's 11 primary verdicts, only H02d (p=0.011) clears
this bar.

**Rule**: future result.md files for any new SUPPORTED test on
existing channels must include a "correlation with prior load-
bearing primitives" line (Spearman ρ to each previously-SUPPORTED
primitive). If ρ > 0.7 with an existing primitive, the new test
is corroborative within an existing cluster, NOT a new independent
finding.

### 6.2 Card specificity / posterior probability

Discrimination magnitudes do NOT translate to "card correctness
when it fires." For any candidate card, compute Bayesian
posterior:

```
P(crash within 4 days | card fires) =
    (sensitivity × base rate) /
    (sensitivity × base rate + (1 − specificity) × (1 − base rate))
```

Where:
- sensitivity = card fire rate on crash 4-day windows
- specificity = 1 − card fire rate on null 4-day windows
- base rate ≈ 1.7% validate / similar magnitude train (15 crashes
  in ~890 days per era)

A card with +20 pp discrimination at 80% sensitivity / 60%
specificity has posterior ~3% per fire — **NOT a predictive
card**, even though the discrimination clears the locked bar.

**Specificity tables required BEFORE any card.md is written.**
Card text calibrated to posterior probability, NOT discrimination
magnitude.

### 6.3 Era as moderator, not just generalisation gate

The chronological train/validate split (per §4.3) serves TWO
statistical jobs:
- Held-out external validation
- Heterogeneity detection (era moderation)

The locked rule (both eras must SUPPORT per §4.4) does both with
one bar. The narrative layer should treat era as a moderator-of-
interest, not just a generalisation gate. Era-specific findings
are findings, not failures.

### 6.4 Symmetric application of methodology revisions

When methodology is revised (criteria, baseline, threshold type),
apply the revision SYMMETRICALLY to ALL tests in the affected
family — including tests that the project would prefer to keep.
The Theme A bundled re-test and the v2 threshold-sweep round
are the exemplars.

### 6.5 Atomic synthesis updates

When a methodology revision affects multiple tests, the synthesis
update must be ATOMIC: locked AFTER all tests under the revision
have completed, applied across all affected docs in one pass.
No partial updates that read selectively (e.g. updating with
RESCUES while CLOSES are still pending).

### 6.6 What NOT to surface in cards or synthesis (the no-go list)

Per [pem-pacing-indicators.md §5.4](../pem-pacing-indicators.md#54-what-not-to-build),
the following are refused in any user-facing surface regardless of
how well a test SUPPORTS:

- A composite **"crash risk percentage"** — we don't have a
  calibrated multi-day predictor; any single percentage is either
  dishonestly precise or trivially the base rate.
- **Red/yellow/green traffic lights** implying certainty.
- **Push notifications / alerts** — induces anxiety in PAIS
  patients; crowds the autonomic recovery the indicators are
  trying to protect.
- **Athletic "recovery score" framing** — conflates muscular
  adaptation with autonomic-envelope recharge; does damage in
  PAIS context.
- **Automated daily targets** (e.g. "aim for ≤ 3 000 steps") —
  step away from a control-and-shame loop that has hurt many
  patients in published activity-prescription literature on
  ME/CFS.
- **Age-predicted HR-max zones** — clinically wrong for this
  population (chronotropic incompetence affects >85% of ME/CFS
  patients per Workwell).
- **Time-/quota-contingent escalation** ("streaks", fixed weekly
  increments) — the GET harm mechanism.

A test verdict that would naturally suggest one of these surfaces
must explicitly redirect to a different framing in result.md.

## 7. Statistical reporting rules

### 7.1 Fisher's exact + binomial 95% CI

Every primary verdict table should report:
- Fisher's exact p-value on the 2×2 (crash trigger × null trigger)
- Binomial 95% CI on the crash-trigger frequency
- Binomial 95% CI on the null-trigger frequency

**Retrofit completed 2026-06-08** for all 11 then-existing primary
verdicts; results centralised at
[primary-verdict-statistics.md](../cards/primary-verdict-statistics.md)
(computed by [compute_fisher_ci.py](../cards/compute_fisher_ci.py)).
**Required going forward** for new tests: include this line in the
result.md template per §9.

### 7.2 Multi-comparison disclosure

Every result.md must state:
- The number of pre-registered hypotheses in the H##/HA## series
  to date
- The number of those that REFUTED
- For tests with sensitivity arms, explicit labelling of
  "PRIMARY arm" vs "SECONDARY / sensitivity arm" results

For diagnostics that evaluate multiple sub-conditions (e.g.
per-axis decomposition, parameter sensitivity), the family-wise
multi-comparison concern must be quantified explicitly (e.g.
expected ≥ 1 SUPPORTED under the null at the locked bar across
N comparisons).

### 7.3 Pooled-corpus descriptive arm

For tests with chronological train/validate split, optionally
report a pooled-corpus discrimination arm as exploratory
secondary. Surfaces homogeneous-but-weak signals that the
both-eras rule masks. Does NOT change the primary verdict.

### 7.4 Effect-size honesty

Discrimination in percentage points (pp) is the project's
standard; report alongside any other effect-size measure used.
Avoid using "strong" / "robust" / "substantial" without numbers
attached.

### 7.5 Pre-registration bar vs conventional statistical significance

**The lesson (2026-06-08)**: the project's 3-criterion bar
(frequency ≥ 60%, discrimination ≥ +15 pp, magnitude floor) is
**more permissive than conventional α=0.05 Fisher's exact** with
n=14-15 crash episodes per era. This was a conscious calibration
choice for n-of-1 exploratory research — the bar was set to
"discrimination worth seeing if real" rather than "discrimination
that distinguishes signal from null at conventional p < 0.05".

**Worked example from the 2026-06-08 retrofit
([primary-verdict-statistics.md](../cards/primary-verdict-statistics.md))**:

| anchor | recall | disc (pp) | Fisher p (one-sided) | passes locked bar? | passes α=0.05? |
|---|---:|---:|---:|:-:|:-:|
| H02b train | 71.4% | +29.9 | 0.029 | ✓ | ✓ |
| H02d bridge × 5d train | 92.3% | +28.3 | 0.011 | ✓ | ✓ |
| HA07d train | 84.6% | +19.6 | 0.093 | ✓ | — |
| HA07d validate | 86.7% | +21.7 | 0.070 | ✓ | — |
| HA10 validate | 86.7% | +16.2 | 0.148 | ✓ | — |
| HA01c validate | 80.0% | +19.5 | 0.109 | ✓ | — |

Only 2 of 11 primary verdicts reach α=0.05. Zero reach Bonferroni
α=0.005. The locked-bar SUPPORTED verdicts stay on record (locked
spec binds), but synthesis-level claims must be framed honestly
against both gates.

**Rules going forward**:

1. **The locked 3-criterion bar remains the pre-registration
   verdict gate**. This is unchanged. Project verdicts are
   evaluated against the locked bar, not against conventional
   α=0.05.

2. **result.md must report BOTH bars in the primary verdict table**:
   the locked-bar PASS/fail per criterion AND the Fisher's exact
   p-value with significance flags (α=0.05, Bonferroni-effective).
   This is the §7.1 retrofit-now-required-going-forward rule, with
   §7.5 specifying the dual-bar framing.

3. **Synthesis-level claims must use the appropriate bar for the
   audience**:
   - For internal n-of-1 research framing: locked-bar SUPPORTED is
     the headline.
   - For peer-review-level / generalisability claims: Fisher's
     exact significance is the headline, and "fails α=0.05"
     verdicts must be flagged explicitly.

4. **Effective-N Bonferroni** (per §6.1 + the
   [cross-channel-correlation.md](../cards/cross-channel-correlation.md)
   findings): use the cluster count, NOT the verdict count.
   Current effective N ≈ 3-4 clusters → α_effective ≈ 0.013.

5. **Future pre-registrations must specify the intended audience
   bar**. If the test is for synthesis-only use, the locked
   3-criterion bar is sufficient. If the test will inform
   shareable claims, the hypothesis.md should pre-commit to
   Fisher's exact at α=0.05 as a secondary bar.

**Why this matters for the project**: the 2026-06-08 retrofit
revealed that the project's "seven SUPPORTED on six channels"
synthesis framing was honest at the locked bar but **misleading
at conventional significance**. The framing tightens to
"three-to-four effectively-independent signal clusters, of which
one (within-day stress spike) clears α=0.05 one-sided Fisher's
exact". The discrimination findings stay on record; the framing
tightens.

## 8. Cross-references to other locked documents

The playbook does NOT duplicate rules that live in other locked
project documents; instead it references them:

- **Code conventions** (Python style, no unicode in scripts,
  surgical changes, etc.): [CLAUDE.md](../../../../CLAUDE.md) and
  [.claude/conventions.md](../../../../.claude/conventions.md).
- **Test discipline (TDD doctrine)**: [.claude/testing.md](../../../../.claude/testing.md)
  — RED-first rule, mandatory test layers, anti-patterns.
- **Security checklist**: [.claude/security-checklist.md](../../../../.claude/security-checklist.md).
- **UI / UX / design**: [docs/design/brief.md](../../design/brief.md)
  and [docs/architecture/frontend-conventions.md](../../architecture/frontend-conventions.md).
- **Cardinal principles + v1 requirements**: [docs/REQUIREMENTS.md](../../REQUIREMENTS.md).
- **Hypothesis registry**: [docs/research/garmin/hypotheses/registry.md](../hypotheses/registry.md)
  — the authoritative list of every pre-registered test, current
  verdict, and downstream implications.
- **Locked memory files** (user-specific principles): see
  `~/.claude/projects/c--Users-Gebruiker-Documents-gevoelscore-app/memory/`
  — particularly
  [`feedback_relative_not_absolute`](../../../../../.claude/projects/c--Users-Gebruiker-Documents-gevoelscore-app/memory/feedback_relative_not_absolute.md),
  [`feedback_no_emdash_in_ui`](../../../../../.claude/projects/c--Users-Gebruiker-Documents-gevoelscore-app/memory/feedback_no_emdash_in_ui.md),
  [`feedback_flag_contradictions`](../../../../../.claude/projects/c--Users-Gebruiker-Documents-gevoelscore-app/memory/feedback_flag_contradictions.md).

If a rule appears to be in tension between this playbook and one
of the above, surface the contradiction explicitly per
[`feedback_flag_contradictions`](../../../../../.claude/projects/c--Users-Gebruiker-Documents-gevoelscore-app/memory/feedback_flag_contradictions.md);
do not silently pick one.

## 9. Compliance checklist for new pre-registrations

A new hypothesis.md or diagnostic.md is compliant if it:

- [ ] Lives at `hypotheses/H##-name/` with the standard folder
      structure per §4.7
- [ ] Locks claim, measurement, threshold, window, direction
      BEFORE data
- [ ] References this playbook explicitly
- [ ] Uses **crash_v1** as default outcome per §4.2 (or
      explicitly justifies opting into crash_v2)
- [ ] Uses the **default train/validate split** per §4.3 + applies
      the **both-eras rule** per §4.4 (or explicitly marks as
      descriptive-only per §4.4)
- [ ] Uses **lagged baseline `[d-90, d-30]`** per §3.3 (unless
      explicitly justifying rolling)
- [ ] Uses **relative (z-score / percentile) thresholds** per §3.4
      (unless explicitly justifying absolute)
- [ ] Pre-commits primary direction per §3.5
- [ ] Pre-registers a **3-episode dry-run gate** per §2.3
- [ ] Specifies **3-criterion bar** (frequency / discrimination /
      magnitude) per §2.1
- [ ] Uses **null sample seed `20260605`** + N=200 per §4.5
- [ ] Applies validity floors per §4.6
- [ ] Pre-commits **decision rules** per §2.1 + maps outcomes to
      §2.6 verdict categories
- [ ] **Acknowledges caveats** the result.md must carry
      (channel-independence per §6.1; specificity per §6.2 where
      applicable)
- [ ] Plans **Fisher's exact + 95% CI** per §7.1
- [ ] Specifies **intended audience bar** per §7.5 (locked
      3-criterion only for internal n-of-1 research; locked +
      Fisher's α=0.05 for peer-review / shareable claims)
- [ ] If the test extends an existing primitive with a new window
      or sentinel handling, pre-checks **per-day correlation
      against the existing primitive** per §3.9 (if ρ > 0.95,
      reframe as an arm of the existing hypothesis)
- [ ] If the test claims a new channel SUPPORTED in synthesis,
      plans to extend the
      [cross-channel-correlation.md](../cards/cross-channel-correlation.md)
      matrix with the new primitive per §6.1 (do not assert
      "another channel converging" without the correlation row)
- [ ] States **multi-comparison context** per §7.2
- [ ] Plans **v2 threshold-sweep diagnostic** if applicable per
      §5.1
- [ ] Plans **parameter sensitivity** if applicable per §5.3
- [ ] If a SUPPORTED outcome is plausible, identifies which **no-go
      surfaces** per §6.6 must be avoided in any downstream card
- [ ] Notes any **hardware constraint** per §4.8 that applies

For DIAGNOSTICS (not new precursor tests), the additional rules
in §5 apply (per-axis: §5.2; threshold-monotonicity: §5.1;
parameter sensitivity: §5.3).

For CARDS (post-SUPPORTED craft step), the rules in §2.7 + §6.2 +
§6.6 apply.

## 10. Methodology history (context)

The current playbook reflects:
- Pre-registration discipline established with H01-H05 (2026-06-05)
- Train/validate split + both-eras rule + verdict categories
  established with the H01-H05 batch (2026-06-05)
- Crash_v1 + crash_v2 + dip + cluster locked (2026-06-05 → 2026-06-06)
- Sentinel handling banked from H02d (2026-06-06)
- Lagged baseline banked from Theme A (2026-06-06)
- Relative thresholds banked from HA06 → HA06b (2026-06-07)
- Direction choice banked from HA10 (2026-06-07)
- Second-order primitives banked from HA07c → HA07d (2026-06-07)
- Threshold-monotonicity v2 banked from v1→v2 round (2026-06-07,
  per user-locked Option C tightened)
- Channel non-independence + card specificity + era-as-moderator
  banked from peer-review §3/§4/§5 (2026-06-07)
- Atomic synthesis update + symmetric methodology revision banked
  from v1→v2 round (2026-06-07)
- Folder structure + card.md craft rule + verdict categories +
  no-go list incorporated into playbook (2026-06-07, Option A
  consolidation expansion)
- Composite construction lesson banked from HA01b per-axis
  diagnostic (2026-06-07, §3.8)
- **Tier 2 statistical audits banked (2026-06-08)** —
  Fisher's exact retrofit on 11 verdicts revealed only 2 clear
  α=0.05; cross-channel correlation matrix revealed H02b ≡ H02d
  (ρ=+1.000) and HA10 ≡ −HA07c (ρ=−0.922). Three playbook
  additions:
  - §3.9 same-primitive-different-window tests are not independent
    corroborations
  - §6.1 quantification requirement for "multiple channels
    converging" claims — must be backed by correlation matrix,
    not asserted by sentence
  - §7.5 pre-registration bar vs conventional statistical
    significance — explicitly different gates, dual-bar reporting
    required
  Compliance checklist (§9) gained two new items: per-day
  correlation pre-check for window-variants, and synthesis
  correlation-matrix extension for new channels.

## 11. When this playbook itself needs revision

If a new lesson is banked from a future test or peer review:
1. Lock the lesson in a dated update note here ("Updated 2026-06-XX")
2. Apply the lesson to subsequent pre-registrations
3. If the lesson invalidates a prior interpretation, follow the
   symmetric-revision discipline of §6.4

If the playbook itself has a defect (e.g. a rule that produces
an inconvenient outcome), revision follows the v3 escape hatch
rule of §5.4: external authority, pre-locked inadequacy,
symmetric re-application.

A revision lock creates a new methodology document
(`testing-playbook-v2.md`) rather than editing this document in
place. This document becomes the historical baseline.

---

*Locked 2026-06-07 (Option A consolidation + established-conventions
expansion). Tier 2 statistical-audit additions 2026-06-08
(§3.9, §6.1 quantification rule, §7.5, §9 checklist items + §10
history entry). All subsequent pre-registrations must comply with
§9 checklist or explicitly justify deviation.*
