import streamlit as st
from chatbot.chatbot_engine import get_response

st.title("🤖 Personal Assistant Chatbot")
st.markdown("Ask me anything: weather, tasks, wiki, math, or just chat!")

if "history" not in st.session_state:
    st.session_state.history = []

user_input = st.text_input("You:", "")

if user_input:
    bot_response = get_response(user_input)
    st.session_state.history.append(("You", user_input))
    st.session_state.history.append(("Bot", bot_response))

for role, msg in st.session_state.history:
    if role == "You":
        st.markdown(f"**🧑 You:** {msg}")
    else:
        st.markdown(f"**🤖 Bot:** {msg}")
