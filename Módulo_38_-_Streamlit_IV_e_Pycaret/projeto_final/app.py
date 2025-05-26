# app.py

import streamlit as st
import pandas as pd
import numpy as np
import joblib
from sklearn.pipeline import Pipeline

# Título
st.title("Credit Scoring - Streamlit App")
st.markdown("Upload um arquivo `.csv` para escoragem com o modelo treinado.")

# Upload de arquivo
uploaded_file = st.file_uploader("Escolha um arquivo CSV", type="csv")

# Carregar o modelo treinado
@st.cache_resource
def load_model(path='modelo_credit_scoring_lgbm.pkl'):
    return joblib.load(path)

model = load_model()

# Carregar e processar os dados
if uploaded_file is not None:
    try:
        df_input = pd.read_csv(uploaded_file)

        st.subheader("Prévia dos dados carregados:")
        st.dataframe(df_input.head())

        # Verificação básica das colunas esperadas
        expected_columns = ['sexo', 'posse_de_veiculo', 'posse_de_imovel', 'qtd_filhos', 
                            'idade', 'tempo_emprego', 'qt_pessoas_residencia', 'renda',
                            'educacao', 'estado_civil', 'tipo_residencia']
        
        missing_cols = [col for col in expected_columns if col not in df_input.columns]
        if missing_cols:
            st.error(f"As colunas a seguir estão faltando no arquivo CSV: {missing_cols}")
        else:
            # Fazer escoragem
            predictions = model.predict(df_input)
            probabilities = model.predict_proba(df_input)[:, 1]  # probabilidade de ser 'mau'
            
            # Adicionar resultados ao dataframe
            df_input['probabilidade_mau'] = probabilities
            df_input['previsao_mau'] = predictions

            st.subheader("Resultados da Escoragem:")
            st.dataframe(df_input[['probabilidade_mau', 'previsao_mau']].head())

            # Baixar resultado
            csv_result = df_input.to_csv(index=False).encode('utf-8')
            st.download_button(
                label="📥 Baixar resultados como CSV",
                data=csv_result,
                file_name='resultado_escoragem.csv',
                mime='text/csv'
            )
    except Exception as e:
        st.error(f"Erro ao processar o arquivo: {e}")