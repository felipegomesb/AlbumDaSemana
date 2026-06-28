import base64

import requests
from django.conf import settings


def get_access_token():
    client_id = settings.SPOTIFY_CLIENT_ID
    client_secret = settings.SPOTIFY_CLIENT_SECRET

    if not client_id or not client_secret:
        return None

    credentials = base64.b64encode(f"{client_id}:{client_secret}".encode()).decode()

    response = requests.post(
        "https://accounts.spotify.com/api/token",
        headers={
            "Authorization": f"Basic {credentials}",
            "Content-Type": "application/x-www-form-urlencoded",
        },
        data={"grant_type": "client_credentials"},
        timeout=10,
    )

    if response.status_code == 200:
        return response.json().get("access_token")
    return None


def search_spotify(query, search_type="track", limit=10):
    token = get_access_token()
    if not token:
        return None

    response = requests.get(
        "https://api.spotify.com/v1/search",
        headers={"Authorization": f"Bearer {token}"},
        params={"q": query, "type": search_type, "limit": limit},
        timeout=10,
    )

    if response.status_code == 200:
        return response.json()
    return None


def get_album_tracks(album_spotify_id):
    token = get_access_token()
    if not token:
        return None

    response = requests.get(
        f"https://api.spotify.com/v1/albums/{album_spotify_id}/tracks",
        headers={"Authorization": f"Bearer {token}"},
        params={"limit": 50},
        timeout=10,
    )

    if response.status_code == 200:
        return response.json()
    return None
