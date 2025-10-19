# 1. Import necessary libraries
from flask import Flask, request, jsonify
import joblib
import pandas as pd
import os

# 2. Create a Flask application instance
app = Flask(__name__)

# --- 3. Load All Assets: Model, Scaler, and Training Columns ---
try:
    # Get the directory where the current script is located
    base_dir = os.path.dirname(os.path.abspath(__file__))
    
    # Construct absolute paths to the model assets
    model_path = os.path.join(base_dir, '..', 'models', 'best_model_xgboost_v1.pkl')
    scaler_path = os.path.join(base_dir, '..', 'models', 'scaler_v1.pkl')
    columns_path = os.path.join(base_dir, '..', 'models', 'training_columns.pkl')
    
    model = joblib.load(model_path)
    scaler = joblib.load(scaler_path)
    training_columns = joblib.load(columns_path)
    
    print("Model, Scaler, and Training Columns loaded successfully!")

except Exception as e:
    model, scaler, training_columns = None, None, None
    print(f"Error loading assets: {e}")

# --- 4. Define the Prediction Route ---
@app.route('/predict', methods=['POST'])
def predict():
    if model is None or scaler is None or training_columns is None:
        return jsonify({'error': 'Assets not loaded. Check server logs for errors.'}), 500
    
    try:
        data = request.get_json(force=True)
        print(f"Received data: {data}")

        # --- PREPROCESSING - REPLICATING ASSETS EXACTLY ---
        
        # 1. Convert incoming JSON to a DataFrame
        input_df = pd.DataFrame([data])

        # 2. DO NOT map 'Other' -> 'Male'. (Proven by 'gender_Other' in columns)
        # input_df['gender'] = input_df['gender'].replace({'Other': 'Male'})

        # 3. Perform one-hot encoding in SEPARATE steps to match the assets
        
        # Step 3a: Encode 'gender' with drop_first=True (to match 'gender_Male', 'gender_Other')
        input_df = pd.get_dummies(input_df, columns=['gender'], drop_first=True)
        
        # Step 3b: Encode 'smoking_history' with drop_first=False (to match all 5 smoking columns)
        # This is the line that fixes your bug.
        input_df = pd.get_dummies(input_df, columns=['smoking_history'], drop_first=False)

        # 4. Reindex the DataFrame to match the training columns
        # This will now correctly find 'smoking_history_never' (with value 1)
        # and align it.
        input_df = input_df.reindex(columns=training_columns, fill_value=0)
        
        # 5. Scale the ENTIRE DataFrame
        scaled_features = scaler.transform(input_df)
        
        # 6. Convert the scaled array back to a DataFrame for the model
        final_df = pd.DataFrame(scaled_features, columns=training_columns)

        # --- PREDICTION ---
        prediction = model.predict(final_df)
        prediction_proba = model.predict_proba(final_df)

        # --- FORMAT OUTPUT ---
        output = {
            'prediction': int(prediction[0]),
            'prediction_probability_diabetes': float(prediction_proba[0][1])
        }
        
        print(f"Sending response: {output}")
        return jsonify(output)

    except Exception as e:
        print(f"Error during prediction: {e}")
        return jsonify({'error': str(e)}), 400

# 5. Run the application
if __name__ == '__main__':
    # Use 0.0.0.0 to make the app accessible on your local network
    app.run(host='0.0.0.0', port=5000, debug=True)