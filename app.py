import streamlit as st
from dotenv import load_dotenv
import os

from openai_chatbot import get_openai_response
from gemini_fallback import get_gemini_response
from human_handoff import connect_to_human

# ------------------------
# Load ENV
load_dotenv()

st.title("💹 Medatiq Markets Chatbot")

# ------------------------
# Session memory
if "messages" not in st.session_state:
    st.session_state.messages = []

# ------------------------
# Display chat
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# ------------------------
# Sidebar (Human option ALWAYS visible)
st.sidebar.title("Support")

if st.sidebar.button("👩‍💼 Talk to Human"):
    reply = connect_to_human()
    st.session_state.messages.append({
        "role": "assistant",
        "content": reply
    })
    st.rerun()

# ------------------------
# User input
user_input = st.chat_input("Ask about Forex or Crypto...")

if user_input:
    # Save user message
    st.session_state.messages.append({
        "role": "user",
        "content": user_input
    })

    with st.chat_message("user"):
        st.markdown(user_input)

    # ------------------------
    # 1. TRY OPENAI (PRIMARY)
    bot_reply = get_openai_response(user_input)

    # ------------------------
    # 2. CHECK FOR FALLBACK TRIGGER
    if bot_reply == "FALLBACK_TRIGGER":
        st.warning("⚠️ Primary AI unavailable. Switching to backup...")

        try:
            bot_reply = get_gemini_response(user_input)
        except Exception:
            bot_reply = "❌ Both AI services are currently unavailable. Please try again later."

    # ------------------------
    # Save + show reply
    st.session_state.messages.append({
        "role": "assistant",
        "content": bot_reply
    })

    with st.chat_message("assistant"):
        st.markdown(bot_reply)