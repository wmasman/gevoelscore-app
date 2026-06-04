# Probe MULTIPLE routes with the GS_SESSION from .env.local to isolate
# whether the session is broken vs route-specific.

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
$headers = @{
  'Cookie' = "gs_session=$session"
  'Origin' = $base
}

function ProbeRoute($method, $path, $body) {
  try {
    $req = @{
      Uri = ($base + $path)
      Method = $method
      Headers = $headers
      UseBasicParsing = $true
      MaximumRedirection = 0
      ErrorAction = 'Stop'
    }
    if ($body) {
      $req.Body = $body
      $req.ContentType = 'application/json'
    }
    $resp = Invoke-WebRequest @req
    $loc = $resp.Headers['Location']
    Write-Host "$method $path -> $($resp.StatusCode)$(if ($loc) { ' Location: ' + $loc })"
  } catch {
    $code = if ($_.Exception.Response) { $_.Exception.Response.StatusCode.value__ } else { 'no-status' }
    $loc = ''
    if ($_.Exception.Response) {
      try { $loc = $_.Exception.Response.Headers['Location'] } catch {}
    }
    Write-Host "$method $path -> $code$(if ($loc) { ' Location: ' + $loc })"
  }
}

ProbeRoute 'GET' '/' $null
ProbeRoute 'GET' '/settings' $null
ProbeRoute 'POST' '/api/calendars/sync' '{}'
