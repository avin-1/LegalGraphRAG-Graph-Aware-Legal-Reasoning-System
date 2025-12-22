from app.storage.vector_store import similarity_search

def vector_search(query: str):
    return similarity_search(query)

    
def graph_search(query: str):
    # later: Neo4j legal graph traversal
    return [
        "GraphDoc: authoritative statute",
        "GraphDoc: cited precedent"
    ]
    
    
def hybrid_retrieval(query: str):
    vector_results = vector_search(query)
    graph_results = graph_search(query)

    # merge + dedupe later
    return vector_results + graph_results