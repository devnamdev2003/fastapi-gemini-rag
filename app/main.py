# ---------------------------------------------------------
# Company AI Agent - FastAPI
#
# This file exposes our AI Agent through a REST API.
from fastapi import FastAPI
from pydantic import BaseModel

from .agent import run_agent


# ---------------------------------------------------------
# Create FastAPI application.
# ---------------------------------------------------------

app = FastAPI(
    title="Company AI Agent",
    description=(
        "Agentic AI assistant with RAG and tool calling"
    ),
    version="1.0.0"
)


# ---------------------------------------------------------
# Request model
#
# Defines the JSON format accepted by /ask.
# ---------------------------------------------------------

class QuestionRequest(BaseModel):

    question: str


# ---------------------------------------------------------
# Health-check endpoint
#
# Used to verify that the API is running.
# ---------------------------------------------------------

@app.get("/")
def home():

    return {
        "message": "Company AI Agent is running"
    }


# ---------------------------------------------------------
# Main Agent endpoint
#
# The user's question is passed to the Agent.
# The Agent decides whether it needs:
# - employee tools
# - company knowledge / RAG
# - multiple capabilities
# ---------------------------------------------------------

@app.post("/ask")
def ask_question(request: QuestionRequest):

    # Run the Agent.
    result = run_agent(
        request.question
    )

    # Return a clean API response.
    return {
        "question": request.question,
        "answer": result["answer"]
    }