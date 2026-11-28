# Standard library
import json
import os
from typing import Literal

# Third-party libraries
from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException
from google import genai
from google.genai import errors, types
from pydantic import BaseModel, Field, ValidationError


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


class FeedbackRequest(BaseModel):
    review: str = Field(min_length=5)


class FeedbackResponse(BaseModel):
    sentiment: Literal["Positive", "Negative", "Neutral", "Mixed"]
    delivery_feedback: str
    product_feedback: str


@app.post("/analyze-feedback")
def analyze_feedback(feedback_request: FeedbackRequest):
    try:
        instruction = "Act as an e-commerce customer feedback analyzer. You have to analyze the customer's actual review and extract the relevant feedback. Sentiment must be Positive, Negative, Neutral, or Mixed. Extract delivery-related feedback into delivery_feedback. And extract product-related feedback into product_feedback. Don't invent information. If the review doesn't mention delivery or product quality, return an empty string for that field. Return exactly one JSON object. Do not wrap the object inside a list or array. Include only the three specified fields."
        review = client.models.generate_content(
            model="gemini-3.5-flash-lite",
            contents=feedback_request.review,
            config=types.GenerateContentConfig(
                system_instruction=instruction,
                response_mime_type="application/json",
                response_schema=FeedbackResponse
            )
        )

        generated_text = review.text
        if not generated_text or not generated_text.strip():
            raise HTTPException(
                status_code=502,
                detail="AI returned an empty response."
            )
        data = json.loads(generated_text)
        validated_response = FeedbackResponse.model_validate(data)

        return validated_response.model_dump()

    except json.JSONDecodeError:
        raise HTTPException(
                status_code=502,
                detail="AI returned an invalid JSON response."
        )
    except ValidationError:
        raise HTTPException(
            status_code=502,
            detail="AI returned an invalid response format."
        )
    except errors.APIError as e:
        if e.message == "API key not valid. Please pass a valid API key.":
            raise HTTPException(
                status_code=401,
                detail="Authentication failed."
            )
        elif e.code == 400:
            raise HTTPException(
                status_code=400,
                detail="The request sent to Gemini is invalid."
            )
        elif e.code == 429:
            raise HTTPException(
                status_code=429,
                detail="You've exceeded a quota or rate limit."
            )
        else:
            raise HTTPException(
                status_code=500,
                detail="An error occurred while communicating with the AI service."
            )
    except HTTPException:
        raise

    except Exception:
        raise HTTPException(
            status_code=500,
            detail="An unexpected server error occurred."
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

        if not response.text or not response.text.strip():
            raise HTTPException(
                status_code=502,
                detail="AI returned an empty response."
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
    except errors.APIError as e:
        if e.message == "API key not valid. Please pass a valid API key.":
            raise HTTPException(
                status_code=401,
                detail="Authentication failed."
            )
        elif e.code == 400:
            raise HTTPException(
                status_code=400,
                detail="The request sent to Gemini is invalid."
            )
        elif e.code == 429:
            raise HTTPException(
                status_code=429,
                detail="You've exceeded a quota or rate limit."
            )
        elif e.code == 500:
            raise HTTPException(
                status_code=500,
                detail="Something went wrong on the AI provider's side."
            )
        else:
            raise HTTPException(
                status_code=500,
                detail="An error occurred while communicating with the AI service."
            )
    except HTTPException:
        raise

    except Exception:
        raise HTTPException(
            status_code=500,
            detail="An unexpected server error occurred."
        )
