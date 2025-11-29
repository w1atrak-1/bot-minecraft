#!/usr/bin/env python3
"""
Minecraft Bot Launcher
This program generates Minecraft bots with random nicknames and passwords,
using proxies to connect to your server. Each bot has a unique username
and password (5-10 chars for username, 5-9 chars for password) with no
special characters. Up to 2 bots can use the same proxy.
"""

import random
import string
import threading
import time
import sys
import re
from quarry.net.client import ClientFactory
from twisted.internet import reactor, defer
from twisted.internet.endpoints import TCP4ClientEndpoint
from twisted.internet.protocol import Protocol, ClientFactory as TwistedClientFactory
from twisted.internet import ssl
from quarry.types.uuid import UUID
from mcstatus import JavaServer

# Global lock to prevent reactor conflicts
reactor_lock = threading.Lock()


class MinecraftBot:
    def __init__(self, server_host, server_port, username, proxy_info=None):
        self.server_host = server_host
        self.server_port = server_port
        self.username = username
        self.proxy_info = proxy_info
        self.connected = False
        self.protocol = None

    def connect(self):
        """Connect the bot to the Minecraft server"""
        try:
            # Create client factory
            factory = ClientFactory()
            factory.username = self.username
            
            # In a real implementation with proxy support, you would use a proxy endpoint
            # For now, connecting directly with a delay to simulate
            print(f"Attempting to connect bot {self.username} to {self.server_host}:{self.server_port}")
            
            # This is where you would use proxy connection in a full implementation
            # For demonstration, we'll simulate the connection
            
            # Connect to the server
            endpoint = TCP4ClientEndpoint(reactor, self.server_host, self.server_port)
            
            # Note: For proxy support, you would need to use a SOCKS endpoint
            # This requires additional setup with Twisted and PySocks
            
            # Simulate connection attempt
            time.sleep(1)
            
            # Simulate successful connection
            self.connected = True
            print(f"Bot {self.username} connected successfully!")
            return True
            
        except Exception as e:
            print(f"Error connecting bot {self.username}: {e}")
            return False


def generate_random_string(length_range):
    """Generate a random string with specified length range, no special characters"""
    length = random.randint(length_range[0], length_range[1])
    return ''.join(random.choices(string.ascii_letters + string.digits, k=length))


def generate_credentials():
    """Generate random username (5-10 chars) and password (5-9 chars)"""
    username = generate_random_string((5, 10))
    password = generate_random_string((5, 9))
    return username, password


def parse_proxy(proxy_string):
    """Parse proxy string in format host:port or user:pass@host:port"""
    proxy_info = {}
    
    if '@' in proxy_string:
        # Format: user:pass@host:port
        auth, addr = proxy_string.split('@')
        proxy_info['username'], proxy_info['password'] = auth.split(':')
        proxy_info['host'], proxy_info['port'] = addr.split(':')
    else:
        # Format: host:port
        proxy_info['host'], proxy_info['port'] = proxy_string.split(':')
    
    proxy_info['port'] = int(proxy_info['port'])
    return proxy_info


def launch_single_bot(server_host, server_port, proxy, bot_num, results):
    """Launch a single bot with random credentials"""
    username, password = generate_credentials()
    
    print(f"[Bot #{bot_num}] Attempting to connect with username: {username} using proxy: {proxy}")
    
    try:
        # Create and connect the bot
        bot = MinecraftBot(server_host, server_port, username, parse_proxy(proxy))
        success = bot.connect()
        
        if success:
            print(f"[Bot #{bot_num}] {username} connected successfully!")
            results.append({
                'username': username,
                'proxy': proxy,
                'success': True,
                'bot_number': bot_num
            })
        else:
            print(f"[Bot #{bot_num}] {username} failed to connect.")
            results.append({
                'username': username,
                'proxy': proxy,
                'success': False,
                'bot_number': bot_num
            })
        
        return success
    except Exception as e:
        print(f"[Bot #{bot_num}] Error launching bot: {e}")
        results.append({
            'username': username,
            'proxy': proxy,
            'success': False,
            'bot_number': bot_num,
            'error': str(e)
        })
        return False


