
import pytest

from app import create_app


@pytest.fixture
def client(tmp_path):
    db_path = tmp_path / "test_task3.db"

    app = create_app(db_path)
    app.config["TESTING"] = True

    return app.test_client()


def start_refund(client, user_id="user1"):
    return client.post(
        "/run",
        json={
            "user_id": user_id,
            "message": "Please check and refund order 1042",
        },
    )


def test_refund_waits_for_approval(client):
    response = start_refund(client)

    assert response.status_code == 202

    data = response.get_json()
    assert data["status"] == "WAITING_APPROVAL"

    pending = client.get("/pending-actions").get_json()
    assert len(pending) == 1
    assert pending[0]["status"] == "PENDING"


def test_approve_executes_refund(client):
    response = start_refund(client)
    action_id = response.get_json()["pending_action_id"]

    approval = client.post(
        f"/pending-actions/{action_id}/approve"
    )

    assert approval.status_code == 200

    data = approval.get_json()
    assert data["status"] == "APPROVED"
    assert data["agent_status"] == "COMPLETED"
    assert data["action_result"]["status"] == "EXECUTED"


def test_reject_does_not_issue_refund(client):
    response = start_refund(client)
    action_id = response.get_json()["pending_action_id"]

    rejection = client.post(
        f"/pending-actions/{action_id}/reject"
    )

    assert rejection.status_code == 200
    assert rejection.get_json()["status"] == "REJECTED"
    assert "Refund not issued" in rejection.get_json()["message"]


def test_prompt_injection_is_ignored(client):
    response = start_refund(client)

    data = response.get_json()

    assert response.status_code == 202
    assert data["injection_note"] == "Ignored - untrusted order data"
    assert data["status"] == "WAITING_APPROVAL"


def test_input_guard_blocks_out_of_scope(client):
    response = client.post(
        "/run",
        json={
            "user_id": "guard_user",
            "message": "Tell me a joke",
        },
    )

    assert response.status_code == 400
    assert response.get_json()["status"] == "BLOCKED"


def test_input_guard_blocks_pii(client):
    response = client.post(
        "/run",
        json={
            "user_id": "pii_user",
            "message": "Refund order 1042 using test@example.com",
        },
    )

    assert response.status_code == 400
    assert "PII" in response.get_json()["message"]


def test_output_guard_blocks_card_number():
    from app import output_guard

    valid, message = output_guard(
        "Your card number is 4111111111111111"
    )

    assert valid is False
    assert "card number" in message


def test_output_guard_blocks_unsupported_claim():
    from app import output_guard

    valid, message = output_guard(
        "Refund issued successfully"
    )

    assert valid is False
    assert "unsupported claim" in message


def test_rate_limit_allows_five_and_blocks_sixth(client):
    for number in range(1, 6):
        response = start_refund(client, user_id="limit_user")
        assert response.status_code == 202

    sixth = start_refund(client, user_id="limit_user")

    assert sixth.status_code == 429
    assert "Rate limit exceeded" in sixth.get_json()["error"]


def test_write_tool_executes_and_notifies(client):
    response = client.post(
        "/run",
        json={
            "user_id": "write_user",
            "message": "Please draft an email for order 1042",
        },
    )

    assert response.status_code == 200
    assert response.get_json()["status"] == "COMPLETED"
    assert response.get_json()["write_result"]["status"] == "DRAFTED"


def test_action_cannot_be_approved_twice(client):
    response = start_refund(client)
    action_id = response.get_json()["pending_action_id"]

    first = client.post(
        f"/pending-actions/{action_id}/approve"
    )
    second = client.post(
        f"/pending-actions/{action_id}/approve"
    )

    assert first.status_code == 200
    assert second.status_code == 409