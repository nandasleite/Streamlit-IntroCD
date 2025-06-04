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
    
    tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs(["🌎 País", "📅 Data", "🏦 Empresa", "⭐ Missão", "🚀 Foguete", "🤑 Custo"])

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
        st.subheader("📅 Missões espaciais por ano")

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
                        labels={'x': 'Ano', 'y': 'Número de Lançamentos'})
        fig_ano.update_layout(xaxis_title='Ano', yaxis_title='Número de Lançamentos')
        # Separa as barras
        fig_ano.update_traces(marker=dict(line=dict(width=1, color='DarkSlateGrey')))
        fig_ano.update_xaxes(dtick="M12", tickformat="%Y")  # Formata o eixo x para mostrar apenas o ano
        st.plotly_chart(fig_ano, use_container_width=True)


        st.markdown("---")
        st.subheader("📅 Missões espaciais por mês")

        # Gráfico com o número de lançamentos por mês, individualizando os meses
        fig_mes = px.bar(df['Date'].dt.month.value_counts().sort_index(), 
                        x=df['Date'].dt.month.value_counts().sort_index().index, 
                        y=df['Date'].dt.month.value_counts().sort_index().values,
                        labels={'x': 'Mês', 'y': 'Número de Lançamentos'})
        fig_mes.update_layout(xaxis_title='Mês', yaxis_title='Número de Lançamentos')
        fig_mes.update_xaxes(tickvals=np.arange(1, 13), 
                             ticktext=['Jan', 'Fev', 'Mar', 'Abr', 'Mai', 'Jun', 
                                       'Jul', 'Ago', 'Set', 'Out', 'Nov', 'Dez'])
        fig_mes.update_traces(marker=dict(line=dict(width=1, color='DarkSlateGrey')))
        st.plotly_chart(fig_mes, use_container_width=True)
    

        st.markdown("---")
        st.subheader("📅 Missões espaciais por dia da semana")

        # Gráfico com o número de lançamentos por dia da semana, individualizando os dias
        fig_dia = px.bar(df['Weekday'].value_counts().sort_index(), 
                        x=df['Weekday'].value_counts().sort_index().index, 
                        y=df['Weekday'].value_counts().sort_index().values, 
                        labels={'x': 'Dia da Semana', 'y': 'Número de Lançamentos'})
        fig_dia.update_layout(xaxis_title='Dia da Semana', yaxis_title='Número de Lançamentos')
        fig_dia.update_traces(marker=dict(line=dict(width=1, color='DarkSlateGrey')))
        fig_dia.update_xaxes(tickvals=['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun'], 
                            ticktext=['Seg', 'Ter', 'Qua', 'Qui', 'Sex', 'Sáb', 'Dom'])
        fig_dia.update_xaxes(categoryorder='array', categoryarray=['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun'])
        st.plotly_chart(fig_dia, use_container_width=True)


    with tab3:
        st.subheader("🏦 Missões Espaciais por Empresa")
        
        # Gráfico de barras
        company_counts = df['Company Name'].value_counts().reset_index()
        company_counts.columns = ['Company Name', 'Mission Count']
        
        fig = px.bar(company_counts, x='Company Name', y='Mission Count', color='Mission Count',
                    text='Mission Count')
        fig.update_layout(xaxis_title='Empresa', yaxis_title='Número de Missões')
        st.plotly_chart(fig, use_container_width=True)


    with tab4:
        st.subheader("⭐ Missões Espaciais por Status")
        
        col1, col2 = st.columns(2)
        with col1:
            with st.container(border=True):
                st.metric(label="Missões com sucesso", value=df[df['Mission Status'] == 'Success'].shape[0])
        with col2:
            with st.container(border=True):
                st.metric(label="Missões com falha", value=df[df['Mission Status'] == 'Failure'].shape[0])
        # Gráfico de pizza
        mission_status_counts = df['Mission Status'].value_counts().reset_index()
        mission_status_counts.columns = ['Mission Status', 'Count']
        fig = px.pie(mission_status_counts, values='Count', names='Mission Status')
        fig.update_traces(textposition='inside', textinfo='percent+label')
        fig.update_layout(showlegend=False)
        st.plotly_chart(fig, use_container_width=True)


        st.markdown("---")
        st.subheader("⭐ Razão de Sucesso das Missões Espaciais")

        col1, col2 = st.columns(2)
        with col1:
            with st.container(border=True):
                ano_sucesso = df.groupby(df['Date'].dt.year)['Mission Status'].value_counts(normalize=True).unstack().fillna(0)
                ano_sucesso['Success Ratio'] = ano_sucesso['Success'] / (ano_sucesso['Success'] + ano_sucesso['Failure'])
                ano_sucesso = ano_sucesso.sort_values(by='Success Ratio', ascending=False)
                st.metric(label="Ano com maior razão de sucesso", value=ano_sucesso.index[0], 
                          delta=f"{ano_sucesso['Success Ratio'].iloc[0]:.2%}")
        with col2:
            with st.container(border=True):
                ano_falha = ano_sucesso.sort_values(by='Success Ratio', ascending=True)
                st.metric(label="Ano com menor razão de sucesso", value=ano_falha.index[0], 
                            delta=f"-{ano_falha['Success Ratio'].iloc[0]:.2%}")
                
        # Gráfico de linha com a taxa de sucesso ao longo dos anos
        fig_sucesso_ano = px.line(
            ano_sucesso.sort_index(),
            x=ano_sucesso.sort_index().index,
            y='Success Ratio',
            title='Razão de Sucesso das Missões Espaciais ao Longo dos Anos',
            labels={'x': 'Ano', 'Success Ratio': 'Razão de Sucesso'}
        )
        fig_sucesso_ano.update_layout(xaxis_title='Ano', yaxis_title='Taxa de Sucesso')
        fig_sucesso_ano.update_traces(line=dict(color='blue', width=2)) 
        st.plotly_chart(fig_sucesso_ano, use_container_width=True)


        st.markdown("---")
        st.subheader("⭐ Relação entre Lançamentos e Sucesso das Missões Espaciais")
        
        lancamentos_ano_status = (
            df.groupby([df['Date'].dt.year, 'Mission Status'])
            .size()
            .reset_index(name='Quantidade')
            .rename(columns={'Date': 'Ano'})
        )
        lancamentos_ano_status.rename(columns={'Date': 'Ano'}, inplace=True)
        lancamentos_ano_status['Ano'] = lancamentos_ano_status['Ano'].astype(int)

        # Gráfico de barras agrupadas por ano e status da missão com cores customizadas
        color_map = {'Failure': 'red', 'Success': 'green'}
        fig_status_missao = px.line(
            lancamentos_ano_status,
            x='Ano',
            y='Quantidade',
            color='Mission Status',
            color_discrete_map=color_map,
            markers=True,
            labels={'Ano': 'Ano', 'Quantidade': 'Número de Lançamentos', 'Mission Status': 'Status da Missão'}
        )
        fig_status_missao.update_layout(
            xaxis_title='Ano',
            yaxis_title='Número de Lançamentos',
            xaxis_tickangle=90,
            xaxis=dict(tickmode='linear')
        )
        fig_status_missao.update_traces(line=dict(width=2), marker=dict(size=8, line=dict(width=1, color='DarkSlateGrey')))
        st.plotly_chart(fig_status_missao, use_container_width=True)


        st.markdown("---")
        st.subheader("⭐ Top 10 Países com Mais Lançamentos Bem-Sucedidos")

        # Localidades com mais lançamentos bem-sucedidos
        lancamentos_sucesso = df[df['Mission Status'] == 'Success']['Country'].value_counts().head(10)
        # Gráfico de barras com os 10 países com mais lançamentos bem-sucedidos
        fig_sucesso_pais = px.bar(
            lancamentos_sucesso,
            x=lancamentos_sucesso.index,
            y=lancamentos_sucesso.values,
            labels={'x': 'País', 'y': 'Quantidade de Lançamentos Bem-Sucedidos'}
        )
        fig_sucesso_pais.update_layout(
            xaxis_title='País',
            yaxis_title='Quantidade de Lançamentos Bem-Sucedidos'
        )
        fig_sucesso_pais.update_traces(texttemplate='%{y}', textposition='outside')
        fig_sucesso_pais.update_xaxes(tickangle=45)
        fig_sucesso_pais.update_traces(marker=dict(line=dict(width=1, color='DarkSlateGrey')))
        st.plotly_chart(fig_sucesso_pais, use_container_width=True)

        st.markdown("---")
        st.subheader("⭐ Status das Missões Espaciais por País")

        lancamentos_pais_status = df.groupby(['Country', 'Mission Status']).size().reset_index(name='Quantidade')
        lancamentos_pais_status = lancamentos_pais_status.sort_values(by='Quantidade', ascending=False)
        lancamentos_pais_status = lancamentos_pais_status.head(10)

        # Cria um gráfico de barras empilhadas para visualizar o status das missões por país
        fig_pais_status = px.bar(
            lancamentos_pais_status,
            x='Country',
            y='Quantidade',
            color='Mission Status',
            title='Status das Missões por País',
            labels={'Country': 'País', 'Quantidade': 'Número de Lançamentos', 'Mission Status': 'Status da Missão'},
            color_discrete_map={'Success': 'green', 'Failure': 'red'}
        )
        fig_pais_status.update_layout(
            xaxis_title='País',
            yaxis_title='Número de Lançamentos',
            xaxis_tickangle=45,
            barmode='stack'
        )
        fig_pais_status.update_traces(texttemplate='%{y}', textposition='outside')
        fig_pais_status.update_xaxes(tickangle=45)
        fig_pais_status.update_traces(marker=dict(line=dict(width=1, color='DarkSlateGrey')))
        st.plotly_chart(fig_pais_status, use_container_width=True)


    with tab5:
        st.subheader("🚀 Situação dos Foguetes em 2020")
        df['Status Rocket'] = df['Status Rocket'].str.replace('Status', '', regex=False)

        # Gráfico de pizza com StatusRocket
        fig_status_rocket = px.pie(
            df,
            names='Status Rocket',
            color='Status Rocket',
            color_discrete_map={
                'Active': 'blue',
                'Retired': 'gray',
                'Destroyed': 'red'
            }
        )
        fig_status_rocket.update_traces(textposition='inside', textinfo='percent+label')
        fig_status_rocket.update_layout(showlegend=False)
        st.plotly_chart(fig_status_rocket, use_container_width=True)


        st.markdown("---")
        st.subheader("🚀 Top 10 Países com mais Foguetes Ativos em 2020")
        # Gráfico de barras com o número de foguetes ativos por país
        fig_ativos_pais = px.bar(
            df[df['Status Rocket'] == 'Active']['Country'].value_counts().head(10),
            x=df[df['Status Rocket'] == 'Active']['Country'].value_counts().head(10).index,
            y=df[df['Status Rocket'] == 'Active']['Country'].value_counts().head(10).values,
            title='Top 10 Países com mais Foguetes Ativos',
            labels={'x': 'País', 'y': 'Número de Foguetes Ativos'}
        )
        fig_ativos_pais.update_layout(
            xaxis_title='País',
            yaxis_title='Número de Foguetes Ativos',
        )
        fig_ativos_pais.update_traces(texttemplate='%{y}', textposition='outside')
        fig_ativos_pais.update_xaxes(tickangle=45)
        fig_ativos_pais.update_traces(marker=dict(line=dict(width=1, color='DarkSlateGrey')))
        st.plotly_chart(fig_ativos_pais, use_container_width=True)

        st.markdown("---")
        st.subheader("🚀 Top 10 Países com mais Foguetes Aposentados em 2020")
        # Gráfico de barras com o número de foguetes aposentados por país
        fig_aposentados_pais = px.bar(
            df[df['Status Rocket'] == 'Retired']['Country'].value_counts().head(10),
            x=df[df['Status Rocket'] == 'Retired']['Country'].value_counts().head(10).index,
            y=df[df['Status Rocket'] == 'Retired']['Country'].value_counts().head(10).values,
            title='Top 10 Países com mais Foguetes Aposentados',
            labels={'x': 'País', 'y': 'Número de Foguetes Aposentados'}
        )
        fig_aposentados_pais.update_layout(
            xaxis_title='País',
            yaxis_title='Número de Foguetes Aposentados',
        )   
        fig_aposentados_pais.update_traces(texttemplate='%{y}', textposition='outside')
        fig_aposentados_pais.update_xaxes(tickangle=45)
        fig_aposentados_pais.update_traces(marker=dict(line=dict(width=1, color='DarkSlateGrey')))
        st.plotly_chart(fig_aposentados_pais, use_container_width=True)


    with tab6:
        st.subheader("🤑 Custo Médio das Missões Espaciais por País")
        # Gráfico de barras com o custo médio por pais
        fig_cost_country = px.bar(
            df.groupby('Country')['Mission Cost'].mean().sort_values(ascending=False).head(10),
            x=df.groupby('Country')['Mission Cost'].mean().sort_values(ascending=False).head(10).index,
            y=df.groupby('Country')['Mission Cost'].mean().sort_values(ascending=False).head(10).values,
            labels={'x': 'País', 'y': 'Custo Médio da Missão (USD)'}
        )
        fig_cost_country.update_layout(
            xaxis_title='País',
            yaxis_title='Custo Médio da Missão (USD)',
            yaxis_tickprefix='$',
            yaxis_tickformat=','
        )
        fig_cost_country.update_traces(texttemplate='%{y:.2f}', textposition='outside')
        fig_cost_country.update_xaxes(tickangle=45)
        fig_cost_country.update_traces(marker=dict(line=dict(width=1, color='DarkSlateGrey')))
        st.plotly_chart(fig_cost_country, use_container_width=True)


        st.markdown("---") 
        st.subheader("🤑 Custo Médio das Missões Espaciais por Empresa")

        # Gráfico de barras com o custo médio das missões espaciais por empresa
        fig_mission_cost = px.bar(
            df.groupby('Company Name')['Mission Cost'].mean().sort_values(ascending=False).head(10),
            x=df.groupby('Company Name')['Mission Cost'].mean().sort_values(ascending=False).head(10).index,
            y=df.groupby('Company Name')['Mission Cost'].mean().sort_values(ascending=False).head(10).values,
            labels={'x': 'Empresa', 'y': 'Custo Médio da Missão (USD)'}
        )
        fig_mission_cost.update_layout(
            xaxis_title='Empresa',
            yaxis_title='Custo Médio da Missão (USD)',
            yaxis_tickprefix='$',
            yaxis_tickformat=','
        )
        fig_mission_cost.update_traces(texttemplate='%{y:.2f}', textposition='outside')
        fig_mission_cost.update_xaxes(tickangle=45)
        fig_mission_cost.update_traces(marker=dict(line=dict(width=1, color='DarkSlateGrey')))
        st.plotly_chart(fig_mission_cost, use_container_width=True)
        