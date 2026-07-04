# Research-thinking note — site scope, score-watch epistemics, Step 1 steel-manning

*Conversation date: 2026-06-26. Captured as essence, not transcript.*

## Why this note exists

A mid-research thinking session that produced (a) one documentation edit, (b) a clearer site scope model, (c) several reframings worth not losing, and (d) a concrete to-do list for steel-manning the foundation layer. Logged here so future-me (or another session) can pick up the thread without re-deriving it.

---

## Trigger

Starting question: *"Do we see a different autonomic signature (stress, body battery, lowest HR, bout variables, peak measurements) on crash/dip days vs good days? Do we have data collection planned, or already collected, on this?"*

Triggered by reading [topic-stress-fatigue-pacing.md](analyses/translation/patient-audience/topic-stress-fatigue-pacing.md) and pausing on a line about whether Garmin-stress means the same thing Wiggers means by "stress" — same epistemic family as the score-watch correspondence question.

---

## Coverage map that came back

**Already done** (crash vs dip vs all-days baseline):

- [cohort_topology/findings.md](analyses/descriptive/trajectory/cohort_topology/findings.md) (2026-06-25): 7 autonomic channels via z-score trajectory `[t+1..t+5]`. Crashes substantively deeper than dips on every channel (e.g. RHR +1.45z crash vs +0.37z dip; bb_lowest −1.46 vs +0.18). Multi-channel coherence — same direction, severity-scaled.
- [HA-P6 v3 result.md](analyses/hypotheses/HA-P6/result.md) (2026-06-17): 4/7 channels distinguishable from matched non-event days via paired stationary-bootstrap CIs.

**Considered and declined** (with reasons):

- **Q1 — discriminativeness / AUC / ROC**: capped by data, not methodology. Base rate ~2 crashes/year; small positive count makes ROC CI uninformative. Tier-C ("wrong 24 of 25") in [card-b-train-specificity.md](analyses/garmin_exploration/cards/card-b-train-specificity.md) is the current honest separation bound. Also: `_plan_results_analysis_layer.md §3.10` explicitly forbids classifier metrics at HA-level (belongs at actionability layer, post-replication).
- **Q2 — retrospective inference into unlabeled Stratum 1/3 era**: methodologically thin. No ground truth in unlabeled period by definition; validation reduces to post-hoc subject recall on 3-4-year-old events against current theory of the case — textbook confirmation-bias setup. Honest as narrative (cf. [lived_experience_garmin_pacing_2026-06-14.md](lived_experience_garmin_pacing_2026-06-14.md)), not as science.
- **Q3 — healthy-era null check** (expect no crash signature in Stratum 1, n=217): sounds rigorous, isn't. Single 7-month Aug-Mar window confounds illness state with season (already flagged in `lc_era_temporal_segmentation §1`); device-generation confound (FR935 vs FR245); age/baseline confound. Even a clean "0 fires" result has 3 alternative explanations none ruleable-out from this data.
- **"Good day" symmetric counter-pole to crash_v2**: structurally infeasible. The gevoelscore distribution is left-tailed with upper register compressed near 5-6 (ceiling effect of recalibrated self-report in chronic illness). No positive tail to anchor against. cohort_topology and HA-P6 chose the right comparators by instinct given this data shape (pooled-baseline z-score, matched non-event days) — these are exactly what you do when the positive tail is missing.

---

## Edit landed during conversation

**[crash_v2-definition.md §6 Caveats](analyses/hypotheses/crash_v2-definition/definition.md)** — added one bullet:

> No symmetric positive counter-pole in this dataset. A "good day" definition mirroring crash_v2 on the right tail is structurally infeasible: gevoelscore distribution is left-tailed with upper register compressed near 5-6 (ceiling effect of recalibrated self-report in chronic illness). Comparators for crash analyses therefore use pooled-baseline z-scores or matched non-event days, not "good vs crash" contrasts. This is a documented design choice grounded in the data shape, not a methodology gap.

Conversion of what looked like a gap into a documented design choice. Saves future-me from re-asking.

---

## Pivotal reframings (do not lose these)

### 1. From "score validation by watch" → "two windows on the same upstream cause"

Initial framing for the proposed website panel was "does the body agree?" (validation-y). Wrong epistemics. The score and Garmin's derived measures are BOTH downstream of the same physiological substrate (HRV, RHR, autonomic state). They're not independent measurements one can validate the other; they're two reads on the same upstream cause through different machinery.

