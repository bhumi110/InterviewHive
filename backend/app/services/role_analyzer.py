import json

from app.services.llm import generate_response
from app.models.interview import InterviewBlueprint


def analyze_role(
    target_role: str,
    candidate_profile: dict
):

    prompt = f"""
You are an expert technical interviewer.

Create an interview blueprint for the following candidate.

TARGET ROLE:
{target_role}

CANDIDATE PROFILE:
{json.dumps(
    candidate_profile,
    indent=2,
    ensure_ascii=False
)}

Determine:

1. priority topics
2. important technical skills
3. project areas worth questioning
4. competencies to evaluate
5. suggested difficulty
6. interview focus

The interview should be tailored to BOTH:
- the target role
- the candidate's actual resume

Do not invent skills or experience.

IMPORTANT:
- Return ONLY valid JSON.
- Do not use markdown.
- Do not use ```json.
- Do not add explanations.
- Keep every string concise.
- Do not write long descriptions.
- Make sure every string is properly closed.

Expected format:

{{
    "target_role": "{target_role}",
    "priority_topics": [],
    "technical_skills": [],
    "project_topics": [],
    "competencies": [],
    "difficulty": "medium",
    "interview_focus": []
}}
"""

    response_text = generate_response(
        messages=[
            {
                "role": "system",
                "content": (
                    "You are an expert technical interviewer. "
                    "Return ONLY valid JSON. "
                    "Never return markdown or explanations."
                )
            },
            {
                "role": "user",
                "content": prompt
            }
        ],
        model="openai/gpt-oss-120b",
        temperature=0
    )

    print(
        "\n========== ROLE ANALYZER RAW RESPONSE =========="
    )
    print(response_text)
    print(
        "=================================================\n"
    )

    # Remove accidental markdown fences
    response_text = response_text.strip()

    if response_text.startswith("```"):
        response_text = response_text.replace(
            "```json", ""
        )
        response_text = response_text.replace(
            "```", ""
        )
        response_text = response_text.strip()

    try:

        result = json.loads(
            response_text
        )

    except json.JSONDecodeError as e:

        print(
            "ROLE ANALYZER JSON ERROR:",
            e
        )

        raise ValueError(
            "Role analyzer returned invalid JSON."
        )

    # Validate against Pydantic model
    blueprint = InterviewBlueprint.model_validate(
        result
    )

    return blueprint