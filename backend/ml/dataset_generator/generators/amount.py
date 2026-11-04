import random

from ml.dataset_generator.config import (
    MIN_AMOUNT,
    MAX_AMOUNT,
)


def generate_amount(is_fraud: bool) -> float:
    """
    Generate realistic transaction amount.
    """

    if is_fraud:

        if random.random() < 0.70:
            return round(random.uniform(2500, MAX_AMOUNT), 2)

        return round(random.uniform(1000, 3000), 2)

    # Normal Transactions

    r = random.random()

    if r < 0.60:
        return round(random.uniform(5, 100), 2)

    if r < 0.90:
        return round(random.uniform(100, 1000), 2)

    return round(random.uniform(1000, 2500), 2)