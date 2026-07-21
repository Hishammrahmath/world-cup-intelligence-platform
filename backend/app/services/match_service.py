import pandas as pd

from app.services.data_loader import load_all_data


def get_all_matches() -> pd.DataFrame:
    datasets = load_all_data()
    return datasets["matches"]


def get_match_by_id(match_id: int) -> pd.Series:
    matches = get_all_matches()
    matching_rows = matches[matches["match_id"] == match_id]

    if matching_rows.empty:
        raise ValueError(f"Match not found for match_id: {match_id}")

    return matching_rows.iloc[0]


def get_match_teams(match_id: int) -> pd.DataFrame:
    datasets = load_all_data()
    match = get_match_by_id(match_id)
    team_ids = [match["home_team_id"], match["away_team_id"]]

    return datasets["teams"][datasets["teams"]["team_id"].isin(team_ids)]


def get_match_events(match_id: int) -> pd.DataFrame:
    get_match_by_id(match_id)
    datasets = load_all_data()

    return datasets["events"][datasets["events"]["match_id"] == match_id]


def get_match_team_stats(match_id: int) -> pd.DataFrame:
    get_match_by_id(match_id)
    datasets = load_all_data()

    return datasets["team_stats"][datasets["team_stats"]["match_id"] == match_id]
