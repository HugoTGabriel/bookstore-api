from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_delete_book():
    book = {
        "title": "Test Book",
        "author": "Author",
        "status": "Lido"
    }

    create = client.post("/books/", json=book)
    assert create.status_code == 200, create.json()

    book_id = create.json()["id"]

    response = client.delete(f"/books/{book_id}")

    assert response.status_code == 204
    assert response.text == ""

    check = client.get(f"/books/{book_id}")
    assert check.status_code == 404