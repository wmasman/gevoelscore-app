"""Audit annotations.yaml for duplicates and overlapping loads.

Surfaces four issues:
  1. Exact duplicates: same (start, end, label).
  2. Same-day event clusters: multiple events landing on the same date.
     For each cluster, shows whether they are distinct events or
     potential duplicates.
  3. Load-bearing days: days where multiple events have explicit loads.
     Each event's loads are independent (an evening social plus a
     morning medical visit are two events with two load profiles), but
     it is worth surfacing them to spot accidental double-scoring.
  4. Umbrella vs nested-event overlap: events contained inside a long
     umbrella where the umbrella label is conceptually the same theme
     (e.g. an individual citalopram-phase span inside the
     citalopram umbrella; an individual relatiecoach session inside
     the Mirjam-periode umbrella).
"""
from __future__ import annotations

import re
from collections import defaultdict
from datetime import date
from pathlib import Path

import yaml

HERE = Path(__file__).resolve().parent
TIMELINE_ROOT = HERE.parent
DATA = TIMELINE_ROOT / "data"
ANNOTATIONS = DATA / "annotations.yaml"


def parse_date(s) -> date | None:
    if not s:
        return None
    if isinstance(s, date):
        return s
    try:
        return date.fromisoformat(str(s))
    except ValueError:
        return None


def parse_loads_from_note(note: str) -> tuple[str, str, str]:
    """Extract c/p/e load values from a note string.

    Handles both formats:
      'load: cog=3/phy=3/emo=2'   (merge_calendar_triage / merge_notes_triage)
      'load: c3/p3/e2'             (older legacy format, defensive)
    """
    if not note:
        return "", "", ""
    cm = re.search(r"\bcog\s*=\s*(\d)", note, re.IGNORECASE)
    pm = re.search(r"\bphy\s*=\s*(\d)", note, re.IGNORECASE)
    em = re.search(r"\bemo\s*=\s*(\d)", note, re.IGNORECASE)
    if cm or pm or em:
        return (cm.group(1) if cm else "",
                pm.group(1) if pm else "",
                em.group(1) if em else "")
    # Legacy "c3/p3/e2" anywhere in note
    cm2 = re.search(r"\bc(\d)\b", note, re.IGNORECASE)
    pm2 = re.search(r"\bp(\d)\b", note, re.IGNORECASE)
    em2 = re.search(r"\be(\d)\b", note, re.IGNORECASE)
    return (cm2.group(1) if cm2 else "",
            pm2.group(1) if pm2 else "",
            em2.group(1) if em2 else "")


def has_any_load(c: str, p: str, e: str) -> bool:
    return any(x for x in (c, p, e))


def clean_label(s: str) -> str:
    return re.sub(r'[^\x20-\x7e]', '', s or '').strip()


