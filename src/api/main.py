#! D:\Python\myvenv\Scripts\python.exe

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from prometheus_client import make_asgi_app, Counter, Histogram
import mlflow
import mlflow.pyfunc
from mlflow.tracking import MlflowClient
import os
from typing import Optional

app = FastAPI()
metrics_app = make_asgi_app()
app.mount("/metrics", metrics_app)

# Configuration
MODEL_NAME = "sentiment-analysis"  # Your registered model name
ALIAS = "champion"  # Using champion alias instead of stage
MLFLOW_TRACKING_URI = os.getenv("MLFLOW_TRACKING_URI", "http://localhost:5000")

API_REQUESTS = Counter("api_requests_total", "Total API requests")
API_ERRORS = Counter("api_errors_total", "Total API errors")
REQUEST_DURATION = Histogram("request_duration_seconds", "Request duration")

class TextInput(BaseModel):
    text: str

@app.on_event("startup")
def load_model():
    global model
    try:
        # Initialize MLflow client
        mlflow.set_tracking_uri(MLFLOW_TRACKING_URI)
        client = MlflowClient()

        # Get model version by alias
        model_uri = f"models:/{MODEL_NAME}@{ALIAS}"
        
        # Load the model
        model = mlflow.pyfunc.load_model(model_uri)
        
        # Get model details for logging
        model_version = client.get_model_version_by_alias(MODEL_NAME, ALIAS)
        print(f"Successfully loaded model '{MODEL_NAME}' version {model_version.version} with alias '{ALIAS}'")

    except Exception as e:
        raise RuntimeError(f"Model loading failed: {str(e)}")

@app.post("/analyze")
@REQUEST_DURATION.time()
def analyze_sentiment(input_data: TextInput):
    API_REQUESTS.inc()
    try:
        result = model.predict([input_data.text])[0]
        return {
            "text": input_data.text,
            "sentiment": result["label"].upper(),
            "score": float(result["score"])
        }
    except Exception as e:
        API_ERRORS.inc()
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/health")
def health_check():
    return {"status": "healthy"}

@app.get("/model-info")
def get_model_info():
    """Endpoint to get information about the loaded model"""
    try:
        client = MlflowClient()
        model_version = client.get_model_version_by_alias(MODEL_NAME, ALIAS)
        return {
            "model_name": MODEL_NAME,
            "model_version": model_version.version,
            "alias": ALIAS,
            "run_id": model_version.run_id,
            "current_stage": model_version.current_stage,
            "description": model_version.description
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))