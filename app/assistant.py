import os
from dotenv import load_dotenv
from google import genai
from google.genai import types

from .rag import ask_rag
from .tools import TOOLS

load_dotenv()

# Create the Gemini client using the API key
# stored in the .env file.
client = genai.Client(
    api_key=os.getenv("GEMINI_API_KEY")
)


# ---------------------------------------------------------
# Define the tools that Gemini is allowed to use.
# ---------------------------------------------------------

tool = types.Tool(
    function_declarations=[

        # Tool 1: Get employee leave balance
        types.FunctionDeclaration(
            name="get_leave_balance",
            description="Get the current leave balance of a specific employee.",
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

        # Tool 2: Get employee WFH usage
        types.FunctionDeclaration(
            name="get_wfh_days",
            description="Get the number of work-from-home days used by a specific employee this week.",
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
        )
    ]
)


def ask_assistant(question):

    # -----------------------------------------------------
    # STEP 1:
    # Ask Gemini whether it wants to use a tool.
    # -----------------------------------------------------

    response = client.models.generate_content(
        model="gemini-3.5-flash-lite",
        contents=question,
        config=types.GenerateContentConfig(
            tools=[tool]
        )
    )

    tool_responses = []

    # -----------------------------------------------------
    # STEP 2:
    # Check whether Gemini requested a tool.
    # -----------------------------------------------------

    for part in response.candidates[0].content.parts:

        if part.function_call:

            function_name = part.function_call.name
            tool_arguments = part.function_call.args

            print("Gemini selected tool:", function_name)
            print("Tool arguments:", tool_arguments)

            # Find the actual Python function from our registry.
            # ---------------------------------------------------------
            # Security check:
            # Only execute tools that exist in our approved registry.
            # Never execute an arbitrary function requested by the LLM.
            # ---------------------------------------------------------

            if function_name not in TOOLS:
                return {
                    "type": "error",
                    "answer": "The requested tool is not available."
                }

            try:
                # Get the approved Python function.
                tool_function = TOOLS[function_name]

                # Execute the tool using Gemini's arguments.
                tool_result = tool_function(**tool_arguments)

            except Exception as error:
                # Prevent the entire API from crashing if a tool fails.
                print("Tool execution error:", error)

                return {
                    "type": "error",
                    "answer": "I was unable to execute the requested operation."
                }

            print("Tool result:", tool_result)

            # Convert Python result into a Gemini
            # function-response message.
            tool_response = types.Part.from_function_response(
                name=function_name,
                response={
                    "result": tool_result
                }
            )

            tool_responses.append(tool_response)

    # -----------------------------------------------------
    # STEP 3:
    # If tools were used, send their results back to Gemini.
    # Gemini will now create the final answer.
    # -----------------------------------------------------

    if tool_responses:

        final_response = client.models.generate_content(
            model="gemini-3.5-flash-lite",
            contents=[
                # Original user question
                types.Content(
                    role="user",
                    parts=[
                        types.Part.from_text(text=question)
                    ]
                ),

                # Gemini's original response containing
                # the requested tool calls.
                response.candidates[0].content,

                # Results returned by our Python tools.
                types.Content(
                    role="user",
                    parts=tool_responses
                )
            ],
            config=types.GenerateContentConfig(
                tools=[tool]
            )
        )

        return {
            "type": "tool",
            "answer": final_response.text
        }

    # -----------------------------------------------------
    # STEP 4:
    # If Gemini did not request a tool,
    # use RAG for company-document questions.
    # -----------------------------------------------------

    print("Gemini did not select a tool.")
    print("Sending question to RAG...")

    rag_result = ask_rag(question)

    return {
        "type": "rag",
        "answer": rag_result["answer"],
        "sources": rag_result["sources"]
    }


# ---------------------------------------------------------
# Local testing
# ---------------------------------------------------------

if __name__ == "__main__":

    question = input("Ask the assistant: ")

    result = ask_assistant(question)

    print("\nFinal Result:")
    print(result)