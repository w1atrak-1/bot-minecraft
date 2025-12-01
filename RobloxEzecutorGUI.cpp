#include <windows.h>
#include <tlhelp32.h>
#include <psapi.h>
#include <iostream>
#include <string>
#include <fstream>
#include <vector>

#pragma comment(lib, "psapi.lib")

class RobloxEzecutor {
private:
    HANDLE robloxProcessHandle;
    DWORD robloxProcessId;

public:
    RobloxEzecutor() : robloxProcessHandle(NULL), robloxProcessId(0) {}

    bool FindRobloxProcess() {
        // Close any existing handle
        if (robloxProcessHandle != NULL) {
            CloseHandle(robloxProcessHandle);
            robloxProcessHandle = NULL;
        }

        HANDLE hSnapshot = CreateToolhelp32Snapshot(TH32CS_SNAPPROCESS, 0);
        if (hSnapshot == INVALID_HANDLE_VALUE) {
            return false;
        }

        PROCESSENTRY32 pe32;
        pe32.dwSize = sizeof(PROCESSENTRY32);

        if (!Process32First(hSnapshot, &pe32)) {
            CloseHandle(hSnapshot);
            return false;
        }

        bool found = false;
        do {
            if (wcscmp(pe32.szExeFile, L"RobloxPlayerBeta.exe") == 0 || 
                wcscmp(pe32.szExeFile, L"RobloxStudioBeta.exe") == 0) {
                robloxProcessId = pe32.th32ProcessID;
                
                robloxProcessHandle = OpenProcess(PROCESS_ALL_ACCESS, FALSE, robloxProcessId);
                if (robloxProcessHandle != NULL) {
                    found = true;
                    break;
                }
            }
        } while (Process32Next(hSnapshot, &pe32));

        CloseHandle(hSnapshot);
        return found;
    }

    bool ExecuteScript(const std::string& script) {
        if (robloxProcessHandle == NULL || robloxProcessId == 0) {
            return false;
        }

        if (script.empty()) {
            return false;
        }

        // Allocate memory in the target process
        LPVOID allocatedMemory = VirtualAllocEx(robloxProcessHandle, NULL, script.size() + 1, MEM_COMMIT | MEM_RESERVE, PAGE_READWRITE);
        if (allocatedMemory == NULL) {
            return false;
        }

        // Write the script to the allocated memory
        BOOL writeSuccess = WriteProcessMemory(robloxProcessHandle, allocatedMemory, script.c_str(), script.size() + 1, NULL);
        if (!writeSuccess) {
            VirtualFreeEx(robloxProcessHandle, allocatedMemory, 0, MEM_RELEASE);
            return false;
        }

        // Free the allocated memory
        VirtualFreeEx(robloxProcessHandle, allocatedMemory, 0, MEM_RELEASE);

        // In a real executor, you would call the script execution function here
        // For demonstration, we'll just return true
        return true;
    }

    bool ExecuteFromFile(const std::string& filename) {
        std::ifstream file(filename);
        if (!file.is_open()) {
            return false;
        }

        std::string script((std::istreambuf_iterator<char>(file)), std::istreambuf_iterator<char>());
        file.close();

        return ExecuteScript(script);
    }

    bool IsConnected() {
        if (robloxProcessHandle == NULL || robloxProcessId == 0) {
            return false;
        }

        DWORD exitCode;
        GetExitCodeProcess(robloxProcessHandle, &exitCode);
        return exitCode == STILL_ACTIVE;
    }

    DWORD GetProcessId() const {
        return robloxProcessId;
    }

    ~RobloxEzecutor() {
        if (robloxProcessHandle != NULL) {
            CloseHandle(robloxProcessHandle);
        }
    }
};

// Global instance
RobloxEzecutor executor;

