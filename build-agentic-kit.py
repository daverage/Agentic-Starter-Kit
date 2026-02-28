#!/usr/bin/env python3
"""
build-agentic-kit.py
Builds the Agentic Coding Tools starter kit in the current directory.
Works on Mac, Linux, and Windows. Requires Python 3.6+
"""

import os, sys, stat

# ── Colours (disabled on Windows) ────────────────────────────────────────────
NO_COLOUR = sys.platform == "win32"
def g(s): return s if NO_COLOUR else f"\033[0;32m{s}\033[0m"
def y(s): return s if NO_COLOUR else f"\033[1;33m{s}\033[0m"
def b(s): return s if NO_COLOUR else f"\033[1m{s}\033[0m"
def c(s): return s if NO_COLOUR else f"\033[0;36m{s}\033[0m"

def hdr(s):  print(b(s))
def ok(s):   print(g(f"  ✓ {s}"))
def info(s): print(c(f"  · {s}"))
def warn(s): print(y(f"  ⚠ {s}"))

def ask(prompt, default=None):
    suffix = f" [{default}]" if default else ""
    val = input(f"  {prompt}{suffix}: ").strip()
    return val if val else (default or "")

def write(path, content, executable=False):
    os.makedirs(os.path.dirname(path) if os.path.dirname(path) else ".", exist_ok=True)
    with open(path, "w", newline="\n") as f:
        f.write(content)
    if executable and sys.platform != "win32":
        st = os.stat(path)
        os.chmod(path, st.st_mode | stat.S_IEXEC | stat.S_IXGRP | stat.S_IXOTH)
    ok(path)

# ─────────────────────────────────────────────────────────────────────────────
# QUESTIONS
# ─────────────────────────────────────────────────────────────────────────────
print()
hdr("════════════════════════════════════════════════════════")
hdr("  Agentic Coding Tools — Kit Builder")
hdr("════════════════════════════════════════════════════════")

print("""
  Where should the rules live?

   1) Global only  — rules apply to ALL projects on this machine
                     Installs to:  ~/.claude/  ~/.codex/  ~/.gemini/

   2) Project only — rules live inside one repo, safe to commit
                     Creates:  .claude/  .codex/  .gemini/  in current dir

   3) Both         — global defaults + per-project overrides  (recommended)
""")
scope = ask("Choice", "3")
build_global  = scope in ("1", "3")
build_project = scope in ("2", "3")

print("""
  Select your primary language(s).
  Enter numbers separated by spaces, e.g: 1 3

   1) C++          2) C# / .NET     3) VB.NET        4) Rust
   5) Go           6) TypeScript    7) JavaScript     8) Python
   9) PHP         10) Java         11) Kotlin        12) Swift
  13) Ruby        14) Scala        15) Haskell       16) Lua
  17) Zig         18) Elixir       19) Dart/Flutter  20) Other/All
""")
lang_input = ask("Your choice(s)", "20")
selected = set(lang_input.split())
all_langs = "20" in selected or not selected

def sel(n): return all_langs or str(n) in selected

# Build system follow-ups
build_system = "cmake"
if sel(1) and not all_langs:
    print("\n  C++ build system:  1) CMake (default)  2) Make  3) Ninja  4) Manual")
    bs = ask("Choice", "1")
    build_system = {"2": "make", "3": "ninja", "4": "manual"}.get(bs, "cmake")

java_build = "maven"
if sel(10) and not all_langs:
    print("\n  Java build system:  1) Maven (default)  2) Gradle")
    jb = ask("Choice", "1")
    java_build = "gradle" if jb == "2" else "maven"

# Derive primary stack label + build command for context files
lang_note, build_cmd = "Add your primary language here", "# Add your build command here"
if   sel(1)  and not all_langs:
    build_cmd = {"cmake": "cmake --build build -j$(nproc)", "make": "make -j$(nproc)",
                 "ninja": "ninja -C build", "manual": "# Configure your build command"}[build_system]
    lang_note = f"C++ / {build_system.title()}"
elif sel(2)  and not all_langs: lang_note, build_cmd = "C# / .NET",        "dotnet build"
elif sel(3)  and not all_langs: lang_note, build_cmd = "VB.NET / .NET",    "dotnet build"
elif sel(4)  and not all_langs: lang_note, build_cmd = "Rust",             "cargo build"
elif sel(5)  and not all_langs: lang_note, build_cmd = "Go",               "go build ./..."
elif sel(6)  and not all_langs: lang_note, build_cmd = "TypeScript",       "npx tsc --noEmit"
elif sel(7)  and not all_langs: lang_note, build_cmd = "JavaScript",       "npm run build"
elif sel(8)  and not all_langs: lang_note, build_cmd = "Python",           "ruff check ."
elif sel(9)  and not all_langs: lang_note, build_cmd = "PHP",              "php -l src/"
elif sel(10) and not all_langs:
    lang_note = f"Java / {java_build.title()}"
    build_cmd = "mvn compile" if java_build == "maven" else "gradle classes"
elif sel(11) and not all_langs: lang_note, build_cmd = "Kotlin / Gradle",  "gradle compileKotlin"
elif sel(12) and not all_langs: lang_note, build_cmd = "Swift / SPM",      "swift build"
elif sel(13) and not all_langs: lang_note, build_cmd = "Ruby",             "bundle exec rake"
elif sel(14) and not all_langs: lang_note, build_cmd = "Scala",            "sbt compile"
elif sel(15) and not all_langs: lang_note, build_cmd = "Haskell",          "cabal build"
elif sel(16) and not all_langs: lang_note, build_cmd = "Lua",              "luac -p *.lua"
elif sel(17) and not all_langs: lang_note, build_cmd = "Zig",              "zig build"
elif sel(18) and not all_langs: lang_note, build_cmd = "Elixir",           "mix compile"
elif sel(19) and not all_langs: lang_note, build_cmd = "Dart / Flutter",   "flutter build"

# ─────────────────────────────────────────────────────────────────────────────
# FILE CONTENT DEFINITIONS
# ─────────────────────────────────────────────────────────────────────────────

