import pytest
import pandas as pd
from app.services.stats import (
    load_dataset,
    filter_and_sort_players,
    get_paginated_players,
    get_filter_options,
    get_overview_summary
)


@pytest.fixture
def sample_df():
    return pd.DataFrame([
        {
            "player_id": "P001",
            "player_name": "Virat Kohli",
            "season": 2024,
            "role": "Batsman",
            "team": "RCB",
            "matches": 15,
            "runs": 741,
            "balls_faced": 479,
            "batting_strike_rate": 154.7,
            "powerplay_strike_rate": 162.5,
            "middle_strike_rate": 138.4,
            "death_strike_rate": 191.2,
            "boundaries_fours": 62,
            "boundaries_sixes": 38,
            "highest_score": 113,
            "fifties": 5,
            "hundreds": 1,
            "overs_bowled": 0.0,
            "runs_conceded": 0,
            "wickets": 0,
            "bowling_economy": 0.0,
            "death_over_economy": 0.0,
            "dot_ball_percentage": 0.0
        },
        {
            "player_id": "P011",
            "player_name": "Jasprit Bumrah",
            "season": 2024,
            "role": "Bowler",
            "team": "MI",
            "matches": 13,
            "runs": 12,
            "balls_faced": 8,
            "batting_strike_rate": 150.0,
            "powerplay_strike_rate": 0.0,
            "middle_strike_rate": 120.0,
            "death_strike_rate": 180.0,
            "boundaries_fours": 1,
            "boundaries_sixes": 0,
            "highest_score": 8,
            "fifties": 0,
            "hundreds": 0,
            "overs_bowled": 51.5,
            "runs_conceded": 334,
            "wickets": 20,
            "bowling_economy": 6.45,
            "death_over_economy": 7.1,
            "dot_ball_percentage": 51.8
        }
    ])


def test_load_dataset():
    df = load_dataset()
    assert not df.empty
    assert "player_name" in df.columns
    assert "batting_strike_rate" in df.columns
    assert "death_over_economy" in df.columns


def test_filter_by_season(sample_df):
    filtered = filter_and_sort_players(sample_df, season=2024)
    assert len(filtered) == 2


def test_filter_by_search(sample_df):
    filtered = filter_and_sort_players(sample_df, search="Virat")
    assert len(filtered) == 1
    assert filtered.iloc[0]["player_name"] == "Virat Kohli"


def test_filter_by_role(sample_df):
    filtered = filter_and_sort_players(sample_df, role="Bowler")
    assert len(filtered) == 1
    assert filtered.iloc[0]["player_name"] == "Jasprit Bumrah"


def test_sorting(sample_df):
    sorted_df = filter_and_sort_players(sample_df, sort_by="runs", sort_order="desc")
    assert sorted_df.iloc[0]["player_name"] == "Virat Kohli"
    
    sorted_asc = filter_and_sort_players(sample_df, sort_by="runs", sort_order="asc")
    assert sorted_asc.iloc[0]["player_name"] == "Jasprit Bumrah"


def test_pagination(sample_df):
    records, total, pages = get_paginated_players(page=1, page_size=1, df=sample_df)
    assert len(records) == 1
    assert total == 2
    assert pages == 2


def test_filter_options(sample_df):
    options = get_filter_options(sample_df)
    assert options["seasons"] == [2024]
    assert "Batsman" in options["roles"]
    assert "Bowler" in options["roles"]
    assert "RCB" in options["teams"]
    assert "MI" in options["teams"]


def test_overview_summary(sample_df):
    summary = get_overview_summary(df=sample_df)
    assert summary["total_players"] == 2
    assert summary["highest_runs_player"] == "Virat Kohli"
    assert summary["highest_runs"] == 741
    assert summary["highest_wickets_player"] == "Jasprit Bumrah"
    assert summary["highest_wickets"] == 20
