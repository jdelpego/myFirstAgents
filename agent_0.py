from langchain.agents import create_agent

def get_weather(city: str) -> str:
    """Get weather for a given city."""
    return f"It's always sunny in {city}!"

def print_message(message: str):
    """Print a message to the console."""
    print(message)

agent = create_agent(
    model="claude-sonnet-4-5-20250929",
    tools=[get_weather, print_message],
    system_prompt="You are a helpful assistant",
)

# Run the agent
agent.invoke(
    {"messages": [{"role": "user", "content": "Print out the weather in sf to the console"}]}
)