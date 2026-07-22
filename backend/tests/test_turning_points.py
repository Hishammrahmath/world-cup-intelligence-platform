import pandas as pd

from app.services.turning_points import find_match_turning_points, find_turning_points


def test_find_turning_points_detects_large_sustained_change():
    momentum = pd.DataFrame(
        [
            {"minute": 0, "team_id": 1, "event_score": 0, "momentum_score": 0},
            {"minute": 5, "team_id": 1, "event_score": 5, "momentum_score": 6},
        ]
    )
    events = pd.DataFrame(
        [
            {
                "event_id": 1,
                "match_id": 1,
                "minute": 5,
                "event_type": "Goal",
                "team_id": 1,
                "player_id": 9,
            }
        ]
    )

    turning_points = find_turning_points(momentum, events)

    assert len(turning_points) == 1
    assert turning_points[0]["start_minute"] == 0
    assert turning_points[0]["end_minute"] == 5
    assert turning_points[0]["team_id"] == 1
    assert turning_points[0]["change_size"] == 6


def test_find_turning_points_ignores_small_change():
    momentum = pd.DataFrame(
        [
            {"minute": 0, "team_id": 1, "event_score": 0, "momentum_score": 0},
            {"minute": 5, "team_id": 1, "event_score": 2, "momentum_score": 2},
        ]
    )
    events = pd.DataFrame(columns=["minute", "event_type", "team_id"])

    turning_points = find_turning_points(momentum, events)

    assert turning_points == []


def test_find_turning_points_adds_nearby_events_only():
    momentum = pd.DataFrame(
        [
            {"minute": 0, "team_id": 1, "event_score": 0, "momentum_score": 0},
            {"minute": 5, "team_id": 1, "event_score": 5, "momentum_score": 5},
        ]
    )
    events = pd.DataFrame(
        [
            {"minute": "4", "event_type": "Assist", "team_id": 1},
            {"minute": "5", "event_type": "Goal", "team_id": 1},
            {"minute": "20", "event_type": "Yellow Card", "team_id": 2},
        ]
    )

    turning_points = find_turning_points(momentum, events, event_window=2)

    nearby_event_types = {
        event["event_type"] for event in turning_points[0]["nearby_events"]
    }
    assert nearby_event_types == {"Assist", "Goal"}


def test_find_turning_points_handles_empty_momentum():
    momentum = pd.DataFrame(columns=["minute", "team_id", "momentum_score"])
    events = pd.DataFrame(columns=["minute", "event_type", "team_id"])

    assert find_turning_points(momentum, events) == []


def test_find_match_turning_points_returns_list_for_real_match():
    turning_points = find_match_turning_points(1)

    assert isinstance(turning_points, list)


def test_scheduled_match_has_no_turning_points():
    turning_points = find_match_turning_points(104)

    assert turning_points == []
