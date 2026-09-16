# 🌧️ ClimateForecast AI: Monsoon Prediction Model
### A neural network-based approach to forecasting Total Monsoon Rainfall (TMRF)

## 📖 Overview
ClimateForecast AI is a robust machine learning project designed to predict Total Monsoon Rainfall (TMRF) using 12 distinct climatic parameters. By applying data normalization techniques and a custom-built feedforward neural network, it processes historical climate datasets to generate highly accurate predictions, helping meteorologists and researchers analyze weather patterns more effectively.

## ✨ Features
* **Data Normalization & Denormalization:** Scales climatic parameters into optimal ranges for machine learning, and reverses them back to real-world values.
* **TMRF Calculation:** Automatically aggregates monthly data (June to September) to calculate Total Monsoon Rainfall.
* **Long Period Average (LPA) Processing:** Converts and compares TMRF against historical LPA values in percentage terms.
* **Custom Neural Network:** Features a backpropagation algorithm with momentum for training, utilizing TensorFlow and NumPy.
* **Comprehensive Metrics Evaluation:** Evaluates model performance using Mean Absolute Deviation (MAD), Standard Deviation (SD), Correlation Coefficient (CC), and Mean Squared Error (MSE).

## 🛠 Tech Stack
* **Python:** The core programming language powering the logic.
* **Pandas:** Used for robust data manipulation, filtering, and Excel file handling.
* **NumPy:** Handles complex mathematical operations, arrays, and matrix multiplication.
* **TensorFlow:** Utilized for building and optimizing the neural network's forward and backward passes.
* **Scikit-learn:** Provides utilities for efficiently splitting data into training and testing sets.

## 📋 Prerequisites
Before you start, make sure you have the following installed:
* **Python v3.8+**: Essential for running the scripts and ensuring library compatibility.
* **Git**: To clone the repository.
* **pip**: Python's package installer, typically included with Python.

## 🚀 Local Development (Step-by-Step)

### 1. Clone the repository
Open your terminal and clone the project to your local machine:
```bash
git clone <your-repo-url>
cd <your-repo-directory>
```

### 2. Set up a Virtual Environment (Optional but recommended)
Keep your project dependencies isolated by creating a virtual environment:
```bash
python -m venv venv
```
Activate it:
* On Windows: `venv\Scripts\activate`
* On macOS/Linux: `source venv/bin/activate`

### 3. Install Dependencies
Install the required Python packages:
```bash
pip install pandas numpy tensorflow scikit-learn openpyxl
```
*(Note: `openpyxl` is required by Pandas to read/write Excel files).*

### 4. Prepare the Dataset
Ensure your dataset files (e.g., `dataset.xlsx`, `normalized_data.xlsx`, `TMRF_input.xlsx`) are placed in the root directory or the respective folders as expected by the scripts.

### 5. Run the Data Preprocessing
Generate normalized and denormalized data, or calculate TMRF:
```bash
# To denormalize data
python denormalized_data_code.py

# To calculate TMRF
python CODES/TMRF_program.py

# To process LPA percentages
python CODES/LPA.py
```

### 6. Run the Main Prediction Model
Train the neural network and output the predictions and metrics (which will be saved to `predictions.xlsx` and `metrics.xlsx`):
```bash
python "CODES/main program accurate.py"
```

## 🧠 How It Works (Architecture)
1. **Data Ingestion:** The application reads historical climate data from Excel sheets.
2. **Preprocessing:** Raw parameters are scaled (normalized) between 0 and 1. Monthly data (June-September) is aggregated to form the target variable, TMRF.
3. **Model Training:** The preprocessed 12-factor dataset is fed into a neural network. The model uses a forward pass to guess the rainfall and a backward pass (Delta rule) combined with momentum to adjust its weights, learning from its mistakes.
4. **Evaluation & Output:** The model predicts the TMRF for unseen data, calculates accuracy metrics (like MSE and MAD), and exports the final predictions and metrics back into Excel files for easy review.

## 📁 Folder Structure
```text
.
├── CODES/
│   ├── Data Preprocessing/     # Scripts for cleaning and structuring raw data
│   ├── Graph generating codes/ # Scripts for visual analysis
│   ├── WEIGHTS/                # Stored weights for the neural network
│   ├── LPA.py                  # Calculates Long Period Average percentages
│   ├── TMRF_program.py         # Computes Total Monsoon Rainfall
│   └── main program accurate.py # Core neural network model for forecasting
├── DATASETS/
│   ├── Climatalogy with most parameters/ # Raw climatology data
│   ├── Daily dataset for mainpat/        # Daily granular datasets
│   └── Monthly or Yearly dataset/        # Aggregated datasets
├── denormalized_data_code.py   # Reverses normalized data to actual values
├── dataset.xlsx                # Primary raw input data
└── README.md                   # This documentation file
```