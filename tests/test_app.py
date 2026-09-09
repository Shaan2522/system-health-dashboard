"""
Automated tests for the System Health Dashboard API.

Run the full suite with:
    pytest tests/
"""
import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import pytest
from app import app


@pytest.fixture
def client():
    app.config["TESTING"] = True
    with app.test_client() as client:
        yield client


def test_health_returns_up(client):
    """/health should report status UP with a 200 response."""
    response = client.get("/health")
    assert response.status_code == 200
    assert response.get_json() == {"status": "UP"}


def test_version_returns_expected_version(client):
    """/version should return the app's current version string."""
    response = client.get("/version")
    assert response.status_code == 200
    body = response.get_json()
    assert "version" in body
    assert body["version"] == "v1.1.0"


def test_environment_reads_from_env_var(client, monkeypatch):
    """/environment should reflect the APP_ENV environment variable."""
    monkeypatch.setenv("APP_ENV", "staging")
    response = client.get("/environment")
    assert response.status_code == 200
    assert response.get_json() == {"environment": "staging"}


def test_environment_has_sensible_default(client, monkeypatch):
    """/environment should still respond even if APP_ENV is unset."""
    monkeypatch.delenv("APP_ENV", raising=False)
    response = client.get("/environment")
    assert response.status_code == 200
    assert "environment" in response.get_json()