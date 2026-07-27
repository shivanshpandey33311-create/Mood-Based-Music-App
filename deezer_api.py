import requests


def search_deezer(query, limit=10):
    url = "https://api.deezer.com/search"

    params = {
        "q": query,
        "limit": limit
    }

    try:
        response = requests.get(
            url,
            params=params,
            timeout=10
        )

        if response.status_code != 200:
            return []

        data = response.json()

        songs = []

        for track in data.get("data", []):

            songs.append({
                "title": track.get("title", "Unknown"),
                "artist": track.get("artist", {}).get(
                    "name",
                    "Unknown"
                ),
                "album": track.get("album", {}).get(
                    "title",
                    "Unknown"
                ),
                "cover": track.get(
                    "album",
                    {}
                ).get(
                    "cover_medium"
                ),
                "preview": track.get("preview"),
                "link": track.get("link")
            })

        return songs

    except requests.RequestException:
        return []


def get_songs(mood, language="Both", limit=10):

    if language == "Hindi":

        query = f"Hindi Bollywood {mood} songs"

        return search_deezer(
            query,
            limit
        )

    if language == "English":

        query = f"English {mood} songs"

        return search_deezer(
            query,
            limit
        )

    hindi_songs = search_deezer(
        f"Hindi Bollywood {mood} songs",
        5
    )

    english_songs = search_deezer(
        f"English {mood} songs",
        5
    )

    return hindi_songs + english_songs
