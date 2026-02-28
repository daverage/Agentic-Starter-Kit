#!/usr/bin/env bash
# install.sh — installs global configs to ~/.claude  ~/.codex  ~/.gemini
# Usage:
#   ./install.sh                        # global only
#   ./install.sh /path/to/your/project  # also copy project files into repo

set -e
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
G='\033[0;32m'; Y='\033[1;33m'; R='\033[0m'
ok()   { echo -e "${G}  ✓ $*${R}"; }
warn() { echo -e "${Y}  ⚠ $*${R}"; }

cp_file() {
  local src="$1" dest="$2"
  mkdir -p "$(dirname "$dest")"
  if [ -f "$dest" ]; then
    read -r -p "  $dest exists — overwrite? [y/N] " yn
    [[ "$yn" =~ ^[Yy]$ ]] || { warn "Skipped $dest"; return; }
  fi
  cp "$src" "$dest" && ok "$dest"
}
cp_dir() {
  local src="$1" dest="$2"
  mkdir -p "$(dirname "$dest")"
  if [ -d "$dest" ]; then
    read -r -p "  $dest/ exists — overwrite? [y/N] " yn
    [[ "$yn" =~ ^[Yy]$ ]] || { warn "Skipped $dest/"; return; }
  fi
  cp -r "$src" "$dest" && ok "$dest/"
}

echo ""
echo "── Claude Code global  (~/.claude/) ──────────────────────"
[ -d "$SCRIPT_DIR/global/.claude" ] && {
  cp_file "$SCRIPT_DIR/global/.claude/settings.json" "$HOME/.claude/settings.json"
  cp_file "$SCRIPT_DIR/global/.claude/CLAUDE.md"     "$HOME/.claude/CLAUDE.md"
}

echo ""
echo "── Codex CLI global  (~/.codex/) ─────────────────────────"
[ -d "$SCRIPT_DIR/global/.codex" ] && {
  cp_file "$SCRIPT_DIR/global/.codex/config.toml" "$HOME/.codex/config.toml"
  cp_file "$SCRIPT_DIR/global/.codex/AGENTS.md"   "$HOME/.codex/AGENTS.md"
}

echo ""
echo "── Gemini CLI global  (~/.gemini/) ───────────────────────"
[ -d "$SCRIPT_DIR/global/.gemini" ] && {
  cp_file "$SCRIPT_DIR/global/.gemini/settings.json" "$HOME/.gemini/settings.json"
  cp_file "$SCRIPT_DIR/global/.gemini/GEMINI.md"     "$HOME/.gemini/GEMINI.md"
  cp_dir  "$SCRIPT_DIR/global/.gemini/commands"      "$HOME/.gemini/commands"
}

PROJECT_DIR="${1:-}"
if [ -n "$PROJECT_DIR" ]; then
  [ -d "$PROJECT_DIR" ] || { echo "Project dir not found: $PROJECT_DIR"; exit 1; }
  echo ""
  echo "── Project files  ($PROJECT_DIR) ───────────────────────"
  [ -d "$SCRIPT_DIR/project/.claude"  ] && cp_dir "$SCRIPT_DIR/project/.claude"  "$PROJECT_DIR/.claude"
  [ -d "$SCRIPT_DIR/project/.codex"   ] && cp_dir "$SCRIPT_DIR/project/.codex"   "$PROJECT_DIR/.codex"
  [ -d "$SCRIPT_DIR/project/.gemini"  ] && cp_dir "$SCRIPT_DIR/project/.gemini"  "$PROJECT_DIR/.gemini"
  chmod +x "$PROJECT_DIR/.claude/hooks/"*.sh 2>/dev/null && ok "hooks executable"
fi

echo ""
echo "Done. See README.md for next steps."
