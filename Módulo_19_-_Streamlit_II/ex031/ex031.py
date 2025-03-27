import timeit
import streamlit as st
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from PIL import Image
import requests
from io import BytesIO

sns.set_theme(style='ticks',
              rc={'axes.spines.right': False,
                  'axes.spines.top': False})

# FUNÇÃO PARA CARREGAR OS DADOS
@st.cache_data
def load_data(file_data: str, sep: str) -> pd.DataFrame:
    return pd.read_csv(filepath_or_buffer=file_data, sep=sep)

def multiselect_filter(data: pd.DataFrame,
                      col: str,
                      selected: list[str]
                      ) -> pd.DataFrame:
    if 'all' in selected:
        return data
    else:
        return data[data[col].isin(selected)].reset_index(drop=True)

def load_image_from_url(url):
    try:
        response = requests.get(url)
        return Image.open(BytesIO(response.content))
    except:
        return None

def main():
    st.set_page_config(
        page_title="EBAC | Modulo 19 | Streamlit II | Exercicio 1",
        page_icon=":bank:",
        layout="wide",
        initial_sidebar_state="expanded",
    )

    # Carregar imagem do sidebar
    sidebar_image = load_image_from_url(
        "https://raw.githubusercontent.com/earapanos/DataScienceExcercises/refs/heads/main/M%C3%B3dulo_19_-_Streamlit_II/ex031/img/Bank-Branding.jpg"
    )
    if sidebar_image:
        st.sidebar.image(sidebar_image)

    # Título com imagem centralizada
    st.markdown('''
    <div style="text-align:center">
        <a href="https://github.com/earapanos/DataScienceExcercises.git">
            <img src="https://raw.githubusercontent.com/earapanos/DataScienceExcercises/refs/heads/main/M%C3%B3dulo_19_-_Streamlit_II/ex031/img/telmarketing_icon.png" alt="ebac_logo-data_science" width=100%>
        </a>
    </div>
    ---
    ### **Modulo 19** | Streamlit II | Exercicio 1
    **Aluno:** [Eduardo Adriani Rapanos](https://www.linkedin.com/in/eduardo-rapanos/)<br>
    **Data:** 03 de marco de 2025.
    ---
    ''', unsafe_allow_html=True)

    st.write('# Telemarketing analysis')
    st.markdown(body='---')

    start = timeit.default_timer()

    # Carregar dados
    bank_raw = load_data(
        file_data='https://media.githubusercontent.com/media/earapanos/DataScienceExcercises/refs/heads/main/M%C3%B3dulo_19_-_Streamlit_II/ex031/datainput/bank-additional-full.csv',
        sep=';'
    )
    bank = bank_raw.copy()

    st.write('Time:', timeit.default_timer() - start)

    st.write('## Antes dos filtros')
    st.write(bank_raw)
    st.write('Quantidade de linhas:', bank_raw.shape[0])
    st.write('Quantidade de colunas:', bank_raw.shape[1])

    with st.sidebar.form(key='my_form'):
        # Filtros
        min_age, max_age = min(bank['age']), max(bank['age'])
        idades = st.slider('Idade', min_age, max_age, (min_age, max_age), 1)

        filter_options = {
            'Profissoes': 'job',
            'Estado Civil': 'marital',
            'Default': 'default',
            'Tem financiamento imobiliario?': 'housing',
            'Tem emprestimo?': 'loan',
            'Meio de contato': 'contact',
            'Mes do contato': 'month',
            'Dia da semana do contato': 'day_of_week'
        }

        selected_values = {}
        for label, col in filter_options.items():
            options = bank[col].unique().tolist()
            options.append('all')
            selected_values[col] = st.multiselect(label, options, ['all'])

        submit_button = st.form_submit_button('Aplicar')

    # Aplicar filtros
    bank = bank.query('age >= @idades[0] and age <= @idades[1]')
    for col, selected in selected_values.items():
        bank = multiselect_filter(bank, col, selected)

    st.write('## Apos os filtros')
    st.write(bank)
    st.write('Quantidade de linhas:', bank.shape[0])
    st.write('Quantidade de colunas:', bank.shape[1])
    st.markdown('---')

    # Gráficos
    fig, axes = plt.subplots(1, 2, figsize=(12, 4))
    
    # Dados brutos
    bank_raw_pct = bank_raw['y'].value_counts(normalize=True) * 100
    sns.barplot(x=bank_raw_pct.index, y=bank_raw_pct.values, ax=axes[0])
    axes[0].set_title('Dados brutos', fontweight='bold')
    axes[0].bar_label(axes[0].containers[0])
    
    # Dados filtrados
    bank_pct = bank['y'].value_counts(normalize=True) * 100
    sns.barplot(x=bank_pct.index, y=bank_pct.values, ax=axes[1])
    axes[1].set_title('Dados filtrados', fontweight='bold')
    axes[1].bar_label(axes[1].containers[0])
    
    st.write('## Proporcao de aceite')
    st.pyplot(fig)

if __name__ == '__main__':
    main()