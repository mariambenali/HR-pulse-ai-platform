import pytest
import joblib
import pandas as pd


@pytest.fixture
def model():
    return joblib.load("/Users/miriambenali/Desktop/Project-Simplon/HR-pulse-ai-platform/model/hr_ai_platform.pkl")

def test_predict(model):
    sample = pd.DataFrame([{
        "Rating": 3.1,
        "Company_Name": "healthfirst",
        "Industry": "insurance carriers",
        "Sector": "insurance",
        "seniority": "senior",
        "job_role": "data scientist",
        "skills": "Azure Machine Learning",
        "log_revenue": 19.519293,
        "company_age": 33.0,
        "size_category": "medium"

    }])

    prediction = model.predict(sample)
    assert prediction is not None