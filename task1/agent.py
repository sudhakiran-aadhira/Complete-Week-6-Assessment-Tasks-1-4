"""
Task 1 - Customer Refund Agent

Maximum 8 iterations.
Stops when:
1. Final answer is reached
2. A terminal tool signal is returned
3. Maximum iterations are reached
"""

import uuid

from tool_registry import TOOL_REGISTRY, execute_tool
from audit import (
    clear_audit_log,
    log_step,
    print_audit_trail
)


MAX_ITERATIONS = 8


def estimate_tokens(thought, action, observation):
    """
    Simple token estimation for assessment purposes.

    This is not an actual LLM token counter.
    """

    text = f"{thought} {action} {observation}"

    return max(1, len(text.split()))


def run_agent(user_request: str):

    run_id = str(uuid.uuid4())

    print("\n" + "=" * 70)
    print("CUSTOMER REFUND AGENT")
    print("=" * 70)

    print(f"Request: {user_request}")
    print(f"Run ID: {run_id}")

    # -----------------------------------------------------
    # Step 1 - Get order
    # -----------------------------------------------------

    step = 1

    thought = (
        "The customer is requesting a refund. "
        "First I need to retrieve the order details."
    )

    action = "get_order"

    action_input = {
        "order_id": 1042
    }

    observation = execute_tool(
        action,
        action_input
    )

    print(f"\nStep {step}: get_order(1042)")

    log_step(
        run_id=run_id,
        step=step,
        thought=thought,
        action=action,
        action_input=action_input,
        observation=observation,
        tokens=estimate_tokens(
            thought,
            action,
            observation
        )
    )

    if not observation.get("success"):
        final_answer = "Unable to find the order."
        print(final_answer)
        print_audit_trail(run_id)
        return

    order = observation["order"]

    order_amount = order["amount"]

    # -----------------------------------------------------
    # Step 2 - Check refund policy
    # -----------------------------------------------------

    step += 1

    thought = (
        "I found the order. "
        "Before issuing a refund, I need to check the refund policy."
    )

    action = "check_policy"

    action_input = {
        "order_id": 1042
    }

    observation = execute_tool(
        action,
        action_input
    )

    print(
        f"Step {step}: check_policy(1042) "
        f"-> {'eligible' if observation.get('eligible') else 'not eligible'}"
    )

    log_step(
        run_id=run_id,
        step=step,
        thought=thought,
        action=action,
        action_input=action_input,
        observation=observation,
        tokens=estimate_tokens(
            thought,
            action,
            observation
        )
    )

    if not observation.get("eligible"):

        final_answer = "Refund is not eligible according to policy."

        print(f"\nFinal answer: {final_answer}")

        print_audit_trail(run_id)

        return

    # -----------------------------------------------------
    # Step 3 - Issue refund
    # -----------------------------------------------------

    step += 1

    thought = (
        "The order is eligible for a refund. "
        "Issuing a refund is a HIGH-RISK action, "
        "so human approval is required."
    )

    action = "issue_refund"

    action_input = {
        "order_id": 1042,
        "amount": order_amount
    }

    # Check risk level from registry
    risk_level = TOOL_REGISTRY[action]["risk_level"]

    if risk_level == "HIGH":

        observation = {
            "success": True,
            "status": "PENDING APPROVAL",
            "order_id": 1042,
            "amount": order_amount,
            "message": "Human approval required before refund is issued"
        }

    else:

        observation = execute_tool(
            action,
            action_input
        )

    print(
        f"Step {step}: issue_refund "
        f"-> {observation['status']}"
    )

    log_step(
        run_id=run_id,
        step=step,
        thought=thought,
        action=action,
        action_input=action_input,
        observation=observation,
        tokens=estimate_tokens(
            thought,
            action,
            observation
        )
    )

    # -----------------------------------------------------
    # Terminal tool signal
    # -----------------------------------------------------

    if observation.get("status") == "PENDING APPROVAL":

        final_answer = (
            f"Refund of ${order_amount:.2f} for order 1042 "
            "is pending human approval."
        )

        print(f"\nFinal answer: {final_answer}")

        print_audit_trail(run_id)

        return

    # -----------------------------------------------------
    # Safety fallback
    # -----------------------------------------------------

    final_answer = "Agent completed without a final result."

    print(f"\nFinal answer: {final_answer}")

    print_audit_trail(run_id)


if __name__ == "__main__":

    clear_audit_log()

    request = "Customer 5 asks for a refund for order 1042"

    run_agent(request)