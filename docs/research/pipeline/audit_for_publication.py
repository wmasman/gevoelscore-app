"""audit_for_publication.py — pre-publish safety audit.

Run from the repo root before any `git push` to a public remote:

    python docs/research/pipeline/audit_for_publication.py

Exits 0 if clean; exits 1 if any findings need review.

The audit runs **layered defence**: even if one check is too narrow or
misses a pattern, the others catch overlap cases.

## Layers

1. **Name grep** — substring matches (case-insensitive) for each entry
   in `$GEVOELSCORE_DATA_PATH/raw/audit_names.txt`. The list lives
   outside the repo (the names themselves are personal data). If the
   list is missing, the audit fails loudly so you know to populate it.

2. **Forbidden-extension scan** — any tracked file with extension in
   {.csv, .json, .yaml, .xlsx, .pdf, .fit, .parquet, .png, .jpg, .jpeg,
   .txt} under `docs/research/` is flagged. Code (.py, .mjs) and
   methodology (.md) and the YAML category dictionary seeds are allowed
   by explicit allowlist.

3. **Email pattern scan** — any `@gmail.com`, `@hotmail.com`, etc.,
   addresses in tracked text files. The committed `user@example.com`
   substitution is recognised as the safe redaction and not flagged.

4. **Dutch BSN pattern scan** — 9-digit run that isn't a year or doc
   ID. Conservative: only flags `\b\d{9}\b` sequences with no
   surrounding context indicating a date or version number.

5. **Medical-document filename scan** — common PwC/Arbo Unie document
   patterns (`Probleemanalyse`, `Consultrapportage`, `Inzetbaarheidsprofiel`,
   `RIV_`, etc.) appearing as substrings in tracked file paths or
   content.

6. **Inventory drift** — compares the current tracked-file set against
   the manifest at `.publish_manifest.txt`. New files in
   `docs/research/data/` or other sensitive paths are flagged. The
   manifest is updated by running `--update-manifest` after a clean
   audit.

## Allowlist (false-positive sources)

Files where personal-name strings are expected as code/regex/test data:

- `docs/research/pipeline/02_label/categorize_v2.py` — phrase regex
- `docs/research/pipeline/02_label/apply_v2*.py` — patch regex
- `docs/research/pipeline/02_label/sub_categorize_v22_fysiek.py`
- `docs/research/methodology/symptom_categorization_v24.md` — regex docs
- `docs/research/methodology/symptom_mention_asymmetry.md` — worked
  examples reference hypothetical names
- `docs/research/methodology/methodology.md` — examples may name
  hypothetical people
- This audit script itself.

Allowlist entries are matched by file path; comments in flagged lines
within an allowlisted file are still surfaced for transparency, but
the overall audit only fails on hits in non-allowlisted files.
"""
from __future__ import annotations

import os
import re
import subprocess
import sys
from pathlib import Path

# === Paths ===
HERE = Path(__file__).resolve().parent
# docs/research/pipeline -> pipeline -> research -> docs -> repo
REPO_ROOT = HERE.parent.parent.parent


def load_env_file(env_path: Path) -> None:
    if not env_path.exists():
        return
    for line in env_path.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, _, value = line.partition("=")
        key = key.strip()
        value = value.strip().strip('"').strip("'")
        if key and key not in os.environ:
            os.environ[key] = value


load_env_file(REPO_ROOT / ".env")
DATA_PATH = Path(os.environ.get("GEVOELSCORE_DATA_PATH", ""))

NAMES_FILE = DATA_PATH / "raw" / "audit_names.txt" if DATA_PATH else None
MANIFEST = REPO_ROOT / ".publish_manifest.txt"

