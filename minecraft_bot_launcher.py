import random
import string
import threading
import time
import sys
import json
from typing import List, Dict, Tuple, Optional

class MinecraftBotLauncher:
    def __init__(self):
        self.proxies = []
        self.bots = []
        self.server_ip = ""
        self.server_port = 25565
        self.num_bots = 0
        
    def generate_random_string(self, min_length: int, max_length: int, include_special: bool = False) -> str:
        """Generate random string with specified length constraints"""
        length = random.randint(min_length, max_length)
        if include_special:
            chars = string.ascii_letters + string.digits + "!@#$%^&*"
        else:
            chars = string.ascii_letters + string.digits
        return ''.join(random.choice(chars) for _ in range(length))
    
    def generate_credentials(self) -> Tuple[str, str]:
        """Generate random username (5-10 chars) and password (5-9 chars) without special chars"""
        username = self.generate_random_string(5, 10, include_special=False)
        password = self.generate_random_string(5, 9, include_special=False)
        return username, password
    
    def parse_proxy(self, proxy_str: str) -> Dict[str, str]:
        """Parse proxy string in format ip:port or user:pass@ip:port"""
        proxy_info = {}
        
        if '@' in proxy_str:
            auth, addr = proxy_str.split('@', 1)
            user, pwd = auth.split(':', 1)
            ip, port = addr.split(':', 1)
            proxy_info['username'] = user
            proxy_info['password'] = pwd
        else:
            ip, port = proxy_str.split(':', 1)
        
        proxy_info['ip'] = ip
        proxy_info['port'] = int(port)
        return proxy_info
    
    def validate_proxy_format(self, proxy_str: str) -> bool:
        """Validate proxy format"""
        try:
            if '@' in proxy_str:
                auth, addr = proxy_str.split('@', 1)
                user, pwd = auth.split(':', 1)
                ip, port = addr.split(':', 1)
                int(port)  # Check if port is a number
                return True
            else:
                ip, port = proxy_str.split(':', 1)
                int(port)  # Check if port is a number
                return True
        except:
            return False
    
    def launch_bot(self, proxy_info: Dict[str, str], username: str, password: str) -> Dict[str, any]:
        """Launch a single bot with proxy and credentials"""
        try:
            # Simulate Minecraft bot connection
            print(f"Bot {username} connecting through proxy {proxy_info['ip']}:{proxy_info['port']}...")
            
            # Simulate connection process (in real implementation, connect to Minecraft server)
            time.sleep(1)  # Simulate connection delay
            
            # Simulate connection success
            return {
                'status': 'success',
                'username': username,
                'password': password,
                'proxy': f"{proxy_info['ip']}:{proxy_info['port']}",
                'message': f'Bot {username} connected successfully through proxy'
            }
        except Exception as e:
            return {
                'status': 'error',
                'username': username,
                'password': password,
                'proxy': f"{proxy_info['ip']}:{proxy_info['port']}",
                'error': str(e),
                'message': f'Bot {username} failed to connect: {str(e)}'
            }
    
    def load_proxies_from_file(self, filename: str) -> List[str]:
        """Load proxies from a text file"""
        try:
            with open(filename, 'r') as f:
                proxies = [line.strip() for line in f if line.strip() and not line.startswith('#')]
            return proxies
        except FileNotFoundError:
            print(f"Proxy file {filename} not found!")
            return []
    
    def launch_all_bots(self) -> List[Dict[str, any]]:
        """Launch all bots with proper proxy distribution"""
        results = []
        
        # Parse all proxies
        parsed_proxies = []
        for proxy_str in self.proxies:
            if self.validate_proxy_format(proxy_str):
                parsed_proxies.append(self.parse_proxy(proxy_str))
            else:
                print(f"Invalid proxy format: {proxy_str}")
        
        if not parsed_proxies:
            print("No valid proxies found!")
            return results
        
        # Launch bots with max 2 bots per proxy
        for i in range(self.num_bots):
            username, password = self.generate_credentials()
            
            # Assign proxy (max 2 bots per proxy)
            proxy_idx = (i // 2) % len(parsed_proxies)  # Rotate proxies, max 2 bots per proxy
            proxy_info = parsed_proxies[proxy_idx]
            
            result = self.launch_bot(proxy_info, username, password)
            results.append(result)
            
            print(f"Launched bot {i+1}/{self.num_bots}: {username} via {proxy_info['ip']}:{proxy_info['port']}")
            time.sleep(0.5)  # Small delay between bot launches
        
        return results

def main():
    launcher = MinecraftBotLauncher()
    
    print("Minecraft Bot Launcher")
    print("=" * 30)
    
    # Get server information
    server_input = input("Enter Minecraft server IP: ")
    if ':' in server_input:
        server_ip, port_str = server_input.split(':')
        server_port = int(port_str)
    else:
        server_ip = server_input
        server_port = 25565  # Default Minecraft port
    
    launcher.server_ip = server_ip
    launcher.server_port = server_port
    
    # Get proxy information
    print("\nProxy input options:")
    print("1. Enter proxies directly (one per line, empty line to finish)")
    print("2. Load from file")
    
    proxy_choice = input("Choose option (1 or 2): ").strip()
    
    if proxy_choice == '1':
        print("Enter proxies in format 'ip:port' or 'user:pass@ip:port' (one per line, empty line to finish):")
        proxies = []
        while True:
            proxy = input().strip()
            if not proxy:
                break
            proxies.append(proxy)
        launcher.proxies = proxies
    elif proxy_choice == '2':
        proxy_file = input("Enter proxy file path: ").strip()
        launcher.proxies = launcher.load_proxies_from_file(proxy_file)
    else:
        print("Invalid choice!")
        return
    
    if not launcher.proxies:
        print("No proxies provided!")
        return
    
    # Get number of bots
    try:
        num_bots = int(input(f"\nEnter number of bots to launch (max {len(launcher.proxies) * 2}): "))
        if num_bots <= 0:
            print("Number of bots must be positive!")
            return
        if num_bots > len(launcher.proxies) * 2:
            print(f"Warning: You have {len(launcher.proxies)} proxies which support max {len(launcher.proxies) * 2} bots.")
            confirm = input(f"Do you want to proceed with {num_bots} bots? (y/n): ")
            if confirm.lower() != 'y':
                return
        launcher.num_bots = num_bots
    except ValueError:
        print("Invalid number!")
        return
    
    # Launch bots
    print(f"\nStarting {launcher.num_bots} bots with random credentials...")
    print("Proxies will be shared (max 2 bots per proxy)")
    
    try:
        results = launcher.launch_all_bots()
        
        # Print results
        print("\n" + "="*50)
        print("LAUNCH RESULTS")
        print("="*50)
        
        success_count = 0
        error_count = 0
        
        for result in results:
            if result['status'] == 'success':
                print(f"✅ {result['message']}")
                success_count += 1
            else:
                print(f"❌ {result['message']}")
                error_count += 1
        
        print(f"\nSummary: {success_count} successful, {error_count} failed")
        
        # Print credentials summary
        print("\nBot Credentials Summary:")
        print("-" * 30)
        for i, result in enumerate(results):
            print(f"Bot {i+1}: Username={result['username']}, Password={result['password']}, Proxy={result['proxy']}")

    except KeyboardInterrupt:
        print("\nOperation cancelled by user.")
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    main()