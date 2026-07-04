"""Post-crash exertion relapse ("danger window"): producer-mode test execution.

Implements the LOCKED pre-registration verbatim:
  docs/research/analyses/hypotheses/post-crash-exertion-relapse/hypothesis.md
  (LOCKED 2026-07-04; any change to the claim, primary exposure, danger-window
  definition, matched-baseline construction, null, relapse window, or primary
  test creates a v2).

Question (pre-reg section 1): after a crash, during the DANGER WINDOW
(felt-state recovered, gevoelscore >= 4, but autonomic not yet settled, from
the felt-recovery day through nadir+10), is a single supra-threshold PEAK
CARDIAC-STRAIN spike more likely to trip a RELAPSE (a new crash or dip within
4 days) than the SAME-MAGNITUDE peak-strain spike at a constructed matched
baseline?

  "stress" = Garmin HRV-derived Stress Score (GSS), never mental/emotional
             stress. "exertion" / "strain" = physical / cardiac load only.

Primary exposure (locked, section 4b + 4e): the peak single-day
MASKED max_hr_rank_lagged_lcera in the danger window. The mask (section 4e)
excludes is_crash / is_dip days from the [d-90, d-30] lagged baseline pool.
The stored (un-masked) column is the single named sensitivity.

Method (all locked in the pre-reg; sections referenced inline):
  0. Reproduction check (section 4e-2): recompute the UN-masked rank from raw
     max_hr and confirm it reproduces the stored max_hr_rank_lagged_lcera; this
     proves the masked recompute is the same algorithm minus the masking.
  1. Masked-primary recompute (section 4e): the locked PRIMARY exposure.
  2. Events (section 3, 5): crash nadirs (28 usable of 29) primary arm; dip days
     (79) mechanism-control arm. Felt-recovery gate gevoelscore >= 4 in
     t+1..t+10 (section 4a). Danger window = felt-recovery day .. nadir+10
     (primary window = 10; 7/10/14 sensitivity, section 4a).
  3. Danger-window PEAK exposure = the MAX single-day masked rank over the
     danger-window days (section 4b); record the peak-day.
  4. Relapse outcome (section 5): a NEW crash OR dip within 4 days AFTER the
     peak-day (peak strictly precedes relapse; ordering guard section 4f);
     3/4/5-day sensitivity.
  5. Matched-baseline reference set (section 4d, all-eligible-in-caliper, no
     random draw): every LC-era day OUTSIDE any post-crash danger window that
     meets all three calipers (rank-band +/- 0.03; same recovery_phase;
     preceding-3-day gevoelscore mean +/- 1.0). Each baseline day gets its own
     relapse outcome.
  6. The ONE primary statistic (section 6): the standardised mean over the 28
     usable crash events of delta_i = (danger-window relapse 0/1) - (mean
     relapse rate of that peak's matched-baseline pool). Also the rank-slope
     reading (relapse-excess regressed on peak-rank magnitude).
  7. Event-level block-permutation null (section 6): ACF readout on the masked
     rank to justify E[L]=7 (data-driven E[L]* companion, factor-of-2 override);
     >= 10,000 replicates block-permute the danger-window-vs-baseline LABELS
     across pooled labelled units under stationary calendar blocks at E[L],
     holding each unit's peak magnitude and relapse outcome fixed, recomputing
     the one primary statistic. Observed percentile = p-analogue; 2.5/97.5
     percentiles = CI.
  8. Crash-vs-dip formal slope interaction (section 7), base-rate-conditioned;
     the 2.7x power asymmetry stated; the dip arm is SECONDARY.
  9. Activity-volume COMPARISON arm (eff_exertion_rank_lagged_lcera, same
     window, same peak rule) - the strain-vs-volume in-sample confound test.
 10. Cumulative-strain SECONDARY (danger-window aggregate of
     hr_area_above_daytime_baseline_waking_lcera).
 11. Sensitivities: 7/10/14 window; 3/4/5 relapse; masked vs un-masked;
     autonomic-trend exclusion (drop danger-window days with
     stress_mean_sleep_lagged_lcera_z rising, primary key;
     resting_hr_lagged_lcera_z rising, second read).

RNG seed (recorded): 20260704. Only the block-permutation null uses the RNG;
the all-eligible-in-caliper matching has NO random draw.

No PII. No emojis. No em-dashes. ASCII-only printed output.
"""

from __future__ import annotations

import sys
from pathlib import Path

import numpy as np
import pandas as pd

# House stationary-block mechanic + data-driven block-length estimator, so the
# permutation matches the project pattern (mirrors the sibling peri-event-covid
# test.py precedent).
_UTILS = Path(__file__).resolve().parents[2] / "_utils"
sys.path.insert(0, str(_UTILS.parent))
from _utils.inference import (  # noqa: E402
    compute_data_driven_block_length,
    _stationary_bootstrap_indices,
)

# ----------------------------------------------------------------------------
# Locked constants (all from the pre-reg / precondition / the _lcera extractor)
# ----------------------------------------------------------------------------

DATA_PATH = r"C:\Users\Gebruiker\Documents\gevoelscore-data\unified\per_day_master.csv"

# _lcera lagged-baseline parameters, reproduced from
# analyses/garmin_exploration/activity-labels/scripts/11_compute_lagged_baseline.py
# (compute_lagged_rank). LCERA_START = date(2022, 4, 4).
LCERA_START = pd.Timestamp(2022, 4, 4)
LAG_START_DAYS = 30            # earliest excluded day (recent candidate region)
LAG_END_DAYS = 90             # oldest included day
MIN_LAGGED_DAYS = 40          # require ~2/3 of the 60-day window

# Danger window + relapse + matching calipers (pre-reg sections 4a, 4d, 5).
DANGER_WINDOW_PRIMARY = 10    # nadir+10; 7/10/14 sensitivity band
DANGER_WINDOW_BAND = (7, 10, 14)
RELAPSE_PRIMARY = 4           # new crash/dip within 4 days AFTER the peak-day
RELAPSE_BAND = (3, 4, 5)
FELT_RECOVERY_GATE = 4        # gevoelscore >= 4 in t+1..t+10
FELT_RECOVERY_LOOKAHEAD = 10  # t+1..t+10

