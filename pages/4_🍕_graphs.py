import pandas as pd
from pathlib import Path
import streamlit as st
from datetime import date, timedelta
import plotly.express as px

st.set_page_config(
    layout="wide",
    page_title="Gráficos",
    page_icon="🍕"
)

PERCENTUAL_COMISSAO = 0.08
COLUNAS_ANALISE = ['filial', 'vendedor', 'produto']

pasta_datasets = Path(__file__).parent.parent / 'datasets'
df_vendas = pd.read_csv(pasta_datasets / 'vendas.csv', decimal=',', sep=';', index_col='id_venda')
df_filiais = pd.read_csv(pasta_datasets / 'filiais.csv', decimal=',', sep=';', index_col=0)
df_produtos = pd.read_csv(pasta_datasets / 'produtos.csv', decimal=',', sep=';', index_col=0)

df_produtos = df_produtos.rename(columns={'nome': 'produto'})

df_vendas = pd.merge(left=df_vendas, right=df_produtos, on='produto', how='left')
df_vendas = df_vendas.drop(columns=df_vendas.columns[6])
df_vendas['comissao'] = df_vendas['preco'] * PERCENTUAL_COMISSAO
df_vendas['data'] = pd.to_datetime(df_vendas['data'], errors='coerce')

data_inicio = st.sidebar.date_input('Data Inicial', df_vendas['data'].dt.date.max() - timedelta(days=7), format="DD/MM/YYYY")

data_final = st.sidebar.date_input('Data Final', df_vendas['data'].dt.date.max(), format="DD/MM/YYYY")

df_vendas_corte = df_vendas[(df_vendas['data'].dt.date >= data_inicio) & (df_vendas['data'].dt.date <= data_final +timedelta(days=1))]
valor_total = df_vendas_corte['preco'].sum()
valor_vendas = f'R$ {valor_total:.2f}'

quantidade_total = df_vendas_corte['preco'].count()
quantidade_vendas = f'{quantidade_total}'

col11, col12, col13 = st.columns([0.5, 0.25, 0.25])
col11.markdown("# Números Gerais")
col12.metric("Valor de vendas no periodo", valor_vendas)
col13.metric("Quantidade total das vendas no periodo", quantidade_vendas)

st.divider()

col21, col22 = st.columns(2)
df_vendas_corte['vendas_dia'] = df_vendas_corte['data'].dt.date

dia_vendas = df_vendas_corte.groupby('vendas_dia').agg({'preco': 'sum'})

fig = px.line(dia_vendas)
col21.plotly_chart(fig)

analise_selecionada = st.sidebar.selectbox('Analisar:', COLUNAS_ANALISE)
fig = px.pie(df_vendas_corte, values='preco', names=analise_selecionada)
col22.plotly_chart(fig)
st.divider()