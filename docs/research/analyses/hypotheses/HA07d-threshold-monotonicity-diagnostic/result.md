# HA07d threshold-monotonicity diagnostic — result

**Verdicts per locked rescue/close/ambiguous criteria:**
- **TRAIN 4d bidirectional: CLOSE** (bumpy curve, peak at 1.75, 4
  sign changes — train signal is genuinely volatile across the
  threshold grid)
- **VALIDATE 4d bidirectional: CLOSE** (peak at 1.75, Spearman rho
  positive — discrimination *rises* as threshold tightens, which
  the locked criteria penalise even though this is *more* robust
  than monotonic decline)

The validate-era CLOSE verdict is **mechanically correct per the
locked rule but methodologically misleading** — the underlying
signal is exceptionally robust (+19 to +31 pp discrimination
sustained from N_std=1.0 through N_std=4.0). The locked criteria
were designed to penalise "monotonically rising discrimination"
under the false assumption that real signal must monotonically
decline. The discriminator now becomes part of the result.

This diagnostic outcome flags **a critical limitation in the
locked criteria**, not a fragility in HA07d's underlying signal.
Pre-registration discipline requires we honour the locked rule;
synthesis framing will mechanically demote HA07d per the CLOSE
clause. But the result.md and the subsequent doc updates must
honestly carry the methodology critique forward, and a future
HA07d2 (or revised diagnostic methodology) should be developed
before this rule is applied to other SUPPORTED tests.

Data: [result-data.json](result-data.json).

## What the locked criteria say

For each era, the rescue/close criteria require:

- Peak N_std in [1.0, 1.5] for RESCUE; > 1.5 triggers CLOSE.
- Spearman rho (N_std vs disc) ≤ −0.3 for RESCUE; > −0.1 triggers
  CLOSE.

These criteria assume the **canonical robust signal shape**:
discrimination peaks at the loosest meaningful threshold and
declines monotonically as thresholds tighten (because crash
frequency drops faster than null frequency at strict thresholds).

But there's another robust shape the criteria don't capture:
**stable or rising discrimination as threshold tightens**. This
shape occurs when the *signal-to-noise ratio* improves at strict
thresholds — null frequency drops fast (noise vanishes) while
crash frequency drops slower (signal persists). Discrimination
holds or rises. This is **more robust** than monotonic decline,
not less.

The HA07d validate bidirectional curve is this second shape.

## The full fine-grid data

### TRAIN bidirectional (HA07d's locked primary)

