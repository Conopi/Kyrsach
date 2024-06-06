import logging
from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from .. import crud, schemas
from ..database import SessionLocal

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

logger = logging.getLogger("uvicorn.error")

@router.post("/performances/", response_model=schemas.Performance)
def create_performance(performance: schemas.PerformanceCreate, db: Session = Depends(get_db)):
    try:
        logger.info(f"Received request to create performance: {performance}")
        return crud.create_performance(db=db, performance=performance)
    except Exception as e:
        logger.error(f"Error creating performance: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")

@router.get("/cd/{cd_id}/performances", response_model=List[schemas.Performance])
def get_performances_by_cd(cd_id: int, db: Session = Depends(get_db)):
    performances = crud.get_performances_by_cd(db, cd_id)
    if performances is None:
        raise HTTPException(status_code=404, detail="Performances not found")
    return performances
