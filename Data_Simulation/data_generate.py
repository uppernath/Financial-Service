import pandas as pd
import random
from faker import Faker
from tqdm import tqdm
import os
import logging
from pathlib import Path
import argparse
from typing import Tuple, List

# Setup Logging
logging.basicConfig(
    format="%(asctime)s - %(levelname)s - %(message)s",
    level=logging.INFO
)

# Initialize Faker and Seed
fake = Faker()
Faker.seed(42)
random.seed(42)

# Global merchant and country data
MERCHANTS: List[Tuple[str, str]] = [
    ('amazon', 'online'), ('walmart', 'retail'), ('mcdonalds', 'restaurant'),
    ('shell', 'gas'), ('starbucks', 'restaurant'), ('target', 'retail'),
    ('uber', 'transport'), ('netflix', 'subscription'), ('paypal', 'financial'),
    ('apple', 'online'), ('google', 'online'), ('microsoft', 'online')
]

COUNTRIES: List[str] = ['US', 'GB', 'DE', 'FR', 'CA', 'IN', 'BR', 'ZA', 'NG', 'CN', 'RU']

# Generate a chunk of fake data
def generate_fraud_data_chunk(num_records: int) -> pd.DataFrame:
    """
    Generate a chunk of synthetic fraud transaction data.

    Args:
        num_records (int): Number of records to generate.

    Returns:
        pd.DataFrame: A DataFrame containing synthetic fraud transaction data.
    """
    users = [fake.uuid4() for _ in range(num_records // 8)]
    data = []

    for _ in range(num_records):
        user_id = random.choice(users)
        merchant_name, merchant_category = random.choice(MERCHANTS)
        device_type = random.choice(['mobile', 'desktop', 'tablet'])

        hour = random.randint(8, 22) if random.random() < 0.7 else random.randint(0, 23)
        transaction_time = fake.date_time_between(start_date='-2y', end_date='now').replace(hour=hour)

        amount_ranges = {
            'restaurant': (5, 150),
            'retail': (10, 500),
            'gas': (20, 100),
            'online': (15, 300),
            'transport': (10, 80),
            'subscription': (5, 50),
            'financial': (50, 1000)
        }

        min_amt, max_amt = amount_ranges.get(merchant_category, (10, 200))
        amount = round(random.uniform(min_amt, max_amt), 2)
        if amount > 300 and random.random() < 0.7:
            amount = round(random.uniform(min_amt, 300), 2)

        payment_method = random.choices(
            ['credit_card', 'debit_card', 'digital_wallet', 'bank_transfer'],
            weights=[45, 35, 15, 5]
        )[0]

        country = random.choice(COUNTRIES)
        location = f"{fake.city()}, {fake.state_abbr()}, {country}"

        ip_address = fake.ipv4_private() if random.random() < 0.05 else fake.ipv4_public()
        is_private_ip = ip_address.startswith(('10.', '192.', '172.'))

        device_id = f"device_{hash(user_id) % 10000:04d}"

        transaction_type = random.choices(
            ['purchase', 'withdrawal', 'transfer', 'refund'],
            weights=[75, 15, 8, 2]
        )[0]

        transaction_status = random.choices(
            ['completed', 'failed', 'pending'],
            weights=[92, 6, 2]
        )[0]

        # Risk score and fraud logic
        fraud_score = 0
        if amount > 500: fraud_score += 30
        if amount > 1000: fraud_score += 20
        if hour < 6 or hour > 23: fraud_score += 15
        if merchant_category == 'online': fraud_score += 10
        if payment_method == 'digital_wallet': fraud_score += 5
        if transaction_status == 'failed': fraud_score += 25
        if is_private_ip: fraud_score += 20

        fraud_score += random.randint(-5, 10)
        risk_score = max(0, min(100, fraud_score))
        is_fraud = risk_score > 70 and random.random() < 0.3

        data.append({
            'transaction_id': fake.uuid4(),
            'user_id': user_id,
            'transaction_timestamp': transaction_time,
            'transaction_amount': amount,
            'merchant_id': f"merchant_{merchant_name}",
            'merchant_category': merchant_category,
            'payment_method': payment_method,
            'ip_address': ip_address,
            'geolocation': location,
            'device_id': device_id,
            'device_type': device_type,
            'transaction_type': transaction_type,
            'transaction_status': transaction_status,
            'is_fraud': is_fraud,
            'risk_score': risk_score
        })

    return pd.DataFrame(data)


# Write data to CSV in chunks
def stream_to_csv(filename: str, output_dir: str = "output", total_records: int = 500_000, chunk_size: int = 50_000) -> None:
    """
    Streams generated fraud data to a CSV file in chunks.

    Args:
        filename (str): Name of the output CSV file.
        output_dir (str): Directory to save the CSV file.
        total_records (int): Total number of records to generate.
        chunk_size (int): Number of records per chunk.
    """
    Path(output_dir).mkdir(parents=True, exist_ok=True)
    full_path = Path(output_dir) / filename

    first_chunk = True
    for i in tqdm(range(0, total_records, chunk_size), desc="Saving to CSV"):
        chunk_df = generate_fraud_data_chunk(min(chunk_size, total_records - i))
        chunk_df.to_csv(full_path, mode='a', header=first_chunk, index=False)
        first_chunk = False

    logging.info(f"✅ CSV saved to {full_path.absolute()}")


# Command line interface
def main():
    parser = argparse.ArgumentParser(description="Generate synthetic fraud transaction data.")
    parser.add_argument('--filename', type=str, default='fraud_data.csv', help='Output CSV filename')
    parser.add_argument('--output_dir', type=str, default='output', help='Directory to save the file')
    parser.add_argument('--total_records', type=int, default=500_000, help='Total number of records to generate')
    parser.add_argument('--chunk_size', type=int, default=50_000, help='Number of records per chunk')
    args = parser.parse_args()

    logging.info(f"Generating {args.total_records} records in chunks of {args.chunk_size}")
    stream_to_csv(
        filename=args.filename,
        output_dir=args.output_dir,
        total_records=args.total_records,
        chunk_size=args.chunk_size
    )

if __name__ == "__main__":
    stream_to_csv("fraud_data.csv", output_dir="Data_Simulation", total_records=500_000, chunk_size=50_000)
