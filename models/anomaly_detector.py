'''
File: models/anomaly_detector.py
Purpose: Detect budget variances and unusual spending patterns
Python pseudocode
# FP&A-focused anomaly types:
# - Budget overruns and underruns
# - Seasonal spending anomalies
# - Vendor payment pattern changes
# - Contract compliance violations
# - Duplicate payments and billing errors

def detect_anomalies(spend_data, budget_data):
    # Budget variance threshold analysis
    # Statistical outlier detection for spending patterns
    # Contract compliance monitoring
    # Seasonal adjustment for anomaly detection
    # Multi-dimensional anomaly scoring
    return anomaly_alerts, budget_impact, recommended_actions

'''

import pandas as pd
from sklearn.ensemble import IsolationForest
from sklearn.preprocessing import OneHotEncoder, StandardScaler
import numpy as np

def detect_anomalies(spend_data: pd.DataFrame, budget_data: pd.DataFrame):
    data = pd.merge(
        spend_data, budget_data,
        on=['department', 'category', 'month', 'year'],
        suffixes=('_spend', '_budget')
    )

    data['variance'] = data['actual_spend'] - data['budget']
    data['utilization'] = data['actual_spend'] / data['budget'].replace(0, 1)
    data['month_sin'] = np.sin(2 * np.pi * data['month'] / 12)
    data['month_cos'] = np.cos(2 * np.pi * data['month'] / 12)

    data['budget_overrun'] = data['variance'] > (0.1 * data['budget'])  # 10% over budget
    data['budget_underrun'] = data['variance'] < (-0.1 * data['budget']) # 10% under budget

    categorical = ['department', 'category', 'vendor']
    numerical = ['actual_spend', 'budget', 'variance', 'utilization', 'month_sin', 'month_cos']
    encoder = OneHotEncoder(sparse=False, handle_unknown='ignore')
    cat_encoded = encoder.fit_transform(data[categorical])
    scaler = StandardScaler()
    num_scaled = scaler.fit_transform(data[numerical])
    X = np.hstack([num_scaled, cat_encoded])
    model = IsolationForest(contamination=0.05, random_state=42)
    data['anomaly_score'] = model.fit_predict(X)

    data['rolling_mean'] = data.groupby(['department', 'category'])['actual_spend'].transform(
        lambda x: x.rolling(window=3, min_periods=1, center=True).mean()
    )
    data['seasonal_anomaly'] = np.abs(data['actual_spend'] - data['rolling_mean']) > (0.2 * data['rolling_mean'])

    data['prev_vendor_spend'] = data.groupby(['vendor'])['actual_spend'].shift(1)
    data['vendor_pattern_change'] = (data['prev_vendor_spend'] > 0) & \
        (data['actual_spend'] > 2 * data['prev_vendor_spend'])

    if 'contract_limit' in data.columns:
        data['contract_violation'] = data['actual_spend'] > data['contract_limit']
    else:
        data['contract_violation'] = False

    data['is_duplicate'] = data.duplicated(subset=['vendor', 'actual_spend', 'month', 'department'], keep=False)

    anomaly_flags = (
        (data['anomaly_score'] == -1) |
        data['budget_overrun'] |
        data['budget_underrun'] |
        data['seasonal_anomaly'] |
        data['vendor_pattern_change'] |
        data['contract_violation'] |
        data['is_duplicate']
    )
    anomaly_alerts = data[anomaly_flags].copy()
    budget_impact = anomaly_alerts['variance'].sum()
    recommended_actions = [
        "Review flagged transactions for approval errors or duplicate payments.",
        "Investigate vendors with sudden spend pattern changes.",
        "Check contracts for compliance on flagged items.",
        "Analyze seasonal anomalies for business justification."
    ]

    return anomaly_alerts, budget_impact, recommended_actions