import uuid
from app.orchestration.graph import build_research_graph
from app.orchestration.state import ResearchState

# In-memory store for now (Redis later)
TASK_STORE = {}

graph = build_research_graph()


def run_research(query: str) -> str:
    task_id = str(uuid.uuid4())

    initial_state: ResearchState = {
        "query": query,
        "documents": [],
        "confidence": 0.0,
        "reflection_steps": [],
        "web_search_required": False,
    }

    # Run graph synchronously for now
    result = graph.invoke(initial_state)

    TASK_STORE[task_id] = result
    return task_id


def get_result(task_id: str):
    return TASK_STORE.get(task_id)


