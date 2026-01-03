from langchain.tools import tool
from langchain_xai import ChatXAI
from typing_extensions import TypedDict, List
from langgraph.graph import MessagesState
from langchain.messages import SystemMessage, HumanMessage, ToolMessage, BaseMessage


llm = ChatXAI(
    model="grok-4-1-fast-reasoning"    
)

class State(TypedDict):
    count: int
    messages: List[BaseMessage]

@tool
def add_x(state: State, x: int) -> State:
    """Adds x to the current count in state"""
    return {"count": state["count"] + x}

@tool
def print_message(message: str) -> None:
    """Print a message to the console."""
    print(message)
    
tools = [add_x, print_message]
tools_by_name = {tool.name: tool for tool in tools}
llm_with_tools = llm.bind_tools(tools)

