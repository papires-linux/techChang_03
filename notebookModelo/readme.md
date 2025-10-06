# Documentação Completa do Notebook

"""
Este notebook realiza uma análise exploratória e modelagem preditiva dos dados de vendas de carros da BMW.

## Etapas do notebook:

1. **Introdução e Descrição dos Dados**
    - Apresentação do objetivo e contexto dos dados de vendas da BMW.

2. **Importação de Bibliotecas**
    - Importação das principais bibliotecas para análise de dados, visualização e machine learning.

3. **Coleta dos Dados**
    - Extração dos dados do BigQuery para um DataFrame pandas.

4. **Análise Exploratória dos Dados**
    - Visualização das primeiras e últimas linhas do dataset.
    - Análise de tipos de dados, valores ausentes, duplicados e estatísticas descritivas.
    - Visualização gráfica dos dados: vendas por ano, distribuição regional, preços, tipos de combustível e transmissão, correlação entre variáveis, etc.

5. **Refinamento e Salvamento dos Dados**
    - Salvamento da tabela refinada no BigQuery para futuras análises.

6. **Pré-processamento dos Dados**
    - Codificação de variáveis categóricas usando LabelEncoder.
    - Salvamento dos mapeamentos de codificação no BigQuery.

7. **Divisão dos Dados**
    - Separação dos dados em conjuntos de treino e teste para modelagem.

8. **Modelagem Preditiva**
    - Treinamento e avaliação de diversos modelos de classificação (Decision Tree, Random Forest, Gradient Boosting, AdaBoost, KNN, SVM, Naive Bayes, XGBoost, Logistic Regression).
    - Comparação das acurácias dos modelos.

9. **Persistência do Modelo**
    - Salvamento do modelo escolhido em formato .pkl.
    - Backup do modelo anterior no bucket do Google Cloud Storage.
    - Upload do novo modelo treinado para o bucket.

## Observações:
- O notebook utiliza recursos do Google Cloud Platform (BigQuery e Cloud Storage).
- Todos os passos são automatizados para facilitar a reprodutibilidade e versionamento dos dados e modelos.
- As visualizações auxiliam na compreensão dos padrões de vendas e características dos veículos.

## Dependências:
- pandas, seaborn, matplotlib, scikit-learn, xgboost, joblib, google-cloud-storage

"""