#!/usr/bin/env bash
set -euo pipefail

INPUT="$(cat)"
ROOT="$(git rev-parse --show-toplevel 2>/dev/null || pwd)"
LOG_DIR="$ROOT/tooling/hooks/logs"

mkdir -p "$LOG_DIR"

TIMESTAMP="$(printf '%s' "$INPUT" | jq -r '.timestamp // empty' 2>/dev/null || true)"
CWD_VALUE="$(printf '%s' "$INPUT" | jq -r '.cwd // empty' 2>/dev/null || true)"
PROMPT_VALUE="$(printf '%s' "$INPUT" | jq -r '.prompt // empty' 2>/dev/null || true)"
PROMPT_CHARS="$(printf '%s' "$PROMPT_VALUE" | wc -m | tr -d ' ')"

jq -cn \
  --arg event "userPromptSubmitted" \
  --arg ts "$TIMESTAMP" \
  --arg cwd "$CWD_VALUE" \
  --arg chars "$PROMPT_CHARS" \
  '{event:$event, timestamp:$ts, cwd:$cwd, prompt_chars:$chars}' \
  >> "$LOG_DIR/audit.jsonl"

exit 0
