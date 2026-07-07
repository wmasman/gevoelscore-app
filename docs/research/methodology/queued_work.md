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
output). 2023's 69 is the largest year by some margin, reflecting
many low-but-not-crashed days that year.

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
`Relational-spanning 2024 (umbrella)` 2024-06-06 → 2024-11-24, category
`levensgebeurtenis`.

**Method**: keyword-clustering across single-day events in 2024-2025.
15 candidate clusters surfaced; on review:

- **Strong thematic cluster (1)**: one relational-themed keyword,
  4 events Jun-Nov 2024, captured as the umbrella above.
- **Family-name clusters (3)**: three household-member name
  aggregations — high event counts but not thematic; just people
  who appear in many events. Rejected.
- **Generic activity-type clusters (4)**: sailing, weekendje, eten,
  koffie — recurring activities without a unifying narrative.
  Rejected.
- **Friend-pair clusters (2)**: hans+mat — fixed social group, weak
  signal. Rejected.
- **Generic-relation clusters (3)**: kids, kinderen, gezin — too broad.
  Rejected.

**Why so conservative**: methodology §4 advises "at most 2-3 concurrent
umbrellas per period". The relational-spanning umbrella adds one
concurrent span during a period already covered by PwC reintegration
2023 ending in nov 2023 and Q3a-era qualitative context (which is now
methodology-only, not an annotation). One new umbrella is the right
ceiling.

**Output file kept for traceability**:
[`data/umbrella_candidates_2024-2025.csv`](data/umbrella_candidates_2024-2025.csv)
— the 15 candidate clusters with the user-review columns; one row
(the relational-themed cluster) was actioned, rest left as is.

(Original context kept below for traceability.)

---

## Q3b (original). Umbrella-span review pattern for 2024 + 2025

**Status**: queued — methodology-level question, do when 2022 lands.

**Context**: 2023's 8 PwC-Amsterdam visits surfaced the need for an
**umbrella span** ("PwC reintegratie 2023") covering thematically
related but non-consecutive events. Added 2026-06-11.

The same pattern likely applies to:

- 2024: a recurring relational-tension theme appears across May (24),
  Aug (19), Nov (24) — three discrete events on a long-running theme.
  Worth an umbrella?
- 2024: relatiecoach sessions span multiple sessions (umbrella
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
[docs/research/reviews/longcovid_analysis_strategy from an independent advisor.md](../reviews/longcovid_analysis_strategy%20from%20an%20independent%20advisor.md))
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

- [Independent advisor review §4.1](../reviews/longcovid_analysis_strategy%20from%20an%20independent%20advisor.md)
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

## Q7. HeartMath-paired validation of the Garmin sleep-stress HRV proxy

**Status**: queued — depends on Q7's predecessor (in-corpus descriptive
validation per [`hrv_proxy_via_stress.md`](hrv_proxy_via_stress.md) § 7
Checks 7.1-7.4). Run the in-corpus checks first; only run the
HeartMath-paired validation if the in-corpus checks support the proxy
direction (option (b) → option (c) in the methodology doc § 9).

**Context**: The methodology proposal in
[`hrv_proxy_via_stress.md`](hrv_proxy_via_stress.md) argues
`stress_mean_sleep` is a usable HRV proxy on the Forerunner 245 /
Elevate V3 sensor despite the absence of nightly HRV Status. The
proposal's effect-size degradation estimate (≈0.6× the equivalent
HRV-direct effect size) is literature-derived (Rosenbach et al. 2025
on the Vivosmart 4, *Stress and Health*, Wiley) and not yet
calibrated to the user's specific sensor + physiology.

The user owns a HeartMath device (Inner Balance / emWave class) that
exports raw inter-beat-interval (IBI) data per session. Paired
HeartMath IBI + Garmin stress measurements over the same wallclock
windows would give the **direct n-of-1 calibration** the methodology
proposal currently lacks.

The user is currently wearing the FR245 daily, so paired sessions are
operationally feasible at any time.

**What it validates**:

- Personal r between Garmin stress (3-min resolution) and
  HeartMath-derived RMSSD (60-sec windows). Removes the Rosenbach
  cross-subject SD (0.42) as a concern by replacing it with a point
  estimate.
- Algorithm/sensor calibration: same Firstbeat algorithm, Elevate V3
  input. If the algorithm produces a meaningful HRV-derived output
  from V3 in the user's wrist-fit + skin-pigment + perfusion
  conditions, this is direct evidence.
- HR confound, locally. With paired IBI you can compute mean HR and
  RMSSD separately per window; partial-r(stress, RMSSD | HR) isolates
  the HRV-specific component.

**What it does NOT validate**:

- Different timescale: HeartMath gives ~10 min at 3-min Garmin
  resolution. The methodology proposal is about 7-hour
  `stress_mean_sleep` aggregates. Minute-level coupling is necessary
  but not sufficient for the nightly-mean proxy to work.
- State-space coverage: HeartMath sessions are typically at-rest or
  coherence-breathing — a narrow band of physiological state.
- Cross-time portability: HeartMath data is recent; the master is
  2022-onward. The user's physiology may differ between years, which
  limits the HeartMath calibration's generalisation across the
  earlier corpus.

**Protocol when ready**:

Sessions:
- Minimum **3 paired sessions**, ideally **5-8** across conditions.
- Mix conditions: at least one "calm baseline" (HeartMath without
  coherence protocol), one "active coherence" (breathing protocol),
  and one "post-activity" (15 min after a walk / stair-climb, HR
  elevated, RMSSD suppressed).
- Span at least a week so day-to-day variation is sampled.
- Flag any sessions that fall on PEM/dip/crash days — gold for the
  validation.
- Optional but high-value: one paired session including a deliberate
  stressor (camera speaking, mental arithmetic, or POTS-tolerable
  stand-up) to push GSS into the 50-70 range that the H-tests
  actually probe.

Exports:
- HeartMath: raw IBI per session with start-timestamp. Inner Balance
  and emWave both export this; confirm which the user owns.
- Garmin: per-minute or per-3-min stress trace for the matching day
  (FIT `stress_level` message via the existing pipeline). Resting HR
  / windowed HR around the session for the HR-covariate analysis.

Analysis steps:
1. Compute RMSSD per 60-sec window from HeartMath IBI. Drop windows
   with < 30 IBI samples.
2. Compute mean HR per 60-sec window from HeartMath IBI (60000 / mean
   RR).
3. Extract Garmin stress for the same wallclock window. Resample to
   match HeartMath's 60-sec grid (linear interpolation between
   Garmin's 3-min points).
4. Per session: Pearson + Spearman correlation between RMSSD and
   stress.
5. Per session: partial Spearman correlation, controlling for HR.
6. Across sessions: pool per-session r values; report median + IQR
   (small n; median more informative than mean).

Decision rule (median session r, Spearman, partial on HR):

- r ≤ −0.5 → strong proxy; move to option (c) of methodology § 9.
- −0.5 < r ≤ −0.3 → moderate proxy; option (c) with ~0.5× effect-size
  degradation flagged in pre-regs.
- −0.3 < r < 0 → weak proxy; stay at option (a).
- r ≥ 0 → no proxy; option (a) permanently, audit doc updated.

Practical flags:
- Clock alignment: HeartMath and Garmin clocks may drift; confirm
  offset via session-start HR spike alignment before correlating.
- Breathing-protocol artefact: coherence breathing drives HF + RMSSD
  upward; Garmin algorithm not tuned for paced breathing. Report
  active-coherence vs passive sessions separately.
- 3-min Garmin resolution: single 10-min session → only ~3 stress
  data points. Pooling across 5+ sessions is required for usable
  estimate.
- Do not normalise to baseline before pooling — between-session
  variance is the main test.

**Why queued**: § 7.1-7.4 in the methodology doc (in-corpus
descriptive validation on existing master columns) is faster, lower-
risk, and gates this. If in-corpus checks show `stress_mean_sleep`
does not even carry the basic exertion signal (Check 7.1) or
collapses entirely under `resting_hr` control (Check 7.2), the
HeartMath-paired validation has nothing to refine and is moot. Run
the in-corpus tier first.

**When to do**:
- After in-corpus § 7.1-7.4 checks land AND
- Either the in-corpus checks support the proxy direction (option
  (b) → (c) gating), OR
- The in-corpus checks are inconclusive and the user wants a
  stronger signal before deciding.

