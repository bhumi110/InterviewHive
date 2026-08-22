import json

from app.services.llm import generate_response
from app.models.evaluation import AnswerEvaluation
from app.prompts import load_prompt


EVALUATOR_PROMPT = load_prompt(
    "evaluator.txt"
)


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
Evaluate the candidate's interview answer using the provided
question and expected concepts.

QUESTION CONTEXT
{json.dumps(
    evaluation_input,
    indent=2,
    ensure_ascii=False
)}

Return ONLY valid JSON matching the expected evaluation structure.

Expected fields:
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

    result = json.loads(
        response_text
    )

    return AnswerEvaluation.model_validate(
        result
    )