from typing_extensions import Annotated, List, Union, TypedDict, Optional
from langgraph.graph.message import add_messages
from langchain_core.messages import HumanMessage, AIMessage, ToolMessage

# Define LangGraph state
# Define LangGraph state
class State(TypedDict, total=False):
    messages: Annotated[List[Union[HumanMessage, AIMessage]], add_messages]
    symptoms: list[str]
    patient_details: dict[str, str]
    weather_info: dict[str, str]
    human: str
    report: Optional[str]
    analysis: str
    generated_symptoms: str
    diagnosis_result: str
    final_plan: str