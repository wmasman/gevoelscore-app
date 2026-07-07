"""PEM vs POTS separability: are they distinguishable in the watch data (descriptive).

Answers the reframing questions: which POTS-signature signal do we have and WHEN
does it appear; is it separable from the PEM-signature signal or heavily
correlated; are POTS-signature days lower in felt-state (gevoelscore); and can the
symptom notes corroborate POTS episodes.

Operationalisation (grounded in Wiggers' own framing; PROXY, not a diagnosis):
  - POTS-signature marker = elevated within-day stress U-dip (`u_dip_count`), the
    orthostatic / blood-volume pattern Wiggers ties to ORS/electrolytes (the one
    relatively-specific orthostatic watch-signal on this corpus).
  - PEM-signature marker  = elevated overnight stress (`stress_mean_sleep`, the
    HRV-proxy autonomic load), with `stress_stdev_sleep` as a secondary read.
Both as z vs the personal lagged [d-90, d-30] trimmed baseline (project standard).
A "signature day" = marker z >= Z_THRESH.

Descriptive Layer-1, single-pool (no era split), baseline-relative, aggregated.
No causal marks per CONVENTIONS section 4.1; the markers are proxies and the
correlations are associations, not mechanism.

Run from repo root:
    python docs/research/analyses/descriptive/pem_pots_separability/run.py

Outputs:
    summary.json (research side; gitignored per docs/research/**/*.json rule)
    prints the separability / timing / felt-state / notes tables to stdout
"""
from __future__ import annotations

import json
import os
from datetime import date, datetime
from pathlib import Path

import numpy as np
import pandas as pd
from scipy import stats as sps

HERE = Path(__file__).resolve().parent
STRATUM_4_START = date(2022, 9, 3)
AS_OF_DATE = date(2026, 6, 5)
Z_THRESH = 1.0  # a "signature day" = marker z >= 1.0 (stated threshold; correlation is threshold-free)

PHASE_ORDER = [
    ("lc_pre_ergo", "3"),
    ("pacing_pre_citalopram_learning", "4a"),
    ("pacing_habit_established", "4b"),
    ("citalopram_modulated", "5"),
]

# POTS-symptom keywords for the notes-corroboration check (Dutch clause text).
POTS_KEYWORDS = ["duizel", "licht in het hoofd", "staan", "opstaan", "orthostat",
                 "hartklop", "bloeddruk", "flauw", "zout", "electrolyt", "bloedvolume"]


def _data_root() -> Path:
    raw = os.environ.get("GEVOELSCORE_DATA_PATH", "") or r"C:\Users\Gebruiker\Documents\gevoelscore-data"
    return Path(raw)


def load_master() -> pd.DataFrame:
    cols = ["date", "u_dip_count", "stress_mean_sleep", "stress_stdev_sleep",
            "gevoelscore", "recovery_phase", "is_crash"]
    df = pd.read_csv(_data_root() / "unified" / "per_day_master.csv",
                     usecols=cols, parse_dates=["date"], low_memory=False)
    df["date"] = df["date"].dt.date
    df = df[(df["date"] >= STRATUM_4_START) & (df["date"] <= AS_OF_DATE)].copy()
    return df.sort_values("date").reset_index(drop=True)


def lagged_z(df: pd.DataFrame, col: str, sigma_floor: float) -> np.ndarray:
    """z vs [d-90, d-30] trimmed (10/90) mean/std personal baseline; NaN if uncomputable."""
    vals = df[col].to_numpy(dtype=float)
    ords = np.array([d.toordinal() for d in df["date"]])
    out = np.full(len(df), np.nan)
    for i in range(len(df)):
        v = vals[i]
        if np.isnan(v):
            continue
        lo = ords[i] - 90
        hi = ords[i] - 30
        w = vals[(ords >= lo) & (ords <= hi)]
        w = w[~np.isnan(w)]
        if len(w) < 40:
            continue
        w = np.sort(w)
        c0, c1 = int(len(w) * 0.10), int(len(w) * 0.90)
        if c1 <= c0:
            continue
        tr = w[c0:c1]
        mu = float(tr.mean())
        sd = float(tr.std(ddof=1))
        if sd <= sigma_floor:
            continue
        out[i] = (v - mu) / sd
    return out


