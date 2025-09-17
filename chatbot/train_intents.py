import json
import os
import pickle
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.svm import LinearSVC

os.makedirs("models", exist_ok=True)

# Load intents
with open("data/intents.json", "r") as f:
    data = json.load(f)

X, y = [], []
for intent in data["intents"]:
    for pattern in intent["patterns"]:
        X.append(pattern)
        y.append(intent["tag"])

# Vectorize text
vectorizer = TfidfVectorizer()
X_vec = vectorizer.fit_transform(X)

# Train classifier
clf = LinearSVC()
clf.fit(X_vec, y)

# Save model + vectorizer
with open("models/intent_classifier.pkl", "wb") as f:
    pickle.dump(clf, f)

with open("models/vectorizer.pkl", "wb") as f:
    pickle.dump(vectorizer, f)

print("✅ Intent classifier trained and saved!")
