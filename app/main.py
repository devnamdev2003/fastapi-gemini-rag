import os

from dotenv import load_dotenv
from fastapi import FastAPI
from pydantic import BaseModel
from google import genai
from google.genai import types

from .rag import ask_rag


load_dotenv()

app = FastAPI()


class QuestionRequest(BaseModel):
    question: str


@app.get("/")
def home():
    return {
        "message": "Company AI Assistant is running"
    }


@app.post("/ask")
def ask_question(request: QuestionRequest):

    result = ask_rag(request.question)

    return {
        "question": request.question,
        "answer": result["answer"],
        "sources": result["sources"]
    }