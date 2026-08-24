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

    session = interview_sessions.get(
        session_id
    )

    if session is None:

        raise HTTPException(
            status_code=404,
            detail="Interview session not found"
        )

    state = session["state"]

    if state.interview_status != "completed":

        raise HTTPException(
            status_code=400,
            detail="Interview has not been completed yet"
        )

    # Return existing report if already generated
    if state.final_report is not None:

        return {
            "status": "completed",
            "report": state.final_report
        }

    report = generate_final_report(
        state=state,
        candidate_profile=session[
            "candidate_profile"
        ],
        target_role=session[
            "blueprint"
        ]["target_role"]
    )

    return {
        "status": "completed",
        "report": report.model_dump()
    }