import json

from app.services.llm import generate_response
from app.models.interview import FinalInterviewReport
from app.prompts import load_prompt


JUDGE_PROMPT = load_prompt(
    "judge.txt"
)


def judge_agent(
    candidate_profile,
    target_role,
    questions,
    answers,
    evaluations,
    topics_covered
):

    interview_data = {
        "candidate_profile": candidate_profile,
        "target_role": target_role,
        "questions": questions,
        "answers": answers,
        "evaluations": evaluations,
        "topics_covered": topics_covered
    }

    response_text = generate_response(
        messages=[
            {
                "role": "system",
                "content": JUDGE_PROMPT
            },
            {
                "role": "user",
                "content": json.dumps(
                    interview_data,
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

    return FinalInterviewReport.model_validate(
        parsed
    )