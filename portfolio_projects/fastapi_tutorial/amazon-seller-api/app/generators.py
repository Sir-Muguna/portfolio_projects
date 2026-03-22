import random
import pandas as pd
from faker import Faker

class AmazonDataGenerator:
    def __init__(self):
        self.fake = Faker()
        self.categories = [
            'Electronics', 'Home & Kitchen', 'Books', 'Toys', 'Clothing',
            'Beauty', 'Sports', 'Office Products', 'Garden & Outdoor'
        ]
        self.conditions = ['New', 'Used - Like New', 'Used - Very Good', 'Used - Good', 'Used - Acceptable']
        self.fba_warehouses = ['ABE2', 'CLT2', 'DFW6', 'EWR4', 'LAX9', 'MDW2', 'PHX3', 'SJC7', 'SMF1', 'TPA1']
        self.suppliers = [
            'RetailArbitrage Inc', 'Liquidation LLC', 'Closeout Deals', 'Wholesale Unlimited',
            'Bulk Distributors', 'Discount Suppliers', 'Online Retail Wholesale'
        ]

    def _asin(self):
        return f"B0{random.randint(100000000, 999999999)}"

    def _upc(self):
        return f"{random.randint(100000000000, 999999999999)}"

    def generate_master_sheet(self, num_entries=2500):
        """Generate the initial master sheet with products"""
        products = []

        for i in range(num_entries):
            purchase_date = self.fake.date_between(start_date='-600d', end_date='-30d')
            purchase_cost = round(random.uniform(5, 500), 2)
            quantity = random.randint(1, 50)

            # Occasional inconsistent identifiers
            asin = self._asin()
            if random.random() < 0.05:
                asin = random.choice(['Invalid', 'N/A', 'Pending', ''])

            upc = self._upc()
            if random.random() < 0.03:
                upc = random.choice(['UPC-', 'Unknown', str(random.randint(1000, 9999))])

            product = {
                'product_id': f"PROD_{i+1:04d}",
                'product_name': self.fake.catch_phrase(),
                'asin': asin,
                'upc': upc,
                'purchase_date': purchase_date,
                'purchase_cost': purchase_cost,
                'quantity_purchased': quantity,
                'total_cost': round(purchase_cost * quantity, 2),
                'supplier': random.choice(self.suppliers),
                'category': random.choice(self.categories),
                'condition': random.choice(self.conditions),
                'status': random.choice(['Not Sent', 'In Transit', 'At FBA', 'Sold', 'Returned']),
                'fba_warehouse': random.choice(self.fba_warehouses) if random.random() > 0.3 else '',
                'notes': self.fake.sentence() if random.random() > 0.7 else ''
            }
            products.append(product)

        return pd.DataFrame(products)

    def generate_daily_data(self, master_df, num_entries=100):
        """Generate daily data with specified number of entries (list[dict])"""
        if master_df is None or len(master_df) == 0:
            raise ValueError("Master sheet must be generated first")

        daily_entries = []

        existing_products = random.sample(list(master_df['product_id']), min(70, len(master_df)))

        for i in range(num_entries):
            if i < len(existing_products):
                product_id = existing_products[i]
                product_data = master_df[master_df['product_id'] == product_id].iloc[0].to_dict()
            else:
                # Create new product (not in master sheet)
                product_id = f"PROD_{len(master_df) + i + 1:04d}"
                product_data = {
                    'product_id': product_id,
                    'product_name': self.fake.catch_phrase(),
                    'asin': self._asin(),
                    'upc': self._upc(),
                    'purchase_date': self.fake.date_between(start_date='-30d', end_date='today'),
                    'purchase_cost': round(random.uniform(5, 500), 2),
                    'quantity_purchased': random.randint(1, 50),
                    'supplier': random.choice(self.suppliers),
                    'category': random.choice(self.categories),
                    'condition': random.choice(self.conditions),
                    'status': 'Not Sent',
                    'fba_warehouse': '',
                    'notes': ''
                }
                product_data['total_cost'] = round(product_data['purchase_cost'] * product_data['quantity_purchased'], 2)

            # Sales logic
            sale_date = self.fake.date_between(start_date='-7d', end_date='today')
            was_sold = random.random() > 0.4  # 60% chance of being sold

            if was_sold:
                selling_price = round(product_data['purchase_cost'] * random.uniform(1.5, 3.5), 2)
                quantity_sold = random.randint(1, min(product_data['quantity_purchased'], 10))
                total_revenue = round(selling_price * quantity_sold, 2)

                fulfillment_fee = round(random.uniform(2.5, 15.0), 2)
                referral_fee = round(total_revenue * 0.15, 2)
                storage_fee = round(random.uniform(0.5, 5.0), 2)
                total_fees = fulfillment_fee + referral_fee + storage_fee

                if random.random() < 0.1:
                    additional_fee = round(random.uniform(5, 30), 2)
                    fee_type = random.choice(['inbound_shipping', 'removal_fee', 'disposal_fee', 'long_term_storage'])
                    total_fees += additional_fee
                else:
                    additional_fee = 0
                    fee_type = ''

                had_returns = random.random() < 0.2
                if had_returns:
                    return_quantity = random.randint(1, min(2, quantity_sold))
                    return_reason = random.choice(['Customer changed mind', 'Defective', 'Wrong item sent', 'Late delivery'])
                else:
                    return_quantity = 0
                    return_reason = ''

                had_reimbursement = random.random() < 0.05
                if had_reimbursement:
                    reimbursement_amount = round(random.uniform(10, 200), 2)
                    reimbursement_reason = random.choice(['Lost inventory', 'Damaged in warehouse', 'Customer return not received'])
                else:
                    reimbursement_amount = 0
                    reimbursement_reason = ''

                net_profit = total_revenue - product_data['total_cost'] - total_fees - (selling_price * return_quantity) + reimbursement_amount
                status = 'Sold' if return_quantity == 0 else 'Returned'
            else:
                selling_price = 0
                quantity_sold = 0
                total_revenue = 0
                fulfillment_fee = 0
                referral_fee = 0
                storage_fee = 0
                additional_fee = 0
                fee_type = ''
                return_quantity = 0
                return_reason = ''
                reimbursement_amount = 0
                reimbursement_reason = ''
                total_fees = 0               # ✅ ensure defined
                net_profit = -product_data['total_cost']
                status = random.choice(['At FBA', 'In Transit', 'Not Sent'])

            # Introduce data issues (properly applied)
            if random.random() < 0.05:
                if random.random() < 0.5:
                    selling_price = None
                else:
                    product_data['asin'] = None   # ✅ update dict, not stray var

            # Consistent date as string
            if random.random() < 0.03:
                sale_date_str = sale_date.strftime('%m-%d-%Y')  # intentional format issue
            else:
                sale_date_str = sale_date.strftime('%Y-%m-%d')

            entry = {
                'product_id': product_data['product_id'],
                'product_name': product_data['product_name'],
                'asin': product_data.get('asin'),
                'upc': product_data.get('upc'),
                'sale_date': sale_date_str,
                'purchase_cost': product_data['purchase_cost'],
                'quantity_purchased': product_data['quantity_purchased'],
                'selling_price': selling_price,
                'quantity_sold': quantity_sold,
                'total_revenue': total_revenue,
                'fulfillment_fee': fulfillment_fee,
                'referral_fee': referral_fee,
                'storage_fee': storage_fee,
                'additional_fee': additional_fee,
                'fee_type': fee_type,
                'total_fees': total_fees,
                'return_quantity': return_quantity,
                'return_reason': return_reason,
                'reimbursement_amount': reimbursement_amount,
                'reimbursement_reason': reimbursement_reason,
                'net_profit': net_profit,
                'status': status,
                'category': product_data['category'],
                'condition': product_data['condition'],
                'supplier': product_data['supplier'],
                'fba_warehouse': product_data.get('fba_warehouse', ''),
                'data_quality_issues': random.random() < 0.1
            }

            daily_entries.append(entry)

        return daily_entries
