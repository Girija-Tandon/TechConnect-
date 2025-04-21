import streamlit as st
import google.generativeai as genai
import os
import pyttsx3
import speech_recognition as sr
from dotenv import load_dotenv
import threading

# Load environment variables
load_dotenv()

# Configure Gemini API
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

# Initialize TTS engine
engine = pyttsx3.init()
engine.setProperty('rate', 170)
engine_lock = threading.Lock()
is_speaking_allowed = True  # Global control flag

# Function to generate response using Gemini API
def generate_response(user_input):
    model = genai.GenerativeModel("gemini-1.5-flash")
    response = model.generate_content(user_input)
    return response.text

# Recognize speech from microphone
def recognize_speech():
    recognizer = sr.Recognizer()
    mic = sr.Microphone()

    with mic as source:
        st.info("🎤 Listening...")
        recognizer.adjust_for_ambient_noise(source)
        audio = recognizer.listen(source)

    try:
        st.info("🧠 Processing...")
        text = recognizer.recognize_google(audio)
        st.success(f"✅ You said: {text}")
        return text
    except sr.UnknownValueError:
        st.warning("⚠️ Could not understand.")
        return None
    except sr.RequestError:
        st.error("❌ Speech service failed.")
        return None

# Speak response using pyttsx3
def speak(text):
    def run():
        global is_speaking_allowed
        with engine_lock:
            if is_speaking_allowed and text.strip():
                try:
                    engine.say(text)
                    engine.runAndWait()
                except Exception as e:
                    st.error(f"🛑 TTS Error: {str(e)}")

    t = threading.Thread(target=run)
    t.daemon = True
    t.start()

# Stop any ongoing speech
def stop_speaking():
    global is_speaking_allowed
    with engine_lock:
        is_speaking_allowed = False
        engine.stop()
    st.success("🛑 Voice stopped.")

# Reactivate voice
def allow_speaking():
    global is_speaking_allowed
    is_speaking_allowed = True

# Streamlit UI
st.set_page_config(page_title="TechConnect Voice Chat", page_icon="🗣️")
st.title("🗣️ TechConnect Voice + Text Chatbot")

# Chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display previous chat messages
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# Button layout
col1, col2 = st.columns(2)

with col1:
    if st.button("🎙️ Start Voice Chat"):
        allow_speaking()
        user_input = recognize_speech()
        if user_input:
            st.session_state.messages.append({"role": "user", "content": user_input})
            with st.chat_message("user"):
                st.markdown(user_input)

            with st.chat_message("assistant"):
                response_area = st.empty()
                try:
                    response_text = generate_response(user_input)
                except Exception as e:
                    response_text = f"❌ Error: {str(e)}"
                response_area.markdown(response_text)

            st.session_state.messages.append({"role": "assistant", "content": response_text})
            speak(response_text)

with col2:
    if st.button("🔇 Stop Speaking"):
        stop_speaking()

# --- Text-to-Text Section ---
st.markdown("---")
st.subheader("⌨️ Text-to-Text Chat")

text_input = st.text_input("Type your message here:")

if st.button("📤 Send"):
    if text_input.strip():
        allow_speaking()
        st.session_state.messages.append({"role": "user", "content": text_input})
        with st.chat_message("user"):
            st.markdown(text_input)

        with st.chat_message("assistant"):
            response_area = st.empty()
            try:
                response_text = generate_response(text_input)
            except Exception as e:
                response_text = f"❌ Error: {str(e)}"
            response_area.markdown(response_text)

        st.session_state.messages.append({"role": "assistant", "content": response_text})
        speak(response_text)
    else:
        st.warning("⚠️ Please enter a message to send.")
