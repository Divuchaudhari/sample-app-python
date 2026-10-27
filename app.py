import os

from flask import Flask, jsonify

app = Flask(__name__)


@app.route("/health")
def health():
    return jsonify(status="ok")


@app.route("/add/<int:a>/<int:b>")
def add(a, b):
    return jsonify(result=a + b)


if __name__ == "__main__":
    host = os.environ.get("APP_HOST", "127.0.0.1")
    app.run(host=host, port=5000)