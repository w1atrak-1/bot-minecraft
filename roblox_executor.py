import requests
import time
import json

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
    print("=== Roblox Executor ===")
    
    cookie = input("Enter your .ROBLOSECURITY cookie: ")
    
    executor = RobloxExecutor(cookie)
    
    user_info = executor.get_user_info()
    if user_info:
        print(f"Logged in as: {user_info.get('name', 'Unknown')}")
    else:
        print("Failed to authenticate with the provided cookie")
        return
    
    while True:
        print("\nOptions:")
        print("1. Execute script")
        print("2. Exit")
        
        choice = input("Select option (1-2): ")
        
        if choice == '1':
            script = input("Enter Lua script to execute: ")
            place_id = input("Enter Place ID: ")
            
            success = executor.execute_script(script, place_id)
            if success:
                print("Script sent successfully!")
            else:
                print("Failed to execute script")
                
        elif choice == '2':
            print("Exiting...")
            break
        else:
            print("Invalid option")

if __name__ == "__main__":
    main()