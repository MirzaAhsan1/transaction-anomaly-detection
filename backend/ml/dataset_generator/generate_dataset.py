import random
import pandas as pd
from faker import Faker

from ml.dataset_generator.config import (
    CURRENCIES,
    TRANSACTION_TYPES,
    PAYMENT_METHODS,
    MERCHANT_CATEGORIES
)
from pathlib import Path
from ml.dataset_generator.generators.amount import generate_amount
from ml.dataset_generator.generators.geo import generate_location
from ml.dataset_generator.generators.device import generate_device
from ml.dataset_generator.generators.user import generate_user
from ml.dataset_generator.generators.time import generate_datetime
from ml.dataset_generator.fraud_rules import calculate_risk

fake = Faker()


def generate_transaction():

      # 5% fraud, 95% normal
    is_fraud = random.random() < 0.05

    user = generate_user()

    device = generate_device()

    location = generate_location()

    transaction_time = generate_datetime()

    transaction = {

        "amount": generate_amount(is_fraud),

        "currency": random.choice(CURRENCIES),

        "transaction_type": random.choice(TRANSACTION_TYPES),

        "payment_method": random.choice(PAYMENT_METHODS),

        "transaction_time": transaction_time,

        "sender_name": user["sender_name"],

        "sender_account_number": user["sender_account_number"],

        "sender_bank": fake.company(),

        "receiver_name": user["receiver_name"],

        "receiver_account_number": user["receiver_account_number"],

        "receiver_bank": fake.company(),

        "merchant_name": user["merchant_name"],

        "merchant_category": random.choice(MERCHANT_CATEGORIES),

        "country": location["country"],

        "city": location["city"],

        "region": location["region"],

        "latitude": location["latitude"],

        "longitude": location["longitude"],

        "ip_address": fake.ipv4_public(),

        **device

    }

    return transaction


def add_features(transaction):

    transaction["transaction_hour"] = transaction["transaction_time"].hour

    transaction["transaction_day"] = transaction["transaction_time"].weekday()

    transaction["is_weekend"] = int(
        transaction["transaction_day"] >= 5
    )

    transaction["screen_area"] = (
        transaction["screen_width"]
        *
        transaction["screen_height"]
    )

    transaction["is_mobile"] = int(
        transaction["device_type"] == "Mobile"
    )

    return transaction


def label_transaction(transaction):

    risk = calculate_risk(transaction)

    transaction["risk_score"] = risk

    if risk >= 50:
        transaction["label"] = 1
    else:
        transaction["label"] = 0

    return transaction



def generate_dataset(size=50000):

    rows = []

    for _ in range(size):

        t = generate_transaction()

        t = add_features(t)

        t = label_transaction(t)

        rows.append(t)

    return pd.DataFrame(rows)


if __name__ == "__main__":

    print("Generating dataset...")

    df = generate_dataset(50000)

    script_dir = Path(__file__).resolve().parent

    # 2. Go up 3 levels to reach the 'backend' folder, then target 'dataset'
    target_dir = script_dir.parents[2] / "dataset"

    # 3. Create the 'dataset' directory if it doesn't exist
    target_dir.mkdir(parents=True, exist_ok=True)

    # 4. Define the final file path
    output_file = target_dir / "transactions.csv"

    # 5. Save the DataFrame
    df.to_csv(output_file, index=False)

    print(df.head())

    print()

    print(df["label"].value_counts())

    print()

    print("Dataset saved successfully.")