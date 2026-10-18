from app import app


def test_home():
    client = app.test_client()
    resp = client.get("/")
    assert resp.status_code == 200
    assert resp.get_json()["message"] == "Hello from CloudForge"


def test_health():
    client = app.test_client()
    resp = client.get("/health")
    assert resp.status_code == 200
    assert resp.get_json() == {"status": "ok"}


def test_metrics():
    client = app.test_client()
    resp = client.get("/metrics")
    assert resp.status_code == 200
    assert b"app_requests_total" in resp.data
