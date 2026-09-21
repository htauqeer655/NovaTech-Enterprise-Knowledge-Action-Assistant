from app.answer import answer_question

test_cases = [
    {
        "question": "How many annual leaves does a confirmed employee get?",
        "expected": "24 days"
    },
    {
        "question": "How many sick leave days do employees get?",
        "expected": "12 days"
    },
    {
        "question": "How many annual leave days can be carried forward?",
        "expected": "10"
    },
    {
        "question": "When do carried-forward leave days lapse?",
        "expected": ["March 31", "31 March"]
    },
    {
        "question": "What should attendance be marked as during business travel?",
        "expected": "Off-site"
    },
    {
        "question": "What is required for international business travel?",
        "expected": "VPN geo-unblock"
    },
    {
        "question": "How many annual leaves does an employee get?",
        "expected": "24 days"
    }
]


def run_evaluation():

    passed = 0
    total = len(test_cases)

    print()
    print("RAG Evaluation")
    print("=" * 60)

    for i, test in enumerate(test_cases, start=1):

        question = test["question"]
        expected = test["expected"]

        answer = answer_question(question)

        if answer is None:
            answer = ""

        if isinstance(expected, list):
            is_pass = any(
                item.lower() in answer.lower()
                for item in expected
            )
        else:
            is_pass = (
                expected.lower()
                in answer.lower()
            )

        if is_pass:
            passed += 1
            status = "PASS"
        else:
            status = "FAIL"

        print()
        print(f"Test {i}: {status}")
        print(f"Question: {question}")
        print(f"Expected: {expected}")
        print(f"Answer: {answer}")

    accuracy = (
        passed / total
    ) * 100

    print()
    print("=" * 60)
    print(f"Passed: {passed}/{total}")
    print(f"Accuracy: {accuracy:.2f}%")


if __name__ == "__main__":
    run_evaluation()