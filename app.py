import streamlit as st

from emotion_model import detect_emotion
from youtube_api import get_songs


st.set_page_config(
    page_title="Mood-Based Music Recommendation",
    layout="wide"
)


EMOTION_DESCRIPTIONS = {

    "sad":
        "You seem to be feeling low or emotional.",

    "happy":
        "You seem to be in a positive and energetic mood.",

    "love":
        "You seem to be feeling romantic or affectionate.",

    "angry":
        "You seem to be feeling intense or frustrated.",

    "fear":
        "You seem to be feeling worried or uneasy.",

    "surprise":
        "You seem to be feeling excited or surprised."
}


if "songs" not in st.session_state:
    st.session_state["songs"] = []

if "emotion" not in st.session_state:
    st.session_state["emotion"] = ""

if "confidence" not in st.session_state:
    st.session_state["confidence"] = 0.0

if "shown_song_ids" not in st.session_state:
    st.session_state["shown_song_ids"] = set()

if "recommendation_count" not in st.session_state:
    st.session_state["recommendation_count"] = 0


st.title("Mood-Based Music Recommendation")

user_text = st.text_area(
    "How are you feeling?",
    height=120
)

language = st.selectbox(
    "Language",
    [
        "Both",
        "Hindi",
        "English"
    ]
)


col1, col2 = st.columns(2)

with col1:

    recommend = st.button(
        "Recommend Songs",
        use_container_width=True
    )

with col2:

    reset = st.button(
        "Reset",
        use_container_width=True
    )


if reset:

    st.session_state["songs"] = []

    st.session_state["emotion"] = ""

    st.session_state["confidence"] = 0

    st.session_state["shown_song_ids"] = set()

    st.session_state["recommendation_count"] = 0

    st.rerun()


if recommend:

    if not user_text.strip():

        st.warning(
            "Enter your feelings first."
        )

        st.stop()

    emotion, confidence = detect_emotion(
        user_text
    )

    st.session_state["emotion"] = emotion

    st.session_state["confidence"] = confidence

    songs = get_songs(
        emotion=emotion,
        language=language,
        limit=10,
        exclude_ids=st.session_state["shown_song_ids"]
    )

    st.session_state["songs"] = songs

    for song in songs:

        st.session_state["shown_song_ids"].add(
            song["id"]
        )

    st.session_state["recommendation_count"] += 1


if st.session_state["emotion"]:

    st.subheader("Emotion Analysis")

    st.write(
        f"Emotion: {st.session_state['emotion'].title()}"
    )

    st.write(
        f"Confidence: {st.session_state['confidence']:.1f}%"
    )

    st.info(
        EMOTION_DESCRIPTIONS.get(
            st.session_state["emotion"],
            ""
        )
    )


if st.session_state["songs"]:

    st.subheader(
        f"Recommendations for {st.session_state['emotion'].title()}"
    )

    for i, song in enumerate(
        st.session_state["songs"],
        start=1
    ):

        st.markdown(
            f"### {i}. {song['title']}"
        )

        st.write(
            f"Artist: {song['artist']}"
        )

        if song.get("artwork"):

            st.image(
                song["artwork"],
                width=250
            )

        st.video(
            song["stream_url"]
        )

        st.link_button(
            "Watch on YouTube",
            song["stream_url"]
        )

        st.divider()

elif st.session_state["emotion"]:

    st.error(
        "No recommendations found."
    )


