
import asyncio

from parallel_agent import (
    get_order,
    get_customer,
    check_policy,
    call_with_retry,
    run_lookup_workflow
)


def test_async_tools():

    assert asyncio.iscoroutinefunction(get_order)
    assert asyncio.iscoroutinefunction(get_customer)
    assert asyncio.iscoroutinefunction(check_policy)


def test_retry_maximum_two():

    attempts = 0

    async def failing_tool():

        nonlocal attempts

        attempts += 1

        if attempts <= 2:
            raise TimeoutError("timeout")

        return {"status": "success"}

    result = asyncio.run(
        call_with_retry(
            "test_tool",
            failing_tool,
            {},
            max_retries=2,
            show_output=False
        )
    )

    assert result["success"] is True
    assert result["attempts"] == 3
    assert attempts == 3


def test_parallel_tools_complete():

    result = asyncio.run(
        run_lookup_workflow(
            1,
            enable_random_failure=False,
            show_output=False
        )
    )

    assert result["get_order"]["success"] is True
    assert result["get_customer"]["success"] is True
    assert result["check_policy"]["success"] is True


def test_three_runs_never_crash():

    results = asyncio.run(
        run_three_times()
    )

    assert len(results) == 3

    for result in results:
        assert set(result.keys()) == {
            "get_order",
            "get_customer",
            "check_policy"
        }


async def run_three_times():

    import random

    random.seed(7)

    results = []

    for i in range(1, 4):

        result = await run_lookup_workflow(
            i,
            enable_random_failure=True,
            show_output=False
        )

        results.append(result)

    return results