import os
from typing import Optional
from fastapi import FastAPI, Path, Query, HTTPException
from starlette import status
from fastapi.middleware.cors import CORSMiddleware

import numpy as np
import pandas as pd
import json

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# Initialize FastAPI application
app = FastAPI()

# Erlaube dem Frontend Zugriff auf das Backend (Nur zum Testen)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Define the path to the CSV file containing movie data.
# The CSV file is located in a folder named 'data' relative to this script's directory.
csv_path = os.path.join(os.path.dirname(__file__), "data", "tmdb_5000_movies.csv")

# Read the CSV file into a Pandas DataFrame.
df = pd.read_csv(csv_path)

# Convert the first 12 rows of the DataFrame into a JSON-like structure (list of dictionaries)
data = json.loads(df.head(12).to_json(orient='records'))


def genres_and_keywords_to_string(row):
    """
    Convert genres and keywords from a movie DataFrame row into a single string.

    The function extracts JSON formatted 'genres' and 'keywords' columns,
    splits the 'name' of each genre/keyword, removes any extra whitespace,
    and concatenates them into a single string separated by a space.
    
    Args:
        row (pd.Series): A row from the DataFrame with at least 'genres' and 'keywords' columns.

    Returns:
        str: A concatenated string containing all genres and keywords.
    """
    # Parse the 'genres' column, which is stored as a JSON string.
    genres = json.loads(row['genres'])
    # Extract the 'name' field from each genre, remove spaces, and join them with spaces.
    genres = ' '.join(''.join(genre['name'].split()) for genre in genres)

    # Parse the 'keywords' column, which is also a JSON string.
    keywords = json.loads(row['keywords'])
    # Extract the 'name' field from each keyword, remove spaces, and join them with spaces.
    keywords = ' '.join(''.join(keyword['name'].split()) for keyword in keywords)

    # Return a concatenated string of genres and keywords.
    return f"{genres} {keywords}"


# Create a new column 'string' in the DataFrame by applying the genres_and_keywords_to_string function to each row.
df['string'] = df.apply(genres_and_keywords_to_string, axis=1)

# Initialize the TF-IDF Vectorizer with a maximum of 5000 features.
tfidf = TfidfVectorizer(max_features=5000)
# Fit and transform the 'string' column of the DataFrame to create a TF-IDF matrix.
X = tfidf.fit_transform(df['string'])

# Create a mapping from movie titles to DataFrame indices.
# This is useful for quickly finding the index of a movie by its title.
movie2idx = pd.Series(df.index, index=df['title'])


@app.get("/", status_code=status.HTTP_200_OK)
def read_all_movies():
    """
    Retrieve the first 10 movies as a JSON list.

    Returns:
        list: A list of movie dictionaries containing the first 10 movies.
    """
    return data


@app.get("/movies/{movie_id}", status_code=status.HTTP_200_OK)
def read_movie_by_id(movie_id: int = Path(gt=0)):
    """
    Retrieve a movie from the dataset by its ID.

    Args:
        movie_id (int): The ID of the movie to retrieve.

    Returns:
        dict: A dictionary containing the movie details, or a 404 error if not found.
    """
    # Filter the DataFrame for the row where the 'id' column matches the given movie_id
    movie = df[df["id"] == movie_id]

    # Check if a matching movie was found
    if not movie.empty:
        # Convert the single-row DataFrame to JSON and parse it into a Python dict
        movie_json = json.loads(movie.to_json(orient="records"))[0]
        return movie_json

    # If no movie was found, raise a 404 error
    raise HTTPException(status_code=404, detail="Movie not found")


@app.get("/movies", status_code=status.HTTP_200_OK)
def read_movie_by_title(movie_title: str):
    """
    Retrieve a movie from the dataset by its title.

    Args:
        movie_title (str): The Title of the movie to retrieve.

    Returns:
        dict: A dictionary containing the movie details, or a 404 error if not found.
    """
    # Filter the DataFrame for the row where the 'title' column matches the given movie_title
    movie = df[df["title"] == movie_title]

    # Check if a matching movie was found
    if not movie.empty:
        # Convert the single-row DataFrame to JSON and parse it into a Python dict
        movie_json = json.loads(movie.to_json(orient="records"))[0]
        return movie_json

    # If no movie was found, raise a 404 error
    raise HTTPException(status_code=404, detail="Movie not found")


@app.get("/movie-recommendation", status_code=status.HTTP_200_OK)
def get_movie_recommendation(movie_title: str):
    """
    Generate movie recommendations based on a provided movie title.

    This endpoint calculates cosine similarity between the TF-IDF vector of the input movie and
    all other movies in the dataset. It returns the titles of the top 10 most similar movies,
    excluding the input movie itself.

    Args:
        movie_title (str): The title of the movie for which recommendations are needed.

    Returns:
        pd.Series: A Pandas Series of recommended movie titles.
    """
    # Retrieve the DataFrame index corresponding to the movie_title.
    idx = movie2idx[movie_title]
    # If multiple indices are returned (i.e., if there are duplicate titles), select the first one.
    if type(idx) == pd.Series:
        idx = idx.iloc[0]

    # Get the TF-IDF vector for the selected movie.
    query = X[idx]
    # Compute cosine similarity scores between the query vector and all vectors in the matrix.
    scores = cosine_similarity(query, X)
    # Flatten the scores array into a 1D array.
    scores = scores.flatten()
    # Sort the indices of the movies based on similarity scores in descending order,
    # then select the top 10 movies (excluding the input movie at index 0).
    recommended_idx = (-scores).argsort()[1:11]
    # Create a DataFrame containing 'id' and 'title' for the recommended movies.
    recommended_movies = df.loc[recommended_idx, ['id', 'title']]
    # Convert the DataFrame to a JSON string with a list of records.
    recommended_movies_json = json.loads(recommended_movies.to_json(orient='records'))
    return recommended_movies_json
