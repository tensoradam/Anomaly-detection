from flask import Flask,request,jsonify
import pandas as pd
import matplotlib.pyplot as plt
import base64
import numpy as np
from numpy import percentile
from io import StringIO
import json
import csv
import io

from sklearn.preprocessing import MinMaxScaler
from sklearn.ensemble import IsolationForest
from sklearn.metrics import confusion_matrix
from flask_cors import CORS,cross_origin


app=Flask(__name__)
CORS(app)
@app.route('/api/uploadfile',methods=['POST'])
def process_csv():
    
    file=request.files['myFile']
    file_stream=StringIO(file.stream.read().decode('utf-8'))
    reader=csv.reader(file_stream)
    with open("input_sales_data.csv", "w",newline="") as csvfile:
        writer=csv.writer(csvfile)
        for row in reader:
            writer.writerow(row)
    csv_file = "input_sales_data.csv"
    algos = ['isolation_forest']
    result = detect_anomalies(csv_file, algos)
    print(result)
    return jsonify(result)

def convert_and_save(b64_string):
    fileName = "input_sales_data.csv"
    bytes_io=io.BytesIO()
    with open(fileName, "wb") as fh:
        fh.write(bytes_io.getvalue())
def convert_csv(csv_file):
    df=pd.read_csv(csv_file)
    smaller_df=df.describe()
    print(smaller_df)
    smaller_df.to_csv('smaller_csv.csv',index=False)
    return'smaller_csv.csv'

# Function to generate summary text
def generate_summary(df, anomalies):
    num_anomalies = anomalies.shape[0]
    total_records = df.shape[0]
    normal_records = total_records - num_anomalies
    anomaly_percentage = (num_anomalies / total_records) * 100

    summary_text = f"Total records in dataset: {total_records}\n"
    summary_text += f"Normal records (non-anomalies): {normal_records}\n"
    summary_text += f"Anomalies detected: {num_anomalies} ({anomaly_percentage:.2f}% of total)\n"

    return summary_text

def generate_insights(anomalies):
    insights = ""

    if not anomalies.empty:
        # Example insights based on anomaly detection
        insights += "### Insights from Anomalies:\n"
        insights += "- Anomalies were detected in the dataset.\n"
        insights += "- These records deviate significantly from the norm in terms of quantity sold, sale price, cost price, and profit.\n"
        insights += "- Consider investigating further to understand the root causes of these anomalies.\n"
    else:
        insights += "### No Anomalies Detected:\n"
        insights += "- No anomalies were found in the dataset.\n"
        insights += "- All records appear to be within expected ranges.\n"
        insights += "- Continue monitoring to ensure data consistency and quality.\n"

    return insights

