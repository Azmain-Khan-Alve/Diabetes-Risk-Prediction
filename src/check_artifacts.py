import joblib, os, pandas as pd

base_dir = os.path.dirname(os.path.abspath(__file__))
model_path = os.path.join(base_dir, '..', 'models', 'best_model_xgboost_v1.pkl')
scaler_path = os.path.join(base_dir, '..', 'models', 'scaler_v1.pkl')
columns_path = os.path.join(base_dir, '..', 'models', 'training_columns.pkl')

print("Loading files...")
model = joblib.load(model_path)
scaler = joblib.load(scaler_path)
training_columns = joblib.load(columns_path)

print("Model loaded:", type(model))
print("Scaler mean length:", len(getattr(scaler, 'mean_', [])))
print("Training columns length:", len(training_columns))

if hasattr(model, 'n_features_in_'):
    print("Model expects:", model.n_features_in_)

# Check if numbers match
if hasattr(scaler, 'mean_'):
    if len(scaler.mean_) != len(training_columns):
        print("⚠️ Problem: scaler and training_columns length mismatch!")
    else:
        print("✅ Scaler and training_columns lengths match.")

if hasattr(model, 'n_features_in_'):
    if model.n_features_in_ != len(training_columns):
        print("⚠️ Problem: model expects different number of columns!")
    else:
        print("✅ Model and training_columns lengths match.")

# Show first few columns
print("First 10 training columns:")
print(training_columns[:13])
