import pytest
from fastapi.testclient import TestClient
from src.app import app

client = TestClient(app)

def test_get_activities():
    response = client.get("/activities")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, dict)
    assert "Chess Club" in data


def test_signup_for_activity():
    activity = "Chess Club"
    email = "newstudent@mergington.edu"
    response = client.post(f"/activities/{activity}/signup?email={email}")
    assert response.status_code == 200
    assert f"Signed up {email} for {activity}" in response.json()["message"]
    # Clean up: remove the test participant
    client.post(f"/activities/{activity}/unregister?email={email}")


def test_unregister_from_activity():
    activity = "Chess Club"
    email = "removeme@mergington.edu"
    # Add participant first
    client.post(f"/activities/{activity}/signup?email={email}")
    # Now remove
    response = client.post(f"/activities/{activity}/unregister?email={email}")
    assert response.status_code == 200
    assert f"Removed {email} from {activity}" in response.json()["message"]


def test_signup_activity_not_found():
    response = client.post("/activities/Nonexistent/signup?email=test@mergington.edu")
    assert response.status_code == 404
    assert response.json()["detail"] == "Activity not found"


def test_unregister_participant_not_found():
    response = client.post("/activities/Chess Club/unregister?email=notfound@mergington.edu")
    assert response.status_code == 404
    assert response.json()["detail"] == "Participant not found"