**Where to put when done**: extension of
[`hrv_proxy_via_stress.md`](hrv_proxy_via_stress.md) as § 7.5, or
spun out as `hrv_proxy_heartmath_validation.md` in the methodology
folder if the protocol grows into its own pre-registered analysis.

**Cross-refs**:

- [`hrv_proxy_via_stress.md`](hrv_proxy_via_stress.md) § 7 (the
  in-corpus prerequisite checks) and § 9 (the three decision options
  this calibrates between).
- [`garmin_indicators_audit.md`](garmin_indicators_audit.md) § HRV —
  hardware blocked (the doc that would be revised under option (c)).
- [`../wiggers_testable_hypotheses.md`](../wiggers_testable_hypotheses.md)
  B-block + H1, H4, H5 — the pre-reg entries this would unblock
  under option (c).
- Rosenbach et al. 2025, *Stress and Health* (Wiley) — the
  group-level r ≈ −0.6 anchor we are trying to localise to n=1.

## Q9. Reproduce Wiggers' PEM vs non-PEM visual comparison plots on personal data

**Status**: queued — research question, not yet scoped. Surfaced
2026-06-12 during Wiggers verify-pass batch 2.

**Context**: Wiggers' Stress chapter (PDF lines 1106-1110,
[`../literature/wiggers_pacing_handleiding.pdf`](../literature/wiggers_pacing_handleiding.pdf),
local-only) shows "No PEM" vs "with PEM" side-by-side plots for the
same person — Garmin stress traces visually contrasted across the two
states. Wiggers' plots use Garmin-pattern-derived PEM labelling. **Our
crash labels come from a different source**: self-report via `crash_v2`
(gevoelscore ≤ 3 for ≥ 2 consecutive days; 29 crashes). Reproducing
Wiggers-style same-person comparison plots on our data would test
whether the two unrelated labellings (self-report vs Garmin-pattern)
converge on the same physiological signatures.

The research question is therefore not "can we make a pretty plot" but
**does cross-source label convergence hold for this corpus?** If
`is_crash=True` days produce the same intraday Garmin signature
Wiggers shows on her PEM days, that's independent confirmation that
the self-report labels track real PEM events, not self-report
artefacts. If the signatures diverge, the labels mean something other
than "physiological PEM" — which is itself important to know.

**Why queued, not done**: requires (i) per-minute intraday extraction
from FIT (may already exist as a Wave 4 intermediate, needs
verification before assuming Wave-5 work), (ii) matching machinery for
same-DOW within-baseline-window crash/non-crash pairs, (iii) plot-
rendering pipeline. Sizable enough to warrant explicit scoping and
acceptance criteria rather than ad-hoc work.

**What it would deliver**:

- **Aggregate panel**: mean intraday stress / BB / HR trace across all
  29 crashes vs across matched non-crashes, with 95% CI bands.
  Statistically defensible single chart; tests population-level
  signature.
- **Example panel** (Wiggers-style): 6-9 matched crash/non-crash
  example pairs, same person, similar baseline period, contrasted
  side-by-side. Visually narrative; supports the aggregate.
- **Dip-granularity check** (bonus): same machinery on `is_dip=True`
  days. Do dips show a muted signature, or none? Tests whether the
  crash/dip 2-tier scheme is physiologically justified.
- **Raw + z-scored variants** per
  [[feedback_relative_not_absolute]]: two rows per metric in the
  panels — raw (Wiggers-comparable) and z-scored-vs-personal-baseline
  (PEM-research-relevant).

**Workflow when ready**:

1. **Check per-minute extraction availability**: do Wave 4
   intermediate outputs include per-minute stress / BB / HR traces, or
   only daily aggregates? If only aggregates, plan a Wave-5 extension
   off the existing FIT pipeline.
2. **Matching spec**: for each crash day, find a matched non-crash
   neighbour within ± 2-3 weeks (same calendar window), same day-of-
   week, similar prior-week `exertion_rank_composite_lagged` (within
   one quartile). Random pair selection across 4 years would conflate
   PEM signature with multi-year baseline drift.
3. **Aggregate analysis**: per metric (stress, BB, HR), align all 29
   crash days at t=0 (define: sleep-onset or wake), average trace
   across crashes and across matched non-crashes, plot with 95% CI
   bands.
4. **Example panel**: pick 6-9 of the matched pairs with strongest
   contrast on the aggregate, render Wiggers-style two-column plots.
5. **Dip extension**: repeat with `is_dip=True` days.
6. **Crash-distortion sensitivity row** per
   [[feedback_crash_distortion_sensitivity]]: quantify aggregate-CI-
   band overlap between crash and non-crash means. Strong non-overlap
   = strong cross-source convergence.

**Acceptance criteria**:

- All 29 crashes covered by at least one matched non-crash pair, OR
  clear documentation of which crashes had no acceptable match and
  why.
- Per-metric aggregate plot with 95% CI bands; report effect-size
  summary (Cohen's d on the daily-mean reduction, or paired-band
  separation index).
- Example panel with at least 6 pairs that visually contrast.
- Methodology note: matching algorithm + Wave-5 extraction spec (if
  new) + plot-rendering reproducibility info.

**Where to put when done**:
`docs/research/analyses/descriptive/cross_source_label_validation_visual/`
— descriptive analysis folder; sits before any hypothesis pre-reg per
[[feedback_descriptive_before_inference]].

**Cross-refs**:

- [`../literature/wiggers_pacing_handleiding.pdf`](../literature/wiggers_pacing_handleiding.pdf)
  lines 1106-1110 — the source plots
- [`../wiggers_testable_hypotheses.md`](../wiggers_testable_hypotheses.md)
  § Source verification log (batch 2) — where this question surfaced
- [`../analyses/hypotheses/crash_v2-definition/`](../analyses/hypotheses/crash_v2-definition/)
  — the labels being cross-validated
- Q1 — the brainfog-hidden-dip hypothesis would benefit from the same
  per-minute extraction infrastructure if this work creates it

## Q10. Historical pre-reg cross-check under the new validation framework

**Status**: queued — descriptive cross-check; no automatic re-locking.

**Context**: With [`train_validate_split_fate.md`](train_validate_split_fate.md) replacing the 2023-12-31 train/validate split with single-pool primary on Stratum 4, and [`permutation_null_block_length.md`](permutation_null_block_length.md) introducing stationary-bootstrap E[L]=7 as the day-resampling layer, the historical locked verdicts (HA01b, HA02c, HA08, HA11, H05) were computed under a different framework. The cross-check produces one side-by-side report of locked verdict vs the same primitive computed under the new framework.

**Why queued**: implementation needs (i) the data-driven block-length companion estimator (see Q13), (ii) the Stratum-4 single-pool re-run of each primitive, (iii) the side-by-side report template. Sizable but bounded.

**Binding recipe** (per [`train_validate_split_fate.md`](train_validate_split_fate.md) §5):
- Output: one table with rows = locked pre-regs (HA01b, HA02c, HA08, HA11, H05); columns = `locked verdict`, `verdict under MD 2 + MD 3 framework`, `divergence (yes/no)`, `brief note on the source of divergence`.
- No automated re-locking of any historical verdict. Original `result.md` files unchanged.
- On divergence: name plausible drivers descriptively (block scheme, single-pool vs split, multiplicity threshold, finite-sample variability). Do NOT pick which framework is "correct".
- User-owned decision on follow-up actions.

**Where to put when done**: `docs/research/analyses/_cross_checks/historical_under_new_framework.md` + supporting `*.csv`.

**Cross-refs**:
- [`train_validate_split_fate.md`](train_validate_split_fate.md) §5 (the binding recipe)
- [`permutation_null_block_length.md`](permutation_null_block_length.md) (the block-length policy being applied)
- [`wiggers_test_design_on_chained_regime.md`](wiggers_test_design_on_chained_regime.md) § Cross-cutting statistical hygiene §§ 1-4 (the new framework rules)
- [primary-verdict-statistics.md](../analyses/garmin_exploration/cards/primary-verdict-statistics.md) (the locked verdict statistics)

## Q11. Bootstrap CI finite-sample coverage calibration at n=29

**Status**: queued — methodology empirical check; one-time exercise.

**Context**: [`permutation_null_block_length.md`](permutation_null_block_length.md) commits to stationary-bootstrap E[L]=7 with 95% CI as the default reporting interval. Bootstrap consistency is asymptotic. At n=29 crash episodes, empirical coverage of the nominal 95% interval may be materially below 95%. Without a calibration simulation we cannot put an honest number on the coverage gap; CI widths get reported as-computed with only the asymptotic caveat.

