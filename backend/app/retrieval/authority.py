COURT_WEIGHT = {
    "Supreme Court": 3,
    "High Court": 2,
    "District Court": 1
}

def authority_score(court: str, year: int, hops: int):
    court_score = COURT_WEIGHT.get(court, 0)
    recency_score = 1 if year >= 2000 else 0
    hop_penalty = max(0, 3 - hops)

    return court_score + recency_score + hop_penalty
