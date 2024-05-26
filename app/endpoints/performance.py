import logging
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
