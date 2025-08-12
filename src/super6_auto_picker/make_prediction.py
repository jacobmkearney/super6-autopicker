import math

def implied_prob(price: float) -> float:
    return 1.0 / price

def normalize_probs(probs: list[float]) -> list[float]:
    total = sum(probs)
    return [p / total for p in probs]

def estimate_lambdas(p_home: float, p_draw: float, p_away: float,
                     p_over: float, p_under: float, goal_line: float) -> tuple[float, float]:
    exp_total_goals = (p_over * (goal_line + 0.5)) + (p_under * (goal_line - 0.5))
    home_ratio = p_home / (p_home + p_away)
    λ_home = exp_total_goals * home_ratio
    λ_away = exp_total_goals - λ_home
    return λ_home, λ_away

def poisson_prob(lmbda: float, k: int) -> float:
    return (math.exp(-lmbda) * (lmbda ** k)) / math.factorial(k)

def most_likely_score(λ_home: float, λ_away: float, max_goals: int = 5) -> tuple[tuple[int, int], float]:
    best_score = None
    best_prob = 0
    for home_goals in range(max_goals + 1):
        for away_goals in range(max_goals + 1):
            p = poisson_prob(λ_home, home_goals) * poisson_prob(λ_away, away_goals)
            if p > best_prob:
                best_prob = p
                best_score = (home_goals, away_goals)
    return best_score, best_prob

def predict_score(h2h_dict: dict, totals_dict: dict) -> dict:
    home_team = h2h_dict.get("home_team")
    away_team = h2h_dict.get("away_team")

    # Extract H2H prices explicitly
    home_price = next(o["price"] for o in h2h_dict["predictions"] if o["name"] == home_team)
    away_price = next(o["price"] for o in h2h_dict["predictions"] if o["name"] == away_team)
    draw_price = next(o["price"] for o in h2h_dict["predictions"] if o["name"].lower() == "draw")

    h2h_probs = normalize_probs([implied_prob(home_price), implied_prob(draw_price), implied_prob(away_price)])
    p_home, p_draw, p_away = h2h_probs

    # Extract totals prices
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


if __name__ == "__main__":
    h2h_example = {
        'market': 'h2h',
        'bookmaker': 'Sky Bet',
        'home_team': 'Liverpool',
        'away_team': 'Bournemouth',
        'predictions': [
            {'name': 'Bournemouth', 'price': 9.5},
            {'name': 'Liverpool', 'price': 1.25},
            {'name': 'Draw', 'price': 6.0}
        ],
        'most_likely': {'name': 'Liverpool', 'price': 1.25}
    }

    totals_example = {
        'market': 'totals',
        'bookmaker': 'Unibet',
        'home_team': 'Liverpool',
        'away_team': 'Bournemouth',
        'predictions': [
            {'name': 'Over', 'price': 2.0, 'point': 3.5},
            {'name': 'Under', 'price': 1.82, 'point': 3.5}
        ],
        'most_likely': {'name': 'Under', 'price': 1.82, 'point': 3.5}
    }

    result = predict_score(h2h_example, totals_example)
    print(result)
