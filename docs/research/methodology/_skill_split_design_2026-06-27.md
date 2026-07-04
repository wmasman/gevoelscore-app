# Skill-split design — `/research-interpret` → 7 sub-skills

**Status**: DECISION-CAPTURED 2026-06-27. Not yet implemented. Migration scheduled AFTER Phase A re-open closes (see §4 migration-scope rule).

**Origin**: 2026-06-26 conversation reflecting on Phase A's friction. Seven type-level errors in one cluster wave (construct-validity miss; dispatch-mode vocabulary drift; proper-name fabrication; null-prior inflation; analogue mischaracterisation; L7 channel/derivative; stratum-boundary dates) — all caught by user spot-check or fresh-session review, none by agent self-discipline. Diagnosis: methodology substance is well-justified; agent-facing surface (1 catch-all skill + 6 guides + 70+ anti-patterns held simultaneously) exceeds reliable attention budget per invocation. Skill split targets the attention-budget strain without touching the methodology substance the user wants to keep intact ("lets keep the basis for now").

---

## 1. Skill set (7 total, replacing the 1 catch-all)

| Skill | Scope | Loads (per-invocation working set) |
|---|---|---|
| `/interpret-bootstrap` | Once per session — scaffolds `_open_inputs.md` + `plain_language_dictionary.md`; checks layer state | plan + map + stocktake |
| `/interpret-d` | Stage D — descriptive precondition audit per HA | guide #1 + target HA pre-reg + result.md |
| `/interpret-i` | Stage I — verdict→inference per HA | guide #2 + target HA + Stage D artefact |
| `/interpret-s1` | Stage S₁ — internal cluster synthesis | guide #3 + map + constituent HAs' Stage I artefacts |
| `/interpret-s2` | Stage S₂ — external contextualisation per topic | guide #4 + map + constituent clusters' S₁ artefacts + literature anchors |
| `/interpret-a` | Stage A — actionability per construct | guide #5 + map + constituent topics' S₂ artefacts |
| `/interpret-t` | Stage T — translation to audience | guide #6 + target construct's A artefact |

Per-invocation context drops ~60-70% vs the current catch-all (1 guide loaded vs 6; one stage's anti-patterns vs all six stages' combined).

## 2. Namespace decision — router (not 7 top-level commands)

Single top-level `/research-interpret` slash-command with stage as the first argument. `/research-interpret d HA-C3` routes to the d sub-skill; `/research-interpret s2 topic-stress-fatigue-pacing` routes to s2; etc.

Reasons:
- 7 slash-commands inflates the discoverability surface
- Stage-as-argument lets stage args evolve without renaming the user-facing command
- Matches existing project pattern (`/code-review ultra <args>`, `/plan-feature <args>`)
- Bootstrap is the one exception — `/research-interpret bootstrap` with no other args.

## 3. Phase-halt pattern inside each stage-skill — 5 halts

This is the load-bearing cooperation design. Each stage-skill is internally a 5-phase pipeline that **halts at each phase boundary for user input**:

| Phase | What the agent does | Halt to user |
|---|---|---|
| **1. LOAD + GATE** | Read inputs; confirm upstream artefacts LOCKED; identify missing inputs | "Ready to proceed? Open-inputs list: …" |
| **2. INTERVIEW** | Walk §8 interview seeds with user, one seed at a time | Per seed: collect answer (no `DEFAULTED-PENDING-USER-INPUT` defaults via guess) |
| **3. DRAFT** | Draft the artefact from collected interview answers | Present full draft for read |
| **4. PRE-LOCK STRUCTURAL CHECK** | Run the structural checklist (see §3.1 below) | Report check results — accept r1 / iterate / dispatch fresh review |
| **5. LOCK** | Write lock-log entry; update status header; register drift triggers | Confirm lock |

Precedent: matches `/build-step`'s RED → GREEN → REFACTOR halt-loop pattern.

### 3.1 Pre-lock structural check items (Phase 4)

