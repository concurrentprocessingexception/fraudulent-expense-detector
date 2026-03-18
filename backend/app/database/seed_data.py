import random
from datetime import datetime, timedelta

from faker import Faker

from .connection import SessionLocal
from .models import User, Transaction

fake = Faker()

MERCHANT_CATEGORIES = [
    "groceries",
    "restaurant",
    "electronics",
    "transport",
    "clothing",
    "entertainment",
    "travel",
]

PAYMENT_METHODS = [
    "credit_card",
    "debit_card",
    "online_transfer",
]

DEVICE_TYPES = [
    "mobile",
    "web",
    "pos_terminal",
]

CITIES_NL = [
    "Amsterdam",
    "Rotterdam",
    "Utrecht",
    "The Hague",
    "Eindhoven",
]


def create_users(db, n=10):

    users = []

    for _ in range(n):

        user = User(
            name=fake.name(),
            home_country="Netherlands"
        )

        db.add(user)
        users.append(user)

    db.commit()

    for u in users:
        db.refresh(u)

    return users


def create_normal_transactions(db, user, n=400):

    base_date = datetime.now() - timedelta(days=90)

    for _ in range(n):

        category = random.choice(MERCHANT_CATEGORIES)

        amount_ranges = {
            "groceries": (20, 120),
            "restaurant": (15, 80),
            "electronics": (50, 300),
            "transport": (5, 40),
            "clothing": (30, 200),
            "entertainment": (10, 70),
            "travel": (100, 500),
        }

        min_amt, max_amt = amount_ranges[category]

        txn = Transaction(
            user_id=user.user_id,
            amount=random.uniform(min_amt, max_amt),
            merchant=fake.company(),
            merchant_category=category,
            country="Netherlands",
            city=random.choice(CITIES_NL),
            payment_method=random.choice(PAYMENT_METHODS),
            device_type=random.choice(DEVICE_TYPES),
            timestamp=base_date + timedelta(days=random.randint(0, 90)),
        )

        db.add(txn)

    db.commit()


def create_fraud_transactions(db, user):

    fraud_cases = [

        # large electronics purchase abroad
        {
            "amount": random.uniform(900, 2000),
            "category": "electronics",
            "country": "Singapore",
            "city": "Singapore",
        },

        # unusual travel purchase
        {
            "amount": random.uniform(800, 1500),
            "category": "travel",
            "country": "Thailand",
            "city": "Bangkok",
        },

        # abnormal clothing purchase
        {
            "amount": random.uniform(600, 1200),
            "category": "clothing",
            "country": "United States",
            "city": "New York",
        },
    ]

    for fraud in fraud_cases:

        txn = Transaction(
            user_id=user.user_id,
            amount=fraud["amount"],
            merchant=fake.company(),
            merchant_category=fraud["category"],
            country=fraud["country"],
            city=fraud["city"],
            payment_method="credit_card",
            device_type="mobile",
            timestamp=datetime.now(),
        )

        db.add(txn)

    db.commit()


def seed_database():

    db = SessionLocal()

    print("Creating users...")

    users = create_users(db)

    print("Generating normal transactions...")

    for user in users:
        create_normal_transactions(db, user)

    print("Injecting fraud transactions...")

    for user in users:
        create_fraud_transactions(db, user)

    db.close()

    print("Seeding complete.")


if __name__ == "__main__":
    seed_database()