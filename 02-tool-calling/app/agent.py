# ---------------------------------------------------------
# Company AI Agent - Agent Orchestrator
#
# This is the main brain of our Agentic AI system.
#
# The agent can:
# 1. Understand the user's question
# 2. Decide which capability it needs
# 3. Call one or multiple tools
# 4. Use company knowledge through RAG
# 5. Observe the results
# 6. Continue deciding if more actions are required
# 7. Return a final answer
# ---------------------------------------------------------

import os

from dotenv import load_dotenv
from google import genai
from google.genai import types

from .tools import TOOLS
from .rag import ask_rag
from .tool_definitions import get_tool_definition
from .tool_executor import execute_tool


# ---------------------------------------------------------
# Load environment variables from .env
# ---------------------------------------------------------

load_dotenv()


# ---------------------------------------------------------
# Create Gemini client.
# ---------------------------------------------------------

client = genai.Client(
    api_key=os.getenv("GEMINI_API_KEY")
)


# ---------------------------------------------------------
# RAG Tool
#
# This wrapper allows the Agent to use our existing
# RAG system as a tool.
# ---------------------------------------------------------

def search_company_knowledge(question):
    """
    Search company documents using the RAG system.

    The Agent can use this when the user asks about:
    - company policies
    - company rules
    - procedures
    - general company information
    """

    result = ask_rag(question)

    return {
        "answer": result["answer"],
        "sources": result["sources"]
    }


# ---------------------------------------------------------
# Add RAG to the approved tool registry.
#
# tools.py contains the normal Python tools.
# We add the RAG capability here so the Agent can also
# request company knowledge.
# ---------------------------------------------------------

TOOLS["search_company_knowledge"] = (
    search_company_knowledge
)


# ---------------------------------------------------------
# Load all tool definitions.
#
# This tells Gemini what tools are available and
# what parameters each tool requires.
# ---------------------------------------------------------

tool = get_tool_definition()


# ---------------------------------------------------------
# Agent Instructions
#
# These instructions define the behavior of our Agent.
# ---------------------------------------------------------

system_instruction = """
You are a company employee assistant.

Your job is to answer employee questions accurately.

Rules:

1. Use employee-specific tools when employee data
   is required.

2. Never invent employee data.

3. Use tool results as the source of truth for
   employee-specific information.

4. Use search_company_knowledge for company policies,
   rules, procedures, and general company information.

5. You may use multiple tools when necessary.

6. You may use both employee tools and company
   knowledge search when a question requires both.

7. Do not call tools unnecessarily.

8. After collecting enough information, provide a
   clear and concise final answer.

9. If the required information cannot be found,
   clearly tell the user instead of guessing.
"""


def run_agent(question, max_steps=5):
    """
    Run the Agent for a user's question.

    The Agent can perform multiple actions before
    producing its final answer.

    max_steps prevents the Agent from running forever.
    """

    # -----------------------------------------------------
    # Conversation history.
    #
    # The Agent keeps the original question, Gemini's
    # responses, and tool results in this list.
    # -----------------------------------------------------

    contents = [
        types.Content(
            role="user",
            parts=[
                types.Part.from_text(
                    text=question
                )
            ]
        )
    ]

    # -----------------------------------------------------
    # Agent loop
    #
    # Each iteration represents one decision cycle.
    # -----------------------------------------------------

    for step in range(max_steps):

        print(
            f"\n--- Agent Step {step + 1} ---"
        )

        # -------------------------------------------------
        # Ask Gemini what to do next.
        # -------------------------------------------------

        response = client.models.generate_content(
            model="gemini-3.5-flash-lite",
            contents=contents,
            config=types.GenerateContentConfig(
                tools=[tool],
                system_instruction=system_instruction
            )
        )

        # -------------------------------------------------
        # Save Gemini's response to the conversation.
        #
        # This is important because the next iteration
        # needs to know what Gemini requested previously.
        # -------------------------------------------------

        contents.append(
            response.candidates[0].content
        )

        tool_responses = []

        # -------------------------------------------------
        # Check whether Gemini requested any tools.
        # -------------------------------------------------

        for part in response.candidates[0].content.parts:

            if not part.function_call:
                continue

            function_name = (
                part.function_call.name
            )

            tool_arguments = (
                part.function_call.args
            )

            print(
                "Agent selected tool:",
                function_name
            )

            print(
                "Arguments:",
                tool_arguments
            )

            # -------------------------------------------------
            # Execute the tool through the centralized
            # security/execution layer.
            # -------------------------------------------------

            execution_result = execute_tool(
                function_name,
                tool_arguments
            )

            # -------------------------------------------------
            # Stop if the tool execution failed.
            # -------------------------------------------------

            if not execution_result["success"]:

                return {
                    "answer": execution_result["error"]
                }

            tool_result = execution_result["result"]

            print(
                "Tool result:",
                tool_result
            )

            # -------------------------------------------------
            # Convert the Python result into a Gemini
            # function-response message.
            # -------------------------------------------------

            tool_response = (
                types.Part.from_function_response(
                    name=function_name,
                    response={
                        "result": tool_result
                    }
                )
            )

            tool_responses.append(
                tool_response
            )

        # -------------------------------------------------
        # If Gemini requested tools:
        #
        # Send the results back to Gemini and continue
        # the Agent loop.
        # -------------------------------------------------

        if tool_responses:

            contents.append(
                types.Content(
                    role="user",
                    parts=tool_responses
                )
            )

            # Gemini will now observe the tool results
            # and decide what to do next.
            continue

        # -------------------------------------------------
        # No tool was requested.
        #
        # This means Gemini has produced the final answer.
        # -------------------------------------------------

        return {
            "answer": response.text
        }

    # -----------------------------------------------------
    # Maximum number of Agent steps reached.
    #
    # This protects the application from an infinite loop.
    # -----------------------------------------------------

    return {
        "answer": (
            "I could not complete the request within "
            "the allowed number of steps."
        )
    }


# ---------------------------------------------------------
# Local testing
# ---------------------------------------------------------

if __name__ == "__main__":

    question = input(
        "Ask the agent: "
    )

    result = run_agent(question)

    print("\nFinal Answer:")
    print(result["answer"])