resource "google_storage_bucket" "data_bucket" {
  name          = "london_traffic_data_bucket"
  location      = "EU"
  force_destroy = true  # Allows the bucket to be destroyed even if it contains objects; use with caution
}

