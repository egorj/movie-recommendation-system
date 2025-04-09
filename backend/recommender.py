"""
recommender.py

Dieses Modul kapselt die Logik zur Berechnung von Filmempfehlungen.
Hier wird der TF-IDF-Vectorizer verwendet, um Features aus den kombinerten
Genres und Keywords zu extrahieren, und die Cosine Similarity berechnet,
um die Ähnlichkeit zwischen Filmen zu ermitteln.
"""

import json
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

def genres_and_keywords_to_string(row: pd.Series) -> str:
    """
    Wandelt die JSON-formatierten 'genres'- und 'keywords'-Spalten eines DataFrame-Zeile in einen String um.
    
    Es werden die 'name'-Einträge extrahiert, Leerzeichen entfernt und zu einem zusammenhängenden String kombiniert.

    Args:
        row (pd.Series): Eine Zeile des DataFrames mit mindestens den Spalten 'genres' und 'keywords'.

    Returns:
        str: Ein String, der alle Genres und Keywords enthält.
    """
    try:
        genres = json.loads(row['genres'])
    except Exception as e:
        genres = []
    genres_str = ' '.join(''.join(genre.get('name', '').split()) for genre in genres)

    try:
        keywords = json.loads(row['keywords'])
    except Exception as e:
        keywords = []
    keywords_str = ' '.join(''.join(keyword.get('name', '').split()) for keyword in keywords)

    return f"{genres_str} {keywords_str}"


class MovieRecommender:
    def __init__(self, df: pd.DataFrame):
        """
        Initialisiert den MovieRecommender: Es wird eine neue Spalte erstellt, 
        in der Genres und Keywords zusammengeführt werden. Anschließend wird die TF-IDF-Matrix
        berechnet und die Cosine Similarity erstellt.
        
        Args:
            df (pd.DataFrame): Der DataFrame, der die Filmdaten enthält.
        """
        self.df = df.copy()
        # Erstelle eine neue Spalte 'string' aus Genres und Keywords
        self.df['string'] = self.df.apply(genres_and_keywords_to_string, axis=1)
        # Initialisierung des TF-IDF Vectorizers mit maximal 5000 Features
        self.tfidf = TfidfVectorizer(max_features=5000, stop_words='english')
        # Erstelle die TF-IDF-Matrix basierend auf der Spalte 'string'
        self.X = self.tfidf.fit_transform(self.df['string'])
        # Berechne die Cosine Similarity Matrix
        self.cosine_sim = cosine_similarity(self.X, self.X)
        # Erstelle ein Mapping von Filmtiteln auf DataFrame-Indizes
        self.movie2idx = pd.Series(self.df.index, index=self.df['title']).to_dict()

    def get_recommendations(self, movie_title: str, top_n: int = 10) -> list:
        """
        Ermittelt basierend auf dem gegebenen Filmtitel die Top-N ähnlichen Filme.

        Es wird die Cosine Similarity zwischen dem TF-IDF-Vektor des Input-Films und
        allen anderen Filmen berechnet. Anschließend werden die Filme absteigend nach
        Ähnlichkeit sortiert, wobei der Input-Film ausgeschlossen wird.

        Args:
            movie_title (str): Der Titel des Films, für den Empfehlungen benötigt werden.
            top_n (int): Anzahl der empfohlenen Filme (Standard: 10).

        Returns:
            list: Eine Liste von Dictionaries mit 'id' und 'title' der empfohlenen Filme.

        Raises:
            ValueError: Falls der angefragte Titel nicht im Datensatz gefunden wird.
        """
        # Überprüfe, ob der Filmtitel im Mapping vorhanden ist
        if movie_title not in self.movie2idx:
            raise ValueError(f"Film mit Titel '{movie_title}' wurde nicht gefunden.")

        idx = self.movie2idx[movie_title]
        query_vector = self.X[idx]
        scores = cosine_similarity(query_vector, self.X).flatten()
        # Sortiere die Indizes basierend auf den Ähnlichkeitswerten und schließe den Input-Film aus
        recommended_idx = (-scores).argsort()[1:top_n+1]
        # Extrahiere 'id' und 'title' der empfohlenen Filme
        rec_movies = self.df.loc[recommended_idx, ['id', 'title', 'overview', 'release_date']]
        return rec_movies.to_dict(orient='records')
