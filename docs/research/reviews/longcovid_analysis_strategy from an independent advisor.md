# Analysis Strategy — N=1 Long COVID Crash/PEM Study

**Purpose of this document:** a handoff brief for a data analyst/statistician with access to the real data. It states the questions, the data, the design, and — most importantly — the validity threats and the *gates* that decide whether each finding is honest or circular. It is deliberately opinionated. Where I flag a risk, treat it as a requirement to check, not a suggestion.

**Status:** strategy only. Two structural facts are still unknown at time of writing (see §10) and should be resolved before building the pipeline, as they change the architecture.

---

## 1. Subject and goals

Single-subject (N=1) longitudinal study of one person's trajectory: healthy → acute SARS-CoV-2 infection → long COVID aftermath. The analytic interest is post-exertional malaise (PEM), pacing, and crash dynamics.

Four goals, **listed in order of how defensible each is** — this ordering should govern effort and the order of build:

- **A — Corroborated crash/dip timeline.** A single timeline of crashes and dips, with each event tagged by how many independent sources corroborate it (subjective gevoelscore, symptom notes, Garmin physiological "fingerprint"). *Strongest deliverable. Build fully.*
- **B — Exertion / pacing → crash.** Whether exertion and pacing patterns precede crashes. *Feasible, conditional on the gates in §4.*
- **C — PEM lag.** The delay between an exertion and the subsequent malaise. *Hardest and most prone to spurious confidence. Feasible only as a confirmatory test of a pre-specified lag window (see §7), not free estimation.*
- **D — Null result.** It may not be possible to recognize these patterns at all. **This is a pre-committed, reportable outcome, not a failure.** With this many metrics × lags × crash-definitions, a pattern can always be found by searching; D is the discipline that guards against that.

---

## 2. Data sources

| Source | Granularity | Role | Notes |
|---|---|---|---|
| **Gevoelscore** (subjective feel score) | Daily | Primary label input | Subjective; autocorrelated |
| **Symptom & exertion notes** | Per-day, multiple origins | Label input + exposure | Free text; basis for hand-coded load. **Note: the same text feeds both the crash label and the load exposure — see §4.3 shared-source confound** |
| **Hand-coded load scores** — cognitive, emotional, physical | Daily | Primary exposure (B/C) | Constructed *retrospectively* but *blind to whether a crash followed* (see §4.1) |
| **Garmin full data download** (FIT + exports) | Sub-daily → aggregate | Physiological corroborator + objective exposure | Overnight metrics are cleanest; daytime/derived metrics are circular |
| **Contextual timeline** — single & multi-day events (holidays, weekends away, job loss), interventions (coaching periods/sessions, medication) | Event/interval | Covariates & confounders | Both exposures and confounders; must be modeled, not ignored |

**Garmin metric hygiene (important):**
- *Cleanest, least activity-confounded:* overnight HRV, sleeping resting HR, respiration rate. Use these as the backbone of the physiological fingerprint.
- *Derived / partly circular:* "stress" is itself an HRV transform; Body Battery is a composite. Usable but not independent evidence.
- *Activity exposure:* steps, intensity minutes, training load — valuable precisely because they are an **objective, contamination-free parallel** to the hand-coded physical load (see §4.2).
- **Wear-gaps must be flagged explicitly.** Non-wear masquerades as low activity / missing physiology and will bias anything that treats absence as a low value.

---

## 3. Goal-by-goal feasibility verdict

- **A:** Solid. Execute in full.
- **B:** Feasible *iff* the blind-recode gate (§4.1) survives, objective Garmin exposure agrees with hand-coded load (§4.2), **and** the shared-source confound is broken by decoupling the label from the notes or separating the two extractions (§4.3).
- **C:** Feasible *only* as a confirmatory test of a pre-specified 1–2 day onset window via event-anchored averaging (§7), reported with within-regime cross-validation (not a naive late-period hold-out — see §7 Phase 5) and a negative control. Not as a free multi-parameter lag estimation — the event count forbids it (§5).
- **D:** Keep live throughout. Pre-commit to it.

---

## 4. The three gates for B and C

These are not afterthoughts. If they fail, B and C are circular and should not be reported as findings.

### 4.1 Leakage / hindsight gate (load coding)
Load was coded retrospectively but blind to the specific outcome. **This reduces but does not eliminate the threat.** Hindsight bias ≠ outcome-blindness: a global memory of which stretches were rough can bleed into load scores in a way that is *correlated with the outcome*. That is differential (outcome-correlated) measurement error, which *manufactures* associations rather than merely weakening them.

