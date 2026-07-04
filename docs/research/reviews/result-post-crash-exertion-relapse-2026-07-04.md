# Fresh-session peer review -- post-crash-exertion-relapse RESULT (test execution)

**Target**: [`../analyses/hypotheses/post-crash-exertion-relapse/result.md`](../analyses/hypotheses/post-crash-exertion-relapse/result.md)
and its test code
[`../analyses/hypotheses/post-crash-exertion-relapse/test.py`](../analyses/hypotheses/post-crash-exertion-relapse/test.py),
reviewed against the LOCKED pre-registration
[`../analyses/hypotheses/post-crash-exertion-relapse/hypothesis.md`](../analyses/hypotheses/post-crash-exertion-relapse/hypothesis.md)
(LOCKED 2026-07-04). Authoritative context read cold: the locked methodology MD
[`../methodology/post_crash_exertion_relapse.md`](../methodology/post_crash_exertion_relapse.md)
(DESIGN PROPOSED r3), the descriptive precondition
[`../analyses/descriptive/post_crash_exertion_relapse/precondition.md`](../analyses/descriptive/post_crash_exertion_relapse/precondition.md),
the sibling null precedent
[`../analyses/hypotheses/peri-event-covid/test.py`](../analyses/hypotheses/peri-event-covid/test.py),
the block-length policy
[`../methodology/permutation_null_block_length.md`](../methodology/permutation_null_block_length.md),
the shared inference utilities
[`../analyses/_utils/inference.py`](../analyses/_utils/inference.py),
the lagged-baseline extractor
[`../analyses/garmin_exploration/activity-labels/scripts/11_compute_lagged_baseline.py`](../analyses/garmin_exploration/activity-labels/scripts/11_compute_lagged_baseline.py),
the prior pre-reg review
[`hypothesis-post-crash-exertion-relapse-2026-07-04.md`](hypothesis-post-crash-exertion-relapse-2026-07-04.md),
and CONVENTIONS sections 1.2 / 2.1 / 3.5 / 4.1 / 4.3.

**Review type**: fresh-session independent cold review of a completed test-execution
result against its locked pre-registration. I did not draft or run the test.

**Reviewer mode**: fresh session -- no exposure to the drafting or execution context;
doc-plus-code knowledge only. I re-ran `test.py` independently to reproduce the reported
numbers and to probe the null construction and the matched-baseline pool composition.

---

## Overall verdict: ACCEPT-WITH-MINOR-REVISIONS

The result is a faithful, honestly-reported implementation of the locked pre-registration.
The single primary test is exactly the one section 8 names; the masking, the danger-window
and relapse arithmetic, the three matched-baseline calipers, the event-level block-permutation
null, and the peak-primacy rule are all implemented as locked. The "Cannot resolve" verdict is
read correctly as the pre-committed default for a null-spanning CI, is not upgraded, and the
slightly-negative point estimate is reported without spin. Every headline number reproduces
bit-for-bit on an independent re-run (the RNG is seeded, so the CI is reproducible too). No PII,
no em-dashes, GSS guardrail present, no interpretive/causal marks. NO-OUTCOME-PEEK holds.

It is not an outright ACCEPT because of three reporting-honesty gaps, none verdict-changing:
(1) the matched-baseline reference universe silently admits low-felt-state days, including 50
slots that are themselves `is_crash`/`is_dip` days, which inflates the baseline relapse rate and
biases the point estimate negative -- this is undisclosed and should be disclosed with its
direction; (2) the reported data-driven `E[L]* = 7.000` is a formula-degenerate fallback to the
default, not an independent confirmation, and result.md reads as if the estimator confirmed 7;
(3) a dead copy of the matched-baseline logic (`matched_baseline_pool`, never called) sits beside
the live inlined copy, a latent-drift hazard. All three are fixable in the result text / a code
tidy without re-running the primary or touching the verdict.

## NO-OUTCOME-PEEK INTEGRITY: HELD

The pre-registration was locked (committed) before `test.py` was written; the result is the single
place the exposure-versus-relapse relationship is computed, exactly as the pre-reg's binding box
promised. I checked for any sign the protocol was bent post-hoc to change the outcome and found
none. Specifically:

- The single primary test named in the result (section 1) is verbatim the section-8 primary:
  peak masked `max_hr_rank_lagged_lcera` x crash arm x 10-day window x 4-day relapse x
  matched-baseline contrast. No secondary arm is promoted; the rank-slope point estimate is
  positive (+1.31) while the named-primary standardised statistic is negative (-1.03), and the
  result explicitly keeps the negative standardised difference as the verdict rather than
  promoting the sign-favourable slope. That is the honest, no-peek-consistent choice -- a
  post-hoc bender would have promoted the positive slope.
- The 24-vs-28 event drop is disclosed as a mechanical consequence of the locked masking
  (result section 3 + implementation note A), not a quiet design change. I reproduced it: masking
  `is_crash`/`is_dip` days out of the `[d-90,d-30]` pool drops two dense-era windows (crash-015,
  crash-016) below `MIN_LAGGED_DAYS = 40`, and two early-2022 events (crash-001, crash-002) have
  an empty matched pool, leaving 24 usable of 26 built. This is the neighbouring-crash
  contamination the precondition section 3.3 foresaw.
