"""Probe: dump first 15 monitoring frames + 5 monitoring_info frames from
one mid-window monitoring_b file. Goal: see what timestamp fields look
like at the fitdecode layer so we can handle timestamp_16 correctly."""
from __future__ import annotations

import csv
import io
import sys
import zipfile
from pathlib import Path

import fitdecode

GARMIN_DUMP = Path(
    r"C:\Users\Gebruiker\Documents\gevoelscore-data\garmin data\DI_CONNECT\DI-Connect-Uploaded-Files"
)
CLASSIFIED_CSV = Path(__file__).resolve().parent.parent.parent / "output" / "fit_files_classified.csv"


def main() -> int:
    # Pick a mid-window file with known data presence (2023-06-07 had 762 stress)
    with CLASSIFIED_CSV.open(encoding="utf-8") as fh:
        rows = [r for r in csv.DictReader(fh) if r["type"] == "monitoring_b"]
    rows.sort(key=lambda r: r["time_created"])
    target = next(r for r in rows if r["time_created"].startswith("2023-06-07"))
    print(f"file: {target['filename']}", file=sys.stderr)

    z = zipfile.ZipFile(GARMIN_DUMP / target["zip"])
    buf = z.read(target["filename"])
    z.close()

    n_mon = 0
    n_info = 0
    with fitdecode.FitReader(io.BytesIO(buf)) as fit:
        for frame in fit:
            if not isinstance(frame, fitdecode.FitDataMessage):
                continue
            if frame.name == "monitoring_info" and n_info < 5:
                n_info += 1
                print(f"\n[monitoring_info {n_info}]")
                for f in frame.fields:
                    print(f"  {f.name} = {f.value!r}")
            if frame.name == "monitoring" and n_mon < 15:
                n_mon += 1
                print(f"\n[monitoring {n_mon}]")
                for f in frame.fields:
                    print(f"  {f.name} = {f.value!r}")
                try:
                    resolved = frame.get_value("timestamp")
                    print(f"  >> get_value('timestamp') = {resolved!r}")
                except Exception as e:
                    print(f"  >> get_value('timestamp') raised: {e}")
            if n_mon >= 15 and n_info >= 5:
                break
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
