🧾 Descrição do Script Terraform

Este script Terraform automatiza a criação de uma infraestrutura básica de dados na Google Cloud Platform (GCP). Ele realiza as seguintes ações:

1. Cria um bucket no Cloud Storage.
2. Faz o upload de um arquivo CSV para esse bucket.
3. Cria um dataset no BigQuery.
4. Cria uma tabela externa no BigQuery, que lê os dados diretamente do arquivo CSV no bucket.

⚙️ Recursos Criados
✅ 1. Provider do Google Cloud

Define o provedor da GCP com as credenciais da service account, o projeto (fiap-tc03) e a região (us-central1).
```json
provider "google" {
  credentials = file("../service-account.json")
  project     = "fiap-tc03"
  region      = "us-central1"
}
```
🔑 2. ID Aleatório para Nome Único do Bucket

Gera um sufixo aleatório com 4 bytes (em hexadecimal) para garantir que o nome do bucket seja único (exigência da GCP).
```json
resource "random_id" "sufixo" {
  byte_length = 4
}
```
🪣 3. Bucket no Cloud Storage

Cria um bucket com nome composto pela variável bucket_name e o sufixo aleatório. Isso evita conflitos com outros buckets existentes.
```json
resource "google_storage_bucket" "bucket_csv" {
  name          = "${var.bucket_name}-${random_id.sufixo.hex}"
  location      = "US"
  storage_class = "STANDARD"
}
```

📦 4. Upload de Arquivo CSV

Faz o upload de um arquivo CSV (fornecido via variável csv_dados) para a pasta raw/vendas/ dentro do bucket.
```json
resource "google_storage_bucket_object" "upload_arquivo" {
  name   = "raw/vendas/${var.bucket_name}"
  bucket = google_storage_bucket.bucket_csv.name
  source = "csv/${var.csv_dados}"
}
```

🗃️ 5. Criação de Dataset no BigQuery

Cria um dataset no BigQuery com o nome especificado pela variável dataset_name, com o nome amigável "Dataset Vendas BMW".

```json
resource "google_bigquery_dataset" "dataset_vendas" {
  dataset_id                 = "${var.dataset_name}"
  friendly_name              = "Dataset Vendas BMW"
  location                   = "US"
  delete_contents_on_destroy = false
}
```

🔗 6. Tabela Externa no BigQuery

Cria uma tabela externa no BigQuery que lê diretamente o arquivo CSV armazenado no bucket, sem necessidade de importar os dados.
* O formato do arquivo é CSV.
* O schema da tabela é detectado automaticamente.
* A primeira linha do CSV é ignorada (cabeçalho).
* A tabela depende da existência do arquivo no bucket (depends_on).

```json
resource "google_bigquery_table" "external_table" {
  dataset_id         = "${var.dataset_name}"
  table_id           = "${var.tabela_vendas}"
  deletion_protection = false

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
``` 

📌 Requisitos

* Conta na Google Cloud Platform
* Projeto GCP ativo
* Service account com permissões adequadas (BigQuery Admin, Storage Admin)
* Arquivo service-account.json com as credenciais da conta de serviço

📁 Estrutura Esperada de Arquivos
```text
.
├── main.tf                     # Script Terraform (acima)
├── variables.tf                # Definições das variáveis ├── output.tf                   # Valores atribuídos para saida da informação
├── csv/
│   └── vendas_bmw.csv          # Arquivo CSV com os dados
└── service-account.json        # Credenciais da GCP
````

💬 Exemplo de variables.tf
```json
variable "bucket_name" {
  description = "Nome base do bucket GCP"
  type        = string
}

variable "dataset_name" {
  description = "Nome do dataset no BigQuery"
  type        = string
}

variable "tabela_vendas" {
  description = "Nome da tabela externa no BigQuery"
  type        = string
}

variable "csv_dados" {
  description = "Nome do arquivo CSV com os dados de vendas"
  type        = string
}
```

## 🧪 Como Usar

Configure o Terraform:
```bash
terraform init
```

Valide os arquivos:
```bash
terraform validate
```

Planeje a execução:
```bash
terraform plan
```

Aplique a infraestrutura:
```bash
terraform apply
```
