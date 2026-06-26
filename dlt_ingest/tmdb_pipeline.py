import dlt
import requests
import os
import json

@dlt.resource(write_disposition="replace")
def fetch_all_api_features():
    api_key = os.getenv("TMDB_API_KEY")
    MAX_PAGES = 50 
    
    for page in range(1, MAX_PAGES + 1):
        base_url = f"https://api.themoviedb.org/3/discover/movie?api_key={api_key}&language=en-US&sort_by=popularity.desc&page={page}"
        response = requests.get(base_url)
        if response.status_code != 200: continue
            
        movies = response.json().get("results", [])
        
        for movie in movies:
            movie_id = movie["id"]
            
            # THE ULTIMATE PAYLOAD
            # We append 6 massive datasets to the core movie dictionary
            appends = "credits,keywords,videos,similar,recommendations,release_dates"
            details_url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key={api_key}&language=en-US&append_to_response={appends}"
            
            details_response = requests.get(details_url)
            
            if details_response.status_code == 200:
                data = details_response.json()
                
                # 1. NLP Flattening (For our specific ML Feature Store downstream)
                data['genres_flat'] = " ".join([g["name"] for g in data.get("genres", [])])
                
                cast = data.get("credits", {}).get("cast", [])
                data['cast_flat'] = " ".join([actor["name"].replace(" ", "") for actor in cast[:5]])
                
                crew = data.get("credits", {}).get("crew", [])
                director = [member["name"].replace(" ", "") for member in crew if member["job"] == "Director"]
                data['director_flat'] = " ".join(director)
                
                keywords = data.get("keywords", {}).get("keywords", [])
                data['keywords_flat'] = " ".join([kw["name"] for kw in keywords])
                
                companies = data.get("production_companies", [])
                data['studios_flat'] = " ".join([comp["name"].replace(" ", "") for comp in companies])
                
                # 2. The Unbreakable Backup
                data['raw_json_blob'] = json.dumps(data)
                
                # Yielding this data tells dlt to map EVERY field into the DuckDB database
                yield data

if __name__ == "__main__":
    pipeline = dlt.pipeline(
        pipeline_name="api_pipeline",
        destination=dlt.destinations.duckdb("/app/artifacts/api_features.duckdb"),
        dataset_name="raw_movies"
    )
    # Run the pipeline
    load_info = pipeline.run(fetch_all_api_features())
    print(load_info)