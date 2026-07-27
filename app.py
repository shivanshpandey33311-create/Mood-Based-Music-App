import streamlit as st
from emotion_model import detect_emotion
from youtube_api import search_youtube

st.set_page_config(
    page_title="Mood-Based Music Recommendation",
    layout="centered"
)

st.title("Mood-Based Music Recommendation")

st.write("Tell me how you feel today.")

user_text = st.text_area(
    "Your feelings",
    placeholder="Example: I am feeling very sad today...",
    height=120
)

language = st.selectbox(
    "Choose music language",
    ["Both", "Hindi", "English"]
)

if st.button("Recommend Songs", type="primary"):

    if not user_text.strip():
        st.warning("Please tell me how you feel first.")
        st.stop()

    with st.spinner("Detecting your emotion..."):
        emotion, confidence = detect_emotion(user_text)

    st.session_state["emotion"] = emotion
    st.session_state["confidence"] = confidence

    st.session_state["songs"] = []

    st.success(
        f"Detected Emotion: {emotion.title()} "
        f"({confidence:.1f}% confidence)"
    )

    with st.spinner("Finding songs..."):

        songs = search_youtube(
            emotion=emotion,
            language=language,
            max_results=10
        )

    st.session_state["songs"] = songs

if "songs" in st.session_state and st.session_state["songs"]:

    st.subheader(
        f"Songs for {st.session_state['emotion'].title()} Mood"
    )

    for index, song in enumerate(st.session_state["songs"]):

        st.markdown(
            f"### {index + 1}. {song['title']}"
        )

        st.write(
            f"Channel: {song['channel']}"
        )

        st.video(
            song["video_url"]
        )

        st.divider()

elif "songs" in st.session_state and not st.session_state["songs"]:

    st.error(
        "No songs were found. Try another mood or language."
    )
