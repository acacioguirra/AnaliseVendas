import pandas as pd
from pathlib import Path
import streamlit as st
import plotly.express as px

st.set_page_config(
    layout="wide",
    page_title="Produtos X Vendedores",
    page_icon="👨‍💻"
)

PERCENTUAL_COMISSAO = 0.08

pasta_datasets = Path(__file__).parent.parent / 'datasets'
df_vendas = pd.read_csv(pasta_datasets / 'vendas.csv', decimal=',', sep=';', index_col=0)
df_filiais = pd.read_csv(pasta_datasets / 'filiais.csv', decimal=',', sep=';', index_col=0)
df_produtos = pd.read_csv(pasta_datasets / 'produtos.csv', decimal=',', sep=';', index_col=0)

df_produtos = df_produtos.rename(columns={'nome': 'produto'})

df_vendas = pd.merge(left=df_vendas, right=df_produtos, on='produto', how='left')
df_vendas = df_vendas.set_index('data')
df_vendas = df_vendas.drop(columns=df_vendas.columns[6])

df_vendas['comissao'] = df_vendas['preco'] * PERCENTUAL_COMISSAO

COLUNAS_ANALISE = ['filial', 'vendedor', 'produto', 'cliente_genero', 'forma_pagamento']
COLUNAS_NUMERICAS = ['preco', 'comissao']
AGREGACAO = {'soma' : 'sum', 'contagem': 'count'}

col11, col12 = st.sidebar.columns(2)
indice_dinamica = col11.multiselect('Selecione os indices:', COLUNAS_ANALISE)

colunas_filtradas = []
for c in COLUNAS_ANALISE:
    if not c in indice_dinamica:
        colunas_filtradas.append(c)

coluna_dinamica = col12.multiselect('Selecione as colunas:', colunas_filtradas)
st.sidebar.divider()
col21, col22 = st.sidebar.columns(2)

valor_analise = col21.selectbox('Selecione o valor da análise: ',
COLUNAS_NUMERICAS)

metrica_analise = col22.selectbox('Selecione a métrica: ',
list(AGREGACAO.keys())
)

if len(indice_dinamica) > 0 and len(coluna_dinamica) > 0:
    metrica = AGREGACAO[metrica_analise]
    vendas_dinamica = pd.pivot_table(df_vendas,
                                index=indice_dinamica,
                                columns=coluna_dinamica,
                                values=valor_analise,
                                aggfunc=metrica)
    vendas_dinamica['TOTAL GERAL'] = vendas_dinamica.sum(axis=1)
    vendas_dinamica.loc['TOTAL GERAL'] = vendas_dinamica.sum(axis=0).to_list()
    st.dataframe(vendas_dinamica)
else:
    st.error("NENHUM INDICE SELECIONADO")

