# Roblox Executor

This project contains a Roblox executor that allows you to execute Lua scripts in Roblox games using the Roblox API.

## Files

- `roblox_executor.py` - Console-based Roblox executor
- `roblox_executor_gui.py` - GUI-based Roblox executor (using tkinter)
- `launch_executor.py` - Launcher to choose between GUI and console versions

## Requirements

- Python 3.x
- requests library
- tkinter (for GUI version)

## Installation

1. Install the required dependencies:
```bash
pip install -r requirements.txt
```

2. For the GUI version, ensure tkinter is available:
```bash
# On Debian/Ubuntu systems:
sudo apt-get install python3-tk
```

## How to Use

### Console Version

1. Run the console executor:
```bash
python roblox_executor.py
```

2. Enter your `.ROBLOSECURITY` cookie when prompted
3. Enter the Place ID of the game you want to execute the script in
4. Enter your Lua script

### GUI Version

1. Run the GUI executor:
```bash
python roblox_executor_gui.py
```

2. Enter your `.ROBLOSECURITY` cookie in the first field
3. Enter the Place ID in the second field
4. Enter your Lua script in the large text area
5. Click "Execute Script" button

### Using the Launcher

You can also use the launcher to choose between versions:
```bash
python launch_executor.py
```

## Getting Your .ROBLOSECURITY Cookie

1. Log in to Roblox in your browser
2. Open developer tools (F12)
3. Go to the "Application" or "Storage" tab
4. Look for cookies for roblox.com
5. Find the `.ROBLOSECURITY` cookie value

## Important Security Notice

⚠️ **Warning**: Using executors to run unauthorized scripts in Roblox games may violate Roblox's Terms of Service and could result in account termination. Use at your own risk.

## Example Lua Script

```lua
-- Print a message to the output
print("Hello from Roblox Executor!")

-- Access player information
local Players = game:GetService("Players")
local player = Players.LocalPlayer
if player then
    print("Player name: " .. player.Name)
end
```

## Features

- Authentication with Roblox using security cookie
- Cross-Site Request Forgery (CSRF) token handling
- User information retrieval
- Script execution in Roblox games
- GUI with text area for multi-line scripts
- Thread-safe GUI updates
- Example script loading

## Limitations

- Requires a valid Roblox account and authentication cookie
- Only works with games that support script execution
- May be detected by Roblox anti-cheat systems