# Alias của yarn start:dev (giữ cho ai quen gọi script)
$ErrorActionPreference = "Stop"
Set-Location $PSScriptRoot\..

if (-not (Test-Path ".\.venv\Scripts\python.exe")) {
    Write-Host "Chua co .venv. Chay: python -m venv .venv && pip install -r requirements.txt"
    exit 1
}

$envFile = Join-Path (Get-Location) ".env"
if (Test-Path $envFile) {
    Get-Content $envFile | ForEach-Object {
        if ($_ -match '^\s*([^#][^=]+)=(.*)$') {
            [System.Environment]::SetEnvironmentVariable($matches[1].Trim(), $matches[2].Trim(), "Process")
        }
    }
}

& .\.venv\Scripts\python.exe dev.py
