# Handoff back to the site: HA01c (exertion-shock precursor) — correct verdict + honest framing

**Status**: Stage-T (translation-to-audience) handoff from the research team
back to the site (`wiggers_research_story`). Gives the site team the
**authoritative HA01c verdict**, the **honest reader-facing framing**, and a
**reconciliation checklist** for the surfaces that may still tell the old
story. Drafted 2026-07-04 by Claude (Fable 5), producer-mode, for the
participant-researcher (repo owner). Everything below is aggregated /
date-free and privacy-safe.

Feeds: [`research-requests.md`](../../wiggers_research_story/site/docs/research-requests.md)
**R14** (single-pool primary verdict per signal), **R18** (hypothesis
re-test triage), **R19** (per-signal read along the recovery-phase axis),
and the **closed-hypothesis ledger** (`/workings`). Answers the repo owner's
two questions: *"have we documented this correctly?"* (§4) and *"does the
site tell this story correctly?"* (§3 — a checklist for you to verify, not a
fresh audit by research).

---

## 1. The authoritative HA01c verdict (what every site surface must match)

HA01c = **"a physically heavy day (heavy relative to my own recent normal)
in the 4 days before tends to precede a crash."** Its status, in one place:

| dimension | value |
|---|---|
| Single-pool discrimination | **+19.6 pp** (crashes 82.1% vs ordinary windows 62.5%) |
| Single-pool CI95 | [-19.6, +19.1] pp (**wide — crosses zero**; small-n) |
| Single-pool permutation p | **0.0290** (clears α=0.05; **fails** the Bonferroni ~0.0125) |
| Single-pool verdict | **SUPPORTED** (R14 re-anchor, committed `958bfe2`) |
| Load-bearing | **WITHHELD** — "SUPPORTED-with-stability-mixed" pending the v2 threshold-monotonicity diagnostic |
| Usability | **Tier C**: PPV ~**2.2%**, lift ~**1.06x** — **NOT card-shippable** |
| Scorecard placement | **OFF the seven-signal scorecard** |

**Critical distinction the site keeps getting wrong (see §3):** HA01c is the
**single-axis** exertion signal. The **composite** exertion signal on the
scorecard is **HA01b**, which is single-pool **NOT-SUPPORTED** (p=0.37,
+5.1 pp, Tier C). Both are true and not contradictory: *the composite fails
single-pool; the single isolated exertion axis passes, but only weakly and
without load-bearing status.* Keep the scorecard at seven (HA01b is the
exertion representative there); present HA01c as an **adjacent companion**,
not a scorecard row, and never as HA01b's success.

## 2. How to describe it honestly to a reader

The plain-language version, with three corrections the copy must respect:

- **It is physical exertion, not stress, not heart rate.** "Exertion" here =
  Garmin's brisk-movement minutes + logged workouts. Garmin "stress" (an
  HRV-derived score) and resting heart rate are **different signals tested as
  separate hypotheses** — do not fold them into this one.
- **It is crashes, not dips.** The target is the strict crash (feeling-score
  ≤ 3 for ≥ 2 consecutive days), not single-day dips.
- **"Heavy" is personal and relative.** A day counts as heavy+ if it lands in
  the participant's **own top ~25%** vs his prior 1–3 months — not an absolute
  step target.

**Suggested framing (honest, reader-facing):** *"Overdoing it physically does
tend to come before my crashes — about 82% of crashes had a heavy-exertion day
in the 4 days before, versus about 62% of ordinary stretches. That gap is
real, but it's a soft tendency, not a reliable trigger: heavy days are so
common that an alarm built on this would fire almost constantly, and when it
fired a crash would follow only about 2% of the time. It's the isolated
physical-exertion signal that showed this — the combined activity signal
didn't hold up, and stress and heart rate are separate stories."*

Do **not** ship: "the signal that got stronger", any crash-risk percentage, a
traffic-light/alert, or a "reliable warning" framing. Reflective-only.

## 3. Reconciliation checklist — surfaces to verify (this answers "does the site tell it right?")

These are surfaces flagged as **suspect in earlier passes** (2026-07-02/03);
research has **not** re-audited them now — **please verify current state and
reconcile**. The current Astro scorecard
(`closed-hypothesis-ledger.astro`) was correct as of the last look (HA01b
NOT-SUPPORTED, HA01c absent); confirm it still is.

**(a) Legacy narrative ledger — `story.md` closed-hypothesis table.**
The HA01c row was last seen in the retired two-era framing:
`| HA01c | Effective-exertion shock | Supported | Supported | Supported with stability concerns |`.
Proposed correction (Overall cell) + a one-line note:
> `| HA01c | Effective-exertion shock | Supported | Supported | Single-pool supported (p=0.029), not load-bearing |`
>
> *Note:* HA01c reproduces on the full single pool (permutation p=0.029, R14
> re-anchor) but its load-bearing status stays withheld pending the v2
> threshold-stability diagnostic, and its effect CI is wide (crosses zero). It
> sits off the seven-signal scorecard, where the exertion channel is the
> composite HA01b (single-pool not-supported).

