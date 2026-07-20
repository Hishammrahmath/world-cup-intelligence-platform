import pandas as pd
import pytest

from app.services.data_loader import (
    EXPECTED_MATCH_COUNT,
    REQUIRED_FILES,
    load_all_data,
    load_csv_file,
    validate_match_count,
)


def test_load_all_data_loads_required_csv_files():
    datasets = load_all_data()

    assert set(datasets.keys()) == set(REQUIRED_FILES.keys())

    for dataset in datasets.values():
        assert isinstance(dataset, pd.DataFrame)
        assert not dataset.empty


def test_matches_csv_contains_expected_match_count():
    datasets = load_all_data()

    assert len(datasets["matches"]) == EXPECTED_MATCH_COUNT


def test_missing_csv_file_has_clear_error(tmp_path):
    missing_file = tmp_path / "missing.csv"

    with pytest.raises(FileNotFoundError, match="Required CSV file is missing"):
        load_csv_file(missing_file)


def test_loaded_files_have_expected_columns():
    datasets = load_all_data()

    assert "team_id" in datasets["teams"].columns
    assert "match_id" in datasets["matches"].columns
    assert "event_type" in datasets["events"].columns
    assert "possession_pct" in datasets["team_stats"].columns


def test_validate_match_count_rejects_wrong_count():
    matches = pd.DataFrame({"match_id": [1, 2, 3]})

    with pytest.raises(ValueError, match="Expected 104 matches"):
        validate_match_count(matches)
