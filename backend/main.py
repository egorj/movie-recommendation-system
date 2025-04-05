import os
from typing import Optional
from fastapi import FastAPI, Path, Query, HTTPException
from starlette import status

import numpy as np
import pandas as pd
import json

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

app = FastAPI()

csv_path_movies = os.path.join(os.path.dirname(__file__), "data", "tmdb_5000_movies.csv")
csv_path_credits = os.path.join(os.path.dirname(__file__), "data", "tmdb_5000_credits.csv")

df_movies = pd.read_csv(csv_path_movies)
df_credits = pd.read_csv(csv_path_credits)
df = df_movies.merge(df_credits, left_on='id', right_on='movie_id')
df.drop(columns=['movie_id'], inplace=True)


@app.get("/", status_code=status.HTTP_200_OK)
def read_all_movies():
    return df.head(5).to_dict(orient="records")


@app.get("/movies/{movie_id}", status_code=status.HTTP_200_OK)
def read_movie(movie_id: int = Path(gt=0)):
    for movie in df.to_dict(orient="records"):
        if movie["id"] == movie_id:
            return movie
    raise HTTPException(status_code=404, detail="Movie not found")


