import streamlit as st
from datetime import datetime
import random

# Dummy database of intents
intents = {
    "symptoms": {
        "keywords": ["fever", "cough", "headache", "cold", "sore throat", "बुखार", "खांसी", "सरदर्द"],
        "responses": [
            "It could be a mild flu or infection. Drink plenty of water and rest.",
            "Sometimes these symptoms indicate dehydration or viral fever. Stay hydrated!",
            "If symptoms persist, it’s best to consult a doctor."
        ]
    },
    "greeting": {
        "keywords": ["hello", "hi", "hey", "नमस्ते"],
        "responses": [
            "Hello! How can I assist you today?",
            "Hi there! Tell me your symptoms, and I’ll try to guide you.",
            "Hey! What health issue are you facing?"
        ]
    },
    "goodbye": {
        "keywords": ["bye", "thank you", "thanks", "goodbye"],
        "responses": [
            "Take care! Wishing you good health.",
            "Goodbye! Stay safe and healthy.",
            "Thanks for chatting. Hope you feel better soon!"
        ]
    }
}

# Function to get chatbot response
def chatbot_response(user_input):
    user_input = user_input.lower()
    for intent, data in intents.items():
        if any(keyword in user_input for keyword in data["keywords"]):
            return random.choice(data["responses"])
    return "I'm not sure about that. Please consult a medical professional."

# --- Streamlit UI ---
st.set_page_config(page_title="Healthcare Chatbot", page_icon="🤖")

st.title("🤖 Healthcare Chatbot")
st.write("I can answer simple health-related queries. (For serious conditions, please consult a doctor!)")

# Chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display previous messages
for msg in st.session_state.messages:
    if msg["role"] == "user":
        st.chat_message("user").markdown(msg["content"])
    else:
        st.chat_message("assistant").markdown(msg["content"])

# User input
if prompt := st.chat_input("Type your message..."):
    # Save user message
    st.session_state.messages.append({"role": "user", "content": prompt})
    st.chat_message("user").markdown(prompt)

    # Generate bot response
    response = chatbot_response(prompt)
    st.session_state.messages.append({"role": "assistant", "content": response})
    st.chat_message("assistant").markdown(response)


