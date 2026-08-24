from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from app.services.interview_engine import run_interview_turn


router = APIRouter(
    prefix="/interview",
    tags=["Interview"]
)


# REQUEST MODELS

class StartInterviewRequest(BaseModel):
    candidate_profile: dict
    blueprint: dict


class AnswerRequest(BaseModel):
    session_id: str
    answer: str


# TEMPORARY SESSION STORAGE

# IMPORTANT:
# This is intentionally in-memory for now.
#
# You said you do NOT want persistent user login.
# We will later replace this with a temporary interview-session
# mechanism rather than user accounts.

interview_sessions = {}


# START INTERVIEW

@router.post("/start")
def start_interview(
    request: StartInterviewRequest
):

    # Your InterviewState class should already exist.
    # Import it from wherever you created it.
    
    from app.models.interview import InterviewState
    
    state = InterviewState(
        target_role=request.blueprint["target_role"]
    )

    result = run_interview_turn(
        state=state,
        blueprint=request.blueprint,
        candidate_profile=request.candidate_profile
    )

    # Temporary session ID.
    # We'll improve session handling later.
    import uuid

    session_id = str(
        uuid.uuid4()
    )

    interview_sessions[session_id] = {
        "state": state,
        "blueprint": request.blueprint,
        "candidate_profile": request.candidate_profile
    }

    return {
        "session_id": session_id,
        **result
    }


# SUBMIT ANSWER

@router.post("/start")
def start_interview(
    request: StartInterviewRequest
):

    from app.models.interview import InterviewState

    state = InterviewState(
        target_role=request.blueprint["target_role"]
    )

    result = run_interview_turn(
        state=state,
        blueprint=request.blueprint,
        candidate_profile=request.candidate_profile
    )

    import uuid

    session_id = str(
        uuid.uuid4()
    )

    interview_sessions[session_id] = {
        "state": state,
        "blueprint": request.blueprint,
        "candidate_profile": request.candidate_profile
    }

    return {
        "session_id": session_id,
        **result
    }