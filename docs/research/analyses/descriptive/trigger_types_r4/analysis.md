# R4 analysis -- crash-specificity of load INTENSITY (does emotional load precede crashes?)

**Status**: producer-mode descriptive analysis, Layer-1 descriptive per
[CONVENTIONS section 4.1](../../../CONVENTIONS.md). Follow-up to the precondition
[`precondition.md`](precondition.md), which found that load *presence* is
degenerate (ambient, no crash contrast). This asks the intensity-graded question:
does *severe* or *moderate-plus* load of each type elevate in the pre-onset run-up
of a crash, versus ordinary windows? Drafted 2026-07-04 by Claude (Opus 4.8) under
producer-mode authorization, for the participant-researcher (repo owner). Every
number is reproduced by
[`crash_specificity_analysis.py`](crash_specificity_analysis.py) (seed 20260704).
This is a descriptive read, not a locked inferential test; its main output is a
lead hypothesis for a future pre-registration, plus honest limits.

> "physical / emotional / cognitive load" = the self-reported Section-2 1-3 load
> triage (mild / moderate / severe event intensity), per
> [DATA_DICTIONARY.md](../../../DATA_DICTIONARY.md) section 2.

---

## 1. Why intensity, not presence

The precondition ([`precondition.md`](precondition.md) section 4) established that
a presence-based trigger share is degenerate: the internal loads are ambient
(48-74% of any 6-day window carries one), so their presence in a crash run-up is
almost all base rate. The remaining honest question is whether **intensity**
carries what presence does not: do the *severe* (level-3) or *moderate-plus*
(level-2+) loads concentrate before crashes?

## 2. Design (pre-committed, descriptive)

- **Trigger window**: `[episode-start - 5 .. episode-start - 1]`, the five days
  *before* the crash begins. It **excludes the crash days themselves**, so a load
  is a pre-onset trigger candidate, not the crash being logged.
- **Crash units**: the **29 crash-episode starts** (earliest day per
  `crash_episode_id` with an `is_crash` day).
- **Ordinary comparison**: LC-corpus days **at least 7 days from any crash day**
  (938 days), so ordinary run-ups never overlap a crash.
- **Per load type**: the run-up **max load level** (0 if none). Statistics on the
  crash-vs-ordinary difference in `P(severe >= 3)`, `P(moderate+ >= 2)`, and mean
  max-load, each with a **two-group bootstrap 95% CI** and a **label-permutation
  p-analogue** (10,000 permutations).
- **Confound reads**: `recovery_phase`-stratified severe rate (era / note-density
  control) and infection (`cat_triggers_extern`) in a wider pre-onset window.

## 3. Results

Crash n=29, ordinary n=938. `*` = bootstrap 95% CI excludes 0.

| load | metric | crash | ordinary | diff [95% CI] | perm-p |
|---|---|---|---|---|---|
| **emotional** | **moderate+ (>=2)** | 48% | 29% | **+19pp [+0, +37]\*** | **0.028** |
| emotional | mean max-load | 1.31 | 0.86 | +0.45 [-0.03, +0.93] | 0.032 |
| emotional | severe (>=3) | 28% | 16% | +12pp [-4, +29] | 0.084 |
| physical | moderate+ (>=2) | 59% | 50% | +9pp [-10, +26] | 0.239 |
| physical | severe (>=3) | 34% | 31% | +3pp [-14, +21] | 0.429 |
| physical | mean max-load | 1.59 | 1.41 | +0.17 [-0.32, +0.62] | 0.271 |
| cognitive | moderate+ (>=2) | 72% | 67% | +5pp [-12, +21] | 0.356 |
| cognitive | severe (>=3) | 45% | 47% | -2pp [-21, +16] | 0.658 |
| cognitive | mean max-load | 1.93 | 1.83 | +0.10 [-0.36, +0.54] | 0.374 |

## 4. The emotional standout, and the guards that bound it

**Emotional load is the only trigger type with a signal.** Its moderate-plus rate
is elevated before crashes (48% vs 29%, +19pp, CI barely excludes 0, perm-p
0.028), with the mean (p=0.032) and severe (p=0.084) readings corroborating the
same direction. Physical and cognitive show essentially nothing at any intensity
threshold (every CI spans 0, perm-p 0.24-0.66).

Three guards keep this **suggestive, not established**:

- **Multiplicity.** Three load types were tested; even a lenient 3-way correction
  (0.05 / 3 ~ 0.017) leaves the best emotional p (0.028) **not significant**. The
  CI lower bounds also sit *at* 0 (moderate+) or just below (mean, severe). So the
  signal does not clear a corrected bar.
- **Era concentration (single-pool primacy).** The emotional elevation is
  **entirely in the `citalopram_modulated` phase** (severe 45% vs 15%, nC=11) and
  **absent in `pacing_habit_established`** (13% vs 16%, nC=15). Per single-pool
  primacy (CONVENTIONS), this is a **number, not an era verdict** -- but it means
  the one signal rests on a small, medication-era-confounded slice, which weakens
  even the suggestive read. It could be a real change in trigger profile over
  time, a logging / note-density shift, or chance; an n=1 design cannot adjudicate.
