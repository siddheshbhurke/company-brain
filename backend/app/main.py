from fastapi import FastAPI

app = FastAPI(
    title="Company Brain API",
    description="Organizational Intelligence Layer for AI Agents",
    version="0.1.0"
)


@app.get("/")
def root():
    return {
        "project": "Company Brain",
        "status": "running",
        "version": "0.1.0"
    }


@app.get("/health")
def health():
    return {
        "status": "healthy"
    }
