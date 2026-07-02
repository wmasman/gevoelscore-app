# Review — R23 pre-registration `peri-event-covid/hypothesis.md`

**Target**: [`../analyses/hypotheses/peri-event-covid/hypothesis.md`](../analyses/hypotheses/peri-event-covid/hypothesis.md)
(R23 pre-registration: does the overnight autonomic factor visibly move
during the 2022-03 COVID infection versus the pre-COVID healthy
baseline?)
**Review date**: 2026-07-02
**Reviewer**: Claude (Opus 4.8), fresh-session peer reviewer.
**Fresh session, no exposure to the drafting context; doc-only
knowledge.** Independent reviewer-mode peer review per
[CONVENTIONS §1.2](../CONVENTIONS.md) (drafting-under-authorization ->
fresh-session review), against the locked methodology
[`../methodology/peri_event_known_event_check.md`](../methodology/peri_event_known_event_check.md),
its methodology review
[`methodology-peri_event_known_event_check-2026-06-30.md`](methodology-peri_event_known_event_check-2026-06-30.md)
(M1 to M6), the descriptive precondition
[`../analyses/descriptive/peri_event_covid/precondition.md`](../analyses/descriptive/peri_event_covid/precondition.md),
and the predicted-direction anchor
[`../literature/reviews/acute_viral_infection_autonomic_signature_review.md`](../literature/reviews/acute_viral_infection_autonomic_signature_review.md).

---

## Overall verdict

**ACCEPT-WITH-MINOR-REVISIONS.**

**NO-OUTCOME-PEEK: HELD.**

**Counts: 0 BLOCKING, 0 MAJOR, 5 MINOR, 2 NIT.**

This is a disciplined, faithful pre-registration. The no-outcome-peek
lock holds airtight, the predicted direction is genuinely prior-given
from the external literature review, and all six methodology fixes (M1
to M6) are absorbed. The M1 null re-specification is implemented
correctly and the drafting agent's three self-flagged ambiguities are
each resolved in the defensible direction. The remaining items are
clarity and internal-consistency tightenings, none of which change the
design or gate the test. It can lock and proceed to `test.py` after the
MINOR items are addressed (or explicitly waived by the researcher); none
is a hard blocker.

---

## Findings (keyed to the checklist)

### 1. NO-OUTCOME-PEEK held? — HELD (no finding)

**Verdict: HELD. This is the single most important check and it passes.**

I audited every quantitative statement in the pre-reg for a leak of a
factor value, mean, z-score, percentile, trend, or infection-vs-baseline
contrast. Nothing leaked.

- The binding lock (lines 24 to 57) enumerates exactly what has been
  seen (event dates, window length, non-null coverage counts, factor
  definition, comparator-window counts, resolved anchor) and what has
  not (any value / mean / median / z / percentile / trend / contrast in
  any window). It states plainly that no `test.py` has been written or
  run and the value columns have not been opened for the infection
  window.
- Every quantitative statement in the body is a **row-presence / non-null
  day count**: `14/14`, `31/31`, `215/217`, `216/217`, `217/217`
  (lines 37 to 39, 164 to 165); comparator-window counts `15` and `204`
  (lines 43 to 44, 250 to 258); the `lc_phase` span 217 days (line 158).
  No channel value appears anywhere.
- The correlation structure disclosed in the factor-provenance paragraph
  (rho = -0.922, +0.377, lines 167 to 175) is a **fixed instrument
  definition** computed on the 2022-09-03 to 2026-06-05 window, and the
  pre-reg says so explicitly and states it is NOT re-fit on the infection
  window and is NOT an infection-vs-baseline contrast. This closes the
  one residual peek-surface the methodology review flagged as M3. These
  rho values are a factor-structure property, not an R23 outcome.
- The literature anchor reads no project data and fixes direction from
  population physiology only (confirmed against the acute review's own
  no-outcome-peek statement, lines 5, 80, 99 there). So the prior is
  genuinely external.

I found no place where an infection-vs-baseline result could have leaked.
**Contract verdict: HELD.**

### 2. Direction genuinely prior-given (confirmatory, §4.3), not fished — PASS (no finding)

The high-autonomic-load-pole direction is sourced from the literature
review and physiology, not from a data look:

- §1's per-channel table (`stress_mean_sleep` UP, `bb_highest` DOWN,
  `resting_hr` UP, lines 83 to 86) maps channel-for-channel onto the
  acute review's RQ1 table (lines 15 to 21 there), including the strength
  gradations (RHR strong/direct; GSS moderate-strong / one inferential
  step; BB moderate/inferred).
- §2 (lines 101 to 136) runs the §4.3 three-test justification explicitly
  (lived-through dates from contemporaneous notes; external literature;
  mechanistic argument) and correctly states the pre-registration
  protects the **outcome** (unseen) while the **direction** is prior-given.
  This is the correct §4.3 posture.
