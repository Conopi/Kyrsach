import logging
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from .. import crud, schemas
from ..database import SessionLocal


router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get("/ensembles/", response_model=List[schemas.Ensemble])
def read_ensembles(db: Session = Depends(get_db)):
    ensembles = crud.get_all_ensembles_with_musicians(db)
    return ensembles

@router.post("/ensembles/", response_model=schemas.Ensemble, status_code=201)
def create_ensemble(ensemble: schemas.EnsembleCreate, db: Session = Depends(get_db)):
    db_ensemble = crud.get_ensemble_by_name(db, name=ensemble.name)
    if db_ensemble:
        raise HTTPException(status_code=400, detail="Ensemble already registered")
    return crud.create_ensemble(db=db, ensemble=ensemble)

logger = logging.getLogger("uvicorn.error")

@router.get("/ensembles/{ensemble_id}/cds/", response_model=List[schemas.CD])
def read_cds_by_ensemble(ensemble_id: int, db: Session = Depends(get_db)):
    try:
        cds = crud.get_cds_by_ensemble(db, ensemble_id=ensemble_id)
        if cds is None:
            raise HTTPException(status_code=404, detail="Ensemble not found")
        return cds
    except Exception as e:
        logger.error(f"Error fetching CDs for ensemble {ensemble_id}: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")

@router.get("/ensembles/{ensemble_id}/music_count", response_model=int)
def get_music_count_by_ensemble(ensemble_id: int, db: Session = Depends(get_db)):
    count = crud.get_music_count_by_ensemble(db, ensemble_id=ensemble_id)
    if count is None:
        raise HTTPException(status_code=404, detail="Ensemble not found")
    return count
