from fastapi import APIRouter, UploadFile, File, HTTPException

from app.services.resume_parser import parse_resume


router = APIRouter(
    prefix="/resume",
    tags=["Resume"]
)


@router.post("/parse")
async def parse_resume_endpoint(
    file: UploadFile = File(...)
):

    # --------------------------------------------------------
    # Validate file
    # --------------------------------------------------------

    if not file.filename:
        raise HTTPException(
            status_code=400,
            detail="No file provided"
        )

    if not file.filename.lower().endswith(".pdf"):
        raise HTTPException(
            status_code=400,
            detail="Only PDF resumes are supported"
        )

    # --------------------------------------------------------
    # Read PDF
    # --------------------------------------------------------

    file_bytes = await file.read()

    if not file_bytes:
        raise HTTPException(
            status_code=400,
            detail="Uploaded file is empty"
        )

    # --------------------------------------------------------
    # Parse resume
    # --------------------------------------------------------

    try:

        candidate_profile = parse_resume(
            file_bytes
        )

    except Exception as e:

        raise HTTPException(
            status_code=500,
            detail=f"Resume parsing failed: {str(e)}"
        )

    # --------------------------------------------------------
    # Return candidate profile
    # --------------------------------------------------------

    return {
        "filename": file.filename,
        "candidate_profile": candidate_profile
    }