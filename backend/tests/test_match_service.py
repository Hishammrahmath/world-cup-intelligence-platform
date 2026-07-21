import pytest

from app.services.match_service import (
    get_all_matches,
    get_match_by_id,
    get_match_events,
    get_match_team_stats,
    get_match_teams,
)


def test_get_all_matches_returns_104_matches():
    matches = get_all_matches()

    assert len(matches) == 104


def test_get_match_by_id_returns_one_match():
    match = get_match_by_id(1)

    assert match["match_id"] == 1
    assert match["home_team_id"] == 1
    assert match["away_team_id"] == 2


def test_get_match_by_id_rejects_unknown_match():
    with pytest.raises(ValueError, match="Match not found"):
        get_match_by_id(999)


def test_get_match_teams_returns_home_and_away_teams():
    teams = get_match_teams(1)

    assert len(teams) == 2
    assert set(teams["team_id"]) == {1, 2}


def test_get_match_events_returns_events_for_match():
    events = get_match_events(1)

    assert not events.empty
    assert set(events["match_id"]) == {1}


def test_get_match_team_stats_returns_stats_for_match():
    stats = get_match_team_stats(1)

    assert len(stats) == 2
    assert set(stats["match_id"]) == {1}


def test_scheduled_match_can_have_no_events_or_stats():
    events = get_match_events(104)
    stats = get_match_team_stats(104)

    assert events.empty
    assert stats.empty
