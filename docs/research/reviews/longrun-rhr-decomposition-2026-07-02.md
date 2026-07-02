# Peer review: multi-year RHR trajectory + confounder decomposition

**Target**: [`../analyses/longrun_rhr_trend/findings.md`](../analyses/longrun_rhr_trend/findings.md)
(+ [`../analyses/longrun_rhr_trend/decomposition.py`](../analyses/longrun_rhr_trend/decomposition.py)).
**Design under review**: [`../analyses/longrun_rhr_trend/driver_ledger.md`](../analyses/longrun_rhr_trend/driver_ledger.md).
**Priors**: [`../literature/reviews/deconditioning_vs_disease_longrun_rhr_review.md`](../literature/reviews/deconditioning_vs_disease_longrun_rhr_review.md).
**Checklist anchor**: CONVENTIONS section 3.1 (robust stats), 3.6 (named counts),
4.1 (no causal marks on descriptive layer), plus the reviews/ 4-layer checklist.

**Reviewer mode**: fresh session, no exposure to the drafting context; doc-only
knowledge. Reproduction run locally against
`per_day_master.csv` and `97794221_userBioMetrics.json` on 2026-07-02.

The claim under scrutiny is CONVENIENT: it rebuts the researcher's own
deconditioning-dominant hypothesis and strengthens the wearable-factor
LC-tracking story. Convenient results were given the harshest scrutiny.

---

## Overall verdict

**MAJOR-REVISIONS.**

The analysis is numerically reproducible to the digit, the discipline hygiene is
good, and the central *direction* survives adversarial stress-testing better than
expected. But two load-bearing quantitative claims are overstated: the headline
confidence interval **[1.05, 1.37]** is an analytic Theil-Sen interval on a series
with lag-1 autocorrelation of **0.94** and is far too tight (the honest
block-bootstrap interval is roughly **[0.6, 1.9]**), and the aggregate is
**not robust to dropping 2024** (leave-2024-out collapses the slope to
**0.13 [-0.14, 0.44]**, CI crossing zero). The doc also under-discloses that the
post-2023 weight series is entirely interpolated/extrapolated across a 523-day
gap, and the residual is materially sensitive to the weight coefficient. These
are fixable with honest CI reporting, a wobble/LOYO caveat, and a weight-fragility
caveat; the qualitative conclusion can survive if downgraded and re-conditioned.

**CIRCULARITY: present-but-honestly-conditioned** (the flat-by-year-1 assumption is
made explicit in B3, B6, ledger section 5, and is licensed by the literature review's
actual verdict; and, decisively, the residual verdict does NOT actually depend on it,
see finding 1).

**Central conclusion ("deconditioning does not dominate the long-run drift"):
SUPPORTED-WITH-CAVEATS.** The direction survives; the *magnitude and precision* as
stated (+1.21 bpm/yr [1.05, 1.37], "CI excludes zero", "fully robust") are
overclaimed and must be softened.

**Counts: 2 BLOCKING-adjacent MAJOR, 3 MAJOR, 4 MINOR, 3 NIT.** (No true BLOCKING:
nothing is fabricated or non-reproducible; the fixes are disclosure/precision, not
retraction.)

---

## Findings (keyed to the 7 checks)

### 1. Circularity (the big one): MAJOR (but the conclusion survives it)

**Verdict: present-but-honestly-conditioned, and NOT load-bearing.**

