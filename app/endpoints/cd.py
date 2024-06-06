from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from .. import crud, schemas
from ..database import SessionLocal
import logging

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/cds/", response_model=schemas.CD, operation_id="create_cd")
def create_cd(cd: schemas.CDCreate, db: Session = Depends(get_db)):
    try:
        return crud.create_cd(db=db, cd=cd)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.put("/cds/{cd_id}", response_model=schemas.CD, operation_id="update_cd")
def update_cd(cd_id: int, cd: schemas.CDCreate, db: Session = Depends(get_db)):
    db_cd = crud.update_cd(db=db, cd_id=cd_id, cd_update=cd)
    if db_cd is None:
        raise HTTPException(status_code=404, detail="CD not found")
    return db_cd

@router.get("/cds/top-selling/", response_model=List[schemas.CD], operation_id="get_top_selling_cds")
def get_top_selling_cds(db: Session = Depends(get_db)):
    return crud.get_top_selling_cds(db=db)

logger = logging.getLogger("uvicorn.error")

@router.delete("/cds/{cd_id}", response_model=schemas.CD)
def delete_cd(cd_id: int, db: Session = Depends(get_db)):
    try:
        logger.info(f"Received request to delete CD with id: {cd_id}")
        cd = crud.get_cd(db, cd_id=cd_id)
        if not cd:
            raise HTTPException(status_code=404, detail="CD not found")
        return crud.delete_cd(db=db, cd_id=cd_id)
    except Exception as e:
        logger.error(f"Error deleting CD: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")
