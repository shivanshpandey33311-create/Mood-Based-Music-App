import requests
import streamlit as st
import random


BASE_URL = "https://api.audius.co/v1"


MOOD_SEARCHES = {
    "sad": {
        "Hindi": [
            "hindi sad",
            "bollywood sad",
            "hindi emotional",
            "hindi heartbreak"
        ],
        "English": [
            "english sad",
            "sad emotional",
            "heartbreak",
            "melancholy"
        ]
    },
    "happy": {
        "Hindi": [
            "hindi happy",
            "bollywood happy",
            "hindi party",
            "hindi feel good"
        ],
        "English": [
            "english happy",
            "feel good",
            "happy pop",
            "party"
        ]
    },
    "love": {
        "Hindi": [
            "hindi love",
            "hindi romantic",
            "bollywood romantic",
            "hindi romance"
        ],
        "English": [
            "english love",
            "romantic",
            "love songs",
            "romantic pop"
        ]
    },
    "angry": {
        "Hindi": [
            "hindi angry",
            "hindi energetic",
            "bollywood energetic"
        ],
        "English": [
            "angry",
            "aggressive",
            "intense",
            "energetic"
        ]
    },
    "fear": {
        "Hindi": [
            "hindi calm",
            "hindi relaxing",
            "hindi peaceful",
            "hindi ambient"
        ],
        "English": [
            "calm",
            "relaxing",
            "peaceful",
            "ambient"
        ]
    },
    "surprise": {
        "Hindi": [
            "hindi energetic",
            "hindi party",
            "bollywood party",
            "hindi upbeat"
        ],
        "English": [
            "energetic",
            "party",
            "upbeat",
            "dance"
        ]
    }
}


def make_request(endpoint, params=None):

    try:

        response = requests.get(
            f"{BASE_URL}{endpoint}",
            params=params,
            timeout=15
        )

        response.raise_for_status()

        return response.json()

    except requests.RequestException:

        return None


def get_artist(track):

    user = track.get("user")

    if isinstance(user, dict):

        name = user.get("name")

        if name:
            return name

    artists = track.get("artists")

    if isinstance(artists, list):

        names = []

        for artist in artists:

            if isinstance(artist, dict):

                name = artist.get("name")

                if name:
                    names.append(name)

        if names:
            return ", ".join(names)

    return "Unknown Artist"


def get_artwork(track):

    artwork = track.get("artwork")

    if isinstance(artwork, dict):

        return (
            artwork.get("1000x1000")
            or artwork.get("480x480")
            or artwork.get("150x150")
        )

    return None


def convert_track(track):

    track_id = track.get("id")

    if not track_id:
        return None

    permalink = track.get(
        "permalink",
        ""
    )

    if permalink:

        if permalink.startswith("/"):
            audius_url = (
                f"https://audius.co{permalink}"
            )
        else:
            audius_url = (
                f"https://audius.co/{permalink}"
            )

    else:

        audius_url = "https://audius.co"

    return {
        "id": track_id,
        "title": track.get(
            "title",
            "Unknown Track"
        ),
        "artist": get_artist(track),
        "genre": track.get(
            "genre",
            ""
        ),
        "mood": track.get(
            "mood",
            ""
        ),
        "artwork": get_artwork(track),
        "stream_url": (
            f"{BASE_URL}/tracks/"
            f"{track_id}/stream"
        ),
        "audius_url": audius_url,
        "play_count": track.get(
            "play_count",
            0
        ),
        "repost_count": track.get(
            "repost_count",
            0
        ),
        "favorite_count": track.get(
            "favorite_count",
            0
        )
    }


def search_tracks(query, limit=50):

    params = {
        "query": query,
        "limit": limit,
        "sort_method": "popular"
    }

    data = make_request(
        "/tracks/search",
        params
    )

    if not data:
        return []

    tracks = data.get(
        "data",
        []
    )

    songs = []

    for track in tracks:

        song = convert_track(track)

        if song:
            songs.append(song)

    return songs


def remove_duplicates(songs):

    seen = set()
    unique = []

    for song in songs:

        key = (
            song["title"].lower(),
            song["artist"].lower()
        )

        if key in seen:
            continue

        seen.add(key)
        unique.append(song)

    return unique


def score_track(
    track,
    emotion,
    language
):

    score = 0

    title = track["title"].lower()
    genre = track["genre"].lower()
    mood = track["mood"].lower()

    emotion_words = {

        "sad": [
            "sad",
            "emotional",
            "heartbreak",
            "melancholy",
            "alone"
        ],

        "happy": [
            "happy",
            "party",
            "upbeat",
            "feel good",
            "fun"
        ],

        "love": [
            "love",
            "romantic",
            "romance",
            "heart"
        ],

        "angry": [
            "angry",
            "aggressive",
            "intense",
            "rage",
            "hard"
        ],

        "fear": [
            "calm",
            "peaceful",
            "relax",
            "ambient",
            "chill"
        ],

        "surprise": [
            "energetic",
            "party",
            "upbeat",
            "dance"
        ]
    }

    for word in emotion_words.get(
        emotion,
        []
    ):

        if word in title:
            score += 25

        if word in genre:
            score += 15

        if word in mood:
            score += 30

    if language == "Hindi":

        hindi_words = [
            "hindi",
            "bollywood",
            "indian",
            "india"
        ]

        for word in hindi_words:

            if word in title:
                score += 20

            if word in genre:
                score += 10

    elif language == "English":

        english_words = [
            "english",
            "pop",
            "rock",
            "hip hop",
            "r&b"
        ]

        for word in english_words:

            if word in title:
                score += 10

            if word in genre:
                score += 10

    return score


def get_songs(
    emotion,
    language="Both",
    limit=10
):

    searches = MOOD_SEARCHES.get(
        emotion,
        MOOD_SEARCHES["happy"]
    )

    candidates = []

    queries = []

    if language in [
        "Hindi",
        "Both"
    ]:

        queries.extend(
            searches["Hindi"]
        )

    if language in [
        "English",
        "Both"
    ]:

        queries.extend(
            searches["English"]
        )

    random.shuffle(queries)

    for query in queries:

        results = search_tracks(
            query,
            limit=50
        )

        candidates.extend(
            results
        )

    candidates = remove_duplicates(
        candidates
    )

    if not candidates:
        return []

    scored = []

    for song in candidates:

        score = score_track(
            song,
            emotion,
            language
        )

        song["score"] = score

        scored.append(song)

    scored.sort(
        key=lambda x: x["score"],
        reverse=True
    )

    strong_matches = [
        song
        for song in scored
        if song["score"] >= 10
    ]

    if len(strong_matches) < limit:
        strong_matches = scored

    random.shuffle(
        strong_matches
    )

    selected = strong_matches[:limit]

    selected.sort(
        key=lambda x: x["score"],
        reverse=True
    )

    return selected
