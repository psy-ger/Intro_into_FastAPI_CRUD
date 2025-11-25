from fastapi.testclient import TestClient
from main import app

client = TestClient(app)


def test_create_and_read():
    data = {"title": "Test", "price": 1.23}
    resp = client.post('/items/', json=data)
    assert resp.status_code == 201
    item = resp.json()
    assert item['title'] == 'Test'

    get_resp = client.get(f"/items/{item['id']}")
    assert get_resp.status_code == 200
    assert get_resp.json()['id'] == item['id']
