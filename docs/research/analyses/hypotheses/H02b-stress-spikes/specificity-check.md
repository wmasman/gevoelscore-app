# H02b — Specificity check: what are the spike-firing non-crash windows?

Reproduction of the H02b null sample (seed 20260605), filtered to the ~41% of windows
that fired the +10-min spike criterion. For each: 3 lead-up day scores + reference day score,
peak-spike day, workout overlap, distance to nearest crash, and the note on the peak day.

## Counts

- null sample size: **200**
- false-positive windows (delta ≥ +10 min): **83** (42%)

**Categorization (multi-label, each window can carry several tags):**

| tag | count | % of false positives |
|-----|------:|---------------------:|
| `unexplained` | 37 | 45% |
| `near_miss` | 32 | 39% |
| `close_to_crash` | 28 | 34% |
| `activity_induced` | 15 | 18% |

Tag meanings:
- `near_miss`: any day in window or reference had score = 3 (a sub-threshold dip crash_v1 missed)
- `activity_induced`: a recorded workout ≥ 30 min on the peak-spike day
- `close_to_crash`: within ±14 days of an actual crash (but outside our 3-day lead-up window)
- `unexplained`: none of the above

**Combination counts:**

| combination | count |
|-------------|------:|
| unexplained | 37 |
| near_miss | 13 |
| close_to_crash+near_miss | 13 |
| activity_induced+close_to_crash+near_miss | 5 |
| close_to_crash | 5 |
| activity_induced+close_to_crash | 5 |
| activity_induced | 4 |
| activity_induced+near_miss | 1 |

## Per-window detail

Sorted by spike duration (largest first).