- Every deviation from the pre-reg's anticipated n is disclosed and runs in the
  hypothesis-unfavourable direction or is neutral, which is the opposite of what outcome-peeking
  would produce.

## Reproduction

I ran `test.py` twice independently. All headline numbers match result.md exactly:
primary stat -1.0287, CI [-8.5780, +5.2134], p-analogue 0.6608, mean delta -0.1156, rank-slope
+1.3100, pool sizes min=0/median=17/max=50, 2 empty pools, ACF rho(1)=+0.1113 / rho(7)=+0.0843,
all sensitivities as tabled, per-event detail identical. The reproduction check (correlation
1.000000, max abs diff 0.000500) reproduces. The "verified across three runs" claim in section 1
is credible: the point estimates are seed-independent and the null CI is fixed by `RNG_SEED`.

---

## Findings by severity

### BLOCKING: none.

### MAJOR: none.

### MINOR

**M1. The matched-baseline reference universe admits low-felt-state days, including crash/dip
nadir days, and this is undisclosed (result section 6, test.py `reference_universe` line 541 +
the inlined pool builder lines 654-671).**
The danger-window peaks are gated felt-recovered (`gevoelscore >= 4`, the pre-reg's felt-recovery
gate). The matched-baseline reference, however, applies only the three locked calipers (rank-band
+/- 0.03, same `recovery_phase`, preceding-3-day gevoelscore mean +/- 1.0) with NO felt-recovered
gate on the baseline day itself. The felt-trajectory caliper is on the *preceding* 3-day mean, so
the baseline day's own felt-state is unconstrained. I measured the consequence directly on the
primary arm: of 530 matched-baseline pool-member slots across the 24 events, 50 (9.4%) have
`gevoelscore <= 3`, and all 50 of those are actual `is_crash` / `is_dip` days. Their follow-on
relapse rate is 0.580 versus 0.327 for the non-crash/dip baseline members. Including them inflates
the baseline relapse rate and pushes the delta negative: excluding them moves the point estimate
from mean delta -0.1156 / stat -1.0287 to -0.0871 / -0.7573. The verdict does not change (still
null-spanning "Cannot resolve"), and the direction of the bias is *conservative against the
hypothesis*, so it cannot have manufactured a false "Supported." But two honesty consequences
follow and are not currently carried:
- Result caveat (a) reads the overwhelmingly-high-strain non-relapsing danger windows as "case (2)
  territory (disconfirming)". That reading is partly an artefact of a baseline whose relapse rate
  is inflated by crash/dip contamination; the slightly-negative point estimate should not be
  leaned on as evidence of a disconfirming direction without this disclosure.
- The pre-reg's own framing (section 4d) is "equal-magnitude peak-strain days ... the same spike
  at baseline." A baseline "day" that is itself a crash/dip nadir is not naturally read as "the
  same spike at a settled baseline."
The code IS faithful to the three *named* calipers (the felt-recovered gate is not among the
locked three), so this is not a protocol violation -- it is an unstated property of the locked
construction that materially colours the point estimate.
**Fix**: add one paragraph to result.md section 6 (or the caveats) disclosing that the baseline
universe is not felt-recovery-gated, that N of the pool slots are `is_crash`/`is_dip` days, and
that their inclusion biases the point estimate negative (report the exclude-crash/dip sensitivity:
stat -0.76 vs -1.03, verdict unchanged). No re-lock and no verdict change; this is a disclosure.

**M2. The reported data-driven `E[L]* = 7.000` is a formula-degenerate fallback to the default,
not an independent confirmation, and result section 5 reads as a positive confirmation
(test.py line 692; `compute_data_driven_block_length`).**
I called the estimator directly on the masked series: it returns `optimal_block_length = 7.0` with
`note = "Closed-form formula degenerate; returning default"` and `cutoff_lag = 1`. The weak ACF
(rho(1) = +0.11) collapses the Patton-Politis-White Bartlett-kernel term, so the estimator does not
produce an independent E[L]*; it returns the project default of 7. result.md section 5 states
"Data-driven E[L]* = 7.000 (Politis-White / Patton-Politis-White estimator; cutoff lag 1). The
factor-of-2 override did NOT fire", which reads as if an independent estimate landed on 7. It did
not; the override "not firing" is trivially true because the fallback value equals the default it
is compared against. This over-states the strength of the companion diagnostic.
**Fix**: state in section 5 that the data-driven estimator degenerated on the weak ACF and fell
back to the default of 7 (so E[L] = 7 rests on the first-principles policy plus the ACF readout,
not on an independent data-driven optimum), and that the factor-of-2 flag is therefore
uninformative here rather than a confirmation. This aligns the reporting with the pre-reg's own
honest "the data-driven companion" language and with the null MD's deferred-citation posture.

