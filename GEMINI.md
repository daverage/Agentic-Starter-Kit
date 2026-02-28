# Agentic Coding Tools — Starter Kit

This project is a utility for generating and deploying optimized configurations for AI coding assistants, specifically **Claude Code**, **Codex CLI**, and **Gemini CLI**. It focuses on reducing token usage and managing quotas through strategic settings and instructional context.

## Project Overview
- **Purpose**: Automate the setup of "agent-friendly" environments with pre-configured rules, hooks, and slash commands.
- **Architecture**:
    - `build-agentic-kit.py`: An interactive Python script that generates custom configurations based on the user's primary programming languages and build systems.
    - `global/`: Template directory for machine-wide configurations (e.g., `~/.claude/`, `~/.gemini/`).
    - `project/`: Template directory for repository-specific configurations, including pre-commit hooks and CI-like validation scripts.
    - `install.sh` / `install.ps1`: Platform-specific scripts to deploy the generated files to the appropriate locations.

## Building and Running
- **Generate Configuration**:
  ```bash
  python3 build-agentic-kit.py
  ```
  *This will prompt for scope (global/project), languages, and build systems.*

- **Install Global Files (Mac/Linux)**:
  ```bash
  ./install.sh
  ```

- **Install to a Specific Project**:
  ```bash
  ./install.sh /path/to/your/repo
  ```

- **Install (Windows PowerShell)**:
  ```powershell
  .\install.ps1 -ProjectPath C:\path\to\repo
  ```

## Key Components
- **Rules (`GEMINI.md`, `CLAUDE.md`, `AGENTS.md`)**: Provide high-level instructions to the AI models to ensure concise, high-signal interactions.
- **Hooks**: Located in `project/.claude/hooks/`, these scripts automate tasks like git state reporting, dangerous command blocking, and post-write linting/building.
- **Slash Commands**: Pre-configured for Gemini CLI (e.g., `/task:plan`, `/code:review`, `/git:commit`) to streamline common developer workflows.

## Development Conventions
- **Lean Context**: Always prioritize minimal token usage. Project rules should be specific and not duplicate global rules.
- **Safety First**: Use the provided `pre-bash` and `pre-write` hooks to prevent the AI from modifying sensitive files or executing destructive commands.
- **Validation**: Every change should be verified using the project's native build and linting tools, which are integrated into the `post-write` hooks.
