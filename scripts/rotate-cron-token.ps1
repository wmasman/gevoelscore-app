# Rotate the cron Directus token AND set it as the Fly secret in one
# shot. Never echoes the token value to the terminal.
#
# - Runs directus/scripts/setup-cron-service-token.mjs (which rotates
#   the user's static token; previous is invalidated by Directus on
#   overwrite).
# - Captures stdout, extracts the new token from the script's marker
#   lines, pipes it directly to `fly secrets set --from-file -`.
# - Clears all variables before exit.
#
# Use when:
#   - First-time setup (no CALENDAR_CRON_DIRECTUS_TOKEN on Fly yet)
#   - After accidental leak (transcript, copy/paste mistake)
#   - Periodic rotation (every 90 days per the security checklist)

$ErrorActionPreference = 'Stop'

# Source DIRECTUS_TOKEN (admin) + DATABASE_URL from .env.local without
# echoing them.
$envFile = Join-Path $PSScriptRoot '..' | Resolve-Path | ForEach-Object { Join-Path $_ '.env.local' }
if (-not (Test-Path $envFile)) {
  Write-Host 'ERROR: .env.local not found.'
  exit 2
}
foreach ($line in Get-Content $envFile) {
  if ($line -match '^\s*([A-Z_][A-Z0-9_]*)=(.+?)\s*$') {
    $name = $Matches[1]
    $value = $Matches[2].Trim("'").Trim('"')
    if ($name -in @('DIRECTUS_TOKEN', 'DIRECTUS_URL', 'DATABASE_URL')) {
      Set-Item -Path "env:$name" -Value $value
    }
  }
}
if (-not $env:DIRECTUS_TOKEN) {
  Write-Host 'ERROR: DIRECTUS_TOKEN missing in .env.local.'
  exit 2
}

Push-Location (Resolve-Path (Join-Path $PSScriptRoot '..'))
try {
  # Run the Directus setup script; capture its full output.
  $output = & node directus/scripts/setup-cron-service-token.mjs 2>&1 | Out-String
  if ($LASTEXITCODE -ne 0) {
    Write-Host 'ERROR: setup-cron-service-token.mjs failed.'
    Write-Host '--- last 30 lines of output (token line redacted) ---'
    $sanitized = $output -split "`n" | ForEach-Object {
      if ($_ -match '^[A-Za-z0-9_-]{40,}$') { '<REDACTED TOKEN>' } else { $_ }
    }
    $sanitized | Select-Object -Last 30
    exit 3
  }

  # Extract the token: the script prints it on its own line between two
  # `=======` separators. Find the single line that's 40+ base64url chars.
  $token = $null
  foreach ($line in ($output -split "`r?`n")) {
    $trimmed = $line.Trim()
    if ($trimmed -match '^[A-Za-z0-9_-]{40,}$') {
      $token = $trimmed
      break
    }
  }
  if (-not $token) {
    Write-Host 'ERROR: could not extract token from script output.'
    exit 4
  }

  # Pipe directly to `fly secrets import` via stdin. The value never appears
  # in process arg lists (ps shows the command), never in shell history,
  # never echoed. --stage so deploy is explicit + batchable with other
  # secrets/changes.
  "CALENDAR_CRON_DIRECTUS_TOKEN=$token" | & fly secrets import -a gevoelscore-frontend --stage
  if ($LASTEXITCODE -ne 0) {
    Write-Host 'ERROR: fly secrets import failed.'
    exit 5
  }

  Write-Host ''
  Write-Host 'OK: CALENDAR_CRON_DIRECTUS_TOKEN staged on Fly.'
  Write-Host '    Token NOT echoed. Old token invalidated server-side.'
  Write-Host ''
  Write-Host 'Next:'
  Write-Host '  fly deploy -a gevoelscore-frontend   # picks up the new secret'
} finally {
  Pop-Location
  # Clear any captured value.
  if ($token) {
    Remove-Variable token -ErrorAction SilentlyContinue
  }
  Remove-Variable output -ErrorAction SilentlyContinue
}
