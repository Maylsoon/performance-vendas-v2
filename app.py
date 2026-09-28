import streamlit as st
import pandas as pd


# =========================
# CONFIGURAÇÃO DA PÁGINA
# =========================

st.set_page_config(
    page_title="Performance de Vendas",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# =========================
# ESTILO VISUAL
# =========================

st.markdown("""
<style>

    /* Título principal */
    .main-title {
        font-size: 32px;
        font-weight: 700;
        margin-bottom: 0px;
    }

    /* Subtítulo */
    .subtitle {
        font-size: 16px;
        color: #666;
        margin-top: 0px;
        margin-bottom: 25px;
    }

    /* Espaçamento entre seções */
    .section-space {
        margin-top: 30px;
    }

</style>
""", unsafe_allow_html=True)

# =========================
# DADOS
# =========================

url = "https://docs.google.com/spreadsheets/d/1OzIG2ZC4kIBtvgpyJ0ueF0uuSrMBt5hws7Qj3h7wHQQ/export?format=csv&gid=735400805"
url_2 = "https://docs.google.com/spreadsheets/d/1OzIG2ZC4kIBtvgpyJ0ueF0uuSrMBt5hws7Qj3h7wHQQ/export?format=csv&gid=733381442"

df = pd.read_csv(url)
df_giro = pd.read_csv(url_2)

# corrigindo tipo data
df['data'] = pd.to_datetime(df['data'], format='%d/%m/%Y')
df_giro['data'] = pd.to_datetime(df_giro['data'], format='%d/%m/%Y')

# criando mês e ano
df["ano"] = df["data"].dt.year
df["mes"] = df["data"].dt.month

# corrigindo valores para tipo float
df['preco_unitario'] = df['preco_unitario'].str.replace('R$ ', '').str.replace(',', '.').astype(float)
df['frete'] = df['frete'].str.replace('R$ ', '').str.replace(',', '.').astype(float)
df['desconto'] = df['desconto'].str.replace('R$ ', '').str.replace(',', '.').astype(float)
df['acréscimo'] = df['acréscimo'].str.replace('R$ ', '').str.replace(',', '.').astype(float)
df['receita'] = df['receita'].str.replace('R$ ', '').str.replace(',', '.').astype(float)
df['custo_total'] = df['custo_total'].str.replace('R$ ', '').str.replace(',', '.').astype(float)

df_giro['valor'] = df_giro['valor'].str.replace('R$ ', '').str.replace(',', '.').astype(float)

# excluindo colunas lucro bruto e margem 
df = df.drop(['lucro_bruto', 'margem'], axis=1)

# recriando-as a partir do python
df['lucro_bruto'] = df['receita'] - df['custo_total']
df['margem'] = round(df['lucro_bruto'] / df['receita'],2)


# =========================
# TÍTULO
# =========================

st.markdown(
    '<div class="main-title">📊 Performance de Vendas</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="subtitle">Acompanhamento de vendas, receita, lucro e margem</div>',
    unsafe_allow_html=True
)

# =========================
# FILTRO DE PERÍODO
# =========================

st.sidebar.header("Período")

periodo = st.sidebar.selectbox(
    "Visualizar",
    [
        "Hoje",
        "Últimos 7 dias",
        "Este mês",
        "Tudo",
        "Personalizado"
    ],
    index=1
)

hoje = pd.Timestamp.today().normalize()

# =========================
# APLICAÇÃO DO FILTRO
# =========================

if periodo == "Hoje":

    df_filtrado = df[
        df["data"].dt.normalize() == hoje
    ]

elif periodo == "Últimos 7 dias":

    data_inicio = hoje - pd.Timedelta(days=6)

    df_filtrado = df[
        df["data"].dt.normalize().between(
            data_inicio,
            hoje
        )
    ]

elif periodo == "Este mês":

    df_filtrado = df[
        (df["data"].dt.year == hoje.year) &
        (df["data"].dt.month == hoje.month)
    ]

elif periodo == "Tudo":

    df_filtrado = df.copy()

elif periodo == "Personalizado":

    data_inicio = st.sidebar.date_input(
        "Data inicial",
        value=df["data"].min().date()
    )

    data_fim = st.sidebar.date_input(
        "Data final",
        value=df["data"].max().date()
    )

    df_filtrado = df[
        df["data"].dt.date.between(
            data_inicio,
            data_fim
        )
    ]

st.caption(f"Período analisado: {periodo}")

# =========================
# COMPRAS POR DIA
# =========================

compras_dia = df_giro.groupby('data')['valor'].sum().reset_index()

# =========================
# FILTRO DE COMPRAS
# =========================

if periodo == "Hoje":

    giro_filtrado = df_giro[
        df_giro["data"].dt.normalize() == hoje
    ]

elif periodo == "Últimos 7 dias":

    data_inicio = hoje - pd.Timedelta(days=6)

    giro_filtrado = df_giro[
        df_giro["data"].dt.normalize().between(
            data_inicio,
            hoje
        )
    ]

elif periodo == "Este mês":

    giro_filtrado = df_giro[
        (df_giro["data"].dt.year == hoje.year) &
        (df_giro["data"].dt.month == hoje.month)
    ]

elif periodo == "Tudo":

    giro_filtrado = df_giro.copy()

elif periodo == "Personalizado":

    giro_filtrado = df_giro[
        df_giro["data"].dt.date.between(
            data_inicio,
            data_fim
        )
    ]

# =========================
# VENDAS POR DIA
# =========================

vendas_dia = (
    df_filtrado
    .groupby("data")["receita"]
    .sum()
    .reset_index()
)

# =========================
# VENDAS E COMPRAS POR DIA
# =========================

vendas_dia = (
    df_filtrado
    .assign(
        data=df_filtrado["data"].dt.normalize()
    )
    .groupby("data")["receita"]
    .sum()
    .reset_index()
    .rename(columns={"receita": "vendas"})
)


compras_dia = (
    giro_filtrado
    .assign(
        data=giro_filtrado["data"].dt.normalize()
    )
    .groupby("data")["valor"]
    .sum()
    .reset_index()
    .rename(columns={"valor": "compras"})
)




# =========================
# CRUZAMENTO VENDAS × COMPRAS
# =========================

vendas_compras = pd.merge(
    vendas_dia,
    compras_dia,
    on="data",
    how="outer"
).fillna(0)

vendas_compras = (
    vendas_compras
    .sort_values("data")
    .reset_index(drop=True)
)

vendas_compras["saldo"] = (
    vendas_compras["vendas"]
    - vendas_compras["compras"]
)

# =========================
# KPIs
# =========================

receita = df_filtrado["receita"].sum()
lucro = df_filtrado["lucro_bruto"].sum()
quantidade = df_filtrado["quantidade"].sum()

margem = (
    lucro / receita * 100
    if receita != 0
    else 0
)

col1, col2, col3, col4 = st.columns(4)

col1.metric(
    "Receita",
    f"R$ {receita:,.2f}"
)

col2.metric(
    "Lucro Bruto",
    f"R$ {lucro:,.2f}"
)

col3.metric(
    "Margem",
    f"{margem:.1f}%"
)

col4.metric(
    "Quantidade Vendida",
    f"{quantidade:,.0f}"
)

# =========================
# INSIGHTS AUTOMÁTICOS
# =========================

st.subheader("💡 Destaques do período")

produto_receita = (
    df_filtrado
    .groupby("produto")["receita"]
    .sum()
    .sort_values(ascending=False)
)

if not produto_receita.empty:

    produto_top = produto_receita.index[0]
    receita_top = produto_receita.iloc[0]

    st.info(
        f"🏆 **Produto com maior receita:** {produto_top} "
        f"— R$ {receita_top:,.2f}"
    )

else:

    st.warning("Não há vendas no período selecionado.")


# =========================
# PRODUTO COM MAIOR LUCRO
# =========================

produto_lucro = (
    df_filtrado
    .groupby("produto")["lucro_bruto"]
    .sum()
    .sort_values(ascending=False)
)

if not produto_lucro.empty:

    produto_top_lucro = produto_lucro.index[0]
    lucro_top = produto_lucro.iloc[0]

    st.info(
        f"💰 **Produto com maior lucro:** {produto_top_lucro} "
        f"— R$ {lucro_top:,.2f}"
    )

else:

    st.warning("Não há vendas no período selecionado.")

# =========================
# PRODUTO MAIS VENDIDO
# =========================

produto_quantidade = (
    df_filtrado
    .groupby("produto")["quantidade"]
    .sum()
    .sort_values(ascending=False)
)

if not produto_quantidade.empty:

    produto_top_qtd = produto_quantidade.index[0]
    quantidade_top = produto_quantidade.iloc[0]

    st.info(
        f"📦 **Produto mais vendido:** {produto_top_qtd} "
        f"— {quantidade_top:,.0f} unidades"
    )

else:

    st.warning("Não há vendas no período selecionado.")

# =========================
# PRODUTO COM MELHOR MARGEM
# =========================

margem_produto = (
    df_filtrado
    .groupby("produto")
    .agg(
        receita=("receita", "sum"),
        lucro=("lucro_bruto", "sum")
    )
)

margem_produto["margem"] = (
    margem_produto["lucro"] /
    margem_produto["receita"] * 100
)

margem_produto = margem_produto.sort_values(
    "margem",
    ascending=False
)

if not margem_produto.empty:

    produto_melhor_margem = margem_produto.index[0]
    melhor_margem = margem_produto.iloc[0]["margem"]

    st.info(
        f"📈 **Melhor margem:** {produto_melhor_margem} "
        f"— {melhor_margem:.1f}%"
    )

else:

    st.warning("Não há vendas no período selecionado.")


# =========================
# EVOLUÇÃO DE RECEITA E LUCRO
# =========================

import altair as alt


if periodo == "Tudo":

    vendas_tempo = (
        df_filtrado
        .assign(
            data_periodo=df_filtrado["data"].dt.to_period("M").dt.to_timestamp()
        )
        .groupby("data_periodo", as_index=False)
        .agg(
            receita=("receita", "sum"),
            lucro=("lucro_bruto", "sum")
        )
        .sort_values("data_periodo")
    )

    formato_data = "%b/%Y"

else:

    vendas_tempo = (
        df_filtrado
        .assign(
            data_periodo=df_filtrado["data"].dt.floor("D")
        )
        .groupby("data_periodo", as_index=False)
        .agg(
            receita=("receita", "sum"),
            lucro=("lucro_bruto", "sum")
        )
        .sort_values("data_periodo")
    )

    formato_data = "%d/%m"

col1, col2 = st.columns(2)

with col1:
    st.subheader("📈 Evolução de Receita e Lucro")


    grafico = alt.Chart(vendas_tempo).transform_fold(
    ["receita", "lucro"],
    as_=["tipo", "valor"]
    ).mark_line(
    point=True
    ).encode(
    x=alt.X(
    "data_periodo:T",
    title=None,
    axis=alt.Axis(
        format="%d/%m",
        labelAngle=0,
        values=vendas_tempo["data_periodo"].tolist()
    )
    ),
    y=alt.Y(
        "valor:Q",
        title="Valor (R$)"
    ),
    color=alt.Color(
        "tipo:N",
        title=None
    ),
    tooltip=[
        alt.Tooltip(
            "data_periodo:T",
            title="Período",
            format=formato_data
        ),
        alt.Tooltip(
            "tipo:N",
            title="Indicador"
        ),
        alt.Tooltip(
            "valor:Q",
            title="Valor",
            format=",.2f"
        )
    ]
    ).properties(
    height=350
    )


    st.altair_chart(
    grafico,
    use_container_width=True
    )

with col2:

    st.subheader("🛒 Vendas × Compras")

    grafico_compras = alt.Chart(vendas_compras).transform_fold(
        ["vendas", "compras"],
        as_=["tipo", "valor"]
    ).mark_line(
        point=True
    ).encode(
        x=alt.X(
            "data:T",
            title=None,
            axis=alt.Axis(
                format="%d/%m",
                labelAngle=0,
                values=vendas_compras["data"].tolist()
            )
        ),
        y=alt.Y(
            "valor:Q",
            title="Valor (R$)"
        ),
        color=alt.Color(
            "tipo:N",
            title=None
        ),
        tooltip=[
            alt.Tooltip(
                "data:T",
                title="Data",
                format="%d/%m"
            ),
            alt.Tooltip(
                "tipo:N",
                title="Movimento"
            ),
            alt.Tooltip(
                "valor:Q",
                title="Valor",
                format=",.2f"
            )
        ]
    ).properties(
        height=350
    )

    st.altair_chart(
        grafico_compras,
        use_container_width=True
    )

# =========================
# RESUMO VENDAS × COMPRAS
# =========================

total_vendas = vendas_compras["vendas"].sum()
total_compras = vendas_compras["compras"].sum()

saldo = total_vendas - total_compras

col1, col2, col3 = st.columns(3)

col1.metric(
    "🛍️ Total vendido",
    f"R$ {total_vendas:,.2f}"
)

col2.metric(
    "🛒 Total comprado",
    f"R$ {total_compras:,.2f}"
)

col3.metric(
    "💰 Saldo Vendas − Compras",
    f"R$ {saldo:,.2f}"
)

# =========================
# RANKING DE PRODUTOS
# =========================

ranking_produtos = (
    df_filtrado
    .groupby("produto")
    .agg(
        quantidade=("quantidade", "sum"),
        receita=("receita", "sum"),
        lucro=("lucro_bruto", "sum")
    )
)

ranking_produtos["margem"] = (
    ranking_produtos["lucro"] /
    ranking_produtos["receita"] * 100
).round(2)

ranking_produtos = (
    ranking_produtos
    .sort_values("receita", ascending=False)
    .reset_index()
)

st.subheader("🏆 Ranking de Produtos")

st.dataframe(
    ranking_produtos.style.format({
        "quantidade": "{:,.0f}",
        "receita": "R$ {:,.2f}",
        "lucro": "R$ {:,.2f}",
        "margem": "{:.1f}%"
    }),
    use_container_width=True,
    hide_index=True
)

# ==============================
# Performance por tamanho
# ==============================

tamanho = (
    df_filtrado
    .groupby("tamanho", as_index=False)
    .agg(
        quantidade=("quantidade", "sum"),
        receita=("receita", "sum"),
        lucro=("lucro_bruto", "sum")
    )
    .sort_values("quantidade", ascending=False)
)

st.subheader("📦 Vendas por Tamanho")

st.bar_chart(
    tamanho.set_index("tamanho")["quantidade"]
)

estoque = (
    df_filtrado
    .groupby("produto", as_index=False)
    .agg(
        estoque_disponivel=("estoque_disponivel", "sum"),
        quantidade_vendida=("quantidade", "sum"),
        receita=("receita", "sum")
    )
    .sort_values(
        "estoque_disponivel",
        ascending=False
    )
)

st.subheader("📦 Estoque por Produto")

st.dataframe(
    estoque,
    use_container_width=True
)