The circularity is real in structure: the conclusion "post-2023 rise is not
deconditioning" is *stated* as resting on both model curves being flat after
year 1 by construction (B3: "because both decond curves are flat after ~year 1
by construction, the deconditioning term cannot explain any RHR movement after
year 1 whatever its amplitude"). Read alone, that is assuming the answer to the
exact question the researcher originally hypothesised the other way (deconditioning
*continues* for years).

Three things rescue it from "overclaimed":

(a) **It is made explicit.** B3, B6, ledger section 3 and section 5, and the
findings' honesty block all state the flat-by-year-1 assumption openly and
condition on it. This is caveat-class disclosure, not hidden framing (CONVENTIONS
4.2). The falsification framing in B5 is written as a conditional.

(b) **The literature prior licenses it.** I read the deconditioning review's actual
verdict. Section 1 verdict: RHR determinants reverse "weeks-to-months, not years...
reaches a new near-untrained equilibrium within roughly the first year." Section 6.2:
"By year 4 it should have plateaued and be essentially flat. Therefore, if the
project's RHR series is still rising at year 4, that late component is NOT
well-explained by deconditioning." The review is careful that this is *inferred, not
measured* (its section 7: "the multi-year human RHR time-course is INFERRED, not
directly measured... treat the plateau timing as a well-grounded expectation, not a
calibrated constant"). So the flat-by-year-1 shape is a defensible external prior, and
the review does not adopt the deconditioning-flattering side. The prior is strong
enough to license conditioning on it, and the doc conditions on it rather than
asserting it as fact.

(c) **Decisively: the residual verdict does not actually depend on the flat
assumption.** I re-ran the fit substituting slow-continuing deconditioning shapes
that the researcher's original hypothesis would favour (exp with tau = 1, 2, 4, 8 yr;
i.e. curves still rising at year 4). In every case the robust fit still drives
decond_amp to ~0-1.1 bpm and the post-2023 residual slope stays **1.21**. Only an
explicitly *linear, never-plateauing* ramp (amp fit to 5.86 bpm, a physiologically
unjustified 3.36 bpm rise across 2024-2026) moves the residual at all, and only from
**1.21 to 1.08**. So even handing deconditioning a shape designed to absorb the
late rise, it absorbs almost none of it, because weight and age (both monotone-rising,
mutually correlated 0.96) are already competing for that trend and the optimizer
prefers them. The conclusion is therefore robust to the assumption it appears to
depend on.

**Fix**: keep the honest conditioning, but ADD the (c) result. Right now the doc
argues the conclusion "survives regardless of amplitude *because the curve is flat*"
(B3), a purely by-construction argument that reads as circular. Replace/augment it
with the empirical demonstration that *even a non-flat, still-rising deconditioning
curve cannot absorb the post-2023 residual*. That converts a "we assumed it away"
argument into a "we tried to let it explain the rise and it could not" argument,
which is exactly what defeats the circularity charge. This is the single most
valuable revision.

### 2. decond_amp = 0 collapse: MINOR (interpretation is correct)

The doc interprets the amp=0 collapse as collinearity / non-identifiability
against the intercept and plateau level (B3, ledger section 5), explicitly NOT as
"deconditioning didn't happen" or "has no RHR effect". I confirmed the mechanism:
the flat literature curve (tau=4mo) is ~constant post-cessation (mean 0.922, std
0.183 over post-cess days), so it is near-collinear with the intercept; and any
residual monotone slope is claimed by weight and age (corr(weight,age)=0.958). The
interpretation is correct and appropriately non-overclaimed. The Garmin curve's
wider amp CI (up to 6.27 bpm) is reported honestly.

**NIT within**: B1 shows decond_amp CI `[0.00, 0.28]` for tau=3 but `[0.00, 0.00]`
for tau=4/6; the representative-fit table uses tau=4. Fine, but a one-line note that
the amp CI is non-degenerate only for the shortest tau would be tidy.

**Fix**: none required; optionally add the collinearity-mechanism numbers
(constant-ness + weight/age correlation) to B3 for the reader.

### 3. Year-wobble in the residual + CI credibility: MAJOR

This is the most serious quantitative problem. Two parts:

(a) **The CI [1.05, 1.37] is too tight and is mislabelled as bootstrap.** The
post-2023 residual has lag-1 autocorrelation **0.94**, not decorrelating even by
lag 20. The reported CI comes from `theilslopes(..., alpha=0.95)` in
`summarise_residual`, an *analytic* Theil-Sen interval that assumes near-independence.
The block bootstrap the doc advertises (2000 resamples, block=10d) is applied only to
the regression *betas* in `block_bootstrap_betas`; **the residual slope's CI is never
block-bootstrapped**. When I block-bootstrap the residual slope properly:
block=10d gives **[0.79, 1.60]**, block=20d **[0.69, 1.63]**, block=30d **[0.64, 1.73]**,
block=45d **[0.56, 1.89]**. So the honest interval is about **[0.6, 1.9]**, still
excludes zero at block=10-20, but the claimed **[1.05, 1.37]** overstates precision by
roughly 3x in width. The narrative "The confidence interval excludes zero" is
defensible at short block lengths but the *stated interval* is not the one that handles
the autocorrelation the doc itself says block-bootstrap is there to handle.

(b) **The aggregate is carried by 2024 (and 2026), with 2025 negative.** Reproduced
year slopes: 2024 +1.06, 2025 -1.05, 2026 +1.14. Leave-one-year-out: **dropping 2024
collapses the post-2023 slope to 0.13 [-0.14, 0.44] (CI crosses zero)**; dropping 2025
leaves 1.22; dropping 2026 leaves 1.31. So the "+1.21, CI excludes zero" verdict is
not robust to the single most influential year. This must be surfaced, not buried.

**Fix**:
- Report the block-bootstrap residual-slope CI (roughly [0.6, 1.9] at block=10-20d) as
  the headline interval, and stop presenting [1.05, 1.37] as if it were the
  autocorrelation-aware interval. Either bootstrap the residual slope in
  `summarise_residual`, or relabel [1.05, 1.37] explicitly as "analytic Theil-Sen CI,
  not autocorrelation-corrected" and add the wider bootstrap CI beside it.
- Add the leave-one-year-out table and state plainly that the aggregate is driven by
  2024 and 2026 and that dropping 2024 removes significance. Frame the verdict as "the
  residual rises across most of the post-2023 window but the aggregate slope is
  2024/2026-driven and is not robust to removing 2024," which is the honest reading of
  the wobble.

### 4. Aging attribution: MINOR (direction of the caveat is correct)

The doc claims capping aging at 0.5 bpm/yr is conservative for the residual verdict
("the residual verdict is if anything conservative", B1/section-limits). I confirmed
the direction: with aging removed at the 0.5 cap the residual slope is 1.21; with
aging=0 it is **1.71**; with aging at the literature-typical 0.3 it is **1.41**. So a
higher aging cap soaks MORE trend and *shrinks* the residual; capping high is indeed
conservative *for the "residual still moves" conclusion*. That claim is honest.

Two caveats the doc should keep sharp:
- Labeling the residual "LC/aging" is honest (the doc repeatedly says LC and aging
  cannot be separated within the residual). Keep that; do not let downstream synthesis
  quietly drop "aging" and call it "LC".
- On magnitude: a residual of ~1.2 bpm/yr sitting *on top of* an already-capped
  0.5 bpm/yr aging term implies a total unattributed-to-nuisance drift of ~1.7 bpm/yr,
  which is far above any plausible adult aging rate (~0.1-0.3 bpm/yr per the doc's own
  prior). So the residual is more plausibly LC than aging in magnitude, but the doc
  correctly does NOT make that a hard claim, and should not start to. The current
  wording ("a real LC/aging component") is right.

**Fix**: none required; optionally state the arithmetic (0.5 cap + ~1.2 residual =
~1.7 bpm/yr unattributed, vs ~0.1-0.3 aging prior) to make explicit why aging alone
cannot carry the residual.

### 5. Plateau claim (Part A): MAJOR

"Not plateauing" is the second headline and it is more window-sensitive than the doc
admits. Reproduced and stress-tested raw Theil-Sen windows:
early 2022-2023 **1.31**, recent 2025-2026 **1.61**, 2024-2026 **2.30**, last-12mo
**4.77**, last-18mo **1.76**, but **mid 2023-2024 gives 0.00 [-0.85, 0.00]**, a flat
window sits inside the record. The plateau-refutation rests entirely on the comparison
of two hand-chosen multi-year windows (early-LC vs recent), and the within-year
Theil-Sen slopes are degenerate 0.00 from integer ties (the doc discloses this in A2,
good). The *direction* (recent not below early, so not front-loaded) holds across the
honestly-chosen windows, but the estimator is fragile: integer-tie degeneracy makes
single-year and some multi-month windows collapse to 0.00, and window choice swings the
slope from 0.00 to 4.77.

**Fix**: (a) state that the non-plateau conclusion rests on a two-window comparison and
report at least one alternative windowing (e.g. 2023-2024 flat vs 2024-2026 steep) so
the reader sees the sensitivity; (b) since RHR is integer-tied, consider reporting the
28-day-rolling-median trajectory slope (which the doc already computes for A1) as the
plateau discriminator instead of raw-daily Theil-Sen, to sidestep the tie degeneracy.
The conclusion likely survives but the current presentation understates window-dependence.

### 6. Reproduction of the headline numbers: PASS

Ran `decomposition.py` (seed 20260702) and an independent recompute. All headline
numbers reproduce:

| quantity | claimed | reproduced | source |
|---|---|---|---|
| RHR coverage | 1731 non-null days | **1731** | script + independent |
| RHR span | 2021-08-16 to 2026-06-05 | overall master span reproduces; **non-null RHR max is 2026-05-29** | see NIT below |
| raw weigh-ins | 56 raw / 54 distinct | **56 / 54** | independent |
| citalopram | 788 traject / 787 dose>0 / first 2024-04-10 | **788 / 787 / 2024-04-10**, max dose 30 mg | independent |
| VO2Max | 302 raw / 244 distinct, peak 53 floor 37 | **302 / 244 / 53 / 37** | independent |
| b_weight | 0.322 bpm/kg | **0.322** | script |
| b_dose (citalopram) | -0.038 bpm/mg (-1.14 at 30mg) | **-0.0381 / -1.14** | script |
| b_age | 0.500 (at cap) | **0.500 pinned** | script |
| seasonal amp | ~1.07 bpm | **sqrt(0.811^2+0.698^2)=1.07** | script |
| post-2023 residual slope | +1.21 [1.05, 1.37] | **+1.21 [1.05, 1.37]** point reproduces; CI too tight (finding 3) | script + independent |
| robustness across 4 curves | identical 1.21 | **identical** | script |

**Reproduction verdict: PASS on every reported number.** The point estimates are
exactly as stated; the only reproduction-level discrepancy is the CI's statistical
basis (finding 3), not its printed value.

### 7. Discipline: PASS with NITs

- **Part A causal-mark-free (CONVENTIONS 4.1)**: yes. A1-A4 are descriptive; A3's
  plain-language "the opposite of the deconditioning shape" is a shape statement with
  the explicit parenthetical "(Descriptive statement of shape only; attribution is
  Part B)". Acceptable, though it leans close to the line, see NIT.
