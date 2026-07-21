import pandas as pd

from app.services.momentum_engine import (
    EVENT_WEIGHTS,
    calculate_match_momentum,
    calculate_momentum_by_minute,
    get_event_weight,
    parse_match_minute,
)


def test_each_known_event_type_has_expected_weight():
    expected_weights = {
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

    assert EVENT_WEIGHTS == expected_weights


def test_unknown_event_type_has_zero_weight():
    assert get_event_weight("Unknown Event") == 0


def test_calculate_momentum_by_minute_scores_events_for_each_team():
    events = pd.DataFrame(
        [
            {"minute": 10, "team_id": 1, "event_type": "Goal"},
            {"minute": 10, "team_id": 1, "event_type": "Assist"},
            {"minute": 12, "team_id": 2, "event_type": "Yellow Card"},
        ]
    )

    momentum = calculate_momentum_by_minute(
        events,
        team_ids=[1, 2],
        final_minute=12,
        rolling_window=5,
    )

    team_1_minute_10 = momentum[
        (momentum["team_id"] == 1) & (momentum["minute"] == 10)
    ].iloc[0]
    team_2_minute_12 = momentum[
        (momentum["team_id"] == 2) & (momentum["minute"] == 12)
    ].iloc[0]

    assert team_1_minute_10["event_score"] == 7
    assert team_1_minute_10["momentum_score"] == 7
    assert team_2_minute_12["event_score"] == -1
    assert team_2_minute_12["momentum_score"] == -1


def test_rolling_window_keeps_recent_scores_only():
    events = pd.DataFrame(
        [
            {"minute": 1, "team_id": 1, "event_type": "Goal"},
            {"minute": 4, "team_id": 1, "event_type": "Goal"},
        ]
    )

    momentum = calculate_momentum_by_minute(
        events,
        team_ids=[1],
        final_minute=6,
        rolling_window=3,
    )

    minute_4 = momentum[momentum["minute"] == 4].iloc[0]
    minute_6 = momentum[momentum["minute"] == 6].iloc[0]

    assert minute_4["momentum_score"] == 5
    assert minute_6["momentum_score"] == 5


def test_empty_events_return_zero_momentum():
    events = pd.DataFrame(columns=["minute", "team_id", "event_type"])

    momentum = calculate_momentum_by_minute(events, team_ids=[1, 2], final_minute=2)

    assert len(momentum) == 6
    assert set(momentum["event_score"]) == {0}
    assert set(momentum["momentum_score"]) == {0.0}


def test_calculate_match_momentum_returns_real_match_timeline():
    momentum = calculate_match_momentum(1)

    assert not momentum.empty
    assert set(momentum.columns) == {
        "minute",
        "team_id",
        "event_score",
        "momentum_score",
    }
    assert set(momentum["team_id"]) == {1, 2}


def test_scheduled_match_returns_zero_momentum_for_both_teams():
    momentum = calculate_match_momentum(104)

    assert len(momentum) == 182
    assert set(momentum["event_score"]) == {0}
    assert set(momentum["momentum_score"]) == {0.0}


def test_parse_match_minute_handles_stoppage_time():
    assert parse_match_minute("90+6") == 96
    assert parse_match_minute("120+1") == 121
