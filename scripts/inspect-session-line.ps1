# Show shape (NOT value) of GS_SESSION line in .env.local. Helps spot
# common mistakes: stray quotes, leading whitespace, line wrapped.
# NEVER prints the actual cookie value.

$envFile = Join-Path $PSScriptRoot '..' | Resolve-Path | ForEach-Object { Join-Path $_ '.env.local' }
$matches = Get-Content $envFile | Where-Object { $_ -match '^GS_SESSION=' }
Write-Host "number of GS_SESSION lines: $($matches.Count)"
$line = $matches | Select-Object -First 1
if (-not $line) {
  Write-Host 'NO GS_SESSION line found'
  exit 1
}
$val = ($line -split '=', 2)[1]
Write-Host "raw line length: $($line.Length)"
Write-Host "value length: $($val.Length)"
Write-Host "starts with quote: $($val.StartsWith('"') -or $val.StartsWith("'"))"
Write-Host "ends with quote: $($val.EndsWith('"') -or $val.EndsWith("'"))"
Write-Host "contains spaces: $($val -match '\s')"
Write-Host "first 6 chars: $($val.Substring(0, [Math]::Min(6, $val.Length)))"
Write-Host "last 6 chars: $($val.Substring([Math]::Max(0, $val.Length - 6)))"
# Position of dashes — UUID format expects 8-4-4-4-12 = dashes at 8, 13, 18, 23
$dashPositions = @()
for ($i = 0; $i -lt $val.Length; $i++) {
  if ($val[$i] -eq '-') { $dashPositions += $i }
}
Write-Host "dash positions: $($dashPositions -join ',')"
# Char codes for any non-hex, non-dash chars
$bad = @()
for ($i = 0; $i -lt $val.Length; $i++) {
  $c = $val[$i]
  if (-not (($c -ge '0' -and $c -le '9') -or ($c -ge 'a' -and $c -le 'f') -or ($c -ge 'A' -and $c -le 'F') -or $c -eq '-')) {
    $bad += "pos $i char-code $([int][char]$c)"
  }
}
if ($bad.Count -gt 0) {
  Write-Host "NON-HEX/DASH chars found: $($bad -join '; ')"
} else {
  Write-Host "all chars are hex or dash (UUID-shaped)"
}
