from __future__ import annotations

from dataclasses import asdict, dataclass
from datetime import datetime
from typing import Any, Dict, Iterable, List, Optional

import requests

DEFAULT_TSHWANE_COORDS = {"latitude":-25.7479, "longitude": 28.2293}

WEATHER_REASONING = {
    "sunny": {"keywords": ["outdoor", "park", "garden", "hiking", "monument", "scenic", "nature"], "avoid": ["indoor", "covered"], "reason": "Great weather for outdoor exploration."},
    "rainy": {"keywords": ["indoor", "museum", "gallery", "shopping", "theater", "cultural", "covered"], "avoid": ["outdoor", "hiking"], "reason": "Better to focus on indoor or covered attractions."},
    "cloudy": {"keywords": ["walking", "city", "historic", "market", "cultural", "photography"], "avoid": [], "reason": "Comfortable conditions for city walks and sightseeing."},
    "hot": {"keywords": ["water", "shade", "indoor", "cool", "air-conditioned", "swimming"], "avoid": ["hiking", "strenuous"], "reason": "Look for cooler or shaded experiences."},
    "cold": {"keywords": ["indoor", "warm", "cozy", "heated", "shelter", "hot drinks"], "avoid": ["outdoor", "water"], "reason": "Warm indoor activities are the best fit."},
    "windy": {"keywords": ["indoor", "sheltered", "stable"], "avoid": ["outdoor", "high places"], "reason": "Sheltered venues are safer and more comfortable."},
    "mild": {"keywords": ["walking", "outdoor", "sightseeing", "flexible", "family"], "avoid": [], "reason": "The weather suits a broad mix of activities."},
}


@dataclass(frozen=True)
class WeatherSnapshot:
    location_name: str
    latitude: float
    longitude: float
    temperature_c: float
    apparent_temperature_c: float
    wind_speed_kmh: float
    precipitation_mm: float
    weather_code: int
    condition: str
    observed_at: str

    def as_dict(self) -> Dict[str, Any]:
        return asdict(self)


class WeatherService:
    """Fetches live weather and scores tourism recommendations against weather conditions."""

    def classify_condition(self, temperature_c: float, wind_speed_kmh: float,
                           precipitation_mm: float, weather_code: int) -> str:
        if precipitation_mm > 0 or weather_code in {51, 53, 55, 61, 63, 65, 80, 81, 82, 95}:
            return "rainy"
        if wind_speed_kmh >= 28:
            return "windy"
        if temperature_c >= 29:
            return "hot"
        if temperature_c <= 12:
            return "cold"
        if weather_code in {0, 1}:
            return "sunny"
        if weather_code in {2, 3, 45, 48}:
            return "cloudy"
        return "mild"

    def snapshot_from_api_payload(self, payload: Dict[str, Any], location_name: str="Tshwane") -> Optional[WeatherSnapshot]:
        current = payload.get("current") or {}
        if not current:
            return None

        temperature = float(current.get("temperature_2m", 0.0))
        apparent = float(current.get("apparent_temperature", temperature))
        wind_speed = float(current.get("wind_speed_10m", 0.0))
        precipitation = float(current.get("precipitation", 0.0))
        weather_code = int(current.get("weather_code", 0))
        observed_at = current.get("time") or datetime.utcnow().isoformat()

        return WeatherSnapshot(
            location_name=location_name,
            latitude=float(payload.get("latitude", DEFAULT_TSHWANE_COORDS["latitude"])),
            longitude=float(payload.get("longitude", DEFAULT_TSHWANE_COORDS["longitude"])),
            temperature_c=temperature,
            apparent_temperature_c=apparent,
            wind_speed_kmh=wind_speed,
            precipitation_mm=precipitation,
            weather_code=weather_code,
            condition=self.classify_condition(temperature, wind_speed, precipitation, weather_code),
            observed_at=observed_at,
        )

    def fetch_current_weather(self, location_name: str="Tshwane", latitude: float=DEFAULT_TSHWANE_COORDS["latitude"],
                              longitude: float=DEFAULT_TSHWANE_COORDS["longitude"]) -> Optional[WeatherSnapshot]:
        try:
            response = requests.get(
                "https://api.open-meteo.com/v1/forecast",
                params={
                    "latitude": latitude,
                    "longitude": longitude,
                    "current": "temperature_2m,apparent_temperature,precipitation,weather_code,wind_speed_10m",
                    "timezone": "auto",
                    "forecast_days": 1,
                },
                timeout=10,
            )
            response.raise_for_status()
            return self.snapshot_from_api_payload(response.json(), location_name=location_name)
        except Exception:
            return None

    def format_summary(self, snapshot: WeatherSnapshot) -> str:
        condition = snapshot.condition.capitalize()
        return (
            f"Live weather in {snapshot.location_name}: {condition}, {snapshot.temperature_c:.1f}°C "
            f"(feels like {snapshot.apparent_temperature_c:.1f}°C), wind {snapshot.wind_speed_kmh:.1f} km/h."
        )

    def score_places_for_weather(self, places_data: Iterable[Dict[str, Any]], weather_condition: str,
                                 temp_df: Any=None, limit: int=5) -> List[Dict[str, Any]]:
        normalized_condition = str(weather_condition or "mild").lower()
        if normalized_condition in {"auto", "current", "live"}:
            snapshot = self.fetch_current_weather()
            normalized_condition = snapshot.condition if snapshot else "mild"

        if temp_df is not None and hasattr(temp_df, "columns") and {"weather", "place"}.issubset(set(temp_df.columns)):
            weather_series = temp_df["weather"].fillna("").astype(str).str.lower()
            valid_places = temp_df[weather_series == normalized_condition]["place"].tolist()
            suggestions = []
            for place in places_data:
                if place.get("name") in valid_places:
                    enriched = dict(place)
                    enriched["weather_suitability_score"] = 5
                    enriched["reason"] = f"Matched the historical temperature dataset for {normalized_condition} weather."
                    suggestions.append(enriched)
            if suggestions:
                return suggestions[:limit]

        reasoning = WEATHER_REASONING.get(normalized_condition, WEATHER_REASONING["mild"])
        suggestions: List[Dict[str, Any]] = []
        for place in places_data:
            content = " ".join(str(place.get(field, "")) for field in ("name", "description", "content", "type", "category")).lower()
            positive_score = sum(1 for keyword in reasoning["keywords"] if keyword in content)
            negative_score = sum(1 for keyword in reasoning["avoid"] if keyword in content)
            final_score = max(0, min(5, positive_score - negative_score))
            if final_score > 0:
                enriched = dict(place)
                enriched["weather_suitability_score"] = final_score
                enriched["reason"] = reasoning["reason"]
                suggestions.append(enriched)

        suggestions.sort(key=lambda item: item.get("weather_suitability_score", 0), reverse=True)
        return suggestions[:limit]