- **Reverse causation.** The run-up is pre-onset, but a crash **prodrome** can
  begin before the formal onset day, so heightened emotional reactivity (or more
  emotional-load logging) in the five days before could be an early sign of the
  crash rather than its trigger. Not excludable here.

## 5. Physical and cognitive: no crash-specificity (and why physical may be masked)

Neither physical nor cognitive load elevates before crashes at any intensity. For
cognitive this is consistent with its Garmin-invisibility (precondition section
5). For physical, note the **good-day confound works against detection**: physical
load happens on higher-capacity days (precondition: felt-state +0.29), while
crashes follow low days, so physical load is structurally *anti-correlated* with
imminent crashes. A genuine physical trigger could therefore be **masked** by that
selection, not absent. This is a limit of the observational design, stated, not a
claim that physical exertion does not trigger crashes (the pre-registered
push-crash test
[`../../hypotheses/post-crash-exertion-relapse/result.md`](../../hypotheses/post-crash-exertion-relapse/result.md)
separately could not resolve the physical push-to-relapse question).

## 6. Infection is not a pre-onset trigger

In the wider pre-onset window `[start-14 .. start-1]`, infection
(`cat_triggers_extern`) appears in **0% of crash run-ups vs 3% of ordinary
windows**. The precondition's nadir-inclusive "7% vs 2%" was infection logged
*at / around the nadir* -- co-occurring with, or retrospectively attributed to,
the crash -- not preceding it. So infection **co-occurs with** crashes rather than
**leading** them. (This is distinct from R23's single known COVID event near LC
onset, which is a specific dated event, not a general crash trigger.)

## 7. Coherence with the autonomic-fingerprint finding

The two threads point the same way. Emotional load is **both** the most
autonomically visible channel (precondition section 5: flat in HR, robust in
daytime GSS +0.35 and battery-floor -0.43) **and** the only trigger type
suggestively elevated before crashes (this analysis). Physical is autonomically
visible but not crash-predictive (and possibly masked, section 5); cognitive is
neither. That the wearable-visible channel and the pre-crash channel are the same
one (emotional) is a coherent, if underpowered, through-line.

## 8. Verdict (honest-limit)

- **Emotional load is the lead -- and only -- trigger candidate**: autonomically
  visible and suggestively pre-crash (moderate+ perm-p 0.028 uncorrected). But it
  **does not survive multiplicity correction** and **rests on an era-confounded
  slice**, so it is **suggestive, not established** -- the right target for a
  future *pre-registered* test with a locked threshold, a matched baseline, and
  the era-confound built in, not a settled result.
- **Physical / cognitive load**: no crash-specificity at any intensity (physical
  possibly masked by the good-day confound).
- **Infection**: not a pre-onset trigger.
- This confirms the precondition's R4 verdict: no defensible presence-based trigger
  share; the honest deliverables are these bounded reads plus the autonomic-
  fingerprint description. It also **feeds site request R32(a)**: even at intensity,
  self-reported load barely distinguishes crash run-ups, except for a suggestive
  emotional signal that does not clear a corrected bar.

## 9. Caveats

- **n=29 crashes, underpowered.** All CIs are wide; the one sub-0.05 result does
  not survive multiplicity correction.
- **Self-report, presence-conditioned** load (calendar + notes), not an instrument
  measure; note-density itself varies (partly by era), which the phase read only
  crudely controls.
- **Bootstrap CIs are day-level / unit-level**, autocorrelation not modelled ->
  approximate.
- **Era / medication confound** on the emotional signal (section 4); **reverse
  causation** not excluded (section 4).
- **No causal / interpretive marks** (CONVENTIONS section 4.1): "emotional load
  co-occurred more in crash run-ups in this subject," never "emotional load caused
  the crashes."

## 10. Cross-references

- Precondition + concordance: [`precondition.md`](precondition.md);
  analysis script [`crash_specificity_analysis.py`](crash_specificity_analysis.py).
- Physical push-to-relapse (pre-registered, could-not-resolve):
  [`../../hypotheses/post-crash-exertion-relapse/result.md`](../../hypotheses/post-crash-exertion-relapse/result.md).
- Site register R4 (trigger type), R32 (no visible trigger-into-crash signal): the
  site's `docs/research-requests.md` (external repo `wiggers_research_story`).
- Data semantics: [DATA_DICTIONARY.md](../../../DATA_DICTIONARY.md) section 2.
- CONVENTIONS: single-pool primacy, section 3.6 (named counts), section 4.1 (no
  interpretive marks), section 4.3 (a prior-driven direction, here emotional
  triggers, is confirmatory; this descriptive read is hypothesis-generating for a
  future pre-registration).

## Authorship

| Field | Value |
|---|---|
| Drafted by | Claude (Opus 4.8) under producer-mode authorization, for the participant-researcher (repo owner) |
| Date | 2026-07-04 |
| Discipline | Descriptive-only (no locked verdict); single-pool primacy; no interpretive marks (section 4.1); presence-conditioned semantics honoured; multiplicity + era-confound + reverse-causation stated. |
