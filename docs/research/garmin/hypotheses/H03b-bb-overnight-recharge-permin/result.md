# H03b — Per-minute BB overnight recharge — result (INCONCLUSIVE by data availability)

**Run date**: 2026-06-07. **Test script**: [test.py](test.py).
**Pre-registration**: [hypothesis.md](hypothesis.md), locked 2026-06-07.
**Output data**: [result-data.json](result-data.json).

## TL;DR

**H03b returns INCONCLUSIVE across all 12 evaluation cells** (3
N_std tiers × 2 lead-up windows × 2 eras). Data-availability
investigation 2026-06-07 surfaced two cutover dates in the Garmin
Connect API:
- `bodyBatteryChange` (daily scalar) — None for all dates before
  ~2023-12-31
- `sleepBodyBattery` (per-3-min array during sleep) — empty for
  all dates before ~2024-06-03

H03b needs the per-3-min array for its `peak_during_sleep -
sleep_onset_value` integral. With the array only populated from
~2024-06-03 onwards, and the locked lagged-baseline requiring ≥40
valid days in [d-90, d-30], **only 6 of the 15 validate-era
crashes have both per-minute data AND a usable baseline**. Train
era (14 crashes) has zero coverage.

**Both eras fall below the locked n_clean ≥ 10 threshold** for the
inconclusive cutoff (hypothesis.md §5). The locked spec returns
INCONCLUSIVE without proceeding to verdict computation.

## Section 1: Data-availability finding (the actual H03b finding)

This is the substantive finding from the H03b run.

### 1.1 Two cutover dates in the Garmin Connect API

| field | endpoint | populated from | notes |
|---|---|---|---|
| `bodyBatteryChange` (scalar) | `get_sleep_data().bodyBatteryChange` | ~2023-12-31 | daily overnight recharge as a single number |
| `sleepBodyBattery` (array) | `get_sleep_data().sleepBodyBattery` | ~2024-06-03 | per-3-min BB during sleep window; 200-250 samples per night |
| `bodyBatteryValuesArray` (sparse) | `get_body_battery()` | full history but only ~6 transitions per day | NOT per-minute; sparse "key event" points |
| `get_body_battery_events()` | events endpoint | mostly empty | returns sleep/activities/naps events, NOT samples |

The hypothesis.md §3 specified the
`/wellness-service/wellness/bodyBattery/events/{date}` endpoint
(intended to give per-minute BB). Investigation 2026-06-07
confirmed this endpoint returns event records (sleep, activities,
naps), NOT per-minute samples. For 2026-05-15,
`get_body_battery_events()` returned an empty list.

The per-3-min BB during sleep window IS available — but only via
the sleep API's `sleepBodyBattery` array (236 samples for
2026-05-15, ~3-min interval). This is **sufficient for H03b's
metric** (peak − sleep_onset_value is computed from values within
the sleep window). Per playbook §2.2, the endpoint clarification
is audit-trail, not a spec change (the substantive metric, claim,
threshold, window, direction, and bar are all unchanged from
hypothesis.md).

### 1.2 Coverage of crash episodes

| era | total crashes | crashes with any leadup recharge | crashes with usable baseline |
|---|---:|---:|---:|
| **train** (2022-09 → 2023-12) | 14 | **0** | **0** |
| **validate** (2024-01 → 2026-06) | 15 | 9 | **6** |

Of the 9 validate crashes with at least one leadup day having
`sleepBodyBattery`, only 6 have a baseline window with ≥40 valid
days (the baseline starts being valid only ~2024-09, 90 days after
sleepBodyBattery starts; earlier validate crashes have insufficient
baseline history).

### 1.3 First/last valid days

- First valid overnight recharge: **2024-06-03**
- Last valid overnight recharge: **2026-06-05**
- Total valid recharge days: **716** (out of ~735 days in the
  2024-06-03 → 2026-06-05 window, ~97% coverage in that range)

## Section 2: Verdict — INCONCLUSIVE × 12

Per locked hypothesis.md §5: "If fewer than 10 clean crash episodes
per window → inconclusive."

