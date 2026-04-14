#!/usr/bin/env bash
set -euo pipefail

cat <<'EOF'
HOOK POLICY ACTIVE
- Read BOUNDARY.md before changing project rules or runtime state.
- Treat governance/hooks.policy.md as the project-level hook truth source.
- Treat governance/files.registry.json and governance/intent.routes.json as registry and route truth.
- Hooks are guardrails and audit helpers, not approval authority.
EOF
