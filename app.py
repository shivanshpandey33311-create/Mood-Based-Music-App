import streamlit as st
from emotion_model import detect_emotion
from audius_api import get_songs

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

    with st.spinner("Finding songs..."):
        songs = get_songs(
            emotion=emotion,
            language=language,
            limit=10
        )

    st.session_state["songs"] = songs

    if not songs:
        st.error(
            "No matching songs were found. Try another mood or language."
        )
        st.stop()


if "emotion" in st.session_state:

    st.success(
        f"Detected Emotion: {st.session_state['emotion'].title()} "
        f"({st.session_state['confidence']:.1f}% confidence)"
    )


if "songs" in st.session_state and st.session_state["songs"]:

    st.subheader(
        f"Recommended Songs for "
        f"{st.session_state['emotion'].title()} Mood"
    )

    for index, song in enumerate(st.session_state["songs"]):

        st.markdown(
            f"### {index + 1}. {song['title']}"
        )

        st.write(
            f"Artist: {song['artist']}"
        )

        if song["genre"]:
            st.write(
                f"Genre: {song['genre']}"
            )

        if song["mood"]:
            st.write(
                f"Song Mood: {song['mood']}"
            )

        if song["artwork"]:
            st.image(
                song["artwork"],
                width=220
            )

        if song["stream_url"]:
            st.audio(
                song["stream_url"],
                format="audio/mpeg"
            )

        if song["audius_url"]:
            st.link_button(
                "Open on Audius",
                song["audius_url"]
            )

        st.divider()
