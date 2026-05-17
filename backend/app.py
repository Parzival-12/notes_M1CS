import requests
from flask import Flask, jsonify, request
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

NOTES_URL = "https://raw.githubusercontent.com/Gladrat/notes_M1CS/main/notes.json"


@app.route("/notes")
def notes():
    try:
        r = requests.get(NOTES_URL, timeout=5)
        r.raise_for_status()
        data = r.json()
        if "etudiants" not in data:
            raise ValueError("invalid structure")
        return jsonify(data)
    except Exception:
        return jsonify({"error": "Service temporairement indisponible"}), 503


@app.route("/search")
def search():
    try:
        r = requests.get(NOTES_URL, timeout=5)
        r.raise_for_status()
        data = r.json()
    except Exception:
        return jsonify({"error": "Service temporairement indisponible"}), 503

    q = request.args.get("q", "").lower()
    results = [
        e for e in data["etudiants"]
        if q in e["nom"].lower() or q in e["prenom"].lower()
    ]
    return jsonify({**data, "etudiants": results})


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
