# HA01 + HA02 + HA05 — Activity-vs-PEM test results

Pre-registered 2026-06-06; criteria locked before run. All three criteria required, both windows, for 'supported'.

## HA01 (train crash)

- n events clean: **13** | null sample: 200
- frac event with shock: **69.2%** | frac null: 68.5%
- median n_shock_days: **2** | lower-q: 0
- discrimination: **+0.7 pp**
- crit (a) freq ≥60%: **PASS**
- crit (b) disc ≥+15 pp: fail
- crit (c) magnitude: **PASS**
- **verdict: REFUTED**

## HA01 (validate crash)

- n events clean: **15** | null sample: 200
- frac event with shock: **80.0%** | frac null: 68.5%
- median n_shock_days: **1** | lower-q: 1
- discrimination: **+11.5 pp**
- crit (a) freq ≥60%: **PASS**
- crit (b) disc ≥+15 pp: fail
- crit (c) magnitude: **PASS**
- **verdict: REFUTED**

## HA02 (train crash)

- n events clean: **13** | null sample: 200
- frac event >=push_T: **38.5%** | frac null: 40.0%
- median max_push_7d: **2** | lower-q: 1
- discrimination: **-1.5 pp**
- crit (a) freq ≥60%: fail
- crit (b) disc ≥+15 pp: fail
- crit (c) magnitude: fail
- **verdict: REFUTED**

## HA02 (validate crash)

- n events clean: **15** | null sample: 200
- frac event >=push_T: **40.0%** | frac null: 40.0%
- median max_push_7d: **2** | lower-q: 1
- discrimination: **+0.0 pp**
- crit (a) freq ≥60%: fail
- crit (b) disc ≥+15 pp: fail
- crit (c) magnitude: fail
- **verdict: REFUTED**

## HA05 — Crash-vs-dip discrimination ratio

- HA01 train: crash disc = +0.7 pp, dip disc = +9.3 pp, ratio = 0.08x
- HA02 train: crash disc = -1.5 pp, dip disc = -3.0 pp, ratio = 0.52x

**verdict: REFUTED** (supported if both ratios ≥2)

## Reference: HA01 + HA02 on dips (informs HA05)

- HA01 (train dip): frac=77.8%, disc=+9.3 pp, verdict=refuted
- HA01 (validate dip): frac=73.1%, disc=+4.6 pp, verdict=refuted
- HA02 (train dip): frac=37.0%, disc=-3.0 pp, verdict=refuted
- HA02 (validate dip): frac=26.9%, disc=-13.1 pp, verdict=refuted

---

*Run 2026-06-06. Seed `20260605` matches H02b.*