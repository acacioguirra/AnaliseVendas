from pathlib import Path
import streamlit as st
import pandas as pd
from datetime import datetime

st.set_page_config(
    layout="wide",
    page_title="Adicionar Venda",
    page_icon="💸"
)
pasta_datasets = Path(__file__).parent.parent / 'datasets'

caminho_vendas = pasta_datasets / 'vendas.csv'
caminho_filiais = pasta_datasets / 'filiais.csv'
caminho_produtos = pasta_datasets / 'produtos.csv'

#VENDAS
df_vendas = pd.read_csv(caminho_vendas, sep=';', decimal=',', index_col='id_venda')
#FILIAIS
df_filiais = pd.read_csv(caminho_filiais, decimal=',', sep=';')
df_filiais.index.name = 'id'
df_filiais['Cidade/Estado'] = df_filiais['cidade'] + '/' + df_filiais['estado']
#PRODUTOS
df_produtos = pd.read_csv(caminho_produtos, sep=';', decimal=',', index_col='id')


lista_filiais = df_filiais['Cidade/Estado'].to_list()
filial_selecionada = st.sidebar.selectbox('Selecione a Filial: ' , lista_filiais)

lista_vendedor = df_filiais.loc[df_filiais['Cidade/Estado'] == filial_selecionada, 'vendedores'].iloc[0]
lista_vendedor = lista_vendedor.strip('][').replace("'", '').split(', ')
vendedor_selecionado = st.sidebar.selectbox('Selecione o Vendedor: ', lista_vendedor)

lista_produtos = df_produtos['nome'].to_list()
produto_selecionado = st.sidebar.selectbox('Selecione o Produto: ', lista_produtos)

nome_cliente = st.sidebar.text_input('Nome do Cliente')
genero_cliente = st.sidebar.selectbox('Genero do Cliente: ', ['Masculino', 'Feminino'])

forma_pagamento = ['Pix', 'Débito', 'Crédito', 'à vista']
forma_pag_selecionado = st.sidebar.selectbox("Forma de Pagamento", forma_pagamento)


if st.sidebar.button('Adicionar nova venda'):
    lista_adicionar = [datetime.now(),
                  filial_selecionada,
                  vendedor_selecionado,
                  produto_selecionado,
                  nome_cliente,
                  genero_cliente,
                  forma_pag_selecionado]
    df_nova_venda = pd.DataFrame([lista_adicionar], columns=df_vendas.columns)
    df_vendas = pd.concat([df_vendas, df_nova_venda], ignore_index=True)
    df_vendas.to_csv(caminho_vendas, sep=';', decimal=',', index=True, index_label='id_venda')
    st.success("Venda Adicionada!")

st.dataframe(df_vendas, height=800)
