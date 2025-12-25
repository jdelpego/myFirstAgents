import os
import json
import requests
from dotenv import load_dotenv
from langchain.tools import tool
from dataclasses import dataclass
from langchain.agents import create_agent
from langchain.agents.structured_output import ToolStrategy


load_dotenv()
GUILD_ID = os.environ.get("DISCORD_GUILD_ID")
BOT_TOKEN = os.environ.get("DISCORD_BOT_TOKEN")

SYSTEM_PROMPT = """
You are a discord manager who manages and restructures Discord Guilds (Servers).

You have access to the following tools:
- print_message: use this to send updates to the user in the console as you make progress
- get_guild 

If a user asks you to make a change to their discord server follow their instructions carefully.
Do not delete channels without them telling you to get rid of old/unused channels or explicitly giving permission.
 
Use modifying, creation, and if needed, deletion, of categories and channels to maximize:
- Effective communication
- Aesthetic Organization
- Achievement of user goals
"""

@tool
def print_message(message: str):
    """Prints a message to the console for logging or user feedback."""
    print(message)

@tool
def get_guild_channels() -> json:
    """Retrieves a list of all channels in the guild, including their details like ID, name, type, and position."""
    url = f"https://discord.com/api/v10/guilds/{GUILD_ID}/channels"
    headers = {"Authorization": f"Bot {BOT_TOKEN}"}
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        return response.json()
    else:
        return {"error": f"Failed to fetch channels: {response.status_code}"}

@tool
def delete_channel(id: str) -> json:
    """Deletes a channel by its ID. Requires MANAGE_CHANNELS permission. Returns the deleted channel object or an error."""
    url = f"https://discord.com/api/v10/channels/{id}"
    headers = {"Authorization": f"Bot {BOT_TOKEN}"}
    response = requests.delete(url, headers=headers)
    if response.status_code == 200:
        return response.json()
    else:
        return {"error": f"Failed to delete channel: {response.status_code}"}

@tool 
def create_channel(name: str, parent_id: str = "", position: int = 0) -> json:
    """Creates a text channel with the given name. Optionally set parent_id (category) and position. Returns the created channel or an error."""
    url = f"https://discord.com/api/v10/guilds/{GUILD_ID}/channels"
    headers = {"Authorization": f"Bot {BOT_TOKEN}"}
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
    headers = {"Authorization": f"Bot {BOT_TOKEN}"}
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
def create_category(name: str) -> json:
    """Creates a category channel with the given name. Categories group text/voice channels. Returns the created category or an error."""
    url = f"https://discord.com/api/v10/guilds/{GUILD_ID}/channels"
    headers = {"Authorization": f"Bot {BOT_TOKEN}"}
    data = {"name": name, "type": 4}
    response = requests.post(url, headers=headers, json=data)
    if response.status_code == 201:
        return response.json()
    else:
        return {"error": f"Failed to create channel: {response.status_code}"}
    
@dataclass
class ResponseFormat:
    completed_actions: list[str]
    final_summary: str


agent = create_agent(
    model="claude-sonnet-4-5-20250929",
    tools=[print_message, get_guild_channels, delete_channel, create_channel, modify_channel, create_category],
    system_prompt=SYSTEM_PROMPT,
    response_format= ToolStrategy(ResponseFormat)
)

# Run the agent
agent.invoke(
    {"messages": [{"role": "user", "content": "Dekete all channels. Then create an entrepreneurial hackathon server setup. Then after you finish that convert it to be an entrepreneurial group setup by renaming the channels with no deletions. Do all this while outputting updates to the console."}]}
)