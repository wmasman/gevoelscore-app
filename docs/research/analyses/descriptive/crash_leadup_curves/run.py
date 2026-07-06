"""R1 fresh per-timestep crash lead-up curves (single-pool, descriptive).

Produces the REAL lead-up shape the site's beat-2 charts wanted, honestly: for
each channel, the pooled t-6..t0 z-vs-lagged-baseline trajectory across all 29
crash episodes, with a null band (the same statistic over random ordinary-day
reference windows). This replaces the RETIRED per-era decay / early-vs-late
fabrications (chart-exports.md flags F1/F2) with a real, single-pool, descriptive
curve - no per-era split, no verdict, wide CI honesty at n=29.

Reuses the R14 lagged-baseline machinery verbatim (imported from
operationalisation_support/single_pool_reanchor/run.py): the same [d-90, d-30]
trimmed-mean/std personal baseline the locked crash operands use. The only new
thing is reading the z at EACH day-offset (t-6..t0) rather than the max over the
window.

Discipline: Layer-1 descriptive shape (no falsification bar, no new verdict);
single-pool (all 29 crashes pooled, no era split); baseline-relative (z vs the
personal lagged baseline, no dated raw values); aggregated per-offset means +
bootstrap CIs only. Per CONVENTIONS section 2.1 / 4.1.

Emits, on disk:
  - summary.json (research side; gitignored per docs/research/**/*.json rule)
  - the site chart JSONs under <SITE>/site/data/charts/ (for the user to commit
    from the site checkout): parasympathetic-swing, walls-of-orange, hrv-decline
    (fresh curves) + crash-frequency, exertion-lead-up (reframed from
    chart-exports.md). Set GEVOELSCORE_SITE_PATH to override the site location;
    if the site path is absent the site writes are skipped with a warning.

Run from repo root:
    python docs/research/analyses/descriptive/crash_leadup_curves/run.py
"""
from __future__ import annotations

import importlib.util
import json
import os
from datetime import timedelta, datetime
from pathlib import Path

import numpy as np
import pandas as pd

HERE = Path(__file__).resolve().parent
R14_PATH = HERE.parent / "operationalisation_support" / "single_pool_reanchor" / "run.py"

_spec = importlib.util.spec_from_file_location("r14_run", R14_PATH)
r14 = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(r14)

OFFSETS = list(range(-6, 1))  # t-6 .. t0 (0 = crash onset day)
SEED = 20260706
N_BOOT = 10_000

# Fresh-curve channels: the lead-up signals whose requested shape was retired /
# a null-chip, plus HA07d (the one SUPPORTED signal, best shown as a real curve).
CURVE_CHANNELS = [
    {
        "chart": "parasympathetic-swing", "col": "bb_highest", "sigma_floor": 2.0,
        "signal": "HA10_morning_body_battery_peak_z",
        "single_pool": {"disc_pp": 4.1, "ci95": [-16.5, 16.8], "verdict": "NOT-SUPPORTED",
                        "crash_leadup_share": 0.769, "ordinary_day_share": 0.729},
        "unit_note": "signed z vs [d-90,d-30] personal baseline; higher = higher morning body-battery peak",
    },
    {
        "chart": "walls-of-orange", "col": "max_spike_minutes", "sigma_floor": 1.0,
        "signal": "H02b_per_minute_stress_spike_minutes_z",
        "single_pool": {"disc_pp": 3.5, "ci95": [-21.2, 21.7], "verdict": "NOT-SUPPORTED",
                        "crash_leadup_share": 0.500, "ordinary_day_share": 0.465,
                        "era_overlay_number_only": {"train_disc_pp": 29.9, "validate_disc_pp": -8.2,
                                                    "as": "number_not_verdict_retired"}},
        "unit_note": "signed z vs personal baseline; higher = more per-minute stress-spike minutes",
    },
    {
        "chart": "hrv-decline", "col": "stress_stdev_sleep", "sigma_floor": 0.5,
        "signal": "HA07d_sleep_stress_variability_z",
        "single_pool": {"disc_pp": 19.7, "ci95": [-18.1, 17.0], "verdict": "SUPPORTED",
                        "crash_leadup_share": 0.880, "ordinary_day_share": 0.683,
                        "ppv_at_base_2_11pct": 2.71, "lift": 1.28, "tier": "C"},
        "unit_note": "signed z vs personal baseline of overnight stress variability (the HRV proxy; FR245 HRV hardware-blocked)",
    },
]


def z_matrix(refs, df_indexed, col, sigma_floor):
    """[n_ref x n_offset] matrix of z-vs-lagged-baseline; NaN where missing/uncomputable."""
    series = df_indexed[col]
    dates = df_indexed["date"]
    d2i = df_indexed.attrs["date_to_idx"]
    M = np.full((len(refs), len(OFFSETS)), np.nan)
    for i, ref in enumerate(refs):
        for j, off in enumerate(OFFSETS):
            d = ref + timedelta(days=off)
            if d not in d2i:
                continue
            val = series.iloc[d2i[d]]
            if pd.isna(val):
                continue
            mu, sigma = r14.compute_lagged_baseline(series, dates, d, sigma_floor=sigma_floor)
            if mu is None or sigma is None:
                continue
            M[i, j] = (float(val) - mu) / sigma
    return M


