from datasets import Dataset

def build_ragas_dataset(records: list[dict]):
    """
    records: [{
        question, answer, contexts, ground_truth
    }]
    """
    return Dataset.from_list(records)

def build_sample_from_state(state, ground_truth: str):
    return {
        "question": state["query"],
        "answer": state["final_answer"],
        "contexts": state["documents"],
        "ground_truth": ground_truth
    }