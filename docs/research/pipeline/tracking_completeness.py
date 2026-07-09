#!/usr/bin/env python3
"""Tracking-completeness check for the beyond-the-guide register system (R36).

Enforces the four-leg tracking invariant documented in CONVENTIONS.md 2.4 and
the STOCKTAKE.md 2a coherence note, so the multi-home tracking cannot silently
drift or drop a thread again:

  LEDGER      docs/research/personal_hypotheses.md            (## P# entries + the crosswalk table)
  STOCKTAKE   docs/research/STOCKTAKE.md                      (2a personal register)
  TEST INDEX  docs/research/analyses/hypotheses/registry.md   (1a register: provenance tags)
  ON-STAGE    <site>/data/addendum-register.json              (optional cross-repo; --site or GEVOELSCORE_SITE_PATH)

Hard invariants (FAIL, exit 1):
  - every '## P#' ledger entry has exactly one crosswalk row, and vice versa
  - the ledger's P# set matches STOCKTAKE 2a's P# set
  - the site register (if given) is valid JSON and every item carries the required fields

Soft checks (WARN; --strict promotes them to FAIL):
  - every hypothesis test folder is covered by a registry 1a tag
  - the site register's guide-extension items match the expected set

Run standalone (python docs/research/pipeline/tracking_completeness.py) or from a
pre-commit / pre-push hook. Stdlib only.
"""
from __future__ import annotations

import argparse
import json
import os
import re
import sys
from pathlib import Path

RESEARCH = Path(__file__).resolve().parents[1]  # .../docs/research
LEDGER = RESEARCH / "personal_hypotheses.md"
STOCKTAKE = RESEARCH / "STOCKTAKE.md"
REGISTRY = RESEARCH / "analyses" / "hypotheses" / "registry.md"
HYP_DIR = RESEARCH / "analyses" / "hypotheses"

SKIP_DIRS = {"_archive", "__pycache__"}
EXPECTED_GUIDE_EXTENSIONS = {"rest-stress-low-motion", "what-the-watch-catches", "best-in-the-middle"}
REQUIRED_ITEM_FIELDS = ("id", "title", "kind", "stage", "note", "provenance")

fails: list[str] = []
warns: list[str] = []
infos: list[str] = []


def read(p: Path) -> str:
    return p.read_text(encoding="utf-8") if p.exists() else ""


def slice_section(text: str, heading_re: str, stop_re: str = r"^#{1,3} ") -> str:
    """Body from the heading matching heading_re up to the next heading matching stop_re."""
    m = re.search(heading_re, text, re.M)
    if not m:
        return ""
    rest = text[m.end():]
    stop = re.search(stop_re, rest, re.M)
    return rest[: stop.start()] if stop else rest


def check_ledger_stocktake() -> None:
    ledger = read(LEDGER)
    if not ledger:
        fails.append(f"ledger not found: {LEDGER}")
        return
    entries = set(re.findall(r"^## (P\d+[a-z]?)\.", ledger, re.M))
    xwalk_sec = slice_section(ledger, r"^## Register crosswalk & status")
    xwalk = set(re.findall(r"^\|\s*(P\d+[a-z]?)\s*\|", xwalk_sec, re.M))
    if not xwalk:
        fails.append("ledger crosswalk table not found or empty (## Register crosswalk & status)")
        return
    infos.append(f"ledger: {len(entries)} P-entries, {len(xwalk)} crosswalk rows")
    for p in sorted(entries - xwalk):
        fails.append(f"ledger P-entry '{p}' has no crosswalk row")
    for p in sorted(xwalk - entries):
        fails.append(f"crosswalk row '{p}' has no matching '## {p}' entry")

    stk = read(STOCKTAKE)
    stk_sec = slice_section(stk, r"^### 2a\.", stop_re=r"^#{2,3} ")
    if not stk_sec:
        warns.append("STOCKTAKE 2a section not found; skipped ledger<->stocktake check")
        return
    first_cells = re.findall(r"^\|\s*(P[\w, ]+?)\s*\|", stk_sec, re.M)
    stk_ps = set(re.findall(r"P\d+[a-z]?", " ".join(first_cells)))
    for p in sorted(xwalk - stk_ps):
        fails.append(f"thread '{p}' is in the ledger crosswalk but missing from STOCKTAKE 2a")
    for p in sorted(stk_ps - xwalk):
        fails.append(f"thread '{p}' is in STOCKTAKE 2a but missing from the ledger crosswalk")