def main():
    raw = yaml.safe_load(ANNOTATIONS.read_text(encoding="utf-8")) or {}
    spans = raw.get("spans") or []
    markers = raw.get("markers") or []

    # Normalize
    norm_spans = []
    for s in spans:
        start = parse_date(s.get("start"))
        end = parse_date(s.get("end")) or start
        if start is None:
            continue
        note = s.get("note") or ""
        c, p, e = parse_loads_from_note(note)
        norm_spans.append({
            "start": start,
            "end": end,
            "label": (s.get("label") or "").strip(),
            "category": (s.get("category") or "").strip(),
            "note": note,
            "c": c, "p": p, "e": e,
            "loads": has_any_load(c, p, e),
        })

    print(f"Loaded {len(norm_spans)} spans + {len(markers)} markers.\n")

    # ---- 1) Exact duplicates -------------------------------------------------
    print("=" * 100)
    print("1) EXACT DUPLICATES (same start + end + label)")
    print("=" * 100)
    key_counts: dict[tuple, int] = defaultdict(int)
    for s in norm_spans:
        key = (s["start"], s["end"], s["label"])
        key_counts[key] += 1
    dupes = [(k, n) for k, n in key_counts.items() if n > 1]
    if not dupes:
        print("  None found. ✓")
    else:
        for k, n in dupes:
            print(f"  x{n}: {k[0]} -> {k[1]} | {clean_label(k[2])}")
    print()

    # ---- 2) Same-day event clusters ------------------------------------------
    print("=" * 100)
    print("2) SAME-DAY EVENT CLUSTERS (single date hosting 2+ point-events)")
    print("   NB: events whose start == end on the same day. Long umbrellas covering")
    print("   the date are NOT clustered here (those are §4 below).")
    print("=" * 100)
    by_date: dict[date, list[dict]] = defaultdict(list)
    for s in norm_spans:
        # Treat short spans (<= 1 day) as point-events
        if (s["end"] - s["start"]).days <= 1:
            by_date[s["start"]].append(s)
    clusters = [(d, evs) for d, evs in sorted(by_date.items()) if len(evs) > 1]
    if not clusters:
        print("  None found. ✓")
    else:
        print(f"  {len(clusters)} dates have 2+ point-events.")
        # Show the top 15 by cluster size, then summary
        clusters_sorted = sorted(clusters, key=lambda x: -len(x[1]))[:15]
        for d, evs in clusters_sorted:
            print(f"\n  {d} ({len(evs)} events):")
            for ev in evs:
                loads = f"c{ev['c'] or '-'}/p{ev['p'] or '-'}/e{ev['e'] or '-'}"
                print(f"    [{ev['category']:18}] {loads:11} {clean_label(ev['label'])[:60]}")
    print()

    # ---- 3) Load-bearing day analysis ----------------------------------------
    print("=" * 100)
    print("3) DAYS WITH MULTIPLE LOAD-BEARING EVENTS")
    print("   (per-day list of events that have explicit cog/phy/emo loads)")
    print("=" * 100)
    load_day: dict[date, list[dict]] = defaultdict(list)
    for s in norm_spans:
        if not s["loads"]:
            continue
        # Walk every date covered by the span
        d = s["start"]
        while d <= s["end"]:
            load_day[d].append(s)
            d = date.fromordinal(d.toordinal() + 1)
    multi = [(d, evs) for d, evs in load_day.items() if len(evs) > 1]
    print(f"  total load-bearing events: {sum(1 for s in norm_spans if s['loads'])}")
    print(f"  unique dates with at least one load-bearing event: {len(load_day)}")
    print(f"  dates with MULTIPLE load-bearing events: {len(multi)}")
    if multi:
        # Show the top 10 by overlap count, plus all the days with 3+ overlapping loads
        multi_sorted = sorted(multi, key=lambda x: -len(x[1]))[:15]
        print()
        for d, evs in multi_sorted:
            print(f"\n  {d} ({len(evs)} load-bearing events):")
            for ev in evs:
                loads = f"c{ev['c'] or '-'}/p{ev['p'] or '-'}/e{ev['e'] or '-'}"
                span_len = (ev["end"] - ev["start"]).days
                span_tag = f"({span_len + 1}d span)" if span_len > 0 else "(1d)"
                print(f"    [{ev['category']:18}] {loads:11} {span_tag:10} {clean_label(ev['label'])[:55]}")
    print()

    # ---- 4) Umbrella vs nested-event overlap ---------------------------------
    print("=" * 100)
    print("4) UMBRELLA-vs-NESTED OVERLAP (events nested inside long umbrellas)")
    print("   Long umbrella = levensgebeurtenis or interventie span >= 30 days.")
    print("   This is mostly INTENTIONAL (e.g. citalopram-phase inside citalopram-umbrella),")
    print("   but flagged so the user can verify.")
    print("=" * 100)
    umbrellas = [s for s in norm_spans
                 if (s["end"] - s["start"]).days >= 30
                 and s["category"] in {"levensgebeurtenis", "interventie"}]
    short_events = [s for s in norm_spans
                    if (s["end"] - s["start"]).days < 30]
    print(f"  {len(umbrellas)} umbrella spans (>=30d), {len(short_events)} short events.")
    print()
    for u in sorted(umbrellas, key=lambda u: u["start"]):
        nested = [s for s in short_events
                  if u["start"] <= s["start"] and s["end"] <= u["end"]]
        if not nested:
            continue
        u_len = (u["end"] - u["start"]).days + 1
        print(f"\n  UMBRELLA: {u['start']} -> {u['end']} ({u_len}d) "
              f"[{u['category']}] {clean_label(u['label'])[:55]}")
        print(f"    {len(nested)} nested short events:")
        # Highlight ones with same theme keyword
        u_label_lower = u["label"].lower()
        u_keywords = set(re.findall(r"\w+", u_label_lower))
        for s in sorted(nested, key=lambda x: x["start"])[:10]:
            s_label_lower = s["label"].lower()
            s_keywords = set(re.findall(r"\w+", s_label_lower))
            common = u_keywords & s_keywords - {"de", "het", "een", "van", "met", "voor",
                                                 "in", "op", "te", "en", "of"}
            theme_match = "* same theme" if common else ""
            loads = f"c{s['c'] or '-'}/p{s['p'] or '-'}/e{s['e'] or '-'}"
            print(f"      {s['start']} {loads:11} {clean_label(s['label'])[:50]} {theme_match}")
        if len(nested) > 10:
            print(f"      ... +{len(nested) - 10} more")


if __name__ == "__main__":
    main()
