# Wrapper for scripts/auth-smoke.mjs that sources WILLEM_EMAIL and
# WILLEM_PASSWORD from the project's .env.local (gitignored). Never
# echoes the password to the terminal.
#
# Usage:
#   powershell -ExecutionPolicy Bypass -File scripts/run-auth-smoke.ps1

$ErrorActionPreference = 'Stop'

$envFile = Join-Path $PSScriptRoot '..' | Resolve-Path | ForEach-Object { Join-Path $_ '.env.local' }
if (-not (Test-Path $envFile)) {
  Write-Host "ERROR: $envFile not found."
  Write-Host 'Add WILLEM_EMAIL=... and WILLEM_PASSWORD=... to .env.local first.'
  exit 2
}

foreach ($line in Get-Content $envFile) {
  if ($line -match '^\s*([A-Z_][A-Z0-9_]*)=(.+?)\s*$') {
    $name = $Matches[1]
    $value = $Matches[2].Trim("'").Trim('"')
    if ($name -in @('WILLEM_EMAIL', 'WILLEM_PASSWORD', 'BASE_URL')) {
      Set-Item -Path "env:$name" -Value $value
    }
  }
}

if (-not $env:WILLEM_EMAIL -or -not $env:WILLEM_PASSWORD) {
  Write-Host 'ERROR: WILLEM_EMAIL and WILLEM_PASSWORD not found in .env.local.'
  Write-Host 'Add the lines:'
  Write-Host '  WILLEM_EMAIL=user@example.com'
  Write-Host '  WILLEM_PASSWORD=<your-password>'
  exit 2
}

Push-Location (Resolve-Path (Join-Path $PSScriptRoot '..'))
try {
  node scripts/auth-smoke.mjs
  exit $LASTEXITCODE
} finally {
  Pop-Location
}
