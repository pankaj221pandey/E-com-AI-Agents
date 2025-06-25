import pytest
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

@pytest.mark.parametrize("payload,expected_keys", [
    (
        {
            "user_id": "USER1001",
            "message": "What is your return policy?"
        },
        ["faq_answer", "final_response"]
    ),
    (
        {
            "user_id": "USER1234",
            "message": "Where is my order ORD12345?"
        },
        ["order_status", "final_response"]
    ),
    (
        {
            "user_id": "USER1002",
            "message": "Suggest me something like MagSafe"
        },
        ["product_recommendations", "final_response"]
    ),
    (
        {
            "user_id": "USER9878",
            "message": "What is your return policy for damaged products? Also, where is my order?"
        },
        ["faq_answer", "order_status", "final_response"]
    )
])
def test_query_endpoint(payload, expected_keys):
    response = client.post("/query", json=payload)
    assert response.status_code == 200
    data = response.json()

    for key in expected_keys:
        assert key in data
        assert data[key] != ""  # Ensure it's not empty
