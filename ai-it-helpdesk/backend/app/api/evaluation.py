from fastapi import APIRouter

from app.evaluation.evaluator import InferenceEvaluator
from app.evaluation.summary import EvaluationSummary

router = APIRouter(
    prefix="/api/evaluation",
    tags=["Evaluation"],
)


@router.get("/summary")
def get_evaluation_summary():
    evaluator = InferenceEvaluator()
    results = evaluator.evaluate_all()

    summary = EvaluationSummary(results).calculate()

    return {
        "summary": summary,
        "scenarios": results,
    }