RANK_BAND_CALIPER = 0.03      # peak rank +/- 0.03 (section 4d-i)
FELT_TRAJ_CALIPER = 1.0       # preceding-3-day gevoelscore mean +/- 1.0 (4d-iii)
FELT_TRAJ_LOOKBACK = 3        # preceding 3-day gevoelscore mean

EXPECTED_BLOCK_LENGTH = 7     # E[L]=7 (permutation_null_block_length.md)
N_REPLICATES = 10000          # >= 10,000 per the locked pre-reg
RNG_SEED = 20260704           # fixed seed, recorded (pre-reg lock date)

# Column names (exact; abbreviated eff_exertion, not effective_exertion).
COL_PRIMARY_RAW = "max_hr"                                   # raw daily max HR
COL_PRIMARY_STORED = "max_hr_rank_lagged_lcera"             # stored un-masked rank
COL_COMPARISON = "eff_exertion_rank_lagged_lcera"           # activity-volume arm
COL_CUMULATIVE = "hr_area_above_daytime_baseline_waking_lcera"
COL_AUTO_STRESS = "stress_mean_sleep_lagged_lcera_z"        # autonomic-trend primary key
COL_AUTO_RHR = "resting_hr_lagged_lcera_z"                  # autonomic-trend second read

LINE = "-" * 72


# ----------------------------------------------------------------------------
# Lagged-rank recompute (the compute_lagged_rank algorithm; masked / un-masked)
# ----------------------------------------------------------------------------


def compute_lagged_rank_series(dates, values, is_crash, is_dip, *, mask_events):
    """Percentile-rank each day's value within its [d-90, d-30] LC-era pool.

    Exact reproduction of compute_lagged_rank from 11_compute_lagged_baseline.py:
    for each day d, the pool = days in [d-LAG_END, d-LAG_START] with date >=
    LCERA_START; require >= MIN_LAGGED_DAYS valid pool days; midrank-for-ties
    rank = (n_below + n_at_or_below) / (2 * n_pool). If mask_events is True the
    pool additionally excludes any is_crash or is_dip pool day (the pre-reg
    section 4e locked masked PRIMARY). Returns a dict date -> rank (or NaN).
    """
    dates = list(dates)
    valmap = dict(zip(dates, values))
    crashmap = dict(zip(dates, is_crash))
    dipmap = dict(zip(dates, is_dip))
    dset = set(dates)
    out = {}
    for d in dates:
        pool = []
        # window [d-LAG_END, d-LAG_START], mirroring the range(LAG_START+1, LAG_END+1)
        # of the original (days d-31 .. d-90 inclusive).
        for i in range(LAG_START_DAYS + 1, LAG_END_DAYS + 1):
            wd = d - pd.Timedelta(days=i)
            if wd < LCERA_START:
                continue
            if wd in dset:
                if mask_events and (crashmap[wd] or dipmap[wd]):
                    continue
                v = valmap[wd]
                if pd.notna(v):
                    pool.append(float(v))
        if len(pool) < MIN_LAGGED_DAYS:
            out[d] = np.nan
            continue
        today = valmap[d]
        if pd.isna(today):
            out[d] = np.nan
            continue
        today = float(today)
        below = sum(1 for v in pool if v < today)
        at_or_below = sum(1 for v in pool if v <= today)
        out[d] = (below + at_or_below) / (2 * len(pool))
    return out


# ----------------------------------------------------------------------------
# Event construction: crash nadirs, dip days, felt-recovery gate, danger window
# ----------------------------------------------------------------------------


def crash_nadirs(df):
    """t0 = min-gevoelscore day per crash episode (episodes with >= 1 is_crash day)."""
    nadirs = []
    for eid, g in df[df["crash_episode_id"].notna()].groupby("crash_episode_id"):
        if not g["is_crash"].any():
            continue
        gg = g.dropna(subset=["gevoelscore"])
        if len(gg) == 0:
            continue
        nrow = gg.loc[gg["gevoelscore"].idxmin()]
        nadirs.append((eid, nrow["date"]))
    nadirs.sort(key=lambda x: x[1])
    return nadirs


def dip_nadirs(df):
    """t0 = each is_dip day (transient single-bad-day events)."""
    return sorted(df.loc[df["is_dip"], "date"].tolist())


def felt_recovery_day(t0, gs_map):
    """First day in t+1..t+FELT_RECOVERY_LOOKAHEAD with gevoelscore >= gate."""
    for k in range(1, FELT_RECOVERY_LOOKAHEAD + 1):
        d = t0 + pd.Timedelta(days=k)
        v = gs_map.get(d)
        if v is not None and pd.notna(v) and v >= FELT_RECOVERY_GATE:
            return d
    return None


def danger_window_days(t0, window, gs_map, all_dates):
    """Danger window = felt-recovery day .. nadir+window (present rows only)."""
    fr = felt_recovery_day(t0, gs_map)
    if fr is None:
        return None
    end = t0 + pd.Timedelta(days=window)
    days = []
    d = fr
    while d <= end:
        if d in all_dates:
            days.append(d)
        d += pd.Timedelta(days=1)
    return days


def preceding_gs_mean(day, gs_map):
    """Mean gevoelscore over the FELT_TRAJ_LOOKBACK days strictly before `day`."""
    vals = []
    for k in range(1, FELT_TRAJ_LOOKBACK + 1):
        v = gs_map.get(day - pd.Timedelta(days=k))
        if v is not None and pd.notna(v):
            vals.append(float(v))
    if len(vals) == 0:
        return np.nan
    return float(np.mean(vals))


