from app.answer import answer_question

conversation_history = []


def chat(question):

    # Convert history list into text
    history_text = "\n".join(conversation_history)

    # Get answer from assistant
    full_answer = answer_question(
        question,
        conversation_history=history_text
    )

    # Separate answer from sources
    answer_only = full_answer.split("\n\nSources:")[0]

    # Save only clean conversation
    conversation_history.append(f"User: {question}")
    conversation_history.append(f"Assistant: {answer_only}")

    return full_answer


if __name__ == "__main__":

    print("NovaTech Enterprise Knowledge Assistant")
    print("Type 'exit' to quit.\n")

    while True:

        question = input("You: ")

        if question.lower() == "exit":
            break

        answer = chat(question)

        print("\nAssistant:")
        print(answer)