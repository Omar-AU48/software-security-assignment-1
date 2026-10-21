from flask import Flask, request, jsonify
import requests
from export_helper.formatter import make_export
import os

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


@app.route("/save-export/<document_id>", methods=["POST"])
def save_export(document_id):
    auth_header = request.headers.get("Authorization")

    if auth_header is None:
        return jsonify({"message": "No token"}), 401

    data = request.get_json()

    if data is None:
        return jsonify({"message": "No data"}), 400

    filename = data.get("filename")

    if not isinstance(filename, str) or filename.strip() == "":
        return jsonify({"message": "Filename is required"}), 400

    safe_filename = os.path.basename(filename)

    response = requests.get(
        f"http://127.0.0.1:5001/documents/{document_id}",
        headers={"Authorization": auth_header}
    )

    if response.status_code != 200:
        return jsonify(response.json()), response.status_code

    document = response.json()
    export_text = make_export(document)

    os.makedirs("exports", exist_ok=True)

    path = os.path.join("exports", safe_filename)

    with open(path, "w") as file:
        file.write(export_text)

    return jsonify({"message": "Export saved", "path": path}), 200


if __name__ == "__main__":
    app.run(port=5002)