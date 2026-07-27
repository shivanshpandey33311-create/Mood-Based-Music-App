import os
import pickle
import streamlit as st


MODEL_PATH = "emotion_model.pkl"
VECTORIZER_PATH = "tfidf_vectorizer 2.pkl"


@st.cache_resource
def load_model():

    if not os.path.exists(MODEL_PATH):
        raise FileNotFoundError(
            f"{MODEL_PATH} was not found."
        )

    if not os.path.exists(VECTORIZER_PATH):
        raise FileNotFoundError(
            f"{VECTORIZER_PATH} was not found."
        )

    with open(MODEL_PATH, "rb") as file:
        model = pickle.load(file)

    with open(VECTORIZER_PATH, "rb") as file:
        vectorizer = pickle.load(file)

    return model, vectorizer


def normalize_emotion(value):

    value = str(value).strip().lower()

    mapping = {
        "sadness": "sad",
        "sad": "sad",
        "joy": "happy",
        "happy": "happy",
        "happiness": "happy",
        "love": "love",
        "loving": "love",
        "anger": "angry",
        "angry": "angry",
        "fear": "fear",
        "afraid": "fear",
        "surprise": "surprise",
        "surprised": "surprise"
    }

    return mapping.get(value, value)


def detect_emotion(text):

    model, vectorizer = load_model()

    text_vector = vectorizer.transform([text])

    prediction = model.predict(text_vector)[0]

    confidence = 0.0

    if hasattr(model, "predict_proba"):

        probabilities = model.predict_proba(
            text_vector
        )[0]

        confidence = float(
            max(probabilities) * 100
        )

    emotion = normalize_emotion(
        prediction
    )

    return emotion, confidence
