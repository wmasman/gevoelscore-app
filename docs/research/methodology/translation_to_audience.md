# Translation to audience — Stage T guide

**Status**: **LOCKED r2** by user acceptance 2026-06-25 — **closes
§11 step 6 (six-guide arc complete)**. r1 authored 2026-06-25 by a
fresh agent per §11 step 6.6 of
[`_plan_results_analysis_layer.md`](_plan_results_analysis_layer.md)
(r5 LOCKED 2026-06-24). r1 → r2 absorbed a fresh-session
`/research-methodology-review` (verdict REVISION RECOMMENDED (mild),
report at
[`reviews/methodology-translation_to_audience-2026-06-25.md`](../reviews/methodology-translation_to_audience-2026-06-25.md))
that confirmed §3.12 patient-audience-ONLY commentary separation
holds at six enforcement layers; layperson-test gate operationally
implementable; layer-closure clean. Two required actions absorbed
(R1: `plain_language_dictionary.md` bootstrap responsibility added
to §9.1 with §11 step 7 sibling-task alternative; R2: §5.7 sixth
refusal-path added for source-stage map-change-needed). Three of
four recommended absorbed (A2: §5.10 cross-refs add §3.6 + §5; A3:
§9.6 gate with per-category headers; A4: this lock-log split into
per-event paragraphs). **A1 density compression deferred** per
reviewer's "for future revision pass" framing. **Layer ready for
§11 step 7 (skill build for `/research-interpret`).**

This guide is the sixth and final of six binding methodology MDs for
the results-analysis layer. It governs **Stage T** (translation to
audience): the per-source-artefact translation that takes any upstream
locked artefact — Stage I `interpretation.md`, Stage S₁
`cluster-*.md`, Stage S₂ `topic-*.md`, or Stage A `construct-*.md` —
and renders it onto **two audience tracks** (research-audience and
patient-audience). Each track produces one MD at
`analyses/translation/<track>/<source-name>.md`. Patient-audience
track carries the §3.12 subject-narrative commentary when the source
is a Stage A `construct-*.md` with a §5.9 commentary block filled;
research-audience track is FORBIDDEN to carry §3.12 commentary per
the locked-plan §3.12 hard separation. Patient-audience track is
layperson-test-gated; commentary fails the test if a layperson reads
it as a soft prediction.

Stage T sits at the layer's **outbound interface** — what other
humans actually read. Stages D / I / S₁ / S₂ / A produce internal
research artefacts; Stage T ports them to readers outside the
research line. It refuses to start on a source artefact that is not
locked, on a source whose technical terms are not present in
`plain_language_dictionary.md` for the patient-audience track, and on
a translation that would require a stronger claim than the source
artefact's verdict / coherence call / positioning / tier permits. It
operates on one source artefact per session and produces both tracks
per source (or records the skip-research-internal decision
explicitly).

---

## 1. Purpose

> **A locked upstream artefact is research output written for the
> research line itself. Stage T produces — or refuses to produce —
> audience-targeted translations on two tracks (research-audience +
> patient-audience), rendering the source's claim, caveats, L-IDs,
> and follow-ups in wording the named audience can actually use.
> Patient-audience track carries §3.12 subject-narrative commentary
> when the source has one; research-audience track is FORBIDDEN to
> carry commentary. Patient-audience track is layperson-test-gated;
> the layperson's interpretation, not the drafter's intent, is the
> binding test.**

Findings that exist only as technical MDs do not reach the people
they could most help; findings translated badly mislead. Stage T
governs both risks. Per
[`_plan_results_analysis_layer.md`](_plan_results_analysis_layer.md)
§3 stage-map: `D → I → S₁ → S₂ → A → T`. Stage T is the one stage
that may target any prior stage's output (not just Stage A — Stage T
can translate an interpretation, a cluster synthesis, a topic
contextualisation, or a construct actionability artefact), and the
one stage whose skip is allowed (research-internal scaffolding
artefacts that have no outward-communication purpose may record a
skip-research-internal decision instead of producing translation
artefacts). The two-track output is what lets a finding sit on the
public record honestly for both the researcher who reads N-of-1
methodology and the PAIS patient who is looking for daily-life
guidance.

**What Stage T does NOT do.**

- **NOT re-test the hypothesis or any upstream verdict, coherence
  call, positioning, or tier.** Source is read as fixed input;
  source revision is a Stage I / S₁ / S₂ / A drift trigger per
  §3.7, not a Stage T activity.
- **NOT predict beyond what the source's tier permits.** Per §3.10
  the gate applies to **wording**, not just tier-label — a tier-1
  source rendered with forecast wording is a tier-3 claim in
  disguise; §7.1 + §7.2 refuse such renderings. Per §3.12
  commentary cannot promote tier even in translation; §7.3 + §7.4
  operationalise.
- **NOT invent new caveats post-hoc.** Caveats come from source
  (Stage I §4.5; S₁ §4.5; S₂ §4.6+§4.7; Stage A §5.4+§5.11) and
  from the limitations doc L-IDs the source cites; §7.6 enforces.
  **Exception**: layperson-test wording-clarification sentences
  (not new caveats) are logged at §5.7.
- **NOT carry §3.12 commentary in research-audience track.** Per
  §3.12 hard separation + §6.6: commentary is patient-track ONLY.
  Research-track of a Stage A source MUST OMIT source §5.9. §4.2 +
  §5.11 + §7.3 + §9.6 operationalise.
- **NOT advise.** Advice prohibition inherited from Stage A; §7.5
  enforces. Patient-track carries highest advice-drift risk.
- **NOT translate an unlocked source.** Per §3 dependency rule;
  §9.2 gate refuses.
- **NOT operate on more than one source per session.** Source-
  bounded scope keeps translations commensurate.
- **NOT defer layperson-test indefinitely.** Per §3.12 + §6.6: gate
  fires before lock OR artefact is marked **layperson-test-
  pending** explicitly. §7.8 + §9.6 enforce.

**Alternatives considered** (per CONVENTIONS §2.2 item 3). Natural
alternatives: (a) single "general-audience" track; (b) merging
Stage T into Stage A. Both rejected for: (1) **audience mismatch**
— researcher and PAIS-patient personas have different prior
knowledge; a single track patronises both; (2) **commentary
segregation** — §3.12 mandates patient-track-only; single track
cannot enforce; (3) **layperson-test scoping** — gate is meaningful
only for patient-rendering; single track over- or under-applies;
(4) **commensurability across source stages** — dedicated Stage T
translates I / S₁ / S₂ / A through one structure; Stage-A-embedded
would forbid upstream-stage translations without A pass-through.

