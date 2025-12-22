import chromadb
from app.ingestion.embeddings import get_embedding_model

client = chromadb.Client()
collection = client.get_or_create_collection(
    name="legal_docs"
)

def add_documents(chunks: list[str], metadata: list[dict]):
    model = get_embedding_model()
    embeddings = model.encode(chunks).tolist()

    import uuid
    ids = [str(uuid.uuid4()) for _ in range(len(chunks))]

    collection.add(
        documents=chunks,
        embeddings=embeddings,
        metadatas=metadata,
        ids=ids
    )


def similarity_search(query: str, k=5):
    model = get_embedding_model()
    query_embedding = model.encode([query]).tolist()

    results = collection.query(
        query_embeddings=query_embedding,
        n_results=k
    )

    return results["documents"][0]
