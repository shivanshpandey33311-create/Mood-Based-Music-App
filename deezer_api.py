import requests

def get_songs(mood, limit=10):
    url = "https://api.deezer.com/search"

    params = {
        "q": mood,
    }

    response = requests.get(url, params=params)

    if response.status_code != 200:
        return []

    data = response.json()

    songs = []

    for track in data["data"][:limit]:
        songs.append({
            "title": track["title"],
            "artist": track["artist"]["name"],
            "album": track["album"]["title"],
            "cover": track["album"]["cover_medium"],
            "preview": track["preview"],
        })

    return songs
