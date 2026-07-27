import random
import re



EMOTION_CONFIG = {

    "sad": {
        "moods": [
            "Melancholy",
            "Sentimental",
            "Yearning"
        ],
        "keywords": [
            "sad",
            "emotional",
            "heartbreak",
            "heart broken",
            "melancholy",
            "alone",
            "lonely",
            "pain",
            "cry",
            "tears",
            "broken",
            "memories"
        ],
        "genres": [
            "Pop",
            "R&B/Soul",
            "Acoustic",
            "Lo-Fi",
            "Ambient"
        ],
        "queries": [
            "sad",
            "emotional",
            "heartbreak",
            "melancholy",
            "sad song",
            "broken heart",
            "lonely"
        ]
    },

    "happy": {
        "moods": [
            "Upbeat",
            "Excited",
            "Energizing",
            "Empowering"
        ],
        "keywords": [
            "happy",
            "happiness",
            "joy",
            "party",
            "fun",
            "upbeat",
            "good mood",
            "feel good",
            "dance",
            "celebration",
            "positive"
        ],
        "genres": [
            "Pop",
            "Dancehall",
            "House",
            "Disco",
            "Funk",
            "Hip-Hop/Rap"
        ],
        "queries": [
            "happy",
            "upbeat",
            "feel good",
            "party",
            "joy",
            "dance",
            "good vibes"
        ]
    },

    "love": {
        "moods": [
            "Romantic",
            "Tender",
            "Sensual",
            "Yearning"
        ],
        "keywords": [
            "love",
            "romantic",
            "romance",
            "lover",
            "heart",
            "darling",
            "kiss",
            "relationship",
            "valentine",
            "tender"
        ],
        "genres": [
            "Pop",
            "R&B/Soul",
            "Acoustic"
        ],
        "queries": [
            "love",
            "romantic",
            "romance",
            "love song",
            "lover",
            "heart"
        ]
    },

    "angry": {
        "moods": [
            "Aggressive",
            "Fiery",
            "Defiant",
            "Rowdy",
            "Gritty"
        ],
        "keywords": [
            "angry",
            "rage",
            "aggressive",
            "fight",
            "revenge",
            "intense",
            "hard",
            "power",
            "fire",
            "strong"
        ],
        "genres": [
            "Rock",
            "Metal",
            "Hip-Hop/Rap",
            "Trap",
            "Hardstyle"
        ],
        "queries": [
            "angry",
            "aggressive",
            "rage",
            "intense",
            "hard",
            "power"
        ]
    },

    "fear": {
        "moods": [
            "Peaceful",
            "Easygoing",
            "Cool",
            "Serious"
        ],
        "keywords": [
            "calm",
            "peaceful",
            "relax",
            "relaxing",
            "chill",
            "ambient",
            "soft",
            "quiet",
            "meditation"
        ],
        "genres": [
            "Ambient",
            "Lo-Fi",
            "Acoustic",
            "Classical",
            "Downtempo"
        ],
        "queries": [
            "calm",
            "peaceful",
            "relaxing",
            "chill",
            "ambient",
            "meditation"
        ]
    },

    "surprise": {
        "moods": [
            "Excited",
            "Energizing",
            "Upbeat",
            "Stirring"
        ],
        "keywords": [
            "surprise",
            "excited",
            "energetic",
            "upbeat",
            "dance",
            "party",
            "power",
            "amazing"
        ],
        "genres": [
            "Pop",
            "Electronic",
            "House",
            "Dancehall",
            "Hip-Hop/Rap"
        ],
        "queries": [
            "excited",
            "energetic",
            "upbeat",
            "dance",
            "party",
            "amazing"
        ]
    }
}


LANGUAGE_TERMS = {

    "Hindi": [
        "hindi",
        "bollywood",
        "indian",
        "india",
        "desi",
        "bhangra",
        "punjabi",
        "filmi"
    ],

    "English": [
        "english",
        "pop",
        "rock",
        "indie",
        "r&b",
        "hip hop",
        "rap"
    ]
}


def safe_text(value):

    if value is None:
        return ""

    if isinstance(value, list):

        return " ".join(
            str(item)
            for item in value
        ).lower()

    if isinstance(value, dict):

        return " ".join(
            str(item)
            for item in value.values()
        ).lower()

    return str(value).lower()


def normalize_text(value):

    value = safe_text(value)

    value = re.sub(
        r"[^a-z0-9\s]",
        " ",
        value
    )

    value = re.sub(
        r"\s+",
        " ",
        value
    )

    return value.strip()


def api_request(endpoint, params=None):

    try:

        response = requests.get(
            f"{BASE_URL}{endpoint}",
            params=params,
            timeout=REQUEST_TIMEOUT
        )

        response.raise_for_status()

        data = response.json()

        if not isinstance(data, dict):
            return None

        return data

    except (
        requests.RequestException,
        ValueError
    ):

        return None


