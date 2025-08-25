import streamlit as st      
import tempfile
from gtts import gTTS
import os
import requests
from core.report_loader import medical_report

st.set_page_config( page_title="AI Health Assistant", page_icon=":hospital:", )

Base_URL = "http://localhost:8000"

class APIClient:
    def __init__(self, base_url):
        self.base_url = base_url

    def start_diagnosis(self, symptoms, patient_details, report=None):
        payload = {
            "symptoms": symptoms if isinstance(symptoms, list) else [symptoms],
            "patient_details": patient_details,
            "report": report
        }
        response = requests.post(f"{self.base_url}/diagnose/start", json=payload)
        return response.json()

    def resume_diagnosis(self, thread_id, human, more_symptoms=None):
        payload = {"thread_id": thread_id, "human": human}
        if more_symptoms:
            payload["more_symptoms"] = more_symptoms
        response = requests.post(f"{self.base_url}/diagnosis/resume", json=payload)
        return response.json()

api_client = APIClient(Base_URL)

st.markdown("""
<div style="text-align: center; padding: 1rem; background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
            border-radius: 10px; margin-bottom: 1rem;">
    <h1 style="color: white; margin: 0;">🏥 AI Health Assistant</h1>
    <p style="color: white; margin: 0; font-size: 1.1em;">
        Advanced Multi-Agent Medical Diagnosis System
    </p>
</div>
""", unsafe_allow_html=True)

# ---------------- Patient Info ---------------- #
with st.expander("👤 Patient Information"):
    col1, col2, col3 = st.columns(3)
    with col1:
        name = st.text_input("Patient Name")
    with col2:
        age = st.number_input("Age", min_value=0, max_value=120, value=25)
    with col3:
        sex = st.selectbox("Sex", ["Male", "Female", "Other"])
    with col1:
        location = st.text_input("Location (City)")
    with col2:
        weight = st.number_input("Weight (kg)", min_value=0.0, value=70.0)
    with col3:
        height = st.number_input("Height (cm)", min_value=0.0, value=170.0)

# ---------------- Symptoms ---------------- #
with st.expander("🩺 Symptoms", expanded=True):
    custom_symptoms = st.text_area(
        "Enter your symptoms:",
        height=100,
        placeholder="Explain your symptoms here..."
    )
    
    uploaded_pdf = st.file_uploader("Upload Test Report, If Any", type=["pdf"])

patient_details = {
    "Name": name, "Age": age, "Gender": sex,
    "Location": location, "Weight": weight, "Height": height
}

# --------------- Voice Command ---------------
audio_output = st.checkbox("Use Audio Output")

# def text_to_audio_and_play(text):
#     # Create a temporary MP3 file
#     with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as tmp:
#         tts = gTTS(text=text, lang='en')
#         tts.save(tmp.name)
#         return st.audio(tmp.name, format="audio/mp3")
        
        
def text_to_audio_and_play(text, filename="output.mp3"):
    tts = gTTS(text=text, lang='en')
    tts.save(filename)
    st.audio(filename, format="audio/mp3", start_time=0)
    os.remove(filename)

# ---------------- Session State ---------------- #
if "diagnosis_result" not in st.session_state:
    st.session_state["diagnosis_result"] = None

# ---------------- Start Diagnosis ---------------- #
if st.button("🔍 Get Diagnosis", type="primary", disabled=not custom_symptoms):
    report = medical_report(uploaded_pdf)

    with st.spinner("Bot is thinking..."):
        try:
            user_symptoms = [s.strip() for s in custom_symptoms.split("\n") if s.strip()]
            result = api_client.start_diagnosis(user_symptoms, patient_details, report)
            st.session_state["diagnosis_result"] = result
            st.session_state["thread_id"] = result.get("thread_id")
        except Exception as e:
            st.error(f"API request failed: {e}")

# ---------------- Show Results + HITL ---------------- #
if st.session_state["diagnosis_result"] and not st.session_state.get("finished", False):
    # print here user provided symptoms
    st.write(f"##### ***:blue[{patient_details['Name']}] Provided Symptoms***")
    for s in st.session_state["diagnosis_result"].get("symptoms", []):
        st.markdown(f"{s}")


    st.write("#### :rainbow[New Generated Symptoms]")
    st.write(st.session_state["diagnosis_result"].get("result"))
    if audio_output:
        text_to_audio_and_play(st.session_state["diagnosis_result"].get("result"))

    choice = st.selectbox(
        "Based on the Above Symptoms selected right option to continue?",
        ["Select an option", "Yes, New Symptoms Matched", "No, Above Symptoms not matched."],
        key=f"choice_{len(st.session_state['diagnosis_result'].get('symptoms', []))}"
        )

    more_symptoms = None
    if choice == "No, Above Symptoms not matched.":
        more_symptoms = st.text_area("Please enter additional symptoms for clarification")
        

    if st.button("Resume Diagnosis", disabled=(choice == "Select an option")):
        try:
            if choice == "Yes, New Symptoms Matched":
                resumed = api_client.resume_diagnosis(st.session_state["thread_id"], "approved")
                st.success("Patient confirmed. AI Agent Process finished.")
                st.write(resumed.get("result"))
                
                if audio_output and resumed.get("result"):
                    text_to_audio_and_play(resumed.get("result"))
                    
                st.session_state["finished"] = True  # stop loop

            elif choice == "No, Above Symptoms not matched.":
                if not more_symptoms:
                    st.warning("⚠️ Please enter additional symptoms before resuming.")  
                else:
                    additional_symptoms = [s.strip() for s in more_symptoms.split("\n") if s.strip()]
                    resumed = api_client.resume_diagnosis(st.session_state["thread_id"], "feedback", additional_symptoms)
                    st.info("🔄 Diagnosis resumed with additional symptoms.")
                    st.session_state["diagnosis_result"] = resumed
                    
                    if audio_output and resumed.get("result"):
                        text_to_audio_and_play(resumed.get("result"))
                    
                    st.session_state["finished"] = False
                    st.session_state["choice_reset"] = None
                    st.rerun()

        except Exception as e:
            st.error(f"Resume failed: {e}")

with st.sidebar:
    st.markdown("## 🧭 Project Flow")
    st.image("src/image.png")
    
    st.markdown("""
    - **How this works:**
    1. Enter **Patient Information**
    2. Provide **PatientSymptoms**
    3. (Optional) Upload **Medical Report**
    4. AI Agent Analyze **patient info, symptoms, weather, report if any**
    5. AI Agent Generates **Possible Symptoms based on analyzed disease**
    6. Human-in-the-loop (**HITL**) feedback: Confirm or add more symptoms
    7. AI Agent refines diagnosis based on **feedback & history** and strongly suggests final diagnosis
    8. AI Agent makes **Final Treatment Plan using last agent diagnosis report**
    """)