GLOBAL_CLAUDE_SETTINGS = """{
  "$schema": "https://json.schemastore.org/claude-code-settings.json",
  "env": {
    "MAX_THINKING_TOKENS":                      "8000",
    "DISABLE_NON_ESSENTIAL_MODEL_CALLS":        "1",
    "CLAUDE_CODE_DISABLE_NONESSENTIAL_TRAFFIC": "1",
    "ANTHROPIC_SMALL_FAST_MODEL":               "claude-haiku-4-5-20251001"
  }
}
"""

GLOBAL_CLAUDE_MD = """# Global Claude Code Rules
# Loaded for EVERY Claude Code session on this machine.
# Project rules go in <project>/.claude/CLAUDE.md — do not duplicate here.
# Keep lean: every token here costs quota on every prompt.

## Core
- Simplicity first. Touch minimal code. Find root causes, not workarounds.
- Never mark a task done without proving it works.
- Fix bugs autonomously.

## Context
- Read only specific files needed. Never explore broadly unless asked.
- Use /clear between unrelated tasks to reset accumulated context.
- Reference exact file paths, not vague descriptions.
- Keep responses concise. No padding.

## Planning
- Non-trivial tasks (3+ steps): write a brief plan first, check in before executing.
- Simple fixes: skip planning overhead.

## Subagents
- Use only when genuine parallelism is needed.
- Return summaries, not full file contents.
- Never spawn a subagent for a single-file task.

## Git
- Never commit without being asked.
- Never force-push to main, master, production, or release branches.
"""

GLOBAL_CODEX_CONFIG = """# Global Codex CLI config — applies to all sessions on this machine.
# Project overrides go in <project>/.codex/config.toml
# Validated Feb 2026: https://developers.openai.com/codex/config-reference/

model_reasoning_effort  = "medium"
model_reasoning_summary = "none"
tool_output_token_limit = 3000
project_doc_max_bytes   = 8192
approval_policy         = "on-request"
sandbox_mode            = "workspace-write"

[profiles.light]
model_reasoning_effort  = "low"
tool_output_token_limit = 1500

[profiles.deep]
model_reasoning_effort  = "high"
tool_output_token_limit = 8000

[profiles.review]
approval_policy         = "untrusted"
sandbox_mode            = "read-only"
model_reasoning_effort  = "low"
tool_output_token_limit = 2000
"""

GLOBAL_AGENTS_MD = """# Global AGENTS.md
# Read by Codex CLI and any tool honouring the Linux Foundation AGENTS.md standard.
# Project rules go in <project>/.codex/AGENTS.md — do not duplicate here.
# Keep lean: every token here costs quota on every turn.

## Core Rules
- Simplicity first. Touch minimal code. Find root causes, not workarounds.
- Never mark a task done without proving it works.

## Context
- Read only specific files needed. Keep responses concise.

## Planning
- Non-trivial tasks: plan first, check in before executing.

## Git
- Never commit without being asked.
- Never force-push to main, master, production, or release branches.
"""

GLOBAL_GEMINI_SETTINGS = """{
  "chatCompression": { "contextPercentageThreshold": 0.5 },
  "model": {
    "summarizeToolOutput": {
      "run_shell_command": { "tokenBudget": 500 },
      "read_file":         { "tokenBudget": 2000 },
      "list_directory":    { "tokenBudget": 300 }
    }
  },
  "fileFiltering":  { "respectGitIgnore": true },
  "checkpointing":  { "enabled": true },
  "autoAccept": false
}
"""

GLOBAL_GEMINI_MD = """# Global Gemini CLI Context
# Loaded for every Gemini CLI session on this machine.
# Project rules go in <project>/.gemini/GEMINI.md — do not duplicate here.
# Keep lean: every token here costs quota on every turn.

## Core Rules
- Simplicity first. Touch minimal code. Find root causes, not workarounds.
- Never mark a task done without proving it works.
- Use /clear between unrelated tasks.
- Keep responses concise.

## Git
- Never commit without being asked.
- Never force-push to main, master, production, or release branches.
"""

GEMINI_CMD_PLAN = """description = "Plan a task step-by-step without implementing anything."
prompt = \"\"\"
Task: {{args}}

Produce a numbered implementation plan:
1. List every file that needs to change and why.
2. For each file, describe what changes are needed — no code yet.
3. Flag risks, unknowns, edge cases, dependencies.
4. Estimate complexity: trivial / small / medium / large.

Do NOT write any code or make any file changes.
Wait for the user to confirm before proceeding.
\"\"\"
"""

GEMINI_CMD_REVIEW = """description = "Review current context for bugs, security issues, and improvements."
prompt = \"\"\"
Review all code in the current context.

Check for:
1. Bugs and logic errors
2. Unhandled edge cases
3. Security issues (injection, overflow, untrusted input, secrets in code)
4. Performance problems
5. Missing error handling

For each issue: state file/line, describe the problem, suggest a fix.
Rank each: critical / major / minor / suggestion.
\"\"\"
"""

GEMINI_CMD_COMMIT = """description = "Generate a conventional commit message from the current diff."
prompt = \"\"\"
Git status:
!{git status --short}

Diff (first 300 lines):
!{git diff HEAD | head -300}

Write a conventional commit message.
Format:  <type>(<scope>): <short description>
Types: feat | fix | refactor | docs | chore | test | perf | style | build | ci
Rules: max 72 chars, imperative mood, no trailing period.
Hint: {{args}}
Output the commit message only — no preamble.
\"\"\"
"""

GEMINI_CMD_CHANGELOG = """description = "Generate a CHANGELOG.md entry from recent commits."
prompt = \"\"\"
Recent commits:
!{git log --oneline -30}

Generate a CHANGELOG.md entry (Keep a Changelog format).
## [{{args}}] - !{date +%Y-%m-%d}
Sections: Added / Changed / Fixed / Removed
Omit chore/ci/docs unless user-visible. Plain language, no hashes.
\"\"\"
"""

GEMINI_EXTENSION = """{
  "name": "project",
  "version": "1.0.0",
  "description": "Project-specific commands and context.",
  "contextFileName": "GEMINI.md"
}
"""

def project_claude_md(lang, cmd):
    return f"""# Project Rules — Claude Code
# Global rules are in ~/.claude/CLAUDE.md — do not duplicate here.
# Keep lean: every token here costs quota on every prompt.

## Stack
# Primary language: {lang}
# Build command:    {cmd}

## Conventions
# Add project-specific coding conventions here.
# e.g. "Use snake_case for all identifiers"
# e.g. "All public functions must have a docstring"
"""

