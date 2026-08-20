from fastapi import APIRouter, File, UploadFile, HTTPException

from app.services.resume_parser import parse_resume


router = APIRouter(
    prefix="/resume",
    tags=["Resume"]
)


@router.post("/parse")
async def parse_resume_endpoint(
    file: UploadFile = File(...)
):

    if file.content_type != "application/pdf":
        raise HTTPException(
            status_code=400,
            detail="Only PDF resumes are supported."
        )

    file_bytes = await file.read()

    try:
        candidate_profile = parse_resume(
            file_bytes
        )

        return {
            "success": True,
            "candidate": candidate_profile.model_dump()
        }

    except Exception as e:

        raise HTTPException(
            status_code=500,
            detail=f"Resume processing failed: {str(e)}"
        )