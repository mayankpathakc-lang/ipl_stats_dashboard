from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_health_check():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "ok"


def test_list_players_endpoint():
    response = client.get("/api/players?page=1&page_size=5")
    assert response.status_code == 200
    data = response.json()
    assert "total" in data
    assert "data" in data
    assert len(data["data"]) <= 5
    assert data["total"] > 0


def test_list_players_filter_season():
    response = client.get("/api/players?season=2024")
    assert response.status_code == 200
    data = response.json()
    for item in data["data"]:
        assert item["season"] == 2024


def test_list_players_search():
    response = client.get("/api/players?search=Kohli")
    assert response.status_code == 200
    data = response.json()
    assert data["total"] > 0
    assert "Kohli" in data["data"][0]["player_name"]


def test_filter_options_endpoint():
    response = client.get("/api/players/filters")
    assert response.status_code == 200
    data = response.json()
    assert "seasons" in data
    assert "roles" in data
    assert "teams" in data
    assert 2024 in data["seasons"]


def test_summary_endpoint():
    response = client.get("/api/players/summary")
    assert response.status_code == 200
    data = response.json()
    assert "total_players" in data
    assert "highest_runs_player" in data
    assert data["total_players"] > 0


def test_get_player_by_id_endpoint():
    response = client.get("/api/players/P001")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) > 0
    assert data[0]["player_id"] == "P001"


def test_get_player_by_invalid_id():
    response = client.get("/api/players/INVALID_ID_999")
    assert response.status_code == 404
