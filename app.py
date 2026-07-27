import streamlit as st
from deezer_api import get_songs

st.set_page_config(
    page_title="Mood-Based Music Recommendation",
    page_icon="🎧",
    layout="centered"
)

st.title("Mood-Based Music Recommendation")

st.write("Write how you feel today:")

user_text = st.text_input(
    "Your mood",
    placeholder="Example: I am feeling sad today"
)

language = st.selectbox(
    "Choose music language",
    ["Both", "Hindi", "English"]
)


def detect_emotion(text):
    text = text.lower()

    emotion_keywords = {
        "happy": [
            "happy", "joy", "joyful", "excited", "good",
            "great", "awesome", "fun", "cheerful",
            "खुश", "खुशी", "मज़ा", "उत्साहित"
        ],
        "sad": [
            "sad", "sadness", "unhappy", "depressed",
            "lonely", "cry", "crying", "hurt",
            "broken", "low", "upset",
            "दुखी", "उदास", "अकेला", "रोना", "परेशान"
        ],
        "angry": [
            "angry", "anger", "mad", "furious",
            "annoyed", "irritated", "hate",
            "गुस्सा", "क्रोधित", "नाराज़", "चिढ़"
        ],
        "romantic": [
            "love", "romantic", "romance", "loving",
            "crush", "relationship", "date",
            "प्यार", "इश्क", "रोमांटिक", "मोहब्बत"
        ],
        "calm": [
            "calm", "peaceful", "relaxed", "relax",
            "quiet", "peace", "stress free",
            "शांत", "सुकून", "आराम", "शांति"
        ],
        "energetic": [
            "energetic", "energy", "motivated",
            "motivation", "power", "active",
            "dance", "party",
            "जोश", "ऊर्जा", "मोटिवेशन", "नाचना"
        ]
    }

    for emotion, keywords in emotion_keywords.items():
        for keyword in keywords:
            if keyword in text:
                return emotion

    return "happy"


if st.button("Recommend Songs"):

    if not user_text.strip():
        st.warning("Please write how you feel first.")
        st.stop()

    detected_emotion = detect_emotion(user_text)

    st.success(f"Detected Emotion: {detected_emotion.title()}")

    songs = get_songs(
        mood=detected_emotion,
        language=language,
        limit=10
    )

    if not songs:
        st.error("No songs found. Please try another mood.")
        st.stop()

    st.subheader("Recommended Songs")

    for song in songs:

        st.image(
            song["cover"],
            width=250
        )

        st.markdown(
            f"### {song['title']}"
        )

        st.write(
            f"Artist: {song['artist']}"
        )

        st.write(
            f"Album: {song['album']}"
        )

        if song["preview"]:
            st.audio(song["preview"])
        else:
            st.write("Preview not available.")

        st.link_button(
            "Listen on Deezer",
            song["link"]
        )

      
