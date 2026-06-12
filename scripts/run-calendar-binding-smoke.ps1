# PowerShell wrapper for the calendar-binding production smoke. Sources
# GS_SESSION from .env.local (which you add manually for this test —
# the value is the gs_session cookie value from your logged-in browser).
#
# Usage:
#   powershell -ExecutionPolicy Bypass -File scripts/run-calendar-binding-smoke.ps1
#
# The smoke pauses for manual OAuth in your browser; follow its prompts.

param(
  [string]$Base = 'https://gevoelscore-frontend.fly.dev'
)

$ErrorActionPreference = 'Stop'

$envFile = Join-Path $PSScriptRoot '..' | Resolve-Path | ForEach-Object { Join-Path $_ '.env.local' }
if (-not (Test-Path $envFile)) {
  Write-Host "ERROR: $envFile not found."
  exit 2
}

foreach ($line in Get-Content $envFile) {
  if ($line -match '^\s*GS_SESSION=(.+?)\s*$') {
    $env:GS_SESSION = $Matches[1].Trim("'").Trim('"')
  }
}

if (-not $env:GS_SESSION) {
  Write-Host 'ERROR: GS_SESSION not found in .env.local.'
  Write-Host 'Add this line to .env.local first:'
  Write-Host '  GS_SESSION=<paste-the-gs_session-cookie-value-from-your-logged-in-browser>'
  Write-Host ''
  Write-Host 'How to get the cookie value:'
  Write-Host '  1. Open https://gevoelscore-frontend.fly.dev in your browser'
  Write-Host '  2. Log in if not already'
  Write-Host '  3. DevTools (F12) -> Application -> Cookies -> gevoelscore-frontend.fly.dev'
  Write-Host '  4. Find the gs_session row, copy the Value column'
  exit 2
}

$env:CALENDAR_TEST_BASE = $Base

Push-Location (Resolve-Path (Join-Path $PSScriptRoot '..'))
try {
  node scripts/calendar-binding-smoke.mjs
  exit $LASTEXITCODE
} finally {
  Pop-Location
  Remove-Item env:GS_SESSION -ErrorAction SilentlyContinue
  Remove-Item env:CALENDAR_TEST_BASE -ErrorAction SilentlyContinue
}
