# chatbot.py
import streamlit as st
import os
from dotenv import load_dotenv

# Optional: OpenAI for smart fallback answers
try:
    import openai
except ImportError:
    openai = None

# Load environment variables (for OpenAI API key)
load_dotenv()
OPENAI_KEY = os.getenv("OPENAI_API_KEY")

# This dictionary contains common FAQs about Iron Lady programs
faq = {
    "programs": "Iron Lady offers leadership programs focused on women empowerment, communication, confidence building, and professional growth. Typical tracks include Leadership 101, Career Acceleration, Public Speaking for Leaders, and Mentorship Circles.",
    "duration": "Program durations vary: most curated leadership tracks run 8–12 weeks. Short workshops and masterclasses run 1–3 days.",
    "mode": "Programs are primarily online for flexibility, with occasional offline workshops and city meetups.",
    "certificates": "Yes — participants receive a verified certificate after successful completion of the program requirements.",
    "mentors": "Mentors and coaches are experienced industry leaders, certified leadership coaches, and Iron Lady alumni who guide participants."
}

# Map keywords in user input to FAQ keys
keyword_map = {
    "what programs": "programs",
    "programs does": "programs",
    "which programs": "programs",
    "program duration": "duration",
    "how long": "duration",
    "duration": "duration",
    "online or offline": "mode",
    "is the program online": "mode",
    "is it online": "mode",
    "certificate": "certificates",
    "certificates": "certificates",
    "who are the mentors": "mentors",
    "who are the coaches": "mentors",
    "mentors": "mentors",
    "coaches": "mentors"
}

#Functions 
def rule_based_answer(user_input: str):
    """
    Check if the user's question matches our predefined FAQ.
    Returns the answer if found, otherwise None.
    """
    user_input = user_input.lower()
    for key, faq_key in keyword_map.items():
        if key in user_input:
            return faq[faq_key]
    # fallback: check direct FAQ keys
    for key, answer in faq.items():
        if key in user_input:
            return answer
    return None

def ai_fallback(user_input: str):
    """
    Optional OpenAI fallback for questions not in FAQ.
    Requires OPENAI_KEY and openai installed.
    """
    if not (OPENAI_KEY and openai):
        return None
    try:
        openai.api_key = OPENAI_KEY
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are the Iron Lady assistant. Be concise and friendly."},
                {"role": "user", "content": user_input}
            ],
            temperature=0.5,
            max_tokens=200
        )
        return response["choices"][0]["message"]["content"].strip()
    except Exception as e:
        print("OpenAI error:", e)
        return None

#  Streamlit UI 
st.set_page_config(page_title="Iron Lady Chatbot", page_icon="🤖", layout="centered")

st.title("🤖 Iron Lady — FAQ Chatbot")
st.markdown("Ask me about **programs, duration, mode, certificates, or mentors**.")

# Initialize chat history in session state
if "messages" not in st.session_state:
    st.session_state["messages"] = [
        {"role": "bot", "content": "Hi! I'm your Iron Lady assistant. How can I help you today?"}
    ]

# Display chat messages
for msg in st.session_state.messages:
    if msg["role"] == "user":
        st.chat_message("user").markdown(msg["content"])
    else:
        st.chat_message("assistant").markdown(msg["content"])

# Chat input box
if prompt := st.chat_input("Type your question here..."):
    # Add user message to history
    st.session_state.messages.append({"role": "user", "content": prompt})
    st.chat_message("user").markdown(prompt)

    # Get bot reply
    answer = rule_based_answer(prompt)
    if not answer:
        answer = ai_fallback(prompt)
    if not answer:
        answer = "Sorry, I don’t have that info. Please contact Iron Lady support."

    # Add bot message to history and display it
    st.session_state.messages.append({"role": "bot", "content": answer})
    st.chat_message("assistant").markdown(answer)
