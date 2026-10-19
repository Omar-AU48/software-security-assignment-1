from flask import Flask
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

if __name__ == "__main__":
    app.run(port=5000)