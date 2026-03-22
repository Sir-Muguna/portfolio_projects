from faker import Faker
import pandas as pd
import random
from datetime import timedelta
import uuid

# Initialize Faker
fake = Faker()
Faker.seed(42)
random.seed(42)

# Load user_ids
users_df = pd.read_csv("/root/projects/portfolio_projects/data_engineering/azure_fabric_customer_data_platform_project/data/users_data.csv")
user_ids = users_df['user_id'].tolist()

# Parameters
num_records = 15000  # Increase volume for better simulation

# Possible values
txn_types = ['Deposit', 'Withdrawal', 'deposit', 'withdraw', 'Wd', '']
payment_methods = ['Bank Transfer', 'Credit Card', 'PayPal', 'Crypto', 'Cash', 'Mobile Money', 'mpesa', '']
statuses = ['Completed', 'Pending', 'Failed', 'cancelled', 'SUCCESS', '', 'processing']

# Timestamp formats (all valid)
timestamp_formats = [
    "%Y-%m-%d %H:%M:%S",
    "%d/%m/%Y %H:%M",
    "%b %d, %Y %H:%M",
    "%m-%d-%Y %I:%M %p",
    "%Y-%m-%d",
    "%d %B %Y, %H:%M"
]

# Generate data
transaction_data = []
for i in range(1, num_records + 1):
    txn_id = f"TSC{10000000 + i}"  # Custom format
    user_id = random.choice(user_ids)
    txn_type = random.choice(txn_types)

    # Simulate invalid/missing amounts
    amount = round(random.uniform(-100.0, 5000.0), 2) if random.random() > 0.02 else 0.0

    payment_method = random.choice(payment_methods)
    if random.random() < 0.02:
        payment_method = None

    status = random.choice(statuses)

    # Timestamp in inconsistent formats
    txn_dt = fake.date_time_between(start_date='-1y', end_date='now')
    txn_time = txn_dt.strftime(random.choice(timestamp_formats))

    # Randomly inject missing fields
    if random.random() < 0.01:
        txn_type = ''
    if random.random() < 0.01:
        status = ''

    transaction_data.append({
        "txn_id": txn_id,
        "user_id": user_id,
        "txn_type": txn_type,
        "amount": amount,
        "payment_method": payment_method,
        "status": status,
        "txn_time": txn_time
    })

# Save to CSV
txns_df = pd.DataFrame(transaction_data)
output_path = "/root/projects/portfolio_projects/data_engineering/azure_fabric_customer_data_platform_project/data/transactions.csv"
txns_df.to_csv(output_path, index=False)
print(f"Generated {len(txns_df)} transactions with formatted txn_ids and inconsistencies. Saved to {output_path}.")
