from flask import Flask, request, jsonify
import requests
from export_helper.formatter import make_export

app = Flask(__name__)

@app.route("/")
def home():
    return "Processing Service is running"

@app.route("/export/<document_id>", methods=["GET"])
def export_document(document_id):
    auth_header = request.headers.get("Authorization")

    if auth_header is None:
        return jsonify({"message": "No token"}), 401

    response = requests.get(
        f"http://127.0.0.1:5001/documents/{document_id}",
        headers={"Authorization": auth_header}
    )

    if response.status_code != 200:
        return jsonify(response.json()), response.status_code

    document = response.json()

    export_text = make_export(document)

    return jsonify({
        "export": export_text
    }), 200

if __name__ == "__main__":
    app.run(port=5002)