# app.py

import pandas as pd
import streamlit as st
import numpy as np
from datetime import datetime
from PIL import Image
from io import BytesIO
from pathlib import Path

# Função para converter df para CSV
@st.cache_data
def convert_df(df):
    return df.to_csv(index=False).encode('utf-8')

# Função para converter df para Excel
@st.cache_data
def to_excel(df):
    output = BytesIO()
    writer = pd.ExcelWriter(output, engine='xlsxwriter')
    df.to_excel(writer, index=False, sheet_name='Sheet1')
    writer.close()
    processed_data = output.getvalue()
    return processed_data

# Funções de classificação
def recencia_class(x, r, q_dict):
    if x <= q_dict[r][0.25]:
        return 'A'
    elif x <= q_dict[r][0.50]:
        return 'B'
    elif x <= q_dict[r][0.75]:
        return 'C'
    else:
        return 'D'

def freq_val_class(x, fv, q_dict):
    if x <= q_dict[fv][0.25]:
        return 'D'
    elif x <= q_dict[fv][0.50]:
        return 'C'
    elif x <= q_dict[fv][0.75]:
        return 'B'
    else:
        return 'A'

# Função principal
def main():
    st.set_page_config(
        page_title="EBAC | Módulo 31 | Streamlit V | Exercício 1",
        page_icon='📊',
        layout="wide",
        initial_sidebar_state="expanded",
    )

    # Título e introdução
    st.markdown("""
    ### **Módulo 31** | Streamlit V | Exercício 1  
    **Aluno:** [Eduardo Adriani Rapanos](https://www.linkedin.com/in/eduardo-rapanos/)<br>
    **Data:** 14 de novembro de 2025.
    ---
    """, unsafe_allow_html=True)

    st.write("""# RFV - Recência, Frequência, Valor
    Essa aplicação calcula o score RFV com base nas compras dos clientes.
    """)

    st.sidebar.image("https://raw.githubusercontent.com/rhatiro/Curso_EBAC-Profissao_Cientista_de_Dados/main/ebac-course-utils/media/logo/newebac_logo_black_half.png")
    st.sidebar.write("## Suba um arquivo")
    data_file_1 = st.sidebar.file_uploader("Selecione um arquivo .csv ou .xlsx", type=['csv', 'xlsx'])

    # Botão para carregar arquivo demonstrativo
    demo_path = Path('./input/dados.csv')
    if st.sidebar.button('Carregar Arquivo Demonstrativo'):
        if demo_path.exists():
            data_file_1 = demo_path.open('rb')
        else:
            st.sidebar.error('Arquivo ./input/dados.csv não encontrado.')

    # Processamento do arquivo
    if data_file_1 is not None:
        try:
            if hasattr(data_file_1, 'name') and data_file_1.name.endswith('.xlsx'):
                df_compras = pd.read_excel(data_file_1, parse_dates=['DiaCompra'])
            else:
                df_compras = pd.read_csv(data_file_1, parse_dates=['DiaCompra'])
        except Exception as e:
            st.error(f"Erro ao ler o arquivo: {e}")
            return

        # Recência
        dia_atual = df_compras['DiaCompra'].max()
        st.write('## Recência (R)')
        st.write('Dia máximo na base de dados:', dia_atual)

        df_recencia = df_compras.groupby(by='ID_cliente', as_index=False)['DiaCompra'].max()
        df_recencia.columns = ['ID_cliente', 'DiaUltimaCompra']
        df_recencia['Recencia'] = df_recencia['DiaUltimaCompra'].apply(lambda x: (dia_atual - x).days)
        df_recencia.drop('DiaUltimaCompra', axis=1, inplace=True)
        st.write(df_recencia.head())

        # Frequência
        st.write('## Frequência (F)')
        df_frequencia = df_compras[['ID_cliente', 'CodigoCompra']].groupby('ID_cliente').count().reset_index()
        df_frequencia.columns = ['ID_cliente', 'Frequencia']
        st.write(df_frequencia.head())

        # Valor
        st.write('## Valor (V)')
        df_valor = df_compras[['ID_cliente', 'ValorTotal']].groupby('ID_cliente').sum().reset_index()
        df_valor.columns = ['ID_cliente', 'Valor']
        st.write(df_valor.head())

        # Tabela RFV
        st.write('## Tabela RFV final')
        df_RF = df_recencia.merge(df_frequencia, on='ID_cliente')
        df_RFV = df_RF.merge(df_valor, on='ID_cliente')
        df_RFV.set_index('ID_cliente', inplace=True)
        st.write(df_RFV.head())

        # Segmentação
        st.write('## Segmentação utilizando o RFV')
        quartis = df_RFV.quantile(q=[0.25, 0.5, 0.75])
        st.write('Quartis:', quartis)

        df_RFV['R_quartil'] = df_RFV['Recencia'].apply(recencia_class, args=('Recencia', quartis))
        df_RFV['F_quartil'] = df_RFV['Frequencia'].apply(freq_val_class, args=('Frequencia', quartis))
        df_RFV['V_quartil'] = df_RFV['Valor'].apply(freq_val_class, args=('Valor', quartis))
        df_RFV['RFV_Score'] = df_RFV['R_quartil'] + df_RFV['F_quartil'] + df_RFV['V_quartil']

        st.write(df_RFV.head())
        st.write('## Contagem por grupo RFV')
        st.write(df_RFV['RFV_Score'].value_counts())

        st.write('#### Top clientes AAA')
        st.write(df_RFV[df_RFV['RFV_Score'] == 'AAA'].sort_values('Valor', ascending=False).head(10))

        # Estratégias de marketing
        st.write('### Ações de marketing/CRM sugeridas')
        dict_acoes = {
            'AAA': 'Enviar cupons, pedir indicação, amostras grátis.',
            'DDD': 'Churn provável - não fazer nada.',
            'DAA': 'Recuperar com cupons.',
            'CAA': 'Recuperar com cupons.',
        }
        df_RFV['acoes de marketing/crm'] = df_RFV['RFV_Score'].map(dict_acoes)
        st.write(df_RFV[['RFV_Score', 'acoes de marketing/crm']].head())

        # Download
        df_xlsx = to_excel(df_RFV.reset_index())
        st.download_button('📥 Baixar RFV em Excel', data=df_xlsx, file_name='RFV_.xlsx')

        st.write('## Ações por tipo de cliente')
        st.write(df_RFV['acoes de marketing/crm'].value_counts(dropna=False))

if __name__ == '__main__':
    main()