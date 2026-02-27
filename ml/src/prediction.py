import joblib
import os


BASE_DIR = os.path.abspath(
    os.path.join(
        os.path.dirname(__file__), "../""../"
    )
)

def load_model():
    file_path = os.path.join(
    BASE_DIR,
    "model",
    "hr_ai_platform.pkl"
)
    model_path = joblib.load(file_path)

    return model_path

'''model= load_model()
print(model)'''


