from app.storage.vector_store import add_documents

def ingest_web_results(results: list[dict]):
    chunks = [r["content"] for r in results if r["content"]]
    metadata = [{
        "source": r["url"],
        "origin": "web"
    } for r in results if r["content"]]

    if chunks:
        add_documents(chunks, metadata)