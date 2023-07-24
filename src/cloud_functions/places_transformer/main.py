########## global imports ##########
import os
from google.cloud import bigquery
import pandas as pd
from google.cloud import storage
from .config import get_app_secrets, settings
from .geo import get_geocode_by_place_name
import functions_framework
from cloudevents.http import CloudEvent


secrets = get_app_secrets()

########## global vars ##########

########## classes & functions ##########
def get_data_file() -> str:
    bucket_name = os.environ.get('BUCKET_NAME')
    storage_client = storage.Client()
    bucket = storage_client.bucket(bucket_name)
    blob = bucket.blob('places.csv')
    blob.download_to_filename('/tmp/temp.csv')        
    with open('/tmp/temp.csv','rb') as f:
        df = pd.read_csv(f)
    print(f'File downloaded from bucket {bucket_name}')
    return df

def generate_transformed_data_frame(df: pd.DataFrame) -> list:
    final_list = [get_geocode_by_place_name(place, visited) for place, visited in zip(df['places'], df['visited'])]
    places_df = pd.DataFrame(final_list)
    places_df.drop_duplicates(inplace=True)
    places_df['place_name_list'].to_string(index=False)
    places_df['formatted_address'].to_string(index=False)
    places_df['place_id'].to_string(index=False)
    print(f'File transformed')
    return places_df

def update_bigquery_table(places_df: pd.DataFrame) -> None:
    table_id = f'{settings.BQ_DATASET_PREFIX}.places'
    bq_client = bigquery.Client()
    bq_client.delete_table(table_id, not_found_ok=True)
    job = bq_client.load_table_from_dataframe(
        places_df, 
        table_id
    )
    job.result()
    print(f'Data uploaded to BigQuery')

@functions_framework.cloud_event
def places_transformer(cloud_event: CloudEvent) -> tuple:
    data = cloud_event.data

    event_id = cloud_event["id"]
    event_type = cloud_event["type"]
    bucket = data["bucket"]
    name = data["name"]

    print(f"Event ID: {event_id}")
    print(f"Event type: {event_type}")
    print(f"Bucket: {bucket}")
    print(f"File: {name}")

    try:
        df = get_data_file()
        places_df = generate_transformed_data_frame(df)
        update_bigquery_table(places_df)
        return ("OK", 200)
    except Exception as e:
        return (str(e), 500)

########## complete ##########