# Review - PEM vs POTS reframing (methodology MD + separability analysis + note + catalog section J + site card)

**Reviewer mode**: independent peer review by a subagent with NO exposure to the
drafting session. Isolated-context cold read, doc-only knowledge; fresh session,
no shared context with whoever produced these artefacts, per
[CONVENTIONS section 1.2](../CONVENTIONS.md) (drafting-under-authorization
requires a different-session peer review). The reviewer read the five target
artefacts plus the two citation-faithfulness targets cold, applied the 4-layer
checklist in [reviews/README.md](README.md), and re-ran the reproducible analysis.

**Targets reviewed**:
1. `methodology/pem_pots_mechanism_framing.md` (methodology / operationalisation MD)
2. `analyses/descriptive/pem_pots_separability/findings.md` + `run.py` (analysis)
3. `note_2026-07-07_session_consolidation_pem_pots.md` (consolidation note)
4. `wiggers_testable_hypotheses.md` section J "PEM vs POTS" only
5. `analyses/garmin_exploration/cards/pem-and-pots-mechanisms-export.md` (site card)

**Citation-faithfulness-only** (characterisation checked, not re-reviewed):
`recovery_phase_confounder_bound/findings.md` (R30),
`crash_leadup_curves/findings.md` (R1).

**Reproduction**: the separability analysis reproduces **exactly**. Re-run with
`GEVOELSCORE_DATA_PATH=... python .../pem_pots_separability/run.py` returned, to
the digit: n_days=1090; Pearson +0.092 / Spearman +0.060 / phi +0.050; contingency
both 77 / POTS-only 169 / PEM-only 219 / neither 625; per-phase 4a/4b/5 rates
33.3/16.7, 27.0/30.0, 18.7/24.8; felt-state neither 4.483 / POTS-only 4.574 /
PEM-only 4.151 / both 4.026; notes 2 of 246. Every number in the findings.md tables
matches the live run.

---

## 1. What the data shows (empirical claim separated from framing)

Stripped of interpretation, the analysis establishes four descriptive facts on the
Stratum-4 window (2022-09-03 to 2026-06-05, n=1090 days with both markers
computable):

1. Two watch-derived day-markers - a within-day stress-U-dip count z ("POTS proxy")
   and an overnight-stress-mean z ("PEM proxy"), both against the personal
   [d-90, d-30] lagged trimmed baseline - correlate **weakly positively**:
   Pearson +0.092, Spearman +0.060.
2. Cross-tabulated at z>=1.0: 77 days fire both, 169 POTS-only, 219 PEM-only, 625
   neither.
3. Group-mean felt-state (gevoelscore, 1-6): neither 4.48, POTS-only 4.57,
   PEM-only 4.15, both 4.03.
4. Across recovery phases 4b (pre-citalopram) vs 5 (citalopram), POTS-day-rate is
   27.0 percent vs 18.7 percent. Symptom notes carry essentially no
   orthostatic-symptom vocabulary (2 of 246 POTS-signature days have any keyword
   note; the specific orthostatic terms orthostat/hartklop/bloeddruk/flauw/zout/
   electrolyt/bloedvolume have zero hits).

The **framing** layered on top by the producer: "PEM and POTS are separable, not
correlated" / "essentially independent day-markers" (findings section 1, note Part
C, catalog J, card section 2); "POTS-signature days are NOT lower in felt-state,
the PEM marker is" (all five); "the two together mark the lowest felt-state" (findings
section 1/4, note C, card section 4); "the POTS signal recedes into the citalopram
era" (findings section 3, note C, card section 3).

The empirical facts are solid and reproduce. Two of the four framing claims are
where the review pushes.

---

## Layer 1 - Universal reporting (SCRIBE 3-5/14/18/22-24; STROBE 6/12/13)

### L1-1 [MAJOR] "Separable, not correlated" overstates a correlation the same data shows is significantly non-zero

Inherits from STROBE item 12 (report the actual estimate with precision) and the
[reviews/README.md](README.md) verdict spec (separate empirical claim from framing).

