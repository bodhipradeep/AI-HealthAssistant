from langgraph.graph import StateGraph, START, END
from config.graph_state import State
from langgraph.checkpoint.memory import InMemorySaver
from workflow.append_symptoms import add_symptoms
from workflow.hitl import human_assistance, human_decision
from workflow.agent_nodes import (
    node_symptoms_analysis,
    node_generated_symptoms,
    node_diagnosis,
    node_treatment_plan
)

memory = InMemorySaver()

agentflow = StateGraph(State)
agentflow.add_node("Symptoms_Analysis", node_symptoms_analysis)
agentflow.add_node("Generated_Symptoms", node_generated_symptoms)
agentflow.add_node("Patient_Confirmation", human_assistance)
agentflow.add_node("Need_More_Symptoms", add_symptoms)
agentflow.add_node("Diagnosis", node_diagnosis)
agentflow.add_node("Final_Report", node_treatment_plan)

agentflow.add_edge(START, "Symptoms_Analysis")
agentflow.add_edge("Symptoms_Analysis", "Generated_Symptoms")
agentflow.add_edge("Generated_Symptoms", "Patient_Confirmation")
agentflow.add_conditional_edges(
    "Patient_Confirmation",
    human_decision,
    {"Symptoms_Matched": "Diagnosis", "Symptoms_Not_Matched": "Need_More_Symptoms"}
)
agentflow.add_edge("Need_More_Symptoms", "Symptoms_Analysis")
agentflow.add_edge("Diagnosis", "Final_Report")
agentflow.add_edge("Final_Report", END)

agentflow.set_entry_point("Symptoms_Analysis")
agentflow.set_finish_point("Final_Report")

graph = agentflow.compile(checkpointer=memory)
