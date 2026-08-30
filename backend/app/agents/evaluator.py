import json
import re

from app.services.llm import generate_response
from app.models.evaluation import AnswerEvaluation
from app.prompts import load_prompt


EVALUATOR_PROMPT = load_prompt(
    "evaluator.txt"
)


def extract_json(text: str):
    """
    Extract and parse the first JSON object from an LLM response.
    Handles markdown fences and extra text around JSON.
    """

    if not text or not text.strip():
        raise ValueError("LLM returned an empty response.")

    text = text.strip()

    # Remove markdown code fences if present
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

    # First try parsing the complete response
    try:
        return json.loads(text)
    except json.JSONDecodeError:
        pass

    # Find JSON object inside additional text
    start = text.find("{")
    end = text.rfind("}")

    if start == -1 or end == -1 or end <= start:
        raise ValueError(
            "LLM did not return a JSON object.\n"
            f"Response:\n{text}"
        )

    json_text = text[start:end + 1]

    try:
        return json.loads(json_text)
    except json.JSONDecodeError as e:
        raise ValueError(
            f"LLM returned invalid JSON: {e}\n"
            f"Response:\n{json_text}"
        ) from e


def evaluate_answer(
    question,
    candidate_answer,
    target_role
):

    evaluation_input = {
        "target_role": target_role,

        "question": question["question"],

        "topic": question.get(
            "topic",
            ""
        ),

        "category": question.get(
            "category",
            ""
        ),

        "difficulty": question.get(
            "difficulty",
            ""
        ),

        "question_type": question.get(
            "question_type",
            ""
        ),

        "expected_concepts": question.get(
            "expected_concepts",
            []
        ),

        "candidate_answer": candidate_answer
    }

    prompt = f"""
Evaluate the candidate's interview answer.

QUESTION CONTEXT:

{json.dumps(
    evaluation_input,
    indent=2,
    ensure_ascii=False
)}

Evaluate:

- overall_score
- technical_accuracy
- depth
- reasoning
- clarity
- communication
- confidence
- strengths
- weaknesses
- should_challenge
- suggested_follow_up
- missing_concepts

IMPORTANT:

Return ONLY one valid JSON object.

Do not use markdown.
Do not use ```json.
Do not add explanations before or after the JSON.

All string values must be properly escaped.

Expected structure:

{{
    "overall_score": 0.0,
    "technical_accuracy": 0.0,
    "depth": 0.0,
    "reasoning": 0.0,
    "clarity": 0.0,
    "communication": 0.0,
    "confidence": 0.0,
    "strengths": [],
    "weaknesses": [],
    "should_challenge": false,
    "suggested_follow_up": "",
    "missing_concepts": []
}}
"""

    response_text = generate_response(
        messages=[
            {
                "role": "system",
                "content": EVALUATOR_PROMPT
            },
            {
                "role": "user",
                "content": prompt
            }
        ],
        model="openai/gpt-oss-120b",
        temperature=0
    )

    if not response_text or not response_text.strip():
        raise RuntimeError(
            "Evaluator LLM returned an empty response."
        )

    print("\n===== EVALUATOR RAW RESPONSE =====")
    print(response_text)
    print("==================================\n")

    try:

        result = extract_json(
            response_text
        )

        return AnswerEvaluation.model_validate(
            result
        )

    except Exception as e:

        print(
            "\nEvaluator JSON parsing failed:"
        )

        print(e)

        print(
            "\nRaw evaluator response:"
        )

        print(response_text)

        raise