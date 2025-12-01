# Roblox Ezecutor

A simple C++ based Roblox script executor that allows you to execute Lua scripts in Roblox.

## Features

- Find Roblox process automatically
- Execute Lua scripts directly from console
- Execute Lua scripts from files
- Simple menu-based interface

## How to Compile

To compile this executor, you'll need a Windows C++ compiler that supports Windows API functions.

### Using g++ (MinGW):
```bash
g++ -o RobloxEzecutor.exe RobloxEzecutor.cpp -lpsapi -lwinmm
```

### Using Visual Studio:
```bash
cl RobloxEzecutor.cpp /link /out:RobloxEzecutor.exe psapi.lib
```

## How to Use

1. Compile the program using one of the methods above
2. Launch Roblox and join a game
3. Run the executor executable
4. Choose option 1 to find the Roblox process
5. Choose option 2 to execute a script directly or option 3 to execute a script from a file

## Important Note

This is a basic implementation for educational purposes. Real Roblox executors require more complex memory manipulation and injection techniques to properly interface with the Roblox Lua environment. This example demonstrates the basic structure and concept but may not work with current Roblox security measures.

## Disclaimer

Using script executors in Roblox may violate Roblox Terms of Service. Use at your own risk.

## Sample Script

A sample Lua script (`sample_script.lua`) is included that creates a part in the workspace and displays a message.