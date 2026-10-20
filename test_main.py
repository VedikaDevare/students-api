from fastapi.testclient import TestClient
from main import app

client = TestClient(app)


def test_protected_without_token():
    response = client.get("/protected")

    assert response.status_code == 401

def test_protected_with_invalid_token():
    response = client.get(
        "/protected",
        headers={"Authorization": "Bearer invalid-token"}
    )

    assert response.status_code == 401
def test_student_not_found():
    response = client.get("/students/2/courses")

    assert response.status_code == 404
    assert response.json()["detail"] == "Student Not Found"