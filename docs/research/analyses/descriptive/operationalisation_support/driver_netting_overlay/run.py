"""R20 driver-netting overlay: net-of-citalopram-driver re-read of the scorecard.

Applies the locked section 5.B dose-adjusted-predictor recipe from
``methodology/citalopram_phase_stratification.md`` to the driver-exposed
scorecard rows, as a DESCRIPTIVE OVERLAY on the R14 single-pool verdicts.
No verdict is re-locked; this is a transparency layer per site request R20 and
the R18 triage (``methodology/hypothesis_retest_triage.md`` section 4).

Reuses the R14 single-pool operand machinery verbatim (imported from the sibling
``single_pool_reanchor/run.py``) so the RAW single-pool numbers reproduce
byte-for-byte and the ONLY new quantity is the netted number. The netted channel
is injected into the master and dispatched through the same low-level trigger
builders the locked operands use.

Net recipe (section 5.B):
    channel_adj(d) = channel(d) - beta_dose * dose_plasma_mg(d)
with beta_dose the locked buildup beta from citalopram_phase_stratification
section 2:
    stress_mean_sleep : +0.43 / mg   (CONFIRMED, load-bearing)
    resting_hr        : +0.03 / mg   (weakly-consistent, non-significant; sensitivity only)
``dose_plasma_mg`` is read from the canonical per_day_master column (0 in the
unmedicated phase, PK-ramped over buildup, 30mg plateau in consolidation, ramped
down over afbouw).

Scope: the five driver-exposed scorecard rows (HA07c, H02b, HA11, HA10, HA06b)
plus the SUPPORTED row HA07d (confirmatory) and the off-scorecard sibling HA08c
(same beta channel, different operator). Of these, exactly one scorecard row
(HA07c) uses a channel carrying a locked citalopram beta; the rest are
family-adjacent with no per-mg coefficient to subtract.

Run from repo root:
    python docs/research/analyses/descriptive/operationalisation_support/driver_netting_overlay/run.py

Outputs:
    result-data.json (machine-readable; gitignored per docs/research/**/*.json rule)
    prints a comparison table to stdout
"""
from __future__ import annotations

import importlib.util
import json
from datetime import datetime
from pathlib import Path

import numpy as np

HERE = Path(__file__).resolve().parent
R14_PATH = HERE.parent / "single_pool_reanchor" / "run.py"

# Import the R14 machinery by file path (avoids run.py name-collision with this file).
_spec = importlib.util.spec_from_file_location("r14_run", R14_PATH)
r14 = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(r14)


# -----------------------------------------------------------------------------
# Locked buildup betas per citalopram_phase_stratification.md section 2 / 5.B
# -----------------------------------------------------------------------------

BETA_SMS = 0.43   # stress_mean_sleep, CONFIRMED, per mg plasma citalopram
BETA_RHR = 0.03   # resting_hr, weakly-consistent + non-significant; sensitivity arm only


def add_adjusted(df, col: str, beta: float):
    """Inject a section-5.B dose-adjusted channel: col_adj = col - beta*dose_plasma_mg."""
    df[col + "_adj"] = df[col].astype(float) - beta * df["dose_plasma_mg"].astype(float)
    return df


def summarize(res: dict) -> dict:
    """Extract the overlay-relevant fields from an evaluate_ha result dict."""
    return {
        "disc_pp": res.get("disc_pp"),
        "ci95_lo": res.get("ci95_disc_pp_lower"),
        "ci95_hi": res.get("ci95_disc_pp_upper"),
        "perm_p": res.get("perm_pvalue_greater_E_L_7"),
        "frac_crash": res.get("frac_crash"),
        "frac_null": res.get("frac_null"),
        "n_crash_clean": res.get("n_crash_clean"),
        "n_null_clean": res.get("n_null_clean"),
        "crit_a": res.get("crit_a_pass_freq60"),
        "crit_b": res.get("crit_b_pass_disc15"),
        "crit_c": res.get("crit_c_pass_median"),
        "verdict": res.get("verdict_single_pool"),
    }


