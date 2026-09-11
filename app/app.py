from flask import Flask, jsonify

app = Flask(__name__)


@app.route("/")
def home():
    return jsonify({
        "service": "devops-platform-lab",
        "status": "running"
    }), 200


@app.route("/health")
def health():
    return jsonify({
        "status": "healthy"
    }), 200


@app.route("/ready")
def ready():
    return jsonify({
        "status": "ready"
    }), 200


@app.route("/error")
def error():
    return jsonify({
        "error": "intentional internal server error"
    }), 500


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)