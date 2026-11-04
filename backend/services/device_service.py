import logging
from user_agents import parse
from fastapi import Request

logger = logging.getLogger(__name__)

def parse_user_agent(ua_string: str) -> dict:
    """
    Parses a User-Agent string to extract browser, OS, and device type information.
    """
    if not ua_string:
        logger.warning("Empty User-Agent string provided.")
        return {
            "browser": "Unknown",
            "browser_version": "",
            "operating_system": "Unknown",
            "os_version": "",
            "device_type": "Unknown"
        }
    
    try:
        user_agent = parse(ua_string)
        
        device_type = "Desktop"
        if user_agent.is_mobile:
            device_type = "Mobile"
        elif user_agent.is_tablet:
            device_type = "Tablet"
        elif user_agent.is_bot:
            device_type = "Bot"

        return {
            "browser": user_agent.browser.family or "Unknown",
            "browser_version": user_agent.browser.version_string or "",
            "operating_system": user_agent.os.family or "Unknown",
            "os_version": user_agent.os.version_string or "",
            "device_type": device_type
        }
    except Exception as e:
        logger.error(f"Error parsing User-Agent: {e}")
        return {
            "browser": "Unknown",
            "browser_version": "",
            "operating_system": "Unknown",
            "os_version": "",
            "device_type": "Unknown"
        }



def get_client_ip(request: Request) -> str:
    """
    Get the real client IP address.
    Supports proxies and load balancers.
    """

    forwarded_for = request.headers.get("X-Forwarded-For")

    if forwarded_for:
        return forwarded_for.split(",")[0].strip()

    real_ip = request.headers.get("X-Real-IP")

    if real_ip:
        return real_ip

    return request.client.host