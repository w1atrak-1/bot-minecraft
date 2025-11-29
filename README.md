# Minecraft Bot Spawner

This program generates multiple Minecraft bots with random credentials and connects them to a server using proxies.

## Features

- Generates random usernames (5-10 characters) and passwords (5-9 characters)
- Uses proxies from `active_proxies.txt` file
- Each proxy can handle up to 2 bots simultaneously
- Random credentials contain only alphanumeric characters (no special characters)

## Requirements

- Python 3.6+
- A list of active proxies in `active_proxies.txt`

## Setup

1. Install required dependencies:
   ```bash
   pip install -r requirements.txt
   ```

2. Create a file named `active_proxies.txt` with your active proxies (one per line).

3. Run the script:
   ```bash
   python minecraft_bot_spawner.py
   ```

## Proxy Format

The proxy file should contain proxies in one of these formats:
- `ip:port` (e.g., `127.0.0.1:8080`)
- `user:password@ip:port` (e.g., `myuser:mypass@127.0.0.1:8080`)

## Note

This is a basic implementation. To make actual Minecraft connections, you'll need to integrate with a Minecraft client library such as:

- `mcproto` (Python)
- `mineflayer` (Node.js - can be called from Python)
- Or other available Minecraft client libraries

The current implementation simulates the connection process. You'll need to add the actual Minecraft connection logic based on your preferred library.