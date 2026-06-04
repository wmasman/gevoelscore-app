# Step 4 (v2 — explicit defer marker): Learned exclusion rules

**Status:** Deferred — v2 (post-soak follow-up).
**Trigger to graduate:** v1.6.x keyword-rules feature has shipped AND the `calendar_events.user_decision` field has enough signal (typically: > 20 events with `user_excluded` across recognisable title patterns over a sustained period) to make a learned-rules engine non-speculative.
**Why deferred:** The signal we need lives in `calendar_events.user_decision`, which v1.6 already captures at no cost. There's no point designing the inference engine before we know what patterns the user actually exhibits.

---

## What this step would deliver

A background aggregation that watches `calendar_events.user_decision = 'user_excluded'` patterns and, when a new event arrives whose title / attendee count / time-of-day matches a strong-signal exclusion pattern, sets `included_as_context = false` proactively + surfaces a one-time `Suggestie: deze series uitsluiten? (X eerder uitgesloten)` chip in the Context tab.

## Proposed shape (subject to refinement when the trigger fires)

### Data

- New collection `calendar_pattern_decisions(id, pattern_kind, pattern_value, decision, confidence_score, last_observed_at)` storing aggregated patterns.
- `calendar_events.user_decision` already exists from v1.6 step-0 (AC0.19).

### Pull-time logic

- Sync orchestrator (the same `src/lib/sync/calendar-sync.ts` from v1.6 step-1) gains an optional `applyLearnedRules` step that runs AFTER `computeDefaultIncluded` but BEFORE the upsert. If a pattern matches with high confidence, sets `included_as_context = false` + `user_decision = 'auto'` (so the chip can flip it back to `user_included` if the user disagrees).

### UX

- A small `Suggestie` chip surfaces in the per-event sheet for events that were auto-included-OR-auto-excluded by a learned rule. One-tap to confirm or undo.

### Aggregation

- A new daily cron job (`learned_rules_aggregation`) reads `user_decision` from the last N days and updates `calendar_pattern_decisions`. Re-uses the existing `cron_monitor` + `/api/health/cron` infrastructure from v1.6 step-2.

## Out of scope at trigger time

- No LLM. Pattern matching is rule-based (title substring, attendee-count threshold, time-of-day band).
- No cross-user learning (single-user app).
- No "explanation" UI for why a rule fired beyond the chip text.

## Acceptance criteria, technical constraints, and test plan

To be filled in when the trigger fires. Pattern: copy the rigor of v1.6 step-1's structure; keep the data layer lean since the field (`user_decision`) is already present.

## Done

Not applicable until graduated. Updating this file is the graduation step.
