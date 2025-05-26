import pandas as pd
import numpy as np
import streamlit as st
from pycaret.classification import load_model, predict_model
from io import BytesIO
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import StandardScaler, FunctionTransformer
from sklearn.decomposition import PCA
from sklearn.pipeline import Pipeline
from typing import Tuple, List

# Configurações globais
SAMPLE_SIZE = 50000
N_FEATURES = 8
N_COMPONENTS = 5
MODELS = {
    'LightGBM': 'Final_LightGBM_Model_20250315',
    'Regressão Logística': 'model_final_pipe'
}

# Cache das funções de conversão
@st.cache_data
def convert_to_format(df: pd.DataFrame, format: str = 'csv') -> bytes:
    """Converte DataFrame para CSV ou Excel."""
    if format == 'csv':
        return df.to_csv(index=False).encode('utf-8')
    
    output = BytesIO()
    with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
        df.to_excel(writer, index=False, sheet_name='Sheet1')
    return output.getvalue()

class DataPreprocessor:
    @staticmethod
    def clean_data(df: pd.DataFrame) -> pd.DataFrame:
        """Remove nulos e outliers."""
        df = df.dropna()
        
        for col in df.select_dtypes(include=[np.number]).columns:
            Q1, Q3 = df[col].quantile([0.25, 0.75])
            IQR = Q3 - Q1
            mask = (df[col] >= (Q1 - 1.5 * IQR)) & (df[col] <= (Q3 + 1.5 * IQR))
            df = df[mask]
        
        return df

    @staticmethod
    def feature_engineering(df: pd.DataFrame) -> Tuple[pd.DataFrame, pd.Series]:
        """Prepara features para modelagem."""
        y = df['mau']
        X = pd.get_dummies(df.drop(columns=['mau']), drop_first=True)
        
        # Seleção de features
        rf = RandomForestClassifier(n_jobs=-1)
        rf.fit(X, y)
        top_features = pd.Series(rf.feature_importances_, index=X.columns)\
                        .nlargest(N_FEATURES)\
                        .index
        X = X[top_features]
        
        # PCA
        scaler = StandardScaler()
        pca = PCA(n_components=N_COMPONENTS)
        X_pca = pca.fit_transform(scaler.fit_transform(X))
        X_transformed = pd.DataFrame(
            X_pca, 
            columns=[f'PC{i+1}' for i in range(N_COMPONENTS)]
        )
        
        return X_transformed, y

    def process(self, df: pd.DataFrame) -> pd.DataFrame:
        """Pipeline completo de preprocessamento."""
        df = self.clean_data(df)
        X_transformed, y = self.feature_engineering(df)
        X_transformed['mau'] = y.reset_index(drop=True)
        return X_transformed

def create_footer():
    """Cria o footer da aplicação."""
    return """
        <style>
            footer {
                position: fixed;
                bottom: 0;
                left: 0;
                width: 100%;
                background-color: #f0f2f6;
                padding: 10px;
                text-align: center;
                font-size: 14px;
            }
        </style>
        <footer>
            <p>Projeto EBAC - Ciência de Dados | Alex Silva de Assunção</p>
        </footer>
    """

def main():
    # Configuração da página
    st.set_page_config(
        page_title='Credit Scoring - PyCaret',
        layout="wide",
        initial_sidebar_state='expanded'
    )

    # Interface principal
    st.write("## Credit Scoring com Pycaret")
    st.write("Faça o upload dos dados e escolha o modelo a ser ajustado ao lado.")
    st.markdown("---")

    # Sidebar
    with st.sidebar:
        st.write("## Suba o arquivo")
        data_file = st.file_uploader("Bank Credit Dataset", type=['csv', 'ftr'])
        model_choice = st.selectbox("Escolha o modelo", list(MODELS.keys()))
        start_analysis = st.button("Analyze!")

    # Footer
    st.markdown(create_footer(), unsafe_allow_html=True)

    if data_file is not None:
        try:
            # Carregamento e preparação dos dados
            df_credit = pd.read_feather(data_file)
            df_credit = df_credit.drop(columns=['data_ref', 'index'])\
                                .sample(SAMPLE_SIZE)
            
            st.write("Dados originais:")
            st.write(df_credit.head())

            if start_analysis:
                # Preprocessamento
                preprocessor = DataPreprocessor()
                df_transformed = preprocessor.process(df_credit)
                st.write("Dados transformados:", df_transformed.head())

                # Predição
                model = load_model(MODELS[model_choice])
                if model_choice == 'LightGBM':
                    predictions = predict_model(model, data=df_credit.drop(columns='mau'))
                else:
                    y_pred = model.predict(df_transformed.drop(columns='mau'))
                    predictions = df_credit.copy()
                    predictions['Prediction'] = y_pred

                st.write("Previsões:", predictions.head())
                
                # Download
                excel_file = convert_to_format(predictions, 'excel')
                st.download_button(
                    label='📥 Download',
                    data=excel_file,
                    file_name='predictions.xlsx'
                )

        except Exception as e:
            st.error(f"Erro durante o processamento: {e}")

if __name__ == '__main__':
    main()










