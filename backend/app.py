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

# Initialisiere die FastAPI-Applikation
app = FastAPI(
    title="Movie Recommendation API",
    description="Empfiehlt Filme basierend auf TF-IDF und Cosine Similarity",
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

# Entferne ungültige Werte für eine sichere JSON-Ausgabe
safe_df_excerpt = df.head(12).replace([float("inf"), float("-inf")], pd.NA).fillna("N/A")
data_excerpt = json.loads(safe_df_excerpt.to_json(orient="records"))

# Initialisiere den MovieRecommender
recommender = MovieRecommender(df)


@app.get("/", status_code=status.HTTP_200_OK)
def read_all_movies():
    """
    Liefert die ersten 12 Filme als JSON-Liste.

    Returns:
        list: Eine Liste von Dictionaries mit den Details der ersten 12 Filme.
    """
    return data_excerpt


@app.get("/movies/{movie_id}", status_code=status.HTTP_200_OK)
def read_movie_by_id(movie_id: int = Path(..., gt=0, description="Die ID des zu suchenden Films")):
    """
    Liefert einen Film anhand der übergebenen Film-ID.
    """
    movie = df[df["id"] == movie_id]
    if not movie.empty:
        # Sichere Konvertierung (ersetze inf/NaN → "N/A")
        clean_movie = movie.replace([float("inf"), float("-inf")], pd.NA).fillna("N/A")
        return clean_movie.to_dict(orient='records')[0]
    raise HTTPException(status_code=404, detail="Movie not found")


@app.get("/movies", status_code=status.HTTP_200_OK)
def read_movie_by_title(movie_title: str = Query(..., description="Der Titel des zu suchenden Films")):
    """
    Liefert einen Film anhand des übergebenen Titels.
    """
    movie = df[df["title"] == movie_title]
    if not movie.empty:
        clean_movie = movie.replace([float("inf"), float("-inf")], pd.NA).fillna("N/A")
        return clean_movie.to_dict(orient='records')[0]
    raise HTTPException(status_code=404, detail="Movie not found")


@app.get("/movie-recommendation", status_code=status.HTTP_200_OK)
def get_movie_recommendation(movie_title: str = Query(..., description="Der Titel des Films, zu dem Empfehlungen benötigt werden")):
    """
    Generiert Filmempfehlungen basierend auf einem gegebenen Filmtitel.
    """
    try:
        recommendations = recommender.get_recommendations(movie_title)
        return recommendations
    except ValueError as ve:
        raise HTTPException(status_code=404, detail=str(ve))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Ein unerwarteter Fehler ist aufgetreten: {e}")
