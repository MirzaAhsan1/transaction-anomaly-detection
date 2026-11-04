import random

from ml.dataset_generator.config import (
    MERCHANT_CATEGORIES,
    BANKS,
)


def generate_merchant():
    return {
        "merchant_category": random.choice(MERCHANT_CATEGORIES),
        "sender_bank": random.choice(BANKS),
        "receiver_bank": random.choice(BANKS),
    }