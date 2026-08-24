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

Return ONLY valid JSON.

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
                    "Return only valid JSON."
                )
            },
            {
                "role": "user",
                "content": prompt
            }
        ],
        model="openai/gpt-oss-120b",
        temperature=0.2
    )

    

    result = json.loads(response_text)

    return result