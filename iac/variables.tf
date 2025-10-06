variable "bucket_name" {
  description = "Prefixo do nome do bucket GCS"
  type        = string
  default     = "gcs-raw-fiap"
} 

variable "project_gcp" {
  description = "Nome do projeto do GCS"
  type        = string
  default     = "fiap-tc03"
} 


variable "dataset_name"{
  description = ""
  type        = string
  default     = "vendas"
}

variable "csv_dados"{
  description = "Dados de vendas"
  type = string
  default = "BMW_dados_vendas.csv"
}


variable "tabela_vendas"{
  description = "nome da tabela de vendas"
  type = string
  default = "tb_vendas"
}

