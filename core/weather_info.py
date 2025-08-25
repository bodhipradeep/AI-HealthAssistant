import requests
import os
from dotenv import load_dotenv
load_dotenv()

Weather_Api_Key = os.getenv("WEATHER_API_KEY")


def get_weather(location: str) -> dict:
    # Example: open-meteo, weatherapi.com, or your API
    url = f"http://api.weatherapi.com/v1/current.json?key={Weather_Api_Key}&q={location}&days=3"
    res = requests.get(url).json()
    
    if "current" not in res:
        # API returned error
        return {"Error": res.get("error", {"message": "Weather API returned unexpected data"})}

    weather_info = {
        "Condition": res["current"]["condition"]["text"],
        "Temperature": f"{res['current']['temp_c']} °C",
        "Humidity": f"{res['current']['humidity']}%",
        "Air Quality": res["current"].get("air_quality", {}),
        "Rainfall": f"{res['current'].get('precip_mm', 0)} mm",
        "Pressure": f"{res['current']['pressure_mb']} mb",
        "Wind": f"{res['current']['wind_kph']} kph {res['current']['wind_dir']}",
        "UV Index": res["current"].get("uv", "N/A"),
        "Region": res["location"]["region"],
        "Local Time": res["location"]["localtime"]
    }
    return weather_info