# DataPilot

Painel de vendas em Streamlit com uma página para conversar com os dados via OpenRouter.

## Como rodar

1. Instale as dependências: `uv sync` (ou `pip install openrouter pandas plotly python-dotenv streamlit`).
2. Copie `.env.example` para `.env` e coloque sua chave em `OPENROUTER_API_KEY`.
3. (Opcional) Regere os dados limpos: `python -m src.preprocess`.
4. Rode: `streamlit run main.py`.

## Estrutura

- `main.py`: navegação entre as páginas.
- `src/app.py`: painel de vendas.
- `src/data_chat.py`: página "Converse com os dados".
- `src/llm.py`: monta o contexto e chama o OpenRouter.
- `src/metrics.py`: cálculos de vendas.
- `src/preprocess.py`: limpeza do `sales.csv`.
