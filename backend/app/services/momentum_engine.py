import pandas as pd

from app.services.match_service import get_match_events, get_match_teams


EVENT_WEIGHTS = {
    "Goal": 5,
    "Assist": 2,
    "Shot on Target": 2,
    "Shot": 1,
    "Corner": 1,
    "VAR Review": 1,
    "Penalty Shootout Goal": 3,
    "Penalty Shootout Miss": -3,
    "Yellow Card": -1,
    "Red Card": -4,
}

DEFAULT_FINAL_MINUTE = 90
DEFAULT_ROLLING_WINDOW = 5


def get_event_weight(event_type: str) -> int:
    return EVENT_WEIGHTS.get(event_type, 0)


def calculate_momentum_by_minute(
    events: pd.DataFrame,
    team_ids: list[int],
    final_minute: int = DEFAULT_FINAL_MINUTE,
    rolling_window: int = DEFAULT_ROLLING_WINDOW,
) -> pd.DataFrame:
    prepared_events = _prepare_events(events)

    if not prepared_events.empty:
        final_minute = max(final_minute, int(prepared_events["minute"].max()))

    timeline = _build_empty_timeline(team_ids, final_minute)

    if prepared_events.empty:
        timeline["event_score"] = 0
        timeline["momentum_score"] = 0.0
        return timeline

    event_scores = _calculate_event_scores(prepared_events)
    timeline = timeline.merge(event_scores, on=["minute", "team_id"], how="left")
    timeline["event_score"] = timeline["event_score"].fillna(0).astype(int)
    timeline["momentum_score"] = (
        timeline.sort_values("minute")
        .groupby("team_id")["event_score"]
        .transform(lambda scores: scores.rolling(rolling_window, min_periods=1).sum())
    )

    return timeline


def calculate_match_momentum(match_id: int) -> pd.DataFrame:
    events = get_match_events(match_id)
    teams = get_match_teams(match_id)
    team_ids = teams["team_id"].tolist()

    return calculate_momentum_by_minute(events, team_ids)


def parse_match_minute(minute: int | str) -> int:
    minute_text = str(minute).strip()

    if "+" in minute_text:
        base_minute, added_time = minute_text.split("+", maxsplit=1)
        return int(base_minute) + int(added_time)

    return int(minute_text)


def _prepare_events(events: pd.DataFrame) -> pd.DataFrame:
    prepared_events = events.copy()

    if prepared_events.empty:
        return prepared_events

    prepared_events["minute"] = prepared_events["minute"].apply(parse_match_minute)
    prepared_events["team_id"] = prepared_events["team_id"].astype(int)

    return prepared_events


def _build_empty_timeline(team_ids: list[int], final_minute: int) -> pd.DataFrame:
    rows = [
        {"minute": minute, "team_id": team_id}
        for minute in range(final_minute + 1)
        for team_id in team_ids
    ]

    return pd.DataFrame(rows)


def _calculate_event_scores(events: pd.DataFrame) -> pd.DataFrame:
    scored_events = events.copy()
    scored_events["event_score"] = scored_events["event_type"].apply(get_event_weight)

    return (
        scored_events.groupby(["minute", "team_id"], as_index=False)["event_score"]
        .sum()
        .sort_values(["minute", "team_id"])
    )
