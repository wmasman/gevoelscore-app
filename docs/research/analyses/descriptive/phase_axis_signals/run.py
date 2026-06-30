"""R19 phase-axis re-aggregation of the single-pool reanchor operands.

Re-uses the EXACT operand definitions + recipe from
docs/research/analyses/descriptive/operationalisation_support/single_pool_reanchor/run.py
(imported as module), but stratifies the crash episodes by the per-day-master
`recovery_phase` column (lc_recovery_phase_axis.md M1 boundaries, ids 1..5 with
phase 4 split 4a/4b). Descriptive Layer 1 only: per-(signal, phase) disc_pp +
stationary-bootstrap CI + n_crashes. NO per-phase verdict, NO split, NO causal claim.

The crash episode is assigned to a phase by the phase of its episode_start date.
The null pool is the SAME single-pool null set (whole Stratum 4) -- we do NOT
re-sample a per-phase null (would shrink n_null catastrophically and is not the
ask). The reference frame is therefore: per-phase crash trigger-fraction vs the
SAME whole-pool null trigger-fraction. disc_pp = (frac_crash_phase - frac_null_pool)*100.
This is the honest descriptive shape: "how does this signal's crash-leadup
trigger rate look within each lived phase, against the common null backdrop".

Output: JSON to scratchpad; the MD is hand-authored from it.
"""
from __future__ import annotations

import json
import sys
from datetime import date
from pathlib import Path

import numpy as np
import pandas as pd

REANCHOR_DIR = Path(
    r"c:\Users\Gebruiker\Documents\gevoelscore-app\docs\research\analyses"
    r"\descriptive\operationalisation_support\single_pool_reanchor"
)
sys.path.insert(0, str(REANCHOR_DIR))
UTILS_DIR = Path(
    r"c:\Users\Gebruiker\Documents\gevoelscore-app\docs\research\analyses\_utils"
)
sys.path.insert(0, str(UTILS_DIR))

import run as R  # the locked reanchor module  # noqa: E402
from inference import stationary_bootstrap_ci  # noqa: E402

OUT = Path(__file__).resolve().parent / "phase_axis_result.json"

# ---- phase axis helper (verbatim from lc_recovery_phase_axis.md Sec 2.1) ----
def lc_recovery_phase(d: date) -> str:
    if d < date(2022, 3, 21):
        return "pre_illness_healthy"          # 1
    if d < date(2022, 4, 4):
        return "acute_infection"              # 2
    if d < date(2022, 9, 22):
        return "lc_pre_ergo"                  # 3
    if d < date(2022, 11, 17):
        return "pacing_pre_citalopram_learning"  # 4a
    if d < date(2024, 4, 9):
        return "pacing_habit_established"     # 4b
    return "citalopram_modulated"             # 5

PHASE_ORDER = [
    ("1", "pre_illness_healthy"),
    ("2", "acute_infection"),
    ("3", "lc_pre_ergo"),
    ("4a", "pacing_pre_citalopram_learning"),
    ("4b", "pacing_habit_established"),
    ("5", "citalopram_modulated"),
]

# ---- the 7 requested scorecard signals -> reanchor trigger builders ----
# Each returns (crash_triggers_array, crash_medians, n_skipped) for a list of refs,
# and we need a matching null-trigger array for the whole pool.

def build_HA07c(refs, df):
    return R._build_trigger_arrays_delta_signed(refs, df, "stress_mean_sleep", sigma_floor=2.0)

def build_HA07d(refs, df):
    return R._build_trigger_arrays_delta_abs(refs, df, "stress_stdev_sleep", sigma_floor=0.5)

def build_HA10(refs, df):
    return R._build_trigger_arrays_z_abs(refs, df, "bb_highest", sigma_floor=2.0)

def build_HA11(refs, df):
    return R._build_trigger_arrays_z_signed(refs, df, "u_dip_count", sigma_floor=0.5)

def build_HA06b(refs, df):
    return R._build_trigger_arrays_z_abs(refs, df, "resting_hr", sigma_floor=0.5)

