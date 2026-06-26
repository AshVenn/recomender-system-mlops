from dagster import asset, Definitions, AssetExecutionContext, MetadataValue, define_asset_job, ScheduleDefinition
import subprocess
import duckdb
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.neighbors import NearestNeighbors
import joblib

@asset
def ingest_api_data():
    subprocess.run(["python", "dlt_ingest/tmdb_pipeline.py"], check=True)
    return "API data ingested successfully"

@asset(deps=[ingest_api_data])
def transform_reco_features():
    subprocess.run([
        "dbt", "run", 
        "--project-dir", "dbt_transform", 
        "--profiles-dir", "dbt_transform"
    ], check=True)
    return "Recommendation features transformed successfully"

@asset(deps=[transform_reco_features])
def train_demo_recommender(context: AssetExecutionContext):
    # 1. Connect exclusively to the isolated Feature Store
    con = duckdb.connect('/app/artifacts/reco_features.duckdb')
    df = con.sql("SELECT movie_id, title, combined_features FROM analytics.ml_feature_table").df()
    con.close()
    
    if df.empty: raise ValueError("Feature table is empty.")

    # 2. Train the NLP Model
    vectorizer = TfidfVectorizer(stop_words='english')
    tfidf_matrix = vectorizer.fit_transform(df['combined_features'])

    knn_model = NearestNeighbors(metric='cosine', algorithm='brute')
    knn_model.fit(tfidf_matrix)

    # 3. Package and Save to the Artifacts folder
    recommender_package = {
        'knn_model': knn_model,
        'vectorizer': vectorizer,
        'movie_metadata': df[['movie_id', 'title']] 
    }
    
    model_path = "/app/artifacts/content_recommender.pkl"
    joblib.dump(recommender_package, model_path)

    context.add_output_metadata({
        "API Database": MetadataValue.path("/app/artifacts/api_features.duckdb"),
        "Feature Database": MetadataValue.path("/app/artifacts/reco_features.duckdb"),
        "Model Artifact": MetadataValue.path(model_path)
    })
    return "Recommender saved successfully"

# Automation Schedule
movie_pipeline_job = define_asset_job(name="movie_pipeline_job", selection="*")
movie_pipeline_schedule = ScheduleDefinition(name="daily_recommender_update", job=movie_pipeline_job, cron_schedule="0 0 * * *")

defs = Definitions(
    assets=[ingest_api_data, transform_reco_features, train_demo_recommender],
    schedules=[movie_pipeline_schedule]
)