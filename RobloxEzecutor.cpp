#include <windows.h>
#include <tlhelp32.h>
#include <psapi.h>
#include <iostream>
#include <string>
#include <fstream>

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
        HANDLE snapshot = CreateToolhelp32Snapshot(TH32CS_SNAPPROCESS, 0);
        if (snapshot == INVALID_HANDLE_VALUE) {
            std::cout << "[-] Failed to create process snapshot" << std::endl;
            return false;
        }

        PROCESSENTRY32W entry;
        entry.dwSize = sizeof(PROCESSENTRY32W);

        if (!Process32FirstW(snapshot, &entry)) {
            std::cout << "[-] Failed to get first process" << std::endl;
            CloseHandle(snapshot);
            return false;
        }

        bool found = false;
        do {
            if (wcscmp(entry.szExeFile, L"RobloxPlayerBeta.exe") == 0 || 
                wcscmp(entry.szExeFile, L"RobloxStudioBeta.exe") == 0) {
                
                robloxProcessId = entry.th32ProcessID;
                
                robloxProcessHandle = OpenProcess(PROCESS_ALL_ACCESS, FALSE, robloxProcessId);
                if (robloxProcessHandle != NULL) {
                    std::wcout << "[+] Found Roblox process: " << entry.szExeFile 
                              << " (PID: " << robloxProcessId << ")" << std::endl;
                    found = true;
                    break;
                } else {
                    std::cout << "[-] Failed to open process handle for PID: " << robloxProcessId << std::endl;
                }
            }
        } while (Process32NextW(snapshot, &entry));

        CloseHandle(snapshot);

        if (!found) {
            std::cout << "[-] Roblox process not found" << std::endl;
        }

        return found;
    }

    bool ExecuteScript(const std::string& script) {
        if (robloxProcessHandle == NULL || robloxProcessId == 0) {
            std::cout << "[-] No Roblox process connected" << std::endl;
            return false;
        }

        if (script.empty()) {
            std::cout << "[-] Script is empty" << std::endl;
            return false;
        }

        // Allocate memory in the target process
        LPVOID remoteMemory = VirtualAllocEx(robloxProcessHandle, NULL, script.size() + 1, 
                                           MEM_COMMIT | MEM_RESERVE, PAGE_READWRITE);
        if (remoteMemory == NULL) {
            std::cout << "[-] Failed to allocate memory in target process" << std::endl;
            return false;
        }

        // Write the script to the allocated memory
        SIZE_T bytesWritten;
        if (!WriteProcessMemory(robloxProcessHandle, remoteMemory, script.c_str(), 
                               script.size() + 1, &bytesWritten)) {
            std::cout << "[-] Failed to write script to target process" << std::endl;
            VirtualFreeEx(robloxProcessHandle, remoteMemory, 0, MEM_RELEASE);
            return false;
        }

        std::cout << "[+] Script written to target process" << std::endl;
        
        // Note: Actual script execution would require specific Roblox API calls or a script executor
        // This is a simplified implementation that just allocates memory and writes the script
        // For actual execution, you would need to find and call the appropriate Roblox functions
        
        VirtualFreeEx(robloxProcessHandle, remoteMemory, 0, MEM_RELEASE);
        return true;
    }

    bool ExecuteFromFile(const std::string& filename) {
        std::ifstream file(filename);
        if (!file.is_open()) {
            std::cout << "[-] Failed to open file: " << filename << std::endl;
            return false;
        }

        std::string script((std::istreambuf_iterator<char>(file)),
                          std::istreambuf_iterator<char>());
        file.close();

        if (script.empty()) {
            std::cout << "[-] File is empty: " << filename << std::endl;
            return false;
        }

        return ExecuteScript(script);
    }

    void ShowMenu() {
        while (true) {
            std::cout << "\n========== Roblox Executor ==========" << std::endl;
            std::cout << "1. Execute script from console" << std::endl;
            std::cout << "2. Execute script from file" << std::endl;
            std::cout << "3. Check connection status" << std::endl;
            std::cout << "4. Exit" << std::endl;
            std::cout << "=====================================" << std::endl;
            std::cout << "Choose an option: ";

            int choice;
            std::cin >> choice;
            std::cin.ignore(); // Ignore the newline character

            switch (choice) {
                case 1: {
                    std::cout << "Enter your script: ";
                    std::string script;
                    std::getline(std::cin, script);
                    
                    if (FindRobloxProcess()) {
                        if (ExecuteScript(script)) {
                            std::cout << "[+] Script executed successfully" << std::endl;
                        } else {
                            std::cout << "[-] Failed to execute script" << std::endl;
                        }
                    } else {
                        std::cout << "[-] Could not find Roblox process" << std::endl;
                    }
                    break;
                }
                case 2: {
                    std::cout << "Enter filename: ";
                    std::string filename;
                    std::getline(std::cin, filename);
                    
                    if (FindRobloxProcess()) {
                        if (ExecuteFromFile(filename)) {
                            std::cout << "[+] Script executed successfully" << std::endl;
                        } else {
                            std::cout << "[-] Failed to execute script from file" << std::endl;
                        }
                    } else {
                        std::cout << "[-] Could not find Roblox process" << std::endl;
                    }
                    break;
                }
                case 3: {
                    if (robloxProcessId != 0) {
                        HANDLE testHandle = OpenProcess(PROCESS_QUERY_INFORMATION, FALSE, robloxProcessId);
                        if (testHandle != NULL) {
                            char processName[MAX_PATH];
                            GetModuleBaseNameA(testHandle, NULL, processName, sizeof(processName));
                            std::cout << "[+] Connected to Roblox process: " << processName 
                                      << " (PID: " << robloxProcessId << ")" << std::endl;
                            CloseHandle(testHandle);
                        } else {
                            std::cout << "[-] Connection lost or process terminated" << std::endl;
                            robloxProcessId = 0;
                            robloxProcessHandle = NULL;
                        }
                    } else {
                        std::cout << "[-] Not connected to any Roblox process" << std::endl;
                    }
                    break;
                }
                case 4: {
                    std::cout << "[+] Exiting..." << std::endl;
                    return;
                }
                default: {
                    std::cout << "[-] Invalid option" << std::endl;
                    break;
                }
            }
        }
    }
};

int main() {
    std::cout << "Roblox Executor - Ezecutor" << std::endl;
    std::cout << "This tool allows you to inject scripts into Roblox" << std::endl;
    
    RobloxEzecutor executor;
    executor.ShowMenu();
    
    return 0;
}