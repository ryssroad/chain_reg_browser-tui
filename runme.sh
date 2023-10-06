#!/bin/bash

# Display a cool message
echo "Yo, dude! We're about to download and run the Chain Registry Browser TUI."
read -p "Are you totally sure you wanna do this? (Y/n): " answer

if [ "$answer" != "n" ]; then
    # Clone the repo
    echo "Sweet! Cloning the repo..."
    git clone https://github.com/ChainTools-Tech/chain_reg_browser-tui
    cd chain_reg_browser-tui

    # Create a virtual environment
    echo "Creating a virtual environment..."
    python3 -m venv ./venv
    source venv/bin/activate

    # Install dependencies
    echo "Installing dependencies..."
    pip install -r requirements.txt

    echo "Installation complete, bro!"
else
    echo "Installation canceled, no worries, dude."
fi
