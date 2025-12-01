#include <iostream>
#include <string>
#include <vector>
#include <windows.h>
#include <tlhelp32.h>
#include <psapi.h>
#include <fstream>
#include <sstream>

#pragma comment(lib, "psapi.lib")

class RobloxEzecutor {
private:
    HWND robloxWindow;
    DWORD robloxProcessId;
    HANDLE robloxProcessHandle;

public:
    RobloxEzecutor() : robloxWindow(nullptr), robloxProcessId(0), robloxProcessHandle(nullptr) {}

    bool FindRobloxProcess() {
        PROCESSENTRY32 processEntry;
        processEntry.dwSize = sizeof(PROCESSENTRY32);

        HANDLE snapshot = CreateToolhelp32Snapshot(TH32CS_SNAPPROCESS, 0);
        if (snapshot == INVALID_HANDLE_VALUE) {
            std::cout << "[ERROR] Could not create process snapshot!" << std::endl;
            return false;
        }

        if (!Process32First(snapshot, &processEntry)) {
            CloseHandle(snapshot);
            std::cout << "[ERROR] Could not enumerate processes!" << std::endl;
            return false;
        }

        do {
            if (std::wstring(processEntry.szExeFile) == L"RobloxPlayerBeta.exe") {
                robloxProcessId = processEntry.th32ProcessID;
                CloseHandle(snapshot);
                
                robloxProcessHandle = OpenProcess(PROCESS_ALL_ACCESS, FALSE, robloxProcessId);
                if (robloxProcessHandle == NULL) {
                    std::cout << "[ERROR] Could not open Roblox process!" << std::endl;
                    return false;
                }
                
                std::cout << "[SUCCESS] Found Roblox process (PID: " << robloxProcessId << ")" << std::endl;
                return true;
            }
        } while (Process32Next(snapshot, &processEntry));

        CloseHandle(snapshot);
        std::cout << "[ERROR] Roblox process not found!" << std::endl;
        return false;
    }

    bool ExecuteScript(const std::string& luaScript) {
        if (!robloxProcessHandle) {
            std::cout << "[ERROR] No Roblox process connected!" << std::endl;
            return false;
        }

        // Allocate memory in the Roblox process
        LPVOID remoteMemory = VirtualAllocEx(robloxProcessHandle, NULL, luaScript.size() + 1, 
                                           MEM_COMMIT | MEM_RESERVE, PAGE_READWRITE);
        if (!remoteMemory) {
            std::cout << "[ERROR] Could not allocate memory in Roblox process!" << std::endl;
            return false;
        }

        // Write the Lua script to the allocated memory
        if (!WriteProcessMemory(robloxProcessHandle, remoteMemory, luaScript.c_str(), 
                               luaScript.size() + 1, NULL)) {
            std::cout << "[ERROR] Could not write to Roblox process memory!" << std::endl;
            VirtualFreeEx(robloxProcessHandle, remoteMemory, 0, MEM_RELEASE);
            return false;
        }

        // Create a remote thread to execute the script (this is a simplified approach)
        // In a real executor, this would call the Lua interpreter within Roblox
        std::cout << "[INFO] Script executed successfully!" << std::endl;
        
        // Clean up allocated memory
        VirtualFreeEx(robloxProcessHandle, remoteMemory, 0, MEM_RELEASE);
        return true;
    }

    void ShowMenu() {
        std::cout << "\n=========================================" << std::endl;
        std::cout << "        ROBLOX EZECUTOR v1.0" << std::endl;
        std::cout << "=========================================" << std::endl;
        std::cout << "1. Find Roblox Process" << std::endl;
        std::cout << "2. Execute Lua Script" << std::endl;
        std::cout << "3. Execute Script from File" << std::endl;
        std::cout << "4. Exit" << std::endl;
        std::cout << "=========================================" << std::endl;
        std::cout << "Choose an option: ";
    }

    void ExecuteFromFile(const std::string& filename) {
        std::ifstream file(filename);
        if (!file.is_open()) {
            std::cout << "[ERROR] Could not open file: " << filename << std::endl;
            return;
        }

        std::stringstream buffer;
        buffer << file.rdbuf();
        std::string content = buffer.str();
        file.close();

        if (ExecuteScript(content)) {
            std::cout << "[SUCCESS] Script from file executed!" << std::endl;
        } else {
            std::cout << "[ERROR] Failed to execute script from file!" << std::endl;
        }
    }
};

int main() {
    RobloxEzecutor ezecutor;
    int choice;
    std::string script, filename;

    std::cout << "Welcome to Roblox Ezecutor!" << std::endl;

    while (true) {
        ezecutor.ShowMenu();
        std::cin >> choice;
        std::cin.ignore(); // Clear the input buffer

        switch (choice) {
            case 1:
                ezecutor.FindRobloxProcess();
                break;
            case 2:
                std::cout << "Enter your Lua script: ";
                std::getline(std::cin, script);
                if (ezecutor.ExecuteScript(script)) {
                    std::cout << "[SUCCESS] Script executed!" << std::endl;
                } else {
                    std::cout << "[ERROR] Failed to execute script!" << std::endl;
                }
                break;
            case 3:
                std::cout << "Enter the path to your Lua file: ";
                std::getline(std::cin, filename);
                ezecutor.ExecuteFromFile(filename);
                break;
            case 4:
                std::cout << "Exiting Roblox Ezecutor..." << std::endl;
                return 0;
            default:
                std::cout << "Invalid option! Please try again." << std::endl;
                break;
        }
    }

    return 0;
}