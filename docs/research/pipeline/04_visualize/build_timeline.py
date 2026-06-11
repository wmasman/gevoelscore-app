"""Build the research timeline visualization.

Reads from canonical research data sources + user-curated annotations.yaml.
Produces a multi-row matplotlib chart spanning 2021-08-16 to 2026-06-05.

Output: docs/research/timeline/output/timeline.png

Re-run after editing data/annotations.yaml to refresh the picture.
"""
from __future__ import annotations

import csv
from datetime import date, timedelta
from pathlib import Path

import matplotlib.cm as mcm
import matplotlib.dates as mdates
import matplotlib.patches as mpatches
import matplotlib.pyplot as plt
import yaml

HERE = Path(__file__).resolve().parent
TIMELINE_ROOT = HERE.parent
DATA_DIR = TIMELINE_ROOT / "data"
OUTPUT_DIR = TIMELINE_ROOT / "output"
RESEARCH_ROOT = TIMELINE_ROOT.parent

ANNOTATIONS = DATA_DIR / "annotations.yaml"
PER_DAY_INTENSITY_CSV = DATA_DIR / "per_day_intensity.csv"
SUB_THRESHOLD_DIPS_CSV = DATA_DIR / "sub_threshold_dips.csv"
REINTEGRATION_HOURS_CSV = DATA_DIR / "reintegration_hours_2022-2024.csv"
LABELS_CSV = RESEARCH_ROOT / "garmin" / "hypotheses" / "crash_v2-definition" / "labels_crash_v2.csv"
DAILY_UDS_CSV = RESEARCH_ROOT / "garmin" / "activity-labels" / "output" / "daily_uds.csv"
SLEEP_STRESS_CSV = RESEARCH_ROOT / "garmin" / "scripts" / "sleep_stress_extract" / "sleep_stress_nightly.csv"
ACTIVITY_FEATURES_CSV = RESEARCH_ROOT / "garmin" / "activity-labels" / "output" / "activity_features_daily.csv"
DAILY_MAX_SPIKE_CSV = RESEARCH_ROOT / "garmin" / "hypotheses" / "H02b-stress-spikes" / "daily_max_spike.csv"

# Heatstripe colormaps per load axis (cog/phy/emo).
# Load 1 -> light; load 3 -> deep. Empty days remain axis-background.
LOAD_AXIS_CONFIG = {
    "cog": {"label": "cog load", "cmap": mcm.Blues,   "sub_dip_color": "#1565c0"},
    "phy": {"label": "phy load", "cmap": mcm.Oranges, "sub_dip_color": "#ef6c00"},
    "emo": {"label": "emo load", "cmap": mcm.Purples, "sub_dip_color": "#6a1b9a"},
}
SUB_THRESHOLD_DIP_COLOR = "#ad6a6a"  # muted brick; sits between dip-pink and crash-red

OUTPUT_PNG = OUTPUT_DIR / "timeline.png"

WINDOW_START = date(2021, 8, 16)
WINDOW_END = date(2026, 6, 5)

# Era boundaries (research-related; subtle gray dashed)
ERA_BOUNDARIES = [
    (date(2022, 9, 3), "score start"),
    (date(2023, 12, 31), "train/validate"),
]

# Biographical milestones (life-event anchors; saturated solid color)
# Each: (date, label, color)
BIOGRAPHICAL_LINES = [
    (date(2022, 3, 23), "covid krijgen", "#d84315"),
    (date(2022, 4, 1), "acute over / start LC", "#7e57c2"),
    (date(2022, 5, 6), "LC dx", "#7e57c2"),
    (date(2024, 7, 18), "uit dienst PwC", "#5d4037"),
]

# Post-LC era starts here; subtle background tint applied to score row
POST_LC_START = date(2022, 4, 1)

