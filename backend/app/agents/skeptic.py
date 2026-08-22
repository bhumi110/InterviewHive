import json

from app.services.llm import generate_response
from app.models.interview import SkepticResponse
from app.prompts import load_prompt


SKEPTIC_PROMPT = load_prompt(
    "skeptic.txt"
)


def skeptic_agent(
    candidate_answer,
    question,
    candidate_profile
):

    input_data = {
        "question": question,
        "candidate_answer": candidate_answer,
        "candidate_profile": candidate_profile
    }

    response_text = generate_response(
        messages=[
            {
                "role": "system",
                "content": SKEPTIC_PROMPT
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
        temperature=0
    )

    parsed = json.loads(
        response_text
    )

    return SkepticResponse.model_validate(
        parsed
    )