**(b) Prototype contradiction — `site/prototypes/verdict-ledger.html`.**
A prototype line last read: *"Heavy exertion in the 4-day lead-up preceded 93%
of recent crashes — the signal that got stronger. Wiggers E · HA01b."* This
**contradicts** HA01b's single-pool NOT-SUPPORTED verdict. Correct it or
confirm the prototype is dead/unshipped before it can go live.

**(c) Prototype/index mention — `index.html`.** A prose mention of HA01c
(composite-vs-single-axis lineage) was seen; verify it doesn't imply a
load-bearing or "got stronger" reading.

## 4. Have we documented it correctly (research side)? — yes, with one cleanup done

For the repo owner's first question, the research-side record is **internally
consistent**:
- **Locked verdict**: [`analyses/hypotheses/HA01c-effective-exertion-shock/result.md`](analyses/hypotheses/HA01c-effective-exertion-shock/result.md)
  (SUPPORTED both eras at the locked bar) + the v2 diagnostic
  ([`.../HA01c-threshold-monotonicity-diagnostic-v2/result.md`](analyses/hypotheses/HA01c-threshold-monotonicity-diagnostic-v2/result.md),
  SUPPORTED-with-stability-mixed, not load-bearing).
- **Single-pool verdict**: [`analyses/descriptive/operationalisation_support/single_pool_reanchor/findings.md`](analyses/descriptive/operationalisation_support/single_pool_reanchor/findings.md)
  (SUPPORTED, p=0.0290). This is the authoritative single-pool source —
  **not** the seven-signal scorecard, which carries HA01b.
- **Cleanup done**: a redundant single-pool re-run drafted 2026-07-03 was
  **withdrawn and archived** (redundant with the R14 re-anchor + method-
  divergent) at
  [`analyses/hypotheses/_archive/HA01c-single-pool-crosscheck/WITHDRAWN.md`](analyses/hypotheses/_archive/HA01c-single-pool-crosscheck/WITHDRAWN.md).
  Do not run or cite it.
- **One genuinely-open research item (not a site concern)**: the data-driven
  E[L]* for the `effective_exertion` channel is uncharacterised (R14
  Limitations). It would refine HA01c's (already wide) bootstrap CI, **not**
  the verdict. Low priority; site ships nothing that depends on it.

## 5. The connection worth telling: HA01c is the *early-crash-type* signal

For R18/R19 and the `/workings/the-recovery-in-six-phases` page: HA01c is the
**early-era, sympathetic-overarousal** precursor (physical exertion → crash),
which is exactly the mechanism the "kind of crash changed" thesis assigns to
the early years. A **descriptive** per-phase read (R19) would likely show the
exertion-shock precursor concentrated in the pacing-era phases and fading in
the citalopram-modulated phase — honest corroboration that *the exertion
precursor belongs to the early crash type.* Two hard constraints for the site
if it tells this:
- The 29 crashes collapse to essentially **two populated cells** (phase 4b vs
  phase 5), and that boundary **is** the citalopram-onset date — so any
  phase-5 difference is **confounded with medication by construction**.
  Descriptive only; attribution stays in the **driver ledger**, never read off
  the phase axis.
- It stays a **described shape with wide error**, never a per-phase verdict,
  and it does **not** fix the Tier-C usability (slicing by phase makes per-cell
  precision worse).

## 6. Sources (research-side, for `/workings` and the ledger)

- Single-pool: [`analyses/descriptive/operationalisation_support/single_pool_reanchor/findings.md`](analyses/descriptive/operationalisation_support/single_pool_reanchor/findings.md)
  (HA01c row + Sec 3.x narrative).
- Locked verdict + stability: [`analyses/hypotheses/HA01c-effective-exertion-shock/`](analyses/hypotheses/HA01c-effective-exertion-shock/)
  and [`analyses/hypotheses/HA01c-threshold-monotonicity-diagnostic-v2/`](analyses/hypotheses/HA01c-threshold-monotonicity-diagnostic-v2/).
- Usability numbers (PPV/lift/Tier, base rate 2.11%): [`analyses/garmin_exploration/cards/trust-panel-export.md`](analyses/garmin_exploration/cards/trust-panel-export.md)
  (HA01b row) + [`analyses/garmin_exploration/cards/primary-verdict-statistics.md`](analyses/garmin_exploration/cards/primary-verdict-statistics.md).
- Cold reviews behind this handoff: [`reviews/hypothesis-HA01c-single-pool-crosscheck-2026-07-03.md`](reviews/hypothesis-HA01c-single-pool-crosscheck-2026-07-03.md),
  [`reviews/methodology-HA01c-single-pool-crosscheck-implementation-2026-07-03.md`](reviews/methodology-HA01c-single-pool-crosscheck-implementation-2026-07-03.md).
- Phase axis (for §5): [`methodology/lc_recovery_phase_axis.md`](methodology/lc_recovery_phase_axis.md).
