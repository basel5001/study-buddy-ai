"""Tests for the Study Buddy AI API."""
import pytest
from fastapi.testclient import TestClient

from app.main import app, generate_quiz_prompt


client = TestClient(app)


def test_health():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "healthy"


def test_generate_quiz_validation_empty_text():
    response = client.post("/api/generate-quiz", json={
        "text": "short",
        "num_questions": 5,
        "difficulty": "medium",
    })
    assert response.status_code == 422


def test_generate_quiz_validation_bad_difficulty():
    response = client.post("/api/generate-quiz", json={
        "text": "A" * 20,
        "num_questions": 5,
        "difficulty": "impossible",
    })
    assert response.status_code == 422


def test_generate_quiz_validation_too_many_questions():
    response = client.post("/api/generate-quiz", json={
        "text": "A" * 20,
        "num_questions": 50,
        "difficulty": "medium",
    })
    assert response.status_code == 422


def test_prompt_generation():
    prompt = generate_quiz_prompt("Test material", 3, "easy")
    assert "3" in prompt
    assert "easy" in prompt
    assert "Test material" in prompt
    assert "JSON" in prompt