def get_artist_name(track):

    user = track.get("user")

    if isinstance(user, dict):

        name = user.get("name")

        if name:
            return str(name)

    artists = track.get("artists")

    if isinstance(artists, list):

        names = []

        for artist in artists:

            if isinstance(artist, dict):

                name = artist.get("name")

                if name:
                    names.append(
                        str(name)
                    )

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
            or artwork.get("_1000x1000")
            or artwork.get("_480x480")
            or artwork.get("_150x150")
        )

    if isinstance(artwork, str):
        return artwork

    return None


def build_stream_url(track_id):

    return (
        f"{BASE_URL}/tracks/"
        f"{track_id}/stream"
    )


def build_audius_url(permalink):

    permalink = str(
        permalink or ""
    ).strip()

    if not permalink:
        return "https://audius.co"

    if permalink.startswith("http"):
        return permalink

    if permalink.startswith("/"):
        return (
            f"https://audius.co{permalink}"
        )

    return (
        f"https://audius.co/{permalink}"
    )


def convert_track(track):

    if not isinstance(track, dict):
        return None

    track_id = track.get("id")

    if not track_id:
        return None

    is_streamable = track.get(
        "is_streamable"
    )

    if is_streamable is None:
        is_streamable = track.get(
            "isStreamable"
        )

    if is_streamable is False:
        return None

    title = (
        track.get("title")
        or "Unknown Track"
    )

    artist = get_artist_name(
        track
    )

    genre = (
        track.get("genre")
        or ""
    )

    mood = (
        track.get("mood")
        or ""
    )

    tags = track.get(
        "tags"
    ) or ""

    description = (
        track.get("description")
        or ""
    )

    permalink = track.get(
        "permalink"
    )

    play_count = (
        track.get("play_count")
        or track.get("playCount")
        or 0
    )

    favorite_count = (
        track.get("favorite_count")
        or track.get("favoriteCount")
        or 0
    )

    repost_count = (
        track.get("repost_count")
        or track.get("repostCount")
        or 0
    )

    duration = (
        track.get("duration")
        or 0
    )

    return {

        "id": str(track_id),

        "title": str(title),

        "artist": str(artist),

        "genre": str(genre),

        "mood": str(mood),

        "tags": safe_text(tags),

        "description": str(
            description
        ),

        "artwork": get_artwork(
            track
        ),

        "stream_url": build_stream_url(
            track_id
        ),

        "audius_url": build_audius_url(
            permalink
        ),

        "play_count": safe_number(
            play_count
        ),

        "favorite_count": safe_number(
            favorite_count
        ),

        "repost_count": safe_number(
            repost_count
        ),

        "duration": safe_number(
            duration
        )
    }


def safe_number(value):

    try:
        return float(value)

    except (
        ValueError,
        TypeError
    ):

        return 0.0


def search_tracks(
    query,
    offset=0,
    limit=CANDIDATES_PER_QUERY,
    sort_method="relevant"
):

    params = {

        "query": query,

        "offset": offset,

        "limit": limit,

        "sort_method": sort_method
    }

    data = api_request(
        "/tracks/search",
        params
    )

    if not data:
        return []

    tracks = data.get(
        "data",
        []
    )

    if not isinstance(
        tracks,
        list
    ):
        return []

    songs = []

    for track in tracks:

        song = convert_track(
            track
        )

        if song:
            songs.append(song)

    return songs


def remove_duplicates(
    songs
):

    unique = {}

    for song in songs:

        song_id = str(
            song.get("id")
        )

        if song_id:
            unique[song_id] = song

    return list(
        unique.values()
    )


def get_search_queries(
    emotion,
    language
):

    config = EMOTION_CONFIG.get(
        emotion,
        EMOTION_CONFIG["happy"]
    )

    queries = []

    emotion_queries = list(
        config["queries"]
    )

    random.shuffle(
        emotion_queries
    )

    if language == "Both":

        for query in emotion_queries:

            queries.append(
                f"{query} hindi"
            )

            queries.append(
                f"{query} english"
            )

    else:

        terms = LANGUAGE_TERMS.get(
            language,
            []
        )

        language_term = random.choice(
            terms
        )

        for query in emotion_queries:

            queries.append(
                f"{query} {language_term}"
            )

    random.shuffle(
        queries
    )

    return queries


def keyword_score(
    song,
    emotion
):

    config = EMOTION_CONFIG.get(
        emotion,
        EMOTION_CONFIG["happy"]
    )

    title = normalize_text(
        song.get("title")
    )

    artist = normalize_text(
        song.get("artist")
    )

    genre = normalize_text(
        song.get("genre")
    )

    mood = normalize_text(
        song.get("mood")
    )

    tags = normalize_text(
        song.get("tags")
    )

    description = normalize_text(
        song.get("description")
    )

    score = 0.0

    for word in config[
        "keywords"
    ]:

        word = normalize_text(
            word
        )

        if not word:
            continue

        if word in title:
            score += 35

        if word in tags:
            score += 22

        if word in description:
            score += 12

        if word in artist:
            score += 5

    for mood_name in config[
        "moods"
    ]:

        mood_name = normalize_text(
            mood_name
        )

        if mood_name == mood:
            score += 65

        elif mood_name in mood:
            score += 45

    for genre_name in config[
        "genres"
    ]:

        genre_name = normalize_text(
            genre_name
        )

        if genre_name == genre:
            score += 28

        elif genre_name in genre:
            score += 18

    return score