**Required check — blind re-code:** pull a random subset of ~30–40 days' note text; strip dates and surrounding context; shuffle order; re-score load from the note alone (ideally a separate rater or an LLM with no timeline access). Then:
1. Agreement of re-coded vs original scores (inflation estimate).
2. Whether re-coded scores **still predict crashes** as strongly. If the association survives blinding → real. If it shrinks → you have quantified the hindsight inflation, and the original estimate is biased upward.

### 4.2 Objective-parallel gate (physical load)
Channel asymmetry: **physical** load has an objective corroborator (Garmin activity); **cognitive** and **emotional** load have none. Therefore any headline finding resting on cognitive/emotional load is the *least* defensible — hindsight has the freest hand there and nothing external can check it.

**Required checks:**
- Run the exertion→crash analysis twice: once with hand-coded physical load, once with Garmin activity. Agreement → strong. Hand-coded predicts but objective activity does not → **treat the divergence as a symptom of leakage, not a discovery.**
- Confirm hand-coded physical load correlates with same-day Garmin activity. If physical load predicts crashes but same-day activity is unremarkable, the score is capturing a retrospective sense of "that was too much" rather than exertion — i.e., the leak made visible.

### 4.3 Shared-source confound (notes drive both label and exposure)
This is distinct from §4.1 and survives even if §4.1 passes cleanly. The crash **label** is built from gevoelscore + notes; the load **exposure** is also coded from the *same* notes. One document generates both variables, so a load–symptom association is partly a shared-method artifact rather than a relationship between two independent measurements. Outcome-blindness (§4.1) does not fix this — even a perfectly outcome-blind coder reading one note to produce both "symptoms today" and "load today" couples them through shared wording, mood, and recall in that single text.