def project_agents_md(lang, cmd):
    return f"""# Project AGENTS.md
# Read by Codex CLI and AGENTS.md-compatible tools (Cursor, Amp, etc.)
# Global rules are in ~/.codex/AGENTS.md — do not duplicate here.
# Keep lean: every token here costs quota on every turn.

## Stack
# Primary language: {lang}
# Build command:    {cmd}

## Conventions
# Add project-specific instructions here.
"""

def project_gemini_md(lang, cmd):
    return f"""# Project Context — Gemini CLI
# Global rules are in ~/.gemini/GEMINI.md — do not duplicate here.
# Keep lean: every token here costs quota on every turn.

## Stack
# Primary language: {lang}
# Build command:    {cmd}
"""

PROJECT_CLAUDE_SETTINGS = """{
  "hooks": {
    "SessionStart": [{
      "hooks": [{ "type": "command", "command": "bash .claude/hooks/session-start.sh" }]
    }],
    "PreToolUse": [
      { "matcher": "Bash",
        "hooks": [{ "type": "command", "command": "bash .claude/hooks/pre-bash.sh" }] },
      { "matcher": "Edit|Write|MultiEdit",
        "hooks": [{ "type": "command", "command": "bash .claude/hooks/pre-write.sh" }] }
    ],
    "PostToolUse": [{
      "matcher": "Edit|Write|MultiEdit",
      "hooks": [{ "type": "command", "command": "bash .claude/hooks/post-write.sh" }]
    }],
    "PostToolUseFailure": [{
      "hooks": [{ "type": "command", "command": "bash .claude/hooks/post-failure.sh" }]
    }],
    "Stop": [{
      "hooks": [{ "type": "command", "command": "bash .claude/hooks/on-stop.sh" }]
    }]
  },
  "permissions": {
    "deny": [
      "Bash(rm -rf /)", "Bash(rm -rf ~)", "Bash(sudo rm -rf *)",
      "Bash(git push --force*)", "Bash(git push -f *)",
      "Read(**/.env)", "Read(**/.env.*)", "Edit(**/.env)", "Edit(**/.env.*)"
    ],
    "allow": [
      "Bash(git status)", "Bash(git diff*)", "Bash(git log*)", "Bash(git branch*)"
    ]
  }
}
"""

PROJECT_CLAUDE_SETTINGS_WIN = """{
  "_note": "Windows version — hooks use PowerShell. This file is auto-activated by install.ps1.",
  "hooks": {
    "SessionStart": [{
      "hooks": [{ "type": "command", "command": "powershell -ExecutionPolicy Bypass -File .claude/hooks/session-start.ps1" }]
    }],
    "PreToolUse": [
      { "matcher": "Bash",
        "hooks": [{ "type": "command", "command": "powershell -ExecutionPolicy Bypass -File .claude/hooks/pre-bash.ps1" }] },
      { "matcher": "Edit|Write|MultiEdit",
        "hooks": [{ "type": "command", "command": "powershell -ExecutionPolicy Bypass -File .claude/hooks/pre-write.ps1" }] }
    ],
    "PostToolUse": [{
      "matcher": "Edit|Write|MultiEdit",
      "hooks": [{ "type": "command", "command": "powershell -ExecutionPolicy Bypass -File .claude/hooks/post-write.ps1" }]
    }],
    "PostToolUseFailure": [{
      "hooks": [{ "type": "command", "command": "powershell -ExecutionPolicy Bypass -File .claude/hooks/post-failure.ps1" }]
    }],
    "Stop": [{
      "hooks": [{ "type": "command", "command": "powershell -ExecutionPolicy Bypass -File .claude/hooks/on-stop.ps1" }]
    }]
  },
  "permissions": {
    "deny": [
      "Bash(rm -rf /)", "Bash(rm -rf ~)", "Bash(git push --force*)",
      "Read(**/.env)", "Edit(**/.env)"
    ],
    "allow": [
      "Bash(git status)", "Bash(git diff*)", "Bash(git log*)"
    ]
  }
}
"""

PROJECT_CODEX_CONFIG = """# Project-level Codex CLI config — overrides ~/.codex/config.toml for this project.
tool_output_token_limit = 3000
project_doc_max_bytes   = 8192
sandbox_mode            = "workspace-write"

[profiles.build]
model_reasoning_effort  = "high"
tool_output_token_limit = 8000

[profiles.review]
approval_policy         = "untrusted"
sandbox_mode            = "read-only"
model_reasoning_effort  = "low"
"""

PROJECT_GEMINI_SETTINGS = """{
  "chatCompression": { "contextPercentageThreshold": 0.5 },
  "model": {
    "summarizeToolOutput": {
      "run_shell_command": { "tokenBudget": 500 },
      "read_file":         { "tokenBudget": 2000 },
      "list_directory":    { "tokenBudget": 300 }
    }
  },
  "fileFiltering":  { "respectGitIgnore": true },
  "checkpointing":  { "enabled": true },
  "autoAccept": false
}
"""

HOOK_SESSION_START_SH = """#!/usr/bin/env bash
# SessionStart hook — shows project context when a Claude Code session opens.
cd "${CLAUDE_PROJECT_DIR:-$PWD}" 2>/dev/null || exit 0
echo "=== Project context ============================================="
echo "  Dir  : $PWD"
echo "  Date : $(date)"
if git rev-parse --git-dir >/dev/null 2>&1; then
  echo "  Branch      : $(git branch --show-current 2>/dev/null)"
  echo "  Last commit : $(git log --oneline -1 2>/dev/null)"
  DIRTY=$(git status --porcelain 2>/dev/null | wc -l | tr -d ' ')
  [ "$DIRTY" -gt 0 ] && echo "  Uncommitted : $DIRTY changed file(s)"
fi
[ -f CMakeLists.txt ]   && echo "  Stack : C++ / CMake"
[ -f Cargo.toml ]       && echo "  Stack : Rust"
[ -f go.mod ]           && echo "  Stack : Go"
[ -f package.json ]     && echo "  Stack : Node.js / JS / TS"
[ -f pyproject.toml ]   && echo "  Stack : Python"
[ -f composer.json ]    && echo "  Stack : PHP"
[ -f pom.xml ]          && echo "  Stack : Java / Maven"
[ -f build.gradle ]     && echo "  Stack : Java|Kotlin / Gradle"
[ -f Package.swift ]    && echo "  Stack : Swift / SPM"
[ -f mix.exs ]          && echo "  Stack : Elixir"
[ -f pubspec.yaml ]     && echo "  Stack : Dart / Flutter"
[ -f build.zig ]        && echo "  Stack : Zig"
for f in *.sln *.csproj *.vbproj; do [ -f "$f" ] && echo "  Stack : .NET" && break; done
echo "================================================================="
exit 0
"""

