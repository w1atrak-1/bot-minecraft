# Roblox Executor

A Roblox script executor with C++ core functionality and C# GUI.

## Components

1. **C++ Core (`RobloxExecutor.cpp`)**: Handles authentication, script execution, and communication with Roblox APIs
2. **C# GUI (`RobloxExecutorGUI.cs`)**: Provides a user-friendly interface to interact with the executor

## Building

### Prerequisites
- Visual Studio or C++ Build Tools
- .NET 6.0 SDK
- libcurl development libraries
- jsoncpp development libraries

### Steps

1. **Build the C++ DLL:**
   ```bash
   g++ -shared -fPIC -o RobloxExecutor.dll RobloxExecutor.cpp -lcurl -ljsoncpp
   ```
   
   Or with Visual Studio:
   ```bash
   cl /LD RobloxExecutor.cpp /link /LIBPATH:"path_to_curl_lib" /LIBPATH:"path_to_jsoncpp_lib" libcurl.lib jsoncpp.lib
   ```

2. **Build the C# GUI:**
   ```bash
   dotnet build
   ```

3. **Run the application:**
   ```bash
   dotnet run
   ```

## Usage

1. Obtain your ROBLOSECURITY cookie from your browser's developer tools
2. Enter the Place ID of the game you want to execute scripts in
3. Write or paste your Lua script in the script area
4. Click "Execute Script" to run your script in the Roblox game

## Important Notes

- This tool is for educational purposes only
- Use responsibly and in accordance with Roblox Terms of Service
- Scripts may not work in all games due to security restrictions
- Keep your ROBLOSECURITY cookie private and secure

## Security Warning

Never share your ROBLOSECURITY cookie with anyone. This token provides access to your Roblox account.