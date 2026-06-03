# One-shot helper: fetches DB_CONNECTION_STRING from the Fly Directus app
# via `fly ssh console -C printenv` and appends it as DATABASE_URL to
# .env.local. Never echoes the value.
#
# Usage:
#   powershell -ExecutionPolicy Bypass -File scripts/fetch-database-url.ps1

$ErrorActionPreference = 'Stop'

$envFile = Join-Path $PSScriptRoot '..' | Resolve-Path | ForEach-Object { Join-Path $_ '.env.local' }

# Skip if already present
if (Test-Path $envFile) {
  if (Get-Content $envFile | Select-String -Pattern '^DATABASE_URL=' -Quiet) {
    Write-Host "DATABASE_URL already present in .env.local. Skipping."
    exit 0
  }
}

Write-Host "Fetching DB_CONNECTION_STRING from gevoelscore-backend via fly ssh..."

# fly ssh writes progress lines to stderr; lower the error preference around
# the call so that doesn't abort the script, then collect stdout + stderr
# together so we can extract the postgres:// line.
$prevPref = $ErrorActionPreference
$ErrorActionPreference = 'Continue'
$raw = & fly ssh console -a gevoelscore-backend -C 'printenv DB_CONNECTION_STRING' 2>&1 | Out-String
$ErrorActionPreference = $prevPref

# Find the postgres:// line anywhere in the captured text
$value = ($raw -split "`r?`n") | Where-Object { $_ -match '^postgres' } | Select-Object -First 1
if (-not $value) {
  Write-Host "ERROR: no postgres:// line in output."
  Write-Host "First 200 chars of raw output:"
  Write-Host $raw.Substring(0, [Math]::Min(200, $raw.Length))
  exit 2
}

$value = $value.Trim()
Add-Content -Path $envFile -Value "DATABASE_URL=$value"
Write-Host ("DATABASE_URL appended to .env.local (length: " + $value.Length + ")")