HOOK_PRE_BASH_SH = """#!/usr/bin/env bash
# PreToolUse:Bash — blocks destructive shell commands. exit 2 = blocking error to Claude.
INPUT=$(cat)
CMD=$(echo "$INPUT" | python3 -c \\
  "import sys,json; d=json.load(sys.stdin); print(d.get('tool_input',{}).get('command',''))" 2>/dev/null)
PATTERNS=(
  "rm -rf /" "rm -rf ~" "rm -rf \\$HOME" ":(){:|:&};:" "mkfs"
  "dd if=/dev/zero" "> /dev/sd" "curl.* | bash" "curl.* | sh"
  "wget.* | bash" "wget.* | sh" "chmod -R 777 /" "chown -R.* /"
)
for p in "${PATTERNS[@]}"; do
  if echo "$CMD" | grep -qiE "$p"; then
    echo "BLOCKED: Dangerous pattern matched: $p" >&2; echo "Command: $CMD" >&2; exit 2
  fi
done
if echo "$CMD" | grep -qE "git push.*(--force|-f).*(main|master|production|prod|release)"; then
  echo "BLOCKED: Force-push to protected branch not allowed." >&2; exit 2
fi
exit 0
"""

HOOK_PRE_WRITE_SH = """#!/usr/bin/env bash
# PreToolUse:Edit|Write — blocks writes to secrets and lock files. exit 2 = blocking.
INPUT=$(cat)
FILE=$(echo "$INPUT" | python3 -c \\
  "import sys,json; d=json.load(sys.stdin); print(d.get('tool_input',{}).get('path',''))" 2>/dev/null)
[ -z "$FILE" ] && exit 0
SENSITIVE=(\\.env$ \\.env\\. id_rsa id_ed25519 id_ecdsa \\.pem$ \\.key$ \\.p12$ \\.pfx$ secrets\\. credentials\\. \\.netrc$ auth\\.json$)
for p in "${SENSITIVE[@]}"; do
  echo "$FILE" | grep -qiE "$p" && echo "BLOCKED: Sensitive file: $FILE" >&2 && exit 2
done
LOCKFILES=(package-lock\\.json$ yarn\\.lock$ pnpm-lock\\.yaml$ Cargo\\.lock$ Gemfile\\.lock$ poetry\\.lock$ composer\\.lock$ go\\.sum$)
for p in "${LOCKFILES[@]}"; do
  echo "$FILE" | grep -qiE "$p" && echo "BLOCKED: Do not hand-edit lock files: $FILE" >&2 && exit 2
done
exit 0
"""

