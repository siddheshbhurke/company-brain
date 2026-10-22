
from fastapi import FastAPI

from app.api.skills import router as skills_router
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(
    title="Company Brain API",
    description="Organizational Intelligence Layer for AI Agents",
    version="0.1.0",
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

app.include_router(skills_router)


@app.get("/")
def root():
    return {
        "project": "Company Brain",
        "status": "running",
        "version": "0.1.0",
    }


@app.get("/health")
def health():
    return {"status": "healthy"}
