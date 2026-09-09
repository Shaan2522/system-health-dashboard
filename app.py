"""
System Health Dashboard API

A lightweight status API exposing basic health, version, and
environment information for an operations team.
"""

import os
from flask import Flask, jsonify

app = Flask(__name__)

APP_VERSION = "v1.1.0"

@app.route("/health", methods=["GET"])
def health():
    """Basic liveness check used by engineers and monitoring tools."""
    return jsonify({"status": "UP"}), 200


@app.route("/version", methods=["GET"])
def version():
    """Return the currently deployed application version."""
    return jsonify({"version": APP_VERSION}), 200


@app.route("/environment", methods=["GET"])
def environment():
    """Return the current environment name, sourced from an env var.

    Defaults to 'development' when APP_ENV is not set, so the app
    still starts cleanly with no extra configuration.
    """
    env_name = os.environ.get("APP_ENV", "development")
    return jsonify({"environment": env_name}), 200


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)