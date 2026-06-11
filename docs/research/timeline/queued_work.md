# Queued research work

Items deferred from active triage / methodology sessions. Each entry
captures the **what**, the **why we queued instead of doing**, and
enough context to pick it up later without re-deriving.

This file is **not** the methodology and **not** a TODO list for code
changes. It tracks **research follow-ups** that emerged during triage
and were explicitly deferred.

## Q1. Pre-register symptom-mention asymmetry hypotheses as HA-files

**Status**: queued — do **not** create HA-files yet.

**Context**: Two interpretation hypotheses were added to methodology §3a
on 2026-06-11 as informal guidance:

1. **Brainfog-hidden-dip hypothesis**: gevoelscore-4 days where the
   note mentions `brainfog` / `duf hoofd` / `wazig hoofd` /
   `vergeetachtig` / `niet helder` are candidate sub-threshold dips
   (the day score sits at 4 because brainfog suppresses it from 5,
   not because of somatic pain).
2. **Muscle-pain crash-precursor hypothesis**: days where the note
   mentions `spierpijn` / `zere benen` / `zwaar in de benen` /
   `dof gevoel` may show elevated crash/dip probability in the
   following 1-3 days, even when the mention-day score is
   unremarkable.

Both are framed in methodology §3a as **interpretation rules** for now,
not formal pre-registered hypotheses.

**Why queued**: formal pre-registration (in the style of
[HA01b](../garmin/hypotheses/HA01b-exertion-shock/) or
[HA02](../garmin/hypotheses/H02b-stress-spikes/)) requires:

- A pre-specified discrimination threshold ("considered SUPPORTED if
  X% of mention-days lead to a dip within 72h, vs Y% of mention-free
  control days")
- A train/validate era split
- A complete corpus to test on — which means **after the 2022 triage
  round lands** so all 4 years are covered

**When to do**: after 2022 per-day intensity triage completes (last
remaining triage year), at which point both the corpus and the
v2-tagged symptom mentions can be queried in full.

**Where to put when done**:

- `docs/research/garmin/hypotheses/HA-brainfog-hidden-dip/`
- `docs/research/garmin/hypotheses/HA-muscle-pain-crash-precursor/`

**Cross-refs**:

- Methodology §3a (interpretation rule, current home)
- v2 category dictionary entries for brainfog, spierpijn, zere benen
- `labels_crash_v2.csv` for the existing dip / crash labels
- `sub_threshold_dips.csv` for the manually-marked dips (small N now,
  grows with each triage round)

## Q2. Hidden-dip review on quasi_crash_context days [PARTIAL COMPLETE 2026-06-11]

**Status**: partial complete. Conservative resolution: 8 brainfog-mention
days marked as `dip_type=brainfog` in
[`data/sub_threshold_dips.csv`](data/sub_threshold_dips.csv) on 2026-06-11.
21 ambiguous candidates (no brainfog/muscle-pain mention but classifier
flagged) **deliberately not labeled** per user choice — keeps the
§3a training-label set high-specificity instead of inflating with
"moe/groggy" days that lack the canonical PEM-symptom-cluster anchor.

**What was queued vs what was done**:

- Original count (queued doc): 88 quasi_crash_context days across all
  years.
- After cross-checking against `labels_crash_v2.csv` crashes/dips +
  existing `sub_threshold_dips.csv`: **29 candidates remained** (203
  dates already labeled, much higher coverage than originally
  estimated).
- Of those 29: **8 had brainfog mentions** in original or triage notes
  (the §3a-relevant signal).
- All 8 were added to sub_threshold_dips.csv with `dip_type=brainfog`.
  The remaining 21 were not added.

**Implication for Q1 (HA-pre-registration)**: there are now 8 explicit
brainfog-typed dips as the training-label set for the brainfog-hidden-
dip hypothesis (in addition to the existing 27 `general` dips). 8 is
small but enough to pre-register and run an initial discrimination
test; if the signal is real, the test should be detectable at this
N. 0 muscle-pain mentions were found in the candidate set — the
muscle-pain-crash-precursor hypothesis (also Q1) has no training
labels yet from this review, so its formal pre-registration depends
on either expanding the regex or accepting that the user does not
typically describe muscle pain in note text.

(Original context kept below for traceability.)

---

**Status**: queued — review needed.

**Context**: After the 2023 triage round (2026-06-11),
[`data/triage_notes_classified_2023.csv`](data/triage_notes_classified_2023.csv)
placed **69 days into the `quasi_crash_context` bucket**: gevoelscore
≤ 4 with crash-signal words (`hoofdpijn`, `moe`, `brainfog`, `naproxen`,
etc.) in the original `day_entries.note` text, but where during triage
the user wrote a non-committal `no data that signifies load` or similar.

These are the operational candidates for the brainfog-hidden-dip
hypothesis (Q1.1): the score sits at 4 with crash-like symptoms but
nothing was tagged as a load. Many may be hidden dips.

**Why queued, not auto-merged**: the classifier flagged them via
heuristic regex, not via user judgement. Treating them as confirmed
sub-threshold dips would inject high-uncertainty entries into
[`data/sub_threshold_dips.csv`](data/sub_threshold_dips.csv) and
contaminate downstream statistical analyses. The user has to confirm
each one.

**Workflow when ready**:

1. Filter `triage_notes_classified_2023.csv` to `bucket = quasi_crash_context`.
2. Surface as a focused review sheet (date + original note +
   current score + crash-signal word that triggered classification).
3. User confirms per row: real hidden dip → `mark_dip` action; not a
   dip → leave; needs context but not a dip → `add_to_context`.
4. Re-run [`scripts/process_triage_actions.py`](scripts/process_triage_actions.py)
   2023.

**Same review owed for**: 2024 (21 quasi_crash_context), 2025
(9 quasi_crash_context), 2026 (count not re-tallied; see classifier
output). 2023's 69 is the largest year, reflecting that 2023 was deep
in the stabilisation period with many low-but-not-crashed days.

**Cross-refs**:

- Methodology §3a (the hypothesis these days are evidence for)
- Q1 (formal pre-registration depends on this review for clean training
  labels)

## Q3a. Energie-allocatie shift — RESOLVED as qualitative methodology context [2026-06-11]

**Status**: resolved without a timeline annotation.

**Resolution trail**:

1. Initially proposed as a timeline umbrella span (2023-10-09 → 2023-12-08)
   marking the user's energy-priority shift.
2. Shipped briefly with label "Energie-allocatie shift (van all-to-work
   naar split met recovery)", category `levensgebeurtenis`.
