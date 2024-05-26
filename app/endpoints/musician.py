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

@router.post("/musicians/", response_model=schemas.Musician, status_code=201)
def create_musician(musician: schemas.MusicianCreate, db: Session = Depends(get_db)):
    try:
        return crud.create_musician(db=db, musician=musician)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
