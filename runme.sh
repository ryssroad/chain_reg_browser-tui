#!/bin/bash

# Display a cool message
echo "Yo, dude! We're about to download and run the Chain Registry Browser TUI "
read -p "Are you totally sure you wanna do this? (Y/n): " answer

if [ "$answer" != "n" ]; then
    # Clone the repo
    echo "Nice! Cloning the repo..."
    # git clone https://github.com/ryssroad/testnet_chain_reg_browser-tui
    cd testnet_chain_reg_browser-tui

    # Create a virtual environment
    echo "Creating a virtual environment..."
    python3 -m venv ./venv
    source venv/bin/activate

    # Install dependencies
    echo "Installing dependencies..."
    pip install -r requirements.txt

    echo "Installation complete, bro!"
    
    # Activate virtual environment and run chain_reg_browser.py
    echo "Launching the Chain Registry Browser..."
    read -p "input GITHUB_TOKEN (default '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'): " github_token

    # Использовать значение по умолчанию, если ввод пользователя пуст
    github_token="${github_token:-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}"

    # Заменить значение GITHUB_TOKEN в файле config.json
    sed -i "s/\"GITHUB_TOKEN\": \".*\"/\"GITHUB_TOKEN\": \"$github_token\"/" config.json
    echo "GITHUB_TOKEN set complete!"
    python chain_reg_browser.py
else
    echo "Installation canceled, no worries, dude."
fi