def language_score(
    song,
    language
):

    if language == "Both":
        return 0.0

    title = normalize_text(
        song.get("title")
    )

    artist = normalize_text(
        song.get("artist")
    )

    genre = normalize_text(
        song.get("genre")
    )

    tags = normalize_text(
        song.get("tags")
    )

    description = normalize_text(
        song.get("description")
    )

    searchable = " ".join([
        title,
        artist,
        genre,
        tags,
        description
    ])

    score = 0.0

    terms = LANGUAGE_TERMS.get(
        language,
        []
    )

    for term in terms:

        term = normalize_text(
            term
        )

        if term in searchable:
            score += 25

    return score


def popularity_score(
    song
):

    plays = safe_number(
        song.get("play_count")
    )

    favorites = safe_number(
        song.get("favorite_count")
    )

    reposts = safe_number(
        song.get("repost_count")
    )

    score = 0.0

    if plays > 0:

        score += min(
            20,
            5 * (
                plays / 10000
            ) ** 0.5
        )

    if favorites > 0:

        score += min(
            10,
            3 * (
                favorites / 100
            ) ** 0.5
        )

    if reposts > 0:

        score += min(
            5,
            2 * (
                reposts / 50
            ) ** 0.5
        )

    return score


def duration_score(
    song
):

    duration = safe_number(
        song.get("duration")
    )

    if duration <= 0:
        return 0

    if 60 <= duration <= 600:
        return 5

    if 30 <= duration <= 900:
        return 2

    return 0


def calculate_score(
    song,
    emotion,
    language
):

    score = 0.0

    score += keyword_score(
        song,
        emotion
    )

    score += language_score(
        song,
        language
    )

    score += popularity_score(
        song
    )

    score += duration_score(
        song
    )

    score += random.uniform(
        0,
        15
    )

    return score


def artist_diversity(
    songs,
    limit
):

    selected = []

    artist_count = {}

    remaining = list(
        songs
    )

    random.shuffle(
        remaining
    )

    while remaining and len(
        selected
    ) < limit:

        best_index = None

        best_score = None

        for index, song in enumerate(
            remaining
        ):

            artist = str(
                song.get(
                    "artist",
                    "Unknown Artist"
                )
            ).lower()

            count = artist_count.get(
                artist,
                0
            )

            score = song.get(
                "recommendation_score",
                0
            )

            if count == 0:
                score += 20

            elif count == 1:
                score += 5

            else:
                score -= count * 15

            if (
                best_score is None
                or score > best_score
            ):

                best_score = score

                best_index = index

        song = remaining.pop(
            best_index
        )

        artist = str(
            song.get(
                "artist",
                "Unknown Artist"
            )
        ).lower()

        artist_count[
            artist
        ] = artist_count.get(
            artist,
            0
        ) + 1

        selected.append(
            song
        )

    return selected


def get_songs(
    emotion,
    language="Both",
    limit=10,
    exclude_ids=None
):

    emotion = normalize_text(
        emotion
    )

    if emotion not in EMOTION_CONFIG:

        emotion = "happy"

    if language not in [
        "Hindi",
        "English",
        "Both"
    ]:

        language = "Both"

    exclude_ids = set(
        str(x)
        for x in (
            exclude_ids
            or set()
        )
    )

    queries = get_search_queries(
        emotion,
        language
    )

    candidates = []

    used_queries = set()

    for query in queries:

        if query in used_queries:
            continue

        used_queries.add(
            query
        )

        offsets = list(
            range(
                0,
                MAX_PAGES_PER_QUERY * 50,
                50
            )
        )

        random.shuffle(
            offsets
        )

        for offset in offsets:

            results = search_tracks(
                query=query,
                offset=offset,
                limit=CANDIDATES_PER_QUERY,
                sort_method="relevant"
            )

            candidates.extend(
                results
            )

            if len(candidates) >= 400:
                break

        if len(candidates) >= 400:
            break

    candidates = remove_duplicates(
        candidates
    )

    if exclude_ids:

        fresh = [
            song
            for song in candidates
            if str(
                song.get("id")
            ) not in exclude_ids
        ]

        if len(fresh) >= limit:

            candidates = fresh

        elif fresh:

            candidates = fresh

        else:

            candidates = [
                song
                for song in candidates
                if str(
                    song.get("id")
                ) not in exclude_ids
            ]

    if not candidates:
        return []

    for song in candidates:

        song[
            "recommendation_score"
        ] = calculate_score(
            song,
            emotion,
            language
        )

    candidates.sort(
        key=lambda song:
            song.get(
                "recommendation_score",
                0
            ),
        reverse=True
    )

    pool_size = min(
        len(candidates),
        max(
            limit * 5,
            50
        )
    )

    pool = candidates[
        :pool_size
    ]

    selected = artist_diversity(
        pool,
        limit
    )

    random.shuffle(
        selected
    )

    for song in selected:

        song.pop(
            "recommendation_score",
            None
        )

    return selected
