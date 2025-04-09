import { useState, useEffect } from "react";
import { getMovies, getRecommendations } from "./services/api.js";
import MovieCard from './components/MovieCard'
import './App.css'

function App() {
  const [searchQuery, setSearchQuery] = useState("");
  const [movies, setMovies] = useState([]);
  const [error, setError] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const loadMovies = async () => {
      try {
        const movies = await getMovies();
        console.log("Movies from API:", movies); // Debug-Ausgabe
        setMovies(movies);
      } catch (err) {
        console.log(err);
        setError("Failed to load movies...");
      } finally {
        setLoading(false);
      }
    };

    loadMovies();
  }, []);

  const handleRecommendations = async (e) => {
    e.preventDefault();
    if (!searchQuery.trim()) return
    if (loading) return

    setLoading(true)
    try {
      const searchResults = await getRecommendations(searchQuery)
      setMovies(searchResults)
      setError(null)
    } catch (err) {
      console.log(err)
      setError("Failed to search movies...")
    } finally {
      setLoading(false)
    }
  };

  return (
    <>
      <h1>Which movie would you like to get recommendations for ?</h1>
      {loading ? (
        <div className="loading">Loading...</div>
      ) : (
        <main>
          {movies.map((movie) =>
            movie ? <MovieCard movie={movie} key={movie.id} /> : null
          )}
        </main>
      )}
    </>
  )
}

export default App
