# Imports
import pandas as pd
import streamlit as st
from io import BytesIO
from pycaret.classification import load_model, predict_model

# Função para converter DataFrame em Excel
@st.cache_data
def to_excel(df):
    output = BytesIO()
    with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
        df.to_excel(writer, index=False, sheet_name='Resultados')
    processed_data = output.getvalue()
    return processed_data

# Função principal
def main():
    # Configuração da página
    st.set_page_config(page_title='Credit Scoring - PyCaret', layout="centered")

    st.title("🏦 Credit Scoring com PyCaret")
    st.markdown("Faça upload de um arquivo `.csv` para aplicar o modelo.")

    # Upload do arquivo CSV
    uploaded_file = st.file_uploader("📄 Upload do CSV", type=["csv"])

    if uploaded_file is not None:
        try:
            df = pd.read_csv(uploaded_file)
            st.success("Arquivo carregado com sucesso!")
            st.dataframe(df.head())

            # Carregar modelo treinado
            model = load_model("modelo_credit_scoring_lgbm.pkl")

            # Aplicar predições
            results = predict_model(model, data=df)

            # Mostrar resultados
            st.subheader("🔍 Resultados da Escoragem")
            st.dataframe(results[['prediction_label', 'prediction_score']].head())

            # Botão de download
            df_xlsx = to_excel(results)
            st.download_button(label="📥 Baixar resultados em Excel",
                               data=df_xlsx,
                               file_name="resultado_credit_scoring.xlsx")
        except Exception as e:
            st.error(f"Ocorreu um erro: {e}")

if __name__ == "__main__":
    main()