def build_HA01b(refs, df):
    # frac windows with >=1 day heavy/very_heavy exertion in 4d leadup
    triggers = []
    n_shock_list = []
    for ref in refs:
        n_shock, n_valid = R.episode_ha01b_n_shock(ref, df)
        if n_shock is None:
            triggers.append(np.nan)
            continue
        triggers.append(1 if n_shock >= 1 else 0)
        n_shock_list.append(n_shock)
    return np.array(triggers, dtype=float), n_shock_list, 0

def build_H02b(refs, df):
    triggers = []
    deltas = []
    for ref in refs:
        dv, _ = R.episode_h02b_max_delta(ref, df, "max_spike_minutes",
                                         baseline_threshold=10.0, leadup_days=3)
        if dv is None:
            triggers.append(np.nan)
            continue
        triggers.append(1 if dv >= 10.0 else 0)
        deltas.append(dv)
    return np.array(triggers, dtype=float), deltas, 0

SIGNALS = {
    "H02b":  (build_H02b,  3, "frac windows max(max_spike_minutes - baseline) over 3d leadup >= +10 min"),
    "HA06b": (build_HA06b, 4, "max |z| (4d) of resting_hr; lagged baseline; sigma_floor=0.5 bpm"),
    "HA07c": (build_HA07c, 4, "max signed z (4d) of n/n delta of stress_mean_sleep; sigma_floor=2.0"),
    "HA07d": (build_HA07d, 4, "max |z| (4d) of n/n delta of stress_stdev_sleep; sigma_floor=0.5"),
    "HA10":  (build_HA10,  4, "max |z| (4d) of bb_highest; lagged baseline; sigma_floor=2.0 BB"),
    "HA11":  (build_HA11,  4, "max signed z (4d) of u_dip_count; lagged baseline; sigma_floor=0.5 events"),
    "HA01b": (build_HA01b, 4, "frac windows with >=1 heavy/very_heavy exertion day in 4d leadup"),
}


