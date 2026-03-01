# Global AGENTS.md
# Read by Codex CLI and any tool honouring the Linux Foundation AGENTS.md standard.
# Project rules go in <project>/.codex/AGENTS.md — do not duplicate here.
# Keep lean: every token here costs quota on every turn.

## Core Rules
- Simplicity first. Touch minimal code. Find root causes, not workarounds.
- Never mark done without proving it works (tests, logs, diff).
- For non-trivial changes: pause and ask if there is a more elegant solution.
- Bug reports: fix autonomously. No hand-holding needed.

## Context Management
- Use /clear between unrelated tasks. Do not carry stale context.
- Read only the specific files needed. Never explore broadly unless asked.

## Planning
- Non-trivial tasks (3+ steps): write a brief plan to `tasks/todo.md` first, then check in.
- If something goes sideways, stop and re-plan. Do not push through.
- Simple or obvious fixes: skip planning overhead entirely.

## Subagents
- Use only when genuine parallelism is needed, not by default.
- One focused task per subagent. Keep spawn prompts minimal.
- Clean up subagents when done. Idle ones still consume tokens.

## Lessons
- After any user correction, append one concise rule to `tasks/lessons.md`.
- Keep lessons under 30 entries. Prune redundant ones.
- Load lessons only when starting work on a relevant project, not by default.

## Git
- Never commit without being asked.
- Never force-push to main, master, production, or release branches.