The headline "PEM and POTS are **separable, not correlated** ... they are essentially
independent day-markers" (findings section 1), "essentially independent" (card section
2), "largely independent days" (methodology section 5, catalog J), and "share almost
no variance" (findings section 2) all treat r ~ 0.09 as functionally zero. It is not.
At n=1090 the reviewer computed the 95 percent CI on the Pearson r: **[0.033,
0.151] - it excludes zero** - and the Spearman test is significant (p=0.047). The
markers are **weakly but statistically-significantly positively correlated**, not
uncorrelated. This is a small effect (r-squared ~ 0.8 percent of shared variance),
so "separable / largely distinguishable" is defensible; "not correlated" and
"essentially independent" are not - they contradict the producer's own numbers.

Magnitude of concern: this is the load-bearing public-facing headline. "Separable"
is honest; "not correlated" is a claim the data refutes at the conventional
threshold. An outside reviewer reading only the card's "essentially independent"
would be misled about what the analysis found.

**Revision**: replace "separable, not correlated" / "essentially independent"
throughout (findings section 1/2, note Part C item 1, catalog J, card section 2)
with the accurate form, e.g. "weakly correlated (r ~ 0.09, 95 percent CI [0.03,
0.15]) - a small shared component but largely distinguishable days." Report the CI
in findings section 2's table. The two-axis warrant survives the correction (0.8
percent shared variance still supports looking for both), so nothing downstream
breaks; only the word "not" has to go.

### L1-2 [MINOR] No inferential test reported on the felt-state contrasts, though the central claim is a group difference

Inherits from STROBE item 12 (report estimates and their uncertainty). The findings,
note, and card all assert "the PEM marker tracks lower felt-state" and "POTS-only is
not lower." These are group-difference claims stated purely as raw means (4.15 vs
4.48 vs 4.57) with no test, no CI, no effect size - only the prose qualifier "small."
The reviewer supplied the missing tests: PEM-only vs neither is a real difference
(Mann-Whitney p < 0.0001, Cohen d = -0.40, small-to-medium); POTS-only vs neither is
**not** distinguishable (p = 0.19). So the directional claims are actually *correct*
and *supportable* - but the artefacts leave the reader unable to tell that the PEM
gap is robust while the POTS non-gap is a genuine null rather than an underpowered
one. Reporting the tests would strengthen the finding, not weaken it.

**Revision**: add to findings section 4 a one-line inferential row - PEM-only vs
neither (MWU p, Cohen d ~ -0.40); POTS-only vs neither (MWU p ~ 0.19, i.e. a
supported null). Then the "small but real for PEM, null for POTS" reading is earned,
not asserted.

### L1-3 [MINOR] The card's "confidence" line is the only place uncertainty is quantified, and it is qualitative

The card section 6 says "moderate for separability, lower for the felt-state gap."
That is the right instinct but it is the sole uncertainty statement and it is a word,
not a number, on a public-facing artefact. Combined with L1-1 and L1-2, the card
under-quantifies. **Revision**: once L1-1 (CI on r) and L1-2 (test on the PEM gap)
land in the findings, echo the numeric forms into the card's honesty floor.

---

## Layer 2 - Observational n=1 (Daza 2018; Personal Science norms)

### L2-1 [MINOR] Proxy-status is disclosed well; the U-dip-as-POTS-axis validity is the residual risk and is honestly flagged

The methodology MD section 3.1 states the U-dip is a narrow, mechanism-faithful but
single-pattern proxy, weights specificity over coverage explicitly, and names the
absent ideal marker (positional / standing-HR, off-instrument on the FR245). The
findings, note, and card all repeat "proxy, not diagnosis." This is good n=1
discipline - the proxy status travels.

The residual concern the review was asked to push: **is one within-day pattern enough
to carry a "POTS axis"?** The reviewer inspected what a "POTS-signature day" (z>=1.0)
actually is in raw units: it maps almost entirely to raw `u_dip_count` >= 2 (of the
246 signature-days, 130 have exactly 2 U-dips, only 28 have value 1; the marker is a
heavily zero-inflated small-integer count - 45 percent of in-window days are 0,
77 percent are 0 or 1, max is 5). So the entire POTS axis rests on the contrast
between "0-1 U-dips" and ">=2 U-dips" per day. That is a thin substrate for a named
mechanism axis, and the failure modes are real: any within-day artefact that inflates
the U-dip count (device gaps, nap-driven body-battery rises unrelated to blood
volume, motion segmentation) feeds the "POTS" marker directly. The MD does not
enumerate these failure modes.

