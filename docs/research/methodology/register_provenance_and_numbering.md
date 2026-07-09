# Register provenance & numbering — the Guide/Beyond split and its id discipline

*Methodology MD. Drafted 2026-07-08 to lock a structural (registry-organisation) choice, not a statistical one, per [CONVENTIONS §2.2](../CONVENTIONS.md#22-methodology-md-before-locking-a-major-choice). It formalises the split that already half-exists across two register files ([`personal_hypotheses.md`](../personal_hypotheses.md), [`wiggers_testable_hypotheses.md`](../wiggers_testable_hypotheses.md)) and the provenance-aware view in [STOCKTAKE §2a](../STOCKTAKE.md), and pins the numbering rules that keep the P#, HA-*, R#, and site-slug vocabularies from drifting into each other. Companion to [`hypothesis_lock_process.md`](hypothesis_lock_process.md) (which already binds the register-row pointer at §3.1 + §3.8). Motivated by site request R36 in [`research-requests.md`](../../../wiggers_research_story/site/docs/research-requests.md) ("reconcile the P-register + export it as a status list").*

**Status: LOCKED r3 — 2026-07-09 by user acceptance.** Drafted 2026-07-08; r2 + r3 closed two fresh-session `/research-methodology-review` passes ([r1 review](../reviews/methodology-register_provenance_and_numbering-2026-07-08.md), [r2 review](../reviews/methodology-register_provenance_and_numbering-2026-07-09-v2.md)); locked at r3 per the r2 review's clear-to-lock-after-L2.4-fix verdict. Phase-1/2/3 application work is now unblocked. **§8 illustrative-example erratum applied 2026-07-09** (post-Phase-1; no rule change). See §11 for the revision + lock log.

---

## 1. What this MD is, and what it does not

**Is**: the binding rule-set for (a) which of the subject's testable hypotheses live in the **Guide** ledger vs the **Beyond** ledger, (b) how each is numbered, and (c) how the four id vocabularies in play — backend thread ids, test ids, site slugs, site request ids — map onto one another coherently. It exists so a future session can add a hypothesis to the right register with the right id without re-deriving the split each time.

**Is not**: a statistical-methodology MD (it locks no inference choice). Not the hypothesis lock arc — that is [`hypothesis_lock_process.md`](hypothesis_lock_process.md). Not the reviewer-mode clause — that is [CONVENTIONS §1.2](../CONVENTIONS.md#12-reviewer-mode-claude-reads--critiques--explains-does-not-edit-unless-asked). Not the site's editorial layer model — that lives in the site repo's `docs/site-architecture.md`.

Applies to: [`personal_hypotheses.md`](../personal_hypotheses.md) (Beyond), [`wiggers_testable_hypotheses.md`](../wiggers_testable_hypotheses.md) (Guide), [`analyses/hypotheses/registry.md`](../analyses/hypotheses/registry.md) (the test index), [STOCKTAKE §2a](../STOCKTAKE.md) (the register-only view), and any producer-mode export that projects these to the site.

---

## 2. The split: one axis — authorship of the tested hypothesis

The split has **one axis**: *whose hypothesis is being tested against the subject's corpus.* Not scorecard status, not "did we run an inferential test", not settledness. Authorship.

- **Guide ledger** — [`wiggers_testable_hypotheses.md`](../wiggers_testable_hypotheses.md). Hypotheses that test **Laure Wiggers' own claims at her own operationalisation** (the smartwatch-pacing handleiding, 07-2025). Indexed by her source-PDF section: `A1`–`A3`, `B1`–`B5`, `C1`–`C5`, `D1`–`D5`, `E1`–`E3`, `F1`–`F4`, plus the later `G`/`H`/`I`/`J` families.
- **Beyond ledger** — [`personal_hypotheses.md`](../personal_hypotheses.md). Hypotheses the **subject authored** — from lived experience, from general (non-Wiggers) literature, from mechanistic reasoning about the device, **or as a *distinct* extension of a Wiggers idea (a claim she does not make)** — but *not* a mere operational refinement of one of her claims (that stays in the Guide ledger, §2.1). Indexed `P1`, `P2`, …

### 2.1 The membership test (the load-bearing rule)

For any testable hypothesis, ask: **is the tested prediction a theoretical claim distinct from Wiggers', or an operational refinement of her same claim?**

- **The tested claim is Wiggers' → Guide** (a Wiggers claim code). Two recorded ways a thread lands here — keep them distinct:
  - *Prior-authorship is Wiggers'.* The subject's motivation, on inspection, is retrospective felt-recognition of a pattern Wiggers describes — a literature-prior + on-corpus-test shape — not an independent lived-experience-protocol prior. **P3 → Wiggers A4** is this case ("that's a Wiggers-test shape, not a Personal-register shape").
  - *Operational refinement.* The claim is Wiggers'; the subject added an operationalisation detail (a motion filter to reject motion-artefact minutes; a sensor choice) that sharpens *her* claim without making a new one. **P5a → Wiggers C4b** is this case. The subject's contribution is named in the entry's prior-sources, but the entry sits in Guide.
- **The tested claim is a distinct one the subject authored → Beyond** (a P#). A prediction Wiggers does not make, resting on an independent subject prior (lived-experience-protocol, mechanism, or general non-Wiggers literature): a different scope (the *prevailing* rather than post-exertion form), a different mechanism, a confound she does not name, or a pattern outside her guide entirely.

The subject supplying the operationalisation does **not** by itself move an entry to Beyond; a great deal of operationalisation work sharpens Wiggers' own claims without displacing them. What moves an entry to Beyond is the tested prediction being a *distinct theoretical claim.* This is the rule the subject already applied, by hand, on 2026-06-14: P5a (post-exertion rest-stress + motion filter) was routed to Wiggers C4b because "the motion filter is an operational refinement on the same shape, not a distinct theoretical claim," while P5b (the *prevailing* form with evening amplification) stayed in Beyond because it "genuinely extends beyond Wiggers' C4." This MD codifies that call; it does not invent a new one.

**Standing routing decisions are authoritative.** Where a thread has already been routed by user direction and/or has an executed test under one provenance (C4b / `HA-C4b`), this MD's rule does not silently re-route it. The rule governs new mintings and unrouted threads; a change to a standing routing is a user decision, disclosed and made explicitly, never a side effect of applying these conventions.

### 2.2 Cross-attribution for shared-lineage threads

Two mechanisms record shared Wiggers↔subject lineage, depending on which way the membership test (§2.1) lands:

- **Claim-is-Wiggers' → Guide, with the subject contribution named.** When the membership test lands on either Guide sub-case (§2.1), the thread lives in the Guide ledger under her claim code, and the entry names the subject's contribution explicitly. The two current `ROUTED to Wiggers` entries route for the two *different* rationales §2.1 distinguishes — do not lump them:
  - **P5a → Wiggers C4b** (operational refinement): C4b's entry records "the Wiggers prior is C4's; the motion filter is the participant's contribution." The participant contribution is cited in C4b's prior-sources; the entry sits in Guide because the tested claim is C4.
  - **P3 → Wiggers A4** (prior-authorship): P3's routing reason is that its lived-experience component is "retrospective felt-recognition of the pattern Wiggers describes, not an active-monitoring prior — a Wiggers-test shape, not a Personal-register shape." It is *not* an operational refinement; the routing turns on whose prior it is. (A separate refinement of A4's threshold bands is offered in P3's entry, but that is surfaced for user decision, not the routing reason.)
- **Distinct extension → Beyond, with a reciprocal Guide pointer.** When the test is a distinct theoretical claim built on a Wiggers idea, it lives in Beyond as a P#, names its Wiggers antecedent (*"extends Wiggers `<claim code>` — she claims X; this tests the distinct prediction Y she does not make"*), and the Guide entry carries a reciprocal *"subject extension: see `P#`"* pointer. P5b is the worked case: prevailing rest-stress with evening amplification, kept in Beyond because the scope genuinely extends past C4.

Either way the entry sits where the *tested claim* originated; the cross-reference records the shared lineage without duplicating the entry.

### 2.3 The external-comparator register is outside the binary

[`founderandthecity_testable_hypotheses.md`](../founderandthecity_testable_hypotheses.md) (FC-H# within-person tests mining the population-scale Welltory dataset) is **neither Guide nor Beyond**. It is an external-comparator register that informs Stage S₂ contextualisation, not the subject's own n-of-1 testable registers. It is tagged `external-comparator` (§3) and cross-referenced, but it does not take P# ids and does not project to either site ledger. Keeping it out of the binary preserves the honesty of the Guide/Beyond distinction (both of those are *the subject's body against a hypothesis*; FC is a *population against a hypothesis*).

---

## 3. Provenance tagging at the test layer

The register split lives at the **idea** layer (two register files). It must also be queryable at the **test** layer, where verdicts live, so "list every beyond-the-guide test" is a grep rather than a memory exercise.

Every row in [`registry.md`](../analyses/hypotheses/registry.md) carries a `register:` field with one of:

| Value | Meaning | Site projection |
|---|---|---|
| `wiggers:<claim>` | tests a Wiggers claim at her operationalisation (incl. operational refinements like C4b) | `guide-ledger.json` (Layer 4) + scorecard where applicable; **also** `addendum-register.json` as `provenance: guide-extension` where the site editorially surfaces the participant refinement on `/beyond` |
| `beyond:<P#>` | tests a subject-authored hypothesis | `addendum-register.json` (Layer 4, `provenance: beyond`) + `/beyond` where surfaced |
| `foundational` | the pre-split precursor batch (H01–H05, K01–K02) — motivated by general pacing literature (Workwell RHR+15, etc.) before either register existed | Layer 4 workings / ledger; neither `/guide` nor `/beyond` |
| `methodological` | tests about the instrument or method, not the body (data-quality `I`-family, archived stabilisation `S`-family) | Layer 4 workings only |
| `external-comparator` | reserved for FC-H# tests once they dispatch | `/reading` + Stage S₂ contextualisation; neither subject ledger |

**Projection rule (the site-inheritance operationalisation).** The site is the patient-audience track of the framework's Stage T; it *inherits* this split, it does not reinvent it. Concretely: `addendum-register.json` is the projection of all `beyond:*`-tagged threads (`provenance: beyond`) **plus** the small set of `wiggers:*` threads the site editorially surfaces on `/beyond` as participant refinements (`provenance: guide-extension`, e.g. C4b); `guide-ledger.json` is the projection of all `wiggers:*` (the exhaustive Guide accounting, C4b included). The per-item `provenance` field keeps the two apart honestly, so a reader can tell a subject-authored thread from an editorially-surfaced Guide refinement. `foundational` / `methodological` / `external-comparator` surface at Layer 4 workings, in neither subject ledger. So the two backend ledgers and the two site ledgers are symmetric:

```
Layer 2 hub (curated):       guide.json         ↔  addendum.json
Layer 4 ledger (exhaustive): guide-ledger.json  ↔  addendum-register.json   ← R36-B target
Test index (provenance):     registry.md  ── register: tag on every row ──┘
```

**Note on the `foundational` batch.** Assigning `foundational` vs `beyond:<P#>` to H01–H05 / K01–K02 is a per-row curation judgment (several were lived-experience-adjacent). The default is `foundational` — they predate both registers and were driven by general pacing literature, not by a Wiggers claim or a distinct subject-authored prior. Any row a curator judges to be genuinely subject-authored gets a P# and `beyond:<P#>` instead. This curation happens when the tag field is added (the register-tagging phase), not in this MD.

---

## 4. Numbering & id coherence

Four vocabularies describe "beyond" things in different layers; without a discipline they conflate. (They already have: R36's own summary lists the P-register as "P1, P2, P3, P6, P7", silently dropping the P4a/P4b/P5b entries that exist — a live symptom of the drift this section prevents.)

**Rule 1 — `P#` is the canonical Beyond-thread id.** One subject-authored thread = one P-entry. New threads take the next free integer (`P8`, `P9`, …). Sub-letters (`P4a`/`P4b`) denote one thread at two operationalisations and are the established precedent for that case. P# is minted **only** for Beyond threads; a Wiggers claim never receives a P#.

**Rule 2 — each P-entry declares a stable slug, which is the site's id.** The site speaks kebab-case slugs (`after-the-crash`, `rest-stress-low-motion`), not P#; it references backend test ids only inside `ha_ids` arrays. So each P-entry declares one stable slug that **is** the site's `addendum-register.json` item id, aligned to any slug already shipping in the site's `addendum.json` for that thread. The slug — not P# — is the backend↔site join key. This respects the site's existing vocabulary instead of forcing P# onto it.

**Rule 3 — `ROUTED` / dual-attribution is the only cross-split mechanism** (§2.2). No new relocation vocabulary is introduced.

**Rule 4 — every P-entry carries a crosswalk block.** This is the single place the four vocabularies meet:

```
Crosswalk
- Thread id (backend):  P#
- Site slug (site id):  <kebab-case>
- Test id(s):           HA-P#, HA-C#, K#, …  (or "none — register-only")
- Site claim key:       <claims.json id>     (or "none")
- Site request(s):      R#                    (or "none")
- addendum-register id: = site slug
```

The mapping is not always 1:1, which is exactly why the block earns its place: one site slug may bundle two P-entries (`after-the-crash` ↔ P6 + P7), and one thread may surface as two site items (an observation and its scoped test). The crosswalk block absorbs these many-to-one cases explicitly rather than leaving them implicit.

**Rule 5 — `registry.md` carries the `register:` provenance field** (§3) on every test row, so the split is queryable where verdicts live.

**Rule 6 — `kind × stage` is derived from backend state, never hand-set** (§5). The export cannot then disagree with the ledger.

---

## 5. The `kind × stage` status model

The site register (R36-B) presents each Beyond thread on two orthogonal axes. Both are **derived** from backend state, not authored independently.

- **`kind`** — `descriptive` · `tested` · `both`. From whether the thread carries an inferential HA-* test (`tested`), a descriptive characterisation only (`descriptive`), or both.
- **`stage`** — pipeline position, **not** a verdict:

| `stage` | Backend state that produces it |
|---|---|
| `idea` | register-only, or an operationalisation is proposed/designed but no `hypothesis.md` is locked |
| `scoped` | `hypothesis.md` locked, not yet run |
| `done` | `result.md` landed **or** descriptively characterised |
| `inconclusive` | ran, could not resolve (e.g. an n-below-floor cell) |
| `parked` | deliberately held — narrative-only, gated, or awaiting a pre-registered test |

**Two disciplines the model must encode** (both from R36, both load-bearing):

1. **A `stage` is not a verdict.** `idea`/`scoped`/`parked` describe where a thread sits in the pipeline, not how strong its evidence is. A `done` *tested* item points to its verdict for evidence strength; a `done` *descriptive* item is a finished characterisation with no pass/fail bar.
2. **Descriptive `done` is a finished result, never a lesser "not-yet-tested" state.** A thread that was descriptively confirmed and, by Beyond-register discipline, never given a formal HA (e.g. P1, confirmed at episode-level d = +0.90) is `descriptive / done` — not `tested / idea`. The generator must not render "not yet tested" over a characterised finding. This mirrors the existing narrative-only discipline in the corpus (`DECLINED-NARRATIVE-ONLY`).

---

## 6. Alternatives considered

| Alternative | Why rejected |
|---|---|
| **Scorecard-status split** (Beyond = "off the 7-signal scorecard") | This was the site's *pre-2026-07-08* framing. The site's guide rewrite (`guide-rewrite-extraction-plan.md`, shipped) explicitly demoted the scorecard from organising spine to one bucket, because it "reproduced the crash-prediction over-focus." A scorecard-status split would misfile Wiggers-derived-but-off-scorecard items into Beyond and drift as the scorecard's membership changes. |
| **Dual-axis** (provenance on the backend, scorecard-status on the site, reconciled by a per-item tag) | Rejected as the *primary* axis: the site's 2026-07-08 rewrite moved off scorecard-status onto authorship, so a full second axis is not warranted. But there is a genuine residual — authorship (backend provenance) and editorial surfacing (which site layer shows a thread) do **not** coincide for operational-refinement hybrids: C4b is Guide by provenance yet the site surfaces it on `/beyond` because the refinement is the participant's. The design keeps one *provenance* axis and handles this small residual with a per-item `provenance: guide-extension` tag on the site register (§3), not a full dual-axis with its own id space. An earlier draft of this MD over-claimed that no gap exists; C4b is the live counter-example, and it is handled explicitly rather than denied. |
| **Mint site-only ids** (`item-1..N` in `addendum-register.json`) | Breaks id coherence. The site already speaks kebab-case slugs joined to backend test ids; a parallel numeric id space would be a third thing to keep in sync. Rule 2 (declared slug = site id) reuses the existing vocabulary instead. |
| **Provenance tag on `registry.md` only, no P-register reconciliation** | Leaves the Beyond ledger incomplete (R36-A unmet): several subject-authored threads live only as R-requests / queued items / site copy and would never become first-class, queryable entries. The tag alone makes the split visible but not the ledger authoritative. |

**Chosen**: a single provenance axis (authorship), P#-canonical thread ids with a declared slug as the site join key, dual-attribution for hybrids, a crosswalk block per entry, and a `register:` provenance tag at the test layer. This is the minimal structure that makes the split first-class on the backend *and* keeps the site a clean projection.

---

## 7. Four-input reasoning (CONVENTIONS §2.2)

This is producer-mode registry infrastructure, so the four-input bar applies in the lighter form used for the guide MDs. All four are addressed:

| Input | How it is met |
|---|---|
| **1. Best-practices standards** | Two families. (i) Single-case / n-of-1 reporting standards require the *origin* of each hypothesis be transparent (SCRIBE 2016 participant-as-researcher transparency; CENT 2015 pre-specification reporting) — recording provenance as a first-class, queryable field operationalises that. (ii) Research-data-management practice for the id machinery: FAIR principle **F1** (data assigned globally unique, persistent identifiers) and **authority-control** (one authoritative identifier per entity, aliases cross-referenced) motivate the single-canonical-thread-id (P#) + declared join-key-slug design in §4, with the crosswalk block as the alias record; **PROV**-style explicit lineage motivates the §2.2 cross-references. |
| **2. Established literature** | Cited only where it materially bears on the choice. **CONVENTIONS §4.3** (prior-driven hypotheses are confirmatory; the pre-flight asks *which* prior drove the hypothesis) is the materially exact anchor: the `register:` tag *is* the durable record of which prior — Wiggers' claim vs the subject's lived-experience / mechanism / general literature — drove each thread, exactly the distinction §4.3 says must be recorded. No inference-methodology citation (Daza, Natesan) is invoked — this MD locks no inference choice, and citing them for a numbering convention would be ornamental. |
| **3. Tradeoff vision** | §6 states the alternatives and the dimension weighted: **coherence and honesty over minimal disruption.** The split is kept provenance-pure (one axis, both layers agree) even though a scorecard-status reading would match R36's stale crosswalk more literally, because the pure axis is what stays true as the site evolves and what prevents cross-vocabulary conflation. |
| **4. Research limitations + objectives** | n=1, single subject, observational. The honesty objective the whole research line serves ("weather report, not an alarm"; showing work-in-progress) *depends* on the reader being able to tell what is the subject's own poking-around from what is a test of Wiggers' published guide — the site says so in as many words. The numbering discipline directly serves that: it prevents the conflation already observed (R36's dropped P-entries; C4b and the activity-map mis-filed against their own provenance). |

---

## 8. Worked examples

*Erratum 2026-07-09: this roster was illustrative in r1, written before Phase 1 ran. Phase 1 (the [`personal_hypotheses.md`](../personal_hypotheses.md) reconciliation, 2026-07-09) made the actual calls, and the roster is corrected to match — three r1 guesses were superseded: `what-the-watch-catches` ("Pure Beyond P8" → guide-extension), the strict-§5 relabels of P8/P9 (were tested/scoped/parked → descriptive), and the id assignments. The §2.1 / §4 / §5 rules are unchanged; only these applications moved. See §11 lock log.*

The reconciled Beyond roster, keyed to the live `/beyond` slugs:

- **`after-the-crash`** — bundles **P6** (post-crash recovery *signature*; test `HA-P6`; `descriptive / done`) and **P7** (recovery *debt*; test `HA-P7`, NOT-SUPPORTED; `tested / done`). One site slug, two P-entries — the many-to-one case Rule 4 exists for. `register: beyond:P6` and `beyond:P7` on the two HA rows.
- **`changing-crash`** / **`character-flip`** — **P8** (the changing kind of crash). One thread, two site items: the observation (`changing-crash`, `descriptive / done`, backed by K01 + K02) and its future test (`character-flip`, `idea` — designed but not pre-registered; **not** `scoped`, which per §5 requires a locked `hypothesis.md`). `kind: descriptive` (no HA-P8 locked yet). `register: beyond:P8`.
- **`emotional-trigger`** — **P9** (emotional load as a crash *trigger*). `descriptive / parked` under strict §5 (its only run artefact is a Layer-1 descriptive analysis; no locked HA-P9), held for a pre-registered test. `register: beyond:P9`.
- **`what-the-watch-catches`** — **guide-extension, not a Beyond entry** (decided 2026-07-09). The autonomic-fingerprints work refines Wiggers' mental-PEM concession (a *visibility* claim) at her own operationalisation; the emotional/cognitive decomposition is the subject's lens, but the claim under test is hers (source framing: *"refine[s] Wiggers' mental-PEM concession"*). Per §2.1 a Guide operational-refinement, surfaced on `/beyond` via `provenance: guide-extension`. (r1 illustratively mis-guessed this as "Pure Beyond P8".)
- **`rest-stress-low-motion`** — this is **Wiggers C4b** (executed as test `HA-C4b`), *not* a Beyond entry. Per §2.1 the motion filter is an operational refinement of C4, not a distinct claim, and the subject already routed P5a → C4b on 2026-06-14; §2.2 keeps that standing routing. `register: wiggers:C4b`. The site surfaces it on `/beyond` for editorial salience (the refinement is the participant's), so its `addendum-register.json` item carries `provenance: guide-extension` (§3) — it is **not** re-routed to Beyond and `HA-C4b` is untouched. Its verdict is a live backend fact (the `HA-C4b` register row has moved to a v3 honest-close on the n=9/n=10 cell) — per §5 the site's `/beyond` `inconclusive, n=9` copy must be reconciled to whatever that row currently says, not frozen here; this stale-projection risk is exactly why kind/stage is derived, not hand-set. Stage: `done` (a verdict / honest-close was reached, not a pending idea).
- **`best-in-the-middle`** (activity-conditioning on the C3 stress→fatigue curve, R21 / site `C3 × E`) — **guide-extension, not a Beyond entry** (decided 2026-07-09; r1 left this a pending call). Built directly on her C3 curve + C4 coupling; the activity-conditioning control is the subject's lens on her claim, so per §2.1 a Guide-extension surfaced on `/beyond` via `provenance: guide-extension`.

C4b and the activity-map are the two items R36's starter crosswalk filed under "beyond" while its stated rule said "not Wiggers-derived." §2.1 resolves both as Guide operational-refinements / extensions editorially surfaced on `/beyond` (**not** Beyond mints) — C4b on its standing 2026-06-14 routing, the activity-map by the 2026-07-09 decision.

**Id assignment (actual, post-Phase-1):** P8 = `changing-crash`, P9 = `emotional-trigger`; `what-the-watch-catches`, `best-in-the-middle`, `rest-stress-low-motion` take no P# (guide-extensions). The r1 illustrative ids (P8 = what-the-watch-catches, P9 = changing-crash, P10 = emotional-trigger) are superseded.

---

## 9. How this is applied (and the privacy note)

This MD **locks the rules only.** It is Phase 0 of the R36 work. Applying them is later, gated, work:

1. **Reconcile the Beyond ledger** (`personal_hypotheses.md`): promote each subject-authored thread to a full P-entry, add the crosswalk block + `kind`/`stage` to every entry. This is reviewer-mode content drafted under authorization; it goes to a fresh-session [`/research-review`](../../../.claude/commands/research-review.md) before lock, per [`hypothesis_lock_process.md`](hypothesis_lock_process.md) §3.1 and [CONVENTIONS §1.2](../CONVENTIONS.md#12-reviewer-mode-claude-reads--critiques--explains-does-not-edit-unless-asked).
2. **Tag the test index** (`registry.md` `register:` field); reconcile [STOCKTAKE §2a](../STOCKTAKE.md).
3. **Generate the export** (`addendum-register.json`) as a producer-mode projection of the `beyond:*` threads.

**Privacy.** The export is titles + `kind` + `stage` + a one-line note per thread — no dated raw values, no per-day data. It is answerable entirely in the label/aggregate layer and passes [`pipeline/audit_for_publication.py`](../pipeline/audit_for_publication.py) by construction. The mandatory audit-before-push gate ([CONVENTIONS §2.3](../CONVENTIONS.md#23-audit-before-push)) still runs.

---

## 10. Cross-references

- [CONVENTIONS §1.2](../CONVENTIONS.md#12-reviewer-mode-claude-reads--critiques--explains-does-not-edit-unless-asked) — reviewer-mode-with-authorization (governs the Phase-1 ledger reconciliation).
- [CONVENTIONS §2.2](../CONVENTIONS.md#22-methodology-md-before-locking-a-major-choice) — the four-input bar this MD is graded against.
- [CONVENTIONS §2.3](../CONVENTIONS.md#23-audit-before-push) — the privacy gate the export passes through.
- [CONVENTIONS §4.3](../CONVENTIONS.md#43-prior-driven-hypotheses-are-confirmatory-not-exploratory) — the confirmatory-vs-exploratory prior discipline the `register:` tag operationalises.
- [`hypothesis_lock_process.md`](hypothesis_lock_process.md) §3.1 (register-entry-exists pre-step) + §3.8 (register-row pointer discipline) — the existing register↔pre-reg binding this MD extends.
- [`personal_hypotheses.md`](../personal_hypotheses.md) — the Beyond ledger.
- [`wiggers_testable_hypotheses.md`](../wiggers_testable_hypotheses.md) — the Guide ledger.
- [`founderandthecity_testable_hypotheses.md`](../founderandthecity_testable_hypotheses.md) — the external-comparator register.
- [`analyses/hypotheses/registry.md`](../analyses/hypotheses/registry.md) — the test index gaining the `register:` field.
- [STOCKTAKE §2a](../STOCKTAKE.md) — the register-only view this formalises.
- Site: `research-requests.md` R36 (the driving request; specs `addendum-register.json`); `docs/beyond-rewrite-plan.md` (where the `/workings/beyond-the-guide-register` down-link is specced as phase-2); `guide-rewrite-extraction-plan.md` (the scorecard-demotion that made the split canonical); `data/addendum.json` (the shipped `/beyond` slugs Rule 2 aligns to) — all in the `wiggers_research_story` site repo.

---

## 11. Status

**Drafted 2026-07-08 (DRAFT r1).** **Revised 2026-07-09 (DRAFT r2)** to close the fresh-session review [`reviews/methodology-register_provenance_and_numbering-2026-07-08.md`](../reviews/methodology-register_provenance_and_numbering-2026-07-08.md) (verdict DEFENSIBLE-with-revision). r2 closes the two lock-blockers:

- **R1 (Layer 2 provenance)** — the §2.1/§2.2 membership rule is corrected to the *distinct-theoretical-claim vs operational-refinement* axis the subject already applied on 2026-06-14; the false "P5a was Wiggers-native" characterisation is removed; the standing-routing-is-authoritative clause is added; §8 no longer reverses the C4b routing.
- **R2 (§6 tradeoff premise)** — §6 no longer claims the site/backend gap vanished; it names the C4b operational-refinement case as the live residual and the `provenance: guide-extension` tag (§3) as its handling, so §6 and §8 now agree.

r2 also closes the three strengthening items: **I1** (FAIR-F1 / authority-control / PROV anchors added to §7 input 1), **I2** (Daza demoted as ornamental, CONVENTIONS §4.3 centred in §7 input 2), and the side fixes (§10 cross-ref corrected to `beyond-rewrite-plan.md` / R36; §8 illustrative ids marked pending Phase-1 minting).

**Revised 2026-07-09 (DRAFT r3)** to close the second fresh-session review [`reviews/methodology-register_provenance_and_numbering-2026-07-09-v2.md`](../reviews/methodology-register_provenance_and_numbering-2026-07-09-v2.md) (verdict DEFENSIBLE-with-revision; all four r1 items confirmed closed). r3 closes the one fresh minor fire it raised (**L2.4**): the r2 §2.2 rewrite un-lumped P5a but left P3 mischaracterised as an operational-refinement routing, when P3's recorded reason ([`personal_hypotheses.md`](../personal_hypotheses.md) §P3) is *prior-authorship* — retrospective felt-recognition of Wiggers A4, not a refinement. r3 adds the prior-authorship Guide sub-case to the §2.1 test (per the review's Section 4 suggestion) and un-lumps P3 from P5a in §2.2, citing each source rationale. It also fixes the §8 side note (the stale `HA-C4b` verdict is replaced with a derive-from-backend pointer per §5).

**LOCKED r3 — 2026-07-09 by user acceptance.** The r2 review cleared the choice to lock after the L2.4 fix; r3 is that fix, accepted by the user 2026-07-09. No third review was required (the L2.4 fix is reviewer-scoped; the axis is unchanged, only its Guide side is now fully articulated). Phase-1/2/3 application work is unblocked. Phase 1 (reconcile `personal_hypotheses.md`: full P-entries + crosswalk + kind/stage) is reviewer-mode content drafted under authorization and goes to its own fresh-session [`/research-review`](../../../.claude/commands/research-review.md) before its lock, per §9.

**Erratum 2026-07-09 (post-lock; illustrative examples only — no rule change).** Applied after Phase 1 ran, per user authorization. Phase 1 (the [`personal_hypotheses.md`](../personal_hypotheses.md) reconciliation) resolved the §8 worked-examples, several of which r1 had guessed before the calls were made. Corrections, driven by the 2026-07-09 targeted check on the Phase-1 draft: (1) `what-the-watch-catches` reclassified from the r1 "Pure Beyond P8" guess to a **guide-extension** (check Finding A — it refines Wiggers' mental-PEM concession at her operationalisation, per §2.1); (2) P8/P9 relabelled to strict §5 — `changing-crash`/P8 = `descriptive / done` (its `character-flip` test is `idea`, not `scoped`) and `emotional-trigger`/P9 = `descriptive / parked` (check Finding B — the r1 §8 labels were looser than §5's own definitions); (3) the §5 `idea` stage widened to close the "designed-but-not-locked" gap Finding B exposed; (4) `best-in-the-middle` resolved to guide-extension (user decision; was a pending call); (5) §8 id assignment corrected to the actual mints. The §2.1 / §4 / §5 **rules are unchanged** — only illustrative applications moved — so no re-review, per the user's 2026-07-09 ruling. **Process note**: Phase 1 itself took a lightweight targeted provenance-accuracy + crosswalk check (not the full §9/§11 `/research-review`), per the 2026-07-09 agreement that a register-layer reconcile introducing no new verdicts does not warrant the verdict-grade review; recorded in the `personal_hypotheses.md` authorship block.
