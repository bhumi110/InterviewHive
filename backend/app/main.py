from fastapi import FastAPI

from app.api.interview import router as interview_router


app = FastAPI(
    title="AI Interview Room",
    version="1.0.0"
)


app.include_router(
    interview_router,
    prefix="/api"
)


@app.get("/")
def root():

    return {
        "message": "AI Interview Room API is running"
    }