"""First-order analysis: do user-marked high_intensity events precede crashes?

Reads:
- annotations.yaml (user-marked events with categories)
- labels_crash_v2.csv (research-derived crashes + dips)

Outputs per stdout:
1. Per-crash: nearest preceding high_intensity event (within 14 days)
2. Per-high_intensity: did a crash follow within 7 / 14 days?
3. Era-stratified summary (train: pre-2024 / validate: 2024+)
4. Umbrella-period overlap (Mirjam, Werk-transitie, vakanties)

No statistical hypothesis test (would need null sample design); this is
a descriptive cross-reference between user intuition and research labels.
"""
from __future__ import annotations

import csv
import re
from datetime import date, timedelta
from pathlib import Path

import yaml

HERE = Path(__file__).resolve().parent
TIMELINE_ROOT = HERE.parent
DATA = TIMELINE_ROOT / "data"
RESEARCH_ROOT = TIMELINE_ROOT.parent

ANNOTATIONS = DATA / "annotations.yaml"
LABELS_CSV = RESEARCH_ROOT / "garmin" / "hypotheses" / "crash_v2-definition" / "labels_crash_v2.csv"

TRAIN_END = date(2023, 12, 31)
LEAD_UP_DAYS = 7
WIDE_LEAD_UP_DAYS = 14


def parse_date(s) -> date | None:
    if not s:
        return None
    if isinstance(s, date):
        return s
    return date.fromisoformat(str(s))


def clean_ascii(s: str) -> str:
    return re.sub(r'[^\x20-\x7e]', '', s or '').strip()


def load_annotations() -> tuple[list[dict], list[dict]]:
    raw = yaml.safe_load(ANNOTATIONS.read_text(encoding="utf-8"))
    spans = []
    for s in (raw.get("spans") or []):
        spans.append({
            "start": parse_date(s.get("start")),
            "end": parse_date(s.get("end")) or parse_date(s.get("start")),
            "label": s.get("label", ""),
            "category": s.get("category", ""),
            "note": s.get("note", "") or "",
        })
    markers = []
    for m in (raw.get("markers") or []):
        markers.append({
            "date": parse_date(m.get("date")),
            "label": m.get("label", ""),
            "category": m.get("category", ""),
        })
    return spans, markers


def load_crashes_dips() -> tuple[list[dict], list[date]]:
    """Returns (crash_episodes, dip_dates)."""
    crashes_by_id: dict[str, list[date]] = {}
    dips = []
    for r in csv.DictReader(LABELS_CSV.open(encoding="utf-8")):
        d = parse_date(r["date"])
        if r["label"] == "crash":
            ep = r.get("episode_id", "") or ""
            crashes_by_id.setdefault(ep, []).append(d)
        elif r["label"] == "dip":
            dips.append(d)
    crashes = []
    for ep, ds in crashes_by_id.items():
        ds_sorted = sorted(ds)
        crashes.append({
            "id": ep,
            "start": ds_sorted[0],
            "end": ds_sorted[-1],
        })
    crashes.sort(key=lambda c: c["start"])
    return crashes, sorted(dips)


def overlaps(a_start: date, a_end: date, b_start: date, b_end: date) -> bool:
    return a_start <= b_end and b_start <= a_end


def event_ends_before_or_on(ev: dict, when: date) -> bool:
    return ev["end"] <= when


def days_between_event_end_and_target(ev_end: date, target: date) -> int:
    return (target - ev_end).days


def preceding_events(target: date, spans: list[dict], window: int,
                     categories: set[str] | None = None) -> list[tuple[int, dict]]:
    """Return list of (days_before, event) for events whose END is within
    `window` days BEFORE target. Filters by category if provided.
    Sorted by closeness (smallest days_before first)."""
    out = []
    for ev in spans:
        if categories and ev["category"] not in categories:
            continue
        if ev["end"] is None:
            continue
        # Event must have ended on or before target, within window
        if not (target - timedelta(days=window) <= ev["end"] <= target):
            continue
        days_before = (target - ev["end"]).days
        out.append((days_before, ev))
    out.sort(key=lambda x: x[0])
    return out


