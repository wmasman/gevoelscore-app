"""Dispatch dossier-review actions from filled CSV into triage_events.csv.

Reads:  data/pwc_dossier_review_filled_v2.csv (user-filled)
Writes (idempotent upserts): data/triage_events.csv
Audit log: data/dispatch_dossier_actions.log

User vocabulary in `action_to_take`:
  keep    -> add to triage_events with suggested_annotations_category
  drop    -> skip (don't add)
  skip    -> skip
  (other) -> skip with warning

`user_label_override` overrides:
  "as event"   -> confirm single-day event (category stays as suggested)
  "as context" -> downgrade to `levensgebeurtenis` (background umbrella)
  (other text) -> use as actual label override

`user_notes` is preserved in the `note` field of the new entry.
"""
from __future__ import annotations

import csv
import re
from pathlib import Path

HERE = Path(__file__).resolve().parent
DATA = HERE.parent / "data"

INPUT = DATA / "pwc_dossier_review_filled_v2.csv"
TRIAGE_EVENTS = DATA / "triage_events.csv"
AUDIT_LOG = DATA / "dispatch_dossier_actions.log"

SOURCE_TAG = "pwc_dossier_2022-2024"


def read_csv_indexed(path: Path) -> dict:
    """Returns {(date_start, label): row} for existing triage_events."""
    if not path.exists():
        return {}
    out = {}
    for r in csv.DictReader(path.open(encoding="utf-8")):
        ds = r.get("date_start", "")
        lbl = r.get("label", "")
        if ds:
            out[(ds, lbl)] = r
    return out


def write_csv(path: Path, rows: list[dict], fields: list[str]):
    rows.sort(key=lambda r: (r.get("date_start", ""), r.get("label", "")))
    with path.open("w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=fields)
        w.writeheader()
        for r in rows:
            w.writerow({k: r.get(k, "") for k in fields})


def resolve_category(suggested: str, label_override_raw: str, user_notes: str) -> str:
    """Apply user overrides to the suggested category."""
    lo = (label_override_raw or "").strip().lower()
    un = (user_notes or "").strip().lower()

    # Special: "not a crash but this is context" -> levensgebeurtenis
    if "not a crash" in lo or "not a crash" in un:
        return "levensgebeurtenis"
    # Generic "as context" -> levensgebeurtenis (background umbrella)
    if "as context" in lo or "as context" in un:
        return "levensgebeurtenis"
    # "as event" -> confirm category as suggested (no change needed)
    if "as event" in lo:
        return suggested
    return suggested


def resolve_label(title: str, label_override_raw: str) -> str:
    """If label_override is a real label (not a meta-marker), use it; else keep title."""
    lo = (label_override_raw or "").strip()
    if not lo:
        return title
    # Meta-markers that aren't actual labels
    if lo.lower() in ("as event", "as context") or lo.lower().startswith("not a crash"):
        return title
    return lo


def main():
    if not INPUT.exists():
        print(f"ERROR: {INPUT} does not exist.")
        return 1

    rows = list(csv.DictReader(INPUT.open(encoding="utf-8")))
    existing = read_csv_indexed(TRIAGE_EVENTS)
    audit_lines = []

    n_added = 0
    n_skipped = 0
    n_unknown = 0
    cat_counts = {}

    for r in rows:
        action = (r.get("action_to_take") or "").strip().lower()
        ds = r.get("date_start", "").strip()
        de = (r.get("date_end") or ds).strip()
        suggested_cat = (r.get("suggested_annotations_category") or "").strip()
        title = (r.get("title") or "").strip()
        label_override = (r.get("user_label_override") or "").strip()
        user_notes = (r.get("user_notes") or "").strip()
        dossier_notes = (r.get("dossier_notes") or "").strip()
        dossier_type = (r.get("dossier_type") or "").strip()
        person = (r.get("person") or "").strip()
        source_pdf = (r.get("source_pdf") or "").strip()

        if action in ("drop", "skip"):
            n_skipped += 1
            audit_lines.append(f"{ds} {dossier_type}: SKIP ({action}) — {user_notes[:60]}")
            continue

        if action != "keep":
            n_unknown += 1
            audit_lines.append(f"{ds} {dossier_type}: UNKNOWN action {action!r}, treating as skip")
            continue

        # KEEP path
        category = resolve_category(suggested_cat, label_override, user_notes)
        label = resolve_label(title, label_override)
        cat_counts[category] = cat_counts.get(category, 0) + 1

        # Combine notes: dossier_notes + user clarification + PDF source
        note_parts = []
        if user_notes:
            note_parts.append(f"user: {user_notes}")
        if dossier_notes:
            note_parts.append(f"dossier: {dossier_notes}")
        if source_pdf:
            note_parts.append(f"src: {source_pdf}")
        if person:
            note_parts.append(f"person: {person}")
        combined_note = " | ".join(note_parts)

        existing[(ds, label)] = {
            "date_start": ds,
            "date_end": de,
            "label": label,
            "category": category,
            "cognitive_load": "",
            "physical_load": "",
            "emotional_load": "",
            "source": SOURCE_TAG,
            "note": combined_note,
        }
        n_added += 1
        cat_note = f" (cat: {suggested_cat} -> {category})" if category != suggested_cat else ""
        audit_lines.append(f"{ds} -> {de} keep [{category}]: {label}{cat_note}")

    fields = ["date_start", "date_end", "label", "category",
              "cognitive_load", "physical_load", "emotional_load",
              "source", "note"]
    write_csv(TRIAGE_EVENTS, list(existing.values()), fields)

    with AUDIT_LOG.open("w", encoding="utf-8") as f:
        f.write("\n".join(audit_lines))

    print(f"Dispatched {len(rows)} dossier rows:")
    print(f"  kept (added to triage_events): {n_added}")
    print(f"  dropped/skipped: {n_skipped}")
    print(f"  unknown action: {n_unknown}")
    print()
    print("Category distribution of kept entries:")
    for k, n in sorted(cat_counts.items(), key=lambda x: -x[1]):
        print(f"  {k}: {n}")
    print()
    print(f"triage_events.csv now: {len(existing)} entries")
    print(f"Audit log: {AUDIT_LOG}")


if __name__ == "__main__":
    raise SystemExit(main())
