import subprocess
import sys

def install(package):
    subprocess.check_call([sys.executable, "-m", "pip", "install", package])

# Install seaborn if not already installed
install("seaborn==0.13.2")

import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import streamlit as st

# Function to Filter the DataFrame
@st.cache_data
def filter(df):
    ''' Function to filter the information in the DataFrame '''
    df = df.drop(['Unnamed: 0', 'id_cliente'], axis=1)
    df['data_ref'] = pd.to_datetime(df['data_ref'])
    df_new = df.dropna().reset_index(drop=True)
    return df_new

# Function to Create All Stability Plots
@st.cache_data
def point(_df):
    ''' Receives a DataFrame, filters the categorical variables, and returns
    all point plots of average income over time for the distribution of variables in the list '''
    var_qualitativo = _df.select_dtypes(exclude=['int64', 'float64', 'datetime']).columns

    for var in var_qualitativo:
        st.markdown(f'#### Stability of the explanatory variable {var} over time:')
        fig, ax = plt.subplots(figsize=(20, 5))
        sns.pointplot(data=previsao_renda_filter,
                      x='data_ref',
                      y='renda',
                      hue=var,
                      dodge=True,
                      errorbar=('ci', 95),
                      ax=ax)
        tick_data = previsao_renda_filter['data_ref'].map(lambda data: data.strftime('%m/%Y')).unique()
        tick_data.tolist()
        ticks = ax.set_xticks(list(range(previsao_renda_filter['data_ref'].nunique())))
        labels = ax.set_xticklabels(tick_data, rotation=45)
        plt.xlabel('Time')
        plt.ylabel('Average Income ($)')
        plt.legend(bbox_to_anchor=(1.05, 1),
                   loc=2,
                   borderaxespad=0,
                   title=var.capitalize())
        st.pyplot(fig)

# Function to Create a Single Stability Plot
def point_unico(_var: str):
    ''' Receives a string of a categorical variable and returns
    a point plot of average income over time for the distribution of the variable '''
    if _var == 'sexo':
        st.markdown(f'#### Stability of the explanatory variable {_var} over time:')
    elif _var == 'posse_de_veiculo':
        st.markdown(f'#### Stability of the explanatory variable {_var} over time:')
    elif _var == 'posse_de_imovel':
        st.markdown(f'#### Stability of the explanatory variable {_var} over time:')
    elif _var == 'tipo_renda':
        st.markdown(f'#### Stability of the explanatory variable {_var} over time:')
    elif _var == 'educacao':
        st.markdown(f'#### Stability of the explanatory variable {_var} over time:')
    elif _var == 'estado_civil':
        st.markdown(f'#### Stability of the explanatory variable {_var} over time:')
    elif _var == 'tipo_residencia':
        st.markdown(f'#### Stability of the explanatory variable {_var} over time:')

    fig, ax = plt.subplots(figsize=(20, 5))
    sns.pointplot(data=previsao_renda_filter,
                  x='data_ref',
                  y='renda',
                  hue=_var,
                  dodge=True,
                  errorbar=('ci', 95),
                  ax=ax)
    tick_data = previsao_renda_filter['data_ref'].map(lambda data: data.strftime('%m/%Y')).unique()
    tick_data.tolist()
    ticks = ax.set_xticks(list(range(previsao_renda_filter['data_ref'].nunique())))
    labels = ax.set_xticklabels(tick_data, rotation=45)
    plt.xlabel('Time')
    plt.ylabel('Average Income ($)')
    plt.legend(bbox_to_anchor=(1.05, 1),
               loc=2,
               borderaxespad=0,
               title=_var.capitalize())
    st.pyplot(fig)

def hist(_var: str):
    if _var == 'renda':
        st.markdown(f'##### Distribution of the quantitative variable {_var}:')
    elif _var == 'qtd_filhos':
        st.markdown(f'##### Distribution of the quantitative variable {_var}:')
    elif _var == 'idade':
        st.markdown(f'##### Distribution of the quantitative variable {_var}:')
    elif _var == 'tempo_emprego':
        st.markdown(f'##### Distribution of the quantitative variable {_var}:')
    elif _var == 'qt_pessoas_residencia':
        st.markdown(f'##### Distribution of the quantitative variable {_var}:')

    fig, ax = plt.subplots(figsize=(20, 5))
    sns.histplot(previsao_renda_filter,
                 x=_var,
                 kde=True)
    plt.ylabel('Count')
    st.pyplot(fig)

@st.cache_data
def hist_todos(_df: pd.DataFrame):
    var_quantitativo = _df.select_dtypes(exclude=['bool', 'object', 'datetime']).columns

    for var in var_quantitativo:
        st.markdown(f'##### Distribution of the quantitative variable {var}:')
        fig, ax = plt.subplots(figsize=(20, 5))
        sns.histplot(_df,
                     x=var,
                     kde=True)
        plt.ylabel('Count')
        st.pyplot(fig)

# Page Configuration
st.set_page_config(page_title='Exploratory Analysis',
                   page_icon='https://cdn-icons-png.freepik.com/512/8649/8649621.png',
                   layout='wide')

