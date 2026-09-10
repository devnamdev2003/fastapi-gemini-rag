import os

from dotenv import load_dotenv
from fastapi import FastAPI
from pydantic import BaseModel
from google import genai
from google.genai import types

from .rag import ask_rag

load_dotenv()

app = FastAPI()

api_key = os.getenv("GEMINI_API_KEY")


class QuestionRequest(BaseModel):
    question: str


@app.get("/")
def home():
    return {"message": "Company AI Assistant is running"}


@app.post("/ask")
def ask_question(request: QuestionRequest):

    result = ask_rag(request.question)

    return {
        "question": request.question,
        "answer": result["answer"],
        "sources": result["sources"],
    }


@app.post("/ai")
def ask_ai(request: QuestionRequest):
    client = genai.Client(
        api_key=api_key, http_options=types.HttpOptions(timeout=60000)
    )

    response = client.models.generate_content(
        model="gemini-3.5-flash-lite", contents=request.question
    )
    client.close()
    return {"question": request.question, "answer": response.text}
