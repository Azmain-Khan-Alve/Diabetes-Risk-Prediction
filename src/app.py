
import gradio as gr
import pandas as pd
import joblib
import os

# --- 1. Load All Assets ---
try:
    model = joblib.load("models/best_model_xgboost_v1.pkl")
    scaler = joblib.load("models/scaler_v1.pkl")
    training_columns = joblib.load("models/training_columns.pkl")
    print("Model, Scaler, and Training Columns loaded successfully!")
except Exception as e:
    model, scaler, training_columns = None, None, None
    print(f"Error loading assets: {e}")

# --- 2. Define the Prediction Function ---
# This function now ONLY returns the dictionary for the gr.Label
def predict(gender, age, hypertension, heart_disease, smoking_history, bmi, HbA1c_level, blood_glucose_level):
    if model is None or scaler is None or training_columns is None:
        return {"Error": 1.0, "Message": "Model assets not loaded."} 
        
    try:
        # --- Preprocessing ---
        input_data = {
            'gender': gender, 'age': age, 'hypertension': hypertension, 'heart_disease': heart_disease,
            'smoking_history': smoking_history, 'bmi': bmi, 'HbA1c_level': HbA1c_level,
            'blood_glucose_level': blood_glucose_level
        }
        input_df = pd.DataFrame([input_data])
        input_df['gender'] = input_df['gender'].replace({'Other': 'Male'})
        input_df = pd.get_dummies(input_df, columns=['gender', 'smoking_history'], drop_first=True)
        input_df = input_df.reindex(columns=training_columns, fill_value=0)
        scaled_features = scaler.transform(input_df)
        final_df = pd.DataFrame(scaled_features, columns=training_columns)

        # --- Prediction ---
        prediction_proba = model.predict_proba(final_df)[0] 

        # --- 3. Format Output Dictionary for gr.Label ---
        output_dict = {
            "Prediction: No Diabetes": prediction_proba[0], # Prob class 0
            "Prediction: Diabetes": prediction_proba[1]  # Prob class 1
        }
        return output_dict # Return dictionary

    except Exception as e:
        return {"Error": 1.0, "Message": f"Prediction Error: {str(e)}"} 

# --- 4. Create the Gradio Interface using gr.Blocks ---
with gr.Blocks() as iface:
    # Add Title and Description at the top
    gr.Markdown("# Diabetes Risk Prediction")
    gr.Markdown("Enter the patient's details to predict their risk of diabetes.")
    
    # Define Input components in rows for better layout (optional)
    with gr.Row():
        gender = gr.Radio(['Female', 'Male', 'Other'], label="Gender")
        age = gr.Number(label="Age")
    with gr.Row():
        hypertension = gr.Radio([0, 1], label="Hypertension (0=No, 1=Yes)")
        heart_disease = gr.Radio([0, 1], label="Heart Disease (0=No, 1=Yes)")
    with gr.Row():
        smoking_history = gr.Dropdown(['never', 'No Info', 'current', 'former', 'ever', 'not current'], label="Smoking History")
        bmi = gr.Number(label="BMI")
    with gr.Row():
        HbA1c_level = gr.Number(label="HbA1c Level")
        blood_glucose_level = gr.Number(label="Blood Glucose Level")

    # Define the Submit Button
    submit_button = gr.Button("Submit Prediction")
    
    # Define the Output Label component
    prediction_label = gr.Label(num_top_classes=2, label="Prediction Result")
    
    # Define the Disclaimer Text using Markdown, placed *below* the label
    gr.Markdown(
        "**Disclaimer:** This AI prediction is for informational purposes only and is not a substitute for professional medical advice. Please consult a qualified healthcare provider."
    )

    # Link the button click event to the prediction function
    submit_button.click(
        fn=predict,  # Function to call when button is clicked
        inputs=[gender, age, hypertension, heart_disease, smoking_history, bmi, HbA1c_level, blood_glucose_level], # List of input components
        outputs=[prediction_label] # List of output components to update
    )

