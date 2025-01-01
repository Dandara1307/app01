import streamlit as st
import pandas as pd
import plotly.express as px

# Título do app
st.title("Otimização de Transporte e Logística: Análise de Vistoria e Coleta")

# Instruções iniciais antes de carregar a planilha
st.write("""
    Bem-vindo ao aplicativo de análise de logística e transporte.
    Por favor, carregue sua base de dados (CSV ou Excel) para visualizar a análise.
    O app irá gerar gráficos sobre o status da vistoria e da coleta, além de mostrar a tabela completa.
""")

# Opção para carregar uma base de dados (CSV ou Excel)
uploaded_file = st.file_uploader("Carregue sua base de dados (CSV ou Excel)", type=["csv", "xlsx"])

# Inicialização do DataFrame
df = None

# Verifica se o arquivo foi carregado
if uploaded_file is not None:
    file_extension = uploaded_file.name.split('.')[-1]

    # Leitura da base de dados dependendo da extensão
    if file_extension == 'csv':
        df = pd.read_csv(uploaded_file)
    elif file_extension == 'xlsx':
        df = pd.read_excel(uploaded_file)

    # Verificar se o cabeçalho está correto e garantir que os nomes das colunas sejam consistentes
    st.write("Exibindo as primeiras linhas da base de dados para conferência do cabeçalho:")
    st.write(df.head())

    # Limpar espaços e caracteres especiais nos nomes das colunas
    df.columns = df.columns.str.strip().str.replace(' ', '_').str.lower()

    # Garantir que as colunas estão presentes no DataFrame
    if 'status_vistoria' in df.columns and 'status_da_coleta' in df.columns:
        # Exibir a tabela completa de dados
        st.header("Tabela Completa de Dados")
        st.write(df)  # Exibe o DataFrame completo em forma de tabela interativa

        # Filtragem dos dados para status de vistoria
        status_vistoria = df['status_vistoria'].value_counts().reset_index()
        status_vistoria.columns = ['Status da Vistoria', 'Quantidade']
        status_vistoria['Porcentagem'] = (status_vistoria['Quantidade'] / status_vistoria['Quantidade'].sum()) * 100
        status_vistoria['Porcentagem'] = status_vistoria['Porcentagem'].round(2).astype(str) + '%'

        # Filtragem dos dados para status da coleta
        status_coleta = df['status_da_coleta'].value_counts().reset_index()
        status_coleta.columns = ['Status da Coleta', 'Quantidade']
        status_coleta['Porcentagem'] = (status_coleta['Quantidade'] / status_coleta['Quantidade'].sum()) * 100
        status_coleta['Porcentagem'] = status_coleta['Porcentagem'].round(2).astype(str) + '%'

        # Mostrar as porcentagens de cada status
        st.subheader("Status de Vistoria e Coleta")
        st.write("Status de Vistoria:")
        st.write(status_vistoria)
        st.write("Status de Coleta:")
        st.write(status_coleta)

        # **Gráfico de Pizza para o Status da Vistoria**
        st.header("Distribuição do Status da Vistoria (Gráfico de Pizza)")

        # Cores para o gráfico de Vistoria
        color_map_vistoria = {
            'Ok': '#D3D3D3',       # Cinza Claro
            'Pendente': '#A9A9A9',  # Cinza Médio
            'Cancelada': '#A9A9A9', # Cinza Médio (substituindo o vermelho escuro)
        }

        # Gerar o gráfico de pizza para a vistoria
        fig_vistoria = px.pie(status_vistoria,
                              names='Status da Vistoria',
                              values='Quantidade',
                              title='Distribuição do Status da Vistoria (Pizza)',
                              color='Status da Vistoria',
                              color_discrete_map=color_map_vistoria,
                              labels={'Quantidade': 'Quantidade', 'Status da Vistoria': 'Status da Vistoria'})

        st.plotly_chart(fig_vistoria)

        # **Gráfico de Colunas para o Status da Coleta**
        st.header("Distribuição do Status da Coleta (Gráfico de Colunas)")

        # Cores para o gráfico de Coleta
        color_map_coleta = {
            'Concluído': '#D3D3D3',   # Cinza Claro
            'Pendente': '#A9A9A9',    # Cinza Médio
            'Cancelada': '#A9A9A9',   # Cinza Médio (substituindo o cinza escuro)
        }

        # Gerar o gráfico de colunas para a coleta
        fig_coleta = px.bar(status_coleta,
                            x='Status da Coleta',
                            y='Quantidade',
                            title='Distribuição do Status da Coleta (Colunas)',
                            color='Status da Coleta',
                            color_discrete_map=color_map_coleta,
                            labels={'Quantidade': 'Quantidade', 'Status da Coleta': 'Status da Coleta'},
                            barmode='group')

        # Ajustando o gráfico de colunas
        fig_coleta.update_traces(marker=dict(line=dict(width=1)))
        fig_coleta.update_layout(bargap=0.2)
        st.plotly_chart(fig_coleta)

        # **Análise Geral e Pontos Importantes**
        st.header("Análise Geral e Pontos Importantes")
        st.write("""
            **Análise do Status da Vistoria:**
            - **Cancelada**: Embora a taxa de cancelamento seja baixa, é importante investigar as causas desses cancelamentos para evitar mais problemas e ineficiência.
            - **Ok**: A maior parte das vistorias está sendo concluída com sucesso, o que indica boa eficiência na operação. No entanto, ainda há espaço para otimização.
            - **Pendente**: A alta quantidade de pendências deve ser investigada. Pode haver gargalos ou falhas no planejamento das vistorias que precisam ser resolvidas.

            **Análise do Status da Coleta:**
            - **Cancelada**: Similar às vistorias, as coletas canceladas também devem ser analisadas para identificar causas subjacentes.
            - **Concluído**: Um bom número de coletas concluídas, mas com espaço para melhorias.
            - **Pendente**: Uma alta porcentagem de coletas pendentes, o que pode resultar em atrasos e custos adicionais. Deve ser uma prioridade reduzir esse número.
        """)
    else:
        st.error("As colunas 'status_vistoria' ou 'status_da_coleta' não foram encontradas no DataFrame.")
