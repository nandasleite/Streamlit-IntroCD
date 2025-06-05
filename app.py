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

# ------------------------------------

st.sidebar.subheader("🚀")
st.sidebar.subheader("Análise Exploratória dos Dados de Missões Espaciais")
st.sidebar.write("Este permite explorar dados de missões espaciais, incluindo informações sobre empresas, locais de lançamento, datas e status das missões, de 1957 a 2020.")
st.sidebar.markdown("**Fernanda Leite e Maria Fernanda**")

# ------------------------------------

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
# Textos descritivos

# Países
grafico1 = 'Este gráfico resume a contribuição histórica acumulada de cada nação para a atividade de lançamento. A Rússia (ex-URSS) e os EUA dominam a lista com 1399 e 1381 lançamentos, respectivamente, reafirmando sua primazia histórica e o impacto da Guerra Fria na aceleração das missões espaciais. O Cazaquistão (701) aparece em terceiro devido ao uso do Cosmódromo de Baikonur, a primeira e maior base de lançamentos de foguetes do mundo. A França e a China seguem com números significativos (303 e 268), destacando suas capacidades espaciais bem estabelecidas, enquanto Japão e Índia também mostram um número considerável. A presença de Irã, Nova Zelândia e Israel com volumes menores indica a expansão do "clube espacial" para incluir países com programas mais recentes ou de nicho. Este gráfico é uma representação concisa da concentração de capacidade de lançamento espacial nas mãos de poucas potências ao longo da história.'

# Ano
grafico2 = 'O gráfico oferece uma perspectiva histórica sobre a frequência dos lançamentos. Observa-se um rápido crescimento nos anos 1960 e 1970, impulsionado pela corrida espacial entre EUA e URSS, com picos significativos por volta de 1967-1968 e novamente em meados dos anos 1970 (1975-1976), quando ambos os países realizavam dezenas de lançamentos anuais. Após esses picos, houve uma ligeira diminuição na frequência nos anos 1980 e 1990, e uma estabilização nos anos 2000. No entanto, a década de 2010 mostra um ressurgimento notável no número de lançamentos, com um novo pico em 2018 (quase 120 lançamentos), impulsionado pela ascensão de novos players como a China, o crescimento de empresas privadas e o aumento da demanda por serviços de lançamento de satélites, indicando uma nova era de expansão espacial.'

# Mês
grafico3 = 'O gráfico revela uma distribuição relativamente uniforme de lançamentos ao longo do ano, com uma leve tendência de aumento no final do ano. Dezembro se destaca como o mês com o maior número de lançamentos (450), seguido de perto por abril, junho e outubro. Essa distribuição sugere que não há sazonalidade climática ou operacional rígida que concentre lançamentos em apenas alguns meses, indicando que as janelas de lançamento são aproveitadas de forma consistente, possivelmente otimizando o uso das infraestruturas e atendendo a demandas de órbita específicas ou a prazos de projetos que se estendem ao longo de todo o ano.'

# Dia da semana
grafico4 = 'Este gráfico demonstra a frequência de lançamentos espaciais distribuída pelos dias da semana. Notavelmente, a maioria dos lançamentos ocorre nos dias úteis, com quartas, quintas e sextas-feiras apresentando o maior número de atividades. Há uma queda acentuada nos lançamentos durante os fins de semana, especialmente aos domingos, que mostram a menor quantidade. Essa distribuição reflete as operações típicas de uma indústria que segue um cronograma de trabalho padronizado, onde a disponibilidade de equipes, infraestrutura e apoio técnico é maior durante a semana comercial, priorizando a eficiência e coordenação das operações.'

# Empresa
grafico5 = 'O gráfico destaca a esmagadora contribuição histórica da RVSN URSS (Forças de Foguetes Estratégicos da União Soviética) com 1777 lançamentos, um número muito superior ao de qualquer outra entidade, reiterando o papel central da União Soviética na corrida espacial e na exploração inicial. A grande lacuna para a segunda colocada, Arianespace (279), e outras empresas como General Dynamics (251) e CASC (251), demonstra a magnitude do esforço espacial soviético. A presença de entidades militares como a US Air Force (161) e a VKS RF (201) (Forças Aeroespaciais Russas) sublinha a natureza frequentemente dual, civil e militar, das operações espaciais. A NASA (203) e empresas aeroespaciais tradicionais como Boeing (136), ULA (140) e Martin Marietta (114) também aparecem, mostrando a diversidade de atores que contribuíram para a história dos lançamentos espaciais. '

