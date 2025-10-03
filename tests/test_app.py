import io
import pandas as pd
from fastapi.testclient import TestClient
import app  # if app.py is at project root
# from threatlens import app  # if inside package

client = TestClient(app.app)


def test_root_redirect():
    """Root endpoint should redirect to /docs"""
    response = client.get("/")
    assert response.status_code in (200, 307)
    assert "docs" in str(response.url)


def test_train_model():
    """Test /train endpoint (just checks status code)"""
    response = client.get("/train")
    assert response.status_code == 200


def test_predict(monkeypatch):
    """Test /predict endpoint with mocked model and preprocessor"""
    from threatlens.utils.mains import utils
    from threatlens.utils.learning.model.classifier import ThreatLensModel

    # Mock pickle loading
    class MockPreprocessor:
        def transform(self, X):
            return X

    class MockModel:
        def predict(self, X):
            return [0] * len(X)

    monkeypatch.setattr(utils, "load_pickle",
                        lambda _: MockPreprocessor() if "preprocessor" in _ else MockModel())

    # Override ThreatLensModel
    class MockThreatLensModel(ThreatLensModel):
        def predict(self, X):
            return [1] * len(X)

    monkeypatch.setattr(app, "ThreatLensModel", MockThreatLensModel)

    payload = {"data": [{"url": "http://example.com", "feature1": 1, "feature2": 0.5}]}
    response = client.post("/predict", json=payload)
    assert response.status_code == 200
    assert response.json()["predictions"] == [1]


def test_batch_predict(monkeypatch, tmp_path):
    """Test batch prediction with a fake CSV upload"""
    from threatlens.utils.mains import utils
    from threatlens.utils.learning.model.classifier import ThreatLensModel

    # Mock pickle loading
    class MockPreprocessor:
        def transform(self, X):
            return X

    class MockModel:
        def predict(self, X):
            return [1] * len(X)

    monkeypatch.setattr(utils, "load_pickle",
                        lambda _: MockPreprocessor() if "preprocessor" in _ else MockModel())

    class MockThreatLensModel(ThreatLensModel):
        def predict(self, X):
            return [1] * len(X)

    monkeypatch.setattr(app, "ThreatLensModel", MockThreatLensModel)

    # Create fake CSV
    csv_path = tmp_path / "input.csv"
    df = pd.DataFrame({"url": ["http://example.com"], "feature1": [1], "feature2": [0.5]})
    df.to_csv(csv_path, index=False)

    with open(csv_path, "rb") as f:
        response = client.post("/batch_predict", files={"file": ("input.csv", f, "text/csv")})

    assert response.status_code == 200
    assert "table" in response.text
