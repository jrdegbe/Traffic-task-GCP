import os
from google.cloud import storage
import logging

# Initialize logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def upload_to_gcs(bucket_name, source_file_name, destination_blob_name):
    """
    Uploads a file to the specified GCS bucket.

    :param bucket_name: Name of the GCS bucket.
    :param source_file_name: Path to the file to upload.
    :param destination_blob_name: Name for the file in the GCS bucket.
    """
    storage_client = storage.Client()
    bucket = storage_client.bucket(bucket_name)
    blob = bucket.blob(destination_blob_name)

    try:
        blob.upload_from_filename(source_file_name)
        logging.info(f"File {source_file_name} uploaded to {destination_blob_name}.")
    except Exception as e:
        logging.error(f"Error occurred during upload: {e}")

# File paths and bucket name
bucket_name = 'london_traffic_data_bucket'
source_file_path = '/Users/jrdegbe/Desktop/Traffic-task-GCP/data/traffic_data.csv' 
destination_blob_name = 'traffic_data.csv' 

# Upload the file
upload_to_gcs(bucket_name, source_file_path, destination_blob_name)