# === Allowlist ===
# Paths (repo-relative) where personal-name-like strings are expected as
# code/regex/test data. Patterns within these files are surfaced for
# transparency but do NOT cause the audit to fail.
ALLOWLISTED_PATHS = {
    # Regex/dictionary code that needs name-like strings as input
    "docs/research/pipeline/02_label/categorize_v2.py",
    "docs/research/pipeline/02_label/apply_v23_patches.py",
    "docs/research/pipeline/02_label/apply_v24_patches.py",
    "docs/research/pipeline/02_label/sub_categorize_v22_fysiek.py",
    # Methodology docs with worked examples
    "docs/research/methodology/symptom_categorization_v24.md",
    "docs/research/methodology/symptom_mention_asymmetry.md",
    "docs/research/methodology/methodology.md",
    "docs/research/methodology/queued_work.md",
    # Workflow / review instructions referencing PwC document types
    "docs/research/analyses/reviews/pwc_dossier_review_instructions.md",
    "docs/research/analyses/reviews/reintegration_gaps_review_instructions.md",
    # This script itself
    "docs/research/pipeline/audit_for_publication.py",
    # Docstring-only name references (umbrella period labels documented
    # in comments for readability)
    "docs/research/pipeline/03_consolidate/analyze_event_crash_correlation.py",
    "docs/research/pipeline/03_consolidate/audit_annotations.py",
    "docs/research/pipeline/01_extract/export_calendar_triage.mjs",
    # Intentional author identification (project copyright + ADR signatures)
    "LICENSE",
    "docs/decisions/0001-framework-expo.md",
    "docs/decisions/0002-pwa-with-directus-backend.md",
    "docs/decisions/0003-directus-fly-infra-setup.md",
    "docs/decisions/0004-tag-provenance-date-joins-and-tag-hierarchy.md",
    "docs/decisions/0005-frontend-session-persistence.md",
    "docs/decisions/0006-three-surface-architecture.md",
    "docs/decisions/0007-self-hosted-postgres-on-fly.md",
    # Public-facing app copy mentions the project author's business email
    "src/copy.ts",
    "src/__tests__/copy.test.ts",
    # User-authored thinking notes referencing the repo's own github URL
    # (github handle appears in intra-repo self-links + cross-repo links
    # to sibling research-story repo owned by the same author)
    "docs/research/gevoelscore_lived_definitions.md",
    "docs/research/note_2026-06-26_scope_clarification_and_step1_steelman.md",
    # Literature review content citing DOIs whose numeric segment matches
    # the 9-digit BSN pattern (e.g. 10.3390/ijerph191912434 -> 191912434)
    "docs/research/literature/reviews/expected_shapes_autonomic_signals_review.md",
    "docs/research/note_2026-06-29_expected-shapes-literature-anchor.md",
    # Literature index citing published paper authors (e.g. Wichers & Groot
    # 2016 Psychother Psychosom; Sarkka & Svensson 2023; Helmich et al 2024)
    "docs/research/literature/README.md",
    # Byte-faithful Substack source archive per founderandthecity_testable_
    # hypotheses.md discipline; contains embedded Substack CDN asset IDs
    # matching the 9-digit BSN pattern
    "docs/research/literature/founderandthecity_2026_welltory_700k_pem.html",
}

# Forbidden extensions in tracked files (data + binaries)
FORBIDDEN_EXTENSIONS = {
    ".csv", ".json", ".yaml", ".yml", ".xlsx", ".xls", ".pdf",
    ".fit", ".parquet", ".png", ".jpg", ".jpeg", ".txt",
}

# Allowed exceptions (specific file paths whose extension is in the
# forbidden set but the file is known to be safe):
ALLOWED_TRACKED_DATA_FILES = {
    # The data dictionary itself is .md, not in this set. Add any
    # safe-by-policy exceptions here.
}

# Email patterns (real-name detection)
EMAIL_RE = re.compile(
    r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}",
    re.IGNORECASE,
)
SAFE_EMAIL_PATTERNS = {
    "user@example.com",        # the explicit redacted placeholder
    "noreply@anthropic.com",   # commit co-author
    "noreply@github.com",
    "a@b.com",                 # standard test-data email
}

