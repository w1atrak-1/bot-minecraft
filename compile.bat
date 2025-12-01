#!/bin/bash
echo "Compiling Roblox Ezecutor..."

# Compile console version for Windows
x86_64-w64-mingw32-g++ RobloxEzecutor.cpp -o RobloxEzecutor.exe -lpsapi -static

if [ $? -ne 0 ]; then
    echo "Failed to compile console version"
    exit 1
fi

# Compile GUI version for Windows (with required Windows libraries)
x86_64-w64-mingw32-g++ RobloxEzecutorGUI.cpp -o RobloxEzecutorGUI.exe -lpsapi -lgdi32 -lcomdlg32 -lcomctl32 -static

if [ $? -ne 0 ]; then
    echo "Failed to compile GUI version"
    exit 1
fi

echo "Compilation completed successfully!"
echo "Console version: RobloxEzecutor.exe"
echo "GUI version: RobloxEzecutorGUI.exe"