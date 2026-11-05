import os

from flask import Flask, jsonify
from prometheus_flask_exporter import PrometheusMetrics

app = Flask(__name__)
metrics = PrometheusMetrics(app)


@app.route("/health")
def health():
    if os.environ.get("SIMULATE_FAILURE") == "1":
        return jsonify(status="error"), 500
    return jsonify(status="ok")


@app.route("/add/<int:a>/<int:b>")
def add(a, b):
    return jsonify(result=a + b)


if __name__ == "__main__":
    host = os.environ.get("APP_HOST", "127.0.0.1")
    app.run(host=host, port=5000)
