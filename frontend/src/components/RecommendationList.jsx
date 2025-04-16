import React from 'react';

function RecommendationList({ recommendations, loading, error }) {
    if (loading) return <p>Loading . . .</p>;
    if (error) return <p style={{ color: 'red' }}>{error}</p>;
    if (recommendations.length === 0) return <p>Sorry, No recommendations found . . .</p>;

    return (
        <ul>
            {recommendations.map(rec => (
                <main key={rec.id}>
                    <section style={{ pointerEvents: 'none', cursor: 'default' }}>
                        <figure>
                            <img src={rec.poster} alt={rec.title} />
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
    );
}

export default RecommendationList;
