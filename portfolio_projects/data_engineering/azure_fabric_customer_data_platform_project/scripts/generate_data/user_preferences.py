from faker import Faker
import pandas as pd
import random

# Initialize Faker and seed
fake = Faker()
Faker.seed(42)
random.seed(42)

# Load user_ids
users_df = pd.read_csv("/root/projects/portfolio_projects/data_engineering/azure_fabric_customer_data_platform_project/data/users.csv")
user_ids = users_df['user_id'].tolist()

# Sample pools
sports = ['Football', 'Basketball', 'Tennis', 'Cricket', 'Golf', 'Rugby', 'Baseball', 'Boxing', 'Hockey']
odds_formats = ['Decimal', 'Fractional', 'American', 'DECIMAL', 'fractional', 'AMERICAN', 'Dec', '', None]
marketing_choices = ['true', 'false', '1', '0', 'Yes', 'No', 'TRUE', 'FALSE', None]

# Generate preferences data
preferences_data = []

for user_id in user_ids:
    # 15% chance user has no preferences
    if random.random() < 0.15:
        continue

    # Choose 1–4 sports, with a 10% chance of repeating some
    favorite_sports = random.choices(sports, k=random.randint(1, 4))
    if random.random() < 0.1:
        favorite_sports += favorite_sports[:1]
    favorite_sports_str = ",".join(favorite_sports)

    # 10% chance of null odds format
    odds_format = None if random.random() < 0.1 else random.choice(odds_formats)

    # 5% chance of missing marketing value
    marketing_opt_in = None if random.random() < 0.05 else random.choice(marketing_choices)

    preferences_data.append({
        "user_id": user_id,
        "favorite_sports": favorite_sports_str,
        "odds_format": odds_format,
        "marketing_opt_in": marketing_opt_in
    })

# Save to CSV
preferences_df = pd.DataFrame(preferences_data)
output_path = "/root/projects/portfolio_projects/data_engineering/azure_fabric_customer_data_platform_project/data/user_preferences.csv"
preferences_df.to_csv(output_path, index=False)
print(f"Generated {len(preferences_df)} user_preferences records with realistic imperfections. Saved to {output_path}.")
