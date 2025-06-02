'''
- Generate comprehensive vendor spend data (all categories)
- Create realistic budget vs actual patterns
- Generate contract data with renewal cycles
- Include marketing vendor subcategories
- Add seasonal budget patterns and variance scenarios
'''
import pandas as pd
import numpy as np
import random
from faker import Faker
from datetime import datetime, timedelta

faker = Faker()
np.random.seed(42)
Faker.seed(42)

NUM_VENDORS = 1000
NUM_TRANSACTIONS = 100_000
FISCAL_YEARS = [2022, 2023, 2024, 2025]
CATEGORIES = ['IT', 'Marketing', 'Operations', 'HR', 'Facilities']
SUBCATEGORIES = {
    'IT': ['Software', 'Hardware', 'Cloud'],
    'Marketing': ['Digital Ads', 'SEO', 'Events'],
    'Operations': ['Logistics', 'Utilities'],
    'HR': ['Recruiting', 'Training'],
    'Facilities': ['Maintenance', 'Cleaning']
}
DEPARTMENTS = ['Sales', 'Finance', 'HR', 'Engineering', 'Admin']
COST_CENTERS = ['CC1001', 'CC1002', 'CC1003']
GL_ACCOUNTS = ['GL5001', 'GL5002', 'GL5003']

def generate_vendors(n):
    vendors = []
    for i in range(n):
        category = random.choice(CATEGORIES)
        subcategory = random.choice(SUBCATEGORIES[category])
        vendors.append({
            'vendor_id': f'V{i:04}',
            'vendor_name': faker.company(),
            'category': category,
            'subcategory': subcategory,
            'risk_score': round(random.uniform(0, 10), 2),
            'financial_health': random.choice(['Good', 'Average', 'Poor']),
            'location': faker.city(),
            'size': random.choice(['Small', 'Medium', 'Large']),
            'contract_start': faker.date_between(start_date='-3y', end_date='-1y'),
            'primary_contact': faker.email(),
            'payment_terms': random.choice(['Net 30', 'Net 45', 'Net 60']),
            'preferred_vendor_status': random.choice([True, False]),
            'spend_volume_tier': random.choice(['Low', 'Medium', 'High']),
            'contract_complexity': random.choice(['Low', 'Medium', 'High']),
            'renewal_frequency': random.choice(['Annual', 'Biennial']),
            'price_escalation_terms': random.choice(['CPI Linked', 'Fixed', 'Negotiated'])
        })
    return pd.DataFrame(vendors)

def generate_contracts(vendors_df):
    contracts = []
    for i, row in vendors_df.iterrows():
        start_date = row['contract_start']
        duration = random.choice([180, 365, 730])
        end_date = start_date + timedelta(days=duration)
        contracts.append({
            'contract_id': f'C{i:05}',
            'vendor_id': row['vendor_id'],
            'start_date': start_date,
            'end_date': end_date,
            'contract_value': round(np.random.normal(50_000, 15_000), 2),
            'payment_terms': row['payment_terms'],
            'renewal_option': random.choice(['Auto', 'Manual']),
            'price_escalation_clause': row['price_escalation_terms'],
            'auto_renewal': random.choice([True, False]),
            'termination_notice': f"{random.randint(30, 90)} days",
            'sla_terms': random.choice(['Standard', 'Custom', 'Strict']),
            'penalty_clauses': random.choice(['None', 'Moderate', 'Strict']),
            'renegotiation_opportunity': random.choice([True, False]),
            'volume_discounts': random.choice([True, False]),
            'preferred_rates': random.choice([True, False])
        })
    return pd.DataFrame(contracts)

def generate_transactions(vendors_df, n):
    txns = []
    for i in range(n):
        vendor = vendors_df.sample(1).iloc[0]
        date = faker.date_between(start_date='-3y', end_date='today')
        year = date.year
        month = date.month
        amount = round(np.random.normal(1000, 300), 2)
        txns.append({
            'transaction_id': f'TX{i:06}',
            'date': date,
            'vendor_id': vendor['vendor_id'],
            'amount': amount,
            'currency': 'USD',
            'category': vendor['category'],
            'subcategory': vendor['subcategory'],
            'department': random.choice(DEPARTMENTS),
            'cost_center': random.choice(COST_CENTERS),
            'gl_account': random.choice(GL_ACCOUNTS),
            'description': faker.sentence(nb_words=6),
            'status': random.choice(['Approved', 'Pending', 'Rejected']),
            'budget_line': f'BL{random.randint(100,999)}',
            'fiscal_year': year,
            'fiscal_month': month,
            'approval_level': random.choice(['Manager', 'Director', 'VP']),
            'contract_reference': f'C{random.randint(0, NUM_VENDORS-1):05}',
            'purchase_order': f'PO{random.randint(10000,99999)}',
            'invoice_number': f'INV{random.randint(100000,999999)}'
        })
    return pd.DataFrame(txns)

def generate_budget_plans():
    plans = []
    for year in FISCAL_YEARS:
        for month in range(1, 13):
            for cat in CATEGORIES:
                for sub in SUBCATEGORIES[cat]:
                    plans.append({
                        'budget_id': f'B{year}{month:02}{cat[:2].upper()}{sub[:2].upper()}',
                        'fiscal_year': year,
                        'fiscal_month': month,
                        'category': cat,
                        'subcategory': sub,
                        'department': random.choice(DEPARTMENTS),
                        'budget_allocated': round(np.random.normal(10_000, 3000), 2),
                        'budget_type': random.choice(['OPEX', 'CAPEX']),
                        'approval_status': random.choice(['Approved', 'Pending', 'Rejected']),
                        'budget_owner': faker.name(),
                        'variance_threshold': round(random.uniform(0.05, 0.2), 2),
                        'reallocation_allowed': random.choice([True, False]),
                        'forecasted_spend': round(np.random.normal(9500, 2500), 2),
                        'contingency_buffer': round(random.uniform(200, 1000), 2)
                    })
    return pd.DataFrame(plans)

def generate_benchmarks():
    data = []
    for cat in CATEGORIES:
        for sub in SUBCATEGORIES[cat]:
            low = random.randint(800, 1200)
            high = random.randint(1300, 2000)
            avg = round((low + high) / 2, 2)
            data.append({
                'category': cat,
                'subcategory': sub,
                'market_price_low': low,
                'market_price_high': high,
                'market_price_avg': avg,
                'pricing_model': random.choice(['Fixed', 'Tiered', 'Volume-Based']),
                'geographic_region': random.choice(['North America', 'Europe', 'APAC']),
                'last_updated': faker.date_between(start_date='-6m', end_date='today'),
                'data_source': random.choice(['Gartner', 'Internal', 'External Consultant']),
                'confidence_level': random.choice(['High', 'Medium', 'Low']),
                'trend_direction': random.choice(['Up', 'Down', 'Stable']),
                'seasonal_adjustment': random.choice([True, False]),
                'volume_tier_pricing': random.choice([True, False])
            })
    return pd.DataFrame(data)

def export_all():
    vendors_df = generate_vendors(NUM_VENDORS)
    contracts_df = generate_contracts(vendors_df)
    transactions_df = generate_transactions(vendors_df, NUM_TRANSACTIONS)
    budget_df = generate_budget_plans()
    benchmark_df = generate_benchmarks()

    vendors_df.to_csv('vendors.csv', index=False)
    contracts_df.to_csv('contracts.csv', index=False)
    transactions_df.to_csv('transactions.csv', index=False)
    budget_df.to_csv('budget_plans.csv', index=False)
    benchmark_df.to_csv('benchmarks.csv', index=False)

if __name__ == '__main__':
    export_all()
