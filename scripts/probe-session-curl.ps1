# Probe with curl.exe instead of Invoke-WebRequest — strips out any
# PowerShell-specific cookie/header handling.

$ErrorActionPreference = 'Stop'

$envFile = Join-Path $PSScriptRoot '..' | Resolve-Path | ForEach-Object { Join-Path $_ '.env.local' }
$session = ''
foreach ($line in Get-Content $envFile) {
  if ($line -match '^\s*GS_SESSION=(.+?)\s*$') {
    $session = $Matches[1].Trim("'").Trim('"')
  }
}
if (-not $session) {
  Write-Host 'NO_GS_SESSION'
  exit 1
}

$base = 'https://gevoelscore-frontend.fly.dev'

# /api/health (public, no auth — sanity check curl works)
Write-Host '--- /api/health (sanity) ---'
& curl.exe -s -o NUL -w "status: %{http_code}`n" "$base/api/health"

# /settings with cookie (browser equivalent of being logged in)
Write-Host '--- /settings (with gs_session cookie) ---'
& curl.exe -s -o NUL -w "status: %{http_code}`nlocation: %{redirect_url}`n" `
  --cookie "gs_session=$session" `
  "$base/settings"

# /api/calendars/sync POST (what the backfill uses)
Write-Host '--- POST /api/calendars/sync ---'
& curl.exe -s -o response.tmp -w "status: %{http_code}`n" `
  -X POST `
  -H "Origin: $base" `
  -H "Content-Type: application/json" `
  --cookie "gs_session=$session" `
  --data '{}' `
  "$base/api/calendars/sync"
if (Test-Path response.tmp) {
  Write-Host "body (first 200 chars): $(Get-Content response.tmp -Raw | Select-Object -First 1 | ForEach-Object { $_.Substring(0, [Math]::Min(200, $_.Length)) })"
  Remove-Item response.tmp -Force
}
