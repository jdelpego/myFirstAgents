from langchain.tools import tool
from langchain_xai import ChatXAI
from typing_extensions import TypedDict


llm = ChatXAI(
    model="grok-4-1-fast-reasoning"    
)

class State(TypedDict):
    count: int

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
