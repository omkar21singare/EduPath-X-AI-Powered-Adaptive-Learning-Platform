from fastapi import APIRouter
from app.evaluation.evaluator import evaluator
from app.schemas.schemas import EvaluationRequest, EvaluationResponse

router = APIRouter(prefix="/api/evaluation", tags=["Evaluation"])

@router.post("/run", response_model=EvaluationResponse)
def run_evaluation(payload: EvaluationRequest):
    res = evaluator.run_evaluation(num_trials=payload.num_trials, days_to_simulate=payload.days_to_simulate)
    return EvaluationResponse(**res)
