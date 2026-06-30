# Trust-panel export (R2) — per-signal usability metrics, single-pool primary

**Producer-mode export artefact.** Assembled 2026-06-30 for Wiggers-site request R2.
Derivative computation over already-locked single-pool numbers — **no new null draws,
no new hypothesis tests, no re-lock**. Read-only on all source results.

**What this is.** For each autonomic/stress/exertion scorecard signal: sensitivity
(recall), specificity, PPV (positive predictive value), lift, and base rate — with
95% CIs — framed as **how usable the signal is in daily life**, NOT as evidence the
underlying relationship is real. The reality question is owned by the locked HA
verdicts and is not restated, relabelled, or re-decided here.

**Primary source.** `docs/research/analyses/descriptive/operationalisation_support/single_pool_reanchor/findings.md:14-24`
(per-HA single-pool `frac_crash` = sensitivity, `frac_null` = 1−specificity, disc_pp,
CI95, perm-p, n). Single pool = full Stratum 4, 2022-09-03 → 2026-06-05, n_days=1372,
n_crash_episodes=29 (`findings.md:170`).

---

## 0. Framing rules this export obeys (do not strip on re-use)

1. **Single-pool primary.** Every headline number below is the single-pool number
   from `findings.md`. The retired train/validate era split appears as a one-line
   **overlay only** (§4) — never as a per-era verdict.
2. **§3.10 layer discipline.** PPV / sensitivity / specificity / lift are
   **actionability-layer usability measures, base-rate framed** — FORBIDDEN at the
   HA-test level per `docs/research/methodology/_plan_results_analysis_layer.md:448-456`
   and `personal_hypotheses.md §32`. They answer *"how usable in life"*, base-rate
   framed, in plain language ("right N of M when it fires"). They are **not** evidence
   the relationship is real, and this export does **not** restate any HA verdict.
