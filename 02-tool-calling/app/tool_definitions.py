# ---------------------------------------------------------
# Company AI Agent - Tool Definitions
#
# This file describes our tools to Gemini.
#
# IMPORTANT:
# These are only TOOL DEFINITIONS.
#
# The actual Python functions are implemented in tools.py.
# ---------------------------------------------------------

from google import genai
from google.genai import types


def get_tool_definition():
    """
    Return all tools that Gemini is allowed to use.

    Gemini uses these definitions to understand:
    - tool name
    - what the tool does
    - parameters required by the tool
    """

    return types.Tool(
        function_declarations=[

            # -------------------------------------------------
            # Tool 1: Get employee leave balance
            # -------------------------------------------------

            types.FunctionDeclaration(
                name="get_leave_balance",

                description=(
                    "Get the current leave balance of a specific employee."
                ),

                parameters=types.Schema(
                    type=types.Type.OBJECT,

                    properties={
                        "employee_id": types.Schema(
                            type=types.Type.STRING,
                            description="The ID of the employee."
                        )
                    },

                    required=["employee_id"]
                )
            ),

            # -------------------------------------------------
            # Tool 2: Get employee WFH usage
            # -------------------------------------------------

            types.FunctionDeclaration(
                name="get_wfh_days",

                description=(
                    "Get the number of work-from-home days "
                    "used by a specific employee this week."
                ),

                parameters=types.Schema(
                    type=types.Type.OBJECT,

                    properties={
                        "employee_id": types.Schema(
                            type=types.Type.STRING,
                            description="The ID of the employee."
                        )
                    },

                    required=["employee_id"]
                )
            ),

            # -------------------------------------------------
            # Tool 3: Search company knowledge
            #
            # This connects Gemini to our RAG system.
            # -------------------------------------------------

            types.FunctionDeclaration(
                name="search_company_knowledge",

                description=(
                    "Search company documents for policies, "
                    "rules, procedures, and other company information."
                ),

                parameters=types.Schema(
                    type=types.Type.OBJECT,

                    properties={
                        "question": types.Schema(
                            type=types.Type.STRING,
                            description=(
                                "The question to search for "
                                "in company documents."
                            )
                        )
                    },

                    required=["question"]
                )
            )
        ]
    )