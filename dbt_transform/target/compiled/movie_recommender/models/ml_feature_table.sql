

WITH raw_data AS (
    -- Read from the linked API Database, using the updated ultimate function name
    SELECT * FROM api_db.raw_movies.fetch_all_api_features
)

SELECT
    id AS movie_id,
    title,
    popularity,
    -- Combine ALL the new metadata into the ultimate NLP corpus
    -- COALESCE prevents the whole string from breaking if one field is missing
    LOWER(
        title || ' ' || 
        COALESCE(genres_flat, '') || ' ' || 
        COALESCE(cast_flat, '') || ' ' || 
        COALESCE(director_flat, '') || ' ' || 
        COALESCE(keywords_flat, '') || ' ' || 
        COALESCE(studios_flat, '') || ' ' || 
        COALESCE(overview, '')
    ) AS combined_features
FROM raw_data
WHERE overview IS NOT NULL 
  AND overview != ''