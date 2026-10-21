import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_absolute_error, r2_score
import joblib
import json
import os

# Create directories
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATASETS_DIR = os.path.join(BASE_DIR, 'datasets')
ARTIFACTS_DIR = os.path.join(BASE_DIR, 'artifacts')
os.makedirs(DATASETS_DIR, exist_ok=True)
os.makedirs(ARTIFACTS_DIR, exist_ok=True)

print("Generating synthetic datasets...")

# 1. Synthetic Vehicle Efficiency Dataset
np.random.seed(42)
n_samples = 1000
vehicles_df = pd.DataFrame({
    'engine_size': np.random.uniform(1.0, 5.0, n_samples),
    'weight_kg': np.random.uniform(1000, 3000, n_samples),
    'year': np.random.randint(2000, 2024, n_samples),
    'is_highway': np.random.randint(0, 2, n_samples)
})

base_kml = 20 - (vehicles_df['engine_size'] * 2) - (vehicles_df['weight_kg'] * 0.002) + ((vehicles_df['year'] - 2000) * 0.1)
vehicles_df['target_kml'] = base_kml + (vehicles_df['is_highway'] * 3) + np.random.normal(0, 1, n_samples)
vehicles_df.to_csv(os.path.join(DATASETS_DIR, 'vehicles.csv'), index=False)

# 2. Synthetic Fuel Price Dataset
n_price_samples = 500
days = np.arange(n_price_samples)
base_price = 95.0
price_trend = base_price + np.sin(days / 10) * 2 + days * 0.01 + np.random.normal(0, 0.5, n_price_samples)

prices_df = pd.DataFrame({
    'day': days,
    'price': price_trend
})
# Target is price 7 days from now
prices_df['target_price_7d'] = prices_df['price'].shift(-7)
prices_df.dropna(inplace=True)
prices_df.to_csv(os.path.join(DATASETS_DIR, 'prices.csv'), index=False)

# Train Efficiency Model
print("Training Efficiency Predictor...")
X_eff = vehicles_df[['engine_size', 'weight_kg', 'year', 'is_highway']]
y_eff = vehicles_df['target_kml']

X_train_eff, X_test_eff, y_train_eff, y_test_eff = train_test_split(X_eff, y_eff, test_size=0.2, random_state=42)
eff_model = RandomForestRegressor(n_estimators=100, random_state=42)
eff_model.fit(X_train_eff, y_train_eff)

y_pred_eff = eff_model.predict(X_test_eff)
eff_metrics = {
    "mae": mean_absolute_error(y_test_eff, y_pred_eff),
    "r2": r2_score(y_test_eff, y_pred_eff)
}

joblib.dump(eff_model, os.path.join(ARTIFACTS_DIR, 'efficiency_model.joblib'))

# Train Price Forecaster Model
print("Training Price Forecaster...")
X_price = prices_df[['day', 'price']]
y_price = prices_df['target_price_7d']

X_train_pr, X_test_pr, y_train_pr, y_test_pr = train_test_split(X_price, y_price, test_size=0.2, random_state=42)
price_model = RandomForestRegressor(n_estimators=100, random_state=42)
price_model.fit(X_train_pr, y_train_pr)

y_pred_pr = price_model.predict(X_test_pr)
price_metrics = {
    "mae": mean_absolute_error(y_test_pr, y_pred_pr),
    "r2": r2_score(y_test_pr, y_pred_pr)
}

joblib.dump(price_model, os.path.join(ARTIFACTS_DIR, 'price_model.joblib'))

# Train Recommendation Model (Simple Decision Tree for fuel grade based on engine size/year)
from sklearn.tree import DecisionTreeClassifier
from sklearn.metrics import accuracy_score

print("Training Recommendation Model...")
def get_optimal_grade(row):
    if row['engine_size'] > 3.0 or row['year'] > 2018:
        return 1 # Premium
    return 0 # Regular

vehicles_df['optimal_grade'] = vehicles_df.apply(get_optimal_grade, axis=1)

X_rec = vehicles_df[['engine_size', 'year']]
y_rec = vehicles_df['optimal_grade']

X_train_rec, X_test_rec, y_train_rec, y_test_rec = train_test_split(X_rec, y_rec, test_size=0.2, random_state=42)
rec_model = DecisionTreeClassifier(random_state=42)
rec_model.fit(X_train_rec, y_train_rec)

y_pred_rec = rec_model.predict(X_test_rec)
rec_metrics = {
    "accuracy": accuracy_score(y_test_rec, y_pred_rec)
}

joblib.dump(rec_model, os.path.join(ARTIFACTS_DIR, 'recommendation_model.joblib'))


# Save Metrics
metrics = {
    "efficiency_model": eff_metrics,
    "price_model": price_metrics,
    "recommendation_model": rec_metrics
}

with open(os.path.join(ARTIFACTS_DIR, 'metrics.json'), 'w') as f:
    json.dump(metrics, f, indent=4)

print(f"Metrics: {metrics}")
print("Models trained and saved successfully.")

