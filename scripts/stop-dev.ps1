# Tắt uvicorn dev server theo port (mặc định 8888)
param(
    [int[]]$Ports = @(8888, 8000)
)

$ErrorActionPreference = "SilentlyContinue"
$killed = @()

foreach ($port in $Ports) {
    $lines = netstat -ano | Select-String ":$port\s" | Select-String "LISTENING"
    foreach ($line in $lines) {
        $parts = ($line -replace '\s+', ' ').ToString().Trim().Split(' ')
        $pid = [int]$parts[-1]
        if ($pid -gt 0 -and $killed -notcontains $pid) {
            Write-Host "Dang tat PID $pid (port $port)..."
            taskkill /PID $pid /F /T | Out-Null
            $killed += $pid
        }
    }
}

if ($killed.Count -eq 0) {
    Write-Host "Khong co process LISTENING tren port $($Ports -join ', ')."
} else {
    Write-Host "Da tat: PID $($killed -join ', ')"
}

Start-Sleep -Seconds 1
Write-Host "`nKiem tra con port:"
foreach ($port in $Ports) {
    $left = netstat -ano | Select-String ":$port\s" | Select-String "LISTENING"
    if ($left) { Write-Host "  Port $port van con LISTENING" -ForegroundColor Yellow }
    else { Write-Host "  Port $port da trong" -ForegroundColor Green }
}
