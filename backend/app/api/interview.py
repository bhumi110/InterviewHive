from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
import uuid

from app.services.interview_engine import run_interview_turn
from app.services.role_analyzer import analyze_role
from app.models.interview import InterviewState


router = APIRouter(
    prefix="/interview",
    tags=["Interview"]
)


# REQUEST MODELS

class StartInterviewRequest(BaseModel):
    candidate_profile: dict
    target_role: str


class AnswerRequest(BaseModel):
    session_id: str
    answer: str


# TEMPORARY SESSION STORAGE

interview_sessions = {}


# START INTERVIEW

@router.post("/start")
def start_interview(
    request: StartInterviewRequest
):

    # 1. Analyze role

    blueprint = analyze_role(
        target_role=request.target_role,
        candidate_profile=request.candidate_profile
    )

    # If analyze_role returns a Pydantic model
    if hasattr(blueprint, "model_dump"):
        blueprint_dict = blueprint.model_dump()
    else:
        blueprint_dict = blueprint

    # 2. Create interview state

    state = InterviewState(
        target_role=request.target_role
    )

    # 3. Generate first interview question

    result = run_interview_turn(
        state=state,
        blueprint=blueprint_dict,
        candidate_profile=request.candidate_profile
    )

    # 4. Create temporary session

    session_id = str(uuid.uuid4())

    interview_sessions[session_id] = {
        "state": state,
        "blueprint": blueprint_dict,
        "candidate_profile": request.candidate_profile
    }

    # 5. Return response

    return {
        "session_id": session_id,
        **result
    }


# SUBMIT ANSWER

@router.post("/answer")
def submit_answer(
    request: AnswerRequest
):

    # 1. Find session

    session = interview_sessions.get(
        request.session_id
    )

    if session is None:

        raise HTTPException(
            status_code=404,
            detail="Interview session not found"
        )

    # 2. Retrieve interview data

    state = session["state"]

    blueprint = session["blueprint"]

    candidate_profile = session[
        "candidate_profile"
    ]

    # 3. Process candidate answer

    result = run_interview_turn(
        state=state,
        blueprint=blueprint,
        candidate_profile=candidate_profile,
        candidate_answer=request.answer
    )

    # 4. Return next turn

    return result