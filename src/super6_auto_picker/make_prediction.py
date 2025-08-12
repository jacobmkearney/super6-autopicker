import json
import math
from pathlib import Path

DATA_DIR = Path("data")

def implied_prob(price: float) -> float:
    return 1.0 / price

def normalize_probs(probs: list[float]) -> list[float]:
    total = sum(probs)
    return [p / total for p in probs]

def estimate_lambdas(p_home, p_draw, p_away, p_over, p_under, goal_line):
    exp_total_goals = (p_over * (goal_line + 0.5)) + (p_under * (goal_line - 0.5))
    home_ratio = p_home / (p_home + p_away)
    λ_home = exp_total_goals * home_ratio
    λ_away = exp_total_goals - λ_home
    return λ_home, λ_away

def poisson_prob(lmbda, k):
    return (math.exp(-lmbda) * (lmbda ** k)) / math.factorial(k)

def most_likely_score(λ_home, λ_away, max_goals=5):
    best_score = None
    best_prob = 0
    for home_goals in range(max_goals + 1):
        for away_goals in range(max_goals + 1):
            p = poisson_prob(λ_home, home_goals) * poisson_prob(λ_away, away_goals)
            if p > best_prob:
                best_prob = p
                best_score = (home_goals, away_goals)
    return best_score, best_prob

def predict_score(h2h_dict, totals_dict):
    home_team = h2h_dict["home_team"]
    away_team = h2h_dict["away_team"]

    if not h2h_dict["predictions"] or not totals_dict["predictions"]:
        return {home_team: None, away_team: None, "probability": None}

    # Map odds to correct teams
    home_price = next(o["price"] for o in h2h_dict["predictions"] if o["name"] == home_team)
    away_price = next(o["price"] for o in h2h_dict["predictions"] if o["name"] == away_team)
    draw_price = next(o["price"] for o in h2h_dict["predictions"] if o["name"].lower() == "draw")

    h2h_probs = normalize_probs([implied_prob(home_price), implied_prob(draw_price), implied_prob(away_price)])
    p_home, p_draw, p_away = h2h_probs

    # Totals
    over_price = next(o["price"] for o in totals_dict["predictions"] if o["name"].lower() == "over")
    under_price = next(o["price"] for o in totals_dict["predictions"] if o["name"].lower() == "under")
    goal_line = totals_dict["predictions"][0]["point"]

    totals_probs = normalize_probs([implied_prob(over_price), implied_prob(under_price)])
    p_over, p_under = totals_probs

    λ_home, λ_away = estimate_lambdas(p_home, p_draw, p_away, p_over, p_under, goal_line)
    (home_goals, away_goals), prob = most_likely_score(λ_home, λ_away)

    return {
        home_team: home_goals,
        away_team: away_goals,
        "probability": round(prob, 4)
    }

def load_json(filename):
    with open(DATA_DIR / filename, "r") as f:
        return json.load(f)

def save_json(data, filename):
    with open(DATA_DIR / filename, "w") as f:
        json.dump(data, f, indent=2)

def predict_all_matches():
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

if __name__ == "__main__":
    all_predictions = predict_all_matches()
    save_json(all_predictions, "score_predictions.json")
    print(f"Saved score predictions to {DATA_DIR / 'score_predictions.json'}")
