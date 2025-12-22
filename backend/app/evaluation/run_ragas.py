from ragas import evaluate
from ragas.metrics import (
    faithfulness,
    context_precision,
    answer_relevancy,
    context_recall
)

def run_ragas(dataset):
    return evaluate(
        dataset,
        metrics=[
            faithfulness,
            context_precision,
            context_recall,
            answer_relevancy
        ]
    )
