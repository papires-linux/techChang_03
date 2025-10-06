# API de Predição de Vendas de Carros — Flask + Google Cloud

Esta API foi desenvolvida em **Python (Flask)** para realizar **previsões de vendas de carros** com base em um modelo de Machine Learning previamente treinado e armazenado no **Google Cloud Storage (GCS)**.

A aplicação pode rodar **localmente** ou **baixar automaticamente o modelo do GCS**, conforme configurado nas variáveis de ambiente.

---

## 📁 Estrutura do Projeto

├── app.py           |# Código principal da API Flask \
├── requirements.txt |# Dependências do projeto \
├── .env |# Variáveis de ambiente \
├── model.pkl |# (Opcional) Modelo local de ML \
└── README.md |# Documentação do projeto


---

## Variáveis de Ambiente (.env)

Crie um arquivo `.env` na raiz do projeto com as seguintes variáveis:

```env
# Nome do bucket no Google Cloud Storage
BUCKET_NAME=meu-bucket-gcp

# Nome do arquivo do modelo dentro do bucket
MODEL_FILE_NAME=model.pkl

# Caminho local onde o modelo será salvo após o download
LOCAL_MODEL_PATH=./model.pkl

# Define se o modelo deve ser carregado localmente (True) ou baixado do GCS (False)
MODEL_LOCAL=False
````

* Caso MODEL_LOCAL=True, a API utilizará o arquivo local informado em MODEL_FILE_NAME.
* Caso MODEL_LOCAL=False, o modelo será baixado automaticamente do bucket do GCS.

### Instalação

Clone o repositório

```bash

git clone https://github.com/seuusuario/seuprojeto.git
cd seuprojeto
```
Crie um ambiente virtual

```bash

python3 -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows
```
Instale as dependências
```bash

pip install -r requirements.txt
````

Configure o acesso ao Google Cloud

Certifique-se de estar autenticado com uma conta que possua acesso ao bucket do GCS:

bash

gcloud auth application-default login
🚀 Execução da API
Execute o servidor Flask:

bash

python app.py
Por padrão, o servidor iniciará em:

cpp

http://127.0.0.1:5000/
🧠 Estrutura do Código
🔹 Carregamento do Modelo
O modelo é carregado automaticamente com base na configuração:

Se MODEL_LOCAL=True, o modelo é lido localmente.

Caso contrário, a função download_model() baixa o arquivo do GCS usando google.cloud.storage.

🔹 Features esperadas
A API espera as seguintes colunas de entrada:

| Coluna | Tipo | Descrição |
| -------|------|-----------|
| Model | string| Nome do modelo do veículo |
|Year	|int| Ano de fabricação| 
|Region	|string| 	Região de venda|
|Color	|string| 	Cor do veículo|
|Fuel_Type|string| Tipo de combustível|
|Transmission|string| 	Tipo de transmissão|
|Engine_Size_L|float| 	Tamanho do motor (em litros)|
|Mileage_KM|int	| Quilometragem|
|Price_USD|float| Preço do veículo em dólares|

## Endpoints
POST /predict
🔹 Descrição
Recebe um JSON com os atributos de um veículo e retorna a predição e as probabilidades associadas.

🔹 Exemplo de Request
```bash
curl -X POST http://127.0.0.1:5000/predict \
     -H "Content-Type: application/json" \
     -d '{
        "input": {
            "Model": "Toyota Corolla",
            "Year": 2018,
            "Region": "South",
            "Color": "White",
            "Fuel_Type": "Gasoline",
            "Transmission": "Automatic",
            "Engine_Size_L": 1.8,
            "Mileage_KM": 35000,
            "Price_USD": 15000
        }
     }'
```

🔹 Exemplo de Response
```json
{
  "input": {
    "Model": "Toyota Corolla",
    "Year": 2018,
    "Region": "South",
    "Color": "White",
    "Fuel_Type": "Gasoline",
    "Transmission": "Automatic",
    "Engine_Size_L": 1.8,
    "Mileage_KM": 35000,
    "Price_USD": 15000
  },
  "prediction": [1],
  "probabilities": [[0.25, 0.75]]
}
```

## Possíveis Erros

|Código|Motivo|
|---|---|
|400|Campo "input" ausente no JSON|
|400|Faltam campos obrigatórios|
|500|Erro interno ao carregar ou processar o modelo|


## Dependências Principais
Pacote	Função
flask	Framework web para criação da API
joblib	Carregamento do modelo de Machine Learning
pandas	Manipulação dos dados de entrada
python-dotenv	Leitura das variáveis de ambiente
google-cloud-storage	Download do modelo armazenado no GCS

## Exemplo de requirements.txt
```txt
flask==3.0.3
joblib==1.4.2
pandas==2.2.3
python-dotenv==1.0.1
google-cloud-storage==2.18.2
````
