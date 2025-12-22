from app.retrieval.cross_encoder import get_cross_encoder
def cross_encoder_score(query: str, doc: str) -> float:
    """
    Stub.
    Later: cross-encoder (e.g., bge-reranker, colbert, monoT5).
    """
    # simple heuristic placeholder
    return len(set(query.lower().split()) & set(doc.lower().split()))


def rerank(query: str, documents: list[str], top_k: int = 3):
    if not documents:
        return []

    model = get_cross_encoder()

    pairs = [(query, doc) for doc in documents]
    scores = model.predict(pairs)

    ranked = sorted(
        zip(documents, scores),
        key=lambda x: x[1],
        reverse=True
    )

    return [doc for doc, _ in ranked[:top_k]]

