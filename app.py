import streamlit as st
# import sounddevice as sd
# import wavio
from gtts import gTTS
from google import genai
import os
from tempfile import NamedTemporaryFile
# import speech_recognition as sr
import json 
from streamlit_lottie import st_lottie 
import requests

# GEMINI_API_KEY = "API KEY" 

if "GEMINI_API_KEY" in st.secrets:
    GEMINI_API_KEY = st.secrets["GEMINI_API_KEY"]
else:
    GEMINI_API_KEY = "API KEY"

RECORDING_DURATION = 5 # seconds
FS = 44100

# Top section
st.set_page_config(page_title="AITR Helper", page_icon="🎓", layout="wide")

# Lottie Function
@st.cache_data
def load_lottieurl(url: str):
    try:
        r = requests.get(url, timeout=5)
        if r.status_code == 200:
            return r.json()
        return None
    except requests.exceptions.RequestException:
        return None

# Lottie Animation URLs
LOTTIE_WRITING = load_lottieurl("https://lottie.host/7e02b662-79e0-4965-9831-29e3776b6d5f/qQ53jJ03lP.json")
LOTTIE_CALENDAR = load_lottieurl("https://lottie.host/880a18ab-70b5-4148-8e6d-66e5111b2383/pL4fFfC6K4.json")
LOTTIE_CHATBOT = load_lottieurl("https://lottie.host/80a22f30-84e1-450f-a99f-43183569420b/mK4oF8sFw3.json")

lottie_config = {
    "speed": 1, 
    "loop": True, 
    "quality": "high", 
    "height": 100,
    "width": 100,
}

