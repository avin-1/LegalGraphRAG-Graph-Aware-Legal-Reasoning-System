from typing import TypedDict, List, Optional


class ResearchState(TypedDict):
    # User input
    query: str

    # Retrieved content
    documents: List[str]

    # Confidence from CRAG
    confidence: float

    # Reflection / self-rag signals
    reflection_steps: List[str]

    # Control flags
    web_search_required: bool

    claims: list[str]
    audit_trail: list[dict]
    final_answer: str

    # Loop safety
    retry_count: int
    low_confidence: bool