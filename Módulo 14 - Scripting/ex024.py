# bibliotecas necessárias
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import os

sns.set_theme()

# função de plotagem
def plota_pivot_table(df, value, index, func, ylabel, xlabel, opcao='nada'):
    if opcao == 'nada':
        pd.pivot_table(df, values=value, index=index, aggfunc=func).plot(figsize=[15, 5])
    elif opcao == 'sort':
        pd.pivot_table(df, values=value, index=index, aggfunc=func).sort_values(value).plot(figsize=[15, 5])
    elif opcao == 'unstack':
        pd.pivot_table(df, values=value, index=index, aggfunc=func).unstack().plot(figsize=[15, 5])
    plt.ylabel(ylabel)
    plt.xlabel(xlabel)

# arquivos para os meses desejados
meses = ['MAR', 'ABR', 'MAI', 'JUN', 'DEZ']
caminho_base = r'C:\Users\earap\Documents\EBAC\DataScienceExcercises\Módulo 14 - Scripting\input\\'

# looping para processar todos os arquivos e gerar gráficos automaticamente
for mes in meses:
    sinasc = pd.read_csv(f'{caminho_base}SINASC_RO_2019_{mes}.csv')
    print(f'{mes}:', sinasc.DTNASC.min(), sinasc.DTNASC.max())

    # pasta de saída para salvar gráficos
    max_data = sinasc.DTNASC.max()[:7]
    os.makedirs(f'./output/figs/{max_data}', exist_ok=True)

    # gera e salvamento dos gráficos
    plota_pivot_table(sinasc, 'IDADEMAE', 'DTNASC', 'count', 'Quantidade de Nascimento', 'Data de Nascimento')
    plt.savefig(f'./output/figs/{max_data}/quantidade_de_nascimento.png')
    plt.close()

    plota_pivot_table(sinasc, 'IDADEMAE', ['DTNASC', 'SEXO'], 'mean', 'Média Idade Mãe', 'Data de Nascimento', 'unstack')
    plt.savefig(f'./output/figs/{max_data}/media_idade_mae_por_sexo.png')
    plt.close()

    plota_pivot_table(sinasc, 'PESO', ['DTNASC', 'SEXO'], 'mean', 'Média Peso Bebê', 'Data de Nascimento', 'unstack')
    plt.savefig(f'./output/figs/{max_data}/media_peso_bebe_por_sexo.png')
    plt.close()

    plota_pivot_table(sinasc, 'APGAR1', 'GESTACAO', 'mean', 'Média APGAR1', 'Gestação', 'sort')
    plt.savefig(f'./output/figs/{max_data}/media_apgar1_por_gestacao.png')
    plt.close()

    plota_pivot_table(sinasc, 'APGAR5', 'GESTACAO', 'mean', 'Média APGAR5', 'Gestação', 'sort')
    plt.savefig(f'./output/figs/{max_data}/media_apgar5_por_gestacao.png')
    plt.close()

# final
print("Gráficos gerados e salvos com sucesso!")