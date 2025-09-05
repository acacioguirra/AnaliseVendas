import pandas as pd
from pathlib import Path
import streamlit as st
from datetime import date, timedelta, datetime


st.set_page_config(
    layout="wide",
    page_title="Vendedores",
    page_icon="👨‍💻"
)
pasta_datasets = Path(__file__).parent.parent / 'datasets'

caminho_vendas = pasta_datasets / 'vendas.csv'
caminho_filiais = pasta_datasets / 'filiais.csv'
caminho_produtos = pasta_datasets / 'produtos.csv'

#VENDAS
df_vendas = pd.read_csv(caminho_vendas, sep=';', decimal=',', index_col='id_venda', parse_dates=True)
#FILIAIS
df_filiais = pd.read_csv(caminho_filiais, decimal=',', sep=';')
df_filiais.index.name = 'id'
df_filiais['Cidade/Estado'] = df_filiais['cidade'] + '/' + df_filiais['estado']
#PRODUTOS
df_produtos = pd.read_csv(caminho_produtos, sep=';', decimal=',', index_col='id')
df_produtos = df_produtos.drop(columns=df_produtos.columns[0])
df_produtos = df_produtos.rename(columns={'nome': 'produto'})

#VENDAS X PRODUTOS
df_vendas_mesclado = pd.merge(
    left=df_vendas, right=df_produtos,
     on='produto', how='left'
)
df_vendas_mesclado['data'] = pd.to_datetime(df_vendas_mesclado['data'])

COMISSAO = 0.08
df_vendas_mesclado['Comissao'] = df_vendas_mesclado['preco'] * COMISSAO


data_inicio = st.sidebar.date_input('Data Inicial', df_vendas_mesclado['data'].min().date(), format="DD/MM/YYYY")
data_final = st.sidebar.date_input('Data Final', df_vendas_mesclado['data'].max().date(), format="DD/MM/YYYY")

df_vendas_cortado = df_vendas_mesclado[(df_vendas_mesclado['data'].dt.date >= data_inicio) & (df_vendas_mesclado['data'].dt.date < data_final + timedelta(days=1))]

# Numeros Gerais
st.markdown("# Números Gerais")
col11, col12 = st.columns(2)
valor_vendas = df_vendas_cortado['preco'].sum()
valor_vendas = f'R$ {valor_vendas:.2f}'
quantidade_vendas = df_vendas_cortado['preco'].count()


col11.metric("Valor de vendas no periodo", valor_vendas)
col12.metric("Quantidade de vendas no periodo", quantidade_vendas)

st.divider()

principal_filial = df_vendas_cortado["filial"].value_counts().index[0]
st.markdown(f"## Princiapal Filial: {principal_filial}")
col21, col22 = st.columns(2)
valor_vendas = df_vendas_cortado[df_vendas_cortado['filial'] == principal_filial]['preco'].sum()
valor_vendas = f'R$ {valor_vendas:.2f}'
quantidade_vendas = df_vendas_cortado[df_vendas_cortado['filial'] == principal_filial]['preco'].count()

col21.metric("Valor de vendas por filial", valor_vendas)
col22.metric("Quantidade de vendas por filial", quantidade_vendas)

st.divider()

principal_vendedor = df_vendas_cortado["vendedor"].value_counts().index[0]
st.markdown(f"## Princiapal Vendedor: {principal_vendedor}")

col31, col32, col33 = st.columns(3)
valor_vendas = df_vendas_cortado[df_vendas_cortado['vendedor'] == principal_vendedor]['preco'].sum()
valor_vendas = f'R$ {valor_vendas:.2f}'
valor_comissao = df_vendas_cortado[df_vendas_cortado['vendedor'] == principal_vendedor]['Comissao'].sum()
valor_comissao = f'R$ {valor_comissao:.2f}'
quantidade_vendas = df_vendas_cortado[df_vendas_cortado['vendedor'] == principal_vendedor]['preco'].count()

col31.metric("Valor de vendas por vendedor", valor_vendas)
col32.metric("Quantidade de vendas por vendedor", quantidade_vendas)
col33.metric("Comissao no periodo", valor_comissao)

