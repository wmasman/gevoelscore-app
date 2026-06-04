# Probe whether the GS_SESSION in .env.local still authenticates against
# the production /api/calendars/sync endpoint. Read-only: just calls the
# route once with an empty body and reports the status code.
#
# Usage: powershell -ExecutionPolicy Bypass -File scripts/probe-session.ps1

$ErrorActionPreference = 'Stop'

$envFile = Join-Path $PSScriptRoot '..' | Resolve-Path | ForEach-Object { Join-Path $_ '.env.local' }
$session = ''
foreach ($line in Get-Content $envFile) {
  if ($line -match '^\s*GS_SESSION=(.+?)\s*$') {
    $session = $Matches[1].Trim("'").Trim('"')
  }
}
if (-not $session) {
  Write-Host 'NO_GS_SESSION_IN_ENV_LOCAL'
  exit 1
}

$base = 'https://gevoelscore-frontend.fly.dev'
$headers = @{
  'Cookie' = "gs_session=$session"
  'Origin' = $base
}

try {
  $resp = Invoke-WebRequest -Uri "$base/api/calendars/sync" -Method POST -Headers $headers -Body '{}' -ContentType 'application/json' -UseBasicParsing -ErrorAction Stop
  Write-Host "STATUS $($resp.StatusCode)"
  Write-Host ("BODY " + ($resp.Content.Substring(0, [Math]::Min(300, $resp.Content.Length))))
} catch {
  $code = if ($_.Exception.Response) { $_.Exception.Response.StatusCode.value__ } else { 'no-status' }
  $body = ''
  if ($_.Exception.Response) {
    try {
      $stream = $_.Exception.Response.GetResponseStream()
      $reader = New-Object IO.StreamReader($stream)
      $body = $reader.ReadToEnd()
    } catch {}
  }
  Write-Host "FAIL_STATUS $code"
  if ($body) { Write-Host "FAIL_BODY $($body.Substring(0, [Math]::Min(300, $body.Length)))" }
}
