import streamlit as st
import pandas as pd
# matplotlib dark theme
import matplotlib.pyplot as plt
import matplotlib
from pyecharts import options as opts
from pyecharts.charts import Bar
from pyecharts.charts import Line
from streamlit_echarts import st_pyecharts

st.title('Trabalho Final')
st.header('Disciplina: Business Intelligence')
st.subheader('Professor: Erik Santos')

st.divider()

# Carregando e tratando o dataset
df = pd.read_csv('Superstore Sales Training_PBI.csv', sep=';', encoding='latin-1')
df['Sales'] = df['Sales'].str.replace('.', '').str.replace(',', '.').astype(float)
df['Profit'] = df['Profit'].str.replace('.', '').str.replace(',', '.').astype(float)
df['Order Date'] = pd.to_datetime(df['Order Date'], format='%d/%m/%Y')
df['Ship Date'] = pd.to_datetime(df['Ship Date'], format='%d/%m/%Y')

st.sidebar.title('Regiao')
regiao = st.sidebar.selectbox('Selecione a regiao', df['Region'].unique())

# st.sidebar.title('Categoria')
# categoria = st.sidebar.selectbox('Selecione a categoria', df['Category'].unique())

filtro_regiao = df['Region'] == regiao
# filtro_categoria = df['Category'] == categoria

# groupby region and aggregate sales and profit
df_grouped = df.groupby('Region').agg({'Sales': 'sum', 'Profit': 'sum'}).sort_values(by='Sales', ascending=False)
st.subheader('Informações Globais')
bar = (
    Bar()
    .add_xaxis(df_grouped.index.tolist())
    .add_yaxis("Sales", df_grouped['Sales'].tolist(), label_opts=opts.LabelOpts(is_show=False))
    .add_yaxis("Profit", df_grouped['Profit'].tolist(), label_opts=opts.LabelOpts(is_show=False))
    .set_global_opts(title_opts=opts.TitleOpts(title="Sales and Profit by Region"))
)
st_pyecharts(bar)

### Parte Total de Vendas e Lucro
df_grouped = df.groupby('Department').agg({'Sales': 'sum', 'Profit': 'sum'}).sort_values(by='Sales', ascending=False)
st.subheader('Informações Globais')
bar = (
    Bar()
    .add_xaxis(df_grouped.index.tolist())
    .add_yaxis("Sales", df_grouped['Sales'].tolist())
    .add_yaxis("Profit", df_grouped['Profit'].tolist())
    .set_global_opts(title_opts=opts.TitleOpts(title="Sales and Profit by Department"))
)
st_pyecharts(bar)

# df_filtrado = df[filtro_regiao & filtro_categoria]
df_filtrado = df[filtro_regiao]

### Parte de Vendas e Lucro por Regiao
df_grouped_filtrado = df_filtrado.groupby('Department').agg({'Sales': 'sum', 'Profit': 'sum'}).sort_values(by='Sales', ascending=False)
st.subheader('Informações por Região')
bar = (
    Bar()
    .add_xaxis(df_grouped_filtrado.index.tolist())
    .add_yaxis("Sales", df_grouped_filtrado['Sales'].tolist())
    .add_yaxis("Profit", df_grouped_filtrado['Profit'].tolist())
    .set_global_opts(title_opts=opts.TitleOpts(title="Sales and Profit by Department"))
)
st_pyecharts(bar)

st.divider()

### Top 10 clientes por regiao
df_grouped_filtrado = df_filtrado.groupby('Customer Name').agg({'Sales': 'sum', 'Profit': 'sum'}).sort_values(by='Sales', ascending=False).head(5)
st.subheader('Top 10 clientes por região')
bar = (
    Bar()
    .add_xaxis(df_grouped_filtrado.index.tolist())
    .add_yaxis("Sales", df_grouped_filtrado['Sales'].tolist(), label_opts=opts.LabelOpts(is_show=False))
    .add_yaxis("Profit", df_grouped_filtrado['Profit'].tolist(), label_opts=opts.LabelOpts(is_show=False))
    .set_global_opts(title_opts=opts.TitleOpts(title="Sales and Profit by Department"))
)
st_pyecharts(bar)

st.divider()

# Vendas e Lucro por mes ao longo do tempo
df_filtrado = df[filtro_regiao]
df_grouped_filtrado = df_filtrado.groupby('Order Date').agg({'Sales': 'sum', 'Profit': 'sum'}).sort_values(by='Order Date', ascending=True)
st.subheader('Vendas e Lucro por mes ao longo do tempo')

df['Order Date'] = pd.to_datetime(df['Order Date'])
df['YearMonth'] = df['Order Date'].dt.to_period('M')
df_grouped = df.groupby('YearMonth').agg({'Sales': 'sum', 'Profit': 'sum'}).sort_index()

# Criar um gráfico de linhas com Pyecharts
line = (
    Line()
    .add_xaxis(df_grouped.index.astype(str).tolist()) # Converte o índice em uma lista de strings
    .add_yaxis("Sales", df_grouped['Sales'].tolist(), label_opts=opts.LabelOpts(is_show=False))
    .add_yaxis("Profit", df_grouped['Profit'].tolist(), label_opts=opts.LabelOpts(is_show=False))
    .set_global_opts(title_opts=opts.TitleOpts(title="Sales and Profit Over Time"))
)

# Use a função st_pyecharts para exibir o gráfico
st_pyecharts(line)
