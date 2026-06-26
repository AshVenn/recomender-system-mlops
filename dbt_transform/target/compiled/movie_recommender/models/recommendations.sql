

WITH raw_data AS (
    -- dlt creates tables using the resource name: fetch_popular_movies
    SELECT * FROM raw_movies.fetch_popular_movies
)

SELECT
    id AS movie_id,
    title,
    vote_average AS rating,
    popularity,
    release_date,
    overview AS description
FROM raw_data
-- Filter for highly-rated movies to generate the "recommendation"
WHERE vote_average >= 7.0 
ORDER BY popularity DESC
LIMIT 10