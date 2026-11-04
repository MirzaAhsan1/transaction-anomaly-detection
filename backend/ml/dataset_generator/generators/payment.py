import random

from ml.dataset_generator.config import (
    PAYMENT_METHODS,
    TRANSACTION_TYPES,
    CURRENCIES,
)


def generate_payment():
    return {
        "currency": random.choice(CURRENCIES),
        "transaction_type": random.choice(TRANSACTION_TYPES),
        "payment_method": random.choice(PAYMENT_METHODS),
    }