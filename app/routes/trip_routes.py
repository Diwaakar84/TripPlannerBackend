from fastapi import APIRouter
from app.schemas import TripRequest, PlanDetails
from app.services.trip_service import generate_trip_plan

router = APIRouter()

@router.post("/generate", response_model=PlanDetails)
async def create_trip_plan(request: TripRequest):
    """
    Generate a trip plan based on location and number of days.
    """
    return generate_trip_plan(request)
