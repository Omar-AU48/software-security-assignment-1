import requests


BASE_API = "http://127.0.0.1:5000"
RESOURCE_API = "http://127.0.0.1:5001"


def get_token():
    response = requests.post(
        f"{BASE_API}/login",
        json={
            "username": "omar",
            "password": "omar123"
        }
    )

    return response.json()["token"]


def test_export_own_document_works():
    token = get_token()

    response = requests.get(
        f"{BASE_API}/export/1",
        headers={
            "Authorization": f"Bearer {token}"
        }
    )

    assert response.status_code == 200


def test_internal_user_header_route_is_gone():
    response = requests.get(
        f"{RESOURCE_API}/internal/documents/2",
        headers={
            "X-User": "yamal"
        }
    )

    assert response.status_code == 404