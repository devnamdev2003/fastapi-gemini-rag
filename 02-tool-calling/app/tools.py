# ---------------------------------------------------------
# Company AI Agent - Tools
#
# This file contains the actual Python functions that our
# AI agent is allowed to execute.
#
# Gemini decides WHICH tool to call.
# Python executes the actual function.
# ---------------------------------------------------------


# ---------------------------------------------------------
# Tool 1: Get employee leave balance
# ---------------------------------------------------------

def get_leave_balance(employee_id):
    """
    Return the remaining leave balance for an employee.

    In a real application, this information could come from:
    - PostgreSQL
    - Oracle
    - REST API
    - HR database
    """

    # Demo employee data.
    employees = {
        "101": 12,
        "102": 8,
        "103": 15
    }

    return {
        "employee_id": employee_id,
        "remaining_leaves": employees.get(employee_id, 0)
    }


# ---------------------------------------------------------
# Tool 2: Get employee WFH usage
# ---------------------------------------------------------

def get_wfh_days(employee_id):
    """
    Return the number of WFH days used by an employee
    during the current week.
    """

    # Demo WFH data.
    wfh_data = {
        "101": 1,
        "102": 2,
        "103": 0
    }

    return {
        "employee_id": employee_id,
        "wfh_days_used": wfh_data.get(employee_id, 0)
    }


# ---------------------------------------------------------
# Tool Registry
#
# This is an allow-list of functions that the AI agent
# is permitted to execute.
#
# IMPORTANT:
# Never execute an arbitrary function requested by an LLM.
# Only execute functions present in this registry.
# ---------------------------------------------------------

TOOLS = {
    "get_leave_balance": get_leave_balance,
    "get_wfh_days": get_wfh_days
}