import json
import uuid
from app.schemas import DayPlan, TripRequest, PlanDetails, PlaceDetails
from google import genai
import os
from dotenv import load_dotenv
import requests
 
load_dotenv()

def get_weather_forecast(req: TripRequest):
    api_key = os.getenv("WEATHER_API_KEY")
    url = f"https://weather.visualcrossing.com/VisualCrossingWebServices/rest/services/timeline/{req.location}?unitGroup=metric&key={api_key}&include=days"
    
    # Uncomment for actual API call
    response = requests.get(url)
    response.raise_for_status()
    data = response.json()

    # Dummy data used for testing
    # test_data = {'queryCost': 1, 'latitude': 13.6983, 'longitude': 123.4889, 'resolvedAddress': 'Goa', 'address': 'Goa', 'timezone': 'Asia/Manila', 'tzoffset': 8.0, 'days': [{'datetime': '2025-10-26', 'datetimeEpoch': 1761408000, 'tempmax': 30.4, 'tempmin': 23.3, 'temp': 25.5, 'feelslikemax': 35.1, 'feelslikemin': 23.3, 'feelslike': 26.9, 'dew': 23.4, 'humidity': 88.9, 'precip': 5.9, 'precipprob': 100.0, 'precipcover': 45.83, 'preciptype': ['rain'], 'snow': 0.0, 'snowdepth': 0.0, 'windgust': 16.6, 'windspeed': 10.1, 'winddir': 116.3, 'pressure': 1010.7, 'cloudcover': 63.9, 'visibility': 20.2, 'solarradiation': 244.6, 'solarenergy': 21.0, 'uvindex': 9.0, 'severerisk': 60.0, 'sunrise': '05:38:50', 'sunriseEpoch': 1761428330, 'sunset': '17:21:05', 'sunsetEpoch': 1761470465, 'moonphase': 0.15, 'conditions': 'Rain, Partially cloudy', 'description': 'Partly cloudy throughout the day with storms possible.', 'icon': 'rain', 'stations': ['remote'], 'source': 'comb'}, {'datetime': '2025-10-27', 'datetimeEpoch': 1761494400, 'tempmax': 29.9, 'tempmin': 23.4, 'temp': 25.8, 'feelslikemax': 34.1, 'feelslikemin': 23.4, 'feelslike': 26.9, 'dew': 23.5, 'humidity': 87.7, 'precip': 6.7, 'precipprob': 64.5, 'precipcover': 41.67, 'preciptype': ['rain'], 'snow': 0.0, 'snowdepth': 0.0, 'windgust': 13.0, 'windspeed': 7.9, 'winddir': 129.0, 'pressure': 1011.1, 'cloudcover': 76.5, 'visibility': 22.2, 'solarradiation': 236.8, 'solarenergy': 20.5, 'uvindex': 9.0, 'severerisk': 60.0, 'sunrise': '05:39:05', 'sunriseEpoch': 1761514745, 'sunset': '17:20:39', 'sunsetEpoch': 1761556839, 'moonphase': 0.19, 'conditions': 'Rain, Partially cloudy', 'description': 'Partly cloudy throughout the day with storms possible.', 'icon': 'rain', 'stations': None, 'source': 'fcst'}, {'datetime': '2025-10-28', 'datetimeEpoch': 1761580800, 'tempmax': 30.0, 'tempmin': 23.8, 'temp': 25.7, 'feelslikemax': 33.9, 'feelslikemin': 23.8, 'feelslike': 26.9, 'dew': 23.4, 'humidity': 87.4, 'precip': 7.5, 'precipprob': 100.0, 'precipcover': 41.67, 'preciptype': ['rain'], 'snow': 0.0, 'snowdepth': 0.0, 'windgust': 11.2, 'windspeed': 6.8, 'winddir': 110.7, 'pressure': 1011.4, 'cloudcover': 76.1, 'visibility': 20.9, 'solarradiation': 233.2, 'solarenergy': 20.1, 'uvindex': 8.0, 'severerisk': 60.0, 'sunrise': '05:39:20', 'sunriseEpoch': 1761601160, 'sunset': '17:20:13', 'sunsetEpoch': 1761643213, 'moonphase': 0.22, 'conditions': 'Rain, Partially cloudy', 'description': 'Partly cloudy throughout the day with storms possible.', 'icon': 'rain', 'stations': None, 'source': 'fcst'}, {'datetime': '2025-10-29', 'datetimeEpoch': 1761667200, 'tempmax': 31.2, 'tempmin': 23.3, 'temp': 25.8, 'feelslikemax': 35.5, 'feelslikemin': 23.3, 'feelslike': 27.2, 'dew': 23.3, 'humidity': 86.9, 'precip': 4.7, 'precipprob': 93.5, 'precipcover': 29.17, 'preciptype': ['rain'], 'snow': 0.0, 'snowdepth': 0.0, 'windgust': 7.2, 'windspeed': 5.8, 'winddir': 4.6, 'pressure': 1011.2, 'cloudcover': 58.4, 'visibility': 22.5, 'solarradiation': 244.4, 'solarenergy': 21.0, 'uvindex': 9.0, 'severerisk': 60.0, 'sunrise': '05:39:36', 'sunriseEpoch': 1761687576, 'sunset': '17:19:48', 'sunsetEpoch': 1761729588, 'moonphase': 0.25, 'conditions': 'Rain, Partially cloudy', 'description': 'Partly cloudy throughout the day with storms possible.', 'icon': 'rain', 'stations': None, 'source': 'fcst'}, {'datetime': '2025-10-30', 'datetimeEpoch': 1761753600, 'tempmax': 30.8, 'tempmin': 23.1, 'temp': 25.6, 'feelslikemax': 34.7, 'feelslikemin': 23.1, 'feelslike': 26.9, 'dew': 23.0, 'humidity': 86.0, 'precip': 3.9, 'precipprob': 93.5, 'precipcover': 33.33, 'preciptype': ['rain'], 'snow': 0.0, 'snowdepth': 0.0, 'windgust': 6.8, 'windspeed': 4.3, 'winddir': 348.9, 'pressure': 1011.0, 'cloudcover': 75.7, 'visibility': 22.4, 'solarradiation': 238.9, 'solarenergy': 20.7, 'uvindex': 9.0, 'severerisk': 60.0, 'sunrise': '05:39:52', 'sunriseEpoch': 1761773992, 'sunset': '17:19:25', 'sunsetEpoch': 1761815965, 'moonphase': 0.25, 'conditions': 'Rain, Partially cloudy', 'description': 'Partly cloudy throughout the day with storms possible.', 'icon': 'rain', 'stations': None, 'source': 'fcst'}, {'datetime': '2025-10-31', 'datetimeEpoch': 1761840000, 'tempmax': 29.8, 'tempmin': 23.1, 'temp': 25.2, 'feelslikemax': 33.7, 'feelslikemin': 23.1, 'feelslike': 26.2, 'dew': 23.0, 'humidity': 87.9, 'precip': 12.5, 'precipprob': 90.3, 'precipcover': 29.17, 'preciptype': ['rain'], 'snow': 0.0, 'snowdepth': 0.0, 'windgust': 4.7, 'windspeed': 4.3, 'winddir': 101.7, 'pressure': 1010.9, 'cloudcover': 84.6, 'visibility': 20.6, 'solarradiation': 263.4, 'solarenergy': 22.6, 'uvindex': 8.0, 'severerisk': 60.0, 'sunrise': '05:40:10', 'sunriseEpoch': 1761860410, 'sunset': '17:19:02', 'sunsetEpoch': 1761902342, 'moonphase': 0.32, 'conditions': 'Rain, Partially cloudy', 'description': 'Partly cloudy throughout the day with storms possible.', 'icon': 'rain', 'stations': None, 'source': 'fcst'}, {'datetime': '2025-11-01', 'datetimeEpoch': 1761926400, 'tempmax': 30.1, 'tempmin': 23.1, 'temp': 25.3, 'feelslikemax': 33.9, 'feelslikemin': 23.1, 'feelslike': 26.2, 'dew': 22.8, 'humidity': 87.0, 'precip': 5.7, 'precipprob': 93.5, 'precipcover': 25.0, 'preciptype': ['rain'], 'snow': 0.0, 'snowdepth': 0.0, 'windgust': 5.8, 'windspeed': 5.4, 'winddir': 100.6, 'pressure': 1011.6, 'cloudcover': 28.0, 'visibility': 23.5, 'solarradiation': 244.1, 'solarenergy': 21.2, 'uvindex': 7.0, 'severerisk': 30.0, 'sunrise': '05:40:27', 'sunriseEpoch': 1761946827, 'sunset': '17:18:40', 'sunsetEpoch': 1761988720, 'moonphase': 0.35, 'conditions': 'Rain, Partially cloudy', 'description': 'Partly cloudy throughout the day with storms possible.', 'icon': 'rain', 'stations': None, 'source': 'fcst'}, {'datetime': '2025-11-02', 'datetimeEpoch': 1762012800, 'tempmax': 29.7, 'tempmin': 22.4, 'temp': 25.3, 'feelslikemax': 32.9, 'feelslikemin': 22.4, 'feelslike': 26.3, 'dew': 22.3, 'humidity': 84.5, 'precip': 1.3, 'precipprob': 93.5, 'precipcover': 12.5, 'preciptype': ['rain'], 'snow': 0.0, 'snowdepth': 0.0, 'windgust': 9.4, 'windspeed': 6.5, 'winddir': 28.5, 'pressure': 1011.8, 'cloudcover': 44.3, 'visibility': 24.1, 'solarradiation': 253.4, 'solarenergy': 22.1, 'uvindex': 8.0, 'severerisk': 30.0, 'sunrise': '05:40:46', 'sunriseEpoch': 1762033246, 'sunset': '17:18:20', 'sunsetEpoch': 1762075100, 'moonphase': 0.39, 'conditions': 'Rain, Partially cloudy', 'description': 'Partly cloudy throughout the day with storms possible.', 'icon': 'rain', 'stations': None, 'source': 'fcst'}, {'datetime': '2025-11-03', 'datetimeEpoch': 1762099200, 'tempmax': 28.0, 'tempmin': 23.2, 'temp': 25.1, 'feelslikemax': 31.0, 'feelslikemin': 23.2, 'feelslike': 26.0, 'dew': 22.8, 'humidity': 87.9, 'precip': 10.9, 'precipprob': 87.1, 'precipcover': 33.33, 'preciptype': ['rain'], 'snow': 0.0, 'snowdepth': 0.0, 'windgust': 13.7, 'windspeed': 8.6, 'winddir': 347.1, 'pressure': 1010.1, 'cloudcover': 90.3, 'visibility': 22.7, 'solarradiation': 203.6, 'solarenergy': 17.9, 'uvindex': 7.0, 'severerisk': 30.0, 'sunrise': '05:41:05', 'sunriseEpoch': 1762119665, 'sunset': '17:18:00', 'sunsetEpoch': 1762161480, 'moonphase': 0.42, 'conditions': 'Rain, Overcast', 'description': 'Cloudy skies throughout the day with storms possible.', 'icon': 'rain', 'stations': None, 'source': 'fcst'}, {'datetime': '2025-11-04', 'datetimeEpoch': 1762185600, 'tempmax': 25.1, 'tempmin': 23.9, 'temp': 24.4, 'feelslikemax': 25.1, 'feelslikemin': 23.9, 'feelslike': 24.4, 'dew': 23.4, 'humidity': 94.4, 'precip': 32.8, 'precipprob': 83.9, 'precipcover': 33.33, 'preciptype': ['rain'], 'snow': 0.0, 'snowdepth': 0.0, 'windgust': 52.2, 'windspeed': 24.1, 'winddir': 340.7, 'pressure': 1006.0, 'cloudcover': 99.8, 'visibility': 10.3, 'solarradiation': 51.9, 'solarenergy': 4.5, 'uvindex': 2.0, 'severerisk': 30.0, 'sunrise': '05:41:25', 'sunriseEpoch': 1762206085, 'sunset': '17:17:41', 'sunsetEpoch': 1762247861, 'moonphase': 0.45, 'conditions': 'Rain, Overcast', 'description': 'Cloudy skies throughout the day with storms possible.', 'icon': 'rain', 'stations': None, 'source': 'fcst'}, {'datetime': '2025-11-05', 'datetimeEpoch': 1762272000, 'tempmax': 25.0, 'tempmin': 23.2, 'temp': 24.3, 'feelslikemax': 25.0, 'feelslikemin': 23.2, 'feelslike': 24.3, 'dew': 23.3, 'humidity': 94.3, 'precip': 34.7, 'precipprob': 83.9, 'precipcover': 33.33, 'preciptype': ['rain'], 'snow': 0.0, 'snowdepth': 0.0, 'windgust': 53.6, 'windspeed': 24.1, 'winddir': 33.1, 'pressure': 1001.6, 'cloudcover': 100.0, 'visibility': 11.6, 'solarradiation': 53.1, 'solarenergy': 4.5, 'uvindex': 2.0, 'severerisk': 30.0, 'sunrise': '05:41:45', 'sunriseEpoch': 1762292505, 'sunset': '17:17:24', 'sunsetEpoch': 1762334244, 'moonphase': 0.5, 'conditions': 'Rain, Overcast', 'description': 'Cloudy skies throughout the day with storms possible.', 'icon': 'rain', 'stations': None, 'source': 'fcst'}, {'datetime': '2025-11-06', 'datetimeEpoch': 1762358400, 'tempmax': 26.8, 'tempmin': 23.3, 'temp': 24.6, 'feelslikemax': 29.4, 'feelslikemin': 23.3, 'feelslike': 24.7, 'dew': 23.2, 'humidity': 91.7, 'precip': 5.7, 'precipprob': 80.6, 'precipcover': 29.17, 'preciptype': ['rain'], 'snow': 0.0, 'snowdepth': 0.0, 'windgust': 31.3, 'windspeed': 17.3, 'winddir': 124.0, 'pressure': 1003.5, 'cloudcover': 97.3, 'visibility': 22.7, 'solarradiation': 189.1, 'solarenergy': 16.4, 'uvindex': 7.0, 'severerisk': 30.0, 'sunrise': '05:42:06', 'sunriseEpoch': 1762378926, 'sunset': '17:17:07', 'sunsetEpoch': 1762420627, 'moonphase': 0.52, 'conditions': 'Rain, Overcast', 'description': 'Cloudy skies throughout the day with storms possible.', 'icon': 'rain', 'stations': None, 'source': 'fcst'}, {'datetime': '2025-11-07', 'datetimeEpoch': 1762444800, 'tempmax': 29.3, 'tempmin': 22.9, 'temp': 25.3, 'feelslikemax': 32.0, 'feelslikemin': 22.9, 'feelslike': 26.1, 'dew': 22.1, 'humidity': 83.4, 'precip': 0.5, 'precipprob': 80.6, 'precipcover': 16.67, 'preciptype': ['rain'], 'snow': 0.0, 'snowdepth': 0.0, 'windgust': 17.3, 'windspeed': 10.4, 'winddir': 183.8, 'pressure': 1006.3, 'cloudcover': 99.6, 'visibility': 23.8, 'solarradiation': 234.4, 'solarenergy': 20.6, 'uvindex': 7.0, 'severerisk': 10.0, 'sunrise': '05:42:27', 'sunriseEpoch': 1762465347, 'sunset': '17:16:52', 'sunsetEpoch': 1762507012, 'moonphase': 0.55, 'conditions': 'Rain, Overcast', 'description': 'Cloudy skies throughout the day with rain in the morning and afternoon.', 'icon': 'rain', 'stations': None, 'source': 'fcst'}, {'datetime': '2025-11-08', 'datetimeEpoch': 1762531200, 'tempmax': 29.6, 'tempmin': 22.8, 'temp': 25.2, 'feelslikemax': 32.3, 'feelslikemin': 22.8, 'feelslike': 26.1, 'dew': 21.9, 'humidity': 82.9, 'precip': 2.0, 'precipprob': 77.4, 'precipcover': 8.33, 'preciptype': ['rain'], 'snow': 0.0, 'snowdepth': 0.0, 'windgust': 17.6, 'windspeed': 14.4, 'winddir': 199.8, 'pressure': 1007.4, 'cloudcover': 87.9, 'visibility': 23.8, 'solarradiation': 242.0, 'solarenergy': 21.0, 'uvindex': 8.0, 'severerisk': 30.0, 'sunrise': '05:42:50', 'sunriseEpoch': 1762551770, 'sunset': '17:16:37', 'sunsetEpoch': 1762593397, 'moonphase': 0.59, 'conditions': 'Rain, Partially cloudy', 'description': 'Partly cloudy throughout the day with storms possible.', 'icon': 'rain', 'stations': None, 'source': 'fcst'}, {'datetime': '2025-11-09', 'datetimeEpoch': 1762617600, 'tempmax': 27.7, 'tempmin': 22.7, 'temp': 24.5, 'feelslikemax': 30.6, 'feelslikemin': 22.7, 'feelslike': 25.0, 'dew': 22.5, 'humidity': 88.9, 'precip': 4.3, 'precipprob': 77.4, 'precipcover': 20.83, 'preciptype': ['rain'], 'snow': 0.0, 'snowdepth': 0.0, 'windgust': 12.2, 'windspeed': 9.4, 'winddir': 208.4, 'pressure': 1007.9, 'cloudcover': 99.9, 'visibility': 22.0, 'solarradiation': 156.5, 'solarenergy': 13.4, 'uvindex': 7.0, 'severerisk': 30.0, 'sunrise': '05:43:12', 'sunriseEpoch': 1762638192, 'sunset': '17:16:24', 'sunsetEpoch': 1762679784, 'moonphase': 0.62, 'conditions': 'Rain, Overcast', 'description': 'Cloudy skies throughout the day with storms possible.', 'icon': 'rain', 'stations': None, 'source': 'fcst'}]}
    
    # Extract 30-day forecast summary
    days = test_data.get("days", [])

    forecast_summary = []
    for day in days[:30]:
        forecast_summary.append({
            "date": day["datetime"],
            "temp": day["temp"],
            "conditions": day["conditions"]
        })
    
    return forecast_summary

