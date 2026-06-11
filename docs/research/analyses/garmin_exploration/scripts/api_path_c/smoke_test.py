"""H04b Path C - Smoke test.

Pulls one calendar day of Body Battery + HRV + Sleep from the
Garmin Connect REST API to verify:
  1. Authentication via cached token works
  2. Endpoints respond
  3. Field names + value shapes match what we expect
  4. Response is parseable

USAGE:
  python smoke_test.py YYYY-MM-DD

PREREQUISITE:
  setup_auth.py must have run successfully and saved tokens to
  ~/.garminconnect_tokens/.

The script reads tokens from that directory, hits three API
endpoints, prints field-name + value-shape summary, and dumps the
full responses to smoke_test_output/ for review.

Credentials are never read; only the cached token.
"""
from __future__ import annotations

import json
import sys
from datetime import date
from pathlib import Path

try:
    from garminconnect import Garmin
except ImportError:
    print("ERROR: garminconnect not installed.", file=sys.stderr)
    sys.exit(1)

TOKEN_DIR = Path.home() / ".garminconnect_tokens"


def _safe_for_json(o):
    if isinstance(o, (str, int, float, bool, type(None))):
        return o
    if isinstance(o, list):
        return [_safe_for_json(x) for x in o]
    if isinstance(o, dict):
        return {k: _safe_for_json(v) for k, v in o.items()}
    return str(o)


def _summarise(name: str, value) -> None:
    print(f"--- {name} ---")
    print(f"  raw type: {type(value).__name__}")
    if isinstance(value, list):
        print(f"  list length: {len(value)}")
        if value:
            first = value[0]
            print(f"  first element type: {type(first).__name__}")
            if isinstance(first, dict):
                print(f"  first element keys: {sorted(first.keys())}")
                for k, v in list(first.items())[:8]:
                    print(f"    {k}: {repr(v)[:100]}")
    elif isinstance(value, dict):
        print(f"  keys: {sorted(value.keys())}")
        for k, v in value.items():
            if isinstance(v, list):
                print(f"  field '{k}' is a list of len {len(v)}")
                if v:
                    print(f"    first item: {repr(v[0])[:200]}")
            elif isinstance(v, dict):
                print(f"  field '{k}' is a dict with keys: {sorted(v.keys())}")
                for k2, v2 in list(v.items())[:6]:
                    print(f"    {k}.{k2}: {repr(v2)[:100]}")
            else:
                print(f"  field '{k}': {repr(v)[:200]}")
    else:
        print(f"  raw: {repr(value)[:300]}")
    print()


def main() -> int:
    if len(sys.argv) != 2:
        print("Usage: python smoke_test.py YYYY-MM-DD", file=sys.stderr)
        return 1
    try:
        target = date.fromisoformat(sys.argv[1])
    except ValueError as e:
        print(f"ERROR: bad date format: {e}", file=sys.stderr)
        return 1
    if not TOKEN_DIR.exists():
        print(f"ERROR: no token dir at {TOKEN_DIR}. Run setup_auth.py first.",
              file=sys.stderr)
        return 1

    print(f"\n=== H04b Path C smoke test for {target.isoformat()} ===\n")
    print(f"Loading tokens from {TOKEN_DIR}...")
    client = Garmin()
    try:
        client.login(tokenstore=str(TOKEN_DIR))
    except Exception as e:
        print(f"LOGIN FAILED: {e}", file=sys.stderr)
        return 1
    print("  authenticated.\n")

    dump = {"date": target.isoformat()}

    # Body Battery
    print("--- 1. Body Battery ---")
    bb = None
    try:
        bb = client.get_body_battery(target.isoformat())
        _summarise("Body Battery (default)", bb)
        dump["body_battery"] = _safe_for_json(bb)
    except Exception as e:
        print(f"  get_body_battery failed: {e}\n")

    # Try other BB methods that may exist
    print("  Other BB-related methods on client:")
    for attr in sorted(dir(client)):
        if "batter" in attr.lower():
            print(f"    {attr}")
    print()

    # HRV
    print("--- 2. HRV ---")
    hrv = None
    print("  HRV-related methods on client:")
    hrv_methods = [m for m in sorted(dir(client)) if "hrv" in m.lower() and not m.startswith("_")]
    for m in hrv_methods:
        print(f"    {m}")
    print()
    for method_name in hrv_methods:
        method = getattr(client, method_name)
        try:
            r = method(target.isoformat())
            _summarise(f"HRV via {method_name}", r)
            dump[f"hrv_via_{method_name}"] = _safe_for_json(r)
            if hrv is None:
                hrv = r
        except TypeError:
            try:
                r = method()
                _summarise(f"HRV via {method_name}()", r)
                dump[f"hrv_via_{method_name}_noargs"] = _safe_for_json(r)
                if hrv is None:
                    hrv = r
            except Exception as e2:
                print(f"  {method_name}() failed: {e2}\n")
        except Exception as e:
            print(f"  {method_name}({target}) failed: {e}\n")

    # Sleep
    print("--- 3. Sleep ---")
    try:
        sleep = client.get_sleep_data(target.isoformat())
        _summarise("Sleep", sleep)
        dump["sleep"] = _safe_for_json(sleep)
    except Exception as e:
        print(f"  get_sleep_data failed: {e}\n")

    # Stress (per-minute) for cross-check with H02b's existing extraction
    print("--- 4. Stress (per-minute, cross-check) ---")
    try:
        stress = client.get_stress_data(target.isoformat())
        _summarise("Stress", stress)
        dump["stress"] = _safe_for_json(stress)
    except Exception as e:
        print(f"  get_stress_data failed: {e}\n")

    # Dump
    out_dir = Path(__file__).resolve().parent / "smoke_test_output"
    out_dir.mkdir(exist_ok=True)
    dump_path = out_dir / f"smoke_{target.isoformat()}.json"
    dump_path.write_text(json.dumps(dump, indent=2, default=str), encoding="utf-8")
    print(f"\n=== Full response dump: {dump_path} ===")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
