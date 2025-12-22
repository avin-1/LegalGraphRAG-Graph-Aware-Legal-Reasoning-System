def extract_claims(answer: str) -> list[str]:
    """
    Later: LLM sentence-level claim splitter.
    """
    return [s.strip() for s in answer.split(".") if s.strip()]