Layered model of the gevoelscore:
1. **Physiology** — real autonomic state
2. **Interoception** — brain's read of layer 1 (noisy in LC / brainfog)
3. **Cognitive overlay** — mood, expectation, narrative, attention
4. **Score** — the 1-10

The watch reads layer 1 close to directly. Score = layers 1+2+3 compressed through verbal-numeric channel. When they agree, they're agreeing about layer 1 — expected, not an independence-supplying validation. When they disagree, the disagreement is informative: score sees layers 2-3 watch can't; watch sees layer-1 changes that may not have crossed into felt awareness.

Honest claim shape: "both register the same underlying body state; agreement is the expected shape of shared-cause measurement; disagreement is research material."

### 2. From "watch as companion for chronic illness" → "Step 1+2+3 scope" (the big realignment)

I was scaling outward into "can the watch be used as a companion to understand the body as a chronic illness patient" — and the user pulled it back. The site's scope is strictly bounded:

| Step | Claim | Status |
|---|---|---|
| 1 | The watch produces signal at all (vs noise) | Assumed, audit-hooked (device-baseline lag, device-change points). **See steel-manning to-do below.** |
| 2 | Signal connects to felt experience | **Met** — cohort_topology + HA-P6 |
| 3 | Wiggers' named channels behave as she says, on this body | In progress — Tier 1/2/3 register in [wiggers_testable_hypotheses.md](wiggers_testable_hypotheses.md), with verbatim-source-verification, pre-registered operationalisations on `per_day_master.csv`, prior-test family acknowledgement, stop-rules |

Anything past Step 3 lives in [personal_hypotheses.md](personal_hypotheses.md) — P1-P7 — with **a different validation discipline**: descriptive characterisation only, no held-out required, named priors before any look at the corpus, forward-collected data as natural validation, validated-era stratification. Not the same kind of work, not the same verdict standards.

Confounders ARE built into the design at Step 3 — citalopram dose-response (multi-channel per-phase stratification on stress_mean_sleep / all_day_stress_avg / bb_lowest), seasonality (`seasonality_dow/findings.md`), era / device generation (`lc_era_temporal_segmentation.md`), crash-distortion sensitivity (CONVENTIONS §3.4), Holm step-down multiplicity, block bootstrap for autocorrelation.

What I was treating as "missing methodology MDs" was overreach. The scaffolding is already tighter than I gave it credit for.

### 3. From "validation reading" → "instrument-resolution + research-enabler reading" for the website panel

Best framing for the **what-is-a-crash** page panel:

> **Why the rest of this site is possible.**
>
> A crash defined on the score also shows up on the watch: about 1 standard deviation above the personal baseline on resting heart rate and on overall stress, about 1.5 below baseline on body battery's daily low. Dip days move the same channels in the same direction, about a third as far. Normal days sit near baseline.
>
> The two measurements — the felt-state score and the watch's autonomic signals — pick up the same days, in proportion to severity. That overlap is what makes it worth analysing them together. Most of the rest of this site does exactly that.

Placement: between **Two tiers** and **Why a score, not the PEM tag**. Calibrated: corroborator + severity mirror, NOT predictor / oracle / actionability. Doesn't trip §3.10 (no claims of discriminative or predictive power).

Open: needs to see actual site architecture before deciding self-contained-panel vs panel-with-forward-link-to-findings-section.

---

## Steel-manning Step 1 — the to-do that came out of this conversation

Step 1 is currently "assumed, audit-hooked." Three cheap moves to strengthen it:

### A. Literature backbone (highest leverage, lowest effort)

The literature folder already contains the validation papers — they're not synthesized as the evidential base for Step 1. Pull these into a short methodology MD (`methodology/watch_signal_validity_evidence_base.md` or similar):

- [quer_2020_daily_rhr_variability_n92k.pdf](literature/quer_2020_daily_rhr_variability_n92k.pdf) — n=92k consumer-wearable RHR validation
- [nelson_2020_wrist_wearable_hr_guidelines.pdf](literature/nelson_2020_wrist_wearable_hr_guidelines.pdf) — wrist PPG capability bounds
- [shaffer_2017_hrv_metrics_and_norms.pdf](literature/shaffer_2017_hrv_metrics_and_norms.pdf) — HRV-derived measures
- [vancampen_2022_mecfs_rhr_elevated.pdf](literature/vancampen_2022_mecfs_rhr_elevated.pdf) — RHR sensitivity in ME/CFS
- [mooren_2023_postcovid_hrv_autonomic_dysregulation.pdf](literature/mooren_2023_postcovid_hrv_autonomic_dysregulation.pdf) + [suh_2023_lc_hrv_systematic_review.pdf](literature/suh_2023_lc_hrv_systematic_review.pdf) — LC-population HRV signal validity

