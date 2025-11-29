import random
import string
import time
import threading
from typing import List, Tuple
import requests
import json

class MinecraftBotSpawner:
    def __init__(self, proxy_file: str = "active_proxies.txt"):
        self.proxy_file = proxy_file
        self.proxies = self.load_proxies()
        self.active_bots = []
        
    def load_proxies(self) -> List[str]:
        """Load proxy list from file"""
        try:
            with open(self.proxy_file, 'r') as f:
                proxies = [line.strip() for line in f if line.strip()]
            return proxies
        except FileNotFoundError:
            print(f"Proxy file {self.proxy_file} not found!")
            return []
    
    def generate_random_string(self, min_length: int, max_length: int, include_uppercase: bool = True) -> str:
        """Generate a random string with specified length range"""
        length = random.randint(min_length, max_length)
        chars = string.ascii_lowercase + string.digits
        if include_uppercase:
            chars += string.ascii_uppercase
        return ''.join(random.choice(chars) for _ in range(length))
    
    def generate_credentials(self) -> Tuple[str, str]:
        """Generate random username and password"""
        username = self.generate_random_string(5, 10, include_uppercase=True)
        password = self.generate_random_string(5, 9, include_uppercase=True)
        return username, password
    
    def connect_bot(self, proxy: str, username: str, password: str, bot_id: int):
        """Simulate connecting a bot to Minecraft server"""
        print(f"Bot {bot_id}: Connecting with username '{username}' and password '{password}' via proxy '{proxy}'")
        
        # Here you would add the actual Minecraft connection logic
        # For now, we'll simulate the connection
        try:
            # Parse proxy string (assuming format: ip:port or user:pass@ip:port)
            proxy_dict = {}
            if '@' in proxy:
                auth, addr = proxy.split('@')
                user, pwd = auth.split(':')
                proxy_dict = {
                    'http': f'http://{user}:{pwd}@{addr}',
                    'https': f'http://{user}:{pwd}@{addr}'
                }
            else:
                proxy_dict = {
                    'http': f'http://{proxy}',
                    'https': f'https://{proxy}'
                }
            
            # This is a placeholder - in a real implementation you would use a Minecraft client library
            # For example: mineflayer, mcproto, or similar
            print(f"Bot {bot_id}: Successfully connected to server!")
            self.active_bots.append((username, bot_id))
            
            # Keep the bot alive for some time (simulated)
            time.sleep(30)  # Simulate bot being active for 30 seconds
            
        except Exception as e:
            print(f"Bot {bot_id}: Failed to connect - {e}")
    
    def spawn_bots(self, num_bots: int):
        """Spawn multiple bots using available proxies"""
        if not self.proxies:
            print("No proxies available!")
            return
        
        print(f"Starting {num_bots} bots with {len(self.proxies)} available proxies...")
        
        # Each proxy can handle 2 bots, so calculate how many proxies we need
        required_proxies = (num_bots + 1) // 2  # Ceiling division
        available_proxies = self.proxies * 2  # Each proxy can be used twice
        
        threads = []
        for i in range(num_bots):
            proxy = available_proxies[i % len(available_proxies)]
            username, password = self.generate_credentials()
            
            # Create a thread for each bot
            bot_thread = threading.Thread(
                target=self.connect_bot,
                args=(proxy, username, password, i+1)
            )
            threads.append(bot_thread)
            bot_thread.start()
            
            # Small delay between bot connections
            time.sleep(1)
        
        # Wait for all threads to complete
        for thread in threads:
            thread.join()
        
        print(f"All {num_bots} bots have finished their session.")


def main():
    spawner = MinecraftBotSpawner()
    
    # Get number of bots from user
    try:
        num_bots = int(input("How many bots would you like to spawn? "))
        if num_bots <= 0:
            print("Number of bots must be positive!")
            return
    except ValueError:
        print("Please enter a valid number!")
        return
    
    spawner.spawn_bots(num_bots)


if __name__ == "__main__":
    main()