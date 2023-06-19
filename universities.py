# -*- coding: utf-8 -*-
"""universities

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1PcteeMM-lDrZurcizvjVDJiEeyor-oRW
"""

# -*- coding: utf-8 -*-
"""University Raspagem

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/16RHuw35dIoGJf_g2axgB9TGrvioHrX2l
"""
pip install beautifulsoup4
# Baixar as Bibliotecas Necessárias
import requests  # Usado para obter o conteúdo HTML
import pandas as pd  # Usada para analisar e manipular os dados
import streamlit as st
from bs4 import BeautifulSoup 
# Organizar/Localizar as tabelas
def fazer_raspagem():  # Definir a função que vai fazer a raspagem
    url = "https://www.earj.com.br/university-acceptances/"
    response = requests.get(url)  # Obter o conteúdo HTML
    soup = BeautifulSoup(response.content, "html.parser")  # Usa o conteúdo HTML para criar um objeto BeautifulSoup
    table = soup.find("table")  # A variável table extrair as linhas e as colunas da tabela de dados

    if table is None:  # Se o programa reconhecer a variável table como 'None', ela não foi encontrada na página
        print("Tabela não encontrada.")  # Retorna "Tabela não encontrada" ao invés de dar uma mensagem de erro
        return None

    colunas = table.find_all("th")  # Tag TH reconhece os headers da tabela
    nomes_colunas = [coluna.text.strip() for coluna in colunas]  # Extrai os nomes das headers, retira os espaçõs em branco, e armazena em colunas
    linhas = table.find_all("tr")[1:]  # Tag TR reconhece as linhas da tabela
    dados = []  # Criar lista para organizar dados
    for linha in linhas:  # Loop para todas as linhas na tabela
        celulas = linha.find_all("td")
        valores_celulas = [celula.text.strip() for celula in celulas]  # Extrair o texto, removendo espaços em branco
        dados.append(valores_celulas)  # Adicionar a lista de linhas para a lista dados
    df = pd.DataFrame(dados, columns=nomes_colunas)  # Cria um DataFrame no pandas
    return df

df = fazer_raspagem()
if df is not None:
    if "Region" in df.columns:
        regiões_especificas = ['United States', 'United Kingdom', 'Europe', 'Canada', 'Brazil']
        região_selecionada = st.selectbox("Pick a region", regiões_especificas)
        df_filtrado = df[df['Region'] == região_selecionada]
        if not df_filtrado.empty:
            st.write("Dados Filtrados")
            st.dataframe(df_filtrado)
            st.write("Chart")
            chart_data = df_filtrado.groupby("University")["Acceptances"].sum()
            st.bar_chart(chart_data)
        else:
            st.write("Dado não encontrado")
    else:
        st.write("Coluna não encontrada no Data Frame")
