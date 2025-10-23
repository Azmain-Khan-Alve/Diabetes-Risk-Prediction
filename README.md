---
title: Diabetes Risk Prediction
sdk: docker
app_port: 7860
---

# Diabetes Risk Prediction Web Application

[![Hugging Face Spaces](https://img.shields.io/badge/%F0%9F%A4%97%20Hugging%20Face-Spaces-blue)](https://alve69-diabetes-risk-prediction.hf.space) [![Python Version](https://www.google.com/search?q=https://img.shields.io/badge/Python-3.11-blue)](https://www.python.org/downloads/release/python-3110/)

This repository contains the code for an end-to-end machine learning application that predicts the risk of diabetes based on diagnostic measures. The application features a user-friendly web interface built with Gradio, is containerized using Docker, and automatically deployed via a CI/CD pipeline using GitHub Actions.

**Live Demo:** [**https://alve69-diabetes-risk-prediction.hf.space**](https://alve69-diabetes-risk-prediction.hf.space)

## Table of Contents

[Demo Screenshot](#demo-screenshot)

[Problem Statement](#problem-statement)

[Features](#features)

[Tech Stack](#tech-stack)

[Model Information](#model-information)

[Project Structure](#project-structure)

[Getting Started](#getting-started)

[Prerequisites](#prerequisites)

[Local Installation (Python Environment)](#local-installation-python-environment)

[Running with Docker](#running-with-docker)

[Usage](#usage)

[Using the Web Interface](#using-the-web-interface)

[Using the API Directly](#using-the-api-directly)

[Deployment & CI/CD](#deployment--cicd)

[Dataset](#dataset)

[Contributing](#contributing)

[License](#license)

[Contact](#contact)

## Demo Screenshot

![Gradio App Screenshot](https://www.google.com/search?q=https://raw.githubusercontent.com/Azmain-Khan-Alve/Diabetes-Risk-Prediction/main/gradio_demo.png)

## Problem Statement

Diabetes is a prevalent chronic disease affecting millions worldwide. Early detection is crucial for effective management and prevention of complications. This project aims to leverage machine learning to predict the likelihood of an individual having diabetes based on key health indicators, providing a tool for preliminary risk assessment.

## Features

**Interactive Web Interface:** User-friendly UI built with Gradio for easy input of patient data.

**Real-time Prediction:** Uses a trained XGBoost model to provide instant risk predictions and confidence scores.

**Built-in API:** Gradio automatically provides an API endpoint for programmatic access.

**Containerized:** Packaged with Docker for consistent deployment across different environments.

**Automated Deployment:** CI/CD pipeline ensures the latest code changes are automatically deployed to Hugging Face Spaces.

## Tech Stack

**Language:** Python 3.11

**ML Libraries:** Scikit-learn, XGBoost, Pandas, NumPy

**Web Framework:** Gradio

**Containerization:** Docker

**Deployment:** Hugging Face Spaces

**CI/CD:** GitHub Actions

**Version Control:** Git, GitHub

## Model Information

**Model:** XGBoost Classifier (models/best_model_xgboost_v1.pkl)

**Performance:** Achieved 97.1% accuracy and 0.964 ROC-AUC on the test set during development.

**Preprocessing:** Input data is preprocessed using a saved StandardScaler (models/scaler_v1.pkl) and one-hot encoding consistent with the training pipeline (models/training_columns.pkl).

**Features Used:** The model predicts based on the following 8 input features:

Gender (Female, Male, Other - mapped internally)

Age (years)

Hypertension (0 = No, 1 = Yes)

Heart Disease (0 = No, 1 = Yes)

Smoking History (never, No Info, current, former, ever, not current)

BMI (Body Mass Index)

HbA1c Level

Blood Glucose Level

## Project Structure

diabetes-risk-prediction/
├── .github/
│   └── workflows/
│       └── deploy.yml        # GitHub Actions workflow for CI/CD
├── models/
│   ├── best_model_xgboost_v1.pkl # Trained XGBoost model
│   ├── scaler_v1.pkl           # Fitted StandardScaler
│   └── training_columns.pkl    # List of required feature columns
├── notebooks/
│   └── diabetic.ipynb        # Jupyter Notebook for EDA and model training
├── src/
│   └── app.py                # Gradio application code
├── .dockerignore             # Specifies files to ignore in Docker build
├── .gitignore                # Specifies files Git should ignore
├── Dockerfile                # Instructions to build the Docker image
├── README.md                 # This file
├── requirements.txt          # Python dependencies
└── gradio_demo.png           # Screenshot file

## Getting Started

### Prerequisites

Python 3.11 or later

Git

Docker Desktop (if running with Docker)

### Local Installation (Python Environment)

**Clone the repository:**

git clone https://github.com/Azmain-Khan-Alve/Diabetes-Risk-Prediction.git
cd Diabetes-Risk-Prediction

**Create and activate a virtual environment:**

python -m venv .venv
# On Windows
.\.venv\Scripts\Activate.ps1
# On macOS/Linux
# source .venv/bin/activate

**Install the required dependencies:**

pip install -r requirements.txt

**Run the Gradio application:**

python src/app.py

The application will be available locally at http://127.0.0.1:7860.

### Running with Docker

Ensure Docker Desktop is running.

**Build the Docker image:**

docker build -t diabetes-risk-prediction .

**Run the Docker container:**

docker run -d -p 7860:7860 --name diabetes-app diabetes-risk-prediction

The application will be available locally at http://localhost:7860.

## Usage

### Using the Web Interface

Once the application is running, navigate to the provided URL ([Live Demo](https://alve69-diabetes-risk-prediction.hf.space) or your local URL) in your web browser. Enter the patient's diagnostic information into the form and click "Submit" to see the diabetes risk prediction and associated confidence score.

### Using the API Directly

Gradio automatically creates an API endpoint. You can send a POST request to the /api/predict endpoint of your running application (either locally or the live demo URL).

**Example using curl:**

curl -X POST \
  -H "Content-Type: application/json" \
  -d '{
    "data": [
      "Female",  # Gender
      80.0,      # Age
      1,         # Hypertension
      1,         # Heart Disease
      "never",   # Smoking History
      27.32,     # BMI
      6.6,       # HbA1c Level
      140        # Blood Glucose Level
    ]
  }' \
  https://alve69-diabetes-risk-prediction.hf.space/api/predict

**Expected Response:**

{
  "data": [
    {
      "label": "Prediction: Diabetes",
      "confidences": [
        { "label": "Prediction: Diabetes", "confidence": 0.9932... },
        { "label": "Prediction: No Diabetes", "confidence": 0.0067... }
      ]
    }
  ],
  "is_generating": false,
  "duration": 0.123...,
  "average_duration": 0.123...
}

*(Note: You can find detailed API documentation by scrolling to the bottom of the live demo page and clicking the "Use via API" link.)*

## Deployment & CI/CD

This application is automatically deployed to Hugging Face Spaces via a GitHub Actions workflow defined in .github/workflows/deploy.yml. Any push to the main branch on GitHub triggers the workflow, which pushes the code to the Hugging Face Space repository, initiating a new build and deployment of the Gradio application.

## Dataset

The model was trained on the "Diabetes prediction dataset" containing diagnostic measurements. *(Dataset source not specified)*

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

Fork the repository.

Create your feature branch (git checkout -b feature/AmazingFeature).

Commit your changes (git commit -m 'Add some AmazingFeature').

Push to the branch (git push origin feature/AmazingFeature).

Open a Pull Request.

## License

*(License file not added yet. Consider adding an MIT License.)*

## Contact

For questions or feedback, please open an issue in the repository.




# **Diabetes Risk Prediction Web Application**

This repository contains the code for an end-to-end machine learning application that predicts the risk of diabetes based on diagnostic measures. The application features a user-friendly web interface built with Gradio, is containerized using Docker, and automatically deployed via a CI/CD pipeline using GitHub Actions.

**Live Demo:** [**https://alve69-diabetes-risk-prediction.hf.space**](https://alve69-diabetes-risk-prediction.hf.space)

## **Table of Contents**

* [Demo Screenshot](#bookmark=id.1pw5o7iggelt)  
* [Problem Statement](#bookmark=id.5bjwtxrl5khl)  
* [Features](#bookmark=id.2lovgq7j31dj)  
* [Tech Stack](#bookmark=id.ikbsiykht94k)  
* [Model Information](#bookmark=id.u2s2rfmqlcx)  
* [Project Structure](#bookmark=id.s33wdg3w65xf)  
* [Getting Started](#bookmark=id.l2u4i2hnvvy8)  
  * [Prerequisites](#bookmark=id.i9oaudf1mb6x)  
  * [Local Installation (Python Environment)](#bookmark=id.58h3096h7jzw)  
  * [Running with Docker](#bookmark=id.ux8yo9b06zyl)  
* [Usage](#bookmark=id.8ovid4njda4i)  
  * [Using the Web Interface](#bookmark=id.lys9p9eru8gs)  
  * [Using the API Directly](#bookmark=id.oqq08zs8v8cr)  
* [Deployment & CI/CD](#bookmark=id.36kp2xxtcql5)  
* [Dataset](#bookmark=id.wd1wrypq5ow0)  
* [Contributing](#bookmark=id.wpl9f7prctyo)  
* [License](#bookmark=id.uie8mwxqexs5)  
* [Contact](#bookmark=id.ram70j9ns4cy)

## **Demo Screenshot**

*(Optional: Add a screenshot of your Gradio application here)*

\<\!-- Example: \--\>

## **Problem Statement**

Diabetes is a prevalent chronic disease affecting millions worldwide. Early detection is crucial for effective management and prevention of complications. This project aims to leverage machine learning to predict the likelihood of an individual having diabetes based on key health indicators, providing a tool for preliminary risk assessment.

## **Features**

* **Interactive Web Interface:** User-friendly UI built with Gradio for easy input of patient data.  
* **Real-time Prediction:** Uses a trained XGBoost model to provide instant risk predictions and confidence scores.  
* **Built-in API:** Gradio automatically provides an API endpoint for programmatic access.  
* **Containerized:** Packaged with Docker for consistent deployment across different environments.  
* **Automated Deployment:** CI/CD pipeline ensures the latest code changes are automatically deployed to Hugging Face Spaces.

## **Tech Stack**

* **Language:** Python 3.11  
* **ML Libraries:** Scikit-learn, XGBoost, Pandas, NumPy  
* **Web Framework:** Gradio  
* **Containerization:** Docker  
* **Deployment:** Hugging Face Spaces  
* **CI/CD:** GitHub Actions  
* **Version Control:** Git, GitHub

## **Model Information**

* **Model:** XGBoost Classifier (xgboost\_diabetes\_v1.pkl)  
* **Performance:** Achieved 97.1% accuracy and 0.964 ROC-AUC on the test set during development.  
* **Preprocessing:** Input data is preprocessed using a saved StandardScaler (scaler\_v1.pkl) and one-hot encoding consistent with the training pipeline (training\_columns.pkl).  
* **Features Used:** The model predicts based on the following 8 input features:  
  1. Gender (Female, Male, Other \- mapped internally)  
  2. Age (years)  
  3. Hypertension (0 \= No, 1 \= Yes)  
  4. Heart Disease (0 \= No, 1 \= Yes)  
  5. Smoking History (never, No Info, current, former, ever, not current)  
  6. BMI (Body Mass Index)  
  7. HbA1c Level  
  8. Blood Glucose Level

## **Project Structure**

diabetes-risk-prediction/  
├── .github/  
│   └── workflows/  
│       └── deploy.yml        \# GitHub Actions workflow for CI/CD  
├── models/  
│   ├── best\_model\_xgboost\_v1.pkl \# Trained XGBoost model  
│   ├── scaler\_v1.pkl           \# Fitted StandardScaler  
│   └── training\_columns.pkl    \# List of required feature columns  
├── notebooks/  
│   └── diabetic.ipynb        \# Jupyter Notebook for EDA and model training  
├── src/  
│   └── app.py                \# Gradio application code  
├── .dockerignore             \# Specifies files to ignore in Docker build  
├── .gitignore                \# Specifies files Git should ignore  
├── Dockerfile                \# Instructions to build the Docker image  
├── README.md                 \# This file  
└── requirements.txt          \# Python dependencies

## **Getting Started**

### **Prerequisites**

* Python 3.11 or later  
* Git  
* Docker Desktop (if running with Docker)

### **Local Installation (Python Environment)**

1. **Clone the repository:**  
   git clone \[https://github.com/Azmain-Khan-Alve/diabetes-risk-prediction.git\](https://github.com/Azmain-Khan-Alve/diabetes-risk-prediction.git)  
   cd diabetes-risk-prediction

2. **Create and activate a virtual environment:**  
   python \-m venv .venv  
   \# On Windows  
   .\\.venv\\Scripts\\Activate.ps1  
   \# On macOS/Linux  
   \# source .venv/bin/activate

3. **Install the required dependencies:**  
   pip install \-r requirements.txt

4. **Run the Gradio application:**  
   python src/app.py

   The application will be available locally at http://127.0.0.1:7860.

### **Running with Docker**

Ensure Docker Desktop is running.

1. **Build the Docker image:**  
   docker build \-t diabetes-risk-prediction .

2. **Run the Docker container:**  
   docker run \-d \-p 7860:7860 \--name diabetes-app diabetes-risk-prediction

   The application will be available locally at http://localhost:7860.

## **Usage**

### **Using the Web Interface**

Once the application is running, navigate to the provided URL ([Live Demo](https://alve69-diabetes-risk-prediction.hf.space) or your local URL) in your web browser. Enter the patient's diagnostic information into the form and click "Submit" to see the diabetes risk prediction and associated confidence score.

### **Using the API Directly**

Gradio automatically creates an API endpoint. You can send a POST request to the /api/predict endpoint of your running application (either locally or the live demo URL).

**Example using curl:**

curl \-X POST \\  
  \-H "Content-Type: application/json" \\  
  \-d '{  
    "data": \[  
      "Female",  \# Gender  
      80.0,      \# Age  
      1,         \# Hypertension  
      1,         \# Heart Disease  
      "never",   \# Smoking History  
      27.32,     \# BMI  
      6.6,       \# HbA1c Level  
      140        \# Blood Glucose Level  
    \]  
  }' \\  
  \[https://alve69-diabetes-risk-prediction.hf.space/api/predict\](https://alve69-diabetes-risk-prediction.hf.space/api/predict)

**Expected Response:**

{  
  "data": \[  
    {  
      "label": "Prediction: Diabetes",  
      "confidences": \[  
        { "label": "Prediction: Diabetes", "confidence": 0.9932... },  
        { "label": "Prediction: No Diabetes", "confidence": 0.0067... }  
      \]  
    }  
  \],  
  "is\_generating": false,  
  "duration": 0.123...,  
  "average\_duration": 0.123...  
}

*(Note: You can find detailed API documentation by scrolling to the bottom of the live demo page and clicking the "Use via API" link.)*

## **Deployment & CI/CD**

This application is automatically deployed to Hugging Face Spaces via a GitHub Actions workflow defined in .github/workflows/deploy.yml. Any push to the main branch on GitHub triggers the workflow, which pushes the code to the Hugging Face Space repository, initiating a new build and deployment of the Gradio application.

## **Dataset**

The model was trained on the "Diabetes prediction dataset" containing diagnostic measurements from Kaggle: [Link to Dataset (if available)](http://docs.google.com/Replace%20with%20actual%20link%20if%20you%20have%20one)

## **Contributing**

Contributions are welcome\! Please feel free to submit a Pull Request.

1. Fork the repository.  
2. Create your feature branch (git checkout \-b feature/AmazingFeature).  
3. Commit your changes (git commit \-m 'Add some AmazingFeature').  
4. Push to the branch (git push origin feature/AmazingFeature).  
5. Open a Pull Request.

## **License**

This project is licensed under the MIT License \- see the LICENSE file for details (if you add one).

## **Contact**

For questions or feedback, please open an issue in the repository.

\#\#\# Next Steps:

1\.  \*\*Add Screenshot (Optional but Recommended):\*\* As mentioned before.  
2\.  \*\*Add Dataset Link:\*\* Find the link to the dataset you used (e.g., on Kaggle) and add it to the "Dataset" section.  
3\.  \*\*Add License File (Optional):\*\* If you want to formally license your code, create a file named \`LICENSE\` in your project root and paste the standard MIT License text into it.  
4\.  \*\*Push the Updated README to GitHub:\*\*  
    \* Save the changes to your local \`README.md\` file.  
    \* Run the usual Git commands:  
        \`\`\`bash  
        git add README.md  
        git commit \-m "Add detailed usage, model info, and standard sections to README"  
        git push origin main  