def pool_curve(M, rng):
    """Per-offset mean z + bootstrap 95% CI over refs; plus per-offset n."""
    means, los, his, ns = [], [], [], []
    for j in range(M.shape[1]):
        col = M[:, j]
        col = col[~np.isnan(col)]
        ns.append(int(len(col)))
        if len(col) == 0:
            means.append(None); los.append(None); his.append(None); continue
        means.append(round(float(col.mean()), 3))
        idx = rng.integers(0, len(col), size=(N_BOOT, len(col)))
        boot = col[idx].mean(axis=1)
        los.append(round(float(np.percentile(boot, 2.5)), 3))
        his.append(round(float(np.percentile(boot, 97.5)), 3))
    return means, los, his, ns


def build_curves():
    df = r14.load_master()
    df_indexed = r14._index_master(df)
    crash_starts = r14.load_crash_episodes()
    null_dates = r14.build_null_dates(df_indexed, crash_starts, leadup_days=r14.LEADUP_DAYS,
                                      seed=r14.LEGACY_NULL_SEED)
    rng = np.random.default_rng(SEED)

    curves = {}
    for ch in CURVE_CHANNELS:
        col = ch["col"]
        cM = z_matrix(crash_starts, df_indexed, col, ch["sigma_floor"])
        nM = z_matrix(null_dates, df_indexed, col, ch["sigma_floor"])
        c_mean, c_lo, c_hi, c_n = pool_curve(cM, rng)
        n_mean, n_lo, n_hi, n_n = pool_curve(nM, rng)
        curves[ch["chart"]] = {
            "signal": ch["signal"], "col": col, "unit_note": ch["unit_note"],
            "single_pool": ch["single_pool"],
            "offsets": OFFSETS,
            "crash_mean": c_mean, "crash_lo": c_lo, "crash_hi": c_hi, "n_crash_per_offset": c_n,
            "null_mean": n_mean, "null_lo": n_lo, "null_hi": n_hi, "n_null_per_offset": n_n,
        }
    meta = {"n_crash_episodes": len(crash_starts), "n_null": len(null_dates),
            "offsets": OFFSETS, "seed": SEED, "n_bootstrap": N_BOOT,
            "baseline": "[d-90,d-30] trimmed mean/std personal lagged baseline (R14 machinery)",
            "run_at": datetime.now().isoformat(timespec="seconds")}
    return curves, meta


# ---------------------------------------------------------------------------
# Site chart JSON emission (on disk; user commits from the site checkout)
# ---------------------------------------------------------------------------

def _site_charts_dir() -> Path | None:
    raw = os.environ.get("GEVOELSCORE_SITE_PATH", "") or r"C:\Users\Gebruiker\Documents\wiggers_research_story"
    d = Path(raw) / "site" / "data" / "charts"
    return d if d.parent.parent.exists() else None


CRASH_FREQUENCY_JSON = {
    "_comment": ("Crash episodes per year (R1). Descriptive count trajectory, NOT an effect-decay. "
                 "2022 partial (logging starts 2022-09); 2026 partial (through 06-05). Sustained crashes "
                 "thin out 2024->2025; medication (citalopram buildup 2024-04, taper 2026-03) + pacing are "
                 "declared confounds - no causal reading. Source: felt_state_timeline (R13) rolled to year."),
    "placeholder": False,
    "unit": "crash_episodes",
    "years": ["2022", "2023", "2024", "2025", "2026"],
    "n_crash": [5, 9, 11, 2, 2],
    "partial_years": ["2022", "2026"],
    "duration_buckets_total": {"short_2_3d": 21, "medium_4_6d": 4, "long_7plus_d": 4},
    "longest_crash_days": 14,
    "note": "Descriptive count over time with declared confounds; the 2024->2025 thinning is a count change, not 'the signal faded'.",
}

