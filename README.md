# 📊 Performance de Vendas V2

**Dashboard interativo para acompanhamento de vendas, receita, lucro, margem, estoque e compras.**

🔗 **[Acessar Dashboard Online](https://performance-vendas-v2-n5c7yc8lytgl5tfspjxfja.streamlit.app/)**

O projeto utiliza dados armazenados no Google Sheets e realiza a análise com Python e pandas, disponibilizando os indicadores em um dashboard desenvolvido com Streamlit.

## 🎯 Objetivo

Transformar dados operacionais de vendas e compras em informações para acompanhamento da performance comercial e apoio à tomada de decisão.

## 🛠️ Tecnologias

* Python
* Pandas
* Streamlit
* Altair
* Google Sheets

## 📊 Indicadores

O dashboard apresenta:

* Receita
* Lucro bruto
* Margem
* Quantidade vendida
* Evolução de receita e lucro
* Performance por produto
* Performance por tamanho
* Estoque disponível
* Ranking de produtos
* Vendas × Compras
* Saldo entre vendas e compras

## 🔎 Filtros

O usuário pode analisar os dados por:

* Hoje
* Últimos 7 dias
* Este mês
* Tudo
* Período personalizado

O mesmo período selecionado é aplicado às análises de vendas e compras.

## 🔄 Fluxo dos dados

```text
Google Sheets
      ↓
Python / Pandas
      ↓
Streamlit
      ↓
Dashboard Online
```

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

```bash
pip install -r requirements.txt
```

Execute o dashboard:

```bash
streamlit run app.py
```

O Streamlit disponibilizará o dashboard no navegador.

## 💡 Aplicação

O projeto foi desenvolvido com foco em uma situação real de negócio, utilizando dados de vendas e compras para demonstrar como Python e ferramentas de BI podem transformar dados operacionais em informações para gestão.

## 🌐 Dashboard

A aplicação está publicada e pode ser acessada diretamente:

**[Performance de Vendas V2 — Dashboard Online](https://performance-vendas-v2-n5c7yc8lytgl5tfspjxfja.streamlit.app/)**

## 👤 Autor

**Maylson Maia**

Projeto desenvolvido para portfólio na área de Dados e Business Intelligence.
