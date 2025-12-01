#include <windows.h>
#include <tlhelp32.h>
#include <psapi.h>
#include <iostream>
#include <string>
#include <fstream>
#include <sstream>
#include <vector>

#pragma comment(lib, "psapi.lib")

// Define window class and control IDs
#define IDC_EXECUTE_BUTTON 101
#define IDC_SCRIPT_EDIT 102
#define IDC_STATUS_LABEL 103
#define IDC_FILE_BUTTON 104
#define IDC_CLEAR_BUTTON 105
#define IDC_MINIMIZE_BUTTON 106
#define IDC_CLOSE_BUTTON 107
#define IDC_PASTE_BUTTON 108

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
            return false;
        }

        PROCESSENTRY32W pe32;
        pe32.dwSize = sizeof(PROCESSENTRY32W);

        if (!Process32FirstW(hSnapshot, &pe32)) {
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
        } while (Process32NextW(hSnapshot, &pe32));

        CloseHandle(hSnapshot);
        return found;
    }

    bool ExecuteScript(const std::string& script) {
        if (robloxProcessHandle == NULL) {
            return false;
        }

        if (script.empty()) {
            return false;
        }

        LPVOID allocatedMemory = VirtualAllocEx(robloxProcessHandle, NULL, script.size() + 1, 
                                               MEM_COMMIT | MEM_RESERVE, PAGE_READWRITE);
        if (allocatedMemory == NULL) {
            return false;
        }

        SIZE_T bytesWritten;
        if (!WriteProcessMemory(robloxProcessHandle, allocatedMemory, script.c_str(), 
                               script.size() + 1, &bytesWritten)) {
            VirtualFreeEx(robloxProcessHandle, allocatedMemory, 0, MEM_RELEASE);
            return false;
        }

        HANDLE hThread = CreateRemoteThread(robloxProcessHandle, NULL, 0, 
                                           (LPTHREAD_START_ROUTINE)allocatedMemory, NULL, 0, NULL);
        if (hThread == NULL) {
            VirtualFreeEx(robloxProcessHandle, allocatedMemory, 0, MEM_RELEASE);
            return false;
        }

        WaitForSingleObject(hThread, INFINITE);
        CloseHandle(hThread);
        VirtualFreeEx(robloxProcessHandle, allocatedMemory, 0, MEM_RELEASE);

        return true;
    }

    bool ExecuteFromFile(const std::string& filename) {
        std::ifstream file(filename);
        if (!file.is_open()) {
            return false;
        }

        std::stringstream buffer;
        buffer << file.rdbuf();
        std::string script = buffer.str();
        file.close();

        return ExecuteScript(script);
    }

    DWORD GetProcessId() const {
        return robloxProcessId;
    }
};

HINSTANCE hInst;
RobloxEzecutor* executor = nullptr;
HWND hwndScriptEdit, hwndStatusLabel;

