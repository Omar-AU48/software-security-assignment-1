import requests


BASE_API = "http://127.0.0.1:5000"
RESOURCE_API = "http://127.0.0.1:5001"


def get_token(username, password):
    response = requests.post(
        f"{BASE_API}/login",
        json={
            "username": username,
            "password": password
        }
    )

    return response.json()["token"]


def test_omar_can_access_own_document():
    token = get_token("omar", "omar123")

    response = requests.get(
        f"{RESOURCE_API}/documents/1",
        headers={
            "Authorization": f"Bearer {token}"
        }
    )

    assert response.status_code == 200


def test_omar_cannot_access_yamal_document():
    token = get_token("omar", "omar123")

    response = requests.get(
        f"{RESOURCE_API}/documents/2",
        headers={
            "Authorization": f"Bearer {token}"
        }
    )

    assert response.status_code == 403

def test_normal_user_cannot_access_admin():
    token = get_token("omar", "omar123")

    response = requests.get(
        f"{BASE_API}/admin",
        headers={
            "Authorization": f"Bearer {token}"
        }
    )

    assert response.status_code == 403


def test_admin_can_access_admin():
    token = get_token("admin", "admin123")

    response = requests.get(
        f"{BASE_API}/admin",
        headers={
            "Authorization": f"Bearer {token}"
        }
    )

    assert response.status_code == 200