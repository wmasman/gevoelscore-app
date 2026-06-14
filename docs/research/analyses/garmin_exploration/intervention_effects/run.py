"""
Intervention-effect descriptive characterisation.

Per docs/research/methodology/intervention_effects_descriptive.md.

Reads per_day_master.csv + annotations.yaml; emits one PNG per
(intervention, channel) pair + summary.csv with one row per
(intervention, channel, transition_buffer_days).

Run:
    GEVOELSCORE_DATA_PATH=/c/Users/Gebruiker/Documents/gevoelscore-data python run.py
or with the env var set in the parent shell.
"""

from pathlib import Path
import os
import sys
import yaml
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import mannwhitneyu


DATA = Path(os.environ.get("GEVOELSCORE_DATA_PATH",
                           r"C:\Users\Gebruiker\Documents\gevoelscore-data"))
if not DATA.exists():
    print(f"ERROR: data path not found: {DATA}", file=sys.stderr)
    sys.exit(1)

OUT = DATA / "analyses" / "intervention_effects"
(OUT / "plots").mkdir(parents=True, exist_ok=True)


# 1. Load per_day_master + annotations
master = pd.read_csv(DATA / "unified" / "per_day_master.csv", parse_dates=["date"])
master = master.set_index("date").sort_index()

annot = yaml.safe_load(
    (DATA / "raw" / "directus_exports" / "annotations.yaml").read_text(encoding="utf-8")
)


# 2. CURATED EXCLUDE LIST (Session C 2026-06-14)
# The interventie category in annotations.yaml is not homogeneous; some entries are
# administrative (Verwijzing), ad-hoc (Naproxen), wachtlijst-overbrugging (Fysiotherapie),
# session-events not steady-state regimes (Breathwork markers), or directly confounded
# with another intervention's boundary (Breinvoeding overlaps citalopram scale-down).
# These are excluded by label keyword.
EXCLUDE_LABEL_KEYWORDS = [
    "fysiotherapie",        # overbrugging wachtlijst, not analytical
    "naproxen",             # ad-hoc reactive use, not steady-state regime
    "breinvoeding",         # confounded with citalopram scale-down (10d apart)
    "verwijzing",           # administrative event, single-day
    "breathwork",           # session-event marker, not intervention regime
]


def _excluded(label):
    low = label.lower()
    return any(k in low for k in EXCLUDE_LABEL_KEYWORDS)


# 3. Extract interventie markers + span boundaries WITH CONTAINMENT FILTER.
# Containment filter: keep only "umbrella" spans (NOT contained in another interventie span),
# so e.g. the 6 citalopram dose-level sub-phases are collapsed automatically. Markers bypass
# the filter, so the 2 phase-transition markers (buildup->consolidation, consolidation->scale-down)
# are picked up explicitly.

int_spans_raw = [s for s in annot.get("spans", []) if s.get("category") == "interventie"]


def _span_bounds(s):
    return pd.Timestamp(s["start"]), pd.Timestamp(s.get("end") or s["start"])


def is_contained_in(small, big):
    if small is big:
        return False
    s_start, s_end = _span_bounds(small)
    b_start, b_end = _span_bounds(big)
    return (
        s_start >= b_start and s_end <= b_end
        and (s_start, s_end) != (b_start, b_end)
    )


umbrella_spans = [
    s for s in int_spans_raw
    if not any(is_contained_in(s, other) for other in int_spans_raw)
]

raw = []
n_excluded_markers = 0
n_excluded_spans = 0
for m in annot.get("markers", []):
    if m.get("category") != "interventie":
        continue
    if _excluded(m["label"]):
        n_excluded_markers += 1
        continue
    raw.append((m["label"], pd.Timestamp(m["date"])))
for s in umbrella_spans:
    if _excluded(s["label"]):
        n_excluded_spans += 1
        continue
    raw.append((f"{s['label']} (start)", pd.Timestamp(s["start"])))
    if s.get("end"):
        raw.append((f"{s['label']} (end)", pd.Timestamp(s["end"])))


# 3b. Dedupe by date: umbrella-and-sub-phase overlap + chained sub-phase boundaries would
# otherwise double-count if any survived. Merge overlapping labels into a single "/"-separated
# label per unique date.
by_date = {}
for label, d in raw:
    by_date.setdefault(d, []).append(label)
interventions = [
    (" / ".join(sorted(set(labels))), d)
    for d, labels in sorted(by_date.items())
]

print(f"Curated catalog: {len(interventions)} boundary dates")
print(f"  (excluded: {n_excluded_markers} markers, {n_excluded_spans} spans by keyword)")
for label, d in interventions:
    print(f"  {d.date()}: {label}")
print()


# 4. Channels of interest -- baseline channels (MD section 3) + outcome channel (MD section 3b).
# gevoelscore is methodologically distinct (outcome contamination, not baseline shift) --
# see MD section 3b for why it's grouped with baseline channels operationally but read separately
# in the findings.
CHANNELS = [
    "resting_hr", "bb_overnight_gain", "bb_lowest",
    "all_day_stress_avg", "stress_mean_sleep",
    "sleep_efficiency", "respiration_avg_sleep",
    "gevoelscore",
]

