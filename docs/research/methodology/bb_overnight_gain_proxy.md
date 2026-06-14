# `bb_overnight_gain_proxy` — definition and validation

*Producer-mode methodology MD. Drafted 2026-06-14 (Session D). Locks the definition + validation evidence behind the `bb_overnight_gain_proxy`, `bb_overnight_gain_best`, and `bb_overnight_gain_source` columns added to `per_day_master.csv` by [`pipeline/01_extract/garmin_uds_extras.py`](../pipeline/01_extract/garmin_uds_extras.py). Sister doc to [`hrv_proxy_via_stress.md`](hrv_proxy_via_stress.md) and [`intervention_effects_descriptive.md` §2b](intervention_effects_descriptive.md#2b-channel-coverage-gap--bb_overnight_gain).*

---

## 1. What this MD asks, and what it does not

**The question.** The truth channel `bb_overnight_gain` (= `bb_sleep_end_value - bb_sleep_start_value`) is structurally absent for ~64% of the LC corpus (1162 / 1755 days) because Garmin's UDS export rolled the underlying stats out in two stages on this user's FR245: `SLEEPSTART` first emitted 2024-07-08, `SLEEPEND` first emitted 2024-09-18 (verified 2026-06-14 Session D by direct inspection of the GDPR dump; documented in [`intervention_effects_descriptive.md` §2b](intervention_effects_descriptive.md#2b-channel-coverage-gap--bb_overnight_gain) and on the `bb_overnight_gain` row of [`../DATA_DICTIONARY.md`](../DATA_DICTIONARY.md)). All analyses that touch BB-overnight-recovery dynamics carry this absence: the 2024-06-20 Citalopram buildup→consolidation boundary has `n_pre = 0, n_post = 0` on the truth channel, and earlier boundaries are simply blank.

The question this MD answers: **can `HIGHEST - SLEEPSTART` substitute for `SLEEPEND - SLEEPSTART` on days where truth is absent but proxy inputs exist, and what disciplines must consumers apply when they do?**

**What this MD does NOT do.** It does NOT recompute or replace any existing hypothesis-test finding that was conducted on the truth channel. It does NOT advocate using the proxy in confirmatory tests of the Wiggers D2 claim — those tests should report on the truth channel and treat the proxy as a coverage-extension sensitivity, not a primary. It does NOT propose a calibration / bias correction; the proxy is stored raw per the discipline rule in §4.

---

## 2. The proxy, in code

```
proxy = bb_highest - bb_sleep_start_value
```

Both inputs are present in `bodyBattery.bodyBatteryStatList` in every UDS file from `2024-07-08` onward (the `SLEEPSTART` rollout date on this FR245). `HIGHEST` is also present in 1116 / 1129 pre-2024-07-08 days (≈99%), but the proxy is bound by `SLEEPSTART` availability, not `HIGHEST` availability.

The fused channel `bb_overnight_gain_best` returns truth where present, proxy otherwise; `bb_overnight_gain_source` carries the provenance flag (`"truth"`, `"proxy"`, or `""`). Implementation: [`pipeline/01_extract/garmin_uds_extras.py`](../pipeline/01_extract/garmin_uds_extras.py).

---

## 3. The four-input reasoning (per [CONVENTIONS §2.2](../CONVENTIONS.md#22-methodology-md-before-locking-a-major-choice))

### 3.1 Best-practices standards — surrogate-validation literature

A surrogate channel substituted for a missing primary channel is canonically validated against three criteria (e.g. Prentice 1989 *Stat Med* surrogate-endpoint criteria, adapted from clinical-trial endpoint substitution to n-of-1 within-subject measurement substitution):

1. **Concordance** — does the surrogate track the primary in direction and magnitude on the subset where both exist?
2. **Bias** — does the surrogate systematically over- or under-estimate the primary?
3. **Coverage gain** — is the surrogate's marginal availability worth the validation overhead? (Surrogate-with-zero-extra-coverage is dead weight.)

All three are reported in §5 below. Standard regression-based concordance (Pearson r) is reported as the primary; residual distribution (mean, median, MAE, RMSE, within-tolerance share) addresses bias and tail behaviour.

The within-subject timing component — does HIGHEST actually sit near wake, when SLEEPEND would sit? — is reported separately because it is the load-bearing assumption: a surrogate that correlates with truth via a different mechanism (e.g. HIGHEST = afternoon nap peak rather than morning wake peak) would invalidate the substitution semantically even if r were high.

### 3.2 Established literature — the only directly-relevant anchor

There is no peer-reviewed external validation of "Garmin HIGHEST as a proxy for SLEEPEND". The Garmin Body Battery algorithm is proprietary (Firstbeat Technologies, acquired by Garmin 2020) and the UDS API is undocumented. The closest established literature is the Firstbeat 2014 white paper on the 24-h stress / recovery algorithm (cited in [`hrv_proxy_via_stress.md` §2](hrv_proxy_via_stress.md#2-how-garmin-stress-is-derived) for the sister proxy), which establishes that BB is a windowed composite of HRV inputs and that recovery accumulates during sleep when motion + HR + respiration are at baseline. The implication for HIGHEST: on a worn-through-night watch, BB rises monotonically across sleep and reaches its daily peak at or shortly after wake. The validation in §5 is the only direct test on this corpus and is necessarily n-of-1.

External Garmin support / community sources confirm the existence of two-stage UDS schema changes during 2024 (Body Battery / Sleep Coach / Morning Report rollouts to older watches) but do not document the specific `SLEEPSTART` / `SLEEPEND` add-dates. The schema dates in §1 are observed in this user's dump, not external claims.

### 3.3 Our own vision on tradeoffs

Three tradeoffs were deliberated; the chosen path is named first in each pair.

**Separate columns + audit flag (chosen) vs unified silent fusion.** Keeping `bb_overnight_gain`, `bb_overnight_gain_proxy`, `bb_overnight_gain_best`, and `bb_overnight_gain_source` as four distinct channels — versus replacing `bb_overnight_gain` in-place with the fused channel — costs +3 columns in the master but preserves the audit trail: any consumer can ask "did the result depend on proxy rows?" and answer it from the data. Per [CONVENTIONS §4.1](../CONVENTIONS.md#41-no-interpretive-marks-on-raw-or-descriptive-layers) (no interpretive marks on raw / descriptive layers), the proxy is a derived interpretive value, and silently merging it into a "raw"-named column would violate that rule. The audit-flag column makes the choice reversible if the proxy turns out problematic on a specific analysis.

**Raw proxy (chosen) vs +0.63 BB bias correction.** §5's mean residual of +0.63 BB units is non-zero but below noise (median = 0, MAE = 0.63, RMSE = 2.05). Applying a calibration constant would (a) tie every consumer to a 593-day calibration sample, which itself can drift if Garmin changes the underlying algorithm or schema, and (b) introduce a "this column has a hidden adjustment factor" footnote at every use-site. Keeping the proxy as a pure subtraction of two raw UDS values preserves traceability and accepts the +0.63 bias as a documented caveat consumers acknowledge per-analysis.

**Coverage extension as sensitivity (chosen) vs coverage extension as primary.** For confirmatory tests of Wiggers D2 (BB overnight gain → next-day gevoelscore), the proxy should be reported as a coverage-extension sensitivity column, not as the primary outcome. Reason: the truth channel is what the Wiggers claim references; substituting silently would mute the methodological signal that the test is operating partially on a proxy. For exploratory / descriptive use (e.g. distribution-shape characterisation, plotting), `bb_overnight_gain_best` is fine as the primary input — the audit flag provides the disclosure.

### 3.4 Our research limitations + objectives

The corpus is n=1, one FR245 worn continuously 2021-08-16 → today (verified 2026-06-14 by direct inspection of `file_id` messages in all 21,219 FIT files: single serial 3377851255, single product `fr245`). The validation in §5 is the only available calibration; cross-subject generalisation is not in scope. The 593-day validation window is the entire post-2024-09-18 truth-availability stretch as of 2026-06-14 — there is no held-out segment to validate against.

This is a within-subject measurement-substitution decision. The analytical objective the proxy serves is preserving the 71 days of post-window coverage at the 2024-06-20 boundary (and any other analyses that want continuous BB-overnight dynamics across the 2024-07-08 → 2024-09-17 bridge) without contaminating confirmatory Wiggers tests. The discipline rules in §6 are what enforce that separation.

---

## 4. Discipline rules for consumers

These are binding for any analysis script or result MD that touches `bb_overnight_gain_best` or `bb_overnight_gain_proxy`.

1. **Provenance disclosure.** Any result that aggregates `bb_overnight_gain_best` (mean, median, distribution, regression coefficient, CCF) must report the share of rows with `bb_overnight_gain_source == "proxy"` alongside the headline number. A finding driven by the 71 bridge days is a different epistemic claim from one driven by 593 truth days.

2. **Truth-first for confirmatory.** Pre-registered Wiggers D2 confirmatory tests report on `bb_overnight_gain` as the primary outcome. `bb_overnight_gain_best` (or `bb_overnight_gain_proxy`) is allowed as a coverage-extension sensitivity, reported in a separate row of the same summary CSV — not in place of the primary.

3. **Saturation handling.** When `bb_highest == 100` the proxy floors. On the validation sample 29 / 593 days were saturated. The bias on those days is small (mean residual +0.10) but the proxy cannot distinguish "actually 100" from "would-have-been-104" if Garmin's cap weren't binding. Sensitivity-conscious analyses can flag and exclude `bb_highest == 100` rows; the audit-flag column does not encode this on its own.

4. **Hard floor on the proxy's date range.** The proxy is NaN before 2024-07-08 by construction (no `SLEEPSTART` upstream). Do not impute, extrapolate, or otherwise extend it backward. Pre-2024-07-08 boundary analyses on this channel are blocked, not proxy-rescuable. The proxy buys 74 days total across the LC corpus (71 in the 2024-07-08 → 2024-09-17 bridge + 3 post-rollout SLEEPEND-failure nights; see §5.4), not the full pre-history.

5. **Per-analysis cross-reference.** Any result MD that uses the proxy must cite this methodology MD in its caveats section, and any future change to the proxy definition (e.g. a calibration constant, a saturation filter) must update both this MD and the implementation in [`pipeline/01_extract/garmin_uds_extras.py`](../pipeline/01_extract/garmin_uds_extras.py) in the same commit.

---

## 5. Validation — descriptive characterisation on n=593 truth-available days

Run 2026-06-14 Session D. Sample: all dates from 2024-09-18 onward where `SLEEPSTART`, `SLEEPEND`, and `HIGHEST` are all present in `bodyBattery.bodyBatteryStatList`. n = 593 total; 29 saturated (`bb_highest == 100` OR `bb_sleep_end_value == 100`); 564 clean.

### 5.1 Concordance (clean subset, n=564)

| statistic | value |
|---|---|
| Pearson r(`proxy`, `truth`) | **0.9886** |
| mean residual = mean(proxy − truth) | **+0.63** BB units |
| median residual | **0** BB units |
| MAE | 0.63 BB units |
| RMSE | 2.05 BB units |
| share with `|residual| ≤ 5` | **550 / 564 = 97.5%** |

The mean residual of +0.63 is non-zero but below the unit resolution of the channel (BB is integer 0–100); the median of exactly 0 indicates no systematic offset in typical cases. The 14 / 564 days outside ±5 BB units cluster at high overnight-gain values where the proxy slightly overshoots — consistent with HIGHEST occasionally landing post-wake on a recovery surge.

### 5.2 Timing of `HIGHEST` vs `SLEEPEND` (clean subset, n=564)

| statistic | value |
|---|---|
| median `HIGHEST` timestamp | 06:00 local |
| 10th–90th percentile | 05:00–07:00 local |
| share where `HIGHEST` is within ±2 h of `SLEEPEND` | **543 / 564 = 96.3%** |
| 7-day rolling jitter | within minutes |

`HIGHEST` is the post-sleep BB peak in 96.3% of validated nights, not a randomly-distributed daytime peak. This confirms the load-bearing assumption named in §3.1: the proxy substitutes for `SLEEPEND` via the same physiological mechanism (BB rises across sleep, peaks at or shortly after wake), not via spurious correlation.

### 5.3 Saturation sub-analysis (n=29 saturated days)

On saturated days the proxy still tracks truth: mean residual +0.10, median 0, range 0–2 BB units. The cap floors both channels symmetrically on this sample, so the proxy doesn't accumulate bias at the high end. The risk that the cap masks divergence on extreme-recovery nights cannot be excluded from this sample — but the validation sample includes 29 days of caps without visible degradation, which bounds the worst case.

### 5.4 Coverage gain (full LC corpus, n=1755)

Run 2026-06-14 Session D, materialised in `per_day_master.csv`:

| channel | non-null days | first non-null date |
|---|---|---|
| `bb_overnight_gain` (truth) | 593 / 1755 = 33.8% | 2024-09-18 |
| `bb_overnight_gain_proxy` | 667 / 1755 = 38.0% | 2024-07-08 |
| `bb_overnight_gain_best` | 667 / 1755 = 38.0% | 2024-07-08 |
| `bb_overnight_gain_source == "proxy"` rows in `_best` | 74 / 1755 = 4.2% | 2024-07-08 → 2025-12-11 |

The 74 proxy-source rows decompose into:

- **71 bridge rows** (2024-07-08 → 2024-09-17) — the full SLEEPSTART-only window before SLEEPEND rollout. These are the entire pre-2024-09-18 gain.
- **3 post-rollout SLEEPEND-failure rows** (2025-04-26, 2025-08-24, 2025-12-11) — nights where Garmin emitted SLEEPSTART and HIGHEST but did not compute SLEEPEND. Sparse (3 / 593 ≈ 0.5% of post-rollout days) but meaningful for any analysis whose window happens to include these specific dates.

Earlier years (2021, 2022, 2023, early 2024) gain zero because `SLEEPSTART` itself is absent — see [`intervention_effects_descriptive.md` §2b](intervention_effects_descriptive.md#2b-channel-coverage-gap--bb_overnight_gain) for the per-boundary breakdown. Net 4.2 percentage-point coverage gain over the truth channel.

---

## 6. Caveats and limits

1. **Single-watch, single-firmware-family validation.** The validation in §5 is on the same FR245 across the entire 593-day post-2024-09-18 window. If the user adds a second watch (different sensor generation), the proxy's r and residual distribution may differ. Re-run §5 before extending the proxy to multi-device data.

2. **No external HRV-style cross-validation.** Unlike `stress_mean_sleep` (where Rosenbach 2025 provides external HRV-stress correlation in 60 subjects), there is no external study of HIGHEST vs SLEEPEND. The proxy is internally validated only.

3. **Garmin can change the schema again without notice.** The 2024-07-08 / 2024-09-18 rollout was undocumented externally; future UDS schema changes are equally unannounced. Any analysis that runs after a re-extraction should sanity-check the source-flag distribution against the expected n_proxy ≈ 71.

4. **The proxy is not a substitute for confirmatory Wiggers D2.** Wiggers' D2 claim references the SLEEPEND-SLEEPSTART arc specifically (peak-to-trough BB charge during sleep). The proxy substitutes HIGHEST for SLEEPEND on the strength of the §5.2 timing alignment, which is 96.3% solid — not 100%. The 3.7% where HIGHEST is more than 2 h from SLEEPEND would be a different physiological event (e.g. a morning nap surge after wake). Confirmatory tests should not let proxy rows drive the headline.

5. **No per-minute BB anywhere in the dump.** This MD substitutes one daily summary statistic for another. It does NOT recover sub-day BB resolution. For sub-day arousal dynamics, see the stress-as-surrogate path in [`hrv_proxy_via_stress.md`](hrv_proxy_via_stress.md).

---

## 7. Cross-references

- [`../DATA_DICTIONARY.md` Body Battery section](../DATA_DICTIONARY.md#body-battery-11-columns) — column-level documentation for `bb_overnight_gain`, `bb_overnight_gain_proxy`, `bb_overnight_gain_best`, `bb_overnight_gain_source`, plus the per-minute BB absence note.
- [`intervention_effects_descriptive.md` §2b](intervention_effects_descriptive.md#2b-channel-coverage-gap--bb_overnight_gain) — boundary-by-boundary breakdown of where the proxy buys coverage and where it doesn't.
- [`hrv_proxy_via_stress.md`](hrv_proxy_via_stress.md) — sister proxy MD for `stress_mean_sleep` as HRV substitute on the same FR245 corpus; structurally similar four-input reasoning + validation pattern.
- [`garmin_indicators_audit.md`](garmin_indicators_audit.md) — per-column provenance for Garmin-sourced channels in `per_day_master.csv`.
- [`../CONVENTIONS.md` §2.2](../CONVENTIONS.md#22-methodology-md-before-locking-a-major-choice) — the four-input methodology-MD bar this doc satisfies.
- Implementation: [`../pipeline/01_extract/garmin_uds_extras.py`](../pipeline/01_extract/garmin_uds_extras.py) (extractor) + [`../pipeline/03_consolidate/build_unified_dataset.py`](../pipeline/03_consolidate/build_unified_dataset.py) (propagator to `per_day_master.csv`).
