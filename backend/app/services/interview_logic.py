import json
import numpy as np

from app.services.llm import generate_response
from app.models.interview import GeneratedQuestion

from sentence_transformers import SentenceTransformer


# QUESTION SIMILARITY MODEL

model = SentenceTransformer(
    "all-MiniLM-L6-v2"
)


# INTERVIEW CONTROL

def should_end_interview(state):

    if state.question_count >= state.max_questions:
        return True

    if state.time_remaining <= 0:
        return True

    return False


def should_follow_up(evaluation):

    if evaluation["should_challenge"]:
        return True

    if evaluation["state"] in [
        "shallow",
        "weak_reasoning"
    ]:
        return True

    return False


# TOPIC SELECTION

def choose_next_topic(
    state,
    blueprint
):

    priority_topics = blueprint[
        "priority_topics"
    ]

    for topic in priority_topics:

        if topic not in state.topics_covered:
            return topic

    # All priority topics have been covered.
    # Cycle through priority topics again.
    for topic in priority_topics:
        return topic

    return "General"


# ANSWER ANALYSIS

def determine_answer_state(evaluation):

    if evaluation["technical_accuracy"] < 5:
        return "technical_gap"

    if evaluation["depth"] < 5:
        return "shallow"

    if evaluation["reasoning"] < 5:
        return "weak_reasoning"

    if evaluation["overall_score"] >= 8:
        return "strong"

    return "acceptable"


# FOLLOW-UP CONTROL

MAX_FOLLOW_UPS = 2


def can_follow_up(state):

    return (
        state.follow_up_count
        < MAX_FOLLOW_UPS
    )


# DIFFICULTY ADAPTATION

DIFFICULTY_LEVELS = [
    "easy",
    "medium",
    "hard"
]


def adjust_difficulty(
    current_difficulty,
    answer_state
):

    current_index = DIFFICULTY_LEVELS.index(
        current_difficulty
    )

    if answer_state == "strong":

        new_index = min(
            current_index + 1,
            len(DIFFICULTY_LEVELS) - 1
        )

    elif answer_state in [
        "technical_gap",
        "shallow"
    ]:

        new_index = max(
            current_index - 1,
            0
        )

    else:

        new_index = current_index

    return DIFFICULTY_LEVELS[new_index]


# QUESTION GENERATION

def generate_question(
    topic: str,
    difficulty: str,
    question_type: str,
    previous_questions: list[str] | None = None
):

    if previous_questions is None:
        previous_questions = []

    previous_text = "\n".join(
        f"- {q}"
        for q in previous_questions[-10:]
    )

    prompt = f"""
You are an expert technical interviewer.

Generate ONE interview question.

Target topic:
{topic}

Difficulty:
{difficulty}

Question type:
{question_type}

Previously asked questions:
{previous_text if previous_text else "None"}

Rules:

1. The question must test the specified topic.
2. Match the requested difficulty.
3. Do not repeat or closely rephrase previous questions.
4. The question should be appropriate for a technical interview.
5. Return expected concepts that a strong answer should contain.
6. Return ONLY valid JSON.

Return:

{{
    "question": "...",
    "topic": "...",
    "difficulty": "...",
    "question_type": "...",
    "expected_concepts": [
        "...",
        "..."
    ]
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
        temperature=0.7
    )

    result = json.loads(
        response_text
    )

    return GeneratedQuestion.model_validate(
        result
    )


# QUESTION HISTORY

def check_question_history(
    new_question: str,
    asked_questions: list[str],
    threshold: float = 0.80
):

    if not asked_questions:

        return {
            "is_duplicate": False,
            "similarity": 0.0,
            "matched_question": None
        }

    new_embedding = model.encode(
        [new_question],
        normalize_embeddings=True
    ).astype("float32")

    history_embeddings = model.encode(
        asked_questions,
        normalize_embeddings=True
    ).astype("float32")

    scores = np.matmul(
        history_embeddings,
        new_embedding[0]
    )

    best_index = int(
        np.argmax(scores)
    )

    best_score = float(
        scores[best_index]
    )

    return {
        "is_duplicate": best_score >= threshold,
        "similarity": best_score,
        "matched_question": (
            asked_questions[best_index]
        )
    }


def is_question_repetitive(
    new_question,
    previous_questions,
    threshold=0.85
):

    if not previous_questions:
        return False

    result = check_question_history(
        new_question,
        previous_questions,
        threshold=threshold
    )

    return result["is_duplicate"]


# UNIQUE QUESTION GENERATION

def generate_unique_question(
    topic,
    difficulty,
    question_type,
    previous_questions,
    max_attempts=3
):

    question = None

    for attempt in range(max_attempts):

        question = generate_question(
            topic=topic,
            difficulty=difficulty,
            question_type=question_type,
            previous_questions=previous_questions
        )

        is_duplicate = is_question_repetitive(
            question.question,
            previous_questions
        )

        if not is_duplicate:
            return question

        print(
            f"Question too similar. "
            f"Regenerating "
            f"({attempt + 1}/{max_attempts})..."
        )

    return question