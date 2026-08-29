from fastapi import APIRouter, HTTPException

from app.services.interview_engine import generate_final_report
from app.api.interview import interview_sessions


router = APIRouter(
    prefix="/report",
    tags=["Report"]
)


@router.get("/{session_id}")
def get_interview_report(
    session_id: str
):

    # Find interview session
    session = interview_sessions.get(session_id)

    if session is None:
        raise HTTPException(
            status_code=404,
            detail="Interview session not found"
        )

    # Get interview state
    state = session["state"]

    # Report only available after interview completion
    if state.interview_status != "completed":
        raise HTTPException(
            status_code=400,
            detail="Interview has not been completed yet"
        )

    # Return cached report
    if state.final_report is not None:

        return {
            "status": "completed",
            "report": state.final_report
        }

    # Generate final report
    report = generate_final_report(
        state=state,
        candidate_profile=session["candidate_profile"],
        target_role=session["blueprint"]["target_role"]
    )

    # Cache report
    state.final_report = report.model_dump()

    return {
        "status": "completed",
        "report": state.final_report
    }