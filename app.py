# app.py
import streamlit as st
import re

# -----------------------
# Initialization
# -----------------------
st.set_page_config(page_title="Healthcare Chatbot (SMS Style)", layout="centered")

if "chat_history" not in st.session_state:
    # chat_history: list of tuples (sender, message, optional_html_flag)
    st.session_state.chat_history = []
if "awaiting_medicine_choice" not in st.session_state:
    st.session_state.awaiting_medicine_choice = False
if "awaiting_age_for_vaccine" not in st.session_state:
    st.session_state.awaiting_age_for_vaccine = False
if "show_medicine_buttons" not in st.session_state:
    st.session_state.show_medicine_buttons = False

# -----------------------
# Data
# -----------------------
medicine_options = {
    "1mg": {"price": "₹32.9", "delivery": "by today", "url": "https://www.1mg.com/drugs/dolo-650-tablet-74467/"},
    "NetMeds": {"price": "₹30.84", "delivery": "1 day", "url": "https://www.netmeds.com/product/dolo-650-tablet-15s-lui1wb-8231049/"},
    "PharmEasy": {"price": "₹25.02", "delivery": "1 day", "url": "https://pharmeasy.in/online-medicine-order/dolo-650mg-strip-of-15-tablets-44140/"},
}

outbreak_alerts = [
    "⚠ Dengue cases rising in Delhi NCR. Use mosquito repellents & keep surroundings clean.",
    "⚠ Seasonal flu spreading in Mumbai. Wear masks & wash hands frequently.",
]

vaccination_schedule = {
    "child": ["BCG", "Polio", "Hepatitis B", "MMR"],
    "adult": ["Tetanus booster (every 10 years)", "Flu shot (annual)", "COVID-19 booster"],
    "elderly": ["Pneumococcal vaccine", "Shingles vaccine"],
}

preventive_tips = [
    "🟢 Wash hands regularly with soap.",
    "🟢 Exercise 30 mins daily.",
    "🟢 Eat balanced diet (fruits & veggies).",
    "🟢 Get 7-8 hours of sleep.",
]

first_aid_tips = {
    "burn": "🔥 Burn: Cool with running water for 20 minutes. Do NOT apply ice.",
    "cut": "🩸 Cut: Wash with clean water, apply antiseptic, cover with bandage.",
    "bleeding": "🩸 Bleeding: Apply firm pressure with clean cloth, seek help if heavy.",
    "faint": "😵 Fainting: Lay person flat, raise legs slightly, loosen tight clothing.",
    "fracture": "🦴 Fracture: Keep limb still, support with splint, seek medical help.",
}

# -----------------------
# Helper: chatbot logic
# -----------------------
def get_bot_response(user_input: str) -> str:
    ui = user_input.lower().strip()

    # If waiting for age for vaccine
    if st.session_state.awaiting_age_for_vaccine:
        try:
            age = int(re.findall(r"\d+", ui)[0])
            st.session_state.awaiting_age_for_vaccine = False
            if age < 18:
                return "💉 Vaccination Reminders for Children: " + ", ".join(vaccination_schedule["child"])
            elif 18 <= age < 60:
                return "💉 Vaccination Reminders for Adults: " + ", ".join(vaccination_schedule["adult"])
            else:
                return "💉 Vaccination Reminders for Elderly: " + ", ".join(vaccination_schedule["elderly"])
        except Exception:
            return "❓ Please enter a valid age (e.g., 25)."

    # If waiting for medicine selection
    if st.session_state.awaiting_medicine_choice:
        # Accept either name typed or selection triggered by buttons (buttons handled elsewhere)
        for key in medicine_options:
            if key.lower() in ui:
                med = medicine_options[key]
                st.session_state.awaiting_medicine_choice = False
                st.session_state.show_medicine_buttons = False
                return f"💊 {key} — Price: {med['price']} | Delivery: {med['delivery']}\nOpen here: {med['url']}"
        # If not matched, prompt valid options
        return "Please choose a valid option: 1mg, NetMeds, or PharmEasy."

    # Greetings
    if any(word in ui for word in ["hi", "hello", "hey", "namaste", "namaskar", "salaam"]):
        return "नमस्ते! 👋 Hello! I can talk in Hindi & English. How can I help you today?"

    # Thanks
    if any(word in ui for word in ["thanks", "thank you", "dhanyavad", "shukriya"]):
        return "You're welcome! 😊 Glad I could help."

    # Symptoms
    if any(word in ui for word in ["fever", "bukhar"]):
        return "🤒 It seems you may have a fever. Stay hydrated and rest. If high fever or danger signs, consult a doctor."
    if any(word in ui for word in ["cough", "khansi", "khasi"]):
        return "🤧 For cough: warm fluids, honey + ginger tea may help. If persists >1 week, consult a doctor."

    # Remedies
    if "home remedy" in ui or "home remedies" in ui:
        return ("✅ Home Remedy Suggestions:\n"
                "- Fever: Tulsi + ginger kadha.\n"
                "- Cough: Honey with warm water.\n"
                "- Cold: Steam inhalation with ajwain seeds.")
    if "ayurveda" in ui or "ayurvedic" in ui:
        return ("🌿 Ayurvedic Tips:\n"
                "- Fever: Giloy juice.\n- Indigestion: Triphala powder with warm water.\n- Immunity: Chyawanprash daily.")
    if "homeopathy" in ui or "homoeopathic" in ui:
        return ("⚪ Homeopathic Suggestions:\n"
                "- Fever: Belladonna 30.\n- Cough: Drosera 30.\n- Cold: Arsenicum Album 30.\n(Use only with doctor’s guidance).")

    # Doctor consultation
    if any(word in ui for word in ["doctor", "consult", "practo"]):
        # Provide link so client can click (opening links server-side is unreliable)
        return "👨‍⚕ Need a doctor? Visit Practo: https://www.practo.com/"

    # Medicine enquiry -> show buttons
    if any(word in ui for word in ["medicine", "tablet", "drug", "dolo"]):
        st.session_state.awaiting_medicine_choice = True
        st.session_state.show_medicine_buttons = True
        comparison_text = "💊 Medicine availability & price comparison:\n"
        for site, info in medicine_options.items():
            comparison_text += f"- {site}: {info['price']} | Delivery: {info['delivery']}\n"
        comparison_text += "\nPlease pick one of the buttons below or type the name (1mg / NetMeds / PharmEasy)."
        return comparison_text

    # Outbreak alerts
    if any(word in ui for word in ["outbreak", "alert", "disease"]):
        return "📢 Current Health Alerts:\n" + "\n".join(outbreak_alerts)

    # Vaccination reminders
    if any(word in ui for word in ["vaccine", "vaccination", "reminder"]):
        st.session_state.awaiting_age_for_vaccine = True
        return "💉 Please tell me your age so I can suggest the right vaccination reminders."

    # Preventive tips
    if any(word in ui for word in ["prevent", "healthy", "tips"]):
        return "🛡 Preventive Healthcare Tips:\n" + "\n".join(preventive_tips)

    # First aid
    for condition, tip in first_aid_tips.items():
        if condition in ui:
            return f"⛑ First Aid Suggestion:\n{tip}"
    if "first aid" in ui:
        tips_list = "\n".join([f"- {k.capitalize()}: {v}" for k, v in first_aid_tips.items()])
        return f"⛑ First Aid Guide:\n{tips_list}"

    # Default
    return ("I can help with:\n"
            "- Symptoms (fever, cough)\n- Remedies (Home, Ayurveda, Homeopathy)\n"
            "- Doctor consultation\n- Medicine info & comparison\n- Outbreak alerts\n- Vaccination reminders\n- Preventive tips\n- First aid")

