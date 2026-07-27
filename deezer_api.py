import requests
import streamlit as st


def get_query(emotion, language):

    queries = {

        "sad": {
            "Hindi": "Hindi Bollywood sad songs",
            "English": "English sad songs",
            "Both": "Hindi Bollywood sad songs English sad songs"
        },

        "happy": {
            "Hindi": "Hindi Bollywood happy songs",
            "English": "English happy songs",
            "Both": "Hindi Bollywood happy songs English happy songs"
        },

        "love": {
            "Hindi": "Hindi Bollywood romantic love songs",
            "English": "English romantic love songs",
            "Both": "Hindi Bollywood romantic songs English romantic songs"
        },

        "angry": {
            "Hindi": "Hindi Bollywood energetic songs",
            "English": "English energetic intense songs",
            "Both": "Hindi energetic songs English intense songs"
        },

        "fear": {
            "Hindi": "Hindi calming peaceful songs",
            "English": "English calming peaceful songs",
            "Both": "Hindi calming songs English calming songs"
        },

        "surprise": {
            "Hindi": "Hindi Bollywood energetic songs",
            "English": "English energetic songs",
            "Both": "Hindi energetic songs English energetic songs"
        }
    }

    return queries.get(
        emotion,
        queries["happy"]
    ).get(
        language,
        queries["happy"]["Both"]
    )


def search_youtube(
    emotion,
    language="Both",
    max_results=10
):

    api_key = st.secrets["YOUTUBE_API_KEY"]

    query = get_query(
        emotion,
        language
    )

    url = "https://www.googleapis.com/youtube/v3/search"

    params = {
        "part": "snippet",
        "q": query,
        "type": "video",
        "videoCategoryId": "10",
        "maxResults": max_results,
        "key": api_key
    }

    try:

        response = requests.get(
            url,
            params=params,
            timeout=15
        )

        if response.status_code != 200:
            return []

        data = response.json()

        songs = []

        for item in data.get("items", []):

            video_id = item["id"].get("videoId")

            if not video_id:
                continue

            songs.append({
                "title": item["snippet"]["title"],
                "channel": item["snippet"]["channelTitle"],
                "video_id": video_id,
                "video_url": (
                    f"https://www.youtube.com/watch?v={video_id}"
                )
            })

        return songs

    except requests.RequestException:

        return []
