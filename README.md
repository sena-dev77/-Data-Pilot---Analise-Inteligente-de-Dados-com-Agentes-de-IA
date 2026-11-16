# 📊 DataPilot — Painel de Vendas & Chat Analítico com IA

O **DataPilot** é uma aplicação web desenvolvida em Python com **Streamlit** que combina um dashboard interativo de indicadores comerciais com um **assistente conversacional de dados** integrado ao **OpenRouter**.

O princípio central do projeto é a **confiabilidade analítica**: todo cálculo matemático e agregação é executado de forma determinística pelo **Pandas/Python**, cabendo ao modelo de linguagem (LLM) apenas interpretar a pergunta do usuário em português e explicar os resultados obtidos — eliminando alucinações numéricas.

---

## 🎯 Funcionalidades

### 1. Painel de Vendas (`Painel`)
- **KPIs Principais:** Receita Total, Total de Pedidos Concluídos e Ticket Médio.
- **Filtro Dinâmico:** Filtragem interativa por categoria de produto na barra lateral.
- **Evolução Temporal:** Gráfico de linha e área com a receita mensal consolidada via **Plotly**.

### 2. Converse com os Dados (`Converse com os dados`)
- Interface de chat em linguagem natural para consultar métricas de negócio (ex.: *"Qual mês teve a maior receita?"*, *"Qual a taxa de cancelamento?"*, *"Quais cidades mais faturam?"*).
- Respostas baseadas exclusivamente nas métricas calculadas pelo backend, utilizando o modelo gratuito `openrouter/free`.

---

## 🚀 Melhoria Implementada

Além das métricas base do projeto, foi implementada a análise de **Faturamento e Volume por Cidade (`revenue_by_city`)** em `src/metrics.py` e integrada ao contexto analítico do agente em `src/llm.py`. Isso permite identificar a distribuição geográfica das vendas e responder perguntas sobre desempenho regional diretamente no chat.

---

## 🛠️ Métricas e Funções Disponíveis (`src/metrics.py`)

Todas as métricas de faturamento consideram exclusivamente pedidos com status **`concluido`**:

| Função | Descrição |
| :--- | :--- |
| `total_revenue(df)` | Calcula a receita total acumulada (`Decimal`). |
| `total_orders(df)` | Conta a quantidade de pedidos únicos concluídos. |
| `products_sold(df)` | Soma o total de unidades vendidas. |
| `unique_clients(df)` | Conta a quantidade de clientes únicos atendidos. |
| `average_ticket_value(df)` | Calcula o ticket médio (`receita total / pedidos`). |
| `cancellation_rate(df)` | Calcula o percentual de pedidos cancelados sobre o total. |
| `monthly_revenue(df)` | Agrupa a receita por mês (`AAAA-MM`). |
| `orders_by_month(df)` | Agrupa o volume de pedidos únicos por mês. |
| `revenue_by_product(df)` | Ranking de receita e unidades por produto. |
| `revenue_by_category(df)` | Ranking de receita e unidades por categoria. |
| `revenue_by_city(df)` | **[Melhoria]** Ranking de receita e unidades por cidade. |

---

## 🗂️ Estrutura do Projeto

```text
datapilot/
├── data_processed/
│   └── sales_clean.csv      # Base tratada (separador ';', decimal ',')
├── src/
│   ├── app.py               # Interface do painel interativo e gráficos
│   ├── data_chat.py         # Interface de chat com histórico de sessão
│   ├── llm.py               # Integração com OpenRouter e montagem de contexto
│   ├── metrics.py           # Regras de negócio e cálculos das métricas
│   └── preprocess.py        # Pipeline de limpeza e padronização dos dados
├── .env.example             # Modelo de variáveis de ambiente
├── .gitignore               # Arquivos ignorados pelo Git (inclui .env)
├── main.py                  # Ponto de entrada e navegação entre páginas
├── pyproject.toml           # Dependências e metadados do projeto
├── README.md                # Documentação do projeto
└── sales.csv                # Base de dados bruta de vendas
