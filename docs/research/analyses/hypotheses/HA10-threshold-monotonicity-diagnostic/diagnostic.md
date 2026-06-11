# HA10 threshold-monotonicity diagnostic — pre-registration

**Pre-registration written 2026-06-07 in response to the
[independent variable-architecture peer review §3](../../review/2026-06-07-variable-architecture-review.md)
which flagged HA10 as "the project's most fragile headline" on the
grounds that HA10 validate-era SUPPORTED at N_std=1.5 only and
refuted at N_std=2.0 and N_std=2.5 — characterised as "signal
sitting in the loose-deviation tail" rather than threshold-monotonic
behaviour expected of robust signals.**

This is a **diagnostic**, NOT a new precursor test. It does not
produce a SUPPORTED/REFUTED verdict that adds to or replaces HA10's
locked primary verdict (validate SUPPORTED at +16.2 pp at 4d
N_std=1.5 bidirectional remains in force regardless of what this
diagnostic finds). The diagnostic produces a **rescue/close/ambiguous
label** that informs how HA10 is framed in synthesis-level documents
going forward.

## Honesty caveat on pre-registration timing

HA10's discrimination values at N_std = 1.5 / 2.0 / 2.5 have
already been computed and inspected. A strict pre-registration on
the same N_std grid would be tainted by that prior inspection.

This diagnostic therefore pre-registers two things that are NOT
direct restatements of values already seen:

1. **Shape criteria** (monotonicity tests, peak-location tests,
   robustness ratios) — these are testable claims about the SHAPE
   of the discrimination-vs-threshold curve, independent of the
   specific N_std=1.5 value.

2. **Fine-grid intermediate values** at N_std ∈ {1.0, 1.25, 1.75,
   2.25, 2.75, 3.0} — these have not been computed for HA10 and
   are genuinely unseen.

The N_std = 1.5 / 2.0 / 2.5 grid points are included for
completeness but should be understood as "expected to reproduce
prior values" rather than as pre-registered predictions.

## 1. The shape question

A real precursor signal embedded in noise should produce a
discrimination-vs-threshold curve that is **monotonically declining
in magnitude as the threshold tightens** — fewer crash and null
windows trigger, but discrimination magnitude holds reasonably or
decays gracefully because the signal is *real* in the underlying
distribution.

A signal that "sits in the loose-deviation tail" (per the peer
review's diagnosis) should show non-monotonic or cliff-like
behaviour: maximum discrimination at intermediate threshold tier,
sharp drop-off above it, or non-monotonic peaks suggesting the
signal is artifact of a specific threshold cut.

This diagnostic measures both qualitative shape and quantitative
robustness ratios across a fine threshold grid.

## 2. Data sources

- Identical to HA10: morning BB peak primitive from
  [HA10-bb-overnight-recharge/](../HA10-bb-overnight-recharge/)
  result-data.json (which uses morning HIGHEST anchor between
  03:00-10:00 local; full corpus 2022-09-03 → 2026-06-05; 1670
  valid days).
- Same lagged baseline machinery, same null sample, same seed
  `20260605`. The diagnostic re-runs the test under a fine grid
  of N_std values; nothing else changes.

## 3. Measurement protocol

### 3.1 Fine N_std grid

Sweep N_std across 13 tiers:

```
0.5, 0.75, 1.0, 1.25, 1.5, 1.75, 2.0, 2.25, 2.5, 2.75, 3.0, 3.5, 4.0
```

(11 tiers in the primary range [0.5, 3.0] plus 2 extra-tight tiers
3.5 and 4.0 to characterise the deep tail.)

### 3.2 For each N_std tier

Compute exactly the same metrics HA10 already reports:

- Crash trigger frequency (per era: train, validate)
- Null trigger frequency
- Discrimination (crash − null, pp)
- Median |z| on triggering crashes
- Verdict under the locked HA10 bar (a + b + c)

For three direction modes: bidirectional, one-sided elevated,
one-sided lowered.

### 3.3 Shape statistics

Computed across the full grid for each (era, direction) pair:

- **Argmax**: at which N_std does discrimination peak?
- **Peak value**: maximum discrimination across grid.
- **Decay-from-peak**: discrimination at N_std=peak+0.5 divided by
  peak value (1.0 = no decay; 0.0 = full collapse).
- **Spearman ρ(N_std, discrimination)**: monotonicity test. Negative
  ρ = discrimination declines as threshold tightens (monotonic
  expected behaviour). Positive ρ or near-zero ρ = non-monotonic /
  signal not behaving like a threshold-deviating-from-baseline.
- **Sign-changes count**: number of times discrimination crosses
  zero as N_std varies across the grid. Robust signal: ≤ 1 sign
  change. Loose-tail noise: ≥ 2 sign changes.

## 4. Pre-committed rescue / close / ambiguous criteria

Applied to HA10's primary arm (4d N_std=1.5 bidirectional
validate-era — the headline whose fragility the peer review
flagged).