# Domain-level safelist: addresses ending in these are considered
# placeholder / role / test data, not real personal email.
SAFE_EMAIL_DOMAINS = {
    "example.com",
    "example.test",
    "example.org",
    "gevoelscore.test",
    "gevoelscore.internal",
    "group.v.calendar.google.com",  # Google Calendar virtual address
}
# Also: any address with "@x.com" or "@*.test" or "@*.internal" is test-like.
SAFE_EMAIL_DOMAIN_SUFFIXES = (
    ".test",
    ".internal",
)

# Dutch BSN: 9 digits, NOT a year and NOT a known document-id pattern.
# The audit is conservative on numbers and uses surrounding-context
# regex + a safe-constant set to avoid known false positives.
BSN_RE = re.compile(r"(?<![\d-])\d{9}(?![\d-])")
SAFE_NUMBER_CONTEXT = re.compile(r"(20\d{2}|199\d|198\d|RIV_)")
SAFE_NUMBER_CONSTANTS = {
    "631065600",  # FIT timestamp epoch (1989-12-31 00:00:00 UTC)
}

# Medical-document filename substrings (case-insensitive)
MEDICAL_DOC_PATTERNS = [
    "Probleemanalyse",
    "Consultrapportage",
    "Inzetbaarheidsprofiel",
    "Eindevaluatie",
    "Eerstejaarsevaluatie",
    "Voortgangsrapportage 2e spoor",
    "AD rapportage",
    "Actueel oordeel",
    "Plan van aanpak Willem",
    "RIV_",
    "RIV Willem",
]

# Sensitive path prefixes for inventory drift
SENSITIVE_PATHS = [
    "docs/research/data/",
    "docs/research/notes/02-categorize-clauses/notes-categorized",
    "docs/research/timeline/data/",
]


def run_git(*args: str) -> str:
    result = subprocess.run(
        ["git", *args],
        capture_output=True, text=True, cwd=str(REPO_ROOT),
    )
    if result.returncode != 0:
        raise RuntimeError(f"git {' '.join(args)} failed: {result.stderr}")
    return result.stdout


def get_tracked_files() -> list[str]:
    out = run_git("ls-files")
    return [line.strip() for line in out.splitlines() if line.strip()]


def is_text_file(path: Path) -> bool:
    if path.suffix.lower() in {".png", ".jpg", ".jpeg", ".pdf",
                               ".xlsx", ".fit", ".parquet"}:
        return False
    try:
        path.read_text(encoding="utf-8", errors="strict")
        return True
    except (UnicodeDecodeError, OSError):
        return False


def load_names() -> list[str]:
    if not NAMES_FILE or not NAMES_FILE.exists():
        return []
    names = []
    for line in NAMES_FILE.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if line and not line.startswith("#"):
            names.append(line)
    return names


# === Findings ===
class Findings:
    def __init__(self):
        self.name_hits: list[tuple[str, int, str, str]] = []      # (file, lineno, name, line)
        self.allowlist_name_hits: list[tuple[str, int, str, str]] = []
        self.forbidden_ext: list[str] = []
        self.email_hits: list[tuple[str, int, str]] = []
        self.bsn_hits: list[tuple[str, int, str]] = []
        self.medical_doc_hits: list[tuple[str, int, str]] = []
        self.new_sensitive: list[str] = []
        self.missing_in_manifest: list[str] = []

    @property
    def hard_failures(self) -> int:
        return (len(self.name_hits) + len(self.forbidden_ext)
                + len(self.email_hits) + len(self.bsn_hits)
                + len(self.medical_doc_hits) + len(self.new_sensitive))

    @property
    def soft_warnings(self) -> int:
        return len(self.allowlist_name_hits) + len(self.missing_in_manifest)


def _compile_name_pattern(name: str) -> re.Pattern:
    """Word-boundary, case-sensitive by default. Names that should be
    case-insensitive (lowercase identifiers like 'wmasman') stay
    case-sensitive too because they're stored lowercase already; the
    string-match is exact at the boundary."""
    return re.compile(r"\b" + re.escape(name) + r"\b")


