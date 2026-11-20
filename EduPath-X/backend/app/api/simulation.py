from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import Dict, Any, List
from app.database.session import get_db
from app.simulation.simulation_engine import simulation_engine, PROFILES
from app.schemas.schemas import SimulationSimulateDaysRequest, SimulationRunResponse

router = APIRouter(prefix="/api/simulation", tags=["Simulation"])

@router.get("/profiles")
def get_simulation_profiles():
    return [
        {"name": k, **v} for k, v in PROFILES.items()
    ]

@router.post("/simulate-days", response_model=SimulationRunResponse)
def simulate_days(req: SimulationSimulateDaysRequest, learner_id: int = 1, db: Session = Depends(get_db)):
    try:
        res = simulation_engine.simulate_days(db, learner_id, req.profile_name, req.days)
        return SimulationRunResponse(**res)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/reset")
def reset_simulation(learner_id: int = 1, db: Session = Depends(get_db)):
    return simulation_engine.reset_simulation(db, learner_id)
