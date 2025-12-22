def detect_reflection_signal(draft: str) -> bool:
    """
    Stub detector.
    Later: LLM emits structured reflection tokens.
    """
    triggers = ["need evidence", "missing precedent", "unclear"]
    return any(t in draft.lower() for t in triggers)

REFLECTION_TOKENS = {
    "<<NEED_EVIDENCE>>",
    "<<MISSING_PRECEDENT>>",
    "<<AMBIGUOUS_LAW>>",
}

def detect_reflection(draft: str) -> list[str]:
    hits = []
    for t in REFLECTION_TOKENS:
        if t in draft:
            hits.append(t)
    return hits