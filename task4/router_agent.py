
"""
Week 6 Assessment - Task 4
Router and Multi-Agent Design
"""

from concurrent.futures import ThreadPoolExecutor


# ------------------------------------------------
# 1. Specialist Agents
# ------------------------------------------------

def refund_agent(request):
    """Handles refund-related requests."""
    return {
        "agent": "refund",
        "response": f"Refund specialist is handling: {request}"
    }


def order_status_agent(request):
    """Handles order tracking requests."""
    return {
        "agent": "order-status",
        "response": f"Order status specialist is handling: {request}"
    }


def general_info_agent(request):
    """Handles general information requests."""
    return {
        "agent": "general-info",
        "response": f"General information specialist is handling: {request}"
    }


# ------------------------------------------------
# 2. Router
# ------------------------------------------------

def route_request(request):
    """Routes requests to the correct specialist agent."""

    text = request.lower()

    refund_keywords = [
        "refund", "money back", "return", "reimbursement"
    ]

    order_keywords = [
        "track", "tracking", "delivery", "shipment",
        "order status", "where is my order"
    ]

    if any(word in text for word in refund_keywords):
        return "refund"

    elif any(word in text for word in order_keywords):
        return "order-status"

    else:
        return "general-info"


# ------------------------------------------------
# 3. Router Execution
# ------------------------------------------------

def run_router(request):

    selected_agent = route_request(request)

    agents = {
        "refund": refund_agent,
        "order-status": order_status_agent,
        "general-info": general_info_agent
    }

    result = agents[selected_agent](request)

    return result


# ------------------------------------------------
# 4. Test 9 Requests (3 per category)
# ------------------------------------------------

TEST_REQUESTS = [
    # Refund requests
    ("I want a refund for my order", "refund"),
    ("Please return my payment", "refund"),
    ("I need my money back", "refund"),

    # Order status requests
    ("Track my order", "order-status"),
    ("When will my delivery arrive?", "order-status"),
    ("What is my order status?", "order-status"),

    # General information requests
    ("What are your business hours?", "general-info"),
    ("How can I contact customer support?", "general-info"),
    ("Tell me about your company", "general-info")
]


def evaluate_routing():

    correct = 0
    total = len(TEST_REQUESTS)

    print("\nROUTING TEST RESULTS")
    print("-" * 60)

    for request, expected in TEST_REQUESTS:

        actual = route_request(request)

        status = "PASS" if actual == expected else "FAIL"

        if actual == expected:
            correct += 1

        print(f"Request: {request}")
        print(f"Expected: {expected}")
        print(f"Actual:   {actual}")
        print(f"Result:   {status}")
        print("-" * 60)

    accuracy = (correct / total) * 100

    print(f"Correct routes: {correct}/{total}")
    print(f"Routing Accuracy: {accuracy:.2f}%")

    return correct, total, accuracy


# ------------------------------------------------
# 5. Orchestrator and Sub-Agent Design
# ------------------------------------------------

def explain_architecture():

    explanation = [
        "1. The orchestrator receives and understands the user request.",
        "2. It breaks complex requests into smaller independent tasks.",
        "3. The router selects the correct specialist sub-agent.",
        "4. Each sub-agent performs its assigned task independently.",
        "5. The orchestrator combines the results into one response.",
        "6. This design is useful for complex tasks needing parallel work."
    ]

    print("\nORCHESTRATOR AND SUB-AGENT DESIGN")
    print("-" * 60)

    for line in explanation:
        print(line)


# ------------------------------------------------
# 6. Parallel Independent Sub-Tasks
# ------------------------------------------------

def check_return_window():
    return "Return window: 30 days from delivery."


def check_payment_status():
    return "Payment status: Payment completed successfully."


def run_parallel_tasks():

    print("\nPARALLEL SUB-TASK EXECUTION")
    print("-" * 60)

    # Run two independent tasks at the same time.
    with ThreadPoolExecutor(max_workers=2) as executor:

        future_return = executor.submit(check_return_window)
        future_payment = executor.submit(check_payment_status)

        return_result = future_return.result()
        payment_result = future_payment.result()

    # Aggregate both results into one answer.
    final_answer = (
        "Customer Support Summary:\n"
        + return_result
        + "\n"
        + payment_result
    )

    print(final_answer)

    return final_answer


# ------------------------------------------------
# 7. Main Program
# ------------------------------------------------

def main():

    print("=" * 60)
    print("WEEK 6 ASSESSMENT - TASK 4")
    print("ROUTER AND MULTI-AGENT DESIGN")
    print("=" * 60)

    # Run routing evaluation
    correct, total, accuracy = evaluate_routing()

    # Explain architecture
    explain_architecture()

    # Run parallel tasks and aggregate results
    final_answer = run_parallel_tasks()

    print("\nFINAL ASSESSMENT SUMMARY")
    print("-" * 60)
    print(f"Routing Accuracy: {correct}/{total}")
    print(f"Accuracy Percentage: {accuracy:.2f}%")
    print("Parallel Execution: Completed")
    print("Result Aggregation: Completed")

    return accuracy


if __name__ == "__main__":
    main()