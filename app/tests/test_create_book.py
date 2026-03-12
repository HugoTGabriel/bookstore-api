from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_create_book():
    data = {
        "title": "Clean Code",
        "author": "Robert Martin",
        "status": "Pendente"
    }

    response = client.post("/books/", json=data)

    assert response.status_code == 200, response.json()

    body = response.json()
    assert body["title"] == "Clean Code"
    assert body["author"] == "Robert Martin"
    assert body["status"] == "Pendente"
    assert "id" in body