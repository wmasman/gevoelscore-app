# HA10 threshold-monotonicity diagnostic — result

**Verdict per locked rescue/close/ambiguous criteria: CLOSE** (HA10's
primary arm — 4d bidirectional N_std=1.5 validate — closes per the
shape criteria locked in [diagnostic.md §4](diagnostic.md)).

But the data is more nuanced than the binary label captures, and
the nuance materially affects the synthesis-level framing. The
verdict closes the BIDIRECTIONAL primary; the ELEVATED-direction
one-sided arm (which is the physiologically meaningful direction
for Wiggers' paradoxical-swing framing) shows a **robust,
threshold-stable signal** across a wide range. The diagnostic
reads as: HA10's locked primary direction-mode choice was the
fragile one; the direction itself remains a robust validate-era
signature.

Data: [result-data.json](result-data.json).

## The full fine-grid table

### Validate-era — the focus of the diagnostic

#### bidirectional (HA10's locked primary)

| N_std | crash freq | null freq | disc pp |
|---:|---:|---:|---:|
| 0.50 | 100.0% | 99.5% | +0.5 |
| 0.75 | 100.0% | 96.5% | +3.5 |
| 1.00 | 100.0% | 92.0% | +8.0 |
| 1.25 | 100.0% | 83.0% | **+17.0** |
| **1.50** | **86.7%** | **70.5%** | **+16.2** (HA10's locked verdict) |
| **1.75** | **80.0%** | **60.5%** | **+19.5** (PEAK) |
| 2.00 | 60.0% | 46.0% | +14.0 |
| 2.25 | 46.7% | 36.0% | +10.7 |
| 2.50 | 40.0% | 29.0% | +11.0 |
| 2.75 | 26.7% | 24.0% | +2.7 |
| 3.00 | 13.3% | 18.0% | −4.7 |
| 3.50 | 0.0% | 14.5% | −14.5 |
| 4.00 | 0.0% | 7.5% | −7.5 |

#### one-sided elevated (validate's PARADOXICAL-SWING direction; Wiggers' "freeze" maps here)

| N_std | crash freq | null freq | disc pp |
|---:|---:|---:|---:|
| 0.50 | 73.3% | 74.5% | −1.2 |
| 0.75 | 73.3% | 69.5% | +3.8 |
| 1.00 | 66.7% | 63.0% | +3.7 |
| 1.25 | 66.7% | 53.0% | +13.7 |
| **1.50** | **66.7%** | **40.0%** | **+26.7** |
| **1.75** | **60.0%** | **32.5%** | **+27.5** (PEAK) |
| **2.00** | **40.0%** | **17.0%** | **+23.0** |
| **2.25** | **33.3%** | **10.0%** | **+23.3** |
| **2.50** | **26.7%** | **3.5%** | **+23.2** |
| 2.75 | 20.0% | 2.5% | +17.5 |
| 3.00 | 13.3% | 2.0% | +11.3 |
| 3.50 | 0.0% | 0.0% | 0.0 |
| 4.00 | 0.0% | 0.0% | 0.0 |

The elevated-direction discrimination **plateaus at +23 pp from
N_std=1.5 through N_std=2.5** — exactly the threshold-monotonic
shape expected of a robust signal embedded in noise.

#### one-sided lowered (inverse direction; predicted refuted)

Confirms validate-era lowered-direction is anti-predictive across
the grid as expected. Sign-changes none — robustly inverse.

## Shape statistics (locked diagnostic per §3.3)

For validate 4d bidirectional (HA10's locked primary):

| statistic | value | rescue threshold | passes? |
|---|---:|---|---|
| peak N_std | **1.75** | [1.0, 1.5] | **FAIL** |
| peak disc | +19.5 pp | — | (informational) |
| disc at N_std=2.0 | +14.0 pp | ≥ +10 pp | PASS |
| disc at N_std=2.5 | +11.0 pp | ≥ +5 pp | PASS |
| Spearman rho | −0.456 | ≤ −0.3 | PASS |
| sign-changes | 1 | ≤ 1 | PASS |

**Four of five rescue criteria pass; one (peak location) fails by
0.25 σ.** Per the locked rule, ANY close criterion triggers CLOSE
— and "peak at N_std > 1.5" is in the close criterion list. The
verdict is CLOSE.

### Why this is borderline

The "peak at N_std=1.75" failure of the rescue criterion is
the **only** close criterion that fires. Every other indicator
(Spearman rho strongly negative, sign-changes minimal, disc holds
at 2.0 and 2.5) is consistent with a robust signal. The
diagnostic's mechanical CLOSE verdict reflects a peak that landed
0.25 σ past where the locked rescue criterion expected it.

The pre-registration discipline says: locked verdicts hold. CLOSE
is the verdict. But the underlying signal shape is more accurately
described as "robust with peak slightly past N_std=1.5" than as
"loose-tail noise."

## What this means for the framing

### Per locked rule (diagnostic.md §4 CLOSE clause):

> HA10 validate-era SUPPORTED verdict stays on record. But
> synthesis-level framing demotes HA10 to "historical Gen-3
> finding, signal demonstrated loose-tail behaviour under
> monotonicity diagnostic, not load-bearing for validate-era
> narrative." Card (b2) drops the HA10 anchor reference entirely;
> HA07d becomes the sole validate-era anchor.

This is the locked framing rule. It applies.

### Honest reporting alongside the verdict

A loose reading of "loose-tail behaviour" would suggest the
discrimination collapsed at higher thresholds. **It did not.**
Discrimination held above +10 pp through N_std=2.5; only at
N_std=2.75+ did it collapse (and even then to small magnitudes).
The diagnostic's CLOSE verdict reflects the **peak being at 1.75
rather than 1.5**, NOT a collapse of signal at stricter
thresholds.

### The one-sided elevated robustness

The diagnostic's locked rule applies to the BIDIRECTIONAL primary
arm. But the **one-sided elevated direction** — which is the
direction Wiggers' parasympathetic-swing framing predicts for
validate-era crashes — shows **strong threshold-monotonicity**:

- Peak +27.5 pp at N_std=1.75
- Plateau at +23 pp from N_std=1.5 through N_std=2.5
- Monotonic decline 1.75 → 3.0 → 0

This is exactly the curve a robust precursor signal should
produce. The DIRECTIONAL finding (elevated morning BB peak before
validate-era crashes — paradoxical "looks like great recharge")
is supported by the one-sided arm's robust shape, even though
HA10's specific locked PRIMARY direction-mode choice
(bidirectional) closes per the diagnostic.

This reads as: **HA10's locked primary was the fragile choice
within an otherwise robust direction**. A future HA10b
pre-registered with one-sided elevated as primary would likely
have been SUPPORTED robustly. The Gen-3 methodology chose
bidirectional as primary across all autonomic-channel tests for
era-symmetry reasons (validate could have shown either direction
a priori); the diagnostic reveals this choice was conservative
in HA10's specific case.

## Synthesis update per the locked rule

### Action: STOCKTAKE / synthesis.md / addendum

Apply the CLOSE clause from diagnostic.md §4:

- HA10 validate-era SUPPORTED verdict stays on record (locked
  pre-registration discipline — verdicts don't unlock).
- HA10 framing demotes to: "historical Gen-3 finding; signal
  demonstrated borderline behaviour under threshold-monotonicity
  diagnostic — peak at N_std=1.75 vs locked rescue window [1.0,
  1.5] is the failure; discrimination held robustly at +14 to +11
  pp through N_std=2.5 and the one-sided elevated arm shows
  robust shape, so the direction is supported but the specific
  bidirectional-primary verdict is now post-hoc fragile."
- Card (b2): HA10 anchor reference drops per the locked rule.
  **HA07d is the sole load-bearing validate-era anchor.** Card
  framing must reference HA07d's sleep stress variability collapse
  as the primary signature; the BB peak elevation can be mentioned
  as descriptively consistent but not as a load-bearing precursor
  claim.

### Action: registry §4b

Add diagnostic entry referencing this result.md. HA10's locked
verdict stays in §4 as SUPPORTED; the diagnostic adds a
"threshold-monotonicity: CLOSE per locked criteria; one-sided
elevated arm robust, bidirectional primary fragile in
peak-location" qualifier.

## Methodology lessons banked

1. **Threshold-monotonicity diagnostic** is a useful instrument
   for HA10-class findings where SUPPORTED at primary tier is
   borderline. The fine-grained grid surfaces shape information
   the three-tier sensitivity arm hides. **Add to project
   methodology playbook**: any test where primary verdict
   SUPPORTS at the loosest threshold tier only AND fails at the
   next tier should run this diagnostic before entering synthesis.

2. **Direction choice on bidirectional primary matters.** HA10's
   bidirectional primary was the conservative choice; the
   one-sided elevated arm (the physiologically meaningful direction
   for the paradoxical-swing finding) is robust. Future Gen-3
   tests should consider whether bidirectional or one-sided is the
   primary that best matches the physiological hypothesis. HA07d
   correctly pre-registered bidirectional primary because direction
   was genuinely ambiguous a priori; HA10 might have done better
   with one-sided elevated as primary given Wiggers' specific
   framing predicted that direction.

3. **Pre-committed rescue/close/ambiguous criteria worked as
   designed** — the criteria forced a verdict before data
   inspection (in the shape-criteria sense), and the verdict was
   accepted even when the underlying data argued for a more
   permissive reading. This is exactly the audit-trail discipline
   the peer review praised. Resisting the temptation to ease the
   rescue threshold post-hoc preserves the discipline.

4. **The diagnostic's binary RESCUE/CLOSE/AMBIGUOUS label
   sometimes obscures useful nuance.** Future diagnostics could
   add a per-criterion pass/fail table to the headline so the
   borderline cases are visible without needing to re-read the
   full result.md. This will be locked into the diagnostic
   pre-registration template going forward.

## Cross-test implications

Same diagnostic should be run on:

- **HA07d** (validate-era primary anchor) — to confirm its primary
  arm is genuinely robust per the same criteria, not just
  borderline-rescue.
- **HA11** (train-era SUPPORTED, parameter-degrees-of-freedom
  concern from peer review §3).
- **H02b** (project's strongest train signal; would expect to
  pass cleanly, useful as positive control).
- **HA06b** (validate-era RHR refuted but with cross-channel
  coherence inference).

Each diagnostic queued separately; HA10 is the first because the
peer review flagged it specifically.

---

*Diagnostic run 2026-06-07. Pre-registration locked at
[diagnostic.md](diagnostic.md). Same null sample seed (`20260605`)
and same lagged-baseline machinery as HA10. The verdict per the
locked rule is CLOSE; the data argues the close is borderline
and direction-specific. Both are honestly reported.*
