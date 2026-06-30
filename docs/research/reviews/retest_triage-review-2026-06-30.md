# Review — R18 hypothesis re-test triage (`_retest_triage_2026-06-30.md`)

**Target**: [`analyses/hypotheses/_retest_triage_2026-06-30.md`](../analyses/hypotheses/_retest_triage_2026-06-30.md)
**Review date**: 2026-06-30
**Reviewer mode**: Fresh session — no exposure to the drafting context; doc-only knowledge (CONVENTIONS §1.2 reviewer-mode-with-authorization fresh-session peer-review). Read-only on the target.
**Standard**: 4-layer checklist in [`reviews/README.md`](README.md), anchored to CONVENTIONS §3 + §4 audit hooks.
**Verdict**: **REVISION RECOMMENDED** — the merged routing is broadly sound and the headline ("most rows no-change/overlay-only; short re-run list") survives independent verification, but the **HA10 measurement-regime rationale is factually wrong on three counts** (Layer 2 data-provenance fire). The *action* (needs-rerun for HA10) survives on a different, sound ground; the *stated reason* must be corrected before this triage feeds R14-v2 / R20 scope, or a downstream re-run will be scoped against a non-existent data artifact.

---

## 1. What the data shows (empirical claim vs framing)

**Empirical core (verified, holds).** The single-pool re-anchor at
[`single_pool_reanchor/findings.md`](../analyses/descriptive/operationalisation_support/single_pool_reanchor/findings.md)
ran 10 HAs on the full Stratum-4 pool (n_days=1372, n_crash_episodes=29,
block-permutation E[L]=7, B=10,000, stationary-bootstrap 95% CI). All 10
CONVERGE with their locked overall verdicts; only **HA07d** clears
single-pool (perm p=0.029, +19.7pp); the other nine are NOT-SUPPORTED
with wide CIs. I cross-checked every single-pool number the triage cites
per row against the findings table — **all match** (HA07c +10.8, HA07d
+19.7, HA08c +13.4, HA10 +16.2→+4.1, HA11 +16.8 p=0.091, H01 −3.1,
H02b +3.5, H04 +0.5, HA06b +6.7; findings.md §2 lines 15-24). The driver
ledger the triage relies on (CONFIRMED dose-modulated channels
`stress_mean_sleep` +0.43/mg, `all_day_stress_avg` +0.57/mg, `bb_lowest`
−1.13/mg; `resting_hr` weak β+0.03 p=0.34; `respiration_avg_sleep`
REJECTED) is reproduced verbatim from
[`citalopram_phase_stratification.md` §2](../methodology/citalopram_phase_stratification.md)
(lines 84-89) and is **correct**.

**Framing (mostly clean, one fire).** The triage's central framing —
"this only routes, no verdict is moved" (§Authorship, lines 17-24) — is
honest and matches the findings doc's own discipline (Sec 5.7 bullet 8:
"number, not narrative"; locked `result.md` unchanged). The one framing
failure is the HA10 row's driver attribution (§2 line 82; §2.2 lines
104-108), detailed at Finding A below.

---

## 2. What fired and why

### Finding A — HA10 measurement-regime rationale is factually wrong (Layer 2: data provenance; Daza 2018 provenance-traceability) — **the load-bearing fire**

The triage's HA10 row (line 82) and §2.2 (lines 104-108) justify the
**needs-rerun (regime-controlled)** call by asserting:

> "**measurement-regime** (per-min BB only from 2024-06, on the split
> boundary) … sits on the 2024-06 per-minute-BB coverage cliff that
> coincides with the split boundary → the finding may be a
> data-availability artifact."

This is wrong on three independently-verifiable counts:

