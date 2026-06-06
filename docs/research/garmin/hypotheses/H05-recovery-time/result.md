# H05 — Result: recovery-time spec produced a trivial distribution

**Verdict: SPEC-INDUCED TRIVIAL. The pre-registered recovery target is
too lenient to be informative. The distribution is not a finding about
recovery; it's a finding about the spec.**

The pre-registered protocol returned **0 days of recovery time for all
25 episodes that qualified for measurement**. Median 0, IQR 0–0, range
0–0. Not just for some episodes — all 25. Hypothesis.md §7 flagged
exactly this case as a data-quality trip wire:

> "If we see median 0 days for everything, the recovery target is set
> too low ... should be flagged in result.md as a data quality issue."

So this is not "the user recovers instantly from crashes." This is "the
recovery target as specified is **structurally** met on the day after
episode-end."

No `card.md`. The path forward is **H05b** with a recovery target that
actually requires sustained recovery to register. Data:
[result-data.json](result-data.json).

## Why the spec is broken

The pre-registration set:
- `crash_v1` low day: score ≤ 3
- Episode merge: episodes within 3 days are merged
- Recovery target: `baseline − 1`
- Recovery = first day with `score ≥ recovery_target`

The trimmed pre-episode baseline for this user typically sits around
4.3–4.5 (driven by the heavy clustering of scores at 4 and 5; see
[counts.md](../00-crash_v1-counts/counts.md)). So `recovery_target ≈
3.3–3.5`.

By definition of episode construction:
- An episode ends on the last low day (score ≤ 3) of its last
  constituent run.
- A non-low day (score > 3) immediately following the run is what made
  the run end. If that day were within 3 days of another low day, the
  merge rule would have absorbed it.
- Therefore the day after episode-end has score > 3, which always
  satisfies the recovery target of 3.3–3.5.

Recovery is trivially satisfied. The 0-day result is mechanical, not
biological.

This kind of error is why hypothesis.md §7 set the trip wire. The
preflight idea would have caught it if we'd run "what's the median
recovery time on a small sample first?" before locking — a meta-lesson
for next batch.

## What this does *not* mean

- **It does NOT mean recovery is instant.** This is a critical
  distinction. The data still contains the recovery information; the
  spec just doesn't extract it.
- **It does NOT mean recovery-time analysis is impossible** — only
  that the specific operationalisation we pre-registered does not
  work.
- **It does NOT invalidate the other tests in this batch.** The
  crash_v1 detection upstream of this test is identical to H01-H04 and
  unaffected.

## Episode counts (still useful)

|                                          | n     |
|------------------------------------------|------:|
| total crash_v1 episodes                  | 29    |
| excluded too close to window end         | 2     |
| excluded insufficient pre-baseline       | 2     |
| **episodes measured**                    | **25** |
| recovered (under broken spec)            | 25    |
| censored by next crash (under broken spec) | 0   |

The 0-censoring count is also revealing: under the broken spec,
recovery is so easy to satisfy that no episode runs into the next
crash before "recovering."

Eras (descriptively useful, even with the broken metric):
- Train (2022–23): 12 episodes measured
- Validate (2024+): 13 episodes measured

That's a reasonable split for any future H05b version.

## What H05b should look like

Candidate revised specs (one would be chosen and pre-registered before
running):

### Option A — Sustained recovery to normal score

- **Recovery target** = the user's pre-episode baseline rounded down
  (so typically score ≥ 4, sometimes ≥ 5).
- **Sustained** = the target must be met for at least 2 consecutive
  days, with no score ≤ LOW_THRESHOLD in between.
- **Recovery time** = day-after-episode-end to first day of the
  sustained-recovery run.

This catches the realistic case where one mediocre day (score 4) after
a low run isn't really "recovered" — full recovery requires the score
to stay normal.

### Option B — Recovery to pre-episode baseline mean

- **Recovery target** = within 0.5 of `baseline` (not `baseline − 1`).
- Same single-day recovery rule.
- **Tighter target, no sustained requirement.**

Likely produces a distribution somewhere between Option A's stricter
version and the broken H05 result.

### Option C — Both

- Run both A and B as parallel descriptive metrics. The card can then
  say "first day back to normal: X. First sustained week of normal: Y."

Recommendation when H05b is pre-registered: **Option A**. The
"sustained" criterion is closer to what the user actually experiences
as recovery and is more useful for the eventual shielder-vs-reliever
analysis.

## Caveats acknowledged

- Per hypothesis.md §8, recovery time as a statistical artifact is not
  the same as clinical recovery. Even a fixed spec would only measure
  "score returns to baseline," not "user feels back to themselves."
- The pre/post-2024 comparison is moot under the broken spec.
- The same data is still there in the same place; H05b can be designed
  and run with confidence in the underlying signal.

## What we do next

- Mark H05 spec-broken in registry. Add H05b stub to deferred.
- Proceed to **the synthesis document** as planned by the user — the
  synthesis can stand even with H05's spec-broken status, because
  H05's failure is informative about the protocol not about recovery.
- The synthesis will list this as one of the methodology lessons:
  *small dry-run on a few episodes before locking a measurement
  protocol catches definitional artifacts that pre-registration
  alone does not.*

---

*Test run 2026-06-05. Re-runnable but uninformative as specified.*
