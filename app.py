import streamlit as st
import re

# Initialize session state
if "messages" not in st.session_state:
    st.session_state.messages = []
if "awaiting_medicine_choice" not in st.session_state:
    st.session_state.awaiting_medicine_choice = False
if "awaiting_age_for_vaccine" not in st.session_state:
    st.session_state.awaiting_age_for_vaccine = False

# Medicine options
medicine_options = {
    "1mg": {"price": "₹50", "delivery": "2 days", "url": "https://www.1mg.com/"},
    "netmeds": {"price": "₹45", "delivery": "3 days", "url": "https://www.netmeds.com/"},
    "pharmeasy": {"price": "₹55", "delivery": "1 day", "url": "https://pharmeasy.in/"},
}

# Outbreak alerts
outbreak_alerts = [
    "⚠ Dengue cases rising in Delhi NCR. Use mosquito repellents & keep surroundings clean.",
    "⚠ Seasonal flu spreading in Mumbai. Wear masks & wash hands frequently.",
]

# Vaccination schedule
vaccination_schedule = {
    "child": ["BCG", "Polio", "Hepatitis B", "MMR"],
    "adult": ["Tetanus booster (every 10 years)", "Flu shot (annual)", "COVID-19 booster"],
    "elderly": ["Pneumococcal vaccine", "Shingles vaccine"],
}

# Preventive tips
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

    # --- Vaccine Age Handling ---
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

    # --- Medicine Choice ---
    if st.session_state.awaiting_medicine_choice:
        for site in medicine_options:
            if site in user_input:
                st.session_state.awaiting_medicine_choice = False
                url = medicine_options[site]["url"]
                return f"💊 Click here to order from [{site.capitalize()}]({url})"
        return "Please choose one of the options: 1mg, NetMeds, or PharmEasy."

    # --- Greetings ---
    if any(word in user_input for word in ["hi", "hello", "hey", "namaste", "namaskar", "salaam"]):
        return "नमस्ते! 👋 Hello! I can talk in Hindi & English. How can I help you today?"

    # --- Thanks ---
    if any(word in user_input for word in ["thanks", "thank you", "dhanyavad", "shukriya"]):
        return "You're welcome! 😊 Glad I could help."

    # --- Fever ---
    if "fever" in user_input or "bukhar" in user_input:
        return "It seems like you may have a fever 🤒. Stay hydrated and rest well.\nFor emergencies, consult a doctor immediately."

    # --- Cough ---
    if "cough" in user_input or "khansi" in user_input:
        return "Cough detected. Drink warm fluids, honey + ginger tea may help.\nIf it persists >1 week, see a doctor."

    # --- Home remedies ---
    if "home remedy" in user_input or "home" in user_input:
        return "✅ Home Remedy:\n- Fever: Tulsi + ginger kadha\n- Cough: Honey with warm water\n- Cold: Steam inhalation with ajwain"

    # --- Ayurveda ---
    if "ayurveda" in user_input:
        return "🌿 Ayurveda Tips:\n- Fever: Giloy juice\n- Indigestion: Triphala powder\n- Immunity: Chyawanprash daily"

    # --- Homeopathy ---
    if "homeopathy" in user_input:
        return "⚪ Homeopathy:\n- Fever: Belladonna 30\n- Cough: Drosera 30\n- Cold: Arsenicum Album 30\n(Consult a doctor first!)"

    # --- Doctor booking ---
    if "doctor" in user_input or "consult" in user_input:
        return "👨‍⚕ Book a doctor here: [Practo](https://www.practo.com/)"

    # --- Medicine availability ---
    if "medicine" in user_input or "tablet" in user_input or "drug" in user_input:
        st.session_state.awaiting_medicine_choice = True
        comparison = "💊 Medicine comparison:\n"
        for site, info in medicine_options.items():
            comparison += f"- {site.capitalize()}: {info['price']} | Delivery: {info['delivery']}\n"
        comparison += "\nPlease type which one you prefer (1mg / NetMeds / PharmEasy)."
        return comparison

    # --- Outbreak Alerts ---
    if "outbreak" in user_input or "alert" in user_input or "disease" in user_input:
        return "📢 Health Alerts:\n" + "\n".join(outbreak_alerts)

    # --- Vaccination reminders ---
    if "vaccine" in user_input or "vaccination" in user_input or "reminder" in user_input:
        st.session_state.awaiting_age_for_vaccine = True
        return "💉 Please tell me your age for vaccination reminders."

    # --- Preventive Healthcare ---
    if "prevent" in user_input or "healthy" in user_input or "tips" in user_input:
        return "🛡 Preventive Healthcare:\n" + "\n".join(preventive_tips)

    # --- First Aid ---
    for condition, tip in first_aid_tips.items():
        if condition in user_input:
            return f"⛑ First Aid: {tip}"

    if "first aid" in user_input:
        tips_list = "\n".join([f"- {k.capitalize()}: {v}" for k, v in first_aid_tips.items()])
        return f"⛑ First Aid Guide:\n{tips_list}"

    # --- Default ---
    return ("I can assist with:\n"
            "- Symptoms (fever, cough, etc.)\n"
            "- Remedies (Home, Ayurveda, Homeopathy)\n"
            "- Doctor consultation\n"
            "- Medicine ordering & comparison\n"
            "- Outbreak alerts\n"
            "- Vaccination reminders\n"
            "- Preventive healthcare tips\n"
            "- First aid guidance")


# --- UI ---
st.title("Healthcare Chatbot 🤖")

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

if user_input := st.chat_input("Type your message..."):
    # Display user msg
    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.markdown(user_input)

    # Get bot response
    bot_response = get_bot_response(user_input)
    st.session_state.messages.append({"role": "assistant", "content": bot_response})
    with st.chat_message("assistant"):
        st.markdown(bot_response)




