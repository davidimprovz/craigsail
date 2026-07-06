"""Test that the obsolete SAVED_SEARCHES / SAVED_SEARCH_STORE globals are gone and
cleanup_globals is wired end-to-end."""
from fastapi.testclient import TestClient
from app.main import app, cleanup_globals


def test_cleanup_globals_returns_empty_list():
    assert cleanup_globals() == []


def test_cleanup_route_reachable():
    client = TestClient(app, raise_server_exceptions=False)
    r = client.get("/api/cleanup/globals")
    assert r.status_code < 500
    body = r.json()
    assert "result" in body
    assert body["result"] == []


def test_no_obsolete_globals_in_main():
    import app.main as m

    assert not hasattr(m, "SAVED_SEARCHES")
    assert not hasattr(m, "SAVED_SEARCH_STORE")
