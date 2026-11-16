import streamlit as st

from src.app import main as dashboard

st.set_page_config(
    page_title="DataPilot",
    page_icon=":material/analytics:",
    layout="wide",
)

pages = [
    st.Page(
        dashboard,
        title="Painel",
        icon=":material/space_dashboard:",
        url_path="painel",
        default=True,
    ),
    st.Page(
        "src/data_chat.py",
        title="Converse com os dados",
        icon=":material/chat:",
        url_path="data_chat",
    ),
]

st.navigation(pages).run()
