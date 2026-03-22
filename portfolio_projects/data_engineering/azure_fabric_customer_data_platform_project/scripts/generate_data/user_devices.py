from faker import Faker
import pandas as pd
import random
import uuid
from datetime import datetime, timedelta

# Initialize Faker
fake = Faker()
Faker.seed(42)
random.seed(42)

# Load user_ids
users_df = pd.read_csv("/root/projects/portfolio_projects/data_engineering/azure_fabric_customer_data_platform_project/data/users_data.csv")
user_ids = users_df['user_id'].tolist()

# Device types and malformed IPs
device_types = ['iPhone', 'Android', 'Windows PC', 'MacBook', 'Linux', 'Tablet', 'Smart TV']
malformed_ips = ['999.999.999.999', 'abc.def.ghi.jkl', 'localhost', '', '0.0.0.0']

# Valid but inconsistent timestamp formats
timestamp_formats = [
    "%Y-%m-%d %H:%M:%S",       # ISO style
    "%d/%m/%Y %H:%M",          # European
    "%Y/%m/%d %I:%M %p",       # 12-hour with AM/PM
    "%b %d, %Y %H:%M",         # Jan 05, 2024 14:30
    "%Y-%m-%d",                # Just date
    "%m-%d-%Y %H:%M:%S",       # US-style with time
    "%d %B %Y, %H:%M"          # 05 January 2024, 14:30
]

# Generate device data
device_data = []

for user_id in user_ids:
    if random.random() < 0.2:
        continue  # 20% of users have no devices
    
    num_devices = random.randint(1, 3)
    
    for _ in range(num_devices):
        device_id = str(uuid.uuid4())

        # Device type with some noise
        device_type = random.choice(device_types)
        if random.random() < 0.02:
            device_type = "SmartToaster"

        # 5% malformed IPs
        ip_address = random.choice(malformed_ips) if random.random() < 0.05 else fake.ipv4_public()

        # Choose a valid timestamp format
        fmt = random.choice(timestamp_formats)
        base_time = fake.date_time_between(start_date='-2y', end_date='now')
        last_used = base_time.strftime(fmt)

        device_data.append({
            "device_id": device_id,
            "user_id": user_id,
            "device_type": device_type,
            "ip_address": ip_address,
            "last_used": last_used
        })

# Save to CSV
devices_df = pd.DataFrame(device_data)
output_path = "/root/projects/portfolio_projects/data_engineering/azure_fabric_customer_data_platform_project/data/user_devices.csv"
devices_df.to_csv(output_path, index=False)
print(f"Generated {len(devices_df)} user_devices records with valid but inconsistent date formats in last_used. Saved to {output_path}.")