def netted_delta_signed(df_indexed, crash_starts, nulls, col_adj, sigma_floor, label):
    ctrig, cmed, _ = r14._build_trigger_arrays_delta_signed(
        crash_starts, df_indexed, col_adj, sigma_floor=sigma_floor)
    ntrig, _, _ = r14._build_trigger_arrays_delta_signed(
        nulls, df_indexed, col_adj, sigma_floor=sigma_floor)
    return r14.evaluate_ha(label, ctrig, ntrig, cmed, r14.N_STD_PRIMARY)


def netted_slope_signed(df_indexed, crash_starts, nulls, col_adj, sigma_floor, label):
    ctrig, cmed, _ = r14._build_trigger_arrays_slope_signed(
        crash_starts, df_indexed, col_adj, sigma_floor=sigma_floor)
    ntrig, _, _ = r14._build_trigger_arrays_slope_signed(
        nulls, df_indexed, col_adj, sigma_floor=sigma_floor)
    return r14.evaluate_ha(label, ctrig, ntrig, cmed, r14.N_STD_PRIMARY)


def netted_z_abs(df_indexed, crash_starts, nulls, col_adj, sigma_floor, label):
    ctrig, cmed, _ = r14._build_trigger_arrays_z_abs(
        crash_starts, df_indexed, col_adj, sigma_floor=sigma_floor)
    ntrig, _, _ = r14._build_trigger_arrays_z_abs(
        nulls, df_indexed, col_adj, sigma_floor=sigma_floor)
    return r14.evaluate_ha(label, ctrig, ntrig, cmed, r14.N_STD_PRIMARY)