**Why queued**: the methodology choice (stationary bootstrap) does not depend on the simulation; what depends is how honestly we report CI coverage. Lower priority than the active pre-reg pipeline.

**Workflow**:
1. Specify a synthetic data-generating process matching our corpus shape (n=29 events, daily resolution, weekly-cyclic ACF, mild non-stationarity over ~1700 days).
2. Define a known ground-truth effect size on a test discrimination statistic (Cohen's d on the daily diff).
3. Repeat B=2000: simulate, compute stationary-bootstrap 95% CI at E[L]=7, check coverage of true effect.
4. Report empirical coverage at nominal 95% with std-error band.
5. Sweep E[L] in {3, 5, 7, 10, 14} to confirm 7 is in the flat region of the coverage curve.
6. Document as `bootstrap_coverage_calibration.md` + one-line empirical-coverage caveat back into MD 2 § Operational consequences.

**Where to put when done**: `docs/research/methodology/bootstrap_coverage_calibration.md` + `docs/research/analyses/_calibration/bootstrap_coverage_at_n29/`.

**Cross-refs**:
- [`permutation_null_block_length.md`](permutation_null_block_length.md) § 4.4 (the n=29 limitation acknowledged)
- Q10 (the historical cross-check uses the new framework; its report can cite the coverage simulation)

## Q12. Westfall-Young step-down multiplicity correction as descriptive overlay

**Status**: queued — sensitivity overlay; NOT used to relax primary verdict threshold.

**Context**: [`wiggers_test_design_on_chained_regime.md`](wiggers_test_design_on_chained_regime.md) § Cross-cutting statistical hygiene §§ 3 locks Holm step-down on N_eff ≈ 4 as the primary multiplicity correction. WY step-down uses the joint permutation distribution to absorb correlation structure directly, potentially relaxing thresholds slightly further. WY is more powerful under correlated tests but couples multiplicity policy to block-length policy and adds permutation complexity. Marginal uplift over Holm-on-N_eff is small (estimated 1-3 pp of threshold relaxation; the big multiplicity win was Holm/Bonferroni-on-N_eff vs naive-N, captured in the primary policy).

**Why queued, not primary**: per MD 2 weighting, defensible-over-powerful favours Holm; cross-hypothesis comparability favours Holm; decoupling-from-block-length favours Holm. WY is run as a descriptive overlay characterising the gap, not to relax primary verdicts.

**Workflow** (when first new pre-reg lands):
1. Build joint block-permutation distribution over the primitives in the family using the same E[L]=7 stationary scheme as the primary null.
2. Compute the empirical distribution of min p-value across primitives per permutation.
3. Per observed test, compute WY-corrected p as P(min permuted p < observed p).
4. Report Holm-corrected p and WY-corrected p side-by-side in the result file.

**Decision rule**: WY is NOT used to relax the primary verdict. If a primitive's verdict hinges on the Holm-vs-WY gap, report both side-by-side and the user owns the decision. If both clear or both fail, the WY column is descriptive context with no operational impact.

**Promote to primary only if**: (a) future N_eff CI sensitivity (Q14) shows N_eff is materially uncertain, (b) literature fetch (Q17) surfaces strong support for joint-distribution-based correction in n-of-1 designs specifically, or (c) a specific primitive's verdict consistently sits in the Holm-vs-WY gap.

**Cross-refs**:
- [`wiggers_test_design_on_chained_regime.md`](wiggers_test_design_on_chained_regime.md) § Cross-cutting §§ 3
- [cross-channel-correlation.md](../analyses/garmin_exploration/cards/cross-channel-correlation.md) (N_eff ≈ 4 source)
- Q14 (N_eff bootstrap CI)

## Q13. Permutation-null block-length override threshold operationalisation

**Status**: queued — single deterministic rule needed.

**Context**: [`permutation_null_block_length.md`](permutation_null_block_length.md) § Decision allows per-hypothesis override of the global E[L]=7 default when "the metric's empirical autocorrelation crosses zero at a lag substantially different from 7 (e.g. < 3 or > 14 days at lag |corr| < 0.1)". This mixes two operational definitions (zero-crossing vs first-lag-below-threshold). For the override to be a script-computable rule, one operationalisation must be chosen.

**Why queued**: not load-bearing until a hypothesis hits the override path. No hypothesis currently uses the override. Pick the rule when the first override candidate appears.

**Candidate operationalisations**:
1. First lag at which `|ρ̂(h)| < c · √(log n / n)` with c ≈ 1.96 (Politis-White convention). Deterministic; data-driven; closed-form.
2. AR(1) integrated autocorrelation time τ. Different convention; less restrictive for slowly-decaying ACFs.
3. Zero-crossing of ρ̂(h). Simpler but more sensitive to small-sample noise.

**Workflow**:
1. Pick one (default: option 1).
2. Document in `permutation_null_block_length.md` § Decision with the formula and a worked example.
3. Implement as a single function `compute_acf_override_E_L(metric_series)` returning `None` (no override; use 7) or the override E[L].
4. Pre-regs that invoke override cite the function + the formula.

**Cross-refs**:
- [`permutation_null_block_length.md`](permutation_null_block_length.md) § Decision (the override rule)
- Q17 / [`_pending_literature_fetch.md`](_pending_literature_fetch.md) P2 (Patton-Politis-White data-driven block length)

## Q14. Bootstrap CI on the effective-N-of-channels estimate

**Status**: queued — sensitivity check on a load-bearing methodological quantity.

**Context**: The Holm-on-N_eff multiplicity correction treats N_eff ≈ 4 as a fixed input. N_eff itself is an estimate from [cross-channel-correlation.md](../analyses/garmin_exploration/cards/cross-channel-correlation.md) on Stratum 4 data, with finite-sample noise. If 95% CI on N_eff brackets {2, 3, 4, 5, 6}, the multiplicity threshold can swing across that range.

**Why queued**: at N_eff ≈ 4 the Holm threshold (α ≈ 0.0125) is unlikely to flip a verdict that wouldn't also flip at N_eff = 3 (α ≈ 0.0167) or 5 (α ≈ 0.01). Becomes load-bearing when a borderline verdict appears.

**Workflow**:
1. Block-bootstrap the cross-channel-correlation analysis (B = 1000) using stationary bootstrap on the underlying daily series.
2. Per replicate, re-derive N_eff using the same effective-independence formula as the point estimate.
3. Report N_eff point estimate + 95% CI.
4. If the CI bracket flips a borderline verdict (Holm threshold crosses observed p at some plausible N_eff), flag in a sensitivity row.

**Where to put when done**: extension of [cross-channel-correlation.md](../analyses/garmin_exploration/cards/cross-channel-correlation.md) with N_eff CI table.

**Cross-refs**:
- [cross-channel-correlation.md](../analyses/garmin_exploration/cards/cross-channel-correlation.md) (the point estimate)
- [`wiggers_test_design_on_chained_regime.md`](wiggers_test_design_on_chained_regime.md) § Cross-cutting §§ 3 (Holm threshold dependent on N_eff)
- Q12 (WY overlay — relevant comparison if N_eff CI is wide)

## Q15. Per-channel lag profiling on autonomic primitives — H5 Tier 2 → Tier 1 promotion gate

**Status**: queued — descriptive work; gates H5 priority-shortlist tier promotion.

**Context**: H5 (per-metric lag-profile ordering BB/stress ≤ RHR < HRV) is source-verified but currently Tier 2 because [lag_profile_report.md](../analyses/garmin_exploration/activity-labels/output/lag_profile_report.md) covers the HA01 exertion-axis lag distribution only — NOT autonomic-channel lag profiles. Per-channel CCF on `bb_overnight_gain`, `stress_mean_sleep`, `resting_hr` vs the exertion proxy is the missing descriptive piece for H5.

**Why queued**: descriptive-before-inference. Once per-channel lag profiles are characterised on Stratum 4, H5 can move to Tier 1 (or be demoted, if the implicit ordering doesn't survive the descriptive pass) before any H5 pre-reg.

**Workflow**:
1. Predictor: `exertion_rank_composite_lagged_lcera` (continuous, first-differenced).
2. Per-channel CCF on lags -10 … +10 days on each of `bb_overnight_gain`, `stress_mean_sleep`, `resting_hr` (all first-differenced) per [`wiggers_test_design_on_chained_regime.md`](wiggers_test_design_on_chained_regime.md) § Class 1 CCF.
3. Report `argmax-ρ` per channel + 95% CI from stationary bootstrap (E[L]=7).
4. Compute the ordering descriptively (smallest absolute `argmax-ρ` lag first).
5. Output: `lag_profile_autonomic.md` — descriptive characterisation, NOT a pre-reg.

**Decision after descriptive pass**:
- Ordering supports H5's implicit BB/stress ≤ RHR claim → H5 promotes to Tier 1.
- Ordering contradicts the claim → H5 stays Tier 2; H5's pre-reg becomes a refutation test rather than a confirmation test.
- Inconclusive (overlapping CIs) → H5 stays Tier 2 with a note documenting why.

**Where to put when done**: `docs/research/analyses/garmin_exploration/activity-labels/output/lag_profile_autonomic.md`.

**Cross-refs**:
- [`wiggers_testable_hypotheses.md`](../wiggers_testable_hypotheses.md) § Priority shortlist Tier 2 (H5 promotion gate)
- [lag_profile_report.md](../analyses/garmin_exploration/activity-labels/output/lag_profile_report.md) (the existing exertion-axis report)
- [`wiggers_test_design_on_chained_regime.md`](wiggers_test_design_on_chained_regime.md) § Class 1 CCF (the canonical method)

## Q16. Seasonality-decomposed Garmin-only baseline contrasts (Strata 1 vs 3 vs 4)

**Status**: queued — descriptive work; methodologically required for any Stratum 1 vs Stratum 3/4 comparison. **Partly superseded 2026-07-02:** the R23 follow-up decomposition ([`../analyses/longrun_rhr_trend/`](../analyses/longrun_rhr_trend/)) now handles seasonality as a **modelled annual-phase term** (~2.1 bpm on RHR, matching the ~2 bpm literature prior) rather than by season-stratified contrasts. Q20 subsumes this Q16 goal for the channels it covers; Q16's per-primitive stratification survives only as an independent descriptive cross-check of the modelled season term.

**Context**: Per [`lc_era_temporal_segmentation.md`](lc_era_temporal_segmentation.md) §1, Stratum 1 (pre-corona, 2021-08-16 → 2022-03-20) covers ~7 months of Aug-Mar = winter + shoulder seasons only. Any Garmin-only contrast between Stratum 1 and Strata 3/4 (LC) baselines confounds illness state with season by construction. Disentangling requires season-stratified contrasts.

**Why queued**: descriptive characterisation; not gating the Wiggers pre-reg pipeline (which runs only on Stratum 4). Becomes load-bearing if a downstream analysis wants to claim "RHR baseline shifted post-LC" or "BB shape changed post-LC".

**Workflow**:
1. Define season buckets: autumn shoulder (Aug-Oct), winter (Nov-Jan), winter shoulder (Feb-Mar). Other seasons (Apr-Jul) cannot use Stratum 1.
2. Per Garmin primitive (RHR, sleep stress mean, BB peak, BB lowest, etc.), compute within-stratum-within-season mean + IQR.
3. Report per-season contrasts Stratum 1 vs Stratum 3 vs Stratum 4 only for seasons covered by all three.
4. The Stratum-1 vs Stratum-3/4 contrast in autumn shoulder is the cleanest illness-state-vs-season disentanglement (both strata have autumn coverage; same season).
5. Flag any contrast that exists only in one stratum's coverage as "cannot disentangle".

**Where to put when done**: extension of [`lc_phase_descriptive.md`](lc_phase_descriptive.md) with season-stratified columns, OR new file `garmin_baseline_season_decomposition.md`.

**Cross-refs**:
- [`lc_era_temporal_segmentation.md`](lc_era_temporal_segmentation.md) §1 Stratum 1 seasonality caveat, §8 follow-up note
- [`lc_phase_descriptive.md`](lc_phase_descriptive.md) (where the per-stratum descriptives sit)
- [[feedback_caveats_vs_apriori]] (season is a caveat, not an a-priori basis)

## Q17. Statistical-methodology literature fetch + verification

**Status**: queued — agent task; self-contained brief exists.

**Context**: The three new methodology MDs ([`lc_era_temporal_segmentation.md`](lc_era_temporal_segmentation.md), [`permutation_null_block_length.md`](permutation_null_block_length.md), [`train_validate_split_fate.md`](train_validate_split_fate.md)) run on first-principles reasoning only. Candidate statistical-methodology citations (stationary bootstrap, automatic block-length selection, SCED replication standards, n-of-1 reporting) have not been read or verified. Each MD has a `## Citation status` block making this explicit; the literature row of each MD's four-input reasoning is honestly downgraded to "deferred".

**Why queued**: the methodological reasoning stands on its own; citations strengthen but do not gate the choices. The fetch task is bounded but non-trivial (open-access search per paper, save to literature folder, verify the cited claim against the paper's actual content, integrate the verified citation back into the MD with the specific section/page checked).

**Self-contained brief**: [`_pending_literature_fetch.md`](_pending_literature_fetch.md). Includes:
- TL;DR and discipline reminders (cite only where the reference materially supports the choice; no secondary sources; flag unobtainable papers honestly; do not invent claims).
- Per-paper sections (candidate citation, candidate claim, what to verify, where to look — open-access sources in order of likelihood).
- Save location: new subfolder `docs/research/literature/methodology/`.
- Step-by-step instructions for integrating verified citations back into the three MDs.
- Empty verification log at the bottom.

**Cross-refs**:
- [`_pending_literature_fetch.md`](_pending_literature_fetch.md) (the agent brief itself)
- [`lc_era_temporal_segmentation.md`](lc_era_temporal_segmentation.md), [`permutation_null_block_length.md`](permutation_null_block_length.md), [`train_validate_split_fate.md`](train_validate_split_fate.md) (the three MDs awaiting citations)
- [[feedback_methodology_decisions_documented_reasoning]] (the discipline this task ultimately serves)

## Q18. Wiggers G3 — barometric pressure × headache / gevoelscore

**Status**: queued — parked 2026-06-14 while Tier 1 (C3 + C4 first; A1 + B1 with revised priors per the HA01b-recomputed correction in [REJECTED.md](../REJECTED.md)) progresses; testable once barometric pressure data is joined.

**Context**: G3 is the only barometric hypothesis in the Wiggers register (line 115: *"Low / falling barometric pressure associates with worse gevoelscore and with headache days"*). Counted in the 11 "partial" set per the register summary table. Tier 3 in the priority shortlist (descriptive pass needed before pre-reg). Wiggers framing: headache is a master variable for this user; pressure is free external data.

**Why queued, not rejected**: the predictor column does not exist in `per_day_master.csv`. G3 cannot run until barometric pressure data is joined. This is a data-availability deferral, not a hypothesis-level rejection.

**Two paths to get the data**:

1. **External KNMI fetch** (the register's current assumption — line 297: *"deferred-external (no Garmin column)"*). Dutch national weather institute publishes hourly atmospheric-pressure records by station. Workflow:
   - Identify the KNMI station nearest the user's residence (~30 stations across NL).
   - Fetch the historical hourly series 2021-08-16 → as-of-date as CSV (KNMI provides this open-access).
   - Aggregate to daily resolution; choose representation per the hypothesis operationalisation (Wiggers says "low / falling" — both level and 1-day slope are candidates; report both).
   - Join to `per_day_master.csv` on `date`.
   - Add column(s) to DATA_DICTIONARY with provenance + KNMI station identifier + station distance + missingness pattern.
   - Engineering: ~1 session.

2. **Garmin on-device pressure** (alternative worth checking first). The FR245 has a barometric altimeter for elevation. Whether the raw pressure trace is exported in the GDPR FIT dump is unknown without checking the extraction. If it IS exported:
   - Same source as the rest of Garmin data; no external API dependency.
   - Timezone-aligned by construction; no station-distance error.
   - Captures the user's actual ambient pressure (accounts for indoor/outdoor pressure differences vs a fixed weather station).
   - But: the pressure trace also responds to elevation change (stairs, hills); needs altitude-vs-pressure decoupling if the user has elevation variation in their day. The user's NL residence is roughly flat, which simplifies this.
   - First step: grep the Garmin extraction code for `pressure` / `barometric_pressure`; check the FIT extraction output for a pressure field; check `monitoring.fit` and `activity.fit` records.
   - If present: extract + aggregate to daily resolution.
   - If absent: fall back to path (1).

**Pre-reg prereqs (Tier 3 discipline)**:
- Pressure data joined to master (path 1 or 2; check path 2 first since it's cheaper if it works).
- Source verification of G3 against the Wiggers PDF (G3 is not yet in the verified set; the PDF passage motivating "low / falling pressure" needs PDF line refs added to the source verification log).
- Descriptive characterisation: `gevoelscore ~ pressure_level` + `gevoelscore ~ pressure_slope_1d` + `cat_sub_hoofdpijn > 0 ~ both` over Stratum 4.
- Crash-distortion sensitivity row per CONVENTIONS §3.4.
- Pressure-quality check (KNMI: station distance + missingness pattern; Garmin: device on-wrist time + altitude-decoupling validation).
- Then write the G3 pre-reg.

**Where to put when done**:
- Pressure column(s) → `per_day_master.csv` via either `pipeline/01_extract/knmi_pressure.py` (path 1) or via extending the Garmin extraction (path 2).
- DATA_DICTIONARY row added with full provenance.
- Descriptive characterisation → `analyses/descriptive/g3_pressure_descriptive/`.
- Source verification log entry added to [`wiggers_testable_hypotheses.md`](../wiggers_testable_hypotheses.md) § Source verification log.
- Pre-reg → `analyses/hypotheses/HA-G3-pressure-headache/hypothesis.md`.

**Cross-refs**:
- [`wiggers_testable_hypotheses.md`](../wiggers_testable_hypotheses.md) Tier 3 G3 row (line 166), G-block row (line 115), Pre-reg-draft G3 row (line 297)
- CONVENTIONS §3.4 (crash-drop sensitivity row)
- [[feedback_descriptive_before_inference]] (Tier 3 discipline)
- Q15 (per-channel autonomic lag profiling — different prereq pattern but same Tier 3 discipline)

## Q19. Statistical-methodology literature fetch for `time_resolution.md`

**Status**: queued — agent task; extends Q17's brief.

**Context**: [`time_resolution.md`](time_resolution.md), the framework MD on picking time-resolution per hypothesis (drafted 2026-06-14), runs on first-principles reasoning + project conventions. Its `## Citation status` block makes this explicit and §11.2 honestly downgrades the literature row to "deferred". Candidate citations that would materially support the four-input reasoning:

- **SCED time-series standards** anchored elsewhere in the project: Daza 2018 (*Methods of Information in Medicine*), WWC 2022 SCED handbook, Natesan Batley 2023 (systematic review). PDFs likely already live in [`literature/methodology/`](../literature/methodology/) per Q17; need re-reading specifically for multi-scale guidance on within-subject time-series.
- **Time-series scale-decomposition methodology**: candidate references on wavelet vs nested-window vs frequency-domain decomposition for non-stationary single-subject series. Open-access candidates: Percival & Walden 2000 (*Wavelet Methods for Time Series Analysis*) chapter on multi-resolution; Daubechies 1992 (CBMS-NSF) Lecture 1.
- **Autonomic / circadian analysis-window conventions**: PEM / ME-CFS literature on choosing daily vs intra-day windows for autonomic markers. Aitken et al. 2026 is one anchor; broader autonomic-marker-window conventions need a fetch pass.
- **Reference-frame correctness in trend detection**: anchor for the lagged-baseline construction (`[d-90, d-30]`). Politis-Romano stationary bootstrap (already in Q17 queue) and Lahiri 2003 chapter on lagged baselines are candidates.

**Why queued**: the methodological reasoning stands on its own; citations strengthen but do not gate the choices. The fetch is bounded but non-trivial (verify the cited claim against the paper's actual content, integrate the verified citation back into the MD with the specific section/page).

**Self-contained brief**: extends [`_pending_literature_fetch.md`](_pending_literature_fetch.md); add a new section "P9. Time-resolution methodology references" with the candidate citations above. Same discipline reminders (cite only where the paper materially supports the choice; no secondary sources; flag unobtainable papers honestly).

**Cross-refs**:
- [`time_resolution.md`](time_resolution.md) `## Citation status` and §11.2
- [`_pending_literature_fetch.md`](_pending_literature_fetch.md) (the agent brief Q19 extends)
- Q17 (the parallel literature fetch for the other three methodology MDs)

## Q20. Long-horizon LC-attributable residual — full multi-confounder decomposition

**Status**: queued — exploratory estimation; the R12-class long-horizon
audit. Blocks any FIRM "the factor drifted over the LC era *because of LC*" /
"structurally different body" quantitative claim. NOT urgent (see why-queued).

**Context (read this cold, 2026-07-02)**: The R23 COVID follow-up built a
literature-gated confounder framework for multi-year Garmin-channel trends and
ran it on `resting_hr`. Result
([`../analyses/longrun_rhr_trend/findings.md`](../analyses/longrun_rhr_trend/findings.md)):
after modelling out deconditioning + weight + citalopram + seasonality +
aging, a residual RHR rise of ~+1.2 bpm/yr persists post-2023, but its CI is
wide (~[0.6, 1.9]) and FRAGILE (leave-2024-out crosses zero; sensitive to the
sparsely-measured weight trajectory). So the LC-attributable residual is
**SUGGESTIVE, not established**. Separately, the citalopram dose-response
re-audit
([`citalopram_dose_response_confounder_reaudit_2026-07-02.md`](citalopram_dose_response_confounder_reaudit_2026-07-02.md))
found the dose BETA is sound but the §5.B dose-CORRECTED channel
(`channel_adj = channel - beta*dose`) is dose-clean, NOT confounder-clean over
the full era. The confounder-exposure triage
([`confounder_exposure_triage.md`](confounder_exposure_triage.md)) classifies
exactly this (long-horizon / cross-era / absolute-level claims) as the class
needing the full audit; the crash-precursor scorecard is immune and does NOT.

**The question**: can we firm up, or honestly bound, the LC-attributable
component of the multi-year drift on the load-bearing channels, by modelling
ALL literature-supported slow confounders together over the full era? Targets:
(a) `resting_hr` (refine/confirm the +1.2 [0.6,1.9] residual); (b) the
dose-corrected stress/BB channels (`stress_mean_sleep`, `all_day_stress_avg`,
`bb_lowest`) whenever a long-horizon claim consumes `channel_adj` — those
still owe weight (~15 kg over the era), the deconditioning tail, and aging
their own correction on top of the dose correction.

**Why queued (and why NOT urgent)**: the crash-precursor scorecard (the
site's core) is immune (short-horizon lagged baselines; triage §2), so nothing
the site currently ships depends on this. It becomes load-bearing only if the
site wants a FIRM quantitative "structurally different body" claim (register
R12's inferential version) instead of the honest "direction robust, magnitude
not cleanly separable" answer already delivered. **The honest expected
outcome is that n=1 with collinear slow drivers may not permit a clean
number** — "we cannot cleanly separate" is a valid, publishable result.

**Workflow (cold-start instructions)**:
1. Reuse the driver ledger
   ([`../analyses/longrun_rhr_trend/driver_ledger.md`](../analyses/longrun_rhr_trend/driver_ledger.md))
   as the confounder set — literature-gated, inputs resolved (weight 56
   weigh-ins; VO2Max peak-measured / decline-modelled; aging <=0.3 bpm/yr;
   citalopram dose; season). Do NOT re-derive it.
2. Per target channel, fit the full decomposition and read the residual using
   the CORRECTED methods the RHR work established (the first draft overclaimed
   the CI 3x; a skeptical review caught it — do not repeat): **block-bootstrap
   OF THE RESIDUAL SLOPE** (not the analytic Theil-Sen interval — lag-1
   autocorrelation ~0.94), leave-one-year-out sensitivity, weight-coefficient
   sensitivity, and the slow-deconditioning sensitivity pair. Template:
   [`../analyses/longrun_rhr_trend/decomposition.py`](../analyses/longrun_rhr_trend/decomposition.py).
3. Fold in Q16 (season-stratified baseline) as the seasonality handling; Q20
   subsumes Q16 for the channels it covers.
4. Report per channel: residual direction (robust?) + magnitude (CI) +
   fragility (year-drop, weight-sensitivity). Carry the honesty limits
   verbatim from ledger §5 (fitness decline modelled not measured; slow
   drivers collinear; static level not attributable; n=1).
5. **Fresh-session skeptical review before any FIRM claim ships** — this
   result class MUST be reviewed cold (convenient results overclaim).

**Where to put when done**: extend
[`../analyses/longrun_rhr_trend/`](../analyses/longrun_rhr_trend/) with
per-channel residual findings, or a new `longrun_channel_residuals/` folder.
Update the triage's residual sub-flag + register R12.

**Cross-refs**:
- [`../analyses/longrun_rhr_trend/`](../analyses/longrun_rhr_trend/) (driver
  ledger, decomposition, findings, skeptical review — the whole substrate)
- [`citalopram_dose_response_confounder_reaudit_2026-07-02.md`](citalopram_dose_response_confounder_reaudit_2026-07-02.md)
  (the `channel_adj` residual sub-flag) + [`confounder_exposure_triage.md`](confounder_exposure_triage.md)
- Q16 (season decomposition — subsumed for the covered channels)
- register R12 (structurally-different-body inferential version)
- [[feedback_research_discipline_statistical]] (block-bootstrap,
  autocorrelation, named counts); [[reference_garmin_weight_vo2max_biometrics]]
  (weight/VO2Max data location + the nested-object gotcha)

## Q21. Site R4 -- trigger type (physical / emotional / cognitive) full treatment

**Status**: **descriptive treatment DELIVERED 2026-07-06** (much of the parked
scope done); two forward tests spun out to Q26 (phenotype-validation) + Q27
(household-illness prospective logging).

**DELIVERED 2026-07-06** (`analyses/descriptive/trigger_types_r4/`): the full
descriptive arc. (1) Precondition: coverage is adequate (100% triaged, 83% of
crash run-ups carry a structured load) but presence is degenerate, so no defensible
trigger share. (2) Autonomic fingerprints of load (concordance): physical -> cardiac
/ activity, cognitive -> Garmin-invisible, emotional -> flat in HR but robust in
daytime GSS + battery floor; the Wiggers "HRV drop that night or the following
night" timing test confirms this for emotional load (significant the FOLLOWING
night) and refutes it for cognitive load -- a refinement of her mental-PEM
concession. Site card built. (3) Crash-specificity: emotional load is the only
suggestive pre-crash trigger (moderate+ perm-p 0.028 uncorrected), does not survive
multiplicity, era-confounded -- suggestive not established. (4) Crash phenotypes
(exploratory): crashes tend to sort into a quiet/interpersonal (emotional) type and
a loud/illness (physical) type, but a strict tri-axis convergence rule labels only
5/29 cleanly (24 unclear). Feeds R32(a). The mental-PEM headline is answered:
the watch sees emotional load (in the autonomic aftermath, not HR) and does not see
cognitive load.

**Remaining (forward-looking)**: Q26 (the phenotype-validation test the convergence
rule operationalises) and Q27 (log household illness prospectively so viral crashes
become separable). The emotional-TRIGGER pre-reg (prospective-primary, per the
2026-07-04/06 discussion) is also still un-drafted; scope it separately if pursued.

--- original parked note (2026-07-03) below ---

**Status**: queued -- parked 2026-07-03 by user decision; needs a dedicated
session for proper hypothesis formulation + methodology, NOT the honest-limit
note the register scoped.

**Context (cold-read)**: Site register R4 asks what share of crashes are
physically-triggered vs emotionally / cognitively-triggered -- the
"activity-invisible" / mental-PEM fraction (Wiggers' own "the watch can't see
mental PEM"). The register scoped it `weak` (honest-limit only). The user
decided it deserves fuller treatment: a proper hypothesis + methodology, not a
caveated share. The hard constraint is data: the proxies
(`cat_belasting_emotioneel` / `cat_belasting_cognitief`, `state_symptoom_*`)
are sparse (~35% fill, note-days only, max value 2) and were NOT used in
conditioning, so clean tests speak to the physical subset only.

**Why queued**: the operationalisation of "physically vs emotionally /
cognitively triggered crash" is non-trivial and the exposure is sparse; likely
an honest-limit outcome, but that verdict should come from a real
precondition + methodology pass, not an assumption.

**Workflow**: descriptive precondition on proxy coverage/quality first (how
many crashes have a usable trigger-type proxy); then decide testable-vs-
honest-limit; if testable, the Lane-4 arc (methodology MD -> pre-reg -> review
-> test); the mental-PEM fraction is the headline. Keep the "watch can't see
mental PEM" framing central.

**Cross-refs**: site register R4; H2 activity-invisible analysis;
DATA_DICTIONARY §9/§11; [[feedback_research_discipline_interpretive]].

## Q22. Site R7 crash-character flip -- early-vs-late crashes deep pass

**Status**: queued -- parked 2026-07-03 by user decision; a fuller descriptive
pass on R7's crash-character-flip candidate.

**Context (cold-read)**: Site register R7 flags a candidate -- "which
direction dominates appears to have flipped over time." The user wants a
deeper pass: **is there a difference in the EARLY crashes vs the LATER
crashes, using the recovery phases as the guideline?** Does crash character
(deviation-direction mix, depth/duration, the post-crash autonomic signature)
differ across the lived recovery phases (`lc_pre_ergo` / 4a / 4b /
`citalopram_modulated`)?

**Why queued**: deserves a careful descriptive pass, and it is
discipline-sensitive: it MUST stay descriptive (an over-time difference is a
number with wide error, never a per-era/temporal verdict, per
`train_validate_split_fate.md`), and it must guard against labelling /
measurement-regime coverage artifacts (e.g. the per-minute BB cliff) so a data
-availability change is not read as a crash-character change.

**Workflow**: characterise crash properties -- direction mix, K01 depth, K02
duration, the R9 / HA-P6 post-crash autonomic signature -- stratified by
recovery phase, descriptive with wide error; flag every coverage artifact;
never a per-phase verdict. Sibling of R19 (per-signal phase read) and R28
(per-phase quartiles).

**Cross-refs**: site register R7; R13 (the changing-crash story); K01 / K02
(crash depth / duration shift); the recovery-phase axis
(`lc_recovery_phase_axis.md`); `crash_v2-definition/`;
[[feedback_research_discipline_statistical]].

## Q23. Site R32 -- "no visible trigger-into-crash signal" as a finding + per-crash case-histories

**Status**: **(a) DELIVERED 2026-07-06** as a synthesis card
(`analyses/garmin_exploration/cards/no-visible-trigger-into-crash-signal-export.md`):
the no-visible-trigger claim now rests on three independent lines (trust metrics
all Tier C + push-crash null + R4 ambient/off-instrument triggers), with the "not
visibly confirmable, not proven absent" boundary carried. **(b) still queued** --
the per-crash case-histories site section (design + privacy opt-in). Original note
below.

**Status**: queued -- logged 2026-07-04 from the site register. Two parts:
(a) a synthesis/framing finding (mostly `assemble` from existing results),
(b) a design + privacy decision for a future site section (not primarily a
research ask).

**Context (cold-read)**: discussing HA01c, the participant noticed that naming
"what triggered each crash" assumes a trigger->response model the record can't
support. R32(a) asks research to confirm the honest finding -- that **no
scorecard signal reaches a trigger / causal-precursor bar**: the signals are
retrospective discriminators (precision <5%, lift <2x; HA07d ~1-in-37 per fire,
HA01c ~1-in-45), physical exertion (HA01c) is only a soft backward tendency and
not load-bearing, and a large share of plausible triggers (emotional /
cognitive) are off-instrument (R4 `weak`; "the watch can't see mental PEM").
Net claim to sanity-check: *the moment of tipping into a crash is not visibly
encoded in this watch data; the data reads the weather around a crash better
than what set it off.* R32(b) is a per-crash case-histories section
(descriptive; dual-track lived-vs-watch; "unclear" a first-class label; no
"trigger" wording; hindsight-bias caution) -- flagged as a privacy opt-in
(per-crash dated life-events depart from aggregate-only).

**Why queued**: (a) is a one-line confirmation that "no signal reaches a trigger
bar" fairly states the record -- but it should be an explicit research sign-off,
not a site assumption. (b) is editorial/design + a privacy call for the
participant, not a research run.

**Workflow**: research confirms or corrects the (a) framing against the
trust-metric export (R2 / R14) + R4; no new test needed. (b) stays site-side
unless a quantitative companion (R4 / Q21) informs the "unclear" fraction. Keep
the honest bound: the claim is "no trigger is *visibly confirmable*", NOT
"crashes have no triggers".

**Cross-refs**: site register R32 (sibling of R4 / Q21); trust metrics
`cards/trust-panel-export.md` + `cards/primary-verdict-statistics.md`; HA01c
handoff `handoff_back_2026-07-04_HA01c-exertion-verdict-and-framing.md`;
[[feedback_research_discipline_interpretive]].

## Q24. Site R33 -- compensatory rest *after* heavy days, and whether it strengthened over time

**Status**: queued -- logged 2026-07-04 from the site register. `new` (the
within-day sub-part is `blocked` on per-minute extraction). The flip side of
R32.

**Context (cold-read)**: lived experience -- after a heavy day (physical or
emotional) the participant feels far more tired and rests more; if that's
*learned* pacing it should show, more clearly in recent years, as more rest
after heavy days and shorter self-limiting within-day peaks. Status checked
2026-07-04: **none of this is tested** -- pre-crash exertion (HA01b / HA01c) and
post-crash recovery (HA-P6) exist, but not the post-heavy-day direction. Five
sub-questions:
1. **Day-after rest** -- does exertion fall in the 1-3 days after a heavy day
   (HA01c heavy-day def, own top ~25%) vs after matched ordinary days? `new`,
   feasible on daily aggregates.
2. **Within-day shape** -- shorter peaks + more active rest same-day? `blocked`
   on per-minute Garmin extraction (H04b path C; `garmin_pacing_practice.md §8`;
   QUEUED-WORK C.4 / C.5).
3. **Over time** -- stratify (1) / (4) across the recovery-phase axis; the
   pacing-improvement test and the most confounded: **deconditioning** (fewer /
   lighter days recently -> a floor effect, not a choice) and **citalopram**
   (phase-5 boundary = medication-onset date) both mimic "more rest recently".
   Descriptive only; attribution to the driver ledger.
4. **Sleep after a heavy day** -- do `sleep_duration_min` / `stress_mean_sleep`
   / `bb_overnight_gain` / `sleep_efficiency` on the night(s) after differ from
   after matched ordinary days? `new`, closest to testable on existing
   aggregates.
5. **Does resting prevent crashes?** -- hardest; a counterfactual on n=1;
   overlaps R3 (pacing paradox). HA-P7 already NOT-SUPPORTED and post-hoc
   reframed as "maybe pacing prevents the crashes that would have shown the
   signal" -- unfalsifiable. Descriptive bound at best.

**Why queued**: genuine un-operationalised gaps; the feasible parts (1, 4)
could run on existing daily aggregates but need a precondition + methodology
pass; (2) is data-blocked; (3) / (5) are discipline-sensitive (confounds +
counterfactual).

**Workflow**: descriptive precondition on the day-after / night-after reads
first (1, 4); if clean, stratify by phase (3) with the deconditioning +
citalopram rivals attached as caveats; (2) waits on per-minute; (5) routes to R3
/ the driver ledger. The available honest positive is "load is followed by more
rest", NOT "pacing prevents my crashes".

**Cross-refs**: site register R33 (flip side of R32; feeds R15 pacing driver +
R3 pacing paradox); HA01c heavy-day def
`analyses/hypotheses/HA01c-effective-exertion-shock/`; phase axis
`lc_recovery_phase_axis.md`; sleep channels `intervention_effects_descriptive.md
§3`; pacing-efficacy scope `garmin_pacing_practice.md §1 / §5.2 / §7.4` +
QUEUED-WORK C.4 / C.5; within-day blocker H04b path C;
[[feedback_research_discipline_statistical]].

## Q25. Site R34 -- re-test morning-RHR with an overnight-*average* HR proxy (HRM4Pacing caveat)

**Status**: queued -- logged 2026-07-04 from the site register. `new` but
feasible on existing per-minute HR where coverage allows. Does **not** change
the published morning-RHR verdict until it runs.

**Context (cold-read)**: external source HRM4Pacing (Kathryn Dickinson; Workwell
tradition; peer-reviewed Clague-Baker et al. 2023) warns: *"you can't rely on
the figure that Polar and Garmin devices report as RHR, as they show lowest HR
instead, which for our cohort may not be the same thing"* -- recommend
**average overnight / sleeping HR** as the proxy. This bites here: the site's
morning-RHR claim (not-found; H01 / HA06b, Workwell "RHR+15") is tested on
`resting_hr`, which `DATA_DICTIONARY §5` confirms is **Garmin's algorithmic RHR
passed through directly** ("Garmin computes RHR during sleep" -- a
lowest-sustained figure). That IS the figure the caveat warns against; the
recommended overnight-*average* proxy was never used. So the not-found verdict
is measurement-input-exposed -- maybe the wrong RHR definition, not a true
absence.

**Why queued**: re-running A1 / A3 (H01 "+threshold" and the HA06b z-variant) on
an overnight-average sleeping-HR proxy either makes the negative
robust-to-the-caveat (stronger) or moves it. The proxy channel doesn't exist
yet but is computable from per-minute `intraday_hr_stress_daily.csv` x the known
sleep window (feasible `new`); flag coverage gaps. Venu 3 exposes overnight HR /
HRV more richly going forward.

**Workflow**: build `hr_overnight_mean_sleep` from intraday HR x sleep window;
pre-register the proxy + threshold exactly as the original (no fishing for a
positive); re-run A1 / A3; report whether the verdict moves + a
measurement-definition note. Honest bound: the lowest-vs-average gap may be
small / stable (resting_hr range 47-65 bpm) -> verdict unchanged is a valid
outcome. Feeds R17 (measurement-regime) and R18 (mark morning-RHR
measurement-input-exposed).

**Cross-refs**: site register R34; sources `sources.json` -> `hrm4pacing` +
`clague-baker-2023`; `resting_hr` def `DATA_DICTIONARY §5` +
`methodology/nightly_attribution.md` + `methodology/garmin_indicators_audit.md`;
RHR tests `analyses/hypotheses/` A1 / A3 / H01 / HA06b; intraday
`pipeline/01_extract/garmin_intraday_hr_stress.py`; site R17 / R18.

## Q26. Crash-phenotype validation test (the convergence rule operationalised)

**Status**: queued -- operationalisation proposed 2026-07-06 from the R4
crash-phenotype exploration; needs its own methodology MD + pre-reg (different
sessions).

**Context**: the exploration
(`analyses/descriptive/trigger_types_r4/crash_phenotypes_exploratory.md`) found
crashes tend to sort into a quiet/interpersonal (emotional) type and a loud/illness
(physical) type across three independently-measured axes (trigger, autonomic
fingerprint, note content), but a strict convergence rule labels only 5/29 cleanly
(24 unclear). The convergence rule is a strong exposure DEFINITION but **cannot be
tested on these data** (it was found here, and its axes are correlated by
selection).

**Why queued**: promoting the phenotype from description to test requires a
non-circular design. Two clean forms: (1) **prospective lock** -- freeze the
convergence definition + thresholds now, evaluate on crashes AFTER the lock (also
de-confounds the era issue); (2) **external validator** -- predict an outcome NOT
used to define the phenotype (recovery-trajectory shape, recurrence spacing,
differential pacing-vs-emotion-regulation response). NOT part of the
emotional-trigger pre-reg (there the fingerprint is outcome-adjacent and cannot
enter the exposure).

**Workflow**: methodology MD (lock the three axes + thresholds) -> fresh-session
review -> lock -> prospective accrual or external-outcome run. Keep the "unclear is
first-class / largest bucket" honesty.

**Cross-refs**: `analyses/descriptive/trigger_types_r4/crash_phenotypes_exploratory.md`
+ `crash_phenotypes.py`; Q21 (R4); site R4 / R32; the emotional-trigger pre-reg
(separate).

## Q27. Prospective household-illness logging (external de-confounder for viral crashes)

**Status**: queued -- data-collection suggestion, 2026-07-06. Not an analysis;
a one-field logging change that unlocks a future analysis.

**Context**: the participant's own symptoms (runny nose, cough, feeling feverish)
cannot separate a real virus from severe PEM -- they present identically. The clean
de-confounder is an EXTERNAL marker: whether OTHERS in the household are ill. A
feasibility check (`crash_phenotypes.py`) found this signal essentially ABSENT from
the current record (18 note-dates mention illness, 0 pair an illness term with a
household member in the same clause), and the illness mentions that exist are the
participant's own symptoms. So viral crashes cannot be separated from PEM
retrospectively.

**Why queued**: the fix is prospective. Logging a simple "household illness today
(y/n)" field going forward would let future crashes carry the external viral marker,
enabling a clean viral-vs-PEM crash split that the record cannot support now.

**Workflow**: add the field to the daily-entry app (a v1.x form addition, coordinate
with the app roadmap); after a suitable accrual window, revisit the crash-phenotype
typology with a viral bucket separable by the external marker.

**Cross-refs**: `analyses/descriptive/trigger_types_r4/crash_phenotypes_exploratory.md`
section 5; Q21 / Q26; site R4 / R32; Wiggers H3 (acute-illness signature).

## Q28. Sleep descriptive trajectory + Wiggers sleep gaps (F1 / F4 extension)

**Status**: queued -- Layer-1 descriptive, 2026-07-07. Data ready, analysis absent
(per the sleep sweep). Reuses the R19/R30 recovery-phase machinery.

**Context**: Wiggers makes several sleep claims the catalog registered but never
analysed over time. `sleep_duration_min`, `bedtime_hour_local`, `bedtime_std_7d`,
`sleep_awake_min`, and the sleep start/end timestamps all exist in the master;
no trajectory or crash-neighbourhood analysis has landed.

**Why queued**: three descriptive reads fall out cheaply -- (a) **sleep duration +
rhythm per recovery phase / over all phases** (F1); (b) **sleep-onset latency +
waking-later around crashes** (Wiggers PG1, a rare predictive claim: "long sleep
onset after overexertion -> suspect PEM"); (c) **awake/restless minutes** as a
status readout (PG5). Descriptive backdrop, single-pool, no verdict.

**Cross-refs**: `wiggers_testable_hypotheses.md` F1/F4 + §J.3 PG1/PG5;
`lc_recovery_phase_axis.md`; R19/R30 folders; note 2026-07-07.

## Q29. Night-quality 5-state typology + guide graph replication (Wiggers pattern table)

**Status**: queued -- Layer-1 descriptive typology, 2026-07-07. Needs the
`pem_pots_mechanism_framing.md` markers; primitives all exist.

**Context**: the guide's HR x HRV pattern table (image 2 / clean source rows
1394-1400) is a 5-state night typology: (1) high HR + low HRV = severe PEM;
(2) high HR + fluctuating HRV; (3) initial high HR decreasing; (4) both fluctuate;
(5) high HRV + very low HR = parasympathetic swing. Only rows 1 + 5 map to catalog
lines (H3 / H4). No composite night-quality classifier exists.

**Why queued**: build the paired nightly **resting_hr + HRV-proxy** (inverted
overnight stress) series (replicating guide image 1), classify each night into the
5 states by (RHR level, HRV-proxy level, HRV-proxy variability), and describe state
frequency **over time / per phase**, **around crashes**, and **vs felt-state**.
Descriptive first; a predictive "does state X forecast next-day crash" is a
separate pre-reg. Carries the FR245 HRV-proxy caveat throughout.

**Cross-refs**: `wiggers_testable_hypotheses.md` §J.3 PG2/PG3;
`methodology/pem_pots_mechanism_framing.md`; H3/H4; `hrv_proxy_via_stress.md`.

## Q30. Intraday HR-pacing trend + post-peak recovery shape (Wiggers HR-pacing)

**Status**: queued -- intraday, 2026-07-07. Extraction infrastructure mature
(`pipeline/01_extract/garmin_intraday_hr_stress.py`, A4 operands locked); the
recovery-SHAPE part is new compute.

**Context**: Wiggers frames HR pacing as staying near resting HR / under an HR cap.
Two reads are absent: (a) **time-above-threshold / high-HR-minutes trend over the
years** (evidence of improved pacing, consciously or by feel); (b) **post-peak HR
recovery shape** (decay slope / half-life -- did the body settle after a peak). The
A4 operands capture occurrence + duration, not the recovery curve. NB: RHR itself
*rises* over the years but R30 showed that is weight/aging, not worse pacing.

**Cross-refs**: `wiggers_testable_hypotheses.md` A4 + §J.3 PG4/PG6;
`methodology/bout_level_recovery_dynamics.md`; `longrun_rhr_trend/`.

## Q31. POTS / orthostatic family -- descriptive write-up + the electrolyte-intervention test + prospective symptom logging

**Status**: queued -- 2026-07-07. Mixed: descriptive family write-up (do now),
one testable predictive claim (pre-reg), one prospective logging change.

**Context**: the largest catalog gap (per the 2026-07-07 re-read) is a missing
POTS / orthostatic family -- `wiggers_testable_hypotheses.md` §J.2 (O1-O8). The
separability analysis established the U-dip signal is separable from the load signal
(r ~ 0.09, distinct days) and descriptively more frequent early (era-confounded by
citalopram onset). **The external PubMed review
(`literature/reviews/pots_operationalisation_wearable_review.md`) capped the label**:
the U-dip is NOT a validated POTS marker (no orthostatic precedent, off-polarity,
posture-blind), only "a within-day pattern managed as if orthostatic." Three
follow-ups:

**Why queued**: (a) **descriptive family write-up** -- fold O1-O8 into the catalog
proper once §J is reviewed; (b) **the one testable predictive claim, O5**: "water +
salt + compression significantly reduce daytime stress scores" -- a pre-registered
intervention-effect test (needs the electrolyte/compression log; single-pool,
reviewer-mode, fresh-session reviewed); (c) **prospective posture / orthostatic-symptom
logging -- the one channel that would let the watch speak to POTS on the literature's
own terms.** The review is explicit: POTS is defined by a standing HR delta the FR245
cannot form. A lightweight daily field -- a **standing-HR / lean-test reading** and/or
"dizzy-on-standing / palpitations (y/n)" -- would (i) let a future analysis corroborate
the watch U-dip against felt orthostatic symptoms (the notes carry no such vocabulary,
2/246 corroborated), and (ii) supply the orthostatic delta itself, moving the POTS side
from "managed-as-if" to something the instrument can actually check. Same shape as
Q27's household-illness fix.

**Cross-refs**: `wiggers_testable_hypotheses.md` §J.2;
`literature/reviews/pots_operationalisation_wearable_review.md`;
`analyses/descriptive/pem_pots_separability/`;
`methodology/pem_pots_mechanism_framing.md`; HA11; Q27 (sibling prospective-logging).

## Q32. Full intraday parasympathetic-swing composite (H4) vs felt-state

**Status**: queued -- Layer-1 descriptive assembly first, then a pre-reg-deferred
directional test (H4-composite), 2026-07-07. Primitives all exist; the composite
object was never assembled.

**Context**: Wiggers describes the parasympathetic swing / "freeze" as one intraday
object -- a sudden HRV spike, body battery draining *faster* than normal, midday
"low blue" stress lines, and body battery *rising* against that dip, with a small PEM
felt 1-2 days later ("don't be fooled by good values"; the "singing seated" worked
example, clean source lines 1463-1494). The catalog registers it three ways (B4 the
outlier framing, D5 the high-morning-BB framing, H4 the composite), but only its
*components* were ever tested -- HA10 (morning-BB paradox, validate-era SUPPORTED)
and HA11 (within-day U-dip, train-era SUPPORTED). The full intraday composite has
never been assembled as one object or checked against felt-state (catalog §J.4
B4/H4 row: "full intraday composite not modelled").

**Why queued**: (a) **descriptive assembly (do first, §2.1)** -- build the swing-day
object from existing primitives: proxy-HRV rise (inverted overnight / within-day
stress), faster-than-normal BB drain (`bb_drained_24h` / intraday BB slope), a midday
stress U-dip (HA11 `u_dip_count`), BB rising against that dip; describe swing-day
frequency over phases / around crashes / **vs felt-state**. (b) **pre-reg-deferred
predictive extension** -- H4's directional claim ("a swing day raises crash /
steep-drain risk at t+1/t+2") as a single-pool, reviewer-mode, fresh-session-reviewed
pre-reg, built only once the descriptive assembly warrants it. The HRV-spike half stays
a stress proxy and device-blocked-labelled throughout (FR245 HRV Status hardware-blocked).

**Cross-refs**: `wiggers_testable_hypotheses.md` B4 / D5 / H4 + §J.1 / §J.4; HA10;
HA11; `methodology/pem_pots_mechanism_framing.md`; Q29 (night state-5 sibling) /
Q30 (recovery-shape sibling).

---

*Add new queued items with a `Q<n>` header following the same shape:
**status**, **context**, **why queued**, **when / workflow**, **cross-
refs**. Drop items when they ship by replacing the body with a one-
line redirect to where the work landed.*
