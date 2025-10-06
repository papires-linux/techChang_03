output "bucket_csv" {
  description = "Nome do bucket criado no GCP"
  value       = google_storage_bucket.bucket_csv.name
}

output "bigquery_dataset_id" {
  description = "ID do dataset criado no BigQuery"
  value       = google_bigquery_dataset.dataset_vendas.dataset_id
}


