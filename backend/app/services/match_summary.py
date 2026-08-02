import pandas as pd

from app.services.match_service import (
    get_match_by_id,
    get_match_events,
    get_match_team_stats,
    get_match_teams,
)
from app.services.turning_points import find_match_turning_points


def build_match_summary(match_id: int) -> dict:
    match = get_match_by_id(match_id)
    teams = get_match_teams(match_id)
    events = get_match_events(match_id)
    stats = get_match_team_stats(match_id)
    turning_points = find_match_turning_points(match_id)

    home_team = _team_record(teams, int(match["home_team_id"]))
    away_team = _team_record(teams, int(match["away_team_id"]))

    facts = {
        "match_id": int(match["match_id"]),
        "status": match["status"],
        "result_type": _none_if_missing(match.get("result_type")),
        "date": match["date"],
        "home_team": home_team,
        "away_team": away_team,
        "score": {
            "home": int(match["home_score"]),
            "away": int(match["away_score"]),
        },
        "event_count": len(events),
        "goal_count": _count_events(events, "Goal"),
        "card_count": _count_events(events, "Yellow Card") + _count_events(events, "Red Card"),
        "turning_point_count": len(turning_points),
        "top_stat_notes": _build_stat_notes(stats, teams),
    }

    return {
        "facts": facts,
        "fan_explanation": _build_fan_explanation(facts),
        "player_explanation": _build_player_explanation(facts),
        "coach_explanation": _build_coach_explanation(facts),
        "limits": [
            "This explanation uses only calculated match facts.",
            "Nearby events are not treated as proven causes.",
        ],
    }


def _team_record(teams: pd.DataFrame, team_id: int) -> dict:
    row = teams[teams["team_id"] == team_id].iloc[0]
    return {
        "team_id": int(row["team_id"]),
        "team_name": row["team_name"],
        "fifa_code": row["fifa_code"],
    }


def _count_events(events: pd.DataFrame, event_type: str) -> int:
    if events.empty:
        return 0

    return int((events["event_type"] == event_type).sum())


def _build_stat_notes(stats: pd.DataFrame, teams: pd.DataFrame) -> list[str]:
    if stats.empty:
        return []

    notes = []
    for column, label in [
        ("possession_pct", "possession"),
        ("total_shots", "total shots"),
        ("shots_on_target", "shots on target"),
        ("corners", "corners"),
    ]:
        leader = stats.sort_values(column, ascending=False).iloc[0]
        team = _team_record(teams, int(leader["team_id"]))
        notes.append(f"{team['team_name']} led {label} with {leader[column]}.")

    return notes


def _build_fan_explanation(facts: dict) -> str:
    home = facts["home_team"]["team_name"]
    away = facts["away_team"]["team_name"]
    score = facts["score"]

    return (
        f"{home} played {away} and the match finished {score['home']}-{score['away']}. "
        f"The dataset lists {facts['event_count']} tracked events, including "
        f"{facts['goal_count']} goals and {facts['turning_point_count']} momentum turning points."
    )


def _build_player_explanation(facts: dict) -> str:
    return (
        f"This match has {facts['event_count']} tracked events. Review the timeline around "
        f"the {facts['turning_point_count']} detected turning points to understand when match pressure changed."
    )


def _build_coach_explanation(facts: dict) -> str:
    stat_text = " ".join(facts["top_stat_notes"])
    return (
        f"The model detected {facts['turning_point_count']} sustained momentum changes. "
        f"Use those windows as review candidates, then compare them with team stats. {stat_text}"
    ).strip()


def _none_if_missing(value):
    if pd.isna(value):
        return None

    return value
