# chatbot/intent_classifier.py
import pickle
from sentence_transformers import SentenceTransformer
import numpy as np

_model_data = None
_classifier = None
_embedder = None

def _ensure_loaded():
    global _model_data, _classifier, _embedder
    if _model_data is None:
        with open("models/intent_clf.pkl", "rb") as f:
            _model_data = pickle.load(f)
        _classifier = _model_data["classifier"]
        _embedder = SentenceTransformer(_model_data["embed_model_name"])

def predict_intent_with_confidence(text):
    """
    Returns (intent_label, confidence_score_between_0_and_1)
    """
    _ensure_loaded()
    emb = _embedder.encode([text], convert_to_numpy=True)
    probs = None
    # if classifier supports predict_proba
    if hasattr(_classifier, "predict_proba"):
        probs = _classifier.predict_proba(emb)[0]
        idx = int(np.argmax(probs))
        label = _classifier.classes_[idx]
        confidence = float(probs[idx])
    else:
        label = _classifier.predict(emb)[0]
        confidence = 0.5  # unknown; fallback
    return label, confidence
