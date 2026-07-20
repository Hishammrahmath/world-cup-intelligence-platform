from pathlib import Path

import pandas as pd


REQUIRED_FILES = {
    "teams": "teams.csv",
    "matches": "matches.csv",
    "events": "match_events.csv",
    "team_stats": "match_team_stats.csv",
}

EXPECTED_MATCH_COUNT = 104


def get_project_root() -> Path:
    return Path(__file__).resolve().parents[3]


def get_raw_data_dir() -> Path:
    return get_project_root() / "data" / "raw"


def load_csv_file(file_path: Path) -> pd.DataFrame:
    if not file_path.exists():
        raise FileNotFoundError(f"Required CSV file is missing: {file_path}")

    return pd.read_csv(file_path)


def load_all_data(raw_data_dir: Path | None = None) -> dict[str, pd.DataFrame]:
    data_dir = raw_data_dir or get_raw_data_dir()

    return {
        dataset_name: load_csv_file(data_dir / filename)
        for dataset_name, filename in REQUIRED_FILES.items()
    }


def validate_match_count(matches: pd.DataFrame) -> None:
    actual_count = len(matches)

    if actual_count != EXPECTED_MATCH_COUNT:
        raise ValueError(
            f"Expected {EXPECTED_MATCH_COUNT} matches, but found {actual_count}."
        )


def print_dataset_summary(raw_data_dir: Path | None = None) -> None:
    datasets = load_all_data(raw_data_dir)
    validate_match_count(datasets["matches"])

    for dataset_name, dataframe in datasets.items():
        columns = ", ".join(dataframe.columns)
        print(f"{dataset_name}: {len(dataframe)} rows")
        print(f"columns: {columns}")