- **Limits stated honestly**: yes, and thoroughly. The honesty/limits block is strong:
  fitness decline modelled-not-measured, slow-driver collinearity, static-level
  non-attributability, aging-cap, citalopram lower-bound, n=1. Good.
- **PII**: findings.md is clean (no name, no email, no Garmin id). `decomposition.py`
  contains the Garmin account id `97794221` in the data path (NIT below).
- **em-dashes / emoji**: findings.md and decomposition.py have zero em-dashes and zero
  emoji. `driver_ledger.md` has 3 em-dashes (NIT; it is the cross-referenced design
  artefact, not the artefact under review, and the no-em-dash rule is a UI-copy rule).
- **stress = GSS guardrail**: present and prominent in findings.md (top callout + A4 +
  limits), decomposition.py (module docstring), and driver_ledger.md. Good.

**NITs**:
- (7a) findings.md A1 attaches "span 2021-08-16 to 2026-06-05" to the "1731 non-null
  resting_hr days" sentence, but 2026-06-05 is the overall master-calendar max; the last
  non-null RHR is **2026-05-29** (the final 7 calendar rows are RHR-null). Reword so the
  span describes the calendar and the 1731 describes the non-null count, to avoid implying
  RHR is present through 2026-06-05.
- (7b) `decomposition.py` embeds the Garmin account id `97794221` in the BIO path. It is a
  script data path (not user-facing copy) and audit_for_publication.py presumably
  allowlists it, but flagging per the PII sweep; confirm it is on the allowlist before push.
