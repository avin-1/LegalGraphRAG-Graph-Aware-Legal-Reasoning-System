
from pypdf import PdfReader
from app.storage.vector_store import add_documents
from app.ingestion.metadata_extractor import extract_legal_metadata
from app.ingestion.graph_ingestor import ingest_document_graph

def ingest_pdf(path: str):
    print(f"--- [INGEST] Processing: {path} ---")
    
    # 1. Read PDF
    try:
        reader = PdfReader(path)
        chunks = []
        full_text_preview = ""
        
        for page in reader.pages:
            text = page.extract_text()
            if not text: continue
            
            if len(full_text_preview) < 3000:
                full_text_preview += text + "\n"
            
            # Simple chunking by paragraph/lines for now
            # (Ideally use a recursive text splitter)
            page_chunks = [c.strip() for c in text.split('\n\n') if len(c.strip()) > 50]
            chunks.extend(page_chunks)
            
    except Exception as e:
        print(f"Error reading PDF: {e}")
        return


    if not chunks:
        print("--- [INGEST] Warning: No text extracted from PDF. Skipping ingestion. ---")
        return

    # 2. Add to Vector Store (Chroma)
    metadatas = [{"source": path} for _ in chunks]
    # add_documents(chunks, metadata) <-- Assume already exists or implemented
    add_documents(chunks, metadatas)
    print(f"--- [INGEST] Fnished adding documents to vector store ---")

    # 3. Extract Legal Metadata (Robustness Step)
    print("--- [INGEST] STARTING Extracting Legal Metadata... ---")
    try:
        legal_meta = extract_legal_metadata(full_text_preview)
        print(f"--- [INGEST] FINISHED Metadata: {legal_meta} ---")
    except Exception as e:
        print(f"--- [INGEST] Metadata Extraction FAILED: {e}. Using defaults. ---")
        legal_meta = {}

    # 4. Ingest into Neo4j Graph
    try:
        ingest_document_graph(path, chunks, legal_meta)
    except Exception as e:
        print(f"--- [INGEST] Error creating graph nodes: {e} ---")

