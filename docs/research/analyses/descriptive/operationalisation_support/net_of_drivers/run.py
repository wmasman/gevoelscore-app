"""Net-of-drivers descriptive residual re-read (R20 + R16 collapsed).

Overlay on top of the R14 single_pool_reanchor recipe: for each scorecard
signal that rides a CONFIRMED citalopram-dose-modulated channel, subtract
the §5.B dose-adjusted predictor (channel_adj(d) = channel(d) -
beta * dose_plasma_mg(d)) BEFORE re-running the single-pool discrimination.
The site shows the verdict as the RESIDUAL read with the established
driver (citalopram) modelled out.

LICENSED DRIVER: citalopram ONLY, on CONFIRMED channels ONLY, per
  citalopram_phase_stratification.md §5.A/B/C + §2 (CONFIRMED matrix) and
  phase_axis_collapsibility_conventions.md Tier B.
  - stress_mean_sleep : +0.43 / mg  (CONFIRMED, buildup post-CPAP beta)
  - all_day_stress_avg: +0.57 / mg  (CONFIRMED)
  - bb_lowest         : -1.13 / mg  (CONFIRMED)

This is a LAYER-1 DESCRIPTIVE residual re-read (like single_pool_reanchor),
NOT a verdict re-lock. Locked result.md files UNCHANGED. No git/audit/push.

Reuses single_pool_reanchor/run.py as a module (operands, evaluators,
null construction, evaluate_ha, seeds, B, E[L]).

Run from repo root:
    python docs/research/analyses/descriptive/operationalisation_support/net_of_drivers/run.py
"""
from __future__ import annotations

import json
import sys
from datetime import date, datetime
from pathlib import Path

import numpy as np
import pandas as pd

HERE = Path(__file__).resolve().parent
REANCHOR_DIR = HERE.parent / "single_pool_reanchor"
sys.path.insert(0, str(REANCHOR_DIR))

# Import the locked recipe as a module.
import run as spr  # noqa: E402  (single_pool_reanchor/run.py)


# -----------------------------------------------------------------------------
# Confirmed-channel beta table (citalopram_phase_stratification.md §2 / §5.6.1)
# Buildup post-CPAP beta per §5.B (tighter CIs).
# -----------------------------------------------------------------------------
CONFIRMED_BETAS = {
    "stress_mean_sleep": +0.43,    # [+0.16, +0.70], p=0.001
    "all_day_stress_avg": +0.57,   # [+0.24, +0.89], p=0.000
    "bb_lowest": -1.13,            # [-1.78, -0.49], p=0.000
}


def apply_dose_correction(df: pd.DataFrame, channel: str, beta: float) -> pd.DataFrame:
    """Return a copy of df with `channel` replaced by its §5.B dose-adjusted
    value: channel_adj(d) = channel(d) - beta * dose_plasma_mg(d).

    Per §3 explicit zero-dose convention, dose_plasma_mg = 0 on unmedicated
    dates, so the adjusted channel reduces to the raw value there. NaN dose
    propagates to NaN adjusted (treated as missing -> episode skipped),
    matching the locked min-valid gating.
    """
    out = df.copy()
    if "dose_plasma_mg" not in out.columns:
        raise RuntimeError("dose_plasma_mg column missing from master")
    dose = out["dose_plasma_mg"].astype(float)
    out[channel] = out[channel].astype(float) - beta * dose
    return out


def run_signal_netted(df_raw, crash_starts, null_dates, eval_fn, channel, beta):
    """Run one confirmed-channel signal twice: raw and dose-netted.

    Returns (raw_res, netted_res). Both indexed (attrs rebuilt) so the
    delta/slope caches are not shared between raw and netted runs.
    """
    df_raw_ix = spr._index_master(df_raw)
    raw_res = eval_fn(df_raw_ix, crash_starts, null_dates)

    df_net = apply_dose_correction(df_raw, channel, beta)
    df_net_ix = spr._index_master(df_net)
    net_res = eval_fn(df_net_ix, crash_starts, null_dates)
    return raw_res, net_res


