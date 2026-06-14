# crash_episode_prolonged — overlay rule for chained crash + dip events

**Status**: draft, pending Layer 3 descriptive (`crash_episode_descriptive.md`).
**Drafted**: 2026-06-12.
**Relation to crash_v2**: additive overlay; does not modify the locked
[`crash_v2-definition`](../analyses/hypotheses/crash_v2-definition/definition.md).

---

## 1. The rule

A **prolonged episode** is a contiguous span of two or more crash_v2
events (crashes or dips, in any order) whose inter-event gap is shorter
than the **empirical recovery window** for this person. Inter-event gap
is measured in days from `event_A.end_date` to `event_B.start_date − 1`.
The recovery window value is the **75th-percentile time-to-baseline**
across isolated crash episodes, derived from the user's own data in
`crash_episode_descriptive.md`. Until that descriptive lands, the rule
is parameter-free: the threshold value is a placeholder.

Events that have no neighbour within the recovery window stay
**isolated**. Prolonged episodes are not classified as "crash" or "dip"
themselves — they are a higher-order grouping. Each constituent day
keeps its original crash_v2 label (`crash`, `dip`, or `normal`).

## 2. Why

Three reasons for adding the overlay:

1. **Peri-event baseline contamination.** Wiggers hypotheses A1, A3, A4,
   C1, D4, F1, F2, F4, G1 use peri-event alignment around `is_crash=True`
   days. The pre-event baseline window (e.g. `t-14 … t-7`) needs to be
   free of *other* events for the comparison to be clean. If event B
   starts inside event A's recovery window, A's recovery state pollutes
   B's pre-window. The overlay groups such pairs so peri-event tests can
   choose to either: (a) align on the prolonged event's start and end,
   or (b) exclude prolonged events and test only on isolated ones.
