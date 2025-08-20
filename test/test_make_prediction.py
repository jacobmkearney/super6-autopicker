import pytest
from unittest import mock
from src.super6_auto_picker.make_prediction import predict_all_matches
import json

@mock.patch('src.super6_auto_picker.make_prediction.load_json')
def test_predict_all_matches(mock_load_json):
    # Load mock JSON data from files
    with open('test/data/h2h_predictions.json', 'r') as h2h_file:
        h2h_data = json.load(h2h_file)
    with open('test/data/totals_predictions.json', 'r') as totals_file:
        totals_data = json.load(totals_file)

    mock_load_json.side_effect = [h2h_data, totals_data]

    predictions = predict_all_matches()
    assert len(predictions) == 1
    assert predictions[0]["Team A"] is not None
    assert predictions[0]["Team B"] is not None
    assert predictions[0]["probability"] is not None

@mock.patch('src.super6_auto_picker.make_prediction.load_json')
def test_correct_score_prediction(mock_load_json):
    # Mock the JSON data
    mock_load_json.side_effect = [
        [{"home_team": "Team A", "away_team": "Team B", "predictions": [{"name": "Team A", "price": 2.0}, {"name": "draw", "price": 3.0}, {"name": "Team B", "price": 4.0}]}],
        [{"home_team": "Team A", "away_team": "Team B", "market": "totals", "bookmaker": "MockBookmaker", "predictions": [{"name": "Over", "price": 1.5, "point": 2.5}, {"name": "Under", "price": 2.5, "point": 2.5}], "most_likely": {"name": "Over", "price": 1.5, "point": 2.5}}]
    ]

    predictions = predict_all_matches()
    assert len(predictions) == 1
    assert predictions[0]["Team A"] == 1  # Example expected score
    assert predictions[0]["Team B"] == 0  # Example expected score
    assert predictions[0]["probability"] is not None

@mock.patch('src.super6_auto_picker.make_prediction.load_json')
def test_handling_missing_data(mock_load_json):
    # Mock the JSON data with missing predictions
    mock_load_json.side_effect = [
        [{"home_team": "Team A", "away_team": "Team B", "predictions": []}],  # Missing predictions
        [{"home_team": "Team A", "away_team": "Team B", "market": "totals", "bookmaker": "MockBookmaker", "predictions": [{"name": "Over", "price": 1.5, "point": 2.5}, {"name": "Under", "price": 2.5, "point": 2.5}], "most_likely": {"name": "Over", "price": 1.5, "point": 2.5}}]
    ]

    predictions = predict_all_matches()
    assert len(predictions) == 1
    assert predictions[0]["Team A"] is None  # Expect None due to missing data
    assert predictions[0]["Team B"] is None  # Expect None due to missing data
    assert predictions[0]["probability"] is None

@mock.patch('src.super6_auto_picker.make_prediction.load_json')
def test_edge_cases(mock_load_json):
    # Mock the JSON data with edge case prices
    mock_load_json.side_effect = [
        [{"home_team": "Team A", "away_team": "Team B", "predictions": [{"name": "Team A", "price": 0.0}, {"name": "draw", "price": 1000000.0}, {"name": "Team B", "price": -1.0}]}],
        [{"home_team": "Team A", "away_team": "Team B", "market": "totals", "bookmaker": "MockBookmaker", "predictions": [{"name": "Over", "price": 0.0, "point": 2.5}, {"name": "Under", "price": -1.0, "point": 2.5}], "most_likely": {"name": "Over", "price": 0.0, "point": 2.5}}]
    ]

    predictions = predict_all_matches()
    assert len(predictions) == 1
    assert predictions[0]["Team A"] is None  # Expect None due to invalid prices
    assert predictions[0]["Team B"] is None  # Expect None due to invalid prices
    assert predictions[0]["probability"] is None

@mock.patch('src.super6_auto_picker.make_prediction.load_json')
def test_error_handling(mock_load_json):
    # Mock the JSON data with missing keys
    mock_load_json.side_effect = [
        [{"home_team": "Team A", "away_team": "Team B"}],  # Missing predictions key
        [{"home_team": "Team A", "away_team": "Team B", "market": "totals", "bookmaker": "MockBookmaker", "predictions": [{"name": "Over", "price": 1.5, "point": 2.5}, {"name": "Under", "price": 2.5, "point": 2.5}], "most_likely": {"name": "Over", "price": 1.5, "point": 2.5}}]
    ]

    predictions = predict_all_matches()
    assert len(predictions) == 1
    assert predictions[0]["Team A"] is None  # Expect None due to missing keys
    assert predictions[0]["Team B"] is None  # Expect None due to missing keys
    assert predictions[0]["probability"] is None