# Category color palette (warm-earth-ish, distinguishable, accessible)
CATEGORY_COLORS = {
    # User-curated
    "medical": "#7e57c2",          # purple — medical events
    "interventie": "#26a69a",      # teal — interventions
    "levensgebeurtenis": "#8d6e63", # warm brown — life events
    "high_intensity": "#ff9800",   # amber — high-energy weekends / festivals (cause, not outcome)
    "trigger": "#d84315",          # deep orange — illness triggers
    "marker": "#9e9e9e",           # neutral gray — anchors
    # Research-derived
    "crash": "#c62828",            # strong red — crashes (research-derived outcome)
    "dip": "#ef9a9a",              # soft pink-red — dips
}


def parse_date_str(s) -> date | None:
    if s is None or s == "":
        return None
    if isinstance(s, date):
        return s
    return date.fromisoformat(str(s))


def parse_float(v):
    if v in (None, "", "None"):
        return None
    try:
        return float(v)
    except ValueError:
        return None


def load_annotations() -> tuple[list[dict], list[dict]]:
    if not ANNOTATIONS.exists():
        return [], []
    raw = yaml.safe_load(ANNOTATIONS.read_text(encoding="utf-8")) or {}
    markers = raw.get("markers") or []
    spans = raw.get("spans") or []
    # Normalize dates
    for m in markers:
        m["date"] = parse_date_str(m.get("date"))
    for s in spans:
        s["start"] = parse_date_str(s.get("start"))
        s["end"] = parse_date_str(s.get("end"))
        if s["end"] is None:
            s["end"] = WINDOW_END
    return markers, spans


def load_scores_and_episodes() -> tuple[dict[date, int], list[dict]]:
    """Returns (scores_by_date, episodes_list).
    episodes_list contains crash and dip episodes with start, end, kind."""
    scores = {}
    crash_episodes_by_id = {}
    dip_dates = []
    if not LABELS_CSV.exists():
        return scores, []
    for r in csv.DictReader(LABELS_CSV.open(encoding="utf-8")):
        d = parse_date_str(r["date"])
        if d is None:
            continue
        score = r.get("score")
        if score not in (None, "", "None"):
            try:
                scores[d] = int(score)
            except ValueError:
                pass
        label = r.get("label")
        ep_id = r.get("episode_id") or ""
        if label == "crash" and ep_id:
            crash_episodes_by_id.setdefault(ep_id, []).append(d)
        elif label == "dip":
            dip_dates.append(d)

    episodes = []
    for ep_id, ds in crash_episodes_by_id.items():
        ds_sorted = sorted(ds)
        episodes.append({
            "kind": "crash",
            "start": ds_sorted[0],
            "end": ds_sorted[-1],
            "id": ep_id,
        })
    # Dips collapse into 1-day each
    for d in dip_dates:
        episodes.append({
            "kind": "dip",
            "start": d,
            "end": d,
            "id": None,
        })
    return scores, episodes


def load_per_day_loads() -> dict[date, dict[str, int]]:
    """Returns {date: {'cog': int, 'phy': int, 'emo': int}} for days with any load assigned.

    Skips reviewed_no_info entries (which have empty loads) since they contribute nothing
    to the heatstripe — the absence of a bar already encodes 'no data'.
    """
    out: dict[date, dict[str, int]] = {}
    if not PER_DAY_INTENSITY_CSV.exists():
        return out
    for r in csv.DictReader(PER_DAY_INTENSITY_CSV.open(encoding="utf-8")):
        d = parse_date_str(r.get("date"))
        if d is None:
            continue
        loads = {}
        for k in ("cog", "phy", "emo"):
            v = (r.get(k) or "").strip()
            if v.isdigit():
                loads[k] = int(v)
        if loads:
            out[d] = loads
    return out


def load_reintegration_hours() -> dict[date, float]:
    """Returns {date: total_hours} from the PwC reintegration log.

    Hours are total (primary + secondary). Only days where the user
    actually logged a number are included (vacation/empty days excluded).
    """
    out: dict[date, float] = {}
    if not REINTEGRATION_HOURS_CSV.exists():
        return out
    for r in csv.DictReader(REINTEGRATION_HOURS_CSV.open(encoding="utf-8")):
        d = parse_date_str(r.get("date"))
        if d is None:
            continue
        v = parse_float(r.get("total_hours"))
        if v is None:
            continue
        out[d] = v
    return out