def main():
    print("[R19] loading master + crash episodes (whole Stratum-4 single pool)...")
    df = R.load_master()
    df_idx = R._index_master(df)
    crash_starts = R.load_crash_episodes()
    print(f"[R19]   n_days={len(df_idx)}  n_crash={len(crash_starts)}")

    # Assign each crash episode_start to a phase (recompute via helper; also
    # cross-check against per_day_master.recovery_phase where the date exists).
    phase_of = {}
    for d in crash_starts:
        phase_of[d] = lc_recovery_phase(d)
    # cross-check against the column for crashes whose date is in-frame
    col = df.set_index("date")["recovery_phase"].to_dict() if "recovery_phase" in df.columns else {}
    mism = [(str(d), phase_of[d], col.get(d)) for d in crash_starts if d in col and col[d] != phase_of[d]]
    if mism:
        print(f"[R19] WARNING phase mismatch helper-vs-column: {mism}")
    else:
        print("[R19]   helper phase == per_day_master.recovery_phase for all in-frame crashes")

    # Null pools (whole Stratum 4) per leadup length, same seeds as reanchor.
    nulls = {
        3: R.build_null_dates(df_idx, crash_starts, leadup_days=3, seed=R.LEGACY_NULL_SEED),
        4: R.build_null_dates(df_idx, crash_starts, leadup_days=4, seed=R.LEGACY_NULL_SEED),
        7: R.build_null_dates(df_idx, crash_starts, leadup_days=7, seed=R.LEGACY_NULL_SEED),
    }

    out = {"meta": {
        "n_days": len(df_idx),
        "n_crash_total": len(crash_starts),
        "as_of": str(R.AS_OF_DATE),
        "stratum_4_start": str(R.STRATUM_4_START),
        "E_L": R.DEFAULT_EL,
        "n_bootstrap": R.N_BOOTSTRAP,
        "seed": R.SEED,
        "legacy_null_seed": R.LEGACY_NULL_SEED,
        "note": "null pool is whole-Stratum-4 (NOT per-phase); disc = phase-crash-frac - whole-pool-null-frac",
    }, "signals": {}}

    # per-phase crash counts (in single pool == all crashes are >= 2022-09-03,
    # so phases 1+2+3-pre-2022-09-03 will be empty by construction; report anyway)
    phase_crash_lists = {pid: [d for d in crash_starts if phase_of[d] == name]
                         for pid, name in PHASE_ORDER}
    out["meta"]["phase_crash_counts"] = {pid: len(phase_crash_lists[pid]) for pid, _ in PHASE_ORDER}
    print("[R19] per-phase crash counts:", out["meta"]["phase_crash_counts"])

    for sig, (builder, leadup, operand) in SIGNALS.items():
        print(f"[R19] signal {sig} (leadup={leadup})...")
        null_refs = nulls[leadup]
        null_trig, _nm, _ns = builder(null_refs, df_idx)
        null_clean = null_trig[~np.isnan(null_trig)]
        frac_null = float(null_clean.mean()) if len(null_clean) else float("nan")

        # all-crash baseline (single pool) for sanity vs reanchor
        all_trig, _am, _as = builder(crash_starts, df_idx)
        all_clean = all_trig[~np.isnan(all_trig)]
        frac_all = float(all_clean.mean()) if len(all_clean) else float("nan")
        disc_all = (frac_all - frac_null) * 100.0

        sig_rec = {
            "operand": operand,
            "leadup_days": leadup,
            "frac_null_pool": frac_null,
            "n_null_clean": int(len(null_clean)),
            "single_pool_frac_crash": frac_all,
            "single_pool_disc_pp": disc_all,
            "single_pool_n_crash_clean": int(len(all_clean)),
            "phases": [],
        }

        for pid, name in PHASE_ORDER:
            refs = phase_crash_lists[pid]
            n_crashes = len(refs)
            rec = {"id": pid, "name": name, "n_crashes": n_crashes}
            if n_crashes == 0:
                rec.update({"frac_crash": None, "disc_pp": None, "n_crash_clean": 0,
                            "ci_lower": None, "ci_upper": None,
                            "honest_limit": True, "reason": "no crashes in phase (single-pool by construction)"})
                sig_rec["phases"].append(rec)
                continue
            ctrig, _cm, _cs = builder(refs, df_idx)
            cclean = ctrig[~np.isnan(ctrig)]
            n_clean = int(len(cclean))
            if n_clean == 0:
                rec.update({"frac_crash": None, "disc_pp": None, "n_crash_clean": 0,
                            "ci_lower": None, "ci_upper": None,
                            "honest_limit": True, "reason": "all phase crashes dropped (operand not computable)"})
                sig_rec["phases"].append(rec)
                continue
            frac_c = float(cclean.mean())
            disc = (frac_c - frac_null) * 100.0
            # stationary bootstrap CI on disc_pp: pool phase-crash + whole null,
            # same recipe shape as reanchor (E[L]=7).
            pooled = np.concatenate([cclean, null_clean])
            n_c = len(cclean)
            def disc_from_pooled(arr, n_c=n_c, fn=frac_null):
                c = arr[:n_c]
                nl = arr[n_c:]
                if len(c) == 0 or len(nl) == 0:
                    return 0.0
                return float((c.mean() - nl.mean()) * 100.0)
            ci = stationary_bootstrap_ci(
                pooled, disc_from_pooled,
                n_bootstrap=R.N_BOOTSTRAP, expected_block_length=R.DEFAULT_EL,
                confidence_level=0.95, random_state=R.SEED,
            )
            rec.update({
                "frac_crash": frac_c,
                "disc_pp": disc,
                "n_crash_clean": n_clean,
                "ci_lower": float(ci["ci_lower"]),
                "ci_upper": float(ci["ci_upper"]),
                "honest_limit": n_clean < 10,
                "reason": ("n_crash_clean < 10 (small-n honest-limit)" if n_clean < 10 else ""),
            })
            sig_rec["phases"].append(rec)
        out["signals"][sig] = sig_rec

    OUT.write_text(json.dumps(out, indent=2, default=str), encoding="utf-8")
    print(f"[R19] wrote {OUT}")
    # console summary
    for sig, rec in out["signals"].items():
        cells = [f"{p['id']}:{p['disc_pp']:.1f}pp/n{p['n_crash_clean']}" if p['disc_pp'] is not None
                 else f"{p['id']}:--/n0" for p in rec["phases"]]
        print(f"  {sig:7s} null={rec['frac_null_pool']:.3f} | " + "  ".join(cells))


if __name__ == "__main__":
    main()
