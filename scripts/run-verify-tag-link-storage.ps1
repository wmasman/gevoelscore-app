# Wrapper for scripts/verify-tag-link-storage.mjs.
# Sources WILLEM_EMAIL, WILLEM_PASSWORD, DIRECTUS_TOKEN from .env.local
# (gitignored). Never echoes credentials to the terminal.
#
# Usage:
#   powershell -ExecutionPolicy Bypass -File scripts/run-verify-tag-link-storage.ps1

$ErrorActionPreference = 'Stop'

$envFile = Join-Path $PSScriptRoot '..' | Resolve-Path | ForEach-Object { Join-Path $_ '.env.local' }
if (-not (Test-Path $envFile)) {
  Write-Host "ERROR: $envFile not found."
  Write-Host 'Add WILLEM_EMAIL, WILLEM_PASSWORD, and DIRECTUS_TOKEN to .env.local first.'
  exit 2
}

foreach ($line in Get-Content $envFile) {
  if ($line -match '^\s*([A-Z_][A-Z0-9_]*)=(.+?)\s*$') {
    $name = $Matches[1]
    $value = $Matches[2].Trim("'").Trim('"')
    if ($name -in @('WILLEM_EMAIL', 'WILLEM_PASSWORD', 'BASE_URL', 'DIRECTUS_TOKEN', 'DIRECTUS_URL')) {
      Set-Item -Path "env:$name" -Value $value
    }
  }
}

if (-not $env:WILLEM_EMAIL -or -not $env:WILLEM_PASSWORD) {
  Write-Host 'ERROR: WILLEM_EMAIL and WILLEM_PASSWORD not found in .env.local.'
  exit 2
}

if (-not $env:DIRECTUS_TOKEN) {
  Write-Host 'ERROR: DIRECTUS_TOKEN not found in .env.local (needed for direct Directus reads + cleanup).'
  exit 2
}

Push-Location (Resolve-Path (Join-Path $PSScriptRoot '..'))
try {
  node scripts/verify-tag-link-storage.mjs
  exit $LASTEXITCODE
} finally {
  Pop-Location
}
