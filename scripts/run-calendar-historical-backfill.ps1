# Wrapper for the historical calendar backfill. Sources GS_SESSION from
# .env.local and runs the backfill against prod (default range:
# 2022-09-01 .. today).
#
# Usage:
#   powershell -ExecutionPolicy Bypass -File scripts/run-calendar-historical-backfill.ps1
#
# Custom range:
#   powershell -ExecutionPolicy Bypass -File scripts/run-calendar-historical-backfill.ps1 -From 2024-01-01 -To 2024-12-31

param(
  [string]$Base = 'https://gevoelscore-frontend.fly.dev',
  [string]$From = '',
  [string]$To = ''
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
  exit 2
}

$env:CALENDAR_TEST_BASE = $Base
if ($From) { $env:CALENDAR_BACKFILL_FROM = $From }
if ($To) { $env:CALENDAR_BACKFILL_TO = $To }

Push-Location (Resolve-Path (Join-Path $PSScriptRoot '..'))
try {
  node scripts/calendar-historical-backfill.mjs
  exit $LASTEXITCODE
} finally {
  Pop-Location
  Remove-Item env:GS_SESSION -ErrorAction SilentlyContinue
  Remove-Item env:CALENDAR_TEST_BASE -ErrorAction SilentlyContinue
  Remove-Item env:CALENDAR_BACKFILL_FROM -ErrorAction SilentlyContinue
  Remove-Item env:CALENDAR_BACKFILL_TO -ErrorAction SilentlyContinue
}
