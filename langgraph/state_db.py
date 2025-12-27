import os
from dotenv import load_dotenv
from typing_extensions import TypedDict
from langgraph.checkpoint.postgres import PostgresSaver
from langgraph.graph import StateGraph, START, END
from langchain_core.runnables import RunnableConfig

load_dotenv()
POSTGRES_DB_URI = os.environ.get("POSTGRES_DB_URI")

class State(TypedDict):
    count: int

def add_1(state: State) -> State:
    """Adds 1 to the current count in state"""
    return {"count": state["count"] + 1} 

with PostgresSaver.from_conn_string(POSTGRES_DB_URI) as checkpointer:  
    builder = StateGraph(State)
    builder.add_node("add_1", add_1)
    builder.add_edge(START, "add_1")
    builder.add_edge("add_1", END)

    agent = builder.compile(checkpointer=checkpointer)

    config: RunnableConfig = {"configurable": {"thread_id": "1"}}
    print(agent.invoke({"count": 0}, config))



