# Cold review: site card "autonomic fingerprints of load" (R4)

**Under review**:
`docs/research/analyses/garmin_exploration/cards/autonomic-fingerprints-of-load-export.md`
- a Layer-3 "beyond-the-guide" site-facing card for site request R4, framed as a
refinement of a Wiggers (guide) mental-PEM concession.

**Reviewer mode**: independent cold review (reviewer did not write the artifact
under review; fresh-session peer review against the underlying analyses and the
reproducible scripts).

**Date**: 2026-07-06.

**For**: the participant-researcher (repo owner).

**Sources checked against**:
- `docs/research/analyses/descriptive/trigger_types_r4/precondition.md` (section 5
  concordance, section 5.4 the Wiggers timing test)
- `docs/research/analyses/descriptive/trigger_types_r4/analysis.md` (the separate
  crash-specificity / trigger read)
- `docs/research/analyses/descriptive/trigger_types_r4/crash_phenotypes_exploratory.md`
  (the two-phenotype extension)
- Scripts re-run for spot-check: `precondition_analysis.py`, `crash_phenotypes.py`
  (numbers reproduced live). `crash_specificity_analysis.py` cross-read from
  `analysis.md`.
- Wiggers anchor: `docs/research/wiggers_testable_hypotheses.md`, mental-PEM
  concession, PDF lines 1448-1457.

---

## VERDICT

**ACCEPT-WITH-MINOR-REVISIONS** - the card is faithful, honestly limited, and
non-overclaiming on all load-bearing points; the only items are NITs/one MINOR
wording clean-up. It is safe to hand to the website team after the noted small
revisions (or as-is if the team is told the MINOR is a wording nicety, not a
factual defect).

Severity counts: BLOCKING 0, MAJOR 0, MINOR 1, NIT 4.

---

## Findings by severity

### BLOCKING

None.

### MAJOR

None.

### MINOR

**M1. Section 2(c) / 2 "Net" phrasing: "the guide-predicted HRV drop appears ...
overnight stress is suggestive that night and significant the following night."**
This is faithful to the numbers (sleep-stress lag+0 = +0.27, CI [-0.05,+0.60], ns;
lag+1 = +0.53, CI [+0.16,+0.93], `*`; reproduced live). But the card phrases the
overnight aftermath primarily through the sleep-stress channel, whose *that-night*
reading is only suggestive, while the robust both-nights channel (battery floor
-0.42`*` / -0.42`*`) is the stronger evidence and is stated more quietly. The
science is not wrong, but a lay site reader could infer the HRV-proxy drop is
itself significant on both nights. Fix: in 2(c) make explicit that the *robust*
overnight signal is the body-battery floor (both nights), and the sleep-stress
HRV-proxy is suggestive that night and reaches significance only the following
night. The JSON `overnight_hrv: "drop, peaking the following night"` is fine; this
is only about the prose emphasis. Non-blocking because the honesty flags and
section 5.4 wording elsewhere already carry the distinction and the "*" vs "ns"
split is preserved.

### NIT

**N1. Emotional-isolated cell size.** Section 3 honesty flag says "emotional-
isolated cells ~70 days." The precondition caveat states "emo-isolated concordance
n=71" (and emo-only 32). The "~70" is a fair, deliberately-rounded floor; flagged
only for completeness. No change required.

**N2. Physical fingerprint list omits resting HR.** Section 2(a) prose and the JSON
`seen_in` for physical list cardiac strain, activity, and battery floor, but the
source also has `resting_hr` -0.20`*` surviving adjustment for physical. Dropping it
understates (does not overstate) the physical signal, and physical is explicitly the
"least novel / partly circular" channel, so this is a harmless simplification. No
change required; noted so a later editor does not "correct" the card into an
overclaim by re-adding it without the circularity caveat.

**N3. "both survive felt-state adjustment" (emotional, 2c).** Verified: daytime GSS
adj +0.347`*`, battery floor adj -0.428`*`. Correct. Passes cleanly.

**N4. Two-phenotype section header depth/duration.** The card omits the source's
"depth and duration are similar across groups (both are equally real crashes)"
point. Including one clause would slightly strengthen the honesty (it forestalls a
reader assuming emotional crashes are milder). Optional.

---

## Check-by-check results (adversarial pass)

**1. Faithful representation - PASS.** Every number and direction in the card is
reproduced in the sources and in a live re-run of the scripts:
- Physical: max_hr +0.06`*`, eff_exertion +0.05`*` (both survive adj); bb_lowest
  adj -0.208`*`; sleep_stress raw -0.34`*` collapses to adj -0.16 ns (the card
  correctly does NOT claim a robust physical sleep-stress effect). Card's "peak
  cardiac strain and activity volume rise modestly (both CIs exclude 0), plus the
  overnight body-battery floor drops" - accurate.
- Cognitive: every channel ns, isolated, on both same-day and both overnight lags,
  including severe L3 (point estimates if anything slightly negative / wrong
  direction). Card's "moves no channel ... not overnight HRV on either the same
  night or the following night, even at severe intensity" - accurate.