**M3. Dead copy of the matched-baseline pool logic (`matched_baseline_pool`, test.py lines
321-352) is never called; the live pool construction is inlined in `run_arm` (lines 654-671).**
A static call-graph check confirms `matched_baseline_pool` is defined and never invoked. It
returns bare outcomes; the live inlined version returns `(date, outcome, magnitude)` tuples (the
null needs the dates for calendar ordering). Two copies of the caliper logic are a latent-drift
hazard: a future edit to one and not the other would silently diverge, and per the review
checklist a dead function "suggests a different intended path." I verified the inlined copy is what
runs and that it matches the three locked calipers, so the numbers are unaffected.
**Fix**: delete `matched_baseline_pool`, or have `run_arm` call it (adjusted to carry the date), so
one copy is authoritative.

### NIT

**N1. Per-replicate null uses a variable effective n that is not explained (test.py
`block_permutation_null`, `stat_for_labels` lines 431-449).** The null pools 24 danger-window peak
rows with their 530 baseline rows (554 total) and permutes the 24 danger-window labels across all
pooled positions under stationary blocks at E[L] = 7. Per replicate, an event contributes to the
delta only if its key retains at least one danger-window-labelled and one baseline-labelled unit;
I measured that on average only ~12.8 of 24 events contribute per replicate (range 7-18). This is
a legitimate label-permutation mechanic and mirrors the sibling precedent's spirit, and it is the
honest source of the heavy-tailed, very wide CI [-8.58, +5.21] that result section 4 already
attributes to a t-type standardised mean over few events. A one-line note that the permutation's
per-replicate contributing-event count is well below 24 (which is why the null has heavy tails)
would make the "well-behaved null" statement in section 4 fully transparent. Optional.

**N2. `auto_stress_cov` (test.py line 838) is computed and never used** (it counts danger-window
days corpus-wide, labelled "informational", but is not printed or returned). Harmless; drop it.

---

## Checklist pass-through (where a check passes cleanly, said briefly)

- **Faithfulness to sections 1/4/5/6/7/8 -- PASS.** Masked primary (4e) applied to the
  `[d-90,d-30]` pool with `is_crash`/`is_dip` exclusion, verified against the extractor algorithm.
  Peak = max single-day masked rank with deterministic earliest-day tie-break (4b), verified.
  Danger window = felt-recovery day .. nadir+10 inclusive (4a), verified. Three named calipers at
  the exact locked widths (4d), verified. Event-level block-permutation at E[L] = 7 with the
  data-driven companion and factor-of-2 override wired (6), verified present (see M2 on how it
  landed). 4-day relapse, strictly after the peak, `range(1, window+1)` -- no off-by-one (5),
  verified. Single primary test named and its CI is the verdict (8), verified.
- **Reproduction check (4e-2) -- PASS.** Un-masked recompute vs stored column, correlation
  1.000000, max abs diff 0.000500 = 3-decimal rounding of the stored column. Genuinely validating.
  The 24-vs-28 drop is honestly attributed to the masking (M-note A), reproduced independently.
- **Verdict honesty (8, 10) -- PASS.** "Cannot resolve" is the pre-committed reading of a
  null-spanning CI, not upgraded to "suggestive"/"consistent with". The slightly-negative estimate
  is reported straight. Peak-primacy respected: the positive rank-slope is explicitly NOT promoted.
- **Caveats (9 a-g) -- PASS in substance.** All seven are carried (result section 11). Caveat (a)'s
  two-case reading is stated and the mental-PEM escape is correctly confined to case (1); caveat
  (d)'s reverse-causation felt-lag directional bias is named with its suppress-a-true-positive
  direction. See M1: caveat (a)'s "case 2" lean should be tempered by the baseline-contamination
  disclosure.
- **Statistical hygiene -- PASS with M1/M2.** Direction + magnitude always reported with the
  p-analogue, never p alone. Single-pool primacy preserved (crash-vs-dip is a number with wide
  error, no era verdict). The wide CI is honestly explained as design power at 24 units, not hidden
  (N1 would make it fully transparent). The block-permutation respects the event-level structure
  and the E[L] = 7 blocks.
- **No danger-window leakage into the baseline -- PASS.** I confirmed 0 crash danger-window days
  (at the widest band, 14) appear in the reference universe; band-10 primary-window days are a
  subset and also fully excluded. Dip danger-window days are admitted, which is correct per the
  pre-reg's "outside any *post-crash* danger window" wording.

---

## Closing summary

The "Cannot resolve" verdict is trustworthy and faithfully derived. It is the pre-committed default
reading of a genuinely null-spanning CI, the primary test is exactly the locked one, no secondary
arm was promoted, and the no-outcome-peek boundary held. result.md is publishable as an honest null
once the three MINOR reporting gaps are closed: disclose the un-gated baseline universe and its
crash/dip contamination with the exclude-sensitivity (M1), correct the E[L]* reporting to a
formula-degenerate fallback rather than an independent confirmation (M2), and remove the dead
pool-logic copy (M3). None of the three changes the verdict, the primary statistic, or the lock; M1
and M2 make the honest-null even more defensible by naming what mildly pushes the point estimate
against the hypothesis and by not over-crediting the block-length companion. With those folded in,
this is an ACCEPT.

---

## Authorship

Claude (Opus 4.8) fresh-session independent cold reviewer, for the participant-researcher
(repo owner). 2026-07-04.
