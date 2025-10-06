### ThreatLens

End-to-end ML system for phishing/cyber-attack detection with a production-grade training pipeline, object-storage-backed model registry, and FastAPI inference service.

- **Tech**: Python, FastAPI, scikit-learn/XGBoost/LightGBM/CatBoost, MLflow-ready
- **Capabilities**: Data ingestion → validation → transformation → model training → model artifact sync → REST inference (batch & online)

Useful links:
- (Intentionally omitted)

---

## Repository structure
```
threat-lens/
  app.py                      # FastAPI app (train + predict endpoints)
  main.py                     # CLI-style partial pipeline runner (dev)
  Dockerfile                  # Container for API service
  requirements.txt            # Python dependencies
  threatlens/                 # Library code (pipeline, components, utils)
    pipeline/train_pipeline.py
    components/{data_ingestion, data_validator, data_transform, model_training}.py
    cloud/s3_sync.py
    utils/learning/model/classifier.py
  data/                       # Local data (raw/processed)
  predictions/                # Batch prediction outputs (CSV, HTML)
  temp_pred/table.html        # Jinja template for batch results
  tests/                      # Unit tests (e.g., test_app.py)
```

---

## Quick start

1) Prerequisites
- Python 3.10+
- A document database (for metadata)
- An object storage service (for model artifacts)

2) Clone and install
```bash
git clone <repo-url>
cd threat-lens
python -m venv .venv && . .venv/Scripts/activate  # PowerShell: .\.venv\Scripts\Activate.ps1
pip install --upgrade pip
pip install -r requirements.txt
```

3) Environment variables
Create a `.env` file in the project root. Configure variables for:
- Database connection URI
- Object storage access credentials
- Object storage region and bucket/container name(s)
- Optional: frontend web URL for CORS

Do not place real secrets in documentation or version control.

4) Run the API locally (FastAPI + Uvicorn)
```bash
python app.py  # serves at http://localhost:8000 (Swagger UI at /docs)
# or
uvicorn app:app --reload --host 0.0.0.0 --port 8000
```

5) Smoke test
- Open `http://localhost:8000/health` → `{"status":"ok"}`
- Open Swagger: `http://localhost:8000/docs`

---

## API reference (high-level)

- GET `/health` → Service health
- GET `/train` → Triggers end-to-end training pipeline
- POST `/batch_predict` (multipart/form-data)
  - Form field: `file` (CSV). Returns an HTML table and writes:
    - `predictions/predictions.csv`
    - `predictions/table.html`
- POST `/predict` (application/json)
  - Body: `{ "data": [ { "feature1": ..., "feature2": ... }, ... ] }`
  - Returns: `{ "predictions": [ ... ] }`

Notes
- The online `/predict` endpoint loads the latest production preprocessor and model from the configured model registry (object storage) under `production/<timestamp>/`.
- The batch endpoint loads local `production/preprocessor.pkl` and `production/phishing_prod_model.pkl`. Ensure these exist or adapt to load from object storage like `/predict`.

---

## Training pipeline

Pipeline stages (see `threatlens/pipeline/train_pipeline.py`):
- Data Ingestion → Data Validation → Data Transformation → Model Training
- On success, artifacts and production models are synced to the configured object storage:
  - `<object-storage>/artifacts/<timestamp>/` (intermediate artifacts)
  - `<object-storage>/production/<timestamp>/` (deployable models)

Run training via API
```bash
curl -X GET http://localhost:8000/train
```

Run training via Python (advanced)
```bash
python -c "from threatlens.pipeline.train_pipeline import TrainPipeline; TrainPipeline().run_pipeline()"
```

Data sources
- Raw CSVs can live under `data/raw/` (e.g., `phishing.csv`).
- The app also supports a document database connection (configured via environment variables).

---

## Batch prediction usage

```bash
curl -X POST "http://localhost:8000/batch_predict" \
  -H "accept: text/html" \
  -H "Content-Type: multipart/form-data" \
  -F "file=@data/raw/phishing.csv"
```
Outputs
- CSV: `predictions/predictions.csv`
- HTML: `predictions/table.html`

---

## Online prediction usage

Request
```bash
curl -X POST "http://localhost:8000/predict" \
  -H "Content-Type: application/json" \
  -d '{
    "data": [
      {"feature1": 1, "feature2": 0, "feature3": 3.14},
      {"feature1": 0, "feature2": 1, "feature3": 2.71}
    ]
  }'
```

Response
```json
{
  "predictions": [0, 1]
}
```

---

## Frontend integration (placeholder)

- Public backend base URL (to be used by the frontend):
  - `https://api.your-domain.example.com` (placeholder)
- If deploying separately, set a frontend origin in `.env` and tighten CORS:
  - In `app.py`, replace `allow_origins=["*"]` with a list containing your frontend URL.
- Typical frontend calls:
  - `GET /health`, `GET /train`, `POST /predict`, `POST /batch_predict`

You can add a thin web UI for uploading CSVs and visualizing results, pointing to the backend base URL above. Until then, this section serves as a placeholder for the final frontend URL.

---

## Docker

Build
```bash
docker build -t threatlens-api .
```

Run
```bash
docker run --rm -p 8000:8000 \
  --env-file .env \
  threatlens-api
```

Notes
- Ensure required credentials and database URIs are present in the container (via `--env-file` or a secrets manager).
- Mount volumes if you want to persist `predictions/` locally: `-v $(pwd)/predictions:/app/predictions`.

---

## Testing

```bash
pytest -q
```

---

## Troubleshooting

- Object storage credentials/permissions
  - Verify access keys, region, and bucket/container policies.
- Database connectivity
  - Confirm database URI and network access.
- Model not found when calling `/predict`
  - Ensure latest artifacts exist under `<object-storage>/production/<timestamp>/`.
- Batch predict missing local `production/*.pkl`
  - Either place the files locally or refactor batch endpoint to load from object storage.

---

## License

This project is licensed under the MIT License. See `LICENSE` for details.
