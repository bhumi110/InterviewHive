from fastapi import FastAPI

from app.api.resume import router as resume_router


app = FastAPI(
    title="AI Interview Room",
    description="Multi-agent AI interview preparation system",
    version="0.1.0"
)


app.include_router(resume_router)


@app.get("/")
def root():
    return {
        "message": "AI Interview Room API is running"
    }


@app.get("/health")
def health():
    return {
        "status": "healthy"
    }