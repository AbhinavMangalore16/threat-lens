import os
import sys
import logging
import certifi
import pymongo
from dotenv import load_dotenv

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse, RedirectResponse
from uvicorn import run as uvicorn_run
from contextlib import asynccontextmanager

from threatlens.exception.exception import ThreatLensException
from threatlens.logging.logger import logger
from threatlens.pipeline.train_pipeline import TrainPipeline
from threatlens.constants.training_pipeline import DATA_INGESTION_DB, DATA_INGESTION_COLLECTION

load_dotenv()


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


if __name__ == "__main__":
    uvicorn_run(app, host="localhost", port=8000)
