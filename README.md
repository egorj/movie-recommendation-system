# Movie Recommendation System

Ein Machine-Learning-Projekt, das auf Basis von Nutzerpräferenzen Filme empfiehlt. Das System verwendet einen content-basierten Filtering-Ansatz, der mithilfe von TF-IDF (Term Frequency - Inverse Document Frequency) und Cosine Similarity arbeitet, um Filme zu identifizieren, die den individuellen Geschmack des Nutzers treffen.

---

## Inhaltsverzeichnis

- [Überblick](#überblick)
- [Features](#features)
- [Technologien](#technologien)
- [Architektur](#architektur)

---

## Überblick

Dieses Projekt zielt darauf ab, ein Empfehlungssystem zu erstellen, das Filme basierend auf inhaltlichen Merkmalen vorschlägt. Mithilfe von TF-IDF werden Merkmale (wie z. B. Beschreibungen, Genres oder Schlagwörter) in numerische Vektoren umgewandelt. Anschließend kommt die Cosine Similarity zum Einsatz, um Ähnlichkeiten zwischen den Filmen zu berechnen. Dadurch erhält der Nutzer personalisierte Filmempfehlungen, die seinem bisherigen Geschmack entsprechen.

Das System ist in zwei Hauptkomponenten unterteilt:

- **Backend (Python + FastAPI):** Enthält die Logik zur Datenverarbeitung, Feature-Extraktion, Berechnung der TF-IDF-Matrix und Cosine Similarity. Das Backend stellt API-Endpunkte zur Verfügung, über die Empfehlungen angefragt werden können.
- **Frontend (React):** Eine interaktive und ansprechende Benutzeroberfläche, die es Nutzern ermöglicht, Filme auszuwählen und Empfehlungen in Echtzeit anzuzeigen.

---

## Features

- **Content-basierte Filterung:** Nutzt TF-IDF, um filmbezogene Texte in Vektoren umzuwandeln.
- **Berechnung der Cosine Similarity:** Vergleicht Filme anhand der Ähnlichkeit ihrer Merkmale.
- **Einfache API-Schnittstelle:** Das Backend stellt eine API zur Verfügung, um Empfehlungen zu generieren.
- **Interaktives Frontend:** Eine moderne Benutzeroberfläche, die mit React realisiert wurde.
- **Modulare Architektur:** Leicht erweiterbar für zukünftige Features, wie z. B. hybride Empfehlungssysteme oder zusätzliche Filtermöglichkeiten.

---

## Technologien

### Backend

- **Python:** Programmiersprache für Machine Learning und Datenverarbeitung.
- **scikit-learn:** Für die Berechnung von TF-IDF und Cosine Similarity.
- **FastAPI:** Zur Erstellung der RESTful API.

### Frontend

- **React:** Für den Aufbau der Benutzeroberfläche.

---

## Architektur

Das System folgt einem klar getrennten Architekturansatz:

1. **Datenaufbereitung:**  
   - Im Ordner `backend/data` befinden sich die Rohdaten (Filminformationen).  
   - Die Daten werden vor-verarbeitet, um relevante Features zu extrahieren.

2. **Feature-Extraktion:**  
   - Mit TF-IDF werden Textinformationen in numerische Merkmalsvektoren umgewandelt.
   
3. **Ähnlichkeitsberechnung:**  
   - Die Cosine Similarity wird berechnet, um die inhaltliche Nähe zwischen Filmen zu bestimmen.

4. **API-Integration:**  
   - Das Backend stellt Endpunkte zur Verfügung, über die Anfragen zur Empfehlung gestellt werden können.
   
5. **Frontend-Interaktion:**  
   - Das React-Frontend kommuniziert mit der API, um dynamisch Empfehlungen anzuzeigen.

Diese modulare Architektur ermöglicht es, einzelne Komponenten unabhängig zu optimieren und bei Bedarf neue Funktionalitäten hinzuzufügen.

---
