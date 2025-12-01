#!/bin/bash

echo "Installing dependencies for Remote Control Bot..."

# Check if pip is installed
if ! command -v pip &> /dev/null; then
    echo "pip is not installed. Please install pip first."
    exit 1
fi

# Install dependencies from requirements.txt
pip install -r requirements.txt

echo "Dependencies installed successfully!"
echo "You can now run the bot with: python remote_control_bot.py"