| era | window | N_std | n_clean | verdict |
|---|---:|---:|---:|:-:|
| train | 4d | 1.5 | 0 | inconclusive |
| train | 4d | 2.0 | 0 | inconclusive |
| train | 4d | 2.5 | 0 | inconclusive |
| validate | 4d | 1.5 | 6 | inconclusive |
| validate | 4d | 2.0 | 6 | inconclusive |
| validate | 4d | 2.5 | 6 | inconclusive |
| train | 5d | 1.5 | 0 | inconclusive |
| train | 5d | 2.0 | 0 | inconclusive |
| train | 5d | 2.5 | 0 | inconclusive |
| validate | 5d | 1.5 | 6 | inconclusive |
| validate | 5d | 2.0 | 6 | inconclusive |
| validate | 5d | 2.5 | 6 | inconclusive |

The locked bar binds. No verdict mapping to HA10 (per hypothesis.md
§6) can be computed because no verdicts were generated.

## Section 3: What this means for the BB overnight recharge channel

The substantive BB-overnight-recharge question is **already answered
at coarse resolution** by HA10:

- **HA10** (BB overnight recharge using the 3 daily anchor points —
  HIGHEST / LOWEST / MOSTRECENT, available for the full corpus):
  validate SUPPORTED at +16.2 pp (86.7% freq, 4d primary
  bidirectional), v2 threshold-monotonicity RESCUE via Cat 3.
  Currently load-bearing as corroborating secondary anchor for
  validate-era.
  [HA10-bb-overnight-recharge/result.md](../HA10-bb-overnight-recharge/result.md)
  +
  [HA10-threshold-monotonicity-diagnostic-v2/result.md](../HA10-threshold-monotonicity-diagnostic-v2/result.md).

**H03b was the sharpening test.** Per hypothesis.md §6, H03b was
designed to test whether the per-minute integral gives sharper
discrimination than HA10's peak-only metric. With H03b INCONCLUSIVE
on n<10, the sharpening test cannot be performed on the current
data corpus.

**HA10 stays as the canonical BB overnight recharge finding** for
the validate era. The "per-minute sharpens HA10" question is
deferred.

## Section 4: What would un-block H03b

Per hypothesis.md §3 + QUEUED-WORK §H04b path B, the only route to
per-minute BB for the full corpus (especially the 14 train-era
crashes that the API path C cannot reach) is:

- **Path B: FIT decode of `unknown_233`** — decode the per-minute
  Body Battery from local FIT files using path C labels (the 716
  recent days where both sources exist) as ground truth.

This is an open H04b track. If successful, it would unlock
per-minute BB for the full corpus 2021-08-16 → 2026-06-04 (Garmin
FIT files cover this range). H03b could then be re-run with
sufficient n on both eras.

**Estimated effort**: multi-day decoding work; not deferred to a
specific date.

## Section 5: Audit trail (per playbook §2.5)

### 5.1 Endpoint clarification

hypothesis.md §3 specified the
`/wellness-service/wellness/bodyBattery/events/{date}` endpoint as
the per-minute BB source. The endpoint actually returns event
records (sleep, activities, naps), NOT per-minute samples. The
actual per-3-min BB during sleep window is available via the sleep
API's `sleepBodyBattery` array.

Per playbook §2.2, this is an implementation-source clarification,
NOT a spec change. The claim, threshold, window, direction, bar,
and metric definition (peak − sleep_onset value) are all unchanged.
A spec change would require a new hypothesis ID; an
implementation-source clarification is documented in the result.md
audit trail.

### 5.2 Sample requirements

hypothesis.md §4.2 specifies ≥30 valid per-minute BB samples per
night for a valid overnight recharge. With the sleep API providing
~3-min resolution and typical sleep windows of 7-9 hours, valid
nights yield 140-180 samples (well above the threshold). The
sample-count validity gate did not exclude any otherwise-valid
nights in the data-available window.

### 5.3 Inconclusive threshold (n_clean ≥ 10)

hypothesis.md §5 locked the n=10 threshold for the inconclusive
cutoff. The data-availability investigation revealed validate has
only 6 clean episodes (after baseline-validity filtering). Per
playbook §2.1, the locked threshold binds even when the
data-availability gap was not anticipated. Lowering the threshold
mid-run would be a spec change requiring a new hypothesis ID
(H03c), which was offered to the user but they chose to run H03b
as-locked and accept INCONCLUSIVE.

### 5.4 Pre-registration discipline preserved

H03b's INCONCLUSIVE verdict is itself a finding — it documents the
data-availability constraint on per-minute BB analysis for this
participant's corpus. The pre-commitment to "run the locked spec
and accept the verdict" was honored. No post-hoc rescue attempt
was made.