- (7c) driver_ledger.md's 3 em-dashes: cosmetic, ledger only.

---

## Additional finding not in the 7 checks: MAJOR

**Post-2023 weight is entirely interpolated/extrapolated, and the residual is
materially sensitive to it.** The weigh-in series has its largest gap **523 days**
(2023-09-12 last real weigh-in at 81.5 kg to 2025-02-16), and the 2026 value (89 kg)
is participant-reported, not in the dump. So across the *entire* post-2023 leverage
window the weight regressor is a straight-line interpolation between one 2023 weigh-in
and one self-reported 2026 anchor. That interpolated rise removes **2.20 bpm** over
2024-2026 at b_weight=0.322. The residual slope is highly sensitive to this: doubling
b_weight to 0.64 collapses the residual slope from 1.21 to **0.29 [0.13, 0.45]**. The
doc discloses the 14-month 2022-2023 gap prominently but is much quieter about the
523-day 2023-2025 gap that sits directly under the post-2023 residual it is
interpreting. Because weight and the residual trade off almost one-for-one in this
window, and weight there is essentially unmeasured, the post-2023 residual magnitude
inherits the uncertainty of an interpolated weight curve.

**Fix**: surface the 2023-09 to 2025-02 (523-day) weigh-in gap in the limits block with
equal prominence to the 2022-2023 gap, state that the post-2023 weight term is
interpolated/extrapolated (not measured) across the exact leverage window, and add the
b_weight sensitivity (residual slope 0.29 at b_weight=0.64) so the reader sees the
residual is conditional on the weight coefficient being near 0.322.

