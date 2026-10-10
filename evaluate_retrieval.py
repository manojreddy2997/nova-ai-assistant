import sys
from app.backend.vector_store import (
    search_chunks,
    get_collection_count,
)


# Questions with known answers in our PDF documents.
EVALUATION_CASES = [
    {
        "question": "What is machine learning?",
        "expected_source": "ai_basics.pdf",
    },
    {
        "question": "What does RAG do?",
        "expected_source": "ai_basics.pdf",
    },
    {
        "question": "What does ETL stand for?",
        "expected_source": "etl_test.pdf",
    },
    {
        "question": "What happens during the transform step of ETL?",
        "expected_source": "etl_test.pdf",
    },
    {
        "question": "Where is Chilika Lake located?",
        "expected_source": "sample.pdf",
    },
    {
        "question": "What is the ecological importance of Chilika Lake?",
        "expected_source": "sample.pdf",
    },
    {
        "question": "What is the population of Mars in 2026?",
        "expected_source": None,
    },
]


def evaluate_retrieval():
    if get_collection_count() == 0:
        print("No indexed document chunks found.")
        print("Run: python reindex_documents.py")
        return

    recall_hits = 0
    top1_hits = 0
    negative_hits = 0
    positive_cases = 0
    negative_cases = 0

    print("\nNOVA RETRIEVAL EVALUATION")
    print("=" * 60)

    for case in EVALUATION_CASES:
        question = case["question"]
        expected = case["expected_source"]

        results = search_chunks(question, top_k=3)
        sources = [
            result.get("metadata", {}).get("source")
            for result in results
        ]

        print(f"\nQuestion: {question}")
        print(f"Expected source: {expected or 'No relevant source'}")
        print(f"Retrieved sources: {sources or 'No results'}")

        if expected is None:
            negative_cases += 1

            if not results:
                negative_hits += 1
                print("Result: PASS — no irrelevant chunks returned")
            else:
                print("Result: REVIEW — results returned for an unrelated question")

            continue

        positive_cases += 1

        if expected in sources:
            recall_hits += 1
            print("Recall@3: HIT")
        else:
            print("Recall@3: MISS")

        if sources and sources[0] == expected:
            top1_hits += 1
            print("Top-1 source: CORRECT")
        else:
            print("Top-1 source: INCORRECT")

    print("\n" + "=" * 60)
    print("EVALUATION SUMMARY")

    if positive_cases:
        recall = recall_hits / positive_cases * 100
        top1_accuracy = top1_hits / positive_cases * 100

        print(
            f"Recall@3: {recall_hits}/{positive_cases} "
            f"({recall:.1f}%)"
        )
        print(
            f"Top-1 source accuracy: {top1_hits}/{positive_cases} "
            f"({top1_accuracy:.1f}%)"
        )

    if negative_cases:
        rejection_rate = negative_hits / negative_cases * 100
        print(
            f"Unrelated-query rejection: "
            f"{negative_hits}/{negative_cases} "
            f"({rejection_rate:.1f}%)"
        )

        total_failures = (
        (positive_cases - recall_hits)
        + (positive_cases - top1_hits)
        + (negative_cases - negative_hits)
    )

    print("\nEvaluation complete.")

    if total_failures:
        print(f"FAILED: {total_failures} evaluation check(s) failed.")
        sys.exit(1)

    print("SUCCESS: All evaluation checks passed.")


if __name__ == "__main__":
    evaluate_retrieval()
