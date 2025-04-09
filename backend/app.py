"""
app.py

Dieses Modul initialisiert die FastAPI-Anwendung und definiert die API-Endpunkte
zur Bereitstellung von Filmdaten und Filmempfehlungen.
"""

import os
import json
from fastapi import FastAPI, Path, Query, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from starlette import status
import pandas as pd

from data_loader import load_movie_data
from recommender import MovieRecommender
from tmdb_client import fetch_movie_poster

# Initialisiere die FastAPI-Anwendung
app = FastAPI(
    title="Movie Recommendation API",
    description="Empfiehlt Filme basierend auf TF-IDF, Cosine Similarity und liefert passende Filmposter über TMDb",
    version="1.0"
)

# Erlaube Zugriff (CORS) – Nur zum Testen! Im Produktionsbetrieb sollte dies eingeschränkt werden!
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Definiere den Pfad zur CSV-Datei (relativ zu diesem Skript)
csv_path = os.path.join(os.path.dirname(__file__), "data", "tmdb_5000_movies.csv")

# Lade die Filmdaten
try:
    df = load_movie_data(csv_path)
except Exception as e:
    raise RuntimeError(f"Fehler beim Laden der Filmdaten: {e}")

# Entferne ungültige Werte für eine sichere JSON-Ausgabe und erzeuge einen Auszug
safe_df_excerpt = df.head(12).replace([float("inf"), float("-inf")], pd.NA).fillna("N/A")
data_excerpt = json.loads(safe_df_excerpt.to_json(orient="records"))

# Initialisiere den MovieRecommender
recommender = MovieRecommender(df)

def enrich_movie_with_poster(movie_dict: dict) -> dict:
    """
    Ergänzt ein Film-Dictionary um den Poster-Link, sofern verfügbar.

    Args:
        movie_dict (dict): Ein Dictionary mit Filmdaten (muss den Schlüssel 'title' enthalten).

    Returns:
        dict: Das Film-Dictionary, ergänzt um den Schlüssel 'poster', falls ein Poster-Link gefunden wurde.
    """
    title = movie_dict.get("title", "")
    try:
        poster_url = fetch_movie_poster(title)
        movie_dict["poster"] = poster_url if poster_url else ""
    except Exception as e:
        # Bei Fehlern wird ein Standard Poster geladen
        movie_dict["poster"] = "https://images.unsplash.com/photo-1536440136628-849c177e76a1?q=80&w=1325&auto=format&fit=crop&ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D"
    return movie_dict

@app.get("/", status_code=status.HTTP_200_OK)
def read_all_movies():
    """
    Liefert die ersten 12 Filme als JSON-Liste.

    Returns:
        list: Eine Liste von Dictionaries mit den Details der ersten 12 Filme.
    """
    # Um Poster in diesem Auszug einzufügen, wird jedes Film-Dict erweitert:
    enriched = [enrich_movie_with_poster(movie) for movie in data_excerpt]
    return enriched

@app.get("/movies/{movie_id}", status_code=status.HTTP_200_OK)
def read_movie_by_id(movie_id: int = Path(..., gt=0, description="Die ID des zu suchenden Films")):
    """
    Liefert einen Film anhand der übergebenen Film-ID.

    Args:
        movie_id (int): Die eindeutige ID des Films.

    Returns:
        dict: Ein Dictionary mit den Filmdetails (inklusive Poster).

    Raises:
        HTTPException: Falls der Film nicht gefunden wird (404).
    """
    movie = df[df["id"] == movie_id]
    if not movie.empty:
        clean_movie = movie.replace([float("inf"), float("-inf")], pd.NA).fillna("N/A")
        movie_dict = clean_movie.to_dict(orient='records')[0]
        return enrich_movie_with_poster(movie_dict)
    raise HTTPException(status_code=404, detail="Movie not found")


@app.get("/movies", status_code=status.HTTP_200_OK)
def read_movie_by_title(movie_title: str = Query(..., description="Der Titel des zu suchenden Films")):
    """
    Liefert einen Film anhand des übergebenen Titels.

    Args:
        movie_title (str): Der Titel des Films.

    Returns:
        dict: Ein Dictionary mit den Filmdetails (inklusive Poster).

    Raises:
        HTTPException: Falls der Film nicht gefunden wird (404).
    """
    movie = df[df["title"] == movie_title]
    if not movie.empty:
        clean_movie = movie.replace([float("inf"), float("-inf")], pd.NA).fillna("N/A")
        movie_dict = clean_movie.to_dict(orient='records')[0]
        return enrich_movie_with_poster(movie_dict)
    raise HTTPException(status_code=404, detail="Movie not found")


@app.get("/movie-recommendation", status_code=status.HTTP_200_OK)
def get_movie_recommendation(movie_title: str = Query(..., description="Der Titel des Films, zu dem Empfehlungen benötigt werden")):
    """
    Generiert Filmempfehlungen basierend auf einem gegebenen Filmtitel.

    Die Cosine Similarity zwischen dem TF-IDF-Vektor des Input-Films und allen anderen Filmen
    wird berechnet. Es werden die Top-10 ähnlichsten Filme (ohne den Input-Film) zurückgegeben.
    Falls doppelte Filme existieren, wird der erste Eintrag verwendet.
    Zusätzlich werden, sofern verfügbar, passende Poster abgerufen und hinzugefügt.

    Args:
        movie_title (str): Der Titel des Films, für den Empfehlungen benötigt werden.

    Returns:
        list: Eine Liste von Dictionaries mit 'id', 'title' und 'poster' der empfohlenen Filme.

    Raises:
        HTTPException: Falls der angefragte Titel nicht im Datensatz gefunden wird (404).
    """
    try:
        recommendations = recommender.get_recommendations(movie_title)
        # Erweitere die Empfehlungen um Poster-Informationen
        enriched_recommendations = [enrich_movie_with_poster(movie) for movie in recommendations]
        return enriched_recommendations
    except ValueError as ve:
        raise HTTPException(status_code=404, detail=str(ve))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Ein unerwarteter Fehler ist aufgetreten: {e}")
