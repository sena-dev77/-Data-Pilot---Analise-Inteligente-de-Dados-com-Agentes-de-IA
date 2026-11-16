import pandas as pd
import plotly.express as px
import streamlit as st
from pathlib import Path

from src.metrics import (
    average_ticket_value,
    monthly_revenue,
    total_orders,
    total_revenue,
)


@st.cache_data
def load_data():
    base_path = Path(__file__).parent.parent  # Sobe de 'src/' para a raiz do projeto
    csv_path = base_path / "data_processed" / "sales_clean.csv"
    return pd.read_csv(csv_path, sep=";", decimal=",")


def main():
    df = load_data()

    with st.sidebar:
        st.subheader(":material/tune: Controle")
        st.caption("Filtre a visualização")
        categories = st.pills(
            "Categorias",
            sorted(df["categoria"].unique()),
            selection_mode="multi",
            width="stretch",
            key="categories",
        )

    filtered_df = df[df["categoria"].isin(categories)] if categories else df

    data = monthly_revenue(filtered_df)

    with st.container(horizontal=True, horizontal_alignment="distribute", vertical_alignment="center"):
        with st.container(gap="xxsmall"):
            st.title(":material/space_dashboard: :violet[DataPilot]", anchor=False)
            st.caption("Visão consolidada das vendas por categoria e período.")
            st.badge("Painel de vendas", icon=":material/space_dashboard:", color="violet")

    st.space("small")

    revenue_panel, secondary_panel = st.columns([1.65, 1])

    with revenue_panel:
        st.metric(
            ":violet-badge[:material/paid: Receita total]",
            f"R$ {total_revenue(filtered_df):,.2f}",
            border=True,
            height=280,
            chart_data=data["receita"],
            chart_type="area",
            delta_color="violet",
        )

    with secondary_panel:
        st.metric(
            ":blue-badge[:material/receipt_long: Pedidos]",
            total_orders(filtered_df),
            border=True,
            height=132,
        )
        st.metric(
            ":green-badge[:material/analytics: Ticket médio]",
            f"R$ {average_ticket_value(filtered_df):,.2f}",
            border=True,
            height=132,
        )

    st.space("small")

    fig = px.line(data, x="mes", y="receita", markers=True)
    fig.update_traces(
        line={"color": "#cba6f7", "width": 3},
        marker={"color": "#b4befe", "size": 7},
        fill="tozeroy",
        fillcolor="rgba(203, 166, 247, 0.08)",
    )
    fig.update_layout(
        height=380,
        margin={"l": 20, "r": 20, "t": 20, "b": 16},
        hovermode="x unified",
        xaxis_title=None,
        yaxis_title=None,
    )
    fig.update_yaxes(tickprefix="R$ ", tickformat="~s")

    with st.container(border=True):
        with st.container(horizontal=True, horizontal_alignment="distribute", vertical_alignment="center"):
            st.subheader(":material/show_chart: Receita por mês")
            st.badge("Mensal", color="blue")
        st.plotly_chart(
            fig,
            width="stretch",
            config={"displayModeBar": False, "scrollZoom": False},
        )


if __name__ == "__main__":
    main()
