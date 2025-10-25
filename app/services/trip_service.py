import json
import uuid
from app.schemas import DayPlan, TripRequest, PlanDetails, PlaceDetails
from google import genai
import os
from dotenv import load_dotenv

load_dotenv()

def generate_trip_plan(req: TripRequest) -> PlanDetails:
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
                "summary": "A short summary about the things covered in the day and how the days experience will be."
                "places": [
                    {{
                        "name": "Name of place 1",
                        "latitude": "48.8584",
                        "longitude": "2.2945",
                    }},
                    ]
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
        
        # Dummy response to be used for testing
        # parsed = {'trip_plan': [{'day': '1', 'summary': "Immerse yourself in London's iconic history and royal grandeur. This day focuses on the majestic landmarks of Westminster and offers breathtaking views of the city.", 
                                #  'places': [{'name': 'Buckingham Palace', 'latitude': '51.5014', 'longitude': '-0.1419'}, {'name': 'Westminster Abbey', 'latitude': '51.4994', 'longitude': '-0.1275'}, {'name': 'Houses of Parliament & Big Ben', 'latitude': '51.5008', 'longitude': '-0.1246'}, {'name': 'London Eye', 'latitude': '51.5033', 'longitude': '-0.1196'}]}, {'day': '2', 'summary': "A day dedicated to London's vibrant cultural scene, exploring world-class museums, bustling squares, and charming entertainment districts.", 'places': [{'name': 'British Museum', 'latitude': '51.5194', 'longitude': '-0.1269'}, {'name': 'Trafalgar Square & National Gallery', 'latitude': '51.5089', 'longitude': '-0.1283'}, {'name': 'Covent Garden', 'latitude': '51.5132', 'longitude': '-0.1228'}, {'name': 'West End Theatre District', 'latitude': '51.5126', 'longitude': '-0.1293'}]}, {'day': '3', 'summary': 'Explore ancient fortresses, vibrant food markets, and take a leisurely stroll along the historic River Thames, blending history with modern London life.', 'places': [{'name': 'Tower of London', 'latitude': '51.5081', 'longitude': '-0.0759'}, {'name': 'Tower Bridge', 'latitude': '51.5055', 'longitude': '-0.0754'}, {'name': 'Borough Market', 'latitude': '51.5050', 'longitude': '-0.0900'}, {'name': "South Bank Walk (Shakespeare's Globe & Tate Modern)", 'latitude': '51.5076', 'longitude': '-0.0994'}]}]}
    except Exception as e:
        print("⚠️ JSON parsing failed:", e)
        print("Raw output was:", response.text)
        raise ValueError("AI returned non-JSON response")

    # Convert parsed JSON into your response schema
    trip_plan = []
    for day in parsed['trip_plan']:
        places = []
        for place in day['places']:
            places.append(PlaceDetails(id=str(uuid.uuid4()), name=place["name"], latitude=place["latitude"], longitude=place["longitude"]))
        trip_plan.append(DayPlan(id=str(uuid.uuid4()), day=day["day"], summary=day["summary"], places=places))

    res = PlanDetails(id=str(uuid.uuid4()), title=f"""{req.location} Trip""", days=trip_plan)
    print(res)
    return res