def relapse_after(peak_day, window, crash_map, dip_map, all_dates):
    """1 if a new crash OR dip occurs within `window` days AFTER peak_day.

    Peak strictly precedes the relapse (k = 1..window). Reads the is_crash /
    is_dip labels (a different data source from the HR / activity exposures).
    """
    for k in range(1, window + 1):
        d = peak_day + pd.Timedelta(days=k)
        if d in all_dates and (crash_map.get(d, False) or dip_map.get(d, False)):
            return 1
    return 0


# ----------------------------------------------------------------------------
# Danger-window peaks + matched-baseline pools
# ----------------------------------------------------------------------------


def _pick_peak(cand):
    """Max single-day rank; ties resolved to the EARLIEST calendar day.

    `cand` is a list of (date, rank). The compound key (rank, then
    negative-ordinal) makes the selection fully deterministic and independent
    of any set-hash iteration order. Returns (peak_day, peak_rank).
    """
    peak_day, peak_rank = max(cand, key=lambda x: (x[1], -x[0].toordinal()))
    return peak_day, peak_rank


def build_event_peaks(nadirs, rank_map, gs_map, crash_map, dip_map, all_dates,
                      *, window, relapse_window):
    """For each event, the danger-window PEAK exposure day + its relapse outcome.

    Returns a list of dicts (one per usable event): t0, felt_recovery_day,
    dw_days (set of danger-window dates), peak_day, peak_rank,
    peak_preceding_gs_mean, recovery_phase, relapse (0/1). Events with no
    felt-recovery day, no covered danger-window rank, or where every
    danger-window day lacks a rank are skipped (usable-event filter).
    """
    events = []
    for key, t0 in nadirs:
        dw = danger_window_days(t0, window, gs_map, all_dates)
        if dw is None:
            continue  # no felt-recovery day
        dw = sorted(dw)  # deterministic calendar order (no set-hash ordering)
        # PEAK = max single-day rank over the danger-window days (section 4b).
        # Ordering guard (section 4f, crude case): a peak day already in a
        # descending felt-state is excluded as an exposure candidate so a
        # relapse day is never counted as its own exposure. We treat a day whose
        # own gevoelscore drops below the felt-recovery gate (back into the
        # <= 3 crash/dip zone) as "descending" and drop it from the peak
        # candidate set. This keeps the felt-recovered danger-window state.
        # Tie-break (deterministic): candidates are scanned in ascending
        # calendar order, so a rank tie resolves to the EARLIEST day.
        cand = []
        for d in dw:
            r = rank_map.get(d)
            if r is None or pd.isna(r):
                continue
            gv = gs_map.get(d)
            # exclude days that have fallen back out of the felt-recovered band
            if gv is not None and pd.notna(gv) and gv < FELT_RECOVERY_GATE:
                continue
            cand.append((d, float(r)))
        if len(cand) == 0:
            continue  # no covered, felt-recovered danger-window day
        peak_day, peak_rank = _pick_peak(cand)
        events.append({
            "key": key,
            "t0": t0,
            "dw_days": dw,  # sorted list, calendar order
            "peak_day": peak_day,
            "peak_rank": peak_rank,
            "peak_preceding_gs_mean": preceding_gs_mean(peak_day, gs_map),
            "recovery_phase": None,  # filled by caller from phase_map
            "relapse": relapse_after(peak_day, relapse_window, crash_map, dip_map, all_dates),
        })
    return events


def matched_baseline_pool(peak, reference_days, rank_map, gs_map, phase_map,
                          crash_map, dip_map, all_dates, *, relapse_window):
    """All-eligible-in-caliper matched-baseline days for one danger-window peak.

    reference_days = LC-era days OUTSIDE any post-crash danger window. A day
    enters the pool iff ALL three calipers hold (section 4d):
      (i)   masked rank within +/- RANK_BAND_CALIPER of the peak rank;
      (ii)  same recovery_phase as the peak day;
      (iii) the baseline day's preceding-3-day gevoelscore mean within
            +/- FELT_TRAJ_CALIPER of the peak day's preceding-3-day mean.
    Each pooled day gets its own relapse outcome (new crash/dip within
    relapse_window days after it). Returns a list of relapse indicators (0/1).
    """
    outcomes = []
    peak_rank = peak["peak_rank"]
    peak_phase = peak["recovery_phase"]
    peak_traj = peak["peak_preceding_gs_mean"]
    for d in reference_days:
        r = rank_map.get(d)
        if r is None or pd.isna(r):
            continue
        if abs(float(r) - peak_rank) > RANK_BAND_CALIPER:
            continue
        if phase_map.get(d) != peak_phase:
            continue
        traj = preceding_gs_mean(d, gs_map)
        if pd.isna(traj) or pd.isna(peak_traj):
            continue
        if abs(traj - peak_traj) > FELT_TRAJ_CALIPER:
            continue
        outcomes.append(relapse_after(d, relapse_window, crash_map, dip_map, all_dates))
    return outcomes


# ----------------------------------------------------------------------------
# The one primary statistic + the event-level block-permutation null
# ----------------------------------------------------------------------------


def primary_statistic(deltas):
    """Standardised mean of delta_i across events (the ONE primary statistic).

    delta_i = (danger-window relapse 0/1) - (matched-baseline mean relapse rate).
    Standardised = mean(delta) / (sd(delta) / sqrt(n)); i.e. a one-sample
    t-type standardised mean. Returns NaN if sd is 0.
    """
    d = np.asarray(deltas, dtype=float)
    d = d[~np.isnan(d)]
    if len(d) < 2:
        return float("nan")
    sd = d.std(ddof=1)
    if sd == 0:
        return float("nan")
    return float(d.mean() / (sd / np.sqrt(len(d))))


def rank_slope(peak_ranks, deltas):
    """Relapse-excess (delta) regressed on peak-rank magnitude; OLS slope."""
    x = np.asarray(peak_ranks, dtype=float)
    y = np.asarray(deltas, dtype=float)
    ok = ~(np.isnan(x) | np.isnan(y))
    x, y = x[ok], y[ok]
    if len(x) < 2 or x.std() == 0:
        return float("nan")
    slope, _ = np.polyfit(x, y, 1)
    return float(slope)


