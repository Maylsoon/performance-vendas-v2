# 📊 Performance de Vendas V2

Dashboard interativo para acompanhamento de vendas, receita, lucro, margem, estoque e compras.

O projeto utiliza dados armazenados no Google Sheets e realiza a análise com Python e pandas, disponibilizando os indicadores em um dashboard desenvolvido com Streamlit.

## 🎯 Objetivo

Transformar dados operacionais de vendas e compras em informações para acompanhamento da performance comercial e apoio à tomada de decisão.

## 🛠️ Tecnologias

- Python
- Pandas
- Streamlit
- Altair
- Google Sheets

## 📊 Indicadores

O dashboard apresenta:

- Receita
- Lucro bruto
- Margem
- Quantidade vendida
- Evolução de receita e lucro
- Performance por produto
- Performance por tamanho
- Estoque disponível
- Ranking de produtos
- Vendas × Compras
- Saldo entre vendas e compras

## 🔎 Filtros

O usuário pode analisar os dados por:

- Hoje
- Últimos 7 dias
- Este mês
- Tudo
- Período personalizado

O mesmo período selecionado é aplicado às análises de vendas e compras.

## 🔄 Fluxo dos dados

Google Sheets → Python/Pandas → Streamlit → Dashboard

A fonte de dados pode ser atualizada sem necessidade de alterar o código da aplicação.

## 📁 Estrutura

```text
performance_vendas_v2/
│
├── app.py
├── requirements.txt
├── .gitignore
└── README.md
```

## 🚀 Execução local

Instale as dependências:

pip install -r requirements.txt

Execute o dashboard:

streamlit run app.py

## 👤 Autor

Maylson Maia

Projeto desenvolvido para portfólio na área de Dados e Business Intelligence.