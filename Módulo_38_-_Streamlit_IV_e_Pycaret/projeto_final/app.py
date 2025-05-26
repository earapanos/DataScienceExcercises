import streamlit as st
import pandas as pd
import numpy as np
import urllib.request
import os
from pycaret.classification import load_model

# Título
st.title("Credit Scoring - Streamlit App")
st.markdown("Upload um arquivo `.csv` para escoragem com o modelo treinado.")

# Upload de arquivo
uploaded_file = st.file_uploader("Escolha um arquivo CSV", type="csv")

# Carregar o modelo treinado com cache
@st.cache_resource
def load_model_from_url():
    url = "https://raw.githubusercontent.com/earapanos/DataScienceExcercises/main/M%C3%B3dulo_38_-_Streamlit_IV_e_Pycaret/projeto_final/modelo_credit_scoring_lgbm.pkl"
    filename = "modelo_credit_scoring_lgbm.pkl"
    if not os.path.exists(filename):
        urllib.request.urlretrieve(url, filename)
    return load_model(filename)

model = load_model_from_url()

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
