# Lasso Agent

## What this is
A minimal AI agent: the user gives it a CSV file and a target column, it calls a Python tool that fits a Lasso regression, then explains how well it predicts and which variables it used. Users are business executives and investors without a coding background: clarity beats cleverness.

## Folder layout
- context/ — background papers (as Markdown) and project_brief.md
- data/ — datasets (CSV)
- src/tools.py — the ML functions the agent can call
- src/agent.py — the agent loop that talks to the Claude API
- src/system_prompt.md — the agent's instructions
- outputs/ — results the agent saves

## Tech
- Python in .venv (always use it)
- Libraries: anthropic, scikit-learn, pandas. Ask before adding others.
- The API key comes from the ANTHROPIC_API_KEY environment variable. Never write keys in code.
- Model for the agent: claude-sonnet-5-5

## Rules for code
- Short files with clear comments, easy to read for someone new to Python.
- Plain functions, no classes.
- Tool functions return a plain dictionary that can be converted to JSON.
- Test each piece on its own before connecting it to the agent.