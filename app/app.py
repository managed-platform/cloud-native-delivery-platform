import time

from flask import Flask, Response, jsonify, request
from prometheus_client import Counter, Histogram, generate_latest, CONTENT_TYPE_LATEST

app = Flask(__name__)


HTTP_REQUESTS_TOTAL = Counter(
    "cloud_native_platform_http_requests_total",
    "Total number of HTTP requests",
    ["method", "endpoint", "status"],
)

HTTP_REQUEST_DURATION_SECONDS = Histogram(
    "cloud_native_platform_http_request_duration_seconds",
    "HTTP request duration in seconds",
    ["method", "endpoint"],
)


@app.before_request
def start_request_timer():
    request.start_time = time.perf_counter()


@app.after_request
def record_request_metrics(response):
    if request.path != "/metrics":
        endpoint = request.url_rule.rule if request.url_rule else "unknown"

        HTTP_REQUESTS_TOTAL.labels(
            method=request.method,
            endpoint=endpoint,
            status=response.status_code,
        ).inc()

        HTTP_REQUEST_DURATION_SECONDS.labels(
            method=request.method,
            endpoint=endpoint,
        ).observe(time.perf_counter() - request.start_time)

    return response


@app.route("/")
def home():
    return jsonify({
        "service": "cloud-native-platform",
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


@app.route("/metrics")
def metrics():
    return Response(
        generate_latest(),
        mimetype=CONTENT_TYPE_LATEST,
    )


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)