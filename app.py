import time
from flask import Flask, jsonify, request, g
from prometheus_client import Counter, Histogram, generate_latest, CONTENT_TYPE_LATEST

app = Flask(__name__)

REQUESTS = Counter("app_requests_total", "Total requests", ["endpoint"])
ERRORS = Counter("app_errors_total", "Total 5xx responses", ["endpoint"])
LATENCY = Histogram("app_request_duration_seconds", "Request duration in seconds", ["endpoint"])


@app.before_request
def start_timer():
    g.start = time.time()


@app.after_request
def record_metrics(response):
    if request.path != "/metrics":
        endpoint = request.url_rule.rule if request.url_rule else "unmatched"
        LATENCY.labels(endpoint=endpoint).observe(time.time() - g.start)
        if response.status_code >= 500:
            ERRORS.labels(endpoint=endpoint).inc()
    return response


@app.route("/")
def home():
    REQUESTS.labels(endpoint="/").inc()
    return jsonify(message="Hello from CloudForge v2", version="1.0.0")


@app.route("/health")
def health():
    REQUESTS.labels(endpoint="/health").inc()
    return jsonify(status="ok")


@app.route("/error")
def error():
    REQUESTS.labels(endpoint="/error").inc()
    return jsonify(error="simulated failure"), 500


@app.route("/metrics")
def metrics():
    return generate_latest(), 200, {"Content-Type": CONTENT_TYPE_LATEST}


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
