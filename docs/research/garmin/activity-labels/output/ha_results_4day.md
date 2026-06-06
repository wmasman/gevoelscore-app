# HA01 + HA02 + HA05 — Activity-vs-PEM test results

Pre-registered 2026-06-06; criteria locked before run. All three criteria required, both windows, for 'supported'.

## HA01b (train crash)

- n events clean: **13** | null sample: 200
- frac event with shock: **84.6%** | frac null: 76.0%
- median n_shock_days: **2** | lower-q: 1
- discrimination: **+8.6 pp**
- crit (a) freq ≥60%: **PASS**
- crit (b) disc ≥+15 pp: fail
- crit (c) magnitude: **PASS**
- **verdict: REFUTED**

## HA01b (validate crash)

- n events clean: **15** | null sample: 200
- frac event with shock: **93.3%** | frac null: 76.0%
- median n_shock_days: **2** | lower-q: 1
- discrimination: **+17.3 pp**
- crit (a) freq ≥60%: **PASS**
- crit (b) disc ≥+15 pp: **PASS**
- crit (c) magnitude: **PASS**
- **verdict: SUPPORTED**

## HA02b (train crash)

- n events clean: **13** | null sample: 200
- frac event >=push_T: **38.5%** | frac null: 44.5%
- median max_push_7d: **2** | lower-q: 1
- discrimination: **-6.0 pp**
- crit (a) freq ≥60%: fail
- crit (b) disc ≥+15 pp: fail
- crit (c) magnitude: fail
- **verdict: REFUTED**

## HA02b (validate crash)

- n events clean: **15** | null sample: 200
- frac event >=push_T: **46.7%** | frac null: 44.5%
- median max_push_7d: **2** | lower-q: 1
- discrimination: **+2.2 pp**
- crit (a) freq ≥60%: fail
- crit (b) disc ≥+15 pp: fail
- crit (c) magnitude: fail
- **verdict: REFUTED**

## HA05 — Crash-vs-dip discrimination ratio

- HA01 train: crash disc = +8.6 pp, dip disc = +5.5 pp, ratio = 1.57x
- HA02 train: crash disc = -6.0 pp, dip disc = -3.8 pp, ratio = 1.61x

**verdict: REFUTED** (supported if both ratios ≥2)

## Reference: HA01 + HA02 on dips (informs HA05)

- HA01b (train dip): frac=81.5%, disc=+5.5 pp, verdict=refuted
- HA01b (validate dip): frac=75.0%, disc=-1.0 pp, verdict=refuted
- HA02b (train dip): frac=40.7%, disc=-3.8 pp, verdict=refuted
- HA02b (validate dip): frac=30.8%, disc=-13.7 pp, verdict=refuted

---

*Run 2026-06-06. Seed `20260605` matches H02b.*