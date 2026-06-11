"""crash_v2 — apply the locked definition.md to day_entries.csv.

Outputs:
  labels_crash_v2.csv  per-day labels (crash / dip / normal) + episode metadata
  comparison_to_v1.md  diff against crash_v1 (kept / demoted / new dips)

Locked params mirror H02b/test.py crash_v1 detection. Recovery filter
and dip rules per definition.md.
"""
from __future__ import annotations

import csv
import statistics
from datetime import date, timedelta
from pathlib import Path

# ---- Locked params (mirror H02b test.py) ----
ANALYSIS_START = date(2022, 9, 3)
ANALYSIS_END = date(2026, 6, 5)
LOW_THRESHOLD = 3          # score <= 3 is sub-threshold
MIN_RUN_DAYS = 2           # tier-1 a / crash_v1 a
MERGE_WITHIN_DAYS = 3

# ---- crash_v2 additions ----
# Recovery-tail median is computed for descriptive logging only.
# The slow-recovery filter (median <= 5 -> crash, median >= 6 -> dip)
# was removed from definition.md §2.1 after first run showed all 29 v1
# episodes have tail_median in {4.0, 5.0} -- zero would have demoted.
# Tier-1 crash is now exactly crash_v1.
RECOVERY_WINDOW_DAYS = 7   # descriptive only

# Dip-cluster detection (descriptive overlay, not a tier).
# Two dips within DIP_CLUSTER_GAP_DAYS chain into the same cluster
# transitively. Clusters of size < DIP_CLUSTER_MIN_SIZE are not labelled.
DIP_CLUSTER_GAP_DAYS = 7
DIP_CLUSTER_MIN_SIZE = 2

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
DAY_ENTRIES_CSV = ROOT.parent / "H02b-stress-spikes" / "day_entries.csv"
OUT_LABELS = ROOT / "labels_crash_v2.csv"
OUT_COMPARISON = ROOT / "comparison_to_v1.md"


def load_day_entries() -> dict[date, int]:
    out: dict[date, int] = {}
    with DAY_ENTRIES_CSV.open(encoding="utf-8") as fh:
        for r in csv.DictReader(fh):
            s = r["score"]
            if s in ("", "None"):
                continue
            d = date.fromisoformat(r["date"])
            if ANALYSIS_START <= d <= ANALYSIS_END:
                out[d] = int(s)
    return out


def detect_crash_v1_episodes(day_scores: dict[date, int]) -> list[dict]:
    """Identical algorithm to H02b/test.py find_crash_episodes."""
    sorted_dates = sorted(day_scores)
    runs: list[dict] = []
    cur = None
    for d in sorted_dates:
        is_low = day_scores[d] <= LOW_THRESHOLD
        if not is_low:
            if cur and cur["days"] >= MIN_RUN_DAYS:
                runs.append(cur)
            cur = None
            continue
        if not cur:
            cur = {"start": d, "end": d, "days": 1}
            continue
        if (d - cur["end"]).days == 1:
            cur["end"] = d
            cur["days"] += 1
        else:
            if cur["days"] >= MIN_RUN_DAYS:
                runs.append(cur)
            cur = {"start": d, "end": d, "days": 1}
    if cur and cur["days"] >= MIN_RUN_DAYS:
        runs.append(cur)
    merged: list[dict] = []
    for r in runs:
        if merged and (r["start"] - merged[-1]["end"]).days <= MERGE_WITHIN_DAYS:
            merged[-1]["end"] = r["end"]
            merged[-1]["days"] += r["days"]
        else:
            merged.append({"start": r["start"], "end": r["end"], "days": r["days"]})
    return merged


def recovery_tail_median(end: date, day_scores: dict[date, int]) -> tuple[float | None, int]:
    """Median of scores in [end+1, end+7], skipping missing days.
    Returns (median or None, n_days_available).
    """
    vals = []
    for i in range(1, RECOVERY_WINDOW_DAYS + 1):
        d = end + timedelta(days=i)
        if d in day_scores:
            vals.append(day_scores[d])
    if not vals:
        return None, 0
    return statistics.median(vals), len(vals)


