from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.interview import router as interview_router
from app.api.resume import router as resume_router
from app.api.report import router as report_router


app = FastAPI(
    title="AI Interview Room",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(
    interview_router,
    prefix="/api"
)

app.include_router(
    resume_router,
    prefix="/api"
)
app.include_router(
    report_router,
    prefix="/api"
)


@app.get("/")
def root():

    return {
        "message": "AI Interview Room API is running"
    }
    
