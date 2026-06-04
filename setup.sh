#!/bin/bash

# Facebook CLI Setup Script for Termux
# Simple setup for Facebook CLI tool

echo "=========================================="
echo "Facebook CLI - Termux Setup"
echo "=========================================="

# Step 1: Update packages
echo ""
echo "[*] Updating packages..."
pkg update -y
pkg upgrade -y

# Step 2: Install required packages
echo ""
echo "[*] Installing required packages..."
pkg install -y python3
pkg install -y git
pkg install -y curl

# Step 3: Install Python dependencies
echo ""
echo "[*] Installing Python libraries..."
pip install --upgrade pip
pip install -r requirements.txt

# Step 4: Set permissions
echo ""
echo "[*] Setting file permissions..."
chmod +x facebook_cli.py

echo ""
echo "=========================================="
echo "[+] Setup complete!"
echo ""
echo "To run the program:"
echo "    python3 facebook_cli.py"
echo ""
echo "For more information, read README.md"
echo "=========================================="

