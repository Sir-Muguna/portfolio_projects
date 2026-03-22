from faker import Faker
import random
import pandas as pd
from datetime import datetime, timedelta

# Initialize Faker
fake = Faker()
Faker.seed(42)
random.seed(42)

# Parameters
num_rows = 5000
kyc_statuses = ['Pending', 'Verified', 'Rejected', '', 'unknown']
account_statuses = ['Active', 'Suspended', 'Closed', 'active123', '', 'Pending']

malformed_dates = ['N/A', 'unknown', '31/04/1985', '12-31-1990', 'Feb 30 1992']

# Function to maybe corrupt a date
def maybe_corrupt_date(clean_date, allow_future=False):
    chance = random.random()
    if chance < 0.05:
        return random.choice(malformed_dates)  # 5% malformed
    elif chance < 0.10:
        return (datetime.today() + timedelta(days=random.randint(1, 365))).strftime('%Y-%m-%d') if allow_future else clean_date
    elif chance < 0.15:
        return '2050-01-01'  # Static future date
    return clean_date.strftime('%Y-%m-%d')

# Function to generate user records
def generate_user_data(n):
    data = []
    for i in range(1, n + 1):
        user_id = f"BB{10000000 + i:05d}"

        # Generate DOB and registration date
        dob_clean = fake.date_of_birth(minimum_age=18, maximum_age=80)
        reg_clean = fake.date_between(start_date=dob_clean + timedelta(days=6570), end_date='today')

        # Intentionally make some registration dates earlier than DOB
        if random.random() < 0.05:
            reg_clean = dob_clean - timedelta(days=random.randint(100, 3000))

        dob = maybe_corrupt_date(dob_clean, allow_future=True)
        reg_date = maybe_corrupt_date(reg_clean, allow_future=True)

        # Generate inconsistencies
        username = fake.user_name() if random.random() > 0.03 else None
        email = fake.email() if random.random() > 0.05 else ''
        country = fake.country_code() if random.random() > 0.02 else "U.K"
        kyc = random.choices(kyc_statuses, weights=[0.4, 0.3, 0.1, 0.1, 0.1])[0]
        acc_status = random.choices(account_statuses, weights=[0.5, 0.2, 0.1, 0.1, 0.05, 0.05])[0]

        data.append({
            "user_id": user_id,
            "username": username,
            "email": email,
            "first_name": fake.first_name(),
            "last_name": fake.last_name(),
            "date_of_birth": dob,
            "registration_date": reg_date,
            "country_code": country,
            "kyc_status": kyc,
            "account_status": acc_status
        })
    return pd.DataFrame(data)

# Generate and save
users_df = generate_user_data(num_rows)
users_df.to_csv("/root/projects/portfolio_projects/data_engineering/azure_fabric_customer_data_platform_project/data/users.csv", index=False)
print("Generated users.csv with", num_rows, "rows and intentional date inconsistencies.")
