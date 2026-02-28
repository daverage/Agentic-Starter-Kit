# 🤖 Agentic Starter Toolkit

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python: 3.6+](https://img.shields.io/badge/Python-3.6+-blue.svg)](https://www.python.org/downloads/)
[![Platform: Cross-Platform](https://img.shields.io/badge/Platform-macOS%20%7C%20Linux%20%7C%20Windows-lightgrey.svg)](#)

The **Agentic Starter Toolkit** generates starter configs for **Claude Code**, **Codex CLI**, and **Gemini CLI** with a global scope (`~/.<agent>/...`) and/or project scope (`<repo>/.<agent>/...`).

---

## 🎯 Purpose

AI coding agents are powerful but can be expensive and noisy if not configured carefully. This toolkit generates:

*   **Agent-specific settings:** Config files for each supported agent.
*   **Claude project hooks:** `SessionStart`, `PreToolUse`, `PostToolUse`, `PostToolUseFailure`, and `Stop` hooks for shell/write safety and post-write checks.
*   **Context docs:** `CLAUDE.md`, `AGENTS.md`, and `GEMINI.md` templates with stack/build placeholders.
*   **Gemini command templates:** `/task:plan`, `/code:review`, `/git:commit`, `/git:changelog` (Gemini CLI command files under `.gemini/commands`).

---

## ✨ Features

### Claude Code
- **Global:** writes `~/.claude` templates (`settings.json`, `CLAUDE.md`) via installer.
- **Project:** writes `.claude/settings.json`, `.claude/settings.windows.json`, `.claude/CLAUDE.md`, and Bash/PowerShell hook scripts.
- **Safety controls:** deny rules in Claude settings plus pre-bash/pre-write hook checks.
- **Validation hooks:** post-write hooks run language-aware checks when matching tools are installed.

### Codex CLI
- **Global:** writes `~/.codex/config.toml` and `~/.codex/AGENTS.md` via installer.
- **Project:** writes `.codex/config.toml` and `.codex/AGENTS.md`.
- **Scope:** this kit provides config/context templates only for Codex (no Codex hook scripts are generated).

### Gemini CLI
- **Global:** writes `~/.gemini/settings.json`, `~/.gemini/GEMINI.md`, and `.gemini/commands/*` via installer.
- **Project:** writes `.gemini/settings.json`, `.gemini/GEMINI.md`, `.gemini/commands/*`, and a project extension file.
- **Commands provided:** `/task:plan`, `/code:review`, `/git:commit`, `/git:changelog` (Gemini command files, not universal terminal commands).

---

## 🛠️ Quick Start

### 1. Build your configuration
Run the interactive builder. It will ask for your scope (Global/Project), preferred languages, and build systems.

```bash
python3 build-agentic-kit.py
```

### 2. Install
If you selected **Global** or **Both**, the builder generates platform-specific installers (`install.sh`, `install.ps1`).

**macOS / Linux:**
```bash
./install.sh                      # Install global defaults
./install.sh /path/to/your/repo   # Install project-specific agent files
```

**Windows (PowerShell):**
```powershell
.\install.ps1 -ProjectPath C:\path\to\repo
```

If you selected **Project only**, copy `project/.claude`, `project/.codex`, and `project/.gemini` into your repo root manually.

---

## 📂 Architecture

The toolkit organizes configuration into two distinct scopes:

| Scope | Location | Usage |
| :--- | :--- | :--- |
| **Global** | `~/.claude`, `~/.codex`, `~/.gemini` | Machine-wide defaults and context/config templates per agent. |
| **Project** | `<repo_root>/.claude`, etc. | Per-repo overrides, Claude hooks, and Gemini project commands/context. |

### Directory Structure
```text
.
├── build-agentic-kit.py   # The interactive generator
├── install.sh / .ps1      # Deployment scripts
├── global/                # Machine-wide templates
└── project/               # Repository-scoped templates
    └── .claude/hooks/     # Safety and validation scripts
```

---

## 💻 Supported Tools & Stacks

### Supported Agents
- **Claude Code** (`.claude/`)
- **Codex CLI** (`.codex/`)
- **Gemini CLI** (`.gemini/`)

### Supported Languages (Auto-detected Claude post-write hooks)
- **Systems:** C++, Rust, Go, Zig
- **Web:** TypeScript, JavaScript (Node.js)
- **Mobile:** Swift, Kotlin, Dart/Flutter
- **Backend:** Python, PHP, Ruby, Java, Elixir, Scala, Haskell

---

## 🤝 Contributing

Contributions are welcome. Improvements to hooks, templates, or agent-specific defaults are all useful.

1.  Fork the repo.
2.  Create your feature branch.
3.  Commit your changes.
4.  Push to the branch.
5.  Create a new Pull Request.

---

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
