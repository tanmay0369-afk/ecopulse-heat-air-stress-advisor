"""Live data from Open-Meteo (free, no API key, CC-BY; attribute Open-Meteo).
Needs internet. Not exercised in the offline test-suite."""
import requests

W = "https://api.open-meteo.com/v1/forecast"
A = "https://air-quality-api.open-meteo.com/v1/air-quality"


def fetch_hourly(lat: float, lon: float, timeout: int = 15):
    w = requests.get(W, params={"latitude": lat, "longitude": lon, "hourly": "temperature_2m,relative_humidity_2m",
                                "forecast_days": 1, "timezone": "Asia/Kolkata"}, timeout=timeout).json()["hourly"]
    a = requests.get(A, params={"latitude": lat, "longitude": lon, "hourly": "pm2_5",
                                "forecast_days": 1, "timezone": "Asia/Kolkata"}, timeout=timeout).json()["hourly"]
    out = []
    for i, t in enumerate(w["time"]):
        pm = a["pm2_5"][i] if i < len(a["pm2_5"]) else None
        if w["temperature_2m"][i] is None or w["relative_humidity_2m"][i] is None or pm is None:
            continue
        out.append({"hour": int(t[11:13]), "temp_c": w["temperature_2m"][i],
                    "rh": w["relative_humidity_2m"][i], "pm25": pm})
    return out