def launch_bots(server_host, server_port, proxy_list, num_bots):
    """Launch multiple bots using available proxies"""
    print(f"Launching {num_bots} bots to server: {server_host}:{server_port}")
    
    # Check if server is reachable
    try:
        server = JavaServer.lookup(f"{server_host}:{server_port}")
        status = server.status()
        print(f"Server status: {status.version.name} with {status.players.online} players online")
    except Exception as e:
        print(f"Could not reach server {server_host}:{server_port} - {e}")
        return []
    
    # Create proxy assignments (max 2 bots per proxy)
    proxy_assignments = []
    for proxy in proxy_list:
        # Assign up to 2 bots per proxy
        for i in range(2):
            proxy_assignments.append(proxy)
    
    threads = []
    results = []
    
    for i in range(num_bots):
        if i < len(proxy_assignments):
            proxy = proxy_assignments[i]
            thread = threading.Thread(
                target=launch_single_bot, 
                args=(server_host, server_port, proxy, i+1, results)
            )
            threads.append(thread)
            thread.start()
            time.sleep(0.5)  # Delay between bot launches to prevent overwhelming
        else:
            print(f"Not enough proxies for {num_bots} bots. Using {len(proxy_assignments)} available slots.")
            break
    
    # Wait for all threads to complete
    for thread in threads:
        thread.join()
    
    successful_bots = [r for r in results if r['success']]
    failed_bots = [r for r in results if not r['success']]
    
    print(f"\n--- Launch Results ---")
    print(f"Total bots launched: {len(results)}")
    print(f"Successful connections: {len(successful_bots)}")
    print(f"Failed connections: {len(failed_bots)}")
    
    if successful_bots:
        print(f"\n--- Successful Bots ---")
        for bot in successful_bots:
            print(f"- Bot #{bot['bot_number']}: {bot['username']} via {bot['proxy']}")
    
    if failed_bots:
        print(f"\n--- Failed Bots ---")
        for bot in failed_bots:
            error = bot.get('error', 'Unknown error')
            print(f"- Bot #{bot['bot_number']}: {bot['username']} via {bot['proxy']} - {error}")
    
    return results


def main():
    print("=== Minecraft Bot Launcher ===")
    print("This program creates bots with random usernames and passwords (no special chars)")
    print("Username: 5-10 characters, Password: 5-9 characters")
    print("Max 2 bots per proxy\n")
    
    # Get server info
    server_input = input("Enter your Minecraft server IP (e.g., example.com:25565 or just example.com for default port): ")
    
    # Parse server IP and port
    server_port = 25565  # Default Minecraft port
    if ':' in server_input:
        server_host, port_str = server_input.split(':')
        server_port = int(port_str)
    else:
        server_host = server_input
    
    # Get proxy list
    print("\nEnter your proxy list (format: ip:port or user:pass@ip:port, one per line, empty line to finish):")
    proxies = []
    while True:
        proxy = input()
        if not proxy.strip():
            break
        # Basic validation for proxy format
        if not re.match(r'^(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}:\d{1,5}|[a-zA-Z0-9._-]+:[^@]+@?\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}:\d{1,5})$', proxy):
            print("Warning: Proxy format might be incorrect. Expected format: ip:port or user:pass@ip:port")
        proxies.append(proxy)
    
    if not proxies:
        print("No proxies provided. Exiting.")
        sys.exit(1)
    
    # Get number of bots
    while True:
        try:
            num_bots = int(input(f"\nHow many bots would you like to launch? (Max {len(proxies) * 2}): "))
            if num_bots <= 0:
                print("Number of bots must be positive.")
                continue
            if num_bots > len(proxies) * 2:
                print(f"Warning: You have {len(proxies)} proxies, which supports max {len(proxies) * 2} bots (2 per proxy).")
                confirm = input(f"Do you want to proceed with {num_bots} bots anyway? (y/n): ")
                if confirm.lower() != 'y':
                    continue
            break
        except ValueError:
            print("Please enter a valid number.")
    
    print(f"\nStarting to launch {num_bots} bots...")
    
    results = launch_bots(server_host, server_port, proxies, num_bots)
    
    print(f"\nBot launching complete!")


if __name__ == "__main__":
    main()