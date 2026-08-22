from pydantic import BaseModel,  Field

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