from dotenv import load_dotenv
import os
# Load env from parent directory (root of project)
load_dotenv(os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), '.env'))

from flask import Flask, request
# ... imports ...
from flask_cors import CORS
from werkzeug.utils import secure_filename
import os, uuid
from app.controller.queryHandler import queryHandler
import threading
import traceback
import json

app = Flask(__name__)
CORS(app)

from app.orchestration.runner import run_research
# from rq import Queue <-- REMOVED
from app.storage.redis_client import redis_conn
from app.ingestion.pdf_ingestor import ingest_pdf

# q = Queue(connection=redis_conn) <-- REMOVED

# Simple background task runner using threads
def run_background_task(func, *args, **kwargs):
    def wrapper():
        try:
            func(*args, **kwargs)
        except Exception as e:
            print(f"--- [BACKGROUND] Task failed: {e} ---")
            traceback.print_exc()
            
    thread = threading.Thread(target=wrapper)
    thread.daemon = True # Allow app to exit even if thread is running
    thread.start()

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
UPLOAD_FOLDER = os.path.join(BASE_DIR, "app", "uploads")
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024   # 16MB limit

#Endpoint to handle the query
@app.route("/uploadQuery", methods=["POST"])
def uploadQuery():
    query = request.form.get("queryText")
    print(f"--- [API] Received query request: {query} ---")
    if not query:
        return {"error": "queryText required"}, 400

    task_id = str(uuid.uuid4())

    initial_state = {
        "query": query,
        "documents": [],
        "confidence": 0.0,
        "reflection_steps": [],
        "web_search_required": False,
    }

    # q.enqueue(run_task, task_id, initial_state)
    from app.workers.research_worker import run_task # Import here to avoid circular imports if any
    run_background_task(run_task, task_id, initial_state)

    return {"task_id": task_id}, 202


#Endpoint to handle the files
@app.route("/uploadFiles", methods=["POST"])
def uploadFiles():
    """Endpoint to upload Files Expects key=file"""
    print("--- [API] Received uploadFiles request ---")
    if 'file' not in request.files:
        return "No files uploaded", 400

    files = request.files.getlist("file")
    if len(files) == 0:
        return "Please select at least one file", 400

    saved_files = []

    for f in files:
        if f.filename == "":
            continue

        filename = secure_filename(f.filename)
        uploadPath = os.path.join(UPLOAD_FOLDER, filename)

        if os.path.exists(uploadPath):
             # Trigger ingestion even if file exists 
             # q.enqueue(ingest_pdf, uploadPath)
             print(f"--- [API] Enqueueing ingestion for (exists): {filename} ---")
             run_background_task(ingest_pdf, uploadPath)
             continue

        f.save(uploadPath)
        saved_files.append(filename)
        
        # Trigger background ingestion
        print(f"--- [API] Enqueueing ingestion for: {filename} ---")
        # q.enqueue(ingest_pdf, uploadPath)
        run_background_task(ingest_pdf, uploadPath)

    return {
        "uploaded": saved_files,
        "status": "done"
    }, 200

# Returns the TaskID from the getResult in Orchestration.runner
@app.route("/result/<task_id>", methods=["GET"])
def get_result(task_id):
    result_json = redis_conn.get(task_id)

    if result_json is None:
        return {"status": "processing"}, 202
    
    try:
        # Check if it was stored as string or already dict (InMemory might store object if simplified, but let's assume json string for consistency)
        if isinstance(result_json, str):
            result = json.loads(result_json)
        else:
            result = result_json 
    except json.JSONDecodeError:
         return {"error": "Failed to parse result"}, 500

    return {
        "task_id": task_id,
        "result": result
    }, 200

@app.route("/v1/research/audit/<task_id>", methods=["GET"])
def getAudit(task_id):
    result_json = redis_conn.get(task_id)
    
    if not result_json:
        return {"error": "task not found"}, 404
        
    try:
         if isinstance(result_json, str):
            result = json.loads(result_json)
         else:
            result = result_json
    except json.JSONDecodeError:
        return {"error": "processing error"}, 500

    return {
        "task_id": task_id,
        "audit_trail": result.get("reflection_steps", [])
    }, 200

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8000))
    app.run(port=port, debug=True)
