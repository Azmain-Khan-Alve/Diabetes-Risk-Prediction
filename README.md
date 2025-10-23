---
title: Diabetes Risk Prediction
sdk: docker
app_port: 7860
---


# **Diabetes Risk Prediction Web Application**

This repository contains the code for an end-to-end machine learning application that predicts the risk of diabetes based on diagnostic measures. The application features a user-friendly web interface built with **Gradio**, is containerized using **Docker**, and automatically deployed via a **CI/CD pipeline** using **GitHub Actions**.

**Live Demo:** [**https://alve69-diabetes-risk-prediction.hf.space**](https://alve69-diabetes-risk-prediction.hf.space)

-----

## **Table of Contents**

  * [Demo Screenshot](#demo-screenshot)
  * [Problem Statement](#problem-statement)
  * [Features](#features)
  * [Tech Stack](#tech-stack)
  * [Model Information](#model-information)
  * [Project Structure](#project-structure)
  * [Getting Started](#getting-started)
      * [Prerequisites](#prerequisites)
      * [Local Installation (Python Environment)](#local-installation-python-environment)
      * [Running with Docker](#running-with-docker)
  * [Usage & API Reference](#usage--api-reference)
      * [Using the Web Interface](#using-the-web-interface)
      * [Using the API Directly](#using-the-api-directly)
  * [Deployment & CI/CD](#deployment--cicd)
  * [Dataset](#dataset)
  * [Contributing](#contributing)
  * [License](#license)
  * [Contact](#contact)

-----

## **Demo Screenshot**
(https://github.com/Azmain-Khan-Alve/Diabetes-Risk-Prediction/blob/main/Gradio_demo.png)
-----

## **Problem Statement**

Diabetes is a prevalent chronic disease affecting millions worldwide. **Early detection** is crucial for effective management and prevention of complications. This project aims to leverage machine learning to predict the likelihood of an individual having diabetes based on key health indicators, providing a tool for preliminary risk assessment.

-----

## **Features**

  * **Interactive Web Interface:** User-friendly UI built with **Gradio** for easy input of patient data.
  * **Real-time Prediction:** Uses a trained **XGBoost** model to provide instant risk predictions and confidence scores.
  * **Built-in API:** Gradio automatically provides an API endpoint for programmatic access.
  * **Containerized:** Packaged with **Docker** for consistent deployment across different environments.
  * **Automated Deployment:** **CI/CD pipeline** ensures the latest code changes are automatically deployed to Hugging Face Spaces.

-----

## **Tech Stack**

| Component | Technology |
| :--- | :--- |
| **Language** | Python 3.11 |
| **ML Libraries** | Scikit-learn, XGBoost, Pandas, NumPy |
| **Web Framework** | Gradio |
| **Containerization** | Docker |
| **Deployment** | Hugging Face Spaces |
| **CI/CD** | GitHub Actions |
| **Version Control** | Git, GitHub |

-----

## **Model Information**

  * **Model:** XGBoost Classifier (`best_model_xgboost_v1.pkl`)
  * **Performance:** Achieved **97.1% accuracy** and **0.964 ROC-AUC** on the test set.
  * **Preprocessing:** Input data is preprocessed using a saved `StandardScaler` (`scaler_v1.pkl`) and one-hot encoding columns (`training_columns.pkl`).
  * **Features Used:** The model predicts based on the following 8 input features:
    1.  Gender (Female, Male, Other)
    2.  Age (years)
    3.  Hypertension (0 = No, 1 = Yes)
    4.  Heart Disease (0 = No, 1 = Yes)
    5.  Smoking History (never, No Info, current, former, ever, not current)
    6.  BMI (Body Mass Index)
    7.  HbA1c Level
    8.  Blood Glucose Level

-----

## **Project Structure**

```bash
diabetes-risk-prediction/
├── .github/
│   └── workflows/
│       └── deploy.yml          # GitHub Actions workflow for CI/CD
├── models/
│   ├── best_model_xgboost_v1.pkl # Trained XGBoost model
│   ├── scaler_v1.pkl           # Fitted StandardScaler
│   └── training_columns.pkl    # List of required feature columns
├── notebooks/
│   └── diabetic.ipynb          # Jupyter Notebook for EDA and model training
├── src/
│   └── app.py                  # Gradio application code
├── .dockerignore                 # Specifies files to ignore in Docker build
├── .gitignore                    # Specifies files Git should ignore
├── Dockerfile                    # Instructions to build the Docker image
├── README.md                     # This file
└── requirements.txt              # Python dependencies
```

-----

## **Getting Started**

### **Prerequisites**

  * **Python 3.11** or later
  * **Git**
  * **Docker Desktop** (if running with Docker)

### **Local Installation (Python Environment)**

1.  **Clone the repository:**

    ```bash
    git clone https://github.com/Azmain-Khan-Alve/diabetes-risk-prediction.git
    cd diabetes-risk-prediction
    ```

2.  **Create and activate a virtual environment:**

    ```bash
    python -m venv .venv

    # On Windows
    .\.venv\Scripts\Activate.ps1

    # On macOS/Linux
    source .venv/bin/activate
    ```

3.  **Install the required dependencies:**

    ```bash
    pip install -r requirements.txt
    ```

4.  **Run the Gradio application:**

    ```bash
    python src/app.py
    ```

    The application will be available locally at `http://127.0.0.1:7860`.

### **Running with Docker**

Ensure **Docker Desktop** is running.

1.  **Build the Docker image:**

    ```bash
    docker build -t diabetes-risk-prediction .
    ```

2.  **Run the Docker container:**

    ```bash
    docker run -d -p 7860:7860 --name diabetes-app diabetes-risk-prediction
    ```

    The application will be available locally at `http://localhost:7860`.

-----

## **Usage & API Reference**

### **Using the Web Interface**

Once the application is running, navigate to the provided URL ([Live Demo](https://alve69-diabetes-risk-prediction.hf.space) or your local URL) in your web browser. **Enter the patient's diagnostic information** into the form and **click "Submit"** to see the diabetes risk prediction and associated confidence score.

### **Using the API Directly**

Gradio automatically creates an API endpoint. You can send a `POST` request to the `/api/predict` endpoint of your running application.

**Example using `curl`:**

```bash
curl -X POST \
  -H "Content-Type: application/json" \
  -d '{
    "data": [
      "Female",
      80.0,
      1,
      1,
      "never",
      27.32,
      6.6,
      140
    ]
  }' \
  https://alve69-diabetes-risk-prediction.hf.space/api/predict
```

**Expected Response:**

```json
{
  "data": [
    {
      "label": "Prediction: Diabetes",
      "confidences": [
        {
          "label": "Prediction: Diabetes",
          "confidence": 0.9932
        },
        {
          "label": "Prediction: No Diabetes",
          "confidence": 0.0067
        }
      ]
    }
  ],
  "is_generating": false,
  "duration": 0.123,
  "average_duration": 0.123
}
```

*(Note: You can find detailed API documentation by scrolling to the bottom of the live demo page and clicking the "Use via API" link.)*

-----

## **Deployment & CI/CD**

This application is automatically deployed to **Hugging Face Spaces** via a GitHub Actions workflow defined in `.github/workflows/deploy.yml`. Any push to the `main` branch on GitHub triggers the workflow, which pushes the code to the Hugging Face Space repository, initiating a new build and deployment of the Gradio application.

-----

## **Dataset**

The model was trained on the "Diabetes prediction dataset" from Kaggle.

  * **Dataset Link:** `[https://www.kaggle.com/datasets/LINK]`

-----

## **Contributing**

Contributions are welcome\! Please feel free to submit a Pull Request.

1.  **Fork** the repository.
2.  **Create your feature branch:**
    ```bash
    git checkout -b feature/AmazingFeature
    ```
3.  **Commit your changes:**
    ```bash
    git commit -m 'Add some AmazingFeature'
    ```
4.  **Push to the branch:**
    ```bash
    git push origin feature/AmazingFeature
    ```
5.  **Open a Pull Request.**

-----

## **License**

This project is licensed under the **MIT License**.

-----

## **Contact**

For questions or feedback, please **open an issue** in the repository.