# Pizza - Status das Missões
grafico6 = 'O gráfico de pizza acima oferece uma visão consolidada da proporção de sucessos e falhas em todas as missões. Ele revela que a vasta maioria das missões espaciais, 89.7%, foi bem-sucedida, enquanto apenas 10.3% resultaram em falha. Essa alta taxa de sucesso global ressalta a maturidade e a confiabilidade das tecnologias de lançamento, mesmo considerando a complexidade inerente de enviar objetos ao espaço. É um testemunho da dedicação e precisão exigidas na engenharia espacial ao longo das décadas desde o início da era espacial. '

# Razao de sucesso por ano
grafico7 = 'Este gráfico ilustra a evolução da taxa de sucesso das missões espaciais desde 1957. Observa-se que, nas primeiras décadas da exploração espacial (final dos anos 1950 e início dos anos 1960), a taxa de sucesso era consideravelmente baixa, com picos de apenas 20% em 1958, refletindo os desafios e a natureza experimental dos primeiros lançamentos. Contudo, houve um rápido aprendizado e aprimoramento tecnológico, levando a um aumento constante na taxa de sucesso, que se estabilizou em patamares elevados, geralmente acima de 90%, a partir dos anos 1970. Embora haja pequenas flutuações e algumas quedas pontuais (como em meados dos anos 80 e 90, que podem coincidir com acidentes notórios como o desastre do Challenger ou falhas de foguetes), a tendência geral é de alta confiabilidade nas últimas décadas, demonstrando a maturidade e o avanço da engenharia aeroespacial.'

# Sucesso x fracasso por ano
grafico8 = 'O gráfico apresenta a relação entre lançamentos espaciais e o status das missões (sucesso ou falha) por ano, de 1957 a 2020. Observa-se um aumento significativo no número de lançamentos a partir da década de 1960, com picos notáveis durante a corrida espacial (décadas de 1960 e 1970), especialmente entre 1975 e 1977, quando os lançamentos ultrapassaram 100 por ano, com predominância de missões bem-sucedidas (barras verdes). A partir da década de 1980, o número de lançamentos diminuiu e se manteve relativamente estável até o início dos anos 2010, quando houve novo crescimento, atingindo outro pico em 2018. Ao longo do tempo, percebe-se uma tendência clara de aumento da taxa de sucesso, com a quantidade de falhas (barras vermelhas) diminuindo significativamente, evidenciando o avanço tecnológico e a maior confiabilidade dos lançamentos espaciais ao longo das décadas. '

# Top 10 Países com mais lançamentos bem-sucedidos
grafico9 = 'Observa-se que a Rússia e os EUA lideram com 1303 e 1219 lançamentos bem-sucedidos, respectivamente, o que reflete a vasta infraestrutura de lançamento que esses países construíram. O Cazaquistão, novamente, aparece em terceiro lugar com 608 lançamentos bem-sucedidos, reafirmando a importância do Cosmódromo de Baikonur como um dos locais mais ativos e bem-sucedidos na história dos lançamentos espaciais. A França e a China seguem com números significativos (285 e 243, respectivamente), mostrando a relevância de seus próprios locais de lançamento. A inclusão de "New Zealand" e "Kenya" pode indicar locais de lançamento flutuantes ou instalações costeiras usadas para trajetórias específicas, ou ainda a emergência de novos players com menor volume, como a Nova Zelândia com o Rocket Lab.'

