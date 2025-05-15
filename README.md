# Sentiment Analysis Web App

This is a Sentiment Analysis Web App that allows users to input text and receive sentiment classification (e.g., Positive, Negative). It uses a Transformer-based deep learning model and integrates a full ML lifecycle stack.

## Roll No and Name

Roll No: `ME21B057`, Name: Eshan Kulkarni

## Training Dataset

customer reviews dataset: [https://paperswithcode.com/dataset/arxiv-10](https://www.kaggle.com/datasets/bittlingmayer/amazonreviews)
format of the dataset: __label__<X> __label__<Y> ... <Text>

This dataset consists of a few million Amazon customer reviews (input text) and star ratings (output labels) for learning how to train fastText for sentiment analysis. 

## User Manual

I have made a detailed user manual for this app. It is saved as Sentiment_Analysis_App_User_Manual.pdf in this repository. Please go through it after setup of app.

## Categories

The classifier as of now supports only English language text as it was trained on only English Language. 

## Features

| Feature                   | Description                                                                                     |
| ------------------------- | ----------------------------------------------------------------------------------------------- |
| **Real-time Predictions** | Sentiment output with confidence score instantly displayed.                                     |
| **Feedback Loop**         | User feedback triggers retraining after a threshold (e.g., 2 submissions).                      |
| **Auto-Retraining**       | Model retrains automatically with appended feedback data.                                       |
| **Model Versioning**      | MLflow manages multiple versions; models can be promoted/demoted using aliases like `champion`. |
| **Observability**         | Prometheus metrics on API usage and latency for monitoring.                                     |
| **Data Versioning**       | DVC ensures all data changes (training, feedback) are tracked and reproducible.                 |
| **Code Tracking**         | Git ensures all changes to code, configs, and models are traceable.                             |


## Project Structure

```
Amazon-Review-Sentiment-Analysis/
├── .dvc/                      # DVC metadata for data versioning
├── .dvcignore                 # DVC ignore file
├── Dockerfile.api             # Dockerfile for FastAPI backend
├── Dockerfile.streamlit       # Dockerfile for Streamlit frontend
├── README.md                  # Project overview and instructions
├── Sentiment_Analysis_App_User_Manual.pdf  # Detailed user manual
├── app.env                    # Environment variables for the application
├── docker-compose.yaml        # Docker Compose configuration
├── dvc.lock                   # DVC lock file for reproducibility
├── dvc.yaml                   # DVC pipeline stages and dependencies
├── logs/                      # Directory for application logs
├── monitoring/
    ├── prometheus.yaml        # Monitoring configurations (e.g., Prometheus, Grafana)
├── requirements.txt           # Python dependencies
├── sentiment-analysis-with-hugging-face.ipynb  # Jupyter notebook for model development
└── src/                       # Source code directory
    ├── api/                   
        ├── main.py            # FastAPI backend script
    └── data/
        ├── load_data.py       # loading and pre-processing data         
    └── models/
        ├── train_model.py     # Model training script
    └── ui/                     
        ├── app.py             # Streamlit application script
```

## Technologies Used

| Tool / Library                 | Purpose                                                                             |
| ------------------------------ | ----------------------------------------------------------------------------------- |
| **FastAPI**                    | REST API for serving sentiment analysis predictions.                                |
| **MLflow**                     | Model lifecycle management, version control, and deployment.                        |
| **Streamlit**                  | Interactive web UI for non-technical users.                                         |
| **Prometheus**                 | Metrics collection and monitoring (via `/metrics`).                                 |
| **Pydantic**                   | API request data validation.                                                        |
| **Git**                        | Source code tracking and version control.                                           |
| **DVC (Data Version Control)** | Tracks changes in training data and feedback datasets for reproducible experiments. |
| **Docker / Docker Compose**    | Containerization and service orchestration (Streamlit, MLflow, etc.).               |


![Image](https://github.com/user-attachments/assets/a6986b68-e4c1-405d-a960-0a2a33ea5a04)
## Installation

### Local Setup

Clone the repository:

```bash
git clone https://github.com/ehindasche/Amazon-Review-Sentiment-Analysis.git
```

Create and activate a virtual environment:

```bash
python -m venv arxiv_env
source arxiv_env/bin/activate  # On Windows: arxiv_env\Scripts\activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```
Initialize Git:

```bash
git init
```

Initialize DVC:

```bash
dvc init
```

Train the initial model:

```bash
dvc repro train_model
```

Run MLflow:

```bash
mlflow ui
```

Run the application:

```bash
streamlit run app.py
```

Start node_exporter in your system. Start prometheus using config file as prometheus.yml and start the docker image of grafana. The grafana dashboard should look like grafana_dashboard_scrrenshot.png image file.

### Docker Setup

Build and start the containers:

```bash
docker-compose up -d
```

Access the services:

- Frontend: http://localhost:8501
- Backend API: http://localhost:8000
- MLflow: http://localhost:5000
- Prometheus: http://localhost:9090
- Grafana: http://localhost:3000

## Usage

### Paper Classification

### 🧪 How to Use the Application
**Access the Streamlit Frontend:**

- Navigate to http://localhost:8501 in your web browser.

**Input Text for Analysis:**

- Enter the text you wish to analyze in the provided input box and click "Analyze".

**View Results:**

- The application will display the sentiment classification along with a confidence score.

**Provide Feedback:**

- If the prediction is incorrect, select the correct sentiment from the dropdown, add optional comments, and submit feedback.

**Monitor Performance:**

- Access Grafana at http://localhost:3000 to view application metrics and performance dashboards.

### Model Training

Initial training:

```bash
dvc repro train_model
```

## Monitoring

### Prometheus Metrics

The application exposes the following metrics at http://localhost:8000/metrics:

| Metric Name                | Type        | Description                                                                                                |
| -------------------------- | ----------- | ---------------------------------------------------------------------------------------------------------- |
| `api_requests_total`       | `Counter`   | Total number of API requests received by the `/analyze` endpoint. Increments on every call.                |
| `api_errors_total`         | `Counter`   | Total number of errors/exceptions thrown during prediction. Increments when an error occurs in `/analyze`. |
| `request_duration_seconds` | `Histogram` | Time taken to process each `/analyze` request (end-to-end latency). Captures performance distribution.     |


### 📊 Grafana Dashboard Panels
**1. API Request Volume**
Metric: api_requests_total

Panel Type: Time-series graph or single stat

Description: Tracks total number of /analyze requests over time.

Insight: Understand app usage trends and traffic volume.

**2. API Error Rate**
Metric: api_errors_total

Panel Type: Time-series graph or bar chart

Description: Tracks number of prediction errors over time.

Insight: Detect model serving failures or system issues.

**3. Request Latency (Duration)**
Metric: request_duration_seconds

Panel Type: Histogram (bucket view), percentile (95th/99th), or heatmap

Description: Shows how long each /analyze request takes.

Insight: Monitor inference performance and identify bottlenecks.

**4. Error Rate %**
Formula: (rate(api_errors_total[5m]) / rate(api_requests_total[5m])) * 100

Panel Type: Line graph or gauge

Description: Percentage of requests resulting in errors.

Insight: Spot spikes in system instability.

**5. Uptime Monitoring**
Metric: Use custom Prometheus rules or health check probes (/health)

Panel Type: Status panel (green/red)

Description: Indicates if the FastAPI backend is healthy.

Insight: Instantly see if the model serving is down.

**6. Model Info Panel**
Static Info from /model-info

Description: Show current model name, version, alias (champion), and run ID.

Insight: Know which model is currently deployed.

## Continuous Learning

The system automatically:

- Monitors user feedback in `data/feedback/user_corrections.csv`
- Triggers retraining when feedback count reaches threshold (default: 2, ideally should be large)
- Evaluates new models against existing ones in mlflow
- Automatically serves the best-performing model present in mlflow runs
