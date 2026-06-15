# Hypothesis lock process — workflow + sanity-check patterns

*Methodology MD. Drafted 2026-06-15 as a retrospective from the HA-C4b + HA-P7 locking sessions (option-A discipline arc). Companion to [CONVENTIONS.md §1.2](../CONVENTIONS.md#12-reviewer-mode-claude-reads--critiques--explains-does-not-edit-unless-asked) (reviewer-mode-with-authorization) and [reviews/README.md](../reviews/README.md) (audit layer structure). Anchored on what actually worked + what to look for, with worked examples cross-referenced.*

---

## 1. What this MD is, and what it does not

**Is**: a practical how-to for the project's hypothesis-pre-registration cycle — drafting → audit → revision → lock → run. Documents the discipline pattern that emerged from the HA-C4b + HA-P7 sessions and gives sanity-check questions a seasoned researcher should ask before signing a lock.

**Is not**: a methodology MD that locks a specific statistical choice (those live in their own MDs). Not the audit layer spec (that's [reviews/README.md](../reviews/README.md)). Not the reviewer-mode clause itself (that's [CONVENTIONS.md §1.2](../CONVENTIONS.md#12-reviewer-mode-claude-reads--critiques--explains-does-not-edit-unless-asked)).

Applies to: any Claude-drafted reviewer-mode pre-reg (`analyses/hypotheses/HA*-*/hypothesis.md`). Does not bind methodology MD locking (covered by [CONVENTIONS.md §2.2](../CONVENTIONS.md#22-methodology-md-before-locking-a-major-choice) and [`/research-methodology-review`](../../../.claude/commands/research-methodology-review.md)).

---

## 2. The 9-step arc (option A discipline)

For each hypothesis, the discipline is: 3 sessions × 3 stages. The arc is sequential per hypothesis but multiple hypotheses can be at different stages in parallel.

| stage | session type | output | locking signal |
|---|---|---|---|
| **1. Draft** | drafting (may be shared-context with research session) | `hypothesis.md` with `## Authorship` block at top | commit, but NOT a lock signal yet |
| **2. Audit** | **fresh session, no shared drafting context** | `reviews/HA-<id>-<date>.md` (audit report) | n/a |
| **3. Revise + lock** | shared-context (typically same drafting session continues) | revised `hypothesis.md` + explicit lock signal | commit with "LOCKED" status in Authorship |

The next stage after lock is the test-execution session (not part of the 3-stage lock arc):

| post-lock | session type | output |
|---|---|---|
| **4. Run** | shared-context test-execution session | `test.py` + `result.md` |

So for N hypotheses, the option-A arc is **3N sessions to lock** + N more to run. HA-C4b and HA-P7 each took ~3 sessions in this thread to reach lock (some compressed because the drafting + revision happened in the same shared-context session, with only the audit step requiring fresh context).

---

## 3. Step-by-step process (with what to do at each step)

### 3.1 Pre-step — register entry exists

Before drafting a formal pre-reg, the hypothesis lives at the register level:

- **Personal register**: [`personal_hypotheses.md`](../personal_hypotheses.md) (P1-P7)
- **Wiggers register**: [`wiggers_testable_hypotheses.md`](../wiggers_testable_hypotheses.md) (entries indexed A-F by Wiggers source-PDF section)

Register entries are reviewer-mode artefacts. They state intent + predictor + outcome + caveats, but at a less-locked level of operationalisation precision than a formal pre-reg. The register entry is the input to the drafting step.

### 3.2 Drafting step (Step 1 of the arc)

**Authorization**: the user explicitly invokes the option-A discipline. This grants reviewer-mode-with-authorization per [CONVENTIONS §1.2](../CONVENTIONS.md#12-reviewer-mode-claude-reads--critiques--explains-does-not-edit-unless-asked).

**Procedure**:

1. **Read the register entry + cited sources** end-to-end. Note any inconsistencies (e.g. P7's eligibility-outcome contradiction — eligibility "d not in episode" excluded the outcome `is_crash at d` by construction).

2. **Operationalisation-precision interview** — surface 2-4 load-bearing decisions the pre-reg needs to lock that the register glosses. Use the [AskUserQuestion tool](../../../.claude/) batch pattern to get all decisions in one round-trip. **Example questions that emerged in this thread**:
   - Eligibility framing precision (HA-P7: "d-1 not in episode" vs "d not in episode" vs "both")
   - Train/validate split inheritance (use HA11 family split for cross-test comparability)
   - Density encoding (continuous logistic vs binned tabulation vs both)
   - Null pre-spec form (3-criterion bar vs single criterion)
   - Construct-disambiguation sibling selection (HA-C4b: which channel ρ is closest)

3. **Set up the folder**: `mkdir -p docs/research/analyses/hypotheses/HA-<id>/`. The HA-prefix convention applies for the Wiggers + Personal register descendants (HA-C4b, HA-P7).

4. **Draft `hypothesis.md`** following the [HA11 pre-reg pattern](../analyses/hypotheses/HA11-stress-udip/hypothesis.md) — 10 sections + `## Authorship` block at top:
   - `## Authorship` block (top) — drafting date, agent, authorising user, drafting-session context, locked decisions from §3.2.2 interview, status line
   - §1 Claim
   - §2 Why we think this (prior sources)
   - §3 Data sources
   - §4 Measurement protocol (subsections per operationalisation choice)
   - §5 Pre-registered falsification criterion
   - §6 Exclusion rules
   - §7 Expected effect size if true (sanity-check ranges)
   - §8 Caveats result.md must explicitly acknowledge
   - §9 What we do with each outcome (branching pre-spec)
   - §10 Detection script architecture (run protocol)

5. **Authorship block status**: write `**Status**: drafted, not locked.` — the lock signal does not come at draft time.

6. **Commit** the draft. Commit message names the locked operationalisation decisions from the interview. **Push** to make the audit step possible in a separate session.

### 3.3 Optional post-draft revision r1 (data-exploration absorption)

If a data-exploration session runs between draft and audit (e.g. a visualisation pass that surfaces construct-validity facts about the predictor), the draft may be revised. **This is on the pragmatic side of the pre-registration debate** — strict pre-registration purists would object that any data-touching invalidates the lock.

**Discipline that makes this defensible**:

- Document the data exploration AS data exploration — not as test execution. The exploration's output (e.g. ρ values across sibling channels) does not touch the §5 falsification bar.
- Record the revision in the Authorship block as a separate revision entry (r1) with the rationale and what was changed.
- The revision absorbs *what siblings to include in the construct-disambiguation arm*, *what coverage gate to apply*, etc. — operationalisation refinements that the data informs without revealing the test outcome.
- Per the project pattern, this is acceptable when documented; a strict reviewer may still object on principle.

**Example**: HA-C4b's r1 absorbed the stress_low_motion_viz session findings:
- §4.11 sibling reordering (stress_high_duration_min ρ=0.79 → primary disambiguation sibling; HA11 u_dip_count ρ=0.556 → secondary)
- §4.3 wake-window coverage gate strengthening (the viz showed the inherited HA11 600-sample gate was too permissive)

### 3.4 Audit step (Step 2 of the arc)

**Critical discipline**: the audit MUST run in a **fresh session, no shared drafting-session context**. Same Claude model, but a new conversation — doc-only knowledge.

**To trigger** (paste into a fresh Claude session):

> Run `/research-review` on `docs/research/analyses/hypotheses/HA-<id>/hypothesis.md`. This is a Claude-drafted pre-reg under reviewer-mode-with-authorization per CONVENTIONS §1.2; produce the review report in `docs/research/reviews/` with the addendum "Fresh session — no exposure to the drafting context; doc-only knowledge." Apply the 4-layer checklist per `reviews/README.md`.

The audit report's filename convention: `HA-<id>-<YYYY-MM-DD>.md` (or `-v2.md` etc. for follow-up audits on revisions).

**What the auditor produces**:

- 4-layer checklist verdict (Layer 1 universal reporting / Layer 2 observational n=1 / Layer 3 time-series specific / Layer 4 project-specific audit hooks)
- Severity-graded fires (blocking / substantive / minor)
- Side observations (typos, broken paths, off-by-ones)
- "What would strengthen this finding" recommendations (may include substantive Layer-4 additions that aren't strictly fires)
- Verdict: REVISION RECOMMENDED / DEFENSIBLE / DEFENSIBLE-with-revision / etc.

### 3.5 Revise step (r2 — the bulk of methodological strengthening)

The audit's fires drive r2 in the drafting session (shared-context with the original draft is fine here — the audit was the independence step). **All r2 changes must be tracked in the Authorship block** as a separate revision entry.

**The pattern that emerged**:

- **L3.1/L3.4 (autocorrelation in null / CIs)** — almost always fires on the first audit. Fix: cite and adopt [`methodology/permutation_null_block_length.md`](permutation_null_block_length.md) — stationary bootstrap with `E[L] = 7` days + block-permutation null with the same E[L] policy + data-driven `E[L]*` companion + factor-of-2 flag. **Both HA-C4b and HA-P7 had this fire.** The HA-family null-machinery inheritance predates the canonical MD; new pre-regs adopt the canonical default.

- **L3.3 (multi-comparison discipline implicit)** — almost always fires when the falsification bar reports multiple cells. Fix: **single-cell headline lock** — pre-specify ONE cell as the SUPPORTED-bar-driving combination; all other arms are diagnostic / sensitivity ONLY (no independent SUPPORTED bar). **Both HA-C4b and HA-P7 had this fire.**

- **L4.4 (CONVENTIONS §3.4 crash-drop sensitivity)** — typically fires when a same-day correlation is reported. Fix: either add the sensitivity row (ρ with `is_crash == True` dropped, `|Δρ| > 0.10` flagged) OR explicitly dispatch §3.4 as inapplicable-by-construction (when the outcome IS `is_crash`, dropping crash rows eliminates the positive cases).

- **L4.3 (CONVENTIONS §3.3 column-duplication)** — fires when sensitivity ladders include near-identical columns. Fix: mark identical-by-construction columns explicitly in the table; they emit to the CSV for completeness but are NOT counted as independent sensitivity arms.

- **L4.6 (CONVENTIONS §3.6 named-counts triplet)** — fires when count phrasings lack the predicate + source-file. Fix: add the scheme + unit + source-file in the same phrasing.

- **Side observations** (paths, off-by-ones, date arithmetic, monotonicity tolerance, label ambiguity) — fix opportunistically; some side fixes may propagate to already-locked sibling pre-regs and require a v2 of those siblings.

### 3.6 Optional r3 (interpretability augmentation)

After r2 closes the audit fires, the user may ask for additional reporting that doesn't change the falsification bar but improves external interpretability. **Heuristic for "approach change vs reporting layer"**:

- **Approach change**: new conjunct in the falsification bar, new covariate that changes the headline, new statistical machinery (e.g. switching from logistic to ITS). These require a new audit gate.
- **Reporting layer** (no approach change): different formulation of an already-locked quantity, additional sensitivity arm that does NOT promote to SUPPORTED, descriptive companion output. These do NOT require a new audit gate.

**Example from this thread**: HA-C4b's r3 added Odds Ratio (OR) + Risk Difference (RD) with bootstrap CIs alongside the existing 15pp RD gate. The (a)+(b)+(c) falsification bar was unchanged; the OR was a more interpretable formulation of the existing (b) discrimination. **Reporting layer, not approach change.** No new audit gate needed.

### 3.7 Lock step (Step 3 of the arc)

**Lock signal**: explicit user acceptance + a commit message naming the lock + the Authorship block status updated to `**Status: LOCKED <date> by user acceptance.**`

**The lock commit's message** should:

- Name the revision number being locked (r2, r3, etc.)
- Confirm all audit fires are closed (or explicitly note any that are deferred to v2)
- State the next session writes `test.py` + runs + emits `result.md`

**After lock**: further modifications create v2 with v1 archived per the project's locked-pre-reg discipline. **The v1 result (if it lands first) is the canonical citation**; any subsequent v2 result is reported as a separate verdict with its own audit lineage.

### 3.8 Run step (post-lock)

Separate session (shared-context with the lock session is fine):

1. **Implement `test.py`** per the §10 detection script architecture in the pre-reg.
2. **`--dry-run` mode** prints sample sizes per phase × era, bin distributions, and sanity-check ranges per §7. **If sanity check fails → halt + revise spec → v2 with audit trail.**
3. **Full run** emits `result.md` directly into the pre-reg folder.
4. **No iteration on the spec after dry-run passes.** Post-dry-run revisions create v2 with v1 result archived.

---

## 4. Patterns for typical audit fires

Compiled from the HA-C4b + HA-P7 audits (both received REVISION RECOMMENDED on first audit; both closed all fires in r2).

### 4.1 Layer 3 BLOCKING — autocorrelation

**Fires when**: the pre-reg uses Wald CIs / Wilson CIs / Pearson CIs / asymptotic p-values on:
- Per-day metrics drawn from auto-correlated time series
- Rolling-window predictors (overlapping windows share input days)
- Crash-clustered outcomes (episodes span consecutive days)
- "No external null needed" claims on logistic regression

**Closure**: cite and adopt [`methodology/permutation_null_block_length.md`](permutation_null_block_length.md):
- Wald CI → stationary-bootstrap 95% percentile CI at `E[L] = 7`
- Wilson CI → block-bootstrap percentile CI at same `E[L] = 7`
- Asymptotic null → block-permutation null at `E[L] = 7` with B = 10,000 resamples
- Data-driven `E[L]*` companion + factor-of-2 flag (halt for review if outside `[3.5, 10.5]`)

**Why it's almost always fired**: the canonical MD was added 2026-06-13; the HA-family null-machinery predates it; new pre-regs that copy-paste from HA11 inherit the pre-MD pattern and need explicit adoption.

### 4.2 Layer 3 substantive — multi-comparison discipline

**Fires when**: the falsification bar reports multiple cells (per-phase × per-tier × per-window × per-direction × per-sensitivity-column) with implicit "headline is the primary cell + others are alongside" framing.

**Closure**: pick one of:
- **(a) Single-cell headline lock** — pre-specify ONE cell as the SUPPORTED-bar-driving combination; all other arms are diagnostic / sensitivity ONLY (cannot promote to SUPPORTED independently). **Used by both HA-C4b and HA-P7.**
- **(b) Bonferroni-style correction** across reported tiers. More machinery, less common in this project.

The (a) option is simpler and matches what most pre-regs implicitly mean by "headline".

### 4.3 Layer 4 minor — §3.4 crash-drop sensitivity

**Fires when**: a same-day correlation between a PEM-pacing variable and another channel is reported without the §3.4 crash-drop sensitivity row.

**Closure** — pick one of:
- **(a) Add the sensitivity row** — report ρ both on the full sample and with `is_crash == True` dropped; `|Δρ| > 0.10` flagged as a finding.
- **(b) Explicit inapplicable-to-primary dispatch** — when the inferential test's outcome IS `is_crash`, dropping `is_crash == True` rows eliminates positive cases by construction. Add a one-sentence §8 dispatch naming the descriptive correlation as the §3.4-binding venue.

HA-P7 used (b) for the primary + (a) for the descriptive Spearman.

### 4.4 Layer 4 minor — §3.3 column-duplication

**Fires when**: a sensitivity ladder includes near-identical columns (e.g. `_Mlow` and `_Mbelow_mod` that are identical-by-construction in v1).

**Closure**: explicit table marking each column "unique" or "identical-by-construction to <other> in vN". The duplicate columns emit to the CSV for completeness but are NOT counted as independent sensitivity arms.

### 4.5 Side observations — typical noise

- **Broken file paths** (especially when copy-pasted from a sibling pre-reg)
- **Off-by-one** in Python slice vs prose ("4-day window" but `[d : d + 3]`)
- **Date arithmetic** (boundary buffer being 21 or 22 days)
- **Loose tolerance** at small expected rates (absolute pp tolerance waiving the gate)
- **Register-row staleness** (pre-reg revised an eligibility rule, register entry not updated)
- **Caveat compression** (pre-reg paraphrases a register caveat in a way that loses precision)

Fix opportunistically. Some side fixes propagate to siblings — e.g. the labels CSV path bug in HA-P7 §3 was also in HA-C4b §3 (HA-C4b locked first, so fixing it requires a v2 of HA-C4b — queued for a separate commit).

---

## 5. Sanity-check questions before lock

A seasoned researcher (or a strict re-auditor) should ask these. If the pre-reg can answer "yes" or "explicitly dispatched", it's ready for lock.

| sanity check | applies to | pass condition |
|---|---|---|
| Is block-aware inference applied? | any test on time-series data | stationary bootstrap E[L]=7 + block-permutation null cited & applied |
| Is the headline cell unique and pre-specified? | any test with multiple sensitivity arms | single-cell §5.0 lock OR explicit Bonferroni correction |
| Is causal-attribution ambiguity surfaced if applicable? | any test where multiple causal stories fit | §8 caveat explicit + §9 outcome branching surfaces alternatives |
| Are effect sizes in community-standard formulation? | any inferential test | OR / RD / Cohen's d / Hedges' g reported with CIs |
| Are §3.4 / §3.7 / project audit hooks engaged or explicitly dispatched? | any Layer 4+ analysis | one of: applied, OR explicit one-sentence dispatch |
| Is the eligibility rule self-consistent? | any pre-reg with eligibility + outcome | rule does NOT exclude every possible positive outcome (the contradiction P7's audit caught) |
| Are FIT files / CSV paths verified? | any pre-reg citing source files | path exists in the audit-able tree OR is documented as external |
| Does the §9 branching enumerate all outcome paths? | every pre-reg | {SUPPORTED both, train-only, validate-only, refuted both, inconclusive, dry-run-fails, sensitivity-arm-diverges} all have explicit pre-spec |
| Does the §10 run protocol include a dry-run halt? | every pre-reg | "If sanity check fails → halt + revise spec → v2" |

---

## 6. Honest retrospective — what worked, what we'd do differently

### 6.1 What worked

- **The operationalisation-precision interview before drafting.** Surfaced the P7 eligibility-outcome contradiction. Surfaced the C4b sibling-ordering question. Without this step, those issues would have been audit fires (more expensive to fix).
- **The fresh-session audit pattern.** Both audits (C4b + P7) caught the autocorrelation BLOCKING fire that the drafting session was structurally blind to (the drafting session inherited the HA-family pattern without noticing it predated the canonical MD). The fresh-session discipline IS doing real work.
- **Numbered revisions (r1, r2, r3) with Authorship-block lineage.** Made the diff between revisions transparent. Made the lock signal unambiguous. Survived multi-day context without confusion.
- **The single-cell headline lock pattern.** Cleaner than Bonferroni; easier to reason about; matches the way most reviewers think about "primary outcome".
- **The "approach change vs reporting layer" heuristic for r3.** Let us add OR + RD to C4b without triggering a new audit gate.

### 6.2 What we'd do differently

- **Re-audit r2 in a fresh session before lock.** We mostly skipped this and went straight to user acceptance. The Wiggers Tier 1 plan suggests fresh-session audit AFTER lock as the canonical pattern. We compressed by skipping the r2 re-audit. For load-bearing project claims this compression may be too aggressive; for the option-A initial pass it was acceptable.
- **Power-calc dispatch.** Neither pre-reg has an explicit one-line dispatch about formal power calculation (defensible for n=1, but worth a one-line "power calc inapplicable per Daza 2018 within-subject design"). Add to the lock-process template for future pre-regs.
- **Propagate side fixes to siblings during the same session.** The labels CSV path bug in HA-C4b §3 was identified during HA-P7's audit but not fixed in HA-C4b before P7 lock. Now requires a separate v2 commit. Future practice: when an audit identifies a side fix that propagates, fix the sibling in the same commit if it's still unlocked, or open a v2 ticket immediately.
- **Register-entry updates after pre-reg revisions.** HA-P7's eligibility revision (Option A) is not yet reflected in `personal_hypotheses.md` P7. Queued but not actioned. Should be a step in the lock signal itself ("if the pre-reg supersedes the register entry, update the register with a forward pointer").

### 6.3 Time + cost estimates from this thread

| hypothesis | draft | r1 | audit | r2 | r3 + lock | run + result | total to-lock |
|---|---|---|---|---|---|---|---|
| HA-C4b | ~1.5h | ~30min | (fresh session) | ~45min | ~15min | pending | ~3h drafting time + audit |
| HA-P7 | ~2h | n/a | (fresh session) | ~45min | ~5min | pending | ~3h drafting time + audit |

Both audits took roughly 1 fresh-session of audit time + a few hundred KB of report. The total 3-session-per-hypothesis estimate from the option-A arc held in practice.

---

## 7. Cross-references

- [CONVENTIONS §1.2](../CONVENTIONS.md#12-reviewer-mode-claude-reads--critiques--explains-does-not-edit-unless-asked) — reviewer-mode-with-authorization clause; the discipline this MD operationalises.
- [CONVENTIONS §2.2](../CONVENTIONS.md#22-methodology-md-before-locking-a-major-choice) — methodology-MD-before-locking-a-major-choice; the methodology-side discipline this MD complements.
- [reviews/README.md](../reviews/README.md) — 4-layer audit checklist + verdict format.
- [methodology/permutation_null_block_length.md](permutation_null_block_length.md) — the canonical block-aware-inference policy that audits routinely fire on.
- [methodology/citalopram_phase_stratification.md §6](citalopram_phase_stratification.md#6-pre-registration-template-for-new-hypothesis-mds) — pre-registration template for new hypothesis MDs (the framework-adopter template).
- Worked examples (locked):
  - [`analyses/hypotheses/HA-C4b/hypothesis.md`](../analyses/hypotheses/HA-C4b/hypothesis.md) — stress-with-low-motion C4b pre-reg, locked at commit `80607e4`. 4 revisions (draft + r1 viz + r2 audit + r3 OR/RD).
  - [`analyses/hypotheses/HA-P7/hypothesis.md`](../analyses/hypotheses/HA-P7/hypothesis.md) — recent-crash-density P7 pre-reg, locked at commit `7f1ecc8`. 3 revisions (draft + r2 audit + r3 lock signal).
  - [`reviews/HA-C4b-2026-06-15.md`](../reviews/HA-C4b-2026-06-15.md) — C4b audit report.
  - [`reviews/HA-P7-2026-06-15.md`](../reviews/HA-P7-2026-06-15.md) — P7 audit report.
- [Wiggers Tier 1 execution plan](C:/Users/Gebruiker/.claude/plans/wiggers-tier1-execution-plan-2026-06-14.md) — the parallel-session Bucket C arc (HA-C3 + HA-C4 in inference.py + frame.py + pre-regs).
- Handoffs (open):
  - [P6 drafting handoff](C:/Users/Gebruiker/.claude/plans/session-p6-prereg-handoff-2026-06-15.md) — the descriptive-mode sibling pre-reg pending.

---

## 8. Status

**Drafted 2026-06-15** from the HA-C4b + HA-P7 retrospective. Working document — extend as the lock pattern evolves with subsequent pre-regs.

**Open follow-ups** for the lock process itself:
- Power-calc dispatch added to the §3.2 drafting checklist
- Re-audit-r2-before-lock as the canonical pattern (currently compressed)
- Auto-propagation of side fixes to sibling locked artefacts (currently manual)
- Register-row pointer update as a lock-step requirement (currently queued)
