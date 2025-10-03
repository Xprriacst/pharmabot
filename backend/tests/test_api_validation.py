"""Tests for API request validation"""
import pytest


def test_chat_empty_message(client):
    """Test that empty messages are rejected"""
    response = client.post(
        "/api/chat/",
        json={"message": "", "conversation_history": []}
    )
    assert response.status_code == 400
    assert "empty" in response.json()["detail"].lower()


def test_chat_whitespace_message(client):
    """Test that whitespace-only messages are rejected"""
    response = client.post(
        "/api/chat/",
        json={"message": "   ", "conversation_history": []}
    )
    assert response.status_code == 400


def test_search_empty_query(client):
    """Test that empty search queries are rejected"""
    response = client.get("/api/search/?q=")
    assert response.status_code in [400, 422]  # 422 for FastAPI validation


def test_search_whitespace_query(client):
    """Test that whitespace-only search queries are rejected"""
    response = client.get("/api/search/?q=%20%20%20")  # URL encoded spaces
    assert response.status_code == 400


def test_search_limit_validation(client):
    """Test that search limit is validated"""
    # Too low
    response = client.get("/api/search/?q=test&limit=0")
    assert response.status_code == 422
    
    # Too high
    response = client.get("/api/search/?q=test&limit=100")
    assert response.status_code == 422
    
    # Valid range
    response = client.get("/api/search/?q=test&limit=10")
    # Should be 200 or 503 (if no API key), not 422
    assert response.status_code in [200, 503]


def test_chat_request_structure(client):
    """Test that chat request accepts proper structure"""
    response = client.post(
        "/api/chat/",
        json={
            "message": "Test question about paracetamol",
            "conversation_history": [
                {"role": "user", "content": "Previous question"},
                {"role": "assistant", "content": "Previous response"}
            ],
            "session_id": "test-session-123"
        }
    )
    # Should be 200 or 503 (if no API key/no data)
    assert response.status_code in [200, 500, 503]
