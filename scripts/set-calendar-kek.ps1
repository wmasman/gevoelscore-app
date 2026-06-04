# One-shot helper to generate a 32-byte base64 CALENDAR_KEK and set it
# as a Fly secret. The KEK value is NEVER written to disk, stdout, or
# chat — it lives in $kek briefly, gets piped to fly secrets, and the
# variable is cleared.
#
# Usage:
#   powershell -ExecutionPolicy Bypass -File scripts/set-calendar-kek.ps1
#
# Re-running this script ROTATES the KEK. Do NOT re-run unless you've
# already migrated existing ciphertexts (no-op in v1.6 — no rows exist
# yet at step-0 time).

param(
  [string]$App = 'gevoelscore-frontend'
)

$ErrorActionPreference = 'Stop'

Write-Host "Generating 32-byte base64 CALENDAR_KEK for $App..."
# PowerShell 5.1-compatible RNG. Newer .NET has a static GetBytes(int)
# overload; 5.1 needs the buffer-fill style.
$bytes = New-Object byte[] 32
$rng = [System.Security.Cryptography.RandomNumberGenerator]::Create()
try {
  $rng.GetBytes($bytes)
} finally {
  $rng.Dispose()
}
$kek = [Convert]::ToBase64String($bytes)
Remove-Variable bytes

try {
  fly secrets set "CALENDAR_KEK=$kek" -a $App
  Write-Host "CALENDAR_KEK set on $App."
} finally {
  Remove-Variable kek -ErrorAction SilentlyContinue
  Write-Host 'KEK variable cleared from session.'
}
