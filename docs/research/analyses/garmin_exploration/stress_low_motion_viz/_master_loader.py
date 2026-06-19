"""Master CSV loader + shared constants for the stress_low_motion viz session.

Single source of truth for phase boundaries, anchor dates, output path, and
the master slice loader. All family modules import from here.
"""
from __future__ import annotations

from pathlib import Path
import pandas as pd

# ----------------------------- paths ----------------------------------
DATA_ROOT = Path(r"C:\Users\Gebruiker\Documents\gevoelscore-data")
MASTER_CSV = DATA_ROOT / "unified" / "per_day_master.csv"
FIT_INDEX_CSV = DATA_ROOT / "analyses" / "garmin_exploration" / "fit_files_classified.csv"
FIT_DIR = DATA_ROOT / "garmin data" / "DI_CONNECT" / "DI-Connect-Uploaded-Files"

PLOTS_DIR = DATA_ROOT / "analyses" / "stress_low_motion_viz" / "plots"
NOTES_PATH = DATA_ROOT / "analyses" / "stress_low_motion_viz" / "viz-notes.md"
PLOTS_DIR.mkdir(parents=True, exist_ok=True)

# ----------------------------- column keys ----------------------------
PRIMARY = "stress_low_motion_min_count_S60_Mlow"
ALL_NINE = [
    f"stress_low_motion_min_count_S{s}_M{m}"
    for s in (50, 60, 75)
    for m in ("strict", "low", "below_mod")
]
RESP_ABOVE_18 = "n_minutes_resp_above_18"
RESP_REST_BAND = "n_minutes_resp_in_rest_band_10_18"

# ----------------------------- anchor dates ---------------------------
LC_ONSET = pd.Timestamp("2022-04-04")
CPAP_START = pd.Timestamp("2024-01-10")
CPAP_END = pd.Timestamp("2024-04-16")
PHASE_BOUNDARIES = {
    "unmedicated_end": pd.Timestamp("2024-04-08"),
    "buildup_end":     pd.Timestamp("2024-06-19"),
    "consolidation_end": pd.Timestamp("2026-03-19"),
}
# (phase_name, start, end, color)
PHASES_FULL = [
    ("pre_cit",        LC_ONSET,                 PHASE_BOUNDARIES["unmedicated_end"], "#8a7b6e"),
    ("buildup",        pd.Timestamp("2024-04-09"), PHASE_BOUNDARIES["buildup_end"],     "#c89770"),
    ("consolidation",  pd.Timestamp("2024-06-20"), PHASE_BOUNDARIES["consolidation_end"], "#3f6b6e"),
    ("afbouw",         pd.Timestamp("2026-03-20"), pd.Timestamp("2026-06-05"),           "#b04a32"),
]
# 4-phase variant used when user opted to skip pre-citalopram
PHASES_FOUR = PHASES_FULL  # all four are post-LC; the question was about including a "pre-LC unmedicated" view we don't need
PHASES_POST_BUILDUP = PHASES_FULL[1:]  # exclude pre_cit (per interview answer: 4 phases, skip pre-cit)


# ----------------------------- loaders --------------------------------
def load_master(parse_dates: bool = True) -> pd.DataFrame:
    df = pd.read_csv(MASTER_CSV, low_memory=False)
    if parse_dates:
        df["date"] = pd.to_datetime(df["date"])
        df = df.sort_values("date").reset_index(drop=True)
    return df


def add_phase(df: pd.DataFrame, phases=PHASES_FULL) -> pd.DataFrame:
    """Append a 'phase' column based on PHASES_FULL boundaries. Days outside
    any phase get phase=None."""
    out = df.copy()
    out["phase"] = None
    for name, start, end, _color in phases:
        mask = (out["date"] >= start) & (out["date"] <= end)
        out.loc[mask, "phase"] = name
    return out


def phase_color(name: str) -> str:
    for n, _s, _e, c in PHASES_FULL:
        if n == name:
            return c
    return "#888"


def lc_era(df: pd.DataFrame) -> pd.DataFrame:
    return df[df["date"] >= LC_ONSET].copy()
