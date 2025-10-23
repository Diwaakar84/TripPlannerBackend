import json
from app.schemas import TripRequest, TripResponse, DayPlan
from google import genai
import os
from dotenv import load_dotenv

load_dotenv()

def generate_trip_plan(req: TripRequest) -> TripResponse:
    api_key = os.getenv("GEMINI_API_KEY")

    if not api_key:
        raise ValueError("Missing GOOGLE_API_KEY in environment")
    
    client = genai.Client(api_key=api_key)

    prompt = f"""
        You are a travel planning assistant.

        Create a {req.days}-day travel itinerary for {req.location}.
        For each day, include 2-4 recommended activities.

        Return ONLY valid JSON in this exact format:
        {{
        "trip_plan": [
            {{
            "day": 1,
            "activities": ["Activity 1", "Activity 2", "Activity 3"]
            }}
        ]
        }}
        """
    response = client.models.generate_content(
        model="gemini-2.5-flash", 
        contents=prompt
    )
    
    try:
        # Some Gemini responses may include code block markers — strip them
        raw_text = response.text.strip().strip("`").replace("json", "")
        parsed = json.loads(raw_text)
    except Exception as e:
        print("⚠️ JSON parsing failed:", e)
        print("Raw output was:", response.text)
        raise ValueError("AI returned non-JSON response")

    # Convert parsed JSON into your response schema
    trip_plan = [
        DayPlan(day=day["day"], activities=day["activities"])
        for day in parsed["trip_plan"]
    ]

    return TripResponse(trip_plan=trip_plan)
