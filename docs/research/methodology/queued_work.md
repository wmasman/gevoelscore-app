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

**Status**: queued — descriptive work; methodologically required for any Stratum 1 vs Stratum 3/4 comparison.

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

---

*Add new queued items with a `Q<n>` header following the same shape:
**status**, **context**, **why queued**, **when / workflow**, **cross-
refs**. Drop items when they ship by replacing the body with a one-
line redirect to where the work landed.*
