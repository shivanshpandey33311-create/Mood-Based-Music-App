import pickle
import streamlit as st
from deezer_api import get_songs

with open("emotion_model.pkl", "rb") as f:
    model = pickle.load(f)

with open("tfidf_vectorizer 2.pkl", "rb") as f:
    vectorizer = pickle.load(f)

emotion_map = {
    0: "admiration",
    1: "amusement",
    2: "anger",
    3: "annoyance",
    4: "approval",
    5: "caring",
    6: "confusion",
    7: "curiosity",
    8: "desire",
    9: "disappointment",
    10: "disapproval",
    11: "disgust",
    12: "embarrassment",
    13: "excitement",
    14: "fear",
    15: "gratitude",
    16: "grief",
    17: "joy",
    18: "love",
    19: "nervousness",
    20: "optimism",
    21: "pride",
    22: "realization",
    23: "relief",
    24: "remorse",
    25: "sadness",
    26: "surprise",
    27: "neutral"
}

mood_map = {
    "admiration": "admiration",
    "amusement": "happy",
    "anger": "angry",
    "annoyance": "angry",
    "approval": "happy",
    "caring": "calm",
    "confusion": "calm",
    "curiosity": "energetic",
    "desire": "romantic",
    "disappointment": "sad",
    "disapproval": "sad",
    "disgust": "angry",
    "embarrassment": "sad",
    "excitement": "energetic",
    "fear": "calm",
    "gratitude": "happy",
    "grief": "sad",
    "joy": "happy",
    "love": "romantic",
    "nervousness": "calm",
    "optimism": "happy",
    "pride": "energetic",
    "realization": "calm",
    "relief": "calm",
    "remorse": "sad",
    "sadness": "sad",
    "surprise": "energetic",
    "neutral": "chill"
}

st.title("Mood-Based Music Recommendation")

user_text = st.text_area("Write how you feel today:")

if st.button("Detect Emotion & Recommend"):

    if user_text.strip() == "":
        st.warning("Please write something first!")

    else:
        X_vec = vectorizer.transform([user_text])

        probs = model.predict_proba(X_vec)[0]

        emotions = model.classes_

        top_idx = probs.argmax()

        detected_emotion = emotions[top_idx]

        try:
            emotion_number = int(detected_emotion)
            emotion_name = emotion_map.get(
                emotion_number,
                str(detected_emotion)
            )
        except (ValueError, TypeError):
            emotion_name = str(detected_emotion)

        music_mood = mood_map.get(
            emotion_name.lower(),
            emotion_name
        )

        st.success(
            f"Detected Emotion: {emotion_name}"
        )

        st.info(
            f"Music Mood: {music_mood}"
        )

        songs = get_songs(music_mood)

        st.subheader("Recommended Songs")

        if not songs:
            st.warning("No songs found. Please try again.")

        else:
            for song in songs:

                st.markdown(
                    f"### {song['title']}"
                )

                st.write(
                    f"Artist: {song['artist']}"
                )

                st.write(
                    f"Album: {song['album']}"
                )

                if song.get("cover"):
                    st.image(
                        song["cover"],
                        width=200
                    )

                if song.get("preview"):
                    st.audio(
                        song["preview"],
                        format="audio/mp3"
                    )

                else:
                    st.write(
                        "Preview not available for this song."
                    )

                st.divider()
      
