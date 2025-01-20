import streamlit as st
import pandas as pd

# Exemplo 1: Título e Texto
st.title("Minha Primeira Aplicação Streamlit")
st.write("Bem-vindo à minha aplicação!")

# Exemplo 2: Widgets Interativos
name = st.text_input("Qual é o seu nome?")
st.write(f"Olá, {name}!")

# Exemplo 3: Slider
age = st.slider("Quantos anos você tem?", 0, 100)
st.write(f"Você tem {age} anos.")

# Exemplo 4: Botão
if st.button("Clique aqui"):
    st.write("Botão clicado!")

# Exemplo 5: Checkbox
if st.checkbox("Mostrar/Ocultar"):
    st.write("Checkbox marcado!")

# Exemplo 6: Selectbox
option = st.selectbox("Escolha uma opção", ["Opção 1", "Opção 2", "Opção 3"])
st.write(f"Você escolheu: {option}")

# Exemplo 7: Multiselect
options = st.multiselect("Escolha várias opções", ["Opção A", "Opção B", "Opção C"])
st.write(f"Você escolheu: {options}")

# Exemplo 8: Radio Button
choice = st.radio("Escolha uma opção", ["Opção X", "Opção Y", "Opção Z"])
st.write(f"Você escolheu: {choice}")

# Exemplo 9: File Uploader
uploaded_file = st.file_uploader("Escolha um arquivo")
if uploaded_file is not None:
    st.write("Arquivo carregado com sucesso!")

# Exemplo 10: Dataframe
data = {'Coluna 1': [1, 2, 3], 'Coluna 2': [4, 5, 6]}
df = pd.DataFrame(data)
st.write("DataFrame:")
st.write(df)

# Exemplo 11: Gráfico de Linha
st.line_chart(df)

# Exemplo 12: Gráfico de Barras
st.bar_chart(df)

# Exemplo 13: Gráfico de Área
st.area_chart(df)

# Exemplo 14: Mapas
map_data = pd.DataFrame({'lat': [37.76, 37.77], 'lon': [-122.4, -122.41]})
st.map(map_data)

# Exemplo 15: Caching
@st.cache
def expensive_computation(a, b):
    return a + b

result = expensive_computation(1, 2)
st.write(f"Resultado: {result}")

# Exemplo 16: Session State
if 'counter' not in st.session_state:
    st.session_state.counter = 0

if st.button("Incrementar"):
    st.session_state.counter += 1

st.write(f"Contador: {st.session_state.counter}")

# Exemplo 17: Markdown
st.markdown("### Este é um título Markdown")
st.markdown("Este é um **texto em negrito**.")

# Exemplo 18: LaTeX
st.latex(r"\sqrt{a^2 + b^2}")

# Exemplo 19: Colunas
col1, col2 = st.columns(2)
with col1:
    st.write("Coluna 1")
with col2:
    st.write("Coluna 2")

# Exemplo 20: Expander
with st.expander("Clique para expandir"):
    st.write("Conteúdo expandido!")