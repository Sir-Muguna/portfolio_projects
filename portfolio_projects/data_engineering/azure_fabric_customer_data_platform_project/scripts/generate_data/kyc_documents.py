from faker import Faker
import pandas as pd
import random
import uuid
from datetime import datetime, timedelta

# Initialize Faker and seed
fake = Faker()
Faker.seed(42)
random.seed(42)

# Load users data
users_df = pd.read_csv("/root/projects/portfolio_projects/data_engineering/azure_fabric_customer_data_platform_project/data/users.csv")
user_ids = users_df['user_id'].tolist()

# Configurations
document_types = ['Passport', 'Driver License', 'National ID', 'Utility Bill']
verification_statuses = ['Verified', 'Pending', 'Rejected', '', 'invalid']
document_versions_per_type = [1, 2, 3]

# Define 20 compliance employees
compliance_names = [
    "jane.doe", "john.smith", "emily.jones", "michael.brown", "sarah.davis",
    "daniel.miller", "lisa.wilson", "kevin.moore", "laura.taylor", "brian.anderson",
    "olivia.thomas", "joshua.jackson", "emma.white", "ryan.harris", "megan.martin",
    "alex.robinson", "chloe.clark", "nathan.lewis", "zoe.lee", "benjamin.walker"
]
compliance_domain = "@boltbettingcompliance.com"

# Generate KYC data
kyc_data = []

for user_id in user_ids:
    if random.random() < 0.1:
        continue  # 10% of users have no documents

    doc_types_for_user = random.sample(document_types, k=random.choice([1, 2, 3]))

    for doc_type in doc_types_for_user:
        num_versions = random.choices(document_versions_per_type, weights=[0.6, 0.3, 0.1])[0]

        base_date = fake.date_between(start_date='-2y', end_date='-1y')

        for version in range(num_versions):
            # Generate sequential upload dates
            upload_date = base_date + timedelta(days=random.randint(version * 30, (version + 1) * 30))

            # Choose status
            status = random.choice(verification_statuses)

            # 10% chance of missing verifier
            if random.random() > 0.1:
                verifier_name = random.choice(compliance_names)
                verified_by = f"{verifier_name}{compliance_domain}"
            else:
                verified_by = ''

            # Introduce inconsistencies
            doc_type_variant = doc_type if random.random() > 0.03 else "Scan_" + doc_type
            status = status if random.random() > 0.05 else 'UNKNOWN'

            kyc_data.append({
                'document_id': str(uuid.uuid4()),
                'user_id': user_id,
                'document_type': doc_type_variant,
                'upload_date': upload_date.strftime('%Y-%m-%d'),
                'status': status,
                'verified_by': verified_by
            })

# Create and save DataFrame
kyc_df = pd.DataFrame(kyc_data)

# Ensure column order
kyc_df = kyc_df[['document_id', 'user_id', 'document_type', 'upload_date', 'status', 'verified_by']]

output_path = "/root/projects/portfolio_projects/data_engineering/azure_fabric_customer_data_platform_project/data/kyc_documents.csv"
kyc_df.to_csv(output_path, index=False)
print(f"Generated {len(kyc_df)} KYC records with document_id and document versioning. Saved to {output_path}.")