- The "one inferential step" gap on the derived Garmin indices (GSS-up,
  BB-down inferred from the directly-validated HRV-down / RHR-up inputs)
  is disclosed as a caveat, not laundered as direct evidence (lines 120
  to 124, 342 to 346). This is the §4.2 caveat-vs-a-priori discipline
  applied correctly.

Confirmatory framing is justified. No data-fishing. **PASS.**

### 3. Null specification valid (M1 fix) — PASS, one MINOR clarity note

**MINOR-1 (clarity).** The M1 fix is implemented correctly. §5
(lines 228 to 277) specifies the primary p-analogue as the **daily-series
stationary bootstrap with E[L]=7** regenerating the null distribution of
the 14-day-window-mean factor-z statistic, and it explicitly states the
204 overlapping sliding windows are "**never** a p-value denominator"
(lines 256 to 258) — exactly the M1 correction (adjacent sliding windows
share 13 of 14 days, so a naive percentile against 204 understates the
tail). The n=15 non-overlapping windows are correctly framed as a
**transparent sanity-check rank**, not the primary inference (lines 246
to 252), and named with scheme + unit + source per §3.6. The E[L]=7 /
E[L]* within-2x confirmation is present and correctly gated "before
locking the inference" (lines 244 to 245).

The methodology review offered two routes for M1: route (i) percentile
against the n=15 non-overlapping windows as primary, or route (ii) a
daily-series stationary bootstrap regenerating the window-statistic null.
The pre-reg selects **route (ii)** and demotes the n=15 rank to a sanity
check. This is defensible and is in fact the E[L]=7-consistent route the
methodology MD's revised d3 already named (MD lines 315 to 329). No
defect.

The only clarity note: §5 says the bootstrap "regenerates the null
distribution of the 14-day-window-mean factor-z statistic" but does not
spell out the resampling mechanics (does each bootstrap replicate
regenerate a synthetic 217-day daily series and then take one 14-day
window mean, or the full sliding distribution per replicate?). Route (ii)
as the methodology review described it regenerates a synthetic baseline
per resample; the pre-reg text is compatible with that but under-specifies
it. **Recommended fix**: add one sentence to §5 stating the per-replicate
mechanic (resample the daily factor-z series under E[L]=7 blocks to a
217-day synthetic series, compute the 14-day-window-mean statistic under
that synthetic null, repeat to build the reference distribution). This is
a `test.py`-level detail but pinning it in the locked pre-reg removes a
post-lock degree of freedom. Not blocking; the intent is unambiguous.

### 4. Tiered criterion (e3) coherent and locked before the look — PASS, one MINOR (adjudicates self-flag #2)

The three tiers (§6, lines 289 to 303) are unambiguous and correctly
one-sided-oriented: MOVED = beyond the 95th percentile in the predicted
(high-load) direction; AMBIGUOUS = inside the band; MOVED-UNEXPECTED-
DIRECTION = beyond the 5th percentile in the opposite direction, framed
explicitly as a severity-gated guard, not a prediction (consistent with
the acute review's RQ3 severity-gated / moderate reading). The predicted
tail and 95th-percentile threshold are stated locked before the look
(lines 295 to 296). Coherent and locked.

**MINOR-2 (internal consistency — adjudicates self-flag #2, the factor-z
sign convention).** The primary statistic is the single-anchor daily
factor-z on `stress_mean_sleep` (g1), z-scored so that **upward = the
high-load pole** (anchor stress elevated). The tiered criterion is
oriented entirely on this single anchor's sign, and that is internally
consistent: the MOVED tail is unambiguously "`stress_mean_sleep`
elevated" (line 291), and the percentile is read on the anchor's
factor-z, which has one sign. So the **primary** inference has no sign
ambiguity — good.

The residual risk is in the **g2 triad companion**, which mixes an
inverse channel: `bb_highest` is predicted to move DOWN at the high-load
pole while `stress_mean_sleep` and `resting_hr` move UP. The pre-reg's
coherence flag is defined as "did all three move in the predicted signs
together (anchor up, `bb_highest` down, `resting_hr` up)" (lines 194 to
198, 307 to 309), which is correct — but a `test.py` author computing a
naive z on `bb_highest` and asking "is it in the high-load tail?" could
sign-flip it if the coherence flag is implemented as "all three z-scores
positive" rather than "all three in their predicted signs." **The sign
convention on the primary is consistent and locked; the risk is confined
to the companion's implementation.** Recommended fix: add one explicit
sentence to §4.1 g2 stating that the coherence flag tests each channel
against **its own predicted sign** (anchor and RHR: positive deviation;
`bb_highest`: negative deviation), NOT a uniform "all z positive" test,
so the inverse channel is not accidentally sign-aligned in `test.py`.
Adjudication: **the g2 sign convention is correct as written but should
be made implementation-proof.** MINOR, not blocking; the primary contrast
is unaffected.

