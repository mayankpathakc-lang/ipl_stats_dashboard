from typing import Optional, List
from fastapi import APIRouter, Query, HTTPException
from app.models.schemas import (
    PlayerStats,
    PlayerStatsListResponse,
    FilterOptionsResponse,
    OverviewSummaryResponse
)
from app.services.stats import (
    get_paginated_players,
    get_filter_options,
    get_player_history,
    get_overview_summary
)

router = APIRouter(prefix="/api/players", tags=["Players"])


@router.get("", response_model=PlayerStatsListResponse)
def list_players(
    search: Optional[str] = Query(None, description="Search by player name"),
    season: Optional[int] = Query(None, description="Filter by IPL season (e.g. 2024)"),
    role: Optional[str] = Query(None, description="Filter by player role"),
    team: Optional[str] = Query(None, description="Filter by IPL team (e.g. RCB)"),
    sort_by: str = Query("runs", description="Column to sort by"),
    sort_order: str = Query("desc", description="Sort order: 'asc' or 'desc'"),
    page: int = Query(1, ge=1, description="Page number"),
    page_size: int = Query(10, ge=1, le=100, description="Items per page")
):
    """Retrieves paginated list of player statistics with filtering and sorting."""
    records, total_items, total_pages = get_paginated_players(
        search=search,
        season=season,
        role=role,
        team=team,
        sort_by=sort_by,
        sort_order=sort_order,
        page=page,
        page_size=page_size
    )
    return PlayerStatsListResponse(
        total=total_items,
        page=page,
        page_size=page_size,
        total_pages=total_pages,
        data=records
    )


@router.get("/filters", response_model=FilterOptionsResponse)
def get_filters():
    """Retrieves available distinct filter options for seasons, roles, and teams."""
    options = get_filter_options()
    return FilterOptionsResponse(**options)


@router.get("/summary", response_model=OverviewSummaryResponse)
def get_summary(
    season: Optional[int] = Query(None, description="Filter by season"),
    role: Optional[str] = Query(None, description="Filter by role"),
    team: Optional[str] = Query(None, description="Filter by team")
):
    """Retrieves top-level summary statistics for key metric highlight cards."""
    summary = get_overview_summary(season=season, role=role, team=team)
    return OverviewSummaryResponse(**summary)


@router.get("/{player_id}", response_model=List[PlayerStats])
def get_player_by_id(player_id: str):
    """Retrieves all season stats records for a specific player ID."""
    history = get_player_history(player_id)
    if not history:
        raise HTTPException(status_code=404, detail=f"Player with ID '{player_id}' not found.")
    return history