def contains(span: dict, day: date) -> bool:
    return span["start"] <= day <= span["end"]


def umbrella_containing(day: date, spans: list[dict],
                         min_length_days: int = 30) -> list[dict]:
    """Find long levensgebeurtenis spans (umbrella periods) that contain `day`."""
    out = []
    for ev in spans:
        if ev["category"] != "levensgebeurtenis":
            continue
        length = (ev["end"] - ev["start"]).days + 1
        if length < min_length_days:
            continue
        if contains(ev, day):
            out.append(ev)
    return out


def crash_following_event(ev: dict, crashes: list[dict], window: int) -> dict | None:
    """Did a crash start within `window` days AFTER the event ended?"""
    for c in crashes:
        gap = (c["start"] - ev["end"]).days
        if 0 <= gap <= window:
            return c
    return None


def main():
    spans, markers = load_annotations()
    crashes, dips = load_crashes_dips()
    print(f"Loaded: {len(spans)} spans, {len(markers)} markers, "
          f"{len(crashes)} crash episodes, {len(dips)} dips")

    high_intensity = [s for s in spans if s["category"] == "high_intensity"]
    interventies = [s for s in spans if s["category"] == "interventie"]
    triggers = [s for s in spans if s["category"] == "trigger"]
    umbrellas = [s for s in spans
                 if s["category"] == "levensgebeurtenis"
                 and (s["end"] - s["start"]).days >= 30]
    print(f"  high_intensity: {len(high_intensity)}")
    print(f"  interventies:   {len(interventies)}")
    print(f"  triggers:       {len(triggers)}")
    print(f"  umbrella periods (levensgebeurtenis >=30d): {len(umbrellas)}")
    print()

    # -----------------------------------------------------------
    # 1. Per-crash: nearest preceding high_intensity event
    # -----------------------------------------------------------
    print("=" * 100)
    print("PART 1: For each crash, nearest preceding high_intensity / trigger")
    print(f"        within {WIDE_LEAD_UP_DAYS} days (event END within window).")
    print("=" * 100)
    print()
    print(f"{'crash_start':12} {'era':9} {'preceded_by':40}  gap(d)  umbrella?")
    print("-" * 100)
    train_with_pre = 0
    validate_with_pre = 0
    train_total = 0
    validate_total = 0
    train_with_pre_7d = 0
    validate_with_pre_7d = 0
    for c in crashes:
        era = "train" if c["start"] <= TRAIN_END else "validate"
        if era == "train":
            train_total += 1
        else:
            validate_total += 1
        # Find nearest preceding high_intensity or trigger
        preceding = preceding_events(
            c["start"], spans, WIDE_LEAD_UP_DAYS,
            categories={"high_intensity", "trigger"},
        )
        umbrella = umbrella_containing(c["start"], spans)
        umb_str = ""
        if umbrella:
            umb_str = "; ".join(clean_ascii(u["label"])[:30] for u in umbrella)
        if preceding:
            days_before, ev = preceding[0]
            label = clean_ascii(ev["label"])[:38]
            print(f"{c['start']!s:12} {era:9} {label:40}  {days_before:>5}   {umb_str}")
            if era == "train":
                train_with_pre += 1
                if days_before <= LEAD_UP_DAYS:
                    train_with_pre_7d += 1
            else:
                validate_with_pre += 1
                if days_before <= LEAD_UP_DAYS:
                    validate_with_pre_7d += 1
        else:
            print(f"{c['start']!s:12} {era:9} {'(no preceding HI within 14d)':40}  {'':>5}   {umb_str}")

    print()
    print(f"Train crashes ({train_total}): {train_with_pre} preceded by HI in {WIDE_LEAD_UP_DAYS}d, "
          f"{train_with_pre_7d} in {LEAD_UP_DAYS}d "
          f"({train_with_pre/train_total*100:.0f}% / {train_with_pre_7d/train_total*100:.0f}%)")
    print(f"Validate crashes ({validate_total}): {validate_with_pre} preceded by HI in {WIDE_LEAD_UP_DAYS}d, "
          f"{validate_with_pre_7d} in {LEAD_UP_DAYS}d "
          f"({validate_with_pre/validate_total*100:.0f}% / {validate_with_pre_7d/validate_total*100:.0f}%)")

    # -----------------------------------------------------------
    # 2. Per-high_intensity: did a crash follow?
    # -----------------------------------------------------------
    print()
    print("=" * 100)
    print(f"PART 2: For each high_intensity event, did a crash start within {WIDE_LEAD_UP_DAYS}d after end?")
    print("=" * 100)
    print()
    print(f"{'event_end':12} {'era':9} {'event':40}  followed_by_crash?")
    print("-" * 100)
    train_hi_followed = 0
    validate_hi_followed = 0
    train_hi_total = 0
    validate_hi_total = 0
    for ev in sorted(high_intensity, key=lambda e: e["start"]):
        era = "train" if ev["end"] <= TRAIN_END else "validate"
        if era == "train":
            train_hi_total += 1
        else:
            validate_hi_total += 1
        c = crash_following_event(ev, crashes, WIDE_LEAD_UP_DAYS)
        if c:
            gap = (c["start"] - ev["end"]).days
            label = clean_ascii(ev["label"])[:38]
            print(f"{ev['end']!s:12} {era:9} {label:40}  YES (+{gap}d -> crash {c['start']})")
            if era == "train":
                train_hi_followed += 1
            else:
                validate_hi_followed += 1
        else:
            label = clean_ascii(ev["label"])[:38]
            print(f"{ev['end']!s:12} {era:9} {label:40}  no")

    print()
    print(f"Train HI events ({train_hi_total}): {train_hi_followed} followed by crash within {WIDE_LEAD_UP_DAYS}d "
          f"({train_hi_followed/max(train_hi_total,1)*100:.0f}%)")
    print(f"Validate HI events ({validate_hi_total}): {validate_hi_followed} followed by crash within {WIDE_LEAD_UP_DAYS}d "
          f"({validate_hi_followed/max(validate_hi_total,1)*100:.0f}%)")

    # -----------------------------------------------------------
    # 3. Umbrella period vs crash overlap
    # -----------------------------------------------------------
    print()
    print("=" * 100)
    print("PART 3: Crashes occurring INSIDE umbrella periods (long levensgebeurtenis >=30d)")
    print("=" * 100)
    print()
    if umbrellas:
        for u in umbrellas:
            length = (u["end"] - u["start"]).days + 1
            era = "train" if u["start"] <= TRAIN_END else "validate"
            inside_crashes = [c for c in crashes if contains(u, c["start"])]
            inside_dips = [d for d in dips if u["start"] <= d <= u["end"]]
            label = clean_ascii(u["label"])[:50]
            print(f"  {u['start']} -> {u['end']} ({length:>4}d, {era}): {label}")
            print(f"    crashes inside: {len(inside_crashes)}")
            for c in inside_crashes:
                print(f"      - crash {c['start']} -> {c['end']}")
            print(f"    dips inside: {len(inside_dips)}")
            print()
    else:
        print("  No umbrella periods >=30 days found.")

    # -----------------------------------------------------------
    # 4. Bonus: which crashes had NO user-marked context at all
    # -----------------------------------------------------------
    print("=" * 100)
    print("PART 4: Crashes with NO user-marked context (no HI/trigger within 14d,")
    print("        not inside any levensgebeurtenis span)")
    print("=" * 100)
    print()
    no_context = []
    for c in crashes:
        preceding = preceding_events(
            c["start"], spans, WIDE_LEAD_UP_DAYS,
            categories={"high_intensity", "trigger"},
        )
        any_overlap = [s for s in spans
                       if s["category"] == "levensgebeurtenis"
                       and overlaps(s["start"], s["end"], c["start"], c["end"])]
        if not preceding and not any_overlap:
            no_context.append(c)
    print(f"  {len(no_context)} of {len(crashes)} crashes have no user-marked context:")
    for c in no_context:
        era = "train" if c["start"] <= TRAIN_END else "validate"
        print(f"    {c['start']} -> {c['end']} ({era})")


if __name__ == "__main__":
    main()
