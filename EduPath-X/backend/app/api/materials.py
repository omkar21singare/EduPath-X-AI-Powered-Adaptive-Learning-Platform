from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.database.session import get_db
from app.models.models import LearningMaterial, ContentSource, Concept
from app.schemas.schemas import LearningMaterialResponse, ContentSourceResponse

router = APIRouter(prefix="/api/materials", tags=["Materials"])

@router.get("/sources", response_model=List[ContentSourceResponse])
def list_sources(db: Session = Depends(get_db)):
    return db.query(ContentSource).all()

@router.get("/{concept_id}", response_model=LearningMaterialResponse)
def get_material_for_concept(concept_id: int, db: Session = Depends(get_db)):
    mat = db.query(LearningMaterial).filter(LearningMaterial.concept_id == concept_id).first()
    if not mat:
        # Fallback to first material if specific not present
        mat = db.query(LearningMaterial).first()
        if not mat:
            raise HTTPException(status_code=404, detail="Material not found")

    return LearningMaterialResponse.from_orm(mat)
