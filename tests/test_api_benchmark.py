def test_benchmark_placeholder():
    from fastapi.testclient import TestClient
    from app.main import app
    client = TestClient(app)
    resp = client.get('/api/search/benchmark')
    assert resp.status_code == 200
    assert 'detail' in resp.json() and resp.json()['detail'] == 'placeholder'