3. **n=29 honesty.** CIs are wide at this n and are reported in full, never hidden.
   PPV at a ~1.7–2.1% base rate is **low even for a good signal** — see the project
   precedent at `docs/research/RESEARCH-REPORT.md §5.2` (~4% PPV → "wrong 24 times out
   of 25"). This holds here: the best signal (HA07d) lands at ~2.7% PPV.

**Verdict honesty (single-pool).** Of the 7 scorecard signals, **only HA07d is
single-pool SUPPORTED**; the other six are single-pool **NOT-SUPPORTED**
(`findings.md:15-24`). The trust panel shows this plainly. A usable PPV number on a
NOT-SUPPORTED signal does **not** rehabilitate the signal — usability and reality are
different axes (§3.10). A NOT-SUPPORTED signal with a non-trivial recall is still a
signal the research could not show is real; its trust chip must read as such.

---

## 1. Derivation method (assembly, not new computation)

Per-signal inputs taken verbatim from `findings.md:15-24`:

- **sensitivity (recall)** = `frac_crash` = P(signal fired in the lead-up window | a
  crash followed). 95% CI = Wilson score on `round(frac_crash × n_crash) / n_crash`.
- **specificity** = `1 − frac_null` = P(signal stayed quiet | a random non-crash day).
  95% CI = Wilson score on `round(specificity × n_null) / n_null`.
- **base rate** = P(crash on a random day). **Single-pool: 29/1372 = 2.11%**
  (`findings.md:170`). Overlay anchor: **validate-era 1.69%**
  (`card-b2-validate-specificity.md:10`), the most conservative recent rate.
- **PPV (precision / posterior per fire)** by Bayes, the project's locked formula at
  `specificity-tables-spec.md:54-59`:
  `PPV = (recall × base) / (recall × base + nullfire × (1 − base))`, where
  `nullfire = frac_null`.
- **lift** = PPV / base (`specificity-tables-spec.md:64`).
- **PPV 95% band** = corner propagation: best = high-sens × low-nullfire bound,
  worst = low-sens × high-nullfire bound (both Wilson). This is an assembly
  approximation, flagged in §6 open questions.

CI/Fisher style matches the retired primary-verdict card
(`primary-verdict-statistics.md:17-33`) — Wilson on the proportions, Wald on the
discrimination — but the **numbers** here are single-pool, not that card's per-era
numbers (that card is the RETIRED train/validate version; used for method style only).

---

## 2. Full trust table — single-pool, with CIs (research layer)

Base rate, single pool = **2.11%** (29/1372). PPV and lift shown at single-pool base
and, in brackets, at the conservative validate-era base of 1.69%.

| signal | construct | single-pool verdict | sensitivity (recall) 95% CI | specificity 95% CI | PPV @2.11% [@1.69%] | PPV 95% band (@2.11%) | lift @2.11% [@1.69%] | tier |
|---|---|---|---|---|---|---|---|---|
| **HA07d** | sleep stress variability (stdev delta, bidir) | **SUPPORTED** | 88.0% [70–96]% | 31.7% [26–39]% | **2.71%** [2.17%] | [1.99–3.27]% | **1.28×** [1.28×] | C |
| **HA11** | within-day U-dip count (elevated) | NOT-SUPPORTED | 58.3% [39–76]% | 58.5% [51–66]% | 2.94% [2.36%] | [1.68–4.53]% | 1.39× [1.40×] | C |
| **HA06b** | RHR z-score (bidir) | NOT-SUPPORTED | 61.5% [43–78]% | 45.1% [38–52]% | 2.36% [1.89%] | [1.47–3.38]% | 1.12× [1.12×] | C |
| **HA07c** | sleep stress mean delta (elevated) | NOT-SUPPORTED | 60.0% [41–77]% | 50.8% [44–58]% | 2.57% [2.05%] | [1.54–3.77]% | 1.21× [1.22×] | C |
| **HA01b** | exertion-class lead-up (heavy/very-heavy) | NOT-SUPPORTED | 82.1% [64–92]% | 23.0% [18–29]% | 2.25% [1.80%] | [1.66–2.74]% | 1.06× [1.07×] | C |
| **HA10** | morning BB peak z (bidir) | NOT-SUPPORTED | 76.9% [58–89]% | 27.1% [21–34]% | 2.23% [1.78%] | [1.57–2.82]% | 1.05× [1.05×] | C |
| **H02b** | per-minute stress-spike count (3d) | NOT-SUPPORTED | 50.0% [32–68]% | 53.5% [47–60]% | 2.27% [1.81%] | [1.28–3.56]% | 1.07× [1.07×] | C |

Source rows: HA07d `findings.md:46`; HA11 `findings.md:67`; HA06b `findings.md:95`;
HA07c `findings.md:39`; HA01b `findings.md:32`; HA10 `findings.md:60`; H02b
`findings.md:81`. Tier per `specificity-tables-spec.md:124-128` (Tier C = lift < 2×
OR precision < 5%). **Every scorecard signal is Tier C at the single-pool base rate.**

**Headline.** At the ~1.7–2.1% crash base rate, the best scorecard signal (HA07d, the
only single-pool SUPPORTED one) has a PPV of about **2.7%** and a lift of **1.28×**.
In plain frequency: when HA07d fires, a crash follows roughly **1 time in 37** — it is
**wrong about 36 times out of 37**. The lift over knowing nothing is ~1.3×. Every other
signal sits at a lower or equal lift, all below the 2× Tier-C/Tier-B boundary. This is
the same story RESEARCH-REPORT §5.2 told for H02b's train window (~4% PPV, "wrong 24
out of 25"), now confirmed on the single pool for the whole scorecard.

---

## 3. Plain-language frame per §3.10 (field-guide chips)

Per `_plan_results_analysis_layer.md:419-446`: number **plus** what-it-means-in-everyday-
frequencies. Each chip is base-rate framed and says "right N of M when it fires." None
of these chips claims the relationship is real — they describe usability of a signal
whose reality status is the locked HA verdict, shown alongside.

> **Reading rule for the chips.** "Fires" = the signal showed its trigger in the days
> before a day. "Right N of M when it fires" = of M days where it fired, a crash
> actually followed on N. Higher recall just means it fires on *more* of the real crash
> lead-ups — it does **not** make the fire trustworthy when the base rate is ~1 in 50.

| signal | chip (plain language) | reality status to show with chip |
|---|---|---|
| **HA07d** | "Catches about 9 in 10 crash lead-ups, but fires on ~2 of every 3 ordinary days too. When it fires, a crash follows roughly **1 time in 37**. Right ~1 of 37 when it fires; wrong the other ~36." | single-pool SUPPORTED |
| **HA11** | "Fires on a bit over half of crash lead-ups and a bit over half of ordinary days. When it fires, a crash follows roughly **1 time in 34**. Right ~1 of 34 when it fires." | single-pool NOT-SUPPORTED |
| **HA06b** | "Fires on ~6 of 10 crash lead-ups and ~5–6 of 10 ordinary days. When it fires, a crash follows roughly **1 time in 42**." | single-pool NOT-SUPPORTED |
| **HA07c** | "Fires on ~6 of 10 crash lead-ups and ~half of ordinary days. When it fires, a crash follows roughly **1 time in 39**." | single-pool NOT-SUPPORTED |
| **HA01b** | "Catches ~8 of 10 crash lead-ups but also fires on ~3 of every 4 ordinary days. When it fires, a crash follows roughly **1 time in 44**." | single-pool NOT-SUPPORTED |
| **HA10** | "Catches ~8 of 10 crash lead-ups but fires on ~7 of 10 ordinary days. When it fires, a crash follows roughly **1 time in 45**." | single-pool NOT-SUPPORTED |
| **H02b** | "Fires on ~half of crash lead-ups and ~half of ordinary days. When it fires, a crash follows roughly **1 time in 44**." | single-pool NOT-SUPPORTED |

**Field-guide framing line (verbatim-ready):** *"None of these signals is a crash
alarm. Even the strongest one is wrong ~36 times for every 1 time it's right, because
crashes are rare (~1 in 50 days). They describe what tended to show up before crashes
in retrospect; they are not a forecast."* (anchored on RESEARCH-REPORT §5.2 style.)

---

## 4. Era overlay (number, not narrative)

Per `findings.md:5` and `_plan_results_analysis_layer.md` train/validate retirement,
the era split ships as a **single number, never a per-era verdict.** For continuity
with the retired cards only:

- HA07d retrospective precision was **3.73%** (train, base 2.89%) and **2.24%**
  (validate, base 1.69%) — `card-b-train-specificity.md:18`,
  `card-b2-validate-specificity.md:16`. Single-pool consolidates these to **2.71%**
  at the single-pool base.
- No per-era SUPPORTED/REFUTED claim is exported. The era contrast exists in the
  retired cards for method lineage; it is not a trust-panel verdict.

---

## 5. Proposed export shape for the Wiggers site

Two surfaces, one source table:

1. **Field guide (patient-facing) — translated chips.** One chip per signal from §3,
   each paired with its reality status word (SUPPORTED / NOT-SUPPORTED) and the standing
   framing line. No percentages-as-risk, no traffic lights, no alerting
   (`specificity-tables-spec.md:133-147` no-go list). Chips are reflective/retrospective
   only.
2. **Research layer — full table.** §2 table verbatim, with the §1 derivation note and
   the §6 open-questions list, so a peer reader can see the CIs, the base-rate framing,
   and the assembly-vs-fresh-computation boundary.

**Ordering.** Lead with HA07d (only SUPPORTED), then the NOT-SUPPORTED six. Do **not**
rank the NOT-SUPPORTED signals by PPV as if PPV were a quality score — PPV here is a
usability number on signals the research could not show are real. Sort them by construct
or keep the §2 order; annotate each with NOT-SUPPORTED prominently.

---

## 6. Privacy statement

This export is **aggregated and contains no dated values, no per-day records, and no
raw physiological readings.** Every number is a corpus-level proportion (a recall, a
specificity, a base rate) or an arithmetic function of those proportions (PPV, lift)
over the full Stratum 4 pool. The only counts disclosed are the cohort-level n's
(n_days=1372, n_crash_episodes=29) and per-signal denominators (n_crash 24–28,
n_null 171–200). No date, no timestamp, no individual crash episode, and no individual
signal reading is exported. Consistent with the presence-conditioned / no-prevalence-
claim discipline (`research_line_limitations.md`), no chip asserts a population
prevalence — base rate here is this subject's own crash frequency, not a claim about
any population.

---

## 7. Open questions — what needs FRESH computation (not assembly)

Everything in §2 is **assembled** from `findings.md` + the Bayes formula. The following
would require a fresh run and should NOT be faked by assembly:

1. **Exact PPV / lift confidence intervals.** §2's PPV band is a Wilson-corner
   approximation (best = high-sens × low-nullfire, worst = low-sens × high-nullfire).
   A defensible PPV CI needs a proper method (bootstrap over the joint
   sensitivity/nullfire sampling, or a delta-method / logit-interval on the posterior).
   **Fresh computation required** if the site publishes a PPV CI rather than a point
   estimate. Until then publish PPV as a point estimate + the approximate band, labelled
   approximate.
2. **Single-pool specificity Wilson denominators.** Specificity CIs use the null-sample
   n (171–200) as the denominator. Those nulls are the 200 random-window reference set
   inherited from the legacy HA frames (`findings.md:162`), not the full 1372-day pool.
   The point estimate (1−frac_null) is the project's standard, but a specificity CI on
   the *whole* day pool would need a fresh count of signal-fire days across all 1372
   days. **Fresh computation required** for a population-grounded specificity CI.
3. **NPV, F1, lead-time, reliability.** §3.10 lists these as optional-but-encouraged at
   tier-2+. They are **not** in `findings.md` and cannot be assembled from it. NPV needs
   the quiet-day crash rate; lead-time and reliability need per-fire timing and
   test-retest runs that do not exist in the single-pool table. **Fresh computation
   required** for any of these; flag as open in the export, do not improvise.
4. **Base-rate sensitivity arm at single pool.** The retired cards report PPV at
   0.5×/1×/2× base (`card-b-train-specificity.md:38-46`). §2 gives single-pool (2.11%)
   and validate (1.69%). A full 0.5×/1×/2× single-pool arm is cheap to add but is a
   **fresh small computation**, not present in `findings.md`.

None of these block the v1 export: the field-guide chips and the research table run on
assembled point estimates with the wide-CI honesty note. Items 1–4 are the acquire-tasks
if the site later wants published CIs on the derived metrics or the optional §3.10
measures.

---

## 8. Source citations (file:line)

- Single-pool per-signal numbers + n's + base: `findings.md:14-24, 32, 39, 46, 60, 67, 81, 95, 170`.
- §3.10 actionability-layer discipline + plain-language frame + HA-level prohibition:
  `_plan_results_analysis_layer.md:407-468`.
- Bayes PPV / lift / tier formulas: `specificity-tables-spec.md:54-64, 124-128`.
- §5.2 PPV precedent ("wrong 24 of 25"): `_plan_results_analysis_layer.md:412-417`
  (quoting `RESEARCH-REPORT.md §5.2`).
- Retired-era specificity (overlay only): `card-b-train-specificity.md:16-22`,
  `card-b2-validate-specificity.md:16-17`.
- CI/Fisher method style (RETIRED per-era numbers, style not value):
  `primary-verdict-statistics.md:17-39`.

*End of export. Producer-mode, read-only on sources, no re-lock, no audit run, no git.*
