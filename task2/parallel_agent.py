
"""
Week 6 Assessment - Task 2
Parallel Execution and Error Recovery

- Async tools
- asyncio.gather()
- Sequential vs parallel timing
- Random timeout
- Maximum 2 retries
- Run 3 times without crashing
"""

import asyncio
import random
import time


MAX_RETRIES = 2
RANDOM_FAILURE_ENABLED = True


# --------------------------------------------------
# Mock database
# --------------------------------------------------

ORDERS = {
    1042: {
        "order_id": 1042,
        "customer_id": 5,
        "amount": 99.99,
        "status": "DELIVERED"
    }
}

CUSTOMERS = {
    5: {
        "customer_id": 5,
        "name": "John Smith",
        "email": "john.smith@example.com"
    }
}


# --------------------------------------------------
# Three asynchronous lookup tools
# --------------------------------------------------

async def get_order(order_id: int):

    await asyncio.sleep(1)

    order = ORDERS.get(order_id)

    if not order:
        raise ValueError("Order not found")

    return order


async def get_customer(customer_id: int):

    await asyncio.sleep(1)

    # Random timeout simulation
    if RANDOM_FAILURE_ENABLED and random.random() < 0.5:
        raise TimeoutError("timeout")

    customer = CUSTOMERS.get(customer_id)

    if not customer:
        raise ValueError("Customer not found")

    return customer


async def check_policy(order_id: int):

    await asyncio.sleep(1)

    order = ORDERS.get(order_id)

    if not order:
        raise ValueError("Order not found")

    if order["status"] == "DELIVERED":
        return {
            "eligible": True,
            "reason": "Order is eligible for refund"
        }

    return {
        "eligible": False,
        "reason": "Order is not eligible"
    }


# --------------------------------------------------
# Retry mechanism
# --------------------------------------------------

async def call_with_retry(
    tool_name,
    tool_function,
    tool_input,
    max_retries=MAX_RETRIES,
    show_output=True
):

    for attempt in range(max_retries + 1):

        try:

            result = await tool_function(**tool_input)

            if attempt > 0 and show_output:
                print(
                    f"retry {attempt} succeeded"
                )

            return {
                "tool": tool_name,
                "success": True,
                "observation": result,
                "attempts": attempt + 1
            }

        except Exception as error:

            # Return error as observation to the agent
            observation = {
                "error": str(error)
            }

            if show_output:
                print(
                    f"Tool failed: {error} "
                    f"-> Observation: {observation}"
                )

            if attempt < max_retries:

                if show_output:
                    print(f"Retry {attempt + 1}")

            else:

                if show_output:
                    print(
                        f"{tool_name} failed after "
                        f"{max_retries} retries"
                    )

                return {
                    "tool": tool_name,
                    "success": False,
                    "observation": observation,
                    "attempts": attempt + 1
                }


# --------------------------------------------------
# Sequential execution
# --------------------------------------------------

async def sequential_lookup():

    start = time.perf_counter()

    await get_order(1042)
    await get_customer(5)
    await check_policy(1042)

    return time.perf_counter() - start


# --------------------------------------------------
# Parallel execution
# --------------------------------------------------

async def parallel_lookup():

    start = time.perf_counter()

    await asyncio.gather(
        get_order(1042),
        get_customer(5),
        check_policy(1042)
    )

    return time.perf_counter() - start


# --------------------------------------------------
# Time comparison
# --------------------------------------------------

async def compare_execution_time():

    global RANDOM_FAILURE_ENABLED

    # Disable random failure for fair timing
    RANDOM_FAILURE_ENABLED = False

    sequential_time = await sequential_lookup()

    parallel_time = await parallel_lookup()

    print("\n========== TIME COMPARISON ==========")

    print(f"Sequential: {sequential_time:.1f} s")
    print(f"Parallel:   {parallel_time:.1f} s")

    saved = sequential_time - parallel_time

    print(f"Time saved: {saved:.1f} s")

    print("=====================================\n")


# --------------------------------------------------
# Agent workflow
# --------------------------------------------------

async def run_lookup_workflow(
    run_number,
    enable_random_failure=True,
    show_output=True
):

    global RANDOM_FAILURE_ENABLED

    RANDOM_FAILURE_ENABLED = enable_random_failure

    if show_output:
        print(f"\n========== AGENT RUN {run_number} ==========")

    # Run three tools concurrently.
    # Each tool has its own retry mechanism.

    results = await asyncio.gather(

        call_with_retry(
            "get_order",
            get_order,
            {"order_id": 1042},
            show_output=show_output
        ),

        call_with_retry(
            "get_customer",
            get_customer,
            {"customer_id": 5},
            show_output=show_output
        ),

        call_with_retry(
            "check_policy",
            check_policy,
            {"order_id": 1042},
            show_output=show_output
        ),

        return_exceptions=True
    )

    # Protect the agent from unexpected exceptions
    safe_results = {}

    for tool_name, result in zip(
        ["get_order", "get_customer", "check_policy"],
        results
    ):

        if isinstance(result, Exception):

            safe_results[tool_name] = {
                "success": False,
                "observation": {
                    "error": str(result)
                }
            }

        else:
            safe_results[tool_name] = result

    if show_output:

        print("\nAGENT OBSERVATIONS:")

        for tool_name, result in safe_results.items():

            print(f"{tool_name}: {result['observation']}")

        if all(
            result["success"]
            for result in safe_results.values()
        ):

            print("\nAgent completed successfully.")

        else:

            print("\nAgent completed with tool errors. No crash.")

    return safe_results


# --------------------------------------------------
# Main function - run 3 times
# --------------------------------------------------

async def main():

    # Fixed random seed makes the demo reproducible.
    # The failure itself is still randomly simulated.
    random.seed(7)

    print("\nCUSTOMER REFUND AGENT - TASK 2")

    # Compare execution time
    await compare_execution_time()

    # Run the agent 3 times
    for run_number in range(1, 4):

        try:

            await run_lookup_workflow(run_number)

        except Exception as error:

            print(
                f"Run {run_number} recovered from error: {error}"
            )

    print("\n=====================================")
    print("ALL 3 AGENT RUNS FINISHED")
    print("Agent did not crash.")
    print("Maximum retries allowed: 2")
    print("=====================================")


if __name__ == "__main__":

    asyncio.run(main())