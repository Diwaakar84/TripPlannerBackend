from pydantic import BaseModel
from typing import List

class TripRequest(BaseModel):
    location: str
    days: int

class DayPlan(BaseModel):
    day: int
    activities: List[str]

class TripResponse(BaseModel):
    trip_plan: List[DayPlan]