HOOK_POST_WRITE_SH = """#!/usr/bin/env bash
# PostToolUse:Edit|Write — runs build/lint for the saved file's language.
# exit 1 = check failed; stderr fed back to Claude as context.
INPUT=$(cat)
FILE=$(echo "$INPUT" | python3 -c \\
  "import sys,json; d=json.load(sys.stdin); print(d.get('tool_input',{}).get('path',''))" 2>/dev/null)
[ -z "$FILE" ] && exit 0
EXT=$(echo "${FILE##*.}" | tr '[:upper:]' '[:lower:]')
ROOT="${CLAUDE_PROJECT_DIR:-$PWD}"
NCPU=$(sysctl -n hw.ncpu 2>/dev/null || nproc 2>/dev/null || echo 4)

chk() {
  local label="$1"; shift
  local out; out=$("$@" 2>&1); local s=$?
  [ $s -ne 0 ] && { echo "[$label] FAILED: $FILE" >&2; echo "$out" | tail -50 >&2; exit 1; }
}
chk_sh() {
  local label="$1"; shift
  local out; out=$(eval "$*" 2>&1); local s=$?
  [ $s -ne 0 ] && { echo "[$label] FAILED: $FILE" >&2; echo "$out" | tail -50 >&2; exit 1; }
}

case "$EXT" in
  c|cpp|cc|cxx|c++|h|hpp|hxx|hh|inl)
    if [ -d "$ROOT/build" ]; then
      if   [ -f "$ROOT/build/build.ninja" ] && command -v ninja >/dev/null 2>&1; then chk "Ninja" ninja -C "$ROOT/build" -j"$NCPU"
      elif [ -f "$ROOT/build/CMakeCache.txt" ] && command -v cmake >/dev/null 2>&1; then chk "CMake" cmake --build "$ROOT/build" -j"$NCPU"
      elif [ -f "$ROOT/Makefile" ] && command -v make >/dev/null 2>&1; then chk "Make" make -C "$ROOT" -j"$NCPU"
      fi
    fi
    command -v clang-tidy >/dev/null 2>&1 && [ -f "$ROOT/.clang-tidy" ] && chk_sh "clang-tidy" "clang-tidy '$FILE' --quiet 2>&1 | head -40"
    ;;
  cs|vb|fs|fsx|fsi|csproj|vbproj|fsproj)
    command -v dotnet >/dev/null 2>&1 && {
      T=$(find "$ROOT" -maxdepth 3 \\( -name "*.sln" -o -name "*.*proj" \\) | head -1)
      [ -n "$T" ] && chk_sh "dotnet" "dotnet build '$T' --no-restore -v quiet 2>&1 | tail -30"
    } ;;
  rs)
    command -v cargo >/dev/null 2>&1 && [ -f "$ROOT/Cargo.toml" ] &&
      chk_sh "cargo" "cargo check --manifest-path '$ROOT/Cargo.toml' --quiet 2>&1 | tail -30" ;;
  go)
    command -v go >/dev/null 2>&1 && [ -f "$ROOT/go.mod" ] &&
      { chk "go build" go build "$ROOT/..."; chk "go vet" go vet "$ROOT/..."; } ;;
  js|jsx|mjs|cjs)
    command -v eslint >/dev/null 2>&1 &&
      [ -n "$(find "$ROOT" -maxdepth 2 \\( -name '.eslintrc*' -o -name 'eslint.config*' \\) | head -1)" ] &&
      chk "ESLint" eslint "$FILE" --quiet ;;
  ts|tsx|mts|cts)
    command -v tsc >/dev/null 2>&1 && {
      T=$(find "$ROOT" -maxdepth 2 -name "tsconfig*.json" | head -1)
      if [ -n "$T" ]; then chk_sh "tsc" "tsc --project '$T' --noEmit 2>&1 | tail -30"
      else chk_sh "tsc" "tsc --noEmit --strict '$FILE' 2>&1 | tail -20"; fi
    } ;;
  py)
    if   command -v ruff   >/dev/null 2>&1; then chk "ruff"   ruff check "$FILE" --quiet
    elif command -v flake8 >/dev/null 2>&1; then chk "flake8" flake8 "$FILE" --max-line-length=120 --quiet
    elif command -v pylint >/dev/null 2>&1; then chk_sh "pylint" "pylint '$FILE' --errors-only --score=no 2>&1 | tail -20"
    fi
    command -v mypy >/dev/null 2>&1 && {
      for f in mypy.ini setup.cfg pyproject.toml .mypy.ini; do
        [ -f "$ROOT/$f" ] && chk_sh "mypy" "mypy '$FILE' --ignore-missing-imports --no-error-summary 2>&1 | tail -20" && break
      done
    } ;;
  php)
    command -v php    >/dev/null 2>&1 && chk "php -l" php -l "$FILE"
    command -v phpstan >/dev/null 2>&1 && chk_sh "phpstan" "phpstan analyse '$FILE' --level=5 --no-progress 2>&1 | tail -20" ;;
  java)
    if   command -v mvn    >/dev/null 2>&1 && [ -f "$ROOT/pom.xml" ]; then chk_sh "Maven"  "mvn compile -f '$ROOT/pom.xml' -q 2>&1 | tail -30"
    elif command -v gradle >/dev/null 2>&1 && { [ -f "$ROOT/build.gradle" ] || [ -f "$ROOT/build.gradle.kts" ]; }; then chk_sh "Gradle" "gradle compileJava -p '$ROOT' --quiet 2>&1 | tail -30"
    elif command -v javac  >/dev/null 2>&1; then chk_sh "javac" "javac '$FILE' -d /tmp 2>&1 | tail -20"; fi ;;
  kt|kts)
    if   command -v gradle  >/dev/null 2>&1 && { [ -f "$ROOT/build.gradle.kts" ] || [ -f "$ROOT/build.gradle" ]; }; then chk_sh "Gradle Kotlin" "gradle compileKotlin -p '$ROOT' --quiet 2>&1 | tail -30"
    elif command -v kotlinc >/dev/null 2>&1; then chk_sh "kotlinc" "kotlinc '$FILE' -include-runtime -d /tmp/out.jar 2>&1 | tail -20"; fi ;;
  swift)
    if   command -v swift  >/dev/null 2>&1 && [ -f "$ROOT/Package.swift" ]; then chk_sh "swift build" "swift build --package-path '$ROOT' 2>&1 | tail -30"
    elif command -v swiftc >/dev/null 2>&1; then chk_sh "swiftc" "swiftc -typecheck '$FILE' 2>&1 | tail -20"; fi ;;
  rb)
    command -v ruby    >/dev/null 2>&1 && chk "ruby -c" ruby -c "$FILE"
    command -v rubocop >/dev/null 2>&1 && chk_sh "rubocop" "rubocop '$FILE' --no-color --format quiet 2>&1 | tail -20" ;;
  scala|sc)
    command -v sbt >/dev/null 2>&1 && [ -f "$ROOT/build.sbt" ] && chk_sh "sbt" "sbt compile 2>&1 | tail -30" ;;
  hs|lhs)
    if   command -v cabal >/dev/null 2>&1 && ls "$ROOT"/*.cabal >/dev/null 2>&1; then chk_sh "cabal" "cabal build 2>&1 | tail -30"
    elif command -v stack >/dev/null 2>&1 && [ -f "$ROOT/stack.yaml" ]; then chk_sh "stack" "stack build 2>&1 | tail -30"; fi ;;
  lua)  command -v luac >/dev/null 2>&1 && chk "luac" luac -p "$FILE" ;;
  zig)  command -v zig  >/dev/null 2>&1 && [ -f "$ROOT/build.zig" ] && chk_sh "zig" "zig build 2>&1 | tail -30" ;;
  ex|exs)
    command -v mix >/dev/null 2>&1 && [ -f "$ROOT/mix.exs" ] &&
      chk_sh "mix" "cd '$ROOT' && mix compile --warnings-as-errors 2>&1 | tail -30" ;;
  dart)
    if   command -v flutter >/dev/null 2>&1 && [ -f "$ROOT/pubspec.yaml" ]; then chk_sh "flutter" "flutter analyze '$FILE' 2>&1 | tail -20"
    elif command -v dart    >/dev/null 2>&1; then chk_sh "dart" "dart analyze '$FILE' 2>&1 | tail -20"; fi ;;
esac
exit 0
"""

HOOK_ON_STOP_SH = """#!/usr/bin/env bash
# Stop hook — prints a git diff summary at the end of each Claude turn.
cd "${CLAUDE_PROJECT_DIR:-$PWD}" 2>/dev/null || exit 0
if git rev-parse --git-dir >/dev/null 2>&1; then
  CHANGED=$(git diff --stat HEAD 2>/dev/null | tail -1)
  UNTRACKED=$(git ls-files --others --exclude-standard 2>/dev/null | wc -l | tr -d ' ')
  if [ -n "$CHANGED" ] || [ "${UNTRACKED:-0}" -gt 0 ]; then
    echo ""
    echo "=== Turn summary ================================================="
    [ -n "$CHANGED" ]              && echo "  Modified : $CHANGED"
    [ "${UNTRACKED:-0}" -gt 0 ]    && echo "  New files: $UNTRACKED untracked"
    echo "================================================================="
  fi
fi
exit 0
"""

