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
arxiv-classifier/
├── app/
│   ├── backend/
│   │   ├── main.py             # FastAPI backend server
│   │   ├── mlflow_utils.py     # MLflow model loading utilities
│   │   ├── pdf_extractor.py    # extraction of title and abstract from pdf
│   │   ├── tasks.py            # Background tasks (feedback monitoring, model updates)
│   ├── frontend/
│   │   ├── app.py              # Streamlit frontend
│   ├── run.py                  # Script to run all services
├── data/
│   ├── feedback/
│   │   ├── user_corrections.csv # User feedback storage
│   ├── processed/              # Processed datasets
│   ├── raw/                    # Raw datasets
├── data_processing/            # Data preprocessing modules
├── model/                      # Model definition and training code
├── pipelines/                  # DVC pipeline definitions
│   ├── fine_tune.py            # Fine-tuning with user feedback
│   ├── train.py                # Initial model training
├── prometheus.yml              # Prometheus configuration
├── docker-compose.yml          # Docker Compose configuration
├── Dockerfile                  # Docker image definition
├── requirements.txt            # Python dependencies
├── .dockerignore               # Docker build exclusions
├── dvc.yaml                    # DVC pipeline definition
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
git clone https://github.com/YashG2003/arXiv_papers_classification_app.git
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

Initialize DVC:

```bash
dvc init
```

Train the initial model:

```bash
dvc repro train
```

Run the application:

```bash
python -m app.run
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

1. Navigate to http://localhost:8501
2. Upload a research paper PDF
3. View the predicted category
4. Provide feedback, if the prediction is incorrect select the correct category

### Model Training and Fine-tuning

Initial training:

```bash
python -m pipelines.train --data_version v1 --run_experiments
```

Fine-tuning with user feedback:

```bash
python -m pipelines.fine_tune --check_feedback
```

Or run training and fine tuning using DVC commands:

```bash
dvc repro train
dvc repro check_feedback
```

## Monitoring

### Prometheus Metrics

The application exposes the following metrics at http://localhost:8000/metrics:

- `unique_users_total`: Unique users by IP address
- `classify_pdf_requests_total`: Total number of classification requests
- `classify_pdf_latency_seconds`: Classification request latency in seconds
- `feedback_requests_total`: Total number of feedback submissions
- `feeedback_latency_seconds`: Feedback request latency in seconds
- `samples_requests_total`: Total number of sample prediction requests
- `samples_latency_seconds`: Sample prediction request latency in seconds

### Grafana Dashboards

Import the provided dashboard JSON to visualize:

- API requests count
- Request latencies (95th percentile)
- Unique user counts
- System resource usage

## Continuous Learning

The system automatically:

- Monitors user feedback in `data/feedback/user_corrections.csv`
- Triggers retraining when feedback count reaches threshold (default: 2, ideally should be large)
- Evaluates new models against existing ones in mlflow
- Automatically serves the best-performing model present in mlflow runs
