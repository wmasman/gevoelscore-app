# Hypothesis lock process — workflow + sanity-check patterns

*Methodology MD. Drafted 2026-06-15 as a retrospective from the HA-C4b + HA-P7 locking sessions (option-A discipline arc). Companion to [CONVENTIONS.md §1.2](../CONVENTIONS.md#12-reviewer-mode-claude-reads--critiques--explains-does-not-edit-unless-asked) (reviewer-mode-with-authorization) and [reviews/README.md](../reviews/README.md) (audit layer structure). Anchored on what actually worked + what to look for, with worked examples cross-referenced.*

---

## 1. What this MD is, and what it does not

**Is**: a practical how-to for the project's hypothesis-pre-registration cycle — drafting → audit → revision → lock → run. Documents the discipline pattern that emerged from the HA-C4b + HA-P7 sessions and gives sanity-check questions a seasoned researcher should ask before signing a lock.

**Is not**: a methodology MD that locks a specific statistical choice (those live in their own MDs). Not the audit layer spec (that's [reviews/README.md](../reviews/README.md)). Not the reviewer-mode clause itself (that's [CONVENTIONS.md §1.2](../CONVENTIONS.md#12-reviewer-mode-claude-reads--critiques--explains-does-not-edit-unless-asked)).

Applies to: any Claude-drafted reviewer-mode pre-reg (`analyses/hypotheses/HA*-*/hypothesis.md`). Does not bind methodology MD locking (covered by [CONVENTIONS.md §2.2](../CONVENTIONS.md#22-methodology-md-before-locking-a-major-choice) and [`/research-methodology-review`](../../../.claude/commands/research-methodology-review.md)).

---

## 2. The arc (canonical + option-A compression)

For each hypothesis, the **canonical** discipline is: 4 sessions × 5 stages (1 drafting + 2 fresh-session audits + 1 revision + 1 lock). The **option-A compression** collapses the second audit (re-audit r2 before lock) into the lock signal itself — acceptable for the initial-pass discipline work HA-C4b + HA-P7 lived in, not the default for load-bearing claims going forward. The arc is sequential per hypothesis but multiple hypotheses can be at different stages in parallel.

| stage | session type | output | locking signal |
|---|---|---|---|
| **1. Draft** | drafting (may be shared-context with research session) | `hypothesis.md` with `## Authorship` block at top | commit, but NOT a lock signal yet |
| **2. Audit** | **fresh session, no shared drafting context** | `reviews/HA-<id>-<date>.md` (audit report) | n/a |
| **3. Revise (r2)** | shared-context (typically same drafting session continues) | revised `hypothesis.md` (r2) | commit, but NOT a lock signal yet |
| **4. Re-audit (canonical)** | **fresh session, no shared drafting context** | `reviews/HA-<id>-<date>-v2.md` (re-audit report) | n/a |
| **5. Lock** | shared-context | hypothesis.md status: LOCKED + register-row pointer | commit with "LOCKED" status in Authorship + register pointer |

The next stage after lock is the test-execution session (not part of the 5-stage lock arc):

| post-lock | session type | output |
|---|---|---|
| **6. Run** | shared-context test-execution session | `test.py` + `result.md` |

So for N hypotheses, the **canonical arc** is **4N + N sessions** (4 lock-arc + 1 run). The **option-A compression** is **3N + N sessions** (skip step 4 with a documented compression decision per §3.6). HA-C4b and HA-P7 each took ~3 sessions in this thread to reach lock under option-A compression; the canonical 4-session arc is recommended for any subsequent load-bearing pre-reg.

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
   - §8 Caveats result.md must explicitly acknowledge — **MUST include a power-calc dispatch**: either the one-line "power calc inapplicable per Daza 2018 within-subject design — see [Daza 2018 PDF](../../literature/methodology/daza_2018_self_tracked_n_of_1_counterfactual.pdf) for the within-subject counterfactual framing" OR an explicit power calculation with assumptions named (effect size, α, β, n-per-arm). The dispatch is non-optional; the absence of any §8 power-calc line is itself a Layer 1 fire (silent power-calc invokes asymptotic-power assumptions that don't hold at n=1)
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

### 3.5 Revise step (Stage 3 of the arc — r2 — the bulk of methodological strengthening)

The audit's fires drive r2 in the drafting session (shared-context with the original draft is fine here — the audit was the independence step). **All r2 changes must be tracked in the Authorship block** as a separate revision entry.

**The pattern that emerged**:

- **L3.1/L3.4 (autocorrelation in null / CIs)** — almost always fires on the first audit. Fix: cite and adopt [`methodology/permutation_null_block_length.md`](permutation_null_block_length.md) — stationary bootstrap with `E[L] = 7` days + block-permutation null with the same E[L] policy + data-driven `E[L]*` companion + factor-of-2 flag. **Both HA-C4b and HA-P7 had this fire.** The HA-family null-machinery inheritance predates the canonical MD; new pre-regs adopt the canonical default.

- **L3.3 (multi-comparison discipline implicit)** — almost always fires when the falsification bar reports multiple cells. Fix: **single-cell headline lock** — pre-specify ONE cell as the SUPPORTED-bar-driving combination; all other arms are diagnostic / sensitivity ONLY (no independent SUPPORTED bar). **Both HA-C4b and HA-P7 had this fire.**

- **L4.4 (CONVENTIONS §3.4 crash-drop sensitivity)** — typically fires when a same-day correlation is reported. Fix: either add the sensitivity row (ρ with `is_crash == True` dropped, `|Δρ| > 0.10` flagged) OR explicitly dispatch §3.4 as inapplicable-by-construction (when the outcome IS `is_crash`, dropping crash rows eliminates the positive cases).

- **L4.3 (CONVENTIONS §3.3 column-duplication)** — fires when sensitivity ladders include near-identical columns. Fix: mark identical-by-construction columns explicitly in the table; they emit to the CSV for completeness but are NOT counted as independent sensitivity arms.

- **L4.6 (CONVENTIONS §3.6 named-counts triplet)** — fires when count phrasings lack the predicate + source-file. Fix: add the scheme + unit + source-file in the same phrasing.

- **Side observations** (paths, off-by-ones, date arithmetic, monotonicity tolerance, label ambiguity) — fix opportunistically AND check sibling pre-regs for propagation.

  **Propagation discipline** (added 2026-06-15 from the HA-C4b labels-CSV-path retrospective):
  - **Step 1**: for each side fix in r2, grep the same construct (file path, regex pattern, off-by-one, date arithmetic) across all `analyses/hypotheses/HA-*/hypothesis.md` siblings.
  - **Step 2 — sibling unlocked**: fix in the same r2 commit. Commit message names the propagation explicitly (e.g. `"Side-fix: labels CSV path corrected in HA-C4b + HA-P7 (caught in HA-P7 audit, propagated to sibling)"`).
  - **Step 3 — sibling locked**: pick one of:
    - **(a) Same-session v2** — open v2 of the sibling in the same drafting session, separate commit. Preferred when the side fix is unambiguous (e.g. broken file path).
    - **(b) Tracked queue** — add a TODO marker in the sibling's `## Authorship` block under a `### Pending v2 fixes` heading with the source (which audit / which date), AND record the queue entry in this MD's §8 follow-ups list with a date.
  - **Step 4 — never defer silently**. Silent deferral is how the HA-C4b labels CSV path bug propagated past the lock window without any audit-able trace. The Authorship block is the audit-able record.

### 3.6 Re-audit step (Stage 4 of the arc — canonical, can be compressed)

After r2 closes the first audit's fires, the **canonical** lock arc adds a second audit in a **fresh session** before lock. This verifies that r2 actually closed the fires (rather than merely paraphrasing them) and catches issues that r2 may have introduced. The HA-C4b + HA-P7 initial pass compressed this step; the §8 retrospective concluded the compression was acceptable for option-A but not the canonical default.

**To trigger** (paste into a fresh Claude session):

> Run `/research-review` on `docs/research/analyses/hypotheses/HA-<id>/hypothesis.md` at revision r2. This is a **second-pass audit** on a revised Claude-drafted pre-reg under reviewer-mode-with-authorization per CONVENTIONS §1.2; produce the review report at `docs/research/reviews/HA-<id>-<date>-v2.md` with the addendum "Fresh session, second-pass audit on revision r2; doc-only knowledge; verifying r2 closed the fires from `reviews/HA-<id>-<original-date>.md`."

**Expected outcomes**:

- **No new fires + r2 closures verified** → proceed to §3.7 (optional r3) or §3.8 lock.
- **New fires (r2 introduced something) + r2 closures verified** → r4 to close, then re-audit again. The cycle continues until clean.
- **r2 closures NOT verified** → either r2 didn't actually close the fire, OR the r2 closure introduced a different fire pattern. Back to §3.5 with explicit notes in the Authorship block describing what the second-pass audit caught.

**Compression option** (used in option-A initial pass for HA-C4b + HA-P7): skip the re-audit, go straight to lock. **Acceptable for**:

- Pre-regs whose r2 fixes were mechanical (citation additions, single-cell-lock decision, column-list edits) with no architectural change.
- Low-stakes pre-regs where the v1 result will be treated as descriptive-only.
- Initial-pass discipline work (the option-A pattern) where the lock-process itself is being developed.

**NOT acceptable for**:

- Load-bearing project claims (crash-predictor architectures, mechanism-of-action claims).
- r2 that introduces new statistical machinery (e.g. swap of inference method, new transformation of the predictor).
- r2 that changes the falsification bar.

When compressing, the lock-commit message MUST include a one-line compression justification: `Compression: re-audit skipped per §3.6 acceptability criteria — <one-sentence reason naming which criterion>.` This makes the compression decision audit-able and recoverable later.

### 3.7 Optional r3 (interpretability augmentation)

After r2 (and re-audit, if not compressed) closes the audit fires, the user may ask for additional reporting that doesn't change the falsification bar but improves external interpretability. **Heuristic for "approach change vs reporting layer"**:

- **Approach change**: new conjunct in the falsification bar, new covariate that changes the headline, new statistical machinery (e.g. switching from logistic to ITS). These require a new audit gate (back to §3.4 + §3.6).
- **Reporting layer** (no approach change): different formulation of an already-locked quantity, additional sensitivity arm that does NOT promote to SUPPORTED, descriptive companion output. These do NOT require a new audit gate.

**Example from this thread**: HA-C4b's r3 added Odds Ratio (OR) + Risk Difference (RD) with bootstrap CIs alongside the existing 15pp RD gate. The (a)+(b)+(c) falsification bar was unchanged; the OR was a more interpretable formulation of the existing (b) discrimination. **Reporting layer, not approach change.** No new audit gate needed.

### 3.8 Lock step (Stage 5 of the arc)

**Lock signal**: explicit user acceptance + a commit message naming the lock + the Authorship block status updated to `**Status: LOCKED <date> by user acceptance.**`

**The lock commit's message** should:

- Name the revision number being locked (r2, r3, etc.).
- Confirm all audit fires are closed (or explicitly note any deferred to v2 with TODO markers per §3.5 propagation discipline).
- State whether the canonical re-audit (§3.6) was completed OR was compressed with the one-line justification per §3.6.
- State the next session writes `test.py` + runs + emits `result.md`.

**Register-row pointer update** (added 2026-06-15 from the HA-P7 register-staleness retrospective): if the pre-reg supersedes the register entry that spawned it (e.g. eligibility revision, predictor refinement, outcome reframe), the lock-step is NOT complete until the register row is updated. Two acceptable patterns:

- **(a) Inline pointer (preferred)**: in the same lock commit, edit the register row in [`personal_hypotheses.md`](../personal_hypotheses.md) (P-entry) or [`wiggers_testable_hypotheses.md`](../wiggers_testable_hypotheses.md) (Wiggers entry) to add a `→ superseded by: see [HA-<id>/hypothesis.md](analyses/hypotheses/HA-<id>/hypothesis.md) r<N> locked <date>` forward pointer. The register entry text itself stays (it's the historical genesis), but the pointer makes the supersession discoverable to future sessions.
- **(b) Companion commit**: same-session, separate commit, explicitly named (`"Register-row pointer: P7 → HA-P7 r2 locked"`). Acceptable when the register update needs more than a single-line pointer (e.g. summarising the revision rationale alongside the pointer).

**Not acceptable**: silent supersession (locking the pre-reg without touching the register entry). This is how HA-P7's eligibility revision left [`personal_hypotheses.md`](../personal_hypotheses.md) P7 stale post-lock.

**Lock-commit confirmation gates** (the four items the lock commit message MUST explicitly confirm; other §5 conditions are verified by the audit step at §3.4/§3.6 and need not re-appear in the commit message):

1. Power-calc dispatch present in §8 (per §3.2 step 4) — confirm dispatch type used.
2. Single-cell headline lock OR explicit Bonferroni-style correction (per §4.2) — confirm which.
3. Register-row pointer updated OR explicit non-supersession confirmation (per the register-row sub-section above).
4. Re-audit completed clean OR compression decision documented per §3.6 — confirm which.

If any of the four is unmet, the lock signal is not given.

**After lock**: further modifications create v2 with v1 archived per the project's locked-pre-reg discipline. **The v1 result (if it lands first) is the canonical citation**; any subsequent v2 result is reported as a separate verdict with its own audit lineage.

### 3.9 Run step (post-lock)

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

### 4.6 Result-time — rolling-sum predictor structural autocorrelation factor-of-2 flag

**Fires when**:
- Predictor is a rolling sum / count over a non-trivial window W (e.g. `crash_count_Wd`, `push_burden_Wd`, `exertion_dose_Wd`).
- Locked test.py emits a data-driven `E[L]*` (per [`permutation_null_block_length.md`](permutation_null_block_length.md) §2) at >= 2x the locked `E[L]` default (factor-of-2 flag fires post-result).

**Why it's almost always fired on rolling-sum predictors**: the lag-1 autocorrelation of a rolling sum at window W approaches `(W-1)/W` by construction (consecutive days share `(W-1)/W` of their input days). The data-driven estimator recovers this structural autocorrelation, not a sampling artefact. For W = 14, expect `E[L]*` ~ 12 (HA-P7 observed); for W = 7, expect `E[L]*` ~ 6. Any rolling-sum predictor at W >= 10 is likely to trip the factor-of-2 flag.

**Closure** — post-result verdict-review document per the [HA-P7 `verdict-review.md`](../analyses/hypotheses/HA-P7/verdict-review.md) template:
- (a) Cite the structural rolling-sum explanation for the `E[L]*` divergence (the data-driven estimator is doing its job correctly; the locked `E[L] = 7` anchor targets day-level autocorrelation of raw series, not rolling-sum predictors).
- (b) Run a sensitivity addendum (per [`HA-P7/sensitivity_block_length.py`](../analyses/hypotheses/HA-P7/sensitivity_block_length.py)) at `E[L]` in {locked, `E[L]*`-rounded, 2x locked}; report OR / CI / p-value at each.
- (c) Verify whether any §5 falsification criterion (or §9 propagation trigger) flips at longer `E[L]`. If not, the verdict locks as-is at locked `E[L]`. The OR point is invariant to `E[L]` by MLE construction; CIs drift modestly; permutation p-values increase monotonically with `E[L]` (the theoretically-predicted direction — more autocorrelation in null → wider null distribution → more conservative p). Verdict robustness is the load-bearing read.
- (d) `result.md` preserved verbatim; the review document is the audit trail.

**Anticipatory drafting note**: pre-regs using a rolling-sum predictor should anticipate this flag at drafting — name it in §8 as a foreseen review trigger, not an unexpected event. HA-P7 §8 did NOT anticipate the rolling-sum `E[L]*` flag; the [`verdict-review.md`](../analyses/hypotheses/HA-P7/verdict-review.md) was the workaround. Future pre-regs of this class should pre-emptively cite §4.6 + the verdict-review closure template in their §8.

---

## 5. Sanity-check questions before lock

A seasoned researcher (or a strict re-auditor) should ask these. If the pre-reg can answer "yes" or "explicitly dispatched", it's ready for lock. The `lock-blocking?` column marks every row that must pass before the lock signal is given; the **bolded `yes (§3.8 gate N)`** rows additionally require explicit confirmation in the lock-commit message per §3.8.

| sanity check | applies to | pass condition | lock-blocking? |
|---|---|---|---|
| Is block-aware inference applied? | any test on time-series data | stationary bootstrap E[L]=7 + block-permutation null cited & applied | yes |
| Is the headline cell unique and pre-specified? | any test with multiple sensitivity arms | single-cell §5.0 lock OR explicit Bonferroni correction | **yes (§3.8 gate 2)** |
| Is causal-attribution ambiguity surfaced if applicable? | any test where multiple causal stories fit | §8 caveat explicit + §9 outcome branching surfaces alternatives | yes |
| Are effect sizes in community-standard formulation? | any inferential test | OR / RD / Cohen's d / Hedges' g reported with CIs | yes |
| Is the §8 power-calc dispatch present? | every pre-reg | one of: explicit calc with assumptions named, OR the one-line "power calc inapplicable per Daza 2018 within-subject design" dispatch | **yes (§3.8 gate 1)** |
| Are §3.4 / §3.7 / project audit hooks engaged or explicitly dispatched? | any Layer 4+ analysis | one of: applied, OR explicit one-sentence dispatch | yes |
| Is the eligibility rule self-consistent? | any pre-reg with eligibility + outcome | rule does NOT exclude every possible positive outcome (the contradiction P7's audit caught) | yes |
| Are FIT files / CSV paths verified? | any pre-reg citing source files | path exists in the audit-able tree OR is documented as external | yes |
| Does the §9 branching enumerate all outcome paths? | every pre-reg | {SUPPORTED both, train-only, validate-only, refuted both, inconclusive, dry-run-fails, sensitivity-arm-diverges} all have explicit pre-spec | yes |
| Does the §10 run protocol include a dry-run halt? | every pre-reg | "If sanity check fails → halt + revise spec → v2" | yes |
| Is the canonical re-audit (§3.6) clean OR compressed with documented justification? | every pre-reg pre-lock | one of: r2 re-audit completed with no fires + r2-closure verified, OR the lock-commit message includes the one-line `Compression: re-audit skipped per §3.6 acceptability criteria — <reason>` | **yes (§3.8 gate 4)** |
| Is the register row updated (pointer or non-supersession confirmation)? | every pre-reg that may supersede its register entry | one of: register row has a `→ superseded by: HA-<id> r<N> locked <date>` forward pointer (preferred), OR the lock-commit message explicitly confirms non-supersession | **yes (§3.8 gate 3)** |
| Has a side-fix propagation check been done across siblings? | every r2 that includes side observations | for each side fix in r2, a grep across `analyses/hypotheses/HA-*/hypothesis.md` confirms either no sibling carries the same construct, OR siblings carrying it have been fixed (unlocked) / v2-queued (locked) per §3.5 propagation discipline | yes |
| Are §7 sanity ranges anchored to the EXACT column being measured? | every pre-reg with a §7 anchor range | §7 ranges cite the descriptive card / `per_day_master.csv` statistic for the exact column under test (not a definitional cousin); the cited median / IQR is reproducible from a single script run against that column. **Rationale**: HA-C4b v1 locked an anchor range of [15, 60] for `stress_low_motion_min_count_S60_Mlow` derived from a definitional cousin's distribution; the actual column's unmedicated median was 78, tripping the §7 sanity gate at dry-run and forcing v2. The right check at lock-time would have been "anchor against this exact column's descriptive card." | yes |
| Is the locked headline cell populatable across train AND validate eras? | every pre-reg with a both-eras headline lock + phase / eligibility / temporal stratification | the locked cell (phase x era x sensitivity-column x window) is verified at lock-time to have non-empty n on BOTH train and validate eras given the train/validate split + phase boundaries + eligibility rules — a 30-second arithmetic check is sufficient. **Rationale**: HA-C4b v1 locked a consolidation x train headline cell that was unsatisfiable by construction (consolidation phase starts 2024-06-20; train ends 2023-12-31 — zero overlap). The structural hole was caught at `--dry-run` instead of at lock, forcing a v2 redraft post-lock. | yes |
| Is every category enumeration in the pre-reg algorithmically pre-spec'd? | every pre-reg with a category enumeration (shape classifiers in §4.8.x, status enums, outcome-shape labels in §9) | EVERY member of the enumeration has an algorithmic / operational pre-spec sufficient for reproducible classification from doc-only knowledge; not just the trivial / fallback / negative case. **Rationale**: HA-P6 r1 §4.8.3 enumerated 6 shape categories but only pre-spec'd `no-meaningful-change`; the remaining 5 (`monotonic-recovery`, `stair-step-recovery`, `overshoot-then-settle`, `slow-grind-incomplete`, `noisy-inconclusive`) had no operational definition, preventing reproducible `result.md` classification per the §9 downstream propagations. Closure in r2: full algorithmic pre-specs for all 6 in priority order with first-match wins. | yes |
| Are all natural-language trigger phrases in §9 bound to specific operational machinery? | every pre-reg with §9 branching triggered by phrases like "differs in shape", "statistically-distinguishable", "matches matched-baseline", "survives detrending" | each natural-language trigger phrase in §9 is explicitly bound to specific CI machinery / threshold / operational criteria from §4 (e.g. "CI on median-difference excludes 0 on >= N of M days"; "block-permutation p < α"; "absolute z >= K SD"); the binding is reproducible from doc-only knowledge. **Rationale**: HA-P6 r1 §9 first-branch trigger "statistically-distinguishable median trajectory from matched control" was not bound to the §4.8.1 CI machinery — multiple plausible operationalisations existed (CI-non-overlap; CI excludes 0 on the difference; block-permutation p < α); result.md could not reproducibly fire one branch over another. Closure in r2: §9 head paragraph binds the trigger to per-day block-bootstrap CI on median-difference excludes 0 on >= 2 of 5 days. | yes |

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

**Drafted 2026-06-15** (v1) from the HA-C4b + HA-P7 retrospective. **Revised 2026-06-15 (v1.1)** to close the four §8 follow-ups identified in v1's retrospective. **Revised 2026-06-15 (v1.2)** to add four lessons from the HA-C4b run halt + HA-P6 audit closures + HA-P7 verdict review (see §8.4). Working document — extend as the lock pattern evolves with subsequent pre-regs.

### 8.1 v1.1 closures (2026-06-15)

The four v1 §8 follow-ups are closed in this revision:

- **Power-calc dispatch added to the §3.2 drafting checklist** — closed. The §8 line in the pre-reg's section list now mandates a power-calc dispatch (explicit calc OR the one-line "power calc inapplicable per Daza 2018 within-subject design" dispatch); absence of the dispatch is itself a Layer 1 fire. §5 carries a lock-blocking sanity-check row for this; §3.8 marks it as gate 1 of the lock-blocking checklist.
- **Re-audit-r2-before-lock as canonical pattern** — closed. New §3.6 documents the second-pass-audit step in a fresh session with `/research-review` on r2 (report at `reviews/HA-<id>-<date>-v2.md`). §2 reframes the arc as 4 canonical sessions × 5 stages, with the option-A compression (skip step 4) acceptable for mechanical r2 fixes / low-stakes pre-regs / initial-pass discipline work. Compression decisions must be documented in the lock-commit message. §5 carries a lock-blocking row; §3.8 marks it as gate 4.
- **Side-fix auto-propagation discipline** — closed. §3.5's side-observation bullet now mandates a sibling-grep step + per-status (unlocked / locked) propagation procedure + an explicit "never defer silently" clause. Sibling fixes go in the same r2 commit if unlocked; v2 commit if locked. §5 carries a sanity-check row for the propagation grep.
- **Register-row pointer update as a lock-step requirement** — closed. New §3.8 sub-section on register-row pointers documents two acceptable patterns (inline pointer or companion commit) + an explicit non-acceptance clause for silent supersession. §5 carries a lock-blocking row; §3.8 marks it as gate 3.

### 8.2 v1.1 lock-blocking gates (§3.8 summary)

The lock signal is not given until all four gates pass:

1. Power-calc dispatch present in §8.
2. Single-cell headline lock OR Bonferroni correction.
3. Register-row pointer updated OR explicit non-supersession confirmation.
4. Re-audit completed clean OR compression decision documented.

### 8.3 Open follow-ups (post-v1.1)

The following are queued for a later revision; not in scope for v1.1:

- **[CLOSED 2026-06-15-c] HA-C4b labels CSV path propagation — absorbed by v2 drafting** — context shifted between v1.1 drafting and §8.3 closure: HA-C4b v1 was archived at commit `cf3cafa` (halted at dry-run for unrelated reasons — n-threshold fail + §7 calibration miss), so a v2 redraft is now required regardless of the labels CSV path side fix. Rather than retro-fixing v1-archived (which would violate the locked-pre-reg discipline) or opening a standalone v2 for the labels CSV path alone (now redundant), the fix was added to [`HA-C4b/README.md`](../analyses/hypotheses/HA-C4b/README.md) "v2 must-inherit fixes" list alongside the §7 calibration-anchor fix. The next HA-C4b v2 drafting session will pick up both fixes from the README in its §3.2.1 "read register entry + cited sources" step. **First worked example of §3.5 sibling-locked propagation discipline being supplanted by an already-required v2 redraft** — variant on step 3(a) "same-session v2" where the v2 is required for orthogonal reasons and the fix rides along; document this as a fourth option in §3.5 step 3 if it recurs.
- **[CLOSED 2026-06-15-b] Personal register P7 forward pointer** — landed: top-level supersession blockquote added at [`personal_hypotheses.md`](../personal_hypotheses.md) P7 heading + Sample-cell footnote pointing to HA-P7 §4.2. Closes both the v1.1 §3.8 register-row pointer requirement AND the HA-P7 r2 queued Sample-cell pointer fix in one edit. First worked example of the new §3.8 register-row pointer discipline applied retroactively.
- **Audit-MD acceptability bar for the option-A compression record** — the option-A initial pass compressed step 4 without documenting compression decisions in lock-commit messages (because the §3.6 acceptability criteria are new). The HA-C4b and HA-P7 lock commits did NOT cite §3.6 compression criteria; this is a documentation gap, not a methodological one. Acceptable to leave because v1.1 only binds prospectively (future pre-regs); the existing lock commits stand.
- **Reviewer-mode-with-authorization handoff template for fresh-session audits** — the current trigger paragraphs (§3.4 and §3.6) work but could be turned into a slash-command (`/research-audit HA-<id> [--second-pass]`) for ergonomic invocation. Process improvement, not a methodology change.

### 8.4 v1.2 closures (2026-06-15)

v1.2 adds four lessons from the HA-C4b dry-run halt + HA-P6 audit closures + HA-P7 verdict review:

- **§5 row added — structural-completeness check across train/validate eras**. Closes the HA-C4b v1 structural-hole lesson: the locked headline cell `consolidation x train` was unsatisfiable by phase-boundary construction (consolidation starts 2024-06-20; train ends 2023-12-31; zero overlap). The structural hole would have been caught by a 30-second lock-time arithmetic check; instead it was caught at `--dry-run` post-lock, forcing the v2 redraft. Lock-blocking; not a §3.8 gate (caught at the §5 sanity-check pass).
- **§5 row added — enumeration-completeness rule**. Closes the HA-P6 r1 §4.8.3 lesson: 6 shape categories were enumerated but only 1 (`no-meaningful-change`) was algorithmically pre-spec'd; the other 5 had no operational definition, preventing reproducible `result.md` classification. Generalises to any category enumeration (shape classifiers, status enums, branch labels in §9). Lock-blocking.
- **§5 row added — trigger-phrase binding rule**. Closes the HA-P6 r1 §9 lesson: the natural-language trigger "statistically-distinguishable median trajectory from matched control" was not bound to specific CI machinery from §4.8.1, leaving multiple plausible operationalisations and preventing reproducible branch firing. Generalises to any natural-language trigger phrase in §9 ("differs in shape", "matches matched-baseline", "survives detrending"). Lock-blocking.
- **§4.6 fire pattern added — rolling-sum predictor structural autocorrelation factor-of-2 flag**. Closes the HA-P7 verdict review lesson: rolling-sum predictors (e.g. `crash_count_14d`) structurally exceed the project E[L]=7 anchor by a factor proportional to W; the data-driven `E[L]*` recovers this rolling-sum structure correctly, not a sampling artefact. Result-time fire (not pre-lock); closure pattern cites the HA-P7 `verdict-review.md` template (structural explanation + sensitivity addendum at multiple E[L] + verdict-robustness verification). Drafters of pre-regs using rolling-sum predictors should anticipate the flag in §8 of their draft.

The §3.8 lock-blocking gates remain four (the v1.2 row additions are §5 sanity-check rows, not §3.8 gates — they are caught at the §5 pass which is a precondition to the §3.8 commit-message confirmations).

### 8.5 Open follow-ups (post-v1.2)

The following are queued for a later revision; not in scope for v1.2:

- **Methodology MD `permutation_null_block_length.md` §2 rolling-sum exception note** — the HA-P7 verdict review surfaced that rolling-sum predictors structurally exceed E[L]=7. The methodology MD's §2 should acknowledge this as a class-of-predictor exception with the factor-of-2 flag as expected behaviour rather than a halt signal. Queued for the next methodology MD touch.
- **§4.6 fire pattern → §8 drafting checklist integration** — §4.6 says drafters using rolling-sum predictors should anticipate the flag in §8 of their draft. A natural next step is adding this to the §3.2 drafting checklist as a conditional bullet (if predictor is a rolling sum, §8 must include the anticipation note). Deferred until the next pre-reg with a rolling-sum predictor enters drafting.
