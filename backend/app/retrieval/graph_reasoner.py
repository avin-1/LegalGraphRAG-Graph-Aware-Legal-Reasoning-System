from app.storage.neo4j_client import run_query
from app.retrieval.authority import authority_score
from app.storage.graph_cache import get_cached, set_cache


def traverse_authority_chain(case_ids: list[str]):
    # 1. Check cache
    cached = get_cached(case_ids)
    if cached is not None:
        return cached

    # 2. Real traversal
    query = """
    MATCH (c:Case)-[:DECIDED_IN]->(court:Court)
    WHERE c.case_id IN $case_ids

    OPTIONAL MATCH path=(c)-[:CITES*1..3]->(p:Case)
    WHERE NOT (p)-[:OVERRULED_BY]->(:Case)

    WITH c, p, court, length(path) AS hops
    RETURN
        p.case_id AS case_id,
        p.title AS title,
        p.year AS year,
        court.name AS court,
        hops
    """

    records = run_query(query, {"case_ids": case_ids})

    scored = []
    for r in records:
        score = authority_score(
            r["court"],
            r["year"],
            r["hops"]
        )
        scored.append({
            "case_id": r["case_id"],
            "title": r["title"],
            "score": score
        })

    scored.sort(key=lambda x: x["score"], reverse=True)

    result = scored[:5]

    # 3. Store in cache
    set_cache(case_ids, result)

    return result
