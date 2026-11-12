
# Task 3 - Human-in-the-Loop and Safety Guards

## Features

1. READ tools execute automatically.
2. WRITE tools execute and create a notification.
3. DELETE and SEND tools require human approval.
4. Pending actions are stored in SQLite.
5. Approval and rejection API endpoints.
6. Input guard checks scope and PII.
7. Output guard blocks card numbers and unsupported claims.
8. Prompt injection in order notes is ignored.
9. Rate limit: maximum 5 runs per user per hour.

## Run application

```powershell
py app.py
```

Open http://127.0.0.1:5000

## Run tests

```powershell
py -m pytest -v test_task3.py
```

## API endpoints

POST /run

GET /pending-actions

POST /pending-actions/1/approve

POST /pending-actions/1/reject