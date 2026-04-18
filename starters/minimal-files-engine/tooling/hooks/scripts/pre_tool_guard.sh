#!/usr/bin/env bash
set -euo pipefail

INPUT="$(cat)"

repo_root() {
  git rev-parse --show-toplevel 2>/dev/null || pwd
}

redact() {
  sed -E 's/gh[pous]_[A-Za-z0-9]{20,}/[REDACTED_TOKEN]/g' \
    | sed -E 's/Bearer [A-Za-z0-9._-]+/Bearer [REDACTED]/g' \
    | sed -E 's/--password[= ][^ ]+/--password=[REDACTED]/g' \
    | sed -E 's/--token[= ][^ ]+/--token=[REDACTED]/g'
}

extract_tool_name() {
  printf '%s' "$INPUT" | jq -r '.tool_name // .toolName // empty' 2>/dev/null || true
}

extract_command() {
  printf '%s' "$INPUT" | jq -r '
    if (.tool_input? and (.tool_input.command? // "") != "") then
      .tool_input.command
    elif (.toolArgs? // empty) != "" then
      if (.toolArgs | type) == "string" then
        ((.toolArgs | fromjson? // {}) | .command? // "")
      elif (.toolArgs | type) == "object" then
        .toolArgs.command? // ""
      else
        ""
      end
    else
      ""
    end
  ' 2>/dev/null || true
}

log_event() {
  local event="$1"
  local reason="${2:-}"
  local root log_dir redacted_cmd

  root="$(repo_root)"
  log_dir="$root/tooling/hooks/logs"
  mkdir -p "$log_dir"

  redacted_cmd="$(printf '%s' "$COMMAND" | redact)"

  jq -cn \
    --arg event "$event" \
    --arg tool "$TOOL_NAME" \
    --arg command "$redacted_cmd" \
    --arg reason "$reason" \
    '{event:$event, tool:$tool, command:$command, reason:$reason}' \
    >> "$log_dir/audit.jsonl"
}

deny() {
  local reason="$1"
  log_event "policyDeny" "$reason"

  if printf '%s' "$INPUT" | jq -e '.toolArgs?' >/dev/null 2>&1; then
    jq -cn --arg r "$reason" '{permissionDecision:"deny", permissionDecisionReason:$r}'
    exit 0
  fi

  printf '%s\n' "$reason" >&2
  exit 2
}

TOOL_NAME="$(extract_tool_name)"
COMMAND="$(extract_command)"
LOWER_TOOL_NAME="$(printf '%s' "$TOOL_NAME" | tr '[:upper:]' '[:lower:]')"

case "$LOWER_TOOL_NAME" in
  ""|bash)
    ;;
  *)
    exit 0
    ;;
esac

log_event "preToolUse"

if printf '%s' "$COMMAND" | grep -Eqi '\b(sudo|su|runas)\b'; then
  deny "Privilege escalation requires manual approval."
fi

if printf '%s' "$COMMAND" | grep -Eq 'rm[[:space:]]+-rf[[:space:]]+/([[:space:]]|$)|rm[[:space:]].*-rf[[:space:]]+/([[:space:]]|$)'; then
  deny "Destructive operations targeting the filesystem root require manual approval."
fi

if printf '%s' "$COMMAND" | grep -Eqi '\b(mkfs|dd|format)\b'; then
  deny "System-level destructive operations are not allowed via automated execution."
fi

if printf '%s' "$COMMAND" | grep -Eqi 'curl.*\|[[:space:]]*(bash|sh)|wget.*\|[[:space:]]*(bash|sh)'; then
  deny "Download-and-execute patterns require manual approval."
fi

exit 0
