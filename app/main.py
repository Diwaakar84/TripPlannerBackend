from app.database import engine, Base
from fastapi import FastAPI
from app.routes.trip_routes import router as trip_router

app = FastAPI(
    title="Trip Planner API",
    description="AI-powered trip planner backend",
    version="1.0.0"
)

# Initialize the DB
Base.metadata.create_all(bind=engine)

app.include_router(trip_router, prefix="/trips", tags=["Trips"])

@app.get("/")
def root():
    return {"message": "Trip Planner Backend is running 🚀"}

# Run command
# uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload