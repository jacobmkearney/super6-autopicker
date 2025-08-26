import json
import logging
import math
from pathlib import Path
from src.super6_auto_picker.utils.file_utils import save_json

logger = logging.getLogger(__name__)

DATA_DIR = Path("data")

def result_type(home_goals, away_goals):
    if home_goals > away_goals:
        return "home"
    elif home_goals < away_goals:
        return "away"
    else:
        return "draw"
        
def implied_prob(price: float) -> float:
    if price == 0:
        return 0.0  # Return zero probability if price is zero
    """
    Converts decimal odds (eg 1.5) to implied probability (eg 0.6667)
    """
    return 1.0 / price

def normalize_probs(probs: list[float]) -> list[float]:
    """
    Bookies builds in margins, this function normalizes the probabilities to sum to 1
    """
    total = sum(probs)
    if total == 0:
        return [0 for _ in probs]  # Return zero probabilities if total is zero
    return [p / total for p in probs]

def estimate_lambdas(p_home, p_draw, p_away, p_over, p_under, goal_line):
    """
    Estimated the expected goals for each team based on bookies odds on result and goal lines
    """
    exp_total_goals = (p_over * (goal_line + 0.5)) + (p_under * (goal_line - 0.5))
    home_ratio = p_home / (p_home + p_away)
    exp_goals_home = exp_total_goals * home_ratio
    exp_goals_away = exp_total_goals - exp_goals_home
    return exp_goals_home, exp_goals_away

def poisson_prob(lmbda, k):
    """
    calculates the probability of a team scoring k goals given the expected goals using the Poisson distribution
    """
    return (math.exp(-lmbda) * (lmbda ** k)) / math.factorial(k)

def expected_points_for_guess(guess_home, guess_away, exp_goals_home, exp_goals_away, max_goals=5):
    guess_result = result_type(guess_home, guess_away)
    ev = 0.0

    for h in range(max_goals + 1):
        for a in range(max_goals + 1):
            p = poisson_prob(exp_goals_home, h) * poisson_prob(exp_goals_away, a)

            if (h, a) == (guess_home, guess_away):
                ev += 5 * p
            elif result_type(h, a) == guess_result:
                ev += 2 * p

    return ev

def best_expected_points_score(exp_goals_home, exp_goals_away, max_goals=5):
    best_score = None
    best_ev = -1.0
    best_prob = 0.0

    for h in range(max_goals + 1):
        for a in range(max_goals + 1):
            ev = expected_points_for_guess(h, a, exp_goals_home, exp_goals_away, max_goals)
            p_exact = poisson_prob(exp_goals_home, h) * poisson_prob(exp_goals_away, a)

            if ev > best_ev:
                best_ev = ev
                best_prob = p_exact
                best_score = (h, a)

    return best_score, best_prob, best_ev

def predict_score(h2h_dict, totals_dict):
    """
    Predict the most likely score for a single match using bookmaker odds.

    - Converts head-to-head odds (home/draw/away) into probabilities.
    - Converts over/under odds into expected total goals.
    - Splits expected goals between teams.
    - Finds the most likely scoreline using Poisson probabilities.

    Returns:
        Dict with predicted goals and probability, e.g.:
        {
            "HomeTeam": 1,
            "AwayTeam": 0,
            "probability": 0.1152
        }
    """
    home_team = h2h_dict["home_team"]
    away_team = h2h_dict["away_team"]

    if not h2h_dict["predictions"] or not totals_dict["predictions"]:
        return {home_team: None, away_team: None, "probability": None, "expectedPoints": None}


    # Map odds to correct teams
    try:
        home_price = next(o["price"] for o in h2h_dict["predictions"] if o["name"] == home_team)
        away_price = next(o["price"] for o in h2h_dict["predictions"] if o["name"] == away_team)
        draw_price = next(o["price"] for o in h2h_dict["predictions"] if o["name"].lower() == "draw")

        # Check for invalid prices
        if home_price <= 0 or away_price <= 0 or draw_price <= 0:
            return {home_team: None, away_team: None, "probability": None}
    except (StopIteration, KeyError):
        return {home_team: None, away_team: None, "probability": None}

    h2h_probs = normalize_probs([implied_prob(home_price), implied_prob(draw_price), implied_prob(away_price)])
    p_home, p_draw, p_away = h2h_probs

    # Totals
    try:
        over_price = next(o["price"] for o in totals_dict["predictions"] if o["name"].lower() == "over")
        under_price = next(o["price"] for o in totals_dict["predictions"] if o["name"].lower() == "under")
        goal_line = totals_dict["predictions"][0]["point"]

        # Check for invalid prices
        if over_price <= 0 or under_price <= 0:
            return {home_team: None, away_team: None, "probability": None}
    except (StopIteration, KeyError):
        return {home_team: None, away_team: None, "probability": None}

    totals_probs = normalize_probs([implied_prob(over_price), implied_prob(under_price)])
    p_over, p_under = totals_probs

    exp_goals_home, exp_goals_away = estimate_lambdas(p_home, p_draw, p_away, p_over, p_under, goal_line)
    (home_goals, away_goals), prob, exp_points = best_expected_points_score(exp_goals_home, exp_goals_away)

    return {
        home_team: home_goals,
        away_team: away_goals,
        "probability": round(prob, 4),
        "expectedPoints": round(exp_points, 3)
    }

def load_json(filename):
    with open(DATA_DIR / filename, "r") as f:
        return json.load(f)

def predict_all_matches():
    """
    Generate predictions for all matches
    """
    h2h_list = load_json("h2h_predictions.json")
    totals_list = load_json("totals_predictions.json")

    predictions = []
    for h2h in h2h_list:
        totals = next(
            (t for t in totals_list if t["home_team"] == h2h["home_team"] and t["away_team"] == h2h["away_team"]),
            None
        )
        if totals:
            predictions.append(predict_score(h2h, totals))
    return predictions

def main():
    all_predictions = predict_all_matches()
    save_json(all_predictions, "score_predictions.json")
    logger.debug(f"Saved score predictions to {DATA_DIR / 'score_predictions.json'}")

if __name__ == "__main__":
    main()