def classify_v1_episodes(
    v1_episodes: list[dict], day_scores: dict[date, int]
) -> list[dict]:
    """Attach tail_median to each v1 episode (descriptive). All v1 episodes
    become tier-1 crash under the current spec (no demotion).
    """
    out = []
    for ep in v1_episodes:
        median, n = recovery_tail_median(ep["end"], day_scores)
        out.append({**ep, "tail_median": median, "tail_n_days": n,
                    "verdict": "crash"})
    return out


def find_isolated_dips(
    day_scores: dict[date, int],
    crash_day_set: set[date],
    crash_tail_day_set: set[date],
) -> list[dict]:
    """Single day with score <= 3, both neighbours score >= 4 (or missing).
    Excludes days inside a crash episode or its 7-day recovery tail.
    """
    out = []
    for d, s in day_scores.items():
        if s > LOW_THRESHOLD:
            continue
        if d in crash_day_set or d in crash_tail_day_set:
            continue
        prev_d = d - timedelta(days=1)
        next_d = d + timedelta(days=1)
        prev_high = day_scores.get(prev_d, 99) >= 4 or prev_d not in day_scores
        next_high = day_scores.get(next_d, 99) >= 4 or next_d not in day_scores
        if prev_high and next_high:
            out.append({"start": d, "end": d, "days": 1, "verdict": "dip-isolated"})
    return out


def assign_dip_clusters(isolated_dips: list[dict]) -> dict[date, str]:
    """Group dips into transitive chains: dips within DIP_CLUSTER_GAP_DAYS
    of any neighbour-in-chain belong to the same cluster. Clusters of
    size < DIP_CLUSTER_MIN_SIZE are not labelled (single isolated dips
    get no cluster_id).

    Returns: dict mapping dip date -> cluster_id (e.g. 'dipcluster-001').
    Dips not in any cluster are absent from the dict.
    """
    if not isolated_dips:
        return {}
    sorted_dips = sorted(d["start"] for d in isolated_dips)
    chains: list[list[date]] = []
    cur: list[date] = [sorted_dips[0]]
    for d in sorted_dips[1:]:
        if (d - cur[-1]).days <= DIP_CLUSTER_GAP_DAYS:
            cur.append(d)
        else:
            chains.append(cur)
            cur = [d]
    chains.append(cur)
    out = {}
    cluster_i = 0
    for chain in chains:
        if len(chain) < DIP_CLUSTER_MIN_SIZE:
            continue
        cluster_i += 1
        cid = f"dipcluster-{cluster_i:03d}"
        for d in chain:
            out[d] = cid
    return out


def build_labels(
    day_scores: dict[date, int],
    crash_episodes: list[dict],
    demoted_episodes: list[dict],
    isolated_dips: list[dict],
    crash_tail_day_set: set[date],
    dip_cluster_by_date: dict[date, str] | None = None,
) -> list[dict]:
    """Per-day label rows."""
    if dip_cluster_by_date is None:
        dip_cluster_by_date = {}
    # Index every episode by its days
    day_to_episode: dict[date, tuple[str, int, dict]] = {}
    crash_id = 0
    for ep in crash_episodes:
        crash_id += 1
        eid = f"crash-{crash_id:03d}"
        d = ep["start"]
        while d <= ep["end"]:
            day_to_episode[d] = ("crash", crash_id, ep)
            d += timedelta(days=1)
    dip_id = 0
    for ep in demoted_episodes:
        dip_id += 1
        eid_int = dip_id
        d = ep["start"]
        while d <= ep["end"]:
            day_to_episode[d] = ("dip", eid_int, ep)
            d += timedelta(days=1)
    for ep in isolated_dips:
        dip_id += 1
        day_to_episode[ep["start"]] = ("dip", dip_id, ep)

    rows = []
    for d in sorted(day_scores):
        s = day_scores[d]
        if d in day_to_episode:
            label, eid, ep = day_to_episode[d]
            rows.append({
                "date": d.isoformat(),
                "score": s,
                "label": label,
                "episode_id": f"{label}-{eid:03d}",
                "episode_start": ep["start"].isoformat(),
                "episode_end": ep["end"].isoformat(),
                "episode_length_days": (ep["end"] - ep["start"]).days + 1,
                "tail_median": ep.get("tail_median", ""),
                "tail_n_days": ep.get("tail_n_days", ""),
                "verdict": ep["verdict"],
                "in_crash_tail": False,
                "dip_cluster_id": dip_cluster_by_date.get(d, "") if label == "dip" else "",
            })
        else:
            rows.append({
                "date": d.isoformat(),
                "score": s,
                "label": "normal",
                "episode_id": "",
                "episode_start": "",
                "episode_end": "",
                "episode_length_days": "",
                "tail_median": "",
                "tail_n_days": "",
                "verdict": "",
                "in_crash_tail": d in crash_tail_day_set,
                "dip_cluster_id": "",
            })
    return rows