# Status das Missões por País
grafico10 = 'O gráfico mostra a distribuição de sucessos e falhas por nação. A Rússia (ex-URSS) e os EUA, os dois maiores players históricos, apresentam o maior número de lançamentos bem-sucedidos (1306 e 1219, respectivamente) e também as maiores contagens de falhas (93 e 162, respectivamente). A proporção de falhas para os EUA é um pouco maior que a da Rússia em relação ao volume total de lançamentos, mas ambos os países demonstram uma alta taxa de sucesso. O Cazaquistão, embora não seja um país com capacidade primária de desenvolvimento de foguetes, possui um volume considerável de lançamentos a partir de seu território (608 sucessos e 93 falhas), novamente reforçando seu papel como uma importante base de lançamento. Países como França, China, Japão e Índia também exibem taxas de sucesso elevadas, consolidando suas posições como potências espaciais com capacidades de lançamento robustas.'

# Pizza - Situação dos Foguetes
grafico11 = 'O gráfico oferece uma visão geral concisa do estado da frota de foguetes, indicando que uma vasta maioria, 81.7%, está "Aposentada" (Retired), enquanto apenas 18.3% estão "Ativos" (Active). Essa distribuição é esperada, dada a natureza de uma atividade que se estende por décadas desde 1957; a maioria dos foguetes construídos e lançados ao longo da história naturalmente não está mais em operação. Isso reforça a importância da manutenção e desenvolvimento contínuo de novas tecnologias de lançamento para sustentar a atividade espacial, e também reflete a desativação de tecnologias antigas e a transição para sistemas mais eficientes e modernos '

# Top 10 Países com mais Foguetes Ativos
grafico12 = 'Este gráfico revela uma mudança notável na liderança espacial atual em comparação com o histórico de foguetes aposentados. Atualmente, a China lidera com 223 foguetes ativos, superando os EUA (208) e a França (113). Essa dominância chinesa reflete seus investimentos massivos e o rápido avanço de seu programa espacial nas últimas décadas, posicionando-a como uma força crescente no cenário espacial global. A presença do "Oceano Pacífico" e "Nova Zelândia" na lista sugere o papel de locais de lançamento ou de pequenas nações que estão ganhando relevância em nichos específicos, como o lançamento de pequenos satélites, muitas vezes por meio de empresas privadas. A Rússia, que dominava a contagem de foguetes aposentados, aparece mais abaixo na lista de ativos (36), indicando uma reconfiguração do cenário de poder espacial, onde a China e os EUA se destacam na vanguarda das operações ativas.'

# Top 10 Países com mais Foguetes Aposentados
grafico13 = 'O gráfico apresenta os 10 países com o maior número de foguetes aposentados, ou seja, que já não estão mais em uso. A Rússia lidera com folga, totalizando 1.359 foguetes aposentados, seguida pelos Estados Unidos, com 1.136, e Cazaquistão, com 657. Esses três países possuem um histórico significativo de lançamentos espaciais, o que explica a quantidade elevada de foguetes desativados. Em seguida aparecem França (190), Japão (88) e China (45). Os últimos colocados são Índia (26), Quênia (9), Israel (6) e Austrália (6), demonstrando uma participação mais modesta nas atividades espaciais. O gráfico destaca o domínio histórico de algumas nações no setor aeroespacial, especialmente durante e após a Guerra Fria.'

# Custo Médio das Missões Espaciais por País
grafico14 = 'O gráfico indica que o Cazaquistão apresenta o custo médio mais alto por missão (aproximadamente $264 USD), seguido por EUA (aproximadamente $216 USD) e França (aproximadamente $171 USD). O elevado custo médio para o Cazaquistão, que abriga o Cosmódromo de Baikonur, sugere que as operações a partir deste local, frequentemente de grande porte e complexidade, contribuem para esse valor. A presença de "Gran Canaria" e "Pacific Missile Range Facility" pode se referir a instalações de rastreamento ou apoio a missões, não necessariamente países lançadores. Notavelmente, Rússia e China, apesar de serem grandes players em número de lançamentos, aparecem com custos médios significativamente mais baixos ($40.54 e $40.27, respectivamente), o que pode refletir metodologias de custo diferentes, uma maior padronização de lançadores ou uma política de preços distinta.'