1. **HA10 does not use per-minute BB.** Per
   [`HA10/result.md`](../analyses/hypotheses/HA10-bb-overnight-recharge/result.md)
   line 214 ("3-anchor coarse proxy … captures peak only, not
   trajectory") and the single-pool findings (line 58: "max |z| (4d) of
   **bb_highest** (morning BB peak proxy via UDS)"), HA10's operand is the
   daily UDS `bb_highest` summary statistic, not a per-minute trace.

2. **Per-minute BB does not exist in the dump at all.**
   [`bb_overnight_gain_proxy.md` line 145](../methodology/bb_overnight_gain_proxy.md):
   "**No per-minute BB anywhere in the dump.**" HA10's result.md line 215
   confirms the per-minute version (H03b via H04b) is *unbuilt and
   unauthorised*. There is no "2024-06 per-minute-BB coverage cliff"
   because the channel referenced was never extracted.

3. **The split boundary is 2023-12-31, not 2024-06.**
   [`train_validate_split_fate.md` line 1, 13, 30](../methodology/train_validate_split_fate.md):
   the train/validate split is the 2023-12-31 date-based boundary. 2024-06
   is six months later and is the *citalopram buildup→consolidation*
   boundary (2024-06-20, `citalopram_phase_stratification.md` §3), an
   entirely different event. The triage conflates the citalopram-phase
   boundary with the train/validate split.

`bb_highest`/`bb_lowest` and their lagged variants span **2022-05-08 →
today at ~82% fill** ([`DATA_DICTIONARY.md` line 228](../DATA_DICTIONARY.md));
HA10's result.md reports **98.2% coverage** of valid morning peak across
the full ~1700-day window (line 221-224). There is no data-availability
cliff on HA10's actual operand at either the 2023-12-31 split or 2024-06.
(The one BB channel that *does* have a 2024-09-18 coverage onset is
`bb_overnight_gain`, which HA10 does not use — `DATA_DICTIONARY.md` line
229.)

**Magnitude of concern: high.** The needs-rerun call survives on a sound
alternative ground (see "What does not fire"), so the *routing* is not
wrong — but a downstream R14-v2 / R20 session reading "regime-controlled
re-run, gate on the 2024-06 per-minute-BB cliff" will scope a control
against a confound that does not exist, and may waste an authorisation
cycle chasing per-minute BB that isn't in the dump. The rationale must be
rewritten to the real ground.

### Finding B — H04 carries the *identical* (mis-stated) measurement-regime flag; the rerun/overlay asymmetry needs an honest basis (Layer 1: named confounders)

The triage flags H04 (line 85) with "**measurement-regime**/firmware"
and routes it overlay-only, while HA10 gets the same flag and
needs-rerun. But H04's operand is `bb_net_drain = drained_24h −
charged_24h` (single-pool findings line 86), built from the same UDS
daily charged/drained fields as `bb_highest`/`bb_lowest` — **full-window
coverage, no greater regime exposure than HA10**. So the
measurement-regime flag is equally mis-stated on both rows, and it cannot
be what distinguishes their actions.

The *defensible* basis for the asymmetry (which the triage does not
state cleanly): HA10's locked verdict is **validate-only SUPPORTED** —
the single first-and-only validate-era SUPPORTED test in the corpus
(result.md lines 5-6, 118) — and that headline collapses to +4.1pp
single-pool (perm p=0.4328, deeply null). A live SUPPORTED headline that
evaporates under single-pool is genuinely verdict-fragile and warrants a
documented re-look. H04 is REFUTED-both-eras with only a +13.3pp validate
*near-miss* that collapses to +0.5pp (frac_crash 0.038 — essentially no
signal); nothing there to re-run. **The asymmetry is correct; the stated
reason is not.** Recommend: re-ground both rows on verdict-fragility (HA10
has a live SUPPORTED headline to defend; H04 does not), and demote the
"measurement-regime" wording to, at most, the generic "Garmin BB
algorithm is opaque / firmware drift" caveat HA10's own result.md already
carries (line 218) — which the lagged baseline partially absorbs.

So to the prompt's sharpest question — *does H04 also warrant a rerun?* —
**no.** H04 is correctly overlay-only: REFUTED both eras, single-pool
+0.5pp, no live verdict at stake. HA10 is genuinely the only
verdict-fragility re-run in the BB family. The short list (HA10 + HA01c)
is right *on outcome*; only HA10's *rationale* is defective.

### Finding C — §3.7 detrend hook not explicitly cleared for the BB re-run scope (Layer 4: CONVENTIONS §3.7)

HA10's collapse is being read partly off a *raw* era-contrast (validate
+16.2pp vs train −20.5pp). The recovery-trajectory leakage hook
(CONVENTIONS §3.7) fires on raw pre-vs-post / cross-era contrasts on the
LC frame, and §3.7's empirical-validation note shows BB channels
(`bb_overnight_gain` × 2026-03-20) flipping from raw p<.001 to detrend
p=0.96. The single-pool re-anchor is a z-against-lagged-baseline design
(§3.7 explicitly does NOT apply to lagged-z), so the *cross-check* is
clean — but if the HA10 regime-controlled re-run reports any raw
era-overlay number, §3.7 fires. The triage should name §3.7 as a binding
hook on the HA10 re-run spec, not leave it implicit. Minor, but it is the
exact hook most likely to further null the HA10 "finding," strengthening
the triage's own "residual, not verdict-moving" thesis.

---

## 3. What does not fire (selective, with evidence)

- **The 4-rows-to-R20 "residual not verdict-moving" claim is sound**
  (§2.2 lines 111-115). H02b, HA07c, HA08c, HA11 all ride a CONFIRMED
  positive-β stress channel; single-pool already NOT-SUPPORTED
  (+3.5/+10.8/+13.4/+16.8pp, all p>0.05). The dose-correction logic is
  directionally correct: the CONFIRMED channels are positively
  dose-modulated (+0.43–0.57/mg) and the train era is the higher-dose-era
  for the stress channels, so subtracting `β·dose` removes signal from the
  train-supported arm and pushes the pooled discrimination *further toward
  null*, not toward support. Dose-correction cannot rescue a
  NOT-SUPPORTED single-pool verdict into SUPPORTED here. The R20 routing
  as ledger/residual work is defensible. **One nuance**: the claim "dose
  inflates the train signal" is asserted, not shown, for each of the four
  — it is mechanistically plausible and I did not find a counter-case, but
  it is an inference, not a computed result. Acceptable as a routing
  rationale given no verdict moves; flag only if R20 elevates it to a
  finding.

- **HA01c needs-rerun (single-pool) is correctly identified.** Confirmed
  NOT-RUN in the reanchor: findings.md §5 line 125 ("HA01c — NOT-RUN in
  cross-check … load-bearing WITHHELD pending v2 diag") and line 154
  ("genuinely uncovered remaining are H03 + HA01c"). The triage correctly
  excludes H03 from the short list (REFUTED both eras, low priority —
  findings.md line 121) rather than padding it.

- **Flag (c) = SELF on exactly HA-C3 + HA-C3p is correct.** Verified via
  [`interpretation/HA-C3.md`](../analyses/interpretation/HA-C3.md) lines
  17, 20: HA-C3 is REJECTED (wrong-direction) on the stress→felt *curve*,
  cluster C-stress-fatigue-shape, sister HA-C3p. These two *are* the
  shape finding (the `/not-a-straight-line` source), so they cannot be
  "shape-exposed" by an external shape finding — the flag self-refers,
  which is the right reading. Their named untested rival (R21 activity×
  stress interaction) is surfaced, not silently addressed. No other row
  plausibly carries (c). Clean.

- **C4b n=9 HONEST-CLOSE (§3) is stated honestly and is the defensible
  move at n<10.** Verified distinct from HA-C4c: C4b is the rest-stress
  low-motion *day-count* cell (n=9, site `claims[6]`); HA-C4c is the
  bout-level `bout_n_did_not_return` failure-to-return test
  (fully powered, cross-phase pool) — confirmed as separate clusters
  (HA-C4c = C-bout-substance, the substantive bout test;
  HA11-bout-redo = C-bout-framework, methodology validation —
  [`cluster-C-bout-framework.md`](../analyses/synthesis/cluster-C-bout-framework.md)
  §4.1). The decision is logged consistently at
  [`_open_inputs.md` OI-019](../methodology/_open_inputs.md) (line 40):
  honest-close, decline-a-verdict, accrual-only, no non-peeking expansion
  path. Declining a verdict below a pre-registered n≥10 floor is the
  correct call (manufacturing n≥10 by relaxing the low-motion gate would
  be exactly the post-hoc expansion the floor exists to prevent). The
  triage correctly frames the close as the user's call and reserves the
  fresh-session review to "confirm the close is stated honestly, not
  adjudicate whether to expand" (lines 180-181) — appropriate scoping.
  **Minor §3.6 note**: "n=9" is stated without the full
  `<n> <unit> per <scheme> in <file>` triple CONVENTIONS §3.6 wants. It is
  *day-level rest-stress-low-motion crash-cells* but the scheme/file are
  not named inline at §3. Add the predicate so the close is reproducible
  on the site.

- **§3.4 crash-drop hook**: not independently re-runnable from the triage
  (it routes, it does not compute correlations), and the single-pool
  substrate it leans on is episode-level (n=29 crash episodes, §3.6
  episode-discipline respected — findings.md line 4). No §3.4 fire on the
  triage itself.

---

## 4. What would strengthen this finding

1. **Rewrite the HA10 row + §2.2 HA10 bullet** to the real basis:
   *"Validate-only SUPPORTED headline (the corpus's only validate-era
   SUPPORTED test) collapses to +4.1pp / p=0.43 single-pool; the live
   SUPPORTED verdict is verdict-fragile and warrants a documented
   re-look. The opaque-BB-algorithm / firmware-drift caveat
   (`HA10/result.md` line 218) is the genuine measurement caveat, partly
   absorbed by the lagged baseline."* Delete the "per-min BB only from
   2024-06 / coverage cliff / split boundary" clause entirely — it
   conflates the 2024-06-20 citalopram-phase boundary with the
   2023-12-31 split and references a channel
   (`bb_overnight_gain_proxy.md` line 145: per-minute BB) that is not in
   the dump and is not HA10's operand.

2. **Harmonise the H04 row**: drop "measurement-regime/firmware" as a
   distinguishing flag (its operand has the same full-window UDS coverage
   as HA10's) and keep overlay-only on the honest ground (REFUTED both
   eras, single-pool +0.5pp).

3. **Name CONVENTIONS §3.7 as a binding hook on the HA10 re-run spec**
   (raw era-overlay numbers must carry `mw_p_after_linear_detrend`); cite
   the §3.7 empirical-validation note where a BB channel flipped to
   p=0.96 under detrend — it reinforces the triage's own "residual, not
   verdict-moving" thesis.

4. **Add the §3.6 count-triple at §3** for the n=9 cell
   (`<n> day-cells, scheme, file`) so the honest-close is reproducible.

---

## 5. Verdict + one-sentence reasoning

**REVISION RECOMMENDED.** The merged routing, the short re-run list
(HA10 + HA01c), the 4-row R20-residual call, the SELF flag, and the C4b
honest-close all survive independent verification — but the **HA10
needs-rerun rationale is a Layer-2 data-provenance fire** (per-minute BB
that doesn't exist in the dump; a split boundary off by six months; an
operand that actually has 98.2% full-window coverage), and the identical
mis-stated flag on H04 means the rerun/overlay asymmetry currently rests
on a wrong reason rather than the sound verdict-fragility reason that
actually justifies it. No verdict moves and the *outcomes* are right, so
this is revision, not rejection; correct the HA10/H04 rationale (and add
the §3.7 + §3.6 hooks) before the triage feeds R14-v2 / R20 scope.