HOOK_POST_FAILURE_SH = """#!/usr/bin/env bash
# PostToolUseFailure — logs failed tool calls for diagnostics.
LOG="${CLAUDE_PROJECT_DIR:-$PWD}/.claude/tool-failures.log"
INPUT=$(cat)
TOOL=$(echo "$INPUT" | python3 -c \\
  "import sys,json; d=json.load(sys.stdin); print(d.get('tool_name','unknown'))" 2>/dev/null)
mkdir -p "$(dirname "$LOG")"
echo "[$(date -u +"%Y-%m-%dT%H:%M:%SZ")] tool=$TOOL" >> "$LOG"
echo "$INPUT" >> "$LOG"
echo "---" >> "$LOG"
exit 0
"""

HOOK_SESSION_START_PS1 = """# SessionStart hook — PowerShell (Windows)
$root = if ($env:CLAUDE_PROJECT_DIR) { $env:CLAUDE_PROJECT_DIR } else { (Get-Location).Path }
Set-Location $root -ErrorAction SilentlyContinue
Write-Host "=== Project context ============================================="
Write-Host "  Dir  : $(Get-Location)"
Write-Host "  Date : $(Get-Date)"
$null = git rev-parse --git-dir 2>$null
if ($LASTEXITCODE -eq 0) {
  Write-Host "  Branch      : $(git branch --show-current 2>$null)"
  Write-Host "  Last commit : $(git log --oneline -1 2>$null)"
}
if (Test-Path "CMakeLists.txt") { Write-Host "  Stack : C++ / CMake" }
if (Test-Path "Cargo.toml")     { Write-Host "  Stack : Rust" }
if (Test-Path "go.mod")         { Write-Host "  Stack : Go" }
if (Test-Path "package.json")   { Write-Host "  Stack : Node.js / JS / TS" }
if (Test-Path "pyproject.toml") { Write-Host "  Stack : Python" }
if (Test-Path "pom.xml")        { Write-Host "  Stack : Java / Maven" }
if (Get-Item "*.sln" -ErrorAction SilentlyContinue) { Write-Host "  Stack : .NET" }
Write-Host "================================================================="
exit 0
"""

HOOK_PRE_BASH_PS1 = """# PreToolUse:Bash — PowerShell. exit 2 = blocking error fed back to Claude.
$raw = [Console]::In.ReadToEnd()
try { $data = $raw | ConvertFrom-Json } catch { exit 0 }
$cmd = if ($data.tool_input.command) { $data.tool_input.command } else { "" }
$blocked = @("rm -rf /","rm -rf ~","format ","del /s /q c:\\\\","rd /s /q c:\\\\")
foreach ($p in $blocked) {
  if ($cmd -match [regex]::Escape($p)) {
    [Console]::Error.WriteLine("BLOCKED: Dangerous pattern: $p")
    [Console]::Error.WriteLine("Command: $cmd")
    exit 2
  }
}
if ($cmd -match "git push.*(--force|-f).*(main|master|production|prod|release)") {
  [Console]::Error.WriteLine("BLOCKED: Force-push to protected branch not allowed.")
  exit 2
}
exit 0
"""

HOOK_PRE_WRITE_PS1 = """# PreToolUse:Edit|Write — PowerShell. Blocks writes to secrets and lock files.
$raw = [Console]::In.ReadToEnd()
try { $data = $raw | ConvertFrom-Json } catch { exit 0 }
$file = if ($data.tool_input.path) { $data.tool_input.path } else { "" }
if (-not $file) { exit 0 }
$sensitive = @("\\.env$","\\.env\\.","id_rsa","id_ed25519","\\.pem$","\\.key$","secrets\\.","credentials\\.")
foreach ($p in $sensitive) {
  if ($file -match $p) { [Console]::Error.WriteLine("BLOCKED: Sensitive file: $file"); exit 2 }
}
$locks = @("package-lock\\.json$","yarn\\.lock$","pnpm-lock\\.yaml$","Cargo\\.lock$","go\\.sum$")
foreach ($p in $locks) {
  if ($file -match $p) { [Console]::Error.WriteLine("BLOCKED: Do not hand-edit lock file: $file"); exit 2 }
}
exit 0
"""

