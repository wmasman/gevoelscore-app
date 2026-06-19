"""Per-phase descriptive card for stress_low_motion_min_count_S60_Mlow.

Emits median + IQR + min/max per Citalopram phase on the RAW column (no
HA-C4b §4.3 eligibility restriction), so HA-C4b v2 §7 sanity ranges can
anchor against the exact column being measured rather than a definitional
cousin.

This is the calibration card referenced by the §7 anchor strategy in
HA-C4b v2's hypothesis.md. Reproducible from a single script run against
per_day_master.csv.

Output:
- stdout: per-phase summary table
- {DATA_ROOT}/analyses/stress_low_motion_descriptive/per_phase_card.md
"""
from __future__ import annotations

from pathlib import Path
import numpy as np
import pandas as pd

from _master_loader import (
    MASTER_CSV,
    DATA_ROOT,
    PRIMARY,
    PHASES_FULL,
    add_phase,
    load_master,
)

OUT_DIR = DATA_ROOT / "analyses" / "stress_low_motion_descriptive"
OUT_DIR.mkdir(parents=True, exist_ok=True)
OUT_CARD = OUT_DIR / "per_phase_card.md"


def _percentiles(s: pd.Series) -> dict:
    s = s.dropna()
    if s.empty:
        return {"n": 0, "median": np.nan, "q25": np.nan, "q75": np.nan,
                "iqr": np.nan, "min": np.nan, "max": np.nan, "mean": np.nan,
                "std": np.nan}
    q25, q50, q75 = np.percentile(s.values, [25, 50, 75])
    return {
        "n": int(s.shape[0]),
        "median": float(q50),
        "q25": float(q25),
        "q75": float(q75),
        "iqr": float(q75 - q25),
        "min": float(s.min()),
        "max": float(s.max()),
        "mean": float(s.mean()),
        "std": float(s.std(ddof=1)),
    }


def per_phase_descriptive(df: pd.DataFrame) -> pd.DataFrame:
    df = add_phase(df, phases=PHASES_FULL)
    rows = []
    for name, _start, _end, _color in PHASES_FULL:
        sub = df[df["phase"] == name]
        stats = _percentiles(sub[PRIMARY])
        rows.append({"phase": name, **stats})
    # pooled LC era
    df_lc = df[df["phase"].notna()]
    stats = _percentiles(df_lc[PRIMARY])
    rows.append({"phase": "lc_pooled", **stats})
    return pd.DataFrame(rows)


def _fmt_md(card: pd.DataFrame) -> str:
    cols = ["phase", "n", "median", "q25", "q75", "iqr", "min", "max", "mean", "std"]
    head = "| " + " | ".join(cols) + " |\n"
    sep = "|" + "|".join([" --- "] * len(cols)) + "|\n"
    body = ""
    for _, r in card.iterrows():
        row = []
        for c in cols:
            v = r[c]
            if isinstance(v, (int, np.integer)):
                row.append(str(int(v)))
            elif isinstance(v, float) and np.isnan(v):
                row.append("NA")
            elif isinstance(v, float):
                row.append(f"{v:.1f}")
            else:
                row.append(str(v))
        body += "| " + " | ".join(row) + " |\n"
    return head + sep + body


def main() -> None:
    df = load_master()
    card = per_phase_descriptive(df)
    md = (
        f"# Per-phase descriptive card for `{PRIMARY}` (raw column)\n\n"
        f"Source: `{MASTER_CSV}`\n\n"
        f"Phases per [`citalopram_phase_stratification.md` §3](../../analyses/../../research/methodology/citalopram_phase_stratification.md#3-the-four-phase-citalopram-traject-stratification).\n\n"
        f"No HA-C4b §4.3 eligibility restriction applied — these are the RAW column distributions per phase.\n\n"
        f"{_fmt_md(card)}\n"
        f"---\n"
        f"Reproducible from: `docs/research/analyses/garmin_exploration/stress_low_motion_viz/per_phase_descriptive.py`.\n"
    )
    OUT_CARD.write_text(md, encoding="utf-8")
    print(md)
    print(f"\nWritten to: {OUT_CARD}")


if __name__ == "__main__":
    main()
