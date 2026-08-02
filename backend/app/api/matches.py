import pandas as pd
from fastapi import APIRouter, HTTPException

from app.services.match_service import (
    get_all_matches,
    get_match_by_id,
    get_match_events,
    get_match_team_stats,
    get_match_teams,
)
from app.services.match_summary import build_match_summary
from app.services.momentum_engine import calculate_match_momentum
from app.services.turning_points import find_match_turning_points


router = APIRouter(prefix="/matches", tags=["matches"])


def _dataframe_to_records(dataframe: pd.DataFrame) -> list[dict]:
    cleaned = dataframe.astype(object).where(pd.notna(dataframe), None)
    return cleaned.to_dict(orient="records")


def _series_to_record(series: pd.Series) -> dict:
    cleaned = series.astype(object).where(pd.notna(series), None)
    return cleaned.to_dict()


def _not_found_error(match_id: int) -> HTTPException:
    return HTTPException(status_code=404, detail=f"Match not found for match_id: {match_id}")


@router.get("")
def list_matches() -> dict:
    return {"matches": _dataframe_to_records(get_all_matches())}


@router.get("/{match_id}")
def get_match(match_id: int) -> dict:
    try:
        match = get_match_by_id(match_id)
    except ValueError:
        raise _not_found_error(match_id)

    return {"match": _series_to_record(match)}


@router.get("/{match_id}/teams")
def list_match_teams(match_id: int) -> dict:
    try:
        teams = get_match_teams(match_id)
    except ValueError:
        raise _not_found_error(match_id)

    return {"teams": _dataframe_to_records(teams)}


@router.get("/{match_id}/events")
def list_match_events(match_id: int) -> dict:
    try:
        events = get_match_events(match_id)
    except ValueError:
        raise _not_found_error(match_id)

    return {"events": _dataframe_to_records(events)}


@router.get("/{match_id}/stats")
def list_match_team_stats(match_id: int) -> dict:
    try:
        stats = get_match_team_stats(match_id)
    except ValueError:
        raise _not_found_error(match_id)

    return {"stats": _dataframe_to_records(stats)}


@router.get("/{match_id}/momentum")
def get_match_momentum(match_id: int) -> dict:
    try:
        momentum = calculate_match_momentum(match_id)
    except ValueError:
        raise _not_found_error(match_id)

    return {"momentum": _dataframe_to_records(momentum)}


@router.get("/{match_id}/turning-points")
def get_match_turning_points(match_id: int) -> dict:
    try:
        turning_points = find_match_turning_points(match_id)
    except ValueError:
        raise _not_found_error(match_id)

    return {"turning_points": turning_points}


@router.get("/{match_id}/summary")
def get_match_summary(match_id: int) -> dict:
    try:
        summary = build_match_summary(match_id)
    except ValueError:
        raise _not_found_error(match_id)

    return {"summary": summary}
