# Provider para o GCP
provider "google" {
  credentials = file("../service-account.json")
  project     = "${var.project_gcp}"
  region      = "us-central1"       
}

# Radom dos recursos
resource "random_id" "sufixo" {
  byte_length = 4 
}

# Criação do bucket no GCP
resource "google_storage_bucket" "bucket_csv" {
  name = "${var.bucket_name}-${random_id.sufixo.hex}"
  location = "US"
  storage_class = "STANDARD" 
  force_destroy = true

}

# criacao do dataset para vendas
resource "google_bigquery_dataset" "dataset_vendas" {
  dataset_id                  = "${var.dataset_name}"
  friendly_name               = "Dataset Vendas BMW"
  location                    = "US"
  delete_contents_on_destroy  = true 
}

# criacao do script para subir o csv no bucket
resource "google_storage_bucket_object" "upload_arquivo" {
  name   = "raw/vendas/${var.bucket_name}"
  bucket = google_storage_bucket.bucket_csv.name
  source = "csv/${var.csv_dados}"
}

# Criacao da external table para raw
resource "google_bigquery_table" "external_table" {
  dataset_id =  "${var.dataset_name}"
  table_id   =  "${var.tabela_vendas}"
  deletion_protection = false  # Desativando a proteção

  depends_on = [
    google_storage_bucket_object.upload_arquivo
  ]

  external_data_configuration {
    source_format = "CSV" 

    source_uris = [
      format("gs://%s/%s", google_storage_bucket.bucket_csv.name, google_storage_bucket_object.upload_arquivo.name)
    ]

    autodetect = true

    csv_options {
      skip_leading_rows = 1
      quote             = "\""
    }
  }
}