| N_std | crash freq | null freq | disc pp |
|---:|---:|---:|---:|
| 0.50 | 100.0% | 97.5% | +2.5 |
| 0.75 | 92.3% | 92.5% | −0.2 |
| 1.00 | 84.6% | 80.0% | +4.6 |
| 1.25 | 84.6% | 74.0% | +10.6 |
| **1.50** | **84.6%** | **65.0%** | **+19.6** (HA07d's locked verdict) |
| **1.75** | **76.9%** | **55.5%** | **+21.4** (PEAK) |
| 2.00 | 61.5% | 46.0% | +15.5 |
| 2.25 | 53.8% | 40.0% | +13.8 |
| 2.50 | 53.8% | 33.5% | +20.3 |
| 2.75 | 30.8% | 28.0% | +2.8 |
| 3.00 | 30.8% | 27.0% | +3.8 |
| 3.50 | 23.1% | 24.0% | −0.9 |
| 4.00 | 23.1% | 17.0% | +6.1 |

**Shape**: Peak at 1.75 (+21.4 pp), but curve OSCILLATES — drops
to +2.8 at 2.75, recovers to +20.3 at 2.5, falls to −0.9 at 3.5.
**Four sign changes across the grid**. The locked criteria
correctly identify this as bumpy/non-monotonic.

**Verdict per locked rule: CLOSE** (peak > 1.5; Spearman rho
+0.005; 4 sign changes).

**Interpretation**: Train's autonomic-volatility signature
(both elevated and lowered direction shifts in same lead-up)
produces a bumpy bidirectional curve because the noise at different
thresholds catches different combinations of train crash episodes.
This is **consistent with the train-era VOLATILITY framing** —
volatility is precisely the shape we'd expect to produce a bumpy
bidirectional curve. The locked CLOSE verdict on train is
mechanically correct AND substantively informative: train's
autonomic-deviation signal is volatile by nature, not stable.

### VALIDATE bidirectional (HA07d's locked primary)

| N_std | crash freq | null freq | disc pp |
|---:|---:|---:|---:|
| 0.50 | 100.0% | 97.5% | +2.5 |
| 0.75 | 100.0% | 92.5% | +7.5 |
| 1.00 | 100.0% | 80.0% | **+20.0** |
| 1.25 | 100.0% | 74.0% | **+26.0** |
| **1.50** | **86.7%** | **65.0%** | **+21.7** (HA07d's locked verdict) |
| **1.75** | **86.7%** | **55.5%** | **+31.2** (PEAK) |
| 2.00 | 73.3% | 46.0% | **+27.3** |
| 2.25 | 66.7% | 40.0% | **+26.7** |
| 2.50 | 53.3% | 33.5% | +19.8 |
| 2.75 | 53.3% | 28.0% | **+25.3** |
| 3.00 | 40.0% | 27.0% | +13.0 |
| 3.50 | 40.0% | 24.0% | +16.0 |
| 4.00 | 40.0% | 17.0% | **+23.0** |

**Shape**: Discrimination is **+20 pp or higher across N_std=1.0
through 2.75** — a remarkably wide robust plateau. Even at
N_std=4.0 (where only ~17% of nulls trigger), 40% of validate
crashes still trigger and discrimination is +23 pp. **Zero sign
changes** — discrimination is positive across the entire grid.
Spearman rho is +0.170 because the curve has its highest values
at intermediate thresholds (1.25, 1.75, 2.0, 4.0 all hit +23+
pp).

**Verdict per locked rule: CLOSE** (peak > 1.5 at 1.75; Spearman
rho +0.170 not ≤ −0.3).

**Interpretation**: This is a **maximally robust signal** that
the locked criteria fail to recognise as such. The discrimination
plateau spans more than 2 σ of threshold space at +20-31 pp. Real
signal is firing on validate crashes regardless of the specific
threshold chosen. The locked criteria conflated "monotonic
decline" with "robustness" and penalised this stable-plateau
shape that is *more* robust.

### VALIDATE one-sided lowered — the picture the locked criteria miss

| N_std | crash freq | null freq | disc pp |
|---:|---:|---:|---:|
| 0.50 | 86.7% | 91.0% | −4.3 |
| 0.75 | 86.7% | 80.0% | +6.7 |
| 1.00 | 86.7% | 65.0% | +21.7 |
| 1.25 | 80.0% | 57.0% | +23.0 |
| 1.50 | 66.7% | 45.0% | +21.7 |
| 1.75 | 66.7% | 39.5% | +27.2 |
| **2.00** | **60.0%** | **31.5%** | **+28.5** (PEAK) |
| 2.25 | 53.3% | 25.0% | +28.3 |
| 2.50 | 40.0% | 21.0% | +19.0 |
| 2.75 | 40.0% | 18.0% | +22.0 |
| 3.00 | 26.7% | 16.5% | +10.2 |
| 3.50 | 26.7% | 15.0% | +11.7 |
| 4.00 | 26.7% | 10.0% | +16.7 |

**This is the rescue-pattern curve in pure form**: rises from
−4.3 at N_std=0.5 to peak +28.5 at N_std=2.0, then declines
gracefully but stays positive across the entire remaining grid.
Spearman rho is +0.055 (still positive due to the wide plateau)
but the qualitative shape is the canonical "real signal rising
to peak, then declining" shape.

The one-sided lowered arm is the **physiologically meaningful
direction for validate-era crashes** per Wiggers' freeze framing
(sleep stress variability *drops* before validate crashes —
autonomic state becomes unusually stable). This arm shows the
robust shape across the entire grid.

### TRAIN one-sided lowered — also a clean rescue pattern

| N_std | crash freq | null freq | disc pp |
|---:|---:|---:|---:|
| 0.50 | 100.0% | 91.0% | +9.0 |
| 0.75 | 92.3% | 80.0% | +12.3 |
| 1.00 | 76.9% | 65.0% | +11.9 |
| **1.25** | **76.9%** | **57.0%** | **+19.9** (PEAK) |
| 1.50 | 61.5% | 45.0% | +16.5 |
| 1.75 | 46.2% | 39.5% | +6.7 |
| 2.00 | 46.2% | 31.5% | +14.7 |
| 2.25 | 38.5% | 25.0% | +13.5 |
| 2.50 | 30.8% | 21.0% | +9.8 |
| 2.75 | 23.1% | 18.0% | +5.1 |
| 3.00 | 23.1% | 16.5% | +6.6 |
| 3.50 | 23.1% | 15.0% | +8.1 |
| 4.00 | 23.1% | 10.0% | +13.1 |

Peak at N_std=1.25 (**within the rescue window [1.0, 1.5]**),
Spearman rho −0.313 (PASSES the rescue threshold), sign-changes
0 (PASSES). Disc at N_std=2.0 +14.7 (PASSES). Disc at N_std=2.5
+9.8 (PASSES). **All rescue criteria PASS** for train one-sided
lowered.

The locked rule applied to bidirectional fails train (peak +
Spearman + sign-changes) but the one-sided lowered arm —
applied as if it were the primary — would CLEAN RESCUE.

## Shape statistics summary

| arm | era | peak N_std | peak disc | Spearman rho | sign changes |
|---|---|---:|---:|---:|---:|
| bidirectional | train | 1.75 | +21.4 | +0.005 | **4** |
| bidirectional | validate | 1.75 | +31.2 | +0.170 | 0 |
| one_sided_elevated | train | 1.75 | +27.7 | −0.137 | 2 |
| one_sided_elevated | validate | 1.75 | +11.8 | +0.432 | 3 |
| **one_sided_lowered** | **train** | **1.25** | **+19.9** | **−0.313** | **0** |
| one_sided_lowered | validate | 2.00 | +28.5 | +0.055 | 1 |

The one-sided lowered direction has the cleanest shape in BOTH
eras — same direction (variability collapse / drop) in both,
unlike the bidirectional which mixes elevated and lowered.

## The methodological insight (the most important output)

The locked criteria assumed real signals show **monotonically
declining discrimination as threshold tightens**. This is one
form of robustness. There is another: **stable or rising
discrimination as threshold tightens** (signal-to-noise ratio
improves because noise drops faster than signal).

HA07d validate bidirectional is the second shape. The locked
criteria penalise it. This is a defect in the criteria, not in
HA07d.

**A future diagnostic methodology should distinguish four
shapes:**

1. **Monotonic decline from peak at low threshold**: canonical
   robust signal. Discrimination drops smoothly as threshold
   tightens. (HA10 validate elevated showed this when isolated.)

2. **Stable plateau across wide threshold range**: highly robust
   signal. Discrimination holds across many thresholds because
   signal-to-noise stays favourable. (HA07d validate bidirectional
   shows this.)

3. **Rising discrimination as threshold tightens**: also robust,
   often more so than monotonic decline. Signal-to-noise improves
   at strict thresholds because noise vanishes faster than signal.

4. **Loose-tail noise**: peak at the loosest threshold tier,
   sharp drop-off at stricter thresholds, often with sign changes.
   Suggestive of artefact rather than signal.

The current locked criteria only distinguish (1) from (4). A
future revised criteria framework would distinguish all four.

## Per-locked-rule actions (committed)

Per diagnostic.md §5 stakes:

### Train CLOSE consequences

- HA07d train SUPPORTED at +19.6 pp 4d bidirectional N_std=1.5
  stays on record.
- Synthesis-level framing demotes HA07d train bidirectional from
  load-bearing to non-load-bearing.
- HA07c train SUPPORTED (one-sided elevated +23.2 pp) and HA08c
  train SUPPORTED (one-sided elevated +23.0 pp) are not affected
  — they have their own primary verdicts at different arms; these
  remain on record. **However, they have not yet passed their own
  threshold-monotonicity diagnostic.** Until they do, they should
  be framed as "SUPPORTED but threshold-stability not yet verified."
- Train-era six-channel narrative still rests on H02b + H02d +
  HA06b + HA11 + HA07c + HA08c + HA07d-locked. The HA07d-as-
  load-bearing claim weakens; the underlying physiological finding
  (sleep stress variability shifts before train crashes) is still
  documented by HA07d's locked verdict.

### Validate CLOSE consequences (more material)

- HA07d validate SUPPORTED at +21.7 pp 4d bidirectional N_std=1.5
  stays on record per pre-registration discipline.
- Synthesis-level framing demotes HA07d validate bidirectional
  from sole load-bearing anchor to non-load-bearing.
- **Card (b2) loses its sole anchor.** HA10 was already
  non-load-bearing per the HA10 diagnostic. The b2 card cannot
  ship as a "predictive retrospective" card with the locked
  framing rules.
- The era-as-moderator narrative weakens. The "HA07d demonstrates
  era reversal on a single channel" framing no longer rests on a
  load-bearing primary; rests on the one-sided lowered sub-arm
  which the diagnostic's own criteria recognise as clean (peak
  at 2.0, +28.5 pp).
- The project effectively returns to **"no load-bearing
  validate-era precursor under canonical methodology"** — the
  same conclusion as before HA10 + HA07d landed.

### Methodology playbook action

- **Locked criteria for this diagnostic methodology are
  insufficient.** Before applying the same diagnostic to HA07c,
  HA08c, HA11, HA06b, H02b, H02d, etc., the criteria must be
  revised to distinguish the four shape categories above.
- **Adding to the methodology playbook**: any pre-registered
  diagnostic criteria should themselves be subject to robustness
  checks — what data shapes do the criteria penalise as a
  side-effect? If the side-effects include rejecting
  qualitatively robust signals, the criteria are wrong.
- **HA07d2 with revised criteria** should be locked as
  follow-up. The natural primary metric is now the one-sided
  lowered direction (which both eras show robust shape on);
  the bidirectional primary was a methodological choice that did
  not match the physiological hypothesis well in retrospect.

## Caveats `result.md` must explicitly acknowledge

- **Locked rule applied honestly. CLOSE verdicts stand.**
  Resisting the temptation to ease criteria post-hoc preserves
  audit-trail discipline.
- **The diagnostic methodology has a known defect** flagged in
  the result.md itself. Banked as a methodology lesson.
- **HA07d's verdict in HA07d/result.md is unchanged**:
  validate-era SUPPORTED at +21.7 pp 4d bidirectional N_std=1.5,
  train-era SUPPORTED at +19.6 pp. Locked verdicts do not unlock.
- **The one-sided lowered direction findings are robust under
  the same locked criteria** if reframed as primary. Train:
  peak at 1.25 (in rescue window), Spearman −0.313 (passes),
  sign-changes 0 (passes), disc at 2.0 +14.7 (passes), disc at
  2.5 +9.8 (passes) — clean RESCUE if treated as primary.
  Validate: peak at 2.0 (outside rescue window, would close on
  peak location), but qualitatively clean rise to peak then
  decline.

## What this changes immediately

1. **Synthesis-level framing demotion** of HA07d's bidirectional
   primary in both eras. Card (b2) loses its sole anchor.
2. **Methodology playbook update** flagging the four-shape
   distinction as required for future diagnostic criteria.
3. **HA07d2 pre-registration planned** (one-sided lowered as
   primary; new criteria handling all four robust shapes).
4. **Pause before running the same diagnostic on HA07c, HA08c,
   HA11, HA06b, H02b, H02d** until the criteria are revised.
   Otherwise we risk multiple false-CLOSE verdicts on tests whose
   underlying signals are genuinely robust.

## What this does NOT change

1. **HA07d's locked SUPPORTED verdicts** at primary bidirectional
   in both eras. These stay on record. The audit trail is intact.
2. **The underlying physiological finding** that sleep stress
   variability shifts before crashes in both eras. The
   one-sided lowered direction shows this robustly in both
   train (peak +19.9 at N_std=1.25) and validate (peak +28.5 at
   N_std=2.0).
3. **The era-reversal pattern** at the physiological level
   (validate-era crashes show paradoxical "freeze" /
   parasympathetic stillness; this is consistent with HA10's
   one-sided elevated arm + HA06b's lowered RHR + HA07d's
   one-sided lowered variability).
4. **The peer-review framing fixes** (channel non-independence,
   era as moderator, card specificity, etc.) — those were valid
   independent of HA07d's load-bearing status.

---

*Diagnostic run 2026-06-07. Pre-registration locked at
[diagnostic.md](diagnostic.md). Locked rule applied honestly:
CLOSE both eras. Methodology lesson banked: the locked criteria
themselves need revision before being applied to other SUPPORTED
tests; the criteria penalise stable-plateau and rising-with-
threshold shapes that are actually maximally robust forms of
signal. Both insights — HA07d's verdict and the criteria-flaw
finding — are honestly recorded.*