### 5. Anchor contingency (M2) correctly resolved — PASS (no finding)

HA07c `stress_mean_sleep` is correctly locked as the primary anchor. The
lock (lines 44 to 46), §3 (lines 145 to 149), and the closing footer
(lines 404 to 406) all state the g1 contingency is satisfied by the
**coverage check only** (`stress_mean_sleep` non-null 14/14 in the
infection window and 215/217 = 99.1% in the comparator band per the
precondition §5.1), and that the HA06b `resting_hr` fallback is **NOT
triggered**. This is the M2 fix exactly: the anchor choice is keyed to a
row-presence coverage fact, decided before any value is seen, not a
researcher degree of freedom exercised after the look. The precondition's
§5.1 resolution (its lines 178 to 199) is the coverage-only source and
the pre-reg cites it faithfully. **PASS.**

### 6. All required caveats present (§8) — PASS, one MINOR

§8 (lines 323 to 367) carries all six required caveats, each accurate:

- **(a) M5 acute-vs-LC-onset inseparability** (lines 327 to 336):
  correct and strongly stated — `LC_ERA_START = 2022-04-04` is the day
  after the window's close, the two are temporally inseparable, and a
  MOVED result must be phrased as "departed baseline around the
  infection / LC-onset hinge," never "the acute infection caused the
  factor to move." Matches M5 and CONVENTIONS §5. Good.
- **(b) stress = Garmin GSS, not mental** (lines 337 to 339): present,
  and the guardrail also appears on first substantive use in §1
  (lines 94 to 99) per the project stress-guardrail rule. Accurate.
- **(c) FR245 no direct HRV / proxy** (lines 340 to 346): present,
  correctly names `resting_hr` as the strongest direct channel and the
  GSS/BB legs as one inferential step, and flags the device-generation
  mismatch (Fitbit/Apple/Oura cohorts vs Garmin) with "direction
  generalises, calibration does not." Accurate.
- **(d) n=1, not crash-precursor** (lines 347 to 352): present, bounds
  the reach to "this signal, this subject, this one event" and states it
  does not establish crash-precursor value. Accurate.
- **(e) correlational, effective-N approx 1** (lines 353 to 357):
  present, no variance-explained defined, HA07c/HA10 rho = -0.92 = one
  signal viewed twice per §3.3. Accurate.
- **(f) M4 severity characterisation** (lines 358 to 364): present,
  "home-recovered and febrile, days in bed, 0 training week 12, not
  hospitalised," used to justify down-weighting blunting to moderate.
  Matches M4 and the precondition annotation. Accurate.

**MINOR-3 (completeness).** §8 has a seventh item **(g)** "no causal /
interpretive marks on the descriptive layer (§4.1)" (lines 365 to 367)
which is correct and welcome, but the checklist's six named caveats are
all present and accurate. No missing caveat. The one small gap: caveat
(d) states one event "cannot separate the factor tracks infection from
the factor happened to move that fortnight," which is the correlational-
effective-N-approx-1 point's temporal cousin, but the **effective-N
approx 1 as a correlational-not-independent-witnesses** framing (checklist
item "correlational-effective-N-approx-1") is carried in caveat (e), not
(d). Both are present; this is only a note that the checklist's
"correlational-effective-N-approx-1" maps to (e). No fix required.

### 7. Faithful to the methodology MD — PASS, adjudicates the three self-flags; one MINOR

The pre-reg does not deviate from, over-specify, or under-specify the
locked design in any material way. The three drafting-agent self-flags:

- **(a) E[L]=7 bootstrap governing BOTH the percentile-null AND the d2
  standardised-difference CI.** ADJUDICATED: **correct and faithful.**
  MD decision d3 (MD lines 326 to 329) states "one null model serves
  both the p-analogue and the CI." §5's d2 paragraph (lines 260 to 265)
  says "from the same bootstrap machinery, so one null model serves both."
  This is a legitimate efficiency (one E[L]=7 stationary bootstrap on the
  daily factor-z series yields both the window-statistic reference
  distribution and the standardised-difference CI) and it matches the MD
  verbatim in intent. No conflation, no defect. The only residual is the
  under-specification noted in MINOR-1 (spell out the per-replicate
  mechanic once).

- **(b) the factor-z sign convention.** ADJUDICATED under MINOR-2 above:
  the **primary** single-anchor sign convention is internally consistent
  and locked (upward = high-load pole); the residual risk is confined to
  the g2 companion's inverse channel and is an implementation-proofing
  fix, not a design defect.

