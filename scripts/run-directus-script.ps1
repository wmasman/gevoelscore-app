# Wrapper that sources DIRECTUS_TOKEN (and optionally DIRECTUS_URL) from
# the project's .env.local (gitignored) and runs a directus/scripts/*.mjs
# script. Never echoes the token to the terminal.
#
# Usage:
#   powershell -ExecutionPolicy Bypass -File scripts/run-directus-script.ps1 -Script directus/scripts/add-episodes.mjs

param(
  [Parameter(Mandatory = $true)]
  [string]$Script
)

$ErrorActionPreference = 'Stop'

$envFile = Join-Path $PSScriptRoot '..' | Resolve-Path | ForEach-Object { Join-Path $_ '.env.local' }
if (-not (Test-Path $envFile)) {
  Write-Host "ERROR: $envFile not found."
  Write-Host 'Add DIRECTUS_TOKEN=... (admin static token) to .env.local first.'
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
  Write-Host 'Add the line:'
  Write-Host '  DIRECTUS_TOKEN=<admin static token from Directus admin UI>'
  exit 2
}

$target = if ($env:DIRECTUS_URL) { $env:DIRECTUS_URL } else { 'https://gevoelscore-backend.fly.dev (default)' }
Write-Host "Target: $target"

Push-Location (Resolve-Path (Join-Path $PSScriptRoot '..'))
try {
  node $Script
  exit $LASTEXITCODE
} finally {
  Pop-Location
}
