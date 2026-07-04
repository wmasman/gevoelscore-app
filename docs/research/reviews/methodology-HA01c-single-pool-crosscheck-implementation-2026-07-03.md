# Implementation review — HA01c single-pool cross-check `test.py`

**Reviewer role:** independent implementation reviewer (fresh session, cold read).
**Date:** 2026-07-03.
**Question:** does `HA01c-single-pool-crosscheck/test.py` faithfully implement its
`pre-registration.md`, and is it free of resampling / statistical / coding bugs, as
judged against the two framework MDs
(`permutation_null_block_length.md`, `train_validate_split_fate.md`), the original
locked `HA01c-effective-exertion-shock/test.py`, and the two scorecard cards
(`trust-panel-export.md`, `primary-verdict-statistics.md`)?

**Targets (NOT edited):**
- `docs/research/analyses/hypotheses/HA01c-single-pool-crosscheck/test.py`
- `docs/research/analyses/hypotheses/HA01c-single-pool-crosscheck/pre-registration.md`

**Verification performed.** `python -m py_compile test.py` passes (Python 3.14). The
real CSVs are gitignored and not materialised, so no real-data run is possible (this is
expected and not a finding). I re-ran a synthetic smoke suite: constructed fake
`crash_w` / `bg_w` / feature dicts and exercised `stationary_block_sample`,
`permutation_p`, `bootstrap_disc_ci`, `data_driven_block_len`, `usability`, and the
WR-vs-WOR null comparison directly. Results are cited inline below.

---

## Verdict

**The implementation is FAITHFUL to both framework MDs and to the pre-registration.**
Every mandated result-template output is present and correctly computed: point estimate
(`discrimination_pp`), stationary bootstrap 95% CI at E[L]=7 (`bootstrap_ci`),
permutation p at E[L]=7 (`permutation_null.p_value`), data-driven E[L]* with the
factor-of-2 flag (`block_length_companion`). The verdict rule (`SUPPORTED iff
permutation p < 0.05`) matches the single-pool bar under which "only HA07d cleared."
The usability block reproduces `trust-panel-export.md`'s conventions exactly (my
synthetic call with p_bg=0.77 returned specificity 23.0%, PPV 2.25%, lift 1.06x —
byte-for-byte the HA01b row). The path correction is real and correct.

Findings are **all Low / Informational.** None blocks the run; none biases the verdict
in a way that would flip it. Two items (F1, F4) are worth a one-line note in `result.md`
for full transparency. There are **no High or Medium correctness bugs.**

---

## Path-correction check (pre-reg §3 claim) — CONFIRMED

The pre-reg claims the original test reads a **stale** features path
(`analyses/activity-labels/output/...`) and that the corrected path is
`analyses/garmin_exploration/activity-labels/output/activity_features_daily.csv`.
Verified:
- Original `HA01c-effective-exertion-shock/test.py:39-40` sets
  `GARMIN_ROOT = HERE.parent.parent` then `"activity-labels"/"output"/...`. With that
  file at `hypotheses/HA01c-effective-exertion-shock/`, `HERE.parent.parent` is
  `analyses/`, so it resolves to `analyses/activity-labels/output/...` — a directory
  that **does not exist** in the tree.
- The corrected directory `analyses/garmin_exploration/activity-labels/output/` **does
  exist** and contains the emitting pipeline reports; the emitting script
  `11_compute_lagged_baseline.py` exists at
  `analyses/garmin_exploration/activity-labels/scripts/`.
- New `test.py:39-41` sets `ANALYSES_ROOT = HERE.parent.parent` (= `analyses/`, since
  this file sits one level deeper is **wrong to assume** — verified: this file is at
  `hypotheses/HA01c-single-pool-crosscheck/`, so `HERE.parent.parent` = `analyses/`),
  then `"garmin_exploration"/"activity-labels"/"output"/...`. This resolves to the
  correct, existing path. **The correction is right.**
- `activity_features_daily.csv` is confirmed gitignored (`git check-ignore` hit), so
  lock-precedes-data holds.

---

## Findings (severity-ranked)

### F1 — Permutation implemented as block-**bootstrap** (with replacement), not a without-replacement permutation. `test.py:143-182`, pre-reg §4.4, decision 6.3. Severity: LOW (acceptable stand-in; document it).