# Reading the DataFrame
previsao_renda = pd.read_csv('./input/previsao_de_renda.csv')
# Filtering the DataFrame
previsao_renda_filter = filter(previsao_renda)

metadados = pd.DataFrame({'dtypes': previsao_renda_filter.dtypes})  # Create the metadata DataFrame
metadados['missing'] = previsao_renda_filter.isna().sum()
metadados['perc_missing'] = round((metadados['missing'] / previsao_renda_filter.shape[0]) * 100)
metadados['valores_unicos'] = previsao_renda_filter.nunique()

st.title('Exploratory Analysis for Income Prediction:')
st.markdown('----')

left_column, right_column = st.columns(2)  # Create two columns

with left_column:  # Use the left column
    st.markdown('#### DataFrame used:')
    st.markdown('Complete interactive DataFrame.')
    if st.checkbox('Show DataFrame'):  # Show the DataFrame when the checkbox is selected
        previsao_renda_filter  # Display the DataFrame with magic

with right_column:  # Use the right column
    st.markdown('#### DataFrame Metadata:')
    st.markdown('The DataFrame below contains the metadata of all variables in the DataFrame used.')
    if st.checkbox('Show DataFrame Metadata'):  # Show the metadata DataFrame when the checkbox is selected
        metadados  # Display the DataFrame with magic
st.markdown('----')

st.markdown('### Distribution Plots of Qualitative Variables Over Time:')
st.markdown('''For the following plots, the X-axis represents the analyzed time, and the Y-axis can vary between a total count,
            an overlaid count, or the normalized percentage.''')
st.markdown(' ')

st.sidebar.markdown('### Distribution Plots of Qualitative Variables Over Time:')

if st.sidebar.checkbox('Show all variables'):  # Graphical visualization of all filtered categorical variables
    var_qualitativo = previsao_renda_filter.select_dtypes(exclude=['int64', 'float64', 'datetime']).columns  # Filter categorical variables
    chosen_comp = st.sidebar.radio(  # Options for viewing the plots
        'Choose how to view the distributions:',
        ('Stacked', 'Overlaid', 'Percentage')
    )
    st.sidebar.markdown('----')

    # Translate from Portuguese to English in the sidebar
    if chosen_comp == 'Stacked':
        chosen_comp = 'center'
    elif chosen_comp == 'Overlaid':
        chosen_comp = 'layered'
    elif chosen_comp == 'Percentage':
        chosen_comp = 'normalize'

    for var in var_qualitativo:  # Loop to create all plots
        tab_freq = pd.crosstab(previsao_renda_filter['data_ref'], previsao_renda_filter[var])
        st.markdown(f'#### Distribution of the explanatory variable {var} over time:')
        st.bar_chart(tab_freq, x_label='Date', y_label='Count', stack=chosen_comp)  # Interactive plot with Streamlit
    st.markdown('----')

