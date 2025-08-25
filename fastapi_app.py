from fastapi import FastAPI, HTTPException
from uuid import uuid4
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional, List, Dict, Any, Literal
from workflow.graph_builder import graph
from core.weather_info import get_weather
from langgraph.types import Command

app = FastAPI(
    title="AI Health Assistant API",
    version="1.0",
    description="AI-powered medical diagnosis assistant"
)

# Allow cross-origin requests (for Streamlit)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # update in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Request model
class DiagnosisRequest(BaseModel):
    symptoms: List[str]
    patient_details: Dict[str, Any]
    report: Optional[str] = None

# Store diagnosis sessions in memory
diagnosis_sessions: Dict[str, DiagnosisRequest] = {}

class ResumeDiagnosisRequest(BaseModel):
    thread_id: str
    human: str
    more_symptoms: Optional[List[str]] = None

# Response model
class DiagnosisResponse(BaseModel):
    thread_id: Optional[str] = None
    symptoms: Optional[List[str]] = None
    result: Optional[str] = None

def add_more_symptoms(diagnosis: DiagnosisRequest, add_symptoms: Optional[List[str]]) -> DiagnosisRequest:
    if add_symptoms:
        new_unique = [s for s in add_symptoms if s not in diagnosis.symptoms]
        diagnosis.symptoms.extend(new_unique)
    return diagnosis


@app.post("/diagnose/start", response_model=DiagnosisResponse)
def diagnose(request: DiagnosisRequest):
    try:
        thread_id = str(uuid4())
        config = {"configurable": {"thread_id": thread_id}}
        # Save session
        diagnosis_sessions[thread_id] = request
        
        # Fetch weather info from server based on location
        location = request.patient_details.get("Location", "")
        weather_info = get_weather(location)
        
        # Prepare initial state
        initial_state = {
            "symptoms": request.symptoms,
            "patient_details": request.patient_details,
            "weather_info": weather_info,
            "report": request.report,
        }
        
        # Run the workflow automatically
        events = graph.invoke(input=initial_state, config=config)
        output = events["messages"][-1].content
        return DiagnosisResponse(thread_id=thread_id, symptoms=request.symptoms, result=output)

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Diagnosis Function Error: {e}")
  
@app.post("/diagnosis/resume", response_model=DiagnosisResponse)
def resume_diagnosis(request: ResumeDiagnosisRequest):
    try:
        diagnosis = diagnosis_sessions.get(request.thread_id)
        if not diagnosis:
            raise HTTPException(status_code=404, detail="No ongoing session found")
        
        if request.human == "feedback":
            add_more_symptoms(diagnosis, request.more_symptoms)
            
        updated_state = {
            "symptoms": diagnosis.symptoms,
            "patient_details": diagnosis.patient_details,
            "report": diagnosis.report,
        }
        
        config = {"configurable": {"thread_id": request.thread_id}}
        resume = graph.invoke(Command(resume=request.human, update=updated_state), config)
        final_output = resume["messages"][-1].content
        return DiagnosisResponse(thread_id=request.thread_id, symptoms=diagnosis.symptoms, result=final_output)

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Resume Function Error: {e}")