- **(c) §3.7 detrend applied to the raw g2 triad channels, not the
  z-scored primary (MD decision d / M6).** ADJUDICATED: **correct, and
  the narrowed scope matches intent.** §5's detrend paragraph (lines 267
  to 272) states the §3.7 audit-hook "fires on the **raw** channels in
  the g2 triad companion, not on the z-scored primary (whose scope §3.7
  excludes)." This is exactly M6(b) and the CONVENTIONS §3.7 scope
  ("does NOT apply to lagged-baseline z-score comparisons"). The pre-reg
  narrows the detrend correctly. Note the belt-and-braces framing
  (line 270, "expected negligible ... pre-LC band is flat healthy") is
  the disciplined default and is consistent with §3.7's worked-example
  rationale.

**MINOR-4 (M6(a) wording — window-max semantics).** M6(a) required
clarifying that "window-max" = max **daily** factor-z, not an intraday
§3.5 spike count. §4.2 (lines 205 to 210) carries this correctly:
"window-max here means the max over **daily** factor-z, not an intraday
spike count (per methodology review M6); the per-minute intraday version
is deferred to a higher-resolution follow-up." Absorbed. This is noted as
a confirmed-present item, not a defect. (Listed as MINOR only to record
that I checked it against M6(a); if the researcher prefers, treat as
resolved/no-action.)

**MINOR-5 (§4.4 acute-core overlay under-specification).** §4.4
(lines 220 to 226) correctly states the acute-core (2022-03-23 to
2022-03-30) overlay and the +/-7-day buffer are "presentation, not test"
and do NOT enter the primary contrast (decision a1). Faithful. One small
under-specification: it does not state whether the acute-core overlay's
own percentile (if computed for the sensitivity overlay) is read against
the same E[L]=7 null or is purely visual. Since decision a1 makes it
descriptive-only, "purely visual, no percentile" is the natural reading,
but one clause confirming the overlay carries no separate p-analogue
would remove ambiguity and forestall a second implicit test. Recommended
fix: one clause in §4.4. Not blocking.

### 8. No PII, no em-dashes, stress-guardrail on first use — PASS, two NIT

- **Em-dashes**: none. Confirmed by scan; the file uses commas, periods,
  and colons throughout, per the project no-em-dash rule. **PASS.**
- **Email / real name**: no email address, no personal name, no BSN. The
  Authorship block credits "Claude (Opus 4.8) ... for the
  participant-researcher (repo owner)" with no email or personal name
  (lines 59 to 66). **PASS.**
- **Stress-guardrail on first use**: present at §1 (lines 94 to 99) on
  first substantive use, and repeated in caveat (b). **PASS.**

**NIT-1 (Windows path with OS username).** Line 141 carries the absolute
data path `C:\Users\Gebruiker\Documents\gevoelscore-data\unified\per_day_master.csv`,
and line 143 in §3 repeats the same. "Gebruiker" is the Dutch generic
account name ("User"), not a personal name, and the same path convention
appears in CONVENTIONS.md and the methodology corpus, so the publication
audit (which scans for names from an external names list, emails, BSN,
and medical-doc filenames, not OS usernames) will not flag it. This is a
NIT, not a finding: if the researcher wants belt-and-braces publication
hygiene, replace the absolute prefix with `$GEVOELSCORE_DATA_PATH/...`
(the env-var convention CONVENTIONS §5 already uses) so no local
filesystem layout is disclosed. Purely optional.

**NIT-2 (self-referential review-cross-link).** The footer (lines 405
to 407) says the pre-reg is "to be peer-reviewed by `/research-review` in
a fresh session before `test.py` is written or run" — which is this
review. After this review lands, a one-line lock-log or cross-link to
this report would close the loop. Optional, post-lock housekeeping.

---

## Recommended disposition

Address MINOR-1 (spell out the bootstrap per-replicate mechanic) and
MINOR-2 (implementation-proof the g2 inverse-channel sign convention)
before lock, as they are the two items most likely to bite the `test.py`
author. MINOR-3 through MINOR-5 and both NITs are optional tightenings
the researcher may waive with a one-line note. None gates the test. The
no-outcome-peek lock is airtight and the design is faithful to the locked
methodology; on the two MINOR fixes (or their explicit waiver) this
pre-reg is ready to lock and proceed to `test.py`.

---

## Authorship

| Field | Value |
|---|---|
| Reviewed by | Claude (Opus 4.8) fresh-session reviewer, for the participant-researcher (repo owner) |
| Date | 2026-07-02 |
| Mode | Reviewer-mode fresh-session peer review of a drafting-under-authorization pre-registration (per CONVENTIONS §1.2). No exposure to the drafting context; doc-only knowledge. |
| Verdict | ACCEPT-WITH-MINOR-REVISIONS. NO-OUTCOME-PEEK: HELD. 0 BLOCKING, 0 MAJOR, 5 MINOR, 2 NIT. |