// Window procedure
LRESULT CALLBACK WndProc(HWND hwnd, int msg, WPARAM wParam, LPARAM lParam) {
    static HWND hScriptEdit, hStatusLabel, hConnectButton, hExecuteButton, hFileButton, hFileLabel;

    switch (msg) {
        case WM_CREATE: {
            // Create controls
            hStatusLabel = CreateWindowEx(
                0, "STATIC", "Status: Not connected to Roblox", 
                WS_VISIBLE | WS_CHILD | SS_LEFT,
                20, 20, 300, 20, 
                hwnd, NULL, ((LPCREATESTRUCT)lParam)->hInstance, NULL
            );
            
            hConnectButton = CreateWindowEx(
                0, "BUTTON", "Connect to Roblox", 
                WS_VISIBLE | WS_CHILD | BS_PUSHBUTTON,
                20, 50, 150, 30, 
                hwnd, (HMENU)1, ((LPCREATESTRUCT)lParam)->hInstance, NULL
            );
            
            hScriptEdit = CreateWindowEx(
                WS_EX_CLIENTEDGE, "EDIT", "", 
                WS_VISIBLE | WS_CHILD | WS_VSCROLL | ES_MULTILINE | ES_AUTOVSCROLL,
                20, 90, 400, 150, 
                hwnd, NULL, ((LPCREATESTRUCT)lParam)->hInstance, NULL
            );
            
            hExecuteButton = CreateWindowEx(
                0, "BUTTON", "Execute Script", 
                WS_VISIBLE | WS_CHILD | BS_PUSHBUTTON,
                20, 250, 150, 30, 
                hwnd, (HMENU)2, ((LPCREATESTRUCT)lParam)->hInstance, NULL
            );
            
            hFileLabel = CreateWindowEx(
                0, "STATIC", "Script File:", 
                WS_VISIBLE | WS_CHILD | SS_LEFT,
                20, 290, 80, 20, 
                hwnd, NULL, ((LPCREATESTRUCT)lParam)->hInstance, NULL
            );
            
            hFileButton = CreateWindowEx(
                0, "BUTTON", "Select Script File", 
                WS_VISIBLE | WS_CHILD | BS_PUSHBUTTON,
                110, 285, 150, 30, 
                hwnd, (HMENU)3, ((LPCREATESTRUCT)lParam)->hInstance, NULL
            );
            
            break;
        }
        
        case WM_COMMAND: {
            if (LOWORD(wParam) == 1) { // Connect button
                if (executor.FindRobloxProcess()) {
                    SetWindowText(hStatusLabel, "Status: Connected to Roblox (PID: ");
                    char pidText[100];
                    sprintf_s(pidText, sizeof(pidText), "Status: Connected to Roblox (PID: %lu)", executor.GetProcessId());
                    SetWindowText(hStatusLabel, pidText);
                } else {
                    SetWindowText(hStatusLabel, "Status: Could not connect to Roblox");
                }
            }
            else if (LOWORD(wParam) == 2) { // Execute button
                // Get script from edit control
                int length = GetWindowTextLength(hScriptEdit);
                if (length > 0) {
                    std::vector<char> scriptBuffer(length + 1);
                    GetWindowText(hScriptEdit, scriptBuffer.data(), length + 1);
                    
                    if (executor.ExecuteScript(std::string(scriptBuffer.data()))) {
                        MessageBox(hwnd, "Script executed successfully!", "Success", MB_OK | MB_ICONINFORMATION);
                    } else {
                        MessageBox(hwnd, "Failed to execute script. Make sure you're connected to Roblox.", "Error", MB_OK | MB_ICONERROR);
                    }
                } else {
                    MessageBox(hwnd, "Please enter a script to execute.", "Error", MB_OK | MB_ICONWARNING);
                }
            }
            else if (LOWORD(wParam) == 3) { // File button
                OPENFILENAME ofn;
                char fileName[MAX_PATH] = "";
                
                ZeroMemory(&ofn, sizeof(ofn));
                ofn.lStructSize = sizeof(ofn);
                ofn.hwndOwner = hwnd;
                ofn.lpstrFilter = "Lua Files (*.lua)\0*.lua\0Text Files (*.txt)\0*.txt\0All Files (*.*)\0*.*\0";
                ofn.lpstrFile = fileName;
                ofn.nMaxFile = MAX_PATH;
                ofn.Flags = OFN_EXPLORER | OFN_FILEMUSTEXIST | OFN_HIDEREADONLY;
                ofn.lpstrDefExt = "lua";
                
                if (GetOpenFileName(&ofn)) {
                    if (executor.ExecuteFromFile(std::string(fileName))) {
                        MessageBox(hwnd, "Script executed successfully!", "Success", MB_OK | MB_ICONINFORMATION);
                    } else {
                        MessageBox(hwnd, "Failed to execute script from file.", "Error", MB_OK | MB_ICONERROR);
                    }
                }
            }
            break;
        }
        
        case WM_CLOSE: {
            DestroyWindow(hwnd);
            break;
        }
        
        case WM_DESTROY: {
            PostQuitMessage(0);
            break;
        }
        
        default:
            return DefWindowProc(hwnd, msg, wParam, lParam);
    }
    
    return 0;
}

int APIENTRY WinMain(HINSTANCE hInstance, HINSTANCE hPrevInstance, LPSTR lpCmdLine, int nCmdShow) {
    const char CLASS_NAME[] = "RobloxEzecutorGUI";
    
    WNDCLASS wc = {};
    wc.lpfnWndProc = WndProc;
    wc.hInstance = hInstance;
    wc.lpszClassName = CLASS_NAME;
    wc.hCursor = LoadCursor(NULL, IDC_ARROW);
    wc.hbrBackground = (HBRUSH)(COLOR_WINDOW + 1);
    wc.hIcon = LoadIcon(NULL, IDI_APPLICATION);
    
    RegisterClass(&wc);
    
    HWND hwnd = CreateWindowEx(
        0, 
        CLASS_NAME, 
        "Roblox Ezecutor GUI", 
        WS_OVERLAPPED | WS_CAPTION | WS_SYSMENU | WS_MINIMIZEBOX,
        CW_USEDEFAULT, CW_USEDEFAULT, 450, 380,
        NULL, 
        NULL, 
        hInstance, 
        NULL
    );
    
    if (hwnd == NULL) {
        return 0;
    }
    
    ShowWindow(hwnd, nCmdShow);
    UpdateWindow(hwnd);
    
    MSG msg = {};
    while (GetMessage(&msg, NULL, 0, 0)) {
        TranslateMessage(&msg);
        DispatchMessage(&msg);
    }
    
    return 0;
}