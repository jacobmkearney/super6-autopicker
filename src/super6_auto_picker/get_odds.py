import requests
from dotenv import load_dotenv

API_KEY = os.getenv("ODDS_API_KEY")
BASE_URL = "https://api.the-odds-api.com/v4/sports/soccer_epl/odds"

def get_odds(market):
    url = f"{BASE_URL}?regions=uk&markets={market}&apiKey={API_KEY}"
    response = requests.get(url)
    response.raise_for_status()
    return response.json()

def get_prediction(odds_data, market_key, bookmaker_key="skybet", fallback=False):
    bookmaker_data = None
    
    # Try to find the requested bookmaker
    for bookmaker in odds_data[0].get("bookmakers", []):
        if bookmaker["key"] == bookmaker_key:
            bookmaker_data = bookmaker
            break
    
    # If not found and fallback is enabled, pick first bookmaker available
    if not bookmaker_data and fallback and odds_data[0].get("bookmakers"):
        bookmaker_data = odds_data[0]["bookmakers"][0]
    
    if not bookmaker_data:
        return {"market": market_key, "predictions": None, "most_likely": None, "reason": f"{bookmaker_key} not found"}
    
    # Find the correct market
    for market in bookmaker_data["markets"]:
        if market["key"] == market_key:
            outcomes = market["outcomes"]
            # Sort by decimal odds ascending (lower = more likely)
            outcomes_sorted = sorted(outcomes, key=lambda x: x["price"])
            most_likely = outcomes_sorted[0]
            return {
                "market": market_key,
                "bookmaker": bookmaker_data["title"],
                "predictions": outcomes,
                "most_likely": most_likely
            }
    return {"market": market_key, "predictions": None, "most_likely": None, "reason": f"{market_key} not found"}

# Call 1: Match winner (H2H)
h2h_odds = get_odds("h2h")
skybet_h2h = get_prediction(h2h_odds, "h2h", "skybet", fallback=True)
print("Sky Bet H2H Predictions:", skybet_h2h)

# Call 2: Total goals (Over/Under)
totals_odds = get_odds("totals")
skybet_totals = get_prediction(totals_odds, "totals", "skybet", fallback=True)
print("Sky Bet Totals Predictions:", skybet_totals)

