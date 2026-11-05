from app import app


def test_health():
    client = app.test_client()
    response = client.get("/health")
    assert response.status_code == 200
    assert response.get_json() == {"status": "ok"}


def test_add():
    client = app.test_client()
    response = client.get("/add/2/3")
    assert response.get_json() == {"result": 5}


def test_unknown_route():
    client = app.test_client()
    response = client.get("/nothing")
    assert response.status_code == 404


def test_health_failure_switch(monkeypatch):
    monkeypatch.setenv("SIMULATE_FAILURE", "1")
    client = app.test_client()
    response = client.get("/health")
    assert response.status_code == 500