def main():
    print("[R20] Loading per_day_master + injecting section-5.B adjusted channels...")
    df = r14.load_master()
    if "dose_plasma_mg" not in df.columns:
        raise RuntimeError("per_day_master.csv has no dose_plasma_mg column")
    df = add_adjusted(df, "stress_mean_sleep", BETA_SMS)
    df = add_adjusted(df, "resting_hr", BETA_RHR)
    df_indexed = r14._index_master(df)

    crash_starts = r14.load_crash_episodes()
    print(f"[R20]   n_days={len(df_indexed)} n_crash_episodes={len(crash_starts)}")

    # Reproduce R14's null reference frames exactly (same builder, same seed).
    null_4d = r14.build_null_dates(
        df_indexed, crash_starts, leadup_days=r14.LEADUP_DAYS, seed=r14.LEGACY_NULL_SEED)
    null_3d = r14.build_null_dates(
        df_indexed, crash_starts, leadup_days=3, seed=r14.LEGACY_NULL_SEED)

    rows = {}

    # ---- HA07c: stress_mean_sleep night-over-night delta (CONFIRMED beta) ----
    raw = r14.eval_HA07c(df_indexed, crash_starts, null_4d)
    net = netted_delta_signed(
        df_indexed, crash_starts, null_4d, "stress_mean_sleep_adj", 2.0, "HA07c-netted")
    rows["HA07c"] = {
        "scorecard": True, "nettable": "confirmed", "beta": BETA_SMS,
        "channel": "stress_mean_sleep", "operator": "night-over-night delta, signed z",
        "raw": summarize(raw), "netted": summarize(net),
    }

    # ---- HA08c (off-scorecard sibling): stress_mean_sleep trailing-5d slope ----
    raw = r14.eval_HA08c(df_indexed, crash_starts, null_4d)
    net = netted_slope_signed(
        df_indexed, crash_starts, null_4d, "stress_mean_sleep_adj", 0.5, "HA08c-netted")
    rows["HA08c"] = {
        "scorecard": False, "nettable": "confirmed", "beta": BETA_SMS,
        "channel": "stress_mean_sleep", "operator": "trailing-5d OLS slope, signed z",
        "raw": summarize(raw), "netted": summarize(net),
    }

    # ---- HA06b: resting_hr |z| (weak / non-significant beta; sensitivity) ----
    raw = r14.eval_HA06b(df_indexed, crash_starts, null_4d)
    net = netted_z_abs(
        df_indexed, crash_starts, null_4d, "resting_hr_adj", 0.5, "HA06b-netted")
    rows["HA06b"] = {
        "scorecard": True, "nettable": "weak", "beta": BETA_RHR,
        "channel": "resting_hr", "operator": "level, |z|",
        "reason": ("weakly-consistent non-significant citalopram beta (+0.03/mg, CI spans 0); "
                   "true driver is the slow confounder handled by R30; the [d-90,d-30] lagged "
                   "baseline already detrends slow drift"),
        "raw": summarize(raw), "netted": summarize(net),
    }

    # ---- Non-nettable rows: raw reproduction + reasoned no-netting ----
    rows["HA07d"] = {
        "scorecard": True, "nettable": "no", "channel": "stress_stdev_sleep",
        "operator": "night-over-night delta, |z|",
        "reason": ("variability channel, NOT one of the 3 CONFIRMED mean channels; "
                   "mean-shift-invariant by construction; empirically citalopram-flat "
                   "(buildup delta +0.08)"),
        "raw": summarize(r14.eval_HA07d(df_indexed, crash_starts, null_4d)),
    }
    rows["H02b"] = {
        "scorecard": True, "nettable": "no", "channel": "max_spike_minutes",
        "operator": "spike-minute count delta, threshold",
        "reason": ("spike-count family; no per-mg beta (dose modulates the stress mean "
                   "level, not the within-day spike-minute count)"),
        "raw": summarize(r14.eval_H02b(df_indexed, crash_starts, null_3d)),
    }
    rows["HA11"] = {
        "scorecard": True, "nettable": "no", "channel": "u_dip_count",
        "operator": "level, signed z",
        "reason": ("count family; no per-mg beta (dose modulates the mean level, not the "
                   "count of within-day low-motion U-dips)"),
        "raw": summarize(r14.eval_HA11(df_indexed, crash_starts, null_4d)),
    }
    rows["HA10"] = {
        "scorecard": True, "nettable": "no", "channel": "bb_highest",
        "operator": "level, |z|",
        "reason": ("morning BB peak; the CONFIRMED BB channel is bb_lowest (the overnight "
                   "floor), a different channel; no beta for bb_highest"),
        "raw": summarize(r14.eval_HA10(df_indexed, crash_starts, null_4d)),
    }

    meta = {
        "beta_stress_mean_sleep": BETA_SMS,
        "beta_resting_hr": BETA_RHR,
        "n_days": len(df_indexed),
        "n_crash_episodes": len(crash_starts),
        "n_null_4d": len(null_4d),
        "n_null_3d": len(null_3d),
        "block_length_E_L": r14.DEFAULT_EL,
        "n_bootstrap": r14.N_BOOTSTRAP,
        "perm_boot_seed": r14.SEED,
        "null_sample_seed": r14.LEGACY_NULL_SEED,
        "run_at": datetime.utcnow().isoformat() + "Z",
    }

    result = {"rows": rows, "meta": meta}
    (HERE / "result-data.json").write_text(
        json.dumps(result, indent=2, default=str), encoding="utf-8")

    # ---- stdout comparison table ----
    print("\n[R20] Driver-netting overlay (raw single-pool vs section-5.B netted):\n")
    hdr = f"{'row':8} {'net?':9} {'raw disc':>9} {'net disc':>9} {'delta':>7} {'raw verdict':>14} {'net verdict':>14}"
    print(hdr)
    print("-" * len(hdr))
    for name, r in rows.items():
        raw = r["raw"]
        rawd = raw["disc_pp"]
        rawv = raw["verdict"]
        if "netted" in r:
            netd = r["netted"]["disc_pp"]
            netv = r["netted"]["verdict"]
            delta = netd - rawd
            print(f"{name:8} {r['nettable']:9} {rawd:+9.1f} {netd:+9.1f} {delta:+7.1f} {rawv:>14} {netv:>14}")
        else:
            print(f"{name:8} {r['nettable']:9} {rawd:+9.1f} {'--':>9} {'--':>7} {rawv:>14} {'(unchanged)':>14}")
    print(f"\n[R20] Wrote {HERE / 'result-data.json'}")


if __name__ == "__main__":
    main()
