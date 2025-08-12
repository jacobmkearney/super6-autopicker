import os
import json
import requests
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("ODDS_API_KEY")
BASE_URL = "https://api.the-odds-api.com/v4/sports/soccer_epl/odds"

def get_odds(market):
    url = f"{BASE_URL}?regions=uk&markets={market}&apiKey={API_KEY}"
    response = requests.get(url)
    response.raise_for_status()
    return response.json()

def get_prediction_for_all(odds_data, market_key, bookmaker_key="skybet", fallback=False):
    results = []
    for match in odds_data:
        bookmaker_data = next((b for b in match.get("bookmakers", []) if b["key"] == bookmaker_key), None)

        if not bookmaker_data and fallback and match.get("bookmakers"):
            bookmaker_data = match["bookmakers"][0]

        if not bookmaker_data:
            results.append({
                "home_team": match["home_team"],
                "away_team": match["away_team"],
                "market": market_key,
                "predictions": None,
                "most_likely": None,
                "reason": f"{bookmaker_key} not found"
            })
            continue

        market = next((m for m in bookmaker_data["markets"] if m["key"] == market_key), None)
        if market:
            outcomes = market["outcomes"]
            outcomes_sorted = sorted(outcomes, key=lambda x: x["price"])
            most_likely = outcomes_sorted[0]
            results.append({
                "home_team": match["home_team"],
                "away_team": match["away_team"],
                "market": market_key,
                "bookmaker": bookmaker_data["title"],
                "predictions": outcomes,
                "most_likely": most_likely
            })
    return results

def save_json(data, filename):
    with open(filename, "w") as f:
        json.dump(data, f, indent=2)

if __name__ == "__main__":
    # Fetch all matches H2H
    h2h_odds = get_odds("h2h")
    skybet_h2h_all = get_prediction_for_all(h2h_odds, "h2h", "skybet", fallback=True)
    save_json(skybet_h2h_all, "data/h2h_predictions.json")
    print("Saved H2H predictions to h2h_predictions.json")

    # Fetch all matches Totals
    totals_odds = get_odds("totals")
    skybet_totals_all = get_prediction_for_all(totals_odds, "totals", "skybet", fallback=True)
    save_json(skybet_totals_all, "data/totals_predictions.json")
    print("Saved Totals predictions to totals_predictions.json")
