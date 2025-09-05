from pathlib import Path
import pandas as pd
import streamlit as st


st.set_page_config(
    layout="wide",
    page_title="Análise de Vendas",
    page_icon="✅"
)


pasta_datasets = Path(__file__).parent / 'datasets'
caminho_vendas = pasta_datasets / 'vendas.csv'

st.title('SelliAs')
st.write(f'Pasta Datasets: {pasta_datasets}')

df_vendas = pd.read_csv(caminho_vendas, sep=';', decimal=',', index_col='id_venda')
df_vendas['data'] = pd.to_datetime(df_vendas['data'])
df_vendas['data'] = df_vendas['data'].dt.strftime('%d/%m/%Y')


colunas = list(df_vendas.columns)

colunas_selecionadas = st.sidebar.multiselect('Selecione as colunas: ', colunas, colunas)

col1, col2 = st.sidebar.columns(2)
col_filtro = col1.selectbox('Selecione a Coluna', colunas)
valor_filtro = col2.selectbox('Selecione a Coluna', list(df_vendas[col_filtro].unique()))

status_filtrar = col1.button('Filtrar')
status_limpar = col2.button("Limpar")


if status_filtrar:
    st.dataframe(df_vendas.loc[df_vendas[col_filtro] == valor_filtro, colunas_selecionadas], height=800)
elif status_limpar:
    st.dataframe(df_vendas[colunas_selecionadas], height=800)
else:
    st.dataframe(df_vendas[colunas_selecionadas], height=800)

