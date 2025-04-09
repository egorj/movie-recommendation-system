import '../css/MovieCard.css'
import { useState, useEffect } from 'react';
import { getRecommendations } from '../services/api.js';

function MovieCard({ movie }) {
  const [showOverlay, setShowOverlay] = useState(false);
  const [recommendations, setRecommendations] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  if (!movie) return null;

  // Overlay öffnen und API-Aufruf initiieren
  const openOverlay = () => {
    setShowOverlay(true);
  };

  // Overlay schließen, evtl. bestehende Daten zurücksetzen
  const closeOverlay = () => {
    setShowOverlay(false);
    setRecommendations([]);
    setError(null);
  };

  // Sobald das Overlay sichtbar ist, hole die Empfehlungen vom Server
  useEffect(() => {
    if (showOverlay) {
      setLoading(true);
      getRecommendations(movie.title)
        .then(data => {
          setRecommendations(data);
          setLoading(false);
        })
        .catch(err => {
          setError('Fehler beim Laden der Empfehlungen');
          setLoading(false);
        });
    }
  }, [showOverlay, movie.title]);

  return (
    <>
      <section onClick={openOverlay}>
        <figure>
          <img src={movie.poster} />
        </figure>
        <article>
          <span>Release Year: {movie.release_date?.split("-")[0]}</span>
          <h3>{movie.title}</h3>
          <p>{movie.overview}</p>
        </article>
      </section>

      {showOverlay && (
        <div className='overlay'>
          <button onClick={closeOverlay} className='backButton'>
            &larr;
          </button>
          <div className='overlayContent'>
            <h1>Your Recommendations</h1>
            {loading && <p>Loading . . .</p>}
            {error && <p style={{ color: 'red' }}>{error}</p>}
            {!loading && !error && recommendations.length === 0 && <p>Sorry, No recommendations found . . .</p>}
            <ul>
              {recommendations.map(rec => (
                <main>
                <section>
                <figure>
                    <img src={rec.poster} />
                </figure>
                <article>
                    <span>Release Year: {rec.release_date?.split("-")[0]}</span>
                    <h3>{rec.title}</h3>
                    <p>{rec.overview}</p>
                </article>
                </section>
                </main>
              ))}
            </ul>
          </div>
        </div>
      )}
    </>
  );
}

export default MovieCard;

