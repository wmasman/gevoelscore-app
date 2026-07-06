# The moment of tipping into a crash is not visibly encoded (R32a)

**Status**: producer-mode **assembly** for site request **R32(a)**, Layer 1
(landing honesty) + Layer 4. A **synthesis of existing results, not a new
analysis** -- it draws together the trust metrics (R2 / R14), the pre-registered
push-crash null, and the R4 trigger-type work into one stated finding. Aggregated,
privacy-safe. Drafted 2026-07-06 by Claude (Opus 4.8), producer-mode, for the
participant-researcher (repo owner).

> "stress" = Garmin HRV-derived Stress Score (GSS), never mental / emotional
> stress.

## 1. The finding, stated plainly

**No signal in this body's watch data reaches a trigger / causal-precursor bar.**
The wearable reads the **weather around** a crash far better than **what set it
off**. The moment of tipping into a crash is not visibly encoded. This is the
honest floor the site's Link-1 argument rests on, and it is now backed by three
independent lines of evidence, not an assumption.

**Boundary (do not overreach):** this is NOT "my crashes have no triggers." The
defensible claim is narrower and true: **no trigger is visibly confirmable in this
watch data.** A trigger can be real and simply off-instrument (see strand 3).

## 2. Three independent lines of evidence

**(a) The signals are weak retrospective discriminators, not detectors.** At the
single-pool crash base rate of **2.11%** (29 crashes / 1372 days), the best
scorecard signal -- HA07d, the only single-pool SUPPORTED one -- has a PPV of
**~2.7%** and a lift of **1.28x**: when it fires, a crash follows roughly **1 time
in 37** (wrong about 36 times out of 37). **Every one of the seven scorecard
signals is Tier C** (lift < 2x or precision < 5%). None is a "this is tipping me
into a crash" alarm. Critically, the most trigger-shaped signal -- the exertion
lead-up (HA01b) -- is **NOT-SUPPORTED** single-pool (lift 1.06x), and the
single-axis exertion signal (HA01c) is supported-but-not-load-bearing, Tier C,
~1-in-45, and stays off the scorecard. (Source: `cards/trust-panel-export.md`,
`cards/primary-verdict-statistics.md`; site R2 / R14 / R31.)

**(b) A purpose-built trigger test could not find a push-to-crash signal.** The
pre-registered push-crash "danger window" test
([`../../hypotheses/post-crash-exertion-relapse/result.md`](../../hypotheses/post-crash-exertion-relapse/result.md))
gave the trigger idea its best possible chance -- primary exposure = peak cardiac
strain relative to current capacity (the "cardiac cost of movement" measure), a
constructed matched baseline, focused on the highest-risk post-crash window -- and
still returned **"cannot resolve," with the point estimate if anything slightly
negative.** A cleanly-designed, pre-registered attempt to catch a physical
push-to-relapse signal found nothing.

**(c) The plausible triggers are largely off-instrument, and even the on-instrument
ones are non-specific.** The R4 trigger-type work
([`../../descriptive/trigger_types_r4/`](../../descriptive/trigger_types_r4/))
found that self-reported load is **ambient** -- its *presence* in a crash run-up is
almost all base rate (no contrast) -- and only *emotional* load shows even a
*suggestive* intensity signal before crashes (does not survive multiplicity;
era-confined). And a large share of plausible triggers are **off-instrument by
construction**: cognitive load is Garmin-invisible, and emotional load is invisible
in heart rate (it leaves only a delayed overnight autonomic aftermath, not a
crash-predictive one). The guide names this directly: "the watch can't see mental
PEM."

## 3. The honest boundary

- **A physical trigger could be *masked*, not absent.** Physical load lands on
  higher-capacity days while crashes follow low days, so a genuine physical trigger
  is structurally hard to see in observational n=1 data. "Not visibly confirmable"
  is the honest claim, not "does not exist."
- **The watch reads the aftermath well.** The same channels that fail as triggers
  succeed as a **recovery signature** (R7 / R9: a distinctive days-long post-crash
  autonomic shape). So the wearable is a good *rear-view mirror* and a poor
  *windshield* -- it characterises the crash and its recovery, not its onset.
- **This is a synthesis, not a new test.** It states what the existing closed
  results already imply; no new statistic was computed for this card.

## 4. Site-consumable framing

Layer 1 landing honesty + a Layer 4 method note. Suggested plain-language line:

> The watch is good at showing what a crash looks like and how the body recovers
> from it. It is not good at seeing one coming, and it cannot tell you what set it
> off. The strongest signal, when it fires, is followed by a crash about one time
> in thirty-seven; the rest of the time it is a false alarm. Some of what triggers a
> crash -- especially mental and emotional load -- the watch cannot see at all.

Confidence: high for the negative claim (three independent lines agree); the
boundary ("not visibly confirmable, not proven absent") must travel with it.

## 5. Cross-references

- Trust metrics: `cards/trust-panel-export.md`, `cards/primary-verdict-statistics.md`
  (site R2 / R14); HA01c off-scorecard verdict (site R31).
- Push-crash null: [`../../hypotheses/post-crash-exertion-relapse/result.md`](../../hypotheses/post-crash-exertion-relapse/result.md).
- R4 trigger types: [`../../descriptive/trigger_types_r4/precondition.md`](../../descriptive/trigger_types_r4/precondition.md),
  [`analysis.md`](../../descriptive/trigger_types_r4/analysis.md),
  [`crash_phenotypes_exploratory.md`](../../descriptive/trigger_types_r4/crash_phenotypes_exploratory.md);
  the autonomic-fingerprints card `autonomic-fingerprints-of-load-export.md`.
- Recovery signature (the aftermath the watch DOES read): `beyond-guide-recovery-signature-export.md` (R7 / R9).
- Site register R32; Wiggers H2 (activity-invisible / mental PEM). External repo
  `wiggers_research_story`, `docs/research-requests.md`.
