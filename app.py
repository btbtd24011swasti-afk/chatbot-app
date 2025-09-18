import streamlit as st
import webbrowser
import re

# --- Global states ---
if "awaiting_age_for_vaccine" not in st.session_state:
    st.session_state.awaiting_age_for_vaccine = False

# Medicine options
medicine_options = {
    "1mg": {"price": "₹32.9", "delivery": "by today", "url": "https://www.1mg.com/drugs/dolo-650-tablet-74467/"},
    "NetMeds": {"price": "₹30.84", "delivery": "1 day", "url": "https://www.netmeds.com/product/dolo-650-tablet-15s-lui1wb-8231049/"},
    "PharmEasy": {"price": "₹25.02", "delivery": "1 day", "url": "https://pharmeasy.in/online-medicine-order/dolo-650mg-strip-of-15-tablets-44140/"},
}

# Mock outbreak alerts
outbreak_alerts = [
    "⚠ Dengue cases rising in Delhi NCR. Use mosquito repellents & keep surroundings clean.",
    "⚠ Seasonal flu spreading in Mumbai. Wear masks & wash hands frequently.",
]

# Vaccination schedule sample
vaccination_schedule = {
    "child": ["BCG", "Polio", "Hepatitis B", "MMR"],
    "adult": ["Tetanus booster (every 10 years)", "Flu shot (annual)", "COVID-19 booster"],
    "elderly": ["Pneumococcal vaccine", "Shingles vaccine"],
}

# Preventive healthcare tips
preventive_tips = [
    "🟢 Wash hands regularly with soap.",
    "🟢 Exercise 30 mins daily.",
    "🟢 Eat balanced diet (fruits & veggies).",
    "🟢 Get 7-8 hours of sleep.",
]

# First Aid dictionary
first_aid_tips = {
    "burn": "🔥 Burn: Cool with running water for 20 minutes. Do NOT apply ice.",
    "cut": "🩸 Cut: Wash with clean water, apply antiseptic, cover with bandage.",
    "bleeding": "🩸 Bleeding: Wash with clean water, apply antiseptic, cover with bandage.",
    "faint": "😵 Fainting: Lay person flat, raise legs slightly, loosen tight clothing.",
    "fracture": "🦴 Fracture: Keep limb still, support with splint, seek medical help.",
}

