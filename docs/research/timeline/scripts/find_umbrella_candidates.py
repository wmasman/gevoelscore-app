"""Surface candidate umbrella spans for 2024 and 2025 by clustering events
on shared keywords across time.

A "candidate umbrella" is a group of >=2 events that share a meaningful
keyword AND span >=2 months (so the cluster reflects a recurring theme,
not just consecutive same-day events that we already collapse via
multi-day cluster consolidation).

Reads:  data/triage_events.csv (the source of curated events)
Writes: data/umbrella_candidates_2024-2025.csv

Output columns:
  cluster_id, keyword, n_events, date_first, date_last, span_days,
  suggested_label, events_in_cluster, action_to_take, user_label, user_notes

The user reviews each candidate cluster and decides:
  make_umbrella       -> create a levensgebeurtenis span over the cluster
  split_into_separate -> keep events as-is (no umbrella)
  skip                -> dismiss the cluster (false positive)
"""
from __future__ import annotations

import csv
import re
from collections import defaultdict
from datetime import date
from pathlib import Path

HERE = Path(__file__).resolve().parent
DATA = HERE.parent / "data"

INPUT = DATA / "triage_events.csv"
OUTPUT = DATA / "umbrella_candidates_2024-2025.csv"

# Dutch + English stopwords + common boilerplate so cluster keywords are meaningful
STOPWORDS = {
    "de", "het", "een", "en", "in", "met", "naar", "op", "voor", "aan", "van",
    "te", "ook", "dag", "dagen", "weekend", "uit", "om", "tot", "als",
    "to", "the", "a", "and", "with", "in", "at", "of", "for",
    "add", "event", "events", "note", "notes", "this",
    "the", "had", "have", "was", "were",
    "context", "load", "loads",
}


def normalize_label(s: str) -> list[str]:
    """Extract meaningful keywords from a label."""
    s = (s or "").lower()
    # Strip "add_event " / "add events: " prefixes
    s = re.sub(r"^\s*(add[_\s]events?|add\s+as\s+events?)[:,\s]*", "", s)
    words = re.findall(r"[a-z]{4,}", s)
    return [w for w in words if w not in STOPWORDS]


def main():
    if not INPUT.exists():
        print(f"ERROR: {INPUT} does not exist.")
        return 1

    rows = list(csv.DictReader(INPUT.open(encoding="utf-8")))

    # Filter to single-day events in 2024 and 2025
    # (existing multi-day spans are already umbrellas)
    candidates = []
    for r in rows:
        ds = r.get("date_start", "")
        de = r.get("date_end") or ds
        if ds.startswith("2024") or ds.startswith("2025"):
            if ds == de:  # only single-day events
                candidates.append({
                    "date": ds,
                    "label": r.get("label", ""),
                    "category": r.get("category", ""),
                    "source": r.get("source", ""),
                })
    print(f"Single-day events in 2024-2025: {len(candidates)}")

    # Build keyword index: keyword -> list of (date, label)
    kw_index: dict[str, list[dict]] = defaultdict(list)
    for c in candidates:
        for kw in normalize_label(c["label"]):
            kw_index[kw].append(c)

    # Find clusters: keyword with >=2 events AND spanning >=60 days (2 months)
    clusters = []
    for kw, events in kw_index.items():
        if len(events) < 2:
            continue
        events_sorted = sorted(events, key=lambda e: e["date"])
        d_first = date.fromisoformat(events_sorted[0]["date"])
        d_last = date.fromisoformat(events_sorted[-1]["date"])
        span_days = (d_last - d_first).days
        if span_days < 60:
            continue
        clusters.append({
            "keyword": kw,
            "events": events_sorted,
            "n": len(events_sorted),
            "date_first": d_first,
            "date_last": d_last,
            "span_days": span_days,
        })

    # Sort by n_events DESC then span_days DESC
    clusters.sort(key=lambda c: (-c["n"], -c["span_days"]))

    print(f"\nFound {len(clusters)} candidate clusters (>=2 events, >=60 day span):")
    print()

    # Write review CSV
    rows_out = []
    for i, c in enumerate(clusters, 1):
        ev_summary = " | ".join(f"{e['date']}: {e['label'][:40]}" for e in c["events"])
        rows_out.append({
            "cluster_id": i,
            "keyword": c["keyword"],
            "n_events": c["n"],
            "date_first": c["date_first"].isoformat(),
            "date_last": c["date_last"].isoformat(),
            "span_days": c["span_days"],
            "suggested_label": f"{c['keyword'].title()} (umbrella)",
            "events_in_cluster": ev_summary[:500],
            "action_to_take": "",
            "user_label": "",
            "user_notes": "",
        })
        # Print summary
        print(f"  [{i}] keyword '{c['keyword']}' — {c['n']} events, "
              f"{c['date_first']} -> {c['date_last']} ({c['span_days']}d)")
        for e in c["events"]:
            print(f"        {e['date']}: {e['label'][:60]}")
        print()

    fields = ["cluster_id", "keyword", "n_events",
              "date_first", "date_last", "span_days",
              "suggested_label", "events_in_cluster",
              "action_to_take", "user_label", "user_notes"]
    with OUTPUT.open("w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=fields)
        w.writeheader()
        for r in rows_out:
            w.writerow(r)
    print(f"Wrote {OUTPUT}")


if __name__ == "__main__":
    main()
