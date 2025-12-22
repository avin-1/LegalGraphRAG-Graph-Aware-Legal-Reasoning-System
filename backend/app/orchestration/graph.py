from langgraph.graph import StateGraph,END
from app.orchestration.state import ResearchState
from app.retrieval.retriever import hybrid_retrieval
from app.agents.crag import crag_grade
from app.agents.query_rewriter import rewrite_query
from app.retrieval.graph_reasoner import traverse_authority_chain
from app.agents.self_rag import detect_reflection_signal
from app.retrieval.reranker import rerank
from app.agents.claim_extractor import extract_claims
from app.agents.auditor import map_claims_to_sources
from app.agents.self_rag import detect_reflection
from app.agents.generation_llm import SYSTEM_PROMPT
from app.retrieval.retriever import hybrid_retrieval
from app.retrieval.web_search import web_search
from app.ingestion.web_ingestor import ingest_web_results
from app.agents.query_rewriter import rewrite_query
from app.retrieval.web_search import web_search
from app.ingestion.web_ingestor import ingest_web_results
from app.orchestration.state import ResearchState

# ResearchState is s Type Annotation for State
def retrieve_documents(state: ResearchState) -> ResearchState:
    query = state["query"]
    docs = hybrid_retrieval(query)

    state["documents"] = docs
    return state

def rerank_documents(state: ResearchState) -> ResearchState:
    query = state["query"]
    docs = state["documents"]

    state["documents"] = rerank(query, docs)
    return state

def graph_reasoning(state: ResearchState) -> ResearchState:
    docs = state["documents"]

    authority_docs = traverse_authority_chain(docs)

    state["documents"] = authority_docs
    return state


def grade_relevance(state: ResearchState) -> ResearchState:
    query = state["query"]
    docs = state["documents"]

    relevant_docs, confidence = crag_grade(query, docs)

    state["documents"] = relevant_docs
    state["confidence"] = confidence

    # gate signal
    if confidence < 0.7:
        state["web_search_required"] = True
    else:
        state["web_search_required"] = False

    return state


def corrective_loop(state: ResearchState) -> ResearchState:
    original_query = state["query"]

    # 0. Retry guard (NEW)
    state["retry_count"] = state.get("retry_count", 0) + 1
    if state["retry_count"] > 3:
        # Fallback: Force generation but flag it
        state["low_confidence"] = True
        return state

    # 1. Web fallback ONLY if explicitly required
    if state.get("web_search_required"):
        results = web_search(original_query)
        ingest_web_results(results)

        state["reflection_steps"].append(
            "Web search fallback triggered due to low confidence"
        )
        state["web_search_required"] = False

    # 2. Query reformulation (always)
    rewritten = rewrite_query(original_query)
    state["query"] = rewritten

    state["reflection_steps"].append(
        f"Retry {state['retry_count']}: query reformulated"
    )

    return state

from app.agents.generation_llm import generate_completion, SYSTEM_PROMPT

def generate_answer(state: ResearchState) -> ResearchState:
    query = state["query"]
    docs = state["documents"]

    messages = [
        {"role": "system", "content": SYSTEM_PROMPT},
        {
            "role": "user",
            "content": f"Query: {query}\n\nContext: {docs}"
        }
    ]

    try:
        response = generate_completion(messages)
        draft = response.choices[0].message.content
        
        # Check for self-reflection
        reflections = detect_reflection(draft)
        if reflections:
             state["reflection_steps"].extend(reflections)
             extra_docs = hybrid_retrieval(query)
             state["documents"].extend(extra_docs)
             
             messages.append({"role": "assistant", "content": draft})
             messages.append({"role": "user", "content": "Continue with improved evidence."})
             
             response = generate_completion(messages)
             draft = response.choices[0].message.content

    except Exception as e:
        print(f"--- [GRAPH] Generation failed: {e}. returning context. ---")
        draft = f"⚠️ **System Error: The AI model is unresponsive.**\n\nHere is the raw context found:\n\n{str(docs)[:2000]}..."

    if state.get("low_confidence"):
        draft = "⚠️ **Note: The following answer was generated with low confidence.**\n\n" + draft

    state["final_answer"] = draft
    return state


def build_research_graph():
    graph = StateGraph(ResearchState)

    # Register nodes
    graph.add_node("retrieve", retrieve_documents)
    graph.add_node("graph_reason", graph_reasoning)
    graph.add_node("grade", grade_relevance)
    graph.add_node("correct", corrective_loop)
    graph.add_node("rerank", rerank_documents)
    graph.add_node("generate", generate_answer)

    # Entry point
    graph.set_entry_point("retrieve")

    # Main flow
    graph.add_edge("retrieve", "graph_reason")
    graph.add_edge("graph_reason", "grade")

    # Confidence router
    def confidence_router(state: ResearchState) -> str:
        if state["confidence"] >= 0.7:
            return "rerank"
        return "correct"

    # Conditional routing
    graph.add_conditional_edges(
        "grade",
        confidence_router,
        {
            "rerank": "rerank",
            "correct": "correct"
        }
    )

    # Loop back after correction
    # graph.add_edge("correct", "retrieve") <-- REMOVING static edge

    def correction_router(state: ResearchState) -> str:
        # If we have hit the retry limit, the 'correct' node sets a final failure message.
        # So we should just stop.
        count = state.get("retry_count", 0)
        print(f"--- [GRAPH] Correction Router: retry_count={count} ---")
        if count > 3:
            return "rerank"
        return "retrieve"

    graph.add_conditional_edges(
        "correct",
        correction_router,
        {
            "retrieve": "retrieve",
            "rerank": "rerank",
            END: END
        }
    )

    # Final precision → answer
    graph.add_edge("rerank", "generate")
    graph.add_edge("generate", END)

    return graph.compile()
