# 🧭 TripPlanner Backend

This is the backend service for the **AI-Powered Trip Planner** app.  
It provides intelligent trip itinerary generation based on location, duration, and real-time weather data.  
Built with **FastAPI** for speed, scalability, and easy integration with modern AI APIs.

---

## 🧩 Features

- ✅ AI-based itinerary generation using **Google Gemini**
- 🌦️ Weather-aware trip planning (via **Visual Crossing Weather API**)
- ⚡ Fast and asynchronous performance via FastAPI + Uvicorn

---

## 🏗️ Architecture Overview

**Flow:**
1. User sends location & number of days from iOS app.
2. Backend fetches weather forecast from Visual Crossing API.
3. Backend passes weather data to Gemini for analysis.
4. Gemini returns a JSON trip plan with best dates and daily itinerary.
5. Backend sends structured JSON back to frontend.


---

## ⚙️ Tech Stack & Libraries

| Library / Tool | Purpose | Reason for Choice |
|-----------------|----------|-------------------|
| **FastAPI** | Backend web framework | Modern, easy to scale, async-first |
| **google-genai** | Gemini API client | Large upto date data, Advanced multi-modal features |
| **Visual Crossing Weather API** | Weather data | Very accurate weather reports, JSON output |

---

## 🚀 Running the Backend

### 1. Clone the Repository
Open terminal and enter the following commands:
- git clone https://github.com/Diwaakar84/TripPlannerBackend.git
- cd TripPlannerBackend

### 2. Create and Activate a Virtual Environment
- python3 -m venv venv
- source venv/bin/activate

### 3. Install dependencies
- pip install -r requirements.txt

### 4. Setup Environment Variables
- Create a .env file in your root directory with the following:
GEMINI_API_KEY=your_gemini_key_here
WEATHER_API_KEY=your_weather_api_key_here
- Replace with your actual API keys

### 5. Run your server
- uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

---

## 📈 Current Progress
- ✅ AI trip plan generation working
- ✅ Weather API integrated
- ✅ iOS frontend connected via URLSession
- 🧩 Modularized codebase (routes, services, schemas)

---

## 🧠 System Design Notes
- Microservice-ready — the backend is modular and stateless, ready to scale via containers.
- Highly scalable

---

## 🔮 Future Enhancements
- 🪣 Caching for weather API responses
- 💸 Budgeting
- 📅 Customizable date options
  
