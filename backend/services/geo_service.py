import logging
import requests

logger = logging.getLogger(__name__)

def resolve_ip(ip_address: str) -> dict:
    """
    Resolves an IP address to geographic data.
    Designed so it can use a free IP geolocation provider during development 
    and can be replaced with MaxMind GeoLite2 or similar in production.
    """
    default_geo = {
        "country": "Unknown",
        "city": "Unknown",
        "region": "Unknown",
        "latitude": 0.0,
        "longitude": 0.0
    }
    
    if not ip_address or ip_address in ("127.0.0.1", "localhost", "::1"):
        logger.info(f"Local or empty IP detected ({ip_address}), returning mock geo data.")
        return {
            "country": "United States",
            "city": "San Francisco",
            "region": "California",
            "latitude": 37.7749,
            "longitude": -122.4194
        }
        
    try:
        # Using ip-api.com for free development IP geolocation
        url = f"http://ip-api.com/json/{ip_address}?fields=status,message,country,regionName,city,lat,lon"
        response = requests.get(url, timeout=3)
        
        if response.status_code == 200:
            data = response.json()
            if data.get("status") == "success":
                return {
                    "country": data.get("country", "Unknown"),
                    "city": data.get("city", "Unknown"),
                    "region": data.get("regionName", "Unknown"),
                    "latitude": float(data.get("lat", 0.0)) if data.get("lat") else 0.0,
                    "longitude": float(data.get("lon", 0.0)) if data.get("lon") else 0.0
                }
            else:
                logger.warning(f"IP Geolocation API error: {data.get('message')}")
        else:
            logger.warning(f"IP Geolocation API returned status code {response.status_code}")
    except Exception as e:
        logger.error(f"Error resolving IP {ip_address}: {e}")

    return default_geo
