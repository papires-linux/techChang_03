from flask import Flask, request, jsonify
import joblib
import os
from dotenv import load_dotenv
from google.cloud import storage
import pandas as pd

# Carrega as variáveis de ambiente do arquivo .env
load_dotenv()

# Parâmetros do GCS
BUCKET_NAME = os.getenv("BUCKET_NAME")
MODEL_FILE_NAME = os.getenv("MODEL_FILE_NAME")
LOCAL_MODEL_PATH = os.getenv("LOCAL_MODEL_PATH")

# Defina como True se estiver rodando localmente
MODEL_IS_LOCAL = os.getenv("MODEL_LOCAL", False)
MODEL_IS_LOCAL = bool(MODEL_IS_LOCAL.lower() == 'true')

# Função para baixar o modelo do GCS
def download_model():
    client = storage.Client()
    print("Bucket Name: ", BUCKET_NAME)
    bucket = client.bucket(BUCKET_NAME)
    blob = bucket.blob(f"{MODEL_FILE_NAME}")
    blob.download_to_filename(LOCAL_MODEL_PATH)
    print(f"Modelo baixado para {LOCAL_MODEL_PATH}")

print("Iniciando a API..." )

if not MODEL_IS_LOCAL:
    print("Baixando o modelo do GCS...")
    download_model()
else:
    print("Usando o modelo local...")
    LOCAL_MODEL_PATH = MODEL_FILE_NAME
model = joblib.load(LOCAL_MODEL_PATH)

FEATURE_COLUMNS = [
    "Model",
    "Year",
    "Region",
    "Color",
    "Fuel_Type",
    "Transmission",
    "Engine_Size_L",
    "Mileage_KM",
    "Price_USD"
    
]

app = Flask(__name__)

@app.route("/predict", methods=["POST"])
def predict():
    data = request.get_json()

    if "input" not in data:
        return jsonify({"error": "Campo 'input' ausente no JSON."}), 400

    input_dict = data["input"]

    # Verifica se faltam colunas
    missing = [col for col in FEATURE_COLUMNS if col not in input_dict]
    if missing:
        return jsonify({"error": f"Faltam campos obrigatórios: {missing}"}), 400

    # Cria DataFrame com as features na ordem correta
    X_input = pd.DataFrame([[input_dict[col] for col in FEATURE_COLUMNS]], columns=FEATURE_COLUMNS)

    # Faz a previsão
    pred = model.predict(X_input)
    probs = model.predict_proba(X_input).tolist()

    return jsonify({
        "input": input_dict,
        "prediction": pred.tolist(),
        "probabilities": probs
    })

if __name__ == "__main__":
    app.run(debug=True)