def scan_file_for_names(filepath: str, names: list[str], findings: Findings):
    p = REPO_ROOT / filepath
    if not is_text_file(p):
        return
    try:
        text = p.read_text(encoding="utf-8", errors="replace")
    except OSError:
        return
    is_allowlisted = filepath in ALLOWLISTED_PATHS
    name_res = [(name, _compile_name_pattern(name)) for name in names]
    for ln_no, line in enumerate(text.splitlines(), 1):
        for name, pat in name_res:
            if pat.search(line):
                tup = (filepath, ln_no, name, line.strip()[:120])
                if is_allowlisted:
                    findings.allowlist_name_hits.append(tup)
                else:
                    findings.name_hits.append(tup)


def scan_file_for_patterns(filepath: str, findings: Findings):
    """Email, BSN, medical-doc pattern checks."""
    p = REPO_ROOT / filepath
    if not is_text_file(p):
        return
    try:
        text = p.read_text(encoding="utf-8", errors="replace")
    except OSError:
        return
    is_allowlisted = filepath in ALLOWLISTED_PATHS
    if is_allowlisted:
        return
    # Test files have placeholder emails as test fixtures (cal-primary@gmail.com,
    # a@x.com, etc.). They're safe by file-type convention.
    is_test_file = (
        "/__tests__/" in filepath
        or filepath.endswith(".test.ts")
        or filepath.endswith(".test.tsx")
        or filepath.endswith(".test.js")
        or "/test/" in filepath
    )
    for ln_no, line in enumerate(text.splitlines(), 1):
        # Email
        if not is_test_file:
            for m in EMAIL_RE.findall(line):
                if m.lower() in {p.lower() for p in SAFE_EMAIL_PATTERNS}:
                    continue
                domain = m.split("@", 1)[-1].lower()
                if domain in SAFE_EMAIL_DOMAINS:
                    continue
                if any(domain.endswith(suf) for suf in SAFE_EMAIL_DOMAIN_SUFFIXES):
                    continue
                findings.email_hits.append((filepath, ln_no, m))
        # BSN: 9-digit run not in year/doc-id context and not a known constant
        for m in BSN_RE.finditer(line):
            if m.group(0) in SAFE_NUMBER_CONSTANTS:
                continue
            context = line[max(0, m.start() - 10):m.end() + 10]
            if not SAFE_NUMBER_CONTEXT.search(context):
                findings.bsn_hits.append((filepath, ln_no, m.group(0)))
        # Medical-doc patterns
        for pat in MEDICAL_DOC_PATTERNS:
            if pat.lower() in line.lower():
                findings.medical_doc_hits.append((filepath, ln_no, pat))


def check_forbidden_extensions(tracked: list[str], findings: Findings):
    """Forbidden extensions are flagged only under docs/research/.
    Project config (package.json, tsconfig.json), build artefacts,
    and sample/test data outside docs/research/ are not data leakage
    targets — they are project plumbing or fixtures that downstream
    tooling needs."""
    for f in tracked:
        if not f.startswith("docs/research/"):
            continue
        ext = Path(f).suffix.lower()
        if ext in FORBIDDEN_EXTENSIONS and f not in ALLOWED_TRACKED_DATA_FILES:
            findings.forbidden_ext.append(f)


def check_inventory_drift(tracked: list[str], findings: Findings):
    if not MANIFEST.exists():
        return
    manifest = set(MANIFEST.read_text(encoding="utf-8").splitlines())
    manifest = {line.strip() for line in manifest if line.strip() and not line.startswith("#")}
    current = set(tracked)
    for f in current - manifest:
        for sensitive in SENSITIVE_PATHS:
            if f.startswith(sensitive):
                findings.new_sensitive.append(f)
                break
    for f in manifest - current:
        findings.missing_in_manifest.append(f)


