import random

LOCATIONS = [
    {
        "country": "United States",
        "city": "New York",
        "region": "New York",
        "latitude": 40.7128,
        "longitude": -74.0060,
    },
    {
        "country": "United Kingdom",
        "city": "London",
        "region": "England",
        "latitude": 51.5072,
        "longitude": -0.1276,
    },
    {
        "country": "Pakistan",
        "city": "Karachi",
        "region": "Sindh",
        "latitude": 24.8607,
        "longitude": 67.0011,
    },
    {
        "country": "Canada",
        "city": "Toronto",
        "region": "Ontario",
        "latitude": 43.6532,
        "longitude": -79.3832,
    },
    {
        "country": "Australia",
        "city": "Sydney",
        "region": "NSW",
        "latitude": -33.8688,
        "longitude": 151.2093,
    },
]

def generate_location():
    return random.choice(LOCATIONS)