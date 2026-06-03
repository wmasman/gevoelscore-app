# Wrapper for tier3-constraint-smoke.mjs. Sources DIRECTUS_TOKEN from
# .env.local. Smoke runs against production Directus and asserts each
# CHECK constraint rejects its respective violation.
#
# Usage:
#   powershell -ExecutionPolicy Bypass -File scripts/run-tier3-constraint-smoke.ps1

$ErrorActionPreference = 'Stop'

$envFile = Join-Path $PSScriptRoot '..' | Resolve-Path | ForEach-Object { Join-Path $_ '.env.local' }
if (-not (Test-Path $envFile)) {
  Write-Host "ERROR: $envFile not found."
  exit 2
}

foreach ($line in Get-Content $envFile) {
  if ($line -match '^\s*([A-Z_][A-Z0-9_]*)=(.+?)\s*$') {
    $name = $Matches[1]
    $value = $Matches[2].Trim("'").Trim('"')
    if ($name -in @('DIRECTUS_TOKEN', 'DIRECTUS_URL')) {
      Set-Item -Path "env:$name" -Value $value
    }
  }
}

if (-not $env:DIRECTUS_TOKEN) {
  Write-Host 'ERROR: DIRECTUS_TOKEN not found in .env.local.'
  exit 2
}

Push-Location (Resolve-Path (Join-Path $PSScriptRoot '..'))
try {
  node scripts/tier3-constraint-smoke.mjs
  exit $LASTEXITCODE
} finally {
  Pop-Location
}
