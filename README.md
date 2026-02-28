# 🤖 Agentic Starter Toolkit

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python: 3.6+](https://img.shields.io/badge/Python-3.6+-blue.svg)](https://www.python.org/downloads/)
[![Platform: Cross-Platform](https://img.shields.io/badge/Platform-macOS%20%7C%20Linux%20%7C%20Windows-lightgrey.svg)](#)

The **Agentic Starter Toolkit** provides instant, battle-tested, and token-optimized configurations for the next generation of AI coding agents. Stop wasting your context window and API credits on redundant logs, boilerplate, or unsafe operations.

---

## 🎯 Purpose

AI coding agents (Claude Code, Codex CLI, Gemini CLI) are powerful but can be expensive and noisy if not configured correctly. This toolkit automates the setup of:

*   **Token Optimization:** Aggressive context compression and tool-output limits.
*   **Safety Guards:** Pre-bash and pre-write hooks that block destructive commands (e.g., `rm -rf /`) and protect secrets.
*   **Continuous Validation:** Automated linting and building on every file save, providing immediate feedback to the agent.
*   **High-Signal Context:** Standardized `GEMINI.md`, `CLAUDE.md`, and `AGENTS.md` files to keep the AI focused on your project's architecture and stack.

---

## ✨ Features

### 🚀 Optimized Performance
- **Quota Management:** Pre-configured `MAX_THINKING_TOKENS` and tool budgets to prevent runaway costs.
- **Context Compression:** Forces Gemini and Claude to summarize long tool outputs.

### 🛡️ Safety & Security
- **Command Blocking:** Automatically prevents agents from executing dangerous shell patterns.
- **Secret Protection:** Blocks writes to `.env`, `.pem`, and other sensitive files.
- **Lockfile Integrity:** Prevents agents from manually editing `package-lock.json` or `Cargo.lock`.

### 🛠️ Developer Experience
- **Custom Slash Commands:** Adds `/task:plan`, `/code:review`, and `/git:commit` to your terminal.
- **Unified Hooks:** Bash and PowerShell scripts that work across macOS, Linux, and Windows.
- **Zero-Config Build:** Automatically detects your stack (C++, Rust, Go, TS, Python, etc.) and configures the appropriate build commands.

---

## 🛠️ Quick Start

### 1. Build your configuration
Run the interactive builder. It will ask for your scope (Global/Project), preferred languages, and build systems.

```bash
python3 build-agentic-kit.py
```

### 2. Install
The builder generates platform-specific installers.

**macOS / Linux:**
```bash
./install.sh                      # Install global defaults
./install.sh /path/to/your/repo   # Install project-specific hooks/rules
```

**Windows (PowerShell):**
```powershell
.\install.ps1 -ProjectPath C:\path\to\repo
```

---

## 📂 Architecture

The toolkit organizes configuration into two distinct scopes:

| Scope | Location | Usage |
| :--- | :--- | :--- |
| **Global** | `~/.claude`, `~/.codex`, `~/.gemini` | Machine-wide defaults, core safety rules, and universal slash commands. |
| **Project** | `<repo_root>/.claude`, etc. | Per-repo stack definitions, custom build commands, and local conventions. |

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

### Supported Languages (Auto-detected Hooks)
- **Systems:** C++, Rust, Go, Zig
- **Web:** TypeScript, JavaScript (Node.js)
- **Mobile:** Swift, Kotlin, Dart/Flutter
- **Backend:** Python, PHP, Ruby, Java, Elixir, Scala, Haskell

---

## 🤝 Contributing

Contributions are welcome! If you have a better hook for a specific language or a new safety pattern, please open a PR.

1.  Fork the repo.
2.  Create your feature branch.
3.  Commit your changes.
4.  Push to the branch.
5.  Create a new Pull Request.

---

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