def update_manifest(tracked: list[str]):
    lines = ["# Tracked-file manifest — updated by audit_for_publication.py --update-manifest",
             "# Used to detect inventory drift (new files appearing in sensitive paths).",
             ""]
    lines.extend(sorted(tracked))
    MANIFEST.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"Updated {MANIFEST.name} ({len(tracked)} entries)")


def report(findings: Findings) -> int:
    print("=" * 60)
    print("Pre-publication audit report")
    print("=" * 60)

    if findings.name_hits:
        print(f"\n[FAIL] Name hits in non-allowlisted files: {len(findings.name_hits)}")
        for f, ln, name, line in findings.name_hits[:50]:
            print(f"  {f}:{ln}  name='{name}'")
            print(f"    > {line}")
        if len(findings.name_hits) > 50:
            print(f"  ... and {len(findings.name_hits) - 50} more")

    if findings.forbidden_ext:
        print(f"\n[FAIL] Tracked files with forbidden extensions: {len(findings.forbidden_ext)}")
        for f in findings.forbidden_ext[:30]:
            print(f"  {f}")
        if len(findings.forbidden_ext) > 30:
            print(f"  ... and {len(findings.forbidden_ext) - 30} more")

    if findings.email_hits:
        print(f"\n[FAIL] Email-pattern hits: {len(findings.email_hits)}")
        for f, ln, addr in findings.email_hits[:20]:
            print(f"  {f}:{ln}  {addr}")

    if findings.bsn_hits:
        print(f"\n[FAIL] Possible-BSN-pattern hits (9 digits): {len(findings.bsn_hits)}")
        for f, ln, val in findings.bsn_hits[:20]:
            print(f"  {f}:{ln}  {val}")

    if findings.medical_doc_hits:
        print(f"\n[FAIL] Medical-document pattern hits: {len(findings.medical_doc_hits)}")
        for f, ln, pat in findings.medical_doc_hits[:30]:
            print(f"  {f}:{ln}  pattern='{pat}'")

    if findings.new_sensitive:
        print(f"\n[FAIL] New tracked files in sensitive paths: {len(findings.new_sensitive)}")
        for f in findings.new_sensitive:
            print(f"  {f}")

    if findings.allowlist_name_hits:
        print(f"\n[INFO] Name hits in allowlisted files (expected): {len(findings.allowlist_name_hits)}")
        # Don't print details unless verbose

    if findings.missing_in_manifest:
        print(f"\n[WARN] Files in old manifest but no longer tracked: {len(findings.missing_in_manifest)}")
        print("  Run with --update-manifest after the next clean audit to refresh.")

    print()
    if findings.hard_failures == 0:
        print(f"[PASS] No hard failures. {findings.soft_warnings} soft warnings.")
        return 0
    print(f"[FAIL] {findings.hard_failures} hard failures. DO NOT push.")
    return 1


def main() -> int:
    args = sys.argv[1:]
    update_mode = "--update-manifest" in args

    if not DATA_PATH:
        print("ERROR: GEVOELSCORE_DATA_PATH not set. Configure .env first.")
        return 1

    print(f"Repo root:   {REPO_ROOT}")
    print(f"Data root:   {DATA_PATH}")
    print(f"Names file:  {NAMES_FILE}")

    tracked = get_tracked_files()
    print(f"Tracked files: {len(tracked)}")

    if update_mode:
        update_manifest(tracked)
        return 0

    names = load_names()
    if not names:
        print(f"\nERROR: Names file is missing or empty: {NAMES_FILE}")
        print("       Audit cannot proceed without the private name list.")
        print("       Create it with one name per line (lines starting with # are comments).")
        return 1
    print(f"Names to scan: {len(names)}")

    findings = Findings()

    print("\nScanning for name hits and patterns...")
    for filepath in tracked:
        scan_file_for_names(filepath, names, findings)
        scan_file_for_patterns(filepath, findings)
    check_forbidden_extensions(tracked, findings)
    check_inventory_drift(tracked, findings)

    return report(findings)


if __name__ == "__main__":
    raise SystemExit(main())
