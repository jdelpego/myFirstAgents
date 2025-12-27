from typing_extensions import TypedDict
from langgraph.graph import StateGraph, START, END
from langchain_core.runnables import RunnableConfig
from langgraph.checkpoint.memory import InMemorySaver

class State(TypedDict):
    count: int

def add_1(state: State) -> State:
    """Adds 1 to the current count in state"""
    return {"count": state["count"] + 1} 

builder = StateGraph(State)
builder.add_node("add_1", add_1)
builder.add_edge(START, "add_1")
builder.add_edge("add_1", END)

checkpointer = InMemorySaver()

agent = builder.compile(checkpointer=checkpointer)

config: RunnableConfig = {"configurable": {"thread_id": "1"}}

print(agent.invoke({"count": 0}, config))
print(agent.invoke({}, config))
print(agent.invoke({}, config))