# --- Chatbot logic ---
def get_bot_response(user_input):
    user_input = user_input.lower().strip()

    # --- Vaccine age ---
    if st.session_state.awaiting_age_for_vaccine:
        try:
            age = int(re.findall(r'\d+', user_input)[0])
            st.session_state.awaiting_age_for_vaccine = False
            if age < 18:
                return "💉 Vaccination Reminders for Children:\n" + ", ".join(vaccination_schedule["child"])
            elif 18 <= age < 60:
                return "💉 Vaccination Reminders for Adults:\n" + ", ".join(vaccination_schedule["adult"])
            else:
                return "💉 Vaccination Reminders for Elderly:\n" + ", ".join(vaccination_schedule["elderly"])
        except:
            return "❓ Please enter a valid age (e.g., 25)."

    # --- Greetings ---
    if any(word in user_input for word in ["hi", "hello", "hey", "namaste", "namaskar", "salaam"]):
        return "नमस्ते! 👋 Hello! I can talk in Hindi & English. How can I help you today?"

    # --- Thanks ---
    if any(word in user_input for word in ["thanks", "thank you", "dhanyavad", "shukriya"]):
        return "You're welcome! 😊 Glad I could help."

    # --- Symptoms ---
    if "fever" in user_input or "bukhar" in user_input:
        return "It seems like you may have a fever 🤒. Stay hydrated and rest well.\nFor emergencies, consult a doctor immediately."
    if "cough" in user_input or "khansi" in user_input or "khasi" in user_input:
        return "Cough detected. Drink warm fluids, honey + ginger tea may help.\nIf it persists >1 week, see a doctor."

    # --- Remedies ---
    if "home remedy" in user_input or "home remedies" in user_input:
        return "✅ Home Remedy Suggestion:\n- Fever: Drink tulsi + ginger kadha.\n- Cough: Honey with warm water.\n- Cold: Steam inhalation with ajwain seeds."
    if "ayurveda" in user_input or "ayurvedic" in user_input:
        return "🌿 Ayurvedic Tip:\n- Fever: Giloy juice.\n- Indigestion: Triphala powder with warm water.\n- Immunity: Chyawanprash daily."
    if "homeopathy" in user_input or "homoeopathic" in user_input:
        return "⚪ Homeopathic Suggestion:\n- Fever: Belladonna 30.\n- Cough: Drosera 30.\n- Cold: Arsenicum Album 30.\n(Use only with doctor’s guidance)."

    # --- Doctor consultation ---
    if any(word in user_input for word in ["doctor", "consult"]):
        webbrowser.open("https://www.practo.com/")
        return "👨‍⚕ Redirecting you to Practo for doctor consultation."

    # --- Medicine info (use buttons) ---
    if any(word in user_input for word in ["medicine", "tablet", "drug"]):
        return "💊 Click a button below to visit the pharmacy website:"

    # --- Outbreak alerts ---
    if any(word in user_input for word in ["outbreak", "alert", "disease"]):
        return "📢 Current Health Alerts:\n" + "\n".join(outbreak_alerts)

    # --- Vaccination reminders ---
    if any(word in user_input for word in ["vaccine", "vaccination", "reminder"]):
        st.session_state.awaiting_age_for_vaccine = True
        return "💉 Please tell me your age so I can suggest the right vaccination reminders."

    # --- Preventive healthcare ---
    if any(word in user_input for word in ["prevent", "healthy", "tips"]):
        return "🛡 Preventive Healthcare Tips:\n" + "\n".join(preventive_tips)

    # --- First aid ---
    for condition, tip in first_aid_tips.items():
        if condition in user_input:
            return f"⛑ First Aid Suggestion:\n{tip}"
    if "first aid" in user_input:
        tips_list = "\n".join([f"- {k.capitalize()}: {v}" for k, v in first_aid_tips.items()])
        return f"⛑ First Aid Guide:\n{tips_list}"

    return ("I can assist with:\n- Symptoms (fever, cough, etc.)\n- Remedies (Home, Ayurveda, Homeopathy)\n"
            "- Doctor consultation\n- Medicine ordering & comparison\n- Outbreak alerts\n- Vaccination reminders\n"
            "- Preventive healthcare tips\n- First aid guidance")

# --- Streamlit UI ---
st.set_page_config(page_title="Healthcare Chatbot 🤖", layout="wide")
st.title("Healthcare Chatbot 🤖")
st.markdown("Hello! I am your Healthcare Assistant. Ask me anything about symptoms, remedies, vaccines, or medicines.")

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# User input
user_input = st.text_input("You:", "")

if st.button("Send") or user_input:
    if user_input:
        st.session_state.chat_history.append(("You", user_input))
        bot_response = get_bot_response(user_input)
        st.session_state.chat_history.append(("Bot", bot_response))

# Display chat history
for sender, message in st.session_state.chat_history:
    if sender == "You":
        st.markdown(f"**{sender}:** {message}")
    else:
        st.markdown(f"<span style='color:green'>{sender}: {message}</span>", unsafe_allow_html=True)

# --- Medicine buttons ---
if st.session_state.chat_history and "💊 Click a button" in st.session_state.chat_history[-1][1]:
    st.markdown("**Select a pharmacy:**")
    cols = st.columns(len(medicine_options))
    for i, (site, info) in enumerate(medicine_options.items()):
        if cols[i].button(site):
            webbrowser.open(info["url"])
            st.session_state.chat_history.append(("Bot", f"💊 Redirecting you to {site} for order placement."))