st.markdown(
    """
    <style>
    /* ---------------- FONT IMPORT ---------------- */
    @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;600;700;800;900&display=swap');
    
    /* Remove top whitespace and header */
    .block-container { padding-top: 0rem !important; }
    header, [data-testid="stHeader"] { display: none !important; }

    /* App background & FONT application */
    .stApp {
        font-family: 'Poppins', sans-serif; 
        background: radial-gradient(circle at 10% 10%, #0b0d0f, #0f1113 40%, #0d0f12 100%) !important;
        color: #e6eef3;
    }

    /* Center container */
    .main-container {
        max-width: 980px;
        margin: 30px auto;
        padding: 24px;
    }

    /* Glass card */
    .glass {
        background: rgba(255,255,255,0.03);
        border-radius: 18px; 
        padding: 30px; 
        margin-bottom: 25px; 
        border: 1px solid rgba(255,255,255,0.08); 
        backdrop-filter: blur(10px);
        box-shadow: 0 4px 30px rgba(0, 0, 0, 0.2); 
    }

    .title {
        font-size: 48px; 
        font-weight: 900;
        text-align: center;
        color: #4ec9b0; 
        text-shadow: 0 0 10px rgba(78, 201, 176, 0.4);
        margin-bottom: 8px;
    }

    .subtitle {
        text-align: center;
        color: #bfc9cf;
        font-size: 1.1rem;
        margin-bottom: 30px;
    }

    /* Inputs */
    .stTextInput>div>div>input, .stTextArea textarea {
        background: rgba(255,255,255,0.08) !important;
        color: #f6f9fb !important;
        border-radius: 12px !important;
        padding: 14px !important; 
        border: 1px solid #3d4a5c !important; 
        transition: all 0.3s;
    }
    .stTextInput>div>div>input:focus, .stTextArea textarea:focus {
        border-color: #4ec9b0 !important; 
        box-shadow: 0 0 5px rgba(78, 201, 176, 0.5);
    }
    .stNumberInput input {
        background: rgba(255,255,255,0.08) !important;
        color: #f6f9fb !important;
        border-radius: 12px !important;
        padding: 10px !important;
    }
    
    /* Buttons style */
    .stButton>button {
        border-radius: 10px !important;
        padding: 10px 20px !important;
        font-weight: 700;
        transition: all 0.3s;
        box-shadow: 0 2px 5px rgba(0, 0, 0, 0.3);
    }

    /* Primary/Generate Button */
    .btn-primary button {
        background: #4ec9b0 !important;
        color: #051010 !important;
        border: none !important;
    }
    .btn-primary button:hover {
        background: #3ac0a6 !important;
        transform: translateY(-2px);
    }

    /* Secondary/Voice Button (Blue for action) */
    .btn-secondary button {
        background: #2b8cff !important;
        color: white !important;
        border: none !important;
    }
    .btn-secondary button:hover {
        background: #1a78e7 !important;
        transform: translateY(-2px);
    }

    /* Listen Button (Accent color) */
    .btn-listen button {
        background: #e6a239 !important; 
        color: #051010 !important;
        border: none !important;
        width: 100%;
        margin-top: 10px;
    }
    .btn-listen button:hover {
        background: #d49533 !important;
        transform: scale(1.02);
    }

    /* Headings inside card */
    .card-h {
        font-size: 24px; 
        font-weight: 800;
        margin-bottom: 15px;
        color: #4ec9b0; 
        border-bottom: 2px solid rgba(78, 201, 176, 0.3);
        padding-bottom: 5px;
    }

    /* small muted text */
    .muted { color: #aab6bb; font-size: 14px; margin-top: 10px; }

    /* Custom Info/Success/Error containers */
    div.stAlert {
        border-radius: 10px;
        padding: 10px 15px;
        margin-bottom: 15px;
        color: #f6f9fb;
    }
    .stAlert.info { background-color: rgba(43, 140, 255, 0.2); border-left: 5px solid #2b8cff; }
    .stAlert.success { background-color: rgba(78, 201, 176, 0.2); border-left: 5px solid #4ec9b0; }
    .stAlert.error { background-color: rgba(255, 69, 0, 0.2); border-left: 5px solid #ff4500; }
    
    /* Center Lottie animation in the spinner placeholder */
    .lottie-container {
        display: flex;
        justify-content: center;
        align-items: center;
        margin-top: 10px;
        margin-bottom: 10px;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

st.markdown("<div class='main-container'>", unsafe_allow_html=True)

# Header
st.markdown("<div class='title'>AITR Helper 🎓</div>", unsafe_allow_html=True)
st.markdown("<div class='subtitle'>Your Personal **Gemini-Powered** Student Assistant: Notes, Planning, & College Info.</div>", unsafe_allow_html=True)

# API Key
client = None
if GEMINI_API_KEY and GEMINI_API_KEY != "API KEY":
    client = genai.Client(api_key=GEMINI_API_KEY)
else:
    # Display error only if key is the placeholder or missing
    st.markdown("<div class='glass'>", unsafe_allow_html=True)
    st.markdown("<div class='card-h'>⚠️ Configuration Required</div>", unsafe_allow_html=True)
    st.markdown('<div class="stAlert error">❌ **Error:** Please replace `"API KEY"` with your actual Gemini API Key in the `app.py` file to enable AI features.</div>', unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)
    
# Notes Generator Card
st.markdown("<div class='glass'>", unsafe_allow_html=True)
st.markdown("<div class='card-h'>✍️ Study Notes Generator</div>", unsafe_allow_html=True) 
note_topic = st.text_area("Enter Topic / Paste Text for Notes:", placeholder="e.g. Operating Systems - Process Synchronization or a paragraph from a book.")

# Voice input storage
if "voice_notes" not in st.session_state:
    st.session_state["voice_notes"] = ""

col1, col2 = st.columns([1, 1])
with col1:
    # Voice input button - Secondary Button
    if st.button(f"🎤 Speak for Notes (Max {RECORDING_DURATION}s)", key="speak_notes", help="Record your topic or source material for notes generation."):
        st.warning("Voice feature is disabled in Cloud Deployment.")
        # if client:
        #     st.info(f"🎙️ Recording in progress for **{RECORDING_DURATION} seconds**...")
        #     recording = sd.rec(int(RECORDING_DURATION * FS), samplerate=FS, channels=1, dtype='int16')
        #     sd.wait()
        #     wavio.write("notes_input.wav", recording, FS, sampwidth=2)
        #     try:
        #         recognizer = sr.Recognizer()
        #         with sr.AudioFile("notes_input.wav") as source:
        #             audio_data = recognizer.record(source)
        #             text = recognizer.recognize_google(audio_data)
        #         st.markdown(f'<div class="stAlert success">✅ Recognized Topic: **{text}**</div>', unsafe_allow_html=True)
        #         st.session_state["voice_notes"] = text
        #     except Exception:
        #         st.markdown('<div class="stAlert error">❌ Could not understand audio. Try again or type the text.</div>', unsafe_allow_html=True)
        # else:
        #     st.markdown('<div class="stAlert error">⚠️ API Client not configured. Check the code for the API Key.</div>', unsafe_allow_html=True)

with col2:
    # Generate Button - Primary Button
    st.markdown("<div class='btn-primary'>", unsafe_allow_html=True)
    if st.button("🚀 Generate Notes", key="gen_notes", help="Generate concise notes using the text input or the last voice recording."):
        final_topic = (note_topic or st.session_state.get("voice_notes", "")).strip()
        if client is None or final_topic == "":
            st.markdown('<div class="stAlert error">⚠️ Check API Key in code AND enter a topic/text.</div>', unsafe_allow_html=True)
        else:
            if LOTTIE_WRITING: 
                with st.empty():
                    st.markdown("<div class='lottie-container'>", unsafe_allow_html=True)
                    st_lottie(LOTTIE_WRITING, **lottie_config, key="notes_lottie")
                    st.markdown("</div>", unsafe_allow_html=True)
                    st.info("🧠 Generating **high-quality** notes with Gemini... Please wait.") 
            else: 
                with st.spinner("🧠 Generating **high-quality** notes with Gemini... Please wait."):
                    pass
            try:
                resp = client.models.generate_content(
                    model="gemini-2.0-flash",
                    contents=f"Create clear, concise study notes for students on: {final_topic}. Use bolding, bullet points, and short definitions. Output should be in clean markdown format."
                )
                st.session_state["notes"] = resp.text
                st.markdown('<div class="stAlert success">✅ Notes generated successfully! Scroll down to read.</div>', unsafe_allow_html=True)
            except Exception as e:
                st.markdown(f'<div class="stAlert error">❌ Gemini Error: Could not generate content. Check the topic or Gemini API status.</div>', unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)

# Display notes & listen
if "notes" in st.session_state:
    st.markdown("<hr style='border-color: rgba(255,255,255,0.1); margin-top: 20px; margin-bottom: 20px;'>", unsafe_allow_html=True)
    st.markdown("<div class='card-h'>📄 Generated Notes</div>", unsafe_allow_html=True)
    st.markdown(st.session_state["notes"]) 
    st.markdown("<div class='muted'>Review your notes and use the button below to listen to them.</div>", unsafe_allow_html=True)

    st.markdown("<div class='btn-listen'>", unsafe_allow_html=True)
    if st.button("🔊 Listen to Notes (Text-to-Speech)", key="listen_notes"):
        with st.spinner("🎧 Preparing audio file..."):
            tts = gTTS(st.session_state["notes"])
            with NamedTemporaryFile(delete=False, suffix=".mp3") as tmp:
                tts.save(tmp.name)
                audio_path = tmp.name
            st.audio(audio_path, format="audio/mp3", autoplay=True)
        os.remove(audio_path) 
    st.markdown("</div>", unsafe_allow_html=True)

st.markdown("</div>", unsafe_allow_html=True)

# Exam Planner Card
st.markdown("<div class='glass'>", unsafe_allow_html=True)
st.markdown("<div class='card-h'>🗓️ Custom Exam Study Planner</div>", unsafe_allow_html=True) 
subjects = st.text_area("Enter subject names:", placeholder="e.g. Physics, Mathematics, Chemistry, Computer Networks (comma-separated)", key="subjects_text")

if "voice_subjects" not in st.session_state:
    st.session_state["voice_subjects"] = ""

col1, col2, col3 = st.columns([1, 1, 1])
with col1:
    days = st.number_input("Days Left for Exam:", min_value=1, max_value=180, value=30, help="The number of days you have to prepare for the exams.")

with col2:
    st.markdown("<div style='margin-top: 24px;'>", unsafe_allow_html=True) 
    if st.button(f"🎤 Speak Subjects (Max {RECORDING_DURATION}s)", key="speak_subjects"):
        st.warning("Voice feature is disabled in Cloud Deployment.")
        # if client:
        #     st.info(f"🎙️ Recording subjects for **{RECORDING_DURATION} seconds**...")
        #     recording = sd.rec(int(RECORDING_DURATION * FS), samplerate=FS, channels=1, dtype='int16')
        #     sd.wait()
        #     wavio.write("subjects_input.wav", recording, FS, sampwidth=2)
        #     try:
        #         recognizer = sr.Recognizer()
        #         with sr.AudioFile("subjects_input.wav") as source:
        #             audio_data = recognizer.record(source)
        #             text = recognizer.recognize_google(audio_data)
        #         st.markdown(f'<div class="stAlert success">✅ Recognized Subjects: **{text}**</div>', unsafe_allow_html=True)
        #         st.session_state["voice_subjects"] = text
        #     except Exception:
        #         st.markdown('<div class="stAlert error">❌ Voice not recognized.</div>', unsafe_allow_html=True)
        # else:
        #     st.markdown('<div class="stAlert error">⚠️ API Client not configured. Check the code for the API Key.</div>', unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)


with col3:
    st.markdown("<div class='btn-primary' style='margin-top: 24px;'>", unsafe_allow_html=True) 
    if st.button("📅 Create Study Plan", key="create_plan", help="Generate a daily study schedule based on the subjects and days left."): 
        final_subjects = (subjects or st.session_state.get("voice_subjects", "")).strip()
        if client is None or final_subjects == "":
            st.markdown('<div class="stAlert error">⚠️ Check API Key in code AND enter subjects.</div>', unsafe_allow_html=True)
        else:
            if LOTTIE_CALENDAR:
                with st.empty():
                    st.markdown("<div class='lottie-container'>", unsafe_allow_html=True)
                    st_lottie(LOTTIE_CALENDAR, **lottie_config, key="planner_lottie")
                    st.markdown("</div>", unsafe_allow_html=True)
                    st.info(f"⏳ Creating a balanced **{days}-day** study plan with Gemini... Sit tight!")
            else:
                with st.spinner(f"⏳ Creating a balanced **{days}-day** study plan with Gemini... Sit tight!"):
                    pass
            try:
                resp = client.models.generate_content(
                    model="gemini-2.0-flash",
                    contents=f"Create a balanced and detailed {days}-day study plan for these subjects: {final_subjects}. Include daily tasks, a suggested time-slot for each subject, and dedicated revision slots. Use clear markdown headers and bullet points for the plan."
                )
                st.session_state["study_plan"] = resp.text
                st.markdown('<div class="stAlert success">✅ Study plan created! Get ready to study!</div>', unsafe_allow_html=True)
            except Exception as e:
                st.markdown(f'<div class="stAlert error">❌ Gemini Error: Could not create study plan.</div>', unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)

if "study_plan" in st.session_state:
    st.markdown("<hr style='border-color: rgba(255,255,255,0.1); margin-top: 20px; margin-bottom: 20px;'>", unsafe_allow_html=True)
    st.markdown("<div class='card-h'>✅ Your Custom Study Plan</div>", unsafe_allow_html=True)
    st.markdown(st.session_state["study_plan"])

    st.markdown("<div class='btn-listen'>", unsafe_allow_html=True)
    if st.button("🔊 Listen to Study Plan", key="listen_plan"):
        with st.spinner("🎧 Preparing audio file..."):
            tts = gTTS(st.session_state["study_plan"])
            with NamedTemporaryFile(delete=False, suffix=".mp3") as tmp:
                tts.save(tmp.name)
                audio_path = tmp.name
            st.audio(audio_path, format="audio/mp3", autoplay=True)
        os.remove(audio_path)
    st.markdown("</div>", unsafe_allow_html=True)

st.markdown("</div>", unsafe_allow_html=True)

# Chatbot Card

if "chatbot_messages" not in st.session_state:
    st.session_state["chatbot_messages"] = [
        {"role": "model", "content": "Hello! I am your **AITR College Assistant**, powered by Gemini. Ask me anything **specific about Acropolis Institute (Indore)**! I am programmed to focus only on AITR information."}
    ]

st.markdown("<div class='glass'>", unsafe_allow_html=True)
st.markdown("<div class='card-h'>🏫 AITR College Chatbot</div>", unsafe_allow_html=True) 

# --- Voice Input for Chat ---
col1, col2 = st.columns([1, 1])

with col1:
    if st.button(f"🎤 Speak Question (Max {RECORDING_DURATION}s)", key="speak_chat"):
        st.warning("Voice feature is disabled in Cloud Deployment.")
        # if client:
        #     st.info(f"🎙️ Recording question for **{RECORDING_DURATION} seconds**...")
        #     recording = sd.rec(int(RECORDING_DURATION * FS), samplerate=FS, channels=1, dtype='int16')
        #     sd.wait()
        #     wavio.write("chat_input.wav", recording, FS, sampwidth=2)
        #     try:
        #         recognizer = sr.Recognizer()
        #         with sr.AudioFile("chat_input.wav") as source:
        #             audio_data = recognizer.record(source)
        #             prompt = recognizer.recognize_google(audio_data)
        #         if prompt:
        #             st.markdown(f'<div class="stAlert success">✅ Recognized Question: **{prompt}**</div>', unsafe_allow_html=True)
        #             st.session_state["chatbot_messages"].append({"role": "user", "content": prompt})
        #             with st.empty(): 
        #                 st.info("🤔 Thinking... Getting **AITR info** with Gemini... Almost done!")
        #             contents_list = []
        #             for msg in st.session_state["chatbot_messages"]:
        #                 contents_list.append({"role": msg["role"], "parts": [{"text": msg["content"]}]})

        #             with st.spinner("Generating response..."):
        #                 try:
        #                     resp = client.models.generate_content(
        #                         model="gemini-2.0-flash",
        #                         contents=contents_list
        #                     )
        #                     st.session_state["chatbot_messages"].append({"role": "model", "content": resp.text})
        #                 except Exception as e:
        #                     st.session_state["chatbot_messages"].append({"role": "model", "content": f'❌ **Error:** Could not get answer from Gemini. Check topic or API status. (Reason: {e})'})
                    
        #             st.rerun()

        #     except Exception:
        #         st.markdown('<div class="stAlert error">❌ Voice not recognized.</div>', unsafe_allow_html=True)
        # else:
        #     st.markdown('<div class="stAlert error">⚠️ API Client not configured. Check the code for the API Key.</div>', unsafe_allow_html=True)

# Display Chat History
for message in st.session_state["chatbot_messages"]:
    if message["role"] == "user":
        with st.chat_message("user"):
            st.markdown(message["content"])
    elif message["role"] == "model":
        with st.chat_message("assistant"):
            st.markdown(message["content"])
            
            if message == st.session_state["chatbot_messages"][-1]:
                if st.button("🔊 Listen to Answer", key=f"listen_chat_{len(st.session_state['chatbot_messages'])}"):
                    with st.spinner("🎧 Preparing audio file..."):
                        tts = gTTS(message["content"])
                        with NamedTemporaryFile(delete=False, suffix=".mp3") as tmp:
                            tts.save(tmp.name)
                            audio_path = tmp.name
                        st.audio(audio_path, format="audio/mp3", autoplay=True)
                        os.remove(audio_path)

# Chat Input for continuation
prompt = st.chat_input("Ask a follow-up question about AITR...")

if prompt:
    if client is None:
        st.markdown('<div class="stAlert error">⚠️ API Client not configured. Check the code for the API Key.</div>', unsafe_allow_html=True)
    else:
        # Add user message to history
        st.session_state["chatbot_messages"].append({"role": "user", "content": prompt})

        contents_list = []
        for msg in st.session_state["chatbot_messages"]:
            contents_list.append({"role": msg["role"], "parts": [{"text": msg["content"]}]})

        with st.chat_message("assistant"):
            st.info("🤔 Thinking... Getting **AITR info** with Gemini... Almost done!")
        
        with st.spinner("Generating response..."):
            
            try:
                resp = client.models.generate_content(
                    model="gemini-2.0-flash",
                    contents=contents_list
                )
                # Add model response to history
                st.session_state["chatbot_messages"].append({"role": "model", "content": resp.text})
            except Exception as e:
                st.session_state["chatbot_messages"].append({"role": "model", "content": f'❌ **Error:** Could not get answer from Gemini. Check topic or API status. (Reason: {e})'})
            
            st.rerun()


st.markdown("</div>", unsafe_allow_html=True)

# footer
st.markdown("<div style='text-align:center; color:#556671; margin-top:25px; font-size: 0.9rem;'>**Chat With AITR**</div>", unsafe_allow_html=True)
st.markdown("</div>", unsafe_allow_html=True)