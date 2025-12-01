import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox
import requests
import threading
import json

class RobloxExecutorGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Roblox Executor with GUI")
        self.root.geometry("800x600")
        
        # Configure styles
        self.style = ttk.Style()
        self.style.configure("TFrame", background="#f0f0f0")
        self.style.configure("TLabel", background="#f0f0f0", font=("Arial", 10))
        self.style.configure("TButton", font=("Arial", 10))
        self.style.configure("TEntry", font=("Arial", 10))
        
        # Variables
        self.cookie_var = tk.StringVar()
        self.place_id_var = tk.StringVar()
        self.script_var = tk.StringVar()
        
        self.setup_ui()
        
    def setup_ui(self):
        # Main frame
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Title
        title_label = ttk.Label(main_frame, text="Roblox Executor", font=("Arial", 16, "bold"))
        title_label.grid(row=0, column=0, columnspan=2, pady=(0, 20))
        
        # Cookie input
        ttk.Label(main_frame, text="ROBLOSECURITY Cookie:").grid(row=1, column=0, sticky=tk.W, pady=5)
        cookie_entry = ttk.Entry(main_frame, textvariable=self.cookie_var, width=70, show="*")
        cookie_entry.grid(row=1, column=1, sticky=(tk.W, tk.E), pady=5, padx=(10, 0))
        
        # Place ID input
        ttk.Label(main_frame, text="Place ID:").grid(row=2, column=0, sticky=tk.W, pady=5)
        place_id_entry = ttk.Entry(main_frame, textvariable=self.place_id_var, width=70)
        place_id_entry.grid(row=2, column=1, sticky=(tk.W, tk.E), pady=5, padx=(10, 0))
        
        # Script input (text area)
        ttk.Label(main_frame, text="Lua Script:").grid(row=3, column=0, sticky=(tk.W, tk.N), pady=5)
        self.script_text = scrolledtext.ScrolledText(main_frame, width=60, height=15, wrap=tk.WORD)
        self.script_text.grid(row=3, column=1, sticky=(tk.W, tk.E, tk.N, tk.S), pady=5, padx=(10, 0))
        
        # Buttons frame
        button_frame = ttk.Frame(main_frame)
        button_frame.grid(row=4, column=0, columnspan=2, pady=20)
        
        # Execute button
        execute_btn = ttk.Button(button_frame, text="Execute Script", command=self.execute_script_threaded)
        execute_btn.grid(row=0, column=0, padx=(0, 10))
        
        # Clear button
        clear_btn = ttk.Button(button_frame, text="Clear", command=self.clear_fields)
        clear_btn.grid(row=0, column=1, padx=(0, 10))
        
        # Load example script button
        example_btn = ttk.Button(button_frame, text="Load Example", command=self.load_example_script)
        example_btn.grid(row=0, column=2)
        
        # Status and output area
        ttk.Label(main_frame, text="Output:").grid(row=5, column=0, sticky=(tk.W, tk.N), pady=(10, 0))
        self.output_text = scrolledtext.ScrolledText(main_frame, width=60, height=10, wrap=tk.WORD, state=tk.DISABLED)
        self.output_text.grid(row=5, column=1, sticky=(tk.W, tk.E, tk.N, tk.S), pady=(10, 0), padx=(10, 0))
        
        # Configure grid weights for resizing
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(1, weight=1)
        main_frame.rowconfigure(3, weight=1)
        main_frame.rowconfigure(5, weight=1)
        
    def execute_script_threaded(self):
        # Run execution in a separate thread to prevent GUI freezing
        thread = threading.Thread(target=self.execute_script)
        thread.daemon = True
        thread.start()
        
    def execute_script(self):
        cookie = self.cookie_var.get()
        place_id = self.place_id_var.get()
        script = self.script_text.get("1.0", tk.END).strip()
        
        if not cookie:
            self.update_output("Error: Please enter your .ROBLOSECURITY cookie")
            return
            
        if not place_id:
            self.update_output("Error: Please enter a Place ID")
            return
            
        if not script:
            self.update_output("Error: Please enter a Lua script to execute")
            return
            
        try:
            # Validate place_id is numeric
            int(place_id)
        except ValueError:
            self.update_output("Error: Place ID must be a number")
            return
        
        self.update_output("Initializing executor...")
        
        # Create executor instance
        executor = RobloxExecutor(cookie)
        
        # Authenticate
        user_info = executor.get_user_info()
        if not user_info:
            self.update_output("Failed to authenticate with the provided cookie")
            return
            
        self.update_output(f"Authenticated as: {user_info.get('name', 'Unknown')}")
        
        # Execute script
        self.update_output("Sending script to Roblox...")
        success = executor.execute_script(script, place_id)
        
        if success:
            self.update_output("Script executed successfully!")
        else:
            self.update_output("Failed to execute script")
    
    def update_output(self, message):
        # Thread-safe output update
        def update():
            self.output_text.config(state=tk.NORMAL)
            self.output_text.insert(tk.END, message + "\n")
            self.output_text.see(tk.END)
            self.output_text.config(state=tk.DISABLED)
            
        self.root.after(0, update)  # Schedule update on main thread
    
    def clear_fields(self):
        self.cookie_var.set("")
        self.place_id_var.set("")
        self.script_text.delete("1.0", tk.END)
        self.output_text.config(state=tk.NORMAL)
        self.output_text.delete("1.0", tk.END)
        self.output_text.config(state=tk.DISABLED)
    
    def load_example_script(self):
        example_script = """-- Roblox Executor Example Script
-- This script will print a message to the output

print("Hello from Roblox Executor!")

-- You can also execute other Lua commands
local Players = game:GetService("Players")
local player = Players.LocalPlayer
if player then
    print("Player name: " .. player.Name)
end
"""
        self.script_text.delete("1.0", tk.END)
        self.script_text.insert("1.0", example_script)

