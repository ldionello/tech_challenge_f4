import streamlit as st
import pandas as pd
from modelo import carregar_dados, prever_precos

st.set_page_config(layout="wide")
st.title("Previsão do Preço do Petróleo - Modelo Seasonal Naive")

# Upload de arquivo ou usar local
st.sidebar.title("Configuração")
horizonte = st.sidebar.slider("Dias para prever", 7, 60, 30)

# Carregamento de dados
df = carregar_dados('dados/BD_DADOS_IPEA.csv')

df_ordenado = df.sort_values('ds')
ultimo_dia = df_ordenado['ds'].max()

st.subheader(f"Dados históricos até {ultimo_dia.strftime('%d/%m/%Y')}")
st.line_chart(df_ordenado.set_index('ds')['y'])

# Botão de previsão
if st.button("PREVISÃO"):
    forecast = prever_precos(df, horizonte)

    st.subheader(f"Previsão para os próximos {horizonte} dias")
    st.line_chart(forecast.set_index('ds')['SeasonalNaive'])
    st.dataframe(forecast)
