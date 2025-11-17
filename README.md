# Anomaly Detection System

## Overview

This project addresses the challenge of identifying anomalies in sales data, aiming to optimize sales strategies by uncovering deviations from expected profit patterns. The system utilizes a Flask backend for processing CSV data and detecting anomalies using several machine learning algorithms. The frontend is built with React for interactive data handling and visualization.

## Problem Statement

The existing sales plan during a fiscal year may not align with the predicted profit due to various factors. Understanding which aspects contribute to or detract from profit allows sellers to adjust their strategy and maximize earnings. This project focuses on analyzing sales data to improve sales strategies based on anomaly detection.

## Scope of Proof of Concept (POC)

- **Data Collection**: Gather the dataset reflecting the sales strategy for a financial year.
- **Current Analysis**: Examine the existing sales plan.
- **Dependency Identification**: Determine how each element of the sales plan impacts the expected outcome.
- **Improvement Areas**: Identify areas for potential improvement and gather relevant information.
- **Application**: Apply gathered information to the dataset and revise the strategy.
- **Implementation**: Develop and implement the refined strategy based on the model's findings.

## Solution Approach

The solution involves:

1. **Research**: Analyze sales data, offers, and customer responses to understand the impact of each offer on profit.
2. **Impact Assessment**: Evaluate the influence of offers and discounts on profit generation.
3. **Strategy Enhancement**: Use insights gained to create an improved and more accurate sales strategy.

## Algorithms for Anomaly Detection

The project compares several anomaly detection algorithms to identify the most effective approach for the given sales dataset:

- **Isolation Forest**: A tree-based method effective for high-dimensional data, detecting anomalies by isolating observations.
- **K-Nearest Neighbors (KNN)**: Measures anomaly based on the distance from nearest neighbors.
- **Cluster-Based Local Outlier Factor (CBLOF)**: Combines clustering with local outlier detection.
- **Local Outlier Factor (LOF)**: Identifies anomalies by comparing the local density of points.
- **LSTM Autoencoder**: Utilizes Long Short-Term Memory networks for sequential anomaly detection.
- **Gaussian Mixture Model (GMM)**: Assumes data is generated from a mixture of several Gaussian distributions.


## Features

- **Upload and Process CSV Files:** Upload CSV files via a Flask API.
- **Anomaly Detection:** Detect anomalies using the Isolation Forest algorithm.
- **Data Visualization:** Visualize anomalies with decision boundary plots.
- **Summary and Insights:** Generate summaries and insights based on detected anomalies.

## Frontend

The frontend is implemented using React. It allows users to upload CSV files and view the results returned by the Flask API.

## Backend

The backend is implemented using Flask and includes the following features:

- **CSV Upload Endpoint:** `/api/uploadfile` - Accepts a POST request with a CSV file for anomaly detection.
- **Anomaly Detection:** Utilizes the Isolation Forest algorithm to identify anomalies.
- **Plotting:** Generates and returns base64-encoded plots of detected anomalies.
- **Summary and Insights:** Provides textual summaries and insights based on the anomaly detection results.

## Backend Function: `detect_anomalies`

The `detect_anomalies` function processes a CSV or Excel file to detect anomalies using various algorithms. Here’s how it works:

1. **File Reading**: Reads the data from CSV or Excel files into a Pandas DataFrame.
2. **Data Preparation**: Normalizes 'Sales' and 'Profit' columns using MinMaxScaler.
3. **Algorithm Selection**: Applies selected anomaly detection algorithms from a predefined list.
4. **Anomaly Detection**: Uses each algorithm to detect anomalies in the data.
5. **Plot Generation**: Creates visual plots of detected anomalies.
6. **Results Compilation**: Compiles anomaly data, summaries, and insights into a JSON format for easy consumption.

### Function Details

- **Parameters**:
  - `file_path`: Path to the CSV or Excel file.
  - `algos`: List of algorithms to use for anomaly detection (e.g., `['isolation_forest']`).
  - `outliers_fraction`: Fraction of outliers expected in the data.

- **Process**:
  1. Load the dataset.
  2. Check for required columns: 'Sales' and 'Profit'.
  3. Normalize the data.
  4. Apply selected algorithms to detect anomalies.
  5. Generate plots and summaries.
  6. Return anomalies, summaries, insights, and plots in JSON format.


## Installation

### Backend

1. **Clone the repository:**

    ```bash
    git clone <repository-url>
    cd <repository-directory>
    ```

2. **Create a virtual environment and install dependencies:**

    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows use `venv\Scripts\activate`
    pip install -r requirements.txt
    ```

3. **Run the Flask app:**

    ```bash
    python app.py
    ```

### Frontend

1. **Navigate to the frontend directory:**

    ```bash
    cd <frontend-directory>
    ```

2. **Install dependencies:**

    ```bash
    npm install
    ```

3. **Run the React app:**

    ```bash
    npm start
    ```

## How to Use

1. **Frontend:**

   - Place your CSV files in the designated upload area on the React app.
   - Submit the files to the Flask backend using the provided upload functionality.
   - View the results, including summaries, insights, and visualizations.

2. **Backend:**

   - **Upload your CSV file** through the API endpoint `/api/uploadfile`.
   - The backend will process the file, detect anomalies, and return results including:
     - Anomalies in JSON format.
     - A summary of the dataset and detected anomalies.
     - Insights based on the detected anomalies.
     - Base64-encoded plots for visualization.

## Libraries and APIs Used

- **Flask**: For building the backend API.
- **Pandas**: For data manipulation and analysis.
- **Matplotlib**: For generating plots.
- **Scikit-Learn**: For implementing the Isolation Forest algorithm.
- **Flask-CORS**: For handling Cross-Origin Resource Sharing.
- **React**: For building the frontend application.


## License

This project is licensed under the MIT License

