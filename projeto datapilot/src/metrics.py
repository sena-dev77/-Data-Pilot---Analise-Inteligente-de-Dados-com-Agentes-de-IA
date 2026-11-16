from decimal import Decimal

import pandas as pd


def completed_orders(df: pd.DataFrame) -> pd.DataFrame:
    return df[df["status"] == "concluido"].copy()


def total_revenue(df: pd.DataFrame) -> Decimal:
    # Passar por str evita imprecisões de float ao criar o Decimal
    return Decimal(str(completed_orders(df)["receita"].sum()))


def total_orders(df: pd.DataFrame) -> int:
    return completed_orders(df)["pedido_id"].nunique()


def products_sold(df: pd.DataFrame) -> int:
    return int(completed_orders(df)["quantidade"].sum())


def unique_clients(df: pd.DataFrame) -> int:
    return completed_orders(df)["cliente_id"].nunique()


def average_ticket_value(df: pd.DataFrame) -> Decimal:
    orders = total_orders(df)
    if orders == 0:
        return Decimal(0)
    return total_revenue(df) / orders


def cancellation_rate(df: pd.DataFrame) -> float:
    total = df["pedido_id"].nunique()
    cancelled = df.loc[df["status"] == "cancelado", "pedido_id"].nunique()
    return (cancelled / total * 100) if total else 0.0


def monthly_revenue(df: pd.DataFrame) -> pd.DataFrame:
    return (
        completed_orders(df)
        .groupby("mes", as_index=False)[["receita"]]
        .sum()
        .sort_values(by="mes")
    )


def revenue_by_product(df: pd.DataFrame) -> pd.DataFrame:
    return (
        completed_orders(df)
        .groupby("produto", as_index=False)
        .agg(receita=("receita", "sum"), unidades=("quantidade", "sum"))
        .sort_values("receita", ascending=False)
    )


def orders_by_month(df: pd.DataFrame) -> pd.DataFrame:
    return (
        completed_orders(df)
        .groupby("mes", as_index=False)
        .agg(pedidos=("pedido_id", "nunique"))
        .sort_values("mes")
    )


def revenue_by_category(df: pd.DataFrame) -> pd.DataFrame:
    return (
        completed_orders(df)
        .groupby("categoria", as_index=False)
        .agg(receita=("receita", "sum"), unidades=("quantidade", "sum"))
        .sort_values("receita", ascending=False)
    )

def revenue_by_city(df: pd.DataFrame) -> pd.DataFrame:
    return (
        completed_orders(df)
        .assign(cidade=lambda d: d["cidade"].str.strip())
        .groupby("cidade", as_index=False)
        .agg(receita=("receita", "sum"), unidades=("quantidade", "sum"))
        .sort_values("receita", ascending=False)
    )