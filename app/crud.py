from sqlalchemy.orm import Session, joinedload
from . import models, schemas
import logging
from fastapi import HTTPException

logger = logging.getLogger("uvicorn.error")

def get_ensemble(db: Session, ensemble_id: int):
    return db.query(models.Ensemble).filter(models.Ensemble.id == ensemble_id).first()

def get_ensemble_by_name(db: Session, name: str):
    return db.query(models.Ensemble).filter(models.Ensemble.name == name).first()

def create_ensemble(db: Session, ensemble: schemas.EnsembleCreate):
    db_ensemble = models.Ensemble(name=ensemble.name, leader=ensemble.leader)
    try:
        db.add(db_ensemble)
        db.commit()
        db.refresh(db_ensemble)
        return db_ensemble
    except Exception as e:
        db.rollback()
        raise e

def get_cds_by_ensemble(db: Session, ensemble_id: int):
    try:
        return db.query(models.CD).filter(models.CD.ensemble_id == ensemble_id).all()
    except Exception as e:
        raise e

def get_top_selling_cds(db: Session):
    return db.query(models.CD).order_by(models.CD.sold_this_year.desc()).limit(10).all()

def create_cd(db: Session, cd: schemas.CDCreate):
    existing_cd = db.query(models.CD).filter(models.CD.title == cd.title, models.CD.ensemble_id == cd.ensemble_id).first()
    if existing_cd:
        raise ValueError(f"CD with title '{cd.title}' already exists for ensemble ID {cd.ensemble_id}")

    db_cd = models.CD(**cd.dict())
    try:
        db.add(db_cd)
        db.commit()
        db.refresh(db_cd)
        return db_cd
    except Exception as e:
        db.rollback()
        raise e

def create_music(db: Session, music: schemas.MusicCreate):
    db_music = models.Music(**music.dict())
    try:
        db.add(db_music)
        db.commit()
        db.refresh(db_music)
        return db_music
    except Exception as e:
        db.rollback()
        raise e

def update_cd(db: Session, cd_id: int, cd_update: schemas.CDCreate):
    db_cd = db.query(models.CD).filter(models.CD.id == cd_id).first()
    if db_cd:
        for key, value in cd_update.dict().items():
            setattr(db_cd, key, value)
        db.commit()
        db.refresh(db_cd)
    return db_cd

def get_music_count_by_ensemble(db: Session, ensemble_id: int):
    return db.query(models.Music).filter(models.Music.ensemble_id == ensemble_id).count()

def create_musician(db: Session, musician: schemas.MusicianCreate):
    db_musician = models.Musician(**musician.dict())
    try:
        db.add(db_musician)
        db.commit()
        db.refresh(db_musician)
        return db_musician
    except Exception as e:
        db.rollback()
        raise e

def get_all_ensembles_with_musicians(db: Session):
    try:
        ensembles = db.query(models.Ensemble).options(joinedload(models.Ensemble.musicians)).all()
        return ensembles
    except Exception as e:
        raise e

def create_performance(db: Session, performance: schemas.PerformanceCreate):
    logger.info(f"Creating performance: {performance}")
    db_performance = models.Performance(**performance.dict())
    try:
        db.add(db_performance)
        db.commit()
        db.refresh(db_performance)
        logger.info(f"Performance created successfully: {db_performance}")
        return db_performance
    except Exception as e:
        db.rollback()
        logger.error(f"Error creating performance: {e}")
        raise e

def get_performances_by_cd(db: Session, cd_id: int):
    return db.query(models.Performance).filter(models.Performance.cd_id == cd_id).all()

def get_cd(db: Session, cd_id: int):
    return db.query(models.CD).filter(models.CD.id == cd_id).first()

def delete_cd(db: Session, cd_id: int):
    cd = db.query(models.CD).filter(models.CD.id == cd_id).first()
    if cd:
        db.delete(cd)
        db.commit()
        return cd
    else:
        raise HTTPException(status_code=404, detail="CD not found")
