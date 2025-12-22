TRUSTED_DOMAINS = [
    ".gov", ".nic.in", ".judiciary", ".court", ".edu"
]

def trust_score(url: str) -> int:
    return 1 if any(d in url for d in TRUSTED_DOMAINS) else 0

