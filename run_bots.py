#!/usr/bin/env python3
"""
Script to run the Minecraft bot spawner with a predefined number of bots
"""

from minecraft_bot_spawner import MinecraftBotSpawner
import sys

def run_with_bot_count(num_bots):
    """Run the bot spawner with a specific number of bots"""
    spawner = MinecraftBotSpawner()
    spawner.spawn_bots(num_bots)

if __name__ == "__main__":
    # Default to 5 bots if no argument provided
    num_bots = 5
    if len(sys.argv) > 1:
        try:
            num_bots = int(sys.argv[1])
        except ValueError:
            print("Please provide a valid number for the number of bots.")
            sys.exit(1)
    
    print(f"Starting Minecraft Bot Spawner with {num_bots} bots...")
    run_with_bot_count(num_bots)