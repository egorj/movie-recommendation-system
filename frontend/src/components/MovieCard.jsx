import '../css/MovieCard.css'

function MovieCard({ movie }) {
    if (!movie) return null;

    return (
        <>
            <section>
                <figure>
                    <img src={movie.poster} />
                </figure>
                <article>
                    <span>Release Year: {movie.release_date?.split("-")[0]}</span>
                    <h3>{movie.title}</h3>
                    <p>{movie.overview}</p>
                </article>
            </section>
        </>
    )
}

export default MovieCard