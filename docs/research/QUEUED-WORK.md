# Queued work — cards (C.X) and deferred research

*Living checkpoint, written 2026-06-06 so the items below don't drop
out of context between sessions. Two layers: **Upcoming** (next to
pick up) and **Deferred** (paused with explicit gates). Each entry has
**Intention** (what the artefact is and why it exists) and **TODOs**
(what we still need to work out, concretely).*

The C.X identifiers are insight-card concepts; they overlap with but
are not identical to the a-k tier list in [STOCKTAKE §4](STOCKTAKE.md#4-candidate-indicators-for-the-app--ranked-by-evidence).
Card-concept items live here; research items (H##, dictionary work)
also live here when they have specific, scoped TODOs to track. The
hypothesis-level state of play remains in
[garmin/hypotheses/registry.md §4](garmin/hypotheses/registry.md) and
the synthesis in [garmin/hypotheses/synthesis.md](garmin/hypotheses/synthesis.md).

---

## Recently completed (2026-06-06, later session)

The 4-review literature batch + the Theme A baseline-contamination fix
+ the bundled re-test + H02d (run independently by another agent in
the same session) all landed on 2026-06-06. Resolutions and their
effect on items below:

- **Theme A baseline fix** — implemented at
  [garmin/activity-labels/scripts/11_compute_lagged_baseline.py](garmin/activity-labels/scripts/11_compute_lagged_baseline.py)
  with spec at [severity_spec.md §Lagged baseline (v3.2)](garmin/activity-labels/spec/severity_spec.md)
  and audit trail at [registry.md §4b Theme A entry](garmin/hypotheses/registry.md).
- **Bundled re-test HA02c + HA01b-recomputed** — result at
  [activity-labels/output/ha_results_4day_lagged.md](garmin/activity-labels/output/ha_results_4day_lagged.md).
  Both REFUTED on the lagged baseline. HA01b validate-era went from
  +17.3 pp (originally SUPPORTED) to +4.0 pp (refuted). The "first
  SUPPORTED validate-era precursor" headline was substantially a
  rolling-baseline construction artifact. The pre-committed
  symmetric-re-test discipline held.
- **H02d — stress spikes with uncensored sentinels + wider window**
  ([garmin/hypotheses/H02d-stress-spikes-uncensored/result.md](garmin/hypotheses/H02d-stress-spikes-uncensored/result.md))
  — addressed two operationalisation gaps in H02b (sentinel collapse;
  3-day window). **Refuted overall** but with two clean findings:
  bridge × 5d train produced +31.8 pp discrimination (the strongest
  train-era single-channel signal of the whole project, surpassing
  H02b's +29.9 pp), and validate refuted in all 4 arms (imputed ×
  {4d, 5d}, bridge × {4d, 5d}). **5 stress-channel tests are now
  consistent on validate refutation** (H02, H02b, H02d × 4). The 4-5
  day empirical lag is now corroborated by both H02d bridge train
  (smooth monotonic 3d → 4d → 5d = +29.9 → +27.6 → +31.8 pp) AND
  HA01b's lag profile — two independent channels converging on the
  same lag.
- **Net change to "what's SUPPORTED"**: investigation now has **two
  train-era SUPPORTED stress-spike findings** (H02b 3d, H02d bridge
  × 5d), both overall-REFUTED. **Zero overall-SUPPORTED precursors
  under clean methodology.** The validate-era refutation now spans 5
  stress-channel tests + 4 activity-shock channel tests + all prior
  daily-aggregate tests.
- Synthesis updates landed in [RESEARCH-REPORT-ADDENDUM.md §§5.9-5.11](RESEARCH-REPORT-ADDENDUM.md),
  [STOCKTAKE.md §2a + §3 + §4 + §7](STOCKTAKE.md),
  [synthesis.md](garmin/hypotheses/synthesis.md) "Update 2026-06-06 (later still)" and
  "(later still even)", [pem-pacing-indicators.md §3.3](garmin/pem-pacing-indicators.md),
  and [registry.md §4 + §4b](garmin/hypotheses/registry.md).

## C.1 — clarified

An earlier draft of this document had an "Open question: what is C.1?"
section, because C.4 ("recovery-completeness over time") below was
noted as "depends on C.1" but C.1 had not been written down.

**Resolution**: the C.# naming in this document tracks the C.# in the
recent organising plan ([.claude/plans/adaptive-foraging-hamming.md](../../.claude/plans/adaptive-foraging-hamming.md)).
In that plan:

- **C.1** = **morning resting-HR delta** (a new pre-registered
  HA06-shaped test). See the new C.1 entry under Upcoming below.

The thing C.4 actually depends on is the **H05b sustained-recovery
primitive** ("for each crash, how many days until the score returns
to and stays at pre-crash baseline?"), not C.1. C.4's "depends on"
line has been corrected accordingly.

---

## Upcoming (next to pick up)

### C.1 — Morning resting-HR delta (HA06 pre-registration)

**Intention.** A pre-registered precursor test, not a derivative
one-pager. The strongest external-evidence candidate for a
validate-era precursor remaining after Theme A refuted HA01b on the
cleanest baseline. Operationalises the Bateman Horne Center
"back to baseline next morning?" heuristic and the Workwell
"morning resting HR creeping >10–15 bpm above baseline signals
over-exertion or impending crash" rule. Pairs naturally with push
burden as the cumulative-overnight-recovery-failure mechanism made
visible.

**Computable now from existing UDS resting-HR; does not depend on
H04b decoding.**

**Pre-register before any test runs.**

**TODOs.**
- [ ] Define personal RHR baseline. Candidates:
  - 30-day rolling median of nightly RHR
  - 90-day rolling median (matches Workwell's longer window)
  - Lagged window analogue (per Theme A discipline — avoid
    rebasing into the candidate region)
  - Pick one a priori; the same baseline-construction concern that
    fired Theme A applies here. **Lock the choice in the spec doc
    BEFORE looking at any HA06 outcome.**
- [ ] Define "elevation threshold." Workwell's concrete rule is
  RHR > baseline + 10-15 bpm. Likely lock at +5 bpm as primary
  with +10 as a sensitivity check, OR use a z-score / percentile
  rank against personal distribution.
- [ ] Pre-register lead-up window. Default 4-day (matches HA01b
  framing); consider also 3-day for direct comparability with H02b.
  Test only one window as the pre-registered, others as exploratory.
- [ ] **Pre-register as a both-era test** per the D7 reframe
  pre-commitment ([adaptive-foraging-hamming.md decisions table](../../.claude/plans/adaptive-foraging-hamming.md)):
  evaluate train + validate windows SEPARATELY. SUPPORTED in both
  eras strengthens the single-mechanism-two-regimes reframe (since
  the same overnight-recovery mechanism would be operating across
  the era boundary). SUPPORTED in only one era returns the
  two-mechanism framing to the table. REFUTED in both eras means
  the validate-era residual crashes are precursor-invisible in any
  waking-hour Garmin signal, and the next direction shifts firmly
  to overnight recovery via H04b.
- [ ] SUPPORTED bar: same three-criterion shape as H02b / HA01b
  (frequency ≥ 60% of crash episodes; discrimination ≥ +15 pp above
  null; magnitude criterion C). Pre-commit before running.
- [ ] Same null sample seed and same 4-day lead-up window machinery
  as scripts 08/09/12 for direct comparability.
- [ ] Caveat to flag in any result writeup: >85% of ME/CFS patients
  have chronotropic incompetence (blunted HR response). HR may
  under-report; honest interpretation if REFUTED is "the HR channel
  is blunted, not that overnight recharge is fine."
- [ ] Methodology lesson banked: 3-episode dry-run print before
  locking the spec.

**Why it's next.** Strongest external evidence of any remaining
candidate; computable now without H04b; the only remaining
waking-hour-adjacent test before the direction shifts to overnight
recovery; provides the empirical stake for the D7 reframe that
HA01b was supposed to provide but no longer does.

---

### C.2 — Cognitive / emotional load mining from notes + tags

**Intention.** A precursor hypothesis test, not a descriptive
one-pager. The notes v2 work already showed late-era lead-up days
carry +12 pp `belasting_cognitief` mention and late-era crash days
carry +22 pp `belasting_gezin` mention. The activity-labels work
*originally* showed HA01b (4-day exertion shock) as a candidate
validate-era precursor, but the Theme A bundled re-test refuted that
finding on the cleanest baseline — the +17.3 pp was substantially a
rolling-baseline construction artifact. **C.2 asks the interaction
question regardless**: does tag-load × exertion-class predict dips
(or crashes) better than exertion-class alone? The interaction
question is independent of HA01b's main-effect verdict; even a null
main effect can carry information when conditioned on a tag-load
signal. C.2 becomes *more* important now that the Garmin waking-hour
layer is closed for validate-era crashes — the journal-layer signal
may carry what the biometric layer cannot.

**Pre-register before any model fits.**

**TODOs.**
- [ ] Define "tag load" precisely. Candidates:
  - count of cognitive/emotional tags in the lead-up window
  - rolling sum of tagged-load days across N days
  - distinct categories carried (mentaal vs gebeurtenis vs project)
  - decide single metric or test 2-3 in parallel under a pre-registered grid
- [ ] Decide outcome: `crash_v1` start (29 episodes) vs `crash_v2` dip
      (79 dips) vs both. The HA01 3-day dip finding (+9.3 pp) suggests
      dips may be the more sensitive outcome.
- [ ] Lock lead-up window. Default to 4-day to match HA01b's
      validate-era precursor finding; consider also testing 3-day to
      bracket.
- [ ] Lock the model. Likely logistic regression with main effects +
      interaction term, but spec it out before running. Specify how
      "interaction beats main-effects-only" is operationalised
      (likelihood ratio test? AIC delta? discrimination delta on
      held-out?).
- [ ] Same train/validate split as H##/HA01b (train 2022-09-03 →
      2023-12-31; validate 2024-01-01 → 2026-06-05).
- [ ] Pre-register falsification: interaction term coefficient must be
      meaningfully non-zero AND held-out validate discrimination must
      improve by ≥ X pp over class-only.
- [ ] Methodology lesson banked: do the 3-episode dry-run before
      locking the spec.

**Why it's next.** Cheap (uses existing notes v2 + activity-labels
outputs, no new data extraction) and directly tests the user's lived
framing that emotional/cognitive load combines with exertion to
trigger crashes.

---

### C.3 — Personal-lag teaching one-pager (descriptive)

**Intention.** A derivative artefact, not a hypothesis test. Combines
the crash_v2 + H02b + (now-softened) activity-labels results into a
single piece teaching the participant their own PEM lag pattern:
*"your dips tend to arrive 2–3 days after a heavy day."* Descriptive
only — no prediction bar.

**Important framing change post-Theme A**: HA01b's +17.3 pp validate-era
discrimination was refuted on the lagged baseline (Theme A bundled
re-test, 2026-06-06). The 4-day lag is no longer empirically validated
by a SUPPORTED test. The teaching can still be written, but its
empirical anchors are now (a) the H02b train-era 3-day stress-spike
precursor and (b) the participant's experiential framing
("trigger day, day after still ok, crash sets in day 2-3"). The
HA01b 4-day result becomes "consistent with the experiential framing,
but the underlying activity-shock signal does not survive a
methodologically clean baseline re-test." Honest, not a hook.

**TODOs.**
- [ ] Decide era framing now that the 4-day HA01b SUPPORTED claim is
      withdrawn. Options:
  - Unified experiential framing ("typically 2-3 days") with
      H02b 3-day train-era support as the empirical anchor and the
      validate-era as currently precursor-invisible on cleanest
      baseline.
  - Era-honest framing: train-era ≈ 3-day stress-spike precursor
      (H02b SUPPORTED); validate-era no waking-hour precursor yet
      validated on a clean baseline (HA06 morning RHR is the next
      candidate).
  - Whichever the participant prefers; both are honest.
- [ ] Pull numbers:
  - H02b 3-day discrimination (+29.9 pp train, SUPPORTED)
  - HA01b 4-day rolling-baseline discrimination (originally +17.3 pp
      validate; clearly state this was refuted on the lagged
      baseline at +4.0 pp per Theme A bundled re-test)
  - lag-profile peaks (exploratory, label as such — and also subject
      to the same rolling-baseline construction caveat now)
- [ ] Draft Dutch copy. Respect tone discipline:
  - reflective, no em-dashes ([no em-dash memory](../../C:/Users/Gebruiker/.claude/projects/c--Users-Gebruiker-Documents-gevoelscore-app/memory/feedback_no_emdash_in_ui.md))
  - presents conclusions not prescriptions (pacing-doc)
  - brainfog-readable in seconds (frontend-conventions)
- [ ] Identify 2–3 supporting crash examples with clear visible lag
      (e.g. a validate-era crash with a heavy day on D-4 and the
      anticipated D-1 "still OK").
- [ ] Decide delivery surface. Options:
  - paper-style one-pager (print/PDF) for the participant's own use
  - in-app card concept (later) — but not the same as the
    retrospective per-crash cards b / b2; this is a teaching piece, not
    a per-event surface
- [ ] Cross-link from [STOCKTAKE §4 Tier 1](STOCKTAKE.md#tier-1--strong-evidence-ready-to-prototype)
      once drafted — likely sits between cards (b) / (b2) and (c).

---

### C.4 — Recovery-completeness over time (descriptive)

**Intention.** Derivative one-pager. Tracks the participant's
*recovery* trend in a single monthly metric: percentage of
heavy/very_heavy days that were followed by a sustained return to
baseline. Builds on the **H05b sustained-recovery primitive**
(see Tier 3 below). Descriptive only.

**TODOs.**
- [ ] **Lock H05b sustained-recovery primitive first** (see Tier 3 below).
      Without a precise "returned to baseline" definition, C.4 cannot
      be computed. (Earlier drafts of this document used "C.1" to
      refer to this primitive; that was a naming overlap with the
      C.1 morning-RHR-delta indicator. Corrected: H05b is what C.4
      depends on; C.1 is the separate HA06-shaped pre-registered test
      above.)
- [ ] Decide the "heavy day" reference event:
  - `exertion_class ∈ {heavy, very_heavy}` (activity-labels output)?
  - any `crash_v1` episode start?
  - either, reported as two parallel series?
- [ ] Decide aggregation. Monthly %? Quarterly? Rolling 90-day?
- [ ] Compute series across full corpus 2022-09-03 → 2026-06-05.
- [ ] Plot alongside S01 stabilisation trajectories (max stress-spike
      duration, avg stress baseline, RHR, sleep efficiency) — so the
      recovery-completeness line shares an x-axis with the other
      pendulum signals.
- [ ] Honest framing of partial months and the May 2026 perturbation.
- [ ] Decide whether this lives standalone or as a panel inside the
      stabilisation-arc card (a) in [STOCKTAKE §4 Tier 1](STOCKTAKE.md#tier-1--strong-evidence-ready-to-prototype).

---

### C.5 — Volatility + dip-frequency progress metric (descriptive)

**Intention.** Derivative one-pager. A two-component progress
indicator showing whether the participant is stabilising: rolling
30-day standard deviation of `gevoelscore` (volatility) + monthly dip
count (frequency). Descriptive only.

**TODOs.**
- [ ] Compute rolling 30-day std of score across the full corpus.
      Edge-handling at the boundaries of the analysis window.
- [ ] Compute monthly dip count from `crash_v2` tier-2 labels
      ([labels CSV](garmin/hypotheses/crash_v2-definition/labels_crash_v2.csv)).
- [ ] Decide whether to also overlay monthly crash count (tier-1) or
      keep that for the stabilisation-arc card to avoid duplication.
- [ ] Plot together. Twin-axis (std left, count right) or two stacked
      panels.
- [ ] Honest framing of the May 2026 uptick already visible in S01.
- [ ] Cross-reference: this is a "progress" framing of the same
      pendulum [S01](garmin/hypotheses/S01-stabilisation-trajectories/notes.md)
      visualises through biometrics. Decide whether to ship this as a
      standalone card or as the score-side panel of the
      stabilisation-arc card (a).

---

## Deferred (paused with explicit gates)

### C.6 — Dip attribution

**Intention.** Per-dip retrospective card concept. Attribute each
isolated dip to its most likely contributing factor — exertion shock,
cognitive/emotional load, calendar event, notes content match, or
"no signal." Sits in the same family as Tier 2 (g) caregiving-context
tagging.

**Gate.** *Needs the daily-entry feature design call.* Where the
attribution UX surfaces (inside daily-entry retrospect, calendar
retrospective view, or a separate "look back" surface) determines the
shape of the attribution algorithm.

**TODOs (when un-gated).**
- [ ] Wait for daily-entry design to land enough to pick a surface.
- [ ] Algorithm sketch (rank-order what to surface for each dip):
  1. HA01b-flagged exertion shock in D-4 to D-1
  2. High tag-load (per C.2 once locked) in lead-up
  3. Notes-content match against crash-day signature vocabulary
  4. Calendar event in lead-up (once calendar binding event-type tags land)
  5. "No signal" — honest fallback
- [ ] Decide whether attribution is per-dip or per-dip-cluster (15
      clusters covering 45/79 dips). Cluster-level may be more useful
      for the "rough patch" narrative.
- [ ] May depend on dip_v2 split (almost-crash vs mood-only) — gated
      on H04b. If dip_v2 lands first, attribution can be subtype-aware.
- [ ] Tone: descriptive, no prescription. "What was happening?" not
      "you should have rested."

---

### C.7 — Intervention tagging

**Intention.** Foundation work for the eventual shielder-vs-reliever
experiment (the pacing-doc's eventual payload — Tier 3 (j) in
STOCKTAKE). Tag interventions taken (rest day, supplement,
medication, pacing change, social withdrawal) so we can later ask
"did intervention X reduce crash depth or recovery time?"

**Gate.** *v2 territory.* Substantial design work; cardinal-principle
applies — research first, build second.

**TODOs (when un-gated).**
- [ ] Cardinal-principle research first: characterise existing
      intervention language in the 686 notes BEFORE designing UI.
      Likely a "Goal C" round of notes analysis (parallel to Goal A
      crash-language and Goal B tagging-suggestion).
  - frequencies of mention (rust, medicatie, supplement names,
    pacing-vocabulary)
  - co-occurrence with crash / dip / recovery days
  - whether interventions are stated as planned ("ga vandaag rusten")
    vs done ("heb gerust") vs effective ("rust hielp")
- [ ] Design the tag taxonomy. Curated list vs user-defined vs both
      (with curated as starter). Locked-tag-categories memory
      ([project_tag_clusters](../../C:/Users/Gebruiker/.claude/projects/c--Users-Gebruiker-Documents-gevoelscore-app/memory/project_tag_clusters.md))
      already has `interventie` as one of the eight v1 categories —
      use it.
- [ ] Decide tagging mechanic:
  - inline in daily-entry tag picker?
  - separate "reflection" prompt at the end of the day?
  - retrospective tagging from the timeline view?
- [ ] Decide quantification: binary (tagged y/n) or graded (low /
      medium / high effort)?
- [ ] Hard pre-condition: H05b sustained-recovery primitive (Tier 3
      below) must be working — otherwise there is no "did the
      intervention help?" axis to measure against.

---

### H04b — Decode `unknown_233` for per-minute Body Battery

**Intention.** Unlock per-minute Body Battery data for intra-day
analyses. Specifically: count *occurrences* of BB-rise and BB-drop
events per day (the participant's framing that rises like a
middagslaap are themselves meaningful, not just totals). Unblocks
H03b (overnight BB recharge) and dip subtyping (dip_v2).

**Status.** Protocol fully locked at
[.claude/plans/adaptive-foraging-hamming.md](../../.claude/plans/adaptive-foraging-hamming.md).
Folder scaffolded at
[garmin/hypotheses/H04b-decode-unknown-233/](garmin/hypotheses/H04b-decode-unknown-233/)
(empty, awaiting execution).

**Gate.** Notes label-quality work (participant-requested) must
complete first.

**TODOs (when un-gated).**
- [ ] **Path C — Garmin Connect REST API.**
  - Stand up `cyberjunky/python-garminconnect`. Auth flow with the
    participant's Garmin Connect credentials, stored locally only.
  - ToS-grey awareness: internal endpoint
    `/wellness-service/wellness/bodyBattery/events/{date}`. Accepted
    for personal-use own-data analysis only.
  - Pull per-minute BB for the full corpus 2022-09-03 → 2026-06-05.
    Rate-limit-aware; expect this to take real wall-clock time.
  - Store as tall CSV `(date, timestamp, bb_value)` outside the app
    tree at `C:\Users\Gebruiker\Documents\gevoelscore-data\garmin
    data\bb_per_minute\` (mirror the GDPR-dump location convention).
- [ ] **Path B — Decode `unknown_233` from FIT.**
  - Extract raw `unknown_233` 4-byte payloads from a stratified sample
    of `monitoring_b` files (use the 60-file sample shape from
    `02_profile_monitoring_density.py` as a baseline; expand if needed).
  - Test ~12 candidate byte encodings against the Path C ground truth
    on a 180-day holdout (pre-registered, locked in the plan):
    b3 direct, b2:b3 int16 scaled, byte-delta, off-wrist flag in b1,
    etc.
  - If no direct encoding works: three pre-locked fallback strategies
    (joint-channel regression, state-buffer reframing, raw-stream
    feature mining).
  - Write up findings — small public contribution if direct decode
    succeeds (HarryOnline community sheet, FIT-SDK forum thread).
- [ ] After either path produces per-minute BB:
  - per-day feature extraction: rise-count, drop-count, rise-rate,
    time-of-day-of-lowest, drain-during-waking-hours.
  - join into the daily wide table for hypothesis testing.

---

### H03b — Overnight Body Battery recharge

**Intention.** Replaces H03 (sleep efficiency, refuted decisively).
Tests whether overnight BB recharge is a physiologically targeted
marker of unrefreshing sleep — a sleep precursor whose channel is BB
not efficiency.

**Gate.** *H04b must succeed first.* Without per-minute BB, the
recharge curve cannot be computed.

**TODOs (when un-gated).**
- [ ] Define "overnight BB recharge" precisely. Candidates:
  - `bb_wake − bb_sleep_onset`
  - recharge rate (delta per hour of sleep)
  - "fully recharged" boolean (BB ≥ 90 at wake)
  - normalise vs personal baseline (relative-not-absolute rule per
    [feedback_relative_not_absolute](../../C:/Users/Gebruiker/.claude/projects/c--Users-Gebruiker-Documents-gevoelscore-app/memory/feedback_relative_not_absolute.md))
- [ ] Pre-register falsification matching H02b's three-criterion bar.
- [ ] Same train/validate split as the H## series.
- [ ] Test against both `crash_v1` episodes (29) and `crash_v2` dips
      (79) — H03b on dips folded in from the start, not as a
      separate re-run.
- [ ] Methodology lesson banked: 3-episode dry-run print before
      locking the spec.

---

### Tier 3 — H05b spec (sustained-recovery target)

**Intention.** Recovers the H05 recovery-time card concept after the
v1 spec produced trivial 0-day recoveries (recovery target
`baseline − 1` was met definitionally the day after episode end). C.4
above is the monthly aggregation that builds on this primitive.

**Gate.** None — cheap to run, deferred only by priority.

**TODOs.**
- [ ] Lock new spec. Current candidate (from
      [registry.md §4](garmin/hypotheses/registry.md)): recovery =
      first day of a ≥2-consecutive-day sustained run with
      `score ≥ pre-episode baseline rounded down`.
  - "Pre-episode baseline" — define precisely. 30-day rolling
    median ending D-4? D-7?
  - "Rounded down" — keep, since baselines are typically 4.x.
  - Edge case: what if recovery is never sustained (the participant
    moves into a new lower baseline)? Cap at N days and report as
    "no sustained recovery within window."
- [ ] Same crash_v1 episodes (29).
- [ ] **3-episode dry-run print** before finalising — banked
      methodology lesson from H03 and H05 v1.
- [ ] Descriptive only — no prediction bar. Output median, IQR,
      range of recovery time.
- [ ] Feeds into C.1 lock (see Open question) → unblocks C.4.

---

### Tier 3 — Dictionary v3 (polarity-negation handling)

**Intention.** Cheap fix to a known bug in the notes v2 dictionary.
Substring matching for `polarity_positive` does not apply the 3-word
negation window that symptom matching does — so "het is echt **niet
fijn**" fires positive because "fijn" matches.

**Gate.** None — cheap, deferred only by priority. Estimated effect:
flips 1–2 of the 16 late-era positive-dominant crash days that the
verification round surfaced (real but small).

**TODOs.**
- [ ] Extend the v2 3-word negation window to polarity markers as
      well (same logic, applied to a different marker class).
- [ ] Re-run the v2 analyses end-to-end with v3:
  - clause-categorisation per day
  - era-shift table (notes v2 finding b — mixed-day topology +39 pp)
  - polarity-dominance counts on late-era crash days
- [ ] Report which v2 conclusions changed and which were robust to
      the v3 fix. The expected outcome (per the verification round):
      finding b is mostly robust; the absolute positive-dominant
      count for late-era crashes shifts by 1–2 days but the +39 pp
      direction holds.
- [ ] Update `categories-analysis-v2.md` with a v3 amendment, not
      a fresh document, unless changes are pervasive enough to
      warrant a separate write-up.

---

*Living document. Items move from Upcoming to Deferred (or vice
versa) as gates open and priorities shift. When an item is started,
record the start date here and link to its working folder; when
closed, link to its result writeup and remove from this list.*
