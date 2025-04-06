import '../css/MovieCard.css'

function MovieCard({ movie }) {
    if (!movie) return null;

    return (
        <>
            <section>
                <figure>
                    <img src="https://images.unsplash.com/photo-1536440136628-849c177e76a1?q=80&w=1325&auto=format&fit=crop&ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D" />
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