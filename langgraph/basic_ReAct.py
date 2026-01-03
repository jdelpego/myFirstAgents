from operator import add
from langchain.tools import tool
from langchain_xai import ChatXAI
from typing_extensions import TypedDict, List, Annotated
from langgraph.graph import StateGraph, START, END
from langchain_core.messages import BaseMessage
from langchain.messages import SystemMessage, HumanMessage, ToolMessage


llm = ChatXAI(
    model="grok-4-1-fast-reasoning"    
)

class State(TypedDict):
    count: int
    # Use a reducer to define state so each node (not tool) only needs to return modified parameters
    messages: Annotated[List[BaseMessage], add]
    

# Tools
@tool
def add_x(state: State, x: int) -> None:
    """Adds x to the current count in state"""
    state["count"] += x

@tool
def print_message(message: str) -> None:
    """Print a message to the console."""
    print(message)
    
tools = [add_x, print_message]
tools_by_name = {tool.name: tool for tool in tools}
llm_with_tools = llm.bind_tools(tools)

# Nodes
def llm_call(state: State):
    "LLM decides wether to call a tool or not."
    llm_response = llm_with_tools.invoke(
        [SystemMessage(content="You are a helpful assistant.")] + state["messages"]
    )
    return {"messages": [llm_response]}
    
def tool_node(state: State):
    """Performs the tool call"""
    result = []
    for tool_call in state["messages"][-1].tool_calls:
        tool = tools_by_name[tool_call["name"]]
        observation = tool.invoke(tool_call["args"])
        result.append(ToolMessage(content=observation, tool_call_id=tool_call["id"]))
    return {"messages": result}
    
# Conditional edges
def should_continue(state: State) -> bool:
    last_message = state["messages"][-1]
    if last_message.tool_calls:
        return True
    return False    

# Build graph
agent_builder = StateGraph(State)
agent_builder.add_node("llm_call", llm_call)
agent_builder.add_node("tool_node", tool_node)
agent_builder.add_edge(START, "llm_call")
agent_builder.add_conditional_edges(
    "llm_call",
    should_continue,
    {
        True: "tool_node",
        False: END
    },
)
agent_builder.add_edge("tool_node","llm_call")
agent = agent_builder.compile()

result = agent.invoke({
    "messages": [HumanMessage(content="Add 7 to the intial count, print it out to console, then subtract 3 print it out. Print nothing else.")],
    "count": 4
    })

for m in result["messages"]:
    m.pretty_print()






