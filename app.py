import streamlit as st

from emotion_model import detect_emotion
from audius_api import get_songs


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


st.title(
    "Mood-Based Music Recommendation"
)

st.write(
    "Describe how you feel and get music recommendations based on your detected emotion."
)


with st.container():

    user_text = st.text_area(
        "How are you feeling?",
        placeholder=(
            "Example: I am feeling very sad "
            "because I miss someone today."
        ),
        height=130
    )


language = st.selectbox(
    "Choose music language",
    [
        "Both",
        "Hindi",
        "English"
    ]
)


col1, col2 = st.columns(
    [3, 1]
)


with col1:

    recommend_button = st.button(
        "Recommend Songs",
        type="primary",
        use_container_width=True
    )


with col2:

    reset_button = st.button(
        "Reset",
        use_container_width=True
    )


if reset_button:

    st.session_state["songs"] = []

    st.session_state["emotion"] = ""

    st.session_state["confidence"] = 0.0

    st.session_state["shown_song_ids"] = set()

    st.session_state["recommendation_count"] = 0

    st.rerun()


if recommend_button:

    if not user_text.strip():

        st.warning(
            "Please describe how you feel first."
        )

        st.stop()

    with st.spinner(
        "Analyzing your emotion..."
    ):

        try:

            emotion, confidence = detect_emotion(
                user_text.strip()
            )

        except Exception as error:

            st.error(
                "The emotion model could not be loaded."
            )

            st.exception(
                error
            )

            st.stop()

    st.session_state["emotion"] = emotion

    st.session_state["confidence"] = confidence

    with st.spinner(
        "Finding the best matching songs..."
    ):

        try:

            songs = get_songs(
                emotion=emotion,
                language=language,
                limit=10,
                exclude_ids=(
                    st.session_state["shown_song_ids"]
                )
            )

        except Exception as error:

            st.error(
                "Something went wrong while finding songs."
            )

            st.exception(
                error
            )

            st.stop()

    st.session_state["songs"] = songs

    for song in songs:

        song_id = str(
            song.get("id")
        )

        st.session_state["shown_song_ids"].add(
            song_id
        )

    st.session_state["recommendation_count"] += 1


if st.session_state["emotion"]:

    emotion = st.session_state["emotion"]

    confidence = st.session_state["confidence"]

    st.divider()

    st.subheader(
        "Emotion Analysis"
    )

    col1, col2, col3 = st.columns(
        3
    )

    with col1:

        st.metric(
            "Detected Emotion",
            emotion.title()
        )

    with col2:

        st.metric(
            "Confidence",
            f"{confidence:.1f}%"
        )

    with col3:

        st.metric(
            "Language",
            language
        )

    description = EMOTION_DESCRIPTIONS.get(
        emotion,
        "Your emotion was detected from the text."
    )

    st.info(
        description
    )


songs = st.session_state["songs"]


if songs:

    st.divider()

    st.subheader(
        f"Recommendations for "
        f"{st.session_state['emotion'].title()} Mood"
    )

    st.caption(
        "Recommendation set "
        f"#{st.session_state['recommendation_count']}"
    )

    for index, song in enumerate(songs):

        title = song.get(
            "title",
            "Unknown Track"
        )

        artist = song.get(
            "artist",
            "Unknown Artist"
        )

        artwork = song.get(
            "artwork"
        )

        genre = song.get(
            "genre",
            ""
        )

        mood = song.get(
            "mood",
            ""
        )

        stream_url = song.get(
            "stream_url"
        )

        audius_url = song.get(
            "audius_url"
        )

        col1, col2 = st.columns(
            [1, 4]
        )

        with col1:

            if artwork:

                st.image(
                    artwork,
                    use_container_width=True
                )

            else:

                st.write(
                    "No artwork"
                )

        with col2:

            st.markdown(
                f"### {index + 1}. {title}"
            )

            st.write(
                f"Artist: {artist}"
            )

            metadata = []

            if genre:
                metadata.append(
                    f"Genre: {genre}"
                )

            if mood:
                metadata.append(
                    f"Mood: {mood}"
                )

            if metadata:

                st.caption(
                    " | ".join(metadata)
                )

            if stream_url:

                st.audio(
                    stream_url
                )

            if audius_url:

                st.link_button(
                    "Open on Audius",
                    audius_url
                )

        st.divider()


elif (
    st.session_state["emotion"]
    and not songs
):

    st.warning(
        "No suitable songs were found for this combination. Try Both language or another mood description."
    )
