from fastapi import FastAPI

from app.api.diagnosis import router as diagnosis_router
from app.api.health import router as health_router
from app.api.evaluation import router as evaluation_router


app = FastAPI(
    title="AI IT Helpdesk Expert System",
    description=(
        "Knowledge-based IT diagnostic system using "
        "forward and backward chaining."
    ),
    version="0.1.0",
)


app.include_router(health_router)
app.include_router(diagnosis_router)
app.include_router(evaluation_router)


@app.get("/")
def root():
    return {
        "name": "AI IT Helpdesk Expert System",
        "version": "0.1.0",
        "status": "running",
    }