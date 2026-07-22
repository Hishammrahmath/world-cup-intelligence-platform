from fastapi.testclient import TestClient

from app.main import app


client = TestClient(app)


def test_health_endpoint_returns_ok():
    response = client.get("/health")

    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_matches_endpoint_returns_all_matches():
    response = client.get("/matches")

    assert response.status_code == 200
    assert len(response.json()["matches"]) == 104


def test_match_detail_endpoint_returns_one_match():
    response = client.get("/matches/1")

    assert response.status_code == 200
    assert response.json()["match"]["match_id"] == 1


def test_unknown_match_returns_404():
    response = client.get("/matches/999")

    assert response.status_code == 404
    assert response.json()["detail"] == "Match not found for match_id: 999"


def test_match_events_endpoint_returns_events():
    response = client.get("/matches/1/events")

    assert response.status_code == 200
    assert response.json()["events"]


def test_match_stats_endpoint_returns_stats():
    response = client.get("/matches/1/stats")

    assert response.status_code == 200
    assert len(response.json()["stats"]) == 2


def test_match_momentum_endpoint_returns_momentum():
    response = client.get("/matches/1/momentum")

    assert response.status_code == 200
    assert response.json()["momentum"]


def test_match_turning_points_endpoint_returns_turning_points_list():
    response = client.get("/matches/1/turning-points")

    assert response.status_code == 200
    assert isinstance(response.json()["turning_points"], list)


def test_scheduled_match_endpoints_return_empty_lists_where_expected():
    events_response = client.get("/matches/104/events")
    stats_response = client.get("/matches/104/stats")
    turning_points_response = client.get("/matches/104/turning-points")

    assert events_response.json()["events"] == []
    assert stats_response.json()["stats"] == []
    assert turning_points_response.json()["turning_points"] == []
