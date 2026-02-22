import pytest
import joblib
import pandas as pd


@pytest.fixture
def model():
    return joblib.load("/Users/miriambenali/Desktop/Project-Simplon/HR-pulse-ai-platform/model/hr_ai_platform.pkl")

def test_predict(model):
    sample = pd.DataFrame([{
        "Job Title":"senior data scientist",
        "Job Description":"descriptionthe senior data scientist is respon...",
        "Rating": 3.1,
        "Company Name": "healthfirst3.1",
        "Industry":"insurance carriers",
        "Sector":"insurance",
        "company_age":33.0,
        "size_category":"medium"

    }])

    prediction = model.predict(sample)
    assert prediction is not None