def notes_pots_corroboration(pots_days: list[date]) -> dict:
    """On POTS-signature days, do the symptom notes mention POTS-type symptoms?"""
    path = _data_root() / "processed" / "notes" / "notes-categorized-v24-clauses.csv"
    if not path.exists():
        return {"error": "notes clause file not found"}
    nd = pd.read_csv(path, parse_dates=["date"])
    nd["date"] = nd["date"].dt.date
    txt = nd["clause"].fillna("").astype(str).str.lower()
    kw_hit = pd.Series(False, index=nd.index)
    per_kw = {}
    for k in POTS_KEYWORDS:
        m = txt.str.contains(k, regex=False)
        per_kw[k] = int(m.sum())
        kw_hit = kw_hit | m
    pots_set = set(pots_days)
    hit_dates = set(nd.loc[kw_hit, "date"])
    return {
        "total_pots_keyword_clauses": int(kw_hit.sum()),
        "per_keyword": per_kw,
        "n_pots_signature_days": len(pots_days),
        "n_pots_signature_days_with_a_pots_keyword_note": len(pots_set & hit_dates),
    }


def main():
    df = load_master()
    df["pots_z"] = lagged_z(df, "u_dip_count", sigma_floor=0.5)          # POTS marker
    df["pem_z"] = lagged_z(df, "stress_mean_sleep", sigma_floor=2.0)     # PEM marker
    df["pem_var_z"] = lagged_z(df, "stress_stdev_sleep", sigma_floor=0.5)  # PEM secondary

    both = df.dropna(subset=["pots_z", "pem_z"]).copy()
    both["pots_day"] = both["pots_z"] >= Z_THRESH
    both["pem_day"] = both["pem_z"] >= Z_THRESH

    # 1. Separability: correlation between the two markers (threshold-free).
    pear = float(np.corrcoef(both["pots_z"], both["pem_z"])[0, 1])
    sp = float(both[["pots_z", "pem_z"]].corr(method="spearman").iloc[0, 1])
    pear_var = float(np.corrcoef(both["pots_z"], both["pem_var_z"].fillna(both["pem_var_z"].mean()))[0, 1]) \
        if both["pem_var_z"].notna().sum() > 10 else float("nan")

    # 2. 2x2 contingency (POTS-day x PEM-day) + phi.
    a = int(((both["pots_day"]) & (both["pem_day"])).sum())    # both
    b = int(((both["pots_day"]) & (~both["pem_day"])).sum())   # pots only
    c = int(((~both["pots_day"]) & (both["pem_day"])).sum())   # pem only
    d = int(((~both["pots_day"]) & (~both["pem_day"])).sum())  # neither
    n = a + b + c + d
    r1, r0 = a + b, c + d
    c1, c0 = a + c, b + d
    denom = (r1 * r0 * c1 * c0) ** 0.5
    phi = float((a * d - b * c) / denom) if denom > 0 else float("nan")

    # 3. When: per-phase POTS/PEM signature-day rates.
    per_phase = []
    for ph, pid in PHASE_ORDER:
        sub = both[both["recovery_phase"] == ph]
        if len(sub) == 0:
            continue
        per_phase.append({
            "phase_id": pid, "phase": ph, "n_days": int(len(sub)),
            "pots_day_rate_pct": round(100.0 * sub["pots_day"].mean(), 1),
            "pem_day_rate_pct": round(100.0 * sub["pem_day"].mean(), 1),
            "mean_pots_z": round(float(sub["pots_z"].mean()), 3),
            "mean_pem_z": round(float(sub["pem_z"].mean()), 3),
        })

    # 4. Felt-state by group.
    def gs(mask):
        v = both.loc[mask, "gevoelscore"].dropna()
        return {"n": int(len(v)), "mean_gevoelscore": round(float(v.mean()), 3) if len(v) else None}
    groups = {
        "neither": gs((~both["pots_day"]) & (~both["pem_day"])),
        "pots_only": gs((both["pots_day"]) & (~both["pem_day"])),
        "pem_only": gs((~both["pots_day"]) & (both["pem_day"])),
        "both": gs((both["pots_day"]) & (both["pem_day"])),
        "any_pots": gs(both["pots_day"]),
        "any_pem": gs(both["pem_day"]),
    }

    # 5. Notes corroboration of POTS-signature days.
    pots_days = list(both.loc[both["pots_day"], "date"])
    notes = notes_pots_corroboration(pots_days)

    # 6. Review-requested statistics (2026-07-07 peer review).
    # (a) CI on Pearson r (Fisher z) + Spearman p -- the correlation is small but
    #     the CI decides whether "independent" is warranted.
    def _fisher_ci(r, nn):
        if nn < 4 or not np.isfinite(r):
            return (float("nan"), float("nan"))
        z = np.arctanh(r)
        se = 1.0 / np.sqrt(nn - 3)
        return (round(float(np.tanh(z - 1.96 * se)), 3), round(float(np.tanh(z + 1.96 * se)), 3))
    r_lo, r_hi = _fisher_ci(pear, n)
    _sp_rho, _sp_p = sps.spearmanr(both["pots_z"], both["pem_z"])
    # (b) CONVENTIONS 3.4 crash-drop sensitivity -- is_crash is defined partly on
    #     low gevoelscore, so the felt-state contrasts and correlation are re-run
    #     with crash days dropped.
    nc = both[both["is_crash"] != True]
    pear_nc = round(float(np.corrcoef(nc["pots_z"], nc["pem_z"])[0, 1]), 3) if len(nc) > 3 else float("nan")

    def _gsm(frame, mask):
        v = frame.loc[mask, "gevoelscore"].dropna()
        return round(float(v.mean()), 3) if len(v) else None
    crashdrop_groups = {
        "neither": _gsm(nc, (~nc["pots_day"]) & (~nc["pem_day"])),
        "pots_only": _gsm(nc, (nc["pots_day"]) & (~nc["pem_day"])),
        "pem_only": _gsm(nc, (~nc["pots_day"]) & (nc["pem_day"])),
        "both": _gsm(nc, (nc["pots_day"]) & (nc["pem_day"])),
    }

    def _crash_pct(mask):
        m = mask & (both["is_crash"] == True)
        return round(100.0 * m.sum() / max(1, mask.sum()), 1)
    crash_pct_by_group = {
        "neither": _crash_pct((~both["pots_day"]) & (~both["pem_day"])),
        "pots_only": _crash_pct((both["pots_day"]) & (~both["pem_day"])),
        "pem_only": _crash_pct((~both["pots_day"]) & (both["pem_day"])),
        "both": _crash_pct((both["pots_day"]) & (both["pem_day"])),
    }
    # (c) MWU + Cohen's d for the felt-state contrasts vs neither.
    neither_mask = (~both["pots_day"]) & (~both["pem_day"])

    def _mwu(mask1):
        aa = both.loc[mask1, "gevoelscore"].dropna().to_numpy(dtype=float)
        bb = both.loc[neither_mask, "gevoelscore"].dropna().to_numpy(dtype=float)
        if len(aa) < 5 or len(bb) < 5:
            return None
        _u, p = sps.mannwhitneyu(aa, bb, alternative="two-sided")
        sp_ = np.sqrt(((len(aa) - 1) * aa.var(ddof=1) + (len(bb) - 1) * bb.var(ddof=1)) / (len(aa) + len(bb) - 2))
        d = round(float((aa.mean() - bb.mean()) / sp_), 3) if sp_ > 0 else float("nan")
        return {"p_value": round(float(p), 5), "cohens_d_vs_neither": d, "n1": int(len(aa)), "n_neither": int(len(bb))}
    mwu_tests = {
        "pem_only_vs_neither": _mwu((~both["pots_day"]) & (both["pem_day"])),
        "pots_only_vs_neither": _mwu((both["pots_day"]) & (~both["pem_day"])),
        "both_vs_neither": _mwu((both["pots_day"]) & (both["pem_day"])),
    }
    # marker substrate transparency (thin-substrate flag)
    ud = both["u_dip_count"].dropna()
    pots_substrate = {"pct_zero": round(float((ud == 0).mean() * 100), 1), "max": int(ud.max()),
                      "signature_day_min_raw_count": int(both.loc[both["pots_day"], "u_dip_count"].min())}

    result = {
        "operationalisation": {
            "pots_marker": "u_dip_count z vs lagged baseline (within-day orthostatic U-dip proxy)",
            "pem_marker": "stress_mean_sleep z vs lagged baseline (overnight HRV-proxy load)",
            "z_threshold_for_signature_day": Z_THRESH,
            "n_days_both_markers_computable": n,
        },
        "separability": {"pearson_pots_vs_pem": round(pear, 3),
                         "pearson_ci95": [r_lo, r_hi],
                         "spearman_pots_vs_pem": round(sp, 3),
                         "spearman_p": round(float(_sp_p), 4),
                         "pearson_pots_vs_pem_variability": round(pear_var, 3),
                         "phi_contingency": round(phi, 3),
                         "shared_variance_pct": round(pear * pear * 100, 2),
                         "contingency": {"both": a, "pots_only": b, "pem_only": c, "neither": d}},
        "when_per_phase": per_phase,
        "felt_state_by_group": groups,
        "felt_state_mwu_vs_neither": mwu_tests,
        "crash_drop_sensitivity": {"pearson_crash_dropped": pear_nc, "delta_pearson": round(pear_nc - pear, 3),
                                   "felt_state_by_group_crash_dropped": crashdrop_groups,
                                   "crash_pct_by_group": crash_pct_by_group},
        "pots_marker_substrate": pots_substrate,
        "notes_corroboration": notes,
        "meta": {"stratum_4_start": str(STRATUM_4_START), "as_of_date": str(AS_OF_DATE),
                 "run_at": datetime.now().isoformat(timespec="seconds")},
    }
    (HERE / "summary.json").write_text(json.dumps(result, indent=2, default=str), encoding="utf-8")

    # ---- stdout ----
    print(f"[PEM/POTS] n_days both markers computable = {n}\n")
    print("1. SEPARABILITY (are POTS-days and PEM-days the same days?)")
    print(f"   Pearson  r(pots_z, pem_z)      = {pear:+.3f}  CI95 [{r_lo:+.3f}, {r_hi:+.3f}]  (shared var {pear*pear*100:.2f}%)")
    print(f"   Spearman r(pots_z, pem_z)      = {sp:+.3f}  p={float(_sp_p):.4f}")
    print(f"   Pearson  r(pots_z, pem_var_z)  = {pear_var:+.3f}")
    print(f"   contingency phi                = {phi:+.3f}")
    print(f"   POTS+PEM both={a}  POTS-only={b}  PEM-only={c}  neither={d}")
    print(f"   [crash-drop 3.4] r={pear_nc:+.3f} (delta {pear_nc-pear:+.3f}); POTS substrate {pots_substrate['pct_zero']}% zeros, max {pots_substrate['max']}, sig-day min count {pots_substrate['signature_day_min_raw_count']}")
    print("\n2. WHEN does the POTS signal appear (per recovery phase)?")
    print(f"   {'ph':3} {'n_days':>6} {'POTS-day%':>9} {'PEM-day%':>8} {'mean_pots_z':>11} {'mean_pem_z':>10}")
    for p in per_phase:
        print(f"   {p['phase_id']:3} {p['n_days']:>6} {p['pots_day_rate_pct']:>9} {p['pem_day_rate_pct']:>8} "
              f"{p['mean_pots_z']:>11} {p['mean_pem_z']:>10}")
    print("\n3. FELT-STATE by group (are POTS-signature days lower in gevoelscore?)")
    for k, v in groups.items():
        cd = crashdrop_groups.get(k)
        cp = crash_pct_by_group.get(k)
        extra = f"  | crash-dropped={cd}  crash%={cp}" if k in crashdrop_groups else ""
        print(f"   {k:12} n={v['n']:>4}  mean_gevoelscore={v['mean_gevoelscore']}{extra}")
    print("   MWU vs neither: "
          + "; ".join(f"{k}: {('p='+str(t['p_value'])+' d='+str(t['cohens_d_vs_neither'])) if t else 'n<5'}"
                      for k, t in mwu_tests.items()))
    print("\n4. NOTES corroboration of POTS-signature days")
    if "error" in notes:
        print(f"   {notes['error']}")
    else:
        print(f"   total POTS-keyword clauses in notes: {notes['total_pots_keyword_clauses']}")
        print(f"   POTS-signature days with a POTS-keyword note: "
              f"{notes['n_pots_signature_days_with_a_pots_keyword_note']} / {notes['n_pots_signature_days']}")
    print(f"\n[PEM/POTS] Wrote {HERE / 'summary.json'}")


if __name__ == "__main__":
    main()
