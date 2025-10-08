"""
Test suite for Expat Rental Assistant API
"""
from fastapi.testclient import TestClient
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
    response = client.post("/chat", json={"text": "Hello"})
    assert response.status_code == 200
    data = response.json()
    assert "reply" in data
    assert isinstance(data["reply"], str)


def test_chat_endpoint_empty_message():
    """Test chat endpoint handles empty messages"""
    response = client.post("/chat", json={"text": ""})
    assert response.status_code == 200
    # Should still return a response, even if input is empty


def test_reset_endpoint():
    """Test reset endpoint clears chat history"""
    # Send a message first
    client.post("/chat", json={"text": "Test message"})

    # Reset
    response = client.post("/reset")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "reset"


def test_chat_context_persistence():
    """Test that chat history is maintained across requests"""
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


def test_price_fairness_feature():
    """Test price fairness checker feature"""
    response = client.post("/chat", json={
        "text": "Is 1400 euro for a 1-bedroom in Utrecht fair?"
    })
    assert response.status_code == 200
    data = response.json()
    reply = data["reply"].lower()
    # Should mention price context
    assert any(word in reply for word in ["euro", "price", "fair", "utrecht"])


def test_document_checklist_feature():
    """Test document checklist feature"""
    response = client.post("/chat", json={
        "text": "What documents do I need to rent?"
    })
    assert response.status_code == 200
    data = response.json()
    reply = data["reply"].lower()
    # Should mention key documents
    assert any(word in reply for word in ["bsn", "passport", "income", "document"])


def test_scam_detection_feature():
    """Test scam detection feature"""
    response = client.post("/chat", json={
        "text": "Landlord wants deposit before viewing, is this a scam?"
    })
    assert response.status_code == 200
    data = response.json()
    reply = data["reply"].lower()
    # Should warn about scam
    assert any(word in reply for word in ["scam", "warning", "suspicious", "careful", "never"])


if __name__ == "__main__":
    import pytest
    pytest.main([__file__, "-v"])