3. On reflection: this is a **qualitative context note**, not a discrete
   event. The shift was gradual over weeks/months and lacks crisp
   boundaries; treating it as a span misrepresents continuous priority
   change as a discrete event.
4. Span removed from `triage_events.csv` (2026-06-11). The qualitative
   context is preserved in methodology §3b under "Qualitative context: a
   gradual shift in personal energy-allocation".

**Related but separate**: the dossier review independently established
that work-incapacity and PEM-crash are *always* distinct constructs (not
only after the shift), validated by the user's choice to label the
16-day June 2023 "volledig ziek" period as `levensgebeurtenis` rather
than `crash`. That construct-distinction is the load-bearing methodological
finding from this review, captured in §3b.

(Original context kept below for traceability.)

---

**Status**: queued — depends on dossier review outcome (Q3b).

**Context**: During PwC dossier review on 2026-06-11, a fundamental
methodological insight surfaced: the user's energy-allocation strategy
shifted between approximately October 2023 and December 2023 from
"nearly all available energy to work" to "split with family +
active recovery", as the realisation of chronic illness set in. The
2023-12-08 "extra event" (dossier-documented) is the formal acceleration
catalyst.

**Why it matters**: this shift is the **interpretive boundary** for
cross-validation between work-incapacity records (PwC, Arbo Unie) and
gevoelscore-based subjective state records. Before the shift these two
constructs map ~1-1; after the shift they diverge. Without naming the
shift as a discrete annotation, future analysts (including future-you)
will not know where the lens needs to change.

**Proposed annotation shape**:

- span 2023-10-09 (SMB consult: "20u/wk = plafond" — first formal
  acknowledgement that opbouw to AD-target had stopped) → 2023-12-08
  ("extra event"; sterke toename beperkingen)
- label: "Energie-allocatie shift (van all-to-work naar split met recovery)"
- category: `levensgebeurtenis` (umbrella, background context)
- note: methodology §3b interpretive boundary

**Why queued, not done**: depends on the dossier review (which is in
progress); once the user confirms the December 2023 events as either
crash or rebalanced-uitval, the shift annotation can be placed with a
cleaner end-date.

