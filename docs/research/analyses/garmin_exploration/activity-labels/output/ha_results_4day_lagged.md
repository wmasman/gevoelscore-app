# HA01b-recomputed + HA02c bundled re-test (A.1 lagged baseline)

Pre-registered 2026-06-06 in [severity_spec.md §Lagged baseline (v3.2)](../spec/severity_spec.md) and [registry.md §4b Theme A](../../hypotheses/registry.md) BEFORE this script ran. Same SUPPORTED bar as the original HA01b/HA02b runs (freq ≥60%, disc ≥+15 pp, magnitude). Same null seed (`20260605`) and same 4-day lead-up window as [09_run_ha_tests_4day.py](../scripts/09_run_ha_tests_4day.py) for direct comparability.

Bundled (both tests run together on the same A.1 reference) to maintain symmetric re-test discipline: re-testing only the refutation while keeping the win as-is would be selective rescue.

---

## HA01b-recomputed (validate the win on lagged baseline)

### HA01b-recomputed (train crash)

- n events clean: **11** | null sample: 200
- frac event with shock (heavy+): **81.8%** | frac null: 76.0%
- median n_shock_days: **2** | lower-q: 1
- discrimination: **+5.8 pp**
- crit (a) freq ≥60%: **PASS**
- crit (b) disc ≥+15 pp: fail
- crit (c) magnitude: **PASS**
- **verdict: REFUTED**

Side-by-side with the original HA01b (rolling baseline, [ha_results_4day.md](../output/ha_results_4day.md)):

| metric | rolling (original) | lagged (recomputed) | delta |
|---|---:|---:|---:|
| frac event with shock | 84.6% | 81.8% | -2.8 pp |
| discrimination       | +8.6 pp | +5.8 pp | -2.8 pp |
| verdict              | refuted | refuted | same |

### HA01b-recomputed (validate crash)

- n events clean: **15** | null sample: 200
- frac event with shock (heavy+): **80.0%** | frac null: 76.0%
- median n_shock_days: **2** | lower-q: 1
- discrimination: **+4.0 pp**
- crit (a) freq ≥60%: **PASS**
- crit (b) disc ≥+15 pp: fail
- crit (c) magnitude: **PASS**
- **verdict: REFUTED**

Side-by-side with the original HA01b (rolling baseline, [ha_results_4day.md](../output/ha_results_4day.md)):

| metric | rolling (original) | lagged (recomputed) | delta |
|---|---:|---:|---:|
| frac event with shock | 93.3% | 80.0% | -13.3 pp |
| discrimination       | +17.3 pp | +4.0 pp | -13.3 pp |
| verdict              | supported | refuted | CHANGED |

---

## HA02c (test if push burden was masked by the rolling baseline)

### HA02c (train crash)

- n events clean: **11** | null sample: 200
- frac event with max_push ≥3: **27.3%** | frac null: 46.0%
- median max_push_7d: **2** | lower-q: 1
- discrimination: **-18.7 pp**
- crit (a) freq ≥60%: fail
- crit (b) disc ≥+15 pp: fail
- crit (c) magnitude: fail
- **verdict: REFUTED**

Side-by-side with the original HA02b (rolling baseline, [ha_results_4day.md](../output/ha_results_4day.md)):

| metric | rolling (original) | lagged (recomputed) | delta |
|---|---:|---:|---:|
| frac event ≥push_T   | 23.1% | 27.3% | +4.2 pp |
| discrimination       | -2.0 pp | -18.7 pp | -16.7 pp |
| verdict              | refuted | refuted | same |

### HA02c (validate crash)

- n events clean: **15** | null sample: 200
- frac event with max_push ≥3: **46.7%** | frac null: 46.0%
- median max_push_7d: **2** | lower-q: 1
- discrimination: **+0.7 pp**
- crit (a) freq ≥60%: fail
- crit (b) disc ≥+15 pp: fail
- crit (c) magnitude: fail
- **verdict: REFUTED**

Side-by-side with the original HA02b (rolling baseline, [ha_results_4day.md](../output/ha_results_4day.md)):

| metric | rolling (original) | lagged (recomputed) | delta |
|---|---:|---:|---:|
| frac event ≥push_T   | 6.7% | 46.7% | +40.0 pp |
| discrimination       | -7.4 pp | +0.7 pp | +8.1 pp |
| verdict              | refuted | refuted | same |

---

## Bundled re-test headline

- **HA01b-recomputed validate**: REFUTED (+4.0 pp on lagged baseline; original rolling was +17.3 pp)
- **HA01b-recomputed train**: REFUTED
- **HA02c validate**: REFUTED (+0.7 pp on lagged baseline; original rolling was -7.4 pp)
- **HA02c train**: REFUTED

**HA01b validate-era finding softens on lagged baseline** (+4.0 pp < +15 pp; delta vs original +17.3 pp = -13.3 pp). The addendum's 'first SUPPORTED validate-era precursor' headline needs to soften accordingly. Honest accountancy.

**HA02c stays refuted on lagged baseline**: push burden is not a precursor for this person on either reference frame. The Theme A fix improves the metric's measurement-theoretic standing but does not resurrect it as a predictor.

---

*Run 2026-06-06. Seed `20260605` matches scripts 08/09.*