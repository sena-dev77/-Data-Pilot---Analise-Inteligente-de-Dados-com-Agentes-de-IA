import streamlit as st

from src.app import load_data
from src.llm import ask_openrouter

st.title(":material/chat: :violet[Converse com os dados]", anchor=False)
st.caption("Pergunte sobre as vendas e a IA responde com base nos dados calculados.")

df = load_data()

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if question := st.chat_input("Ex.: qual mês teve a maior receita?"):
    st.session_state.messages.append({"role": "user", "content": question})
    with st.chat_message("user"):
        st.markdown(question)

    with st.chat_message("assistant"):
        with st.spinner("Analisando os dados..."):
            answer = ask_openrouter(question, df)
        st.markdown(answer)

    st.session_state.messages.append({"role": "assistant", "content": answer})