### RESCUE (HA10 was robust all along, peer-review fragility
diagnosis overstated)

All of:

- **Peak at N_std ∈ [1.0, 1.5]** (signal is broad-tail, not
  loose-tail).
- **Discrimination ≥ +10 pp at N_std = 2.0** (gentle decline, not
  cliff).
- **Discrimination ≥ +5 pp at N_std = 2.5** (signal survives into
  the strict tier).
- **Spearman ρ ≤ −0.3** (discrimination is monotonically declining
  as N_std tightens, the shape expected of a real signal).
- **Sign-changes count ≤ 1** (no non-monotonic peaks).

If RESCUE: HA10 framing in synthesis docs upgrades from
"corroborating-but-fragile" to "corroborating, threshold-stable
within reasonable range." HA07d remains the primary validate-era
anchor (it is more robust); HA10 becomes a defensible
co-equal secondary.

### CLOSE (HA10 was loose-tail noise, peer review correct)

Any of:

- **Peak at N_std > 1.5** or **< 0.75** (signal is artefact of a
  specific cut, not a robust threshold-deviation).
- **Discrimination < +5 pp at N_std = 2.0** (cliff).
- **Discrimination < 0 pp at N_std = 2.5** (signal reverses).
- **Spearman ρ > −0.1** (discrimination is NOT monotonic in the
  expected direction).
- **Sign-changes count ≥ 2** (signal is bumpy / non-monotonic).

If CLOSE: HA10 validate-era SUPPORTED verdict stays on record
(pre-registration discipline: locked verdicts don't get unlocked
by post-hoc diagnostics). But synthesis-level framing demotes HA10
to "historical Gen-3 finding, signal demonstrated loose-tail
behaviour under monotonicity diagnostic, not load-bearing for
validate-era narrative." Card (b2) drops the HA10 anchor reference
entirely; HA07d becomes the sole validate-era anchor.

### AMBIGUOUS (neither rescue nor close criteria met)

Default. HA10 framing stays at "corroborating-but-fragile"; the
diagnostic findings get a paragraph in synthesis but neither
upgrade nor downgrade the framing materially. Queue HA10b as a
new pre-registered test on extended data (when available) with
the fine grid as primary.

## 5. Caveats locked before running

- **The criteria above are committed as written; outcome cannot
  trigger criterion revision.** If the data falls between rescue
  and close, the verdict is AMBIGUOUS — no shifting either
  threshold post-hoc.

- **This diagnostic does NOT unlock HA10's locked primary
  verdict.** HA10 validate-era SUPPORTED at +16.2 pp 4d N_std=1.5
  bidirectional remains an accurate report of what the locked spec
  produced. The diagnostic only informs how that verdict is
  *framed* in synthesis-level documents.

- **The diagnostic applies to HA10 specifically.** Whether to run
  the same diagnostic on other tests (HA07d, HA11, HA06b, etc.) is
  a separate decision; if their primary verdicts also show
  loose-tail behaviour on a similar diagnostic, the project's
  methodology playbook needs to add "threshold-monotonicity check"
  as required practice for all SUPPORTED verdicts going forward.

- **The diagnostic does not address other peer-review critiques**
  about HA10 (BB algorithm opacity, channel-non-independence,
  power-bounded N=15). It addresses the specific
  threshold-fragility critique only.

## 6. What the diagnostic produces

A `result.md` reporting:
- The full 13-tier × 3-direction × 2-era discrimination table.
- The shape statistics (argmax, peak, decay-from-peak, Spearman ρ,
  sign-changes).
- The pre-committed verdict (RESCUE / CLOSE / AMBIGUOUS) for the
  validate-era primary arm (4d bidirectional).
- An ASCII discrimination-vs-threshold curve (for quick visual
  shape inspection).
- A one-paragraph framing update for synthesis-level docs.

A `result-data.json` with the full numeric table for downstream
re-analysis.

## 7. What this produces in the registry

The diagnostic's outcome (RESCUE / CLOSE / AMBIGUOUS) is recorded
in registry §4b as a `(diagnostic)` entry alongside HA10's existing
verdict — NOT as a new SUPPORTED/REFUTED test. The registry entry
makes clear that HA10's primary verdict is unchanged.

---

*Pre-registration locked 2026-06-07. The diagnostic does not
require a 3-episode dry-run (no new metric primitive being
introduced; same data, same machinery, only the threshold grid
is being expanded). Same null seed `20260605` as HA10. Outcome
binds the framing in STOCKTAKE, synthesis, addendum, and
pem-pacing-indicators per the rescue/close/ambiguous criteria
in §4.*
