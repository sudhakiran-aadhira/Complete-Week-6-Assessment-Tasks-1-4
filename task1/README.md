# Week 6 Assessment - Task 1
## Agent Core and Audit Trail

## Scenario

Customer 5 asks for a refund for order 1042.

The agent researches the order, checks the refund policy and attempts
to issue the refund.

Refund is a HIGH-RISK operation, therefore human approval is required.

## Tools

The tool registry contains 5 tools:

1. get_order(order_id)
2. get_customer(customer_id)
3. check_policy(order_id)
4. draft_email(customer_id, text)
5. issue_refund(order_id, amount)

## Risk Levels

| Tool | Risk |
|---|---|
| get_order | LOW |
| get_customer | LOW |
| check_policy | LOW |
| draft_email | MEDIUM |
| issue_refund | HIGH |

## Agent Loop

The agent supports a maximum of 8 iterations.

The agent stops when:

- A final answer is generated
- A terminal tool signal is returned
- Maximum iterations are reached

## Audit Trail

Every agent step is stored in `audit.jsonl`.

Schema:

{
    "run_id": "...",
    "timestamp": "...",
    "step": 1,
    "thought": "...",
    "action": "...",
    "action_input": "...",
    "observation": "...",
    "tokens": 10
}

Email addresses are masked in the audit trail.

## Run

From the task1 folder:

python agent.py

## Expected Output

Step 1: get_order(1042)

Step 2: check_policy(1042) -> eligible

Step 3: issue_refund -> PENDING APPROVAL

Final answer:

Refund of $99.99 for order 1042 is pending human approval.

## Tests

Run:

pytest -v test_task1.py