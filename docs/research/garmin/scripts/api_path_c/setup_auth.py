"""H04b Path C - One-time auth setup.

Reads GARMIN_EMAIL + GARMIN_PWD from .env.local at the project
root, authenticates to Garmin Connect via the garminconnect
library, and saves the OAuth tokens to a local directory.

After this runs successfully, smoke_test.py and the backfill
script load tokens from the same directory without needing
credentials.

The password is read silently and never printed/logged. If MFA
is enabled, the script prompts interactively for the 6-digit
code.

USAGE:
  python setup_auth.py
"""
from __future__ import annotations

import os
import sys
from pathlib import Path

# .env.local lives at the project root
PROJECT_ROOT = Path(__file__).resolve().parents[5]
ENV_FILE = PROJECT_ROOT / ".env.local"

# Token cache directory (outside the repo, in user home)
TOKEN_DIR = Path.home() / ".garminconnect_tokens"

try:
    from dotenv import dotenv_values
except ImportError:
    print("ERROR: python-dotenv not installed.", file=sys.stderr)
    print("Run: pip install python-dotenv", file=sys.stderr)
    sys.exit(1)

try:
    from garminconnect import Garmin
except ImportError:
    print("ERROR: garminconnect not installed.", file=sys.stderr)
    print("Run: pip install garminconnect", file=sys.stderr)
    sys.exit(1)


def _redact_exception(exc: Exception, secret: str) -> str:
    msg = str(exc)
    if secret:
        msg = msg.replace(secret, "[REDACTED]")
    return msg


def main() -> int:
    if not ENV_FILE.exists():
        print(f"ERROR: {ENV_FILE} not found", file=sys.stderr)
        return 1

    env = dotenv_values(ENV_FILE)
    email = env.get("GARMIN_EMAIL")
    password = env.get("GARMIN_PWD")

    if not email or not password:
        print("ERROR: GARMIN_EMAIL or GARMIN_PWD missing in .env.local",
              file=sys.stderr)
        return 1

    TOKEN_DIR.mkdir(parents=True, exist_ok=True)
    print(f"Token directory: {TOKEN_DIR}")
    print(f"Authenticating as {email}...")

    def prompt_mfa() -> str:
        return input("Enter the 6-digit MFA code from your authenticator: ").strip()

    try:
        client = Garmin(email, password, prompt_mfa=prompt_mfa)
        result = client.login(tokenstore=str(TOKEN_DIR))
    except Exception as e:
        print(f"\nAUTH FAILED: {_redact_exception(e, password)}", file=sys.stderr)
        return 1
    finally:
        # Best-effort password wipe from local scope
        if "password" in dir():
            password = "x" * len(password) if password else ""

    # result is a tuple; (None, None) on clean success
    needs_mfa, _ = result if isinstance(result, tuple) else (None, None)
    if needs_mfa:
        print(f"\nLogin returned needs_mfa={needs_mfa}; MFA flow may not have "
              f"completed. Inspect token dir.", file=sys.stderr)
        return 1

    # Verify tokens were written
    cached = list(TOKEN_DIR.glob("*"))
    if cached:
        print(f"\nSuccess. {len(cached)} token file(s) in {TOKEN_DIR}.")
        print("You can now run smoke_test.py without credentials.")
        print(f"\nSet this env var so other scripts find the token dir:")
        print(f'  $env:GARMINTOKENS = "{TOKEN_DIR}"')
        return 0
    else:
        print(f"\nWARNING: no token files in {TOKEN_DIR}. Login may have failed.",
              file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
