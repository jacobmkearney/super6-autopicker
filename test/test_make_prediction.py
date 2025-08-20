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