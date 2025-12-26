# Agent0

This is my first agent project, exploring AI agents using LangChain. It includes two basic agents: a simple general-purpose agent (first_agent) and a Discord channel management agent (discord_v1).

## Features

### First Agent (first_agent.py)
A basic AI agent with the following tools:
- **get_weather(city)**: Returns a mock weather response for any city.
- **print_message(message)**: Prints a message to the console.

Example usage: Ask the agent to print the weather in a city.

### Discord Manager (discord_v1.py)
An AI agent for managing Discord server channels with these tools:
- **get_guild_channels()**: Retrieves all channels in the guild.
- **create_channel(name, parent_id="", position=0)**: Creates a text channel with optional category and position.
- **modify_channel(channel_id, name=None, parent_id=None, position=None)**: Modifies channel properties.
- **create_category(name, position=0)**: Creates a category channel.
- **create_forum(name, position=0)**: Creates a forum channel.
- **create_public_thread(parent_id, name, position=0)**: Creates a public thread in a channel.
- **read_channel_messages(channel_id, limit=10)**: Retrieves recent messages from a channel.

Example usage: Restructure a Discord server into a travel group by renaming and organizing channels.

## Setup

1. Clone this repository.
2. Install dependencies:
   ```
   pip install langchain langchain-xai requests python-dotenv
   ```
3. Set API keys:
   - For first_agent: `export ANTHROPIC_API_KEY=your_anthropic_api_key`
   - For discord_v1: `export XAI_API_KEY=your_xai_api_key`
4. For discord_v1.py:
   - Set your Discord bot token in the `DISCORD_BOT_TOKEN` environment variable (via .env or export).
   - Set your guild ID in the `DISCORD_GUILD_ID` environment variable.
   - Ensure your bot has the necessary permissions (MANAGE_CHANNELS, VIEW_CHANNEL, READ_MESSAGE_HISTORY, etc.).

## Running

- Run First Agent: `python first_agent.py`
- Run Discord Manager: `python discord_v1.py`

## Notes

- This is a learning project, so code may not be production-ready.
- Be cautious with Discord API calls, especially deletions.
- Requires a valid Discord bot token for discord_v1.

## License

MIT License