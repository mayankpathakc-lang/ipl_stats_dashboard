from typing import List, Optional
from pydantic import BaseModel, Field


class PlayerStats(BaseModel):
    player_id: str
    player_name: str
    season: int
    role: str
    team: str
    matches: int
    runs: int
    balls_faced: int
    batting_strike_rate: float
    powerplay_strike_rate: float
    middle_strike_rate: float
    death_strike_rate: float
    boundaries_fours: int
    boundaries_sixes: int
    highest_score: int
    fifties: int
    hundreds: int
    overs_bowled: float
    runs_conceded: int
    wickets: int
    bowling_economy: float
    death_over_economy: float
    dot_ball_percentage: float


class PlayerStatsListResponse(BaseModel):
    total: int
    page: int
    page_size: int
    total_pages: int
    data: List[PlayerStats]


class FilterOptionsResponse(BaseModel):
    seasons: List[int]
    roles: List[str]
    teams: List[str]


class OverviewSummaryResponse(BaseModel):
    total_players: int
    total_matches: int
    highest_runs_player: Optional[str] = None
    highest_runs: int = 0
    highest_wickets_player: Optional[str] = None
    highest_wickets: int = 0
    best_strike_rate_player: Optional[str] = None
    best_strike_rate: float = 0.0
    best_death_economy_player: Optional[str] = None
    best_death_economy: float = 0.0
