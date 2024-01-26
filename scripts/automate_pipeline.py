import pandas as pd
import os
from google.cloud import storage
from google.cloud import bigquery
import logging

# Setting up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def convert_and_reformat_xls_to_csv(file_path, output_path):
    """
    Converts an XLS file to CSV and reformats the time column.

    :param file_path: Path to the XLS file.
    :param output_path: Path where the output CSV file will be saved.
    """
    try:
        # Reading the .xls file
        logging.info(f"Reading {file_path}")
        data = pd.read_excel(file_path)

        # Checking if 'time' column exists and reformatting
        if 'time' in data.columns:
            logging.info("Reformatting 'time' column")
            data['time'] = pd.to_datetime(data['time'], format='%d/%m/%Y %H:%M').dt.strftime('%Y-%m-%d %H:%M')
        else:
            logging.warning("'time' column not found in the data")

        # Saving to .csv
        data.to_csv(output_path, index=False)
        logging.info(f"File saved as {output_path}")

    except Exception as e:
        logging.error(f"Error occurred: {e}")

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


def load_data_from_gcs_to_bigquery(bucket_name, blob_name, dataset_id, table_id, project_id):
    """
    Loads data from GCS bucket to a BigQuery table.

    :param bucket_name: Name of the GCS bucket.
    :param blob_name: Name of the blob (file) in the bucket.
    :param dataset_id: BigQuery dataset ID.
    :param table_id: BigQuery table ID.
    :param project_id: Google Cloud project ID.
    """
    try:
        # Construct a BigQuery client object with the specified project.
        client = bigquery.Client(project=project_id)

        # Configure the load job
        job_config = bigquery.LoadJobConfig(
            source_format=bigquery.SourceFormat.CSV,
            skip_leading_rows=1,  # Assumes header row present
            autodetect=True,      # Auto-detect schema
        )

        # Construct the URI for the GCS location
        uri = f"gs://{bucket_name}/{blob_name}"

        # Load job
        load_job = client.load_table_from_uri(
            uri,
            f"{dataset_id}.{table_id}",
            job_config=job_config
        )

        # Wait for the job to complete
        load_job.result()
        logging.info(f"Job finished. Loaded data from {uri} into {dataset_id}.{table_id}")

    except Exception as e:
        logging.error(f"An error occurred: {e}")

# Parameters for the data transformation
input_file = '/Users/jrdegbe/Desktop/Traffic-task-GCP/data/traffic_spreadsheet.xls'
output_file = '/Users/jrdegbe/Desktop/Traffic-task-GCP/data/traffic_data.csv'

# Convert and reformat the XLS file
convert_and_reformat_xls_to_csv(input_file, output_file)

# Parameters for uploading to GCS
bucket_name = 'london_traffic_data_bucket'
source_file_path = '/Users/jrdegbe/Desktop/Traffic-task-GCP/data/traffic_data.csv' 
destination_blob_name = 'traffic_data.csv'

# Upload the file to GCS
upload_to_gcs(bucket_name, source_file_path, destination_blob_name)

# Parameters for loading data into BigQuery
blob_name = 'traffic_data.csv'
dataset_id = 'london_traffic_data'
table_id = 'london_traffic_table'
project_id = 'traffic-data-pipeline'

# Load the data from GCS to BigQuery
load_data_from_gcs_to_bigquery(bucket_name, blob_name, dataset_id, table_id, project_id)