EXERTION_LEADUP_JSON = {
    "_comment": ("Exertion in the 4-day crash lead-up (R1), reframed to SINGLE-POOL (the asset asked "
                 "for a by-era split; that framing is retired). HA01b (the named signal) is single-pool "
                 "NOT-SUPPORTED; its single-pool-SUPPORTED sibling HA01c (rank-shock) is Tier-C and "
                 "WITHHELD. No per-era verdict; CIs shown (they cross zero). Source: single_pool_reanchor (R14)."),
    "placeholder": False,
    "unit": "share_of_windows",
    "framing": "single_pool",
    "primary_signal": "HA01b_exertion_class_heavy_in_4d_leadup",
    "crash_leadup_share": 0.821,
    "ordinary_day_share": 0.770,
    "discrimination_pp": 5.1,
    "discrimination_ci95": [-14.7, 13.3],
    "verdict": "NOT-SUPPORTED",
    "sibling_supported_signal": {
        "name": "HA01c_effective_exertion_rank_shock",
        "crash_leadup_share": 0.821, "ordinary_day_share": 0.625,
        "discrimination_pp": 19.6, "discrimination_ci95": [-19.6, 19.1], "verdict": "SUPPORTED",
        "caveat": "Tier-C PPV (~2%); load-bearing status WITHHELD pending v2 threshold-monotonicity diagnostic",
    },
    "note": ("Single-pool, not per-era. Heavy exertion shows up in ~82% of crash lead-ups but also ~77% of "
             "ordinary days, so HA01b's gap (+5.1 pp) is inside its own CI. The rank-shock sibling HA01c "
             "(+19.6 pp) is the non-null read but is Tier-C and its CI still straddles zero - not a forecast."),
}


def curve_chart_json(chart_key, curve, meta):
    sp = curve["single_pool"]
    return {
        "_comment": (f"REAL single-pool crash lead-up curve (R1, fresh extraction {meta['run_at'][:10]}). "
                     f"Pooled t-6..t0 z-vs-personal-baseline across {meta['n_crash_episodes']} crash episodes "
                     f"(crash band) vs {meta['n_null']} ordinary-day windows (null band). Replaces the retired "
                     f"per-era decay / early-vs-late fabrication with a real descriptive shape. NOT per-era, "
                     f"NOT a verdict; wide CI honesty at n=29. Baseline-relative, no dated values. "
                     f"Source: crash_leadup_curves/ (reuses R14 lagged baseline)."),
        "placeholder": False,
        "framing": "single_pool",
        "signal": curve["signal"],
        "unit": "z_vs_personal_baseline",
        "unit_note": curve["unit_note"],
        "offsets_days_from_onset": curve["offsets"],
        "crash": {"mean": curve["crash_mean"], "lo": curve["crash_lo"], "hi": curve["crash_hi"],
                  "n_per_offset": curve["n_crash_per_offset"]},
        "ordinary_day_null_band": {"mean": curve["null_mean"], "lo": curve["null_lo"], "hi": curve["null_hi"],
                                   "n_per_offset": curve["n_null_per_offset"]},
        "single_pool_summary": sp,
        "note": ("The crash curve is the real pooled trajectory of this signal in the week before a crash; "
                 "the null band is ordinary days. Read the SHAPE against the band, not a forecast: the single-pool "
                 f"windowed discrimination is {sp['disc_pp']} pp (CI {sp['ci95']}), verdict {sp['verdict']}. "
                 "Bands are day-to-day / episode spread (bootstrap 95%), not error of a fitted line; n=29 pooled."),
    }


def main():
    print("[R1-curves] Building fresh single-pool lead-up curves...")
    curves, meta = build_curves()
    (HERE / "summary.json").write_text(json.dumps({"curves": curves, "meta": meta}, indent=2, default=str),
                                       encoding="utf-8")
    print(f"[R1-curves]   n_crash={meta['n_crash_episodes']} n_null={meta['n_null']} offsets={meta['offsets']}")
    for chart, c in curves.items():
        print(f"\n  {chart} ({c['signal']}) verdict={c['single_pool']['verdict']}")
        print(f"    offset : {'  '.join(f'{o:>5}' for o in c['offsets'])}")
        print(f"    crash  : {'  '.join(f'{v:>5}' if v is not None else '   na' for v in c['crash_mean'])}")
        print(f"    null   : {'  '.join(f'{v:>5}' if v is not None else '   na' for v in c['null_mean'])}")
        print(f"    n_crash: {'  '.join(f'{n:>5}' for n in c['n_crash_per_offset'])}")

    site = _site_charts_dir()
    if site is None:
        print("\n[R1-curves] SITE path not found; skipping site JSON writes (research summary written).")
        return
    site.mkdir(parents=True, exist_ok=True)
    written = []
    for chart_key, curve in curves.items():
        p = site / f"{chart_key}.json"
        p.write_text(json.dumps(curve_chart_json(chart_key, curve, meta), indent=2), encoding="utf-8")
        written.append(p.name)
    (site / "crash-frequency.json").write_text(json.dumps(CRASH_FREQUENCY_JSON, indent=2), encoding="utf-8")
    (site / "exertion-lead-up.json").write_text(json.dumps(EXERTION_LEADUP_JSON, indent=2), encoding="utf-8")
    written += ["crash-frequency.json", "exertion-lead-up.json"]
    print(f"\n[R1-curves] Wrote {len(written)} site chart JSONs to {site}:")
    for w in written:
        print(f"    {w}")


if __name__ == "__main__":
    main()
