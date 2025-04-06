const BASE_URL = "http://127.0.0.1:8000/";

export const getMovies = async () => {
    const response = await fetch(`${BASE_URL}`);
    const data = await response.json();
    return data;
};

export const getRecommendations = async (movieTitle) => {
    const response = await fetch(
        `${BASE_URL}movie-recommendation?movie_title=${encodeURIComponent(
            movieTitle
        )}`
    );
    const data = await response.json();
    return data;
};