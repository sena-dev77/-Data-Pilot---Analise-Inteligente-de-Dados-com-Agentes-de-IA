"""Limpa o sales.csv e gera data_processed/sales_clean.csv.

Rode uma vez (ou quando o sales.csv mudar), da raiz do projeto:
    python -m src.preprocess
"""

from pathlib import Path

import pandas as pd

ROOT = Path(__file__).parent.parent
RAW_PATH = ROOT / "sales.csv"
CLEAN_PATH = ROOT / "data_processed" / "sales_clean.csv"


def main() -> None:
    df = pd.read_csv(RAW_PATH)

    # errors="coerce" transforma datas inválidas em nulo (NaT)
    df["data"] = pd.to_datetime(df["data"], errors="coerce")

    # Período ano-mês, ex.: 2025-02
    df["mes"] = df["data"].dt.to_period("M").astype(str)

    # Padroniza o status: sem espaços extras e em minúsculas
    df["status"] = df["status"].str.strip().str.lower()

    # Remove linhas idênticas duplicadas
    df = df.drop_duplicates()

    # Receita por linha de venda
    df["receita"] = df["quantidade"] * df["preco_unitario"]

    CLEAN_PATH.parent.mkdir(exist_ok=True)
    df.to_csv(CLEAN_PATH, index=False, decimal=",", sep=";")
    print(f"{len(df)} linhas salvas em {CLEAN_PATH}")


if __name__ == "__main__":
    main()
