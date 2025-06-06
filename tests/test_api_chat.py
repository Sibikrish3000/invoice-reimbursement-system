import pytest
from unittest.mock import patch

def test_chat_endpoint(client):
    req = {"query": "What is the status of invoice 1?", "chat_history": []}
    fake_response = {
        "response": "Invoice 1 is fully reimbursed.",
        "relevant_invoices": ["1"],
        "chat_history": []
    }
    with patch("app.services.chatbot.Chatbot.process_query", return_value=fake_response):
        response = client.post("/api/v1/chat", json=req)
        assert response.status_code == 200
        assert response.json()["response"] == "Invoice 1 is fully reimbursed." 