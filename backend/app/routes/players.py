import re
from typing import Optional, List
from fastapi import APIRouter, Query, HTTPException, Path
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
    get_overview_summary,
    SORTABLE_COLUMNS
)

router = APIRouter(prefix="/api/players", tags=["Players"])

# Regex for valid player IDs (alphanumeric, 1-20 chars)
PLAYER_ID_PATTERN = re.compile(r"^[A-Za-z0-9_-]{1,20}$")

# Max length for free-text query parameters
MAX_SEARCH_LENGTH = 100
MAX_FILTER_LENGTH = 50


def _validate_string_param(value: Optional[str], max_length: int, param_name: str) -> Optional[str]:
    """Validates and sanitizes a string query parameter."""
    if value is None:
        return None
    value = value.strip()
    if len(value) > max_length:
        raise HTTPException(
            status_code=400,
            detail=f"Parameter '{param_name}' exceeds maximum length of {max_length} characters."
        )
    return value


@router.get("", response_model=PlayerStatsListResponse)
def list_players(
    search: Optional[str] = Query(None, max_length=MAX_SEARCH_LENGTH, description="Search by player name"),
    season: Optional[int] = Query(None, ge=2008, le=2030, description="Filter by IPL season (e.g. 2024)"),
    role: Optional[str] = Query(None, max_length=MAX_FILTER_LENGTH, description="Filter by player role"),
    team: Optional[str] = Query(None, max_length=MAX_FILTER_LENGTH, description="Filter by IPL team (e.g. RCB)"),
    sort_by: str = Query("runs", max_length=MAX_FILTER_LENGTH, description="Column to sort by"),
    sort_order: str = Query("desc", description="Sort order: 'asc' or 'desc'"),
    page: int = Query(1, ge=1, le=1000, description="Page number"),
    page_size: int = Query(10, ge=1, le=100, description="Items per page")
):
    """Retrieves paginated list of player statistics with filtering and sorting."""
    # Validate sort_by against allowlist
    if sort_by not in SORTABLE_COLUMNS:
        raise HTTPException(
            status_code=400,
            detail=f"Invalid sort column '{sort_by}'. Allowed: {', '.join(SORTABLE_COLUMNS)}"
        )

    # Validate sort_order
    if sort_order not in ("asc", "desc"):
        raise HTTPException(
            status_code=400,
            detail="sort_order must be 'asc' or 'desc'."
        )

    # Sanitize string inputs
    search = _validate_string_param(search, MAX_SEARCH_LENGTH, "search")
    role = _validate_string_param(role, MAX_FILTER_LENGTH, "role")
    team = _validate_string_param(team, MAX_FILTER_LENGTH, "team")

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
    season: Optional[int] = Query(None, ge=2008, le=2030, description="Filter by season"),
    role: Optional[str] = Query(None, max_length=MAX_FILTER_LENGTH, description="Filter by role"),
    team: Optional[str] = Query(None, max_length=MAX_FILTER_LENGTH, description="Filter by team")
):
    """Retrieves top-level summary statistics for key metric highlight cards."""
    role = _validate_string_param(role, MAX_FILTER_LENGTH, "role")
    team = _validate_string_param(team, MAX_FILTER_LENGTH, "team")

    summary = get_overview_summary(season=season, role=role, team=team)
    return OverviewSummaryResponse(**summary)


@router.get("/{player_id}", response_model=List[PlayerStats])
def get_player_by_id(
    player_id: str = Path(..., min_length=1, max_length=20, description="Player ID (e.g. P001)")
):
    """Retrieves all season stats records for a specific player ID."""
    # Validate player_id format
    if not PLAYER_ID_PATTERN.match(player_id):
        raise HTTPException(
            status_code=400,
            detail="Invalid player ID format. Must be 1-20 alphanumeric characters."
        )

    history = get_player_history(player_id)
    if not history:
        raise HTTPException(status_code=404, detail="Player not found.")
    return history