HOOK_POST_WRITE_PS1 = """# PostToolUse:Edit|Write — PowerShell. Runs build/lint after file save.
$raw = [Console]::In.ReadToEnd()
try { $data = $raw | ConvertFrom-Json } catch { exit 0 }
$file = if ($data.tool_input.path) { $data.tool_input.path } else { "" }
if (-not $file) { exit 0 }
$ext  = [IO.Path]::GetExtension($file).TrimStart(".").ToLower()
$root = if ($env:CLAUDE_PROJECT_DIR) { $env:CLAUDE_PROJECT_DIR } else { (Get-Location).Path }
$ncpu = (Get-CimInstance Win32_Processor).NumberOfLogicalProcessors

function Chk($label, $cmd) {
  $out = Invoke-Expression $cmd 2>&1
  if ($LASTEXITCODE -ne 0) {
    [Console]::Error.WriteLine("[$label] FAILED: $file")
    $out | Select-Object -Last 50 | ForEach-Object { [Console]::Error.WriteLine($_) }
    exit 1
  }
}

switch -Regex ($ext) {
  "^(cpp|cc|cxx|c|h|hpp|hxx)$" {
    if (Test-Path "$root\\\\build\\\\CMakeCache.txt") { Chk "CMake" "cmake --build '$root\\\\build' -j $ncpu" }
    elseif (Test-Path "$root\\\\Makefile")            { Chk "Make"  "make -C '$root'" }
  }
  "^(cs|vb|fs|fsx|csproj|vbproj|fsproj)$" {
    if (Get-Command dotnet -ErrorAction SilentlyContinue) {
      $t = Get-ChildItem $root -Recurse -Depth 3 -Include "*.sln","*.csproj","*.vbproj" | Select-Object -First 1
      if ($t) { Chk "dotnet" "dotnet build '$($t.FullName)' --no-restore -v quiet" }
    }
  }
  "^rs$"  { if ((Get-Command cargo -EA SilentlyContinue) -and (Test-Path "$root\\\\Cargo.toml"))  { Chk "cargo"   "cargo check --manifest-path '$root\\\\Cargo.toml' --quiet" } }
  "^go$"  { if ((Get-Command go    -EA SilentlyContinue) -and (Test-Path "$root\\\\go.mod"))      { Chk "go build" "go build $root\\\\..."; Chk "go vet" "go vet $root\\\\..." } }
  "^(ts|tsx|mts|cts)$" {
    if (Get-Command tsc -EA SilentlyContinue) {
      $tc = Get-ChildItem $root -Depth 2 -Filter "tsconfig*.json" | Select-Object -First 1
      if ($tc) { Chk "tsc" "tsc --project '$($tc.FullName)' --noEmit" }
      else     { Chk "tsc" "tsc --noEmit --strict '$file'" }
    }
  }
  "^(js|jsx|mjs|cjs)$" { if (Get-Command eslint -EA SilentlyContinue) { Chk "ESLint" "eslint '$file' --quiet" } }
  "^py$"  {
    if (Get-Command ruff   -EA SilentlyContinue) { Chk "ruff"   "ruff check '$file' --quiet" }
    elseif (Get-Command flake8 -EA SilentlyContinue) { Chk "flake8" "flake8 '$file'" }
  }
  "^php$" { if (Get-Command php -EA SilentlyContinue) { Chk "php -l" "php -l '$file'" } }
  "^java$" {
    if ((Get-Command mvn -EA SilentlyContinue) -and (Test-Path "$root\\\\pom.xml")) { Chk "Maven" "mvn compile -f '$root\\\\pom.xml' -q" }
    elseif (Get-Command gradle -EA SilentlyContinue) { Chk "Gradle" "gradle compileJava -p '$root' --quiet" }
  }
  "^(kt|kts)$" { if (Get-Command gradle -EA SilentlyContinue) { Chk "Gradle Kotlin" "gradle compileKotlin -p '$root' --quiet" } }
  "^swift$" {
    if ((Get-Command swift -EA SilentlyContinue) -and (Test-Path "$root\\\\Package.swift")) { Chk "swift" "swift build --package-path '$root'" }
  }
  "^rb$" {
    if (Get-Command ruby   -EA SilentlyContinue) { Chk "ruby -c" "ruby -c '$file'" }
    if (Get-Command rubocop -EA SilentlyContinue) { Chk "rubocop" "rubocop '$file' --no-color --format quiet" }
  }
  "^dart$" {
    if (Get-Command flutter -EA SilentlyContinue) { Chk "flutter" "flutter analyze '$file'" }
    elseif (Get-Command dart -EA SilentlyContinue) { Chk "dart" "dart analyze '$file'" }
  }
}
exit 0
"""

HOOK_ON_STOP_PS1 = """# Stop hook — PowerShell. Shows git diff summary at end of each turn.
$root = if ($env:CLAUDE_PROJECT_DIR) { $env:CLAUDE_PROJECT_DIR } else { (Get-Location).Path }
Set-Location $root -ErrorAction SilentlyContinue
$null = git rev-parse --git-dir 2>$null
if ($LASTEXITCODE -eq 0) {
  $changed   = git diff --stat HEAD 2>$null | Select-Object -Last 1
  $untracked = (git ls-files --others --exclude-standard 2>$null | Measure-Object -Line).Lines
  if ($changed -or $untracked -gt 0) {
    Write-Host "`n=== Turn summary ================================================="
    if ($changed)         { Write-Host "  Modified : $changed" }
    if ($untracked -gt 0) { Write-Host "  New files: $untracked untracked" }
    Write-Host "================================================================="
  }
}
exit 0
"""

HOOK_POST_FAILURE_PS1 = """# PostToolUseFailure — PowerShell. Logs failed tool calls.
$root = if ($env:CLAUDE_PROJECT_DIR) { $env:CLAUDE_PROJECT_DIR } else { (Get-Location).Path }
$log  = "$root\\.claude\\tool-failures.log"
$raw  = [Console]::In.ReadToEnd()
try { $data = $raw | ConvertFrom-Json } catch {}
$tool = if ($data.tool_name) { $data.tool_name } else { "unknown" }
$ts   = (Get-Date).ToUniversalTime().ToString("yyyy-MM-ddTHH:mm:ssZ")
New-Item -ItemType Directory -Path (Split-Path $log) -Force | Out-Null
"[$ts] tool=$tool" | Add-Content $log
$raw | Add-Content $log
"---" | Add-Content $log
exit 0
"""

INSTALL_SH = """#!/usr/bin/env bash
# install.sh — installs global configs to ~/.claude  ~/.codex  ~/.gemini
# Usage:
#   ./install.sh                        # global only
#   ./install.sh /path/to/your/project  # also copy project files into repo

set -e
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
G='\\033[0;32m'; Y='\\033[1;33m'; R='\\033[0m'
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
"""

INSTALL_PS1 = """# install.ps1 — installs global configs and optionally project files (Windows)
# Usage:
#   .\\install.ps1
#   .\\install.ps1 -ProjectPath C:\\path\\to\\repo
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
  Copy-Item $src $dest -Recurse -Force; Write-Host "  OK: $dest\\"
}

Write-Host "`n-- Claude Code global (~\\.claude\\) --"
Cp-File "$ScriptDir\\global\\.claude\\settings.json" "$HOME\\.claude\\settings.json"
Cp-File "$ScriptDir\\global\\.claude\\CLAUDE.md"     "$HOME\\.claude\\CLAUDE.md"

Write-Host "`n-- Codex CLI global (~\\.codex\\) --"
Cp-File "$ScriptDir\\global\\.codex\\config.toml" "$HOME\\.codex\\config.toml"
Cp-File "$ScriptDir\\global\\.codex\\AGENTS.md"   "$HOME\\.codex\\AGENTS.md"

Write-Host "`n-- Gemini CLI global (~\\.gemini\\) --"
Cp-File "$ScriptDir\\global\\.gemini\\settings.json" "$HOME\\.gemini\\settings.json"
Cp-File "$ScriptDir\\global\\.gemini\\GEMINI.md"     "$HOME\\.gemini\\GEMINI.md"
Cp-Dir  "$ScriptDir\\global\\.gemini\\commands"      "$HOME\\.gemini\\commands"

if ($ProjectPath -ne "") {
  if (-not (Test-Path $ProjectPath)) { Write-Error "Not found: $ProjectPath"; exit 1 }
  Write-Host "`n-- Project files ($ProjectPath) --"
  Cp-Dir "$ScriptDir\\project\\.claude"  "$ProjectPath\\.claude"
  Cp-Dir "$ScriptDir\\project\\.codex"   "$ProjectPath\\.codex"
  Cp-Dir "$ScriptDir\\project\\.gemini"  "$ProjectPath\\.gemini"
  # Activate Windows hook paths
  $ws = "$ProjectPath\\.claude\\settings.windows.json"
  if (Test-Path $ws) {
    Copy-Item $ws "$ProjectPath\\.claude\\settings.json" -Force
    Write-Host "  OK: Windows hook paths activated."
  }
}
Write-Host "`nDone. See README.md for next steps."
"""

