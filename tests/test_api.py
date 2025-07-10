import pytest
from fastapi.testclient import TestClient
from unittest.mock import MagicMock
from sklearn.preprocessing import MultiLabelBinarizer

from src.api import main as api_main

# Create dummy artifacts
dummy_mlb = MultiLabelBinarizer()
dummy_mlb.fit([["python"]])

dummy_model = MagicMock()
dummy_model.predict.return_value = dummy_mlb.transform([["python"]])

dummy_vectorizer = MagicMock()
dummy_vectorizer.transform.return_value = None  # not used by dummy_model

# Patch the globals
api_main.model = dummy_model
api_main.vectorizer = dummy_vectorizer
api_main.mlb = dummy_mlb

client = TestClient(api_main.app)


def test_root_endpoint():
    """Basic sanity check on the root endpoint."""
    response = client.get("/")
    assert response.status_code == 200
    assert response.json().get("message") == "Welcome to the StackOverflow Tags Suggester API!"


def test_predict_endpoint_returns_tags():
    """Ensure that the /predict endpoint returns at least one tag for a sample English question."""
    sample_question = {
        "body": "How do I sort a list of integers in Python in ascending order?"
    }

    response = client.post("/predict", json=sample_question)

    # Endpoint should succeed
    assert response.status_code == 200

    # Response structure
    json_data = response.json()
    assert "tags" in json_data, "Response JSON must contain 'tags' key"
    assert isinstance(json_data["tags"], list), "'tags' should be a list"

    # We expect at least one tag, typically 'python'
    assert len(json_data["tags"]) > 0, "At least one tag should be predicted"
    assert "python" in json_data["tags"], "'python' should be among suggested tags for this question" 