**Mitigations (at least one required before B is reported):**
- **Decouple the label from the notes.** Define the crash label primarily from **gevoelscore + Garmin anomaly**, holding the notes for *exposure only*. This removes the shared text from the label side. (Depends on the Garmin fingerprint being real enough to carry label weight — established in the corroboration phase; if it isn't, fall back to gevoelscore-only labels, still notes-free.)
- **Separate the two extractions.** If the notes must feed both, have symptom-extraction and load-extraction done in *independent passes* by different raters (or different LLM sessions with disjoint instructions), so the two variables are not produced in one reading.
- **Report the exposure built from Garmin activity as the primary B result**, with the notes-derived load as corroboration — Garmin activity shares no source with the notes-derived label.

---

## 5. Power and the event-count ceiling

Statistical power lives in the **number of crash events** (~15–25+), not the number of days.

- Working rule: ~1 trustworthy estimated parameter per ~10–15 events. Budget is therefore **1–2 predictors plus a lag**, not a distributed-lag model across 3 load channels × multiple lags × interactions. Fitting the large model will return coefficients that are noise dressed as findings.
- **Independence caveat:** if crashes cluster in one regime (e.g., the early severe phase), effective N is *below* the raw count — clustered events share context. Check the distribution of events across the timeline before trusting any confidence band. If bunched, the lag claim is *within-period*, not general — state it as such.

---

## 6. Key decision points — explicit tradeoffs

Several choices below are genuine forks, not solved problems. Each trades one validity property for another, so the "right" answer depends on which goal you are serving. Where there is a clear default I say so; where it is a true judgment call I say that instead of pretending otherwise. **None of these should be made silently — whichever branch is taken should be stated in the write-up.**

### 6.1 Label definition source — the central fork
Affects A and B differently, and you cannot optimize both at once.

| Option | Buys | Costs | Use when |
|---|---|---|---|
| **Gevoelscore only** | Maximal independence: shares no source with notes-derived load *or* Garmin, so it can be both a clean label for B and leave Garmin free to corroborate A | Noisiest label — one subjective channel, no triangulation; weak events may be missed | Default for **B** if the fingerprint is weak |
| **Gevoelscore + notes** | Richest, most sensitive label | Shares source with the load exposure → confounds B (§4.3); fine for A | Default for **A** |
| **Gevoelscore + Garmin** | Breaks the shared-source confound for B *and* gives a physiologically grounded label | Spends Garmin's independence — you can no longer claim Garmin "corroborates" that same label in A; depends on the fingerprint being real (Phase 3) | **B**, *if* Phase 3 shows a real fingerprint |

**Recommended:** run A and B with *different* labels — `gevoelscore + notes` for the corroboration timeline, a notes-free label for B — and state both openly. The alternative (one label everywhere) is simpler to report but forces you to sacrifice either A's triangulation or B's independence.

### 6.2 Conditioning on prior state — under- vs over-control
Threat #2 ("good day → did more") says you must condition on prior state. But yesterday's gevoelscore may sit *on the causal path* (good day → more exertion → crash), so controlling for it can also remove part of the real effect you're trying to measure.

- **Don't condition:** captures the full exertion→crash path, but contaminated by the prior-good-state confound — likely *overstates* the exertion effect.
- **Condition on prior state:** removes that confound, but if prior state is a mediator you *understate* the effect (over-control / partial collider risk).
- **Recommended:** report *both*, framed as bounds — the unconditioned estimate as an upper bound, the conditioned as a lower bound, with the truth between. This is more honest than picking one and is the only defensible move when the causal graph is uncertain in an N=1 design. Do not present a single conditioned coefficient as "the" effect.

### 6.3 Detrending — residualize vs covariate
- **Residualize** (remove the recovery trend, analyze only daily fluctuations): cleanly kills the shared-recovery-curve confound, but also deletes any *real* exertion→crash relationship that operates on a slow, multi-week timescale.
- **Trend as covariate** (keep the levels, adjust for trend): preserves slow-timescale signal, but the trend is collinear with regime and with slow exertion patterns, so adjustment is imperfect.
- **Recommended:** residualize as primary (the PEM hypothesis is a *fast* day-scale effect, which survives detrending), trend-as-covariate as a sensitivity check. If the two disagree, the effect lives on the slow timescale and you should say so rather than average them away.

### 6.4 Lag window for C — confirmatory vs exploratory
- **Confirmatory only** (pre-specified 1–2 day window, §7): spends the scarce events well, controls false positives, but will *miss* a real lag at a different delay — some PEM reports describe onset out to 72h.
- **Exploratory scan** (test lags 0–4+): finds an off-expectation lag if it exists, but with ~20 events a multi-lag scan will surface a spurious "best" lag readily.
- **Recommended:** confirmatory 1–2 day window as the *primary, reported* test; a wider exploratory scan permitted *only* as explicitly-labeled secondary/hypothesis-generating, never promoted to a headline. This buys one honest confirmatory result plus a flagged lead for a future dataset, without laundering exploration as confirmation.

### 6.5 Anomaly-baseline window length — a timescale tradeoff
The rolling baseline (§7 Phase 2–3) has no free lunch on window length:
- **Short window** (~1–2 weeks): adapts fast to regime change, but a slow multi-week crash gets absorbed *into* the baseline and becomes invisible.
- **Long window** (~6–8 weeks): detects slow crashes, but lags regime transitions and will over-flag during the steep early-recovery slope.
- **Recommended:** no single correct value — run two or three window lengths and report which events are robust across them. Events that appear only at one window length are timescale-specific, not artifacts, but should be labeled as such.

### 6.6 Load channels under the power budget (§5)
You have budget for ~1–2 predictors, but three load channels (physical / cognitive / emotional).
- **Physical-only (objective-anchored):** most defensible — has the Garmin parallel (§4.2), no shared-source escape hatch — but ignores cognitive/emotional exertion, which for many PWME is the *dominant* PEM trigger. Risks a false null on the very mechanism of interest.
- **Composite load (all three):** tests the full hypothesis, but burns the power budget and leans on the two channels with no external check and the freest hand for hindsight.
- **Recommended:** physical-objective as the primary confirmatory predictor; a single pre-specified composite (or the one non-physical channel you most suspect) as one labeled secondary test. Do not enter all three plus interactions — that is the §5 noise-as-findings trap.

### 6.7 Wear-gap handling (smaller, near-clear)
- **Mask** (treat non-wear as missing, drop from physiological analyses): honest, loses days.
- **Impute** physiology: keeps days, but invents the very signal you are testing.
- **Recommended:** mask, with a sensitivity check that wear-gaps aren't themselves correlated with crashes (a crash could *cause* non-wear, which would bias A). This one is close to clear-cut; imputation of overnight HRV/RHR is not defensible here.

---

## 7. Design — phases

### Phase 0 — Alignment
- Build a **daily grid** (gevoelscore and load are daily; PEM is day-scale).
- Aggregate Garmin to daily **but keep overnight features separate** (sleeping RHR, overnight HRV, respiration) — the least activity-confounded signals.
- **Physiologically correct ordering for PEM:** align exertion on day *t* to the *following* night's sleep/HRV (night t→t+1) and to symptoms on t+1, t+2.
- Flag wear-gap days (handling is a fork — mask vs impute, see §6.7; default mask).

### Phase 1 — Define the label cleanly (pre-registered, before looking at Garmin)
- Operationalize crash/dip from **gevoelscore + symptom notes only**. E.g. crash = drop ≥ X below personal rolling baseline, sustained ≥ Y days. Fix X, Y in advance.
- **Keep Garmin out of the definition** so it can later serve as an *independent* corroborator rather than a circular one.
- **Label source is a genuine fork — full options and recommendation in §6.1.** In short: the cleanest fix for the shared-source confound (§4.3) puts Garmin *into* the label, but that spends Garmin's independence as a corroborator for A. You can't have both, so A and B may run on *different* labels. Decide and record per §6.1 before proceeding.
- Record **onset day, trough day, duration separately** — for the lag (C), *onset* is the anchor.

### Phase 2 — Detrend / establish the moving baseline (must precede corroboration)
- The trajectory is **non-stationary** (threat #4): a recovery arc plus regime shifts (healthy / acute / early-LC / later-LC). Decompose every series into slow trend + daily fluctuation. **Residualize vs trend-as-covariate is a fork — see §6.3** (default: residualize as primary, covariate as sensitivity).
- **This must come before the anomaly score below.** An anomaly score computed against a *fixed* whole-series baseline on non-stationary data will flag the entire early-severe period as one long anomaly and detect almost nothing in the recovered late period. The baseline must be **rolling / adaptive** (e.g. trailing personal window, or residuals from the fitted trend), so "anomalous" means *departure from the local recent state*, not from a global mean.
- Skipping this also makes everything correlate with everything through the shared recovery curve.

### Phase 3 — Corroboration (Goal A)
- On the **detrended series with a rolling baseline** (Phase 2), compute a **multivariate Garmin anomaly score** from overnight HRV, sleeping RHR, respiration, and Body Battery — i.e. local departures, not global ones. **Baseline window length is a timescale fork — see §6.5** (run 2–3 lengths, report what's robust across them).
- Measure agreement (Cohen's κ, temporal overlap) between gevoelscore-crashes, notes-crashes, and Garmin-anomalies. This **empirically tests whether a "Garmin fingerprint" exists** rather than assuming it. Pre-specify what counts as "exists" (e.g. a minimum κ / overlap threshold) before looking.
- **Output:** one timeline, each event tagged with corroboration level (1 / 2 / 3 sources).

### Phase 4 — Exertion → crash and lead-lag (B, C)
- **Prewhitened cross-correlation** between exertion and symptoms (the correct way to read lead-lag without autocorrelation artifacts), plus a *small* distributed-lag regression (symptoms ~ exertion at lags 0–3, controlling for lagged gevoelscore and the trend) — kept within the parameter budget of §5.
- **Event-anchored averaging (primary method for C):** align all crash *onsets* at day 0; plot mean exertion/Garmin trajectory over days −5 → 0; **overlay the matched comparison — high-exertion days that did *not* lead to a crash.** That contrast is where the real signal lives; it is robust, assumption-light, and visually inspectable. **For the confidence band, do not use a naive i.i.d. bootstrap** — the trajectories are autocorrelated, so i.i.d. resampling produces bands that are far too narrow (the same overconfidence flagged for p-values in threat #3, reintroduced through the back door). Use a **block bootstrap** (resample contiguous day-blocks to preserve within-event autocorrelation) or a **circular-shift permutation** of the event anchors to build the null band.
- Use objective Garmin activity as the second, less-circular exposure alongside hand-coded load. Note that cognitive/emotional load have no Garmin equivalent — that is exactly where the notes earn their keep, and exactly where §4 caution applies hardest.

### Phase 5 — Don't fool yourself
- **Pre-specify** hypotheses and crash definition before analysis.
- **Hold-out — read it carefully, it is ambiguous.** Reserving the later timeline as a test set is worth doing, but a failure to predict late-period crashes from an early-period pattern has **two indistinguishable causes: overfitting *or* genuine non-stationarity** (threat #4 — the exertion–crash relationship in month 2 need not hold in month 14). The hold-out alone cannot separate them, so do **not** report hold-out failure as a clean overfitting verdict. Two better options: (a) **within-regime cross-validation** — split inside a single regime so the train/test distributions match, accepting that it tests generalization *within* a period and not across the recovery arc; or (b) treat success and failure asymmetrically — late-period success is strong evidence the pattern is real *and* stable, while failure is logged as "either overfit or regime-dependent, undetermined" and followed up by fitting each regime separately to see whether the *form* of the relationship is stable even if its strength is not.
- **Negative control:** shuffle the lag, or test a relationship that should not exist, to calibrate how easily noise looks like signal.
- **Report effect sizes with uncertainty over p-values** throughout.

---

## 8. Confirmatory framing for C (the PEM lag)

Do **not** freely estimate the lag. Pre-register the PEM-literature expectation — malaise onset typically ~12–48h post-exertion — as: *"malaise onset concentrates at lag 1–2 days."* Test that specific window against negative-control lags. Confirmatory beats exploratory here *because* power is limited: it spends the few events on one honest question instead of scattering them across a search. Event-anchored averaging (§7) is the primary vehicle; the regression is supporting cast.

---

## 9. Threat summary (quick reference)

1. **Leakage in load scores** — gate §4.1.
2. **Reverse causation / "good day → did more"** — feeling good raises gevoelscore *and* drives exertion *and* moves Garmin, so "high exertion precedes crash" can be a prior-good-state + regression-to-mean artifact. Conditioning on prior state is itself a fork (under- vs over-control) — **report bounds, see §6.2.**
3. **Autocorrelation** — naive correlations/p-values are wildly overconfident; compute cross-correlations on **prewhitened** series.
4. **Non-stationarity** — healthy / acute / early-LC / later-LC are different regimes; do not pool the whole timeline as one process.
5. **N=1 power** — §5; the event count is the ceiling.

---

## 10. Open questions that change the architecture

These should be answered against the real data before building:

1. **Total span and rough day count.** "Healthy → infection → aftermath" could be ~8 months or ~3 years. Decides how many regimes to split into and whether within-regime cross-validation (§7 Phase 5) leaves enough events inside each regime to be meaningful.
2. **Are crashes roughly evenly spread, or front-loaded in the severe early phase?** Decides whether C is a general claim or a within-period one (the §5 clustering caveat), and whether any cross-validation has enough events per regime to run at all.
3. **Does hand-coded physical load actually track same-day Garmin activity?** (§4.2 sanity check — also the first quick read on leakage.)

---

## 11. Suggested build order

1. Phase 0 alignment + wear-gap flags.
2. Phase 1 label (pre-registered) → Phase 2 detrend / rolling baseline → Goal A timeline via Phase 3 corroboration. *Ship this first; it stands alone.*
3. Resolve §10 questions on real data.
4. **Make the §6 tradeoff calls explicitly and record them** — especially 6.1 (label source per goal) and 6.6 (which load channels) — before any B/C modeling, since they determine what the models even are.
5. Run the three gates (§4) on a subset *before* investing in B/C modeling.
6. Phase 4 event-anchored averaging (B, then confirmatory C per §8), on the detrended series, reporting the §6.2 bounds rather than a single conditioned estimate.
7. Phase 5 within-regime cross-validation + negative control on everything in B/C (not a naive late-period hold-out).
8. Write up — including D as a legitimate outcome if the gates or validation don't hold, and stating which branch of each §6 fork was taken.

---

## 12. Checklist — questions to test or check against the real data

Concrete, data-answerable questions. Each is phrased so the answer either clears an assumption the strategy currently hedges on, or exposes a problem early. A **red flag** note marks answers that should stop or redirect the analysis. Run group A first — several later questions are moot until the data structure is known.

### A. Data inventory & structure (preconditions)
1. What is the exact date range, total day count, and rough boundaries of each regime (healthy / acute / early-LC / later-LC)?
2. What fraction of days have a gevoelscore? Where are the gaps, and do they cluster?
3. **What fraction of days have a same-day (contemporaneous) note vs a retrospective-only score?** Add this as a per-day flag.
4. **Is same-day-note density even across regimes, or front-loaded early?** *Red flag:* if contemporaneous notes are dense early and sparse late, your cleanest exposure data is confined to one regime, which interacts with everything in §5 and Phase 5.
5. What is Garmin coverage per metric (% of days with overnight HRV, sleeping RHR, respiration, Body Battery)? How are wear-gaps distributed?
6. **Are wear-gaps correlated with crashes?** *Red flag:* if crashes cause non-wear, missing Garmin data is informative-missing and biases the Goal A timeline.
7. How many distinct crash events exist under the candidate definition, and how are they distributed across regimes? *Red flag:* heavy clustering in one regime → effective N below raw count (§5), C becomes within-period only.

### B. Label definition & corroboration (Goal A)
8. How sensitive are crash count and timing to the threshold X and duration Y? Sweep both; if the timeline reshapes wildly with small changes, the definition is fragile and must be pre-registered tightly.
9. What is the agreement (Cohen's κ, temporal overlap) between gevoelscore-crashes, notes-crashes, and Garmin-anomalies? **This is the empirical test of whether a "Garmin fingerprint" exists at all.** *Red flag:* near-chance agreement → the fingerprint claim fails; corroboration drops to 2 subjective sources.
10. Does the multivariate Garmin anomaly score separate crash days from matched non-crash days better than chance?
11. Does the fingerprint (if present) hold across regimes, or only in the severe early period?

### C. Contamination gates (decide whether B/C are honest)
12. **§4.1 blind re-code:** on a held-out subset re-scored from same-day note text alone (dates/order stripped), what is the agreement with the original scores? Does the load→crash association survive blinding, and by how much does it shrink?
13. **§4.2 objective parallel:** does hand-coded physical load correlate with same-day Garmin activity (steps, intensity minutes, training load)? *Red flag:* weak correlation → the score isn't tracking exertion.
14. Does physical load predict crashes on days where Garmin activity is *unremarkable*? *Red flag:* yes → the score is capturing retrospective "that was too much," i.e. the leak made visible.
15. **§4.3 shared-source:** does the load→symptom association change when the crash label is rebuilt notes-free (gevoelscore-only or gevoelscore + Garmin) vs notes-based? A large drop quantifies the shared-method inflation.
16. **Contemporaneity split:** does the exertion→crash relationship hold on same-day-note days alone (the cleanest subset)? Holding on this subset is the strongest available evidence and largely sidesteps the hindsight critique.

### D. Confounds & causal direction
17. Does prior-day gevoelscore predict same-day exertion? (Quantifies the "good day → did more" confound, threat #2.)
18. Are crashes systematically preceded by above-baseline *good* days? (Regression-to-mean / boom-bust check.)
19. Do context events (holidays, weekends away, job loss) temporally coincide with crashes more than chance?
20. Do interventions (coaching periods, medication starts) align with measurable shifts in crash frequency or baseline — independent of pacing? *Red flag:* an intervention coinciding with a regime boundary will confound any "pacing improved" reading.
21. How conditioning on prior state changes the exertion coefficient — does it shrink toward zero (mediator / over-control) or stay stable (genuine confound removed)? (Decides the §6.2 bounds.)

### E. Autocorrelation & stationarity
22. What is the autocorrelation structure (ACF) of gevoelscore, HRV, RHR, and load? (Sets how badly naive CIs are inflated and how much prewhitening matters.)
23. How much of each series' variance is explained by the slow recovery trend? (Decides whether §6.3 residualize-vs-covariate actually matters here.)
24. Does the exertion→crash relationship differ in *form* (not just strength) across regimes when fit separately? *Red flag:* opposite signs across regimes → no stable relationship; pooling is invalid.

### F. The PEM lag (Goal C)
25. Relative to high-exertion days, where does malaise/crash onset cluster — and is the 1–2 day pre-specified window where the mass actually sits, vs control lags?
26. Does the lag pattern replicate across within-regime CV folds, or only appear in one fold?
27. **Negative control:** does a shuffled-lag or a deliberately implausible relationship produce comparable "signal"? (Calibrates how easily noise mimics the finding.) *Red flag:* control shows similar signal → the lag result is not distinguishable from noise.
28. Do high-exertion days that did *not* lead to a crash differ systematically from those that did — in the exertion itself, prior state, or context? (This contrast is the core of the event-anchored method.)

### G. Power & feasibility reality checks
29. Given the events-per-regime count, what is the roughly minimum detectable effect size? (Is C even powered within a single regime?)
30. Is there enough data per regime to run within-regime cross-validation at all, or does honest validation collapse for lack of events? *Red flag:* if not, C cannot be validated and should be reported as exploratory-only.
