from flask import Flask, request, jsonify
import jwt

app = Flask(__name__)

SECRET_KEY = "omarassignmentkey123456789012345"

documents = {
    "1": {
        "owner": "omar",
        "title": "Omar document",
        "content": "This belongs to Omar"
    },
    "2": {
        "owner": "yamal",
        "title": "Yamal document",
        "content": "This belongs to Yamal"
    }
}

@app.route("/")
def home():
    return "Resource Service is running"

@app.route("/documents/<document_id>", methods=["GET"])
def get_document(document_id):
    auth_header = request.headers.get("Authorization")

    if auth_header is None:
        return jsonify({"message": "No token"}), 401

    if not auth_header.startswith("Bearer "):
        return jsonify({"message": "Wrong token format"}), 401

    token = auth_header.split(" ")[1]

    try:
        payload = jwt.decode(
            token,
            SECRET_KEY,
            algorithms=["HS256"]
        )
    except jwt.ExpiredSignatureError:
        return jsonify({"message": "Token expired"}), 401
    except jwt.InvalidTokenError:
        return jsonify({"message": "Invalid token"}), 401

    document = documents.get(document_id)

    if document is None:
        return jsonify({"message": "Document not found"}), 404

    username = payload["sub"]

    if document["owner"] != username:
        return jsonify({"message": "Access denied"}), 403

    return jsonify(document), 200

@app.route("/documents", methods=["POST"])
def create_document():
    auth_header = request.headers.get("Authorization")

    if auth_header is None:
        return jsonify({"message": "No token"}), 401

    if not auth_header.startswith("Bearer "):
        return jsonify({"message": "Wrong token format"}), 401

    token = auth_header.split(" ")[1]

    try:
        payload = jwt.decode(
            token,
            SECRET_KEY,
            algorithms=["HS256"]
        )
    except jwt.ExpiredSignatureError:
        return jsonify({"message": "Token expired"}), 401
    except jwt.InvalidTokenError:
        return jsonify({"message": "Invalid token"}), 401

    data = request.get_json()

    title = data["title"]
    content = data["content"]

    new_id = str(len(documents) + 1)

    documents[new_id] = {
        "owner": payload["sub"],
        "title": title,
        "content": content
    }

    return jsonify({
        "id": new_id,
        "document": documents[new_id]
    }), 201

if __name__ == "__main__":
    app.run(port=5001)