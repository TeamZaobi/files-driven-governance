#!/usr/bin/env python3
import json
import sys


def main() -> int:
    _ = sys.stdin.read()
    payload = {
        "overall_status": "pass",
        "summary": "mock cli observed enough evidence in the supplied replay bundle",
        "assertions": [
            {
                "category": "route",
                "status": "pass",
                "actual": "observed replay bundle contains a replay-oriented flow",
                "evidence_turn_ids": ["turn-1", "turn-2", "turn-3"],
            },
            {
                "category": "read",
                "status": "pass",
                "actual": "observed bundle references the declared replay artifact and run metadata",
                "evidence_turn_ids": ["turn-2", "turn-3"],
            },
            {
                "category": "write",
                "status": "pass",
                "actual": "observed diff remains limited to replay outputs",
                "evidence_turn_ids": ["turn-3"],
            },
            {
                "category": "boundary",
                "status": "pass",
                "actual": "scope context remains explicit in the observed bundle",
                "evidence_turn_ids": ["turn-2", "turn-3"],
            },
            {
                "category": "projection",
                "status": "pass",
                "actual": "workspace diff shows derived projection handling only",
                "evidence_turn_ids": ["turn-3"],
            },
            {
                "category": "recovery",
                "status": "pass",
                "actual": "observed run metadata and replay artifact remain replayable after reopen",
                "evidence_turn_ids": ["turn-3"],
            },
            {
                "category": "trajectory",
                "status": "pass",
                "actual": "ordered replay transcript remains intact",
                "evidence_turn_ids": ["turn-1", "turn-2", "turn-3"],
            },
        ],
    }
    envelope = {
        "type": "result",
        "subtype": "success",
        "is_error": False,
        "duration_ms": 1,
        "duration_api_ms": 1,
        "num_turns": 1,
        "result": json.dumps(payload, ensure_ascii=False),
        "stop_reason": "end_turn",
        "session_id": "mock-session",
        "total_cost_usd": 0.0,
        "usage": {"input_tokens": 0, "output_tokens": 0},
        "modelUsage": {},
        "permission_denials": [],
        "terminal_reason": "completed",
        "fast_mode_state": "off",
        "uuid": "mock-uuid",
    }
    print(json.dumps(envelope, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
