from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

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

    return jsonify({
        "message": "Login successful",
        "username": username,
        "role": user["role"]
    }), 200

if __name__ == "__main__":
    app.run(port=5000)