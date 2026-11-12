"""
Task 1 - Audit Logging
"""

import json
import re
from datetime import datetime
from pathlib import Path


AUDIT_FILE = Path(__file__).parent / "audit.jsonl"


def mask_emails(value):
    """
    Mask email addresses.

    Example:
    john.smith@example.com
    becomes:
    j***@example.com
    """

    if isinstance(value, dict):
        return {
            key: mask_emails(val)
            for key, val in value.items()
        }

    if isinstance(value, list):
        return [mask_emails(item) for item in value]

    if isinstance(value, str):

        pattern = r"([A-Za-z0-9._%+-])[A-Za-z0-9._%+-]*@([A-Za-z0-9.-]+\.[A-Za-z]{2,})"

        return re.sub(
            pattern,
            r"\1***@\2",
            value
        )

    return value


def log_step(
    run_id,
    step,
    thought,
    action,
    action_input,
    observation,
    tokens
):
    """Write one audit step to JSONL."""

    record = {
        "run_id": run_id,
        "timestamp": datetime.now().isoformat(),
        "step": step,
        "thought": thought,
        "action": action,
        "action_input": mask_emails(action_input),
        "observation": mask_emails(observation),
        "tokens": tokens
    }

    with open(AUDIT_FILE, "a", encoding="utf-8") as file:
        file.write(json.dumps(record) + "\n")


def clear_audit_log():
    """Clear old audit records."""

    if AUDIT_FILE.exists():
        AUDIT_FILE.unlink()


def get_run(run_id):
    """Return all audit records for a run."""

    records = []

    if not AUDIT_FILE.exists():
        return records

    with open(AUDIT_FILE, "r", encoding="utf-8") as file:

        for line in file:

            if line.strip():

                record = json.loads(line)

                if record["run_id"] == run_id:
                    records.append(record)

    return records


def print_audit_trail(run_id):
    """Print the complete audit trail."""

    records = get_run(run_id)

    print("\n" + "=" * 70)
    print("FULL AUDIT TRAIL")
    print("=" * 70)

    for record in records:

        print(f"\nStep {record['step']}")
        print(f"Run ID: {record['run_id']}")
        print(f"Timestamp: {record['timestamp']}")
        print(f"Thought: {record['thought']}")
        print(f"Action: {record['action']}")
        print(f"Action Input: {record['action_input']}")
        print(f"Observation: {record['observation']}")
        print(f"Tokens: {record['tokens']}")

    print("\n" + "=" * 70)