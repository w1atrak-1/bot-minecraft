#!/usr/bin/env python3
"""
Roblox Executor Launcher
Choose between GUI and console versions
"""

import sys
import os

def main():
    print("=== Roblox Executor Launcher ===")
    print("1. GUI Version")
    print("2. Console Version")
    print("3. Exit")
    
    while True:
        try:
            choice = input("\nSelect option (1-3): ").strip()
            
            if choice == "1":
                print("Starting GUI version...")
                import roblox_executor_gui
                roblox_executor_gui.main()
                break
            elif choice == "2":
                print("Starting console version...")
                import roblox_executor
                roblox_executor.main()
                break
            elif choice == "3":
                print("Exiting...")
                break
            else:
                print("Invalid option. Please select 1, 2, or 3.")
        except KeyboardInterrupt:
            print("\nExiting...")
            break
        except Exception as e:
            print(f"Error: {e}")
            break

if __name__ == "__main__":
    main()