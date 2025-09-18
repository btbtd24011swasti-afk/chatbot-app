import streamlit as st

# --- Chatbot Logic ---
def chatbot_response(user_input):
    user_input = user_input.lower()

    if "hello" in user_input or "hi" in user_input:
        return ("Hello! How can I help you today?",
                ["Check symptoms", "Get general health tips", "Talk to a doctor"])
    
    elif "symptom" in user_input:
        return ("Sure! Please describe your symptoms (e.g., fever, cough, headache).",
                ["Fever", "Cough", "Headache"])
    
    elif "fever" in user_input:
        return ("Fever may be caused by infections like cold or flu. Drink water and rest. "
                "If it persists, consult a doctor.",
                ["General health tips", "Talk to a doctor", "Vaccination reminders"])
    
    elif "tip" in user_input or "health" in user_input:
        return ("Health Tip: Maintain a balanced diet, stay hydrated, and sleep at least 7 hours daily.",
                ["Check symptoms", "Talk to a doctor", "Get vaccination reminders"])
    
    elif "doctor" in user_input:
        return ("I can connect you to a human doctor (if available). Meanwhile, you can follow some basic health tips.",
                ["General health tips", "Check symptoms", "Medicine information"])
    
    else:
        return ("Sorry, I didn't understand that.", 
                ["Try 'Check symptoms'", "Ask for health tips", "Talk to a doctor"])


# --- Streamlit UI ---
st.title("💊 Healthcare Chatbot")

# Store conversation history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Chat display
for msg in st.session_state.messages:
    role, text = msg
    if role == "user":
        st.markdown(f"**🧑 You:** {text}")
    else:
        st.markdown(f"**🤖 Bot:** {text}")

# Input box
user_input = st.text_input("Type your message:")

if user_input:
    # Add user message
    st.session_state.messages.append(("user", user_input))

    # Get bot response
    response, suggestions = chatbot_response(user_input)
    st.session_state.messages.append(("bot", response))

    # Show suggestions
    st.markdown("👉 **Suggestions:**")
    for s in suggestions:
        st.write(f"- {s}")

    # Clear input box for next round
    st.experimental_rerun()
