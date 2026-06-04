# Rotate CALENDAR_SYNC_SECRET — the bearer secret the daily cron GHA
# workflow sends to /api/calendars/sync. Generates a fresh 32-byte
# base64 random value and ships it to BOTH stores in one shot:
#
#   - Fly secret (staged; deploy picks it up): the route reads
#     process.env.CALENDAR_SYNC_SECRET and constant-time-compares
#     against the Authorization: Bearer header.
#   - GitHub Actions secret: daily-calendar-sync.yml interpolates
#     ${{ secrets.CALENDAR_SYNC_SECRET }} into the curl Authorization
#     header.
#
# The two MUST match — that's why this script writes both from one
# generated value rather than rotating them independently.
#
# The secret value is never echoed to stdout, never written to disk,
# never placed in process argv. It exists only in memory and on stdin
# pipes to `fly secrets import` and `gh secret set`.
#
# Use when:
#   - First-time setup (step-2.0b)
#   - After accidental leak (transcript, workflow log dump)
#   - Periodic rotation (per the security checklist)

$ErrorActionPreference = 'Stop'

# Generate 32 random bytes -> base64. ~44 chars; constant-time-safe
# bytes-equal in the route handler.
$bytes = New-Object byte[] 32
[System.Security.Cryptography.RandomNumberGenerator]::Create().GetBytes($bytes)
$secret = [Convert]::ToBase64String($bytes)

try {
  # Stage on Fly via stdin import. --stage keeps deploy explicit so
  # we don't restart the machine until step-2's code is in place.
  "CALENDAR_SYNC_SECRET=$secret" | & fly secrets import -a gevoelscore-frontend --stage
  if ($LASTEXITCODE -ne 0) {
    Write-Host 'ERROR: fly secrets import failed.'
    exit 3
  }

  # Set on GHA via stdin (gh secret set reads value from stdin when
  # --body is omitted).
  $secret | & gh secret set CALENDAR_SYNC_SECRET
  if ($LASTEXITCODE -ne 0) {
    Write-Host 'ERROR: gh secret set failed.'
    Write-Host 'NOTE: Fly secret IS already staged; values now mismatched.'
    Write-Host '      Re-run this script to regenerate and resync both.'
    exit 4
  }

  Write-Host ''
  Write-Host 'OK: CALENDAR_SYNC_SECRET staged on Fly + set on GitHub Actions.'
  Write-Host '    Secret NOT echoed. Same value in both stores.'
  Write-Host ''
  Write-Host 'Next:'
  Write-Host '  fly deploy -a gevoelscore-frontend   # picks up the new secret'
  Write-Host '  (then the GHA workflow can successfully POST to /api/calendars/sync)'
} finally {
  # Best-effort clear of in-memory value. PowerShell zeroes the byte
  # array; the string is immutable so we just drop the reference.
  if ($bytes) {
    [Array]::Clear($bytes, 0, $bytes.Length)
    Remove-Variable bytes -ErrorAction SilentlyContinue
  }
  Remove-Variable secret -ErrorAction SilentlyContinue
}
