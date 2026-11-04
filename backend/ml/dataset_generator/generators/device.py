import random

from ml.dataset_generator.config import (
    BROWSERS,
    DEVICE_TYPES,
    OPERATING_SYSTEMS,
    LANGUAGES,
    TIMEZONES,
)

def generate_device():

    width = random.choice([1280, 1366, 1440, 1600, 1920])

    height = random.choice([720, 768, 900, 1080])

    browser = random.choice(BROWSERS)

    os = random.choice(OPERATING_SYSTEMS)

    device = random.choice(DEVICE_TYPES)

    return {

        "browser": browser,

        "browser_version": "1.0",

        "operating_system": os,

        "os_version": "1.0",

        "device_type": device,

        "language": random.choice(LANGUAGES),

        "timezone": random.choice(TIMEZONES),

        "screen_width": width,

        "screen_height": height,

        "user_agent": f"{browser} {os}"

    }