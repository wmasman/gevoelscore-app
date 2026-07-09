# stress_mean_sleep cross-test interpretation review

**Status**: **LOCKED r1 2026-07-09** by user acceptance ("stress_mean_sleep review can be locked" 2026-07-09; Bundle H+ event 6). Reviewer-mode-with-authorization small
doc per [CONVENTIONS §1.2](../CONVENTIONS.md#12-reviewer-mode-claude-reads--critiques--explains-does-not-edit-unless-asked)
under user authorisation (2026-07-09). Cross-test interpretation-only
pass on the first Strand A `stress_mean_sleep` descriptive analysis
(landed 2026-06-18 at `84b9801`), re-read against the newer landed
corpus: Phase C-exit trio + Bundle H trio. **NOT** a re-analysis;
underlying `stress_mean_sleep` artefact remains LOCKED, and this doc
neither edits it nor changes its verdict.

Fresh-session `/research-review` per plan §4 not required at DRAFT r1
(reviewer-mode small doc; no new source-stage methodology; retained
as retrospective drift-trigger per
[`_plan_results_analysis_layer.md`](../methodology/_plan_results_analysis_layer.md)
§3.7 per §7 lock log below).

## Authorship

Drafted 2026-07-09 by Claude (Opus 4.7) in
reviewer-mode-with-authorization per [CONVENTIONS §1.2](../CONVENTIONS.md#12-reviewer-mode-claude-reads--critiques--explains-does-not-edit-unless-asked).
Authorising user: Willem (2026-07-09). The source
[`stress_mean_sleep/findings.md`](../analyses/descriptive/operationalisation_support/stress_mean_sleep/findings.md)
is LOCKED and is not edited in this session. This doc reads it against
the newer landed corpus and records what those newer landings say about
how the earlier finding should be read.

---

## 1. What the earlier analysis showed

The 2026-06-18 first Strand A analysis characterised the channel
`stress_mean_sleep` on Stratum 4 (n=1339 sleep-valid days, 2022-09-03
through 2026-06-05) as an operationalisation-support descriptive card
answering Q3.1.a through Q3.1.i per programme spec
[`descriptive/README.md`](../analyses/descriptive/README.md) §3.1
(LOCKED r3, `ccbd12e`). The verdict-shape carried in the source's
Headline is preserved verbatim here for reader-traceability
([findings.md](../analyses/descriptive/operationalisation_support/stress_mean_sleep/findings.md)
Headline, `84b9801`):

> "`stress_mean_sleep` on Stratum 4 is a **heavily right-skewed,
> autocorrelation-dense daily channel** (skew=+2.72, excess
> kurtosis=+15.5; data-driven E[L]\*=12.6 — factor-of-2 above the
> project default E[L]=7). The **citalopram-window phase medians are
> nearly flat** (range 17.04 to 20.20 across the four phases) — the
> locked +0.43/mg dose-response slope is a within-buildup-window
> effect, **not a between-phase steady-state level shift**. The
> crash-vs-normal separation is robust (episode-level Cohen's d=+0.91;
> bootstrap CI95 on mean diff [+1.58, +8.40] stress units). **One new
> near-identity pair surfaces**: `asleep_stress_avg_uds` (Pearson
> r=+0.93). All other named near-identity candidates pass the §3.3
> threshold cleanly."

The source's Limitations block preserves the descriptive discipline
per [CONVENTIONS §2.1](../CONVENTIONS.md#21-descriptive-before-inference):
no causal claims, no falsification bar, no HA-verdict frame. Review
verdict at source lock was PASS-with-caveats per fresh-session
`/research-review` at
[`reviews/descriptive-stress_mean_sleep-2026-06-18.md`](descriptive-stress_mean_sleep-2026-06-18.md);
that report remains the standing peer check.

## 2. What newer landings say about the earlier finding

The following cross-reads are informed by seven landed newer inputs
that did not exist at 2026-06-18. Each entry names the source, the
observation it lands, and how it reads against the earlier finding.
Each entry is CAVEAT-CLASS per
[CONVENTIONS §4.2](../CONVENTIONS.md#42-caveats-yes-a-priori-claims-no):
honest acknowledgment of a re-shape lens, NOT a re-analysis or a
new operationalisation choice imposed retroactively.

### 2.1 HA-C3p bin-distribution right-shift observation is cross-op validation of dose-modulation, on a sister-channel

Per [`interpretation/HA-C3p.md`](../analyses/interpretation/HA-C3p.md)
§2 + §4.5 L2 caveat: the unmedicated per-bin distribution on
`all_day_stress_avg` is right-shifted relative to the full Stratum 4
pool (Q1 share 7.7% unmed vs 18.4% full pool; Q5 share 32.5% unmed
vs 22.6% full pool). This is called out in the HA-C3p source as
"consistent with citalopram's CONFIRMED +0.57/mg `all_day_stress_avg`
β per [`citalopram_dose_response_stress_mean_sleep §5.6.1`](../methodology/citalopram_dose_response_stress_mean_sleep.md#561-per-channel-three-pronged-read).
Cross-test validation of the recalibration finding at a different
operationalisation level."

Read against the earlier finding: the earlier Q3.1.d observation was
that the +0.43/mg locked dose-response β on `stress_mean_sleep` did
NOT produce a between-phase median shift; the medians are nearly
flat (17.04 to 20.20 across four phases) despite the +12.9-unit
naive-30mg extrapolation. HA-C3p now supplies a cross-op signature of
the same dose-modulation family on a sibling channel
(`all_day_stress_avg`, +0.57/mg): a right-shifted bin distribution in
the unmedicated sub-pool. The earlier finding's readings (§Q3.1.d
readings 1-3) already anticipated this: the slope is a
within-window effect, the LC trajectory absorbs the between-phase
level shift, the 30mg extrapolation is a slope-extrapolation not a
level prediction, and this cross-test observation on the sibling
channel is CAVEAT-CLASS corroboration of the interpretive-lens the
source already carries. The observation does NOT motivate any change
to Q3.1.c-Q3.1.d numbers or to the reading that steady-state-pooled
tests are the safer default for cross-phase comparisons; it supplies
one more sibling-channel data point for the same cross-op signature.

### 2.2 Stage I §3 stringent-operand-threshold nuance and Stage I §4.6 user-articulated envelope-crossing prior

Per [`interpretation/HA-C4c.md`](../analyses/interpretation/HA-C4c.md)
§3 amendment absorbed at Phase C cluster-level lock 2026-07-08
(user Q B2 verbatim): "modest elevation on already-rare stringent
event is substantively different from same δ on common event."
Per HA-C4c §4.6 USER-ARTICULATED verbatim (Willem, 2026-07-08):
"My felt pattern is that on days that I go out of my energy
envelope (so maybe, heavy exertion above baseline?) and especially
near the end of the day, I can get 'stuck' longer."

Read against the earlier finding: the earlier Q3.1.g Implication was
that `stress_mean_sleep` is by-construction a daily-aggregate and
therefore "dilution-vulnerable for acute-load mechanisms" per
CONVENTIONS §3.5, with an explicit statement that "a future HA whose
mechanism is acute sleep-disturbed arousal ... should NOT use this
channel as primary — a spike-of-night primitive ... would be the
correct surface." The user's 2026-07-08 articulation independently
lands at a similar shape at a different construct layer: the felt
pattern is temporally textured (end-of-day) and personal-envelope
framed (out-of-envelope, not training-load-heavy absolute), NOT
daily-aggregate anywhere-in-24h at absolute levels. The Stage I §3
nuance further clarifies that a small effect on a stringent-tail
operand is substantively different from the same effect on a common
operand. Reading these two nuances back onto the earlier finding: the
earlier Q3.1.d "medians nearly flat" characterisation should be read
with the caveat that a small between-phase median shift on a
daily-aggregate channel does not in itself say much about the
substantive within-day acute-load pattern the user's lived prior
points at. The earlier finding's own Limitations bullet 2 already
carries this shape ("dilution-vulnerable for acute-load mechanisms"),
so the newer nuance is CAVEAT-CLASS corroboration of a caveat the
source already carries; the newer nuance does NOT relax the discipline
that Q3.1.d's numbers are the numbers and cross-phase pooling of
daily aggregates is the safer default the source recommends.

### 2.3 HA-C3 cluster inverted-U joint finding

Per [`interpretation/HA-C3.md`](../analyses/interpretation/HA-C3.md)
§2 + §3 + §4 (wrong-direction override, bin-mean peak at Wiggers
30-40 band) and [`interpretation/HA-C3p.md`](../analyses/interpretation/HA-C3p.md)
§2 + §3 + §4 (2-of-3 PARTIAL with (b) + (c) PASS detecting curvature
in the non-monotone direction; quintile peak at Q4 = stress 34-37):
both sister-HAs on `all_day_stress_avg × gevoelscore` (a sibling
channel to `stress_mean_sleep`) detect a joint inverted-U shape on
the participant's cross-day-aggregate mapping under two
independent operationalisations (Wiggers-verbatim absolute bins +
personal-baseline-anchored quintiles).

Read against the earlier finding: the earlier analysis surfaces
`stress_stdev_sleep` (r=+0.60) and other sibling channels but does
not carry any cross-day-aggregate mapping onto `gevoelscore`. Its
Q3.1.f crash-drop sensitivity row reports `Spearman(stress_mean_sleep,
gevoelscore) = -0.194` on full Stratum 4 (dropping to -0.147 with
crash-days excluded; |Δ| = 0.047 < §3.4 threshold; no flag). The
HA-C3 / HA-C3p cluster joint finding is on `all_day_stress_avg`, not
on `stress_mean_sleep`, so it does not directly re-shape the earlier
finding's numbers. It does, however, motivate carrying forward a
consistent caveat when the earlier finding's channel is used as a
predictor of `gevoelscore` in any future HA: the sibling channel
`all_day_stress_avg` produces an inverted-U shape on the same
outcome at two independent operationalisations, so any future HA on
`stress_mean_sleep × gevoelscore` should probably not pre-commit to a
monotone shape without a sister-pre-reg on the personal-baseline
anchor per HA-C3 / HA-C3p precedent. This is CAVEAT-CLASS for future
HA design; it does NOT change any earlier finding number or verdict.

### 2.4 T-within-day-recovery Stage S₂ AGREES + EXTENDS positioning + guide r4 §5.6 cascade-inheriting topic constellation discipline

Per [`contextualisation/topic-within-day-recovery.md`](../analyses/contextualisation/topic-within-day-recovery.md)
§4.5 topic-level positioning summary (LOCKED r1 2026-07-08) and
[`methodology/external_contextualisation.md`](../methodology/external_contextualisation.md)
r4 §5.6 (cascade-inheriting topic constellation, mirror-application
of `internal_synthesis.md` §5.5 at the S₂ layer): the topic-level
positioning of the C-bout-substance + C-bout-framework constellation
against the LC / ME/CFS autonomic-dysregulation consensus is
AGREES-on-direction + EXTENDS-on-within-day-bout-level-resolution,
with a cascade-source bounded qualifier that TRAVELS through
downstream propagation surfaces per guide r4 §5.6.

Read against the earlier finding: the earlier `stress_mean_sleep`
analysis is not part of the C-bout-substance cluster and is not part
of the T-within-day-recovery topic (which lives at bout-level
resolution rather than daily-aggregate sleep-window resolution).
The topic-level AGREES + EXTENDS positioning therefore does NOT
extend to the earlier finding at any load-bearing level; guide r4
§5.6 explicitly forbids double-counting cascade-source verdicts as
strengthening evidence downstream. The relevant CAVEAT-CLASS pointer
is only that any future HA on `stress_mean_sleep` that reads its
cross-crash separation (episode-level d=+0.91 per Q3.1.f) as a
within-day autonomic-recovery signal would be reading a daily
aggregate as if it were a bout-level operand, which the earlier
finding's own Limitations bullet 2 forbids and which the newer topic
+ guide r4 §5.6 discipline further clarifies is a distinct resolution
layer. No re-shape of the earlier finding's numbers or verdict-shape
is licensed by the topic-level positioning.

### 2.5 K-bout-recovery-signal §5.7 PPV structural corpus-level constraint on within-day warning-signal claims

Per [`actionability/construct-bout-recovery-signal.md`](../analyses/actionability/construct-bout-recovery-signal.md)
§5.7 (LOCKED r1 2026-07-08; Bundle H patient-audience r2 refinement +
Track B OI-025 Step 1 protocol lock + Track A LP-test protocol lock
all landed 2026-07-09 at commit `a943f31` and follow-on): the
PPV-with-base-rate for the bout-level operand `bout_n_did_not_return_day`
at the current-stabilised-era residual-crash base rate (~2/year per
[RESEARCH-REPORT.md](../RESEARCH-REPORT.md) §5.2) sits in the
low-single-digit-percent range, of the same order-of-magnitude as
the ~4% RESEARCH-REPORT §5.2 precedent for daily-aggregate warning
alerts. Per K-bout §5.7 substantive interpretation: "this is the
**structural corpus-level constraint on within-day bout-level
warning-signal claims**, NOT a critique of the finding itself"; any
predictive-alert framing on this construct is refused per §5.4
refusals 1 + 5 + 6.

Read against the earlier finding: `stress_mean_sleep` is a
daily-aggregate channel, and the earlier finding's Q3.1.f
episode-level Cohen's d=+0.91 + Q3.1.i secondary-logistic covariate
recommendations are already in the daily-aggregate register. The
Bundle H refined patient-audience wording ("24 van de 25 keer fout"
per the PPV framing), the OI-025 Step 1 two-step study protocol
(distributional-only + descriptive δ-vs-stringency, with Step 2 pre-reg
strictly separated from any peek at Pass 2 δ curve), and the Track A
LP-test protocol for the layperson-test scheduling on the patient-
audience §5.11 rendering all together clarify that the
structural-PPV-constraint is a corpus-level property at this crash
base rate: any future HA that uses `stress_mean_sleep` as a
predictor of a crash-related outcome, and that would attempt to
translate the descriptive substrate into a warning-signal, would
hit the same low-single-digit-percent PPV ceiling under the current
stabilised-era regime. This is CAVEAT-CLASS foreknowledge for any
future HA-pre-reg author working from the earlier finding: the
descriptive substrate is what it is, and predictive-value translation
requires the tier-3 hard predictive gate per
[`actionability_translation.md`](../methodology/actionability_translation.md)
§3.10 which the earlier finding does not, and cannot, discharge on
its own. It does NOT change the earlier finding's Q3.1.f numbers or
verdict-shape.

### 2.6 Guide r3 §4.2.1 cross-op-independence bar for single-member cascade-inheriting clusters

Per [`methodology/actionability_translation.md`](../methodology/actionability_translation.md)
r3 §4.2.1 (LOCKED 2026-07-08 as retroactive friction-fix at same
commit-cycle as `construct-bout-recovery-signal.md` LOCKED r1): the
tier-2 evidence-floor for single-member cascade-inheriting clusters
is met via a "gap-named + future-closeable-via-named-OI" reading
provided four conditions hold (map §5 tier-2 aspiration pre-declared;
concrete OI names closure pathway; §5.2 flags gap as informative
shape not blocking; cascade-source bounded qualifier travels through
downstream surfaces).

Read against the earlier finding: `stress_mean_sleep` is a
descriptive-Layer-1 operationalisation-support artefact per
CONVENTIONS §2.1, not a Stage A construct-level claim; the guide r3
§4.2.1 bar applies at Stage A construct-level tier-2 licensing, not
at Layer 1 descriptive characterisation. The earlier finding is
therefore not subject to the §4.2.1 bar directly. It is CAVEAT-CLASS
foreknowledge for the design of any future Stage A construct that
would consume the earlier finding as a substrate: if a future
Stage A construct on `stress_mean_sleep` aspires to tier-2, it
would need either two independent HAs (per §4.2 strict cross-op
independence) or a single-member cascade-inheriting configuration
satisfying all four §4.2.1 conditions, plus the §3.10 PPV-with-base-rate
computation at Stage A time. The earlier finding's own Q3.1.i
covariate-sensitivity readiness section already surfaces three
disambiguation covariates (dose_plasma_mg, resting_hr,
stress_mean_sleep_lagged_mean_14d), any of which could motivate
cross-op sister-HA pairs at a future Stage A. This is a design-time
CAVEAT-CLASS pointer for future consumers of the earlier finding, NOT
a re-shape of the earlier finding itself.

### 2.7 Stage I §4.6 first-time L4-agreement-with-substantive-reframe pattern

Per [`interpretation/HA-C4c.md`](../analyses/interpretation/HA-C4c.md)
§4.6 traceability block (L4 pattern verified 4× as of 2026-07-08):
across HA-C3 v2, HA-C3p, HA11-bout-redo, and HA-C4c the subject's
felt prior lives at the personal-envelope / temporal-profile /
actual-felt-quality layer, NOT at the parent-MD's operationalisation
layer or the pre-reg's testing-classifier layer. HA-C4c is the
first-time directional agreement (envelope-crossing produces
"stuck" longer, especially end-of-day) with substantive scope reframe
(from training-load-heavy absolute classifier toward personal-envelope
crossing) and language nuance (declines "SHOULD").

Read against the earlier finding: `stress_mean_sleep` was
descriptive-Layer-1 characterisation without any §4.6-style lived-
experience-prior seed, so the pattern does not fold in as a
re-shape of the earlier finding directly. It IS relevant as a
design-time reminder for any future HA on `stress_mean_sleep`: the
subject's felt prior is likely to arrive as an envelope-crossing +
end-of-day-textured articulation rather than as a Garmin-classifier-
matched absolute-threshold articulation. CAVEAT-CLASS pointer for
future HA design; NOT a re-shape of the earlier finding's numbers.

## 3. What this interpretation licenses

**No new claim added; earlier verdict preserved verbatim.** The
seven newer landings above are each CAVEAT-CLASS per
[CONVENTIONS §4.2](../CONVENTIONS.md#42-caveats-yes-a-priori-claims-no)
and reshape only how the earlier finding is READ into downstream
work, not what the earlier finding SAYS at its own layer. Explicit
enumeration of the verdict-shape preserved verbatim from the source
([findings.md](../analyses/descriptive/operationalisation_support/stress_mean_sleep/findings.md)):

1. Q3.1.a distribution shape verdict: heavily right-skewed
   (skew=+2.72, excess kurtosis=+15.5), heavy_tail_flag = True, MAD
   robust-equivalent SD 30% below raw std, robust personal baselines
   default per CONVENTIONS §3.1. **Preserved verbatim.**
2. Q3.1.b autocorrelation-and-block-length verdict: data-driven
   E[L]\* = 12.6 vs project default 7, factor-of-2 deviation flag
   FIRES per
   [`permutation_null_block_length.md`](../methodology/permutation_null_block_length.md).
   Downstream HA pre-regs on the channel must use E[L]\* ≈ 13 as
   primary bootstrap CI or pre-spec sensitivity at E[L] = 13
   alongside default-E[L] = 7. **Preserved verbatim.**
3. Q3.1.c per-phase base rates: unmedicated n=572 median 19.51;
   buildup n=71 median 17.04; consolidation n=627 median 19.07;
   afbouw n=69 median 20.20; transition phases carry a ~5× n
   disadvantage vs steady-state phases for per-phase verdicts.
   **Preserved verbatim.**
4. Q3.1.d phase-stratified verdict: the locked +0.43/mg dose-response
   slope does NOT translate to a between-phase median shift at
   steady-state (consolidation - unmedicated = -0.44, within MAD);
   the slope is a within-buildup-window effect, not a steady-state
   level shift; three consistent readings preserved. Operational
   consequence: §5.A per-phase stratification is the safer default
   for steady-state pooled tests. **Preserved verbatim.**
5. Q3.1.e near-identity verdict: new pair `asleep_stress_avg_uds`
   (Pearson r = +0.929, Spearman ρ = +0.895) surfaces above the
   §3.3 threshold; other five candidates pass cleanly. Any HA using
   `stress_mean_sleep` should NOT also enter `asleep_stress_avg_uds`
   as a "second autonomic channel". **Preserved verbatim.**
6. Q3.1.f crash-vs-normal verdict: episode-level Cohen's d = +0.91;
   bootstrap CI95 on mean diff [+1.58, +8.40]; day-level d = +1.05
   with block-length-sensitivity showing CIs at E[L] = 7 and E[L] = 13
   differ by only +5% width; crash-drop sensitivity |Δ| = 0.047
   under §3.4 threshold (no flag). **Preserved verbatim.**
7. Q3.1.g spike-detecting primitive availability verdict: channel
   is by-construction a daily aggregate; sleep-window spike
   primitive is latent in monitoring_b FIT and not in the master;
   future acute-load mechanism HAs should NOT use this channel as
   primary. **Preserved verbatim.**
8. Q3.1.h outlier + drift verdict: 16 outlier-days flagged; not
   artefacts; downstream HAs should NOT trim; no calibration-drift
   signature. **Preserved verbatim.**
9. Q3.1.i covariate-sensitivity recommendation: pre-spec three
   secondary sensitivity arms (`dose_plasma_mg(d)`, `resting_hr`,
   `stress_mean_sleep_lagged_mean_14d`); §5.B citalopram-dose
   adjustment obligatory per framework; other two diagnostic.
   **Preserved verbatim.**

**Modest re-reads (CAVEAT-CLASS, all downstream-facing)** landed by
this interpretation pass are:

- Any future HA that uses `stress_mean_sleep` as a predictor of a
  crash-related outcome and that would translate the descriptive
  substrate into a warning-signal reading should carry the K-bout-recovery-signal
  §5.7 structural-PPV-corpus-level-constraint pointer forward
  (~low-single-digit-percent PPV ceiling at the current
  ~2/year residual-crash base rate, wrong ~24 out of 25 times when
  it fires; per §2.5 above).
- Any future Stage A construct that would consume the earlier finding
  as a substrate at tier-2 aspiration should honour the guide r3
  §4.2.1 cross-op-independence bar (either two independent HAs or a
  single-member cascade-inheriting configuration with all four
  §4.2.1 conditions satisfied; per §2.6 above).
- Any future HA on `stress_mean_sleep × gevoelscore` should probably
  not pre-commit to a monotone shape without a sister-pre-reg on the
  personal-baseline anchor per HA-C3 / HA-C3p precedent (per §2.3
  above).
- Any future Stage I on `stress_mean_sleep` HA outputs should
  anticipate the subject's felt prior arriving in envelope-crossing +
  end-of-day-textured language rather than in Garmin-classifier-matched
  absolute-threshold language (per §2.7 above).

All four are CAVEAT-CLASS. None is A-PRIORI-CLASS per
[CONVENTIONS §4.2](../CONVENTIONS.md#42-caveats-yes-a-priori-claims-no):
none presupposes a phenomenon before a test has run, none rebrands
an operationalisation basis, none supersedes a locked finding number
or verdict.

## 4. What this interpretation does NOT license

Enumerated per
[CONVENTIONS §4.3](../CONVENTIONS.md#43-prior-driven-hypotheses-are-confirmatory-not-exploratory)
+ §4.2:

1. **NO new hypothesis pre-registration** triggered by this
   interpretation. Any future HA on `stress_mean_sleep` would need
   its own pre-reg, its own methodology-MD reasoning per CONVENTIONS
   §2.2, its own Stage D + Stage I + Stage S₁ + Stage S₂ + Stage A
   + Stage T cascade if it aspires to actionability. This doc does
   not shortcut any of that. Registering a new HA on the strength of
   this cross-read would violate §4.3 confirmatory-vs-exploratory
   discipline.
2. **NO re-analysis of the underlying `stress_mean_sleep` data.**
   The `run.py`, the `findings.md`, and the derived summary /
   plot artefacts are LOCKED and are not re-run in this session.
   No number in the source is recomputed; no `Δ` re-derived; no
   verdict re-evaluated.
3. **NO verdict change on the earlier finding.** All nine
   Q3.1.a-Q3.1.i verdict-shapes are preserved verbatim per §3
   enumeration above. The peer-review verdict PASS-with-caveats at
   [`reviews/descriptive-stress_mean_sleep-2026-06-18.md`](descriptive-stress_mean_sleep-2026-06-18.md)
   remains standing.
4. **NO reach-extension to group-level or cross-subject claims.**
   The earlier finding is single-subject descriptive per
   [`research_line_limitations.md`](../methodology/research_line_limitations.md)
   L1; the newer landings (topic-level AGREES + EXTENDS at
   T-within-day-recovery; K-bout PPV structural constraint) do
   not extend the earlier finding's reach beyond its own scope.
5. **NO tier promotion of the earlier finding.** The earlier
   finding is Layer-1 descriptive per CONVENTIONS §2.1; it does
   not carry a tier (tier-1 monitoring / tier-2 informative-pattern /
   tier-3 predictive-use). The `actionability_translation.md` tier
   framework applies at Stage A construct-level, not at Layer-1
   descriptive. This interpretation does not promote the earlier
   finding into the tier framework.
6. **NO Stage A construct-level licensing.** No K-* construct
   spins up from this doc. The earlier finding remains an
   operationalisation-support descriptive card, not a substrate for
   Stage A licensing without an independent Stage D + Stage I +
   Stage S₁ + Stage S₂ + Stage A cascade.

## 5. Open questions surfaced (for user decision on OI queue)

Three OI candidates emerged from the cross-read. All are surfaced
here for the user's decision on whether to add to the
[`_open_inputs.md`](../methodology/_open_inputs.md) queue; this doc
does NOT auto-add per authorising-user discipline (Willem's queue
management is user-owned).

- **Candidate OI-A**: Cross-channel-correlation-card refresh to
  propagate the new `stress_mean_sleep` ≡ `asleep_stress_avg_uds`
  near-identity pair (Q3.1.e) into the card's 7-channel panel. The
  earlier finding's Limitations bullet 5 already logs this as a
  queued propagation; surfacing here as a formal OI candidate would
  make the propagation traceable in the OI queue. **Effort**: S
  (single-file update in
  [`analyses/garmin_exploration/cards/cross-channel-correlation.md`](../analyses/garmin_exploration/cards/cross-channel-correlation.md)
  + one cross-reference into the earlier finding's Status refresh
  trigger 4).
- **Candidate OI-B**: `dose_plasma_mg(d)` materialisation in
  `per_day_master.csv` per CONVENTIONS §3.2-style column-lifetime
  discipline. The earlier finding's Q3.1.i first covariate names
  `dose_plasma_mg(d)` as obligatory under
  [`citalopram_phase_stratification.md`](../methodology/citalopram_phase_stratification.md)
  §5.B for any future HA on the channel, and notes the column is
  currently runtime-computed per
  [`citalopram_dose_response/dose_response.py`](../analyses/garmin_exploration/intervention_effects/dose_response.py)
  and "materialisation ... is queued." Surfacing as a formal OI
  candidate would move it from source-inline "queued" language to
  tracked queue item. **Effort**: S-M (column derivation already
  exists at runtime; consolidation into
  [`pipeline/03_consolidate/build_unified_dataset.py`](../pipeline/03_consolidate/build_unified_dataset.py)).
- **Candidate OI-C**: Sleep-window spike primitive extraction from
  monitoring_b FIT (currently latent per Q3.1.g), as a companion
  channel to `stress_mean_sleep` for any future acute-load-mechanism
  HA. The earlier finding's Limitations bullet 2 anticipates this
  ("a future HA whose mechanism is acute sleep-disturbed arousal
  ... should use a sleep-window spike primitive ... rather than
  this channel as primary"), and §2.2 of this doc corroborates the
  same shape from the user-articulated envelope-crossing +
  end-of-day-textured prior at HA-C4c §4.6. Surfacing as a formal
  OI candidate would make the extraction task tracked. **Effort**:
  M (new pipeline step under
  [`garmin/scripts/sleep_stress_extract/`](../../garmin/scripts/sleep_stress_extract/),
  parallel to the current `extract_sleep_stress.py`).

None of the three is blocking anything. The user decides whether to
add any / all to the queue; this doc surfaces only.

**Outcome 2026-07-09** (added post-draft as reader-transparency note per
CONVENTIONS Sec 4.1 descriptive-before-inference; does not change any §5
candidate content above): user delegated the queue-add decision to
orchestrator via routing question "what do you recommend?" 2026-07-09;
orchestrator recommended add A + B (both low-friction; A already logged
as "queued propagation" in source, B is obligatory covariate for any
future HA on the channel) + defer C (higher effort; blocks a specific
speculative future acute-load-mechanism HA class that may not be
actionable near-term). Applied: Candidate OI-A added to
[`_open_inputs.md`](../methodology/_open_inputs.md) as **OI-034**; Candidate
OI-B added as **OI-035**; Candidate OI-C left surfaced-only-deferred per
orchestrator recommendation. Bundle H+ event 5 commit-cycle 2026-07-09.
User may surface OI-C later if the acute-load-mechanism HA class becomes
actionable.

## 6. Cross-references

**Source artefact (LOCKED; NOT edited in this session)**:

- [`analyses/descriptive/operationalisation_support/stress_mean_sleep/README.md`](../analyses/descriptive/operationalisation_support/stress_mean_sleep/README.md)
  (per-analysis README per programme §7a).
- [`analyses/descriptive/operationalisation_support/stress_mean_sleep/findings.md`](../analyses/descriptive/operationalisation_support/stress_mean_sleep/findings.md)
  (Q3.1.a-i writeup + Limitations + Status; commit `84b9801`
  2026-06-18).
- [`analyses/descriptive/operationalisation_support/stress_mean_sleep/run.py`](../analyses/descriptive/operationalisation_support/stress_mean_sleep/run.py)
  (locked runner; uses
  [`_utils/frame.py`](../analyses/_utils/frame.py) +
  [`_utils/inference.py`](../analyses/_utils/inference.py)).
- Standing peer review:
  [`reviews/descriptive-stress_mean_sleep-2026-06-18.md`](descriptive-stress_mean_sleep-2026-06-18.md)
  (verdict PASS-with-caveats).

**Phase C-exit + Bundle H artefacts consulted (LOCKED)**:

- [`analyses/interpretation/HA-C4c.md`](../analyses/interpretation/HA-C4c.md)
  §3 stringent-operand-threshold amendment + §4.6 user-articulated
  envelope-crossing prior (LOCKED r1 2026-07-08).
- [`analyses/interpretation/HA-C3.md`](../analyses/interpretation/HA-C3.md)
  wrong-direction override + inverted-U bin-mean trajectory
  (LOCKED r1 2026-06-25).
- [`analyses/interpretation/HA-C3p.md`](../analyses/interpretation/HA-C3p.md)
  2-of-3 PARTIAL + bin-distribution right-shift observation
  (LOCKED r1 2026-06-25).
- [`analyses/contextualisation/topic-within-day-recovery.md`](../analyses/contextualisation/topic-within-day-recovery.md)
  AGREES-on-direction + EXTENDS-on-within-day-bout-level-resolution
  (LOCKED r1 2026-07-08).
- [`analyses/actionability/construct-bout-recovery-signal.md`](../analyses/actionability/construct-bout-recovery-signal.md)
  §5.2 tier-2 evidence check + §5.7 PPV structural corpus-level
  constraint (LOCKED r1 2026-07-08; patient-audience r2 LOCKED
  2026-07-09).
- [`analyses/actionability/construct-stress-fatigue-monitoring.md`](../analyses/actionability/construct-stress-fatigue-monitoring.md)
  tier-1 monitoring (Phase-A construct precedent; LOCKED r1
  2026-06-25).

**Methodology MDs consulted (LOCKED)**:

- [`methodology/actionability_translation.md`](../methodology/actionability_translation.md)
  r3 §4.2.1 cross-op-independence bar for single-member
  cascade-inheriting clusters (LOCKED r3 2026-07-08).
- [`methodology/external_contextualisation.md`](../methodology/external_contextualisation.md)
  r4 §5.6 cascade-inheriting topic constellation (LOCKED r4
  2026-07-08).
- [`methodology/translation_to_audience.md`](../methodology/translation_to_audience.md)
  r3 (§5.6.1 tier-2 rendering + §5.7.1 four-surface layperson-test +
  §5.11.1 cascade-source qualifier + L4 provenance; LOCKED r3
  2026-07-08).
- [`analyses/hypotheses/HA-C4c-stringency-companion/protocol.md`](../analyses/hypotheses/HA-C4c-stringency-companion/protocol.md)
  Bundle H Track B OI-025 Step 1 two-step study protocol (LOCKED r1
  2026-07-09).
- [`analyses/translation/patient-audience/construct-bout-recovery-signal_layperson-test-protocol.md`](../analyses/translation/patient-audience/construct-bout-recovery-signal_layperson-test-protocol.md)
  Bundle H+ Track A LP-test protocol (LOCKED r1 2026-07-09).
- [`methodology/citalopram_dose_response_stress_mean_sleep.md`](../methodology/citalopram_dose_response_stress_mean_sleep.md)
  v3 §5.6.1 (dose-response locks; unchanged since source lock).
- [`methodology/citalopram_phase_stratification.md`](../methodology/citalopram_phase_stratification.md)
  §3 + §5.A + §5.B (unchanged since source lock).
- [`methodology/permutation_null_block_length.md`](../methodology/permutation_null_block_length.md)
  (unchanged since source lock).

**Governance anchors**:

- [`CONVENTIONS.md`](../CONVENTIONS.md) §1.2
  reviewer-mode-with-authorization; §2.1 descriptive-before-inference;
  §3.1 personal-baseline; §3.3 near-identity threshold; §3.4
  crash-drop sensitivity; §3.5 spike-detecting metrics; §3.6 named
  counts; §4.1 no interpretive marks; §4.2 caveats-yes-a-priori-no;
  §4.3 confirmatory-vs-exploratory.
- [`STOCKTAKE.md`](../STOCKTAKE.md) §7 "Actionable now" (refresh
  2026-07-08 + Bundle H multi-lock 2026-07-09); this doc lands as
  item 4 of the 2026-07-08 refresh "stress_mean_sleep findings
  interpretation pass".
- [`reviews/README.md`](README.md), the 4-layer review checklist +
  filename convention this doc borrows from for style; NOT a
  4-layer peer review (this is a cross-test interpretation-only
  small doc).

## 7. Lock log

| Date | Event | Note |
|---|---|---|
| 2026-07-09 | DRAFT r1 | Reviewer-mode-with-authorization small doc per CONVENTIONS §1.2 under user authorisation 2026-07-09. Fresh-session `/research-review` per plan §4 NOT dispatched at DRAFT r1 (reviewer-mode small doc; no new source-stage methodology; retained as retrospective drift-trigger per `_plan_results_analysis_layer.md` §3.7). **Verdict-shape summary**: newer context LEAVES-ALONE the earlier `stress_mean_sleep` verdict-shape (all nine Q3.1.a-i verdicts preserved verbatim per §3); CAVEAT-CLASS re-shape lens for downstream consumers only (no re-analysis, no HA pre-reg, no tier promotion). **Drift triggers registered**: (1) source [`stress_mean_sleep/findings.md`](../analyses/descriptive/operationalisation_support/stress_mean_sleep/findings.md) re-locks (any Status §Refresh trigger 1-4 firing on the source triggers a re-examination here); (2) Phase C-exit artefact re-locks (any of HA-C4c / HA-C3 / HA-C3p / T-within-day-recovery / K-bout-recovery-signal / K-stress-fatigue-monitoring / guide r3 §4.2.1 / guide r4 §5.6 / Bundle H artefacts re-lock triggers a re-examination here); (3) ≥6 months elapse since this lock; (4) a new Phase-D or Phase-E cross-test interpretation pass lands (this doc folds in or is superseded by the broader cross-test pass). |
| 2026-07-09 | **LOCKED r1** by user acceptance ("stress_mean_sleep review can be locked" 2026-07-09) | Bundle H+ event 6 commit-cycle. Reviewer-mode small doc lifts from DRAFT r1 → LOCKED r1 without content revision (§1-§7 preserved verbatim from DRAFT r1). §5 outcome-note (added post-DRAFT documenting OI-A → OI-034 + OI-B → OI-035 + OI-C deferred queue-add decisions per user delegation "what do you recommend?" 2026-07-09) preserved verbatim. Fresh-session `/research-review` per plan §4 NOT dispatched pre-lock: reviewer-mode small doc under `reviews/` per plan §4 producer/reviewer split table row; no new source-stage methodology; retained as retrospective drift-trigger per plan §3.7. All 4 drift triggers from DRAFT r1 row remain active in LOCKED r1. **Bundle H+ event 6** on origin/main: Stage A construct-bout-recovery-signal.md r1 → r2 revision (OI-025 → OI-033 pointer swap) + Track A LP-test protocol CLOSED-USER-DECIDED-NOT-TO-EXECUTE + OI-032 LP-test component CLOSED + cross-channel-correlation card reframe + OI-034 CLOSED-BY-EXECUTION + OI-035 CLOSED-RETROACTIVELY-PRE-COMPLETED + this stress review LOCKED r1 all landed same commit-cycle. |
