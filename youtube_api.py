import os
import random

from dotenv import load_dotenv
from googleapiclient.discovery import build

load_dotenv()

YOUTUBE_API_KEY = os.getenv("YOUTUBE_API_KEY")

EMOTION_QUERIES = {
    "happy": [
        "happy songs",
        "feel good songs",
        "party songs",
        "upbeat music",
        "dance hits"
    ],
    "sad": [
        "sad songs",
        "heartbreak songs",
        "emotional songs",
        "sad bollywood songs",
        "lonely songs"
    ],
    "love": [
        "romantic songs",
        "love songs",
        "bollywood love songs",
        "romantic hits",
        "english love songs"
    ],
    "angry": [
        "rock songs",
        "rap songs",
        "hard rock",
        "metal songs",
        "power songs"
    ],
    "fear": [
        "calm music",
        "relaxing songs",
        "peaceful music",
        "lofi",
        "meditation music"
    ],
    "surprise": [
        "trending songs",
        "viral songs",
        "energetic songs",
        "dance songs",
        "party hits"
    ]
}


def get_youtube():
    return build(
        "youtube",
        "v3",
        developerKey=YOUTUBE_API_KEY
    )


def get_songs(
    emotion,
    language="Both",
    limit=10,
    exclude_ids=None
):
    youtube = get_youtube()

    exclude_ids = set(exclude_ids or [])

    queries = EMOTION_QUERIES.get(
        emotion,
        EMOTION_QUERIES["happy"]
    ).copy()

    random.shuffle(queries)

    songs = []
    seen = set(exclude_ids)

    for query in queries:

        if language == "Hindi":
            search = f"{query} hindi"

        elif language == "English":
            search = f"{query} english"

        else:
            search = query

        response = youtube.search().list(
            part="snippet",
            q=search,
            type="video",
            videoCategoryId="10",
            maxResults=10
        ).execute()

        items = response.get("items", [])

        random.shuffle(items)

        for item in items:

            video_id = item["id"]["videoId"]

            if video_id in seen:
                continue

            seen.add(video_id)

            snippet = item["snippet"]

            songs.append(
                {
                    "id": video_id,
                    "title": snippet["title"],
                    "artist": snippet["channelTitle"],
                    "genre": "",
                    "mood": emotion,
                    "artwork": snippet["thumbnails"]["high"]["url"],
                    "stream_url": f"https://www.youtube.com/watch?v={video_id}",
                    "audius_url": f"https://www.youtube.com/watch?v={video_id}"
                }
            )

            if len(songs) >= limit:
                random.shuffle(songs)
                return songs

    random.shuffle(songs)

    return songs
