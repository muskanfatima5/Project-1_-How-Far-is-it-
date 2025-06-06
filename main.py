from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import openrouteservice

app = FastAPI()

# 🔑 Paste your ORS API key here:
ORS_API_KEY = "5b3ce3597851110001cf624863a326ea13214066b1b8965157cfd788"

# ORS client setup
client = openrouteservice.Client(key=ORS_API_KEY)

# 🚀 Input model
class RouteRequest(BaseModel):
    source: str
    destination: str

# 🛣️ Output route
@app.post("/route")
def get_route(data: RouteRequest):
    try:
        # 1. Convert addresses to coordinates
        src = client.pelias_search(text=data.source)['features'][0]['geometry']['coordinates']
        dest = client.pelias_search(text=data.destination)['features'][0]['geometry']['coordinates']

        # 2. Get route info (driving)
        route = client.directions(
            coordinates=[src, dest],
            profile='driving-car',
            format='json'
        )

        distance_km = route['routes'][0]['summary']['distance'] / 1000  # meters to km
        duration_min = route['routes'][0]['summary']['duration'] / 60   # seconds to minutes

        return {
            "distance_km": round(distance_km, 2),
            "duration_min": round(duration_min, 2)
        }

    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))







# python -m uvicorn main:app --reload
# this is the command for running