Severity is MINOR only because the artefacts are honest that this is a proxy and
descriptive; but the "POTS axis" language (catalog J.2 "family," card "its own
thing") is heavier than a 0-vs-2-count discriminator warrants.

**Revision**: in methodology MD section 3.1, add a short failure-modes paragraph
(what non-orthostatic processes inflate `u_dip_count`: nap-driven BB rises, device
gaps, motion segmentation) and state the raw-count mapping (signature day ~ raw count
>= 2). Soften "POTS axis" to "POTS-proxy marker (one orthostatic pattern)" where the
axis language over-reaches, consistent with the MD's own section 6 caveat.

### L2-2 [MINOR] Calendar-time vs subject-time: the phase table's two informative cells are a calendar boundary, disclosed but load-bearing (see L3-1)

Flagged here for the record; the substantive concern is at Layer 3 (era-split
re-entry). Data provenance is otherwise clean - operand paths named, notes source
named, baseline construction named in every artefact's verification log.

---

## Layer 3 - Time-series specific (Natesan 2023 autocorrelation; WWC 2022; CENT 2015)

### L3-1 [MAJOR] The per-phase "POTS recedes into the citalopram era" read re-enters the retired era-split; disclosure varies by artefact and is weakest on the public card

Inherits from CENT 2015 carryover/ordering guidance and the project's single-pool
primacy discipline (the R19 rule cited throughout as "descriptive variation, not a
verdict"). The reviewer confirmed the phase-4b/phase-5 boundary is
**2024-04-08 -> 2024-04-09 - exactly the citalopram onset date** (verified against
the recovery_phase date ranges: 4b spans 2022-11-17..2024-04-08, phase 5 spans
2024-04-09..2026-06-05). The only two informative cells in the per-phase table (4a is
n=6, phase 3 drops out entirely to n=0) straddle that single boundary. So "the POTS
signal recedes into the citalopram era" is, structurally, a **pre-citalopram vs
post-citalopram two-window comparison** - the retired era-split, relabelled as
recovery-phases.

The artefacts vary in how squarely they own this:
- Findings section 3 and methodology section 6 disclose it well: "the 4b -> 5 decline
  coincides with the citalopram-onset boundary and is not independent of the
  medication story," tagged as R19 descriptive-variation-not-a-verdict.
- The note Part C item 2 states "recedes into the citalopram era" as a finding with
  the caveat downstream.
- The **card section 3** states it most baldly - "receding in the recent medicated
  years (about 19 percent)" as a positive narrative beat - and the era-coincidence
  caveat is NOT attached to that sentence; it only appears as the generic
  "descriptive, n=1" floor in section 5. On the public artefact the causal-adjacent
  "receding as it is managed" reading travels without its confound.

Per CONVENTIONS section 4.2 this is the caveat-class-vs-a-priori distinction: stating
"the boundary coincides with citalopram, uncorrected" is caveat-class (KEEP); letting
"recedes into the medicated era, matching that it eases as managed" stand as a
narrative claim lifts the era-split from confounder to analytical basis
(a-priori-class, CUT-or-caveat). The findings/methodology stay on the right side; the
card drifts across.

**Revision**: (a) on the card, attach the confound to the sentence, not the
footer - e.g. "the U-dip rate is lower in the later years, which are also the
medicated years, so this timing is entangled with the citalopram change and is not
evidence the medication reduced it." (b) In the note Part C item 2, add the same
one-clause confound inline rather than trusting the downstream caveat. (c) Consider
whether the per-phase table earns its place at all given both informative cells are
one boundary; a single sentence "the marker is lower post-2024-04, which is also
post-citalopram, entangled" may be more honest than a phase table that implies a
multi-phase trajectory.

### L3-2 [MINOR] Autocorrelation of the day-level markers is not addressed for the correlation or the group means

Inherits from Natesan 2023 (83.8 percent of n-of-1 studies ignore autocorrelation).
The Pearson/Spearman r and the group-mean contrasts treat 1090 days as 1090
independent observations. Overnight-stress and U-dip counts are both day-to-day
autocorrelated (multi-day PEM bouts, managed-vs-unmanaged POTS stretches), so the
effective n is smaller than 1090 and the CI in L1-1 [0.033, 0.151] is optimistic -
the true interval is wider and may graze zero. This does not overturn "weakly
correlated" but it means the significance in L1-1 should be stated cautiously.

Severity MINOR: this is a descriptive Layer-1 artefact that explicitly disclaims
inference, so a formal autocorrelation-corrected test is not required; but because
L1-1 asks the producer to *add* a CI, that CI should carry a one-line note that it
is uncorrected for day-level autocorrelation and therefore a lower bound on the true
width. **Revision**: add that half-sentence wherever the CI is reported.

### L3-3 [BLOCKER-downgraded-to-MAJOR] Crash-drop sensitivity (CONVENTIONS section 3.4) is absent, and running it materially weakens the "both together = lowest felt-state" claim

Inherits from CONVENTIONS section 3.4 (crash-drop sensitivity row on every Layer-4+
correlation touching PEM-pacing variables) and the reviews/README Layer-4 hook. The
findings load `is_crash` in run.py but never use it. The audit hook technically
scopes to "Layer 4+," and this is labelled Layer-1 descriptive, which is why this is
MAJOR not BLOCKER - but the *reason* the hook exists fires hard here, so the
Layer-1 label does not excuse it.

The reviewer ran the sensitivity. Two results:
- On the **correlation**: |delta r| = 0.020 (full 0.092 -> crash-dropped 0.072),
  below the 0.10 flag threshold. Clean. Good news for the separability headline.
- On the **felt-state group means**: the "both" group has a **24.7 percent crash
  rate** (19 of 77 days) vs 4.3 percent for neither. With crash days dropped, the
  "both" group mean **jumps from 4.03 to 4.52** - essentially equal to neither
  (4.55). The "the two together mark the lowest felt-state (4.03)" claim (findings
  section 1/4, note C item 3, card section 4 "the worst days are when both fire
  together") is **substantially a crash-circularity artefact**: `is_crash` is defined
  partly on a low-gevoelscore drop, the "both" cell is crash-enriched sixfold, so
  "both = lowest felt-state" is partly "both = where the crashes are, and crashes are
  low-felt-state by construction." The PEM-only gap is more robust - it survives
  crash-drop (4.39 vs 4.55) and the MWU is highly significant even so - but the
  "both together = worst" beat does not survive.

Magnitude of concern: this is the second load-bearing felt-state claim and it is on
the public card. It is not wrong that "both" days have the lowest raw mean; it is
misleading to present that as a felt-state signal of the co-occurring mechanisms when
it is largely the crash definition folding back on itself.

**Revision**: (a) add the crash-drop sensitivity row to findings section 4 (both
the correlation delta and the group means with `is_crash==True` dropped) - the
correlation delta is a clean pass worth showing, the group-mean shift is the finding.
(b) Reframe the "both together = lowest" claim: state that the "both" cell is
crash-enriched (24.7 percent) and that its low mean is largely the crash definition;
with crashes removed "both" is indistinguishable from neither. (c) On the card, drop
or heavily qualify "the worst days are when both fire together." (d) Keep the PEM-only
finding as the robust one - it is the claim that survives.

---

## Layer 4 - Project-specific audit hooks (CONVENTIONS section 3)

### L4-1 [MAJOR] section 3.4 crash-drop hook - FIRED (see L3-3)

The single most consequential audit-hook miss. Detailed under L3-3.

### L4-2 [MINOR] section 3.1 personal-baseline - PASSES with non-trivial evidence

The markers use z vs the personal [d-90, d-30] trimmed (10/90) lagged baseline with
sigma-floors and a 40-prior-day minimum. This is exactly the section 3.1 /
section 3.2 `_lagged` discipline (baseline does the personalisation, threshold z>=1.0
is fixed). The lagged (not trailing-inclusive) window is the correct choice per
section 3.2. Verified in run.py `lagged_z`. Clean pass - noted per the reviews/README
"selective what-does-not-fire" instruction.

### L4-3 [MINOR] section 3.5 spike-metrics - PASSES; the U-dip count is a count-metric not a daily mean, and stress_mean_sleep is the validated proxy

The POTS marker is a within-day event *count*, aligned with section 3.5's preference
for count/peak over daily-mean for autonomic proxies. Good. One asymmetry worth a
note: the PEM marker *is* a daily mean (`stress_mean_sleep`), which section 3.5
generally disprefers - but here it is defensible because the overnight window already
localises it and it is the project's validated HRV proxy (`hrv_proxy_via_stress.md`).
The MD section 3.2 could state that the mean-vs-spike asymmetry between the two
markers is deliberate (load axis vs event axis) - it half-does. MINOR.

### L4-4 [MINOR] section 3.6 named counts - MOSTLY PASSES, one loose count

The findings name counts well in most places (n=1090 both-computable, the 77/169/
219/625 contingency, 2 of 246 notes). Section 5's "only 32 clauses carry any
POTS-adjacent keyword" is the one count without a fully-named scheme/unit/source in
the same sentence - it names the source file in section 7 but the section-5 sentence
itself does not carry unit (clause-level) + predicate. The reviewer verified 32 is the
deduplicated OR-union clause count (raw per-keyword hits sum to 48; the union is 32),
and that essentially all "staan"/"opstaan" hits are non-orthostatic ("opstaan" =
getting up, "stilstaan"), so the null is real. **Revision**: in section 5, name it as
"32 clauses (v24 clause-level, notes-categorized-v24-clauses.csv, OR-union of the
POTS-keyword list)."

### L4-5 [NIT] section 4.1 no-interpretive-marks - PASSES on descriptive layers; watch the card's mechanism language

The findings and methodology keep causal marks off the descriptive layer ("association
at n=1, not mechanism," "no causal marks"). The card section 6's offered site copy
("your circulation struggling with standing and blood volume ... eases when it's
managed with salt and electrolytes") is mechanism-framed - acceptable because it is
explicitly labelled "site-consumable shape (offered, not prescribed)" and Wiggers-
attributed, not a claim about this body's data. Keep the label; do not let that copy
migrate into the findings or note as a data claim. NIT.

---

## Citation-faithfulness check (note + card characterisation of R30, R1, HA11)

- **R30 ("confounder-dominated")**: the note Part A and methodology cite R30's
  RHR-rise-is-confounder-dominated finding. Read against `recovery_phase_confounder_bound/findings.md`,
  the characterisation is faithful - R30's headline is exactly "the per-phase
  resting-HR rise is confounder-dominated; the illness-attributable residual level is
  flat." The MD's use of R30 to reject `resting_hr` as a POTS marker (section 3.4
  alternatives) is a fair application. PASS.
- **R1 ("departure at onset")**: the note Part A cites R1's "the departure is at
  onset (t0), not before." Faithful to `crash_leadup_curves/findings.md` headline.
  PASS. (R1 is not load-bearing for the PEM/POTS claim; cited only in the batch
  table.)
- **HA11 ("U-dip crash-discrimination SUPPORTED early era, recedes later")**: cited
  in findings section 3, methodology section 3.1, catalog J.2/O3, card section 3 as
  the substrate for the U-dip marker and as corroborating the time-varying read. The
  reviewer did not re-open HA11 (out of scope), so this citation is **NOT
  independently verified**; flagged below.

---

## What could NOT be verified

- **HA11's actual verdict and its "SUPPORTED early / recedes later" shape** - relied
  on as corroboration for the time-varying claim (L3-1) but not re-opened by this
  reviewer. If HA11's "recedes later" is itself the same pre/post-citalopram era-split,
  then findings section 3's "this matches HA11" is two disclosures of the same
  confound presented as mutual corroboration, which would strengthen L3-1. Recommend
  the producer confirm HA11's era-handling before leaning on it as independent support.
- **The Wiggers guide quotes** (`wiggers_pacing_handleiding.txt`) - the verbatim
  U-dip / orthostatic passages are quoted in the MD and catalog J; the reviewer did
  not have the guide text and cannot confirm the quotes are verbatim or in-context.
  The catalog itself flags a line-number mapping caveat (clean vs archived
  two-column extraction), which is the right disclosure.
- **`hrv_proxy_via_stress.md`** validity of the stress-as-HRV-proxy - asserted as
  already-validated; not re-reviewed here.
- **Autocorrelation-corrected** version of the correlation CI - the reviewer computed
  only the naive Fisher-z CI (L1-1); an effective-n or block-bootstrap CI was not
  computed (L3-2 asks the producer to caveat, not to compute).

---

## What would strengthen these findings (constructive)

1. **The `is_crash` column is already loaded in run.py** - adding the section-3.4
   crash-drop sensitivity is ~6 lines and turns L3-3/L4-1 from a miss into a
   documented pass-plus-finding. The correlation delta (0.020, clean) is good news to
   show; the group-mean shift is the honest caveat the felt-state claim needs.
2. **The Fisher-z CI on r is a one-liner** (`np.arctanh` +/- 1.96/sqrt(n-3)) - reporting
   [0.033, 0.151] with the "uncorrected for autocorrelation, lower bound on width"
   note fixes L1-1 and L3-2 together and makes "weakly correlated, largely
   distinguishable" a defensible published phrasing.
3. **The MWU + Cohen-d on the PEM-only vs neither contrast** (p<0.0001, d=-0.40) and
   the POTS-only null (p=0.19) are already computable from the same frame - adding
   them (L1-2) converts the asserted "small but directional" into an earned "robust
   for PEM, supported null for POTS."
4. **The raw-count mapping of the POTS signature** (signature day ~ `u_dip_count`>=2)
   belongs in the MD section 3.1 - it is the most honest single statement of what the
   "POTS axis" rests on, and it pre-empts the "one within-day pattern carrying a whole
   axis" objection by owning it.

---

## Verdict

**MAJOR-REVISIONS-NEEDED.**

Reasoning: the underlying analysis is reproducible to the digit, the operationalisation
is transparently reasoned from the section-2.2 four inputs, and the proxy/descriptive/
n=1 caveats are present and mostly travel - this is careful work. But three
load-bearing, public-facing claims do not survive independent scrutiny as currently
worded. (1) "Not correlated / essentially independent" (L1-1, MAJOR) is contradicted
by the producer's own r whose 95 percent CI excludes zero; the correct claim is
"weakly correlated, largely distinguishable." (2) The section-3.4 crash-drop
sensitivity is absent (L3-3 / L4-1, MAJOR), and running it shows the "both mechanisms
together = lowest felt-state" beat is substantially a crash-definition circularity -
it collapses when crash days are removed. (3) The "POTS recedes into the citalopram
era" timing read re-enters the retired era-split at a single calendar boundary
(L3-1, MAJOR), disclosed adequately in the findings/methodology but not on the public
card, where it reads as an unconfounded narrative beat.

None of these overturns the project's genuine result - PEM and POTS proxies ARE
largely distinguishable days, and the PEM marker IS the one that robustly tracks lower
felt-state while the POTS marker is a supported null. That core survives every check
the reviewer ran and is worth publishing. The revisions are about not overstating it:
change "not correlated" to "weakly correlated," add the crash-drop sensitivity and
reframe "both = worst," and attach the citalopram confound to the timing sentence on
the card. Because the concerns land on the highest-priority public claims (Layers 1
and 3) rather than on presentation nits, the verdict is MAJOR-REVISIONS-NEEDED, not
ACCEPT-WITH-MINOR-REVISIONS. Re-review after revision can likely reach ACCEPT quickly:
the fixes are small, the data supports the corrected claims, and the producer already
has the `is_crash` column loaded.

---

*End of review.*
