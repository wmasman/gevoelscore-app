# Generate anonymized sample CSV from the author's private dataset.
# Takes the last 60 rows of date + score only, drops all notes/tags.
# Personal data file is expected at a fixed path outside any repo.

$src = 'C:\Users\Gebruiker\Documents\gevoelscore-data\gevoelscore_verrijkt.csv'
$dst = Join-Path $PSScriptRoot '..\docs\sample-data.csv'

if (-not (Test-Path $src)) {
  Write-Error "Source not found: $src"
  exit 1
}

$rows = Import-Csv $src |
  Select-Object -Last 60 |
  ForEach-Object { [PSCustomObject]@{ date = $_.date; score = $_.score } }

$rows | Export-Csv -Path $dst -NoTypeInformation -Encoding utf8

Write-Host "Wrote $($rows.Count) rows to $dst"
