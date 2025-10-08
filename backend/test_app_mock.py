"""
Fast test suite for Expat Rental Assistant API using mocked model
"""
from fastapi.testclient import TestClient
from unittest.mock import patch, MagicMock
import sys

# Mock the model loading before importing app
mock_tokenizer = MagicMock()
mock_tokenizer.eos_token = "</s>"
mock_tokenizer.pad_token = "</s>"
mock_model = MagicMock()

# Mock the tokenizer and model
with patch('transformers.AutoTokenizer.from_pretrained', return_value=mock_tokenizer):
    with patch('transformers.AutoModelForCausalLM.from_pretrained', return_value=mock_model):
        from app import app, VERSION

client = TestClient(app)


def test_root_endpoint():
    """Test the root endpoint returns API information"""
    response = client.get("/")
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "Expat Rental Assistant API"
    assert data["version"] == VERSION
    assert "endpoints" in data


def test_health_endpoint():
    """Test the health check endpoint"""
    response = client.get("/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "ok"
    assert data["version"] == VERSION


def test_chat_endpoint_structure():
    """Test chat endpoint accepts valid requests"""
    # Mock the model response
    mock_output = MagicMock()
    mock_model.generate.return_value = mock_output
    mock_tokenizer.decode.return_value = "This is a mocked response from the assistant."

    response = client.post("/chat", json={"text": "Hello"})
    assert response.status_code == 200
    data = response.json()
    assert "reply" in data
    assert isinstance(data["reply"], str)


def test_chat_endpoint_empty_message():
    """Test chat endpoint handles empty messages"""
    mock_output = MagicMock()
    mock_model.generate.return_value = mock_output
    mock_tokenizer.decode.return_value = "Please ask me a question."

    response = client.post("/chat", json={"text": ""})
    assert response.status_code == 200


def test_reset_endpoint():
    """Test reset endpoint clears chat history"""
    # Send a message first
    mock_output = MagicMock()
    mock_model.generate.return_value = mock_output
    mock_tokenizer.decode.return_value = "Response"

    client.post("/chat", json={"text": "Test message"})

    # Reset
    response = client.post("/reset")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "reset"


def test_chat_context_persistence():
    """Test that chat history is maintained across requests"""
    mock_output = MagicMock()
    mock_model.generate.return_value = mock_output
    mock_tokenizer.decode.return_value = "Response"

    # Reset first
    client.post("/reset")

    # Send two messages
    response1 = client.post("/chat", json={"text": "What is your purpose?"})
    assert response1.status_code == 200

    response2 = client.post("/chat", json={"text": "Can you repeat that?"})
    assert response2.status_code == 200

    # Both should return valid responses
    assert "reply" in response1.json()
    assert "reply" in response2.json()


def test_invalid_endpoint():
    """Test that invalid endpoints return 404"""
    response = client.get("/invalid")
    assert response.status_code == 404


def test_chat_missing_text_field():
    """Test chat endpoint with missing text field"""
    response = client.post("/chat", json={})
    assert response.status_code == 422  # Validation error


if __name__ == "__main__":
    import pytest
    pytest.main([__file__, "-v"])
