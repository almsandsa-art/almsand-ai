
import json
import os
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.svm import LinearSVC
from sklearn.pipeline import make_pipeline
import joblib

script_dir = os.path.dirname(__file__)
prepared_data_path = os.path.join(script_dir, "prepared_data.json")
model_path = os.path.join(script_dir, "ai_model.joblib")

with open(prepared_data_path, "r", encoding="utf-8") as f:
    data = json.load(f)

X_train = []
y_train = []
for intent in data["intents"]:
    for pattern in intent["patterns"]:
        X_train.append(pattern)
        y_train.append(intent["tag"])

model = make_pipeline(TfidfVectorizer(), LinearSVC(max_iter=2000))
model.fit(X_train, y_train)

joblib.dump(model, model_path)
print("Model retrained and saved successfully.")


