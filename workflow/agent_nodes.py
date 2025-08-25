from config.graph_state import State
from langchain_core.messages import AIMessage
from agents.sym_analyzer import symptoms_analysis
from agents.gen_symptoms import more_symptoms
from agents.diagnosis import diagnosis
from agents.treatment_plan import treatment_plan

def node_symptoms_analysis(state: State):
    result = symptoms_analysis(
        state["symptoms"],
        state["patient_details"],
        state["weather_info"],
        state.get("report")
    )
    text = result.content if hasattr(result, "content") else str(result)
    return {"analysis": text, "messages": [AIMessage(content=text)]}


def node_generated_symptoms(state: State):
    result = more_symptoms(
        state["symptoms"],
        state["patient_details"],
        state["weather_info"],
        state.get("analysis"),
        state.get("report")
    )
    text = result.content if hasattr(result, "content") else str(result)
    return {"generated_symptoms": text, "messages": [AIMessage(content=text)]}


def node_diagnosis(state: State):
    result = diagnosis(
        state["symptoms"],
        state["patient_details"],
        state.get("analysis"),
        state.get("report")
    )
    text = result.content if hasattr(result, "content") else str(result)
    return {"diagnosis_result": text, "messages": [AIMessage(content=text)]}


def node_treatment_plan(state: State):
    result = treatment_plan(state["diagnosis_result"])
    text = result.content if hasattr(result, "content") else str(result)
    return {"final_plan": text, "messages": [AIMessage(content=text)]}