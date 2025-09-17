# chatbot/train_intents_embeddings.py
import json
import os
import pickle
from sentence_transformers import SentenceTransformer
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report
import numpy as np

os.makedirs("models", exist_ok=True)

# load intents
with open("data/intents.json", "r", encoding="utf-8") as f:
    data = json.load(f)

texts = []
labels = []
for intent in data["intents"]:
    for pattern in intent["patterns"]:
        texts.append(pattern)
        labels.append(intent["tag"])

# expand small dataset by repeating small paraphrases if needed (optional)
# Train/val split
X_train, X_val, y_train, y_val = train_test_split(texts, labels, test_size=0.15, random_state=42, stratify=labels)

# sentence-transformers model
embed_model_name = "all-MiniLM-L6-v2"
embedder = SentenceTransformer(embed_model_name)

# encode
X_train_emb = embedder.encode(X_train, convert_to_numpy=True, show_progress_bar=True)
X_val_emb = embedder.encode(X_val, convert_to_numpy=True, show_progress_bar=True)

# classifier
clf = LogisticRegression(max_iter=1000)
clf.fit(X_train_emb, y_train)

# evaluate
y_pred = clf.predict(X_val_emb)
print(classification_report(y_val, y_pred))

# save classifier + metadata
with open("models/intent_clf.pkl", "wb") as f:
    pickle.dump({"classifier": clf, "embed_model_name": embed_model_name}, f)

print("Saved models/intent_clf.pkl")
