from fastapi import FastAPI
from app.routes.trip_routes import router as trip_router

app = FastAPI(
    title="Trip Planner API",
    description="AI-powered trip planner backend",
    version="1.0.0"
)

app.include_router(trip_router, prefix="/trips", tags=["Trips"])

@app.get("/")
def root():
    return {"message": "Trip Planner Backend is running 🚀"}

# Run command
# uvicorn app.main:app --reload