def map_claims_to_sources(claims: list[str], documents: list[str]):
    """
    Later:
    - Span-level grounding
    - Neo4j node + section ids
    """
    audit = []
    for c in claims:
        audit.append({
            "claim": c,
            "sources": documents[:2]  # top evidence only
        })
    return audit