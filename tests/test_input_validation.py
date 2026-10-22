import requests


BASE_API = "http://127.0.0.1:5000"


def get_token():
    response = requests.post(
        f"{BASE_API}/login",
        json={
            "username": "omar",
            "password": "omar123"
        }
    )

    return response.json()["token"]


def test_empty_title_is_rejected():
    token = get_token()

    response = requests.post(
        f"{BASE_API}/documents",
        headers={
            "Authorization": f"Bearer {token}"
        },
        json={
            "title": "",
            "content": "test"
        }
    )

    assert response.status_code == 400


def test_valid_document_is_created():
    token = get_token()

    response = requests.post(
        f"{BASE_API}/documents",
        headers={
            "Authorization": f"Bearer {token}"
        },
        json={
            "title": "My notes",
            "content": "test"
        }
    )

    assert response.status_code == 201