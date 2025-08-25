from config.graph_state import State
from langgraph.types import interrupt


def human_assistance(state: State):
    """Ask the patient to confirm whether the generated symptoms match their experience."""
    options = ("approved", "feedback")
    response = interrupt(options)
    return {"human": response}

    
def human_decision(state: State) -> str:
    """Decide next step based on human input."""
    human_value = state.get("human", "")
    if human_value == "approved":
        return "Symptoms_Matched"
    else:
        return "Symptoms_Not_Matched"
