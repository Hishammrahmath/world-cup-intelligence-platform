"""Export every match's dashboard data to static JSON for the hosted frontend.

Uses the same services as the FastAPI endpoints, so the static site shows the
same momentum, turning points, and summaries the API returns. Needs only pandas.
Output goes to frontend/public/data/.

Usage (from the backend folder):
    python -m scripts.export_static
"""

import json
from pathlib import Path

import pandas as pd

from app.services.match_service import (
    get_all_matches,
    get_match_events,
    get_match_team_stats,
    get_match_teams,
)
from app.services.match_summary import build_match_summary
from app.services.momentum_engine import calculate_match_momentum
from app.services.turning_points import find_match_turning_points

OUTPUT_DIR = Path(__file__).resolve().parents[2] / "frontend" / "public" / "data"


def _records(dataframe: pd.DataFrame) -> list[dict]:
    cleaned = dataframe.astype(object).where(pd.notna(dataframe), None)
    return cleaned.to_dict(orient="records")


def _record(series: pd.Series) -> dict:
    cleaned = series.astype(object).where(pd.notna(series), None)
    return cleaned.to_dict()


def _to_json(payload) -> str:
    def default(value):
        if hasattr(value, "item"):
            return value.item()
        if pd.isna(value):
            return None
        return str(value)

    return json.dumps(payload, default=default, separators=(",", ":"))


def main() -> None:
    matches_dir = OUTPUT_DIR / "matches"
    matches_dir.mkdir(parents=True, exist_ok=True)

    matches = get_all_matches()
    index = []

    for _, match in matches.iterrows():
        match_id = int(match["match_id"])
        teams = get_match_teams(match_id)
        turning_points = find_match_turning_points(match_id)
        payload = {
            "match": _record(match),
            "teams": _records(teams),
            "events": _records(get_match_events(match_id)),
            "stats": _records(get_match_team_stats(match_id)),
            "momentum": _records(calculate_match_momentum(match_id)),
            "turning_points": turning_points,
            "summary": build_match_summary(match_id),
        }
        (matches_dir / f"{match_id}.json").write_text(_to_json(payload))

        names = {int(row["team_id"]): row for _, row in teams.iterrows()}
        home = names.get(int(match["home_team_id"]))
        away = names.get(int(match["away_team_id"]))
        index.append(
            {
                "match_id": match_id,
                "date": match["date"],
                "home_team": None if home is None else home["team_name"],
                "home_code": None if home is None else home["fifa_code"],
                "away_team": None if away is None else away["team_name"],
                "away_code": None if away is None else away["fifa_code"],
                "home_score": match["home_score"],
                "away_score": match["away_score"],
                "turning_point_count": len(turning_points),
            }
        )

    (OUTPUT_DIR / "matches.json").write_text(_to_json({"matches": index}))
    print(f"Exported {len(index)} matches to {OUTPUT_DIR}")


if __name__ == "__main__":
    main()
