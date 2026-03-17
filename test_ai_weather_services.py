import unittest

from services.tourism_ai_service import rerank_records
from services.weather_service import WeatherService


class TestAIWeatherServices(unittest.TestCase):
    def setUp(self):
        self.weather_service = WeatherService()
        self.places = [
            {"name": "Pretoria Art Museum", "description": "An indoor museum and cultural gallery with covered exhibitions."},
            {"name": "Botanical Gardens", "description": "A scenic outdoor garden ideal for walking and nature photography."},
            {"name": "Indoor Water Park", "description": "A cool indoor family venue with shaded activities and swimming."},
        ]

    def test_weather_snapshot_classification(self):
        snapshot = self.weather_service.snapshot_from_api_payload({
            "latitude": -25.7,
            "longitude": 28.2,
            "current": {
                "temperature_2m": 23.4,
                "apparent_temperature": 22.8,
                "precipitation": 2.1,
                "weather_code": 61,
                "wind_speed_10m": 11.2,
                "time": "2026-03-17T10:00"
            }
        })
        self.assertIsNotNone(snapshot)
        self.assertEqual(snapshot.condition, "rainy")

    def test_rainy_weather_prefers_indoor_places(self):
        suggestions = self.weather_service.score_places_for_weather(self.places, "rainy", limit=2)
        self.assertGreaterEqual(len(suggestions), 1)
        self.assertEqual(suggestions[0]["name"], "Pretoria Art Museum")

    def test_record_reranking_promotes_relevant_place(self):
        ranked = rerank_records("museum gallery in tshwane", self.places, limit=2)
        self.assertGreaterEqual(len(ranked), 1)
        self.assertEqual(ranked[0]["name"], "Pretoria Art Museum")


if __name__ == "__main__":
    unittest.main()