from flask import Flask, request, jsonify
import requests
import jwt
import os
from datetime import datetime, timedelta, timezone

app = Flask(__name__)

SECRET_KEY = os.environ["JWT_SECRET"]

users = {
    "omar": {
        "password": os.environ["OMAR_PASSWORD"],
        "role": "user"
    },
    "yamal": {
        "password": os.environ["YAMAL_PASSWORD"],
        "role": "user"
    },
    "admin": {
        "password": os.environ["ADMIN_PASSWORD"],
        "role": "admin"
    }
}

@app.route("/")
def home():
    return "Application API is running"

@app.route("/resource-check")
def resource_check():
    response = requests.get(
        "http://127.0.0.1:5001/",
        timeout=5
    )
    return response.text

@app.route("/processing-check")
def processing_check():
    response = requests.get(
        "http://127.0.0.1:5002/",
        timeout=5
    )
    return response.text

@app.route("/login", methods=["POST"])
def login():
    data = request.get_json()

    username = data["username"]
    password = data["password"]

    user = users.get(username)

    if user is None:
        return jsonify({"message": "Invalid username or password"}), 401

    if user["password"] != password:
        return jsonify({"message": "Invalid username or password"}), 401

    payload = {
        "sub": username,
        "role": user["role"],
        "exp": datetime.now(timezone.utc) + timedelta(hours=1)
    }

    token = jwt.encode(
        payload,
        SECRET_KEY,
        algorithm="HS256"
    )

    return jsonify({
        "message": "Login successful",
        "token": token
    }), 200

@app.route("/profile", methods=["GET"])
def profile():
    auth_header = request.headers.get("Authorization")

    if auth_header is None:
        return jsonify({"message": "Authorization header missing"}), 401

    if not auth_header.startswith("Bearer "):
        return jsonify({"message": "Invalid authorization format"}), 401

    token = auth_header.split(" ")[1]

    try:
        payload = jwt.decode(
            token,
            SECRET_KEY,
            algorithms=["HS256"]
        )

        return jsonify({
            "username": payload["sub"],
            "role": payload["role"]
        }), 200

    except jwt.ExpiredSignatureError:
        return jsonify({"message": "Token expired"}), 401

    except jwt.InvalidTokenError:
        return jsonify({"message": "Invalid token"}), 401

@app.route("/admin", methods=["GET"])
def admin():
    auth_header = request.headers.get("Authorization")

    if auth_header is None:
        return jsonify({"message": "Authorization header missing"}), 401

    if not auth_header.startswith("Bearer "):
        return jsonify({"message": "Invalid authorization format"}), 401

    token = auth_header.split(" ")[1]

    try:
        payload = jwt.decode(
            token,
            SECRET_KEY,
            algorithms=["HS256"]
        )

        if payload["role"] != "admin":
            return jsonify({"message": "Access denied"}), 403

        return jsonify({"message": "Admin access"}), 200

    except jwt.ExpiredSignatureError:
        return jsonify({"message": "Token expired"}), 401

    except jwt.InvalidTokenError:
        return jsonify({"message": "Invalid token"}), 401

@app.route("/documents/<document_id>", methods=["GET"])
def get_document(document_id):
    auth_header = request.headers.get("Authorization")

    if auth_header is None:
        return jsonify({"message": "No token"}), 401

    response = requests.get(
        f"http://127.0.0.1:5001/documents/{document_id}",
        headers={"Authorization": auth_header},
        timeout=5
    )

    return jsonify(response.json()), response.status_code

@app.route("/documents", methods=["POST"])
def create_document():
    auth_header = request.headers.get("Authorization")

    if auth_header is None:
        return jsonify({"message": "No token"}), 401

    data = request.get_json()

    response = requests.post(
        "http://127.0.0.1:5001/documents",
        headers={"Authorization": auth_header},
        json=data,
        timeout=5
    )

    return jsonify(response.json()), response.status_code

@app.route("/export/<document_id>", methods=["GET"])
def export_document(document_id):
    auth_header = request.headers.get("Authorization")

    if auth_header is None:
        return jsonify({"message": "No token"}), 401

    response = requests.get(
        f"http://127.0.0.1:5002/export/{document_id}",
        headers={"Authorization": auth_header},
        timeout=5
    )

    return jsonify(response.json()), response.status_code

if __name__ == "__main__":
    app.run(port=5000)