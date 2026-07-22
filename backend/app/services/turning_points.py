import pandas as pd

from app.services.match_service import get_match_events
from app.services.momentum_engine import calculate_match_momentum, parse_match_minute


DEFAULT_LOOKBACK_MINUTES = 5
DEFAULT_MINIMUM_CHANGE = 5
DEFAULT_EVENT_WINDOW = 2


def find_turning_points(
    momentum: pd.DataFrame,
    events: pd.DataFrame,
    lookback_minutes: int = DEFAULT_LOOKBACK_MINUTES,
    minimum_change: int = DEFAULT_MINIMUM_CHANGE,
    event_window: int = DEFAULT_EVENT_WINDOW,
) -> list[dict]:
    if momentum.empty:
        return []

    prepared_events = _prepare_events(events)
    turning_points = []

    for team_id, team_momentum in momentum.groupby("team_id"):
        team_momentum = team_momentum.sort_values("minute").reset_index(drop=True)

        for index, row in team_momentum.iterrows():
            start_minute = int(row["minute"]) - lookback_minutes

            if start_minute < 0:
                continue

            previous_rows = team_momentum[team_momentum["minute"] == start_minute]

            if previous_rows.empty:
                continue

            previous_score = previous_rows.iloc[0]["momentum_score"]
            current_score = row["momentum_score"]
            change_size = current_score - previous_score

            if change_size >= minimum_change:
                turning_points.append(
                    {
                        "start_minute": start_minute,
                        "end_minute": int(row["minute"]),
                        "team_id": int(team_id),
                        "change_size": float(change_size),
                        "nearby_events": _get_nearby_events(
                            prepared_events,
                            int(row["minute"]),
                            event_window,
                        ),
                    }
                )

    return _remove_overlapping_turning_points(turning_points)


def find_match_turning_points(match_id: int) -> list[dict]:
    momentum = calculate_match_momentum(match_id)
    events = get_match_events(match_id)

    return find_turning_points(momentum, events)


def _prepare_events(events: pd.DataFrame) -> pd.DataFrame:
    prepared_events = events.copy()

    if prepared_events.empty:
        return prepared_events

    prepared_events["minute"] = prepared_events["minute"].apply(parse_match_minute)
    prepared_events["team_id"] = prepared_events["team_id"].astype(int)

    return prepared_events


def _get_nearby_events(
    events: pd.DataFrame,
    minute: int,
    event_window: int,
) -> list[dict]:
    if events.empty:
        return []

    nearby_events = events[
        events["minute"].between(minute - event_window, minute + event_window)
    ]

    return nearby_events.to_dict(orient="records")


def _remove_overlapping_turning_points(turning_points: list[dict]) -> list[dict]:
    sorted_points = sorted(
        turning_points,
        key=lambda point: (point["team_id"], point["start_minute"], -point["change_size"]),
    )
    filtered_points = []

    for point in sorted_points:
        overlaps_existing = any(
            point["team_id"] == existing["team_id"]
            and point["start_minute"] <= existing["end_minute"]
            and point["end_minute"] >= existing["start_minute"]
            for existing in filtered_points
        )

        if not overlaps_existing:
            filtered_points.append(point)

    return filtered_points