# -----------------------
# CSS: SMS-style bubbles
# -----------------------
st.markdown(
    """
    <style>
    .chat-wrapper { max-width:760px; margin:0 auto; }
    .chat-bubble { max-width: 78%; padding: 10px 14px; border-radius: 18px; margin: 6px 2px; font-size: 15px; line-height:1.4; }
    .user { background: #DCF8C6; color: #000; margin-left: auto; border-bottom-right-radius: 4px; text-align: right; }
    .bot { background: #F1F0F0; color: #000; margin-right: auto; border-bottom-left-radius: 4px; text-align: left; }
    .meta { font-size:12px; color: #666; margin-top:4px; }
    .pharm-btn { display:inline-block; padding:8px 12px; border-radius:8px; background:#e7eefc; margin-right:8px; text-decoration:none; color:#073b7a; border:1px solid #cfe0ff; }
    </style>
    """,
    unsafe_allow_html=True,
)

st.title("💬 Healthcare Chatbot — SMS Style")
st.write("Ask about symptoms, medicines, vaccines, or first aid. (Press Enter or click Send)")

# -----------------------
# Render chat history
# -----------------------
st.markdown("<div class='chat-wrapper'>", unsafe_allow_html=True)
for sender, message in st.session_state.chat_history:
    if sender == "user":
        st.markdown(f"<div class='chat-bubble user'>{st.session_state.get('username','You')}: {st.markdown if False else ''}{message}</div>", unsafe_allow_html=True)
    else:
        # bot messages may contain URLs; show as plain text which will render link automatically
        # make URLs clickable:
        safe_msg = re.sub(r"(https?://\S+)", r"<a href='\1' target='_blank'>\1</a>", message)
        st.markdown(f"<div class='chat-bubble bot'>{safe_msg}</div>", unsafe_allow_html=True)

st.markdown("</div>", unsafe_allow_html=True)

# -----------------------
# Medicine buttons area (shows only when relevant)
# -----------------------
if st.session_state.show_medicine_buttons:
    st.markdown("**Select a pharmacy (click the link to open in a new tab):**")
    cols = st.columns(len(medicine_options))
    for i, (site, info) in enumerate(medicine_options.items()):
        # show as a link styled like a button
        cols[i].markdown(f"<a class='pharm-btn' href='{info['url']}' target='_blank'>{site} — {info['price']}</a>", unsafe_allow_html=True)
    st.markdown("---")

# -----------------------
# Input form (Enter to submit)
# -----------------------
with st.form(key="chat_form", clear_on_submit=True):
    user_text = st.text_input("", placeholder="Type a message... (e.g., fever, medicine, vaccine)", key="user_input")
    submitted = st.form_submit_button("Send")
    if submitted and user_text:
        # append user message
        st.session_state.chat_history.append(("user", user_text))
        # get bot response
        bot_reply = get_bot_response(user_text)
        st.session_state.chat_history.append(("bot", bot_reply))
        # If medicine buttons were shown earlier, keep them visible until user picks or types
        # (show_medicine_buttons is toggled inside get_bot_response)
        # Rerun to refresh UI
        st.experimental_rerun()

