One paragraph per paper: what it establishes about wearable signal validity at the device/population/population-of-interest level.

### B. Built-in positive control via Stratum 2 (acute COVID infection)

Stratum 2 is 14 days (2022-03-21 → 2022-04-03) of a known autonomic perturbation. Built-in positive control: if the watch were producing noise, it shouldn't have shown a measurable shift beyond Stratum 1 baseline fluctuation. One descriptive analysis: per-channel z-score of Stratum 2 vs Stratum 1 distribution on the cohort_topology channel set. Comparator n=217 (large), event n=14 (adequate for shape detection).

Bonus value: if Stratum 2's signature resembles the crash signature, that's biologically coherent (both autonomic stress events) and tightens the construct.

### C. Multi-channel coherence reframing (free)

cohort_topology's 7-channel coherence (same direction, severity-scaled) on crash days is currently labelled as a finding about crashes. It's *also* a noise-rejection argument — random noise wouldn't cluster across 7 channels like that. Add a sentence to wherever the cohort_topology finding gets cited as foundation: "this also rules out the random-noise hypothesis at Step 1."

### Combined effect

After A+B+C: Step 1 reads "assumed, audit-hooked, AND positively supported by (a) external validation literature including in this patient population, (b) detection of a known autonomic event on this body, (c) multi-channel coherence ruling out random-noise hypothesis." Three independent lines of evidence.

**What NOT to chase**: device-level experiments (no gold-standard reference data); redoing Firstbeat's algorithm validation.

---

## What I retracted during the conversation (so I don't drift back)

- The framing "the project rests on the watch being useful as a chronic-illness companion" — too broad. The project rests on the narrower bounded claim of Steps 1+2+3.
- The Q1/Q2/Q3 chain as "gaps to fill" — they're out of scope by design, not gaps.
- The "missing methodology MDs" framing for good-day-def, retrospective-inference, healthy-era-null — none of these belong; the first is structurally infeasible, the second two are out of scope.
- The "watch as actionable pacing tool" or "watch reveals body state felt sense misses" — these are Wiggers' deeper claims and lie beyond what this dataset can corroborate (would need physiological gold-standard or prospective behavioural arm). Out of scope; the site doesn't claim them.

---

## What's left open

1. **Steel-man Step 1** per A+B+C above. A is producer-mode methodology drafting (would need `/research-methodology-review` in a fresh session); B is a small descriptive analysis (would need `/research-interpret` D-stage); C is a one-sentence reframing where cohort_topology gets cited as foundation.
2. **Website panel content + placement**: needs sight of overall site architecture before committing the snippet.
3. **A "scope boundary" page on the site**: small section naming the Wiggers register (this site's scope) vs personal register (sister section, different discipline) vs explicitly out-of-scope (Wiggers' deeper claims about pacing efficacy / body-state-felt-sense-misses, not addressable from this data). Different shape from a traditional "limitations" page — explicit about what the site IS and ISN'T doing.

---

## Epistemic principles surfaced that are worth keeping

- **Multi-channel coherence rules out noise** — load-bearing argument both for Step 1 and Step 2.
- **Shared upstream cause ≠ independent validation** — when two measurements share a cause, agreement is expected; the agreement supports the underlying state, not one measurement validating the other.
- **Disagreement cases are research material** — score-without-watch-confirmation (layer 2/3 carrying the burden) and watch-without-felt-experience (silent layer 1) are both interesting and informative.
- **Two registers, two disciplines** — Wiggers vs Personal isn't just content separation, it's validation-standard separation. Don't conflate them.
- **Bounded scope is what makes corroboration credible** — the site's strict Step 1+2+3 framing is a feature, not a limitation.

---

## Cross-references

- [crash_v2-definition.md](analyses/hypotheses/crash_v2-definition/definition.md) — caveat added during this conversation
- [wiggers_testable_hypotheses.md](wiggers_testable_hypotheses.md) — the Step 3 spine
- [personal_hypotheses.md](personal_hypotheses.md) — the beyond-Wiggers register
- [cohort_topology/findings.md](analyses/descriptive/trajectory/cohort_topology/findings.md) — Step 2 foundation
- [HA-P6 v3 result.md](analyses/hypotheses/HA-P6/result.md) — Step 2 strengthening
- [CONVENTIONS.md](CONVENTIONS.md) §1 (producer/reviewer split), §3.4 (crash-drop sensitivity), §5 (anchors)
- [_plan_results_analysis_layer.md §3.10](methodology/_plan_results_analysis_layer.md) — classifier-metric rule
- [lc_era_temporal_segmentation.md §1](methodology/lc_era_temporal_segmentation.md) — Stratum boundaries (relevant for Step 1 positive-control candidate)

