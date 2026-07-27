import requests
import streamlit as st


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
            "hindi aggressive",
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


def get_track_value(track, key, default=""):

    value = track.get(key)

    if value is None:
        return default

    return value


def get_artist(track):

    user = track.get("user")

    if isinstance(user, dict):

        name = user.get("name")

        if name:
            return name

    artists = track.get("artists")

    if isinstance(artists, list) and artists:

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

    if isinstance(artwork, str):

        return artwork

    return None


def get_stream_url(track_id):

    return (
        f"{BASE_URL}/tracks/"
        f"{track_id}/stream"
    )


def convert_track(track):

    track_id = track.get("id")

    if not track_id:
        return None

    title = get_track_value(
        track,
        "title",
        "Unknown Track"
    )

    artist = get_artist(track)

    genre = get_track_value(
        track,
        "genre",
        ""
    )

    mood = get_track_value(
        track,
        "mood",
        ""
    )

    artwork = get_artwork(track)

    permalink = get_track_value(
        track,
        "permalink",
        ""
    )

    if permalink:

        audius_url = (
            f"https://audius.co{permalink}"
            if permalink.startswith("/")
            else f"https://audius.co/{permalink}"
        )

    else:

        audius_url = "https://audius.co"

    play_count = get_track_value(
        track,
        "play_count",
        0
    )

    repost_count = get_track_value(
        track,
        "repost_count",
        0
    )

    favorite_count = get_track_value(
        track,
        "favorite_count",
        0
    )

    return {
        "id": track_id,
        "title": title,
        "artist": artist,
        "genre": genre,
        "mood": mood,
        "artwork": artwork,
        "stream_url": get_stream_url(track_id),
        "audius_url": audius_url,
        "play_count": play_count,
        "repost_count": repost_count,
        "favorite_count": favorite_count
    }


def score_track(track, emotion, language):

    score = 0

    title = track["title"].lower()
    artist = track["artist"].lower()
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

    for word in emotion_words.get(emotion, []):

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
            "india",
            "indian"
        ]

        for word in hindi_words:

            if word in title:
                score += 25

            if word in artist:
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

    play_count = track.get(
        "play_count",
        0
    )

    repost_count = track.get(
        "repost_count",
        0
    )

    favorite_count = track.get(
        "favorite_count",
        0
    )

    try:
        score += min(
            20,
            int(play_count) / 10000
        )
    except:
        pass

    try:
        score += min(
            10,
            int(repost_count) / 100
        )
    except:
        pass

    try:
        score += min(
            10,
            int(favorite_count) / 100
        )
    except:
        pass

    return score


@st.cache_data(ttl=1800)
def search_tracks(query, limit=10):

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

    results = []

    for track in tracks:

        converted = convert_track(
            track
        )

        if converted:
            results.append(
                converted
            )

    return results


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

    if language in ["Hindi", "Both"]:

        for query in searches["Hindi"]:

            results = search_tracks(
                query,
                limit=10
            )

            candidates.extend(
                results
            )

    if language in ["English", "Both"]:

        for query in searches["English"]:

            results = search_tracks(
                query,
                limit=10
            )

            candidates.extend(
                results
            )

    candidates = remove_duplicates(
        candidates
    )

    for song in candidates:

        song["score"] = score_track(
            song,
            emotion,
            language
        )

    candidates.sort(
        key=lambda x: x["score"],
        reverse=True
    )

    return candidates[:limit]
