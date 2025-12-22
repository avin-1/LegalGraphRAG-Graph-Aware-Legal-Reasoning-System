from app.storage.neo4j_client import run_query
import uuid

def ingest_document_graph(file_path: str, chunks: list[str], metadata: dict):
    """
    Ingests document into Neo4j using the Legal Research SRS schema (Case, Court, Cites).
    """
    case_id = str(uuid.uuid4())
    
    # Unpack metadata
    title = metadata.get("title", "Unknown")
    court = metadata.get("court", "Unknown Court")
    year = metadata.get("year", 0)
    citations = metadata.get("citations", [])

    print(f"--- [GRAPH] Ingesting Case: {title} ({year}) in {court} ---")

    # 1. Create Case and Court nodes
    query_base = """
    MERGE (c:Case {title: $title})
    ON CREATE SET c.case_id = $case_id, c.year = $year, c.path = $path
    
    MERGE (ct:Court {name: $court})
    MERGE (c)-[:DECIDED_IN]->(ct)
    """
    run_query(query_base, {
        "title": title,
        "case_id": case_id,
        "year": year,
        "court": court,
        "path": file_path
    })

    # 2. Link citations (Placeholder nodes for cited cases)
    for cite in citations:
        query_cite = """
        MATCH (c:Case {case_id: $case_id})
        MERGE (target:Case {title: $cite})
        MERGE (c)-[:CITES]->(target)
        """
        run_query(query_cite, {"case_id": case_id, "cite": cite})

    # 3. Create Chunk nodes and link to Case
    for i, chunk_text in enumerate(chunks):
        chunk_id = f"{case_id}_chunk_{i}"
        query_chunk = """
        MATCH (c:Case {case_id: $case_id})
        CREATE (k:Chunk {chunk_id: $chunk_id, text: $text, index: $index})
        MERGE (c)-[:HAS_CHUNK]->(k)
        """
        run_query(query_chunk, {
            "case_id": case_id, 
            "chunk_id": chunk_id, 
            "text": chunk_text, 
            "index": i
        })

        # Link chunks sequentially for completeness
        if i > 0:
            prev_chunk_id = f"{case_id}_chunk_{i-1}"
            query_seq = """
            MATCH (k1:Chunk {chunk_id: $prev_id}), (k2:Chunk {chunk_id: $curr_id})
            MERGE (k1)-[:NEXT]->(k2)
            """
            run_query(query_seq, {"prev_id": prev_chunk_id, "curr_id": chunk_id})

    print(f"--- [GRAPH] Successfully mapped {title} to Neo4j ---")

def ingest_case(case):
    # Fallback/Legacy function just in case
    query = """
    MERGE (c:Case {case_id: $id})
    SET c.title = $title,
    c.year = $year,
    c.court = $court
    """
    run_query(query, case)