A shared sub-skill `/research-interpret prelock <artefact-path>` that any stage-skill calls out to. Single source of truth for the checklist; DRY discipline. Initial items (extendable per stage):

1. Every external claim has a `literature/`-relative path-and-section citation OR a literature-gap log entry. (Maps to guide #4 §9.6 gate 3; analogue across guides.)
2. All mandatory L-IDs for the artefact type are present (per limitations-doc §5 citation row).
3. All dispatch-mode placeholders match SKILL.md r4 locked vocabulary verbatim (no invented names). (Origin: today's R1 finding.)
4. Construct-identity verdicts present per cross-cited named metric (§4.3.5 guide #4 binding). (Origin: today's R1 + Wiggers miss.)
5. Every cross-guide cited anchor (e.g., "internal_synthesis §4.4 default-to-CONFLICT") is verified against the cited guide's current LOCKED content. (Origin: today's A1 finding.)
6. Proper names sourced — no fabricated author / institution names. (Origin: Suzan→Laure miss.)
7. Null priors recorded literally — no guess-default inflation. (Origin: Phase A.1 null-prior inflation friction.)
8. Status header lock-version + lock-log row format matches existing per-file convention.
9. No `SKIPPED-AS-DRY-RUN-DEFAULT` on disciplines that disallow it (e.g., §4.3.5).
10. Hard predictive gate (§3.10) not crossed — no PPV / sensitivity / specificity claims outside Stage A tier-2+.

## 4. Migration scope rule — Phase A re-open FIRST, then migrate

Migration order:
1. **Phase A re-open** under the existing `/research-interpret` skill (closes today's outstanding work without compounding it with restructuring)
2. **Worked-example sub-skill** — draft one stage-skill MD (proposed: `/research-interpret s2` since that's where today's miss lived) as a concrete validation of the split shape before committing all six
3. **Full migration** — write remaining six skills + bootstrap; retire the catch-all (or keep as deprecated-router that delegates)
4. **Citation updates** — guides #1-#6 update their "agent-instruction outline" sections to point to specific stage-skills; SKILL.md r4 retired or marked deprecated
5. **Memory + MEMORY.md** updated with the new pointers

The Phase A re-open uses guide #4 r3 §4.3.5 as authority for the construct-validity correction. The corrected artefacts will be the first inputs the new `/research-interpret s2` skill processes when it lands (validation that the split correctly handles already-corrected artefacts).

## 5. Open at next-pass — items to settle when drafting the s2 worked example

- Exact interview-seed list per stage (currently lives in each guide's §8) — copy verbatim or restructure?
- Pre-lock check #4 (construct-identity verdicts per metric) — only fires for S₂; how does the shared `/interpret prelock` know which checks apply per stage?
- Bootstrap skill responsibilities — what does it do that the current SKILL.md §x bootstrap routine does, and what's hoisted out?
- Cross-stage handoff — when `/interpret s2` finishes, does it suggest the next stage-skill to invoke (auto-recommend `/interpret a` next), or does the user route?
- What replaces the current SKILL.md §4.6 placeholder-discipline section — re-stated per stage, or hoisted to a shared methodology section the skills cite?

## 6. References

- Origin conversation: 2026-06-27 (session continuation from 2026-06-26 Phase A retrospective)
- Related decisions:
  - [[feedback-helpers-design-reactively]] — helper-folder refactor deferred; same general principle (build from observed redundancy not speculation) applies to the worked-example-first migration order
  - [`_plan_results_analysis_layer.md`](_plan_results_analysis_layer.md) — the layer this skill instruments
  - [`/research-interpret SKILL.md`](../../../.claude/skills/research-interpret/SKILL.md) r4 LOCKED — the catch-all being split
  - Today's `/research-methodology-review` of guide #4 r3 ([review report](../reviews/methodology-external_contextualisation-r2-to-r3-2026-06-26.md)) — captured the R1 dispatch-mode vocabulary drift that informs pre-lock check #3
