# BigQuery dataset
resource "google_bigquery_dataset" "traffic_dataset" {
  dataset_id                  = "london_traffic_data"
  location                    = "EU"
  default_table_expiration_ms = 3600000 # Optional: Set table expiration to 1 hour
}

# BigQuery table
resource "google_bigquery_table" "traffic_table" {
  dataset_id = google_bigquery_dataset.traffic_dataset.dataset_id
  table_id   = "london_traffic_table"

  schema = jsonencode([
    {
      "name": "time",
      "type": "TIMESTAMP",
      "mode": "REQUIRED"
    },
    {
      "name": "traffic",
      "type": "INTEGER", # Or FLOAT, STRING, etc., depending on the data
      "mode": "REQUIRED"
    }
  ])
}