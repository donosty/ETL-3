from sqlalchemy import Column, Integer, Float, String, DateTime, BigInteger
from sqlalchemy.orm import declarative_base
from datetime import datetime

Base = declarative_base()

class Earthquake(Base):
    __tablename__ = 'raw_earthquakes'
    
    id = Column(String(50), primary_key=True)
    magnitude = Column(Float)
    place = Column(String(255))
    time_epoch = Column(BigInteger)
    update_epoch = Column(BigInteger)
    longitude = Column(Float)
    latitude = Column(Float)
    depth = Column(Float)
    extracted_at = Column(DateTime, default=datetime.now)