def main():
    print("[net] Loading master + crash episodes via single_pool_reanchor loaders...")
    df = spr.load_master()
    crash_starts = spr.load_crash_episodes()
    print(f"[net]   n_days={len(df)}  n_crash={len(crash_starts)}")

    # dose_plasma_mg presence + sanity
    if "dose_plasma_mg" not in df.columns:
        raise RuntimeError("dose_plasma_mg NOT in master; correction unwireable")
    dose = df["dose_plasma_mg"].astype(float)
    dose_meta = {
        "non_null": int(dose.notna().sum()),
        "n": int(len(dose)),
        "min": float(dose.min()),
        "max": float(dose.max()),
        "n_zero": int((dose == 0).sum()),
        "n_pos": int((dose > 0).sum()),
    }
    print(f"[net]   dose_plasma_mg: {dose_meta}")

    df_for_null = spr._index_master(df)
    null_dates_4d = spr.build_null_dates(df_for_null, crash_starts,
                                         leadup_days=spr.LEADUP_DAYS, seed=spr.LEGACY_NULL_SEED)
    null_dates_3d = spr.build_null_dates(df_for_null, crash_starts,
                                         leadup_days=3, seed=spr.LEGACY_NULL_SEED)

    results = {"netted": {}, "complicates": {}, "meta": {}}

    # ---- CONFIRMED-channel signals: compute netted -------------------------
    # HA07c rides stress_mean_sleep (clean continuous level correction).
    print("[net] HA07c (stress_mean_sleep, +0.43/mg) ...")
    raw, net = run_signal_netted(df, crash_starts, null_dates_4d, spr.eval_HA07c,
                                 "stress_mean_sleep", CONFIRMED_BETAS["stress_mean_sleep"])
    results["netted"]["HA07c"] = {
        "channel": "stress_mean_sleep", "beta_per_mg": 0.43,
        "method": "exact §5.B: channel_adj = stress_mean_sleep - 0.43*dose; delta-of-night taken on adjusted column",
        "raw": raw, "netted": net,
    }

    # HA08c rides stress_mean_sleep slope (clean continuous level correction).
    print("[net] HA08c (slope of stress_mean_sleep, +0.43/mg) ...")
    raw, net = run_signal_netted(df, crash_starts, null_dates_4d, spr.eval_HA08c,
                                 "stress_mean_sleep", CONFIRMED_BETAS["stress_mean_sleep"])
    results["netted"]["HA08c"] = {
        "channel": "stress_mean_sleep", "beta_per_mg": 0.43,
        "method": "exact §5.B: channel_adj = stress_mean_sleep - 0.43*dose; trailing-5d slope taken on adjusted column",
        "raw": raw, "netted": net,
    }

    # H02b rides max_spike_minutes (NOT all_day_stress_avg). The +0.57/mg beta
    # is the all_day_stress_avg DAILY-MEAN beta (points/mg). Applying it to a
    # spike-DURATION metric (minutes/mg) is BOTH a daily-mean-vs-spike approx
    # AND a unit mismatch. Flagged APPROXIMATION.
    print("[net] H02b (max_spike_minutes via all_day_stress_avg beta +0.57/mg, APPROX) ...")
    raw, net = run_signal_netted(df, crash_starts, null_dates_3d, spr.eval_H02b,
                                 "max_spike_minutes", CONFIRMED_BETAS["all_day_stress_avg"])
    results["netted"]["H02b"] = {
        "channel": "max_spike_minutes (proxy for all_day_stress_avg spike)",
        "beta_per_mg": 0.57,
        "method": ("APPROXIMATION §5.B: channel_adj = max_spike_minutes - 0.57*dose. "
                   "The +0.57/mg beta is the all_day_stress_avg DAILY-MEAN beta (stress points/mg); "
                   "H02b's reanchor operand rides max_spike_minutes (spike DURATION, minutes). "
                   "Applying a points/mg beta to a minutes metric is a unit-mismatched daily-mean-to-spike "
                   "approximation. Direction (subtract dose-driven inflation) is correct; magnitude is indicative only."),
        "raw": raw, "netted": net,
        "approximation_flag": True,
    }

    # ---- HA11: gate rides stress, but the gate-level correction is NOT
    #            wireable from the master (S_pre>=40 minute-level gate is baked
    #            into the daily u_dip_count at extraction; no per-minute stress
    #            series exists in per_day_master). A daily-mean dose subtraction
    #            on an EVENT COUNT is dimensionally meaningless, so we run it as
    #            a NULL-EFFECT sensitivity (expect ~no change / degenerate) and
    #            report the wiring gap, NOT a real netted number.
    print("[net] HA11 (u_dip_count; S_pre>=40 gate rides stress; gate-correction UNWIREABLE) ...")
    df11_ix = spr._index_master(df)
    raw11 = spr.eval_HA11(df11_ix, crash_starts, null_dates_4d)
    results["netted"]["HA11"] = {
        "channel": "u_dip_count (S_pre>=40 gate rides stress_mean_sleep / all_day_stress)",
        "beta_per_mg": None,
        "method": ("GATE-CORRECTION NOT WIREABLE FROM MASTER. HA11's u_dip_count is a daily EVENT COUNT "
                   "with the S_pre>=40 per-minute stress gate already applied at extraction. Dose-correcting "
                   "the gate requires re-detecting U-dips on a dose-corrected per-minute stress series, which "
                   "is NOT present in per_day_master (only daily aggregates exist). Subtracting a stress-LEVEL "
                   "beta from an event COUNT is dimensionally meaningless. Reported raw-only with the wiring gap."),
        "raw": raw11, "netted": None,
        "wiring_gap": True,
    }

    # ---- COMPLICATES rows (raw only; NOT on a confirmed channel) ----------
    print("[net] Complicates rows (raw only) ...")
    df_ix = spr._index_master(df)

    # HA10: bb_HIGHEST (not bb_lowest) -> complicates
    results["complicates"]["HA10"] = {
        "channel": "bb_highest", "reason": "rides bb_HIGHEST, not the CONFIRMED bb_lowest channel",
        "raw": spr.eval_HA10(df_ix, crash_starts, null_dates_4d),
    }
    # HA06b: resting_hr (weak / NOT confirmed) -> complicates
    results["complicates"]["HA06b"] = {
        "channel": "resting_hr", "reason": "resting_hr weakly-consistent, NOT confirmed (§2 p=0.34); no correction licensed",
        "raw": spr.eval_HA06b(df_ix, crash_starts, null_dates_4d),
    }
    # HA01b: exertion (pacing, not citalopram) -> complicates
    results["complicates"]["HA01b"] = {
        "channel": "exertion_class_lagged", "reason": "pacing/exertion channel; not citalopram-modulated; no correction licensed",
        "raw": spr.eval_HA01b_recomputed(df_ix, crash_starts, null_dates_4d),
    }

    # ---- HA07d sensitivity: stress variability (variance primitive). The
    #      level-acting dose correction barely moves a variance primitive.
    #      stress_stdev_sleep is the std of within-night stress; subtracting a
    #      constant-per-day (beta*dose) shifts the LEVEL, leaving the within-
    #      night std unchanged EXCEPT through any day-to-day dose variation
    #      inside the night-delta. Run as sensitivity; expect ~no change.
    print("[net] HA07d (stress_stdev_sleep variance primitive) sensitivity ...")
    raw07d = spr.eval_HA07d(spr._index_master(df), crash_starts, null_dates_4d)
    # Apply the stress beta to the channel that FEEDS the stdev? stress_stdev_sleep
    # is itself a per-night std summary; the master stores it as a level. The
    # closest honest correction is subtracting beta*dose from stress_stdev_sleep
    # as a level (which, on a std primitive, is a near-degenerate operation).
    df07d_net = apply_dose_correction(df, "stress_stdev_sleep", CONFIRMED_BETAS["stress_mean_sleep"])
    net07d = spr.eval_HA07d(spr._index_master(df07d_net), crash_starts, null_dates_4d)
    results["netted"]["HA07d_sensitivity"] = {
        "channel": "stress_stdev_sleep (variance primitive)",
        "beta_per_mg": 0.43,
        "method": ("SENSITIVITY ONLY: stress_stdev_sleep is a within-night STD (variance primitive). "
                   "A level-acting dose subtraction (beta*dose) barely moves a variance primitive; "
                   "the night-over-night delta of a std is near-invariant to a per-day level shift. "
                   "Expect ~no change. Not a load-bearing netted number."),
        "raw": raw07d, "netted": net07d,
        "sensitivity_only": True,
    }

    # ---- meta -------------------------------------------------------------
    results["meta"] = {
        "as_of_date": str(spr.AS_OF_DATE),
        "stratum_4_start": str(spr.STRATUM_4_START),
        "n_days_S4": len(df),
        "n_crash_episodes": len(crash_starts),
        "block_length_E_L": spr.DEFAULT_EL,
        "n_bootstrap": spr.N_BOOTSTRAP,
        "seed_bootstrap_perm": spr.SEED,
        "seed_null_sample": spr.LEGACY_NULL_SEED,
        "n_std_primary": spr.N_STD_PRIMARY,
        "n_null_4d": len(null_dates_4d),
        "n_null_3d": len(null_dates_3d),
        "confirmed_betas": CONFIRMED_BETAS,
        "dose_meta": dose_meta,
        "run_at": datetime.utcnow().isoformat() + "Z",
    }

    out_json = HERE / "result-data.json"
    out_json.write_text(json.dumps(results, indent=2, default=str), encoding="utf-8")
    print(f"[net] Wrote {out_json}")

    _print_summary(results)
    return results


def _fmt(res):
    if not res or "disc_pp" not in res:
        v = res.get("verdict_single_pool", "n/a") if res else "n/a"
        return f"(no disc; {v})"
    return (f"disc={res['disc_pp']:+.1f} "
            f"CI[{res['ci95_disc_pp_lower']:+.1f},{res['ci95_disc_pp_upper']:+.1f}] "
            f"p={res['perm_pvalue_greater_E_L_7']:.4f} {res['verdict_single_pool']}")


def _print_summary(results):
    print("\n==== NET-OF-DRIVERS SUMMARY ====")
    for sig, d in results["netted"].items():
        print(f"\n{sig}  [{d['channel']}]")
        print(f"  raw   : {_fmt(d['raw'])}")
        if d.get("netted") is not None:
            print(f"  netted: {_fmt(d['netted'])}")
        else:
            print("  netted: NULL (not wireable)")
    print("\n-- complicates (raw only) --")
    for sig, d in results["complicates"].items():
        print(f"{sig} [{d['channel']}]: {_fmt(d['raw'])}  ({d['reason']})")


if __name__ == "__main__":
    main()