---

## Continuation 2026-06-26 — lived-definitions anchor landed

Participant authored the lived-functioning definitions for gevoelscore levels 1-6. Captured as a stable reference at [gevoelscore_lived_definitions.md](gevoelscore_lived_definitions.md).

### What it adds

- **Anchors the crash_v2 thresholds in lived phenomenology**: levels 1-3 = volledig-or-grootdeels uitgeschakeld with active symptoms; the "≤ 3 for ≥ 2 days" rule maps to "largely-or-fully shut down with active symptoms for at least two consecutive days" — the lived shape of a PEM episode.
- **Confirms the no-good-day caveat from this morning** (crash_v2-definition.md §6): the lived ceiling at 6 corresponds to "level 5 but with end-of-day reserve" — not anything a healthy person would call a good day. The compressed upper register is the lived experience, not a measurement artefact. The structural-infeasibility framing of the "good day" comparator is now anchored in participant-authored lived definitions, not just in distribution shape.
- **Cluster structure self-emerges** (volledig 1-2 / grootdeels 3-4 / deels 5-6) — independent of the project's other three-cluster framing, the lived definitions cluster the same way.
- **Strengthens the score-watch correspondence story**: the graded autonomic-load story cohort_topology established maps directly to a graded lived state (minimal motion → active symptoms during attempted activity → functional within narrow envelope). The watch is detecting a graded lived gradient, not just a statistical category.
- **Foundational for the site**: directly anchors the existing what-is-a-crash page's *"the score runs 1 to 10, but in four years it never once rose above {ceiling}"* line. Readers can now be shown what each level actually means in lived terms.

### Edits / additions this turn

