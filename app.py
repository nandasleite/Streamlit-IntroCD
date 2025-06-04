import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px

st.set_page_config(
    page_title = "Missões Espaciais",
    page_icon = ":bar_chart:",
    layout = "wide"
)


st.sidebar.subheader("🚀")
st.sidebar.subheader("Análise Exploratória dos Dados de Missões Espaciais")
st.sidebar.write("Este permite explorar dados de missões espaciais, incluindo informações sobre empresas, locais de lançamento, datas e status das missões, de 1957 a 2020.")


# Carregamento dos dados
@st.cache_data
def load_data():
    df = pd.read_csv("data/space_missions.csv")
    
    # Remove colunas desnecessárias
    df.drop(columns=['Unnamed: 0', 'Unnamed: 0.1'], inplace=True)
    
    # Cria a coluna 'Country'
    df['Country'] = df['Location'].str.split(',').str[-1].str.strip()
    
    # Ajusta nomes de países
    replace_dict = {
        'Barents Sea': 'Russia',
        'Gran Canaria': 'Spain',
        'Shahrud Missile Test Site': 'Iran',
        'Yellow Sea': 'Russia',
        'Pacific Missile Range Facility': 'USA',
        'Pacific Ocean': 'USA'
    }
    df['Country'] = df['Country'].replace(replace_dict)

    # Processa a coluna 'Datum'
    df['Datum'] = df['Datum'].str.split(' ').str[:4].str.join(' ')
    df[['Weekday', 'Date']] = df['Datum'].str.split(' ', n=1, expand=True)
    df.drop(columns=['Datum'], inplace=True)
    df['Weekday'] = df['Weekday'].str.strip()
    df['Date'] = df['Date'].str.strip()
    df['Date'] = pd.to_datetime(df['Date'])
    
    # Cria a coluna 'Mission Status' para categorizar as missões
    df['Mission Status'] = df['Status Mission'].apply(lambda x: 'Success' if x == 'Success' else 'Failure')

    # Renomeia a coluna ' Rocket' para 'Mission Cost'
    df.rename(columns={' Rocket': 'Mission Cost'}, inplace=True)
    
    # Converte a coluna 'Mission Cost' para numérica
    df['Mission Cost'] = pd.to_numeric(df['Mission Cost'].str.replace(r'[^\d.]', '', regex=True), errors='coerce')

    # Em StatusRocket, remover a palavra Status
    df['Status Rocket'] = df['Status Rocket'].str.replace('Status', '', regex=False)
    
    return df

df = load_data()

# ------------------------------------

col1, col2 = st.columns(2)

with col1:
    with st.expander("Dicionário de Dados", expanded=False, icon=":material/book:"):
        st.markdown("""	
        - **Company Name:** Coluna que apresenta os nomes das empresas que realizaram missões espaciais. Possui 4.324 registros não-nulos;
        - **Location:** Coluna que apresenta os locais onde os lançamentos foram realizados. Possui 4.324 registros não-nulos;
        - **Datum:** Coluna que apresenta as datas e os horários dos lançamentos. Possui 4.324 registros não-nulos;
                    
        """)

with col2:
    # Visualização do DataFrame
    with st.expander("Visualização do DataFrame", expanded=False, icon=":material/view_list:"):
        st.dataframe(df.head(5), use_container_width=True)


# ------------------------------------

with st.container(border=True):
    
    tab1, tab2, tab3, tab4, tab5 = st.tabs(["🌎 País", "📅 Data", "🏦 Empresa", "⭐ Missão", "🚀 Foguete"])

    with tab1:
        st.subheader("🌎 Países com mais missões espaciais")
        
        # Gráfico de barras
        country_counts = df['Country'].value_counts().reset_index()
        country_counts.columns = ['Country', 'Mission Count']
        
        fig = px.bar(country_counts, x='Country', y='Mission Count', color='Mission Count',
                    text='Mission Count')
        fig.update_layout(xaxis_title='País', yaxis_title='Número de Missões')
        st.plotly_chart(fig, use_container_width=True)
    
    with tab2:
        st.subheader("📅 Missões espaciais por data")

        col1, col2 = st.columns(2)
        with col1:
            with st.container(border=True):
                st.metric(label="Maior quantidade de lançamentos", value="1971")
        with col2:
            with st.container(border=True):
                ano_menor_lancamentos = df['Date'].dt.year.value_counts().idxmin()
                st.metric(label="Menor quantidade de lançamentos", value=ano_menor_lancamentos)

        # Gráfico com o número de lançamentos por ano, individualizando os anos
        fig_ano = px.bar(df['Date'].dt.year.value_counts().sort_index(), 
                        x=df['Date'].dt.year.value_counts().sort_index().index, 
                        y=df['Date'].dt.year.value_counts().sort_index().values, 
                        title='Número de Lançamentos Espaciais por Ano',
                        labels={'x': 'Ano', 'y': 'Número de Lançamentos'})
        fig_ano.update_layout(xaxis_title='Ano', yaxis_title='Número de Lançamentos')
        # Separa as barras
        fig_ano.update_traces(marker=dict(line=dict(width=1, color='DarkSlateGrey')))
        fig_ano.update_xaxes(dtick="M12", tickformat="%Y")  # Formata o eixo x para mostrar apenas o ano
        st.plotly_chart(fig_ano, use_container_width=True)