def block_permutation_null(events, baseline_outcomes_per_event, *, e_l, n_replicates, rng):
    """Event-level block-permutation null for the primary statistic + rank-slope.

    Pooled labelled units = the 28 danger-window peaks (label = danger-window)
    plus their matched-baseline days (label = baseline). Each replicate permutes
    which pooled units carry the danger-window label under stationary calendar
    blocks at E[L] (holding each unit's relapse outcome + peak magnitude fixed),
    then recomputes the one primary statistic. Mirrors the sibling test's
    stationary-block mechanic (_stationary_bootstrap_indices) applied to the
    permuted LABEL assignment.

    Construction: build one calendar-ordered pooled table of (date, outcome,
    magnitude) where the danger-window peaks and all matched-baseline days are
    interleaved by date. The observed labelling assigns "danger-window" to the
    peaks. Each replicate draws a stationary-block index permutation of the
    label vector (blocks of contiguous calendar units move together, respecting
    within-block autocorrelation), reassigns the fixed count of danger-window
    labels to the permuted positions, and recomputes the primary statistic as
    if those positions were the danger-window events.
    """
    # Pooled calendar-ordered table.
    rows = []
    for ev in events:
        rows.append({"date": ev["peak_day"], "outcome": ev["relapse"],
                     "magnitude": ev["peak_rank"], "is_dw": 1,
                     "event_key": ev["key"]})
    for ev, outs in zip(events, baseline_outcomes_per_event):
        # baseline days do not carry their own date here (pool is per-event);
        # to respect calendar-block structure we still need a date. The matched
        # pool relapse outcomes are stored with their day so we can order them.
        for (bdate, bout, bmag) in outs:
            rows.append({"date": bdate, "outcome": bout, "magnitude": bmag,
                         "is_dw": 0, "event_key": ev["key"]})
    pooled = pd.DataFrame(rows).sort_values("date").reset_index(drop=True)
    n = len(pooled)
    outcomes = pooled["outcome"].to_numpy(dtype=float)
    magnitudes = pooled["magnitude"].to_numpy(dtype=float)
    keys = pooled["event_key"].to_numpy()
    n_dw = int(pooled["is_dw"].sum())

    # Observed statistic recomputed on the pooled table (identical construction
    # to the direct estimate, used as the reference point in the null).
    def stat_for_labels(dw_mask):
        deltas = []
        pranks = []
        # For each event, delta = (mean dw outcome for that event's dw-labelled
        # units) - (mean outcome of that event's baseline-labelled units). With
        # the label permutation, an event's dw label may fall on different
        # pooled positions; we recompute per event_key using the permuted mask.
        for ev in events:
            k = ev["key"]
            sel = keys == k
            dw_sel = sel & dw_mask
            bl_sel = sel & (~dw_mask)
            if dw_sel.sum() == 0 or bl_sel.sum() == 0:
                continue
            dw_rate = outcomes[dw_sel].mean()
            bl_rate = outcomes[bl_sel].mean()
            deltas.append(dw_rate - bl_rate)
            pranks.append(magnitudes[dw_sel].mean())
        return primary_statistic(deltas), rank_slope(pranks, deltas)

    # Observed labelling: dw units are exactly is_dw == 1.
    obs_mask = pooled["is_dw"].to_numpy(dtype=bool)
    obs_stat, obs_slope = stat_for_labels(obs_mask)

    p = 1.0 / e_l
    null_stats = np.empty(n_replicates)
    null_slopes = np.empty(n_replicates)
    for b in range(n_replicates):
        # Stationary-block permutation of positions: draw a block-structured
        # index order, then assign the first n_dw positions (in that permuted
        # order) the danger-window label. Blocks keep contiguous calendar units
        # together so within-window autocorrelation is respected.
        perm_idx = _stationary_bootstrap_indices(n, p, rng)
        # Unique-ify while preserving block order: the stationary bootstrap draws
        # with replacement, so take the permuted order and assign dw labels to
        # the first n_dw DISTINCT positions encountered.
        seen = set()
        dw_positions = []
        for pos in perm_idx:
            if pos not in seen:
                seen.add(pos)
                dw_positions.append(pos)
                if len(dw_positions) >= n_dw:
                    break
        # If the block draw did not surface n_dw distinct positions (rare),
        # fill remaining from the unseen positions in calendar order.
        if len(dw_positions) < n_dw:
            for pos in range(n):
                if pos not in seen:
                    dw_positions.append(pos)
                    if len(dw_positions) >= n_dw:
                        break
        mask = np.zeros(n, dtype=bool)
        mask[np.asarray(dw_positions, dtype=int)] = True
        s, sl = stat_for_labels(mask)
        null_stats[b] = s
        null_slopes[b] = sl

    return {
        "obs_stat": obs_stat,
        "obs_slope": obs_slope,
        "null_stats": null_stats,
        "null_slopes": null_slopes,
    }


# ----------------------------------------------------------------------------
# Direct estimate (observed primary statistic + rank-slope from the pools)
# ----------------------------------------------------------------------------


def direct_estimate(events, baseline_outcomes_per_event):
    """Observed delta_i, the standardised primary statistic, and rank-slope.

    delta_i = (danger-window relapse 0/1) - (mean relapse rate of matched pool).
    Events whose matched pool is empty are excluded from the primary statistic
    (their delta is undefined). Returns the statistic bundle + per-event detail.
    """
    deltas = []
    peak_ranks = []
    pool_sizes = []
    detail = []
    for ev, outs in zip(events, baseline_outcomes_per_event):
        pool_sizes.append(len(outs))
        if len(outs) == 0:
            detail.append({**{k: ev[k] for k in ("key", "peak_day", "peak_rank", "relapse")},
                           "pool_size": 0, "pool_rate": float("nan"), "delta": float("nan")})
            continue
        pool_rate = float(np.mean([o for (_, o, _) in outs]))
        delta = ev["relapse"] - pool_rate
        deltas.append(delta)
        peak_ranks.append(ev["peak_rank"])
        detail.append({**{k: ev[k] for k in ("key", "peak_day", "peak_rank", "relapse")},
                       "pool_size": len(outs), "pool_rate": pool_rate, "delta": delta})
    return {
        "deltas": deltas,
        "peak_ranks": peak_ranks,
        "pool_sizes": pool_sizes,
        "stat": primary_statistic(deltas),
        "slope": rank_slope(peak_ranks, deltas),
        "n_used": len(deltas),
        "detail": detail,
    }


