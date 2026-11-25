import os

from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException
from google import genai
from google.genai import types
from pydantic import BaseModel, Field

load_dotenv()
app = FastAPI()

client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

class QuestionRequest(BaseModel):
    question: str = Field(
        min_length=3
    )
    temperature: float = Field(
        ge=0.0,
        le=1.0
    )

@app.post("/ask")
def ask_question(payload: QuestionRequest):
    try:
        response = client.models.generate_content(
            model="gemini-3.5-flash-lite",
            contents=payload.question,
            config=types.GenerateContentConfig(
                temperature=payload.temperature,
                thinking_config=types.ThinkingConfig(
                    thinking_level=types.ThinkingLevel.MINIMAL
                ),
            ),
        )

        usage = response.usage_metadata

        return {
            "success_status": 200,
            "received_question": payload.question,
            "temperature": payload.temperature,
            "total_tokens": usage.total_token_count if usage else None,
            "input_tokens": usage.prompt_token_count if usage else None,
            "output_tokens": usage.candidates_token_count if usage else None,
            "response": response.text,
        }
    except ValueError:
        raise HTTPException(status_code=400, detail="Something wrong!")