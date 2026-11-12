"""
Task 1 tests
"""

import json

from tool_registry import (
    TOOL_REGISTRY,
    get_order,
    get_customer,
    check_policy,
    draft_email,
    issue_refund
)

from audit import (
    clear_audit_log,
    log_step,
    get_run
)


def test_five_tools_exist():

    expected_tools = {
        "get_order",
        "get_customer",
        "check_policy",
        "draft_email",
        "issue_refund"
    }

    assert set(TOOL_REGISTRY.keys()) == expected_tools


def test_risk_levels():

    assert TOOL_REGISTRY["get_order"]["risk_level"] == "LOW"

    assert TOOL_REGISTRY["get_customer"]["risk_level"] == "LOW"

    assert TOOL_REGISTRY["check_policy"]["risk_level"] == "LOW"

    assert TOOL_REGISTRY["draft_email"]["risk_level"] == "MEDIUM"

    assert TOOL_REGISTRY["issue_refund"]["risk_level"] == "HIGH"


def test_get_order():

    result = get_order(1042)

    assert result["success"] is True

    assert result["order"]["customer_id"] == 5

    assert result["order"]["amount"] == 99.99


def test_get_customer():

    result = get_customer(5)

    assert result["success"] is True

    assert result["customer"]["email"] == "john.smith@example.com"


def test_check_policy():

    result = check_policy(1042)

    assert result["success"] is True

    assert result["eligible"] is True


def test_draft_email():

    result = draft_email(
        5,
        "Your refund is pending approval."
    )

    assert result["success"] is True

    assert result["status"] == "DRAFT"


def test_refund_requires_approval():

    result = issue_refund(
        1042,
        99.99
    )

    assert result["success"] is True

    assert result["status"] == "PENDING APPROVAL"


def test_audit_email_masking():

    clear_audit_log()

    log_step(
        run_id="test-run",
        step=1,
        thought="Testing email masking",
        action="test",
        action_input={
            "email": "john.smith@example.com"
        },
        observation={
            "email": "john.smith@example.com"
        },
        tokens=10
    )

    records = get_run("test-run")

    assert len(records) == 1

    record = records[0]

    assert "john.smith@example.com" not in str(record)

    assert "j***@example.com" in str(record)


def test_audit_schema():

    clear_audit_log()

    log_step(
        run_id="schema-test",
        step=1,
        thought="test",
        action="get_order",
        action_input={"order_id": 1042},
        observation={"success": True},
        tokens=5
    )

    records = get_run("schema-test")

    record = records[0]

    required_fields = {
        "run_id",
        "timestamp",
        "step",
        "thought",
        "action",
        "action_input",
        "observation",
        "tokens"
    }

    assert required_fields.issubset(record.keys())