import pandas as pd
import streamlit as st
from statsforecast import StatsForecast
from statsforecast.models import SeasonalNaive


def carregar_dados(caminho):
    df = pd.read_csv(caminho, sep=';', encoding='latin1')

    # Normaliza os nomes ANTES de acessar qualquer coluna
    df.columns = df.columns.str.strip().str.upper()
    st.write("Colunas disponíveis:", df.columns)

    # Use colunas já padronizadas
    if 'PERIODO' not in df.columns or 'PRECO_FOB' not in df.columns:
        st.error("As colunas 'PERIODO' e/ou 'PRECO_FOB' não foram encontradas no arquivo.")
        st.stop()

    df['PERIODO'] = pd.to_datetime(df['PERIODO'], dayfirst=True)
    df = df.rename(columns={'PERIODO': 'ds', 'PRECO_FOB': 'y'})
    df['unique_id'] = 'petroleo'

    return df[['unique_id', 'ds', 'y']]



def prever_precos(df, horizonte):
    model = StatsForecast(
        models=[SeasonalNaive(season_length=5)],
        freq='D',
        n_jobs=1
    )
    model.fit(df)
    forecast = model.predict(h=horizonte)
    return forecast
