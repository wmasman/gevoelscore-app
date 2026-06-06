"""Classify every FIT file in the Garmin GDPR dump by file_id.type and product.

Reads both zip parts, opens each FIT file with fitdecode, extracts the file_id
message, and writes a CSV with: filename, size_bytes, type, garmin_product,
serial_number, time_created.

Run from any cwd; paths are absolute. Output CSV goes to docs/research/garmin/output/.

The point: the GDPR dump bundles ~21k FIT files with no metadata. Before we can
mine sub-daily signal (HR spikes, stress spread, body-battery dips) we need to
know which files actually carry that signal versus which are tiny housekeeping
files (settings, totals, weight scale exports).
"""
from __future__ import annotations

import csv
import sys
import zipfile
from pathlib import Path

import fitdecode

GARMIN_DUMP = Path(
    r"C:\Users\Gebruiker\Documents\gevoelscore-data\garmin data\DI_CONNECT\DI-Connect-Uploaded-Files"
)
ZIPS = ["UploadedFiles_0-_Part1.zip", "UploadedFiles_0-_Part2.zip"]
OUT_CSV = Path(__file__).resolve().parent.parent / "output" / "fit_files_classified.csv"


def read_file_id(buf: bytes) -> dict:
    """Return file_id fields from the first matching message; empty dict on failure."""
    try:
        with fitdecode.FitReader(buf) as fit:
            for frame in fit:
                if isinstance(frame, fitdecode.FitDataMessage) and frame.name == "file_id":
                    return {f.name: f.value for f in frame.fields}
    except Exception as exc:  # malformed/truncated FIT — record but don't abort
        return {"_error": repr(exc)[:200]}
    return {}


def main() -> int:
    OUT_CSV.parent.mkdir(parents=True, exist_ok=True)
    rows: list[dict] = []

    for zip_name in ZIPS:
        zip_path = GARMIN_DUMP / zip_name
        if not zip_path.exists():
            print(f"missing {zip_path}", file=sys.stderr)
            continue
        with zipfile.ZipFile(zip_path) as zf:
            names = [n for n in zf.namelist() if n.endswith(".fit")]
            print(f"{zip_name}: {len(names)} FIT files", file=sys.stderr)
            for i, name in enumerate(names):
                if i % 1000 == 0:
                    print(f"  {zip_name} {i}/{len(names)}", file=sys.stderr)
                info = zf.getinfo(name)
                buf = zf.read(name)
                fid = read_file_id(buf)
                rows.append(
                    {
                        "zip": zip_name,
                        "filename": name,
                        "size_bytes": info.file_size,
                        "type": str(fid.get("type", "")),
                        "garmin_product": str(fid.get("garmin_product", "")),
                        "manufacturer": str(fid.get("manufacturer", "")),
                        "serial_number": str(fid.get("serial_number", "")),
                        "time_created": str(fid.get("time_created", "")),
                        "error": fid.get("_error", ""),
                    }
                )

    fieldnames = list(rows[0].keys())
    with OUT_CSV.open("w", newline="", encoding="utf-8") as fh:
        w = csv.DictWriter(fh, fieldnames=fieldnames)
        w.writeheader()
        w.writerows(rows)
    print(f"wrote {len(rows)} rows -> {OUT_CSV}", file=sys.stderr)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
