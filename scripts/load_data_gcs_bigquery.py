from google.cloud import bigquery
import logging

# Initialize logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")


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

# Define your GCS bucket, blob, BigQuery dataset, table, and project information
bucket_name = 'london_traffic_data_bucket'
blob_name = 'traffic_data.csv'  # Name of the file in the bucket
dataset_id = 'london_traffic_data'
table_id = 'london_traffic_table'
project_id = 'traffic-data-pipeline'  #  project ID

# Load the data
load_data_from_gcs_to_bigquery(bucket_name, blob_name, dataset_id, table_id, project_id)