
from router_agent import (
    route_request,
    run_router,
    evaluate_routing,
    run_parallel_tasks,
    TEST_REQUESTS
)


def test_refund_routing():
    assert route_request("I want a refund") == "refund"


def test_order_status_routing():
    assert route_request("Track my order") == "order-status"


def test_general_info_routing():
    assert route_request("Tell me about your company") == "general-info"


def test_all_nine_requests():
    correct, total, accuracy = evaluate_routing()

    assert correct == 9
    assert total == 9
    assert accuracy == 100.0


def test_all_three_agents():
    for request, expected in TEST_REQUESTS:
        result = run_router(request)
        assert result["agent"] == expected


def test_parallel_execution_and_aggregation():
    result = run_parallel_tasks()

    assert "Return window" in result
    assert "Payment status" in result


def test_unknown_request_routes_to_general():
    assert route_request("Hello, good morning") == "general-info"