2. **Dose-response ladder for A1.** A1 ("RHR deviation scales with
   exertion proxy") gains a fifth ordinal level when the
   `prolonged_class` is available: `none / dip-general / dip-brainfog /
   isolated-crash / prolonged-crash`. The prolonged level is predicted
   to show a larger and more *sustained* RHR deviation than the
   isolated level. Tests of A4 (sustained HR elevation) and C4 (stress
   fails to drop) on the same prolonged events give cross-validation
   inside the A/C suite without adding new measurements.
3. **Wiggers H3 (acute illness vs PEM) discriminator.** The overlay's
   illness-marker cross-check (see §5.3 below) may show that prolonged
   events co-occur with `pwc_illness_flag=True` or with
   `cat_sub_keel_resp` / `cat_sub_systemisch_vermoeid` mentions at a
   higher rate than isolated events. If so, the `prolonged_class`
   becomes a stratifier for H3 by itself — separating likely-illness
   spans from likely-PEM spans for the per-day signature comparison.

## 3. What this overlay does NOT do

- Does not change any per-day `is_crash`, `is_dip`, `dip_type`,
  `crash_episode_id`, `dip_cluster_id`, `in_crash_tail`, or `tail_median`
  value. crash_v2 is locked.
- Does not merge isolated dips. Dips that have no crash within the
  recovery window stay as crash_v2 dips (with their existing
  `dip_cluster_id` for the dip-to-dip 7-day chain rule).
- Does not establish a new event tier. There is no "prolonged crash"
  classifier — only a grouping id for events that happen to chain.
- Does not impute mechanism. Whether a prolonged event reflects
  unresolved PEM, an acute illness, an environmental stressor, or
  something else is downstream interpretation; the overlay reports
  structure only.

## 4. Operationalisation

### 4.1 Sidecar CSV (Layer 3 output)

Layer 3 produces
`$GEVOELSCORE_DATA_PATH/processed/crash_labels/prolonged_episodes_proposed.csv`
with columns:

| column | meaning |
|---|---|
| `prolonged_episode_id` | int; shared across all days in the prolonged span |
| `date` | day inside the span |
| `crash_episode_id` | nullable; from crash_v2 |
| `dip_event_id` | nullable; per-dip id from crash_v2 |
| `dip_cluster_id` | nullable; from crash_v2 |
| `prolonged_class` | one of: `isolated_crash`, `isolated_dip`, `prolonged_crash_dip`, `prolonged_crash_crash`, `prolonged_dip_only` |

`isolated_crash` and `isolated_dip` rows are also written for events
with no neighbour inside the recovery window — the sidecar is a complete
event-level index.

### 4.2 Master integration (deferred decision)

The sidecar is **not** folded into `per_day_master.csv` in the same
pass. After reviewing `crash_episode_descriptive.md`, the user decides
whether to add two columns:

- `prolonged_episode_id` (int, nullable on `normal` days)
- `prolonged_class` (categorical, as above)

If folded in, both columns get rows in [`DATA_DICTIONARY.md`](../DATA_DICTIONARY.md)
and an update-log entry. The merge threshold (the recovery-window value)
is recorded in the dictionary entry so the lineage is reproducible.

### 4.3 Re-application

The overlay is deterministic given (a) crash_v2 labels and (b) the
recovery-window threshold. Re-running the rule on an extended corpus
produces a stable id assignment for events before the previous end-date.
If the recovery-window threshold is revised (e.g. after another year of
data shifts the empirical p75), the overlay re-runs and ids may
re-assign; that's an explicit refresh, not silent drift.

## 5. Consequences

### 5.1 Hypotheses gated on this overlay

Each of the following pre-registrations needs the prolonged-episode
column available before locking:

| H | use of the overlay |
|---|---|
| A1 | dose-response ladder, 5-level outcome including `prolonged_crash` as top tier |
| A3 | peri-event window can align on `prolonged_episode.start` instead of per-event `episode_start` |
| A4 | sustained HR elevation predicted stronger inside prolonged spans (cross-validation with A1) |
| C1 | peri-event baseline purity |
| C4 | stress-decay-after-peak predicted to fail more often inside prolonged spans (cross-validation with A1 + A4) |
| D4 | BB drain slope across the full prolonged span, not per sub-event |
| D5 | morning BB after overexertion — the prior-day exertion needs to be measured outside the prolonged span to be clean |
| F1, F2, F4 | sleep metric peri-event baseline purity |
| G1 | respiration peri-event baseline purity |
| H3 | `prolonged_class` becomes a stratifier for the acute-illness vs PEM comparison if §5.3 confirms co-occurrence with illness markers |

H1, H2, H5 are unaffected (they do not use peri-event windows the same
way) or only indirectly affected through the events the overlay groups.

### 5.2 Statistical effects to expect

- **Event count drops** for peri-event hypotheses that switch to the
  overlay — fewer prolonged events than constituent sub-events. Sample
  size reduction is a known consequence of the cleanliness gain.
- **Effect sizes on prolonged events likely larger** than on isolated
  events, if Wiggers' "sustained sympathetic" framing holds. Tests of
  A1 / A4 / C4 should report effect sizes separately for isolated and
  prolonged classes; the magnitude difference is informative
  regardless of which test "wins".
- **Multiple-comparisons accounting** does not change — prolonged-vs-
  isolated is one stratifier inside a single hypothesis test, not a
  separate test.

### 5.3 Illness-marker cross-check

Layer 3's task 6 reports raw co-occurrence rates of prolonged events
with `pwc_illness_flag=True`, `cat_sub_keel_resp > 0`, and
`cat_sub_systemisch_vermoeid > 0` in the span or in the 3 days before.
If co-occurrence is materially higher than for isolated events, two
things follow:

- The `prolonged_class` becomes a usable H3 stratifier (likely-illness
  vs likely-PEM spans) without explicit illness labelling.
- A1 / A4 / C4 results for prolonged events should be reported both
  with and without illness-co-occurring spans, so the Wiggers PEM
  signature is not conflated with the acute-illness signature.

The co-occurrence is reported as counts only. No threshold for
"materially higher" is fixed in this doc — the user inspects the
descriptive output and decides.

### 5.4 What stays the same

- All crash_v2 downstream analyses already built on `episode_id` or
  `dip_cluster_id` keep their inputs unchanged. The overlay is
  optional; existing K01, K02, H02b, notes-categorisation re-runs
  continue to use crash_v2 labels as before.
- The 7-day `in_crash_tail` flag stays as crash_v2's descriptive
  recovery indicator; the empirical recovery window introduced here
  is a separate measurement for the overlay rule only.

## 6. Open items

Resolved by Layer 3 descriptive:

- Empirical recovery-window value (p75 or other percentile).
- Whether to merge dip-only chains (`prolonged_dip_only` class).
  crash_v2 already groups dips via `dip_cluster_id` with a 7-day rule;
  if the empirical recovery window is shorter than 7 days, the
  dip-only overlay would split some existing clusters. The descriptive
  reports both rules' counts so the user picks.
- Whether prolonged events that straddle LC-phase boundaries get split
  or kept whole.

Resolved by user after reviewing descriptive:

- Whether to fold `prolonged_episode_id` + `prolonged_class` into
  `per_day_master.csv` or keep them in the sidecar.
- Whether the overlay supersedes per-event peri-event tests in the
  pre-registration drafts for A1 / A3 / A4 / C1 / D4 / F1 / F2 / F4 / G1,
  or runs alongside as a separate stratification.

## 7. Cross-references

- [`analyses/hypotheses/crash_v2-definition/definition.md`](../analyses/hypotheses/crash_v2-definition/definition.md) —
  the locked v2 spec this overlay sits on top of.
- [`methodology/lc_phase_descriptive.md`](lc_phase_descriptive.md) —
  shape template for the upcoming `crash_episode_descriptive.md`.
- [`methodology/garmin_indicators_audit.md`](garmin_indicators_audit.md) —
  per-column provenance for the predictors used in §5.1 hypotheses.
- [`wiggers_testable_hypotheses.md`](../wiggers_testable_hypotheses.md) —
  pre-registration draft column mapping; entries for A1 / A3 / A4 / C1
  / C4 / D4 / F1 / F2 / F4 / G1 / H3 will reference this overlay once
  it's locked.
- [`DATA_DICTIONARY.md`](../DATA_DICTIONARY.md) — update log entry to
  be added when the overlay is folded into the master.
