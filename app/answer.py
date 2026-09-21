from app.retrieve import search
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

client = OpenAI()


def answer_question(question, conversation_history=None):

    results = search(question, top_k=5)

    context_parts = []

    for result in results:
        context_parts.append(
            result["text"]
        )

    context = "\n\n---\n\n".join(context_parts)

    prompt = f"""
You are NovaTech's Enterprise Knowledge Assistant.

Answer the user's question using ONLY the provided company documents.

Rules:

* Use the company documents as the source of truth.
* Do not invent information.
* If the user asks about a broad topic such as HR policy,
  company policy, finance policy, leave policy, travel policy,
  work from home policy, or IT policy, summarize the relevant
  information available in the provided documents.
* If the user asks for details, provide the relevant details
  available in the documents.
* If the documents contain only partial information, clearly
  provide only that available information.
* If the documents genuinely do not contain relevant information,
  say:
  "I don't know based on the available company documents."
* Give a concise and clear answer.
* Do not provide a Sources section.
* Do not mention filenames.
* Do not mention chunk IDs.
* Do not mention source numbers.

Company documents:

{context}

Conversation history:

{conversation_history or "No previous conversation."}

User question:

{question}
"""

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ],
    )

    return response.choices[0].message.content


if __name__ == "__main__":

    question = "How many annual leaves does a confirmed employee get?"

    answer = answer_question(question)

    print("\nQuestion:")
    print(question)

    print("\nAnswer:")
    print(answer)