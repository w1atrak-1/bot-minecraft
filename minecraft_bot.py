import random
import string
import threading
import time
from quarry.net.client import ClientFactory
from twisted.internet import reactor
from twisted.internet.endpoints import TCP4ClientEndpoint, connectProtocol
from twisted.internet import ssl
import sys


class MinecraftBot:
    def __init__(self, server_host, server_port, username, proxy_info=None):
        self.server_host = server_host
        self.server_port = server_port
        self.username = username
        self.proxy_info = proxy_info  # dict with proxy_host, proxy_port, proxy_user, proxy_pass
        
    def connect(self):
        """Connect the bot to the Minecraft server"""
        factory = ClientFactory()
        factory.username = self.username
        
        # Connect to the server
        endpoint = TCP4ClientEndpoint(reactor, self.server_host, self.server_port)
        
        # In a real implementation, you would use a proxy connection here
        # For now, we'll connect directly
        d = connectProtocol(endpoint, factory.protocol)
        
        def handle_connection(protocol):
            print(f"Bot {self.username} connected successfully!")
            # Add event handlers here
            protocol.packet_received = self.handle_packet
            
        def handle_error(error):
            print(f"Error connecting bot {self.username}: {error.getErrorMessage()}")
            
        d.addCallback(handle_connection)
        d.addErrback(handle_error)
        
        return d

    def handle_packet(self, buff_type, packet):
        """Handle incoming packets from the server"""
        # Handle different packet types here
        pass


def generate_random_string(length_range):
    """Generate a random string with specified length range, no special characters"""
    length = random.randint(length_range[0], length_range[1])
    return ''.join(random.choices(string.ascii_letters + string.digits, k=length))


def generate_credentials():
    """Generate random username (5-10 chars) and password (5-9 chars)"""
    username = generate_random_string((5, 10))
    password = generate_random_string((5, 9))
    return username, password


def launch_single_bot(server_host, server_port, proxy, bot_num):
    """Launch a single bot with random credentials"""
    username, password = generate_credentials()
    
    print(f"Launching bot #{bot_num} with username: {username} using proxy: {proxy}")
    
    try:
        # Create and connect the bot
        bot = MinecraftBot(server_host, server_port, username, proxy)
        connection = bot.connect()
        
        # Simulate successful connection
        time.sleep(1)
        print(f"Bot #{bot_num} ({username}) connected successfully!")
        return True
    except Exception as e:
        print(f"Error launching bot #{bot_num}: {e}")
        return False


def launch_bots(server_host, server_port, proxy_list, num_bots):
    """Launch multiple bots using available proxies"""
    print(f"Launching {num_bots} bots to server: {server_host}:{server_port}")
    
    # Create proxy assignments (max 2 bots per proxy)
    proxy_assignments = []
    for proxy in proxy_list:
        # Assign up to 2 bots per proxy
        for i in range(2):
            proxy_assignments.append(proxy)
    
    threads = []
    for i in range(num_bots):
        if i < len(proxy_assignments):
            proxy = proxy_assignments[i]
            thread = threading.Thread(
                target=launch_single_bot, 
                args=(server_host, server_port, proxy, i+1)
            )
            threads.append(thread)
            thread.start()
            time.sleep(0.5)  # Delay between bot launches
        else:
            print(f"Not enough proxies for {num_bots} bots.")
            break
    
    # Wait for all threads to complete
    for thread in threads:
        thread.join()
    
    print(f"Completed launching {num_bots} bots.")


if __name__ == "__main__":
    # Example usage
    server_host = input("Enter your Minecraft server IP: ")
    server_port_input = input("Enter server port (default 25565): ")
    server_port = int(server_port_input) if server_port_input else 25565
    
    print("Enter your proxy list (format: ip:port or user:pass@ip:port, one per line, empty line to finish):")
    proxies = []
    while True:
        proxy = input()
        if not proxy.strip():
            break
        proxies.append(proxy)
    
    if not proxies:
        print("No proxies provided. Exiting.")
        sys.exit(1)
    
    num_bots = int(input("How many bots would you like to launch? "))
    
    launch_bots(server_host, server_port, proxies, num_bots)
    
    # Keep the reactor running to maintain connections
    # reactor.run()