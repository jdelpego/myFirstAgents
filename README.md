# Agent0

This is my first agent project, exploring AI agents using LangChain. It includes two basic agents: a simple general-purpose agent (Agent0) and a Discord channel management agent (discordManager).

## Features

### Agent0 (agent0.py)
A basic AI agent with the following tools:
- **get_weather(city)**: Returns a mock weather response for any city.
- **print_message(message)**: Prints a message to the console.

Example usage: Ask the agent to print the weather in a city.

### Discord Manager (discordManager.py)
An AI agent for managing Discord server channels with these tools:
- **print_message(message)**: Prints messages to the console for feedback.
- **get_guild_channels()**: Retrieves all channels in the guild.
- **delete_channel(id)**: Deletes a channel by its ID (requires MANAGE_CHANNELS permission).
- **create_channel(name, parent_id="", position=0)**: Creates a text channel with optional category and position.
- **modify_channel(channel_id, name=None, parent_id=None, position=None)**: Modifies channel properties.
- **create_category(name)**: Creates a category channel.

Example usage: Organize a Discord server by deleting channels and creating new categories and channels.

## Setup

1. Clone this repository.
2. Install dependencies:
   ```
   pip install langchain requests
   ```
3. Set your Anthropic API key (required for the agents to work):
   ```
   export ANTHROPIC_API_KEY=your_api_key_here
   ```
4. For discordManager.py:
   - Set your Discord bot token in the `BOT_TOKEN` variable.
   - Set your guild ID in the `GUILD_ID` variable.
   - Ensure your bot has the necessary permissions (MANAGE_CHANNELS, etc.).

## Running

- Run Agent0: `python agent0.py`
- Run Discord Manager: `python discordManager.py`

## Notes

- This is a learning project, so code may not be production-ready.
- Be cautious with Discord API calls, especially deletions.
- Requires a valid Discord bot token for discordManager.

## License

MIT License