def load_sub_threshold_dips() -> list[date]:
    if not SUB_THRESHOLD_DIPS_CSV.exists():
        return []
    out = []
    for r in csv.DictReader(SUB_THRESHOLD_DIPS_CSV.open(encoding="utf-8")):
        d = parse_date_str(r.get("date"))
        if d is not None:
            out.append(d)
    return sorted(out)


def load_daily_column(csv_path: Path, value_field: str, validity_field: str | None = None) -> dict[date, float]:
    if not csv_path.exists():
        return {}
    out = {}
    for r in csv.DictReader(csv_path.open(encoding="utf-8")):
        d = parse_date_str(r.get("date"))
        if d is None:
            continue
        if validity_field and r.get(validity_field, "0") != "1":
            continue
        v = parse_float(r.get(value_field))
        if v is not None:
            out[d] = v
    return out


def restrict_to_window(d: dict[date, float]) -> tuple[list[date], list[float]]:
    pairs = sorted((k, v) for k, v in d.items() if WINDOW_START <= k <= WINDOW_END)
    if not pairs:
        return [], []
    return [p[0] for p in pairs], [p[1] for p in pairs]


def date_to_num(d: date) -> float:
    return mdates.date2num(d)


def add_era_lines(ax, with_labels: bool = False, with_post_lc_tint: bool = True):
    # Post-LC background tint (subtle warm-gray-purple across all post-LC days)
    if with_post_lc_tint and POST_LC_START <= WINDOW_END:
        ax.axvspan(
            date_to_num(POST_LC_START),
            date_to_num(WINDOW_END),
            color="#7e57c2", alpha=0.05, zorder=-2,
        )
    # Research-era boundaries: subtle gray dashed
    for d, label in ERA_BOUNDARIES:
        if WINDOW_START <= d <= WINDOW_END:
            ax.axvline(date_to_num(d), color="#bdbdbd", linestyle="--",
                       linewidth=0.8, alpha=0.6, zorder=0)
            if with_labels:
                ax.text(date_to_num(d), ax.get_ylim()[1] * 0.95, " " + label,
                        fontsize=7, color="#9e9e9e", va="top", ha="left", style="italic")
    # Biographical milestones: saturated solid line
    for d, label, color in BIOGRAPHICAL_LINES:
        if WINDOW_START <= d <= WINDOW_END:
            ax.axvline(date_to_num(d), color=color, linestyle="-",
                       linewidth=1.1, alpha=0.8, zorder=1)
            if with_labels:
                ax.text(date_to_num(d), ax.get_ylim()[1] * 0.95, " " + label,
                        fontsize=8, color=color, va="top", ha="left", weight="semibold")


def rolling_mean(xs: list[float], window: int = 14) -> list[float | None]:
    """Centred rolling mean; returns None where window is incomplete."""
    n = len(xs)
    half = window // 2
    out: list[float | None] = []
    for i in range(n):
        lo = max(0, i - half)
        hi = min(n, i + half + 1)
        vals = [xs[k] for k in range(lo, hi)]
        if len(vals) >= window // 2:
            out.append(sum(vals) / len(vals))
        else:
            out.append(None)
    return out


def overlay_rolling(ax, xs: list[float], ys: list[float], color: str,
                    window: int = 14):
    rolled = rolling_mean(ys, window)
    rx, ry = [], []
    for x, y in zip(xs, rolled):
        if y is not None:
            rx.append(x); ry.append(y)
    ax.plot(rx, ry, color=color, linewidth=1.6, alpha=0.85, zorder=4)


