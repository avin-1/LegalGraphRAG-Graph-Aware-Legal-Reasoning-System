from app.orchestration.graph import build_research_graph
from app.orchestration.state import ResearchState
from app.storage.redis_client import redis_conn

import json

graph = build_research_graph()

def run_task(task_id: str, state: ResearchState):
    print(f"--- [WORKER] Starting research task: {task_id} ---")
    print(f"--- [WORKER] Query: {state.get('query')} ---")
    try:
        result = graph.invoke(state, {"recursion_limit": 100})
        redis_conn.set(task_id, json.dumps(result))
        print(f"--- [WORKER] Task {task_id} completed successfully ---")
    except Exception as e:
        print(f"--- [WORKER] Task {task_id} FAILED: {e} ---")
        raise e