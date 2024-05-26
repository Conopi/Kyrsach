from typing import List, Optional
from pydantic import BaseModel
from datetime import date

class MusicBase(BaseModel):
    title: str
    composer: str

class MusicCreate(MusicBase):
    ensemble_id: int

class Music(MusicBase):
    id: int
    ensemble_id: int

    class Config:
        from_attributes = True

class CDBase(BaseModel):
    title: str
    release_date: date
    wholesale_price: float
    retail_price: float
    sold_last_year: int
    sold_this_year: int
    stock: int
    company: str
    company_address: str

class CDCreate(CDBase):
    ensemble_id: int

class CD(CDBase):
    id: int
    ensemble_id: int
    performances: List['Performance'] = []

    class Config:
        from_attributes = True

class PerformanceBase(BaseModel):
    performer: str

class PerformanceCreate(PerformanceBase):
    cd_id: int
    music_id: int

class Performance(PerformanceBase):
    id: int
    cd_id: int
    music_id: int
    music: Optional[Music] = None

    class Config:
        from_attributes = True

class MusicianBase(BaseModel):
    name: str
    instrument: str

class MusicianCreate(MusicianBase):
    ensemble_id: int

class Musician(MusicianBase):
    id: int
    ensemble_id: int

    class Config:
        from_attributes = True

class EnsembleBase(BaseModel):
    name: str
    leader: str

class EnsembleCreate(EnsembleBase):
    pass

class Ensemble(EnsembleBase):
    id: int
    musicians: List[Musician] = []
    musics: List[Music] = []

    class Config:
        from_attributes = True
