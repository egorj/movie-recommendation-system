import React, { useState, useEffect } from 'react';
import '../css/MovieCard.css';
import { getRecommendations } from '../services/api.js';
import RecommendationList from './RecommendationList';

function Overlay({ movie, onClose }) {
    const [recommendations, setRecommendations] = useState([]);
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState(null);

    // Empfehlungen laden, wenn das Overlay angezeigt wird
    useEffect(() => {
        if (movie) {
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
    }, [movie]);

    // Funktion zum Schließen des Overlays
    const handleClose = () => {
        onClose(); // Callback-Funktion aufrufen, um das Overlay zu schließen
    };

    // Funktion, um das Overlay zu schließen, wenn außerhalb des Overlays geklickt wird
    const handleOverlayClick = (e) => {
        if (e.target === e.currentTarget) {
            onClose();
        }
    };

    return (
        <div
            className={`overlay ${recommendations.length > 0 ? 'show' : ''}`}
            onClick={handleOverlayClick}
        >
            <button onClick={handleClose} className="backButton">
                &larr;
            </button>
            <div className="overlayContent">
                <h1>Your Recommendations</h1>
                <RecommendationList
                    recommendations={recommendations}
                    loading={loading}
                    error={error}
                />
            </div>
        </div>
    );
}

export default Overlay;
