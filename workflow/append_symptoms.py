from config.graph_state import State


# workflow/append_symptoms.py
def add_symptoms(state):
    """Append new symptoms to the state when user provides them."""
    new_symptoms = state.get("new_symptoms", "")
    if not new_symptoms:
        return state

    extra = [s.strip() for s in new_symptoms.split(",") if s.strip()]
    state["symptoms"].extend(extra)
    return state