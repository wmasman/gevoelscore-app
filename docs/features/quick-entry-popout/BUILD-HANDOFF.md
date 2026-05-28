# Build handoff: quick-entry-popout

> **You are picking up an exploration that has been planned, prototyped, and is ready to build.** This document tells you what to do, what to read, what to avoid, and when to stop and ask. Read it end-to-end first (≤ 10 min). Then read the required reading list (≤ 30 min). Then start Step 0.

---

## TL;DR

- This is an **alternative implementation** of the daily-entry UI — a persistent thumb-zone bottom-sheet where score / note / tags morph in place. Not yet on the v1 roadmap; build behind a `/lab` route by default (see Reconciliation below).
- Spec is locked. Five steps are planned. **Steps 0 and 1 are fully detailed and `/build-step`-ready.** Steps 2–5 are outlined; expand each as you approach it.
- **No new dependencies.** Native Pointer Events, vanilla CSS transitions, custom sheet primitive. All validated by two HTML prototypes.
- **Step 3 is blocked on `daily-entry/` Step 5 shipping first** (provides `<NoteField>` and `<TagCategoryList>`). Steps 0, 1, 2 can run in parallel with that other work.
- This is exploration code. Quarantined under `src/components/lab/` and `/lab/...` route. **Do not touch `src/app/page.tsx` or `src/components/today-shell.tsx` until you reach Step 4** — and even then, only after explicit decision per [step-4](step-4-integration-and-past-day.md).

---

## Required reading (in order, ~30 min)

