# Resilience as a latent slow-state: construct definition, dynamics model, confound structure, and licensed pre-registrations

*Producer-mode methodology MD per [CONVENTIONS §1.1](../CONVENTIONS.md#11-producer-mode-claude-writes--edits--runs). Drafted 2026-07-16 as r1. **STATUS: DRAFT r1, awaiting fresh-session `/research-methodology-review`** against the [CONVENTIONS §2.2](../CONVENTIONS.md#22-methodology-md-before-locking-a-major-choice) four-input bar. NOT locked; no downstream pre-registration may cite this MD as a locked anchor until r1 locks.*

---

## Authorship

**Drafted 2026-07-16** by Claude (Fable 5) in producer-mode under user authorisation per [CONVENTIONS §1.1](../CONVENTIONS.md#11-producer-mode-claude-writes--edits--runs). Authorising user: Willem.

**Drafting trigger**: a design conversation (2026-07-16) that (a) mapped the clinician-interpretive "Laure" heart-rate-reading framework against the existing corpus and found it split across two research lines — a zoomed-out crash line (predict / understand / recover-from crashes) and a zoomed-in day-to-day pacing line (symptom + fatigue management inside the energy envelope) — and (b) surfaced the **bridging assumption** the user wants tested: *pacing well and staying inside the envelope builds resilience, which protects against crashing; a crash depletes resilience, which then takes weeks to rebuild.* That assumption reifies a latent variable that neither research line has defined. This MD nails the construct down **before** any test spec commits, per the user's explicit sequencing ("formalise the construct first").

**Sequencing note**: this MD is the definitional anchor for a resilience-lens re-read of HA-P7 (the "recent-crash-density predicts crash" NOT-SUPPORTED verdict). The *interpretive* re-read is now folded into §6.2 (2026-07-16, reviewer-mode overlay; the HA-P7 verdict stays locked). A *formal* HA-P7-v2 re-test remains downstream and out of scope here (§1.2).

**Genre**: this is a **construct-definition + methodology-framing MD**, closer in kind to [`lc_recovery_phase_axis.md`](lc_recovery_phase_axis.md) and [`research_line_limitations.md`](research_line_limitations.md) than to the operand-definition MDs ([`bout_level_recovery_dynamics.md`](bout_level_recovery_dynamics.md), [`post_heavy_day_compensatory_rest.md`](post_heavy_day_compensatory_rest.md)). It defines a latent construct, its observable proxies, its confound structure, and the pre-registrations it licenses. It does **not** lock an operand or a test.

**Register attribution**: this construct is registered as subject-authored [**Beyond P11**](../personal_hypotheses.md) per [`register_provenance_and_numbering.md §2.1`](register_provenance_and_numbering.md). It *extends* the Wiggers pacing handleiding's **descriptive** capacity/pacing observations (§7.2), but the causal build-up claim (R1) and the latent-reserve formalisation are the subject's — the guide explicitly **declines** the causal claim (handleiding p.63) and its "resilience" is a daily Garmin widget score, not a slow reserve. Per §2.1 a distinct theoretical extension lives in Beyond with a reciprocal Guide pointer (§2.2) to the antecedents; that reciprocal pointer is **pending**.

---

## 1. Purpose and scope

### 1.1 What this MD is

A definition of **resilience** as a latent, slowly-varying state of the participant's system, together with:

1. the **asymmetric-dynamics model** that gives the construct its testable shape (§2.2);
2. the **observable proxies** that stand in for the unobserved state, and the naming discipline that keeps them from being mistaken for it (§3);
3. the **confound structure**, worked as a temporal-shape analysis that isolates exactly which factors the era structure can and cannot separate (§4);
4. the **identification strategy and its ceiling** — the honest reach of any resilience claim at n=1 (§5);
5. the **four licensed pre-registration directions** (R1–R4) that decompose the construct, each mapped to what the corpus already found and what stays untested (§6).

The purpose is to give R1–R4 (and the HA-P7 resilience re-read) a single citable definition of "resilience," so that no downstream artefact reifies the construct from memory, inconsistently, or with a stronger causal claim than n=1 permits.

### 1.2 What this MD is NOT

- **NOT a pre-registration.** No falsifier, discrimination threshold, null model, or Stage H test is locked here. The R1–R4 direction pre-commits (§6) are *reading axes*, not test specs. Each becomes a pre-registration only via its own methodology MD + `hypothesis.md`, drafted after this construct locks.
- **NOT a latent-state model fit.** This MD deliberately does not commit to a state-space / hidden-Markov / Kalman operationalisation of the resilience variable. Fitting an explicit latent state at n=1 over a time-collinear treatment would manufacture a state indistinguishable from the disease-recovery arc (§4.3, §5.3). The construct is defined at the level of its *shape* and its *proxies*, not a fitted trajectory.
- **NOT a claim that resilience is measured.** Resilience is unobserved (§2.3). Every operational quantity in §3 is a *proxy* and is named as one (§3.4).
- **NOT a re-open of any locked verdict.** HA-P7, `post-crash-exertion-relapse`, HA-P6, and the Q24 arc keep their locked verdicts. This MD reads them as evidence under a new construct; cross-checks are descriptive, never automatic re-locks, per [methodology/README.md](README.md) discipline note.
- **NOT a resolution of the identification problem.** §5 states plainly that the load-bearing confound (pacing-maturity vs spontaneous recovery) is not identifiable at n=1. The MD's job is to make that boundary explicit and to route the available evidence toward the parts that *are* reachable, not to pretend the boundary away.

### 1.3 Why a construct MD, and why now

The two research lines have each accumulated evidence that *touches* resilience without naming it: the crash line has post-crash recovery-shape work ([`HA-P6`](../analyses/hypotheses/HA-P6/result.md)), a recent-crash-density test ([`HA-P7`](../analyses/hypotheses/HA-P7/result.md)), and a post-crash danger-window test ([`post-crash-exertion-relapse`](../analyses/hypotheses/post-crash-exertion-relapse/result.md)); the pacing line has bout-level recovery morphology ([`bout_level_recovery_dynamics.md`](bout_level_recovery_dynamics.md)) and reactive-vs-proactive rest ([`Q24-mdbeta-wave2c`](../analyses/descriptive/Q24-mdbeta-wave2c-reactive-vs-proactive-rest/)). None of these is framed as a test of a *shared latent reserve*. Without a construct definition, a resilience claim would be assembled ad hoc from whichever of these happened to be top-of-mind — the exact drift [`research_line_limitations.md §2`](research_line_limitations.md) centralises against. Defining the construct first is the descriptive-before-inference discipline ([CONVENTIONS §2.1](../CONVENTIONS.md#21-descriptive-before-inference)) applied at the construct layer.

---

## 2. The construct

### 2.1 Definition

**Resilience** (working name; synonyms considered: reserve, buffer, envelope capacity — §7.3) is a **latent, slowly-varying scalar state** `R(t)` representing the participant's current capacity to absorb exertion without triggering a crash. It is not a symptom, not a felt-state, and not a wearable channel. It is the hypothesised hidden quantity whose level sets, at any moment, how much load the system can take before it tips.

The construct is defined by four commitments:

1. **Latent** — `R(t)` is unobserved. It is inferred only through proxies (§3), never read directly off any instrument.
2. **Slowly-varying** — `R(t)` changes on a multi-day-to-multi-week timescale, not within a day. This is what distinguishes it from the fast within-day autonomic excursions (arches, U-dips) that the bout-level work measures. Those excursions are *inputs* to `R(t)`, not `R(t)` itself.
3. **Protective when high** — higher `R(t)` lowers the instantaneous probability that a given exertion produces a crash. This is the only claim that makes the construct worth testing; it is also the one §5 shows is hardest to identify.
4. **Asymmetric in its dynamics** — `R(t)` builds slowly and depletes fast (§2.2).

### 2.2 The asymmetric-dynamics model

The construct's testable shape is a **leaky integrator with asymmetric response**: `R(t)` accumulates gradually under sustained in-envelope pacing, drops sharply at a crash, and re-accumulates slowly afterwards. Schematically (as a *shape commitment*, not a fitted equation):

- **Build**: during stretches of good pacing-quality (§3.1), `dR/dt > 0`, small and slow — resilience is earned gradually, over weeks.
- **Drop**: at a crash event (§3.3), `R` falls by a large step — the fast, discontinuous depletion.
- **Rebuild**: after a crash, `R` climbs back on the same slow build dynamics, so full recovery of the reserve lags the recovery of felt-state and takes weeks.

This asymmetry is the load-bearing structural claim. It predicts a specific dissociation: **felt-state can recover before `R` does**, leaving a window in which the participant feels ready but the reserve is still low. That dissociation is the substance of the R2 vulnerability-window direction (§6.2) and of the existing `post-crash-exertion-relapse` design's "felt-recovered but autonomic-not-settled" framing.

The model is committed only at the level of these three signs and the felt-state-leads-reserve dissociation. It does **not** commit to a functional form, a leak rate, a build/drop ratio, or an observability model. Those are downstream pre-registration choices, and §5.3 explains why fitting them at n=1 would over-reach.

### 2.3 Why latent, and what follows

`R(t)` is defined as unobserved because no instrument in the corpus measures reserve capacity. What the instruments measure are (a) *inputs* to the reserve (pacing behaviour, exertion, within-day recovery morphology) and (b) *readouts* correlated with the reserve (felt-state, overnight autonomic load). Treating any single channel *as* resilience would collapse the construct into that channel and lose the whole point — that resilience is the thing the channels jointly, imperfectly, point at.

Two consequences follow and bind the rest of this MD:

- Every operational quantity is a **proxy** (§3), carrying its own measurement caveat.
- The construct can only ever be **triangulated**, never identified (§5.3). A latent protective reserve at n=1 over a time-collinear treatment is not point-identified; the honest target is a coherent, confounder-bounded cumulative case.

---

## 3. Operationalisation of the observable proxies

Resilience decomposes, operationally, into a *cause* side (pacing-quality, the input that builds the reserve), a *state-readout* side (the correlates of the current reserve level), and a *depletion* event (the crash). Each is defined here as a proxy family; specific column choices are deferred to the R1–R4 pre-regs.

### 3.1 Pacing-quality proxy (the cause side)

"Pacing well / staying in the envelope / anticipating body signals" is operationalised as **envelope-consistency**, deliberately **not** as activity volume (§7.3 tradeoff; the GET-vs-pacing distinction in §7.2). Candidate daily proxies, all already defined or characterised in the corpus:

| Proxy family | Existing operand / source | What it captures |
|---|---|---|
| Within-day recovery morphology | `bout_n_fast_recovery_day`, `did_not_return_flag`, `recovery_half_life`, `tail_length` ([`bout_level_recovery_dynamics.md`](bout_level_recovery_dynamics.md)) | Laure's "small waves" (fast return) vs "arch / high wall" (stuck elevated) — good pacing produces more small waves, fewer stuck bouts |
| Proactive vs reactive rest | strategic (`gevoelscore ≥ 5`) vs crisis (`≤ 3`) rest on `rest_day_p25` ([`Q24-mdbeta-wave2c`](../analyses/descriptive/Q24-mdbeta-wave2c-reactive-vs-proactive-rest/); [[project_rest_day_operand_semantics]]) | Anticipatory pacing (rest before symptoms) vs forced pacing (rest because already bad) |
| Exertion staying inside the lagged envelope | `exertion_class_lagged_lcera` relative to personal baseline ([CONVENTIONS §3.2](../CONVENTIONS.md#32-lagged-baseline-for-sustained-push-hypotheses)) | Load held below the envelope ceiling vs breaching it |

**Pacing-quality is a composite construct, not a single column.** A specific weighting or single-proxy choice is an R1 pre-registration decision under [CONVENTIONS §2.2](../CONVENTIONS.md#22-methodology-md-before-locking-a-major-choice), not locked here. The [CONVENTIONS §3.1](../CONVENTIONS.md#31-personal-baseline-not-absolute-thresholds) personal-baseline rule binds any such proxy: pacing-quality is measured against the participant's own rolling baseline, never absolute cutoffs.

### 3.2 Resilience-readout proxy (the state side)

Candidate readouts of the current reserve level — channels expected to track `R(t)` because a depleted reserve should show as autonomic dysregulation and lower felt-state:

| Readout family | Existing operand / verdict | Standing as a readout |
|---|---|---|
| Overnight autonomic stability | `stress_stdev_sleep` — [`HA07d`](../analyses/hypotheses/HA07d-sleep-stress-variability/result.md) is the project's only both-eras-SUPPORTED test (variability of sleep-stress discriminates crashes) | Strongest candidate: Laure's "wobbly night line = dysregulation" maps here; a low reserve may show as a less-stable overnight line |
| Felt-state | `gevoelscore` (self-report; [L6](research_line_limitations.md#l6-self-reporting)) | The subject's own readout of the reserve; load-bearing but self-reported (§8) |
| Overnight recharge / floor | `bb_overnight_gain`, `bb_lowest` ([`HA10`](../analyses/hypotheses/HA10-bb-overnight-recharge/), operationalisation-support folders) | Recovery-capacity readouts; era-directional (caveat §4) |

**Caveat carried from the corpus**: resting HR is a *weak* readout in this body — episode-level Cohen's d ≈ 0.07, the weakest channel characterised ([`operationalisation_support/resting_hr/`](../analyses/descriptive/operationalisation_support/resting_hr/)), and both RHR precursor tests ([`H01`](../analyses/hypotheses/H01-rhr-drift/), [`HA06`](../analyses/hypotheses/HA06-morning-rhr-delta/)) were refuted. RHR is retained as a *readout candidate under caveat*, not a primary resilience proxy, because this participant's day-scale RHR is unusually stable (MAD ≈ 2 bpm) and its multi-year drift is confounder-dominated ([`recovery_phase_confounder_bound/`](../analyses/descriptive/recovery_phase_confounder_bound/): weight +3.4, aging +1.7, citalopram −1.0, illness residual flat).

### 3.3 Depletion event (the discontinuity)

The fast-drop in §2.2 is operationalised as a **`crash_v2` tier-1 episode** (29 episodes / 101 crash-days on the corpus; tier-2 = 79 isolated dips) per [`crash_v2-definition/`](../analyses/hypotheses/crash_v2-definition/). Dips are the graded, lower-amplitude depletions. Whether a dip depletes `R` less than a crash (a graded-drop reading) is an R2/R3 question, not locked here.

### 3.4 Naming discipline (binding)

Mirroring the "phase-stratified, never learned-pacing" discipline of [`post_heavy_day_pacing_learning.md §6.1`](post_heavy_day_pacing_learning.md):

- Any operational quantity in §3.1–§3.2 is named a **"pacing-quality proxy"** or **"resilience-readout proxy,"** never "resilience." Resilience is the latent construct; the proxies are its imperfect shadows.
- A finding on a proxy is reported as a finding *on that proxy*, with the resilience interpretation deferred to the synthesis layer (Stage S1 at the earliest) and always carrying the §5 ceiling.
- No artefact may write "resilience rose / fell / was measured." Permitted: "the resilience-readout proxy `X` moved," "consistent with the resilience construct," "as the resilience model would predict."

---

## 4. The confound structure (temporal-shape analysis)

This section is the methodological core. It elaborates [`research_line_limitations.md L2`](research_line_limitations.md#l2-era-confounds) (era confounds) for the specific case of a slow latent state over a time-collinear treatment, and it states precisely which factors the era structure separates and which it cannot.

### 4.1 The factors and their temporal signatures

The participant's LC-era timeline carries several slowly-changing factors, each with a distinct **temporal signature**. The era axis is the project's [`recovery_phase`](lc_recovery_phase_axis.md) schema:

| Factor | Temporal signature | Corpus anchor |
|---|---|---|
| Citalopram | **Sharp step** at 2024-04-09 | Modelled as a dose-response with known β on 3 channels ([`citalopram_phase_stratification.md`](citalopram_phase_stratification.md)) |
| Reintegration emotional burden | **Bounded episode** (PwC reintegration, ~18 months, with a start and an end) | PwC dossier + reintegration log; `pacing_pre_citalopram_learning` → `pacing_habit_established` era |
| Weight / aging | **Slow monotonic drift** | Decomposed in [`longrun_rhr_trend/`](../analyses/longrun_rhr_trend/) driver ledger |
| Pacing maturity | **Gradual monotonic rise** | The learned-pacing arc ([`post_heavy_day_pacing_learning.md`](post_heavy_day_pacing_learning.md)) |
| Tactical-Garmin-pacing improvement | **Gradual monotonic rise** | [[project_garmin_research_bias_boundary]] — real-time Garmin use across the whole LC-era pre-2026 |
| Spontaneous disease recovery | **Gradual monotonic rise** | The multi-year recovery arc ([`trajectory/recovery_arc/`](../analyses/descriptive/trajectory/recovery_arc/)) |

The four LC recovery phases (`lc_pre_ergo` 2022-04-04→2022-09-21, n≈171 days; `pacing_pre_citalopram_learning` →2022-11-16, n≈56; `pacing_habit_established` →2024-04-08, n≈509; `citalopram_modulated` →2026-06-05, n≈788) are the era buckets; day-counts per [`post_heavy_day_pacing_learning.md §3.1`](post_heavy_day_pacing_learning.md).

### 4.2 Separability by temporal shape

The identification principle: **two factors that share a temporal shape over the same window cannot be separated by that window; factors with distinct shapes have partial leverage.**

- **Separable (distinct shapes)**: citalopram (sharp step) and the reintegration burden (bounded episode) are the tractable ones, precisely because they do not look like slow monotonic drift. A change that co-locates with the 2024-04-09 step, or that switches at the reintegration episode's boundaries, is partially attributable to that factor via its timing. The corpus already exploits this — the citalopram step is the strongest era boundary in [`era_boundaries/`](../analyses/descriptive/trajectory/era_boundaries/), and the citalopram effect is modelled as a dose-response, not an era-average.
- **Confounder-dominated era levels**: the corpus has already *demonstrated* that cross-era level differences are dominated by the slow drifts, not by the construct of interest. [`recovery_phase_confounder_bound/`](../analyses/descriptive/recovery_phase_confounder_bound/) decomposed the per-phase RHR rise into weight (+3.4) + aging (+1.7) − citalopram (−1.0) with the illness residual flat, verdict "slow-confounder artefact, not illness signal." Any resilience read that leans on cross-era *levels* inherits this problem.

### 4.3 The unbreakable pair

**Pacing maturity, tactical-Garmin-pacing improvement, and spontaneous disease recovery all share the same temporal signature — a gradual monotonic rise over the same years.** The era structure cannot separate factors that move together, so this cluster is the one it genuinely cannot break. And it is exactly the cluster the resilience hypothesis most needs to tell apart: R1 (build-up is protective) requires attributing improvement to pacing-built reserve rather than to the disease simply getting better on its own.

This is the honest statement of the limit: **not "nothing can be disentangled," but "one specific monotone-rising cluster cannot be, and it is the load-bearing one."** No design at this MD's level identifies pacing-built resilience from spontaneous recovery at n=1 under this shared shape. §5 gives the two partial escapes that do not depend on breaking this pair.

**External corroboration:** the Wiggers pacing handleiding itself flags exactly this confound — its progressing-patient case declines to attribute improvement to pacing vs natural recovery ("I don't know if pacing very well is the reason I'm improving or that I am just one of the lucky people that progresses in the first few years", p.63). The identification limit is acknowledged by the practitioner source, not only by this analysis, which is why R1 is framed as a triangulation target (§5.3), not a claim the corpus can settle.

### 4.4 The pre-ergo era as uncontrolled-baseline anchor

One asset the era structure *does* provide: the **`lc_pre_ergo` phase is the window where the active-controller confound ([L4](research_line_limitations.md#l4-analyst-is-subject); §5.1) is closest to off** — the participant had not yet developed a pacing practice, so exertion→outcome relationships there are least masked by anticipatory self-regulation. `lc_pre_ergo` is therefore the corpus's closest thing to an **uncontrolled dose-response baseline**, against which the controlled later eras can be read. Caveat: n≈171 days / ~19 heavy-episode-ends is small ([`post_heavy_day_pacing_learning.md §6.4`](post_heavy_day_pacing_learning.md)), so this anchor supports descriptive-with-CI reads only, and it is still inside the disease-arc drift.

---

## 5. Identification strategy and its ceiling

### 5.1 The active-controller problem (why associations understate)

The participant paces *in response* to body signals, so an observational pacing→crash association is attenuated by the very self-regulation it is trying to measure: exertion is *lower* on crash-lead-up days because the participant already pulled back ([`exertion_class` operationalisation-support](../analyses/descriptive/operationalisation_support/exertion_class/); [`crash_leadup_curves`](../analyses/descriptive/crash_leadup_curves/) "the watch reads the crash, not its approach"), and [`HA-C4b`](../analyses/hypotheses/HA-C4b/result.md) explicitly reads its own null as "the trigger may be protective rather than predictive because the participant acts on it." This is a manifestation of [L4 (analyst-is-subject)](research_line_limitations.md#l4-analyst-is-subject): the subject is an active controller of the system under study. Any resilience test must treat the controller as part of the system, or read protection as null.

### 5.2 Two partial escapes

Neither escape breaks the §4.3 unbreakable pair; both extract reachable signal without pretending to.

1. **Drop the horizon and the slow confounders vanish.** Weight, aging, citalopram, tactical-Garmin drift, and the disease arc do not move within a day. So any **within-day or next-day** relationship — arch today → worse tonight, small-waves-week → calmer-next-week — is *structurally immune* to the §4 era-confounding, because a day is below the timescale on which those factors change. This is the deep reason the zoomed-in pacing line is the privileged surface for anything causal: it operates below the confounder timescale. The bout-level machinery ([`bout_level_recovery_dynamics.md`](bout_level_recovery_dynamics.md)) and the within-day U-dip ([`HA11`](../analyses/hypotheses/HA11-stress-udip/)) already live here; the resilience construct's short-horizon predictions (R3, part of R1) inherit their confound-immunity.
2. **Lapses dissociate pacing from the arc.** Spontaneous recovery predicts monotone improvement, so late in the timeline the participant should be protected. An episode where **pacing lapsed late in recovery and a crash followed anyway** is a dissociation: the arc says "safe," the pacing-quality proxy says "exposed," and the crash sides with pacing. A handful of such cases carries more identifying weight than any era-level average, because they are the instances where the two collinear factors point in opposite directions. Defining "pacing lapse late in recovery" operationally is a downstream design task (candidate for the R1 pre-reg or a dedicated lapse-dissociation MD); it is named here as the second escape, not locked.

### 5.3 Triangulation, not identification — the ceiling

Even with both escapes, n=1 with a time-collinear treatment lands at **triangulation, not point-identification**. The honest target for the resilience construct is a **cumulative, confounder-bounded case**, assembled from mutually-reinforcing lines rather than a single decisive test — the N-of-1 adaptation of the Bradford-Hill triangulation logic:

- **dose-response within era** (below the confounder timescale, §5.2 escape 1);
- **coherence across independent readout channels** (autonomic + felt-state moving together as the construct predicts);
- **specificity** (pacing-quality predicts protection better than time-alone does);
- **reversibility** (lapses cost protection, §5.2 escape 2);
- **temporal order** (the felt-state-leads-reserve dissociation of §2.2).

The permitted terminal claim for resilience is therefore **"consistent-with, confounder-bounded,"** never "proven" — the same genre the whole research line already occupies ([CONVENTIONS §4.2](../CONVENTIONS.md#42-caveats-yes-a-priori-claims-no); [`research_line_limitations.md`](research_line_limitations.md)). Resilience is not exempt, and does not need to be exempt to be actionable for the subject.

---

## 6. Licensed pre-registration directions

The construct decomposes into four directions. Each is a *reading axis with a pre-committed direction*, not a test spec. For each: the claim, the corpus evidence to date, the standing, and what a future pre-reg must add. Opposite-direction findings are sign-inversion findings in their own right ([CONVENTIONS §4.2](../CONVENTIONS.md#42-caveats-yes-a-priori-claims-no)), never silently inverted.

### 6.1 R1 — build-up is protective (the core, and the gap)

**Claim**: a sustained stretch of in-envelope pacing lowers crash probability in the *following* weeks, over and above what the current day's state predicts (cumulative pacing-quality → forward crash-hazard reduction).

**Standing: essentially untested.** The corpus tests single-day and 7–14d exertion/rest windows ([`push_burden_7d`](../analyses/descriptive/operationalisation_support/push_burden_7d/), the HA0x precursor family) but never *cumulative pacing-quality* as a forward-looking buffer. This is the direct operationalisation of the user's assumption and the largest open gap.

**A future R1 pre-reg must add**: a cumulative pacing-quality proxy (§3.1), a forward crash-hazard outcome with an honest lag, trajectory-detrend against the disease arc ([CONVENTIONS §3.7](../CONVENTIONS.md#37-trajectory-detrend-sensitivity-for-raw-pre-vs-post-comparisons)) so the §4.3 pair is bounded not assumed-away, and the §5.2 lapse-dissociation arm as the identifying complement.

### 6.2 R2 — depletion / vulnerability window

**Claim**: a crash depletes the reserve, leaving crash probability elevated for weeks (the fast-drop + slow-rebuild of §2.2).

**Standing: probed under mis-specification and underpower — not confirmed, and not closed.** A reviewer-mode re-read of [`HA-P7`](../analyses/hypotheses/HA-P7/result.md) `result.md` against this construct (2026-07-16; interpretive overlay per [CONVENTIONS §1.2](../CONVENTIONS.md#12-reviewer-mode-claude-reads--critiques--explains-does-not-edit-unless-asked), the HA-P7 NOT-SUPPORTED verdict stays locked) revises the earlier "probed twice, not confirmed" reading into five findings:

1. **HA-P7 tests a triple-mis-specified R2.** Its predictor is crash-*count density* (`crash_count_14d`), not a depletion-*state*; it enters felt-state as a *nuisance covariate* to be partialled out rather than the *mediator* the construct makes it (§3.2); and its *14-day generic window* is mostly post-recovery filler — [`HA-P6`](../analyses/hypotheses/HA-P6/result.md) shows the post-crash recovery signature concentrates at ~2.5 days across 4/7 channels, not across 14. None of the three is the R2 the construct states.

2. **The "just a recent-low-gevoelscore proxy" reading is overstated by the numbers.** HA-P7's pre-registered §4.5.4 disambiguation fires the proxy conclusion only if β₁ attenuates *and* β₂'s CI excludes 0. In the pooled cell β_crash_count attenuates to OR 0.941 but β_gevoel is −1.157 with CI **[−2.568, +0.138]**, which *includes* 0. The precondition is not met; the covariate arm is inconclusive on mechanism, not a confirmed proxy. (The STOCKTAKE compression to "reads as recent-low-gevoelscore proxy" is stronger than the CI supports; [[feedback_flag_contradictions]].)

3. **Partialling out felt-state is partialling out the mediator.** Under the construct, `gevoelscore` *is* the reserve readout (§3.2), so a crash-count signal that vanishes once `gevoelscore_lagged_mean_14d` is controlled is exactly what a crash → depleted-reserve → low-felt-state → elevated-hazard chain produces. The attenuation is *consistent with* R2, not evidence against it.

4. **The strongest apparent counter-evidence is active-controller-confounded.** [`HA-P6`](../analyses/hypotheses/HA-P6/result.md) partly settles recovery-debt: within-episode-tail YES (rate↔duration ρ = +0.285 [+0.021, +0.585] and +0.389 [+0.013, +0.709]), across-episode NO / inverse (completeness↔next-interval ρ = −0.338 [−0.493, −0.168]). R2 is the across-episode claim, so that inverse is the real challenge — but "more-complete recovery → sooner next crash" is the §5.1 active-controller signature (recover fully → feel good → do more → crash sooner), which the construct predicts will invert observational estimates. Consistent with resilience-plus-controller; not a clean refutation.

5. **The dissociation-faithful test is inconclusive, not negative.** [`post-crash-exertion-relapse`](../analyses/hypotheses/post-crash-exertion-relapse/result.md) operationalises the felt-recovered-but-reserve-low window directly (danger window = felt-recovery day … nadir+10d, exertion → relapse) and returned Cannot-resolve (primary −1.03, 95% CI [−8.58, +5.21], n=24) — probed-once at the n=24 floor, not refuted.

**The wall is power, not sign.** Both HA-P6 and HA-P7 name the ~29-episode / 27-positives sparsity ceiling explicitly. A resilience-faithful R2 is specifiable (points 1–3 give the spec) but would hit the same floor, so the binding open question before drafting it is not the design but the **power**: how many post-crash felt-recovered-but-recently-crashed days the corpus actually holds — which decides whether R2 can carry its own verdict or must ride on the R3 + R4 coherence case (§6.5).

**A future R2 pre-reg / re-read must add**: a mediation framing that treats felt-state as the mediating reserve-readout (crash → low readout → elevated hazard); a window keyed to the felt-recovered/reserve-low dissociation rather than a fixed count horizon; an active-controller model (§5.1) so the across-episode inverse is not read at face value; and a pre-flight power scope against the 27-positives ceiling.

### 6.3 R3 — rebuild takes weeks

**Claim**: after a crash, recovery of the reserve to baseline is slow (weeks), and lags felt-state recovery (§2.2 dissociation).

**Standing: descriptively supported.** [`HA-P6`](../analyses/hypotheses/HA-P6/result.md) shows a multi-day post-crash recovery signature (4/7 channels distinguishable from matched controls); the [`peri-event-recovery`](../analyses/garmin_exploration/cards/peri-event-recovery-export.md) card puts felt-state back in ~2–3 days but overnight autonomic load taking ~2 weeks to settle — the felt-leads-autonomic dissociation the model predicts. Corroborating circumstantial evidence: the corpus's autocorrelation memory-lengths (computed for block-bootstrap, [CONVENTIONS §3.5](../CONVENTIONS.md#35-spike-detecting-metrics-over-daily-averages) family) land in the multi-week range — `gevoelscore` E[L]*≈15d, RHR and the daily stress/BB channels ≈3–4 weeks — a fingerprint *consistent with* a slow latent state on the timescale the construct posits, though not proof one exists.

**A future R3 pre-reg must add**: nothing new is strictly required to *characterise* the rebuild timescale (it is descriptive); the open question R3 does **not** settle is whether the un-rebuilt reserve is *causally* what makes the participant crashable — that is R1/R2 territory.

### 6.4 R4 — anticipation / proactive pacing pays off

**Claim**: heeding body signals and resting proactively (before being forced to) yields fewer crashes than reactive pacing.

**Standing: descriptively supported, with confounding-by-indication caveat.** [`Q24-mdbeta-wave2c`](../analyses/descriptive/Q24-mdbeta-wave2c-reactive-vs-proactive-rest/) finds proactive-strategic rest associated with ~1/3 the crash rate (pooled RR ≈ 0.35) and crisis-reactive rest with ~4× (pooled RR ≈ 4.29; 2023 RR ≈ 6.70). The caveat is load-bearing: reactive rest is enriched for crashes partly *because* it is taken when already crashing (confounding-by-indication / endogeneity; [[project_rest_day_operand_semantics]]), so the contrast overstates the causal protection of proactivity. R4 is the strongest existing descriptive support for the resilience *philosophy*; its intraday-HR-curve version (small-waves→next-day-calm) is only partially instrumented.

**A future R4 pre-reg must add**: an endogeneity-aware design (e.g. conditioning on felt-state at rest-onset) that separates "proactive rest protects" from "the kind of day that permits proactive rest was already low-risk."

### 6.5 Reading discipline across R1–R4

R1–R4 are **not independent tests to be multiplicity-corrected as a family**; they are facets of one construct, each with its own confound profile. A resilience claim earns support to the degree that they *cohere* (§5.3 triangulation), not to the degree that any one clears a threshold. Divergence among them is itself informative (e.g. R3-supported + R1-untested + R2-inconclusive is exactly the pattern "the reserve exists and rebuilds slowly, but we have not shown its build-up is protective" — a coherent, honest, incomplete state).

---

## 7. Four-input reasoning ([CONVENTIONS §2.2](../CONVENTIONS.md#22-methodology-md-before-locking-a-major-choice))

The **major choice** this MD locks is: *adopt a latent slow-state definition of resilience with proxy-based operationalisation and a triangulation-ceilinged identification strategy, rather than an alternative construct framing.* The four inputs:

### 7.1 Best-practices standards

- **Latent-variable / state-space** modelling is the standard apparatus for an unobserved slowly-varying capacity, but its identifiability degrades sharply at n=1 over a collinear treatment. Best practice under that constraint is to define the construct at the level of its *shape and proxies* and to triangulate, not to fit a latent trajectory that the data cannot identify (§2.2, §5.3).
- **N-of-1 reporting standards** ([CENT / CONSORT-N-of-1](../literature/methodology/shamseer_2015_cent_consort_nof1.pdf); [STROBE](../literature/methodology/vonelm_2007_strobe_observational_checklist.pdf) §12d) require limitations stated explicitly — met by §8.
- **Triangulation** (Bradford-Hill viewpoints adapted to single-case) is the accepted route to causal *plausibility* where identification is unavailable — the §5.3 strategy.

### 7.2 Established literature

Grounding survey (2026-07-19), verified against PubMed for indexed items and web sources for books/grey literature (DOIs in the reference list below; the earlier *citation-status-deferred* markers are now resolved). **The honest picture: the construct is grounded in pieces across four literatures, but its packaging — a latent reserve with fast-deplete/slow-rebuild asymmetry that cycles within-person — is a domain-transfer synthesis with no single named home.** Cited by role; one contribution note per cluster.

- **Formal scaffolding for the packaging (nearest formal homes; domain-transfers, not illness-specific proof).** The tightest formal analogues are the **fitness-fatigue two-component model** (Banister 1975; Morton 1990) — two antagonistic exponentials with fatigue decaying faster than fitness (0 < τ₂ < τ₁), which *is* the slow-build/sharp-drop asymmetry and yields R3's felt-leads-reserve dissociation for free (the fast term clears before the slow one); **dynamical-systems resilience** (Scheffer 2018; Gijzel 2017) — resilience = recovery capacity read off time-series "critical slowing down" (rising autocorrelation/variance), which Gijzel operationalises on *daily self-rated-health series* methodologically twin to `gevoelscore`; and the **Energy Model of Allostatic Load** (Bobba-Alves 2022) — an explicit energetic reserve "buffer" depleted by load. These supply the *shape*; none asserts R1's causal build (§7.3).
- **R1 (build-up) — grounded but contested.** Jason's Energy Envelope Theory is the only pacing model claiming the envelope *enlarges* with consistent in-envelope pacing (Jason 2008; O'Connor 2019); mitohormesis and exercise oxidative-adaptation give R1 a mechanism (Ristow 2014; Radak 2008); cognitive reserve is the precedent for a *trainable* latent reserve (Stern 2009). Causality is unproven in every source — matching the guide's own hedge (§4.3).
- **R2 / R3 (deplete / rebuild) — well-grounded.** Frailty / homeostatic-reserve models give the crash mechanism directly — a depleted reserve turns a minor stressor into disproportionate decompensation with incomplete return to baseline (Fried 2001; Clegg 2013), and physical resilience is defined as the *recovery trajectory* after a stressor (Whitson 2016, 2018). The overtraining continuum supplies weeks-to-months disproportionate recovery (Meeusen 2013); allostatic "failure to shut off" supplies delayed recovery (McEwen 1998); post-crash recovery timescale is quantified in ME/CFS (Moore 2023; Keller 2024). The felt-leads-reserve dissociation (R3) is anchored in the corpus's own [`pem_recovery_trajectory_review.md`](../literature/reviews/pem_recovery_trajectory_review.md) (Germain, Radin) — cross-referenced, not re-cited.
- **R4 (anticipation) — well-grounded.** Allostasis-as-predictive-regulation is the formal basis for proactive over reactive (Sterling 2012); the acute:chronic workload ratio encodes "gradually-built chronic load protects, spikes injure" — consistency over volume (Gabbett 2016, with the methodological caveat of Impellizzeri 2020); and OT activity-pacing consensus ranks *building tolerance* above energy-conservation (Antcliff 2019; Barakou 2023), matching this construct's envelope-consistency choice (§3.1).
- **The sign-inversion tension (cited to engage it, not hide it).** Every load→capacity model above carries a healthy-population positive-adaptation sign that the PEM evidence shows *inverts* above threshold: ME/CFS patients fail to reproduce day-2 CPET performance (Snell 2013; Keller 2024), exertion *damages* muscle in long COVID (Appelman 2024), and graded exercise is now advised against (Wilshire 2018; NICE NG206 2021). This is why R1 is operationalised as envelope-*consistency*, never activity volume — borrow the asymmetric *shape*, not the healthy-athlete *sign* (§7.3).
- **What the construct is NOT (divergent framings, cited for contrast).** The dominant illness/OT metaphor is a finite *daily* budget that resets overnight (spoon theory, Miserandino 2003; energy-conservation, Mathiowetz 2001, 2005) — the wrong timescale for a multi-week reserve. Window of tolerance (Siegel 1999) is a tolerance-band on a moment-to-moment timescale; polyvagal (Porges 2011) is scientifically contested (Grossman 2023) — cite only with that caveat. Allostatic load applied to CFS (Goertzel 2006; Arroll 2013) captures the wear-side but has no build term; hormesis (Calabrese 2022) is a static inverted-U, not a temporal reserve. (The within-day-shape-over-daily-mean principle grounding §5.2 + §3.1 stays anchored in [`expected_shapes_autonomic_signals_review.md`](../literature/reviews/expected_shapes_autonomic_signals_review.md).)
- **One lead beyond citation.** Scheffer/Gijzel "critical slowing down" — rising autocorrelation + variance in a daily self-rated-health series signalling a depleting reserve near a tipping point — is simultaneously the tightest formal grounding *and* a concrete operationalisation route for R(t) that connects directly to the corpus's `E[L]*` / autocorrelation work. Flagged as a candidate for a future R-direction, not locked here.
- **Onward work.** The full page-verified, annotated grounding set (this survey) is dense enough to seed a dedicated [`literature/reviews/`](../literature/reviews/) doc; deferred until a first R-direction pre-reg needs it.

**Verified references** (PubMed-indexed items confirmed against PubMed 2026-07-19; DOIs linked). Antcliff D, et al. 2019, *Musculoskeletal Care* 17(4):335-345 [DOI](https://doi.org/10.1002/msc.1421) · Appelman B, et al. 2024, *Nat Commun* 15(1):17 [DOI](https://doi.org/10.1038/s41467-023-44432-3) · Arroll MA. 2013, *Med Hypotheses* 81(3):506-508 [DOI](https://doi.org/10.1016/j.mehy.2013.06.023) · Banister EW, et al. 1975, *Aust J Sports Med* 7:57-61 (not PubMed-indexed); Calvert TW, et al. 1976, *IEEE Trans Syst Man Cybern* SMC-6(2):94-102; Morton RH, et al. 1990, *J Appl Physiol* 69(3):1171-1177 [DOI](https://doi.org/10.1152/jappl.1990.69.3.1171) · Barakou I, et al. 2023, *Ann Med* 55(2):2270688 [DOI](https://doi.org/10.1080/07853890.2023.2270688) · Bobba-Alves N, Juster RP, Picard M. 2022, *Psychoneuroendocrinology* 146:105951 [DOI](https://doi.org/10.1016/j.psyneuen.2022.105951) · Calabrese EJ, Baldwin LA. 2022, *IUBMB Life* 74(1):8-23 [DOI](https://doi.org/10.1002/iub.2529) · Clegg A, et al. 2013, *Lancet* 381(9868):752-762 [DOI](https://doi.org/10.1016/S0140-6736(12)62167-9) · Fried LP, et al. 2001, *J Gerontol A* 56(3):M146-M156 [DOI](https://doi.org/10.1093/gerona/56.3.m146) · Gabbett TJ. 2016, *Br J Sports Med* 50(5):273-280 [DOI](https://doi.org/10.1136/bjsports-2015-095788) · Gijzel SMW, et al. 2017, *J Gerontol A* 72(7):991-996 [DOI](https://doi.org/10.1093/gerona/glx065) · Goertzel BN, et al. 2006, *Pharmacogenomics* 7(3):485-494 [DOI](https://doi.org/10.2217/14622416.7.3.485) · Grossman P. 2023, *Biol Psychol* 180:108589 [DOI](https://doi.org/10.1016/j.biopsycho.2023.108589) · Impellizzeri FM, et al. 2020, *Int J Sports Physiol Perform* 15(6):907-913 [DOI](https://doi.org/10.1123/ijspp.2019-0864) · Jason LA, et al. 2008, *AAOHN J* 56(5):189-195 [DOI](https://doi.org/10.3928/08910162-20080501-06) · Keller B, et al. 2024, *J Transl Med* 22(1):627 [DOI](https://doi.org/10.1186/s12967-024-05410-5) · Mathiowetz V, et al. 2001, *Arch Phys Med Rehabil* 82(4):449-456 [DOI](https://doi.org/10.1053/apmr.2001.22192); 2005, *Mult Scler* 11(5):592-601 [DOI](https://doi.org/10.1191/1352458505ms1198oa) · McEwen BS. 1998, *N Engl J Med* 338(3):171-179 [DOI](https://doi.org/10.1056/NEJM199801153380307) · Meeusen R, et al. 2013, *Med Sci Sports Exerc* 45(1):186-205 [DOI](https://doi.org/10.1249/MSS.0b013e318279a10a) (co-pub *Eur J Sport Sci* 13(1):1-24) · Moore GE, et al. 2023, *Medicina* 59(3):571 [DOI](https://doi.org/10.3390/medicina59030571) · O'Connor K, et al. 2019, *Chronic Illn* 15(1):51-60 [DOI](https://doi.org/10.1177/1742395317746470) · Radak Z, Chung HY, Goto S. 2008, *Free Radic Biol Med* 44(2):153-159 [DOI](https://doi.org/10.1016/j.freeradbiomed.2007.01.029) · Ristow M, Schmeisser K. 2014, *Dose Response* 12(2):288-341 [DOI](https://doi.org/10.2203/dose-response.13-035.Ristow) · Scheffer M, et al. 2018, *PNAS* 115(47):11883-11890 [DOI](https://doi.org/10.1073/pnas.1810630115) · Snell CR, et al. 2013, *Phys Ther* 93(11):1484-1492 [DOI](https://doi.org/10.2522/ptj.20110368) · Sterling P. 2012, *Physiol Behav* 106(1):5-15 [DOI](https://doi.org/10.1016/j.physbeh.2011.06.004) · Stern Y. 2009, *Neuropsychologia* 47(10):2015-2028 [DOI](https://doi.org/10.1016/j.neuropsychologia.2009.03.004) · Whitson HE, et al. 2016, *J Gerontol A* 71(4):489-495 [DOI](https://doi.org/10.1093/gerona/glv202); 2018, *JAGS* 66(8):1459-1461 [DOI](https://doi.org/10.1111/jgs.15233) · Wilshire CE, et al. 2018, *BMC Psychol* 6(1):6 [DOI](https://doi.org/10.1186/s40359-018-0218-3). **Books / grey (attribution-verified, standard editions):** Miserandino 2003 ("The Spoon Theory", essay); Siegel 1999 (*The Developing Mind*, Guilford); Porges 2011 (*The Polyvagal Theory*, Norton); Sterling & Eyer 1988 (in Fisher & Reason eds, *Handbook of Life Stress, Cognition and Health*, Wiley, pp 629-649); Taffet (homeostenosis, in Cassel ed. *Geriatric Medicine*); NICE NG206 (2021). Metadata sourced from PubMed.
- **Wiggers pacing handleiding (07-2025), the proximate practitioner source** ([`literature/wiggers_pacing_handleiding.txt`](../literature/wiggers_pacing_handleiding.txt)): describes capacity growing during recovery (p.62-63, 68-69), the small-waves pacing strategy — HR near RHR, easy activities, fast HR-return (p.63), and a 4-week body-battery buffer ("always want some energy left as a buffer", p.45). These are the descriptive antecedents this construct builds on. Crucially, the guide **declines the causal build-up claim** (p.63) — which is why R1 is subject-authored, not a Guide restatement (see Register attribution, Authorship). Its "resilience" and "buffer" are same-day / 4-week device readouts, distinct from this construct's slow latent reserve.

### 7.3 Our vision on tradeoffs

The central tradeoff is **construct richness vs n=1 identifiability**.

- **Chosen path**: define resilience as a latent state (rich; matches the subject's lived model of "building resilience"; unifies the two research lines) *while* binding it to proxies + a triangulation ceiling so no artefact over-claims. The dimension weighted is **honesty-about-reach over apparent-decisiveness**.
- **Alternative A rejected — don't reify resilience; only test observable pacing→crash associations.** Cleaner and more conservative, but discards the mechanism the subject actually wants understood (the slow reserve, the weeks-long rebuild) and cannot represent the §2.2 dissociation. Rejected because it answers a narrower question than the one asked.
- **Alternative B rejected — fit an explicit latent-state model** (state-space / HMM). Maximally faithful to the construct but *unidentifiable* at n=1 over the §4.3 collinear cluster; it would produce a fitted "reserve" trajectory indistinguishable from the disease arc and present drift as mechanism. Rejected as over-reach; §2.2 keeps only the shape commitment.
- A second tradeoff — **envelope-consistency vs activity-volume** for the pacing-quality proxy — is resolved toward envelope-consistency on the §7.2 GET-vs-pacing grounds; activity-volume would import the graded-exercise premise the PEM literature rejects.

### 7.4 Our research limitations + objectives

- **Limitations**: n=1; 29 crash episodes; observational; the treatment (pacing maturity) is time-collinear with spontaneous recovery (§4.3); the subject is an active controller (§5.1). These are why the ceiling is triangulation, not identification, and why R1 must carry a lapse-dissociation arm rather than lean on cross-era levels.
- **Objectives**: give the two research lines a shared, citable latent variable; license R1–R4 and the HA-P7 re-read with a construct that is honest about its reach; keep the crash line and the pacing line commensurate by routing both through the same reserve definition.

---

## 8. Systemic limitations (per [`research_line_limitations.md`](research_line_limitations.md))

Per the binding citation rule ([`research_line_limitations.md §1`](research_line_limitations.md)), the resilience construct invokes:

- **[L1 Single-subject reach](research_line_limitations.md#l1-single-subject-reach)** — resilience is defined for *this* system; the unusually stable RHR (§3.2) and the specific confound cluster (§4.3) are this participant's, not general. Forbids "resilience behaves this way in LC"; permits "in this participant's corpus."
- **[L2 Era confounds](research_line_limitations.md#l2-era-confounds)** — the load-bearing limitation; §4 is its elaboration for a slow latent state over a collinear treatment. The pacing-maturity / spontaneous-recovery pair (§4.3) is the specific unbreakable manifestation.
- **[L4 Analyst-is-subject](research_line_limitations.md#l4-analyst-is-subject)** — the active-controller problem (§5.1): the subject regulates the system under study, attenuating observational pacing→crash associations.
- **[L6 Self-reporting](research_line_limitations.md#l6-self-reporting)** — `gevoelscore` is a primary resilience-readout proxy (§3.2) and is self-reported; the R2 re-read's mediation framing rests on it, so the self-report caveat is load-bearing there.
- **[L7 Survivorship](research_line_limitations.md#l7-survivorship)** — lightly: crashes/near-misses not logged, or reserve-building stretches not captured, bias the visible evidence; relevant to R1's cumulative-pacing pool.

---

## 9. Evidence-inventory hooks (no new probes locked here)

Consistent with §1.2 (not a pre-registration), this MD locks **no new data probe**. The evidence each direction rests on already lives in the corpus; a future R-direction pre-reg is responsible for its own [CONVENTIONS §2.2](../CONVENTIONS.md#22-methodology-md-before-locking-a-major-choice) homework and data-availability audit. The inventory the R-pre-regs draw from:

| Direction | Existing evidence surface (for the future pre-reg to build on) |
|---|---|
| R1 | `push_burden_7d`, HA0x precursor family, the (to-be-defined) cumulative pacing-quality proxy; `lc_pre_ergo` uncontrolled-baseline anchor (§4.4) |
| R2 | [`HA-P7`](../analyses/hypotheses/HA-P7/result.md), [`post-crash-exertion-relapse`](../analyses/hypotheses/post-crash-exertion-relapse/result.md), `gevoelscore` mediation channel |
| R3 | [`HA-P6`](../analyses/hypotheses/HA-P6/result.md), [`peri-event-recovery`](../analyses/garmin_exploration/cards/peri-event-recovery-export.md), autocorrelation memory-lengths |
| R4 | [`Q24-mdbeta-wave2c`](../analyses/descriptive/Q24-mdbeta-wave2c-reactive-vs-proactive-rest/), `rest_day_p25` operand |

Any count or phase-distribution a downstream pre-reg needs must be re-probed against `per_day_master.csv` at that pre-reg's drafting time; the phase day-counts quoted in §4.1 are carried from [`post_heavy_day_pacing_learning.md §3.1`](post_heavy_day_pacing_learning.md) (probed 2026-07-16) and are indicative, not re-verified here.

---

## 10. Compression and lock discipline

Producer-mode methodology MD per [CONVENTIONS §1.1](../CONVENTIONS.md#11-producer-mode-claude-writes--edits--runs); lock discipline follows the folder pattern:

1. **Draft (this file, r1)**: producer-mode construct definition. No operand, no test spec locked.
2. **Fresh-session [`/research-methodology-review`](../.claude/commands/research-methodology-review.md)**: a different Claude session, cold context, audits this MD against the [CONVENTIONS §2.2](../CONVENTIONS.md#22-methodology-md-before-locking-a-major-choice) four-input bar (§7) + applicable 4-layer-checklist items. Produces a dated report at `docs/research/reviews/methodology-resilience_latent_state-YYYY-MM-DD.md`. Per [[feedback_pre_reg_writer_role]], drafting (this session) and review (a fresh session) must be separate sessions — satisfied by construction.
3. **r2 lock with compression absorption**: reviewer findings absorbed inline if mechanical (clarifications, cross-cites, caveat additions); architectural changes (a change to the construct definition, the dynamics-shape commitment, or the identification ceiling) force r2-with-design-change and re-review.

**Compression rule**: r2 absorption is mechanical, not architectural. A reviewer finding that the construct should be defined differently, or that the §5.3 ceiling is mis-stated, is architectural and re-reviews.

**No-downstream-lock gate**: until r1 locks, no R-direction pre-reg and no HA-P7 re-read may cite this MD as a locked anchor. They may cite it as DRAFT for context, flagged as such.

---

## 11. Lock log

| version | date | change |
|---|---|---|
| r1 | 2026-07-16 | Initial producer-mode draft. Defines resilience as a latent slowly-varying scalar state `R(t)` (§2.1) with asymmetric leaky-integrator dynamics — slow build under in-envelope pacing, fast drop at crash, slow rebuild, felt-state-leads-reserve dissociation (§2.2) — held unobserved (§2.3). Operationalises three proxy families: pacing-quality (within-day recovery morphology + proactive/reactive rest + lagged-envelope exertion; §3.1), resilience-readout (overnight autonomic stability `stress_stdev_sleep` primary, felt-state, BB floor; RHR readout-under-caveat; §3.2), and depletion event (`crash_v2` tier-1; §3.3), with binding naming discipline (never "resilience" for a proxy; §3.4). §4 confound-structure temporal-shape analysis: separable-by-shape (citalopram step, reintegration episode) vs the unbreakable monotone-rising cluster (pacing maturity + tactical-Garmin + spontaneous recovery; §4.3); `lc_pre_ergo` as uncontrolled-baseline anchor (§4.4). §5 identification: active-controller problem (§5.1), two partial escapes — short-horizon confound-immunity + lapse-dissociation (§5.2) — and the triangulation-not-identification ceiling with "consistent-with, confounder-bounded" as the terminal claim (§5.3). §6 licenses four reading axes: R1 build-up-protective (untested; core gap), R2 depletion-window (HA-P7 + relapse probed, not confirmed, flagged for resilience-lens re-read because the felt-state attenuation may be the mechanism not its absence), R3 rebuild-timescale (descriptively supported), R4 proactive-pacing (descriptively supported, confounding-by-indication caveat); read by coherence not family-multiplicity (§6.5). §7 four-input reasoning per CONVENTIONS §2.2 with two alternatives rejected (no-reification; explicit latent-state fit) and the envelope-consistency-over-activity-volume tradeoff. §8 cites L1/L2/L4/L6/L7. §9 locks no new probe; points R-pre-regs at existing surfaces. §6.2 enriched same-day by a reviewer-mode re-read of [`HA-P7`](../analyses/hypotheses/HA-P7/result.md) `result.md` (interpretive overlay, verdict stays locked): R2 standing revised from "probed twice, not confirmed" to "probed under mis-specification and underpower, not closed" — HA-P7 triple-mis-specifies R2 (count-density not depletion-state; felt-state as covariate not mediator; 14d generic window vs HA-P6's ~2.5d recovery), its §4.5.4 covariate arm is inconclusive (β_gevoel pooled CI [−2.568, +0.138] includes 0) not a confirmed gevoelscore-proxy, the across-episode inverse (HA-P6 completeness↔next-interval ρ=−0.338) is active-controller-confounded, and the dissociation-faithful test (`post-crash-exertion-relapse`) is Cannot-resolve at n=24; binding open question is power against the 27-positives ceiling. §7.2 rewritten 2026-07-19 with a page-verified grounding survey (verified against PubMed + web; ~28 sources role-mapped to R1-R4 + the sign-inversion tension + the fitness-fatigue / dynamical-systems / EMAL formal scaffolding); prior *citation-status-deferred* markers resolved; P11 prior-sources synced. Grounding verdict: grounded-in-pieces, novel-in-packaging; nearest formal homes are domain-transfers. **STATUS: DRAFT r1, awaiting fresh-session `/research-methodology-review`.** |

---

## 12. Cross-references

- [CONVENTIONS §2.1](../CONVENTIONS.md#21-descriptive-before-inference) descriptive-before-inference; [§2.2](../CONVENTIONS.md#22-methodology-md-before-locking-a-major-choice) four-input bar (the lock gate for §7); [§3.1](../CONVENTIONS.md#31-personal-baseline-not-absolute-thresholds) personal-baseline (binds §3.1 proxies); [§3.7](../CONVENTIONS.md#37-trajectory-detrend-sensitivity-for-raw-pre-vs-post-comparisons) trajectory-detrend (R1); [§4.2](../CONVENTIONS.md#42-caveats-yes-a-priori-claims-no) caveat-class framing (the §5.3 ceiling).
- [`research_line_limitations.md`](research_line_limitations.md) — L1/L2/L4/L6/L7 cited in §8; §4 is an elaboration of L2 for the latent-state case.
- [`lc_recovery_phase_axis.md`](lc_recovery_phase_axis.md) — the `recovery_phase` era axis used in §4.
- [`post_heavy_day_pacing_learning.md`](post_heavy_day_pacing_learning.md) — the learned-pacing arc + phase day-counts (§4.1) + the "phase-stratified never learned-pacing" naming precedent (§3.4) + the five-confound bundle including tactical-Garmin-pacing.
- [`bout_level_recovery_dynamics.md`](bout_level_recovery_dynamics.md) — the within-day arch/small-wave morphology operands that serve as §3.1 pacing-quality proxies.
- [`HA-P6`](../analyses/hypotheses/HA-P6/result.md) (R3), [`HA-P7`](../analyses/hypotheses/HA-P7/result.md) (R2, the re-read target), [`post-crash-exertion-relapse`](../analyses/hypotheses/post-crash-exertion-relapse/result.md) (R2), [`HA07d`](../analyses/hypotheses/HA07d-sleep-stress-variability/result.md) (§3.2 primary readout), [`Q24-mdbeta-wave2c`](../analyses/descriptive/Q24-mdbeta-wave2c-reactive-vs-proactive-rest/) (R4).
- [`recovery_phase_confounder_bound/`](../analyses/descriptive/recovery_phase_confounder_bound/) — the demonstrated confounder-domination of per-era RHR levels (§4.2).
- Memories: [[project_garmin_research_bias_boundary]] (tactical-Garmin confound, §4.1), [[project_rest_day_operand_semantics]] (proactive/reactive rest operand, §3.1/§6.4), [[feedback_flag_contradictions]] (the R2 flag, §6.2), [[feedback_pre_reg_writer_role]] (separate-session review, §10).

---

*Producer-mode construct-definition MD. Update when (a) the fresh-session `/research-methodology-review` verdict lands and informs r2 compression, (b) an R-direction pre-reg or the HA-P7 resilience re-read lands and needs the construct sharpened, (c) a lapse-dissociation operational definition (§5.2 escape 2) is authorised for a downstream MD.*
