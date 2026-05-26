# gevoelscore-app — context for Claude

Personal Long COVID daily-tracking app. One tap to log a "gevoelscore", optional note + tags, timeline to spot patterns. Pre-prototype: docs only, no source code yet.

## Source of truth

Read the relevant doc before suggesting anything. Don't restate them here.

- [README.md](README.md) — overview, status, license
- [docs/REQUIREMENTS.md](docs/REQUIREMENTS.md) — **cardinal principles** + v1 requirements (read first)
- [docs/app_brief_gevoelscore.md](docs/app_brief_gevoelscore.md) — UX, input flow blokken 1–5, data model, version roadmap
- [docs/technisch_document.md](docs/technisch_document.md) — tech stack, integrations, privacy, licensing
- [.claude/conventions.md](.claude/conventions.md) — file structure, code/copy conventions, repo hygiene
- [.claude/testing.md](.claude/testing.md) — **TDD doctrine** (the loop, mandatory test layers, RED-first rule, anti-patterns)

## Key rules

- NEVER create documentation proactively. Only write `.md` files when the user explicitly asks.
- Follow established patterns in the codebase (once code exists).
- NEVER use unicode/emojis in scripts.
- Store utilities in `scripts/`, `tests/`, `config/` subfolders only.

### Think before coding

- State assumptions explicitly. If uncertain, ask.
- If multiple interpretations exist, present them — don't pick silently.
- If a simpler approach exists, push back.

### Simplicity first

- No features beyond what was asked.
- No abstractions for single-use code.
- No error handling for impossible scenarios.
- If 200 lines could be 50, rewrite it.

### Surgical changes

- Don't "improve" adjacent code, comments, or formatting.
- Don't refactor things that aren't broken.
- Match existing style, even if you'd do it differently.
- Remove imports/variables that YOUR changes made unused.
- Don't remove pre-existing dead code unless asked.

### Goal-driven execution

- Transform tasks into verifiable goals with success criteria.
- For multi-step tasks, state a brief plan with verification checks.
- Loop until verified.

## Working with Claude on this project

- **Planning new work**: `/plan-feature` — turns a requirement or brief section into a feature folder under `docs/features/{name}/` with README + TDD-shaped step files. Enforces cardinal-principle, privacy, security (OWASP MASVS-aligned for mobile + local-first), and v1.5/v2 readiness gates. Every step file produced has Acceptance Criteria, Technical Constraints, and a Test Plan — naming every test before any code is written.
- **Implementing a step**: `/build-step` — walks one step file through the strict RED → GREEN → REFACTOR loop. Pairs with `/plan-feature` and reads from [.claude/testing.md](.claude/testing.md). Refuses to run if the step file lacks acceptance criteria or a test plan.
- **TDD is mandatory.** Tests before implementation, every time. Pure-styling work replaces tests with a visual baseline screenshot — it is not exempt from the loop, only the testing technique changes.
- **Before suggesting a dependency, framework, or pattern**: check it survives all 6 cardinal principles and the local-first / no-telemetry rule. If it doesn't, propose an alternative.
- **When the brief and a clean architecture disagree**: the brief wins. The user has 1.363 days of evidence about what works for daily logging.
- **UX calls (sub-10-second flow, brainfog-friendly)**: ask. They aren't testable in unit tests.
- **No source code yet**: don't fabricate paths or imports as if code exists. Update this section when the first prototype starts.
