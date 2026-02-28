# Global Claude Code Rules
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
