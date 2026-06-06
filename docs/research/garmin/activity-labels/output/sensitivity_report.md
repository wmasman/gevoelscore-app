# Sensitivity test — v3 severity_spec parameter robustness

Pre-registered 2026-06-06. Verdict rule locked before running: Jaccard >= 0.7 vs reference = ROBUST; < 0.5 = SENSITIVE; 0.5-0.7 = MIXED.

## Reference distributions (locked v3 params)

Reference: baseline_window=30, push_window=7, push_threshold=0.75, cutoffs=0.5/0.75/0.85/0.95

**exertion_class:**
| class | count | % |
|---|---:|---:|
| none | 362 | 26.4% |
| light | 325 | 23.7% |
| moderate | 212 | 15.5% |
| heavy | 239 | 17.4% |
| very_heavy | 234 | 17.1% |

**push_burden_class:**
| class | count | % |
|---|---:|---:|
| none | 239 | 17.4% |
| light | 411 | 30.0% |
| moderate | 357 | 26.0% |
| heavy | 340 | 24.8% |
| very_heavy | 25 | 1.8% |

## Alternate configurations

Each row is a single-dimension variation from reference.

| name | param changed | exertion_class very_heavy | push_burden very_heavy | Jaccard vh_exertion | Jaccard vh_push | Jaccard heavy+ exertion | Jaccard heavy+ push | Spearman ranks |
|---|---|---:|---:|---:|---:|---:|---:|---:|
| bw_14 | baseline_window=14 | 243 (17.7%) | 30 (2.2%) | 0.645 | 0.571 | 0.763 | 0.612 | 0.957 |
| bw_21 | baseline_window=21 | 304 (22.2%) | 33 (2.4%) | 0.752 | 0.611 | 0.850 | 0.774 | 0.982 |
| bw_45 | baseline_window=45 | 230 (16.8%) | 36 (2.6%) | 0.778 | 0.525 | 0.863 | 0.784 | 0.985 |
| bw_60 | baseline_window=60 | 215 (15.7%) | 42 (3.1%) | 0.707 | 0.426 | 0.808 | 0.720 | 0.975 |
| pw_5 | push_window=5 | 234 (17.1%) | 1 (0.1%) | 1.000 | 0.040 | 1.000 | 0.463 | n/a |
| pw_10 | push_window=10 | 234 (17.1%) | 115 (8.4%) | 1.000 | 0.217 | 1.000 | 0.545 | n/a |
| pw_14 | push_window=14 | 234 (17.1%) | 369 (26.9%) | 1.000 | 0.068 | 1.000 | 0.385 | n/a |
| pt_0.65 | push_threshold=0.65 | 234 (17.1%) | 104 (7.6%) | 1.000 | 0.240 | 1.000 | 0.593 | n/a |
| pt_0.70 | push_threshold=0.7 | 234 (17.1%) | 67 (4.9%) | 1.000 | 0.373 | 1.000 | 0.693 | n/a |
| pt_0.80 | push_threshold=0.8 | 234 (17.1%) | 17 (1.2%) | 1.000 | 0.680 | 1.000 | 0.742 | n/a |
| pt_0.85 | push_threshold=0.85 | 234 (17.1%) | 8 (0.6%) | 1.000 | 0.320 | 1.000 | 0.384 | n/a |
| cuts_soft | cutoffs=(0.5, 0.7, 0.8, 0.9) | 385 (28.1%) | 25 (1.8%) | 0.608 | 1.000 | 0.784 | 1.000 | n/a |
| cuts_strict | cutoffs=(0.5, 0.8, 0.9, 0.97) | 133 (9.7%) | 25 (1.8%) | 0.568 | 1.000 | 0.814 | 1.000 | n/a |

## Verdict per dimension

### baseline_window
- exertion_class very_heavy: min Jaccard = 0.645; max = 0.778; verdict = **MIXED**
- push_burden very_heavy: min Jaccard = 0.426; max = 0.611; verdict = **SENSITIVE**
- exertion_class heavy+very_heavy: min Jaccard = 0.763; max = 0.863; verdict = **ROBUST**

### push_window
- exertion_class very_heavy: min Jaccard = 1.000; max = 1.000; verdict = **ROBUST**
- push_burden very_heavy: min Jaccard = 0.040; max = 0.217; verdict = **SENSITIVE**
- exertion_class heavy+very_heavy: min Jaccard = 1.000; max = 1.000; verdict = **ROBUST**

### push_threshold
- exertion_class very_heavy: min Jaccard = 1.000; max = 1.000; verdict = **ROBUST**
- push_burden very_heavy: min Jaccard = 0.240; max = 0.680; verdict = **SENSITIVE**
- exertion_class heavy+very_heavy: min Jaccard = 1.000; max = 1.000; verdict = **ROBUST**

### cutoffs
- exertion_class very_heavy: min Jaccard = 0.568; max = 0.608; verdict = **MIXED**
- push_burden very_heavy: min Jaccard = 1.000; max = 1.000; verdict = **ROBUST**
- exertion_class heavy+very_heavy: min Jaccard = 0.784; max = 0.814; verdict = **ROBUST**

## Overall robustness

- min Jaccard across all alternates and all metrics: **0.040**
- mean Jaccard: **0.725**
- counts: ROBUST = 31, MIXED = 11, SENSITIVE = 10

**Overall verdict: PARTIALLY SENSITIVE** — at least one alternate gives Jaccard < 0.5. Re-examine spec before downstream tests.

---
*Generated 2026-06-06 by 07_sensitivity_test.py.*