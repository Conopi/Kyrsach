from sqlalchemy import Column, ForeignKey, Integer, String, Float, Date
from sqlalchemy.orm import relationship
from .database import Base

class Ensemble(Base):
    __tablename__ = "ensembles"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True)
    leader = Column(String)

    musicians = relationship("Musician", back_populates="ensemble")
    cds = relationship("CD", back_populates="ensemble")
    musics = relationship("Music", back_populates="ensemble")

class Musician(Base):
    __tablename__ = "musicians"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    instrument = Column(String)
    ensemble_id = Column(Integer, ForeignKey("ensembles.id"))

    ensemble = relationship("Ensemble", back_populates="musicians")

class Music(Base):
    __tablename__ = "music"
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    composer = Column(String)
    ensemble_id = Column(Integer, ForeignKey("ensembles.id"))

    ensemble = relationship("Ensemble", back_populates="musics")
    performances = relationship("Performance", back_populates="music")

class CD(Base):
    __tablename__ = "cds"
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    release_date = Column(Date)
    wholesale_price = Column(Float)
    retail_price = Column(Float)
    sold_last_year = Column(Integer)
    sold_this_year = Column(Integer)
    stock = Column(Integer)
    ensemble_id = Column(Integer, ForeignKey("ensembles.id"))
    company = Column(String)
    company_address = Column(String)

    ensemble = relationship("Ensemble", back_populates="cds")
    performances = relationship("Performance", back_populates="cd")

class Performance(Base):
    __tablename__ = "performances"
    id = Column(Integer, primary_key=True, index=True)
    cd_id = Column(Integer, ForeignKey("cds.id"))
    music_id = Column(Integer, ForeignKey("music.id"))
    performer = Column(String)

    cd = relationship("CD", back_populates="performances")
    music = relationship("Music", back_populates="performances")
