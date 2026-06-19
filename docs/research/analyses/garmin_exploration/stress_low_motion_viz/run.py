"""Entry point — produces all four families in order.

Outputs land in $GEVOELSCORE_DATA_PATH/analyses/stress_low_motion_viz/plots/
(gitignored). Re-run after master CSV updates to regenerate.
"""
from __future__ import annotations

import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))

from _master_loader import load_master, PLOTS_DIR
import family_a_daily
import family_b_timeseries
import family_c_event
import family_d_diagnostic


def main() -> None:
    print(f"Output folder: {PLOTS_DIR}")
    master = load_master()
    print(f"Master loaded: {len(master)} rows  "
          f"({master['date'].min().date()} -> {master['date'].max().date()})")

    family_b_timeseries.main(master)
    family_d_diagnostic.main(master)
    family_c_event.main(master)
    family_a_daily.main(master)   # Family A last — slowest (FIT re-parse)

    print("\nDone. Plots written to:")
    print(f"  {PLOTS_DIR}")


if __name__ == "__main__":
    main()
