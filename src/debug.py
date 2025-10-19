# debug_inference_check.py
import joblib, numpy as np, pandas as pd, os

base_dir = os.path.dirname(os.path.abspath(__file__))
model_path = os.path.join(base_dir, '..', 'models', 'best_model_xgboost_v1.pkl')   # change to the path you actually load
scaler_path = os.path.join(base_dir, '..', 'models', 'scaler_v1.pkl')
columns_path = os.path.join(base_dir, '..', 'models', 'training_columns.pkl')

print("Files (expected):")
print(" model:", os.path.exists(model_path), model_path)
print(" scaler:", os.path.exists(scaler_path), scaler_path)
print(" columns:", os.path.exists(columns_path), columns_path)
print()

# Load (wrap in try to show error more clearly)
model = joblib.load(model_path)
scaler = joblib.load(scaler_path)
training_columns = joblib.load(columns_path)

print("Model type:", type(model))
# If sklearn-wrapper XGBoost has attribute n_features_in_, show it:
print("Model n_features_in_ (if available):", getattr(model, 'n_features_in_', 'N/A'))
print("Scaler means shape:", getattr(scaler, 'mean_', None).shape if hasattr(scaler, 'mean_') else 'no mean_')
print("Scaler var shape:", getattr(scaler, 'var_', None).shape if hasattr(scaler, 'var_') else 'no var_')
print("Len training_columns:", len(training_columns))
print("First 20 training_columns:", training_columns[:20])
print()

# Now show what your app builds for the given test JSON
test = {
 "gender": "Female", "age": 80.0,
 "hypertension": 1, "heart_disease": 1,
 "smoking_history": "never", "bmi": 27.32,
 "HbA1c_level": 6.6, "blood_glucose_level": 140
}

df = pd.DataFrame([test])
print("Original input dtypes:\n", df.dtypes)

# Map Other->Male if you do that in app:
df['gender'] = df['gender'].replace({'Other': 'Male'})

df_processed = pd.get_dummies(df, columns=['gender', 'smoking_history'], drop_first=True)
print("\nAfter get_dummies (drop_first=True):")
print(df_processed.columns.tolist())

# Reindex to training_columns:
aligned = df_processed.reindex(columns=training_columns, fill_value=0)
print("\nAfter reindex -> columns count:", aligned.shape[1])
print("Aligned columns (first 20):", aligned.columns.tolist()[:20])

# Quick shape checks:
if hasattr(scaler, 'mean_'):
    print("scaler.mean_.shape:", scaler.mean_.shape)
    assert scaler.mean_.shape[0] == aligned.shape[1], "Scaler expects different number of features than aligned input!"

# Run transform (wrapped to show error)
try:
    scaled = scaler.transform(aligned)
    print("Scaled shape:", scaled.shape)
except Exception as e:
    print("Error transforming with scaler:", e)

# Try model predict_proba:
try:
    proba = model.predict_proba(scaled)
    pred = model.predict(scaled)
    print("predict_proba:", proba, " predict:", pred)
except Exception as e:
    print("Error predicting with model:", e)
