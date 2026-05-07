# OGRS — Windows-side port-forward + firewall setup for the WSL2 server.
#
# WSL2 has its own internal IP that changes on every reboot. For phones,
# friends, or remote machines to reach the OGRS game server, Windows
# has to forward its outward-facing ports to the current WSL2 IP, and
# the firewall has to allow inbound traffic on those ports.
#
# Run once (or whenever the WSL IP changes) from an elevated PowerShell:
#     powershell.exe -ExecutionPolicy Bypass -File setup-windows-portforward.ps1

param(
    [string]$WslIp = $null
)

if (-not $WslIp) {
    $WslIp = (wsl.exe -d Ubuntu-24.04 -- hostname -I).Trim().Split(' ')[0]
    Write-Host "Auto-detected WSL IP: $WslIp"
}

$ports = @(43594, 43494)  # game tcp, websocket

Write-Host "Resetting any existing OGRS port-proxies..."
foreach ($port in $ports) {
    netsh interface portproxy delete v4tov4 listenport=$port listenaddress=0.0.0.0 2>$null | Out-Null
}

Write-Host "Adding port-proxies (Windows -> WSL)..."
foreach ($port in $ports) {
    netsh interface portproxy add v4tov4 listenport=$port listenaddress=0.0.0.0 connectport=$port connectaddress=$WslIp
    Write-Host "  $port -> $WslIp`:$port"
}

Write-Host "Ensuring firewall rules exist..."
$rules = @{
    "OGRS Game (43594)"      = 43594
    "OGRS WebSocket (43494)" = 43494
}
foreach ($name in $rules.Keys) {
    if (-not (Get-NetFirewallRule -DisplayName $name -ErrorAction SilentlyContinue)) {
        New-NetFirewallRule -DisplayName $name -Direction Inbound -LocalPort $rules[$name] -Protocol TCP -Action Allow | Out-Null
        Write-Host "  Created: $name"
    } else {
        Write-Host "  Exists:  $name"
    }
}

Write-Host ""
Write-Host "Current portproxy state:"
netsh interface portproxy show all