**Precondition: the `/research-interpret` skill must land first.**
Per [`_plan_results_analysis_layer.md`](_plan_results_analysis_layer.md)
§11 step 7, the `/research-interpret` skill is built after the six
guides (this guide is #6 of six — the last). **No Stage T artefact
can be drafted before §11 step 7 lands** — this guide alone is
necessary but not sufficient. The §9 agent-instruction outline below
is the skill's brief; the skill build (step 7) operationalises it.

## 2. Inputs

The translation MUST load and use the following inputs, in this
order:

1. **The source artefact being translated** — exactly one, locked,
   from any of four upstream stages per §3 dependency rule ("`T`
   may target any prior stage's output; not strictly serial after
   `A`"):
   - **Stage I**: `analyses/interpretation/HA-XX.md` — target:
     §3 licensed claim + §4 not-licensed + §5 caveats + §7 L-IDs
     + §8 follow-ups.
   - **Stage S₁**: `analyses/synthesis/cluster-XXX.md` — target:
     §4.4 coherence call + §4.7a/b joint claim + §4.5 caveats +
     §4.6 open conflicts + §4.7 L-IDs + §4.8 follow-ups.
   - **Stage S₂**: `analyses/contextualisation/topic-XXX.md` —
     target: §4.5 positioning + §4.4 comparability + §4.6 caveats
     + §4.7 L-IDs + §4.8 open conflicts + §4.9 follow-ups.
   - **Stage A**: `analyses/actionability/construct-XXX.md` —
     target: §5.3 tier claim + §5.4 NOT-DO + §5.7 quality measures
     (if tier-2+) + §5.8 follow-ups + §5.11 all-seven L-IDs +
     **§5.9 commentary (patient-track only, when filled)**.
   Stage T reads source as fixed input; does NOT renegotiate.
2. **The source's stage** (I / S₁ / S₂ / A) — determines the §5
   outline content, §4 audience specificity, and §5.11 commentary
   presence (Stage A with §5.9 filled → patient-track §5.11
   present; otherwise omitted).
3. **The synthesis-structure map's row** for the source — §3
   cluster row (S₁), §4 topic row (S₂), §5 construct row (A); for
   Stage I, indirection through the §3 cluster the HA belongs to.
   Cells: tier aspiration, §3.12 commentary-eligibility (A
   sources), L-ID notes.
4. **[`research_line_limitations.md`](research_line_limitations.md)**
   — §3 (seven L-IDs); §5 row for translation: *"Patient-audience
   track translates the applicable limitations into plain-language
   honest-uncertainty wording per §6.6. Research-audience track
   keeps the L-IDs as cross-references."* Source's L-ID block is
   binding ceiling — Stage T renders the **same** L-IDs, per-stage:
   I → HA's primary-signal L-IDs; S₁ → cluster-members' L-IDs
   (L2 if cross-stratum); S₂ → L1+L2+L4 unconditional + L3/L5/L6/L7
   as apply; A → all seven applies-or-NA.
5. **[`plain_language_dictionary.md`](plain_language_dictionary.md)**
   — the live dictionary maintained by Stage T (per locked-plan §4
   producer/reviewer split: "Maintained by `/research-interpret`
   translate stage; one term added per technical term encountered").
   Stage T loads the current dictionary; for every technical term
   appearing in the source artefact, the dictionary MUST contain an
   entry before the patient-audience track can lock per the §9.6
   gate. Stage T appends new terms at §5.10 + §9.5.
6. **The audience-definition specifics** — per-translation interview
   inputs (§8.1 seed). Research-audience: specific reader persona
   (e.g., "LC researcher familiar with wearable data," "clinician
   who has read the PEM-pacing literature"); patient-audience:
   specific reader persona (e.g., "PAIS patient ≥2 years post-onset
   comfortable with Dutch lay-press health articles"). NOT
   "general public" — see §4.4 audience-specificity binding.
7. **The layperson-test recruitment context** (patient-track only).
   Per locked-plan §10.7 deferred question. **Stage T resolution**:
   defer pool-policy at guide level; per artefact, record the pool
   as identified (peer/non-peer identifier + relation to construct
   + research-line exposure) OR mark **layperson-test-pending** per
   §5.7 + §9.6. Indefinite deferral forbidden per §7.8.
8. **The Stage A tier** (if source is Stage A or touches
   actionability) — drives patient-track wording: tier-1
   descriptive; tier-2 "right N out of M" per RESEARCH-REPORT §5.2;
   tier-3 with lead-time + reliability. Read from source §5.2;
   non-A sources default to "tier-pending" framing.
9. **The §3.12 commentary section** (if source is Stage A with
   §5.9 filled) — patient-track renders into plain-language
   equivalent preserving subject-attribution, permitted-wording,
   and "attached to: K-XXX tier-N claim" header. Research-track
   omits per §3.12 hard separation + §4.2 + §5.11 + §7.3 + §9.6.
10. **The relevant methodology MDs** — guides #1-#5 + any
    construct-specific MDs the source cited.
11. **[`RESEARCH-REPORT.md`](../RESEARCH-REPORT.md) §5.2 PPV-with-
    base-rate precedent** — *"wrong 24 times out of 25"*. Required
    at Stage A tier-2+ sources; §5.6 draws verbatim.
12. **CONVENTIONS** — §1, §1.2, §2.1, §4.2, §4.3 as cited.

The translation does NOT load: raw descriptive runs (those were
Stage D inputs; Stage T inherits via the chain); member HAs' `test.py`
or `result-data.json` (those were Stage D / Stage I inputs); other
source artefacts (cross-source reading is out of scope — Stage T
operates on one source per session per §1 NOT-do list); forward-
validation HAs unless the source is a Stage A `construct-*.md`
that already cited them (Stage T does not re-evaluate the §3.10
hard predictive gate; it inherits the source's tier reading).

## 3. Output

The translation produces **two artefacts per source artefact**, one
per audience track:

```
docs/research/analyses/translation/research-audience/<source-name>.md
docs/research/analyses/translation/patient-audience/<source-name>.md
```

**Naming convention.** Both files are named after the source
filename (without the `analyses/<stage>/` prefix). Examples: source
`analyses/interpretation/HA-C4.md` → `translation/research-
audience/HA-C4.md` + `translation/patient-audience/HA-C4.md`;
source `analyses/actionability/construct-bout-recovery-signal.md` →
`translation/research-audience/construct-bout-recovery-signal.md` +
`translation/patient-audience/construct-bout-recovery-signal.md`.
Flat naming inside each audience-track subfolder matches the
locked-plan §5 output-tree exactly. Revision history lives in each
file's §10 lock log; source revisions re-trigger both translations
per §3.7 drift, as do dictionary term shifts affecting the patient-
track per §6.3.

**Skip-research-internal option.** Per locked-plan §3 dependency
rule + §3.8 stopping criteria row for translation artefacts: "Both
audience tracks produced (or skip-research-internal recorded)." A
source artefact whose audience is research-internal only (e.g., a
descriptive audit, a Stage I `interpretation.md` whose downstream
purpose is to feed a Stage S₁ cluster and not to be communicated
outward) may record a **skip-research-internal decision** at the
source artefact's downstream-references section instead of producing
Stage T translations. The skip is **explicit**, not silent: the
source artefact's cross-references record "Stage T translation
skipped — research-internal only; rationale: <one sentence>". The
skip decision is intentional per locked-plan §3 ("the decision to
skip `T` for a given target is recorded explicitly so the skip is
intentional, not accidental").

**Mode.** Reviewer-mode-with-authorization per
[`_plan_results_analysis_layer.md`](_plan_results_analysis_layer.md)
§4 producer/reviewer split table row for translation artefacts:
"Skill-driven / Fresh-session `/research-review` plus layperson-test
where patient-audience track exists." Drafted by Claude under user
authorization via `/research-interpret translate <source-path>`,
each track-file carrying a `## Authorship` block per
[CONVENTIONS §1.2](../CONVENTIONS.md#12-producer-vs-reviewer-mode).
Both track-files receive a fresh-session `/research-review` pass
before lock; the patient-audience track-file additionally receives
the layperson-test gate per §5.7 + §9.6 below.

**L-ID rendering discipline at the output level.** Per
[`research_line_limitations.md`](research_line_limitations.md) §5
table row for translation artefacts:

> ***Patient-audience track translates the applicable limitations
> into plain-language honest-uncertainty wording per §6.6 of the
> plan. Research-audience track keeps the L-IDs as cross-references.***

The **source artefact's L-ID block is the binding ceiling** — Stage
T cites the **same** L-IDs the source cited, in the same
applicability scope. Per-track rendering:

- **Research-audience track**: keeps the L-IDs by ID (e.g., "Cites
  L1 (single-subject reach)..."), with a one-line audience-rendered
  application sentence per L-ID drawn from the source's L-ID block.
  The audience is expected to understand the methodology layer; the
  L-ID names + one-sentence applications are the rendering.
- **Patient-audience track**: renders the L-IDs in plain-language
  without naming L-IDs explicitly (e.g., "this finding is about me,
  not about everyone with PAIS"). The audience does not need the
  L-ID labels; the audience needs the honest-uncertainty content
  the L-IDs encode. The applicable-limitations set is the same as
  research-audience; only the rendering changes.

**Hard rule.** A Stage T artefact whose L-ID rendering omits an
L-ID the source cited cannot be locked per §9.6 gate. The source's
L-ID block is the ceiling; Stage T renders, it does not add or
subtract.

**Hard rule.** Stage T MUST NOT cite an L-ID the source did NOT
cite. New L-ID citations at Stage T time are forbidden per §7.6
anti-pattern (inventing new caveats post-hoc). If Stage T identifies
a source-missing L-ID, the §6.3 + §7.6 routing applies (route back
to source-stage for revision via §3.7 drift); the missing L-ID does
NOT enter the translation through Stage T prose.

**Worked-example anchors** (four likely Stage T sources from map
r3 active chain):

- Stage I `analyses/interpretation/HA-C4.md` → both tracks; no
  §5.11 commentary (Stage I sources don't carry commentary).
- Stage S₂ `analyses/contextualisation/topic-stress-fatigue-
  pacing.md` → both tracks; research-audience keeps L1+L2+L4
  unconditional + L3/L6/L7; patient-audience renders same in plain
  Dutch; no §5.11 commentary.
- Stage A `analyses/actionability/construct-stress-fatigue-
  monitoring.md` (tier-1, commentary-eligible) → both tracks; all
  seven L-IDs applies-or-NA; patient-audience track carries §5.11
  commentary translation.
- Stage A `analyses/actionability/construct-bout-recovery-signal.md`
  (tier-2, commentary-eligible) → both tracks; all seven L-IDs +
  tier-2 PPV-with-base-rate translation per §5.6; patient-audience
  track carries §5.11 commentary.

## 4. The two audience tracks (binding mapping rules)

This section pins the per-track rules. Each track's audience scope
is fixed; each track's wording discipline is bounded; each track's
section presence rules (especially §5.11 commentary) are
non-negotiable. One worked example per track distinction, drawn
from the two active constructs in the map's r3 (K-stress-fatigue-
monitoring; K-bout-recovery-signal). The §3.12 hard separation on
commentary is the load-bearing constraint and is operationalised in
§5.11 (patient-track commentary section), §7.3 (research-audience-
commentary anti-pattern), and §9.6 lock-gate item.

### 4.1 Research-audience track

**Audience scope.** Specific researcher / clinician personas who
have read N-of-1 methodology and the relevant construct literature.
Examples: "LC researcher familiar with Garmin wearable data";
"clinician who has read Wiggers PEM-pacing handbook"; "ME/CFS
researcher familiar with within-day recovery impairment". NOT
"general researcher" — §4.4 specificity binding.

**Prior knowledge assumed.** N-of-1 methodology (CENT 2015, Daza
2018, Natesan 2023); the source's verdict-shape vocabulary
(REJECTED/SUPPORTED/PARTIAL/INCONCLUSIVE at Stage I; CONCORDANT
/PARTIAL/CONFLICT/ORTHOGONAL at S₁; AGREES/EXTENDS/DIVERGES
/CANNOT-SAY at S₂; monitoring/informative-pattern/predictive-use
at Stage A); diagnostic-quality measures where source is tier-2+;
construct-specific methodology MD vocabulary the source cited.

**Wording discipline.** Terse, technical, methodology-vocabulary-
literate. Renders the source's claim-shape vocabulary directly
(a Stage S₁ "PARTIALLY CONCORDANT" stays "PARTIALLY CONCORDANT";
a Stage A tier-2 PPV-with-base-rate stays in PPV-with-base-rate
form). The rendering is **re-framing for audience expectations**,
not **paraphrase for ease**. L-IDs cited by ID with one-sentence
application.

**§3.12 commentary status.** **FORBIDDEN** per locked-plan §3.12
hard separation: commentary lives in Stage T patient-audience-track
ONLY. Research-audience track of a Stage A source MUST OMIT the
source's §5.9 commentary block. The §5.11 patient-track-section is
absent from research-audience track-files; the research-audience
track's §5 outline ends at §5.10 cross-references with no §5.11
commentary section per §5 below.

**Forbidden wording at research-audience track.** Patronising
glosses on methodology vocabulary the audience already has ("N-of-1
means just one person was studied" — patronising to an N-of-1
researcher); methodology-vocabulary collapse ("informative pattern"
re-rendered as "predictive" — collapses the §3.10 hard predictive
gate's evidentiary distinction); commentary content from a Stage A
source (per §3.12 hard separation).

**Worked example — research-audience translation of a Stage A
source.** Source: `analyses/actionability/construct-stress-fatigue-
monitoring.md` (tier-1 monitoring aspiration; commentary-eligible
per map r3 §5).

> *Tier claim*: daily `all_day_stress_avg` tracks daily `gevoelscore`
> descriptively across the Stratum 4 unmedicated window. The two
> signals move together with an inverted-U shape peaking around
> mid-stress range; tracking daily Garmin stress gives a same-day
> window onto the day's gevoelscore range. Tier-1 monitoring;
> §3.10 PPV-with-base-rate exempt (descriptive correspondence
> claim).
>
> *Caveats*: HA-C3 v2 + HA-C3p both pre-registered with Wiggers
> convex-cost prior (confirmatory per CONVENTIONS §4.3); Stratum 4
> unmedicated only; cross-era projection out of scope. Cites L1
> (single-subject reach per Daza 2018); L2 (era confounds; scope
> Stratum 4 unmedicated); L4 (analyst-is-subject; fresh-session
> /research-review the L4 mitigation reach). L5 NA (no v24 primary
> signals).

Tier-1 vocabulary preserved verbatim ("monitoring", "descriptive
correspondence", "exempt"); L-IDs named ("L1", "L2", "L4", "L5
NA"); methodology citations kept (Daza 2018, CONVENTIONS §4.3); no
commentary content from source §5.9.

### 4.2 Patient-audience track

**Audience scope.** Specific laymen / PAIS-patient personas. Examples:
"PAIS patient ≥2 years post-onset, Dutch-speaking, comfortable
reading lay-press health articles, owns a Garmin watch"; "non-PAIS
family member wanting to understand what the wearable data
shows"; "non-specialist clinician (GP, physiotherapist) seeing
PAIS patients without deep ME/CFS methodology background". NOT
"general public" — §4.4 specificity binding.

**Prior knowledge assumed.** Lived experience of PAIS-style
fatigue/crash patterns (PAIS-patient persona); construct's daily-
life manifestation; willingness to read honest-uncertainty wording
(laymen handle uncertainty when framed honestly — §7.7). NOT
assumed: N-of-1 methodology vocabulary; L-ID labels; verdict-shape
vocabulary; diagnostic-quality-measure names; construct-specific
methodology MD vocabulary.

**Wording discipline.** Accessible, jargon-replaced or jargon-
defined, plain-language. Renders source's technical claims into
"what this means for someone living with PAIS." Shorter sentences
than source; one-thought-per-sentence preferred for cognitive-load
reduction. Layperson-test-gated per §5.7 + §9.6.

**§3.12 commentary status.** **ELIGIBLE when source is Stage A
with §5.9 filled**. Patient-audience track-file carries a §5.11
section translating the source's §5.9 commentary into the audience's
plain language; subject-attribution preserved ("ik merk op dat..." /
"in mijn ervaring..." in Dutch; "I notice that..." / "in my
experience..." in English); permitted-wording-only discipline
carries through the translation; forbidden-wording discipline
carries through (no "voorspelt" / "predicts"; no "morgen" / "tomorrow";
no "X betekent Y" / "X means Y"). Layperson-test gate fires
specifically on the commentary block per §5.7 + §3.12
implementability check.

**Forbidden wording at patient-audience track.** Methodology-jargon
that the audience does not have (PPV / NPV / sensitivity / L-IDs /
N-of-1 / monitoring-tier / etc. — see §7.4 anti-pattern); faux-
balanced wording that softens an honest call ("evidence is mixed"
when source said CANNOT-SAY — see §7.7 anti-pattern); predictive-
sounding wording for a monitoring-tier source ("watch for X" =
predictive in disguise per §7.1 + §7.2); advice wording ("you
should rest when X drops" — per §7.5 inherited from Stage A); §3.12
forbidden wording in commentary translation ("predicts", "forecasts",
"will happen", "tomorrow", "X means Y").

**Worked example — patient-audience translation of the same Stage
A source.** Source: `analyses/actionability/construct-stress-fatigue-
monitoring.md` (Dutch base-language per §4.3 default for this
example).

> *Wat dit voor jouw dagelijks leven betekent*: op dagen dat mijn
> Garmin-stresswaarde rond het midden van het bereik zit (~30-40),
> ligt mijn gevoelscore vaak in de hogere helft van wat ik die
> dag aankan. Heel lage stresswaarden gaan vaak samen met dagen
> waarop ik "alles aan het sparen" was; heel hoge waarden met dagen
> waarop ik over mijn grenzen ging. Dit is een *observatiehulp*,
> geen voorspelling — ik kan de waarde gebruiken om mezelf vandaag
> beter te lezen, niet om morgen te voorspellen.
>
> *Wat ik er NIET mee kan*: ik kan deze waarde niet gebruiken om
> te beslissen "rust nu wel of niet". De data laat zien dat de
> twee samen bewegen, niet dat de een de ander veroorzaakt of
> voorspelt. Wat voor mij geldt over deze periode hoeft niet voor
> andere mensen met PAIS te gelden.

No L-ID labels ("L1" → "wat voor mij geldt hoeft niet voor andere
mensen te gelden"); no methodology vocabulary ("monitoring-tier" →
"observatiehulp"); honest-uncertainty wording without faux-balance
("Dit is een observatiehulp, geen voorspelling" preserves the
tier-1 / NOT-tier-3 distinction the source carries); advice
prohibition ("Wat ik er NIET mee kan: rust-of-niet beslissingen").
If source §5.9 is filled, a §5.11 commentary block is added per
the §5.11 worked example below.

### 4.3 Plain-language base language

Per locked-plan §10.6 deferred question: "Dutch (the user's daily-
life language for clinic conversations) or English (the project's
default written-research language)? May depend on per-construct
audience choice." **Stage T resolution**: defer the global default
at the guide level; per translation, the audience-definition (§5.2
+ §8.1) names the base language. **Heuristic** (non-binding):
patient-audience track defaults to Dutch when audience persona is
PAIS-patient looking for daily-life or clinic-conversation use
(the user's actual clinic-conversation language); research-audience
track defaults to English (the project's default written-research
language); per-artefact deviation is allowed when the audience
persona is non-default (e.g., English-language PAIS-patient peer;
Dutch-speaking LC researcher who specifically requested Dutch). The
language choice is recorded in §5.2 audience-definition and
propagates through every section of the track-file.

**Dictionary-language pairing.** The plain-language dictionary
maintains entries in **both Dutch and English** for every term;
patient-audience track in Dutch draws the Dutch entry, in English
draws the English entry. Language consistency within a single
track-file is binding; mixing languages within a track-file is
forbidden per §7.10 below.

### 4.4 Audience-specificity binding

Both tracks: audience MUST be specific (named persona with named
prior knowledge), not "general public" / "general researcher" /
"everyone." A generic audience produces translation that serves no
specific reader — patronises the equipped, loses the unequipped,
and the layperson-test gate cannot fire meaningfully without a
specific layperson persona. Per §6.6 spec: "specific subgroup (not
'general public')." §7.9 enforces as anti-pattern.

**Valid specificity examples.** Research-audience: "LC researcher
familiar with Garmin data and Wiggers PEM-pacing literature."
Patient-audience: "PAIS patient ≥2 years post-onset, Dutch-
speaking, owns a Garmin watch, curious about daily stress reading."

**Forbidden non-specificity.** "Researchers" / "anyone interested
in N-of-1" / "the research community" — too generic to drive
wording. "Patients" / "PAIS community" / "the general public" —
too generic for layperson-test gate.

### 4.5 Track mapping — summary table

The two tracks and their core distinguishing features:

| Track | Audience persona | Methodology vocabulary | §3.12 commentary | Layperson-test |
|---|---|---|---|---|
| Research-audience | Specific researcher / clinician with N-of-1 methodology background | Preserved verbatim | **FORBIDDEN** (locked-plan §3.12 hard separation) | NOT applied |
| Patient-audience | Specific layperson / PAIS patient persona | Plain-language replaced or defined | **ELIGIBLE when source is Stage A with §5.9 filled** | **REQUIRED — fires before lock OR layperson-test-pending** |

The discipline cascade: research-audience preserves methodology
content for an equipped reader; patient-audience renders content
for an unequipped reader with honest-uncertainty preserved AND
optional commentary translated. The track distinction is what lets
each audience read the source's claim in their own vocabulary
without either being patronised (the equipped) or misled (the
unequipped).

## 5. Section outline for the produced translation artefacts

Each translation artefact (one per audience track) MUST contain
ten sections in this order. Patient-audience track adds §5.11 when
the source is Stage A with §5.9 commentary filled; research-
audience track ends at §5.10 with no §5.11. The section structure
mirrors per source-stage where the source itself has a comparable
section; sections specific to Stage T (§5.2 audience definition;
§5.7 layperson-test gate; §5.10 cross-refs; §5.11 commentary
translation) carry the full operational detail per the §6.6 spec
brief.

### 5.1 Section 1 — Source artefact citation

Mechanically copy: source artefact path + lock-version + the single
claim being translated (verbatim from the source's primary claim
sentence — Stage I §3 licensed-claim sentence; S₁ §4.7a joint
claim; S₂ §4.5 positioning sentence; Stage A §5.3 tier-claim
sentence). Header, not analysis; its purpose is to fix the source
target.

**Template.**

> *Source*: [`<source-path>`](<source-path>), locked `<YYYY-MM-DD>`,
> revision `<rN>`.
>
> *Source claim translated*: <verbatim source claim sentence>.
>
> *Source stage*: <I / S₁ / S₂ / A>.
>
> *Source §3.12 commentary status* (Stage A sources only): <filled
> per source §5.9 / skipped-with-rationale per source §5.9 / not
> applicable, source is not Stage A>.

The source-claim sentence is copied verbatim to bind the translation
to the source; the translation's rendering follows in §5.3 but the
verbatim source-claim anchors what is being translated.

### 5.2 Section 2 — Audience definition

The specific audience persona for this track-file, per §4.4
specificity binding. One paragraph: persona description; prior
knowledge assumed (per the per-track §4.1 or §4.2 list); questions
this audience is likely to bring after reading the first paragraph;
base language (per §4.3). **Hard rule**: "general public" /
"general researcher" / "everyone" framings refuse to lock per §7.9
+ §9.6 gate.

**Template** (each track):

> *Audience for this track*: <specific persona>. Prior knowledge
> assumed: <per §4.1 or §4.2 list>. Prior knowledge NOT assumed
> (patient-track only): <methodology vocabulary; L-IDs;
> quality-measure names>. Likely first-read questions: <2-3
> specific questions>. Base language: <Dutch / English>.

### 5.3 Section 3 — Plain-language translation of the source's core claim

The audience-rendered translation of the source's primary claim
sentence (the §5.1 verbatim source-claim). Per-track wording
discipline applies (research-audience: preserved methodology
vocabulary, terse; patient-audience: plain-language replacement,
shorter sentences, layperson-test-gated).

**Research-audience template.** Re-frames the source claim's
sentence-structure for audience expectations while preserving the
verdict-shape / coherence-call / positioning / tier vocabulary.
Methodology citations preserved.

**Patient-audience template.** Renders the source claim's
substantive content in plain-language. Technical terms either
replaced (when the dictionary has a direct equivalent) or
inline-defined (one-line definition in parentheses); L-ID labels
absent (rendered in §5.5 per L-ID rendering discipline). Layperson-
test fires on this paragraph per §5.7 — if a layperson reads the
core claim as forecast / advice / patronising, the paragraph is
revised before lock per §7.7 + §9.6 gate.

**Worked example — Stage A source `construct-bout-recovery-
signal.md` tier-2 claim** (assumes PPV computes).

*Research-audience track*:

> Tier-2 informative-pattern claim: when `bout_n_did_not_return_day`
> exceeded the heavy-T threshold in past cross-phase pooled data, a
> crash day followed within the window N out of M times. Cross-
> phase pooling per [`citalopram_phase_stratification.md`](citalopram_phase_stratification.md)
> §5; residual crash-day base rate ~2/year per RESEARCH-REPORT §5.2.

*Patient-audience track* (Dutch):

> Wanneer mijn bout-niveau hersteldata (het signaal dat aangeeft of
> mijn hartslag tussen inspanningen terugkomt) op een zware dag een
> drempel overschrijdt, is er in mijn eigen data uit het verleden
> in N van de M gevallen binnen een paar dagen een crash gevolgd.
> Crashes komen bij mij ongeveer 2 keer per jaar voor; het signaal
> "afgaan" is zelf dus ook zeldzaam.

Methodology vocabulary replaced; "bout-niveau hersteldata" defined
inline; PPV preserved as "N van de M gevallen" without the label;
RESEARCH-REPORT §5.2 base-rate context preserved in plain Dutch.

### 5.4 Section 4 — Translation of the source's caveats

The source artefact's caveats rendered audience-appropriately,
tier-bounded per source. Stage T does NOT invent new caveats per
§7.6; it renders the caveats the source carried (Stage I §4.5; S₁
§4.5; S₂ §4.6 + §4.7; Stage A §5.4 + §5.11).

**Per-track rendering.**

- **Research-audience track**: keeps the source's caveat vocabulary;
  cites source-section by name (e.g., "Per source §4.6 N-of-1-to-
  group caveats..."). One paragraph per caveat-category the source
  carried; methodology citations preserved.
- **Patient-audience track**: renders caveats in plain-language;
  source-section names omitted (audience doesn't need them); honest-
  uncertainty preserved per §7.7. One paragraph per caveat-category
  the source carried; the audience's likely first-read questions
  (per §5.2) drive whether a caveat needs additional explanatory
  wording or stays terse.

**Hard rule**: patient-track caveats render the source's NOT-DO
refusals (Stage A §5.4 categories — predictive-use / causal /
group-level / advice — per the source's tier-bound list) into "wat
ik er NIET mee kan" / "what I cannot use this for" wording. Advice
prohibition propagates verbatim from Stage A; bare-percentage
prohibition propagates verbatim from Stage A tier-2+.

**Worked example — patient-audience caveats for Stage A source
`construct-stress-fatigue-monitoring.md` tier-1 claim** (Dutch):

> *Wat ik er NIET mee kan*: ik kan deze waarde niet gebruiken om
> de gevoelscore van morgen te voorspellen — het is een
> observatiehulp voor vandaag, niet een vooruitblik. Ik kan er ook
> geen oorzaak-en-gevolg uit afleiden ("stress veroorzaakt
> gevoelscore"); dat de twee samen bewegen, betekent niet dat de
> een de ander aanstuurt. Wat voor mij geldt over deze periode
> hoeft niet voor andere mensen met PAIS te gelden — dit is mijn
> eigen data, niet groepsdata. En de waarde is geen instructie
> ("rust nu wel of niet") — onderzoek dat zou kunnen aantonen of
> rusten op basis van Garmin stress beter werkt dan niet rusten,
> zou een gerandomiseerde studie vereisen die ik op mezelf niet
> kan uitvoeren.

Four NOT-DO categories rendered (predictive / causal / group-level
/ advice); methodology vocabulary absent; honest-uncertainty
preserved without faux-balance.

### 5.5 Section 5 — Translation of the source's L-ID citations

Per the locked-plan §6.6 spec brief + §2 input #4 binding: Stage T
renders the **same** L-IDs the source cited, in the same
applicability scope. Per-track rendering per §3 hard rules:

- **Research-audience track**: keeps L-IDs by ID. One sentence per
  L-ID applying the limitation to the source's claim, drawn from
  the source's L-ID block. Format: "Cites L`<N>` (`<short
  name>`): `<one-sentence application from source>`."
- **Patient-audience track**: renders L-IDs in plain-language
  without naming them. One paragraph per L-ID-group that the
  audience encounters as a single conceptual concern (e.g., L1 +
  L2 may render together as "this is about me over a specific time
  window"). Audience-rendering takes precedence over one-to-one
  L-ID-to-paragraph mapping; the rendering MUST preserve the
  applicability scope the source's L-IDs encoded.

**Hard rule** (per §3 + §9.6): omit no source-cited L-ID in either
track; add no L-ID the source did not cite. Source's L-ID block is
the binding ceiling.

**Worked example — Stage A source `construct-stress-fatigue-
monitoring.md`** (all seven L-IDs applies-or-NA per source §5.11).

*Research-audience track* (terse per-L-ID):

> Cites L1 (single-subject reach): tier-1 within-subject scope
> Stratum 4 unmedicated; per Daza 2018, does not generalise.
> Cites L2 (era confounds): scope Stratum 4 unmedicated;
> cross-era out of scope. Cites L3 (device generations): FR245
> Elevate V3 `all_day_stress_avg`; device upgrade triggers §3.7
> drift. Cites L4 (analyst-is-subject): HA-C3 v2 + HA-C3p with
> Wiggers convex-cost prior; mitigation reach is fresh-session
> `/research-review`. L5 NA: no v24 primary signals. Cites L6
> (self-reporting): gevoelscore outcome respects bin-level noise
> floor. Cites L7 (survivorship): non-NaN-gated; effective
> coverage is gated subset.

*Patient-audience track* (Dutch, grouped):

> *Wat de grenzen van dit signaal zijn*: deze bevinding gaat over
> mij over een bepaalde periode (september 2022 tot voor mijn
> medicatiestart in 2024). Wat voor andere mensen met PAIS geldt,
> kunnen we hier niet uit afleiden. De waarde komt van mijn Garmin
> Forerunner 245 — als ik een ander horloge zou gebruiken, zou ik
> deze bevinding opnieuw moeten controleren.
>
> *Hoe streng het onderzoek zelf is*: ik ben hier zowel onderzoeker
> als onderwerp, dus heb ik het onderzoek voorgelegd aan een
> aparte reviewsessie om blinde vlekken te vinden. De gevoelscore
> die ik gebruik is een eigen inschatting; die werkt op het niveau
> van bereiken (laag / midden / hoog), niet op exacte punten. Ik
> heb de bevinding berekend op de dagen waarop ik volledige data
> had — dagen met gaten in de Garmin-meting zijn niet meegenomen.

Seven L-IDs preserved in content (L1 → "gaat over mij"; L2 →
"september 2022 tot 2024"; L3 → "Garmin Forerunner 245"; L4 →
"zowel onderzoeker als onderwerp" + "aparte reviewsessie"; L5 NA
→ omitted as NA; L6 → "eigen inschatting" + "bereiken niet
punten"; L7 → "dagen met volledige data" + "gaten niet
meegenomen"). No L-ID labels. Grouping is audience-driven (two
groupings: "wat de grenzen zijn" for L1+L2+L3; "hoe streng het
onderzoek is" for L4+L6+L7).

### 5.6 Section 6 — Quality-measure translation per §3.10

**Required when source artefact is Stage A tier-2+** per locked-
plan §3.10 + §6.6 spec brief. Renders the source's §5.7 quality
measures (PPV + base rate + plain-language combined frame;
optionally NPV / sensitivity / specificity / false-alarm rate /
lead time / reliability) audience-appropriately per the §6.6
binding:

> *Research-audience track*: keep the technical measure names (PPV,
> base rate, lead time) alongside the plain-language gloss.
>
> *Patient-audience track*: plain-language frame only — "when this
> fires, it's right N out of M times, in a context where N happens
> M times a year." No bare percentages without their base-rate
> context. The RESEARCH-REPORT §5.2 wording ("wrong 24 times out
> of 25") is the model.

When source is Stage I / S₁ / S₂ (NOT Stage A) → this section is
omitted (§3.10 quality-measures discipline binds at Stage A only;
upstream stages do not produce PPV-with-base-rate per the locked-
plan §3.10 binding).

When source is Stage A tier-1 → this section records "Quality-
measure translation not applicable: source artefact is tier-1
monitoring (per source §5.2); §3.10 PPV-with-base-rate is exempt
at tier-1 (per source §5.7)."

When source is Stage A tier-2+ → required content per track:

- **Research-audience track**: PPV + base rate stated in source's
  numeric form alongside the RESEARCH-REPORT §5.2 plain-language
  gloss; optional measures kept in source's numeric form. Methodology
  vocabulary preserved.
- **Patient-audience track**: plain-language frame only ("wanneer
  het signaal afgaat, klopt het N van de M keer; gebeurtenis komt
  ongeveer M keer per jaar voor"); base-rate context preserved
  non-negotiably; bare-percentage rendering forbidden per §7.4
  anti-pattern.

**Worked example — patient-audience track quality-measure
translation for Stage A source `construct-bout-recovery-signal.md`
tier-2 claim** (Dutch, assumes PPV computes):

> *Hoe vaak het klopt als het signaal afgaat*: in mijn eigen data
> uit het verleden ging in N van de M gevallen een crash binnen
> een paar dagen samen met dit signaal. Crashes komen bij mij
> ongeveer 2 keer per jaar voor; het signaal "gaat dus zelf ook
> niet vaak af". Het patroon is sterk genoeg om in retrospectief
> betekenisvol te zijn, maar niet sterk genoeg om als dagelijkse
> waarschuwing te dienen — dat zou een prospectieve test vereisen
> die nog niet is uitgevoerd (zie ook *wat hier nog open staat*
> in §5.8).

PPV preserved as "N van de M gevallen"; base rate preserved as "~2
keer per jaar"; "informative-pattern" tier-2 framing rendered as
"retrospectief betekenisvol... niet als dagelijkse waarschuwing"
(preserves the §3.10 tier-2-not-tier-3 distinction); RESEARCH-
REPORT §5.2 base-rate-context wording inherited verbatim in plain
Dutch.

### 5.7 Section 7 — `open_inputs` block + layperson-test status

Per locked-plan §3.5. Each entry names: (1) what is missing —
typically a needed plain-language dictionary term not yet added, a
visual not yet produced (per the locked-plan §6.6 spec brief's
visual-summary line — see §5.8 below), a layperson-tester not yet
recruited / scheduled, a source-cited L-ID whose plain-language
rendering needs review; (2) what is blocking — typically a section
of this track-file that cannot lock until the missing input arrives;
(3) cheapest acquisition path — dictionary update via §5.10; visual
production via existing `analyses/.../figures/` scripts; layperson
recruitment per the §10.7 deferred-question-per-translation
resolution; (4) fallback rendering available without it.

**Translation-specific refusal-to-proceed paths** (per §3.5):

1. **Source missing or not locked** → halt; entry: source missing
   → Stage T blocked → "lock source via its stage's
   `/research-review`" → fallback "none."
2. **Source is Stage A commentary-eligible but §5.9 not filled** →
   proceed without §5.11 commentary; entry: §5.9 not filled →
   patient-track §5.11 blocked → "source drafter fills §5.9 OR
   records skip-with-rationale" → fallback "§5.11 omitted with
   note."
3. **Dictionary missing terms** → proceed at research-track but
   NOT at patient-track lock; entry: missing term → patient-track
   lock blocked → "add term per §5.10 + §9.5" → fallback
   "research-track produced; patient-track held."
4. **Layperson-test pool not identified** → proceed to draft
   patient-track; lock as **layperson-test-pending**; entry: pool
   not recruited → final lock blocked → "identify per §10.7;
   run test per §5.7" → fallback "patient-track drafted;
   layperson-test-pending recorded."
5. **Visual summary not produced** (patient-track primary) →
   proceed at lock with visual-pending status; entry: visual spec
   per §5.8 → visual blocked → "produce via existing
   `analyses/.../figures/` scripts OR specify for future" →
   fallback "visual specification recorded; visual pending."
6. **Source-stage map-change-needed surfaces during Stage T**
   (per §6.6 halt-criteria) → halt; entry: map-change-needed →
   Stage T blocked → "route to producer-mode map-revision session
   per locked-plan §3.6 conflict-resolution rule; on map re-lock,
   Stage T resumes against the new map version" → fallback "none —
   Stage T cannot proceed against a structurally-misclassified
   source; the §6.6 halt + map-revision pathway is the only
   resolution." Distinct from refusal-path #1 because the source
   IS locked but the map-source binding is wrong; the §6.6 halt-
   criteria enumerate the four specific in-stage discovery cases
   (cluster membership reveal; topic-cluster mapping reveal;
   construct-topic mapping reveal; tier aspiration reveal).

**Layperson-test status block** (patient-audience track only).
This sub-section records the layperson-test outcome AT THIS lock
cycle, one of:

- **Tested**: "Layperson-test conducted with `<layperson-pool-
  identifier>` on `<date>`. Layperson read `<paragraph or section
  that fired the test>`. Observed interpretation: `<what the
  layperson actually understood / mis-understood>`. Revision
  triggered: `<NO — interpretation matched drafter intent; OR
  YES — paragraph revised per layperson reading; new wording at
  §5.3 / §5.4 / §5.11 as applicable>`."
- **Layperson-test-pending**: "Layperson-test pool not yet
  identified per §10.7 per-artefact resolution. Patient-audience
  track drafted to current discipline; final lock deferred until
  test fires per §3.12 implementability check. Pool identification
  is logged at §5.7 `open_inputs` entry #4; the §3.12 layperson-
  test gate is the binding final-lock event."

**Hard rule**: the layperson-test gate either fires (Tested entry)
or is marked Layperson-test-pending — indefinite deferral without
the pending mark is forbidden per §7.8 + §9.6.

The skill aggregates §5.7 `open_inputs` entries into the layer-
wide [`_open_inputs.md`](_open_inputs.md) queue.

**Open inputs do not block draft completion** per locked-plan
§3.8. Exception: refusal-path #1 (source artefact missing /
unlocked) produces only the `open_inputs` entry; the translation
artefact itself is not drafted. Refusal-paths #2-#5 produce
fallback rendering with the limitation recorded.

### 5.8 Section 8 — Visual summary

Per §6.6: "Visual summary present (patient track) or specified
(research track)." Per-track binding:

- **Research-audience**: image strongly preferred; optional if
  claim is fundamentally non-visual. When present: reference
  existing `analyses/.../figures/` plot OR specify axes + what
  the reader should see. When absent: rationale recorded.
- **Patient-audience**: visual is **mandatory and primary**; prose
  supplements. If no visual exists, §5.7 entry #5 logs spec AND
  track may lock as **visual-pending** with fallback.

**Visual specification template** (when to-be-produced):

> *Visual*: <plot type> of <x-axis> vs <y-axis> for <scope>. What
> the reader should see: <pattern supporting source claim>.
> Annotation: <overlay / threshold>. Source: <existing-plot path
> OR "to-be-produced via <script>">.

**Layperson caption** (patient-track). Technical visuals get a
one-line plain-language caption: "Op de horizontale as: mijn
Garmin-stresswaarde. Op de verticale as: mijn gevoelscore die dag.
De rode lijn laat zien dat midden-stress vaak met hogere
gevoelscores samenging." The caption is itself layperson-test-
gated per §5.7.

### 5.9 Section 9 — Follow-up communication

Per locked-plan §3.11 "Stage T" row. Per-track rendering:

- **Research-audience**: keeps source's §3.11 own + external
  tracks; renders for researcher reader. Own preserves pre-reg-
  shape vocabulary; external preserves N=1-limit scoping.
- **Patient-audience**: renders "what is still unknown" framed
  plainly — own-research analogue at patient scale ("ik zou kunnen
  bijhouden..."); external-research analogue as clinician-question
  ("ik kan vragen of er een groepsstudie bestaat..."). Per §6.6:
  "avoids both false hope and counsel-of-despair."

**Worked example — patient-audience follow-up for Stage A source
`construct-bout-recovery-signal.md`** (Dutch):

> *Wat hier nog open staat*: of dit patroon ook prospectief werkt
> als waarschuwing — dus of het signaal vandaag een crash van
> overmorgen aankondigt — is nog niet getest. Tot een
> vooruitkijkende test loopt en resultaat oplevert, blijft het een
> retrospectief patroon, geen waarschuwing.
>
> *Wat ik zelf zou kunnen observeren*: of het patroon ook
> terugkomt in mijn gemediceerde periode (sinds april 2024
> citalopram; het oorspronkelijke patroon zat daarvoor).
>
> *Wat ik aan een behandelaar zou kunnen vragen*: of er een
> CPET-gebaseerd groepsonderzoek bestaat naar bout-niveau herstel
> bij Long COVID dat dit op groepsniveau heeft getest.

Three categories rendered; honest framing without false hope or
counsel-of-despair; methodology vocabulary absent.

### 5.10 Section 10 — Cross-references

Links out to: source artefact (path + lock-version); synthesis-
structure map row for source's stage; plain-language dictionary
(path + terms added/referenced); limitations doc (cited L-IDs via
§5.5); RESEARCH-REPORT §5.2 (when §5.6 fires at tier-2+); the
source-stage guide (#2 for I; #3 for S₁; #4 for S₂; #5 for A);
locked plan (§3.5; **§3.6**; §3.7; §3.8; §3.9; §3.10; §3.11;
§3.12; §4; **§5**; §6.6). The §3.6 citation binds the §6.6 Stage
T halt-criteria (map conflict-resolution at Stage T); the §5
citation binds the output-structure tree (the binding source for
this guide's §3 output-path convention).

**Dictionary update record.** Per-translation audit trail of terms
added or clarified: term + dictionary path + rationale. Dictionary
itself updated at §9.5 protocol.

### 5.11 Section 11 — Subject-narrative commentary translation (patient-audience track ONLY)

**This section is present only on the patient-audience track-file
AND only when the source is Stage A `construct-*.md` with §5.9
commentary filled.** Research-audience track-files: §5.11 is
absent (commentary FORBIDDEN per locked-plan §3.12 hard
separation; §7.3 anti-pattern enforces). Patient-audience track-
files where source has no §5.9 (Stage I / S₁ / S₂ sources, OR
Stage A sources with §5.9 skipped-with-rationale): §5.11 is absent
or carries one line "Commentary section not applicable for this
source."

**When present**, the section renders source §5.9 into the
audience's plain language (per §4.3 base language). Six-element
§3.12 discipline:

1. **Attached-to citation preserved.** Opens with audience-rendered
   "Deze persoonlijke waarneming hoort bij het bovenstaande
   tier-N claim (`<plain-language construct name>`)."
2. **Subject-attribution every sentence.** Dutch "ik merk op";
   "in mijn ervaring"; "in retrospect"; "ik leun ernaar". English
   equivalents per §3.12. Bare third-person forbidden.
3. **Permitted-wording-only.** §3.12 list translated: "ik merk
   op" / "in mijn ervaring" / "in retrospect" / "ik soms" / "het
   patroon hint op / suggereert-niet-bevestigt" / "ik leun naar".
4. **Forbidden-wording-bound.** §3.12 list translated:
   "voorspelt" / "morgen" / "X betekent Y" / any causal-claim or
   forecast-claim wording. Reverted before lock.
5. **Cannot promote tier.** Translation stays at source tier;
   layperson misread-as-prediction triggers commentary REVISION,
   not tier-promotion.
6. **Layperson-test gate fires here specifically.** Per §3.12 +
   §6.6: layperson's interpretation is binding test. §5.7 records
   outcome; revision on failure happens at §5.11.

**Worked example — Stage A source `construct-stress-fatigue-
monitoring.md` §5.9 commentary translation** (Dutch; tier-1):

> *Deze persoonlijke waarneming hoort bij het tier-1 claim
> hierboven (mijn Garmin-stresswaarde en mijn gevoelscore bewegen
> samen).*
>
> Ik merk op dat op dagen waarop mijn Garmin all-day stresswaarde
> in het midden zit (~30-40), mijn gevoelscore vaker in de hogere
> helft landt dan ik op grond van alleen de lage-stress-dagen zou
> verwachten — het patroon hint op de omgekeerde-U vorm die de
> tests hebben opgepikt. In retrospect waren heel-lage-stress-dagen
> vaak "ik bewaar alles" dagen. Ik leun ernaar om Garmin stress te
> gebruiken als een dagelijkse spiegel-aan-mezelf, niet als input
> voor wat morgen komt.

Subject-attribution every sentence; permitted-wording only ("ik
merk op"; "in retrospect"; "ik leun ernaar"); no forbidden wording.

**Worked example — Stage A source `construct-bout-recovery-
signal.md` §5.9 commentary translation** (Dutch; tier-2):

> *Deze persoonlijke waarneming hoort bij het tier-2 claim
> hierboven (mijn bout-hersteldata vertoont een historisch patroon
> met crash-dagen).*
>
> In mijn ervaring zie ik dat wanneer het bout-signaal
> herhaaldelijk "geen terugkeer" op een zware dag laat zien, ik
> soms een crash bemerk binnen de paar dagen daarna — maar het
> verband is iets wat ik in retrospect lees, niet een voorspelling
> waar ik in het moment naar handel. Crash-dagen zijn zeldzaam
> genoeg dat het signaal "afgaan" zelf zeldzaam is. Ik leun ernaar
> om het bout-signaal te zien als een "achteraf-eerlijkheidscheck"
> in plaats van als een prospectieve waarschuwing.

Subject-attribution every sentence; permitted-wording only;
RESEARCH-REPORT §5.2 base-rate context rendered in plain Dutch
preserving the §3.10 tier-2 distinction without forecast wording.

**Layperson-test gate worked example.** Layperson reads the first
commentary and says "Ah, so I should rest when my Garmin stress is
mid-range?" — read as **advice** (forbidden per §3.12 + §7.5).
Revision fires per §3.12 implementability check: commentary
revised to add "dit is een waarneming over mezelf, geen advies"
qualifier; §5.7 layperson-test status block records "Revision
triggered: layperson read as advice; revised wording in §5.11."

## 6. Conflict rules

Per the §6.6 spec brief and the §3.10 + §3.12 + §3.6 layer
bindings, Stage T's conflict rules:

### 6.1 Translation would require a stronger claim than the source allows

> Translation would require a stronger claim than the source allows
> → refuse the translation; log to `open_inputs`. The remedy is
> more evidence (re-run, new HA, forward-validation), not stronger
> wording.

Per locked-plan §6.6. If audience-rendering would require asserting
more than the source carries (e.g., a Stage I PARTIAL verdict
rendered as SUPPORTED-leaning; a Stage S₂ CANNOT-SAY positioning
rendered as "evidence is mixed but leans toward AGREES"; a Stage A
tier-1 monitoring claim rendered with forecast wording), the
translation REFUSES the stronger rendering. §5.7 `open_inputs`
logs what would unlock the stronger claim — typically a source
re-examination triggered via §3.7 drift, OR an upstream stage
revision that the source artefact would need.

### 6.2 Source has CANNOT-SAY positioning → translation says CANNOT-SAY

> Source artefact has CANNOT-SAY positioning → patient track must
> say "we cannot tell you whether..." not "evidence is mixed" or
> other softening that implies more than CANNOT-SAY warrants.

Per locked-plan §6.6. Source's claim shape is the binding ceiling.
A Stage S₂ source with CANNOT-SAY positioning gets a patient-track
rendering that says "we kunnen op grond hiervan niet zeggen of...";
faux-balanced wording ("er zijn aanwijzingen voor beide kanten") is
forbidden per §7.7 anti-pattern. Research-audience track preserves
the source's CANNOT-SAY label verbatim.

### 6.3 Source and dictionary conflict on meaning

> Source artefact and earlier-translated terms in the dictionary
> conflict on meaning → the source artefact wins; the dictionary
> is updated to match and prior translations re-examined (per §3.7
> drift policy).

Per locked-plan §6.6. The source artefact's terminology is the
binding meaning; the dictionary serves the source, not the reverse.
When a term used differently in a new source than in an existing
dictionary entry, the dictionary is updated (with the source-
specific scope noted) and the drift trigger fires for any prior
translation that used the older meaning. The updated dictionary
entry is recorded in §5.10 cross-references + propagated via §9.5.

### 6.4 Layperson-test fails → patient track revised before lock

> Layperson-test fails → patient track is revised before lock; the
> fail-reason is recorded in `open_inputs` so the next translation
> benefits.

Per locked-plan §6.6. The layperson's reading is the binding test
of the patient-audience track's wording. When the layperson reads
a paragraph as forecast / advice / patronising / dismissive of
uncertainty, the paragraph is REVISED before lock. The fail-reason
+ revised wording are logged at §5.7 layperson-test status block;
the failure becomes drafter-knowledge for future translations
(carried via §3.7 drift to the dictionary if a term-level
misreading caused the failure).

Commentary translation (§5.11) is the highest-risk surface for
layperson-test failure per §3.12 implementability check; commentary
revision on test failure is the §3.12 binding gate.

### 6.5 Commentary translation conflict with source §5.9

When the patient-audience §5.11 commentary translation would
require wording that the source's §5.9 did NOT carry (e.g.,
audience-clarity would benefit from a sentence the source did not
include), the source §5.9 is the binding ceiling. Stage T does NOT
add commentary content beyond what the source carried; if the
audience needs additional content, the routing is via §3.7 drift
back to the source's `construct-*.md` §5.9 for revision, NOT
in-translation commentary expansion. Commentary REVISION-AT-
TRANSLATION-TIME applies only when the layperson-test fires per
§6.4; it does not apply to drafter judgment of what would "improve
the commentary."

### 6.6 Source-stage map-change-needed

When per-translation Stage T work reveals the synthesis-structure
map needs changing (rare at Stage T; mostly happens at S₁ / S₂ /
A), Stage T HALTS and routes the change to a separate producer-
mode map-revision session per locked-plan §3.6. **Concrete halt-
criteria** at Stage T:

1. **Source artefact's stage cell in the map is wrong** — e.g.,
   the map declares the source's cluster / topic / construct under
   one categorisation, but the source's actual content reads as a
   different categorisation. Stage T halts; routes the issue to
   the source's stage for revision via §3.7 drift; Stage T resumes
   on the revised source.
2. **The source artefact's L-ID block contradicts the map's L-ID
   notes column** — e.g., the source cites L5 NA but the map's
   L-ID notes record L5 applies. Stage T halts; routes the
   contradiction to source-revision via §3.7 + source-stage
   review; resumes after reconciliation.

**Route-out instructions.** Stop drafting mid-session; do NOT save
a partial artefact; do NOT edit the map in-session; do NOT edit
the source in-session. Produce only the §5.7 `open_inputs` entry
naming the proposed source-or-map change. Hand off to the user
with the halt-criterion that triggered and the proposed change.
Resume only after a separate producer-mode session updates the
source / map with its own `/research-methodology-review` or
`/research-review` pass before re-lock.

## 7. Anti-patterns explicitly forbidden

The following moves are forbidden in any Stage T translation. One
paragraph each per the brief's density-discipline guidance.

### 7.1 Tier upgrading in wording

Per locked-plan §6.6 + §3.10. Using predictive-sounding language
for a monitoring-tier source ("watch for X" can be predictive in
disguise; "track X" is monitoring; "X has historically appeared
alongside Y" is informative-pattern). The Stage A backdoor-
predictive-claims anti-pattern (guide #5 §7.5) propagates here
verbatim — Stage T MUST NOT render wording that exceeds the
source's tier. Patient-audience track is highest-risk because
plain-language rendering can drift toward forecast-sounding
phrasings without methodology-vocabulary anchors; §5.3 + §5.4
rendering discipline plus the layperson-test gate per §5.7 are the
operational defences.

### 7.2 Faux-balanced wording

Per locked-plan §6.6. "Evidence is mixed", "more research is
needed", "the picture is unclear" used to soften an honest source
call is forbidden. If the source artefact made a clear call
(SUPPORTED / REJECTED / CONCORDANT / AGREES / DIVERGES / tier-N),
the translation states the call clearly in the audience's
vocabulary; if the source said CANNOT-SAY or INCONCLUSIVE, the
translation says so explicitly. "Mixed evidence" rendering of a
clear source-call collapses the source's epistemic discipline; it
is patronising even when motivated by "softening for accessibility"
(see §7.7).

### 7.3 Research-audience track carrying §3.12 commentary

Per locked-plan §3.12 hard separation + §6.6 spec brief
*"commentary is forbidden in research-audience translation track"*.
Research-audience track-files MUST OMIT the source's §5.9
commentary block; rendering commentary content into a research-
audience reader's prose is the load-bearing prohibition that
§3.12 + §6.6 establish. The §5 outline ends at §5.10 cross-refs
for research-audience track; §5.11 commentary section is absent.
§9.6 lock-gate enforces. **Why this anti-pattern is load-bearing**:
research-audience readers consume the source's formal claim +
caveats + L-IDs as analytical input; smuggling commentary into
their read blurs the §3.12 epistemic-category separation between
patient-facing nuance and research-defensible claim.

### 7.4 Commentary translated to predictive wording

Per §3.12 hard separation + §6.6: commentary cannot backdoor §3.10
even in translation. §5.11 commentary stays within §3.12 permitted-
wording ("ik merk op" / "I notice"; "in mijn ervaring"; "in
retrospect"; "ik leun naar"); §3.12 forbidden wording ("voorspelt"
/ "predicts"; "morgen" / "tomorrow"; "X betekent Y") reverted
before lock. Audience-rendering produces plain-language equivalents
of permitted wording, NOT looser wording. Layperson-test fires on
commentary per §5.7; failure → REVISION (not relaxation) per §6.4.

### 7.5 Translation framed as advice

Per locked-plan §6.6 + Stage A §7.2 inherited. Patient-audience
track-files MUST NOT render the source's tier claim as advice
("rust nu" / "rest now"; "vermijd X" / "avoid X"; "doe Y" / "do
Y"). The source artefact licenses what the subject may safely
**say about the signal**, not what to **do** with it; Stage T
inherits this prohibition unchanged. Advice-rendering is the
load-bearing risk at patient-audience track per §4.2 forbidden-
wording list; §5.4 NOT-DO refusals rendering AND §5.11 commentary
translation are the two highest-risk surfaces; layperson-test
fires on advice-misread per §5.7 + §6.4.

### 7.6 Inventing new caveats post-hoc

Per §6.6. Caveats come from locked source (I §4.5; S₁ §4.5; S₂
§4.6+§4.7; A §5.4+§5.11). New caveats invented at Stage T —
neither in source nor limitations doc — forbidden. Source-missing
caveat routes via §3.7 drift to source-stage revision, NOT through
translation prose. **Exception**: layperson-test wording-
clarification sentences (disambiguate source claim for audience
without narrowing reach) are logged at §5.7+§5.11, not as caveats.

### 7.7 Stripping uncertainty for "accessibility"

Per locked-plan §6.6. Laymen handle uncertainty when framed
honestly; removing it patronises and misleads. Patient-audience
track-files MUST NOT collapse the source's honest-uncertainty
content into false-confident wording for "ease of reading." A
Stage S₂ source's CANNOT-SAY positioning rendered as a confident
"this is what we know" is forbidden per §6.2; a Stage A tier-1
monitoring source rendered as "use this to plan tomorrow" is
forbidden per §7.1 + §7.5. **Why this anti-pattern is load-
bearing**: the very PAIS-patient audience the patient-track exists
to serve has typically read more health literature than the
non-PAIS reader assumes; stripping uncertainty insults the reader
AND mis-equips them for clinic conversations or daily-life
decisions.

### 7.8 Indefinite layperson-test deferral

Per locked-plan §6.6 + §3.12 implementability check. The
layperson-test gate either fires (§5.7 Tested entry with §6.4
revision-on-failure operationalised) OR the patient-audience
track-file is marked **layperson-test-pending** explicitly per
§5.7 status block. Indefinite deferral without the pending mark is
forbidden: a patient-track artefact that locks with neither a fired
test nor an explicit pending status has bypassed the §3.12
discipline. §9.6 lock-gate enforces.

### 7.9 Audience definition that is generic

Per locked-plan §6.6 + §4.4 specificity binding. "General public" /
"general researcher" / "patients" / "anyone interested" is forbidden
as audience definition; the wording-discipline cannot calibrate to
a generic reader and the layperson-test gate cannot fire against a
generic layperson persona. §5.2 audience-definition section MUST
name a specific persona with named prior knowledge; §9.6 lock-gate
enforces.

### 7.10 Methodology-jargon in patient-audience track

Per locked-plan §6.6 spec brief: "treating the plain-language
dictionary as optional — undefined jargon in patient-audience track
is a failure mode, not a stylistic choice." Patient-audience track-
files MUST NOT leave methodology terms undefined (PPV / NPV / N-of-
1 / monitoring-tier / informative-pattern / L-IDs by ID / etc.); a
term used MUST have a plain-language replacement OR an inline
definition AND a dictionary entry. The dictionary entry is the
pre-requisite for the patient-track translation of that term per
§2 input #5 + §9.6 lock-gate.

### 7.11 Quoting the source artefact's prose unchanged

Per locked-plan §6.6. Translation is **re-writing for the
audience**, not **excerpting**. A research-audience track-file
that copy-pastes the source's prose without re-framing for the
audience has not produced a translation; a patient-audience track-
file that copy-pastes source prose has produced an inaccessible
text. Both tracks MUST re-frame the source's content for the
audience's vocabulary and questions; verbatim-quote use is
permitted ONLY for §5.1 source-claim citation + §5.5 L-ID-block
verbatim-quote-from-source (which the audience-rendering then
applies in §5.5's per-track rendering).

### 7.12 Producing only one audience track

Per locked-plan §6.6 spec brief: "producing only the research-
audience track — 'the patient version can come later' is how the
patient track never gets written. Both tracks are produced or the
skip is explicit." Both tracks are produced per source artefact;
OR the skip-research-internal decision is recorded explicitly per
§3 output-block; §9.6 lock-gate enforces. The patient-track is
NOT optional; the only mechanism to omit it is the source's
recorded skip-research-internal decision, which itself is an
explicit decision the user signs off on.

### 7.13 Patronising tone toward the patient audience

Per locked-plan §6.6. Laymen are not children; PAIS patients in
particular have often spent years reading their own medical
literature. Patient-audience track-files MUST NOT use tone that
talks down to the audience (over-explanation of self-evident
concepts; childlike sentence structures unless cognitive-load
reduction warrants; over-use of "u" / formal Dutch with audience
personas who would prefer "je" / informal). Per §5.2 audience-
definition: the audience persona's lived expertise sets the tone
calibration; deference to the audience's expertise is the
discipline, not patronisation. Layperson-test fires on tone per
§5.7 + §6.4.

### 7.14 Cross-language drift within a single track-file

Per §4.3 base-language binding. A single track-file mixes languages
only when the audience-definition explicitly requires it (e.g., a
patient-track file for a Dutch-speaking PAIS-patient persona who
will cite the file in an English-language clinic conversation —
rare). Default: the §5.2-declared base language carries through
every section of the track-file. Mixed-language drift WITHOUT
audience-definition warrant is forbidden per §9.6.

### 7.15 Re-routing source artefact to a different stage in-translation

Per §3 dependency rule: the source artefact's stage is read from
the source's path (interpretation / synthesis / contextualisation
/ actionability). Stage T does NOT re-categorise the source in-
stage; if the source's stage assignment is wrong, the §6.6 halt-
and-route applies. Editing the source in-session (or silently
treating the source as if it were a different stage) is forbidden.
Construct-level analogue of guide #5 §7.13.

## 8. Interview-prompt seeds

The `/research-interpret translate <source-path>` skill drives the
translation as an interview. Three required seeds per the locked-
plan §6.6 spec brief, plus an optional fourth for commentary-
eligible Stage A sources.

### 8.1 Audience-selection interview

> "Who specifically is this for? What do they already know? What
> will they ask after reading the first paragraph? Per the §4.4
> specificity binding, name the persona with named prior knowledge
> and named likely first-read questions — for each track separately.
> Per §4.3 base-language heuristic, what base language fits this
> audience persona?"

**Use.** Drives §5.2 for both tracks. Skill walks the audience
persona definition for each track in turn; refuses the "general
public" / "general researcher" framing per §7.9 + §9.6. Records
the persona, prior knowledge, likely first-read questions, and
base language. Skill cross-checks against the source artefact's
content to ensure audience-fit (e.g., a Stage A tier-2+ source
needs a research-audience persona who has quality-measure literacy
per §5.6; a patient-audience persona who can read the RESEARCH-
REPORT §5.2 plain-language frame).

### 8.2 Plain-language rendering interview

> "What is the single most important sentence this audience needs
> to take away? If they remember only one thing, what is it? Which
> technical term from the source artefact does this audience not
> have? What is the plain-language replacement?"

**Use.** Drives §5.3 + §5.10 dictionary-update. Skill walks the
source's primary claim sentence; surfaces the technical-term
candidates (per the source's content); asks the user to draft
plain-language replacements OR to mark the term as needing inline
definition. For every term added: skill appends to dictionary via
§9.5 protocol; records cross-reference at §5.10. Skill flags
terms whose dictionary entry conflicts with source meaning per
§6.3.

### 8.3 Layperson-test scheduling interview

> "Per the §10.7 per-artefact resolution, who plays the layperson
> for this patient-audience track-file? Is the test scheduled
> before this lock cycle, OR is the artefact going to lock as
> layperson-test-pending? If scheduled: what is the test pool
> identifier, what date, what wording-section will fire the test?"

**Use.** Drives §5.7 layperson-test status block. Skill walks the
test pool identification per the user's per-artefact decision
(specific PAIS peer; non-PAIS layperson; both — per locked-plan
§10.7 leaving this to per-artefact judgment); records pool +
schedule + which §5 section fires the test (typically §5.3 core
claim + §5.11 commentary if present + §5.4 caveats). If pool not
identified: skill records layperson-test-pending status with the
§7.8 anti-pattern reminder that indefinite deferral is forbidden.
For commentary-carrying patient-tracks: skill specifically
schedules the §5.11 layperson-test per §3.12 implementability
check.

### 8.4 Optional seed — commentary-rendering interview (Stage A sources with §5.9 filled)

> "Source carries §5.9 subject-narrative commentary attached to
> tier-N claim. Walking the patient-audience §5.11 translation:
> what is the plain-language equivalent of each commentary
> sentence, preserving subject-attribution and permitted-wording-
> only discipline? Are there §3.12 forbidden-wording risks in the
> plain-Dutch rendering ('voorspelt' / 'morgen' / etc.) that need
> reverting?"

**Use.** Drives §5.11 (patient-track only). Skill skips this seed
if source is not Stage A, OR source is Stage A but §5.9 is
skipped-with-rationale, OR research-audience track is being
drafted (commentary FORBIDDEN per §7.3). When user proceeds, skill
walks the §3.12 discipline per sentence: subject-attribution check;
permitted-wording check; forbidden-wording flagging; layperson-
test scheduling per §8.3 specifically for the commentary block.
Skill refuses to lock if any §3.12 discipline rule is violated
per §9.6.

## 9. Agent-instruction outline

What `/research-interpret translate <source-path>` (produced in
§11 step 7) codifies into skill behavior. Compact phase-list form
per the brief's density-discipline guidance.

### 9.1 Load

In order: the source artefact at `<source-path>` (must be locked);
the source's stage (I / S₁ / S₂ / A — read from path); the
synthesis-structure map row for the source (per stage indirection
in §2 input #3); the limitations doc §3 + §5 row for translation
artefacts; the plain-language dictionary; the relevant methodology
MDs (guides #1-#5 + any source-cited construct-specific MDs); the
RESEARCH-REPORT §5.2 PPV-with-base-rate precedent (when source is
Stage A tier-2+); CONVENTIONS §1, §1.2, §2.1, §4.2, §4.3.

**Bootstrap responsibility for `plain_language_dictionary.md`.**
The first Stage T session may find that the plain-language
dictionary does not yet exist on disk (the dictionary is a live
artefact maintained by Stage T sessions per §5 of guide #6 + §3.12
of plan r5; it has no separate creator). The skill MUST scaffold
the empty dictionary at `docs/research/methodology/plain_language_dictionary.md`
on first invocation when not present — with a minimal header
(status: live artefact, producer-mode, maintained by `/research-interpret
translate` invocations) and an empty body table (one row per term).
Subsequent Stage T invocations load and append to it. The
bootstrap is a one-time skill responsibility; once scaffolded, the
dictionary persists across sessions per the normal producer-mode
discipline. **Alternative bootstrap pathway**: if step 7 skill
build (per §11 step 7) prefers, the scaffold may be added there
as a sibling task ("scaffold `plain_language_dictionary.md` empty
artefact before any `/research-interpret translate` invocation
fires"); the §9.1 first-invocation-scaffold path is the fallback
when the skill build does not pre-scaffold.

### 9.2 Gate

Source artefact locked + research_line_limitations.md exists →
§9.3. Source artefact missing or not locked → halt; produce only
§5.7 `open_inputs` entry per refusal-path #1 (source missing /
unlocked). Source-stage map-change-needed surfaces (per §6.6
halt-criteria) → halt; produce only §5.7 entry per refusal-path
#1 variant + route-out instructions.

### 9.3 Extract

Source artefact: §-claim verbatim per stage (Stage I §3; S₁ §4.7a;
S₂ §4.5; Stage A §5.3); §-caveats per stage; §-L-ID block per
stage; §-follow-up per stage (Stage I §8; S₁ §4.8; S₂ §4.9; Stage
A §5.8); §-commentary if source is Stage A with §5.9 filled. Map
row: tier aspiration + §3.12 commentary-eligibility (Stage A
sources) + L-ID notes column. Dictionary: terms used in the source
+ entries; gap-list of source-used terms missing from dictionary.

### 9.4 Interview

Walk §8 seeds in order: §8.1 (audience-selection per track + §5.2
+ §4.4 specificity check); §8.2 (plain-language rendering + §5.3
+ §5.10 dictionary-update); §8.3 (layperson-test scheduling +
§5.7); §8.4 (optional commentary-rendering for Stage A sources
with §5.9 + §5.11 + §3.12 discipline checks). For each seed:
record articulation; cross-check against §4 track mapping rules +
§6 conflict rules + §7 anti-patterns; surface mismatches; seek
rephrasing.

Skill MUST NOT autonomously fill §5.3 plain-language replacements
(user articulates; dictionary records), §5.7 layperson-test pool
(user identifies per §10.7), §5.11 commentary rendering (user
articulates per §3.12 permitted wording; skill flags forbidden
wording).

### 9.5 Produce

Draft both `analyses/translation/research-audience/<source-
name>.md` AND `analyses/translation/patient-audience/<source-
name>.md` per §5. All ten sections filled on research-audience
track (§5.11 absent per §7.3); all ten sections filled on patient-
audience track AND §5.11 if source is Stage A with §5.9 filled.
Status: DRAFT r1, reviewer-mode-with-authorization, `## Authorship`
per CONVENTIONS §1.2.

**Dictionary update protocol.** For every plain-language replacement
or inline-definition added in §5.3 / §5.4 / §5.5 / §5.11 of either
track: append the term to `plain_language_dictionary.md` with the
Dutch + English entries + the source-scope note + the date. Record
the term + dictionary path in this translation's §5.10 cross-
references.

### 9.6 Refuse-to-lock gate

Skill refuses to mark ready for completion if any of the
twenty-three items below fires. Per-category headers added for
scannability (categories are not separate gates — each item is
the binding check):

**Items 1-2: source + audience binding**

- §5.1 source-artefact citation missing OR source-claim sentence
  not verbatim from source.
- §5.2 audience-definition is generic ("general public" / "general
  researcher" / "everyone" — §4.4 specificity binding + §7.9
  anti-pattern).

**Items 3-4: plain-language translation + caveats**
- §5.3 plain-language translation uses methodology vocabulary
  without dictionary entry or inline definition (patient-audience
  track only; §7.10 anti-pattern + §2 input #5 binding).
- §5.4 caveats invent new caveats not in source (§7.6 anti-pattern).

**Items 5-6: L-ID binding**

- §5.5 L-ID rendering omits a source-cited L-ID (§3 hard rule).
- §5.5 L-ID rendering adds an L-ID the source did not cite (§3
  hard rule + §7.6 anti-pattern).

**Items 7-8: quality-measure binding (when source is Stage A tier-2+)**

- §5.6 quality-measure translation missing when source is Stage A
  tier-2+ (§3.10 binding via source).
- §5.6 patient-audience track-file uses bare percentages without
  base-rate context (§7.4 anti-pattern variant; RESEARCH-REPORT
  §5.2 precedent binding).

**Items 9-11: layperson-test + visual binding (patient-audience track)**

- §5.7 layperson-test status block missing on patient-audience
  track (must be either Tested entry OR Layperson-test-pending
  entry; §7.8 anti-pattern + §3.12 implementability check).
- §5.7 patient-audience track locks with indefinite deferral
  (neither Tested nor Layperson-test-pending; §7.8 anti-pattern).
- §5.8 visual missing on patient-audience track without §5.7
  visual-pending entry (§5.8 binding + visual-pending fallback
  unrecorded).

**Items 12-16: §3.12 commentary discipline (patient-audience track ONLY)**

- §5.11 commentary section present on research-audience track-file
  (§3.12 hard separation + §7.3 anti-pattern).
- §5.11 commentary section uses forbidden §3.12 wording on patient-
  audience track (§7.4 anti-pattern + §3.12 + §6.4 layperson-test-
  fail revision unfired).
- §5.11 commentary section's subject-attribution missing on any
  sentence (§3.12 binding + §7.4 anti-pattern).
- §5.11 commentary section's attached-to citation missing (§3.12
  + §5.11 binding).
- §5.11 commentary's layperson-test gate not fired per §5.7
  layperson-test status block (§3.12 implementability check).

**Items 17-19: wording-discipline anti-pattern enforcement**

- §5.3 / §5.4 / §5.11 contains advice-form wording (§7.5 anti-
  pattern + Stage A §7.2 inherited).
- §5.3 / §5.4 / §5.11 contains tier-upgrading wording (§7.1 anti-
  pattern + §3.10 hard predictive gate).
- §5.3 / §5.4 / §5.11 contains faux-balanced wording softening a
  clear source call (§7.2 anti-pattern).

**Items 20-23: cross-cutting structural enforcement**

- §5.5 / §5.6 patient-audience track-file uses methodology jargon
  without plain-language rendering (§7.10 anti-pattern).
- Track-file uses cross-language mixing without audience-definition
  warrant (§4.3 base-language binding + §7.14 anti-pattern).
- Translation includes verbatim source prose without re-framing for
  audience (§7.11 anti-pattern; exceptions: §5.1 source-claim;
  §5.5 source L-ID block).
- Only one track produced without explicit skip-research-internal
  decision recorded at source (§7.12 anti-pattern + §3 output
  binding).
- Patronising tone in patient-audience track per §5.2 audience
  persona's expertise calibration (§7.13 anti-pattern).
- Any §5 section contains anti-pattern violations per §7.

### 9.7 Review handoff

On user-accepted-as-ready-for-completion: recommend fresh-session
`/research-review` per locked-plan §4 (translation artefacts get
`/research-review` plus layperson-test where patient-audience track
exists). Report lands at `docs/research/reviews/translation-
<source-name>-<track>-YYYY-MM-DD.md`. For patient-audience track-
file with commentary translation: the layperson-test (per §5.7
status block) is the additional gate beyond /research-review per
the locked-plan §4 row.

### 9.8 Acceptance + drift-trigger registration

Per §3.8: "user explicitly accepts" is the binding completion
event. On acceptance: status → LOCKED; §5.7 `open_inputs`
propagate to layer-wide `_open_inputs.md`; §5.10 dictionary-update
records propagate to `plain_language_dictionary.md` lock; the
limitations doc §8 downstream-citation-count increments for each
L-ID rendered in §5.5 (manual-pending-skill per limitations doc
§8 worked example). Per §3.7, four re-examination triggers
register at lock:

1. Source artefact re-examined or revised.
2. Plain-language dictionary term shift that affects this
   translation's content (per §6.3 conflict rule).
3. A cited methodology MD changes lock-version (especially the
   limitations doc, the source-stage guide, the locked-plan
   §3.10 / §3.12 if revised).
4. ≥6 months elapse since lock.

Patient-audience track-files with §5.11 commentary translation
add a fifth trigger: layperson-test re-test reveals previously-
undetected forbidden-wording or advice-misread (per §3.12
implementability check); revision triggered per §6.4.

**Drift-trigger registration is manual-pending-skill.** Until §11
step 7 lands, the §10 lock log carries a "Drift triggers
registered" line. The skill also increments the limitations doc's
§8 downstream-citation-count for each of the L-IDs rendered in
§5.5 (manual until skill lands).

## 10. Cross-references

- [`_plan_results_analysis_layer.md`](_plan_results_analysis_layer.md)
  — §6.6 (spec brief); §3 (stage-map dependency + skip-research-
  internal); §3.5 (missing-inputs — five refusal paths at §5.7);
  §3.6 (map pre-reg + §6.6 above conflict-resolution); §3.7
  (drift — four triggers, five for commentary-carrying patient-
  tracks); §3.8 (completion criteria); §3.9 (limitations binding —
  source's L-ID ceiling); §3.10 (**hard predictive gate** — §7.1 +
  §7.4); §3.11 (follow-up per-track at §5.9); **§3.12 (commentary
  layer — patient-track ONLY; §5.11 + §6.4 + §6.5 + §7.3 + §7.4
  operationalise; layperson-test gate per §5.7 implements §3.12
  implementability check)**; §4 (producer/reviewer split); §9
  anti-patterns; §10.6 + §10.7 (deferred questions resolved at
  §4.3 + §2 input #7 + §5.7); §11 step 6.6.
- Guides #1-#5 (LOCKED r2): [`descriptive_precondition_audit.md`](descriptive_precondition_audit.md)
  (Stage D upstream-most chain);
  [`verdict_to_inference.md`](verdict_to_inference.md) (guide #2;
  Stage I source type);
  [`internal_synthesis.md`](internal_synthesis.md) (guide #3;
  Stage S₁ source type);
  [`external_contextualisation.md`](external_contextualisation.md)
  (guide #4; Stage S₂ source type);
  [`actionability_translation.md`](actionability_translation.md)
  (**guide #5; most common upstream source**; Stage A source
  type; §5.7 quality measures → Stage T §5.6; §5.9 commentary →
  Stage T §5.11 patient-track ONLY per §3.12 + §7.3).
- [`research_line_limitations.md`](research_line_limitations.md) —
  §3 seven L-IDs; §5 binding for translation artefacts (per-track
  rendering at §5.5); §8 downstream-citation-count.
- [`synthesis_structure_map.md`](synthesis_structure_map.md) — §3
  cluster table (S₁ source); §4 topic table (S₂ source); §5
  construct table (A source — tier aspiration, §3.12 commentary-
  eligibility, L-ID notes).
- [`plain_language_dictionary.md`](plain_language_dictionary.md) —
  live dictionary maintained by Stage T (locked-plan §4 row); §2
  input #5 + §5.10 + §9.5 protocol.
- [`RESEARCH-REPORT.md`](../RESEARCH-REPORT.md) §5.2 — PPV-with-
  base-rate precedent ("wrong 24 times out of 25"); load-bearing
  for §5.6 at tier-2+ sources.
- [`personal_hypotheses.md`](../personal_hypotheses.md) §32 — HA-
  test-level prohibition on classifier-discrimination measures
  (inherited via Stage A).
- [`hypothesis_lock_process.md`](hypothesis_lock_process.md) —
  forward-validation HA pre-reg (inherited via Stage A §5.5).
- [CONVENTIONS.md](../CONVENTIONS.md) §1, §1.2, §2.1, §4.2, §4.3
  as cited throughout.
- Literature methodology anchors at
  [`literature/methodology/`](../literature/methodology/): Daza
  2018 (N-of-1-to-group reach); CENT 2015 items 21+22 (L-ID
  rendering); SCRIBE 2016 (L4 transparency); Natesan 2023
  (defensibility bar); WWC 2022 SCED (inherited via S₂).
- [`bout_level_recovery_dynamics.md`](bout_level_recovery_dynamics.md);
  [`citalopram_phase_stratification.md`](citalopram_phase_stratification.md);
  [`symptom_mention_asymmetry.md`](symptom_mention_asymmetry.md)
  — construct-specific methodology; relevant when source touches
  the corresponding cluster.

## 11. Lock log

| Date | Event | Note |
|---|---|---|
| 2026-06-25 | Drafted r1 | Producer-mode by fresh agent per §11 step 6.6 of [`_plan_results_analysis_layer.md`](_plan_results_analysis_layer.md) (r5 LOCKED). **Guide #6 of six — the LAST guide in §11 step 6**. **Seven inventions beyond §6.6 spec**: §4.5 two-track summary table; §5 ten-section outline; §5.7 layperson-test status block with Tested-vs-Layperson-test-pending discipline; §5.10 dictionary-update record; §5.11 §3.12 commentary translation section as patient-track-only with six-element discipline; §6.6 source-stage map-change-needed halt rule; §9.6 twenty-three-item refuse-to-lock gate. Worked examples: K-stress-fatigue-monitoring tier-1 + K-bout-recovery-signal tier-2 Stage A source translations. **Three §6.6 spec ambiguities resolved**: (a) output path uses locked-plan §5 output-structure tree (parallel `research-audience/` + `patient-audience/` folders); (b) §10.6 plain-language base language deferred at guide level with per-artefact heuristic; (c) §10.7 layperson-test recruitment-pool resolved as per-artefact judgment with §7.8 anti-pattern preventing indefinite deferral. **Skill-precondition note**: the `/research-interpret translate` skill must land at §11 step 7 before any Stage T artefact can be drafted. |
| 2026-06-25 | Fresh-session `/research-methodology-review` | Verdict REVISION RECOMMENDED (mild). Report: [`reviews/methodology-translation_to_audience-2026-06-25.md`](../reviews/methodology-translation_to_audience-2026-06-25.md). **Three critical confirmations**: (a) §3.12 patient-audience-ONLY commentary separation holds at six enforcement layers; (b) layperson-test gate operationally implementable as either-fired or explicitly-pending-marked; (c) layer-closure clean (all five prior guides cross-referenced, D → I → S₁ → S₂ → A → T flow named, outputs fully specified). **Two required actions**: R1 — `plain_language_dictionary.md` does not yet exist on disk; first Stage T session needs bootstrapping responsibility named (or sibling task at §11 step 7); R2 — §5.7 enumeration of five refusal-to-proceed paths omits the §6.6 source-stage map-change-needed case (§5.7 ↔ §6.6 ↔ §9.2 inconsistency). **Four recommended**: A1 length 44 over upper bound, ~30-50 lines compressible (deferred per pattern); A2 §5.10 omits §3.6 + §5 from plan citations; A3 §9.6 23-item gate per-category headers for scannability; A4 §11 lock-log scannability split. None blocks §11 step 6 closure. |
| 2026-06-25 | Revised r1 → r2 | Both required absorbed: **R1** — §9.1 added bootstrap-responsibility paragraph: the skill MUST scaffold `plain_language_dictionary.md` on first invocation when not present, with minimal header + empty body table; sibling-task alternative at §11 step 7 noted explicitly. **R2** — §5.7 added sixth refusal-path for source-stage map-change-needed surface during Stage T, citing §6.6 halt-criteria and the §3.6 conflict-resolution rule pathway; distinct from refusal-path #1 because the source IS locked but the map-source binding is wrong. Three of four recommended absorbed: A2 — §5.10 plan citation list extended to (§3.5; §3.6; §3.7; §3.8; §3.9; §3.10; §3.11; §3.12; §4; §5; §6.6) with one-sentence bind rationale; A3 — §9.6 reorganised with seven per-category headers (source+audience; plain-language+caveats; L-ID; quality-measure; layperson-test+visual; §3.12 commentary discipline; wording-discipline; cross-cutting structural enforcement); A4 — this lock-log split into per-event paragraphs. A1 density compression deferred per reviewer's "for future revision pass" framing. |
| 2026-06-25 | **LOCKED r2 — closes §11 step 6** | User acceptance ("Absorb all (2 required + A2/A3/A4 recommended; defer A1 compression), lock r2, close step 6"). Status of all sections LOCKED. **§11 step 6 closes — the six-guide methodology arc (D → I → S₁ → S₂ → A → T) is complete and all six guides are LOCKED r2.** No second-pass review per established Option-γ pattern. **Drift triggers registered** (manual-pending-skill): constituent source artefact (Stage I / S₁ / S₂ / A) re-examined; layperson-test fires for layperson-test-pending entries; cited methodology MD changes lock-version (especially the five upstream guides, research_line_limitations.md, synthesis_structure_map.md, _plan_results_analysis_layer.md); plain-language dictionary churn at meaningful scale; ≥6 months elapse since lock. **Layer ready for §11 step 7 (skill build for `/research-interpret` with six-stage routing per plan r5 §7).** |
