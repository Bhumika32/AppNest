Param(
    [string]$Action = 'upgrade'
)

Set-Location -Path $PSScriptRoot\..\
$env:PYTHONPATH = "$PWD"

if ($Action -eq 'upgrade') {
    python -m alembic upgrade head
} elseif ($Action -eq 'stamp') {
    python -m alembic stamp head
} else {
    Write-Host "Unknown action: $Action"
}