class RobloxExecutor:
    def __init__(self, cookie):
        self.cookie = cookie
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
            'Cookie': f'.ROBLOSECURITY={cookie}',
            'Content-Type': 'application/json',
            'Referer': 'https://www.roblox.com/'
        })
        
    def get_xcsrf_token(self):
        """Get X-CSRF-TOKEN for API requests"""
        try:
            response = self.session.post('https://auth.roblox.com/v2/logout')
            if response.status_code == 403:
                xcsrf_token = response.headers.get('X-CSRF-TOKEN')
                if xcsrf_token:
                    self.session.headers['X-CSRF-TOKEN'] = xcsrf_token
                    return xcsrf_token
            return None
        except Exception as e:
            print(f"Error getting X-CSRF-TOKEN: {e}")
            return None

    def execute_script(self, script, place_id):
        """Execute Lua script in a Roblox game"""
        if not self.get_xcsrf_token():
            print("Failed to get X-CSRF-TOKEN")
            return False
            
        url = f"https://apis.roblox.com/automation-script-service/v1/toolboxes/roblox-player-scripts"
        
        payload = {
            "script": script,
            "placeId": place_id
        }
        
        try:
            response = self.session.post(url, json=payload)
            if response.status_code == 200:
                print("Script executed successfully!")
                return True
            else:
                print(f"Script execution failed: {response.status_code} - {response.text}")
                return False
        except Exception as e:
            print(f"Error executing script: {e}")
            return False

    def get_user_info(self):
        """Get user information using the cookie"""
        try:
            response = self.session.get('https://users.roblox.com/v1/users/authenticated')
            if response.status_code == 200:
                user_data = response.json()
                return user_data
            else:
                print(f"Failed to get user info: {response.status_code}")
                return None
        except Exception as e:
            print(f"Error getting user info: {e}")
            return None

def main():
    root = tk.Tk()
    app = RobloxExecutorGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()