def detect_anomalies(file_path, algos, outliers_fraction=0.01):
    try:
        if file_path.endswith('.csv'):
            df = pd.read_csv(file_path)
        elif file_path.endswith('.xls') or file_path.endswith('.xlsx'):
            df = pd.read_excel(file_path)
        else:
            raise ValueError("Unsupported file format. Please provide a CSV or Excel file.")
    except Exception as e:
        print(f"Error reading the file: {e}")
        return

    cols = ['Sales', 'Profit']

    if not all(col in df.columns for col in cols):
        print(f"Columns {cols} not found in the file.")
        return

    original_df = df.copy()  # Keep a copy of the original data

    minmax = MinMaxScaler(feature_range=(0, 1))
    df[cols] = minmax.fit_transform(df[cols])

    X1 = df['Sales'].values.reshape(-1, 1)
    X2 = df['Profit'].values.reshape(-1, 1)
    X = np.concatenate((X1, X2), axis=1)

    anomalies_dict = {}
    plots_dict = {}

    algo_dict = {
        'isolation_forest': IsolationForest(contamination=outliers_fraction, random_state=0),
        #'knn': KNN(contamination=outliers_fraction),
        #'cblof': CBLOF(contamination=outliers_fraction, random_state=0),
        #'lof': LOF(contamination=outliers_fraction)
    }

    for algo in algos:
        # Reset df to original state without any anomaly columns
        df = pd.read_excel(file_path) if file_path.endswith('.xls') or file_path.endswith('.xlsx') else pd.read_csv(file_path)
        df[cols] = minmax.fit_transform(df[cols])

        clf = algo_dict.get(algo)
        if clf is None:
            continue

        clf.fit(X)
        scores_pred = clf.decision_function(X) * -1
        y_pred = clf.predict(X)


        plot_json = plot_anomalies(df, clf, scores_pred, y_pred, algo, outliers_fraction)

        df[f'anomaly_{algo}'] = y_pred
        df[f'anomaly_score_{algo}'] = scores_pred

        

        if algo == 'isolation_forest':
            anomalies = df[df[f'anomaly_{algo}'] == -1].copy()
        else:
            anomalies = df[df[f'anomaly_{algo}'] == 1].copy()

        #anomalies = df[df[f'anomaly_{algo}'] == 1].copy()

        # Merge anomalies with original data to get the original 'Sales' and 'Profit' values
        anomalies = anomalies.merge(original_df, left_index=True, right_index=True, suffixes=('_normalized', ''))

        # Select only the required columns
        anomalies = anomalies[['Offer_description', 'Sales', 'Profit', f'anomaly_score_{algo}']]

        # Convert Timestamps to strings
        anomalies = anomalies.applymap(lambda x: x.strftime('%Y-%m-%d %H:%M:%S') if isinstance(x, pd.Timestamp) else x)

        anomalies_dict[algo] = anomalies
        plots_dict[algo] = plot_json

    #confusion marix
    print("confusion matrix")
    df['anomaly']=y_pred
    true_lables=df['anomaly']
    predicted_labels=y_pred
    cm=confusion_matrix(true_lables,predicted_labels)
    print ("this",cm)
    
    
    
    # Convert anomalies to JSON
    anomalies_json = {}
    for algo, anomalies in anomalies_dict.items():
        anomalies_json[algo] = anomalies.to_dict(orient='records')

    # Generate summary and insights

    if algo == 'isolation_forest':
      summary_text = generate_summary(original_df, df[df[f'anomaly_{algo}'] == -1])
      insights_text = generate_insights(df[df[f'anomaly_{algo}'] == -1])
    else:
      summary_text = generate_summary(original_df, df[df[f'anomaly_{algo}'] == 1])
      insights_text = generate_insights(df[df[f'anomaly_{algo}'] == 1])

    result = {
        "data": anomalies_json,
        "summary": summary_text,
        "insights": insights_text,
        "plots": plots_dict
    }

    return result

def plot_anomalies(df, clf, scores_pred, y_pred, title, outliers_fraction):
    xx, yy = np.meshgrid(np.linspace(0, 1, 100), np.linspace(0, 1, 100))

    # Plotting
    plt.figure(figsize=(8, 8))
    df1 = df.copy()
    df1['outlier'] = y_pred.tolist()

    inliers_sales = np.array(df1['Sales'][df1['outlier'] == 0]).reshape(-1, 1)
    inliers_profit = np.array(df1['Profit'][df1['outlier'] == 0]).reshape(-1, 1)

    outliers_sales = df1['Sales'][df1['outlier'] == 1].values.reshape(-1, 1)
    outliers_profit = df1['Profit'][df1['outlier'] == 1].values.reshape(-1, 1)

    threshold = percentile(scores_pred, 100 * outliers_fraction)

    Z = clf.decision_function(np.c_[xx.ravel(), yy.ravel()]) * -1
    Z = Z.reshape(xx.shape)

    # Ensure levels are valid
    min_level = Z.min()
    if threshold < min_level:
        threshold = min_level

    levels = np.linspace(min_level, Z.max(), 7)

    plt.contourf(xx, yy, Z, levels=levels, cmap=plt.cm.Blues_r)
    a = plt.contour(xx, yy, Z, levels=[threshold], linewidths=2, colors='red')
    plt.contourf(xx, yy, Z, levels=[threshold, Z.max()], colors='orange')
    b = plt.scatter(inliers_sales, inliers_profit, c='white', s=20, edgecolor='k')
    c = plt.scatter(outliers_sales, outliers_profit, c='black', s=20, edgecolor='k')

    plt.axis('tight')
    plt.legend([a.collections[0], b, c], ['learned decision function', 'inliers', 'outliers'],
               prop={'size': 20}, loc='lower right')
    plt.xlim((0, 1))
    plt.ylim((0, 1))
    plt.title(title)

    # Convert plot to base64 string
    buf = io.BytesIO()
    plt.savefig(buf, format='png')
    buf.seek(0)
    image_base64 = base64.b64encode(buf.read()).decode('utf-8')
    buf.close()

    # Clear the plot to avoid overlapping in further plots
    plt.close()

    return image_base64





if __name__=='__main__':
    app.run(debug=True)
    