def write_labels(rows: list[dict]) -> None:
    fields = [
        "date", "score", "label", "episode_id", "episode_start", "episode_end",
        "episode_length_days", "tail_median", "tail_n_days", "verdict",
        "in_crash_tail", "dip_cluster_id",
    ]
    with OUT_LABELS.open("w", encoding="utf-8", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=fields)
        w.writeheader()
        for r in rows:
            w.writerow(r)


def write_comparison(
    v1_episodes: list[dict],
    classified: list[dict],
    isolated_dips: list[dict],
    dip_cluster_by_date: dict[date, str] | None = None,
) -> None:
    n_iso = len(isolated_dips)
    if dip_cluster_by_date is None:
        dip_cluster_by_date = {}
    n_clustered = len(dip_cluster_by_date)
    n_clusters = len(set(dip_cluster_by_date.values()))
    day_scores = load_day_entries()

    lines = []
    lines.append("# crash_v2 vs crash_v1 — comparison\n")
    lines.append(f"Generated by `scripts/apply_crash_v2.py` from "
                 f"`{DAY_ENTRIES_CSV.name}` "
                 f"({ANALYSIS_START} -> {ANALYSIS_END}).\n")
    lines.append("## Summary\n")
    lines.append(f"- **crash_v1 episodes (score <= 3 for >= 2 days, merged):** "
                 f"{len(v1_episodes)}\n")
    lines.append(f"- **crash_v2 tier-1 (`crash`):** {len(classified)} "
                 f"(identical to v1 — slow-recovery filter removed in 2026-06-06 "
                 f"revision after 0 demotions on first run)\n")
    lines.append(f"- **crash_v2 tier-2 (`dip`):** {n_iso} "
                 f"(all from isolated single bad days; none demoted from v1)\n")
    lines.append(f"- **dip clusters (descriptive overlay):** {n_clusters} "
                 f"clusters covering {n_clustered} dips "
                 f"({n_iso - n_clustered} dips stay singleton). "
                 f"Cluster rule: ≥ 2 isolated dips within {DIP_CLUSTER_GAP_DAYS} "
                 f"days form a transitive chain.\n")
    lines.append("")

    lines.append("## Sanity-check vs definition.md §4\n")
    lines.append(f"Counts replaced predictions on first run; see definition.md §4.\n")
    lines.append(f"- Crash: {len(classified)} "
                 f"({'flag if >40' if len(classified) > 40 else 'within review bounds'})\n")
    lines.append(f"- Dip: {n_iso} "
                 f"({'flag if >500' if n_iso > 500 else 'within review bounds'})\n")
    lines.append("")

    lines.append("## crash_v1 episodes — tail-median (descriptive)\n")
    lines.append("All v1 episodes pass to crash_v2 tier-1 unchanged. The `tail_median` "
                 "is the median of scores in days [end+1, end+7] and is kept for "
                 "descriptive analysis (e.g. as a per-episode covariate).\n")
    lines.append("")
    lines.append("| # | start | end | days (low) | tail_n | tail_median |")
    lines.append("|--:|---|---|--:|--:|--:|")
    for i, e in enumerate(classified, 1):
        tm = "" if e["tail_median"] is None else f"{e['tail_median']:.1f}"
        lines.append(
            f"| {i} | {e['start']} | {e['end']} | {e['days']} | "
            f"{e['tail_n_days']} | {tm} |"
        )
    lines.append("")

    if isolated_dips:
        lines.append("## New isolated dips (not present in crash_v1)\n")
        lines.append("Single days with score <= 3 whose neighbours both score >= 4 "
                     "(or are outside the corpus). Excluded if inside a crash episode "
                     "or its 7-day recovery shadow.\n")
        lines.append("")
        lines.append("| # | date | score | prev score | next score | cluster |")
        lines.append("|--:|---|--:|--:|--:|---|")
        for i, d in enumerate(isolated_dips, 1):
            ds = d["start"]
            prev_score = day_scores.get(ds - timedelta(days=1), "—")
            next_score = day_scores.get(ds + timedelta(days=1), "—")
            cid = dip_cluster_by_date.get(ds, "")
            lines.append(
                f"| {i} | {ds.isoformat()} | {day_scores[ds]} | "
                f"{prev_score} | {next_score} | {cid or '—'} |"
            )
        lines.append("")

    # Cluster summary
    if dip_cluster_by_date:
        # Group dates by cluster_id
        by_cluster: dict[str, list[date]] = {}
        for dd, cid in dip_cluster_by_date.items():
            by_cluster.setdefault(cid, []).append(dd)
        lines.append("## Dip clusters (descriptive overlay)\n")
        lines.append(f"Transitive chains of dips within "
                     f"{DIP_CLUSTER_GAP_DAYS} days of each other. "
                     "Each row = one cluster. Per-day labels are unchanged; "
                     "this is a descriptive layer for analyses that need to "
                     "treat a 'rough patch' as one event.\n")
        lines.append("")
        lines.append("| cluster | first dip | last dip | span (days) | n dips | dip dates |")
        lines.append("|---|---|---|--:|--:|---|")
        for cid in sorted(by_cluster):
            dates_ = sorted(by_cluster[cid])
            span = (dates_[-1] - dates_[0]).days + 1
            dates_str = ", ".join(d.isoformat() for d in dates_)
            lines.append(
                f"| {cid} | {dates_[0]} | {dates_[-1]} | {span} | "
                f"{len(dates_)} | {dates_str} |"
            )
        lines.append("")

    lines.append("---")
    lines.append("")
    lines.append(f"*Generated 2026-06-06 from locked definition.md. "
                 f"Recovery filter removed; tail median kept as descriptive only.*")
    OUT_COMPARISON.write_text("\n".join(lines), encoding="utf-8")


