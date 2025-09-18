import streamlit as st
import re

# --- Page Config ---
st.set_page_config(page_title="HelloDoc", page_icon="💊")
st.title("HelloDoc 💊")
st.write("Your personal healthcare assistant (English + Hindi)")

# --- Initialize session state ---
if "messages" not in st.session_state:
    st.session_state.messages = []

if "awaiting_service_choice" not in st.session_state:
    st.session_state.awaiting_service_choice = False


# --- Helper: Menu ---
def get_menu():
    return (
        "1️⃣ Symptoms (fever, cough, etc.)\n"
        "2️⃣ Remedies (Home, Ayurveda, Homeopathy)\n"
        "3️⃣ Doctor Consultation\n"
        "4️⃣ Medicine Ordering & Price Comparison\n"
        "5️⃣ Outbreak Alerts\n"
        "6️⃣ Vaccination Reminders\n"
        "7️⃣ Preventive Healthcare Tips\n"
        "8️⃣ First Aid Guidance\n"
    )


# --- Chatbot Logic ---
def get_bot_response(user_input):
    user_input = user_input.lower().strip()

    # Garbage filter (nonsense or empty)
    if not re.search(r"[a-zA-Z0-9]", user_input) or len(user_input) < 2:
        return "⚠️ That doesn’t look like a valid query. Please type **hi** to see the menu."

    # --- Service selection ---
    if st.session_state.awaiting_service_choice:
        st.session_state.awaiting_service_choice = False
        if user_input in ["1", "symptom", "symptoms"]:
            return "🤒 Please tell me your symptom (e.g., fever, cough)."
        elif user_input in ["2", "remedy", "remedies"]:
            return "✅ Home Remedies:\n- Fever: Tulsi + ginger kadha\n- Cough: Honey + warm water\n- Cold: Steam inhalation"
        elif user_input in ["3", "doctor", "consult"]:
            return "👨‍⚕️ Opening Practo for doctor consultation: [Practo](https://www.practo.com/)"
        elif user_input in ["4", "medicine", "tablet", "drug"]:
            return "💊 Medicine Price Comparison:\n- 1mg: ₹50 (2 days)\n- Netmeds: ₹45 (3 days)\n- PharmEasy: ₹55 (1 day)"
        elif user_input in ["5", "alert", "outbreak", "disease"]:
            return "📢 Current Health Alerts:\n- Dengue cases rising in Delhi NCR\n- Seasonal flu in Mumbai"
        elif user_input in ["6", "vaccine", "vaccination"]:
            return "💉 Please tell me your age to get vaccination reminders."
        elif user_input in ["7", "prevent", "tips", "healthy"]:
            return "🛡 Preventive Tips:\n- Wash hands\n- Exercise daily\n- Eat healthy\n- Sleep 7-8 hrs"
        elif user_input in ["8", "first aid"]:
            return "⛑ First Aid Guide:\n- Burn: Cool with water\n- Cut: Clean & bandage\n- Faint: Lay flat & raise legs"
        else:
            return "❓ Invalid choice. Please type a number (1–8)."

    # --- Greeting triggers ---
    if any(word in user_input for word in ["hi", "hello", "hey", "namaste"]):
        st.session_state.awaiting_service_choice = True
        return "👋 I am HelloDoc. Here are my services:\n" + get_menu()

    # --- Fallback ---
    return "❓ I didn't understand. Type **hi** to see the menu again.\n\n" + get_menu()


# --- UI (Chat) ---
# Display chat history
for sender, msg in st.session_state.messages:
    if sender == "user":
        st.markdown(f"**You:** {msg}")
    else:
        st.markdown(f"**🤖 HelloDoc:** {msg}")

# Input box
user_input = st.text_input("Type your message here:", key="input")

if user_input:
    st.session_state.messages.append(("user", user_input))
    bot_response = get_bot_response(user_input)
    st.session_state.messages.append(("bot", bot_response))
    st.experimental_rerun()






