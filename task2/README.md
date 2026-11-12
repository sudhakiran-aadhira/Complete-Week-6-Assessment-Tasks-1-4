
# Week 6 Assessment - Task 2
## Parallel Execution and Error Recovery

### Requirements

1. Three asynchronous lookup tools.
2. Execute tools using asyncio.gather().
3. Compare sequential and parallel execution.
4. Random timeout simulation in get_customer().
5. Return tool errors as observations.
6. Retry failed tools maximum 2 times.
7. Run the agent 3 times without crashing.

### Tools

- get_order(order_id)
- get_customer(customer_id)
- check_policy(order_id)

### Execution Time

Expected:

Sequential: 3.0 seconds
Parallel: 1.0 second

Time saved: 2.0 seconds.

### Error Recovery

If a tool fails:

Tool failed: timeout

Observation: {"error": "timeout"}

Retry 1

retry 1 succeeded

Maximum retries: 2.

### Run

python parallel_agent.py

### Test

python -m pytest -v test_task2.py