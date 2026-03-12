from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_get_book_by_id():
    book = {
        "title": "DDD",
        "author": "Eric Evans",
        "status": "Lendo"
    }

    create = client.post("/books/", json=book)
    assert create.status_code == 200, create.json()

    book_id = create.json()["id"]

    response = client.get(f"/books/{book_id}")

    assert response.status_code == 200
    body = response.json()
    assert body["id"] == book_id
    assert body["title"] == "DDD"
    assert body["author"] == "Eric Evans"
    assert body["status"] == "Lendo"