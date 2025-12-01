#include <windows.h>
#include <tlhelp32.h>
#include <psapi.h>
#include <iostream>
#include <string>
#include <fstream>
#include <sstream>

#pragma comment(lib, "psapi.lib")

class RobloxEzecutor {
private:
    HANDLE robloxProcessHandle;
    DWORD robloxProcessId;

public:
    RobloxEzecutor() : robloxProcessHandle(NULL), robloxProcessId(0) {}

    ~RobloxEzecutor() {
        if (robloxProcessHandle != NULL) {
            CloseHandle(robloxProcessHandle);
        }
    }

    bool FindRobloxProcess() {
        HANDLE hSnapshot = CreateToolhelp32Snapshot(TH32CS_SNAPPROCESS, 0);
        if (hSnapshot == INVALID_HANDLE_VALUE) {
            std::cout << "[ERROR] Could not create process snapshot\n";
            return false;
        }

        PROCESSENTRY32W pe32;
        pe32.dwSize = sizeof(PROCESSENTRY32W);

        if (!Process32FirstW(hSnapshot, &pe32)) {
            CloseHandle(hSnapshot);
            std::cout << "[ERROR] Could not enumerate processes\n";
            return false;
        }

        bool found = false;
        do {
            if (wcscmp(pe32.szExeFile, L"RobloxPlayerBeta.exe") == 0 || 
                wcscmp(pe32.szExeFile, L"RobloxStudioBeta.exe") == 0) {
                
                robloxProcessId = pe32.th32ProcessID;
                
                // Open the process with required permissions
                robloxProcessHandle = OpenProcess(PROCESS_ALL_ACCESS, FALSE, robloxProcessId);
                if (robloxProcessHandle != NULL) {
                    std::wcout << "[SUCCESS] Found Roblox process: " << pe32.szExeFile 
                              << " (PID: " << robloxProcessId << ")\n";
                    found = true;
                    break;
                } else {
                    std::cout << "[ERROR] Could not open process (PID: " << robloxProcessId << ")\n";
                }
            }
        } while (Process32NextW(hSnapshot, &pe32));

        CloseHandle(hSnapshot);

        if (!found) {
            std::cout << "[ERROR] Roblox process not found\n";
        }

        return found;
    }

    bool ExecuteScript(const std::string& script) {
        if (robloxProcessHandle == NULL) {
            std::cout << "[ERROR] No Roblox process connected\n";
            return false;
        }

        if (script.empty()) {
            std::cout << "[ERROR] Script is empty\n";
            return false;
        }

        // Allocate memory in the target process
        LPVOID allocatedMemory = VirtualAllocEx(robloxProcessHandle, NULL, script.size() + 1, 
                                               MEM_COMMIT | MEM_RESERVE, PAGE_READWRITE);
        if (allocatedMemory == NULL) {
            std::cout << "[ERROR] Could not allocate memory in target process\n";
            return false;
        }

        // Write the script to the allocated memory
        SIZE_T bytesWritten;
        if (!WriteProcessMemory(robloxProcessHandle, allocatedMemory, script.c_str(), 
                               script.size() + 1, &bytesWritten)) {
            std::cout << "[ERROR] Could not write script to target process\n";
            VirtualFreeEx(robloxProcessHandle, allocatedMemory, 0, MEM_RELEASE);
            return false;
        }

        // Create a remote thread to execute the script
        HANDLE hThread = CreateRemoteThread(robloxProcessHandle, NULL, 0, 
                                           (LPTHREAD_START_ROUTINE)allocatedMemory, NULL, 0, NULL);
        if (hThread == NULL) {
            std::cout << "[ERROR] Could not create remote thread\n";
            VirtualFreeEx(robloxProcessHandle, allocatedMemory, 0, MEM_RELEASE);
            return false;
        }

        // Wait for the thread to finish
        WaitForSingleObject(hThread, INFINITE);
        
        // Clean up
        CloseHandle(hThread);
        VirtualFreeEx(robloxProcessHandle, allocatedMemory, 0, MEM_RELEASE);

        std::cout << "[SUCCESS] Script executed successfully\n";
        return true;
    }

    bool ExecuteFromFile(const std::string& filename) {
        std::ifstream file(filename);
        if (!file.is_open()) {
            std::cout << "[ERROR] Could not open file: " << filename << std::endl;
            return false;
        }

        std::stringstream buffer;
        buffer << file.rdbuf();
        std::string script = buffer.str();
        file.close();

        return ExecuteScript(script);
    }

    void ShowMenu() {
        std::cout << "\n========== Roblox Ezecutor ==========\n";
        std::cout << "1. Execute script from console\n";
        std::cout << "2. Execute script from file\n";
        std::cout << "3. Check connection status\n";
        std::cout << "4. Exit\n";
        std::cout << "=====================================\n";
        std::cout << "Choose an option: ";
    }

    void Run() {
        int choice;
        std::string input;

        while (true) {
            ShowMenu();
            std::cin >> choice;
            std::cin.ignore(); // Clear the input buffer

            switch (choice) {
                case 1: {
                    std::cout << "Enter script to execute: ";
                    std::getline(std::cin, input);
                    
                    if (!input.empty()) {
                        ExecuteScript(input);
                    } else {
                        std::cout << "[ERROR] Script cannot be empty\n";
                    }
                    break;
                }
                case 2: {
                    std::cout << "Enter file path: ";
                    std::getline(std::cin, input);
                    
                    if (!input.empty()) {
                        ExecuteFromFile(input);
                    } else {
                        std::cout << "[ERROR] File path cannot be empty\n";
                    }
                    break;
                }
                case 3: {
                    if (FindRobloxProcess()) {
                        std::cout << "[STATUS] Connected to Roblox process (PID: " << robloxProcessId << ")\n";
                    } else {
                        std::cout << "[STATUS] No Roblox process found\n";
                    }
                    break;
                }
                case 4: {
                    std::cout << "Exiting...\n";
                    return;
                }
                default: {
                    std::cout << "[ERROR] Invalid option\n";
                    break;
                }
            }
        }
    }
};

int main() {
    RobloxEzecutor executor;
    
    std::cout << "Roblox Ezecutor - Script Injection Tool\n";
    std::cout << "========================================\n";
    
    if (!executor.FindRobloxProcess()) {
        std::cout << "Please start Roblox before running this tool.\n";
        return 1;
    }
    
    executor.Run();
    
    return 0;
}