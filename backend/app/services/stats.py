import math
from pathlib import Path
from typing import List, Optional, Tuple, Dict, Any
import pandas as pd

# Path resolution for CSV file
DATA_DIR = Path(__file__).resolve().parent.parent.parent / "data"
CSV_PATH = DATA_DIR / "ipl_player_stats.csv"

_df_cache: Optional[pd.DataFrame] = None


def load_dataset(csv_path: Optional[Path] = None) -> pd.DataFrame:
    """Loads and caches the IPL player stats CSV dataset."""
    global _df_cache
    path_to_load = csv_path or CSV_PATH
    
    if not path_to_load.exists():
        raise FileNotFoundError(f"IPL stats CSV file not found at: {path_to_load}")
        
    df = pd.read_csv(path_to_load)
    # Fill NaN values appropriately
    df = df.fillna({
        "batting_strike_rate": 0.0,
        "powerplay_strike_rate": 0.0,
        "middle_strike_rate": 0.0,
        "death_strike_rate": 0.0,
        "bowling_economy": 0.0,
        "death_over_economy": 0.0,
        "dot_ball_percentage": 0.0,
        "runs": 0,
        "wickets": 0,
        "matches": 0,
        "balls_faced": 0,
        "boundaries_fours": 0,
        "boundaries_sixes": 0,
        "highest_score": 0,
        "fifties": 0,
        "hundreds": 0,
        "overs_bowled": 0.0,
        "runs_conceded": 0
    })
    _df_cache = df
    return _df_cache


def get_filter_options(df: Optional[pd.DataFrame] = None) -> Dict[str, List]:
    """Returns available unique seasons, roles, and teams for filters."""
    if df is None:
        df = load_dataset()
        
    seasons = sorted(df["season"].dropna().unique().astype(int).tolist(), reverse=True)
    roles = sorted(df["role"].dropna().unique().astype(str).tolist())
    teams = sorted(df["team"].dropna().unique().astype(str).tolist())
    
    return {
        "seasons": seasons,
        "roles": roles,
        "teams": teams
    }


def filter_and_sort_players(
    df: pd.DataFrame,
    search: Optional[str] = None,
    season: Optional[int] = None,
    role: Optional[str] = None,
    team: Optional[str] = None,
    sort_by: str = "runs",
    sort_order: str = "desc"
) -> pd.DataFrame:
    """Filters dataframe by search query, season, role, team and applies sorting."""
    filtered_df = df.copy()

    if season is not None:
        filtered_df = filtered_df[filtered_df["season"] == season]

    if role is not None and role.strip() and role.lower() != "all":
        filtered_df = filtered_df[filtered_df["role"].str.lower() == role.strip().lower()]

    if team is not None and team.strip() and team.lower() != "all":
        filtered_df = filtered_df[filtered_df["team"].str.lower() == team.strip().lower()]

    if search is not None and search.strip():
        query = search.strip().lower()
        filtered_df = filtered_df[filtered_df["player_name"].str.lower().str.contains(query, regex=False)]

    # Validate sort column
    valid_sort_columns = list(df.columns)
    if sort_by not in valid_sort_columns:
        sort_by = "runs"

    ascending = (sort_order.lower() == "asc")
    filtered_df = filtered_df.sort_values(by=sort_by, ascending=ascending)

    return filtered_df


def get_paginated_players(
    search: Optional[str] = None,
    season: Optional[int] = None,
    role: Optional[str] = None,
    team: Optional[str] = None,
    sort_by: str = "runs",
    sort_order: str = "desc",
    page: int = 1,
    page_size: int = 10,
    df: Optional[pd.DataFrame] = None
) -> Tuple[List[Dict[str, Any]], int, int]:
    """Returns paginated player stats list, total items, total pages."""
    if df is None:
        df = load_dataset()

    filtered_df = filter_and_sort_players(
        df=df,
        search=search,
        season=season,
        role=role,
        team=team,
        sort_by=sort_by,
        sort_order=sort_order
    )

    total_items = len(filtered_df)
    page_size = max(1, min(100, page_size))
    total_pages = max(1, math.ceil(total_items / page_size))
    page = max(1, min(page, total_pages)) if total_items > 0 else 1

    start_idx = (page - 1) * page_size
    end_idx = start_idx + page_size
    sliced_df = filtered_df.iloc[start_idx:end_idx]

    records = sliced_df.to_dict(orient="records")
    return records, total_items, total_pages


def get_player_history(player_id: str, df: Optional[pd.DataFrame] = None) -> List[Dict[str, Any]]:
    """Returns all season records for a given player ID."""
    if df is None:
        df = load_dataset()
    player_df = df[df["player_id"] == player_id].sort_values(by="season", ascending=False)
    return player_df.to_dict(orient="records")


def get_overview_summary(
    season: Optional[int] = None,
    role: Optional[str] = None,
    team: Optional[str] = None,
    df: Optional[pd.DataFrame] = None
) -> Dict[str, Any]:
    """Computes summary statistics for top cards on the dashboard."""
    if df is None:
        df = load_dataset()

    filtered_df = filter_and_sort_players(df=df, season=season, role=role, team=team)

    if filtered_df.empty:
        return {
            "total_players": 0,
            "total_matches": 0,
            "highest_runs_player": None,
            "highest_runs": 0,
            "highest_wickets_player": None,
            "highest_wickets": 0,
            "best_strike_rate_player": None,
            "best_strike_rate": 0.0,
            "best_death_economy_player": None,
            "best_death_economy": 0.0
        }

    # Top scorer
    top_scorer_row = filtered_df.loc[filtered_df["runs"].idxmax()]
    # Top wicket taker
    top_bowler_row = filtered_df.loc[filtered_df["wickets"].idxmax()]
    
    # Best strike rate (min 100 runs)
    batsmen_100_runs = filtered_df[filtered_df["runs"] >= 100]
    best_sr_row = batsmen_100_runs.loc[batsmen_100_runs["batting_strike_rate"].idxmax()] if not batsmen_100_runs.empty else top_scorer_row

    # Best death economy (min 15 overs bowled)
    bowlers_min_overs = filtered_df[(filtered_df["overs_bowled"] >= 15) & (filtered_df["death_over_economy"] > 0)]
    best_econ_row = bowlers_min_overs.loc[bowlers_min_overs["death_over_economy"].idxmin()] if not bowlers_min_overs.empty else (
        filtered_df[filtered_df["death_over_economy"] > 0].loc[filtered_df[filtered_df["death_over_economy"] > 0]["death_over_economy"].idxmin()] if not filtered_df[filtered_df["death_over_economy"] > 0].empty else top_bowler_row
    )

    return {
        "total_players": int(filtered_df["player_name"].nunique()),
        "total_matches": int(filtered_df["matches"].sum()),
        "highest_runs_player": str(top_scorer_row["player_name"]),
        "highest_runs": int(top_scorer_row["runs"]),
        "highest_wickets_player": str(top_bowler_row["player_name"]),
        "highest_wickets": int(top_bowler_row["wickets"]),
        "best_strike_rate_player": str(best_sr_row["player_name"]),
        "best_strike_rate": float(best_sr_row["batting_strike_rate"]),
        "best_death_economy_player": str(best_econ_row["player_name"]),
        "best_death_economy": float(best_econ_row["death_over_economy"])
    }
