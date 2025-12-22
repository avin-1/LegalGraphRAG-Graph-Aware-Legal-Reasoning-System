

from app.agents.crag_llm import grade_chunk_llm

def crag_grade(query: str, documents: list[str]):
    relevant_docs = []

    for doc in documents:
        if grade_chunk_llm(query, doc):
            relevant_docs.append(doc)

    confidence = (
        len(relevant_docs) / len(documents)
        if documents else 0.0
    )

    return relevant_docs, confidence