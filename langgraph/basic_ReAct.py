from operator import add
from langchain.tools import tool
from langchain_xai import ChatXAI
from langgraph.graph import MessagesState, StateGraph, START, END
from langchain.messages import SystemMessage, HumanMessage, ToolMessage


count = 4

llm = ChatXAI(
    model="grok-4-1-fast-reasoning"    
)
# Tools
@tool
def add_x(x: int) -> int:
    """Adds int x to the current count values and returns the count value"""
    global count
    count += x
    return count

@tool
def print_to_console(message: str) -> None:
    """Print a message to the console."""
    print(message)
    
tools = [add_x, print_to_console]
tools_by_name = {tool.name: tool for tool in tools}
llm_with_tools = llm.bind_tools(tools)

# Nodes
def llm_call(state: MessagesState):
    "LLM decides wether to call a tool or not."
    llm_response = llm_with_tools.invoke(
        [SystemMessage(content="You are a helpful assistant.")] + state["messages"]
    )
    return {"messages": [llm_response]}
    
def tool_node(state: MessagesState):
    """Performs the tool call"""
    result = []
    for tool_call in state["messages"][-1].tool_calls:
        tool = tools_by_name[tool_call["name"]]
        observation = tool.invoke(tool_call["args"])
        result.append(ToolMessage(content=observation, tool_call_id=tool_call["id"]))
    return {"messages": result}
    
# Conditional edges
def should_continue(state: MessagesState) -> bool:
    last_message = state["messages"][-1]
    if last_message.tool_calls:
        return True
    return False    

# Build graph
agent_builder = StateGraph(MessagesState)
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
    "messages": [HumanMessage(content="Get the count to equal 7")]   
    })

for m in result["messages"]:
    m.pretty_print()






