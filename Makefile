# Makefile for Roblox Executor

CXX = g++
CSHARP = dotnet
CXXFLAGS = -shared -fPIC
LIBS = -lcurl -ljsoncpp

# Default target
all: RobloxExecutor.dll RobloxExecutorGUI

# Build the C++ DLL
RobloxExecutor.dll: RobloxExecutor.cpp
	$(CXX) $(CXXFLAGS) -o $@ $< $(LIBS)

# Build the C# GUI
RobloxExecutorGUI: RobloxExecutorGUI.csproj RobloxExecutorGUI.cs
	$(CSHARP) build

# Run the application
run: all
	$(CSHARP) run

# Clean build artifacts
clean:
	rm -f RobloxExecutor.dll
	rm -rf bin/ obj/

.PHONY: all run clean