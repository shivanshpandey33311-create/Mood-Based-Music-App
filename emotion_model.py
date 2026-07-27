import pickle
import streamlit as st


MODEL_FILE = "emotion_model.pkl"
VECTORIZER_FILE = "tfidf_vectorizer 2.pkl"


@st.cache_resource
def load_model():

    with open(MODEL_FILE, "rb") as file:
        model = pickle.load(file)

    with open(VECTORIZER_FILE, "rb") as file:
        vectorizer = pickle.load(file)

    return model, vectorizer


def detect_emotion(text):

    model, vectorizer = load_model()

    text_vector = vectorizer.transform([text])

    prediction = model.predict(text_vector)[0]

    confidence = 0.0

    if hasattr(model, "predict_proba"):

        probabilities = model.predict_proba(text_vector)[0]

        confidence = max(probabilities) * 100

    emotion = str(prediction).lower()

    emotion_map = {
        "sadness": "sad",
        "sad": "sad",
        "joy": "happy",
        "happy": "happy",
        "love": "love",
        "anger": "angry",
        "angry": "angry",
        "fear": "fear",
        "surprise": "surprise"
    }

    emotion = emotion_map.get(
        emotion,
        emotion
    )

    return emotion, confidence
