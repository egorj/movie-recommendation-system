import React, { useState } from 'react';
import '../css/MovieCard.css';
import Overlay from './Overlay';

function MovieCard({ movie }) {
    const [showOverlay, setShowOverlay] = useState(false);

    const openOverlay = () => setShowOverlay(true);
    const closeOverlay = () => setShowOverlay(false);

    return (
        <>
            <section onClick={openOverlay}>
                <figure>
                    <img src={movie.poster} alt={movie.title} />
                </figure>
                <article>
                    <span>Release Year: {movie.release_date?.split("-")[0]}</span>
                    <h3>{movie.title}</h3>
                    <p>{movie.overview}</p>
                </article>
            </section>

            {showOverlay && <Overlay movie={movie} onClose={closeOverlay} />}
        </>
    );
}

export default MovieCard;