def render_work_hours_stripe(ax, hours_by_date: dict[date, float]):
    """Render the PwC reintegration work-hours heatstripe.

    Visually distinct from cog/phy/emo (teal colormap, slightly thicker
    bars) to signal it is an OBJECTIVE measurement source, not a
    retrospective triage value. Bins: 0=none, 1-2=light, 3=mid, 4+=deep.
    """
    cmap = mcm.YlGnBu  # teal/green, contrasts with cog-blue
    def bin_to_intensity(h: float) -> float:
        if h < 1:
            return 0.0
        if h < 3:
            return 0.40
        if h < 4:
            return 0.65
        return 0.92
    for d, h in hours_by_date.items():
        if not (WINDOW_START <= d <= WINDOW_END):
            continue
        intensity = bin_to_intensity(h)
        if intensity == 0:
            continue
        color = cmap(intensity)
        x = date_to_num(d)
        ax.barh(0.5, width=1.0, left=x, height=1.0,
                color=color, edgecolor="none", zorder=2)
    ax.set_ylim(0, 1)
    ax.set_yticks([])
    ax.set_ylabel("PwC werk-uren", fontsize=8)
    ax.grid(False)
    add_era_lines(ax, with_labels=False, with_post_lc_tint=False)


def render_load_stripe(ax, loads_by_date: dict[date, dict[str, int]],
                       axis_key: str, config: dict):
    """Render one heatstripe row (cog OR phy OR emo).

    Each day with a load draws a 1-day-wide colored bar; empty days stay axis bg.
    Color comes from the per-axis cmap, mapped at fixed depths so load levels
    are visually unambiguous (1 = light, 2 = mid, 3 = deep).
    """
    cmap = config["cmap"]
    intensity_map = {1: 0.40, 2: 0.65, 3: 0.92}
    for d, axes_loads in loads_by_date.items():
        v = axes_loads.get(axis_key)
        if not v:
            continue
        if not (WINDOW_START <= d <= WINDOW_END):
            continue
        color = cmap(intensity_map.get(v, 0.5))
        x = date_to_num(d)
        ax.barh(0.5, width=1.0, left=x, height=1.0,
                color=color, edgecolor="none", zorder=2)
    ax.set_ylim(0, 1)
    ax.set_yticks([])
    ax.set_ylabel(config["label"], fontsize=8)
    ax.grid(False)
    add_era_lines(ax, with_labels=False, with_post_lc_tint=False)