**Cross-refs**:

- Methodology §3b interpretive lens for cross-validation
- [`data/pwc_dossier_review.csv`](data/pwc_dossier_review.csv) — the
  rows under review that bracket this period
- queued_work Q5 (the general methodology question this raises)

## Q3b. Umbrella-span review for 2024 + 2025 [COMPLETE 2026-06-11]

**Status**: complete. Conservative result: one umbrella added,
`Angela-spanning 2024 (umbrella)` 2024-06-06 → 2024-11-24, category
`levensgebeurtenis`.

**Method**: keyword-clustering across single-day events in 2024-2025.
15 candidate clusters surfaced; on review:

- **Strong thematic cluster (1)**: `angela` keyword, 4 events Jun-Nov
  2024, captured as the umbrella above.
- **Family-name clusters (3)**: Jantine, Tijmen, Tobias — high event
  counts but not thematic; just people who appear in many events.
  Rejected.
- **Generic activity-type clusters (4)**: sailing, weekendje, eten,
  koffie — recurring activities without a unifying narrative.
  Rejected.
- **Friend-pair clusters (2)**: hans+mat — fixed social group, weak
  signal. Rejected.
- **Generic-relation clusters (3)**: kids, kinderen, gezin — too broad.
  Rejected.

**Why so conservative**: methodology §4 advises "at most 2-3 concurrent
umbrellas per period". The Angela umbrella adds one concurrent span
during a period already covered by PwC reintegration 2023 ending in
nov 2023 and Q3a-era qualitative context (which is now methodology-
only, not an annotation). One new umbrella is the right ceiling.

**Output file kept for traceability**:
[`data/umbrella_candidates_2024-2025.csv`](data/umbrella_candidates_2024-2025.csv)
— the 15 candidate clusters with the user-review columns; one row
(`angela`) was actioned, rest left as is.

(Original context kept below for traceability.)

---

## Q3b (original). Umbrella-span review pattern for 2024 + 2025

**Status**: queued — methodology-level question, do when 2022 lands.

**Context**: 2023's 8 PwC-Amsterdam visits surfaced the need for an
**umbrella span** ("PwC reintegratie 2023") covering thematically
related but non-consecutive events. Added 2026-06-11.

The same pattern likely applies to:

- 2024: "issues with angela" appears across May (24), Aug (19),
  Nov (24) — three discrete events on a long-running theme. Worth
  an umbrella?
- 2024: relatiecoach met Jantine spans multiple sessions (umbrella
  already exists in HAND_CURATED, verify span end-date)
- 2025: Hornbach + werkzaamheden aan huis spans, if any clusters
  appear across the year

**Why queued**: identifying umbrellas requires a step back from
per-day triage and is best done after all 4 years are landed, so the
full event-population is visible.

**Cross-refs**:

- Methodology §4 (event-label conventions, umbrella pattern)
- Methodology §9 (hand-curated entries — long-running umbrellas often
  end up here)
- `merge_calendar_triage.py` HAND_CURATED_SPANS_POST_2022 list

## Q6. Blind re-code gate on per_day_intensity loads

**Status**: queued — worth doing, **not a blocker** for current
research.

**Context**: Independent advisor review (received 2026-06-11, at
[docs/research/review/longcovid_analysis_strategy from an independent advisor.md](../review/longcovid_analysis_strategy%20from%20an%20independent%20advisor.md))
§4.1 asks for a hindsight / leakage gate on any retrospectively coded
load variable. Proposed mitigation: pull ~30-40 random days, strip
dates + neighbouring context + research labels, re-score loads from
the note text alone (separate rater or an LLM with no timeline
access), then check (i) agreement with original scores and (ii)
whether the load → crash association survives blinding, and by how
much it shrinks.

The critique applies to `per_day_intensity.csv` because load values
were applied 2026-06 by the user looking back over events 2022-2026.
This produces a known **backfill-recency bias** already documented in
[README.md](README.md): older events have less fine-grained load
attribution than recent ones.

**Why not blocking**: the methodology already locks in the strongest
single defense against hindsight-induced differential measurement
error — the [§2 rule](methodology.md) that **load = event intensity,
not after-effect severity**. A wedding gets the same loads whether or
not it triggered a crash, because the loads describe the event, not
the consequence. This rule was locked on 2026-06-10 after an explicit
inconsistency was caught (the overload-labeling suggestion that would
have used 1-3 for "overload severity"). Combined with the README
backfill-recency caveat and the PwC objective-parallel cross-validation
(§3b), the leakage threat is materially smaller than the advisor's
framing assumes. We have followed strict protocols throughout.