def generate_trip_plan(req: TripRequest) -> PlanDetails:
    api_key = os.getenv("GEMINI_API_KEY")

    if not api_key:
        raise ValueError("Missing GOOGLE_API_KEY in environment")
    
    weather_data = get_weather_forecast(req)
    weather_summary = json.dumps(weather_data[:10], indent=2)

    client = genai.Client(api_key=api_key)

    prompt = f"""
        You are a travel planning assistant.

        Create a {req.days}-day travel itinerary for {req.location}.
        Based on the weather forecast below, recommend the best {req.days}-day trip plan 
        that avoids bad weather and includes sightseeing and activities that suit the conditions.

        Weather forecast (next 30 days):
        {weather_summary}

        For each day, include 2-4 recommended activities.

        Return ONLY valid JSON in this exact format:
        {{
        "best_start_date": recommended date to begin the trip,
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

    res = PlanDetails(id=str(uuid.uuid4()), start_date=parsed["best_start_date"], title=f"""{req.location} Trip""", days=trip_plan)

    # test_res = PlanDetails(id='2f546188-e8b6-4d15-988c-52e744661747', start_date='2025-10-26', title='Goa Trip', days=[DayPlan(id='acf0727c-2773-42f5-94ae-5f0f99906099', day=1, summary="Embrace the cool, rainy weather with a deep dive into Goa's rich history and culture. Explore ancient churches and the charming Latin Quarter, offering a mix of indoor and partially sheltered outdoor experiences. The day concludes with indoor entertainment options, perfect for a rainy evening.", places=[PlaceDetails(id='bf5e8061-d4b4-46e2-852d-921dd76fca86', name='Basilica of Bom Jesus', latitude=15.4983, longitude=73.9118), PlaceDetails(id='3f49b498-ad72-4912-8277-1426845bfa57', name='Se Cathedral', latitude=15.4989, longitude=73.9125), PlaceDetails(id='f102b764-3b99-4fee-8632-6e60d80808bf', name='Fontainhas (Latin Quarter), Panjim', latitude=15.496, longitude=73.824), PlaceDetails(id='95e6bc0e-02f3-4e11-b6c1-ebfd07e2b631', name='Deltin Royale Casino', latitude=15.5034, longitude=73.8341)]), DayPlan(id='070deec8-489a-440b-a77d-2ad3d837e18d', day=2, summary="Discover the lush green landscapes of Goa with a visit to a spice plantation, which provides a largely covered and educational experience. Afterwards, enjoy the serene beauty of South Goa's beaches from the comfort of a covered shack, or visit a historic fort for panoramic views, all while enjoying the intermittent rain and pleasant temperatures.", places=[PlaceDetails(id='0bca8449-a025-4844-9e03-954fe196a421', name='Sahakari Spice Farm', latitude=15.3942, longitude=74.0084), PlaceDetails(id='11e1e9f3-c7dd-44dc-919a-8cfc716500c8', name='Cabo de Rama Fort', latitude=15.048, longitude=73.935), PlaceDetails(id='c368b41a-a409-4f5b-bd20-affe5f59f2d8', name='Palolem Beach (for covered beach shack experience)', latitude=15.0069, longitude=74.0253)]), DayPlan(id='0a03a63a-9f2d-4e47-9114-4562716722c3', day=3, summary='Experience the vibrant markets and coastal charm of North Goa. Start with sheltered shopping at a local market, then enjoy a meal by the beach from a covered restaurant. Conclude your trip with a visit to a historic fort offering views of the Mandovi River, suitable for a partially cloudy, rainy day.', places=[PlaceDetails(id='41170f6e-8e94-44f2-ad87-bb52a726615e', name='Mapusa Market', latitude=15.5901, longitude=73.8116), PlaceDetails(id='6180f8c2-477e-4760-aefa-c5925b7e66f7', name='Reis Magos Fort', latitude=15.5225, longitude=73.8142), PlaceDetails(id='f8aec9c7-3990-435e-9a5c-a2c1575d7c66', name='Beach Shacks (e.g., Baga or Candolim Beach area)', latitude=15.5562, longitude=73.7533)])])
    return res
