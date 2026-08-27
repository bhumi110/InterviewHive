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

    if not file.filename:
        raise HTTPException(
            status_code=400,
            detail="No file provided."
        )

    if not file.filename.lower().endswith(".pdf"):
        raise HTTPException(
            status_code=400,
            detail="Only PDF files are supported."
        )

    try:

        file_bytes = await file.read()

        if not file_bytes:
            raise HTTPException(
                status_code=400,
                detail="Uploaded file is empty."
            )

        candidate_profile = parse_resume(
            file_bytes
        )

        return {
            "filename": file.filename,
            "candidate_profile": (
                candidate_profile.model_dump()
            )
        }

    except HTTPException:
        raise

    except Exception as e:

        print(
            "RESUME PARSING ERROR:",
            repr(e)
        )

        raise HTTPException(
            status_code=500,
            detail=str(e)
        )