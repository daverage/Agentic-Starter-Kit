# install.ps1 — installs global configs and optionally project files (Windows)
# Usage:
#   .\install.ps1
#   .\install.ps1 -ProjectPath C:\path\to\repo
param([string]$ProjectPath = "")
$ScriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path

function Cp-File($src, $dest) {
  if (-not (Test-Path $src)) { return }
  $dir = Split-Path -Parent $dest
  if (-not (Test-Path $dir)) { New-Item -ItemType Directory $dir -Force | Out-Null }
  if (Test-Path $dest) {
    $yn = Read-Host "  $dest exists — overwrite? [y/N]"
    if ($yn -notmatch "^[Yy]$") { Write-Host "  Skipped."; return }
  }
  Copy-Item $src $dest -Force; Write-Host "  OK: $dest"
}
function Cp-Dir($src, $dest) {
  if (-not (Test-Path $src)) { return }
  if (Test-Path $dest) {
    $yn = Read-Host "  $dest exists — overwrite? [y/N]"
    if ($yn -notmatch "^[Yy]$") { Write-Host "  Skipped."; return }
  }
  Copy-Item $src $dest -Recurse -Force; Write-Host "  OK: $dest\"
}

Write-Host "`n-- Claude Code global (~\.claude\) --"
Cp-File "$ScriptDir\global\.claude\settings.json" "$HOME\.claude\settings.json"
Cp-File "$ScriptDir\global\.claude\CLAUDE.md"     "$HOME\.claude\CLAUDE.md"

Write-Host "`n-- Codex CLI global (~\.codex\) --"
Cp-File "$ScriptDir\global\.codex\config.toml" "$HOME\.codex\config.toml"
Cp-File "$ScriptDir\global\.codex\AGENTS.md"   "$HOME\.codex\AGENTS.md"

Write-Host "`n-- Gemini CLI global (~\.gemini\) --"
Cp-File "$ScriptDir\global\.gemini\settings.json" "$HOME\.gemini\settings.json"
Cp-File "$ScriptDir\global\.gemini\GEMINI.md"     "$HOME\.gemini\GEMINI.md"
Cp-Dir  "$ScriptDir\global\.gemini\commands"      "$HOME\.gemini\commands"

if ($ProjectPath -ne "") {
  if (-not (Test-Path $ProjectPath)) { Write-Error "Not found: $ProjectPath"; exit 1 }
  Write-Host "`n-- Project files ($ProjectPath) --"
  Cp-Dir "$ScriptDir\project\.claude"  "$ProjectPath\.claude"
  Cp-Dir "$ScriptDir\project\.codex"   "$ProjectPath\.codex"
  Cp-Dir "$ScriptDir\project\.gemini"  "$ProjectPath\.gemini"
  # Activate Windows hook paths
  $ws = "$ProjectPath\.claude\settings.windows.json"
  if (Test-Path $ws) {
    Copy-Item $ws "$ProjectPath\.claude\settings.json" -Force
    Write-Host "  OK: Windows hook paths activated."
  }
}
Write-Host "`nDone. See README.md for next steps."
