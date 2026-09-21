from app.answer import answer_question
from app.tool_agent import run_agent

session_histories = {}


def assistant(question, session_id="default"):

    if session_id not in session_histories:
        session_histories[session_id] = []

    conversation_history = session_histories[session_id]

    history_text = "\n".join(conversation_history)

    question_lower = question.lower().strip()

    greetings = [
        "hi",
        "hello",
        "hey",
        "good morning",
        "good afternoon",
        "good evening"
    ]

    if question_lower in greetings:

        result = (
            "Hello! I'm NovaTech Enterprise Assistant. "
            "I can help you with company policies, "
            "leave information, HR information, and IT support."
        )

    elif any(word in question_lower for word in [
        "ticket",
        "it support",
        "vpn",
        "password reset",
        "technical issue",
        "it-",
        "employee",
        "employee details",
        "employee profile",
        "leave balance",
        "hr policy",
        "hr details",
        "hr information"
    ]):

        result = run_agent(question)

    else:

        result = answer_question(
            question,
            conversation_history=history_text
        )

    conversation_history.append(
        f"User: {question}"
    )

    conversation_history.append(
        f"Assistant: {result}"
    )

    return result