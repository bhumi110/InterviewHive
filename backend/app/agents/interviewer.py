import json

from app.services.llm import generate_response
from app.models.interview import InterviewerResponse
from app.prompts import load_prompt


INTERVIEWER_PROMPT = load_prompt(
    "interviewer.txt"
)


def interviewer_agent(
    decision,
    question,
    candidate_profile,
    conversation_history=None,
    candidate_answer=None
):

    if conversation_history is None:
        conversation_history = []

    input_data = {
        "candidate_profile": candidate_profile,
        "manager_decision": decision,
        "question": question,
        "conversation_history": conversation_history[-6:],
        "candidate_answer": candidate_answer
    }

    response_text = generate_response(
        messages=[
            {
                "role": "system",
                "content": INTERVIEWER_PROMPT
            },
            {
                "role": "user",
                "content": json.dumps(
                    input_data,
                    indent=2,
                    ensure_ascii=False
                )
            }
        ],
        model="openai/gpt-oss-120b",
        temperature=0.6
    )

    parsed = json.loads(response_text)

    return InterviewerResponse.model_validate(parsed)