# ----------------------------------------------------------------------------
# Reference-day universe (LC-era days outside ANY post-crash danger window)
# ----------------------------------------------------------------------------


def reference_universe(df, all_crash_dw_days):
    """LC-era days with a masked rank, EXCLUDING any post-crash danger-window day.

    LC-era = lc_phase == 'lc' (exactly where the _lcera rank is defined). The
    exclusion removes every crash danger-window day (all windows, across the
    sensitivity band's max length so no window day leaks in). Returns a list of
    dates.
    """
    lc = df[df["lc_phase"] == "lc"]
    return [d for d in lc["date"].tolist() if d not in all_crash_dw_days]


# ----------------------------------------------------------------------------
# Main
# ----------------------------------------------------------------------------


def main():
    rng = np.random.default_rng(RNG_SEED)

    df = pd.read_csv(DATA_PATH, low_memory=False)
    df["date"] = pd.to_datetime(df["date"])
    df = df.sort_values("date").reset_index(drop=True)
    df["is_crash"] = df["is_crash"].astype(bool)
    df["is_dip"] = df["is_dip"].astype(bool)

    dates = df["date"].tolist()
    gs_map = dict(zip(df["date"], df["gevoelscore"]))
    crash_map = dict(zip(df["date"], df["is_crash"]))
    dip_map = dict(zip(df["date"], df["is_dip"]))
    phase_map = dict(zip(df["date"], df["recovery_phase"]))
    all_dates = set(dates)

    # --- 0. Reproduction check (section 4e-2): recompute UN-masked rank ---
    recomp_unmasked = compute_lagged_rank_series(
        df["date"], df[COL_PRIMARY_RAW], df["is_crash"], df["is_dip"], mask_events=False
    )
    df["recomp_unmasked"] = df["date"].map(recomp_unmasked)
    repro = df.dropna(subset=[COL_PRIMARY_STORED, "recomp_unmasked"])
    repro_corr = float(repro[COL_PRIMARY_STORED].corr(repro["recomp_unmasked"]))
    repro_maxdiff = float((repro[COL_PRIMARY_STORED] - repro["recomp_unmasked"]).abs().max())
    repro_meandiff = float((repro[COL_PRIMARY_STORED] - repro["recomp_unmasked"]).abs().mean())
    repro_source = "raw max_hr column in per_day_master.csv"

    # --- 1. Masked-primary recompute (section 4e): the locked PRIMARY exposure ---
    masked_rank = compute_lagged_rank_series(
        df["date"], df[COL_PRIMARY_RAW], df["is_crash"], df["is_dip"], mask_events=True
    )
    df["max_hr_rank_masked"] = df["date"].map(masked_rank)
    rank_map = masked_rank                                    # PRIMARY exposure map
    stored_rank_map = dict(zip(df["date"], df[COL_PRIMARY_STORED]))  # un-masked sensitivity
    comp_map = dict(zip(df["date"], df[COL_COMPARISON]))     # activity-volume arm
    cum_map = dict(zip(df["date"], df[COL_CUMULATIVE]))
    auto_stress_map = dict(zip(df["date"], df[COL_AUTO_STRESS]))
    auto_rhr_map = dict(zip(df["date"], df[COL_AUTO_RHR]))

    # --- 2. Events ---
    crashes = crash_nadirs(df)
    dips = [(d, d) for d in dip_nadirs(df)]  # (key, t0); key = the dip day itself
    n_crash_felt = sum(1 for _, t0 in crashes if felt_recovery_day(t0, gs_map) is not None)
    n_dip_felt = sum(1 for _, t0 in dips if felt_recovery_day(t0, gs_map) is not None)

    # danger-window day universe across the widest sensitivity window (14),
    # so the reference set excludes any day that is a danger-window day at any
    # band length (no leakage of a window day into the baseline).
    all_crash_dw_days = set()
    for _, t0 in crashes:
        dw = danger_window_days(t0, max(DANGER_WINDOW_BAND), gs_map, all_dates)
        if dw:
            all_crash_dw_days.update(dw)

    ref_days = reference_universe(df, all_crash_dw_days)

    # ------------------------------------------------------------------
    # A reusable runner: build peaks + matched pools + estimate, for a given
    # arm (rank map), window, relapse window, and (optionally) a day-filter.
    # ------------------------------------------------------------------
    def run_arm(nadirs, arm_rank_map, *, window, relapse_window, ref_universe,
                day_filter=None, label=""):
        peaks = build_event_peaks(
            nadirs, arm_rank_map, gs_map, crash_map, dip_map, all_dates,
            window=window, relapse_window=relapse_window,
        )
        # apply optional day filter to the peak candidate set (autonomic-trend)
        if day_filter is not None:
            filtered = []
            for ev in peaks:
                # recompute the peak over the filtered danger-window days
                cand = []
                for d in sorted(ev["dw_days"]):
                    r = arm_rank_map.get(d)
                    if r is None or pd.isna(r):
                        continue
                    gv = gs_map.get(d)
                    if gv is not None and pd.notna(gv) and gv < FELT_RECOVERY_GATE:
                        continue
                    if not day_filter(d):
                        continue
                    cand.append((d, float(r)))
                if not cand:
                    continue
                pd_day, pr = _pick_peak(cand)
                ev = dict(ev)
                ev["peak_day"] = pd_day
                ev["peak_rank"] = pr
                ev["peak_preceding_gs_mean"] = preceding_gs_mean(pd_day, gs_map)
                ev["relapse"] = relapse_after(pd_day, relapse_window, crash_map, dip_map, all_dates)
                filtered.append(ev)
            peaks = filtered
        # fill recovery_phase for each peak day
        for ev in peaks:
            ev["recovery_phase"] = phase_map.get(ev["peak_day"])
        # matched-baseline pools, carrying (date, outcome, magnitude) per pool day
        baseline_outcomes = []
        for ev in peaks:
            pool = []
            for d in ref_universe:
                r = arm_rank_map.get(d)
                if r is None or pd.isna(r):
                    continue
                if abs(float(r) - ev["peak_rank"]) > RANK_BAND_CALIPER:
                    continue
                if phase_map.get(d) != ev["recovery_phase"]:
                    continue
                traj = preceding_gs_mean(d, gs_map)
                if pd.isna(traj) or pd.isna(ev["peak_preceding_gs_mean"]):
                    continue
                if abs(traj - ev["peak_preceding_gs_mean"]) > FELT_TRAJ_CALIPER:
                    continue
                pool.append((d, relapse_after(d, relapse_window, crash_map, dip_map, all_dates), float(r)))
            baseline_outcomes.append(pool)
        est = direct_estimate(peaks, baseline_outcomes)
        return peaks, baseline_outcomes, est

    # ==================================================================
    # PRIMARY: masked max_hr rank x crash arm x 10-day window x 4-day relapse
    # ==================================================================
    peaks, baseline_outcomes, est = run_arm(
        crashes, rank_map, window=DANGER_WINDOW_PRIMARY, relapse_window=RELAPSE_PRIMARY,
        ref_universe=ref_days, label="PRIMARY",
    )

    # matched-baseline pool sizes actually constructed
    pool_sizes = [len(o) for o in baseline_outcomes]
    pool_min = min(pool_sizes) if pool_sizes else 0
    pool_med = int(np.median(pool_sizes)) if pool_sizes else 0
    pool_max = max(pool_sizes) if pool_sizes else 0
    n_empty_pool = sum(1 for s in pool_sizes if s == 0)

    # --- 7. ACF readout + data-driven E[L]* companion (section 6) ---
    masked_series = df["max_hr_rank_masked"].to_numpy(dtype=float)
    el_result = compute_data_driven_block_length(
        masked_series, default_block_length=EXPECTED_BLOCK_LENGTH
    )
    el_star = el_result["optimal_block_length"]
    el_flagged = el_result["flagged_deviation"]
    el_used = el_star if el_flagged else EXPECTED_BLOCK_LENGTH
    acf = el_result.get("autocorrelations")
    acf1 = float(acf[1]) if acf is not None and len(acf) > 1 else float("nan")
    acf7 = float(acf[7]) if acf is not None and len(acf) > 7 else float("nan")

    # --- 6+7. Event-level block-permutation null on the primary statistic ---
    null_res = block_permutation_null(
        peaks, baseline_outcomes, e_l=el_used, n_replicates=N_REPLICATES, rng=rng
    )
    null_stats = null_res["null_stats"]
    null_stats_valid = null_stats[~np.isnan(null_stats)]
    obs_stat = est["stat"]
    # percentile of the observed statistic within the null (two-sided reading:
    # report the one-sided upper-tail p-analogue in the predicted positive
    # direction, plus the two-sided percentile for the CI).
    p_upper = float(np.mean(null_stats_valid >= obs_stat))
    percentile = float(np.mean(null_stats_valid <= obs_stat)) * 100.0
    ci_low = float(np.quantile(null_stats_valid, 0.025))
    ci_high = float(np.quantile(null_stats_valid, 0.975))

    null_slopes = null_res["null_slopes"]
    null_slopes_valid = null_slopes[~np.isnan(null_slopes)]
    obs_slope = est["slope"]
    slope_ci_low = float(np.quantile(null_slopes_valid, 0.025))
    slope_ci_high = float(np.quantile(null_slopes_valid, 0.975))
    slope_p_upper = float(np.mean(null_slopes_valid >= obs_slope))

    # --- Verdict (section 10): Supported / Not supported / Cannot resolve ---
    # "Cannot resolve" (CI spanning the null, i.e. spanning 0) is the
    # pre-committed default reading. Supported only if the CI excludes 0 in the
    # predicted positive direction.
    if np.isnan(obs_stat):
        verdict = "Cannot resolve"
    elif ci_low > 0.0:
        verdict = "Supported"
    elif ci_high < 0.0:
        verdict = "Not supported"
    else:
        verdict = "Cannot resolve"

    # ==================================================================
    # 8. Crash-vs-dip formal slope interaction (secondary)
    # ==================================================================
    dip_peaks, dip_baseline, dip_est = run_arm(
        dips, rank_map, window=DANGER_WINDOW_PRIMARY, relapse_window=RELAPSE_PRIMARY,
        ref_universe=ref_days, label="DIP",
    )
    # slope interaction = crash slope - dip slope (base-rate-conditioned via the
    # matched-baseline delta, which subtracts each arm's own base rate).
    crash_slope = est["slope"]
    dip_slope = dip_est["slope"]
    slope_interaction = (crash_slope - dip_slope
                         if not (np.isnan(crash_slope) or np.isnan(dip_slope))
                         else float("nan"))

    # ==================================================================
    # 9. Activity-volume COMPARISON arm (eff_exertion), crash, same window/relapse
    # ==================================================================
    comp_peaks, comp_baseline, comp_est = run_arm(
        crashes, comp_map, window=DANGER_WINDOW_PRIMARY, relapse_window=RELAPSE_PRIMARY,
        ref_universe=ref_days, label="COMPARISON",
    )

    # ==================================================================
    # 10. Cumulative-strain SECONDARY (hr_area danger-window aggregate)
    # ==================================================================
    # The cumulative exposure is the danger-window SUM of hr_area; it is not a
    # single-day peak, so it is contrasted as a per-event dose regressed on the
    # danger-window relapse indicator (delta vs matched-baseline is not defined
    # the same way, so this secondary reports the danger-window relapse rate's
    # dependence on the cumulative dose, disclosed in result.md as the
    # autonomic-conflation caveat, section 9c).
    cum_doses = []
    cum_relapse = []
    for ev in peaks:  # reuse the masked-primary usable events + their windows
        dose = 0.0
        n_cov = 0
        for d in ev["dw_days"]:
            v = cum_map.get(d)
            if v is not None and pd.notna(v):
                dose += float(v)
                n_cov += 1
        if n_cov == 0:
            continue
        cum_doses.append(dose)
        cum_relapse.append(ev["relapse"])
    if len(cum_doses) >= 2 and np.std(cum_doses) > 0:
        cum_slope = float(np.polyfit(cum_doses, cum_relapse, 1)[0])
        cum_corr = float(np.corrcoef(cum_doses, cum_relapse)[0, 1])
    else:
        cum_slope = float("nan")
        cum_corr = float("nan")

    # ==================================================================
    # 11. Sensitivities
    # ==================================================================
    # 11a. Danger-window band 7 / 10 / 14
    window_sens = {}
    for w in DANGER_WINDOW_BAND:
        _, bo, e = run_arm(crashes, rank_map, window=w, relapse_window=RELAPSE_PRIMARY,
                           ref_universe=ref_days, label=f"win{w}")
        window_sens[w] = {"stat": e["stat"], "slope": e["slope"], "n_used": e["n_used"]}

    # 11b. Relapse band 3 / 4 / 5
    relapse_sens = {}
    for rw in RELAPSE_BAND:
        _, bo, e = run_arm(crashes, rank_map, window=DANGER_WINDOW_PRIMARY, relapse_window=rw,
                           ref_universe=ref_days, label=f"rel{rw}")
        relapse_sens[rw] = {"stat": e["stat"], "slope": e["slope"], "n_used": e["n_used"]}

    # 11c. Masked (primary) vs un-masked (stored) exposure
    _, um_bo, um_est = run_arm(crashes, stored_rank_map, window=DANGER_WINDOW_PRIMARY,
                               relapse_window=RELAPSE_PRIMARY, ref_universe=ref_days,
                               label="UNMASKED")
    unmasked_sens = {"stat": um_est["stat"], "slope": um_est["slope"], "n_used": um_est["n_used"]}

    # 11d. Autonomic-trend exclusion: drop danger-window days whose autonomic
    # trend is already adverse (rising). "Rising" keyed to the z-value being
    # positive (above the lagged-lcera baseline) AND above its own value 1 day
    # prior (an upward move). Primary key = stress_mean_sleep_lagged_lcera_z;
    # second read = resting_hr_lagged_lcera_z. Runs on the covered subset.
    def make_rising_filter(zmap):
        def keep(d):
            z = zmap.get(d)
            zprev = zmap.get(d - pd.Timedelta(days=1))
            if z is None or pd.isna(z):
                return True  # uncovered day: retained (disclosed)
            rising = (z > 0) and (zprev is not None and pd.notna(zprev) and z > zprev)
            return not rising
        return keep

    _, as_bo, as_est = run_arm(
        crashes, rank_map, window=DANGER_WINDOW_PRIMARY, relapse_window=RELAPSE_PRIMARY,
        ref_universe=ref_days, day_filter=make_rising_filter(auto_stress_map),
        label="AUTOSTRESS",
    )
    _, ar_bo, ar_est = run_arm(
        crashes, rank_map, window=DANGER_WINDOW_PRIMARY, relapse_window=RELAPSE_PRIMARY,
        ref_universe=ref_days, day_filter=make_rising_filter(auto_rhr_map),
        label="AUTORHR",
    )
    auto_stress_cov = df["date"].isin(all_crash_dw_days).sum()  # informational
    auto_sens = {
        "stress": {"stat": as_est["stat"], "slope": as_est["slope"], "n_used": as_est["n_used"]},
        "rhr": {"stat": ar_est["stat"], "slope": ar_est["slope"], "n_used": ar_est["n_used"]},
    }

    # ------------------------------------------------------------------
    # Report
    # ------------------------------------------------------------------
    print(LINE)
    print("POST-CRASH EXERTION RELAPSE (danger window): TEST EXECUTION")
    print(LINE)
    print(f"RNG seed (recorded): {RNG_SEED}  (only the block-permutation null uses it;")
    print("  the all-eligible-in-caliper matching has no random draw)")
    print(f"Replicates: {N_REPLICATES}   E[L] default: {EXPECTED_BLOCK_LENGTH}")
    print(f"Data rows: {len(df)}   date range {df['date'].min().date()} to {df['date'].max().date()}")
    print(LINE)
    print("0. REPRODUCTION CHECK (un-masked recompute vs stored max_hr_rank_lagged_lcera):")
    print(f"  source: {repro_source}")
    print(f"  n compared: {len(repro)}   correlation: {repro_corr:.6f}")
    print(f"  max abs diff: {repro_maxdiff:.6f}   mean abs diff: {repro_meandiff:.6f}")
    print("  (near-identical => the masked recompute is the same algorithm minus masking)")
    print(LINE)
    print("2. EVENTS:")
    print(f"  crash episodes: {len(crashes)}   with felt-recovery day: {n_crash_felt}")
    print(f"  dip days: {len(dips)}   with felt-recovery day: {n_dip_felt}")
    print(f"  usable crash events (primary): {est['n_used']} (of {len(peaks)} peaks built)")
    print(f"  usable dip events (mechanism-control): {dip_est['n_used']}")
    print(LINE)
    print("MATCHED-BASELINE POOL SIZES (per crash peak, primary arm):")
    print(f"  min={pool_min}  median={pool_med}  max={pool_max}  empty pools={n_empty_pool}")
    print(LINE)
    print("7. ACF / BLOCK LENGTH:")
    print(f"  masked-rank ACF: rho(1)={acf1:+.4f}  rho(7)={acf7:+.4f}")
    print(f"  data-driven E[L]*={el_star:.3f}  cutoff_lag={el_result.get('cutoff_lag')}")
    print(f"  factor-of-2 flag: {el_flagged}   E[L] used: {el_used:.3f}")
    print(LINE)
    print("6. PRIMARY STATISTIC (standardised danger-window-vs-matched-baseline difference):")
    print(f"  point estimate (standardised mean of delta_i): {obs_stat:+.4f}")
    print(f"  event-level block-permutation 95% CI: [{ci_low:+.4f}, {ci_high:+.4f}]")
    print(f"  p-analogue (upper tail, predicted +): {p_upper:.4f}   percentile: {percentile:.2f}")
    mean_delta = float(np.mean(est["deltas"])) if est["deltas"] else float("nan")
    print(f"  direction+magnitude: mean delta = {mean_delta:+.4f} "
          f"(dw relapse rate minus matched-baseline relapse rate)")
    print(f"  >>> VERDICT: {verdict}")
    print(LINE)
    print("6b. RANK-SLOPE READING (relapse-excess delta regressed on peak-rank magnitude):")
    print(f"  slope point: {obs_slope:+.4f}   95% CI: [{slope_ci_low:+.4f}, {slope_ci_high:+.4f}]"
          f"   p-analogue: {slope_p_upper:.4f}")
    print(LINE)
    print("8. CRASH-VS-DIP FORMAL SLOPE INTERACTION (secondary; 79 dips ~2.7x power of 28 crashes):")
    print(f"  crash rank-slope: {crash_slope:+.4f}   dip rank-slope: {dip_slope:+.4f}")
    print(f"  slope interaction (crash - dip): {slope_interaction:+.4f}")
    print(f"  crash primary stat: {est['stat']:+.4f}   dip primary stat: {dip_est['stat']:+.4f}")
    print(LINE)
    print("9. ACTIVITY-VOLUME COMPARISON ARM (eff_exertion; strain-vs-volume confound test):")
    print(f"  comparison primary stat: {comp_est['stat']:+.4f}   rank-slope: {comp_est['slope']:+.4f}"
          f"   n_used: {comp_est['n_used']}")
    print("  (does cardiac strain predict where activity volume does not?)")
    print(LINE)
    print("10. CUMULATIVE-STRAIN SECONDARY (hr_area danger-window aggregate; conflation disclosed):")
    print(f"  cumulative dose vs danger-window relapse: slope={cum_slope:+.6f}  corr={cum_corr:+.4f}"
          f"  n={len(cum_doses)}")
    print(LINE)
    print("11. SENSITIVITIES:")
    print("  11a. danger-window band 7/10/14 (stat / slope / n_used):")
    for w in DANGER_WINDOW_BAND:
        s = window_sens[w]
        print(f"       win={w:>2}: stat={s['stat']:+.4f}  slope={s['slope']:+.4f}  n={s['n_used']}")
    print("  11b. relapse band 3/4/5 (stat / slope / n_used):")
    for rw in RELAPSE_BAND:
        s = relapse_sens[rw]
        print(f"       rel={rw}: stat={s['stat']:+.4f}  slope={s['slope']:+.4f}  n={s['n_used']}")
    print("  11c. masked (primary) vs un-masked (stored) exposure:")
    print(f"       masked  : stat={est['stat']:+.4f}  slope={est['slope']:+.4f}  n={est['n_used']}")
    print(f"       unmasked: stat={unmasked_sens['stat']:+.4f}  slope={unmasked_sens['slope']:+.4f}"
          f"  n={unmasked_sens['n_used']}")
    print("  11d. autonomic-trend exclusion (drop rising-autonomic danger-window days):")
    print(f"       stress-key: stat={auto_sens['stress']['stat']:+.4f}  slope={auto_sens['stress']['slope']:+.4f}"
          f"  n={auto_sens['stress']['n_used']}")
    print(f"       rhr-2ndread: stat={auto_sens['rhr']['stat']:+.4f}  slope={auto_sens['rhr']['slope']:+.4f}"
          f"  n={auto_sens['rhr']['n_used']}")
    print(LINE)
    print("PER-EVENT DETAIL (primary arm; key, peak_day, peak_rank, relapse, pool_size, pool_rate, delta):")
    for row in est["detail"]:
        pr = row["peak_rank"]
        prate = row["pool_rate"]
        dlt = row["delta"]
        print(f"  {row['key']:>10}  {str(row['peak_day'].date())}  rank={pr:.3f}  "
              f"relapse={row['relapse']}  pool={row['pool_size']:>3}  "
              f"pool_rate={('nan' if np.isnan(prate) else f'{prate:.3f}')}  "
              f"delta={('nan' if np.isnan(dlt) else f'{dlt:+.3f}')}")
    print(LINE)

    return {
        "verdict": verdict,
        "repro_corr": repro_corr,
        "repro_maxdiff": repro_maxdiff,
        "n_crash_used": est["n_used"],
        "n_dip_used": dip_est["n_used"],
        "primary_stat": obs_stat,
        "primary_ci": (ci_low, ci_high),
        "p_analogue": p_upper,
        "rank_slope": obs_slope,
        "rank_slope_ci": (slope_ci_low, slope_ci_high),
        "el_star": el_star,
        "el_used": el_used,
        "el_flagged": el_flagged,
        "pool_sizes": (pool_min, pool_med, pool_max),
        "slope_interaction": slope_interaction,
        "comparison_stat": comp_est["stat"],
        "cumulative_slope": cum_slope,
        "window_sens": window_sens,
        "relapse_sens": relapse_sens,
        "unmasked_sens": unmasked_sens,
        "auto_sens": auto_sens,
    }


if __name__ == "__main__":
    main()
