# Minecraft Bot Launcher

This program creates Minecraft bots with random usernames and passwords, using proxies to connect to your server. Each bot has a unique username and password with no special characters.

## Features

- Generates random usernames (5-10 characters) and passwords (5-9 characters) without special characters
- Supports multiple proxies with up to 2 bots per proxy
- Checks server status before launching bots
- Provides detailed results of bot connections

## Requirements

- Python 3.7+
- Required packages: `quarry`, `mcstatus`, `PySocks`, `twisted`

## Installation

```bash
pip install quarry mcstatus PySocks twisted
```

## Usage

Run the program:

```bash
python minecraft_bot_launcher_final.py
```

Follow the prompts:
1. Enter your Minecraft server IP (with or without port)
2. Enter your proxy list (one per line, format: `ip:port` or `user:pass@ip:port`)
3. Enter the number of bots to launch

## Proxy Format

- Simple proxy: `127.0.0.1:8080`
- Authenticated proxy: `username:password@127.0.0.1:8080`

## Notes

- The program currently simulates connections. For actual Minecraft connections, additional proxy setup is required.
- This tool is intended for testing purposes only. Be responsible with its usage.
- Some Minecraft servers may have anti-bot measures that could prevent connections.