The MD text is *"permute crash/null labels in blocks drawn from the geometric E[L]=7
distribution."* A strict permutation is **without replacement** (each background label
used at most once across the pseudo-crash set). `stationary_block_sample`
(`test.py:143-159`) samples **with replacement** from a circular view of the pool, so a
given anchor label can appear multiple times in one pseudo-crash set. The pre-reg is
explicit and honest about this (§4.4: "implemented as a stationary-block bootstrap of
the anchor labels"; decision 6.3 flags it for confirm-at-review), so this is a
disclosed design choice, not a hidden deviation.

**Does the distinction bias p?** At this n-ratio, essentially no. The gap between
sampling with vs without replacement is the finite-population correction
`sqrt((N−n)/(N−1))` on the null SD. At n_clean≈26 drawn from N≈1300 background anchors
that is `sqrt(1274/1299) = 0.9903` — a **1% narrowing** of the true (WOR) null relative
to the WR bootstrap. My synthetic probe on iid Bernoulli(0.40) background (N=1300,
20 000 replicates) confirmed this directly:

| null | mean | sd | one-sided p at t_obs=0.60 |
|---|---|---|---|
| block-bootstrap WR, E[L]=7 (the script) | 0.4065 | 0.0952 | 0.0226 |
| iid without-replacement permutation | 0.4060 | 0.0955 | 0.0239 |

The WR bootstrap is *very slightly wider* (0.0952 vs 0.0955 — noise-level; theory says
WR is the wider one, WOR = WR × 0.9903). The p-values differ by ~0.001, and the WR
choice is **conservative** (marginally larger p → harder to declare SUPPORTED). So the
substitution does not bias the verdict toward SUPPORTED; if anything it is a hair
against it. **Fix:** none required. Optional: add one line to `result.md` stating "the
permutation null is realised as a stationary-block bootstrap; at n=26/N≈1300 the
with-vs-without-replacement difference is a 1% SD effect (fpc 0.990), conservative."

### F2 — E[L]* returns `None` when the ACF never crosses the white-noise band within lags 1–30 (e.g. a strong, slowly-decaying or strongly-periodic trigger series). `test.py:203-243`. Severity: LOW (correctness OK, but the flag silently goes `None`).

`data_driven_block_len` sets `e_l_star = None` if no lag in `range(1, min(31, n))` has
`|ACF| < 2/sqrt(N)`, and then `flag_factor_of_2` is also `None`
(`test.py:232-234`). My synthetic **period-7** trigger series exposed this: lag-7 ACF =
0.9949 and lags 1–6 sat at ≈−0.166 (band = 0.054), so **no lag crossed below the band**
and `e_l_star` came back `None` with `flag = None`. Activity-derived metrics carry
exactly this weekly cycle (the pre-reg §9 and the block-length MD §4 both say so), so a
real-data `None` is plausible. When that happens, the "factor-of-2 review flag" — the
one confirmatory guard the block-length MD mandates — evaluates to `None`, i.e. neither
raised nor cleared, and `main()` prints `E[L]* companion : None (...)` without drawing
attention to the fact that the estimator gave no answer. This is **not a bug** (the MD
calls E[L]* a transparent proxy and the band-crossing rule is a defensible one), but the
silent-`None` path means the mandated flag can be neither True nor False. My AR(1)-latent
synthetic (decaying ACF) correctly recovered E[L]*=6, flag=False, so the estimator works
when the ACF does decay through the band.

**Fix:** treat `e_l_star is None` as a flag-for-review condition, or at minimum have
`main()` print a distinct "E[L]* undetermined (ACF did not cross the band within 30
lags) — review block-length assumption" line rather than a bare `None`. Low severity
because the E[L]=7 default is the primary and E[L]* is only confirmatory.

### F3 — Background-pool anchors starting at `ANALYSIS_START` have lead-up windows that reach into the pre-stratum period; the original null used a `+10 day` floor. `test.py:132` vs original `test.py:120`. Severity: LOW (masked by the ~90-day lagged-baseline warmup; symmetric with the crash side).

`build_background_pool` iterates `d` from `ANALYSIS_START = 2022-09-03`
(`test.py:132`). `leadup_dates(ANALYSIS_START)` = `[2022-09-02, 09-01, 08-31, 08-30]`,
all **before** the Stratum-4 start. The original `build_null_sample` deliberately floored
its candidate dates at `ANALYSIS_START + 10 days` (`HA01c-effective-exertion-shock/
test.py:120`) precisely to keep lead-ups inside the window. The new script has **no such
floor** for the background pool.