- Created [gevoelscore_lived_definitions.md](gevoelscore_lived_definitions.md) — stable anchoring reference, indicative not rigid, Dutch (participant's voice) preserved verbatim, with English meta-framing.

### Open items added by this turn

- **Site-side integration of lived definitions**: when the what-is-a-crash page's panel is drafted, the lived definitions should be available as deeper anchor. Could be inline (compact summary) or linked-to (full doc surfaced separately). Decision: needs the broader site architecture in view.
- **Cross-reference from crash_v2-definition.md**: the operational definition doc currently does not cite the lived-definitions doc. Adding a one-line pointer would help future readers understand WHY the ≤ 3 threshold was chosen at the threshold it was chosen at. (Not done in this turn — flagging only.)

### What the lived definitions did NOT change

The site scope (Steps 1+2+3 with personal_hypotheses sister register) is unchanged. The Step-1 steel-manning to-do (literature backbone + Stratum 2 positive control + multi-channel coherence reframing) is unchanged. The lived definitions strengthen the foundation; they do not redirect the project.

---

## Continuation 2026-06-29 — site-side floor panel landed; promotion-to-room question

### Site-side panel landed

The editor acted on the handoff. A "Does the watch see anything real?" panel is now live with subtitle "The watch is producing signal, not expensive noise" and chip "THE FLOOR WE'RE STILL REINFORCING". Panel covers:

- Multi-channel coherence as primary argument (RHR up + body battery floor down + stress up, severity-graded — "noise doesn't organise itself into a coherent, severity-scaled fingerprint like that")
- Honest caveat that channels share autonomic cause so they're not independent witnesses (weight is in coherence + grading, not count)
- Two checks in flight named explicitly: Stratum 2 COVID positive control + literature backbone
- Forward link to seven-signals-or-one

Calibration tone is right: confident-but-bounded, names the uncertainty, doesn't overpromise.

### Six additional Step-1 reinforcement options surfaced

In response to "what else can reinforce this floor", six further options were identified, ranked by leverage:

1. **Citalopram dose-response as second positive control (highest leverage, already done, never framed as Step-1 evidence)** — research has CONFIRMED dose-response on stress_mean_sleep (+0.43/mg), all_day_stress_avg (+0.57/mg), bb_lowest (−1.13/mg) per [citalopram_dose_response_stress_mean_sleep.md §5.6](methodology/citalopram_dose_response_stress_mean_sleep.md). When a substance with known physiological effects changes dose, the watch registers it monotonically across three channels. Cleanest available Step-1 evidence. Currently only framed as confounder on [the-citalopram-question](https://github.com/wmasman/wiggers_research_story/site/src/pages/workings/the-citalopram-question.astro); needs reframing dual-role (confounder for per-channel readings + positive control for signal validity).
2. **Stratum 1 (pre-illness) vs Stratum 4 (LC era) as illness-state detection** — if autonomic measures shift in expected direction between eras despite known confounds (season, device, age), that's evidence the watch detects the illness as a state. Confounds work against detection, so detection-despite-confounds is the strong argument.
3. **Sleep-window signal quality** — already documented in [hrv_proxy_via_stress.md](methodology/hrv_proxy_via_stress.md) Checks 7.1-7.3: stress_mean_sleep d=+0.90 episode-level on crashes. At the cleanest measurement window (sleep, near-zero motion artefact), signal carries cleanly. Half-sentence addition.
4. **Internal cross-channel coherence beyond crash days** — stress_mean_sleep ↔ resting_hr r=0.342 (related but not collinear). Shape of "two real signals reading related but distinct things" — different angle on noise rejection.
5. **Algorithm provenance** — Firstbeat-published validation of Garmin's stress + body battery algorithms; cite for derivation integrity (separate argument from sensor validity).
6. **Plausibility / absence of failure modes** — noisy periods identified and excluded (device-baseline-lag windows, imputed BB periods); what's left has been screened, not assumed clean. Argument-by-discipline.

### Idea: promote the floor panel to its own room?

Editorial question raised: should "Does the watch see anything real?" become its own Workings room rather than a panel on what-is-a-crash?

**Recommendation: yes, with specific conditions.**

Arguments for:
- Step 1 is genuinely load-bearing for the whole site; visible structural weight matches its actual role
- The material exists and has narrative arc (question → primary evidence → second positive → in-flight checks → honest caveat → forward link) — five-beat structure, not padding
- Serves the journalist / skeptical-reader audience segment per content-map (primary, not secondary) — they need a citable destination, not a sidebar
- Gives in-flight Stratum 2 + literature backbone material a home to land in when complete; without a room they'd either expand the panel without end or scatter across pages
- Pairs naturally with adjacent rooms: from-watch-to-number (pipeline) + what-is-a-crash (definition) + what-this-watch-cant-see (limits) → adding "is the signal real" completes a Part-1 quartet

Arguments against (real, worth respecting):
- The current panel works; promotion might be wanting-more-because-possible
- The argument doesn't change in a room vs panel — more text, same conclusion → diminishing returns
- Every new room is friction in the Workings index (already 13 rooms)
- The honest concession "this is the link we lean on most lightly" lands MORE strikingly as a confession in a panel than as a section header in a page

**Conditions for promotion if pursued:**
1. Keep the existing panel on what-is-a-crash as door/teaser linking to the room — don't remove it
2. Room must be structurally different from a longer panel (sub-headings, breathing room, a visual for multi-channel coherence shape, real narrative beats); if it'd just be panel-but-longer, don't promote
3. Title in question-voice matching site tone: *Does the watch see anything real?* (room title) — keeps the calibrated-doubt register established by the panel
4. Use the room to dual-role citalopram via cross-link from [the-citalopram-question](https://github.com/wmasman/wiggers_research_story/site/src/pages/workings/the-citalopram-question.astro) — "and here it works as a positive control too" — so both pages get the framing without either carrying the whole argument
5. Reserve room for in-flight material: structure so Stratum 2 COVID + literature backbone land as named subsections that fill in when research completes

**The risk to manage:**

Promoting to a room formalises "is this real?" as a question the site visibly worries about. Reads two ways:
- ✅ Honest researchers acknowledge the floor they stand on and check it — the desired reading
- ❌ If they had to write a whole page defending this, maybe it's shaky — the undesired reading

Mitigation: structure each subsection to RESOLVE into a positive ("check passes"). Stack of passes, one acknowledged uncertainty, two in-flight = discipline. Page that reads as defense = anxiety. Tone is binary; getting it right is what justifies the room over the panel.

### Open editorial decision

Final call belongs to the editor/designer per the [handoff doc decisions list](../../../../wiggers_research_story/site/docs/handoff-foundational-layer-from-research-2026-06-26.md). My research-side recommendation is "yes, promote with the five conditions and tone discipline." Research-side will continue to feed material as Stratum 2 + literature backbone complete; placement (room vs panel-with-fold-outs) doesn't change what research produces, only where it lands.

### Research-side action items added by this thread

None new. The Step-1 steel-manning to-do is unchanged (literature backbone + Stratum 2 + multi-channel coherence reframing) — the "promote panel to room" question is downstream of that work, not gated by it.
