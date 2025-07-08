import mlflow
import pickle
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import os

from src.api.lib.process_text import process_text
from src.api.lib.path_utils import get_project_root

# Initialisation de l'application FastAPI
app = FastAPI(
    title="StackOverflow Tags Suggester API",
    description="API to suggest tags for StackOverflow questions.",
    version="0.1.0"
)

# Modèle de données pour les requêtes de prédiction
class Question(BaseModel):
    body: str

# Modèle de données pour les réponses de prédiction
class Tags(BaseModel):
    tags: list[str]

# --- Stockage des modèles et artefacts chargés ---
model = None
vectorizer = None
mlb = None

@app.on_event("startup")
def startup_event():
    """
    Charge les modèles et les artefacts au démarrage de l'application.
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

# Endpoint de prédiction
@app.post("/predict", response_model=Tags)
def predict(question: Question):
    """
    Prédit les tags pour une question donnée.
    """
    if not all([model, vectorizer, mlb]):
        raise HTTPException(status_code=503, detail="Model or artifacts not loaded yet")

    processed_text = process_text(question.body)

    vectorized_text = vectorizer.transform([processed_text])
    prediction = model.predict(vectorized_text)
    predicted_tags = mlb.inverse_transform(prediction)

    return {"tags": list(predicted_tags[0])}

# Endpoint racine
@app.get("/")
def read_root():
    return {"message": "Welcome to the StackOverflow Tags Suggester API!"}
