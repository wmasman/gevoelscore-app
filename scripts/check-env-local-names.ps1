# Lists which expected env var names are present in .env.local (names only,
# values never echoed). Used by sanity checks before /build-step runs.

param(
  [string]$EnvFile = '.env.local'
)

$expected = @(
  'CALENDAR_KEK',
  'DATABASE_URL',
  'DIRECTUS_TOKEN',
  'GOOGLE_CLIENT_ID',
  'GOOGLE_CLIENT_SECRET',
  'WILLEM_EMAIL',
  'WILLEM_PASSWORD',
  'WILLEM_USER_ID'
)

if (-not (Test-Path $EnvFile)) {
  Write-Host "ERROR: $EnvFile not found."
  exit 2
}

$present = @()
foreach ($line in Get-Content $EnvFile) {
  foreach ($name in $expected) {
    if ($line -match "^\s*$name=") {
      $present += $name
    }
  }
}

Write-Host "Expected env vars in $EnvFile (names only):"
foreach ($name in $expected) {
  if ($present -contains $name) {
    Write-Host "  [+] $name"
  } else {
    Write-Host "  [-] $name (missing)"
  }
}