## Section 6: Caveats this result must explicitly acknowledge

Per hypothesis.md §8:

- **Garmin API ToS-grey**: confirmed — the per-minute endpoints
  are populated only for ~2024-06+. Older data is not retrievable
  via the API (and likely never will be without a path B FIT
  decode).
- **Garmin's BB algorithm is opaque**: irrelevant for this result
  (no verdict computed).
- **HRV is one of BB's inputs**: irrelevant for this result.
- **Sleep-onset timing approximation**: still relevant for any
  future re-run on more data; not a factor in the INCONCLUSIVE
  verdict.
- **Per-minute samples may have gaps**: not a factor (samples are
  abundant in the data-available window).
- **Multi-comparison**: H03b is the 17th pre-registered hypothesis
  in the H##/HA## series; the INCONCLUSIVE outcome contributes
  zero to the multi-comparison count (no verdict was generated).

## Section 7: Compliance verification (playbook §9, 19 items)

- [x] Folder structure: `H03b-bb-overnight-recharge-permin/` per §4.7
- [x] Pre-registration locked 2026-06-07 BEFORE this script ran
- [x] References playbook in hypothesis.md and result.md
- [x] crash_v1 used (29 episodes; 14 train, 15 validate)
- [x] Default train/validate split + both-eras rule applied
  (vacuously — neither era reaches the bar)
- [x] Lagged baseline construction
- [x] Relative thresholds (z-score with locked baseline)
- [x] Primary direction: bidirectional (locked from HA10's
  era-reversal finding)
- [x] 3-episode dry-run gate: ran (shows train + early-validate
  have no recharge data; surfaced data-availability finding)
- [x] 3-criterion bar at locked thresholds (vacuously, no verdicts
  generated)
- [x] Null sample seed `20260605`, N=200
- [x] Validity floors per playbook §4.6 (≥30 samples per night,
  ≥40 baseline days, σ floor 3.0 BB points)
- [x] Decision rules → verdict categories per playbook §2.6
  (INCONCLUSIVE per locked n<10 threshold)
- [x] Channel non-independence acknowledgement: BB shares HR/HRV/
  stress inputs (caveat 3 from hypothesis.md §8)
- [x] Multi-comparison disclosure: caveat 6 above
- [x] v2 threshold-monotonicity follow-up: N/A (no verdict to
  diagnose)
- [x] No-go surfaces flagged: N/A (no card.md drafted; INCONCLUSIVE
  cannot lead to card)
- [x] Hardware constraints: FR245 records BB via algorithm; per-minute
  API arrays only populated for ~2024-06+ (Garmin-side cutover, not
  hardware blocker)
- [x] Audit trail: section 5 above

## Section 8: Synthesis implications

**No change to load-bearing list**:
- HA07d (both eras overall-SUPPORTED + v2-validated): unchanged
- HA10 (validate corroborating, v2 RESCUE): **unchanged — remains
  the canonical BB overnight recharge finding**
- HA11 (train): unchanged
- H02b / H02d (train): unchanged
- HA06b (permanently demoted): unchanged
- HA01c (SUPPORTED-with-stability-mixed, not load-bearing):
  unchanged

**No card.md drafted**: INCONCLUSIVE cannot produce a card per
playbook §2.7.

**Documented for QUEUED-WORK**: H03b status updates from
"pending H04b path C authorisation" to "INCONCLUSIVE-by-data-availability
2026-06-07; re-runnable only after H04b path B FIT decode unlocks
per-minute BB for old corpus."

**Methodology lesson banked**: when a pre-registered hypothesis
depends on a third-party API endpoint, verify data-availability
across the analysis window BEFORE locking the inconclusive
threshold. The H03b case shows that an n=10 threshold combined
with a 2024-06 data cutover automatically forces INCONCLUSIVE for
any test using 2024+ data only. This is a generalisable lesson for
future API-dependent pre-registrations; queued for playbook §3
addendum consideration.

---

*Result locked 2026-06-07. H03b runs to completion under the
locked spec; the INCONCLUSIVE verdict documents the
data-availability constraint and preserves the audit trail. HA10
stays as the canonical BB overnight recharge finding for the
validate era; H03b sharpening deferred pending path B (FIT decode).*
