import requests


BASE_API = "http://127.0.0.1:5000"
PROCESSING_API = "http://127.0.0.1:5002"


def get_token():
    response = requests.post(
        f"{BASE_API}/login",
        json={
            "username": "omar",
            "password": "omar123"
        }
    )

    return response.json()["token"]


def test_path_traversal_is_blocked():
    token = get_token()

    response = requests.post(
        f"{PROCESSING_API}/save-export/1",
        headers={
            "Authorization": f"Bearer {token}"
        },
        json={
            "filename": "../outside.txt"
        }
    )

    data = response.json()

    assert response.status_code == 200
    assert data["path"] == "exports\\outside.txt"