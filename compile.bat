@echo off
echo Compiling Roblox Ezecutor...
g++ -o RobloxEzecutor.exe RobloxEzecutor.cpp -lpsapi -lwinmm
if %ERRORLEVEL% EQU 0 (
    echo Compilation successful!
    echo Run RobloxEzecutor.exe to start the executor.
) else (
    echo Compilation failed!
)
pause