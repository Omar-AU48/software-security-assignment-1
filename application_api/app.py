from flask import Flask, request, jsonify
import requests
import jwt
from datetime import datetime, timedelta, timezone

app = Flask(__name__)

SECRET_KEY = "omarassignmentkey123456789012345"

users = {
    "omar": {
        "password": "omar123",
        "role": "user"
    },
    "yamal": {
        "password": "yamal123",
        "role": "user"
    },
    "admin": {
        "password": "admin123",
        "role": "admin"
    }
}

@app.route("/")
def home():
    return "Application API is running"

@app.route("/resource-check")
def resource_check():
    response = requests.get("http://127.0.0.1:5001/")
    return response.text

@app.route("/processing-check")
def processing_check():
    response = requests.get("http://127.0.0.1:5002/")
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

if __name__ == "__main__":
    app.run(port=5000)