- Emotional: HR flat +0.02 ns; daytime GSS +0.35`*` (adj); battery floor -0.43`*`
  (adj -0.428`*`); sleep-stress that-night +0.27 ns, following-night +0.53`*`. Card's
  "flat in heart rate ... robustly raises daytime stress and lowers the overnight
  body-battery floor ... suggestive that night and significant the following night"
  - accurate.
- The `*` (CI excludes 0) vs `ns` distinctions are preserved correctly throughout,
  including the load-bearing one that emotional sleep-stress is ns that night and
  only significant the next night.

**2. Honest limits intact - PASS.** The card carries, without softening: n=1;
self-report (notes + calendar); non-circular for emotional/cognitive but partly
circular for physical (section 3 bullet 3, plus 2(a) framed as "least novel");
the good-day confound (section 2 preamble names it and says the isolated read is
the honest one); the concordance-is-robust-but-the-trigger-is-only-suggestive
distinction (section 3 bullet 2, explicit and strong); wide autocorrelation-
unmodelled bootstrap CIs; small isolated cells (~70). The two-phenotype "5 of 29
labelled, 24 unclear" honest floor is present verbatim, and the card even elevates
it: "the unclear majority is the headline, not a footnote." Nothing dropped.

**3. No overclaim - PASS.** The headline "the watch sees your emotional load, just
not in your heart rate; it does not see your cognitive load at all" is supported by
the data (emotional robust in GSS + battery floor across adjustment; cognitive ns
everywhere) and is appropriately hedged by the confidence field ("newer / less-
settled; n=1; descriptive") and by section 3. The two-phenotype section is clearly
flagged "newer / less-settled," is presented as a "tendency" not a classifier, and
explicitly instructs the site to say "crashes seem to come in a quiet type and a
loud type," never "we can tell you what triggered your crash." Critically, the
emotional-TRIGGER (crash-prediction) claim is kept OUT of the robust section: section
3 bullet 2 quarantines it as suggestive-not-established, era-confined
(citalopram-era), multiplicity-failing, and "must not be presented here as
'emotional load predicts your crashes.'" This matches `analysis.md` (perm-p 0.028
uncorrected, fails 0.017 corrected bar, entirely in the citalopram phase). Correct
and conservative.

**4. Wiggers anchor accuracy - PASS.** The concession is quoted verbatim against
`wiggers_testable_hypotheses.md` (PDF lines 1448-1457): "Too much mental activity,
such as working on your laptop or writing, often goes undetected in your Garmin,
but excessive mental activity can still cause PEM. It will also cause your HRV to
drop that night or the following night. So, be aware that your Garmin can't warn
you about everything." The card's two-part reading (undetected in the activity
view; autonomic aftermath as an HRV drop that night or the next) is a fair reading
of her actual claim. The framing "confirms her mechanism for emotional load,
refines/refutes it for cognitive" is correct: her claim is about "mental activity"
(her example is laptop/writing = cognitive), and the data confirms the overnight-
HRV-drop mechanism for emotional load on her exact "that night or the following
night" timing while refuting it for cognitive load (her own example) - a genuine
refinement of a taxonomy she lumps as "mental activity." The card does not
misattribute confirmation to the cognitive channel.

**5. Privacy - PASS.** The card ships only aggregated / derived personal-baseline
effect sizes (rank deltas, z-score deltas, CIs) and de-identified content tags. No
dated raw values, no raw note text, no PII. The two-phenotype content axis is
described as "interpersonal / brainfog" vs "illness-leaning" note *content*, not
quoted text. The household-illness feasibility is reported as de-identified counts
(18 note-dates, essentially absent as an external marker) with no raw content. The
subject is referred to as "the participant." Clean.

**6. Internal consistency - PASS.** The three sections agree with each other and
with the JSON shape:
- Fingerprints (section 2) <-> JSON `fingerprints` array: physical in_heart_rate
  true, seen_in cardiac/activity/battery; cognitive seen_in empty, overnight_hrv
  "no trace (either night)"; emotional in_heart_rate false, seen_in daytime
  stress/battery, overnight_hrv "drop, peaking the following night." All consistent
  with the prose and the scripts.
- Two-phenotype extension (2b) <-> honesty flags (3): both keep the trigger claim
  out of the robust layer and both foreground the unclear majority.
- Headline in prose (2 "Net") == headline in JSON. Confidence field matches the
  "newer / less-settled" flag in the status header.
The only note (see N2) is that the physical JSON omits resting HR, which is an
understatement, not an inconsistency.

---

## Closing

The card is a faithful, honestly-limited, non-overclaiming summary of the R4
descriptive precondition, the crash-specificity analysis, and the exploratory
two-phenotype note. Every load-bearing number was reproduced live from the scripts;
the `*` vs `ns` distinctions, the good-day confound, the non-circularity split, the
suggestive-not-established quarantine of the emotional-trigger claim, and the
"5 of 29 labelled, 24 unclear" floor are all intact and correctly emphasised. The
Wiggers concession is quoted verbatim and read fairly. Privacy is clean. It is
**safe to hand to the website team as-is**, with the single MINOR (M1) recommended
as a small prose clarification so a lay reader does not read the sleep-stress
HRV-proxy as significant on both nights.