LRESULT CALLBACK WndProc(HWND hwnd, UINT msg, WPARAM wParam, LPARAM lParam) {
    switch (msg) {
        case WM_CREATE: {
            // Create script input edit control
            hwndScriptEdit = CreateWindowExW(
                WS_EX_CLIENTEDGE,
                L"EDIT",
                L"",
                WS_CHILD | WS_VISIBLE | WS_VSCROLL | ES_MULTILINE | ES_AUTOVSCROLL,
                10, 10, 500, 200,
                hwnd,
                (HMENU)IDC_SCRIPT_EDIT,
                hInst,
                NULL
            );

            // Create status label
            hwndStatusLabel = CreateWindowW(
                L"STATIC",
                L"Status: Not connected to Roblox",
                WS_CHILD | WS_VISIBLE,
                10, 220, 500, 20,
                hwnd,
                (HMENU)IDC_STATUS_LABEL,
                hInst,
                NULL
            );

            // Create execute button
            CreateWindowW(
                L"BUTTON",
                L"Execute Script",
                WS_CHILD | WS_VISIBLE,
                10, 250, 100, 30,
                hwnd,
                (HMENU)IDC_EXECUTE_BUTTON,
                hInst,
                NULL
            );

            // Create paste button
            CreateWindowW(
                L"BUTTON",
                L"Paste",
                WS_CHILD | WS_VISIBLE,
                120, 250, 60, 30,
                hwnd,
                (HMENU)IDC_PASTE_BUTTON,
                hInst,
                NULL
            );

            // Create file button
            CreateWindowW(
                L"BUTTON",
                L"From File",
                WS_CHILD | WS_VISIBLE,
                190, 250, 80, 30,
                hwnd,
                (HMENU)IDC_FILE_BUTTON,
                hInst,
                NULL
            );

            // Create clear button
            CreateWindowW(
                L"BUTTON",
                L"Clear",
                WS_CHILD | WS_VISIBLE,
                280, 250, 60, 30,
                hwnd,
                (HMENU)IDC_CLEAR_BUTTON,
                hInst,
                NULL
            );

            // Create minimize button
            CreateWindowW(
                L"BUTTON",
                L"_",
                WS_CHILD | WS_VISIBLE,
                440, 250, 30, 30,
                hwnd,
                (HMENU)IDC_MINIMIZE_BUTTON,
                hInst,
                NULL
            );

            // Create close button
            CreateWindowW(
                L"BUTTON",
                L"X",
                WS_CHILD | WS_VISIBLE,
                480, 250, 30, 30,
                hwnd,
                (HMENU)IDC_CLOSE_BUTTON,
                hInst,
                NULL
            );
            break;
        }
        case WM_COMMAND: {
            if (LOWORD(wParam) == IDC_EXECUTE_BUTTON) {
                // Get script from edit control
                int textLength = GetWindowTextLengthW(hwndScriptEdit);
                if (textLength > 0) {
                    wchar_t* buffer = new wchar_t[textLength + 1];
                    GetWindowTextW(hwndScriptEdit, buffer, textLength + 1);
                    
                    // Convert wide string to narrow string
                    std::wstring wstr(buffer);
                    std::string script(wstr.begin(), wstr.end());
                    
                    delete[] buffer;

                    if (executor->ExecuteScript(script)) {
                        SetWindowTextW(hwndStatusLabel, L"Status: Script executed successfully!");
                    } else {
                        SetWindowTextW(hwndStatusLabel, L"Status: Failed to execute script");
                    }
                } else {
                    SetWindowTextW(hwndStatusLabel, L"Status: Script is empty");
                }
            }
            else if (LOWORD(wParam) == IDC_PASTE_BUTTON) {
                if (IsClipboardFormatAvailable(CF_UNICODETEXT)) {
                    if (OpenClipboard(hwnd)) {
                        HGLOBAL hClipboardData = GetClipboardData(CF_UNICODETEXT);
                        if (hClipboardData != NULL) {
                            wchar_t* pwstr = (wchar_t*)GlobalLock(hClipboardData);
                            if (pwstr != NULL) {
                                SetWindowTextW(hwndScriptEdit, pwstr);
                                GlobalUnlock(hClipboardData);
                            }
                        }
                        CloseClipboard();
                    }
                }
            }
            else if (LOWORD(wParam) == IDC_FILE_BUTTON) {
                // Simple file dialog implementation
                OPENFILENAMEW ofn;
                wchar_t fileName[MAX_PATH] = L"";
                
                ZeroMemory(&ofn, sizeof(ofn));
                ofn.lStructSize = sizeof(ofn);
                ofn.hwndOwner = hwnd;
                ofn.lpstrFile = fileName;
                ofn.nMaxFile = MAX_PATH;
                ofn.lpstrFilter = L"Lua Files\0*.lua\0Text Files\0*.txt\0All Files\0*.*\0";
                ofn.nFilterIndex = 1;
                ofn.lpstrFileTitle = NULL;
                ofn.nMaxFileTitle = 0;
                ofn.lpstrInitialDir = NULL;
                ofn.Flags = OFN_PATHMUSTEXIST | OFN_FILEMUSTEXIST;

                if (GetOpenFileNameW(&ofn)) {
                    std::wstring wfilename(ofn.lpstrFile);
                    std::string filename(wfilename.begin(), wfilename.end());
                    
                    if (executor->ExecuteFromFile(filename)) {
                        SetWindowTextW(hwndStatusLabel, L"Status: Script from file executed successfully!");
                    } else {
                        SetWindowTextW(hwndStatusLabel, L"Status: Failed to execute script from file");
                    }
                }
            }
            else if (LOWORD(wParam) == IDC_CLEAR_BUTTON) {
                SetWindowTextW(hwndScriptEdit, L"");
                SetWindowTextW(hwndStatusLabel, L"Status: Cleared");
            }
            else if (LOWORD(wParam) == IDC_MINIMIZE_BUTTON) {
                ShowWindow(hwnd, SW_MINIMIZE);
            }
            else if (LOWORD(wParam) == IDC_CLOSE_BUTTON) {
                PostMessageW(hwnd, WM_CLOSE, 0, 0);
            }
            break;
        }
        case WM_CTLCOLORBTN:
        case WM_CTLCOLORSTATIC: {
            HDC hdc = (HDC)wParam;
            SetBkColor(hdc, RGB(30, 30, 30));  // Dark background
            SetTextColor(hdc, RGB(220, 220, 220));  // Light text
            static HBRUSH brush = CreateSolidBrush(RGB(30, 30, 30));
            return (LRESULT)brush;
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
            return DefWindowProcW(hwnd, msg, wParam, lParam);
    }
    return 0;
}

int WINAPI WinMain(HINSTANCE hInstance, HINSTANCE hPrevInstance, LPSTR lpCmdLine, int nCmdShow) {
    hInst = hInstance;

    // Create executor instance
    executor = new RobloxEzecutor();

    // Register window class
    const wchar_t CLASS_NAME[] = L"RobloxEzecutorClass";
    
    WNDCLASSEXW wc = {};
    wc.cbSize = sizeof(WNDCLASSEXW);
    wc.style = CS_HREDRAW | CS_VREDRAW;
    wc.lpfnWndProc = WndProc;
    wc.hInstance = hInstance;
    wc.hbrBackground = CreateSolidBrush(RGB(40, 40, 40));  // Dark background
    wc.lpszClassName = CLASS_NAME;
    wc.hCursor = LoadCursor(NULL, IDC_ARROW);
    wc.hIcon = LoadIcon(NULL, IDI_APPLICATION);
    wc.hIconSm = LoadIcon(NULL, IDI_APPLICATION);

    RegisterClassExW(&wc);

    // Create window
    HWND hwnd = CreateWindowExW(
        0,
        CLASS_NAME,
        L"Roblox Ezecutor",
        WS_OVERLAPPEDWINDOW & ~WS_THICKFRAME & ~WS_MAXIMIZEBOX,  // No resize
        CW_USEDEFAULT, CW_USEDEFAULT, 530, 330,
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

    // Check for Roblox process
    if (executor->FindRobloxProcess()) {
        wchar_t status[100];
        swprintf_s(status, 100, L"Status: Connected to Roblox (PID: %lu)", executor->GetProcessId());
        SetWindowTextW(hwndStatusLabel, status);
    } else {
        SetWindowTextW(hwndStatusLabel, L"Status: No Roblox process found - Please start Roblox");
    }

    // Message loop
    MSG msg = {};
    while (GetMessage(&msg, NULL, 0, 0)) {
        TranslateMessage(&msg);
        DispatchMessage(&msg);
    }

    delete executor;
    return (int)msg.wParam;
}