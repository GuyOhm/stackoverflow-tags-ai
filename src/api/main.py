import mlflow
import pickle
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import os

from src.api.lib.process_text import process_text
from src.api.lib.path_utils import get_project_root

# Initialize FastAPI app
app = FastAPI(
    title="StackOverflow Tags Suggester API",
    description="API to suggest tags for StackOverflow questions.",
    version="0.1.0"
)

# Pydantic model for prediction requests
class Question(BaseModel):
    body: str

# Pydantic model for prediction responses
class Tags(BaseModel):
    tags: list[str]

# --- Storage for loaded models and artifacts ---
model = None
vectorizer = None
mlb = None

@app.on_event("startup")
def startup_event():
    """
    Load models and artifacts when the application starts.
    """
    global model, vectorizer, mlb

    project_root = get_project_root()
    
    MODEL_PATH = project_root / "models/sgd_tfidf_model"
    VECTORIZER_PATH = project_root / "models/vectorizer/tfidf_vectorizer_title_and_body.pkl"
    MLB_PATH = project_root / "models/multi_label_binarizer/mlb.pkl"

    try:
        print(f"Loading model from {MODEL_PATH}...")
        model = mlflow.sklearn.load_model(MODEL_PATH)    
        print("Model loaded successfully!")

        print(f"Loading vectorizer from {VECTORIZER_PATH}...")
        with open(VECTORIZER_PATH, "rb") as f:
            vectorizer = pickle.load(f)
        print("Vectorizer loaded successfully!")

        print(f"Loading binarizer from {MLB_PATH}...")
        with open(MLB_PATH, "rb") as f:
            mlb = pickle.load(f)
        print("Binarizer loaded successfully!")

    except Exception as e:
        print(f"❌ An error occurred while loading the model or artifacts:")
        print(e)

# Prediction endpoint
@app.post("/predict", response_model=Tags)
def predict(question: Question):
    """
    Predicts tags for a given question.
    """
    if not all([model, vectorizer, mlb]):
        raise HTTPException(status_code=503, detail="Model or artifacts not loaded yet")

    processed_text = process_text(question.body)

    vectorized_text = vectorizer.transform([processed_text])
    prediction = model.predict(vectorized_text)
    predicted_tags = mlb.inverse_transform(prediction)

    return {"tags": list(predicted_tags[0])}

# Root endpoint
@app.get("/")
def read_root():
    return {"message": "Welcome to the StackOverflow Tags Suggester API!"}