def main():
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    print("Loading data sources...")
    markers, spans = load_annotations()
    print(f"  Annotations: {len(markers)} markers, {len(spans)} spans")

    scores, research_episodes = load_scores_and_episodes()
    crash_episodes = [e for e in research_episodes if e["kind"] == "crash"]
    dip_episodes = [e for e in research_episodes if e["kind"] == "dip"]
    print(f"  Scores: {len(scores)} days; crashes: {len(crash_episodes)}; dips: {len(dip_episodes)}")

    per_day_loads = load_per_day_loads()
    sub_threshold_dips = load_sub_threshold_dips()
    reintegration_hours = load_reintegration_hours()
    print(f"  Per-day loads: {len(per_day_loads)} days with cog/phy/emo")
    print(f"  Sub-threshold dips (user-triaged): {len(sub_threshold_dips)} days")
    print(f"  Reintegration hours: {len(reintegration_hours)} days with PwC work-hours")

    rhr = load_daily_column(DAILY_UDS_CSV, "resting_hr")
    rhr = {k: v for k, v in rhr.items() if v and 30 <= v <= 130}
    print(f"  RHR: {len(rhr)} days")

    sleep_stress_mean = load_daily_column(SLEEP_STRESS_CSV, "stress_mean", "valid")
    print(f"  Sleep stress mean: {len(sleep_stress_mean)} days")

    effective_exertion = load_daily_column(ACTIVITY_FEATURES_CSV, "effective_exertion_min")
    print(f"  Effective exertion: {len(effective_exertion)} days")

    max_spike = load_daily_column(DAILY_MAX_SPIKE_CSV, "max_spike_minutes", "valid")
    print(f"  Max spike minutes: {len(max_spike)} days")

    print("Rendering...")

    # Figure layout: 11 stacked rows sharing the x-axis
    # row 0: episode bands strip (crashes + dips + annotation spans)
    # row 1: point markers strip (annotation markers + era anchors)
    # row 2: gevoelscore (+ user sub-threshold dip markers)
    # row 3: cog load heatstripe (subjective triage)
    # row 4: phy load heatstripe (subjective triage)
    # row 5: emo load heatstripe (subjective triage)
    # row 6: PwC work-hours heatstripe (objective; visible only 2022-09 -> 2024-02)
    # row 7: RHR
    # row 8: sleep stress mean
    # row 9: effective exertion
    # row 10: stress spike duration
    fig, axes = plt.subplots(
        11, 1,
        figsize=(20, 15),
        sharex=True,
        gridspec_kw={"height_ratios": [1.8, 0.6, 1.6, 0.35, 0.35, 0.35, 0.35,
                                       1.1, 1.1, 1.1, 1.1]},
    )
    fig.subplots_adjust(left=0.06, right=0.985, top=0.93, bottom=0.04, hspace=0.18)

    (ax_bands, ax_markers, ax_score,
     ax_cog, ax_phy, ax_emo, ax_work,
     ax_rhr, ax_sleep, ax_exert, ax_spike) = axes

    # -------- Row 0: episode bands -----------------------------------------
    ax_bands.set_title("Research timeline 2021-08-16 to 2026-06-05",
                       fontsize=13, loc="left", pad=8)

    # Collect all bands (research crashes/dips + user spans)
    bands = []
    for c in crash_episodes:
        bands.append({"start": c["start"], "end": c["end"], "label": c["id"] or "crash",
                      "category": "crash"})
    for c in dip_episodes:
        bands.append({"start": c["start"], "end": c["end"], "label": "dip",
                      "category": "dip"})
    for s in spans:
        bands.append({"start": s["start"], "end": s["end"], "label": s.get("label", ""),
                      "category": s.get("category", "marker")})

    # Stack bands greedily (lowest row that doesn't collide)
    bands_sorted = sorted(bands, key=lambda b: (b["start"], b["end"]))
    rows: list[list[dict]] = []
    for b in bands_sorted:
        placed = False
        for row in rows:
            if all(b["start"] > existing["end"] for existing in row):
                row.append(b)
                placed = True
                break
        if not placed:
            rows.append([b])

    max_rows = max(8, len(rows))  # cap visual rows for legibility
    for row_idx, row in enumerate(rows[:max_rows]):
        for b in row:
            color = CATEGORY_COLORS.get(b["category"], "#9e9e9e")
            xs = date_to_num(b["start"])
            xe = date_to_num(b["end"]) + 1
            width = xe - xs
            ax_bands.barh(
                row_idx, width, left=xs, height=0.7,
                color=color, alpha=0.75, edgecolor="none",
            )
    ax_bands.set_ylim(-0.5, max_rows + 0.5)
    ax_bands.set_yticks([])
    ax_bands.set_ylabel("Episodes")
    ax_bands.grid(False)
    add_era_lines(ax_bands, with_labels=True)
    if len(rows) > max_rows:
        ax_bands.text(
            date_to_num(WINDOW_END) - 50, max_rows - 0.5,
            f"+{len(rows) - max_rows} more episode rows not shown",
            fontsize=7, color="#616161", ha="right", va="center",
        )

    # Legend for band colors — placed on the figure top-right so it doesn't
    # collide with any subplot row.
    legend_keys = ["crash", "dip", "high_intensity", "interventie",
                   "levensgebeurtenis", "medical", "trigger", "marker"]
    handles = [
        mpatches.Patch(color=CATEGORY_COLORS[k], label=k, alpha=0.75)
        for k in legend_keys
    ]
    fig.legend(
        handles=handles, loc="upper right",
        ncol=len(legend_keys), fontsize=8, frameon=False,
        bbox_to_anchor=(0.985, 0.99),
    )

    # -------- Row 1: point markers ------------------------------------------
    # Plot user-provided markers + era-boundary markers (subtle)
    ax_markers.set_ylim(0, 1)
    ax_markers.set_yticks([])
    ax_markers.set_ylabel("Markers")
    for m in markers:
        if m["date"] is None:
            continue
        if not (WINDOW_START <= m["date"] <= WINDOW_END):
            continue
        color = CATEGORY_COLORS.get(m.get("category", "marker"), "#9e9e9e")
        x = date_to_num(m["date"])
        ax_markers.plot([x], [0.5], marker="v", color=color, markersize=8, zorder=3)
        ax_markers.text(x, 0.85, m.get("label", ""), fontsize=7,
                        ha="center", va="top", color=color, rotation=0)
    add_era_lines(ax_markers, with_labels=False)
    ax_markers.grid(False)

    # -------- Row 2: gevoelscore line --------------------------------------
    score_dates = sorted(scores.keys())
    score_xs = [date_to_num(d) for d in score_dates]
    score_ys = [scores[d] for d in score_dates]
    ax_score.plot(score_xs, score_ys, color="#37474f", linewidth=0.7,
                  alpha=0.85, label="gevoelscore")

    # Highlight crash days
    crash_days_set = set()
    for c in crash_episodes:
        d = c["start"]
        while d <= c["end"]:
            crash_days_set.add(d)
            d += timedelta(days=1)
    crash_xs = [date_to_num(d) for d in score_dates if d in crash_days_set]
    crash_ys = [scores[d] for d in score_dates if d in crash_days_set]
    if crash_xs:
        ax_score.scatter(crash_xs, crash_ys, color=CATEGORY_COLORS["crash"],
                         s=14, zorder=3, label="crash day")

    dip_days_set = {c["start"] for c in dip_episodes}
    dip_xs = [date_to_num(d) for d in score_dates if d in dip_days_set]
    dip_ys = [scores[d] for d in score_dates if d in dip_days_set]
    if dip_xs:
        ax_score.scatter(dip_xs, dip_ys, color=CATEGORY_COLORS["dip"],
                         s=10, zorder=2, label="dip day (research)")

    # Sub-threshold dips (user-triaged from triage notes): down-pointing
    # triangle, distinct color from the research-derived dips.
    sub_dip_in_window = [d for d in sub_threshold_dips
                         if WINDOW_START <= d <= WINDOW_END]
    sub_dip_xs = [date_to_num(d) for d in sub_dip_in_window]
    sub_dip_ys = [scores.get(d, 4) for d in sub_dip_in_window]
    if sub_dip_xs:
        ax_score.scatter(sub_dip_xs, sub_dip_ys, marker="v",
                         color=SUB_THRESHOLD_DIP_COLOR, s=42,
                         zorder=4, edgecolor="white", linewidth=0.6,
                         label="sub-threshold dip (user)")

    ax_score.set_ylim(0.5, 10.5)
    ax_score.set_yticks([1, 3, 5, 7, 10])
    ax_score.set_ylabel("Gevoelscore")
    ax_score.legend(loc="upper left", fontsize=7, frameon=False)
    ax_score.grid(axis="y", linestyle=":", alpha=0.4)
    add_era_lines(ax_score)

    # -------- Rows 3-5: per-day load heatstripes (cog/phy/emo) -------------
    render_load_stripe(ax_cog, per_day_loads, "cog", LOAD_AXIS_CONFIG["cog"])
    render_load_stripe(ax_phy, per_day_loads, "phy", LOAD_AXIS_CONFIG["phy"])
    render_load_stripe(ax_emo, per_day_loads, "emo", LOAD_AXIS_CONFIG["emo"])

    # -------- Row 6: PwC work-hours (objective cross-validation source) ----
    render_work_hours_stripe(ax_work, reintegration_hours)

    # -------- Row 7: RHR ---------------------------------------------------
    rhr_xs_dates, rhr_ys = restrict_to_window(rhr)
    rhr_xs = [date_to_num(d) for d in rhr_xs_dates]
    ax_rhr.plot(rhr_xs, rhr_ys, color="#bcaaa4", linewidth=0.4, alpha=0.5)
    overlay_rolling(ax_rhr, rhr_xs, rhr_ys, "#5d4037", window=21)
    ax_rhr.set_ylabel("RHR (bpm)")
    ax_rhr.grid(axis="y", linestyle=":", alpha=0.4)
    add_era_lines(ax_rhr)

    # -------- Row 8: sleep stress mean -------------------------------------
    sss_xs_dates, sss_ys = restrict_to_window(sleep_stress_mean)
    sss_xs = [date_to_num(d) for d in sss_xs_dates]
    ax_sleep.plot(sss_xs, sss_ys, color="#90caf9", linewidth=0.4, alpha=0.5)
    overlay_rolling(ax_sleep, sss_xs, sss_ys, "#1565c0", window=21)
    ax_sleep.set_ylabel("Sleep stress (mean)")
    ax_sleep.grid(axis="y", linestyle=":", alpha=0.4)
    add_era_lines(ax_sleep)

    # -------- Row 9: effective exertion ------------------------------------
    eff_xs_dates, eff_ys = restrict_to_window(effective_exertion)
    eff_xs = [date_to_num(d) for d in eff_xs_dates]
    ax_exert.plot(eff_xs, eff_ys, color="#a5d6a7", linewidth=0.4, alpha=0.5)
    overlay_rolling(ax_exert, eff_xs, eff_ys, "#2e7d32", window=21)
    ax_exert.set_ylabel("Exertion (min)")
    ax_exert.grid(axis="y", linestyle=":", alpha=0.4)
    # Clip y-axis to 99th percentile so outliers don't compress the signal.
    if eff_ys:
        clipped_max = max(sorted(eff_ys)[int(len(eff_ys) * 0.99)], 60)
        ax_exert.set_ylim(0, clipped_max * 1.1)
    add_era_lines(ax_exert)

    # -------- Row 10: stress spike duration ---------------------------------
    spike_xs_dates, spike_ys = restrict_to_window(max_spike)
    spike_xs = [date_to_num(d) for d in spike_xs_dates]
    ax_spike.plot(spike_xs, spike_ys, color="#ffcc80", linewidth=0.4, alpha=0.5)
    overlay_rolling(ax_spike, spike_xs, spike_ys, "#ef6c00", window=21)
    ax_spike.set_ylabel("Max spike (min)")
    ax_spike.grid(axis="y", linestyle=":", alpha=0.4)
    if spike_ys:
        clipped_max = max(sorted(spike_ys)[int(len(spike_ys) * 0.99)], 60)
        ax_spike.set_ylim(0, clipped_max * 1.1)
    add_era_lines(ax_spike)

    # X-axis formatting on the bottom row
    ax_spike.set_xlim(date_to_num(WINDOW_START), date_to_num(WINDOW_END))
    ax_spike.xaxis.set_major_locator(mdates.YearLocator())
    ax_spike.xaxis.set_major_formatter(mdates.DateFormatter("%Y"))
    ax_spike.xaxis.set_minor_locator(mdates.MonthLocator(bymonth=[1, 4, 7, 10]))
    ax_spike.xaxis.set_minor_formatter(mdates.DateFormatter("%b"))
    ax_spike.tick_params(axis="x", which="major", labelsize=10, length=6)
    ax_spike.tick_params(axis="x", which="minor", labelsize=7, length=3,
                          colors="#9e9e9e")

    for ax in axes[:-1]:
        ax.tick_params(axis="x", which="both", length=0, labelbottom=False)

    plt.savefig(OUTPUT_PNG, dpi=140, bbox_inches="tight")
    plt.close(fig)
    print(f"\nWrote {OUTPUT_PNG}")
    print(f"Open with: start {OUTPUT_PNG}")


if __name__ == "__main__":
    main()
