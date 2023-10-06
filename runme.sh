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
    read -p "Введите GITHUB_TOKEN (https://github.com/settings/tokens): " github_token
    if [ -n "$github_token" ]; then
    # Заменить значение GITHUB_TOKEN в файле config.json
    sed -i "s/\"GITHUB_TOKEN\": \".*\"/\"GITHUB_TOKEN\": \"$github_token\"/" config.json
    echo "start it up ..."
    python chain_reg_browser.py
    else
        echo "Пустое значение GITHUB_TOKEN. Обновление не выполнено."
    fi
    else
    echo "Installation canceled, no worries, dude."
fi
