from fastapi import APIRouter, HTTPException
from app.knowledge.questions import ALL_QUESTIONS

from app.models.api import (
    AnswerRequest,
    AnswerResponse,
    StartDiagnosisRequest,
    StartDiagnosisResponse,
)
from app.services.api_diagnostic_service import APIDiagnosticService
from app.services.session_service import SessionService


router = APIRouter(
    prefix="/api/diagnosis",
    tags=["Diagnosis"],
)

session_service = SessionService()
diagnostic_service = APIDiagnosticService()

def get_question(question_id: str):
    return next(
        (
            question
            for question in ALL_QUESTIONS
            if question.id == question_id
        ),
        None,
    )


@router.post(
    "/start",
    response_model=StartDiagnosisResponse,
)
def start_diagnosis(
    request: StartDiagnosisRequest,
):

    valid_categories = {
        "Network",
        "System Performance",
        "Authentication",
    }

    if request.category not in valid_categories:
        raise HTTPException(
            status_code=400,
            detail=f"Unsupported category: {request.category}",
        )

    session = session_service.create_session(
        category=request.category,
    )

    result = diagnostic_service.evaluate_session(
        session,
    )

    question = result["next_question"]

    if question is not None:
        session.asked_questions.append(
            question.id
        )

        session_service.save_session(session)

    return StartDiagnosisResponse(
        session_id=session.session_id,
        category=session.category,
        status=result["status"],
        question=question,
        selection_reason=result.get("selection_reason")
    )


@router.post(
    "/{session_id}/answer",
    response_model=AnswerResponse,
)
def submit_answer(
    session_id: str,
    request: AnswerRequest,
):

    session = session_service.get_session(
        session_id
    )

    if session is None:
        raise HTTPException(
            status_code=404,
            detail="Diagnostic session not found.",
        )

    if request.question_id not in session.asked_questions:
        raise HTTPException(
            status_code=400,
            detail="Question does not belong to this session.",
        )
    
    if request.question_id in session.answered_questions:
        raise HTTPException(
            status_code=400,
            detail="Question has already been answered.",
        )
    
    question = get_question(request.question_id)

    if question is None:
        raise HTTPException(
            status_code=400,
            detail="Invalid question ID.",
        )

    allowed_facts = {
        option.fact
        for option in question.options
    }

    if request.fact not in allowed_facts:
        raise HTTPException(
            status_code=400,
            detail=(
                f"Invalid answer for question {request.question_id}. "
                f"Expected one of: {sorted(allowed_facts)}"
            ),
        )
    

 
    session.facts.add(request.fact)

    session.answered_questions.append(
        request.question_id
    )

    result = diagnostic_service.evaluate_session(
        session
    )

    question = result["next_question"]

    if question is not None:
        session.asked_questions.append(
            question.id
        )

    if result["status"] == "diagnosed":
        session.status = "completed"

    session_service.save_session(session)

    return AnswerResponse(
        session_id=session.session_id,
        status=result["status"],
        question=question,
        diagnoses=result["diagnoses"],
        inference=result["inference"],
        forward_inference=result.get("forward_inference"),
        backward_inference=result.get("backward_inference", []),
        selection_reason=result.get("selection_reason")
    )