else:  # Continue to configure only one plot
    var_qualitativo = previsao_renda_filter.select_dtypes(exclude=['int64', 'float64', 'datetime']).columns  # Filter categorical variables
    selectbox_var_comp = st.sidebar.selectbox(  # Select the variable to display
        'Choose the variable:',
        (var_qualitativo)
    )
    tab_freq = pd.crosstab(previsao_renda_filter['data_ref'], previsao_renda_filter[selectbox_var_comp])

    # Select the title to display
    if selectbox_var_comp == 'sexo':
        st.markdown(f'##### Distribution of the explanatory variable {selectbox_var_comp} over time:')
    elif selectbox_var_comp == 'posse_de_veiculo':
        st.markdown(f'##### Distribution of the explanatory variable {selectbox_var_comp} over time:')
    elif selectbox_var_comp == 'posse_de_imovel':
        st.markdown(f'##### Distribution of the explanatory variable {selectbox_var_comp} over time:')
    elif selectbox_var_comp == 'tipo_renda':
        st.markdown(f'##### Distribution of the explanatory variable {selectbox_var_comp} over time:')
    elif selectbox_var_comp == 'educacao':
        st.markdown(f'##### Distribution of the explanatory variable {selectbox_var_comp} over time:')
    elif selectbox_var_comp == 'estado_civil':
        st.markdown(f'##### Distribution of the explanatory variable {selectbox_var_comp} over time:')
    elif selectbox_var_comp == 'tipo_residencia':
        st.markdown(f'##### Distribution of the explanatory variable {selectbox_var_comp} over time:')

    chosen = st.sidebar.radio(  # Options for viewing the plots
        'Choose how to view the distribution:',
        ('Stacked', 'Overlaid', 'Percentage')
    )

    # Translate from Portuguese to English
    if chosen == 'Stacked':
        chosen = 'center'
    elif chosen == 'Overlaid':
        chosen = 'layered'
    elif chosen == 'Percentage':
        chosen = 'normalize'

    st.bar_chart(tab_freq, x_label='Date', y_label='Count', stack=chosen)  # Interactive plot with Streamlit

    if st.sidebar.checkbox('Compare with another variable?'):  # Option in the menu to compare with another variable
        var_qualitativo = previsao_renda_filter.select_dtypes(exclude=['int64', 'float64', 'datetime']).columns  # Filter categorical variables
        selectbox_var_comp = st.sidebar.selectbox(  # Select the variable to compare
            'Choose the variable:',
            (var_qualitativo)
        )
        tab_freq = pd.crosstab(previsao_renda_filter['data_ref'], previsao_renda_filter[selectbox_var_comp])

        # Select the title to display
        if selectbox_var_comp == 'sexo':
            st.markdown(f'##### Distribution of the explanatory variable {selectbox_var_comp} over time:')
        elif selectbox_var_comp == 'posse_de_veiculo':
            st.markdown(f'##### Distribution of the explanatory variable {selectbox_var_comp} over time:')
        elif selectbox_var_comp == 'posse_de_imovel':
            st.markdown(f'##### Distribution of the explanatory variable {selectbox_var_comp} over time:')
        elif selectbox_var_comp == 'tipo_renda':
            st.markdown(f'##### Distribution of the explanatory variable {selectbox_var_comp} over time:')
        elif selectbox_var_comp == 'educacao':
            st.markdown(f'##### Distribution of the explanatory variable {selectbox_var_comp} over time:')
        elif selectbox_var_comp == 'estado_civil':
            st.markdown(f'##### Distribution of the explanatory variable {selectbox_var_comp} over time:')
        elif selectbox_var_comp == 'tipo_residencia':
            st.markdown(f'##### Distribution of the explanatory variable {selectbox_var_comp} over time:')

        chosen_comp = st.sidebar.radio(  # Options for viewing the plots
            'Choose how to view the distribution: ',
            ('Stacked', 'Overlaid', 'Percentage')
        )

        # Translate from Portuguese to English
        if chosen_comp == 'Stacked':
            chosen_comp = 'center'
        elif chosen_comp == 'Overlaid':
            chosen_comp = 'layered'
        elif chosen_comp == 'Percentage':
            chosen_comp = 'normalize'

        st.bar_chart(tab_freq, x_label='Date', y_label='Count', stack=chosen_comp)  # Interactive plot with Streamlit

    st.markdown('----')
    st.sidebar.markdown('----')

st.markdown('### Stability Plots of Qualitative Variables Over Time:')
st.markdown('''For the following plots, the stability of the variables is analyzed.
            Using the variation of average income over time for the selected variable.''')
st.sidebar.markdown('### Stability Plots of Qualitative Variables Over Time:')

if st.sidebar.checkbox('Show all variables '):  # Graphical visualization of all filtered categorical variables
    point(previsao_renda_filter)  # Use the function to plot all stability plots of all filtered categorical variables in the DataFrame
else:
    var_qualitativo = previsao_renda_filter.select_dtypes(exclude=['int64', 'float64', 'datetime']).columns  # Filter categorical variables
    selectbox_var_est = st.sidebar.selectbox(  # Select the variable to display
        'Choose the variable: ',
        (var_qualitativo)
    )
    point_unico(selectbox_var_est)  # Use the function to plot the stability plot of the selected variable

    if st.sidebar.checkbox('Compare with another variable? '):  # Option in the menu to compare with another variable
        var_qualitativo = previsao_renda_filter.select_dtypes(exclude=['int64', 'float64', 'datetime']).columns  # Filter categorical variables
        selectbox_var_comp_est = st.sidebar.selectbox(  # Select the variable to compare
            'Choose the variable:',
            (var_qualitativo)
        )
        point_unico(selectbox_var_comp_est)  # Use the function to plot the stability plot of the selected variable for comparison

st.sidebar.markdown('----')
st.markdown('---')

st.markdown('### Distribution Plots of Quantitative Variables:')
st.sidebar.markdown('### Distribution Plots of Quantitative Variables:')

if st.sidebar.checkbox(' Show all variables '):  # Graphical visualization of all filtered categorical variables
    hist_todos(previsao_renda_filter)  # Use the function to plot all stability plots of all filtered categorical variables in the DataFrame
else:
    var_quantitativo = previsao_renda_filter.select_dtypes(exclude=['bool', 'object', 'datetime']).columns  # Filter quantitative variables
    selectbox_var_quant = st.sidebar.selectbox(  # Select the variable to display
        'Choose the variable: ',
        (var_quantitativo)
    )
    hist(selectbox_var_quant)  # Use the function to plot the stability plot of the selected variable

    if st.sidebar.checkbox(' Compare with another variable? '):  # Option in the menu to compare with another variable
        var_quantitativo = previsao_renda_filter.select_dtypes(exclude=['bool', 'object', 'datetime']).columns  # Filter quantitative variables
        selectbox_var_comp_quant = st.sidebar.selectbox(  # Select the variable to compare
            'Choose the variable:',
            (var_quantitativo)
        )
        hist(selectbox_var_comp_quant)  # Use the function to plot the stability plot of the selected variable for comparison

st.sidebar.button('Reload')