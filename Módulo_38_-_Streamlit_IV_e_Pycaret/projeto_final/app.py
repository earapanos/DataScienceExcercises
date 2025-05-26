# Imports adicionais necessários
import requests
import os

# Função para baixar arquivos do GitHub
def download_file_from_github(url, local_filename):
    response = requests.get(url)
    if response.status_code == 200:
        with open(local_filename, 'wb') as f:
            f.write(response.content)
        return True
    return False

# URLs dos modelos no GitHub
MODEL_URLS = {
    "lightgbm": "https://github.com/earapanos/DataScienceExcercises/raw/main/M%C3%B3dulo_38_-_Streamlit_IV_e_Pycaret/projeto_final/model_final.pkl",
    "logistic": "https://github.com/earapanos/DataScienceExcercises/raw/main/M%C3%B3dulo_38_-_Streamlit_IV_e_Pycaret/projeto_final/model_regressao_logistica.pkl"
}

# Função principal modificada
def main():
    # Título da aplicação
    st.write("## Escorando o modelo gerado no PyCaret ou Scikit-learn")
    st.markdown("---")

    # Baixar modelos se não existirem
    if not os.path.exists('model_final.pkl'):
        st.info("Baixando modelo LightGBM...")
        if download_file_from_github(MODEL_URLS['lightgbm'], 'model_final.pkl'):
            st.success("Modelo LightGBM baixado com sucesso!")
        else:
            st.error("Falha ao baixar o modelo LightGBM")
            return

    if not os.path.exists('model_regressao_logistica.pkl'):
        st.info("Baixando modelo de Regressão Logística...")
        if download_file_from_github(MODEL_URLS['logistic'], 'model_regressao_logistica.pkl'):
            st.success("Modelo de Regressão Logística baixado com sucesso!")
        else:
            st.error("Falha ao baixar o modelo de Regressão Logística")
            return

    # Restante do seu código original...
    st.sidebar.write("## Suba o arquivo")
    data_file_1 = st.sidebar.file_uploader("Bank Credit Dataset", type=['csv', 'ftr'])

    st.sidebar.write("## Escolha o modelo")
    model_choice = st.sidebar.selectbox(
        "Escolha o modelo que deseja utilizar",
        options=["LightGBM (PyCaret)", "Regressão Logística (sklearn)"]
    )

    if data_file_1 is not None:
        df_credit = pd.read_feather(data_file_1)
        df_credit = df_credit.sample(50000)

        if model_choice == "LightGBM (PyCaret)":
            try:
                model_saved = load_model('model_final')
                predict = predict_model(model_saved, data=df_credit)
            except Exception as e:
                st.error(f"Erro ao carregar o modelo LightGBM: {str(e)}")
                return

        elif model_choice == "Regressão Logística (sklearn)":
            try:
                pipeline = joblib.load('model_regressao_logistica.pkl')
                predict = pipeline.predict(df_credit)
                predict = pd.DataFrame(predict, columns=['Previsão'])
            except Exception as e:
                st.error(f"Erro ao carregar o modelo de Regressão Logística: {str(e)}")
                return

        df_xlsx = to_excel(predict)
        st.download_button(label='📥 Download', data=df_xlsx, file_name='predict.xlsx')

if __name__ == '__main__':
    main()