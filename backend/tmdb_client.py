"""
tmdb_client.py

Dieses Modul stellt Funktionen zur Verfügung, um Filmdaten (z. B. Poster) über die TMDb API abzurufen.
Der TMDb API-Key wird aus der .env-Datei geladen.
"""

import os
import requests
from dotenv import load_dotenv

# Lade Umgebungsvariablen aus der .env-Datei
load_dotenv()

TMDB_API_KEY = os.getenv("TMDB_API_KEY")
TMDB_BASE_URL = "https://api.themoviedb.org/3"
TMDB_IMAGE_BASE_URL = "https://image.tmdb.org/t/p/w500"

def fetch_movie_poster(movie_title: str) -> str:
    """
    Ruft für einen gegebenen Filmtitel über die TMDb API den Poster-Link ab.

    Args:
        movie_title (str): Der Titel des Films.

    Returns:
        str: Die vollständige URL des Filmposters, oder einen leeren String, wenn kein Poster gefunden wurde.

    Raises:
        ValueError: Falls der TMDB_API_KEY nicht gesetzt ist.
        requests.HTTPError: Bei HTTP-Fehlern während der Anfrage.
    """
    if not TMDB_API_KEY:
        raise ValueError("TMDB_API_KEY ist nicht in den Umgebungsvariablen gesetzt.")
        
    url = f"{TMDB_BASE_URL}/search/movie"
    params = {
        "api_key": TMDB_API_KEY,
        "query": movie_title
    }
    response = requests.get(url, params=params)
    response.raise_for_status()
    data = response.json()
    
    results = data.get("results")
    if results and len(results) > 0:
        poster_path = results[0].get("poster_path")
        if poster_path:
            return f"{TMDB_IMAGE_BASE_URL}{poster_path}"
    return "https://images.unsplash.com/photo-1536440136628-849c177e76a1?q=80&w=1325&auto=format&fit=crop&ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D"
