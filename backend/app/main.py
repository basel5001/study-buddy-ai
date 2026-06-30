"""Study Buddy AI - FastAPI backend for quiz generation."""
import os
import json
import logging
from typing import Optional

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field

import boto3

logger = logging.getLogger(__name__)

app = FastAPI(
    title="Study Buddy AI",
    description="AI-powered quiz generation from study materials",
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=os.environ.get("ALLOWED_ORIGINS", "*").split(","),
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class QuizRequest(BaseModel):
    text: str = Field(..., min_length=10, description="Study material text")
    num_questions: int = Field(default=5, ge=1, le=20)
    difficulty: str = Field(default="medium", pattern="^(easy|medium|hard)$")


class QuizQuestion(BaseModel):
    question: str
    options: list[str]
    correct_answer: str
    explanation: str


class QuizResponse(BaseModel):
    questions: list[QuizQuestion]
    topic: str
    difficulty: str


def get_bedrock_client():
    """Create Bedrock runtime client."""
    return boto3.client(
        "bedrock-runtime",
        region_name=os.environ.get("AWS_REGION", "us-east-1"),
    )


def generate_quiz_prompt(text: str, num_questions: int, difficulty: str) -> str:
    """Build the prompt for quiz generation."""
    return f"""You are a quiz generator. Based on the following study material, generate exactly {num_questions} multiple-choice questions at {difficulty} difficulty level.

Study Material:
{text[:4000]}

Return ONLY valid JSON in this exact format:
{{
  "topic": "detected topic name",
  "questions": [
    {{
      "question": "the question text",
      "options": ["A) option1", "B) option2", "C) option3", "D) option4"],
      "correct_answer": "A) option1",
      "explanation": "brief explanation of why this is correct"
    }}
  ]
}}

Generate exactly {num_questions} questions. Each must have exactly 4 options."""


@app.get("/health")
async def health():
    """Health check endpoint."""
    return {"status": "healthy", "service": "study-buddy-ai"}


@app.post("/api/generate-quiz", response_model=QuizResponse)
async def generate_quiz(request: QuizRequest):
    """Generate a quiz from study material using AWS Bedrock."""
    try:
        client = get_bedrock_client()
        prompt = generate_quiz_prompt(
            request.text, request.num_questions, request.difficulty
        )

        model_id = os.environ.get("BEDROCK_MODEL_ID", "anthropic.claude-3-haiku-20240307-v1:0")

        response = client.invoke_model(
            modelId=model_id,
            contentType="application/json",
            accept="application/json",
            body=json.dumps({
                "anthropic_version": "bedrock-2023-05-31",
                "max_tokens": 4096,
                "messages": [
                    {"role": "user", "content": prompt}
                ],
            }),
        )

        result = json.loads(response["body"].read())
        content = result["content"][0]["text"]

        # Parse the JSON from the response
        quiz_data = json.loads(content)

        return QuizResponse(
            questions=[
                QuizQuestion(**q) for q in quiz_data["questions"]
            ],
            topic=quiz_data.get("topic", "General"),
            difficulty=request.difficulty,
        )

    except json.JSONDecodeError as e:
        logger.error(f"Failed to parse quiz response: {e}")
        raise HTTPException(status_code=502, detail="Failed to parse AI response")
    except boto3.exceptions.Boto3Error as e:
        logger.error(f"Bedrock API error: {e}")
        raise HTTPException(status_code=502, detail="AI service unavailable")
    except Exception as e:
        logger.error(f"Unexpected error: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")