| ref date | scores [d-3,d-2,d-1,ref] | peak day | peak spike | baseline | days to crash | tags | activity on peak day | peak-day note |
|----------|--------------------------|----------|-----------:|---------:|-------------:|------|---------------------|---------------|
| 2026-01-24 | 5,6,5,6 | 2026-01-21 | 105 | 8.1 | +108 | unexplained | — | — |
| 2023-11-18 | 4,3,2,5 | 2023-11-16 | 90 | 11.4 | -6 | near_miss, close_to_crash | — | — |
| 2024-03-30 | 4,4,4,3 | 2024-03-28 | 88 | 10.4 | +31 | near_miss | — | In de ochtend ingepakt en daarna in de auto naar de Ardennen. Ging goed tot tijm… |
| 2025-10-29 | 5,5,5,5 | 2025-10-28 | 80 | 8.6 | -27 | unexplained | — | — |
| 2024-07-12 | 3,5,4,5 | 2024-07-10 | 69 | 9.5 | +3 | near_miss, close_to_crash | — | Ondanks de heftige dag gisteren, toch een goede dag gehad. Wat buiten kunnen wer… |
| 2026-01-09 | 5,4,5,5 | 2026-01-07 | 68 | 7.0 | -99 | unexplained | — | — |
| 2023-05-17 | 4,5,5,5 | 2023-05-14 | 67 | 12.3 | +11 | close_to_crash | — | moederdagontbijt fixen en daarna zeilen en uit eten |
| 2023-05-15 | 5,5,3,5 | 2023-05-14 | 67 | 12.1 | +13 | near_miss, close_to_crash | — | moederdagontbijt fixen en daarna zeilen en uit eten |
| 2023-05-16 | 5,5,5,4 | 2023-05-14 | 67 | 12.2 | +12 | close_to_crash | — | moederdagontbijt fixen en daarna zeilen en uit eten |
| 2026-02-11 | 5,5,4,3 | 2026-02-08 | 66 | 9.3 | +90 | near_miss | — | Wel ok maar echt een rustdag ook om donderdag as energie te hebben |
| 2025-07-08 | 5,4,5,5 | 2025-07-05 | 60 | 8.9 | -75 | unexplained | — | Famillie hockey tournooi on de middag. Op aan het einde van de dag |
| 2023-12-01 | 1,1,3,1 | 2023-11-30 | 55 | 11.0 | -4 | near_miss, close_to_crash | — | — |
| 2023-03-02 | 5,5,5,5 | 2023-02-28 | 55 | 13.4 | -26 | activity_induced | walking 2892.8min | — |
| 2023-12-01 | 1,1,3,1 | 2023-11-30 | 55 | 11.0 | -4 | near_miss, close_to_crash | — | — |
| 2023-03-03 | 5,5,5,6 | 2023-02-28 | 55 | 13.6 | -27 | activity_induced | walking 2892.8min | — |
| 2024-10-24 | 4,4,4,3 | 2024-10-22 | 53 | 7.8 | -56 | near_miss | — | Met Reynoud gepraat over de situatie met Angela. Daarna heel moe en hoofdpijn. |
| 2024-10-24 | 4,4,4,3 | 2024-10-22 | 53 | 7.8 | -56 | near_miss | — | Met Reynoud gepraat over de situatie met Angela. Daarna heel moe en hoofdpijn. |
| 2024-03-13 | 5,4,5,5 | 2024-03-11 | 48 | 9.7 | -17 | unexplained | — | Dag begin goed, bij Ria geweest. Maar tijdens rusten in de middag wilde het lijf… |
| 2023-07-08 | 5,5,5,3 | 2023-07-07 | 48 | 12.2 | -26 | near_miss | — | Helemaal kapot einde dag, ook naar mat en annel was echt teveel van het goede |
| 2026-01-16 | 6,5,5,5 | 2026-01-14 | 47 | 7.5 | -106 | unexplained | — | — |
| 2026-02-19 | 4,4,5,4 | 2026-02-16 | 47 | 9.5 | +82 | unexplained | — | — |
| 2023-10-07 | 4,4,4,3 | 2023-10-05 | 44 | 12.3 | -10 | near_miss, activity_induced, close_to_crash | walking 23387.5min; walking 22399.5min | — |
| 2023-10-06 | 4,4,3,4 | 2023-10-05 | 44 | 12.2 | -9 | near_miss, activity_induced, close_to_crash | walking 23387.5min; walking 22399.5min | — |
| 2025-03-30 | 5,5,4,4 | 2025-03-29 | 43 | 5.8 | +25 | unexplained | — | Geen hoofdpijn in de middag compost geschept, ging goed ben benieuwd of ik er de… |
| 2026-05-01 | 3,4,5,5 | 2026-04-28 | 42 | 11.2 | +11 | near_miss, close_to_crash | — | — |
| 2025-08-09 | 4,5,5,4 | 2025-08-07 | 42 | 10.6 | +54 | unexplained | — | Maar helemaal eraan einde dag |
| 2025-08-10 | 4,4,5,5 | 2025-08-07 | 42 | 10.9 | +53 | unexplained | — | Maar helemaal eraan einde dag |
| 2026-02-15 | 4,4,5,3 | 2026-02-14 | 41 | 9.3 | +86 | near_miss | — | — |
| 2025-01-21 | 3,4,4,5 | 2025-01-19 | 40 | 7.1 | -29 | near_miss | — | — |
| 2023-11-09 | 4,4,4,4 | 2023-11-07 | 40 | 11.4 | +3 | close_to_crash | — | naar kantoor, hoofdpijn einde dag |
| 2026-04-12 | 5,4,5,5 | 2026-04-11 | 40 | 10.7 | +30 | unexplained | — | — |
| 2023-07-13 | 5,5,5,5 | 2023-07-11 | 40 | 12.3 | -31 | unexplained | — | Goede maar ook drukke dag gehad, met hand wezen zeilen. Daarna echt leeg en in d… |
| 2023-07-14 | 5,5,5,5 | 2023-07-11 | 40 | 12.2 | -32 | unexplained | — | Goede maar ook drukke dag gehad, met hand wezen zeilen. Daarna echt leeg en in d… |
| 2025-01-19 | 4,4,5,4 | 2025-01-17 | 40 | 6.8 | -27 | unexplained | — | — |
| 2024-11-01 | 5,4,4,5 | 2024-10-29 | 40 | 8.1 | +52 | unexplained | — | — |
| 2023-04-20 | 4,5,5,5 | 2023-04-19 | 39 | 13.6 | -18 | unexplained | — | goede dag, wel heel vroeg en moe op bed 19:30 |
| 2023-05-25 | 4,4,3,5 | 2023-05-22 | 38 | 11.9 | +3 | near_miss, close_to_crash | — | geen erge hoofdpijn, wel erg moe en hele dag gelegen |
| 2025-06-07 | 6,6,4,6 | 2025-06-05 | 38 | 6.4 | -44 | unexplained | — | Goed geslapen en goed wakker geworden. Daarna wat groggy dus nu even rustig aan … |
| 2022-12-23 | 5,4,4,5 | 2022-12-22 | 38 | 10.8 | +4 | activity_induced, close_to_crash | walking 15099.6min; walking 20908.4min; walking 57038.6min | — |
| 2023-08-05 | 5,5,5,5 | 2023-08-02 | 36 | 13.3 | +33 | unexplained | — | — |
| 2023-08-03 | 5,4,4,5 | 2023-08-02 | 36 | 13.2 | +35 | unexplained | — | — |
| 2023-08-05 | 5,5,5,5 | 2023-08-02 | 36 | 13.3 | +33 | unexplained | — | — |
| 2025-04-04 | 4,5,5,4 | 2025-04-03 | 36 | 5.8 | +20 | unexplained | — | Weer wakker met lichte hoofdpijn en een naproxen genomen. Daarna veel beter. Van… |
| 2025-07-26 | 4,6,5,6 | 2025-07-23 | 35 | 9.1 | +68 | unexplained | — | — |
| 2024-12-06 | 5,5,5,5 | 2024-12-03 | 35 | 7.0 | +17 | unexplained | — | Dag 2 opruimen schuur. Organizers bij HORNBACH gekocht |
| 2024-02-22 | 4,5,3,4 | 2024-02-19 | 34 | 9.3 | +3 | near_miss, close_to_crash | — | hoofdpijn, niet heel helder. Ook wel wat labiel door vermoeidheid? Redelijke nac… |
| 2023-06-03 | 2,3,4,3 | 2023-06-01 | 34 | 11.4 | -6 | near_miss, close_to_crash | — | Keelpijn |
| 2026-04-10 | 5,4,5,4 | 2026-04-09 | 34 | 10.6 | +32 | unexplained | — | — |
| 2022-12-30 | 3,3,2,3 | 2022-12-29 | 33 | 11.4 | -3 | near_miss, activity_induced | walking 34099.6min | — |
| 2026-01-14 | 5,5,4,5 | 2026-01-13 | 32 | 7.5 | -104 | unexplained | — | — |
| 2023-03-20 | 4,3,4,5 | 2023-03-19 | 31 | 13.1 | +13 | near_miss, activity_induced, close_to_crash | walking 34339.9min | — |
| 2024-10-17 | 4,4,5,4 | 2024-10-14 | 31 | 8.0 | -49 | unexplained | — | — |
| 2022-09-08 | 4,4,4,3 | 2022-09-05 | 31 | 15.1 | -5 | near_miss, activity_induced, close_to_crash | cycling 51610.6min | — |
| 2026-02-02 | 5,5,6,5 | 2026-01-31 | 31 | 8.4 | +99 | unexplained | — | Bestuursweekend |
| 2023-06-15 | 4,3,3,5 | 2023-06-14 | 29 | 12.6 | -3 | near_miss | — | Weinig energie, en mentaal er ook wel een beetje doorheen. Spierpijn |
| 2025-06-10 | 4,5,6,5 | 2025-06-09 | 29 | 7.0 | -47 | unexplained | — | Inpakken |
| 2022-11-15 | 5,5,5,5 | 2022-11-14 | 29 | 12.6 | +8 | activity_induced, close_to_crash | walking 23868.4min; walking 19099.3min | — |
| 2022-09-11 | 2,4,3,5 | 2022-09-10 | 29 | 15.5 | +5 | near_miss, close_to_crash | — | — |
| 2023-05-10 | 5,4,4,5 | 2023-05-09 | 28 | 11.7 | +18 | unexplained | — | naar amsterdam op en neer, goede dag wel intensief. in de middag liggen slapen o… |
| 2024-04-18 | 5,3,5,5 | 2024-04-17 | 27 | 10.7 | +12 | near_miss, close_to_crash | — | Goed geslapen en redelijk ok vanochtend. Rest van de dag ook goed, met veel rust… |
| 2024-10-26 | 4,3,4,5 | 2024-10-24 | 26 | 7.8 | -58 | near_miss | — | Hoofdpijn |
| 2023-08-27 | 4,5,4,4 | 2023-08-26 | 26 | 13.4 | +11 | close_to_crash | — | — |
| 2024-10-26 | 4,3,4,5 | 2024-10-24 | 26 | 7.8 | -58 | near_miss | — | Hoofdpijn |
| 2023-08-29 | 4,4,4,5 | 2023-08-26 | 26 | 13.3 | +9 | close_to_crash | — | — |
| 2023-01-31 | 5,3,4,4 | 2023-01-30 | 25 | 12.6 | +4 | near_miss, activity_induced, close_to_crash | walking 64156.3min | goed geslapen, ben hoofdpijn weg |
| 2023-07-28 | 5,5,4,5 | 2023-07-26 | 25 | 12.6 | +41 | unexplained | — | — |
| 2024-12-07 | 5,5,5,4 | 2024-12-06 | 25 | 7.2 | +16 | unexplained | — | — |
| 2023-01-15 | 4,5,5,5 | 2023-01-14 | 25 | 11.1 | -19 | unexplained | — | — |
| 2025-11-19 | 6,5,5,4 | 2025-11-16 | 25 | 7.2 | -48 | unexplained | — | — |
| 2023-02-16 | 4,5,5,5 | 2023-02-15 | 25 | 12.7 | -12 | activity_induced, close_to_crash | walking 25932.1min | — |
| 2024-03-20 | 3,5,4,5 | 2024-03-17 | 24 | 9.9 | -24 | near_miss | — | Spierpijn in mijn benen en zware benen. Voel mij verder wel redelijk goed. Veel … |
| 2026-02-27 | 4,4,5,3 | 2026-02-26 | 24 | 10.1 | +74 | near_miss | — | Slecht geslapen heel moe |
| 2023-01-07 | 5,5,5,5 | 2023-01-05 | 23 | 11.1 | -11 | activity_induced, close_to_crash | walking 52265.2min | — |
| 2023-01-06 | 5,5,5,5 | 2023-01-05 | 23 | 11.0 | -10 | activity_induced, close_to_crash | walking 52265.2min | — |
| 2025-09-05 | 5,4,6,5 | 2025-09-03 | 23 | 12.0 | +27 | unexplained | — | Rhr sprong omhoog in de middag, na de lunch. Eat de plannen voor de dag in de wa… |
| 2024-03-09 | 3,4,4,4 | 2024-03-07 | 22 | 9.7 | -13 | near_miss, close_to_crash | — | Goed wakker geworden, klein beetje spierpijn, wat meestal een voorbode is voor e… |
| 2023-06-07 | 3,3,2,3 | 2023-06-05 | 22 | 12.0 | +5 | near_miss, close_to_crash | — | Hoesten, moe, snot, lichte hoofdpijn |
| 2024-08-07 | 5,5,4,5 | 2024-08-05 | 21 | 10.1 | +22 | activity_induced | sailing_v2 65.2min; sailing_v2 307.5min | Zeiltochtje naar gaastmeer, was heerlijk! |
| 2024-08-08 | 5,5,5,5 | 2024-08-05 | 21 | 9.9 | +21 | activity_induced | sailing_v2 65.2min; sailing_v2 307.5min | Zeiltochtje naar gaastmeer, was heerlijk! |
| 2024-12-01 | 5,5,3,5 | 2024-11-29 | 20 | 7.0 | +22 | near_miss | — | — |
| 2024-12-02 | 5,5,5,4 | 2024-11-29 | 20 | 7.0 | +21 | unexplained | — | — |
| 2025-05-15 | 4,6,5,5 | 2025-05-13 | 20 | 6.5 | -21 | unexplained | — | — |
| 2025-03-24 | 4,4,5,5 | 2025-03-21 | 17 | 6.1 | +31 | unexplained | — | — |

## How to read this

**If most false positives are `near_miss`**: crash_v1 is too strict. The spike metric is
genuinely detecting physiological strain that didn't manifest as a 2-day score-3 episode.
Argues for a `crash_v2` with a softer threshold OR a `dip_v1` for sub-threshold events.

**If most are `activity_induced`**: the spike extractor needs to filter on activity-overlap
days. Garmin generally suppresses stress samples during recorded activities (`stressTooActiveCount`),
but a long unrecorded effort could leak through.

**If most are `close_to_crash`**: the 3-day lead-up window is too narrow. The signal is
real but lives in a wider window than we tested. Argues for an H02d with 7-day lead-up.

**If most are `unexplained`**: the spike is a necessary-but-not-sufficient signal. Days
with the spike pattern usually pass without becoming a crash; only some combination of
the spike plus other factors precipitates one. Surfacing the spike standalone as a
predictor card would be misleading. Confirms the 'NOT to build' decision in the stocktake.