def main():
    day_scores = load_day_entries()
    print(f"Loaded {len(day_scores)} scored days "
          f"({min(day_scores)} -> {max(day_scores)})")

    v1_episodes = detect_crash_v1_episodes(day_scores)
    print(f"crash_v1 episodes: {len(v1_episodes)}")

    classified = classify_v1_episodes(v1_episodes, day_scores)
    print(f"  -> crash: {len(classified)} (all v1 episodes pass to v2 tier-1)")

    # Build crash-shadow set (episode days + 7-day tail), used to suppress
    # isolated-dip detection inside the crash shadow per definition.md §2.4.
    crash_day_set: set[date] = set()
    crash_tail_day_set: set[date] = set()
    for ep in classified:
        d = ep["start"]
        while d <= ep["end"]:
            crash_day_set.add(d)
            d += timedelta(days=1)
        for i in range(1, RECOVERY_WINDOW_DAYS + 1):
            crash_tail_day_set.add(ep["end"] + timedelta(days=i))

    isolated_dips = find_isolated_dips(
        day_scores,
        crash_day_set,
        crash_tail_day_set,
    )
    print(f"  -> isolated dips (new in v2): {len(isolated_dips)}")

    dip_cluster_by_date = assign_dip_clusters(isolated_dips)
    n_clustered_dips = len(dip_cluster_by_date)
    n_clusters = len(set(dip_cluster_by_date.values()))
    print(f"  -> dip clusters (>=2 dips within {DIP_CLUSTER_GAP_DAYS}d): "
          f"{n_clusters} clusters covering {n_clustered_dips} dips "
          f"({len(isolated_dips) - n_clustered_dips} dips stay isolated)")

    rows = build_labels(
        day_scores,
        crash_episodes=classified,
        demoted_episodes=[],
        isolated_dips=isolated_dips,
        crash_tail_day_set=crash_tail_day_set,
        dip_cluster_by_date=dip_cluster_by_date,
    )
    write_labels(rows)
    print(f"Wrote {OUT_LABELS}")

    write_comparison(v1_episodes, classified, isolated_dips,
                     dip_cluster_by_date)
    print(f"Wrote {OUT_COMPARISON}")


if __name__ == "__main__":
    main()
