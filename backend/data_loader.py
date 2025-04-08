"""
data_loader.py

Dieses Modul enthält Funktionen zum Laden und Vorverarbeiten der Filmdaten.
"""

import os
import pandas as pd

def load_movie_data(csv_path: str) -> pd.DataFrame:
    """
    Lädt Filmdaten aus einer CSV-Datei und gibt sie als pandas DataFrame zurück.

    Args:
        csv_path (str): Der Pfad zur CSV-Datei mit den Filmdaten.

    Returns:
        pd.DataFrame: DataFrame der geladenen Filmdaten.

    Raises:
        FileNotFoundError: Falls die CSV-Datei nicht existiert.
        RuntimeError: Falls das Laden der Datei fehlschlägt oder erforderliche Spalten fehlen.
    """
    if not os.path.exists(csv_path):
        raise FileNotFoundError(f"Die Datei {csv_path} wurde nicht gefunden.")
    try:
        df = pd.read_csv(csv_path)
        # Überprüfen, ob die erforderlichen Spalten vorhanden sind
        required_columns = {'id', 'title', 'genres', 'keywords', 'overview'}
        if not required_columns.issubset(set(df.columns)):
            missing = required_columns - set(df.columns)
            raise RuntimeError(f"Die CSV-Datei fehlt folgende Spalten: {', '.join(missing)}")
        # Sicherstellen, dass die Beschreibungsspalte keine fehlenden Werte enthält
        df['overview'] = df['overview'].fillna('')
        return df
    except Exception as e:
        raise RuntimeError(f"Fehler beim Laden der Datei {csv_path}: {e}")
