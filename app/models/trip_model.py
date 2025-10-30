from sqlalchemy import Column, Integer, String, JSON, DateTime
from datetime import datetime
from app.database import Base

class TripPlan(Base):
    __tablename__ = "trip_plans"

    id = Column(Integer, primary_key=True, index=True)
    location = Column(String, index=True)
    days = Column(Integer)
    response = Column(JSON)
    created_at = Column(DateTime, default=datetime.utcnow)
