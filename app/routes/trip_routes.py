from fastapi import APIRouter
from app.schemas import TripRequest, TripResponse
from app.services.trip_service import generate_trip_plan

router = APIRouter()

@router.post("/generate", response_model=TripResponse)
async def create_trip_plan(request: TripRequest):
    """
    Generate a trip plan based on location and number of days.
    """
    return generate_trip_plan(request)
