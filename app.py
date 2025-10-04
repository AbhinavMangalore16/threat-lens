import os
import sys
import logging
import certifi
import pymongo
import boto3
import pickle
from dotenv import load_dotenv
load_dotenv()

from threatlens.exception.exception import ThreatLensException
from threatlens.logging.logger import logger
from threatlens.pipeline.train_pipeline import TrainPipeline
from threatlens.utils.mains.utils import load_pickle
from threatlens.constants.training_pipeline import DATA_INGESTION_COLLECTION, DATA_INGESTION_DB
from threatlens.utils.learning.model.classifier import ThreatLensModel

from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI, File, UploadFile, Form, Request, Depends
from uvicorn import run as uvicorn_run
from fastapi.responses import HTMLResponse, JSONResponse, Response
from fastapi.encoders import jsonable_encoder
from starlette.responses import RedirectResponse
from contextlib import asynccontextmanager
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel
from typing import List, Dict, Any
templates = Jinja2Templates(directory="temp_pred")


import pandas as pd
ca = certifi.where()
MONGO_DB_URL = os.getenv("MONGO_DB_URI")
AWS_ACCESS_KEY_ID = os.getenv("AWS_ACCESS_KEY_ID")
AWS_SECRET_ACCESS_KEY = os.getenv("AWS_SECRET_ACCESS_KEY")
AWS_REGION = os.getenv("AWS_REGION")
BUCKET_NAME = os.getenv("BUCKET_NAME")

class PredictRequest(BaseModel):
    data: List[Dict[str, Any]]
class PredictResponse(BaseModel):
    predictions: List[Any]

@asynccontextmanager
async def lifespan(app: FastAPI):
    try:
        ca = certifi.where()
        MONGO_DB_URL = os.getenv("MONGO_DB_URI")
        client = pymongo.MongoClient(MONGO_DB_URL, tlsCAFile=ca)
        app.state.db_client = client
        app.state.db = client[DATA_INGESTION_DB]
        app.state.collection = app.state.db[DATA_INGESTION_COLLECTION]
        logger.info("✅ MongoDB connection established.")
        yield
    except Exception as e:
        logger.error("❌ Failed to connect to MongoDB.")
        raise ThreatLensException(e, sys)
    finally:
        client.close()
        logger.info("🔌 MongoDB connection closed.")

app = FastAPI(
    title="ThreatLens ML API",
    description="API for triggering the training pipeline of ThreatLens",
    version="1.0.0",
    lifespan=lifespan
)

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

s3_client = boto3.client(
    "s3",
    aws_access_key_id = AWS_ACCESS_KEY_ID,
    aws_secret_access_key = AWS_SECRET_ACCESS_KEY,
    region_name = AWS_REGION
)

prefix = "production/"
response = s3_client.list_objects_v2(Bucket=BUCKET_NAME, Prefix=prefix, Delimiter='/')
folders = [f['Prefix'] for f in response.get('CommonPrefixes', [])]
latest_folder = sorted(folders)[-1]  # assuming timestamped names sort correctly
print("Latest folder:", latest_folder)
def load_files_from_s3(s3_key: str):
    try:
        res = s3_client.get_object(Bucket = BUCKET_NAME, Key = s3_key)
        obj = pickle.load(res['Body'])
        return obj
    except Exception as e:
        raise RuntimeError(f"Error loading: {e}")


@app.get("/", tags=["Navigation"])
async def root():
    return RedirectResponse(url="/docs")


@app.get("/train", tags=["Pipeline"])
async def train_model():
    try:
        logger.info("⚙️ Training pipeline initiated.")
        train_pipeline = TrainPipeline()
        train_pipeline.run_pipeline()
        logger.info("✅ Training pipeline completed successfully.")
        return JSONResponse(status_code=200, content={"message": "✅ Training completed successfully."})
    except Exception as e:
        logger.exception("❌ Error during training pipeline execution.")
        raise ThreatLensException(e, sys)
@app.post("/batch_predict", tags=["Batch Prediction"])
async def batch_predict(request: Request, file: UploadFile = File(...), response_class: Response = HTMLResponse):
    try:
        df = pd.read_csv(file.file)
        logger.info("⚙️ Batch prediction initiated.")
        
        preprocessor = load_pickle("production/preprocessor.pkl")
        model = load_pickle("production/phishing_prod_model.pkl")
        threatlens_model = ThreatLensModel(preprocessor=preprocessor, model=model)

        y_pred = threatlens_model.predict(df)
        df["prediction"] = y_pred

        table = df.to_html(classes='table table-striped', index=False)
        df.to_csv("predictions/predictions.csv", index=False)
        if not os.path.exists('predictions'):
            os.makedirs('predictions')
        
        # Save the HTML table content to a file in the 'predictions' folder
        with open("predictions/table.html", "w") as f:
            f.write(table)
        logger.info("✅ Batch prediction completed successfully.")
        return templates.TemplateResponse("table.html", {"request": request, "table": table})
    
    except Exception as e:
        logger.exception("❌ Error during batch prediction.")
        raise ThreatLensException(e, sys) from e

@app.post("/predict", response_model=PredictResponse, tags=["Prediction"])
async def predict(request: PredictRequest):
    try:
        logger.info("Initiation prediction pipeline....")
        input_data = pd.DataFrame(request.data)
        preprocessor = load_files_from_s3(f"{latest_folder}preprocessor.pkl")
        model = load_files_from_s3(f"{latest_folder}phishing_prod_model.pkl")
        threatlens_model = ThreatLensModel(preprocessor=preprocessor, model=model)

        y_pred = threatlens_model.predict(input_data)
        logger.info("✅ Prediction completed successfully.")
        return PredictResponse(predictions=list(y_pred))
    
    except Exception as e:
        logger.exception("❌ Error during prediction.")
        raise ThreatLensException(e, sys) from e
    
@app.get("/health", tags=["Health"])
async def health_check():
    return {"status": "ok"}

if __name__ == "__main__":
    uvicorn_run(app, host="localhost", port=8000)
