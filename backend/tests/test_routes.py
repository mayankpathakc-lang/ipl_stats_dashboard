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
    response = client.get("/api/players/INVALID999")
    assert response.status_code == 404


# --- Security-specific tests ---

def test_security_headers_present():
    """Security headers should be set on every response."""
    response = client.get("/health")
    assert response.headers.get("X-Content-Type-Options") == "nosniff"
    assert response.headers.get("X-Frame-Options") == "DENY"
    assert response.headers.get("X-XSS-Protection") == "1; mode=block"
    assert response.headers.get("Referrer-Policy") == "strict-origin-when-cross-origin"


def test_invalid_sort_column_rejected():
    """sort_by with a non-allowlisted column should return 400."""
    response = client.get("/api/players?sort_by=__internal_col__")
    assert response.status_code == 400
    assert "Invalid sort column" in response.json()["detail"]


def test_invalid_sort_order_rejected():
    """sort_order other than asc/desc should return 400."""
    response = client.get("/api/players?sort_order=DROP_TABLE")
    assert response.status_code == 400


def test_search_too_long_rejected():
    """Overly long search strings should be rejected by FastAPI validation."""
    long_search = "A" * 200
    response = client.get(f"/api/players?search={long_search}")
    assert response.status_code == 422


def test_player_id_invalid_format():
    """Player IDs with special characters should be rejected."""
    # Characters like spaces and special chars should fail the regex validator
    response = client.get("/api/players/P001; DROP TABLE")
    assert response.status_code == 400


def test_player_id_too_long():
    """Excessively long player IDs should be rejected."""
    response = client.get(f"/api/players/{'A' * 50}")
    assert response.status_code == 422


def test_season_out_of_range():
    """Season values outside 2008-2030 should be rejected."""
    response = client.get("/api/players?season=1800")
    assert response.status_code == 422

    response = client.get("/api/players?season=9999")
    assert response.status_code == 422


def test_no_path_leak_in_404():
    """404 responses should not contain filesystem paths."""
    response = client.get("/api/players/NONEXISTENT")
    assert response.status_code == 404
    detail = response.json().get("detail", "")
    assert "\\" not in detail
    assert "C:" not in detail