# Verify channels exist
present_channels = [c for c in CHANNELS if c in master.columns]
missing_channels = [c for c in CHANNELS if c not in master.columns]
if missing_channels:
    print(f"WARNING: missing channels in master: {missing_channels}")
print(f"Present channels: {present_channels}")
print()


# 5. Sensitivity-sweep + statistical-descriptors config + helpers
TRANSITION_BUFFERS = [7, 14, 28, 42]
PRIMARY_BUFFER     = 14
N_BOOTSTRAP        = 1000
BLOCK_LEN          = 7
RNG_SEED           = 20260614

rng = np.random.default_rng(RNG_SEED)


def windows_for(d, d_prev, d_next, B):
    pre_start  = max(d - pd.Timedelta(days=30), d_prev + pd.Timedelta(days=B + 1))
    pre_end    = d - pd.Timedelta(days=1)
    post_start = d + pd.Timedelta(days=B + 1)
    post_end   = min(d + pd.Timedelta(days=60), d_next - pd.Timedelta(days=1))
    return pre_start, pre_end, post_start, post_end


def rank_biserial(u, n_pre, n_post):
    return 2.0 * u / (n_pre * n_post) - 1.0


def bootstrap_median_diff_ci(pre_arr, post_arr, n_boot, rng_local, alpha=0.05):
    diffs = np.empty(n_boot)
    n_pre, n_post = len(pre_arr), len(post_arr)
    for i in range(n_boot):
        ps = rng_local.choice(pre_arr,  size=n_pre,  replace=True)
        po = rng_local.choice(post_arr, size=n_post, replace=True)
        diffs[i] = np.median(po) - np.median(ps)
    lo, hi = np.percentile(diffs, [100 * alpha / 2, 100 * (1 - alpha / 2)])
    return float(lo), float(hi)


def block_bootstrap_p(pre_arr, post_arr, obs_u, n_boot, block_len, rng_local):
    """
    Two-tailed block-permutation p for Mann-Whitney U.
    Concatenate (pre, post); form fixed-length blocks (last block may be short);
    shuffle blocks; re-split into pre/post by original sizes; recompute U.
    Compare |U_perm - n_pre*n_post/2| against |obs_u - n_pre*n_post/2|.
    Preserves within-block autocorrelation -> robust to daily autocorrelation
    that inflates the asymptotic Mann-Whitney p.
    """
    combined = np.concatenate([pre_arr, post_arr])
    n_pre, n_post = len(pre_arr), len(post_arr)
    n_total = len(combined)
    n_full_blocks = n_total // block_len
    null_centre = n_pre * n_post / 2.0
    obs_dev = abs(obs_u - null_centre)
    count = 0
    for _ in range(n_boot):
        blocks = [combined[i * block_len:(i + 1) * block_len] for i in range(n_full_blocks)]
        if n_total % block_len:
            blocks.append(combined[n_full_blocks * block_len:])
        rng_local.shuffle(blocks)
        permuted  = np.concatenate(blocks)
        perm_pre  = permuted[:n_pre]
        perm_post = permuted[n_pre:]
        u_perm, _ = mannwhitneyu(perm_pre, perm_post, alternative="two-sided")
        if abs(u_perm - null_centre) >= obs_dev - 1e-9:
            count += 1
    return count / n_boot


def linear_detrend_on_pre(pre_series, post_series, d):
    """
    Fit a linear trend on the pre-window (x = days from d), extrapolate forward
    through the post-window, and subtract from both pre and post values.
    Returns (pre_detrended_arr, post_detrended_arr).

    Closes the recovery-trajectory confound at the column level per CONVENTIONS section 3.7.
    A step that survives detrending is more credibly event-driven; a step that
    disappears under detrending was the underlying trend leaking through.
    """
    pre_x  = np.array([(idx - d).days for idx in pre_series.index],  dtype=float)
    post_x = np.array([(idx - d).days for idx in post_series.index], dtype=float)
    slope, intercept = np.polyfit(pre_x, pre_series.values, deg=1)
    pre_trend  = slope * pre_x  + intercept
    post_trend = slope * post_x + intercept
    return pre_series.values - pre_trend, post_series.values - post_trend


# 6. Per-pair analysis -- neighbour-truncated windows + buffer sweep
sorted_dates = sorted({d for _, d in interventions})
SENTINEL_PREV = pd.Timestamp("1970-01-01")
SENTINEL_NEXT = pd.Timestamp("2099-12-31")

