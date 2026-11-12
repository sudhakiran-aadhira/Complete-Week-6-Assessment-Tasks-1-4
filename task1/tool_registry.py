"""
Task 1 - Tool Registry

Contains 5 tools:
1. get_order
2. get_customer
3. check_policy
4. draft_email
5. issue_refund
"""

from typing import Any


# ---------------------------------------------------------
# Mock database
# ---------------------------------------------------------

ORDERS = {
    1042: {
        "order_id": 1042,
        "customer_id": 5,
        "item": "Wireless Headphones",
        "amount": 99.99,
        "status": "DELIVERED",
    }
}

CUSTOMERS = {
    5: {
        "customer_id": 5,
        "name": "John Smith",
        "email": "john.smith@example.com",
    }
}


# ---------------------------------------------------------
# Tool functions
# ---------------------------------------------------------

def get_order(order_id: int) -> dict:
    """Get order details."""

    order = ORDERS.get(order_id)

    if not order:
        return {
            "success": False,
            "error": f"Order {order_id} not found"
        }

    return {
        "success": True,
        "order": order
    }


def get_customer(customer_id: int) -> dict:
    """Get customer details."""

    customer = CUSTOMERS.get(customer_id)

    if not customer:
        return {
            "success": False,
            "error": f"Customer {customer_id} not found"
        }

    return {
        "success": True,
        "customer": customer
    }


def check_policy(order_id: int) -> dict:
    """Check whether an order is eligible for refund."""

    order = ORDERS.get(order_id)

    if not order:
        return {
            "success": False,
            "error": f"Order {order_id} not found"
        }

    # Simple refund policy for assessment
    if order["status"] == "DELIVERED":
        return {
            "success": True,
            "eligible": True,
            "reason": "Order is eligible for refund"
        }

    return {
        "success": True,
        "eligible": False,
        "reason": "Order is not eligible for refund"
    }


def draft_email(customer_id: int, text: str) -> dict:
    """Create a draft customer email."""

    customer = CUSTOMERS.get(customer_id)

    if not customer:
        return {
            "success": False,
            "error": f"Customer {customer_id} not found"
        }

    return {
        "success": True,
        "status": "DRAFT",
        "customer_id": customer_id,
        "email": customer["email"],
        "text": text
    }


def issue_refund(order_id: int, amount: float) -> dict:
    """
    Issue refund.

    This is a HIGH-RISK action.
    The actual refund is NOT executed automatically.
    Human approval is required.
    """

    order = ORDERS.get(order_id)

    if not order:
        return {
            "success": False,
            "error": f"Order {order_id} not found"
        }

    return {
        "success": True,
        "status": "PENDING APPROVAL",
        "order_id": order_id,
        "amount": amount,
        "message": "Refund requires human approval"
    }


# ---------------------------------------------------------
# Tool Registry
# ---------------------------------------------------------

TOOL_REGISTRY = {
    "get_order": {
        "function": get_order,
        "schema": {
            "name": "get_order",
            "description": "Get order details",
            "parameters": {
                "type": "object",
                "properties": {
                    "order_id": {
                        "type": "integer"
                    }
                },
                "required": ["order_id"]
            }
        },
        "risk_level": "LOW"
    },

    "get_customer": {
        "function": get_customer,
        "schema": {
            "name": "get_customer",
            "description": "Get customer details",
            "parameters": {
                "type": "object",
                "properties": {
                    "customer_id": {
                        "type": "integer"
                    }
                },
                "required": ["customer_id"]
            }
        },
        "risk_level": "LOW"
    },

    "check_policy": {
        "function": check_policy,
        "schema": {
            "name": "check_policy",
            "description": "Check refund policy",
            "parameters": {
                "type": "object",
                "properties": {
                    "order_id": {
                        "type": "integer"
                    }
                },
                "required": ["order_id"]
            }
        },
        "risk_level": "LOW"
    },

    "draft_email": {
        "function": draft_email,
        "schema": {
            "name": "draft_email",
            "description": "Draft an email for the customer",
            "parameters": {
                "type": "object",
                "properties": {
                    "customer_id": {
                        "type": "integer"
                    },
                    "text": {
                        "type": "string"
                    }
                },
                "required": ["customer_id", "text"]
            }
        },
        "risk_level": "MEDIUM"
    },

    "issue_refund": {
        "function": issue_refund,
        "schema": {
            "name": "issue_refund",
            "description": "Issue a customer refund",
            "parameters": {
                "type": "object",
                "properties": {
                    "order_id": {
                        "type": "integer"
                    },
                    "amount": {
                        "type": "number"
                    }
                },
                "required": ["order_id", "amount"]
            }
        },
        "risk_level": "HIGH"
    }
}


# ---------------------------------------------------------
# Execute tool
# ---------------------------------------------------------

def execute_tool(tool_name: str, tool_input: dict) -> Any:

    if tool_name not in TOOL_REGISTRY:
        return {
            "success": False,
            "error": f"Unknown tool: {tool_name}"
        }

    tool = TOOL_REGISTRY[tool_name]

    function = tool["function"]

    try:
        return function(**tool_input)

    except Exception as e:
        return {
            "success": False,
            "error": str(e)
        }