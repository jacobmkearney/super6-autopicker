import pytest
from unittest import mock
from src.super6_auto_picker.get_odds import get_odds, get_prediction_for_all
import requests

@mock.patch('src.super6_auto_picker.get_odds.requests.get')
def test_get_odds_success(mock_get):
    # Given a valid market and a successful API response
    mock_get.return_value.status_code = 200
    mock_get.return_value.json.return_value = [{"key": "value"}]
    
    # When get_odds is called
    result = get_odds("h2h")
    
    # Then it returns the expected JSON data
    assert result == [{"key": "value"}]

@mock.patch('src.super6_auto_picker.get_odds.requests.get')
def test_get_odds_http_error(mock_get):
    # Given a valid market but the API returns an HTTP error
    mock_get.return_value.raise_for_status.side_effect = requests.exceptions.HTTPError
    
    # When get_odds is called
    with pytest.raises(requests.exceptions.HTTPError):
        get_odds("h2h")
    
    # Then it raises an HTTPError

@mock.patch('src.super6_auto_picker.get_odds.requests.get')
def test_get_odds_network_error(mock_get):
    # Given a valid market but a network error occurs
    mock_get.side_effect = requests.exceptions.ConnectionError
    
    # When get_odds is called
    with pytest.raises(requests.exceptions.ConnectionError):
        get_odds("h2h")
    
    # Then it raises a ConnectionError


def test_get_prediction_for_all_valid_data():
    # Given valid odds data
    odds_data = [{
        "home_team": "Team A",
        "away_team": "Team B",
        "bookmakers": [{
            "key": "skybet",
            "title": "Sky Bet",
            "markets": [{
                "key": "h2h",
                "outcomes": [
                    {"name": "Team A", "price": 2.0},
                    {"name": "draw", "price": 3.0},
                    {"name": "Team B", "price": 4.0}
                ]
            }]
        }]
    }]
    
    # When get_prediction_for_all is called
    result = get_prediction_for_all(odds_data, "h2h")
    
    # Then it returns the expected predictions
    assert len(result) == 1
    assert result[0]["home_team"] == "Team A"
    assert result[0]["away_team"] == "Team B"
    assert result[0]["most_likely"]["name"] == "Team A"


def test_get_prediction_for_all_missing_bookmaker():
    # Given odds data with missing bookmaker
    odds_data = [{
        "home_team": "Team A",
        "away_team": "Team B",
        "bookmakers": []  # No bookmakers
    }]
    
    # When get_prediction_for_all is called
    result = get_prediction_for_all(odds_data, "h2h")
    
    # Then it returns None for predictions and a reason
    assert len(result) == 1
    assert result[0]["predictions"] is None
    assert result[0]["reason"] == "skybet not found"


def test_get_prediction_for_all_fallback():
    # Given odds data with a fallback bookmaker
    odds_data = [{
        "home_team": "Team A",
        "away_team": "Team B",
        "bookmakers": [{
            "key": "other",
            "title": "Other Bookmaker",
            "markets": [{
                "key": "h2h",
                "outcomes": [
                    {"name": "Team A", "price": 2.0},
                    {"name": "draw", "price": 3.0},
                    {"name": "Team B", "price": 4.0}
                ]
            }]
        }]
    }]
    
    # When get_prediction_for_all is called with fallback
    result = get_prediction_for_all(odds_data, "h2h", fallback=True)
    
    # Then it uses the fallback bookmaker
    assert len(result) == 1
    assert result[0]["home_team"] == "Team A"
    assert result[0]["away_team"] == "Team B"
    assert result[0]["most_likely"]["name"] == "Team A"