1. **[design/brief.md](../../design/brief.md)** — sections "Spatial principle: thumb-first for input" and "Motion as communication". These are the two principles this feature implements. They were extracted during the design conversation that produced this feature; they now apply to the whole app.
2. **[design/explorations/quick-entry-popout.md](../../design/explorations/quick-entry-popout.md)** — the spec. UX shape, all the trigger moments, the morph mechanics, the end-of-flow pulse, the past-day distinction. Read fully.
3. **[design/explorations/quick-entry-popout.md#validation-log](../../design/explorations/quick-entry-popout.md#validation-log)** — what's already been confirmed and what's deferred. Two HTML prototypes (also in `docs/design/explorations/`) validated the gesture and the full flow visually. Open them in a browser before you start coding — they're your visual reference for "what right looks like".
4. **[README.md](README.md)** — feature plan overview. 32 acceptance criteria, technical decisions, component architecture, alternatives considered, the explicit position relative to the `Soak-test mode` memory.
5. **[architecture/frontend-conventions.md](../../architecture/frontend-conventions.md)** — already familiar to you. **Re-read the styling section.** This feature uses Tailwind utility classes throughout; no CSS modules. (A first draft of step-1 violated this; it has been corrected.)
6. **[testing.md](../../../.claude/testing.md)** — TDD doctrine. RED → GREEN → REFACTOR. Mandatory test layers per step.

Optional but recommended (~10 min):
- Skim the two HTML prototypes in `docs/design/explorations/`. They are not production code, but they are the source of truth for "the gesture works like this" and "the morph timing feels right at these values".
- Skim [daily-entry/README.md](../daily-entry/README.md) sections "Component architecture" and "Steps". Several of those primitives (`useDayEntryUpsert`, `<SaveStatus>`, `<NoteField>`, `<TagCategoryList>`) are reused here.

---

## Build sequence with current status

| # | File | Status | When you can start |
|---|---|---|---|
| 0 | [step-0-shared-primitives.md](step-0-shared-primitives.md) | **Ready** — full ACs, code skeletons, 20 test cases, ~150 LOC budget | Now |
| 1 | [step-1-bottom-sheet.md](step-1-bottom-sheet.md) | **Ready** — full ACs, code skeleton (Tailwind), 10 unit + 3 e2e cases, ~150 LOC | After Step 0 |
| 2 | [step-2-score-circle.md](step-2-score-circle.md) | Outline. Implementation reference is `docs/design/explorations/score-circle-prototype.html` (a near-direct React port of the JS in that file). Expand the plan before `/build-step`. | After Step 1 |
| 3 | [step-3-quick-entry-flow.md](step-3-quick-entry-flow.md) | Outline. **Hard external prerequisite: `daily-entry/` Step 5 must ship first.** Cannot start until then. | After Steps 0, 1, 2 AND `daily-entry/` Step 5 |
| 4 | [step-4-integration-and-past-day.md](step-4-integration-and-past-day.md) | Outline. **Has a reconciliation decision point** — see "Reconciliation" section below. | After Step 3 |
| 5 | [step-5-reconciliation.md](step-5-reconciliation.md) | Outline. Post-deploy mobile validation + cleanup. | After Step 4 ships and is deployed |

**Use `/build-step` for each step.** It enforces the RED → GREEN → REFACTOR loop, runs the verify gate, and writes the Done section into the step file.

---

## The non-obvious rules for THIS feature

Most of these are spelled out in the spec or the brief, but they're easy to forget under build pressure. Read them once, then internalize.

### Quarantine all new code under `src/components/lab/`

This is exploration code. The `lab/` namespace tells the other programmer at a glance that this is not on the v1 production path. Once Step 4 makes a reconciliation decision, code may be promoted out of `lab/` — but **not before that point**.

### Tailwind utility classes, not CSS modules

Every component in this feature uses Tailwind utilities (composed with `cn()` from `src/lib/ui/cn.ts` where dynamic). The only acceptable inline-style values are those driven by imperative state (drag transforms, keyboard-aware bottom positioning). See [step-1-bottom-sheet.md#11-srccomponentslabbottom-sheettsx](step-1-bottom-sheet.md) for an example of how this is done correctly.

### Zero new dependencies

Native Pointer Events, vanilla CSS transitions, `createPortal`, the four shared hooks from Step 0. **Do not add `@use-gesture/react`, `framer-motion`, `vaul`, `@headlessui/react`, or anything else.** The decisions are documented and justified in the README. If you find a case where you genuinely think a new dep is the right call, stop and write up the case — do not add it inline during a build step.

### No em-dash (`—`) in user-facing strings

Project-wide rule, captured in the [feedback memory](../../../../../../.claude/projects/C--Users-Gebruiker-Documents-gevoelscore-app/memory/feedback_no_emdash_in_ui.md). Applies to anything that renders as text on screen: `src/copy.ts`, JSX literals, button labels, ARIA labels. Use comma, period, or colon instead. Prose in docs (including this one) and code comments are exempt.

### Motion is communication, not decoration

Every animation you add must answer "does this tell the user something they need to know?". Allowed: slide-open, crossfade between steps, one-shot tint-pulse on completion, scale-pulse per integer cross on the score circle. Forbidden: ambient glow, loading shimmer, repeating pulses, celebratory bounce. Full rule in [design/brief.md#motion-as-communication](../../design/brief.md#motion-as-communication).

### Thumb-first applies to input only

The popout itself is an input surface — thumb-zone rules apply. Reading surfaces (the day-overview behind the sheet, the timeline, the calendar) are free. Don't try to force the rest of the app into the same pattern.

---

## Coordination with the other in-flight work

### `daily-entry/` Step 5 (the other programmer's work)

That step is building `<NoteField>` and `<TagCategoryList>`. **Our Step 3 imports both.** Implications:

- **Watch their progress.** Don't start our Step 3 until their Step 5 is shipped (in `main`, tests passing).
- **Read their PR when it lands** to verify the component APIs match what our Step 3 plan assumes (prop names, save semantics). If they differ, write a small adapter at the start of our Step 3 — don't fight them on it.
- **Steps 0, 1, 2 of this feature can run in parallel with their Step 5.** Use that parallelism.

### `daily-entry/` Step 4b (also in flight or recently shipped)

Step 4b builds a horizontal score row at the top of `<TodayShell>`. This feature offers an alternative. The two directions cannot coexist on the home route. **Reconciliation is deferred to our Step 4** — see next section.

### What to do if their work and yours conflict

Surface it. Open the question with the user before forcing a resolution. The two efforts were intentionally parallel to keep options open; merging or choosing one is a strategic call, not a tactical one.

---

## Reconciliation: the Step 4 decision point

`daily-entry/` Step 4b's horizontal score row lives at the top of `<TodayShell>`. This feature's popout, if it lands, takes over the home flow. They are incompatible at the route level.

Three options exist; Step 4 of this feature has Option C as the default:

- **Option C (default): build under `/lab/quick-entry-popout`.** Home flow is untouched. User can navigate to the lab route from a deployed environment to test the popout. After post-deploy validation in Step 5, the user decides whether to promote.
- **Option A: rip and replace.** Quick-entry-popout becomes the canonical daily-entry flow; Step 4b code is removed. Bigger, less reversible.
- **Option B: coexist behind a Settings toggle.** Both flows live in the codebase; user picks. More maintenance overhead.

**Your job in Step 4: confirm or revise the option choice with the user before writing the integration code.** Do not assume Option C just because it's the default — circumstances may have changed by the time you reach Step 4.

---

## Logging progress and updates

As steps land, update these places:

| Update | Where | When |
|---|---|---|
| Step file's `Done criteria` checkboxes | The step file itself | After verify passes for that step |
| Step file's `Side-quests caught during implementation` and `Evidence` sections | The step file itself | Same time |
| Validation log entry for any real-device finding | [design/explorations/quick-entry-popout.md#validation-log](../../design/explorations/quick-entry-popout.md#validation-log) | After any mobile or device-specific check |
| If you add a new shared hook the other programmer might use, add a one-liner to the daily-entry README's "Component architecture" section | [daily-entry/README.md](../daily-entry/README.md) | If applicable |
| If the spec changes during build (you discover the design is wrong somewhere), update [design/explorations/quick-entry-popout.md](../../design/explorations/quick-entry-popout.md) and add a brief note about why | Same | Whenever the spec needs revision |

Do not update the design brief or the design-system unless you find a genuine new principle the project should adopt. Both already capture the two principles this feature implements.

---

## When to ask vs when to proceed

**Proceed without asking** when:
- An acceptance criterion is ambiguous in a small way and you can pick a reasonable interpretation. Document the choice in the step's Done section.
- A test is harder to write than expected and you find a cleaner approach. The test plan in each step is a starting point, not a contract.
- You find a small inconsistency between two docs in this feature. Pick the one that's more recent / more specific, fix the other, and note it briefly.

**Stop and ask** when:
- You're considering adding a new dependency. The justification needs to be written up and accepted before the dep lands.
- The reconciliation decision in Step 4 needs to be made. That is explicitly a user-call.
- A spec decision feels wrong once you try to build it. Surface the friction before you work around it — the spec may need revising.
- `daily-entry/` Step 5 ships with an API that meaningfully differs from what our Step 3 plan assumes. A small adapter is fine; a redesign is a conversation.
- Post-deploy mobile validation in Step 5 reveals something that contradicts the design. The validation log lives there for a reason — record and discuss before patching.

---

## Pre-flight checklist (before you start Step 0)

- [ ] Read all 6 required-reading docs (~30 min). You should be able to articulate the thumb-first principle, the motion-as-communication principle, and what each of the five steps ships.
- [ ] Open both HTML prototypes in your browser (`docs/design/explorations/score-circle-prototype.html` and `docs/design/explorations/quick-entry-flow-prototype.html`). Play with them. You should know what the gesture, the morph, and the end-of-flow pulse feel like before you start writing the React equivalent.
- [ ] Confirm `npm run verify` is green on the current branch. If it isn't, that's not yours to fix — surface it.
- [ ] Confirm the other programmer is not mid-rewrite of `daily-entry/` Steps 4b or 5. If they are, coordinate timing so you're not stepping on each other's tests.
- [ ] Skim `src/hooks/use-day-entry-upsert.ts` — that's the existing shared hook our Step 3 will eventually wire up. You don't need it for Steps 0, 1, 2 but knowing it exists shapes how you think about state ownership.

When all checked: run `/build-step` and point it at [`step-0-shared-primitives.md`](step-0-shared-primitives.md). The skill takes it from there.

---

## What "done" looks like for this whole feature

Three exit conditions, any of which is acceptable:

1. **Shipped to home.** Steps 0–5 complete; Step 5 chose Option A or B; reconciliation cleanup landed; mobile validation passed; this feature is now the canonical daily-entry flow.
2. **Living at `/lab/`.** Steps 0–4 complete with Option C; Step 5 validated on deployed device but user decided not to promote. The feature lives indefinitely as an explorable alternative.
3. **Rejected.** Mobile validation in Step 5 reveals the direction doesn't work for the user in practice. The code stays in `lab/` as a learning artifact, or is removed entirely; the two extracted principles (thumb-first, motion-as-communication) remain in the brief regardless. The feature plan gets a `Status: rejected, post-mortem in step-5` line and we move on.

All three are honest outcomes. Don't anchor on shipping if the evidence says rejecting is correct.

---

## Questions about this handoff

If anything in this document feels wrong, contradicts the spec, or is missing context you need to start work — surface it before you start. A 5-minute conversation now beats a half-built feature with the wrong shape.