# --- 5. Launch the App ---
iface.launch(server_name="0.0.0.0", server_port=7860)








#=========================================================================
#==========The Old One (FLASKAPI)===========
# 
# 
# # import gradio as gr
# import pandas as pd
# import joblib
# import os

# # --- 1. Load All Assets (Model, Scaler, and Columns) ---
# # This section is the same as your Flask app, ensuring we load the correct files.
# # The paths are relative to the root of the project inside the Docker container.
# try:
#     model = joblib.load("models/best_model_xgboost_v1.pkl")
#     scaler = joblib.load("models/scaler_v1.pkl")
#     training_columns = joblib.load("models/training_columns.pkl")
#     print("Model, Scaler, and Training Columns loaded successfully!")
# except Exception as e:
#     model, scaler, training_columns = None, None, None
#     print(f"Error loading assets: {e}")

# # --- 2. Define the Prediction Function (The "Engine") ---
# # This function contains the exact same preprocessing logic as your working Flask API.
# def predict(gender, age, hypertension, heart_disease, smoking_history, bmi, HbA1c_level, blood_glucose_level):
#     try:
#         # 1. Create a dictionary from the inputs provided by the user in the web form
#         input_data = {
#             'gender': gender,
#             'age': age,
#             'hypertension': hypertension,
#             'heart_disease': heart_disease,
#             'smoking_history': smoking_history,
#             'bmi': bmi,
#             'HbA1c_level': HbA1c_level,
#             'blood_glucose_level': blood_glucose_level
#         }

#         # 2. Convert to a DataFrame
#         input_df = pd.DataFrame([input_data])

#         # 3. Replicate the 'Other' -> 'Male' mapping from your notebook
#         input_df['gender'] = input_df['gender'].replace({'Other': 'Male'})

#         # 4. Perform one-hot encoding with drop_first=True, exactly like the notebook
#         input_df = pd.get_dummies(input_df, columns=['gender', 'smoking_history'], drop_first=True)

#         # 5. Reindex the DataFrame to match the training columns perfectly
#         input_df = input_df.reindex(columns=training_columns, fill_value=0)

#         # 6. Scale the entire DataFrame, just like in the notebook
#         scaled_features = scaler.transform(input_df)

#         # 7. Convert the scaled array back to a DataFrame for the model
#         final_df = pd.DataFrame(scaled_features, columns=training_columns)

#         # 8. Make the prediction
#         prediction = model.predict(final_df)[0]
#         prediction_proba = model.predict_proba(final_df)[0]

#         # --- 3. Format the Output for the User ---
#         if prediction == 1:
#             prob = prediction_proba[1] # Probability of being class '1' (Diabetes)
#             return {
#                 "Prediction: Diabetes": prob,
#                 "Prediction: No Diabetes": 1 - prob
#             }
#         else:
#             prob = prediction_proba[0] # Probability of being class '0' (No Diabetes)
#             return {
#                 "Prediction: No Diabetes": prob,
#                 "Prediction: Diabetes": 1 - prob
#             }
#     except Exception as e:
#         return str(e) # Return the error message to the UI for debugging

# # --- 4. Create the Gradio Interface (The "Dashboard") ---
# inputs = [
#     gr.Radio(['Female', 'Male', 'Other'], label="Gender"),
#     gr.Number(label="Age"),
#     gr.Radio([0, 1], label="Hypertension (0 = No, 1 = Yes)"),
#     gr.Radio([0, 1], label="Heart Disease (0 = No, 1 = Yes)"),
#     gr.Dropdown(['never', 'No Info', 'current', 'former', 'ever', 'not current'], label="Smoking History"),
#     gr.Number(label="BMI (Body Mass Index)"),
#     gr.Number(label="HbA1c Level"),
#     gr.Number(label="Blood Glucose Level")
# ]

# # The output is a label component that shows confidence scores for each class
# output = gr.Label(num_top_classes=2, label="Prediction Result")

