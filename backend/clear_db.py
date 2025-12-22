import os
import shutil
import glob
from dotenv import load_dotenv

# Load env vars first
load_dotenv()

from app.storage.neo4j_client import run_query
from app.storage.redis_client import redis_conn
import chromadb

def clear_neo4j():
    print("--- [CLEANUP] Clearing Neo4j Database... ---")
    try:
        run_query("MATCH (n) DETACH DELETE n")
        print("--- [CLEANUP] Neo4j cleared successfully. ---")
    except Exception as e:
        print(f"--- [CLEANUP] Failed to clear Neo4j: {e} ---")

def clear_redis():
    print("--- [CLEANUP] Clearing Redis/In-Memory Storage... ---")
    try:
        # Check if it's the real redis client by checking for flushall method
        if hasattr(redis_conn, 'flushall'):
            redis_conn.flushall()
            print("--- [CLEANUP] Redis flushed successfully. ---")
        else:
            # It's InMemoryRedis, just clear the dict
            redis_conn.store.clear()
            print("--- [CLEANUP] In-Memory storage cleared. ---")
    except Exception as e:
        print(f"--- [CLEANUP] Failed to clear Redis: {e} ---")

def clear_chroma():
    print("--- [CLEANUP] Clearing ChromaDB (Vector Store)... ---")
    try:
        client = chromadb.Client()
        # Delete and recreate
        try:
            client.delete_collection("legal_docs")
            print("--- [CLEANUP] 'legal_docs' collection deleted. ---")
        except:
            print("--- [CLEANUP] 'legal_docs' collection did not exist. ---")
            
        client.get_or_create_collection("legal_docs")
        print("--- [CLEANUP] 'legal_docs' collection recreated empty. ---")
    except Exception as e:
         print(f"--- [CLEANUP] Failed to clear ChromaDB: {e} ---")

def clear_files():
    print("--- [CLEANUP] Removing uploaded files... ---")
    upload_dir = os.path.join("app", "uploads")
    if os.path.exists(upload_dir):
        files = glob.glob(os.path.join(upload_dir, "*"))
        for f in files:
            try:
                os.remove(f)
                print(f"Removed: {f}")
            except Exception as e:
                 print(f"Failed to remove {f}: {e}")
    print("--- [CLEANUP] Upload directory cleaned. ---")

if __name__ == "__main__":
    print("WARNING: This will wipe ALL data (Neo4j, Redis, Chroma, Files).")
    confirm = input("Are you sure? (y/n): ")
    if confirm.lower() == 'y':
        clear_neo4j()
        clear_redis()
        clear_chroma()
        clear_files()
        print("\n--- [DONE] All systems cleared. ---")
    else:
        print("Operation cancelled.")
