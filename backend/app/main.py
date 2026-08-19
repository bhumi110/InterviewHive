from fastapi import FastAPI

app = FastAPI(
    title="AI Interview Room",
    description="Multi-agent AI interview preparation system",
    version="0.1.0"
)


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