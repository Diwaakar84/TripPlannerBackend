from pydantic import BaseModel
from typing import List

class TripRequest(BaseModel):
    location: str
    days: int

class PlaceDetails(BaseModel): 
    id: str
    name: str
    latitude: float
    longitude: float

class DayPlan(BaseModel):
    id: str
    day: int
    summary: str
    places: List[PlaceDetails]

class PlanDetails(BaseModel):
    id: str 
    title: str
    days: List[DayPlan]

# class TripResponse(BaseModel):
#     trip_plan: List[DayPlan]
