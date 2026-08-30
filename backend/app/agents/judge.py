import json
import re

from app.services.llm import generate_response
from app.models.interview import FinalInterviewReport
from app.prompts import load_prompt


JUDGE_PROMPT = load_prompt(
    "judge.txt"
)


def extract_json(text: str):
    """
    Safely extract a JSON object from the Judge LLM response.
    Handles:
    - Empty responses
    - ```json ... ``` fences
    - Extra text around JSON
    """

    if not text or not text.strip():
        raise ValueError(
            "Judge LLM returned an empty response."
        )

    text = text.strip()

    # Remove markdown code fences
    text = re.sub(
        r"^```(?:json)?\s*",
        "",
        text,
        flags=re.IGNORECASE
    )

    text = re.sub(
        r"\s*```$",
        "",
        text
    ).strip()

    # Try parsing the entire response
    try:
        return json.loads(text)
    except json.JSONDecodeError:
        pass

    # Find JSON object inside surrounding text
    start = text.find("{")
    end = text.rfind("}")

    if start == -1 or end == -1 or end <= start:
        raise ValueError(
            "Judge LLM did not return a JSON object.\n"
            f"Response:\n{text}"
        )

    json_text = text[start:end + 1]

    try:
        return json.loads(json_text)

    except json.JSONDecodeError as e:
        raise ValueError(
            f"Judge returned invalid JSON: {e}\n"
            f"Response:\n{json_text}"
        ) from e


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

    # Debug the actual LLM response
    print("\n===== JUDGE RAW RESPONSE =====")
    print(response_text)
    print("==============================\n")

    # Safely parse JSON
    parsed = extract_json(
        response_text
    )

    # Validate against Pydantic model
    return FinalInterviewReport.model_validate(
        parsed
    )