# Custo Médio das Missões Espaciais por Empresa
grafico15 = 'Este gráfico mostra uma disparidade gritante, com a RVSN URSS liderando com um custo médio de $5000 USD por missão, valor consideravelmente superior ao de qualquer outra entidade. Essa cifra elevadíssima para a RVSN URSS pode ser um reflexo dos vastos recursos investidos no desenvolvimento de foguetes e mísseis intercontinentais durante a Guerra Fria, onde a performance e a capacidade eram priorizadas sobre a economia, ou talvez uma inclusão de custos de desenvolvimento que não são comparáveis com outras empresas. A NASA aparece em segundo lugar, mas com um custo médio muito inferior (aproximadamente $511 USD), seguida por empresas como Boeing ($177 USD), Arianespace ($170 USD) e ULA ($151 USD). A JAXA (Agência de Exploração Aeroespacial do Japão) e a US Air Force também apresentam custos médios mais baixos, indicando que, fora o caso histórico da RVSN URSS, o custo médio por missão para as demais grandes agências e empresas é substancialmente menor e mais nivelado.'

# ------------------------------------

with st.sidebar.expander("Dicionário de Dados", expanded=False, icon=":material/book:"):
    st.caption("""	
    - **Company Name:** Coluna que apresenta os nomes das empresas que realizaram missões espaciais. Possui 4.324 registros não-nulos;
    - **Location:** Coluna que apresenta os locais onde os lançamentos foram realizados. Possui 4.324 registros não-nulos;
    - **Datum:** Coluna que apresenta as datas e os horários dos lançamentos. Possui 4.324 registros não-nulos;
    - **Detail:** Coluna que apresenta o nome do foguete. Possui 4.234 registros não-nulos;
    - **Rocket:** Coluna que apresenta o custo da missão em milhões de dólares. Possui 964 registrolos não-nulos;
    - **Status:** Coluna que apresenta a situação da missão como Sucedida ou Fracassada. Possui 4.324 registros não-nulos;            
    """)


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

        with st.expander("Informações sobre os Países", expanded=False, icon=":material/info:"):
            st.caption(f"{grafico1}")
    

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

        with st.expander("Análise do Gráfico", expanded=False, icon=":material/info:"):
            st.caption(f"{grafico2}")


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

        with st.expander("Análise do Gráfico", expanded=False, icon=":material/info:"):
            st.caption(f"{grafico3}")
    

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

        with st.expander("Análise do Gráfico", expanded=False, icon=":material/info:"):
            st.caption(f"{grafico4}")


    with tab3:
        st.subheader("🏦 Missões Espaciais por Empresa")
        
        # Gráfico de barras com o número de missões por empresa
        company_counts = df['Company Name'].value_counts().reset_index()
        company_counts.columns = ['Company Name', 'Mission Count']
        
        fig = px.bar(company_counts, x='Company Name', y='Mission Count', color='Mission Count',
                    text='Mission Count')
        fig.update_layout(xaxis_title='Empresa', yaxis_title='Número de Missões')
        st.plotly_chart(fig, use_container_width=True)

        with st.expander("Informações sobre as Empresas", expanded=False, icon=":material/info:"):
            st.caption(f"{grafico5}")


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

        with st.expander("Informações sobre o Status das Missões", expanded=False, icon=":material/info:"):
            st.caption(f"{grafico6}")


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

        with st.expander("Análise do Gráfico", expanded=False, icon=":material/info:"):
            st.caption(f"{grafico7}")


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

        with st.expander("Análise do Gráfico", expanded=False, icon=":material/info:"):
            st.caption(f"{grafico8}")


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

        with st.expander("Análise do Gráfico", expanded=False, icon=":material/info:"):
            st.caption(f"{grafico9}")


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

        with st.expander("Análise do Gráfico", expanded=False, icon=":material/info:"):
            st.caption(f"{grafico10}")


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

        with st.expander("Informações sobre os Foguetes", expanded=False, icon=":material/info:"):
            st.caption(f"{grafico11}")


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

        with st.expander("Análise do Gráfico", expanded=False, icon=":material/info:"):
            st.caption(f"{grafico12}")


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

        with st.expander("Análise do Gráfico", expanded=False, icon=":material/info:"):
            st.caption(f"{grafico13}")


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

        with st.expander("Análise do Gráfico", expanded=False, icon=":material/info:"):
            st.caption(f"{grafico14}")


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

        with st.expander("Análise do Gráfico", expanded=False, icon=":material/info:"):
            st.caption(f"{grafico15}")
        