GITIGNORE_NOTE = """.claude/tool-failures.log
.claude/settings.local.json
"""

# ─────────────────────────────────────────────────────────────────────────────
# BUILD
# ─────────────────────────────────────────────────────────────────────────────
print()
hdr("Building files...")
print()

if build_global:
    hdr("── Global files ──────────────────────────────────────────")
    write("global/.claude/settings.json",            GLOBAL_CLAUDE_SETTINGS)
    write("global/.claude/CLAUDE.md",                GLOBAL_CLAUDE_MD)
    write("global/.codex/config.toml",               GLOBAL_CODEX_CONFIG)
    write("global/.codex/AGENTS.md",                 GLOBAL_AGENTS_MD)
    write("global/.gemini/settings.json",            GLOBAL_GEMINI_SETTINGS)
    write("global/.gemini/GEMINI.md",                GLOBAL_GEMINI_MD)
    write("global/.gemini/commands/task/plan.toml",  GEMINI_CMD_PLAN)
    write("global/.gemini/commands/code/review.toml",GEMINI_CMD_REVIEW)
    write("global/.gemini/commands/git/commit.toml", GEMINI_CMD_COMMIT)
    write("global/.gemini/commands/git/changelog.toml", GEMINI_CMD_CHANGELOG)

if build_project:
    print()
    hdr("── Project files ─────────────────────────────────────────")
    write("project/.claude/CLAUDE.md",               project_claude_md(lang_note, build_cmd))
    write("project/.claude/settings.json",           PROJECT_CLAUDE_SETTINGS)
    write("project/.claude/settings.windows.json",   PROJECT_CLAUDE_SETTINGS_WIN)
    write("project/.codex/AGENTS.md",                project_agents_md(lang_note, build_cmd))
    write("project/.codex/config.toml",              PROJECT_CODEX_CONFIG)
    write("project/.gemini/GEMINI.md",               project_gemini_md(lang_note, build_cmd))
    write("project/.gemini/settings.json",           PROJECT_GEMINI_SETTINGS)
    write("project/.gemini/commands/task/plan.toml",     GEMINI_CMD_PLAN)
    write("project/.gemini/commands/code/review.toml",   GEMINI_CMD_REVIEW)
    write("project/.gemini/commands/git/commit.toml",    GEMINI_CMD_COMMIT)
    write("project/.gemini/commands/git/changelog.toml", GEMINI_CMD_CHANGELOG)
    write("project/.gemini/extensions/project/gemini-extension.json", GEMINI_EXTENSION)
    print()
    hdr("── Hooks (bash — Mac/Linux) ──────────────────────────────")
    write("project/.claude/hooks/session-start.sh",  HOOK_SESSION_START_SH,  executable=True)
    write("project/.claude/hooks/pre-bash.sh",        HOOK_PRE_BASH_SH,       executable=True)
    write("project/.claude/hooks/pre-write.sh",       HOOK_PRE_WRITE_SH,      executable=True)
    write("project/.claude/hooks/post-write.sh",      HOOK_POST_WRITE_SH,     executable=True)
    write("project/.claude/hooks/on-stop.sh",         HOOK_ON_STOP_SH,        executable=True)
    write("project/.claude/hooks/post-failure.sh",    HOOK_POST_FAILURE_SH,   executable=True)
    print()
    hdr("── Hooks (PowerShell — Windows) ──────────────────────────")
    write("project/.claude/hooks/session-start.ps1",  HOOK_SESSION_START_PS1)
    write("project/.claude/hooks/pre-bash.ps1",        HOOK_PRE_BASH_PS1)
    write("project/.claude/hooks/pre-write.ps1",       HOOK_PRE_WRITE_PS1)
    write("project/.claude/hooks/post-write.ps1",      HOOK_POST_WRITE_PS1)
    write("project/.claude/hooks/on-stop.ps1",         HOOK_ON_STOP_PS1)
    write("project/.claude/hooks/post-failure.ps1",    HOOK_POST_FAILURE_PS1)

print()
hdr("── Install scripts ──────────────────────────────────────────")
if build_global:
    write("install.sh",   INSTALL_SH,  executable=True)
    write("install.ps1",  INSTALL_PS1)
write(".gitignore-additions.txt", GITIGNORE_NOTE)

# ─────────────────────────────────────────────────────────────────────────────
# SUMMARY
# ─────────────────────────────────────────────────────────────────────────────
print()
hdr("════════════════════════════════════════════════════════")
hdr("  Done!")
hdr("════════════════════════════════════════════════════════")
print()

all_files = []
for root, dirs, files in os.walk("."):
    dirs[:] = [d for d in dirs if d not in [".git"]]
    for f in files:
        p = os.path.join(root, f).lstrip("./").lstrip(".\\")
        if p not in ["build-agentic-kit.py"]:
            all_files.append(p)

for f in sorted(all_files):
    print(f"  {f}")

print()
if build_global:
    print(b("  Mac / Linux — install global configs:"))
    print("    chmod +x install.sh && ./install.sh")
    print("    ./install.sh /path/to/your/project")
    print()
    print(b("  Windows — install global configs:"))
    print("    Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass")
    print("    .\\install.ps1")
    print("    .\\install.ps1 -ProjectPath C:\\path\\to\\repo")
    print()
if build_project and not build_global:
    print(b("  Project files are in project/"))
    print("  Copy .claude/ .codex/ .gemini/ into your repo root.")
    print("  chmod +x .claude/hooks/*.sh")
    print()
print(b("  Edit the CLAUDE.md / AGENTS.md / GEMINI.md files"))
print("  in your chosen scope to add project-specific context.")
print()