In practice this is almost certainly inert: `effective_exertion_rank_lagged` uses a
~90-day lagged baseline, so ranks are absent (or `None`) for the earliest ~3 months of
the corpus; `window_stats` then fails the `>=3/4 valid` rule (`test.py:114`) and those
early anchors are dropped anyway. Critically, the **crash side uses the identical
`window_stats` validity gate** (`test.py:314-317`), so whatever early-corpus exclusion
happens is applied **symmetrically** to crash episodes and background anchors — the
pre-reg §4.1 even names this ("Episodes failing validity, early-corpus, inside the
~90-day lagged-baseline warmup, are dropped"). So there is no crash-vs-background
asymmetry, which is the property that would actually bias the discrimination. **Fix:**
none required for correctness. Optional robustness: floor the background loop at the same
point the crash validity effectively begins, or assert that no retained anchor has a
lead-up date `< ANALYSIS_START`, to make the boundary explicit rather than
warmup-dependent.

### F4 — Bootstrap CI resamples `p_crash` and `p_bg` on **independent** streams and differences them. `test.py:185-200`, pre-reg §4.5. Severity: LOW / INFORMATIONAL (correct and matches the pre-reg; noting the assumption).

`bootstrap_disc_ci` draws `cs` from `crash_w` and `bs` from `bg_w` independently, then
forms `disc* = mean(cs) − mean(bs)` (`test.py:192-194`). This is exactly what pre-reg
§4.5 specifies ("stationary-block resample the crash W-values → p_crash*; stationary-
block resample the background pool → p_bg*; disc* = p_crash* − p_bg*"). Independent
resampling of the two arms is the **correct** construction here: crash episodes and the
(crash-lead-up-excluded) background pool are disjoint sample sets, so there is no paired
structure to preserve — treating them as independent is right, and Var(disc*) =
Var(p_crash*) + Var(p_bg*) is the intended width. The pre-reg notes "the 26-episode arm
dominates the width," which my synthetic confirmed (crash arm n=26 vs background n=1300;
the CI half-width tracks the crash arm). **No bug.** Percentile CI construction: `discs`
sorted, `discs[int(0.025*N)]` / `discs[int(0.975*N)]` (`test.py:197-198`). At N=10 000
that is indices 250 / 9750 — both valid (max index 9999), no IndexError. Versus a strict
nearest-rank quantile the indices sit ~1 position high (a ~0.01% shift of the
distribution); this is a standard percentile-bootstrap convention and negligible at
B=10 000. The **same** `int(0.025*N)/int(0.975*N)` indexing is reused for
`permutation_null.null_ci95` (`test.py:180-181`), so the two are internally consistent.

### F5 — Single `rng` reused across `permutation_p` then `bootstrap_disc_ci`. `test.py:338-340`. Severity: INFORMATIONAL (reproducible; not an independence bug).

`main()` builds one `rng = random.Random(RANDOM_SEED)` and passes it to `permutation_p`
first, then `bootstrap_disc_ci` (`test.py:338-340`). This is deterministic — my
synthetic ran the same seeded sequence twice and got byte-identical p and CI. It is
**not** an independence problem: the two procedures estimate different quantities
(a null-tail p and a sampling-distribution CI), and consuming the stream in
`permutation_p` merely advances it before the bootstrap draws — the bootstrap still
receives well-distributed pseudo-random numbers. The only subtle consequence is
**coupling**: if `N_RESAMPLES` in `permutation_p` ever changed, the exact bootstrap CI
digits would shift because the stream offset changes. That is a reproducibility nuance,
not a correctness defect, and both use the same locked `N_RESAMPLES = 10000`. The
`p = (1 + ge) / (N_RESAMPLES + 1)` convention (`test.py:174`) is the correct
add-one/Monte-Carlo permutation p-value (Davison–Hinkley / Phipson–Smyth), guaranteeing
p > 0 and unbiasedness of the MC estimate. Confirmed on synthetics: p ≈ 0.47 when
t_obs = pool mean, p = 1e-4 (its floor) when t_obs ≫ pool mean. **Fix:** none;
optionally seed the two procedures with distinct derived seeds
(`Random(SEED)`, `Random(SEED+1)`) to decouple, but this is not required.

### F6 — Verdict rule matches the single-pool scorecard bar. `test.py:359`, pre-reg §5. Severity: NONE (conforms).

`verdict = "supported" if perm["p_value"] < ALPHA_PRIMARY else "not-supported"`
(`test.py:359`, `ALPHA_PRIMARY = 0.05`). This is exactly the bar the pre-reg §5 and
`trust-panel-export.md` describe — "of the seven scorecard signals, only HA07d cleared"
under permutation p < 0.05. The legacy 3-criterion bar is computed and stored but
explicitly labelled "NOT the verdict" (`test.py:356`), and the Bonferroni α=0.0125 is
reported as context only (`test.py:396`), matching pre-reg §5's "reported, not a second
gate." **Conforms.**

### F7 — Usability metrics reproduce `trust-panel-export.md` exactly. `test.py:246-259`, pre-reg §4.7. Severity: NONE (conforms).

`spec = 1 − p_bg`; `PPV = base·sens / (base·sens + (1−base)·(1−spec))`;
`lift = PPV / base` (`test.py:247-251`) — identical to the locked Bayes formula in
`specificity-tables-spec.md` as quoted in `trust-panel-export.md §1`. Tier rule "C if
PPV < 0.05" (`test.py:258`) matches the Tier-C convention. Base rates: single-pool
`BASE_RATE = 0.0211` (verified 29/1372 = 0.0211) and validate `0.0169`, both reported,
per §4.7. My synthetic call `usability(0.821, 0.77, 0.0211)` returned specificity 23.0%,
PPV 2.25%, lift 1.065x — an exact match to the HA01b trust-panel row (spec 23.0%, PPV
2.25%, lift 1.06x). **Conforms.**

### F8 — M3 overlay, n_clean floor, trim-to-n_out — all correct. Severity: NONE.

- **M3 overlay** (`test.py:262-276`): computes train (`d <= SPLIT_BOUNDARY`) and
  validate (`d > SPLIT_BOUNDARY`) discrimination against the **full-pool** `p_bg`
  passed in from `main()` (`test.py:393`). Using the single full-pool `p_bg` for both
  eras is the correct choice for a *descriptive* overlay whose stated question is "is the
  single-pool verdict robust to era partition?" (pre-reg §7) — it isolates the crash-arm
  era difference and does not silently introduce a per-era null. Correctly labelled
  "Number, not narrative. No per-era verdict, no per-era alpha," per
  `train_validate_split_fate.md §5.8`. **Correct.**
- **n_clean floor** (`test.py:325-331`, `N_CLEAN_FLOOR = 10`): writes an
  `inconclusive` result and returns before any resampling if `n_clean < 10`, matching
  pre-reg §4.1 ("Inconclusive if n_clean < 10"). **Correct.**
- **Trim-to-n_out** (`test.py:159`, `out[:n_out]`): the accumulate-then-stop loop never
  exceeds `n_out` (both the outer and inner `while` are guarded by `len(out) < n_out`),
  so `out[:n_out]` is a no-op slice; my synthetic ran 100 000 draws and every returned
  list had length exactly `n_out`. The final block being truncated to hit `n_out`
  exactly is standard Politis–Romano stationary-bootstrap behaviour, not a defect.
  **Correct.**

---

## Data-loading / trigger-logic parity with the original locked test

- **Crash starts**: both scripts group `label == "crash"` rows by `episode_id` and take
  `min(date)` per episode (`test.py:81-87` vs original `70-77`). **Identical.**
- **Per-episode trigger**: 4-day lead-up `[C−1..C−4]`, valid iff ≥3 of 4 days have a
  parseable rank, triggers iff `max_rank >= 0.75` (`test.py:99-121` vs original
  `89-109`). **Identical logic**, same threshold, same validity rule, same direction.
- **`parse_float`** null handling (`""`, `"None"`, non-numeric → `None`)
  (`test.py:90-96`): **identical.**

The only intended divergences are the framework swap (single pool, block-bootstrap null,
bootstrap CI, E[L]* companion) and the corrected features path — exactly what pre-reg §2
tabulates.

---

## Summary table

| # | finding | file:line | severity | flips verdict? |
|---|---|---|---|---|
| F1 | permutation is a WR block-bootstrap, not WOR permutation | `test.py:143-182` | Low | no (conservative, ~1% SD) |
| F2 | E[L]* + factor-of-2 flag go silently `None` if ACF never crosses band | `test.py:203-243` | Low | no |
| F3 | background pool has no `+10d` floor; lead-ups reach pre-stratum | `test.py:132` | Low | no (warmup-masked, symmetric) |
| F4 | independent-arm percentile disc CI; indices off nearest-rank by 1 | `test.py:185-200` | Low/Info | no |
| F5 | single rng reused across perm then bootstrap | `test.py:338-340` | Info | no (deterministic) |
| F6 | verdict rule = perm p < 0.05 | `test.py:359` | none | conforms |
| F7 | usability formulas + base rate | `test.py:246-259` | none | conforms |
| F8 | M3 overlay / n_clean floor / trim | `test.py:262-331,159` | none | conforms |

**Bottom line:** faithful implementation of both MDs and the pre-registration; no High
or Medium correctness bug; the four Low findings are transparency/robustness notes, and
F1 (the one a statistician would scrutinise) is disclosed in the pre-reg and shown to be
conservative at this sample size. The verdict the script will emit is trustworthy under
the locked framework. Recommend a one-line `result.md` note for F1 (WR-vs-WOR fpc) and
F2 (E[L]* undetermined handling); the rest need no change.

---

*Independent implementation review, 2026-07-03. Read-only on `test.py` and
`pre-registration.md`; no target file edited. Synthetic smoke suite only — real CSVs are
gitignored and not materialised, so a real-data run was not possible and its absence is
not a finding.*
