from pydantic import BaseModel, Field
from typing import Optional


class InterviewerResponse(BaseModel):
    message: str
    question: str


class SkepticResponse(BaseModel):
    should_challenge: bool
    concern: str
    challenge_question: str


class FinalInterviewReport(BaseModel):
    overall_score: float
    technical_score: float
    problem_solving_score: float
    communication_score: float
    confidence_score: float
    depth_score: float

    strengths: list[str] = Field(
        default_factory=list
    )

    weaknesses: list[str] = Field(
        default_factory=list
    )

    red_flags: list[str] = Field(
        default_factory=list
    )

    recommended_topics: list[str] = Field(
        default_factory=list
    )

    summary: str


class GeneratedQuestion(BaseModel):
    question: str
    topic: str
    difficulty: str
    question_type: str

    expected_concepts: list[str] = Field(
        default_factory=list
    )


class InterviewState(BaseModel):

    target_role: str

    questions_asked: list[str] = Field(
        default_factory=list
    )

    answers: list[str] = Field(
        default_factory=list
    )

    evaluations: list[dict] = Field(
        default_factory=list
    )

    topics_covered: list[str] = Field(
        default_factory=list
    )

    current_topic: Optional[str] = None

    current_difficulty: str = "medium"

    current_question: Optional[dict] = None

    conversation_history: list[dict] = Field(
        default_factory=list
    )

    time_remaining: int = 900

    max_questions: int = 12

    interview_status: str = "not_started"

    follow_up_count: int = 0

    question_count: int = 0