# # We create the interface with a title and description
# iface = gr.Interface(
#     fn=predict, 
#     inputs=inputs, 
#     outputs=output,
#     title="AI Based Diabetes Risk Prediction",
#     description="Enter the patient's details to predict their risk of diabetes. This tool uses a trained XGBoost model."
# )

# # --- 5. Launch the App ---
# # The 'server_name="0.0.0.0"' makes it accessible inside Docker and on Hugging Face.
# # The port 7860 is the default for Gradio.
# iface.launch(server_name="0.0.0.0", server_port=7860)



#=========================================================================
#==========The Old One (FLASKAPI)===========

# # 1. Import necessary libraries
# from flask import Flask, request, jsonify
# import joblib
# import pandas as pd
# import os

# # 2. Create a Flask application instance
# app = Flask(__name__)

# # --- 3. Load All Assets: Model, Scaler, and Training Columns ---
# try:
#     # Get the directory where the current script is located
#     base_dir = os.path.dirname(os.path.abspath(__file__))
    
#     # Construct absolute paths to the model assets
#     model_path = os.path.join(base_dir, '..', 'models', 'best_model_xgboost_v1.pkl')
#     scaler_path = os.path.join(base_dir, '..', 'models', 'scaler_v1.pkl')
#     columns_path = os.path.join(base_dir, '..', 'models', 'training_columns.pkl')
    
#     model = joblib.load(model_path)
#     scaler = joblib.load(scaler_path)
#     training_columns = joblib.load(columns_path)
    
#     print("Model, Scaler, and Training Columns loaded successfully!")

# except Exception as e:
#     model, scaler, training_columns = None, None, None
#     print(f"Error loading assets: {e}")

# # --- 4. Define the Prediction Route ---
# @app.route('/predict', methods=['POST'])
# def predict():
#     if model is None or scaler is None or training_columns is None:
#         return jsonify({'error': 'Assets not loaded. Check server logs for errors.'}), 500
    
#     try:
#         data = request.get_json(force=True)
#         print(f"Received data: {data}")

#         # --- PREPROCESSING - REPLICATING ASSETS EXACTLY ---
        
#         # 1. Convert incoming JSON to a DataFrame
#         input_df = pd.DataFrame([data])

#         # 2. DO NOT map 'Other' -> 'Male'. (Proven by 'gender_Other' in columns)
#         # input_df['gender'] = input_df['gender'].replace({'Other': 'Male'})

#         # 3. Perform one-hot encoding in SEPARATE steps to match the assets
        
#         # Step 3a: Encode 'gender' with drop_first=True (to match 'gender_Male', 'gender_Other')
#         input_df = pd.get_dummies(input_df, columns=['gender'], drop_first=True)
        
#         # Step 3b: Encode 'smoking_history' with drop_first=False (to match all 5 smoking columns)
#         # This is the line that fixes your bug.
#         input_df = pd.get_dummies(input_df, columns=['smoking_history'], drop_first=False)

#         # 4. Reindex the DataFrame to match the training columns
#         # This will now correctly find 'smoking_history_never' (with value 1)
#         # and align it.
#         input_df = input_df.reindex(columns=training_columns, fill_value=0)
        
#         # 5. Scale the ENTIRE DataFrame
#         scaled_features = scaler.transform(input_df)
        
#         # 6. Convert the scaled array back to a DataFrame for the model
#         final_df = pd.DataFrame(scaled_features, columns=training_columns)

#         # --- PREDICTION ---
#         prediction = model.predict(final_df)
#         prediction_proba = model.predict_proba(final_df)

#         # --- FORMAT OUTPUT ---
#         output = {
#             'prediction': int(prediction[0]),
#             'prediction_probability_diabetes': float(prediction_proba[0][1])
#         }
        
#         print(f"Sending response: {output}")
#         return jsonify(output)

#     except Exception as e:
#         print(f"Error during prediction: {e}")
#         return jsonify({'error': str(e)}), 400

# # 5. Run the application
# if __name__ == '__main__':
#     # Use 0.0.0.0 to make the app accessible on your local network
#     app.run(host='0.0.0.0', port=5000, debug=True)