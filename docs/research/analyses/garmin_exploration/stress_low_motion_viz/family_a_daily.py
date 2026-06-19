"""Family A — within-day per-minute multi-panel plots.

Per interview answers, 3 days:
  2023-11-28 — prodrome (day before deepest crash)
  2023-11-29 — peak crash day, primary 361, score 1
  2024-11-26 — rest exemplar, primary 0, score 4, resp-rest-band 636
"""
from __future__ import annotations

from datetime import date, datetime, timedelta
from pathlib import Path

import matplotlib.dates as mdates
import matplotlib.pyplot as plt
import pandas as pd

from _master_loader import PLOTS_DIR, PRIMARY, load_master
from _fit_loader import parse_day, primary_positive_minutes
from _plot_utils import savefig, stamp_footer


DAYS = [
    ("2023-11-28", "prodrome_crash014"),
    ("2023-11-29", "peak_crash014"),
    ("2024-11-26", "rest_exemplar"),
]


def _format_x(ax, day: date) -> None:
    ax.xaxis.set_major_locator(mdates.HourLocator(byhour=range(0, 24, 3)))
    ax.xaxis.set_major_formatter(mdates.DateFormatter("%H:%M"))
    start = datetime.combine(day, datetime.min.time())
    end = start + timedelta(days=1)
    ax.set_xlim(start, end)


def _plot_day(day_iso: str, label: str, master: pd.DataFrame) -> None:
    target = pd.Timestamp(day_iso).date()
    parsed = parse_day(target)
    n_stress = len(parsed["stress"])
    n_int = len(parsed["intensity"])
    n_resp = len(parsed["respiration"])
    n_hr  = len(parsed["hr"])
    print(f"  {day_iso} ({label}): stress={n_stress}, intensity={n_int}, "
          f"resp={n_resp}, hr={n_hr}")
    if n_stress == 0:
        print(f"  WARN no stress samples for {day_iso}; skipping plot")
        return

    pos_minutes = primary_positive_minutes(parsed["stress"], parsed["intensity"])

    # master row for header context
    mrow = master[master["date"] == pd.Timestamp(day_iso)]
    primary_count = mrow[PRIMARY].iloc[0] if not mrow.empty else None
    gevoelscore = mrow["gevoelscore"].iloc[0] if not mrow.empty else None
    is_crash = bool(mrow["is_crash"].iloc[0]) if not mrow.empty else False
    resp_rest = mrow["n_minutes_resp_in_rest_band_10_18"].iloc[0] if not mrow.empty else None
    resp_above = mrow["n_minutes_resp_above_18"].iloc[0] if not mrow.empty else None

    fig, axes = plt.subplots(4, 1, figsize=(13, 9), sharex=True,
                              gridspec_kw={"height_ratios": [1.4, 0.6, 1.1, 1.1]})

    # Panel 1: per-minute stress
    s_t = [t for t, _ in parsed["stress"]]
    s_v = [v for _, v in parsed["stress"]]
    ax1 = axes[0]
    ax1.plot(s_t, s_v, color="#3f6b6e", linewidth=0.8)
    for thr, col in [(50, "#a7b6a5"), (60, "#c89770"), (75, "#b04a32")]:
        ax1.axhline(thr, color=col, linestyle="--", linewidth=0.7, alpha=0.7)
        ax1.text(s_t[0] if s_t else None, thr + 0.5, f"S{thr}",
                 fontsize=7, color=col, va="bottom")
    ax1.set_ylim(0, 100)
    ax1.set_ylabel("stress")
    ax1.set_title(
        f"{day_iso}  ·  {label}  ·  "
        f"primary count {primary_count if primary_count is not None else '—'}  ·  "
        f"score {gevoelscore if gevoelscore is not None else '—'}  ·  "
        f"crash {'yes' if is_crash else 'no'}  ·  "
        f"resp rest-band {int(resp_rest) if resp_rest is not None else '—'} / "
        f"above-18 {int(resp_above) if resp_above is not None else '—'}"
    )

    # Panel 2: per-minute intensity as a stair-step
    ax2 = axes[1]
    if parsed["intensity"]:
        i_t = [t for t, _ in parsed["intensity"]]
        i_v = [v for _, v in parsed["intensity"]]
        ax2.step(i_t, i_v, where="post", color="#5a4d42", linewidth=0.9)
    ax2.set_ylim(-0.4, 5.4)
    ax2.set_yticks([0, 1, 2, 3])
    ax2.set_yticklabels(["sedentary", "light", "moderate", "vigorous"])
    ax2.set_ylabel("intensity")
    # mark intensity gap visually: where no intensity records exist for a stretch,
    # leave the panel empty (the step plot already does this)

    # Panel 3: per-minute respiration
    ax3 = axes[2]
    r_t = [t for t, _ in parsed["respiration"]]
    r_v = [v for _, v in parsed["respiration"]]
    ax3.plot(r_t, r_v, color="#c89770", linewidth=0.8)
    ax3.axhspan(10, 18, color="#3f6b6e", alpha=0.08, label="rest band 10-18")
    ax3.axhline(18, color="#b04a32", linestyle="--", linewidth=0.6, alpha=0.7)
    ax3.set_ylabel("respiration (br/min)")
    ax3.set_ylim(0, 35)
    ax3.legend(loc="upper right", fontsize=7)

    # Panel 4: per-minute HR
    ax4 = axes[3]
    h_t = [t for t, _ in parsed["hr"]]
    h_v = [v for _, v in parsed["hr"]]
    ax4.plot(h_t, h_v, color="#7a8b6b", linewidth=0.7)
    ax4.set_ylim(30, 180)
    ax4.set_ylabel("HR (bpm)")
    ax4.set_xlabel("time of day (local)")

    # primary-positive minute strip across bottom
    if pos_minutes:
        ax4.scatter(pos_minutes, [33] * len(pos_minutes),
                    s=12, color="#b04a32", marker="|", clip_on=False, zorder=5,
                    label=f"primary-positive minute (n={len(pos_minutes)})")
        ax4.legend(loc="upper right", fontsize=7)

    # sleep window shading (best effort from master row)
    if not mrow.empty and pd.notna(mrow["sleep_start_gmt"].iloc[0]):
        try:
            ss = pd.to_datetime(mrow["sleep_start_gmt"].iloc[0])
            se = pd.to_datetime(mrow["sleep_end_gmt"].iloc[0])
            for ax in axes:
                ax.axvspan(ss, se, color="#5a4d42", alpha=0.07, zorder=0)
        except Exception:
            pass

    _format_x(axes[-1], target)
    for ax in axes:
        ax.grid(True, linestyle=":", alpha=0.4)

    stamp_footer(fig)
    out = PLOTS_DIR / f"A_daily_{day_iso}_{label}.png"
    plt.tight_layout()
    savefig(fig, out)


def main(master: pd.DataFrame | None = None) -> None:
    master = master if master is not None else load_master()
    print("Family A - within-day per-minute")
    for day_iso, label in DAYS:
        _plot_day(day_iso, label, master)


if __name__ == "__main__":
    main()