The blind re-code is still **worth running** as a defensive empirical
check — it converts a methodological argument ("we followed strict
protocols") into a quantitative one ("re-coded loads agree with
originals at X%, and the load → crash association shrinks by Y pp
under blinding"). Stronger evidence and worth the cost, but not
required to keep moving.

**Why queued**: running the re-code now would delay the active
hypothesis pipeline (Q1 brainfog-hidden-dip + muscle-pain-crash-precursor
HA-files, Q2 quasi_crash_context review, the next round of precursor
tests using per_day_intensity as exposure). The advisor's gate is a
**confirmation-of-validity check**, not a precondition. Running it
*after* a body of load-based findings exists also makes it more
informative — we can quantify shrinkage on specific reported claims
rather than against a hypothetical.

**Workflow when ready**:

1. Sample 40 days stratified across years 2022-2026 (8 per year), with
   at least 10 days that have a coded load and at least 10 with blank
   loads, to test both directions of agreement.
2. Strip date, day-of-week, surrounding 7 days of notes, all research
   labels (crash_v2, sub_threshold_dips, annotations.yaml events),
   shuffle order.
3. Re-score cog/phy/emo 1-3 from note text alone — ideally a separate
   rater. If using an LLM, use a session with no project context.
4. Compare to originals: agreement (κ or weighted κ for ordinal scale),
   mean absolute deviation per axis, systematic-bias direction (does
   the rater systematically over- or under-rate?).
5. For any load-bearing load → outcome association, re-run on the
   re-coded subset. Report shrinkage in pp.
6. If shrinkage is substantial (> 30%), the claim is biased upward and
   the result.md gets a quantitative caveat. If small, the load coding
   has held up.

**When to do**: after Q1 pre-registration lands and the first round
of per_day_intensity-as-exposure precursor tests has run. Earlier if
a specific load-based finding becomes load-bearing for a card.

**Cross-refs**:

- [Independent advisor review §4.1](../review/longcovid_analysis_strategy%20from%20an%20independent%20advisor.md)
- Methodology [§2](methodology.md) — the locked event-intensity-not-after-effect rule that is the primary defense
- [README](README.md) backfill-recency-bias caveat — the honest acknowledgement of differential temporal accuracy
- Methodology §3b PwC cross-validation — the partial §4.2 objective-parallel gate already run
- Q1 — the first downstream tests that would benefit from the re-code result

## Q5. Cross-validation lens: external behavior vs internal state

**Status**: queued — methodology-level guidance, applies to every future
objective source.

**Context**: The 2026-06-11 PwC dossier review surfaced that an objective
log can measure one of two related-but-distinct phenomena:

- **External behavior**: hours worked, kilometers run, sleep duration,
  meeting attendance. What the user **did** that day.
- **Internal state**: how the user felt, energy level, symptom presence.
  What the user **experienced** that day.

The PwC log + dossier are behavior-focused (work-incapacity). The
gevoelscore + day_entries.note are state-focused. The two correlate
strongly when energy-allocation is concentrated (e.g. all-to-work), and
diverge when energy is consciously rebalanced.

**Implication for any future objective source we integrate** (Garmin
training-load, sleep windows, calendar exports from other employers,
biometric streams, etc.):

1. Classify the source as **behavior** or **state** before designing
   cross-validation.
2. For behavior sources: expect divergence from gevoelscore in periods
   where energy-allocation is split. This divergence is not error — it
   is the signal.
3. For state sources: expect closer convergence, with deviations more
   likely to indicate measurement gaps.

**Why queued, not done**: this is methodology guidance, not a workflow.
It will be added to §3b once we have at least one more objective source
to validate the framing.

**When to do**: at the integration of the next objective source
(probably Garmin training-load extract or Garmin sleep windows).

**Cross-refs**:

- Methodology §3b interpretive lens (introduced 2026-06-11)
- Q3a (the first instance of this divergence: 2023-10 → 2023-12)

---

*Add new queued items with a `Q<n>` header following the same shape:
**status**, **context**, **why queued**, **when / workflow**, **cross-
refs**. Drop items when they ship by replacing the body with a one-
line redirect to where the work landed.*
