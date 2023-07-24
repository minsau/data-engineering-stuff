########## global imports ##########
import os
import pandas as pd
from google.cloud import storage
from .config import get_app_secrets

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
    
    return str(df.columns)

# def parse_http_request(request: object) -> dict:
#     try:
#         request_args = request.args
#         request_dict = request_args if type(request_args) is dict else dict(request_args)
#         return request_dict
#     except:
#         return dict()

def process(request: object) -> tuple:
    try:
        headers = get_data_file()
        print(headers)
        print(secrets.HOME_LOCATION)
        return ("OK", 200)
    except Exception as e:
        return (str(e), 500)

########## complete ##########