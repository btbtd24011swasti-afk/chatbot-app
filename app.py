import streamlit as st
import re

# Initialize chat history
if "chat_history" not in st.session_state:
    # Each entry: {"role": "user"/"assistant", "content": "..."}
    st.session_state.chat_history = []

# --- Core chatbot logic (edit as needed) ---
def get_bot_response(user_input: str) -> str:
    ui = user_input.lower().strip()
    if "fever" in ui:
        return "🤒 It seems you may have a fever. Stay hydrated and rest. If high fever or danger signs, consult a doctor."
    if "vaccin" in ui or "vaccine" in ui:
        return "💉 Please tell me your age so I can suggest the right vaccination reminders."
    if "thanks" in ui or "thank you" in ui:
        return "You're welcome! 😊"
    if "hi" in ui or "hello" in ui:
        return "नमस्ते! 👋 Hello! I can talk in Hindi & English. How can I help you today?"
    return "I can help with: symptoms (fever, cough), remedies, medicine info, vaccination reminders, and more!"

# --- Optional: CSS for chat look ---
st.markdown("""
    <style>
    .stChatMessage {max-width: 60% !important;}
    .st-emotion-cache-1h9usn6 {padding-bottom: 44px !important;}
    </style>
""", unsafe_allow_html=True)

# --- Render chat history SMS-style ---
st.title("💬 Healthcare Chatbot (SMS Style)")
for msg in st.session_state.chat_history:
    with st.chat_message(msg["role"]):
        st.write(msg["content"])

# --- Input stays at the bottom ---
user_text = st.chat_input("Type a message... (e.g., fever, medicine, vaccine)")
if user_text:
    # Add user message
    st.session_state.chat_history.append({"role": "user", "content": user_text})
    with st.chat_message("user"):
        st.write(user_text)
    # Generate bot reply
    reply = get_bot_response(user_text)
    st.session_state.chat_history.append({"role": "assistant", "content": reply})
    with st.chat_message("assistant"):
        st.write(reply)



