---

## What would make this ACCEPT

1. Report the block-bootstrap residual-slope CI (~[0.6, 1.9]) as headline; stop
   presenting the analytic [1.05, 1.37] as autocorrelation-aware (finding 3a).
2. Add the leave-one-year-out result and reframe the verdict as 2024/2026-driven and
   not robust to dropping 2024 (finding 3b).
3. Add the empirical circularity-defeater: a still-rising deconditioning curve still
   cannot absorb the residual (finding 1c). This is the strongest available rebuttal to
   the circularity charge and it is currently missing.
4. Disclose the 523-day post-2023 weigh-in gap and the b_weight sensitivity (additional
   finding).
5. Add plateau window-sensitivity (finding 5) and fix the two NITs (7a, 7b).

With these, the honest claim becomes: "After modelling nuisance drivers, RHR residual
rises across most of 2024-2026 at a point estimate near +1.2 bpm/yr (block-bootstrap CI
roughly [0.6, 1.9]); the aggregate is driven by 2024 and 2026 and is not robust to
dropping 2024; the rise is not absorbed even by a deliberately slow-continuing
deconditioning curve; conditional on the interpolated post-2023 weight term, this is
consistent with a residual LC/aging component and inconsistent with deconditioning-dominant
drift." That version is SUPPORTED. The current version overstates precision, robustness,
and the by-construction leg of the circularity argument.

---

## Authorship

Claude (Opus 4.8) fresh-session reviewer, for the participant-researcher (repo owner).
Reproduction run 2026-07-02 against `per_day_master.csv` and
`97794221_userBioMetrics.json`. Fresh session, no exposure to the drafting context;
doc-only knowledge. This review does not edit the findings; it recommends and leaves the
decision to the researcher.
