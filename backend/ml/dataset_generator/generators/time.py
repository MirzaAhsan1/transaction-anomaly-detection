import random
from datetime import timedelta

from ml.dataset_generator.config import (
    START_DATE,
    END_DATE
)

def generate_datetime():

    delta = END_DATE - START_DATE

    seconds = random.randint(
        0,
        int(delta.total_seconds())
    )

    return START_DATE + timedelta(seconds=seconds)