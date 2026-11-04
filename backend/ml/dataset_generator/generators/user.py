import random

from faker import Faker

fake = Faker()

def generate_user():

    return {

        "sender_name": fake.name(),

        "sender_account_number": fake.bban(),

        "receiver_name": fake.name(),

        "receiver_account_number": fake.bban(),

        "merchant_name": fake.company(),

    }