def check_test_tags() -> None:
    sec = slice_section(read(REGISTRY), r"^## 1a\.")
    if not sec:
        warns.append("registry 1a provenance index not found; skipped test-tag check")
        return
    tokens = {t.lower() for t in re.findall(
        r"(?i)\b(ha-?[a-z]?\d+[a-z0-9-]*|h\d+[a-z]*|k\d+|s\d+[a-z]*|peri-event-covid|post-crash-exertion-relapse|crash_v[12])\b",
        sec)}
    wildcard = "threshold-monotonicity-diagnostic" in sec.lower()
    if not HYP_DIR.exists():
        return
    folders = sorted(p.name for p in HYP_DIR.iterdir() if p.is_dir() and p.name not in SKIP_DIRS)
    uncovered = []
    for d in folders:
        dl = d.lower()
        covered = any(dl.startswith(t) or t in dl for t in tokens) \
            or (wildcard and "threshold-monotonicity-diagnostic" in dl)
        if not covered:
            uncovered.append(d)
    infos.append(f"test index: {len(folders)} hypothesis folders, {len(folders) - len(uncovered)} covered by a 1a tag")
    for d in uncovered:
        warns.append(f"hypothesis folder not covered by a registry 1a tag: {d}/")


def check_site(site_path: str) -> None:
    reg = Path(site_path) / "data" / "addendum-register.json"
    if not reg.exists():
        warns.append(f"site register not found (skipped): {reg}")
        return
    try:
        d = json.loads(reg.read_text(encoding="utf-8"))
    except json.JSONDecodeError as e:
        fails.append(f"site register is not valid JSON: {e}")
        return
    items = [it for g in d.get("groups", []) for it in g.get("items", [])]
    n_beyond = sum(1 for it in items if it.get("provenance") == "beyond")
    ge = {it["id"] for it in items if it.get("provenance") == "guide-extension"}
    infos.append(f"site register: {len(items)} items ({n_beyond} beyond / {len(ge)} guide-extension)")
    for it in items:
        for field in REQUIRED_ITEM_FIELDS:
            if not it.get(field):
                fails.append(f"site register item '{it.get('id', '?')}' missing required field '{field}'")
    for extra in sorted(ge - EXPECTED_GUIDE_EXTENSIONS):
        warns.append(f"site register guide-extension '{extra}' is not in the expected set")
    for missing in sorted(EXPECTED_GUIDE_EXTENSIONS - ge):
        warns.append(f"expected guide-extension '{missing}' missing from the site register")


def main() -> None:
    ap = argparse.ArgumentParser(description="Beyond-the-guide tracking-completeness check (R36).")
    ap.add_argument("--site", default=os.environ.get("GEVOELSCORE_SITE_PATH"),
                    help="path to the wiggers_research_story/site repo (or set GEVOELSCORE_SITE_PATH)")
    ap.add_argument("--strict", action="store_true", help="promote WARN to FAIL (exit 1 on any warning)")
    args = ap.parse_args()

    print("=" * 60)
    print("Tracking-completeness check (beyond-the-guide register, R36)")
    print("=" * 60)

    check_ledger_stocktake()
    check_test_tags()
    if args.site:
        check_site(args.site)
    else:
        infos.append("no --site / GEVOELSCORE_SITE_PATH; skipped the on-stage cross-repo check")

    for line in infos:
        print(f"[INFO] {line}")
    for w in warns:
        print(f"[WARN] {w}")
    for f in fails:
        print(f"[FAIL] {f}")

    print("-" * 60)
    hard = bool(fails) or (bool(warns) and args.strict)
    if hard:
        print(f"[FAIL] {len(fails)} error(s), {len(warns)} warning(s).")
        sys.exit(1)
    print(f"[PASS] no errors, {len(warns)} warning(s).")
    sys.exit(0)


if __name__ == "__main__":
    main()
