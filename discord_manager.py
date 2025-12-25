import os
import json
import requests
from dotenv import load_dotenv
from langchain.tools import tool
from langchain_xai import ChatXAI
from langchain.agents import create_agent


load_dotenv()
DISCORD_GUILD_ID = os.environ.get("DISCORD_GUILD_ID")
DISCORD_BOT_TOKEN = os.environ.get("DISCORD_BOT_TOKEN")

llm = ChatXAI(
    model="grok-4-1-fast-reasoning"    
)

SYSTEM_PROMPT = """
You are a Discord manager for restructuring guilds to improve user communication and maintain clean aesthetics.

Tools: get_guild_channels, create_channel, modify_channel, create_category, create_forum, create_public_thread.

Follow user instructions precisely. Never delete channels. Archive unused ones in a single "Archive" category at the bottom, clearly labeling channels and dead categories.

Prefer renaming existing channels over creating new. Reuse categories by renaming to avoid excess archives. Use forums/threads for better organization when appropriate.

Optimize for effective communication, aesthetic organization, and user goals.
"""

# @tool
# def print_message(message: str):
#     """Prints a message to the console for logging or user feedback."""
#     print(message)

# def delete_channel(id: str) -> json:
#     """Deletes a channel by its ID. Requires MANAGE_CHANNELS permission. Returns the deleted channel object or an error."""
#     url = f"https://discord.com/api/v10/channels/{id}"
#     headers = {"Authorization": f"Bot {BOT_TOKEN}"}
#     response = requests.delete(url, headers=headers)
#     if response.status_code == 200:
#         return response.json()
#     else:
#         return {"error": f"Failed to delete channel: {response.status_code}"}

@tool
def get_guild_channels() -> json:
    """Retrieves a list of all channels in the guild, including their details like ID, name, type, and position."""
    url = f"https://discord.com/api/v10/guilds/{DISCORD_GUILD_ID}/channels"
    headers = {"Authorization": f"Bot {DISCORD_BOT_TOKEN}"}
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        return response.json()
    else:
        return {"error": f"Failed to fetch channels: {response.status_code}"}

@tool 
def create_channel(name: str, parent_id: str = "", position: int = 0) -> json:
    """Creates a text channel with the given name. Optionally set parent_id (category) and position. Returns the created channel or an error."""
    url = f"https://discord.com/api/v10/guilds/{DISCORD_GUILD_ID}/channels"
    headers = {"Authorization": f"Bot {DISCORD_BOT_TOKEN}"}
    data = {"name": name, "type": 0, "position": position}
    if parent_id:
        data["parent_id"] = parent_id
    response = requests.post(url, headers=headers, json=data)
    if response.status_code == 201:
        return response.json()
    else:
        return {"error": f"Failed to create channel: {response.status_code}"}

@tool
def modify_channel(channel_id: str, name: str = None, parent_id: str = None, position: int = None) -> json:
    """Modifies a channel's properties by ID. Optionally update name, parent_id (category), or position. Returns the updated channel or an error."""
    url = f"https://discord.com/api/v10/channels/{channel_id}"
    headers = {"Authorization": f"Bot {DISCORD_BOT_TOKEN}"}
    data = {}
    if name is not None:
        data["name"] = name
    if parent_id is not None:
        data["parent_id"] = parent_id
    if position is not None:
        data["position"] = position
    response = requests.patch(url, headers=headers, json=data)
    if response.status_code == 200:
        return response.json()
    else:
        return {"error": f"Failed to modify channel: {response.status_code}"}

@tool
def create_category(name: str, position: int = 0) -> json:
    """Creates a category channel with the given name. Optionally set position. Categories group text/voice channels. Returns the created category or an error."""
    url = f"https://discord.com/api/v10/guilds/{DISCORD_GUILD_ID}/channels"
    headers = {"Authorization": f"Bot {DISCORD_BOT_TOKEN}"}
    data = {"name": name, "type": 4, "position": position}
    response = requests.post(url, headers=headers, json=data)
    if response.status_code == 201:
        return response.json()
    else:
        return {"error": f"Failed to create channel: {response.status_code}"}
    
@tool
def create_forum(name: str, position: int = 0) -> json:
    """Creates a forum channel with the given name. Optionally set position. Forums hold public threads. Returns the created forum or an error."""
    url = f"https://discord.com/api/v10/guilds/{DISCORD_GUILD_ID}/channels"
    headers = {"Authorization": f"Bot {DISCORD_BOT_TOKEN}"}
    data = {"name": name, "type": 15, "position": position}
    response = requests.post(url, headers=headers, json=data)
    if response.status_code == 201:
        return response.json()
    else:
        return {"error": f"Failed to create channel: {response.status_code}"}
    
@tool
def create_public_thread(parent_id: str, name: str, position: int = 0) -> json:
    """Creates a public thread in the specified parent channel with the given name. Optionally set position. Returns the created thread or an error."""
    url = f"https://discord.com/api/v10/channels/{parent_id}/threads"
    headers = {"Authorization": f"Bot {DISCORD_BOT_TOKEN}"}
    data = {"name": name, "type": 11, "position": position}
    response = requests.post(url, headers=headers, json=data)
    if response.status_code == 201:
        return response.json()
    else:
        return {"error": f"Failed to create thread: {response.status_code}"}


agent = create_agent(
    model=llm,
    tools=[get_guild_channels, create_channel, modify_channel, create_category, create_forum, create_public_thread],
    system_prompt=SYSTEM_PROMPT
)

# Run the agent
response = agent.invoke(
            {"messages": [{"role": "user", "content": "Reorganize the server into a travel group"}]}
        )

print(response)