from pydantic import BaseModel, Field


class AnswerEvaluation(BaseModel):
    overall_score: float
    technical_accuracy: float
    depth: float
    reasoning: float
    clarity: float
    communication: float
    confidence: float

    strengths: list[str] = Field(
        default_factory=list
    )

    weaknesses: list[str] = Field(
        default_factory=list
    )

    should_challenge: bool = False

    suggested_follow_up: str = ""

    missing_concepts: list[str] = Field(
        default_factory=list
    )