rows = []
for label, d in interventions:
    idx    = sorted_dates.index(d)
    d_prev = sorted_dates[idx - 1] if idx > 0                       else SENTINEL_PREV
    d_next = sorted_dates[idx + 1] if idx < len(sorted_dates) - 1   else SENTINEL_NEXT

    for ch in present_channels:
        # 6a. Buffer sweep -- one row per (intervention, channel, buffer)
        for B in TRANSITION_BUFFERS:
            pre_start, pre_end, post_start, post_end = windows_for(d, d_prev, d_next, B)
            pre  = master.loc[pre_start:pre_end,   ch].dropna()
            post = master.loc[post_start:post_end, ch].dropna()
            pre_window_days  = (pre_end  - pre_start).days  + 1
            post_window_days = (post_end - post_start).days + 1

            base = {
                "intervention": label, "intervention_date": d, "channel": ch,
                "transition_buffer_days": B,
                "is_primary_buffer": (B == PRIMARY_BUFFER),
                "n_pre":  len(pre),  "pre_window_days":  pre_window_days,
                "n_post": len(post), "post_window_days": post_window_days,
            }

            if len(pre) < 5 or len(post) < 5:
                rows.append({
                    **base,
                    "median_pre": np.nan, "iqr_pre": np.nan,
                    "median_post": np.nan, "iqr_post": np.nan,
                    "median_diff": np.nan,
                    "median_diff_ci_lo": np.nan, "median_diff_ci_hi": np.nan,
                    "mw_u": np.nan, "mw_p": np.nan,
                    "mw_p_block_bootstrap": np.nan,
                    "mw_p_after_linear_detrend": np.nan,
                    "r_rb": np.nan,
                })
                continue

            pre_arr  = pre.values
            post_arr = post.values
            u, p = mannwhitneyu(pre_arr, post_arr, alternative="two-sided")
            mdiff       = float(np.median(post_arr) - np.median(pre_arr))
            ci_lo, ci_hi = bootstrap_median_diff_ci(pre_arr, post_arr, N_BOOTSTRAP, rng)
            p_block     = block_bootstrap_p(pre_arr, post_arr, u, N_BOOTSTRAP, BLOCK_LEN, rng)
            rrb         = rank_biserial(u, len(pre_arr), len(post_arr))

            pre_dt, post_dt = linear_detrend_on_pre(pre, post, d)
            _, p_detrend    = mannwhitneyu(pre_dt, post_dt, alternative="two-sided")

            rows.append({
                **base,
                "median_pre":  float(np.median(pre_arr)),
                "iqr_pre":     float(np.quantile(pre_arr, 0.75) - np.quantile(pre_arr, 0.25)),
                "median_post": float(np.median(post_arr)),
                "iqr_post":    float(np.quantile(post_arr, 0.75) - np.quantile(post_arr, 0.25)),
                "median_diff": mdiff,
                "median_diff_ci_lo": ci_lo, "median_diff_ci_hi": ci_hi,
                "mw_u": float(u), "mw_p": float(p),
                "mw_p_block_bootstrap": float(p_block),
                "mw_p_after_linear_detrend": float(p_detrend),
                "r_rb": float(rrb),
            })

        # 6b. Plot once per (intervention, channel) at primary buffer
        prim_pre_start, prim_pre_end, prim_post_start, prim_post_end = windows_for(
            d, d_prev, d_next, PRIMARY_BUFFER)
        prim_pre_days  = (prim_pre_end  - prim_pre_start).days  + 1
        prim_post_days = (prim_post_end - prim_post_start).days + 1

        win = master.loc[d - pd.Timedelta(days=30):d + pd.Timedelta(days=60), ch]
        if win.dropna().empty:
            continue
        fig, ax = plt.subplots(figsize=(10, 3))
        ax.plot(win.index, win.values, marker=".", linestyle="-", alpha=0.7)
        ax.axvline(d, color="red", linestyle="--", label=f"{label} {d.date()}")
        if d_prev > SENTINEL_PREV and d_prev >= d - pd.Timedelta(days=30):
            ax.axvline(d_prev, color="gray", linestyle=":", alpha=0.6,
                       label=f"prev: {d_prev.date()}")
        if d_next < SENTINEL_NEXT and d_next <= d + pd.Timedelta(days=60):
            ax.axvline(d_next, color="gray", linestyle=":", alpha=0.6,
                       label=f"next: {d_next.date()}")
        ax.set_title(f"{ch} around {label} "
                     f"(primary B={PRIMARY_BUFFER}; "
                     f"pre={prim_pre_days}d, post={prim_post_days}d)")
        ax.legend(fontsize=8)
        plt.tight_layout()
        safe_label = label
        for bad, repl in [
            (' ', '_'), ('/', '-'), (':', ''), (',', ''),
            ('<', 'lt'), ('>', 'gt'), ('"', ''), ('|', '-'),
            ('?', ''), ('*', ''), ('(', ''), (')', ''),
        ]:
            safe_label = safe_label.replace(bad, repl)
        plt.savefig(OUT / "plots" / f"{ch}__{safe_label}.png", dpi=100)
        plt.close()

pd.DataFrame(rows).to_csv(OUT / "summary.csv", index=False)
print(f"Wrote {len(rows)} (intervention, channel, buffer) rows to {OUT}/summary.csv")
print(f"Buffer sweep: {TRANSITION_BUFFERS}; primary = {PRIMARY_BUFFER}.")
print("Filter is_primary_buffer == True for the primary reading; "
      "other rows are sensitivity. Open PNGs and human-code transition_shape "
      "per pair using the primary row's stats for the no_visible_change pre-spec check.")
