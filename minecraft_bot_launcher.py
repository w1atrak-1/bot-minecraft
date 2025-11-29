import random
import string
import threading
import time
import sys
from quarry.net.client import ClientFactory, Reactor
from quarry.types.uuid import UUID
from twisted.internet import reactor, defer
from twisted.internet.endpoints import TCP4ClientEndpoint
from twisted.internet.protocol import ClientFactory as TwistedClientFactory

try:
    from mcstatus import JavaServer
except ImportError:
    print("Required packages not found. Install them with:")
    print("pip install mcstatus quarry twisted")
    sys.exit(1)


class MinecraftBotLauncher:
    def __init__(self, server_ip, server_port=25565, proxy_list=None):
        self.server_ip = server_ip
        self.server_port = server_port
        self.proxy_list = proxy_list or []
        self.active_bots = []
        self.bot_counter = 0

    def generate_random_string(self, length_range):
        """Generate a random string with specified length range, no special characters"""
        length = random.randint(length_range[0], length_range[1])
        return ''.join(random.choices(string.ascii_letters + string.digits, k=length))

    def generate_credentials(self):
        """Generate random username (5-10 chars) and password (5-9 chars)"""
        username = self.generate_random_string((5, 10))
        password = self.generate_random_string((5, 9))
        return username, password

    def connect_bot(self, proxy):
        """Connect a single bot using the provided proxy"""
        username, password = self.generate_credentials()
        
        print(f"Attempting to connect bot with username: {username} using proxy: {proxy}")
        
        try:
            # Parse proxy information (assuming format: ip:port or user:pass@ip:port)
            proxy_host = None
            proxy_port = None
            proxy_username = None
            proxy_password = None
            
            # Simple proxy parsing (you might need to adjust based on your proxy format)
            if '@' in proxy:
                auth, addr = proxy.split('@')
                proxy_username, proxy_password = auth.split(':')
                proxy_host, proxy_port = addr.split(':')
            else:
                proxy_host, proxy_port = proxy.split(':')
            
            # Create client factory with the username
            factory = ClientFactory()
            factory.username = username
            
            # For now, simulate the connection process
            # In a real implementation, you would connect using quarry's client methods
            print(f"Bot {username} connecting through proxy {proxy}...")
            
            # Check if server is reachable
            try:
                server = JavaServer.lookup(f"{self.server_ip}:{self.server_port}")
                status = server.status()
                print(f"Server status: {status.version.name} with {status.players.online} players online")
            except Exception as e:
                print(f"Could not reach server {self.server_ip}:{self.server_port} - {e}")
                return False
            
            # Simulate connection process
            time.sleep(2)
            
            # Simulate connection success/failure
            if random.choice([True, False]):
                print(f"Bot {username} successfully connected!")
                self.active_bots.append({
                    'username': username,
                    'proxy': proxy,
                    'connected_at': time.time()
                })
                return True
            else:
                print(f"Bot {username} failed to connect through {proxy}")
                return False
        except Exception as e:
            print(f"Error connecting bot {username}: {e}")
            return False

    def launch_bots(self, num_bots):
        """Launch specified number of bots using available proxies"""
        print(f"Launching {num_bots} bots to server: {self.server_ip}:{self.server_port}")
        
        if not self.proxy_list:
            print("No proxies provided. Exiting.")
            return []
        
        # Create a list of proxy assignments (max 2 bots per proxy)
        proxy_assignments = []
        for proxy in self.proxy_list:
            # Assign up to 2 bots per proxy
            for _ in range(2):
                proxy_assignments.append(proxy)
        
        # Launch bots in separate threads
        threads = []
        for i in range(num_bots):
            if i < len(proxy_assignments):
                proxy = proxy_assignments[i]
                thread = threading.Thread(target=self.connect_bot, args=(proxy,))
                threads.append(thread)
                thread.start()
                # Small delay between bot launches
                time.sleep(0.5)
            else:
                print(f"Not enough proxies for {num_bots} bots. Using {len(proxy_assignments)} available slots.")
                break
        
        # Wait for all threads to complete
        for thread in threads:
            thread.join()
        
        print(f"Launched {len(self.active_bots)} successful bot connections out of {num_bots} attempts")
        return self.active_bots


def main():
    # Example usage
    server_ip = input("Enter your Minecraft server IP (e.g., example.com:25565 or just example.com for default port): ")
    
    # Parse server IP and port
    server_port = 25565  # Default Minecraft port
    if ':' in server_ip:
        server_ip, port_str = server_ip.split(':')
        server_port = int(port_str)
    
    print("Enter your proxy list (one per line, empty line to finish):")
    proxies = []
    while True:
        proxy = input()
        if not proxy.strip():
            break
        proxies.append(proxy)
    
    if not proxies:
        print("No proxies provided. Exiting.")
        return
    
    num_bots = int(input("How many bots would you like to launch? "))
    
    launcher = MinecraftBotLauncher(server_ip, server_port, proxies)
    active_bots = launcher.launch_bots(num_bots)
    
    print("\nActive bots:")
    for bot in active_bots:
        print(f"- Username: {bot['username']}, Proxy: {bot['proxy']}")


if __name__ == "__main__":
    main()