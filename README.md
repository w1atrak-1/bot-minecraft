# Roblox Ezecutor

A powerful script injection tool for Roblox with both console and GUI versions.

## Features

### Console Version (RobloxEzecutor.exe)
- Execute scripts directly from console input
- Execute scripts from files
- Check connection status to Roblox process
- Clean command-line interface

### GUI Version (RobloxEzecutorGUI.exe)
- Dark-themed user interface
- Script input text area with scroll support
- Execute button to run scripts
- Paste button to paste from clipboard
- From File button to load scripts from files
- Clear button to clear the script area
- Minimize and Close buttons
- Status indicator showing connection to Roblox

## Requirements

- Windows OS (the executables are compiled for Windows)
- Roblox Player or Roblox Studio must be running before using the tool

## Usage

### Console Version
1. Start Roblox Player or Roblox Studio
2. Run `RobloxEzecutor.exe`
3. The tool will automatically detect the Roblox process
4. Choose an option from the menu:
   - Option 1: Enter a script directly in the console
   - Option 2: Load a script from a file
   - Option 3: Check connection status
   - Option 4: Exit

### GUI Version
1. Start Roblox Player or Roblox Studio
2. Run `RobloxEzecutorGUI.exe`
3. The tool will automatically detect the Roblox process
4. Type or paste your script in the text area
5. Click "Execute Script" to inject the script
6. Use "Paste" to paste from clipboard
7. Use "From File" to load a script from a file
8. Use "Clear" to clear the script area
9. Use the minimize or close buttons as needed

## How It Works

The Roblox Ezecutor uses Windows API functions to:
1. Find the Roblox process by searching for "RobloxPlayerBeta.exe" or "RobloxStudioBeta.exe"
2. Allocate memory in the target process using `VirtualAllocEx`
3. Write the script to the allocated memory using `WriteProcessMemory`
4. Execute the script by creating a remote thread using `CreateRemoteThread`

## Security Notes

- This tool is designed for educational purposes
- Only use on games you own or have permission to modify
- Be aware of Roblox's Terms of Service when using script injection tools

## Compilation

The source code is provided in:
- `RobloxEzecutor.cpp` - Console version
- `RobloxEzecutorGUI.cpp` - GUI version

To compile on Linux with MinGW-w64:
```bash
x86_64-w64-mingw32-g++ RobloxEzecutor.cpp -o RobloxEzecutor.exe -lpsapi -static
x86_64-w64-mingw32-g++ RobloxEzecutorGUI.cpp -o RobloxEzecutorGUI.exe -lpsapi -lgdi32 -lcomdlg32 -lcomctl32 -static
```