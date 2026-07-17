# Social Wave — one-command Premiere Pro MCP bridge install (Windows, run in PowerShell)
param([string]$Version = "1.1.1")   # pinned known-good; bump deliberately after testing
$ErrorActionPreference = "Stop"
Write-Host "== Premiere MCP bridge install (v$Version) =="

if (-not (Get-Command npm -ErrorAction SilentlyContinue)) { throw "npm not found - install Node.js first (winget install OpenJS.NodeJS.LTS)" }
npm install -g "premiere-pro-mcp@$Version"

$root = Join-Path (npm root -g) "premiere-pro-mcp"
$cepDir = Join-Path $env:APPDATA "Adobe\CEP\extensions\MCPBridgeCEP"
Write-Host "-- installing CEP panel -> $cepDir --"
if (Test-Path $cepDir) { Remove-Item -Recurse -Force $cepDir }
New-Item -ItemType Directory -Force (Split-Path $cepDir) | Out-Null
Copy-Item -Recurse (Join-Path $root "cep-plugin") $cepDir

Write-Host "-- enabling CEP PlayerDebugMode --"
foreach ($v in 11,12) {
  $key = "HKCU:\Software\Adobe\CSXS.$v"
  if (-not (Test-Path $key)) { New-Item -Path $key -Force | Out-Null }
  Set-ItemProperty -Path $key -Name PlayerDebugMode -Value "1" -Type String
}

Write-Host "-- registering with Claude Code --"
claude mcp add premiere-pro --scope user --env "PREMIERE_TEMP_DIR=$env:TEMP\premiere-mcp-bridge" -- premiere-pro-mcp

Write-Host ""
Write-Host "DONE. Restart Premiere Pro, open Window > Extensions > MCP Bridge,"
Write-Host "then verify in Claude Code with the premiere-pro 'ping' tool."
